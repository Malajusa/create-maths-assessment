import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script():
    path = ROOT / "scripts" / "check_release_acceptance.py"
    spec = importlib.util.spec_from_file_location("check_release_acceptance", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ReleaseAcceptancePreflightTests(unittest.TestCase):
    def test_missing_case_a_evidence_is_reported(self):
        module = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            missing = module.missing_case_a_files(run_dir)
            self.assertIn("Student_Test.pptx", missing)
            self.assertIn("render-review.json", missing)
            self.assertIn("artifacts/package-audit.json", missing)

    def test_minimum_file_presence_can_be_satisfied_without_claiming_ready(self):
        module = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            for rel in module.CASE_A_REQUIRED:
                path = run_dir / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"evidence")
            self.assertEqual([], module.missing_case_a_files(run_dir))


if __name__ == "__main__":
    unittest.main()
