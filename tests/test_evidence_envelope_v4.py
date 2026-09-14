import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_evidence_module():
    path = ROOT / "scripts/evidence_envelope.py"
    spec = importlib.util.spec_from_file_location("evidence_envelope_v4", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class EvidenceEnvelopeV4ContractTests(unittest.TestCase):
    def test_default_question_marks_total_25(self):
        evidence = load_evidence_module()
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


if __name__ == "__main__":
    unittest.main()
