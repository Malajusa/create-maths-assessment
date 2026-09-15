import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseReadinessV401Tests(unittest.TestCase):
    def test_version_is_v401(self):
        self.assertEqual("4.0.1", (ROOT / "VERSION").read_text(encoding="utf-8").strip())

    def test_release_provenance_files_exist(self):
        required = [
            "scripts/release_package.py",
            "scripts/verify_install.py",
            ".github/workflows/package-release.yml",
            "docs/acceptance/v4.0.1-release-acceptance.md",
        ]
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing)

    def test_interface_metadata_covers_narrow_workflows(self):
        text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8").casefold()
        for token in ("create", "revise", "review", "mark", "exact-source", "equivalent"):
            self.assertIn(token, text)

    def test_acceptance_doc_does_not_claim_scenarios_have_run(self):
        text = (ROOT / "docs/acceptance/v4.0.1-release-acceptance.md").read_text(encoding="utf-8").casefold()
        self.assertIn("do not count as execution results", text)
        self.assertIn("genuinely distinct", text)
        self.assertIn("architecture barrier", text)


if __name__ == "__main__":
    unittest.main()
