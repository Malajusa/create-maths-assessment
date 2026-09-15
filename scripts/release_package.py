#!/usr/bin/env python3
"""Build a versioned manual-install package with verifiable provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import zipfile


EXCLUDED_ROOTS = {".git", ".github", ".pytest_cache", "__pycache__"}
GENERATED_NAMES = {"INSTALL_MANIFEST.json", "SHA256SUMS.txt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def should_package(path: Path, root: Path, output_zip: Path) -> bool:
    if not path.is_file() or path == output_zip:
        return False
    rel = path.relative_to(root)
    if rel.parts and rel.parts[0] in EXCLUDED_ROOTS:
        return False
    if path.name in GENERATED_NAMES:
        return False
    if any(part == "__pycache__" for part in rel.parts):
        return False
    return True


def collect_files(root: Path, output_zip: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*"))
        if should_package(path, root, output_zip)
    ]


def build_manifest(root: Path, files: list[Path], version: str, source_commit: str) -> dict:
    return {
        "schema_version": 1,
        "skill": "create-maths-assessment",
        "version": version,
        "source_commit": source_commit,
        "files": {
            path.relative_to(root).as_posix(): sha256(path)
            for path in files
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--source-commit", default=os.environ.get("GITHUB_SHA", ""))
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")
    source_commit = args.source_commit.strip()
    if not source_commit:
        raise SystemExit("source commit is required via --source-commit or GITHUB_SHA")

    output_dir = (root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    package_name = f"create-maths-assessment-v{version}.zip"
    output_zip = output_dir / package_name

    files = collect_files(root, output_zip)
    manifest = build_manifest(root, files, version, source_commit)
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())
        archive.writestr("INSTALL_MANIFEST.json", manifest_bytes)

    sums_path = output_dir / "SHA256SUMS.txt"
    sums_path.write_text(f"{sha256(output_zip)}  {package_name}\n", encoding="utf-8")
    (output_dir / "INSTALL_MANIFEST.json").write_bytes(manifest_bytes)

    print(output_zip)
    print(sums_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
