"""Bind release authorisation to current files, rendered review and a fresh audit.

This validates evidence integrity, not the honesty or quality of a reviewer.
Independent mathematical/pedagogical and visual judgement remains mandatory.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


class ReleaseEvidenceError(ValueError):
    """The current package cannot be authorised for release."""


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReleaseEvidenceError(f"{path.name} must contain a JSON object")
    return value


def verify_release(repo_root: Path, run_dir: Path, build_path: Path,
                   content_path: Path, evidence: Any) -> dict[str, str]:
    """Raise on missing/stale evidence; run the real package auditor without a shell.

    All run artefact paths must resolve inside run_dir. An absolute path is allowed
    only inside that directory. No caller-provided command or saved verdict is run.
    """
    try:
        return _verify(repo_root.resolve(), run_dir.resolve(), build_path, content_path, evidence)
    except ReleaseEvidenceError:
        raise
    except (OSError, ValueError, TypeError, KeyError, ImportError, subprocess.SubprocessError) as exc:
        raise ReleaseEvidenceError(str(exc)) from exc


def _verify(repo: Path, run: Path, build_path: Path, content_path: Path,
            evidence: Any) -> dict[str, str]:
    observed: dict[Path, str] = {}
    reserved = {(run / name).resolve() for name in (
        "state.json", "state.tmp", "artifacts/07-release-qa.json", "artifacts/package-audit.json")}

    def tracked(path: Path) -> Path:
        path = path.resolve()
        if not path.is_relative_to(run):
            raise ReleaseEvidenceError("evidence must stay inside the run directory")
        if path in reserved:
            raise ReleaseEvidenceError("reserved controller output cannot be release evidence")
        if not path.is_file() or path.stat().st_size == 0:
            raise ReleaseEvidenceError(f"missing or empty evidence file: {path.name}")
        observed[path] = _hash(path)
        return path

    def file_ref(ref: Any, suffix: str | None = None) -> Path:
        if not isinstance(ref, dict) or not isinstance(ref.get("path"), str):
            raise ReleaseEvidenceError("evidence requires path and sha256 file records")
        path = tracked(run / ref["path"])
        if suffix and path.suffix.lower() != suffix:
            raise ReleaseEvidenceError(f"{path.name} must be a {suffix} file")
        if ref.get("sha256") != observed[path]:
            raise ReleaseEvidenceError(f"evidence hash mismatch: {path.name}")
        return path

    required = {"assessment_spec", "qa_ledger", "design_manifest", "render_review"}
    if not isinstance(evidence, dict) or set(evidence) != required:
        raise ReleaseEvidenceError("release evidence requires spec, ledger, design manifest and render review")
    paths = {key: file_ref(evidence[key], ".json") for key in required}
    build_path, content_path = tracked(build_path), tracked(content_path)
    build = _object(build_path)
    outputs = {role: file_ref(build[role], suffix) for role, suffix in (
        ("student_test", ".pptx"), ("marking_key", ".pptx"), ("curriculum_rationale", ".pdf"))}
    if len(set(outputs.values()) | set(paths.values()) | {build_path, content_path}) != 9:
        raise ReleaseEvidenceError("output and evidence files must have distinct paths")
    if _object(paths["design_manifest"]) != build.get("design_manifest"):
        raise ReleaseEvidenceError("design manifest differs from the recorded build")

    spec = _object(paths["assessment_spec"])
    review = _object(paths["render_review"])
    generator = review.get("generator_execution_id")
    reviewer = review.get("reviewer_execution_id")
    if (review.get("status") != "PASS" or review.get("review_mode") != "independent_reviewer"
            or not isinstance(generator, str) or not generator.strip()
            or not isinstance(reviewer, str) or not reviewer.strip() or generator == reviewer):
        raise ReleaseEvidenceError("an independent reviewer execution is required")
    log = file_ref(review.get("review_record"))
    if log in set(outputs.values()) | set(paths.values()) | {build_path, content_path}:
        raise ReleaseEvidenceError("reviewer execution record must be a distinct file")
    for field, path in (("assessment_spec_sha256", paths["assessment_spec"]),
                        ("content_validation_sha256", content_path), ("build_manifest_sha256", build_path)):
        if review.get(field) != observed[path]:
            raise ReleaseEvidenceError(f"stale review evidence: {field}")

    expected = set()
    for role, count_field in (("student_test", "test_slide_count"), ("marking_key", "key_slide_count"),
                              ("curriculum_rationale", "rationale_page_count")):
        count = spec.get("package", {}).get(count_field)
        if type(count) is not int or count < 1:
            raise ReleaseEvidenceError(f"invalid package page count: {count_field}")
        expected.update((role, page) for page in range(1, count + 1))
    rows = review.get("pages")
    if not isinstance(rows, list):
        raise ReleaseEvidenceError("every final page requires render review evidence")
    seen, images = set(), set()
    from PIL import Image
    for row in rows:
        if not isinstance(row, dict) or type(row.get("page")) is not int:
            raise ReleaseEvidenceError("invalid rendered page record")
        pair = (row.get("artifact"), row["page"])
        if pair not in expected or pair in seen:
            raise ReleaseEvidenceError("missing, duplicate or unexpected rendered page")
        seen.add(pair)
        if row.get("source_sha256") != build[pair[0]]["sha256"]:
            raise ReleaseEvidenceError("render source does not match the current output")
        if (row.get("inspection") != "full_resolution_and_print_scale" or row.get("findings") != []
                or not isinstance(row.get("evidence_inspected"), str)
                or len(row["evidence_inspected"].strip()) < 20):
            raise ReleaseEvidenceError("page inspection is missing, vague or has unresolved findings")
        image = file_ref(row.get("image"), ".png")
        if image in images:
            raise ReleaseEvidenceError("each page needs its own render, not a reused montage")
        images.add(image)
        with Image.open(image) as png:
            if png.format != "PNG" or png.width < 1240 or png.height < 1754:
                raise ReleaseEvidenceError("page render resolution must be at least A4 portrait at 150 dpi")
            png.verify()
    if seen != expected:
        raise ReleaseEvidenceError("render review does not cover every final page")

    script = repo / "scripts/audit_assessment_package.py"
    if not script.is_file():
        raise ReleaseEvidenceError("package audit executable is missing")
    with tempfile.TemporaryDirectory(prefix="release-audit-", dir=run) as temp:
        report = Path(temp) / "report.json"
        command = [sys.executable, str(script), "--spec", str(paths["assessment_spec"]),
                   "--test", str(outputs["student_test"]), "--key", str(outputs["marking_key"]),
                   "--rationale", str(outputs["curriculum_rationale"]), "--ledger", str(paths["qa_ledger"]),
                   "--design-manifest", str(paths["design_manifest"]), "--report", str(report)]
        result = subprocess.run(command, cwd=repo, capture_output=True, text=True, timeout=120)
        if result.returncode != 0 or not report.is_file():
            detail = (result.stdout + result.stderr).strip()[-1500:]
            raise ReleaseEvidenceError(f"fresh package audit failed or produced no report: {detail}")
        audited = _object(report)
        if audited.get("status") != "READY" or audited.get("issues") != []:
            raise ReleaseEvidenceError("fresh package audit did not return READY with zero issues")
        for path, before in observed.items():
            if _hash(path) != before:
                raise ReleaseEvidenceError(f"evidence changed during audit: {path.name}")
        destination = run / "artifacts/package-audit.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(report.read_bytes())
    return {"path": destination.relative_to(run).as_posix(), "sha256": _hash(destination)}
