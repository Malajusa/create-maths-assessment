import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_release_module():
    path = ROOT / "runtime/release_evidence.py"
    spec = importlib.util.spec_from_file_location("release_evidence_v4", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class V4ReleaseRoutingTests(unittest.TestCase):
    def test_v4_spec_routes_to_v4_auditor(self):
        release = load_release_module()
        script = release._audit_script_for_spec(
            ROOT,
            {"evidence_model": "criterion_component_estimate_v1"},
        )
        self.assertEqual(ROOT / "scripts/audit_assessment_package_v4.py", script)

    def test_legacy_spec_routes_to_legacy_auditor(self):
        release = load_release_module()
        script = release._audit_script_for_spec(ROOT, {"schema_version": 1})
        self.assertEqual(ROOT / "scripts/audit_assessment_package.py", script)


if __name__ == "__main__":
    unittest.main()
