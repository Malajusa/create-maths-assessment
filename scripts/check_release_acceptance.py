#!/usr/bin/env python3
"""Check whether the minimum retained evidence for a release acceptance case is present.

This script validates evidence presence only. It does not certify pedagogical quality or
replace the independent reviewer/controller release gate.
"""

from __future__ import annotations

import argparse
from pathlib import Path


CASE_A_REQUIRED = (
    "01-brief.json",
    "02-blueprint.json",
    "05-content-validation.json",
    "assessment-spec.json",
    "Student_Test.pptx",
    "Marking_Key.pptx",
    "Curriculum_Rationale.pdf",
    "qa-ledger.json",
    "design-manifest.json",
    "render-review.json",
    "artifacts/package-audit.json",
)


def missing_case_a_files(run_dir: Path) -> list[str]:
    return [rel for rel in CASE_A_REQUIRED if not (run_dir / rel).is_file()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    args = parser.parse_args()
    run_dir = Path(args.run_dir).resolve()

    missing = missing_case_a_files(run_dir)
    if missing:
        print("NOT COMPLETE: minimum Case A evidence is missing")
        for rel in missing:
            print(f"- {rel}")
        return 1

    print("EVIDENCE PRESENT: run the controller status check and independent re-review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
