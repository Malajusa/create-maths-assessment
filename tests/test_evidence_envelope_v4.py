import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_module(filename: str, module_name: str):
    path = SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_evidence_module():
    return load_module("evidence_envelope.py", "evidence_envelope_v4")


def load_validator_module():
    return load_module("validate_assessment_spec.py", "validate_assessment_spec_v4")


def make_v4_spec() -> dict:
    source = json.loads(
        (ROOT / "examples/benchmarks/year5-fractions-percentages-release-spec.json").read_text(encoding="utf-8")
    )
    candidate = copy.deepcopy(source)
    candidate["evidence_model"] = "criterion_component_estimate_v1"
    candidate["marks"]["total"] = 25
    candidate["marks"]["evidence_envelope"] = {"D": 5, "C": 8, "B": 5, "A": 7}
    candidate["marks"]["indicative_bands"] = {
        "E": [0, 4],
        "D": [5, 9],
        "C": [10, 15],
        "B": [16, 20],
        "A": [21, 25],
    }
    allocations = {
        "q1": ["D"],
        "q2": ["D"],
        "q3": ["D"],
        "q4": ["D", "D"],
        "q5": ["C", "C", "C", "C"],
        "q6": ["C", "C", "C", "C", "B"],
        "q7": ["B", "B", "B", "B", "A"],
        "q8": ["A", "A", "A", "A", "A", "A"],
    }
    topic_subtotals: dict[str, int] = {}
    for question in candidate["questions"]:
        qid = question["id"]
        bands = allocations[qid]
        question["marks"] = len(bands)
        mark_evidence = []
        for index, band in enumerate(bands, start=1):
            item = {
                "mark": index,
                "evidence": f"Observable {band}-band evidence for {qid} mark {index}.",
                "evidence_band": band,
                "band_rationale": f"This criterion is classified as {band} evidence.",
                "why_not_lower_band": "The observable evidence exceeds the next lower demand where one exists.",
            }
            if band == "A":
                item["a_demand_feature"] = "inference"
            mark_evidence.append(item)
        question["mark_evidence"] = mark_evidence
        topic_subtotals[question["topic"]] = topic_subtotals.get(question["topic"], 0) + len(bands)
    candidate["marks"]["topic_subtotals"] = topic_subtotals
    return candidate


class EvidenceEnvelopeV4ContractTests(unittest.TestCase):
    def test_default_question_marks_total_25(self):
        evidence = load_evidence_module()
        self.assertEqual(
            {"q1": 1, "q2": 1, "q3": 1, "q4": 2, "q5": 4, "q6": 5, "q7": 5, "q8": 6},
            evidence.DEFAULT_QUESTION_MARKS,
        )
        self.assertEqual(25, sum(evidence.DEFAULT_QUESTION_MARKS.values()))

    def test_default_evidence_envelope_and_cutoffs_are_canonical(self):
        evidence = load_evidence_module()
        self.assertEqual({"D": 5, "C": 8, "B": 5, "A": 7}, evidence.DEFAULT_EVIDENCE_ENVELOPE)
        self.assertEqual({"D": 5, "C": 10, "B": 16, "A": 21}, evidence.DEFAULT_INDICATIVE_CUTS)

    def test_structural_boundaries_force_target_standard_evidence(self):
        evidence = load_evidence_module()
        self.assertEqual(5, evidence.forced_target_evidence("C"))
        self.assertEqual(3, evidence.forced_target_evidence("B"))
        self.assertEqual(3, evidence.forced_target_evidence("A"))
        self.assertEqual([], evidence.validate_canonical_structure())

    def test_score_classification_uses_canonical_component_bands(self):
        evidence = load_evidence_module()
        cases = {0: "E", 4: "E", 5: "D", 9: "D", 10: "C", 15: "C", 16: "B", 20: "B", 21: "A", 25: "A"}
        for score, expected in cases.items():
            self.assertEqual(expected, evidence.classify_score(score))
        for invalid in (-1, 26, 3.5, True):
            with self.assertRaises(ValueError):
                evidence.classify_score(invalid)

    def test_normative_evidence_band_reference_exists(self):
        reference = ROOT / "references/evidence-band-standard.md"
        self.assertTrue(reference.exists())
        text = reference.read_text(encoding="utf-8")
        for token in ("5D / 8C / 5B / 7A", "0–4", "5–9", "10–15", "16–20", "21–25"):
            self.assertIn(token, text)

    def test_question_schema_requires_mark_level_band_metadata(self):
        schema = json.loads((ROOT / "schemas/question.schema.json").read_text(encoding="utf-8"))
        marking = schema["properties"]["marking"]
        item = marking["items"]
        self.assertEqual(["mark", "evidence", "evidence_band", "band_rationale", "why_not_lower_band"], item["required"])
        self.assertEqual(["D", "C", "B", "A"], item["properties"]["evidence_band"]["enum"])

    def test_blueprint_schema_carries_v4_evidence_contract(self):
        schema = json.loads((ROOT / "schemas/assessment-blueprint.schema.json").read_text(encoding="utf-8"))
        for field in ("evidence_model", "evidence_envelope", "indicative_bands"):
            self.assertIn(field, schema["properties"])
        question_properties = schema["properties"]["questions"]["items"]["properties"]
        self.assertIn("band_distribution", question_properties)

    def test_legacy_20_mark_spec_remains_valid_without_v4_model(self):
        validator = load_validator_module()
        legacy = json.loads(
            (ROOT / "examples/benchmarks/year5-fractions-percentages-release-spec.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validator.validate_spec(legacy))

    def test_canonical_v4_spec_is_valid(self):
        validator = load_validator_module()
        self.assertEqual([], validator.validate_spec(make_v4_spec()))

    def test_v4_rejects_wrong_envelope(self):
        validator = load_validator_module()
        candidate = make_v4_spec()
        candidate["marks"]["evidence_envelope"] = {"D": 6, "C": 7, "B": 5, "A": 7}
        codes = {item["code"] for item in validator.validate_spec(candidate)}
        self.assertIn("E_EVIDENCE_ENVELOPE", codes)

    def test_v4_rejects_wrong_indicative_bands(self):
        validator = load_validator_module()
        candidate = make_v4_spec()
        candidate["marks"]["indicative_bands"]["A"] = [20, 25]
        codes = {item["code"] for item in validator.validate_spec(candidate)}
        self.assertIn("E_INDICATIVE_BANDS", codes)

    def test_v4_rejects_a_mark_without_demand_feature(self):
        validator = load_validator_module()
        candidate = make_v4_spec()
        del candidate["questions"][6]["mark_evidence"][-1]["a_demand_feature"]
        codes = {item["code"] for item in validator.validate_spec(candidate)}
        self.assertIn("E_A_DEMAND_FEATURE", codes)


if __name__ == "__main__":
    unittest.main()
