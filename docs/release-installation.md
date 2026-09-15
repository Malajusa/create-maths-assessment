# Release installation and verification

Versioned release packages are published from tags whose name exactly matches `v$(cat VERSION)`.

A release contains:

- `create-maths-assessment-vX.Y.Z.zip`;
- `SHA256SUMS.txt`; and
- `INSTALL_MANIFEST.json`.

The ZIP also contains `INSTALL_MANIFEST.json`. The manifest records the skill name, version, tagged source commit and SHA-256 of every packaged repository file except generated release metadata.

After extracting the ZIP, verify the installation from its root:

```bash
python scripts/verify_install.py --root .
```

A successful result prints the verified version and source commit. Missing files, changed file hashes, a mismatched `VERSION`, an empty source commit or a manifest path escaping the install root causes verification to fail.

Installation verification proves package/source parity only. It does not prove that a generated assessment is classroom-ready; assessment release still requires the stage-07 evidence-bound release protocol.
