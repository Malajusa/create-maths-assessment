import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class V4SkillRoutingTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_skill_entrypoint_uses_v4_evidence_reference_and_25_mark_default(self):
        skill = self.text("SKILL.md")
        self.assertIn("references/evidence-band-standard.md", skill)
        self.assertIn("25 marks", skill)
        self.assertIn("5D / 8C / 5B / 7A", skill)
        self.assertIn("0–4", skill)
        self.assertIn("21–25", skill)

    def test_assessment_format_explains_component_estimate_not_reporting_grade(self):
        text = self.text("references/assessment-format.md")
        self.assertIn("5D / 8C / 5B / 7A", text)
        self.assertIn("indicative", text.casefold())
        self.assertIn("assessed component", text.casefold())
        self.assertIn("reporting grade", text.casefold())

    def test_all_pipeline_agents_route_to_evidence_standard(self):
        agent_paths = [
            "agents/01-orchestrator-curriculum-resolver.md",
            "agents/02-assessment-blueprint.md",
            "agents/03-question-designer.md",
            "agents/04-complex-problem-specialist.md",
            "agents/05-maths-pedagogy-validator.md",
            "agents/06-document-builder.md",
            "agents/07-release-qa.md",
        ]
        for path in agent_paths:
            with self.subTest(path=path):
                self.assertIn("evidence-band-standard.md", self.text(path))

    def test_orchestrator_preserves_out_of_scope_and_legacy_structures(self):
        text = self.text("agents/01-orchestrator-curriculum-resolver.md").casefold()
        for token in ("years 3–10", "pre-primary", "wace", "key-only", "version b"):
            self.assertIn(token, text)

    def test_blueprint_anchors_c_before_other_bands(self):
        text = self.text("agents/02-assessment-blueprint.md").casefold()
        self.assertIn("c is the anchor", text)
        self.assertIn("5d / 8c / 5b / 7a", text)
        self.assertIn("band_distribution", text)

    def test_generators_classify_individual_marks_not_question_position(self):
        q16 = self.text("agents/03-question-designer.md").casefold()
        q78 = self.text("agents/04-complex-problem-specialist.md").casefold()
        self.assertIn("individual mark", q16)
        self.assertIn("question position", q16)
        self.assertIn("individual mark", q78)
        self.assertIn("routine", q78)
        self.assertIn("a_demand_feature", q78)

    def test_content_validator_rejects_band_inflation(self):
        text = self.text("agents/05-maths-pedagogy-validator.md").casefold()
        self.assertIn("band inflation", text)
        self.assertIn("why_not_lower_band", text)
        self.assertIn("5d / 8c / 5b / 7a", text)

    def test_builder_keeps_band_metadata_off_student_test(self):
        text = self.text("agents/06-document-builder.md").casefold()
        self.assertIn("student test", text)
        self.assertIn("must not display", text)
        self.assertIn("indicative", text)
        self.assertIn("marking key", text)
        self.assertIn("curriculum rationale", text)

    def test_release_qa_checks_component_estimate_outputs(self):
        text = self.text("agents/07-release-qa.md").casefold()
        self.assertIn("evidence envelope", text)
        self.assertIn("student test", text)
        self.assertIn("indicative", text)
        self.assertIn("reporting grade", text)


if __name__ == "__main__":
    unittest.main()
