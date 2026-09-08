import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def test_pipeline_has_seven_separate_agents(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        ids = [stage["id"] for stage in pipeline["stages"]]
        self.assertEqual(7, len(ids))
        self.assertEqual(7, len(set(ids)))

    def test_generators_cannot_certify(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        by_id = {stage["id"]: stage for stage in pipeline["stages"]}
        self.assertFalse(by_id["03-question-designer"]["certifies"])
        self.assertFalse(by_id["04-complex-problem-specialist"]["certifies"])
        self.assertTrue(by_id["05-maths-pedagogy-validator"]["certifies"])
        self.assertTrue(by_id["07-release-qa"]["certifies"])

    def test_content_validator_has_full_context_and_emits_approved_set(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        by_id = {stage["id"]: stage for stage in pipeline["stages"]}
        validator = by_id["05-maths-pedagogy-validator"]
        self.assertEqual(
            ["assessment_brief", "assessment_blueprint", "q1_q6", "q7_q8"],
            validator["consumes"],
        )
        self.assertEqual(
            ["content_validation", "approved_question_set"],
            validator["produces"],
        )

    def test_document_builder_uses_only_approved_question_content(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        by_id = {stage["id"]: stage for stage in pipeline["stages"]}
        consumes = by_id["06-document-builder"]["consumes"]
        self.assertIn("approved_question_set", consumes)
        self.assertNotIn("q1_q6", consumes)
        self.assertNotIn("q7_q8", consumes)
        self.assertNotIn("content_validation", consumes)

    def test_release_qa_can_verify_original_intent_and_validated_content(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        by_id = {stage["id"]: stage for stage in pipeline["stages"]}
        consumes = by_id["07-release-qa"]["consumes"]
        for artifact in ("assessment_brief", "assessment_blueprint", "approved_question_set"):
            self.assertIn(artifact, consumes)

    def test_approved_question_set_schema_is_pass_only_and_complete(self):
        schema = json.loads((ROOT / "schemas/approved-question-set.schema.json").read_text())
        self.assertEqual("PASS", schema["properties"]["status"]["const"])
        questions = schema["properties"]["questions"]
        self.assertEqual(8, questions["minItems"])
        self.assertEqual(8, questions["maxItems"])
        required_ids = {
            rule["contains"]["properties"]["id"]["const"]
            for rule in questions["allOf"]
        }
        self.assertEqual({f"Q{i}" for i in range(1, 9)}, required_ids)

    def test_release_gate_is_binary(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        self.assertEqual("READY", pipeline["release_gate"]["pass_status"])
        self.assertEqual("NOT READY", pipeline["release_gate"]["fail_status"])
        self.assertEqual("open_barrier_count == 0", pipeline["release_gate"]["pass_condition"])

    def test_q7_q8_independence_is_canonical(self):
        skill = (ROOT / "SKILL.md").read_text()
        contract = (ROOT / "standards/assessment-contract.md").read_text()
        self.assertIn("Q7 and Q8 are independent", skill)
        self.assertIn("Q7 and Q8 are independent", contract)

    def test_marking_key_uses_final_test_as_source_of_truth(self):
        builder = (ROOT / "agents/06-document-builder.md").read_text()
        self.assertIn("source of truth", builder)
        self.assertIn("duplicating the final test", builder)

    def test_all_required_defects_are_barriers(self):
        qa = (ROOT / "standards/qa-barriers.md").read_text()
        self.assertIn("Every required defect is a barrier", qa)
        self.assertIn("Any failed item means `NOT READY`", qa)

    def test_targeted_repair_limit_is_three(self):
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        self.assertEqual(3, pipeline["max_targeted_repairs_per_barrier"])
        self.assertEqual("replace_approach", pipeline["after_max_repairs"])

if __name__ == "__main__":
    unittest.main()

class V31RepositoryTests(unittest.TestCase):
    def test_runtime_controller_and_fixture_runner_exist(self):
        self.assertTrue((ROOT / "runtime/controller.py").exists())
        self.assertTrue((ROOT / "scripts/run_regression_fixtures.py").exists())

    def test_ci_workflow_runs_full_validation(self):
        workflow = (ROOT / ".github/workflows/validate-skill.yml").read_text()
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python scripts/validate_repository.py", workflow)
        self.assertIn("python scripts/run_regression_fixtures.py", workflow)

    def test_version_matches_pipeline(self):
        version = (ROOT / "VERSION").read_text().strip()
        pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
        self.assertEqual(version, pipeline["version"])
        self.assertEqual("3.2.0", version)
