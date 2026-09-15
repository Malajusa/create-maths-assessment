import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseInstallDocumentationTests(unittest.TestCase):
    def test_install_documentation_routes_to_verifier(self):
        text = (ROOT / "docs/release-installation.md").read_text(encoding="utf-8")
        self.assertIn("scripts/verify_install.py", text)
        self.assertIn("INSTALL_MANIFEST.json", text)
        self.assertIn("package/source parity", text)
        self.assertIn("does not prove", text)


if __name__ == "__main__":
    unittest.main()
