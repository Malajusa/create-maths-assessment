from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "AGENTS.md",
    "README.md",
    "VERSION",
    "orchestration/pipeline.json",
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

if pipeline["release_gate"]["pass_status"] != "READY":
    raise SystemExit("Release pass status must be READY.")
if pipeline["release_gate"]["fail_status"] != "NOT READY":
    raise SystemExit("Release fail status must be NOT READY.")
if pipeline["max_targeted_repairs_per_barrier"] != 3:
    raise SystemExit("Repair limit must be 3.")

skill = (ROOT / "SKILL.md").read_text()
for phrase in ["Q7 and Q8 are independent", "READY", "NOT READY"]:
    if phrase not in skill:
        raise SystemExit(f"SKILL.md missing required contract phrase: {phrase}")

print("Repository validation passed.")
