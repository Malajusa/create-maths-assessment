#!/usr/bin/env python3
"""Canonical criterion evidence envelope for Years 3–10 component estimates."""

from __future__ import annotations

from itertools import product

BANDS = ("D", "C", "B", "A")
DEFAULT_QUESTION_MARKS = {
    "q1": 1,
    "q2": 1,
    "q3": 1,
    "q4": 2,
    "q5": 4,
    "q6": 5,
    "q7": 5,
    "q8": 6,
}
DEFAULT_EVIDENCE_ENVELOPE = {"D": 5, "C": 8, "B": 5, "A": 7}
DEFAULT_INDICATIVE_CUTS = {"D": 5, "C": 10, "B": 16, "A": 21}
DEFAULT_INDICATIVE_BANDS = {
    "E": (0, 4),
    "D": (5, 9),
    "C": (10, 15),
    "B": (16, 20),
    "A": (21, 25),
}
MIN_FORCED_TARGET_EVIDENCE = {"C": 5, "B": 3, "A": 3}
A_DEMAND_FEATURES = {
    "inference",
    "adaptation",
    "interacting_constraints",
    "evaluation",
    "sustained_reasoning",
    "justification",
}


def classify_score(score: int) -> str:
    """Return the indicative component band for a canonical 25-mark score."""
    if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 25:
        raise ValueError("score must be an integer from 0 to 25")
    for band, (minimum, maximum) in DEFAULT_INDICATIVE_BANDS.items():
        if minimum <= score <= maximum:
            return band
    raise AssertionError("canonical score bands must cover 0 to 25")


def forced_target_evidence(target_band: str) -> int:
    """Return the minimum target-or-higher marks forced by the target cut score."""
    if target_band not in {"C", "B", "A"}:
        raise ValueError("target_band must be C, B or A")
    target_index = BANDS.index(target_band)
    lower_total = sum(DEFAULT_EVIDENCE_ENVELOPE[band] for band in BANDS[:target_index])
    return DEFAULT_INDICATIVE_CUTS[target_band] - lower_total


def validate_canonical_structure() -> list[str]:
    """Return invariant violations for the canonical envelope and every earned-mark profile."""
    issues: list[str] = []
    if sum(DEFAULT_QUESTION_MARKS.values()) != 25:
        issues.append("default question marks must total 25")
    if sum(DEFAULT_EVIDENCE_ENVELOPE.values()) != 25:
        issues.append("default evidence envelope must total 25")
    for band, minimum in MIN_FORCED_TARGET_EVIDENCE.items():
        if forced_target_evidence(band) < minimum:
            issues.append(f"{band} boundary forces too little target evidence")

    previous = None
    for score in range(26):
        current = "EDCBA".index(classify_score(score))
        if previous is not None and current < previous:
            issues.append(f"score classification is not monotonic at {score}")
        previous = current

    for d, c, b, a in product(range(6), range(9), range(6), range(8)):
        score = d + c + b + a
        grade = classify_score(score)
        if grade in {"C", "B", "A"} and c + b + a < MIN_FORCED_TARGET_EVIDENCE["C"]:
            issues.append(f"profile {(d, c, b, a)} reaches {grade} without enough C+ evidence")
            break
        if grade in {"B", "A"} and b + a < MIN_FORCED_TARGET_EVIDENCE["B"]:
            issues.append(f"profile {(d, c, b, a)} reaches {grade} without enough B+ evidence")
            break
        if grade == "A" and a < MIN_FORCED_TARGET_EVIDENCE["A"]:
            issues.append(f"profile {(d, c, b, a)} reaches A without enough A evidence")
            break
    return issues
