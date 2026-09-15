#!/usr/bin/env python3
"""Verify an installed Create Maths Assessment package against its release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(root: Path, manifest_path: Path) -> list[str]:
    issues: list[str] = []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("skill") != "create-maths-assessment":
        issues.append("manifest skill is not create-maths-assessment")

    manifest_version = str(manifest.get("version", "")).strip()
    version_path = root / "VERSION"
    if not version_path.is_file():
        issues.append("VERSION is missing")
    else:
        installed_version = version_path.read_text(encoding="utf-8").strip()
        if installed_version != manifest_version:
            issues.append(
                f"VERSION mismatch: installed={installed_version!r} manifest={manifest_version!r}"
            )

    source_commit = str(manifest.get("source_commit", "")).strip()
    if not source_commit:
        issues.append("manifest source_commit is empty")

    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        issues.append("manifest files mapping is missing or empty")
        return issues

    for rel, expected in sorted(files.items()):
        if not isinstance(rel, str) or not isinstance(expected, str):
            issues.append("manifest contains a non-string file record")
            continue
        path = root / rel
        try:
            path.resolve().relative_to(root.resolve())
        except ValueError:
            issues.append(f"manifest path escapes install root: {rel}")
            continue
        if not path.is_file():
            issues.append(f"missing file: {rel}")
            continue
        actual = sha256(path)
        if actual != expected:
            issues.append(f"hash mismatch: {rel}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", default="INSTALL_MANIFEST.json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    if not manifest_path.is_file():
        print(f"NOT VERIFIED: manifest not found: {manifest_path}")
        return 1

    issues = verify(root, manifest_path)
    if issues:
        print("NOT VERIFIED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(
        "VERIFIED "
        f"create-maths-assessment v{manifest['version']} "
        f"source_commit={manifest['source_commit']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
