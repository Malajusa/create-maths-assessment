import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class V4CanonicalReferenceTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_assessment_contract_uses_25_mark_envelope(self):
        text = self.text("standards/assessment-contract.md")
        for token in ("25-mark", "1, 1, 1, 2, 4, 5, 5, 6", "5D / 8C / 5B / 7A", "indicative"):
            self.assertIn(token, text)
        self.assertIn("Q7 and Q8 are independent", text)

    def test_project_context_records_v4_without_erasing_history(self):
        text = self.text("standards/project-context.md")
        self.assertIn("14 September 2026", text)
        self.assertIn("5D / 8C / 5B / 7A", text)
        self.assertIn("25-mark", text)
        self.assertIn("legacy", text.casefold())
        self.assertIn("component", text.casefold())

    def test_quality_gates_use_v4_design_matrix_and_band_checks(self):
        text = self.text("references/assessment-quality-gates.md")
        for token in ("Q3 | 1", "Q5 | 4", "Q6 | 5", "Q7 | 5", "Q8 | 6"):
            self.assertIn(token, text)
        for token in ("evidence_band", "band_rationale", "why_not_lower_band", "5D / 8C / 5B / 7A"):
            self.assertIn(token, text)
        self.assertNotIn("four distinct marks for Q7 and Q8", text)

    def test_production_contract_requires_v4_evidence_model_when_applicable(self):
        text = self.text("references/assessment-production-contract.md")
        for token in (
            "criterion_component_estimate_v1",
            "5D / 8C / 5B / 7A",
            "evidence_band",
            "band_rationale",
            "why_not_lower_band",
            "indicative standard",
            "reporting grade",
        ):
            self.assertIn(token, text)

    def test_q7_q8_standard_no_longer_assumes_four_marks_each(self):
        text = self.text("references/q7-q8-problem-solving-standard.md")
        self.assertIn("Q7", text)
        self.assertIn("five marks", text.casefold())
        self.assertIn("Q8", text)
        self.assertIn("six marks", text.casefold())
        self.assertIn("individual mark", text.casefold())
        self.assertNotIn("Allocate four marks", text)
        self.assertNotIn("four pieces of meaningful mathematical evidence", text)

    def test_judging_standard_calibration_is_secondary_to_v4_current_curriculum_model(self):
        text = self.text("references/judging-standards-calibration.md")
        self.assertIn("evidence-band-standard.md", text)
        self.assertIn("current curriculum", text.casefold())
        self.assertIn("indicative", text.casefold())
        self.assertIn("reporting grade", text.casefold())


if __name__ == "__main__":
    unittest.main()
