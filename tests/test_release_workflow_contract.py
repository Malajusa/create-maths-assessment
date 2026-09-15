import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseWorkflowContractTests(unittest.TestCase):
    def test_release_workflow_is_tag_driven_and_publishes_assets(self):
        text = (ROOT / ".github/workflows/package-release.yml").read_text(encoding="utf-8")
        self.assertIn("tags:", text)
        self.assertIn("'v*'", text)
        self.assertIn("gh release create", text)
        self.assertIn("SHA256SUMS.txt", text)
        self.assertIn("INSTALL_MANIFEST.json", text)
        self.assertIn("scripts/verify_install.py", text)

    def test_release_workflow_revalidates_repository_before_publish(self):
        text = (ROOT / ".github/workflows/package-release.yml").read_text(encoding="utf-8")
        for command in (
            "python -m unittest discover -s tests -v",
            "python scripts/validate_repository.py",
            "python scripts/validate_visual_assets.py",
            "python scripts/run_regression_fixtures.py",
        ):
            self.assertIn(command, text)


if __name__ == "__main__":
    unittest.main()
