#!/usr/bin/env python3
"""Audit a v4 criterion-evidence assessment package using the mature legacy package checks plus v4 output checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import audit_assessment_package as legacy
from validate_assessment_spec import V4_EVIDENCE_MODEL


DASHES = str.maketrans({"–": "-", "—": "-", "−": "-"})
SCORE_BANDS = {"E": (0, 4), "D": (5, 9), "C": (10, 15), "B": (16, 20), "A": (21, 25)}


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.translate(DASHES)).strip().casefold()


def _issue(issues: list[dict[str, str]], code: str, path: str, message: str) -> None:
    issues.append({"code": code, "path": path, "message": message})


def _expected_marks_for_spec(spec: dict[str, Any]) -> dict[str, int]:
    """Use the validated specification as mark-count authority."""
    result: dict[str, int] = {}
    for question in spec.get("questions", []):
        if not isinstance(question, dict):
            continue
        qid = str(question.get("id", "")).casefold()
        marks = question.get("marks")
        if qid in {f"q{i}" for i in range(1, 9)} and type(marks) is int and marks > 0:
            result[qid] = marks
    return result


def _score_table_present(text: str) -> bool:
    flat = _norm(text)
    return all(f"{band.casefold()} {low}-{high}" in flat for band, (low, high) in SCORE_BANDS.items())


def _audit_v4_teacher_text(
    student_text: str,
    key_text: str,
    rationale_text: str,
    issues: list[dict[str, str]],
) -> None:
    """Verify teacher-only v4 interpretation appears in the right outputs."""
    student = _norm(student_text)
    key = _norm(key_text)
    rationale = _norm(rationale_text)

    forbidden_student_tokens = (
        "evidence band",
        "band rationale",
        "why_not_lower_band",
        "why not lower band",
        "indicative standard",
        "5d / 8c / 5b / 7a",
    )
    if any(token in student for token in forbidden_student_tokens):
        _issue(
            issues,
            "E_STUDENT_BAND_METADATA",
            "test",
            "Student Test must not display teacher-only evidence-band or component-estimate metadata",
        )

    if not _score_table_present(key):
        _issue(
            issues,
            "E_INDICATIVE_BANDS_OUTPUT",
            "key",
            "Marking Key must show E 0-4, D 5-9, C 10-15, B 16-20 and A 21-25",
        )

    if "5d / 8c / 5b / 7a" not in rationale:
        _issue(
            issues,
            "E_EVIDENCE_ENVELOPE_OUTPUT",
            "rationale",
            "Curriculum Rationale must state the 5D / 8C / 5B / 7A evidence envelope",
        )

    boundary_patterns = (
        r"5\s+c(?:-or-higher|\+)",
        r"3\s+b(?:-or-higher|\+)",
        r"3\s+a(?:\s+marks?|\+)",
    )
    if not all(re.search(pattern, rationale) for pattern in boundary_patterns):
        _issue(
            issues,
            "E_BOUNDARY_PROOF_OUTPUT",
            "rationale",
            "Curriculum Rationale must state the 5 C+, 3 B+ and 3 A structural evidence guarantees",
        )

    key_scope = "indicative" in key and "assessed component" in key
    rationale_scope = (
        "indicative" in rationale
        and "assessed component" in rationale
        and "reporting grade" in rationale
    )
    if not (key_scope and rationale_scope):
        _issue(
            issues,
            "E_COMPONENT_SCOPE_OUTPUT",
            "key/rationale",
            "teacher outputs must describe an indicative assessed-component standard and distinguish it from the reporting grade",
        )


def audit_package(
    spec_path: Path,
    test_path: Path,
    key_path: Path,
    rationale_path: Path,
    ledger_path: Path,
    design_manifest_path: Path | None = None,
) -> dict[str, Any]:
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "NOT READY", "issues": [{"code": "E_SPEC", "path": str(spec_path), "message": str(exc)}]}

    if spec.get("evidence_model") != V4_EVIDENCE_MODEL:
        return legacy.audit_package(
            spec_path, test_path, key_path, rationale_path, ledger_path, design_manifest_path
        )

    expected_marks = _expected_marks_for_spec(spec)
    if set(expected_marks) != {f"q{i}" for i in range(1, 9)}:
        return {
            "status": "NOT READY",
            "issues": [{"code": "E_MARK_SEQUENCE", "path": "spec.questions", "message": "v4 package requires auditable Q1-Q8 mark counts"}],
        }

    # The mature package auditor uses a module-level expected-mark mapping for
    # rendered mark labels/key coverage. Override it only for this isolated call.
    original_marks = legacy.EXPECTED_MARKS
    legacy.EXPECTED_MARKS = expected_marks
    try:
        report = legacy.audit_package(
            spec_path, test_path, key_path, rationale_path, ledger_path, design_manifest_path
        )
    finally:
        legacy.EXPECTED_MARKS = original_marks

    issues = list(report.get("issues", []))
    try:
        test = legacy.parse_deck(test_path)
        key = legacy.parse_deck(key_path)
        student_text = " ".join(
            legacy._slide_text(test, number) for number in range(1, len(test.slides) + 1)
        )
        key_text = " ".join(
            legacy._slide_text(key, number) for number in range(1, len(key.slides) + 1)
        )
        _, rationale_pages = legacy._extract_pdf(rationale_path)
        rationale_text = " ".join(rationale_pages)
        _audit_v4_teacher_text(student_text, key_text, rationale_text, issues)
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        _issue(issues, "E_V4_OUTPUT_AUDIT", "package", str(exc))

    return {"status": "READY" if not issues else "NOT READY", "issues": issues}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--rationale", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--design-manifest", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)

    report = audit_package(
        args.spec,
        args.test,
        args.key,
        args.rationale,
        args.ledger,
        args.design_manifest,
    )
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(report["status"])
    for item in report["issues"]:
        print(f"{item['code']} {item['path']}: {item['message']}")
    return 0 if report["status"] == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
