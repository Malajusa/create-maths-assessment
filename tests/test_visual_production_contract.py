import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class VisualProductionContractTests(unittest.TestCase):
    def test_default_visual_profile_is_strict_and_visual_only(self):
        profile = json.loads((ROOT / "assets/visual-profiles/classic-assessment-v1.json").read_text())
        schema = json.loads((ROOT / "schemas/visual-profile.schema.json").read_text())
        errors = list(Draft202012Validator(schema).iter_errors(profile))
        self.assertEqual([], errors)
        self.assertEqual("visual_only", profile["source_role"])
        self.assertGreaterEqual(profile["typography"]["student_body"]["target_min_pt"], 11.25)
        self.assertGreaterEqual(profile["typography"]["assessment_title"]["target_min_pt"], 20)

    def test_build_manifest_requires_design_manifest(self):
        schema = json.loads((ROOT / "schemas/build-manifest.schema.json").read_text())
        self.assertIn("design_manifest", schema["required"])

    def test_builder_and_qa_use_design_manifest(self):
        builder = (ROOT / "agents/06-document-builder.md").read_text()
        qa = (ROOT / "agents/07-release-qa.md").read_text()
        self.assertIn("design_manifest", builder)
        self.assertIn("design_manifest", qa)
        self.assertIn("page balance", qa)

    def test_complex_problem_agents_use_simplest_route_challenge(self):
        specialist = (ROOT / "agents/04-complex-problem-specialist.md").read_text()
        validator = (ROOT / "agents/05-maths-pedagogy-validator.md").read_text()
        self.assertIn("simplest-valid-solution", specialist)
        self.assertIn("simplest-valid-solution", validator)


if __name__ == "__main__":
    unittest.main()
