"""Controller regressions: state fixtures are not assessment-release evidence."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.controller import PipelineController, PipelineError

ROOT = Path(__file__).resolve().parents[1]
READY = {"status": "READY", "open_barrier_count": 0, "barriers": []}


class ProjectContextRuntimeTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.run = Path(tmp.name)
        self.ctl = PipelineController(ROOT, self.run)

    def test_zero_barriers_cannot_release_without_evidence(self):
        self.ctl.state["completed_stages"] = self.ctl.stage_ids[:-1]
        with self.assertRaisesRegex(PipelineError, "release evidence"):
            self.ctl.record("07-release-qa", READY)
        self.assertIsNone(self.ctl.state["release_status"])

    def test_resuming_legacy_ready_cannot_reuse_unsupported_claim(self):
        self.ctl.state.update(completed_stages=self.ctl.stage_ids[:], release_status="READY")
        self.ctl._save_state()
        with self.assertRaisesRegex(PipelineError, "release evidence"):
            PipelineController(ROOT, self.run)

    def issue(self, owner, identifier="FIX1"):
        return {"id": identifier, "owner": owner, "category": "mathematical_error",
                "description": "Incorrect calculation", "required_fix": "Correct and revalidate"}

    def seed_repair(self, issues):
        self.ctl.state["completed_stages"] = self.ctl.stage_ids[:-1]
        self.ctl.state["artifacts"] = {s: f"artifacts/{s}.json" for s in self.ctl.stage_ids[:-1]}
        self.ctl.state["open_issues"] = issues
        self.ctl.state["blocked_gate"] = "content"
        self.ctl._save_state()

    def test_q1_q6_repair_preserves_independent_q7_q8(self):
        self.seed_repair([self.issue("03-question-designer")])
        # Isolate dependency invalidation from question/schema validation.
        with patch.object(self.ctl, "validate_stage_payload"), patch.object(self.ctl, "_validate_against_blueprint"):
            self.ctl.repair("FIX1", {"questions": []})
        self.assertIn("04-complex-problem-specialist", self.ctl.state["completed_stages"])
        self.assertIn("04-complex-problem-specialist", self.ctl.state["artifacts"])
        self.assertEqual("05-maths-pedagogy-validator", self.ctl.expected_stage)

    def test_repair_keeps_unresolved_sibling_barrier(self):
        other = self.issue("04-complex-problem-specialist", "FIX2")
        self.seed_repair([self.issue("03-question-designer"), other])
        with patch.object(self.ctl, "validate_stage_payload"), patch.object(self.ctl, "_validate_against_blueprint"):
            self.ctl.repair("FIX1", {"questions": []})
        self.assertIn(other, self.ctl.state["open_issues"])

    def test_invalid_repair_preserves_existing_state(self):
        self.seed_repair([self.issue("03-question-designer")])
        previous = copy.deepcopy(self.ctl.state)
        previous_bytes = self.ctl.state_path.read_bytes()
        with patch.object(self.ctl, "validate_stage_payload", side_effect=PipelineError("invalid replacement")):
            with self.assertRaises(PipelineError):
                self.ctl.repair("FIX1", {})
        self.assertEqual(previous, self.ctl.state)
        self.assertEqual(previous_bytes, self.ctl.state_path.read_bytes())

    def test_pending_issue_blocks_new_ready_declaration(self):
        self.ctl.state["completed_stages"] = self.ctl.stage_ids[:-1]
        self.ctl.state["open_issues"] = [self.issue("04-complex-problem-specialist")]
        with self.assertRaises(PipelineError):
            self.ctl.record("07-release-qa", READY)


if __name__ == "__main__":
    unittest.main()
