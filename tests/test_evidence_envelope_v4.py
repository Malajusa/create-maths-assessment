import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_validator_module():
    path = ROOT / "scripts/validate_assessment_spec.py"
    spec = importlib.util.spec_from_file_location("validate_assessment_spec_v4", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class EvidenceEnvelopeV4ContractTests(unittest.TestCase):
    def test_default_question_marks_total_25(self):
        validator = load_validator_module()
        self.assertEqual(
            {
                "q1": 1,
                "q2": 1,
                "q3": 1,
                "q4": 2,
                "q5": 4,
                "q6": 5,
                "q7": 5,
                "q8": 6,
            },
            validator.EXPECTED_MARKS,
        )
        self.assertEqual(25, sum(validator.EXPECTED_MARKS.values()))

    def test_default_evidence_envelope_and_cutoffs_are_canonical(self):
        validator = load_validator_module()
        self.assertEqual({"D": 5, "C": 8, "B": 5, "A": 7}, validator.DEFAULT_EVIDENCE_ENVELOPE)
        self.assertEqual({"D": 5, "C": 10, "B": 16, "A": 21}, validator.DEFAULT_INDICATIVE_CUTS)

    def test_structural_boundaries_force_target_standard_evidence(self):
        validator = load_validator_module()
        envelope = validator.DEFAULT_EVIDENCE_ENVELOPE
        cuts = validator.DEFAULT_INDICATIVE_CUTS
        self.assertGreaterEqual(cuts["C"] - envelope["D"], 5)
        self.assertGreaterEqual(cuts["B"] - (envelope["D"] + envelope["C"]), 3)
        self.assertGreaterEqual(cuts["A"] - (envelope["D"] + envelope["C"] + envelope["B"]), 3)

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


if __name__ == "__main__":
    unittest.main()
