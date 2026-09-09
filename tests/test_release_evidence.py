"""Evidence-gate unit tests, not real assessment or model-review acceptance tests.

The subprocess auditor is an explicit test double so these tests isolate evidence
validation and command/report wiring. Production uses the repository's real audit.
"""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image

from runtime.release_evidence import ReleaseEvidenceError, verify_release


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReleaseEvidenceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.repo = self.root / "repo"
        self.run = self.root / "run"
        (self.repo / "scripts").mkdir(parents=True)
        (self.run / "artifacts").mkdir(parents=True)
        self.script = self.repo / "scripts/audit_assessment_package.py"
        self.script.write_text('import json,sys\nfrom pathlib import Path\n'
            'p=Path(sys.argv[sys.argv.index("--report")+1])\n'
            'p.write_text(json.dumps({"status":"READY","issues":[]}))\n')
        self.build = {}
        for role, suffix in [("student_test", ".pptx"), ("marking_key", ".pptx"), ("curriculum_rationale", ".pdf")]:
            # Deliberately not assessment documents: the audit double is explicit.
            path = self.run / (role + suffix)
            path.write_bytes(("synthetic unit-test output: " + role).encode())
            self.build[role] = self.ref(path)
        self.build["design_manifest"] = {"synthetic_test": True}
        self.spec = self.json_file("spec.json", {"package": {
            "test_slide_count": 1, "key_slide_count": 1, "rationale_page_count": 1}})
        self.ledger = self.json_file("ledger.json", {"synthetic_test": True})
        self.design = self.json_file("design.json", self.build["design_manifest"])
        self.content = self.json_file("content.json", {"synthetic_test": True})
        self.build_path = self.json_file("build.json", self.build)
        log = self.run / "review-record.txt"
        log.write_text("Synthetic reviewer execution record; not independent model QA.\n")
        self.review = {
            "status": "PASS", "review_mode": "independent_reviewer",
            "generator_execution_id": "test-generator", "reviewer_execution_id": "test-reviewer",
            "assessment_spec_sha256": digest(self.spec),
            "content_validation_sha256": digest(self.content),
            "build_manifest_sha256": digest(self.build_path),
            "review_record": self.ref(log), "pages": []}
        for role in self.build:
            if role == "design_manifest":
                continue
            image = self.run / (role + ".png")
            Image.new("RGB", (1240, 1754), "white").save(image)
            self.review["pages"].append({
                "artifact": role, "page": 1, "source_sha256": self.build[role]["sha256"],
                "image": self.ref(image), "inspection": "full_resolution_and_print_scale",
                "findings": [], "evidence_inspected": "Synthetic page inspection for gate wiring only."})
        self.review_path = self.json_file("review.json", self.review)
        self.evidence = {"assessment_spec": self.ref(self.spec), "qa_ledger": self.ref(self.ledger),
                         "design_manifest": self.ref(self.design), "render_review": self.ref(self.review_path)}

    def ref(self, path):
        return {"path": str(path.relative_to(self.run)), "sha256": digest(path)}

    def json_file(self, name, value):
        path = self.run / name
        path.write_text(json.dumps(value))
        return path

    def save_review(self):
        self.review_path.write_text(json.dumps(self.review))
        self.evidence["render_review"] = self.ref(self.review_path)

    def verify(self):
        return verify_release(self.repo, self.run, self.build_path, self.content, self.evidence)

    def test_complete_unit_evidence_invokes_auditor_and_saves_report(self):
        result = self.verify()
        self.assertTrue((self.run / result["path"]).is_file())
        self.assertEqual(digest(self.run / result["path"]), result["sha256"])

    def test_missing_evidence_is_rejected(self):
        with self.assertRaises(ReleaseEvidenceError):
            verify_release(self.repo, self.run, self.build_path, self.content, {})

    def test_changed_output_is_rejected(self):
        (self.run / self.build["student_test"]["path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ReleaseEvidenceError, "hash"):
            self.verify()

    def test_missing_output_is_rejected(self):
        (self.run / self.build["marking_key"]["path"]).unlink()
        with self.assertRaises(ReleaseEvidenceError):
            self.verify()

    def test_path_escape_is_rejected(self):
        outside = self.root / "outside.json"
        outside.write_text("{}")
        self.evidence["qa_ledger"] = {"path": "../outside.json", "sha256": digest(outside)}
        with self.assertRaisesRegex(ReleaseEvidenceError, "run directory"):
            self.verify()

    def test_self_review_is_rejected(self):
        self.review["reviewer_execution_id"] = self.review["generator_execution_id"]
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "independent"):
            self.verify()

    def test_fresh_self_review_is_not_independent(self):
        self.review["review_mode"] = "fresh_artifact_only"
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "independent"):
            self.verify()

    def test_missing_page_is_rejected(self):
        self.review["pages"].pop()
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "page"):
            self.verify()

    def test_duplicate_page_is_rejected(self):
        self.review["pages"].append(copy.deepcopy(self.review["pages"][0]))
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "page"):
            self.verify()

    def test_thumbnail_is_rejected(self):
        image = self.run / "student_test.png"
        Image.new("RGB", (200, 300)).save(image)
        self.review["pages"][0]["image"] = self.ref(image)
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "resolution"):
            self.verify()

    def test_stale_render_source_is_rejected(self):
        self.review["pages"][0]["source_sha256"] = "0" * 64
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "source"):
            self.verify()

    def test_visual_findings_cannot_be_ignored(self):
        self.review["pages"][0]["findings"] = ["overlapping mark label"]
        self.save_review()
        with self.assertRaises(ReleaseEvidenceError):
            self.verify()

    def test_stale_content_review_is_rejected(self):
        self.content.write_text('{"changed":true}')
        with self.assertRaisesRegex(ReleaseEvidenceError, "stale"):
            self.verify()

    def test_audit_failure_is_rejected(self):
        self.script.write_text('import sys\nsys.exit(1)\n')
        with self.assertRaisesRegex(ReleaseEvidenceError, "audit"):
            self.verify()

    def test_missing_report_is_rejected_even_with_zero_exit(self):
        self.script.write_text('print("READY")\n')
        with self.assertRaisesRegex(ReleaseEvidenceError, "audit"):
            self.verify()

    def test_report_with_hidden_issues_is_rejected(self):
        self.script.write_text('import json,sys\nfrom pathlib import Path\n'
            'p=Path(sys.argv[sys.argv.index("--report")+1])\n'
            'p.write_text(json.dumps({"status":"READY","issues":[{"code":"defect"}]}))\n')
        with self.assertRaisesRegex(ReleaseEvidenceError, "audit"):
            self.verify()

    def test_reserved_audit_destination_cannot_be_an_input(self):
        reserved = self.run / "artifacts/package-audit.json"
        reserved.write_bytes(self.ledger.read_bytes())
        self.evidence["qa_ledger"] = self.ref(reserved)
        with self.assertRaisesRegex(ReleaseEvidenceError, "reserved"):
            self.verify()

    def test_reviewer_record_cannot_reuse_an_evidence_file(self):
        self.review["review_record"] = self.ref(self.ledger)
        self.save_review()
        with self.assertRaisesRegex(ReleaseEvidenceError, "distinct"):
            self.verify()

    def test_mutation_during_audit_is_rejected(self):
        target = self.run / self.build["student_test"]["path"]
        self.script.write_text(self.script.read_text() + f'Path({str(target)!r}).write_bytes(b"changed during audit")\n')
        with self.assertRaisesRegex(ReleaseEvidenceError, "changed"):
            self.verify()


if __name__ == "__main__":
    unittest.main()
