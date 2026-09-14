import json
import tempfile
import unittest
from pathlib import Path

from runtime.controller import PipelineController, PipelineError

ROOT = Path(__file__).resolve().parents[1]


def blueprint_question(qid, marks, distribution):
    return {
        "id": qid,
        "marks": marks,
        "primary_skill": "fixture",
        "evidence": "fixture evidence",
        "target_level": "fixture",
        "response_form": "written",
        "band_distribution": distribution,
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
    def make_controller_with_blueprint(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ctl = PipelineController(ROOT, Path(tmp.name))
        blueprint = {
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
        path = ctl.run_dir / "blueprint.json"
        path.write_text(json.dumps(blueprint), encoding="utf-8")
        ctl.state["artifacts"]["02-assessment-blueprint"] = "blueprint.json"
        return ctl

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
