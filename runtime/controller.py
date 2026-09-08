from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class PipelineError(RuntimeError):
    """Raised when a pipeline transition or artefact violates the contract."""


class PipelineController:
    SCHEMAS = {
        "01-orchestrator-curriculum-resolver": "assessment-brief.schema.json",
        "02-assessment-blueprint": "assessment-blueprint.schema.json",
        "03-question-designer": "question-set.schema.json",
        "04-complex-problem-specialist": "question-set.schema.json",
        "05-maths-pedagogy-validator": None,
        "06-document-builder": "build-manifest.schema.json",
        "07-release-qa": "release-status.schema.json",
    }

    def __init__(self, repo_root: Path | str, run_dir: Path | str):
        self.repo_root = Path(repo_root).resolve()
        self.run_dir = Path(run_dir).resolve()
        self.pipeline = self._load_json(self.repo_root / "orchestration/pipeline.json")
        self.stage_ids = [stage["id"] for stage in self.pipeline["stages"]]
        self.state_path = self.run_dir / "state.json"
        self.artifact_dir = self.run_dir / "artifacts"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        if self.state_path.exists():
            self.state = self._load_json(self.state_path)
            if self.state.get("pipeline_version") != self.pipeline["version"]:
                raise PipelineError("run state pipeline version does not match repository pipeline version")
        else:
            self.state = {
                "pipeline_version": self.pipeline["version"],
                "completed_stages": [],
                "artifacts": {},
                "blocked_gate": None,
                "release_status": None,
                "repair_counts": {},
                "open_issues": [],
            }
            self._save_state()

    @staticmethod
    def _load_json(path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_state(self) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.state_path)

    @property
    def expected_stage(self) -> str | None:
        completed = len(self.state["completed_stages"])
        return self.stage_ids[completed] if completed < len(self.stage_ids) else None

    def _validate_schema(self, schema_name: str, payload: Any) -> None:
        schema_path = (self.repo_root / "schemas" / schema_name).resolve()
        schema = self._load_json(schema_path)
        # Give schemas a file URI at validation time so relative $ref values
        # (for example ./question.schema.json) resolve deterministically.
        effective_schema = dict(schema)
        effective_schema.setdefault("$id", schema_path.as_uri())
        registry = Registry()
        for candidate in (self.repo_root / "schemas").glob("*.json"):
            contents = self._load_json(candidate)
            registry = registry.with_resource(candidate.resolve().as_uri(), Resource.from_contents(contents))
        validator = Draft202012Validator(effective_schema, registry=registry)
        errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
        if errors:
            detail = "; ".join(error.message for error in errors[:3])
            raise PipelineError(f"schema validation failed: {detail}")

    def _validate_questions(self, payload: dict[str, Any], expected_ids: list[str]) -> None:
        questions = payload.get("questions", [])
        ids = [question.get("id") for question in questions]
        if ids != expected_ids:
            raise PipelineError(f"question set must contain {', '.join(expected_ids)} in order")
        question_schema = self._load_json(self.repo_root / "schemas/question.schema.json")
        validator = Draft202012Validator(question_schema)
        for question in questions:
            errors = sorted(validator.iter_errors(question), key=lambda e: list(e.path))
            if errors:
                detail = "; ".join(error.message for error in errors[:3])
                raise PipelineError(f"schema validation failed for {question.get('id', 'question')}: {detail}")

    def validate_stage_payload(self, stage_id: str, payload: Any) -> None:
        if stage_id not in self.SCHEMAS:
            raise PipelineError(f"unknown stage: {stage_id}")
        if stage_id != "05-maths-pedagogy-validator":
            self._validate_schema(self.SCHEMAS[stage_id], payload)

        if stage_id == "02-assessment-blueprint":
            marks = sum(question["marks"] for question in payload["questions"])
            if marks != payload["total_marks"]:
                raise PipelineError("blueprint total_marks must equal the sum of question marks")

        if stage_id == "03-question-designer":
            self._validate_questions(payload, [f"Q{i}" for i in range(1, 7)])

        if stage_id == "04-complex-problem-specialist":
            self._validate_questions(payload, ["Q7", "Q8"])
            q8 = payload["questions"][1]
            if "Q7" in q8.get("depends_on", []):
                raise PipelineError("Q8 must be independent of Q7")

        if stage_id == "05-maths-pedagogy-validator":
            if not isinstance(payload, dict) or "content_validation" not in payload:
                raise PipelineError("Agent 05 output requires content_validation")
            validation = payload["content_validation"]
            self._validate_schema("validation.schema.json", validation)
            status = validation["status"]
            issues = validation["issues"]
            approved = payload.get("approved_question_set")
            if status == "PASS" and issues:
                raise PipelineError("content PASS requires zero issues")
            if status == "FAIL" and not issues:
                raise PipelineError("content FAIL requires at least one issue")
            if status == "PASS" and approved is None:
                raise PipelineError("content PASS requires approved_question_set")
            if status == "FAIL" and approved is not None:
                raise PipelineError("content FAIL must not emit approved_question_set")
            if approved is not None:
                self._validate_schema("approved-question-set.schema.json", approved)
                ids = [question.get("id") for question in approved["questions"]]
                if ids != [f"Q{i}" for i in range(1, 9)]:
                    raise PipelineError("approved_question_set must contain Q1-Q8 in order")

        if stage_id == "06-document-builder":
            test_hash = payload["student_test"]["sha256"]
            key = payload["marking_key"]
            if not key.get("derived_from_test"):
                raise PipelineError("marking key must be derived from the final student test")
            if key.get("source_test_sha256") != test_hash:
                raise PipelineError("marking key source hash must equal student test hash")

        if stage_id == "07-release-qa":
            count = payload["open_barrier_count"]
            barriers = payload["barriers"]
            if count != len(barriers):
                raise PipelineError("open_barrier_count must equal the number of barriers")
            if payload["status"] == "READY" and (count != 0 or barriers):
                raise PipelineError("READY requires zero open barriers")
            if payload["status"] == "NOT READY" and count == 0:
                raise PipelineError("NOT READY requires at least one open barrier")

    def _validate_approved_question_set_against_drafts(self, payload: Any) -> None:
        if "approved_question_set" not in payload:
            return
        q1_q6_path = self.state["artifacts"].get("03-question-designer")
        q7_q8_path = self.state["artifacts"].get("04-complex-problem-specialist")
        if not q1_q6_path or not q7_q8_path:
            raise PipelineError("approved_question_set requires recorded Q1-Q8 drafts")
        q1_q6 = self._load_json(self.run_dir / q1_q6_path)["questions"]
        q7_q8 = self._load_json(self.run_dir / q7_q8_path)["questions"]
        if payload["approved_question_set"]["questions"] != q1_q6 + q7_q8:
            raise PipelineError("approved_question_set must exactly match the validated Q1-Q8 drafts")

    def _validate_against_blueprint(self, stage_id: str, payload: Any) -> None:
        if stage_id not in {"03-question-designer", "04-complex-problem-specialist"}:
            return
        blueprint_path = self.state["artifacts"].get("02-assessment-blueprint")
        if not blueprint_path:
            return
        blueprint = self._load_json(self.run_dir / blueprint_path)
        expected = {q["id"]: q["marks"] for q in blueprint["questions"]}
        for question in payload["questions"]:
            qid = question["id"]
            if qid not in expected:
                raise PipelineError(f"{qid} is not present in the approved blueprint")
            if question["marks"] != expected[qid]:
                raise PipelineError(f"{qid} marks do not match the approved blueprint")

    def record(self, stage_id: str, payload: Any) -> None:
        if self.state["blocked_gate"] == "content" and stage_id == "06-document-builder":
            raise PipelineError("content gate is blocked; repair and revalidate before document build")
        expected = self.expected_stage
        if stage_id != expected:
            raise PipelineError(f"cannot record {stage_id}; expected stage {expected}")

        self.validate_stage_payload(stage_id, payload)
        self._validate_against_blueprint(stage_id, payload)
        if stage_id == "05-maths-pedagogy-validator":
            self._validate_approved_question_set_against_drafts(payload)

        artifact_path = self.artifact_dir / f"{stage_id}.json"
        artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        relative = artifact_path.relative_to(self.run_dir).as_posix()
        self.state["artifacts"][stage_id] = relative
        self.state["completed_stages"].append(stage_id)

        if stage_id == "05-maths-pedagogy-validator":
            validation = payload["content_validation"]
            self.state["open_issues"] = validation["issues"]
            self.state["blocked_gate"] = None if validation["status"] == "PASS" else "content"

        if stage_id == "07-release-qa":
            self.state["release_status"] = payload["status"]
            self.state["open_issues"] = payload["barriers"]
            self.state["blocked_gate"] = None if payload["status"] == "READY" else "release"

        self._save_state()

    def repair(self, issue_id: str, replacement_payload: Any) -> None:
        issues = {issue["id"]: issue for issue in self.state.get("open_issues", [])}
        if issue_id not in issues:
            raise PipelineError(f"unknown open issue: {issue_id}")
        owner = issues[issue_id]["owner"]
        if owner not in self.stage_ids:
            raise PipelineError(f"repair owner is not an executable pipeline stage: {owner}")

        attempts = self.state["repair_counts"].get(issue_id, 0) + 1
        maximum = self.pipeline["max_targeted_repairs_per_barrier"]
        if attempts > maximum:
            raise PipelineError("targeted repair limit exceeded; replace the approach")
        self.state["repair_counts"][issue_id] = attempts

        owner_index = self.stage_ids.index(owner)
        completed = self.state["completed_stages"]
        self.state["completed_stages"] = [s for s in completed if self.stage_ids.index(s) < owner_index]
        for stage in list(self.state["artifacts"]):
            if self.stage_ids.index(stage) >= owner_index:
                del self.state["artifacts"][stage]
        self.state["blocked_gate"] = None
        self.state["release_status"] = None
        self.state["open_issues"] = []
        self._save_state()
        self.record(owner, replacement_payload)


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Enforce the Create Maths Assessment agent pipeline")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--run-dir", required=True)
    sub = parser.add_subparsers(dest="command", required=True)

    rec = sub.add_parser("record")
    rec.add_argument("stage")
    rec.add_argument("artifact")

    val = sub.add_parser("validate")
    val.add_argument("stage")
    val.add_argument("artifact")

    rep = sub.add_parser("repair")
    rep.add_argument("issue_id")
    rep.add_argument("artifact")

    sub.add_parser("status")

    args = parser.parse_args()
    ctl = PipelineController(args.repo, args.run_dir)
    try:
        if args.command == "record":
            ctl.record(args.stage, json.loads(Path(args.artifact).read_text()))
        elif args.command == "validate":
            ctl.validate_stage_payload(args.stage, json.loads(Path(args.artifact).read_text()))
        elif args.command == "repair":
            ctl.repair(args.issue_id, json.loads(Path(args.artifact).read_text()))
        elif args.command == "status":
            print(json.dumps(ctl.state, indent=2))
    except PipelineError as exc:
        print(f"ERROR: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
