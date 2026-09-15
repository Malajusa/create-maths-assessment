import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ReleasePackagingTests(unittest.TestCase):
    def setUp(self):
        self.packaging = load_script("release_package.py")
        self.verifier = load_script("verify_install.py")

    def test_manifest_binds_version_commit_and_file_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VERSION").write_text("4.0.1\n", encoding="utf-8")
            (root / "SKILL.md").write_text("skill contents\n", encoding="utf-8")
            output_zip = root / "dist" / "create-maths-assessment-v4.0.1.zip"
            files = self.packaging.collect_files(root, output_zip)
            manifest = self.packaging.build_manifest(root, files, "4.0.1", "abc123")

            self.assertEqual("create-maths-assessment", manifest["skill"])
            self.assertEqual("4.0.1", manifest["version"])
            self.assertEqual("abc123", manifest["source_commit"])
            self.assertIn("VERSION", manifest["files"])
            self.assertIn("SKILL.md", manifest["files"])

    def test_verifier_accepts_unchanged_install_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VERSION").write_text("4.0.1\n", encoding="utf-8")
            (root / "SKILL.md").write_text("skill contents\n", encoding="utf-8")
            output_zip = root / "dist" / "create-maths-assessment-v4.0.1.zip"
            files = self.packaging.collect_files(root, output_zip)
            manifest = self.packaging.build_manifest(root, files, "4.0.1", "abc123")
            manifest_path = root / "INSTALL_MANIFEST.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            self.assertEqual([], self.verifier.verify(root, manifest_path))

            (root / "SKILL.md").write_text("changed\n", encoding="utf-8")
            issues = self.verifier.verify(root, manifest_path)
            self.assertTrue(any("hash mismatch: SKILL.md" in issue for issue in issues))

    def test_verifier_rejects_manifest_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VERSION").write_text("4.0.1\n", encoding="utf-8")
            manifest = {
                "skill": "create-maths-assessment",
                "version": "4.0.1",
                "source_commit": "abc123",
                "files": {"../outside.txt": "0" * 64},
            }
            manifest_path = root / "INSTALL_MANIFEST.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            issues = self.verifier.verify(root, manifest_path)
            self.assertTrue(any("escapes install root" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
