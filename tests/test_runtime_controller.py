import json
import tempfile
import unittest
from pathlib import Path

from runtime.controller import PipelineController, PipelineError

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text())


class RuntimeControllerTests(unittest.TestCase):
    def make_controller(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return PipelineController(ROOT, Path(tmp.name))

    def test_cannot_skip_content_validation(self):
        ctl = self.make_controller()
        ctl.record("01-orchestrator-curriculum-resolver", load("fixtures/gold/minimal-run/01-brief.json"))
        ctl.record("02-assessment-blueprint", load("fixtures/gold/minimal-run/02-blueprint.json"))
        ctl.record("03-question-designer", load("fixtures/gold/minimal-run/03-q1-q6.json"))
        ctl.record("04-complex-problem-specialist", load("fixtures/gold/minimal-run/04-q7-q8.json"))
        with self.assertRaisesRegex(PipelineError, "expected stage 05-maths-pedagogy-validator"):
            ctl.record("06-document-builder", load("fixtures/gold/minimal-run/06-build.json"))

    def test_invalid_schema_is_rejected(self):
        ctl = self.make_controller()
        bad = load("fixtures/gold/minimal-run/01-brief.json")
        del bad["topic"]
        with self.assertRaisesRegex(PipelineError, "schema validation failed"):
            ctl.record("01-orchestrator-curriculum-resolver", bad)

    def test_content_fail_blocks_document_builder(self):
        ctl = self.make_controller()
        for stage, file in [
            ("01-orchestrator-curriculum-resolver", "01-brief.json"),
            ("02-assessment-blueprint", "02-blueprint.json"),
            ("03-question-designer", "03-q1-q6.json"),
            ("04-complex-problem-specialist", "04-q7-q8.json"),
        ]:
            ctl.record(stage, load(f"fixtures/gold/minimal-run/{file}"))
        ctl.record("05-maths-pedagogy-validator", {
            "status": "FAIL",
            "issues": [{
                "id": "M1", "owner": "03-question-designer", "question": "Q3",
                "category": "mathematical_error", "description": "Wrong answer",
                "required_fix": "Correct and revalidate"
            }]
        })
        with self.assertRaisesRegex(PipelineError, "content gate is blocked"):
            ctl.record("06-document-builder", load("fixtures/gold/minimal-run/06-build.json"))

    def test_q8_cannot_depend_on_q7(self):
        ctl = self.make_controller()
        bad = load("fixtures/failures/q8-dependency/04-q7-q8.json")
        with self.assertRaisesRegex(PipelineError, "Q8 must be independent of Q7"):
            ctl.validate_stage_payload("04-complex-problem-specialist", bad)

    def test_ready_with_open_barrier_is_rejected(self):
        ctl = self.make_controller()
        bad = load("fixtures/failures/ready-with-barrier/07-release.json")
        with self.assertRaisesRegex(PipelineError, "READY requires zero open barriers"):
            ctl.validate_stage_payload("07-release-qa", bad)

    def test_marking_key_must_derive_from_final_test_hash(self):
        ctl = self.make_controller()
        bad = load("fixtures/failures/key-provenance/06-build.json")
        with self.assertRaisesRegex(PipelineError, "marking key source hash must equal student test hash"):
            ctl.validate_stage_payload("06-document-builder", bad)

    def test_release_failure_can_route_repair_and_invalidate_release_qa(self):
        ctl = self.make_controller()
        for stage, file in [
            ("01-orchestrator-curriculum-resolver", "01-brief.json"),
            ("02-assessment-blueprint", "02-blueprint.json"),
            ("03-question-designer", "03-q1-q6.json"),
            ("04-complex-problem-specialist", "04-q7-q8.json"),
            ("05-maths-pedagogy-validator", "05-validation.json"),
            ("06-document-builder", "06-build.json"),
        ]:
            ctl.record(stage, load(f"fixtures/gold/minimal-run/{file}"))
        ctl.record("07-release-qa", {
            "status": "NOT READY",
            "open_barrier_count": 1,
            "barriers": [{
                "id": "V1", "owner": "06-document-builder", "question": None,
                "category": "visual", "description": "Label overlap",
                "required_fix": "Correct layout and re-render"
            }]
        })
        ctl.repair("V1", load("fixtures/gold/minimal-run/06-build.json"))
        self.assertEqual("07-release-qa", ctl.expected_stage)
        self.assertEqual("06-document-builder", ctl.state["completed_stages"][-1])
        self.assertEqual(1, ctl.state["repair_counts"]["V1"])

    def test_valid_fixture_can_reach_ready(self):
        ctl = self.make_controller()
        sequence = [
            ("01-orchestrator-curriculum-resolver", "01-brief.json"),
            ("02-assessment-blueprint", "02-blueprint.json"),
            ("03-question-designer", "03-q1-q6.json"),
            ("04-complex-problem-specialist", "04-q7-q8.json"),
            ("05-maths-pedagogy-validator", "05-validation.json"),
            ("06-document-builder", "06-build.json"),
            ("07-release-qa", "07-release.json"),
        ]
        for stage, file in sequence:
            ctl.record(stage, load(f"fixtures/gold/minimal-run/{file}"))
        self.assertEqual("READY", ctl.state["release_status"])
        self.assertEqual(sequence[-1][0], ctl.state["completed_stages"][-1])


if __name__ == "__main__":
    unittest.main()
