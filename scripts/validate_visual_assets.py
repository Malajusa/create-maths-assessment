#!/usr/bin/env python3
"""Validate registered maths visual assets and their declared geometry."""

from __future__ import annotations

import hashlib
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "assets/maths-visuals/v1/manifest.json"
SVG_NS = "{http://www.w3.org/2000/svg}"
ALLOWED_LICENCES = {"project-original-distributable", "CC0-1.0"}
FORBIDDEN_TAGS = {"image", "text", "linearGradient", "radialGradient", "filter", "pattern"}
TOLERANCE = 1e-6


def _issue(issues: list[dict[str, str]], code: str, path: str, message: str) -> None:
    issues.append({"code": code, "path": path, "message": message})


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=TOLERANCE, abs_tol=TOLERANCE)


def _float(element: ET.Element, name: str) -> float:
    return float(element.attrib[name])


def _validate_geometry(
    issues: list[dict[str, str]], asset: dict[str, Any], svg_root: ET.Element
) -> None:
    asset_id = str(asset.get("asset_id", "unknown"))
    geometry = asset.get("geometry", {})
    kind = geometry.get("kind")
    parameters = geometry.get("parameters", {})

    if kind == "square":
        elements = svg_root.findall(f"{SVG_NS}rect")
        if len(elements) != 1:
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "square requires one rect")
            return
        rect = elements[0]
        width, height = _float(rect, "width"), _float(rect, "height")
        if not _close(width, height) or not _close(width, float(parameters.get("side", -1))):
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "square sides do not match")
    elif kind == "circle":
        elements = svg_root.findall(f"{SVG_NS}circle")
        if len(elements) != 1:
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "circle requires one circle")
            return
        circle = elements[0]
        if not _close(_float(circle, "r"), float(parameters.get("r", -1))):
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "circle radius does not match")
    elif kind == "equilateral_triangle":
        elements = svg_root.findall(f"{SVG_NS}polygon")
        if len(elements) != 1:
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "triangle requires one polygon")
            return
        points = []
        for pair in elements[0].attrib.get("points", "").split():
            x, y = pair.split(",")
            points.append((float(x), float(y)))
        if len(points) != 3:
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "triangle requires three vertices")
            return
        sides = [_distance(points[i], points[(i + 1) % 3]) for i in range(3)]
        expected = float(parameters.get("side", -1))
        if not all(_close(side, expected) for side in sides):
            _issue(issues, "E_ASSET_GEOMETRY", asset_id, "triangle sides are not equal")
    else:
        _issue(issues, "E_ASSET_GEOMETRY", asset_id, f"unsupported geometry kind {kind!r}")


def validate_manifest_data(root: Path, manifest: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    schema_path = root / "schemas/visual-asset-manifest.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_errors = sorted(
            Draft202012Validator(schema).iter_errors(manifest), key=lambda error: list(error.path)
        )
        for error in schema_errors:
            path = ".".join(str(part) for part in error.path) or "$"
            _issue(issues, "E_ASSET_SCHEMA", path, error.message)
    except (OSError, json.JSONDecodeError) as exc:
        return [{"code": "E_ASSET_SCHEMA", "path": str(schema_path), "message": str(exc)}]

    seen: set[str] = set()
    for asset in manifest.get("assets", []):
        if not isinstance(asset, dict):
            continue
        asset_id = str(asset.get("asset_id", "unknown"))
        if asset_id in seen:
            _issue(issues, "E_ASSET_ID", asset_id, "duplicate asset ID")
        seen.add(asset_id)

        provenance = asset.get("provenance", {})
        if provenance.get("source") != "project_original" or provenance.get("licence") not in ALLOWED_LICENCES:
            _issue(issues, "E_ASSET_LICENCE", asset_id, "asset is not declared distributable")

        asset_path = root / str(asset.get("path", ""))
        try:
            data = asset_path.read_bytes()
        except OSError as exc:
            _issue(issues, "E_ASSET_FILE", asset_id, str(exc))
            continue
        if hashlib.sha256(data).hexdigest() != asset.get("sha256"):
            _issue(issues, "E_ASSET_HASH", asset_id, "SHA-256 does not match")

        try:
            svg_root = ET.fromstring(data)
        except ET.ParseError as exc:
            _issue(issues, "E_ASSET_SVG", asset_id, str(exc))
            continue
        if svg_root.attrib.get("viewBox") != "0 0 1000 1000":
            _issue(issues, "E_ASSET_VIEWBOX", asset_id, "canonical viewBox is required")
        tags = {element.tag.rsplit("}", 1)[-1] for element in svg_root.iter()}
        forbidden = sorted(tags & FORBIDDEN_TAGS)
        if forbidden:
            _issue(issues, "E_ASSET_EFFECT", asset_id, f"forbidden SVG elements: {forbidden}")
        for element in svg_root.iter():
            if "filter" in element.attrib or "style" in element.attrib:
                _issue(issues, "E_ASSET_EFFECT", asset_id, "filters and inline styles are prohibited")
            if element.tag.rsplit("}", 1)[-1] in {"rect", "circle", "polygon"}:
                if element.attrib.get("fill") != "#F8FAFC" or element.attrib.get("stroke") != "#1F2937":
                    _issue(issues, "E_ASSET_TOKEN", asset_id, "fill or stroke does not match tokens")
        _validate_geometry(issues, asset, svg_root)
    return issues


def validate_manifest(root: Path, manifest_path: Path) -> list[dict[str, str]]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [{"code": "E_ASSET_MANIFEST", "path": str(manifest_path), "message": str(exc)}]
    return validate_manifest_data(root, manifest)


def main() -> int:
    issues = validate_manifest(ROOT, DEFAULT_MANIFEST)
    if issues:
        print("Visual asset validation failed.")
        for issue in issues:
            print(f"{issue['code']} {issue['path']}: {issue['message']}")
        return 1
    print("Visual asset validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
