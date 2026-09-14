import json
import tempfile
import unittest
from pathlib import Path

from runtime.controller import PipelineController, PipelineError

ROOT = Path(__file__).resolve().parents[1]


def blueprint_question(qid, marks, distribution=None):
    question = {
        "id": qid,
        "marks": marks,
        "primary_skill": "fixture",
        "evidence": "fixture evidence",
        "target_level": "fixture",
        "response_form": "written",
    }
    if distribution is not None:
        question["band_distribution"] = distribution
    return question


def canonical_v4_blueprint():
    return {
        "evidence_model": "criterion_component_estimate_v1",
        "total_marks": 25,
        "evidence_envelope": {"D": 5, "C": 8, "B": 5, "A": 7},
        "indicative_bands": {"E": [0, 4], "D": [5, 9], "C": [10, 15], "B": [16, 20], "A": [21, 25]},
        "questions": [
            blueprint_question("Q1", 1, {"D": 1}),
            blueprint_question("Q2", 1, {"D": 1}),
            blueprint_question("Q3", 1, {"D": 1}),
            blueprint_question("Q4", 2, {"D": 2}),
            blueprint_question("Q5", 4, {"C": 4}),
            blueprint_question("Q6", 5, {"C": 4, "B": 1}),
            blueprint_question("Q7", 5, {"B": 4, "A": 1}),
            blueprint_question("Q8", 6, {"A": 6}),
        ],
    }


def legacy_blueprint():
    marks = [1, 1, 2, 2, 3, 3, 4, 4]
    return {
        "total_marks": 20,
        "questions": [
            blueprint_question(f"Q{index}", mark)
            for index, mark in enumerate(marks, start=1)
        ],
    }


def generated_question(qid, marks, bands):
    marking = []
    for index, band in enumerate(bands, start=1):
        item = {
            "mark": index,
            "evidence": f"{qid} mark {index}",
            "evidence_band": band,
            "band_rationale": f"{band} fixture evidence",
            "why_not_lower_band": "Fixture distinction",
        }
        if band == "A":
            item["a_demand_feature"] = "inference"
        marking.append(item)
    return {"id": qid, "marks": marks, "marking": marking}


class V4ControllerBandBindingTests(unittest.TestCase):
    def make_controller(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return PipelineController(ROOT, Path(tmp.name))

    def make_controller_with_blueprint(self):
        ctl = self.make_controller()
        blueprint = canonical_v4_blueprint()
        path = ctl.run_dir / "blueprint.json"
        path.write_text(json.dumps(blueprint), encoding="utf-8")
        ctl.state["artifacts"]["02-assessment-blueprint"] = "blueprint.json"
        return ctl

    def test_new_years_3_to_10_brief_cannot_fall_back_to_legacy_blueprint(self):
        ctl = self.make_controller()
        ctl.record("01-orchestrator-curriculum-resolver", {
            "year_levels": [6],
            "topic": "volume and capacity",
            "jurisdiction": "Western Australia",
            "outputs": ["student_test_pptx", "marking_key_pptx", "curriculum_rationale_pdf"],
            "task_type": "new",
            "user_overrides": [],
        })
        with self.assertRaisesRegex(PipelineError, "require criterion_component_estimate_v1"):
            ctl.record("02-assessment-blueprint", legacy_blueprint())

    def test_typed_v4_brief_accepts_canonical_v4_blueprint(self):
        ctl = self.make_controller()
        ctl.record("01-orchestrator-curriculum-resolver", {
            "year_levels": [6],
            "topic": "volume and capacity",
            "jurisdiction": "Western Australia",
            "outputs": ["student_test_pptx", "marking_key_pptx", "curriculum_rationale_pdf"],
            "task_type": "new",
            "architecture_mode": "criterion_component_estimate_v1",
            "user_overrides": [],
        })
        ctl.record("02-assessment-blueprint", canonical_v4_blueprint())
        self.assertEqual("03-question-designer", ctl.expected_stage)

    def test_explicit_user_architecture_override_can_preserve_an_alternate_new_structure(self):
        ctl = self.make_controller()
        ctl.record("01-orchestrator-curriculum-resolver", {
            "year_levels": [6],
            "topic": "volume and capacity",
            "jurisdiction": "Western Australia",
            "outputs": ["student_test_pptx", "marking_key_pptx", "curriculum_rationale_pdf"],
            "task_type": "new",
            "architecture_mode": "explicit_user_override",
            "user_overrides": ["Use the requested 20-mark architecture for this assessment."],
        })
        ctl.record("02-assessment-blueprint", legacy_blueprint())
        self.assertEqual("03-question-designer", ctl.expected_stage)

    def test_explicit_user_architecture_override_requires_actual_user_override(self):
        ctl = self.make_controller()
        ctl.record("01-orchestrator-curriculum-resolver", {
            "year_levels": [6],
            "topic": "volume and capacity",
            "jurisdiction": "Western Australia",
            "outputs": ["student_test_pptx", "marking_key_pptx", "curriculum_rationale_pdf"],
            "task_type": "new",
            "architecture_mode": "explicit_user_override",
            "user_overrides": [],
        })
        with self.assertRaisesRegex(PipelineError, "requires a recorded user override"):
            ctl.record("02-assessment-blueprint", legacy_blueprint())

    def test_matching_q1_q6_band_distribution_passes(self):
        ctl = self.make_controller_with_blueprint()
        payload = {
            "questions": [
                generated_question("Q1", 1, ["D"]),
                generated_question("Q2", 1, ["D"]),
                generated_question("Q3", 1, ["D"]),
                generated_question("Q4", 2, ["D", "D"]),
                generated_question("Q5", 4, ["C", "C", "C", "C"]),
                generated_question("Q6", 5, ["C", "C", "C", "C", "B"]),
            ]
        }
        ctl._validate_against_blueprint("03-question-designer", payload)

    def test_mismatched_band_distribution_is_rejected(self):
        ctl = self.make_controller_with_blueprint()
        payload = {
            "questions": [
                generated_question("Q7", 5, ["B", "B", "B", "B", "B"]),
                generated_question("Q8", 6, ["A", "A", "A", "A", "A", "A"]),
            ]
        }
        with self.assertRaisesRegex(PipelineError, "band distribution does not match"):
            ctl._validate_against_blueprint("04-complex-problem-specialist", payload)


if __name__ == "__main__":
    unittest.main()
