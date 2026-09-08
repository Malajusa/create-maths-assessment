#!/usr/bin/env python3
"""Regression tests for the maths-assessment specification and package gates."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from audit_assessment_package import A4_HEIGHT, A4_WIDTH, REQUIRED_GATES, audit_package
from validate_assessment_spec import EXPECTED_MARKS, QUESTION_IDS, validate_spec


ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "examples" / "benchmarks" / "year5-fractions-percentages-release-spec.json"
CASES_PATH = ROOT / "examples" / "benchmarks" / "regression-cases.json"


def _replace_pointer(document: object, pointer: str, value: object) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.strip("/").split("/")]
    target = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = value
    else:
        target[final] = value


def _shape(
    name: str,
    text: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    size: int = 1100,
    shape_id: int = 1,
    transparent: bool = False,
) -> str:
    text_xml = ""
    if text:
        text_xml = (
            "<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r>"
            f'<a:rPr lang="en-AU" sz="{size}"/><a:t>{escape(text)}</a:t>'
            f'</a:r><a:endParaRPr lang="en-AU" sz="{size}"/></a:p></p:txBody>'
        )
    transparency = "<a:noFill/><a:ln><a:noFill/></a:ln>" if transparent else ""
    return (
        "<p:sp>"
        f'<p:nvSpPr><p:cNvPr id="{shape_id}" name="{escape(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>{transparency}'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        f"{text_xml}</p:sp>"
    )


def _fraction_shapes(qid: str, role: str, fraction_id: str, x: int, y: int, shape_id: int, touching: bool = False) -> tuple[list[str], int]:
    num_y = y
    num_cy = 90_000
    bar_y = y + num_cy if touching else y + num_cy + 40_000
    den_y = bar_y + 40_000
    shapes = [
        _shape(f"{qid}-{role}-frac-{fraction_id}-num", "3", x, num_y, 100_000, num_cy, 1100 if role == "student" else 1000, shape_id),
        _shape(f"{qid}-{role}-frac-{fraction_id}-bar", "", x, bar_y, 100_000, 0, 1100, shape_id + 1),
        _shape(f"{qid}-{role}-frac-{fraction_id}-den", "8", x, den_y, 100_000, 90_000, 1100 if role == "student" else 1000, shape_id + 2),
    ]
    return shapes, shape_id + 3


def _question_origin(qid: str) -> tuple[int, int, int]:
    if qid in {"q1", "q2", "q3", "q4", "q5", "q6"}:
        index = int(qid[1:]) - 1
        row, column = divmod(index, 2)
        return 1, 400_000 + column * 3_800_000, 1_200_000 + row * 3_100_000
    return (2, 500_000, 1_500_000) if qid == "q7" else (3, 500_000, 1_500_000)


def _slide_xml(shapes: list[str], include_table: bool = False) -> str:
    table = ""
    if include_table:
        table = (
            '<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="900" name="q7-student-table"/>'
            '<p:cNvGraphicFramePr/><p:nvPr/></p:nvGraphicFramePr>'
            '<p:xfrm><a:off x="500000" y="6000000"/><a:ext cx="2000000" cy="500000"/></p:xfrm>'
            '<a:graphic><a:graphicData><a:tbl/></a:graphicData></a:graphic></p:graphicFrame>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/>'
        '</p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        + "".join(shapes)
        + table
        + '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    )


def _write_deck(path: Path, spec: dict, role: str, mutation: str | None = None) -> None:
    slides: list[list[str]] = [[], [], []]
    shape_id = 10
    for question in spec["questions"]:
        qid = question["id"]
        slide_number, x, y = _question_origin(qid)
        if mutation == "swapped_page1_cells" and role == "test" and qid == "q1":
            x = 4_200_000
        slide = slides[slide_number - 1]
        prompt = " ".join(question["prompt_audit_tokens"])
        if role == "key" and mutation == "changed_student_prompt" and qid == "q1":
            prompt += " changed"
        slide.append(_shape(f"{qid}-student-anchor", qid.upper(), x, y, 180_000, 120_000, 1100, shape_id))
        shape_id += 1
        slide.append(_shape(f"{qid}-student-mark", f"{question['marks']} mark" + ("s" if question["marks"] != 1 else ""), x + 200_000, y, 400_000, 120_000, 1100, shape_id))
        shape_id += 1
        slide.append(_shape(f"{qid}-student-prompt", prompt, x, y + 180_000, 2_900_000, 300_000, 1100, shape_id))
        shape_id += 1
        for representation_id in question["representation"].get("instance_ids", []):
            if mutation == "missing_representation" and role == "test" and qid == "q5":
                continue
            slide.append(
                _shape(
                    f"{qid}-student-representation-{representation_id}",
                    "",
                    x,
                    y + 520_000,
                    2_500_000,
                    300_000,
                    1100,
                    shape_id,
                    True,
                )
            )
            shape_id += 1
        response_token = {
            "blank_unlined": "blank",
            "compact_final_answer": "final",
            "structured_mathematical": "structured",
            "none": "none",
        }[question["response_space"]["kind"]]
        transparent_response = response_token in {"blank", "none"} and not (
            mutation == "bordered_blank_response" and role == "test" and qid == "q6"
        )
        slide.append(
            _shape(
                f"{qid}-student-response-{response_token}",
                "",
                x,
                y + 600_000,
                2_500_000,
                300_000,
                1100,
                shape_id,
                transparent_response,
            )
        )
        shape_id += 1
        for fraction_index, fraction_id in enumerate(question["notation"]["student_fraction_instance_ids"]):
            touching = mutation == "touching_fraction" and role == "test" and qid == "q1" and fraction_index == 0
            parts, shape_id = _fraction_shapes(qid, "student", fraction_id, x + fraction_index * 180_000, y + 950_000, shape_id, touching)
            slide.extend(parts)
        if role == "key":
            key_size = 900 if mutation == "small_key_annotation" and qid == "q1" else 1000
            slide.append(_shape(f"{qid}-key-answer", "Verified answer", x, y + 1_400_000, 900_000, 160_000, key_size, shape_id))
            shape_id += 1
            for mark_number in range(1, question["marks"] + 1):
                if mutation == "missing_key_mark" and qid == "q8" and mark_number == 4:
                    continue
                slide.append(_shape(f"{qid}-key-mark-{mark_number}", f"Mark {mark_number}", x + 950_000, y + 1_350_000 + mark_number * 90_000, 500_000, 80_000, 1000, shape_id))
                shape_id += 1
            for fraction_index, fraction_id in enumerate(question["notation"]["key_fraction_instance_ids"]):
                parts, shape_id = _fraction_shapes(qid, "key", fraction_id, x + 1_600_000 + fraction_index * 180_000, y + 950_000, shape_id)
                slide.extend(parts)
    if role == "key":
        for slide_number, slide in enumerate(slides, start=1):
            slide.append(_shape(f"key-header-{slide_number}", "MARKING KEY", 6_000_000, 200_000, 1_200_000, 200_000, 1200, shape_id))
            shape_id += 1

    presentation = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:sldIdLst><p:sldId id="256" r:id="rId1"/><p:sldId id="257" r:id="rId2"/>'
        '<p:sldId id="258" r:id="rId3"/></p:sldIdLst>'
        f'<p:sldSz cx="{A4_WIDTH}" cy="{A4_HEIGHT}" type="A4"/></p:presentation>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
        + "".join(
            f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(1, 4)
        )
        + "</Types>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", content_types)
        package.writestr("ppt/presentation.xml", presentation)
        for index, slide in enumerate(slides, start=1):
            package.writestr(
                f"ppt/slides/slide{index}.xml",
                _slide_xml(slide, include_table=mutation == "q7_table" and role == "test" and index == 2),
            )


def _write_pdf(path: Path, spec: dict) -> None:
    import fitz  # type: ignore

    document = fitz.open()
    tokens = " | ".join(spec["package"]["rationale_required_tokens"])
    for index in range(spec["package"]["rationale_page_count"]):
        page = document.new_page(width=595, height=842)
        text = tokens if index == 0 else f"Moderation and curriculum rationale evidence page {index + 1}. All checks are documented here."
        page.insert_textbox(fitz.Rect(50, 50, 545, 790), text, fontsize=11)
    document.save(path)
    document.close()


def _write_ledger(path: Path, spec_path: Path, mutation: str | None = None) -> None:
    ledger = {
        "assessment_spec_sha256": hashlib.sha256(spec_path.read_bytes()).hexdigest(),
        "reviews": [
            {"role": "authoring_qa", "reviewer": "author-fixture", "mode": "authoring_qa", "completed": True},
            {"role": "fresh_review", "reviewer": "reviewer-fixture", "mode": "fresh_artifact_only", "completed": True},
        ],
        "gates": [
            {
                "gate": gate,
                "evidence_inspected": f"Regression fixture evidence for gate {gate}",
                "status": "PASS",
                "correction_made": "none",
            }
            for gate in REQUIRED_GATES
        ],
        "open_items": [],
    }
    if mutation == "vague_ledger":
        ledger["gates"][0]["evidence_inspected"] = "checked"
    path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def _run_package_case(spec: dict, mutation: str | None) -> dict:
    with tempfile.TemporaryDirectory(prefix="maths-assessment-regression-") as temp_dir:
        temp = Path(temp_dir)
        spec_path = temp / "assessment-spec.json"
        test_path = temp / "test.pptx"
        key_path = temp / "key.pptx"
        rationale_path = temp / "rationale.pdf"
        ledger_path = temp / "release-ledger.json"
        spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        _write_deck(test_path, spec, "test", mutation)
        _write_deck(key_path, spec, "key", mutation)
        _write_pdf(rationale_path, spec)
        _write_ledger(ledger_path, spec_path, mutation)
        return audit_package(spec_path, test_path, key_path, rationale_path, ledger_path)


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []

    positive_errors = validate_spec(spec)
    if positive_errors:
        failures.append(f"positive specification failed: {positive_errors}")

    for case in cases["spec_cases"]:
        candidate = copy.deepcopy(spec)
        for operation in case["operations"]:
            if operation["op"] != "replace":
                failures.append(f"unsupported operation in {case['name']}")
                continue
            _replace_pointer(candidate, operation["path"], operation["value"])
        codes = {error["code"] for error in validate_spec(candidate)}
        if case["expected_code"] not in codes:
            failures.append(f"{case['name']} expected {case['expected_code']}, got {sorted(codes)}")

    positive_report = _run_package_case(spec, None)
    if positive_report["status"] != "READY":
        failures.append(f"positive package failed: {positive_report['issues']}")

    for case in cases["package_cases"]:
        report = _run_package_case(spec, case["mutation"])
        codes = {issue["code"] for issue in report["issues"]}
        if case["expected_code"] not in codes:
            failures.append(f"{case['name']} expected {case['expected_code']}, got {sorted(codes)}")

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS: 1 positive spec, {len(cases['spec_cases'])} negative specs, 1 positive package and {len(cases['package_cases'])} negative packages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
