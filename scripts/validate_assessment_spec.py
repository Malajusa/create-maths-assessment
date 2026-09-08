#!/usr/bin/env python3
"""Fail-closed preflight validation for create-maths-assessment specifications."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


QUESTION_IDS = [f"q{i}" for i in range(1, 9)]
EXPECTED_MARKS = dict(zip(QUESTION_IDS, [1, 1, 2, 2, 3, 3, 4, 4]))
EXPECTED_POSITIONS = {
    "q1": "top_left",
    "q2": "top_right",
    "q3": "middle_left",
    "q4": "middle_right",
    "q5": "bottom_left",
    "q6": "bottom_right",
}
REVIEW_ASSERTIONS = {
    "clear_to_student",
    "natural_read_aloud",
    "stem_does_not_supply_answer",
    "solution_independently_verified",
    "mark_value_proportional",
}
RESPONSE_KINDS = {
    "blank_unlined",
    "compact_final_answer",
    "structured_mathematical",
    "none",
}
DEMAND_FEATURES = {
    "interacting_constraints",
    "different_information_forms",
    "inference",
    "dependent_result",
    "reverse_process",
    "connected_concepts",
    "unfamiliar_fair_application",
    "comparison_or_evaluation",
    "reasonableness_check",
    "justification",
}
DEPENDENCY_FEATURES = {"interacting_constraints", "inference", "dependent_result"}
VULGAR_FRACTIONS = set("¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞")
SLASH_FRACTION = re.compile(r"(?<!\w)\d+\s*[⁄/]\s*\d+(?!\w)")
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _error(errors: list[dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append({"code": code, "path": path, "message": message})


def _require_text(
    errors: list[dict[str, str]], value: Any, path: str, code: str = "E_REQUIRED"
) -> str:
    result = _text(value)
    if not result:
        _error(errors, code, path, "must be a non-empty string")
    return result


def _contains_banned_fraction_notation(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return bool(SLASH_FRACTION.search(value) or any(ch in value for ch in VULGAR_FRACTIONS))


def validate_spec(spec: Any) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(spec, dict):
        return [{"code": "E_ROOT", "path": "$", "message": "root must be an object"}]

    if spec.get("schema_version") != 1:
        _error(errors, "E_SCHEMA", "schema_version", "must equal 1")

    assessment = _dict(spec.get("assessment"))
    _require_text(errors, assessment.get("title"), "assessment.title")
    year_levels = _list(assessment.get("year_levels"))
    if not year_levels or any(not isinstance(y, int) for y in year_levels):
        _error(errors, "E_YEAR", "assessment.year_levels", "must contain assessed integer year levels")
    for index, raw_variation in enumerate(_list(assessment.get("authorised_variations"))):
        path = f"assessment.authorised_variations[{index}]"
        variation = _dict(raw_variation)
        if _text(variation.get("source")) != "user":
            _error(errors, "E_VARIATION", f"{path}.source", "must record user authorisation")
        _require_text(errors, variation.get("statement"), f"{path}.statement", "E_VARIATION")
        variation_qids = _list(variation.get("question_ids"))
        if not variation_qids or any(qid not in QUESTION_IDS for qid in variation_qids):
            _error(errors, "E_VARIATION", f"{path}.question_ids", "must list valid affected questions")

    curriculum = _list(spec.get("curriculum"))
    curriculum_by_code: dict[str, dict[str, Any]] = {}
    if not curriculum:
        _error(errors, "E_CURRICULUM", "curriculum", "must contain at least one curriculum entry")
    for index, raw_entry in enumerate(curriculum):
        path = f"curriculum[{index}]"
        entry = _dict(raw_entry)
        code = _require_text(errors, entry.get("code"), f"{path}.code", "E_CURRICULUM")
        if code in curriculum_by_code:
            _error(errors, "E_CURRICULUM_DUPLICATE", f"{path}.code", f"duplicate code {code}")
        if code:
            curriculum_by_code[code] = entry
        _require_text(errors, entry.get("description"), f"{path}.description", "E_CURRICULUM")
        level = entry.get("year_level")
        if not isinstance(level, int):
            _error(errors, "E_CURRICULUM", f"{path}.year_level", "must be an integer")
        alignment = entry.get("alignment")
        if alignment not in {"direct", "authorised_extension"}:
            _error(errors, "E_EXTENSION", f"{path}.alignment", "must be direct or authorised_extension")
        if alignment == "direct" and level not in year_levels:
            _error(errors, "E_EXTENSION", path, "direct curriculum year must be an assessed year level")
        if alignment == "authorised_extension":
            authorisation = _dict(entry.get("authorisation"))
            if _text(authorisation.get("source")) != "user":
                _error(errors, "E_EXTENSION", f"{path}.authorisation.source", "must record user authorisation")
            _require_text(
                errors,
                authorisation.get("statement"),
                f"{path}.authorisation.statement",
                "E_EXTENSION",
            )
            qids = _list(authorisation.get("question_ids"))
            if not qids or any(q not in QUESTION_IDS for q in qids):
                _error(errors, "E_EXTENSION", f"{path}.authorisation.question_ids", "must list valid affected questions")

    marks = _dict(spec.get("marks"))
    if marks.get("total") != 20:
        _error(errors, "E_MARK_TOTAL", "marks.total", "must equal 20")
    topic_subtotals = _dict(marks.get("topic_subtotals"))
    if not topic_subtotals or any(not isinstance(v, int) or v <= 0 for v in topic_subtotals.values()):
        _error(errors, "E_TOPIC_TOTAL", "marks.topic_subtotals", "must contain positive integer subtotals")
    elif sum(topic_subtotals.values()) != marks.get("total"):
        _error(errors, "E_TOPIC_TOTAL", "marks.topic_subtotals", "subtotals must equal the assessment total")

    layout = _dict(spec.get("page_layout"))
    if layout.get("slide_count") != 3 or layout.get("a4_portrait") is not True:
        _error(errors, "E_LAYOUT", "page_layout", "must specify three A4 portrait slides")
    if _dict(layout.get("page1_positions")) != EXPECTED_POSITIONS:
        _error(errors, "E_LAYOUT", "page_layout.page1_positions", "must use exact 1–2 / 3–4 / 5–6 positions")
    if layout.get("page2_question") != "q7" or layout.get("page3_question") != "q8":
        _error(errors, "E_LAYOUT", "page_layout", "Q7 must be Page 2 and Q8 must be Page 3")

    questions = _list(spec.get("questions"))
    found_ids = [q.get("id") for q in questions if isinstance(q, dict)]
    if found_ids != QUESTION_IDS:
        _error(errors, "E_QUESTIONS", "questions", "must contain Q1-Q8 once and in order")

    calculated_topics: dict[str, int] = {}
    for index, raw_question in enumerate(questions):
        q = _dict(raw_question)
        qid = _text(q.get("id")) or f"questions[{index}]"
        path = f"questions[{index}]"
        expected_marks = EXPECTED_MARKS.get(qid)
        if q.get("marks") != expected_marks:
            _error(errors, "E_MARK_SEQUENCE", f"{path}.marks", f"{qid.upper()} must have {expected_marks} marks")
        topic = _require_text(errors, q.get("topic"), f"{path}.topic")
        if topic and isinstance(q.get("marks"), int):
            calculated_topics[topic] = calculated_topics.get(topic, 0) + q["marks"]

        q_codes = _list(q.get("curriculum_codes"))
        if not q_codes:
            _error(errors, "E_CURRICULUM", f"{path}.curriculum_codes", "must identify assessed curriculum")
        for code in q_codes:
            if code not in curriculum_by_code:
                _error(errors, "E_CURRICULUM", f"{path}.curriculum_codes", f"unknown code {code}")
            elif curriculum_by_code[code].get("alignment") == "authorised_extension":
                authorised_qids = _list(_dict(curriculum_by_code[code].get("authorisation")).get("question_ids"))
                if qid not in authorised_qids:
                    _error(errors, "E_EXTENSION", f"{path}.curriculum_codes", f"{code} is not authorised for {qid}")

        for field in (
            "prompt",
            "answer",
            "student_task_restatement",
            "mathematical_action",
            "diagnostic_purpose",
        ):
            value = _require_text(errors, q.get(field), f"{path}.{field}")
            if _contains_banned_fraction_notation(value):
                _error(errors, "E_FRACTION_NOTATION", f"{path}.{field}", "contains slash or vulgar-fraction notation")

        solution_steps = _list(q.get("solution_steps"))
        if not solution_steps or any(not _text(step) for step in solution_steps):
            _error(errors, "E_SOLUTION", f"{path}.solution_steps", "must contain an independently checked solution path")
        for step_index, step in enumerate(solution_steps):
            if _contains_banned_fraction_notation(step):
                _error(errors, "E_FRACTION_NOTATION", f"{path}.solution_steps[{step_index}]", "contains banned fraction notation")

        observable = [_text(item) for item in _list(q.get("observable_evidence"))]
        if not observable or any(not item for item in observable):
            _error(errors, "E_EVIDENCE", f"{path}.observable_evidence", "must list observable evidence")

        mark_evidence = _list(q.get("mark_evidence"))
        mark_numbers: list[int] = []
        evidence_texts: list[str] = []
        for mark_index, raw_mark in enumerate(mark_evidence):
            mark = _dict(raw_mark)
            mark_numbers.append(mark.get("mark"))
            evidence = _require_text(
                errors, mark.get("evidence"), f"{path}.mark_evidence[{mark_index}].evidence", "E_MARK_EVIDENCE"
            )
            if evidence:
                evidence_texts.append(re.sub(r"\W+", " ", evidence.lower()).strip())
        if mark_numbers != list(range(1, (expected_marks or 0) + 1)):
            _error(errors, "E_MARK_EVIDENCE", f"{path}.mark_evidence", "must contain one ordered entry for every mark")
        if len(evidence_texts) != len(set(evidence_texts)):
            _error(errors, "E_MARK_EVIDENCE_DUPLICATE", f"{path}.mark_evidence", "contains duplicated mark evidence")

        assertions = _dict(q.get("review_assertions"))
        for assertion in sorted(REVIEW_ASSERTIONS):
            if assertions.get(assertion) is not True:
                _error(errors, "E_REVIEW_ASSERTION", f"{path}.review_assertions.{assertion}", "must be explicitly verified true")

        response = _dict(q.get("response_space"))
        response_kind = response.get("kind")
        if response_kind not in RESPONSE_KINDS:
            _error(errors, "E_RESPONSE_SPACE", f"{path}.response_space.kind", "has an unsupported response-space type")
        labels = _list(response.get("labels"))
        justification = _text(response.get("mathematical_justification"))
        if response_kind in {"compact_final_answer", "structured_mathematical"} and not justification:
            _error(errors, "E_RESPONSE_SCAFFOLD", f"{path}.response_space.mathematical_justification", "structured response space requires a mathematical justification")
        if labels and not justification:
            _error(errors, "E_RESPONSE_SCAFFOLD", f"{path}.response_space.labels", "every response label requires a mathematical justification")
        if response_kind in {"blank_unlined", "none"} and labels:
            _error(errors, "E_RESPONSE_SCAFFOLD", f"{path}.response_space.labels", "blank or absent response space must not carry labels")
        if any(not _text(label) for label in labels):
            _error(errors, "E_RESPONSE_SPACE", f"{path}.response_space.labels", "labels must be non-empty strings")

        representation = _dict(q.get("representation"))
        representation_required = representation.get("required")
        representation_kind = _text(representation.get("kind"))
        representation_purpose = _text(representation.get("mathematical_purpose"))
        omission_reason = _text(representation.get("omission_reason"))
        representation_ids = _list(representation.get("instance_ids"))
        if any(not isinstance(item, str) or not SAFE_ID.fullmatch(item) for item in representation_ids):
            _error(errors, "E_REPRESENTATION", f"{path}.representation.instance_ids", "representation IDs must use lowercase letters, digits, underscores or hyphens")
        if len(representation_ids) != len(set(representation_ids)):
            _error(errors, "E_REPRESENTATION", f"{path}.representation.instance_ids", "representation IDs must be unique within a question")
        if not isinstance(representation_required, bool):
            _error(errors, "E_REPRESENTATION", f"{path}.representation.required", "must be true or false")
        elif representation_required:
            if not representation_kind or representation_kind == "none" or not representation_purpose or not representation_ids:
                _error(errors, "E_REPRESENTATION", f"{path}.representation", "required representation needs a kind, mathematical purpose and named instance")
        else:
            if not omission_reason:
                _error(errors, "E_REPRESENTATION", f"{path}.representation.omission_reason", "omitted representation needs a reason")
            if representation_ids:
                _error(errors, "E_REPRESENTATION", f"{path}.representation.instance_ids", "omitted representation must not declare instances")
        if q.get("topic_kind") == "fractions" and qid in QUESTION_IDS[:6] and representation_required is not True:
            _error(errors, "E_FRACTION_VISUAL", f"{path}.representation", "fraction questions Q1-Q6 require a purposeful visual model")

        notation = _dict(q.get("notation"))
        student_fraction_ids = _list(notation.get("student_fraction_instance_ids"))
        key_fraction_ids = _list(notation.get("key_fraction_instance_ids"))
        all_fraction_ids = student_fraction_ids + key_fraction_ids
        if any(not isinstance(item, str) or not SAFE_ID.fullmatch(item) for item in all_fraction_ids):
            _error(errors, "E_FRACTION_INSTANCE", f"{path}.notation", "fraction instance IDs must use lowercase letters, digits, underscores or hyphens")
        if len(all_fraction_ids) != len(set(all_fraction_ids)):
            _error(errors, "E_FRACTION_INSTANCE", f"{path}.notation", "fraction instance IDs must be unique within a question")
        if q.get("contains_symbolic_fraction") is True and not all_fraction_ids:
            _error(errors, "E_FRACTION_INSTANCE", f"{path}.notation", "symbolic fractions require named fraction instances")
        if q.get("contains_symbolic_fraction") not in {True, False}:
            _error(errors, "E_FRACTION_INSTANCE", f"{path}.contains_symbolic_fraction", "must be true or false")

        prompt_tokens = _list(q.get("prompt_audit_tokens"))
        if not prompt_tokens or any(not _text(token) for token in prompt_tokens):
            _error(errors, "E_AUDIT_TOKEN", f"{path}.prompt_audit_tokens", "must contain stable prompt tokens")

        if qid in {"q7", "q8"}:
            problem = _dict(q.get("problem_solving"))
            if problem.get("prose_first") is not True or problem.get("information_source") != "sentences":
                _error(errors, "E_PROSE_FIRST", f"{path}.problem_solving", "must be prose-first with information extracted from sentences")
            if problem.get("independent") is not True:
                _error(errors, "E_INDEPENDENCE", f"{path}.problem_solving.independent", "must be an independent problem")
            if problem.get("preorganised_solution_display") is not False:
                _error(errors, "E_PROSE_FIRST", f"{path}.problem_solving.preorganised_solution_display", "must be false")
            if problem.get("supporting_display_role") not in {"none", "mathematical_evidence"}:
                _error(errors, "E_PROSE_FIRST", f"{path}.problem_solving.supporting_display_role", "must be none or mathematical_evidence")
            extracted = _list(problem.get("extracted_information"))
            if len(extracted) < 2 or any(not _text(item) for item in extracted):
                _error(errors, "E_PROSE_FIRST", f"{path}.problem_solving.extracted_information", "must identify at least two pieces of prose information")
            features = _list(problem.get("demand_features"))
            if any(feature not in DEMAND_FEATURES for feature in features):
                _error(errors, "E_DEMAND", f"{path}.problem_solving.demand_features", "contains an unsupported demand feature")
            minimum = 1 if qid == "q7" else 3
            if len(set(features)) < minimum:
                _error(errors, "E_DEMAND", f"{path}.problem_solving.demand_features", f"{qid.upper()} requires at least {minimum} distinct demand features")
            if qid == "q8" and not DEPENDENCY_FEATURES.intersection(features):
                _error(errors, "E_Q8_DEPENDENCY", f"{path}.problem_solving.demand_features", "Q8 requires inference, a dependent result or interacting constraints")
            if problem.get("justified_conclusion") is not True:
                _error(errors, "E_DEMAND", f"{path}.problem_solving.justified_conclusion", "must require a justified conclusion")

    if calculated_topics != topic_subtotals:
        _error(errors, "E_TOPIC_TOTAL", "marks.topic_subtotals", f"declared subtotals {topic_subtotals} do not match questions {calculated_topics}")

    package = _dict(spec.get("package"))
    if package.get("test_slide_count") != 3 or package.get("key_slide_count") != 3:
        _error(errors, "E_PACKAGE", "package", "test and key must each have three slides")
    if not isinstance(package.get("rationale_page_count"), int) or package.get("rationale_page_count") < 1:
        _error(errors, "E_PACKAGE", "package.rationale_page_count", "must be a positive integer")
    rationale_tokens = _list(package.get("rationale_required_tokens"))
    if not rationale_tokens or any(not _text(token) for token in rationale_tokens):
        _error(errors, "E_AUDIT_TOKEN", "package.rationale_required_tokens", "must contain stable rationale tokens")

    return errors


def load_spec(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    try:
        spec = load_spec(args.spec)
        errors = validate_spec(spec)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [{"code": "E_INPUT", "path": str(args.spec), "message": str(exc)}]

    report = {"status": "READY" if not errors else "NOT READY", "errors": errors}
    if args.as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif errors:
        print("NOT READY")
        for item in errors:
            print(f"{item['code']} {item['path']}: {item['message']}")
    else:
        print("READY")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
