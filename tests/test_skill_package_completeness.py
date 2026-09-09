import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageCompletenessTests(unittest.TestCase):
    def test_production_knowledge_is_packaged_with_runtime_pipeline(self):
        required = [
            "agents/openai.yaml",
            "references/assessment-format.md",
            "references/assessment-production-contract.md",
            "references/assessment-quality-gates.md",
            "references/curriculum-index.md",
            "references/curriculum-pre-primary.md",
            *[f"references/curriculum-year-{year}.md" for year in range(1, 11)],
            "references/mathematical-diagram-conventions.md",
            "standards/visual-standard.md",
            "references/contextual-illustration-standard.md",
            "references/powerpoint-output.md",
            "references/q7-q8-demand-2025.md",
            "references/q7-q8-problem-solving-standard.md",
            "assets/year-4-5-ordering-comparing-fractions-quality-exemplar.pptx",
            "assets/year-6-transformations-quality-benchmark.pptx",
            "examples/benchmarks/regression-cases.json",
            "scripts/audit_assessment_package.py",
            "scripts/test_assessment_workflow.py",
            "scripts/validate_assessment_spec.py",
            "scripts/validate_visual_assets.py",
            "schemas/visual-spec.schema.json",
            "schemas/visual-asset-manifest.schema.json",
            "assets/maths-visuals/v1/manifest.json",
        ]

        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing, f"Missing production skill resources: {missing}")

    def test_skill_entrypoint_routes_to_runtime_and_task_specific_references(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        required_links = [
            "orchestration/pipeline.json",
            "runtime/controller.py",
            "references/assessment-format.md",
            "references/assessment-quality-gates.md",
            "references/assessment-production-contract.md",
            "references/curriculum-index.md",
            "references/powerpoint-output.md",
            "references/mathematical-diagram-conventions.md",
            "references/q7-q8-problem-solving-standard.md",
            "references/q7-q8-demand-2025.md",
        ]

        for link in required_links:
            with self.subTest(link=link):
                self.assertIn(link, skill)

    def test_version_is_bumped_for_combined_distribution(self):
        self.assertEqual("3.5.0", (ROOT / "VERSION").read_text(encoding="utf-8").strip())

    def test_each_stage_routes_to_its_required_production_reference(self):
        routes = {
            "agents/01-orchestrator-curriculum-resolver.md": "references/curriculum-index.md",
            "agents/02-assessment-blueprint.md": "references/assessment-format.md",
            "agents/03-question-designer.md": "references/mathematical-diagram-conventions.md",
            "agents/04-complex-problem-specialist.md": "references/q7-q8-problem-solving-standard.md",
            "agents/05-maths-pedagogy-validator.md": "references/assessment-quality-gates.md",
            "agents/06-document-builder.md": "references/powerpoint-output.md",
            "agents/07-release-qa.md": "scripts/audit_assessment_package.py",
        }

        for agent_path, required_reference in routes.items():
            with self.subTest(agent=agent_path):
                agent = (ROOT / agent_path).read_text(encoding="utf-8")
                self.assertIn(required_reference, agent)


if __name__ == "__main__":
    unittest.main()
