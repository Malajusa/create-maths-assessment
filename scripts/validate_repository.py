from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "AGENTS.md",
    "README.md",
    "VERSION",
    "requirements.txt",
    "orchestration/pipeline.json",
    "runtime/controller.py",
    ".github/workflows/validate-skill.yml",
    "scripts/run_regression_fixtures.py",
    "schemas/question-set.schema.json",
    "schemas/approved-question-set.schema.json",
    "schemas/build-manifest.schema.json",
    "fixtures/README.md",
    "standards/assessment-contract.md",
    "standards/maths-conventions.md",
    "standards/exemplar-policy.md",
    "standards/qa-barriers.md",
]
REQUIRED += [f"agents/0{i}-{name}.md" for i, name in [
    (1, "orchestrator-curriculum-resolver"),
    (2, "assessment-blueprint"),
    (3, "question-designer"),
    (4, "complex-problem-specialist"),
    (5, "maths-pedagogy-validator"),
    (6, "document-builder"),
    (7, "release-qa"),
]]

missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    sys.exit(1)

pipeline = json.loads((ROOT / "orchestration/pipeline.json").read_text())
stages = [s["id"] for s in pipeline["stages"]]
if len(stages) != 7 or len(set(stages)) != 7:
    raise SystemExit("Pipeline must contain exactly seven unique stages.")

version = (ROOT / "VERSION").read_text().strip()
if pipeline["version"] != version:
    raise SystemExit("VERSION must match orchestration/pipeline.json version.")
if version != "3.3.0":
    raise SystemExit("Expected v3.3.0 repository contract.")
if not pipeline.get("runtime_enforced"):
    raise SystemExit("Pipeline must declare runtime_enforced=true.")
if pipeline.get("controller") != "runtime/controller.py":
    raise SystemExit("Pipeline controller path is incorrect.")

if pipeline["release_gate"]["pass_status"] != "READY":
    raise SystemExit("Release pass status must be READY.")
if pipeline["release_gate"]["fail_status"] != "NOT READY":
    raise SystemExit("Release fail status must be NOT READY.")
if pipeline["max_targeted_repairs_per_barrier"] != 3:
    raise SystemExit("Repair limit must be 3.")

if pipeline["content_gate"].get("approved_artifact") != "approved_question_set":
    raise SystemExit("Content gate must define approved_question_set as its approved artefact.")

skill = (ROOT / "SKILL.md").read_text()
for phrase in ["Q7 and Q8 are independent", "READY", "NOT READY"]:
    if phrase not in skill:
        raise SystemExit(f"SKILL.md missing required contract phrase: {phrase}")

fixture_files = list((ROOT / "fixtures/failures").glob("*/*.json"))
if len(fixture_files) < 3:
    raise SystemExit("At least three known failure fixtures are required.")

print("Repository validation passed.")
