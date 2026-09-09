#!/usr/bin/env python3
"""Audit a complete maths-assessment package against its validated source spec."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from validate_assessment_spec import EXPECTED_MARKS, EXPECTED_POSITIONS, QUESTION_IDS, load_spec, validate_spec


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}
A4_WIDTH = 7_560_000
A4_HEIGHT = 10_692_000
MIN_STUDENT_FONT = 1_050
MIN_KEY_FONT = 1_000
TARGET_STUDENT_BODY_MIN = 1_125
TARGET_ESSENTIAL_LABEL_MIN = 1_100
MIN_FRACTION_GAP = 25_200  # 0.7 mm in English Metric Units
SLASH_FRACTION = re.compile(r"(?<!\w)\d+\s*[⁄/]\s*\d+(?!\w)")
VULGAR_FRACTIONS = set("¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞")
FRACTION_NAME = re.compile(r"^(q[1-8])-(student|key)-frac-(.+)-(num|bar|den)$")
REQUIRED_GATES = [f"P{i:02d}" for i in range(1, 30)] + [f"R{i:02d}" for i in range(1, 19)]
REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Shape:
    slide: int
    name: str
    text: str
    x: int | None
    y: int | None
    cx: int | None
    cy: int | None
    font_sizes: tuple[int | None, ...]
    no_fill: bool
    no_line: bool
    element_hash: str

    def student_signature(self) -> tuple[Any, ...]:
        return (
            self.slide,
            self.name,
            self.text,
            self.x,
            self.y,
            self.cx,
            self.cy,
            self.font_sizes,
            self.no_fill,
            self.no_line,
            self.element_hash,
        )


@dataclass
class Deck:
    path: Path
    width: int
    height: int
    slides: list[list[Shape]]
    table_counts: list[int]


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _issue(issues: list[dict[str, str]], code: str, path: str, message: str) -> None:
    issues.append({"code": code, "path": path, "message": message})


def _shape_name(element: ET.Element) -> str:
    node = element.find("./p:nvSpPr/p:cNvPr", NS)
    if node is None:
        node = element.find("./p:nvGraphicFramePr/p:cNvPr", NS)
    if node is None:
        node = element.find("./p:nvPicPr/p:cNvPr", NS)
    if node is None:
        node = element.find("./p:nvCxnSpPr/p:cNvPr", NS)
    return node.get("name", "") if node is not None else ""


def _geometry(element: ET.Element) -> tuple[int | None, int | None, int | None, int | None]:
    xfrm = element.find("./p:spPr/a:xfrm", NS)
    if xfrm is None:
        xfrm = element.find("./p:xfrm", NS)
    if xfrm is None:
        xfrm = element.find("./p:grpSpPr/a:xfrm", NS)
    if xfrm is None:
        return (None, None, None, None)
    off = xfrm.find("./a:off", NS)
    ext = xfrm.find("./a:ext", NS)
    if off is None or ext is None:
        return (None, None, None, None)
    return tuple(int(value) for value in (off.get("x", "0"), off.get("y", "0"), ext.get("cx", "0"), ext.get("cy", "0")))


def _font_sizes(element: ET.Element) -> tuple[int | None, ...]:
    paragraph_defaults: dict[int, int | None] = {}
    for index, paragraph in enumerate(element.findall(".//a:p", NS)):
        default = paragraph.find("./a:pPr/a:defRPr", NS)
        paragraph_defaults[index] = int(default.get("sz")) if default is not None and default.get("sz") else None

    sizes: list[int | None] = []
    for paragraph_index, paragraph in enumerate(element.findall(".//a:p", NS)):
        inherited = paragraph_defaults.get(paragraph_index)
        for run in paragraph.findall("./a:r", NS):
            text = "".join(node.text or "" for node in run.findall("./a:t", NS)).strip()
            if not text:
                continue
            props = run.find("./a:rPr", NS)
            sizes.append(int(props.get("sz")) if props is not None and props.get("sz") else inherited)
        for field in paragraph.findall("./a:fld", NS):
            text = "".join(node.text or "" for node in field.findall("./a:t", NS)).strip()
            if not text:
                continue
            props = field.find("./a:rPr", NS)
            sizes.append(int(props.get("sz")) if props is not None and props.get("sz") else inherited)
    return tuple(sizes)


def _element_hash(element: ET.Element) -> str:
    clone = copy.deepcopy(element)
    for node in clone.findall(".//p:cNvPr", NS):
        node.set("id", "0")
    return hashlib.sha256(ET.tostring(clone, encoding="utf-8")).hexdigest()


def parse_deck(path: Path) -> Deck:
    with zipfile.ZipFile(path) as package:
        corrupt = package.testzip()
        if corrupt:
            raise ValueError(f"corrupt ZIP member: {corrupt}")
        presentation = ET.fromstring(package.read("ppt/presentation.xml"))
        slide_size = presentation.find("./p:sldSz", NS)
        if slide_size is None:
            raise ValueError("missing p:sldSz")
        width = int(slide_size.get("cx", "0"))
        height = int(slide_size.get("cy", "0"))
        slide_names = sorted(
            (
                name
                for name in package.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ),
            key=lambda name: int(re.search(r"\d+", name).group()),
        )
        slides: list[list[Shape]] = []
        table_counts: list[int] = []
        for slide_number, slide_name in enumerate(slide_names, start=1):
            root = ET.fromstring(package.read(slide_name))
            shapes: list[Shape] = []
            for tag in ("sp", "graphicFrame", "pic", "cxnSp"):
                for element in root.findall(f".//p:{tag}", NS):
                    name = _shape_name(element)
                    text = " ".join(node.text or "" for node in element.findall(".//a:t", NS)).strip()
                    x, y, cx, cy = _geometry(element)
                    no_fill = element.find("./p:spPr/a:noFill", NS) is not None
                    no_line = element.find("./p:spPr/a:ln/a:noFill", NS) is not None
                    shapes.append(
                        Shape(
                            slide_number,
                            name,
                            text,
                            x,
                            y,
                            cx,
                            cy,
                            _font_sizes(element),
                            no_fill,
                            no_line,
                            _element_hash(element),
                        )
                    )
            slides.append(shapes)
            table_counts.append(len(root.findall(".//a:tbl", NS)))
        return Deck(path, width, height, slides, table_counts)


def _shape_map(deck: Deck) -> dict[str, Shape]:
    result: dict[str, Shape] = {}
    duplicates: set[str] = set()
    for slide in deck.slides:
        for shape in slide:
            if not shape.name:
                continue
            if shape.name in result:
                duplicates.add(shape.name)
            else:
                result[shape.name] = shape
    for name in duplicates:
        result.pop(name, None)
    return result


def _slide_text(deck: Deck, slide_number: int) -> str:
    return " ".join(shape.text for shape in deck.slides[slide_number - 1] if shape.text)


def _question_text(deck: Deck, qid: str) -> str:
    prefix = f"{qid}-student-"
    return " ".join(
        shape.text for slide in deck.slides for shape in slide if shape.name.startswith(prefix) and shape.text
    )


def _position(shape: Shape, width: int, height: int) -> str | None:
    if shape.x is None or shape.y is None or shape.cx is None or shape.cy is None:
        return None
    centre_x = shape.x + shape.cx / 2
    centre_y = shape.y + shape.cy / 2
    column = "left" if centre_x < width / 2 else "right"
    if centre_y < height / 3:
        row = "top"
    elif centre_y < 2 * height / 3:
        row = "middle"
    else:
        row = "bottom"
    return f"{row}_{column}"


def _contains(parent: Shape, child: Shape) -> bool:
    if None in (parent.x, parent.y, parent.cx, parent.cy, child.x, child.y, child.cx, child.cy):
        return False
    return (
        child.x >= parent.x
        and child.y >= parent.y
        and child.x + child.cx <= parent.x + parent.cx
        and child.y + child.cy <= parent.y + parent.cy
    )


def _intersects(a: Shape, b: Shape) -> bool:
    if None in (a.x, a.y, a.cx, a.cy, b.x, b.y, b.cx, b.cy):
        return False
    return not (
        a.x + a.cx <= b.x or b.x + b.cx <= a.x
        or a.y + a.cy <= b.y or b.y + b.cy <= a.y
    )


def _audit_positive_visual_contract(deck: Deck, shapes: dict[str, Shape], issues: list[dict[str, str]]) -> None:
    active = any(f"q{i}-student-cell" in shapes for i in range(1, 7))
    if active:
        for i in range(1, 7):
            qid = f"q{i}"
            cell_name = f"{qid}-student-cell"
            cell = shapes.get(cell_name)
            if cell is None:
                _issue(issues, "E_QUESTION_CELL", f"test:{cell_name}", "strict visual contract requires all six Page 1 cell anchors")
                continue
            for slide in deck.slides:
                for shape in slide:
                    if not shape.name.startswith(f"{qid}-student-") or shape.name == cell_name:
                        continue
                    if shape.slide != cell.slide or not _contains(cell, shape):
                        _issue(issues, "E_CELL_CONTAINMENT", f"test:{shape.name}", f"must remain within {cell_name}")

        for name, shape in shapes.items():
            if re.match(r"^q[1-8]-student-dimension-", name):
                if not shape.font_sizes or any(size is None for size in shape.font_sizes):
                    _issue(issues, "E_VISUAL_TARGET", f"test:{name}", "essential dimension label requires explicit font sizing")
                elif min(size for size in shape.font_sizes if size is not None) < TARGET_ESSENTIAL_LABEL_MIN:
                    _issue(issues, "E_VISUAL_TARGET", f"test:{name}", f"essential dimension label target minimum is {TARGET_ESSENTIAL_LABEL_MIN / 100:.1f} pt")
            if re.match(r"^q[1-8]-student-prompt$", name):
                if shape.font_sizes and all(size is not None for size in shape.font_sizes):
                    if min(size for size in shape.font_sizes if size is not None) < TARGET_STUDENT_BODY_MIN:
                        _issue(issues, "E_VISUAL_TARGET", f"test:{name}", f"student prompt target minimum is {TARGET_STUDENT_BODY_MIN / 100:.2f} pt")

        for qid in QUESTION_IDS:
            response = next((s for n, s in shapes.items() if n.startswith(f"{qid}-student-response-")), None)
            if response is None:
                continue
            for name, representation in shapes.items():
                if name.startswith(f"{qid}-student-representation-") and _intersects(response, representation):
                    _issue(issues, "E_RESPONSE_COLLISION", f"test:{qid}", "required representation intersects reserved response space")


def _audit_deck_basics(deck: Deck, role: str, expected_slides: int, issues: list[dict[str, str]]) -> None:
    if (deck.width, deck.height) != (A4_WIDTH, A4_HEIGHT):
        _issue(issues, "E_A4", role, f"expected A4 portrait {A4_WIDTH}x{A4_HEIGHT}, found {deck.width}x{deck.height}")
    if len(deck.slides) != expected_slides:
        _issue(issues, "E_SLIDE_COUNT", role, f"expected {expected_slides} slides, found {len(deck.slides)}")
    for slide in deck.slides:
        for shape in slide:
            if None in (shape.x, shape.y, shape.cx, shape.cy):
                continue
            if shape.x < 0 or shape.y < 0 or shape.x + shape.cx > deck.width or shape.y + shape.cy > deck.height:
                _issue(issues, "E_BOUNDS", f"{role}:{shape.name or 'unnamed'}", "shape extends beyond the slide boundary")


def _audit_font_sizes(deck: Deck, issues: list[dict[str, str]]) -> None:
    for slide in deck.slides:
        for shape in slide:
            if not shape.text:
                continue
            minimum = None
            if re.match(r"^q[1-8]-student-", shape.name):
                minimum = MIN_STUDENT_FONT
            elif re.match(r"^q[1-8]-key-", shape.name):
                minimum = MIN_KEY_FONT
            if minimum is None:
                continue
            if not shape.font_sizes or any(size is None for size in shape.font_sizes):
                _issue(issues, "E_FONT_UNVERIFIED", shape.name, "all auditable text runs require an explicit font size")
            elif min(size for size in shape.font_sizes if size is not None) < minimum:
                _issue(issues, "E_FONT_SIZE", shape.name, f"minimum is {minimum / 100:.1f} pt")


def _audit_fraction_groups(
    deck: Deck,
    role: str,
    expected: set[tuple[str, str, str]],
    issues: list[dict[str, str]],
) -> None:
    groups: dict[tuple[str, str, str], dict[str, Shape]] = {}
    for slide in deck.slides:
        for shape in slide:
            match = FRACTION_NAME.fullmatch(shape.name)
            if match:
                key = (match.group(1), match.group(2), match.group(3))
                groups.setdefault(key, {})[match.group(4)] = shape
    for key in sorted(expected):
        if key not in groups:
            _issue(issues, "E_FRACTION_INSTANCE", f"{role}:{'-'.join(key)}", "required named fraction instance is missing")
    for key, parts in sorted(groups.items()):
        if set(parts) != {"num", "bar", "den"}:
            _issue(issues, "E_FRACTION_INSTANCE", f"{role}:{'-'.join(key)}", "fraction requires num, bar and den components")
            continue
        num, bar, den = parts["num"], parts["bar"], parts["den"]
        if None in (num.y, num.cy, bar.y, bar.cy, den.y):
            _issue(issues, "E_FRACTION_GEOMETRY", f"{role}:{'-'.join(key)}", "fraction geometry is not auditable")
            continue
        upper_gap = bar.y - (num.y + num.cy)
        lower_gap = den.y - (bar.y + bar.cy)
        if upper_gap < MIN_FRACTION_GAP:
            _issue(issues, "E_FRACTION_CLEARANCE", f"{role}:{'-'.join(key)}", f"numerator gap {upper_gap} EMU is below {MIN_FRACTION_GAP}")
        if lower_gap < MIN_FRACTION_GAP:
            _issue(issues, "E_FRACTION_CLEARANCE", f"{role}:{'-'.join(key)}", f"denominator gap {lower_gap} EMU is below {MIN_FRACTION_GAP}")


def _audit_ledger(path: Path, spec_bytes: bytes, issues: list[dict[str, str]]) -> None:
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _issue(issues, "E_LEDGER", str(path), str(exc))
        return
    expected_hash = hashlib.sha256(spec_bytes).hexdigest()
    if ledger.get("assessment_spec_sha256") != expected_hash:
        _issue(issues, "E_LEDGER_HASH", "ledger.assessment_spec_sha256", "does not match the audited specification")
    reviews = ledger.get("reviews") if isinstance(ledger.get("reviews"), list) else []
    by_role = {review.get("role"): review for review in reviews if isinstance(review, dict)}
    author = by_role.get("authoring_qa", {})
    fresh = by_role.get("fresh_review", {})
    if author.get("completed") is not True or author.get("mode") != "authoring_qa" or not str(author.get("reviewer", "")).strip():
        _issue(issues, "E_REVIEW", "ledger.reviews", "completed authoring QA review is required")
    if fresh.get("completed") is not True or fresh.get("mode") not in {"independent_reviewer", "fresh_artifact_only"} or not str(fresh.get("reviewer", "")).strip():
        _issue(issues, "E_REVIEW", "ledger.reviews", "completed fresh artifact review is required")
    if author == fresh:
        _issue(issues, "E_REVIEW", "ledger.reviews", "review records must be distinct")

    gates = ledger.get("gates") if isinstance(ledger.get("gates"), list) else []
    ids = [gate.get("gate") for gate in gates if isinstance(gate, dict)]
    if sorted(ids) != sorted(REQUIRED_GATES) or len(ids) != len(set(ids)):
        _issue(issues, "E_LEDGER_GATES", "ledger.gates", "must contain P01-P29 and R01-R18 exactly once")
    vague = {"checked", "looks correct", "pass", "passed", "ok", "yes"}
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            _issue(issues, "E_LEDGER_GATES", f"ledger.gates[{index}]", "must be an object")
            continue
        if gate.get("status") != "PASS":
            _issue(issues, "E_LEDGER_STATUS", f"ledger.gates[{index}]", "every gate must record PASS")
        evidence = str(gate.get("evidence_inspected", "")).strip()
        if len(evidence) < 12 or evidence.casefold() in vague:
            _issue(issues, "E_LEDGER_EVIDENCE", f"ledger.gates[{index}]", "must record specific inspected evidence")
        if not str(gate.get("correction_made", "")).strip():
            _issue(issues, "E_LEDGER_EVIDENCE", f"ledger.gates[{index}].correction_made", "must record the correction or 'none'")
    if ledger.get("open_items") != []:
        _issue(issues, "E_LEDGER_OPEN", "ledger.open_items", "must be an empty list")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _audit_visual_system(
    spec: dict[str, Any], design_manifest_path: Path | None, issues: list[dict[str, str]]
) -> None:
    if design_manifest_path is None:
        _issue(issues, "E_VISUAL_ASSET_HASH", "design_manifest", "a design manifest is required for visual-system verification")
        return
    try:
        design = json.loads(design_manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _issue(issues, "E_VISUAL_ASSET_HASH", str(design_manifest_path), str(exc))
        return

    visual = design.get("visual_system") if isinstance(design.get("visual_system"), dict) else {}
    profile_path = REPO_ROOT / "assets/visual-profiles/classic-assessment-v1.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    token_path = REPO_ROOT / profile["token_set"]
    asset_manifest_path = REPO_ROOT / profile["asset_manifest"]
    assets = json.loads(asset_manifest_path.read_text(encoding="utf-8"))["assets"]
    known_asset_ids = {asset["asset_id"] for asset in assets if asset.get("validation_status") == "approved"}
    expected_hashes = {
        "visual_profile_sha256": _sha256(profile_path),
        "token_set_sha256": _sha256(token_path),
        "asset_manifest_sha256": _sha256(asset_manifest_path),
    }
    for field, expected in expected_hashes.items():
        if visual.get(field) != expected:
            _issue(issues, "E_VISUAL_ASSET_HASH", f"design_manifest.visual_system.{field}", "does not match the approved repository resource")
    if design.get("profile_sha256") != expected_hashes["visual_profile_sha256"]:
        _issue(issues, "E_VISUAL_ASSET_HASH", "design_manifest.profile_sha256", "does not match the resolved visual profile")
    if visual.get("greyscale_reviewed") is not True:
        _issue(issues, "E_VISUAL_GREYSCALE", "design_manifest.visual_system.greyscale_reviewed", "must record a completed greyscale review")

    evidence_rows = visual.get("questions") if isinstance(visual.get("questions"), list) else []
    evidence_by_qid = {row.get("question_id", "").casefold(): row for row in evidence_rows if isinstance(row, dict)}
    for question in spec.get("questions", []):
        visual_spec = question.get("visual_spec")
        if not isinstance(visual_spec, dict):
            continue
        qid = question.get("id", "")
        evidence = evidence_by_qid.get(qid)
        if not evidence:
            _issue(issues, "E_VISUAL_ASSET_HASH", f"design_manifest.visual_system.questions.{qid}", "required visual has no build evidence")
            continue
        unknown = set(evidence.get("asset_ids", [])) - known_asset_ids
        if unknown:
            _issue(issues, "E_VISUAL_ASSET_HASH", f"design_manifest.visual_system.questions.{qid}.asset_ids", f"contains unapproved asset IDs: {sorted(unknown)}")
        if evidence.get("asset_ids", []) != visual_spec.get("asset_ids", []):
            _issue(issues, "E_VISUAL_ASSET_HASH", f"design_manifest.visual_system.questions.{qid}.asset_ids", "does not match the approved visual specification")
        if evidence.get("constructor_id") != visual_spec.get("constructor_id") or evidence.get("scale_status") != visual_spec.get("scale_status"):
            _issue(issues, "E_VISUAL_ASSET_HASH", f"design_manifest.visual_system.questions.{qid}", "constructor or scale evidence does not match the approved visual specification")
        dimensions = evidence.get("printed_dimensions_mm", {})
        minimum = visual_spec.get("minimum_print_dimensions_mm", {})
        if any(not isinstance(dimensions.get(axis), (int, float)) or dimensions[axis] < minimum.get(axis, 0) for axis in ("width", "height")):
            _issue(issues, "E_VISUAL_ASSET_HASH", f"design_manifest.visual_system.questions.{qid}.printed_dimensions_mm", "rendered visual is smaller than its approved print minimum")
        if evidence.get("greyscale_safe") is not True:
            _issue(issues, "E_VISUAL_GREYSCALE", f"design_manifest.visual_system.questions.{qid}", "visual is not evidenced as greyscale-safe")
        if evidence.get("demand_preserved") is not True:
            _issue(issues, "E_VISUAL_DEMAND", f"design_manifest.visual_system.questions.{qid}", "visual does not preserve the approved assessment demand")


def _extract_pdf(path: Path) -> tuple[int, list[str]]:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required to audit the rationale PDF") from exc
    with fitz.open(path) as document:
        return len(document), [page.get_text("text") for page in document]


def audit_package(
    spec_path: Path,
    test_path: Path,
    key_path: Path,
    rationale_path: Path,
    ledger_path: Path,
    design_manifest_path: Path | None = None,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    try:
        spec_bytes = spec_path.read_bytes()
        spec = json.loads(spec_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"status": "NOT READY", "issues": [{"code": "E_SPEC", "path": str(spec_path), "message": str(exc)}]}

    for error in validate_spec(spec):
        _issue(issues, error["code"], f"spec:{error['path']}", error["message"])

    package_spec = spec.get("package", {}) if isinstance(spec.get("package"), dict) else {}
    try:
        test = parse_deck(test_path)
        key = parse_deck(key_path)
    except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError, ValueError) as exc:
        _issue(issues, "E_PPTX", "PowerPoint", str(exc))
        return {"status": "NOT READY", "issues": issues}

    _audit_deck_basics(test, "test", package_spec.get("test_slide_count", 3), issues)
    _audit_deck_basics(key, "key", package_spec.get("key_slide_count", 3), issues)
    _audit_font_sizes(test, issues)
    _audit_font_sizes(key, issues)

    test_shapes = _shape_map(test)
    key_shapes = _shape_map(key)
    _audit_positive_visual_contract(test, test_shapes, issues)
    for qid in QUESTION_IDS:
        question = next((q for q in spec.get("questions", []) if q.get("id") == qid), {})
        expected_slide = 1 if qid in EXPECTED_POSITIONS else 2 if qid == "q7" else 3
        anchor_name = f"{qid}-student-anchor"
        anchor = test_shapes.get(anchor_name)
        if anchor is None:
            _issue(issues, "E_STABLE_NAME", f"test:{anchor_name}", "required question anchor is missing or duplicated")
        else:
            if anchor.slide != expected_slide:
                _issue(issues, "E_PAGE_SEQUENCE", f"test:{anchor_name}", f"must be on slide {expected_slide}")
            if qid in EXPECTED_POSITIONS and _position(anchor, test.width, test.height) != EXPECTED_POSITIONS[qid]:
                _issue(issues, "E_PAGE1_POSITION", f"test:{anchor_name}", f"must be {EXPECTED_POSITIONS[qid]}")

        mark_name = f"{qid}-student-mark"
        mark_shape = test_shapes.get(mark_name)
        if mark_shape is None:
            _issue(issues, "E_STABLE_NAME", f"test:{mark_name}", "required mark label is missing or duplicated")
        else:
            expected_mark = EXPECTED_MARKS[qid]
            if not re.search(rf"\b{expected_mark}\s*marks?\b", _norm(mark_shape.text)):
                _issue(issues, "E_MARK_LABEL", f"test:{mark_name}", f"must display {expected_mark} mark(s)")

        response = question.get("response_space", {})
        response_token = {
            "blank_unlined": "blank",
            "compact_final_answer": "final",
            "structured_mathematical": "structured",
            "none": "none",
        }.get(response.get("kind"))
        response_name = f"{qid}-student-response-{response_token}"
        if response_token and response_name not in test_shapes:
            _issue(issues, "E_RESPONSE_SPACE", f"test:{response_name}", "response-space anchor does not match the specification")
        elif response_token in {"blank", "none"}:
            response_shape = test_shapes[response_name]
            if not response_shape.no_fill or not response_shape.no_line:
                _issue(issues, "E_RESPONSE_SCAFFOLD", f"test:{response_name}", "blank response anchor must be explicitly transparent and unbordered")

        for representation_id in question.get("representation", {}).get("instance_ids", []):
            representation_name = f"{qid}-student-representation-{representation_id}"
            if representation_name not in test_shapes:
                _issue(issues, "E_REPRESENTATION", f"test:{representation_name}", "required representation anchor is missing or duplicated")

        prompt_text = _norm(_question_text(test, qid))
        for token in question.get("prompt_audit_tokens", []):
            if _norm(token) not in prompt_text:
                _issue(issues, "E_PROMPT_TOKEN", f"test:{qid}", f"missing prompt token {token!r}")
        permitted_labels = {_norm(label) for label in response.get("labels", [])}
        for label in ("answer:", "working and check", "strategy:"):
            if _norm(label) in prompt_text and _norm(label) not in permitted_labels:
                _issue(issues, "E_RESPONSE_SCAFFOLD", f"test:{qid}", f"unjustified response label {label!r}")

        for key_name in [f"{qid}-key-answer"] + [f"{qid}-key-mark-{i}" for i in range(1, EXPECTED_MARKS[qid] + 1)]:
            if key_name not in key_shapes:
                _issue(issues, "E_KEY_COVERAGE", f"key:{key_name}", "required answer or mark annotation is missing or duplicated")

    student_test = {
        shape.name: shape.student_signature()
        for slide in test.slides
        for shape in slide
        if re.match(r"^q[1-8]-student-", shape.name)
    }
    student_key = {
        shape.name: shape.student_signature()
        for slide in key.slides
        for shape in slide
        if re.match(r"^q[1-8]-student-", shape.name)
    }
    if student_test != student_key:
        missing = sorted(set(student_test) - set(student_key))
        added = sorted(set(student_key) - set(student_test))
        changed = sorted(name for name in set(student_test) & set(student_key) if student_test[name] != student_key[name])
        _issue(issues, "E_TEST_KEY_IDENTITY", "test/key", f"student elements differ; missing={missing}, added={added}, changed={changed}")

    for slide_number in range(1, min(3, len(key.slides)) + 1):
        if "marking key" not in _norm(_slide_text(key, slide_number)):
            _issue(issues, "E_KEY_HEADER", f"key:slide{slide_number}", "MARKING KEY is not visible")

    for role, deck in (("test", test), ("key", key)):
        all_text = " ".join(_slide_text(deck, number) for number in range(1, len(deck.slides) + 1))
        if SLASH_FRACTION.search(all_text) or any(ch in all_text for ch in VULGAR_FRACTIONS):
            _issue(issues, "E_FRACTION_NOTATION", role, "contains slash or vulgar-fraction notation")

    expected_test_fractions: set[tuple[str, str, str]] = set()
    expected_key_fractions: set[tuple[str, str, str]] = set()
    for question in spec.get("questions", []):
        qid = question["id"]
        notation = question.get("notation", {})
        for fraction_id in notation.get("student_fraction_instance_ids", []):
            expected_test_fractions.add((qid, "student", fraction_id))
            expected_key_fractions.add((qid, "student", fraction_id))
        for fraction_id in notation.get("key_fraction_instance_ids", []):
            expected_key_fractions.add((qid, "key", fraction_id))
    _audit_fraction_groups(test, "test", expected_test_fractions, issues)
    _audit_fraction_groups(key, "key", expected_key_fractions, issues)

    for qid, slide_number in (("q7", 2), ("q8", 3)):
        question = next((q for q in spec.get("questions", []) if q.get("id") == qid), {})
        role = question.get("problem_solving", {}).get("supporting_display_role", "none")
        if slide_number <= len(test.table_counts) and test.table_counts[slide_number - 1] and role != "mathematical_evidence":
            _issue(issues, "E_PROSE_FIRST", f"test:{qid}", "table is not authorised as mathematical evidence")

    try:
        page_count, pdf_pages = _extract_pdf(rationale_path)
        expected_pages = package_spec.get("rationale_page_count")
        if page_count != expected_pages:
            _issue(issues, "E_PDF_PAGE_COUNT", "rationale", f"expected {expected_pages} pages, found {page_count}")
        for index, page in enumerate(pdf_pages, start=1):
            if len(page.strip()) < 30:
                _issue(issues, "E_PDF_BLANK", f"rationale:page{index}", "page is blank or contains too little extractable text")
        pdf_text = _norm(" ".join(pdf_pages))
        for token in package_spec.get("rationale_required_tokens", []):
            if _norm(token) not in pdf_text:
                _issue(issues, "E_RATIONALE_TOKEN", "rationale", f"missing required token {token!r}")
        for entry in spec.get("curriculum", []):
            if _norm(entry.get("code", "")) not in pdf_text:
                _issue(issues, "E_RATIONALE_CURRICULUM", "rationale", f"missing curriculum code {entry.get('code')}")
    except (OSError, RuntimeError, ValueError) as exc:
        _issue(issues, "E_PDF", "rationale", str(exc))

    _audit_visual_system(spec, design_manifest_path, issues)
    _audit_ledger(ledger_path, spec_bytes, issues)
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

    report = audit_package(args.spec, args.test, args.key, args.rationale, args.ledger, args.design_manifest)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(report["status"])
    for issue in report["issues"]:
        print(f"{issue['code']} {issue['path']}: {issue['message']}")
    return 0 if report["status"] == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
