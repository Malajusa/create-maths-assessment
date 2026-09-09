import json
import copy
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class VisualSystemContractTests(unittest.TestCase):
    VISUAL_OWNER_FILES = (
        "SKILL.md",
        "agents/02-assessment-blueprint.md",
        "agents/03-question-designer.md",
        "agents/04-complex-problem-specialist.md",
        "agents/05-maths-pedagogy-validator.md",
        "agents/06-document-builder.md",
        "agents/07-release-qa.md",
    )
    def test_default_profile_resolves_visual_tokens(self):
        profile = load_json("assets/visual-profiles/classic-assessment-v1.json")
        self.assertEqual(
            "assets/visual-tokens/assessment-visual-tokens-v1.json",
            profile["token_set"],
        )
        tokens = load_json(profile["token_set"])
        self.assertEqual("#1F2937", tokens["colours"]["primary_outline"])
        self.assertEqual("#F8FAFC", tokens["colours"]["canonical_fill"])
        self.assertTrue(tokens["accessibility"]["greyscale_required"])
        self.assertTrue(tokens["accessibility"]["colour_never_sole_cue"])

    def test_visual_profile_schema_requires_versioned_resources(self):
        profile = load_json("assets/visual-profiles/classic-assessment-v1.json")
        schema = load_json("schemas/visual-profile.schema.json")
        errors = list(Draft202012Validator(schema).iter_errors(profile))
        self.assertEqual([], errors)
        self.assertIn("token_set", schema["required"])
        self.assertIn("asset_manifest", schema["required"])

    def test_canonical_visual_guidance_exists(self):
        visual_standard = (ROOT / "standards/visual-standard.md").read_text(encoding="utf-8")
        contextual = (ROOT / "references/contextual-illustration-standard.md").read_text(encoding="utf-8")
        for phrase in (
            "Every visual must have a declared purpose",
            "exact mathematical mode",
            "contextual problem-solving mode",
            "colour must not be the only",
            "release barrier",
        ):
            self.assertIn(phrase.casefold(), visual_standard.casefold())
        self.assertIn("must not pre-solve", contextual.casefold())
        self.assertIn("original or distributable", contextual.casefold())

    def test_starter_asset_manifest_and_geometry(self):
        from scripts.validate_visual_assets import validate_manifest

        manifest_path = ROOT / "assets/maths-visuals/v1/manifest.json"
        self.assertEqual([], validate_manifest(ROOT, manifest_path))
        manifest = load_json("assets/maths-visuals/v1/manifest.json")
        self.assertEqual(3, len(manifest["assets"]))
        self.assertEqual(
            {
                "shape.square.v1",
                "shape.circle.v1",
                "shape.equilateral-triangle.v1",
            },
            {asset["asset_id"] for asset in manifest["assets"]},
        )

    def test_asset_validator_rejects_protected_or_unknown_provenance(self):
        from scripts.validate_visual_assets import validate_manifest_data

        manifest = load_json("assets/maths-visuals/v1/manifest.json")
        manifest["assets"][0]["provenance"]["licence"] = "personal_reference_only"
        issues = validate_manifest_data(ROOT, manifest)
        self.assertIn("E_ASSET_LICENCE", {issue["code"] for issue in issues})

    def test_visual_spec_schema_requires_semantic_decisions(self):
        schema = load_json("schemas/visual-spec.schema.json")
        required = set(schema["required"])
        self.assertTrue(
            {
                "family",
                "purpose",
                "information_carried",
                "removal_effect",
                "scale_status",
                "student_action",
                "strategy_reveal_risk",
                "source_kind",
                "accessibility_cues",
            }.issubset(required)
        )

    def test_required_representation_requires_visual_spec(self):
        from scripts.validate_assessment_spec import validate_spec

        spec = load_json("examples/benchmarks/year5-fractions-percentages-release-spec.json")
        spec = copy.deepcopy(spec)
        spec["questions"][0]["visual_spec"] = None
        codes = {issue["code"] for issue in validate_spec(spec)}
        self.assertIn("E_VISUAL_PURPOSE", codes)

    def test_q8_rejects_solution_ready_visual(self):
        from scripts.validate_assessment_spec import validate_spec

        spec = load_json("examples/benchmarks/year5-fractions-percentages-release-spec.json")
        spec = copy.deepcopy(spec)
        q8 = spec["questions"][7]
        q8["representation"] = {
            "required": True,
            "kind": "contextual illustration",
            "mathematical_purpose": "Establishes the setting without organising the quantities.",
            "omission_reason": "",
            "instance_ids": ["goal-setting-context"],
        }
        q8["visual_spec"] = {
            "family": "contextual_illustration",
            "purpose": "Establish the setting without encoding a solution path.",
            "information_carried": ["The two records concern the same activity."],
            "removal_effect": "The situation would be less immediately recognisable.",
            "scale_status": "schematic",
            "student_action": "Interpret the prose; do not calculate from the picture.",
            "strategy_reveal_risk": "preorganises_solution",
            "source_kind": "original_contextual",
            "asset_ids": [],
            "constructor_id": None,
            "accessibility_cues": ["Meaning remains clear in greyscale", "No meaning relies on colour alone"],
            "editable_required": True,
            "minimum_print_dimensions_mm": {"width": 45, "height": 30},
        }
        codes = {issue["code"] for issue in validate_spec(spec)}
        self.assertIn("E_VISUAL_STRATEGY", codes)

    def test_visual_can_be_omitted_with_specific_reason(self):
        from scripts.validate_assessment_spec import validate_spec

        spec = load_json("examples/benchmarks/year5-fractions-percentages-release-spec.json")
        spec = copy.deepcopy(spec)
        spec["questions"][7]["visual_spec"] = None
        codes = {issue["code"] for issue in validate_spec(spec)}
        self.assertNotIn("E_VISUAL_PURPOSE", codes)

    def test_visual_standard_is_routed_to_every_visual_owner(self):
        for path in self.VISUAL_OWNER_FILES:
            with self.subTest(path=path):
                self.assertIn(
                    "standards/visual-standard.md",
                    (ROOT / path).read_text(encoding="utf-8"),
                )

    def test_design_manifest_requires_visual_evidence(self):
        schema = load_json("schemas/design-manifest.schema.json")
        self.assertIn("visual_system", schema["required"])
        visual_system = schema["properties"]["visual_system"]
        for field in (
            "visual_profile_sha256",
            "token_set_sha256",
            "asset_manifest_sha256",
            "questions",
            "greyscale_reviewed",
        ):
            self.assertIn(field, visual_system["required"])

    def test_package_audit_requires_visual_release_evidence(self):
        source = (ROOT / "scripts/audit_assessment_package.py").read_text(encoding="utf-8")
        self.assertIn("E_VISUAL_GREYSCALE", source)
        self.assertIn("E_VISUAL_ASSET_HASH", source)
        self.assertIn("E_VISUAL_DEMAND", source)

    def test_visual_proof_artefacts_are_registered(self):
        for path in (
            "assets/visual-benchmarks/canonical-figures-proof.svg",
            "assets/visual-benchmarks/problem-page-proof.svg",
            "examples/benchmarks/visual-semantic-cases.json",
        ):
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
