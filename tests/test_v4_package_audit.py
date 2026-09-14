import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_auditor():
    path = SCRIPTS / "audit_assessment_package_v4.py"
    spec = importlib.util.spec_from_file_location("audit_v4", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class V4PackageAuditTests(unittest.TestCase):
    def test_question_mark_counts_come_from_spec_not_legacy_constant(self):
        auditor = load_auditor()
        spec = {
            "evidence_model": "criterion_component_estimate_v1",
            "questions": [
                {"id": "q1", "marks": 1},
                {"id": "q2", "marks": 1},
                {"id": "q3", "marks": 1},
                {"id": "q4", "marks": 2},
                {"id": "q5", "marks": 4},
                {"id": "q6", "marks": 5},
                {"id": "q7", "marks": 5},
                {"id": "q8", "marks": 6},
            ],
        }
        self.assertEqual(
            {"q1": 1, "q2": 1, "q3": 1, "q4": 2, "q5": 4, "q6": 5, "q7": 5, "q8": 6},
            auditor._expected_marks_for_spec(spec),
        )

    def test_v4_teacher_output_text_passes_when_complete(self):
        auditor = load_auditor()
        issues = []
        auditor._audit_v4_teacher_text(
            student_text="Year 6 assessment questions only.",
            key_text="Indicative standard on this assessed component: E 0–4 D 5–9 C 10–15 B 16–20 A 21–25.",
            rationale_text=(
                "Evidence envelope 5D / 8C / 5B / 7A. "
                "C requires 5 C-or-higher marks, B requires 3 B-or-higher marks, and A requires 3 A marks. "
                "This is an indicative standard on the assessed component, not the student's reporting grade."
            ),
            issues=issues,
        )
        self.assertEqual([], issues)

    def test_v4_teacher_output_rejects_missing_score_table_and_scope_warning(self):
        auditor = load_auditor()
        issues = []
        auditor._audit_v4_teacher_text(
            student_text="Year 6 assessment.",
            key_text="Marking key only.",
            rationale_text="5D / 8C / 5B / 7A.",
            issues=issues,
        )
        codes = {issue["code"] for issue in issues}
        self.assertIn("E_INDICATIVE_BANDS_OUTPUT", codes)
        self.assertIn("E_COMPONENT_SCOPE_OUTPUT", codes)
        self.assertIn("E_BOUNDARY_PROOF_OUTPUT", codes)

    def test_student_test_rejects_teacher_only_evidence_metadata(self):
        auditor = load_auditor()
        issues = []
        auditor._audit_v4_teacher_text(
            student_text="Evidence band: B. Band rationale: transfer.",
            key_text="Indicative standard on this assessed component: E 0-4 D 5-9 C 10-15 B 16-20 A 21-25.",
            rationale_text=(
                "5D / 8C / 5B / 7A; 5 C-or-higher, 3 B-or-higher, 3 A marks; "
                "indicative standard on the assessed component, not the reporting grade."
            ),
            issues=issues,
        )
        self.assertIn("E_STUDENT_BAND_METADATA", {issue["code"] for issue in issues})


if __name__ == "__main__":
    unittest.main()
