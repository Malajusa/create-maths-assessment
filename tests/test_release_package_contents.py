import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleasePackageContentsTests(unittest.TestCase):
    def test_release_package_builder_and_verifier_are_part_of_skill_source(self):
        for rel in ("scripts/release_package.py", "scripts/verify_install.py"):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_release_package_builder_excludes_github_metadata(self):
        text = (ROOT / "scripts/release_package.py").read_text(encoding="utf-8")
        self.assertIn('".github"', text)
        self.assertIn('".git"', text)


if __name__ == "__main__":
    unittest.main()
