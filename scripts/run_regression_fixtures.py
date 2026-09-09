from __future__ import annotations

import json
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.controller import PipelineController, PipelineError


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_fixtures(root: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    sequence = [
        ("01-orchestrator-curriculum-resolver", "01-brief.json"),
        ("02-assessment-blueprint", "02-blueprint.json"),
        ("03-question-designer", "03-q1-q6.json"),
        ("04-complex-problem-specialist", "04-q7-q8.json"),
        ("05-maths-pedagogy-validator", "05-validation.json"),
        ("06-document-builder", "06-build.json"),
        ("07-release-qa", "07-release.json"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        ctl = PipelineController(root, Path(tmp))
        try:
            for stage, filename in sequence[:-1]:
                ctl.record(stage, _load(root / "fixtures/gold/minimal-run" / filename))
            try:
                ctl.record(sequence[-1][0], _load(root / "fixtures/gold/minimal-run" / sequence[-1][1]))
            except PipelineError as exc:
                passed = "release evidence" in str(exc) and ctl.state["release_status"] is None
                detail = "structural stages accepted; synthetic READY correctly blocked: " + str(exc)
            else:
                passed = False
                detail = "synthetic fixture incorrectly reached READY without real release evidence"
        except Exception as exc:
            passed = False
            detail = str(exc)
    results.append({"fixture": "gold/minimal-run", "passed": passed, "detail": detail})

    failures = [
        ("failures/q8-dependency", "04-complex-problem-specialist", "04-q7-q8.json", "Q8 must be independent of Q7"),
        ("failures/ready-with-barrier", "07-release-qa", "07-release.json", "READY requires zero open barriers"),
        ("failures/key-provenance", "06-document-builder", "06-build.json", "marking key source hash must equal student test hash"),
    ]
    for fixture, stage, filename, expected in failures:
        with tempfile.TemporaryDirectory() as tmp:
            ctl = PipelineController(root, Path(tmp))
            try:
                ctl.validate_stage_payload(stage, _load(root / "fixtures" / fixture / filename))
            except PipelineError as exc:
                passed = expected in str(exc)
                detail = str(exc)
            else:
                passed = False
                detail = "invalid fixture was accepted"
        results.append({"fixture": fixture, "passed": passed, "detail": detail})
    return results


def main() -> int:
    results = run_fixtures(ROOT)
    for result in results:
        marker = "PASS" if result["passed"] else "FAIL"
        print(f"{marker}: {result['fixture']} — {result['detail']}")
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
