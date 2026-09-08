---
name: create-maths-assessment
description: Use when creating, revising, adapting, validating, or producing marking keys and curriculum rationales for primary mathematics assessments, especially Western Australian classroom assessments.
---

# Create Maths Assessment

## Core rule

Assessment generation is a gated pipeline. A generating agent must never certify its own work, and no required QA issue is advisory.

## Required workflow

1. **Resolve** the request with `agents/01-orchestrator-curriculum-resolver.md`.
2. **Blueprint** the assessment with `agents/02-assessment-blueprint.md`.
3. **Generate Q1–Q6** with `agents/03-question-designer.md`.
4. **Generate Q7–Q8** independently with `agents/04-complex-problem-specialist.md`.
5. **Validate content** with `agents/05-maths-pedagogy-validator.md`. A passing validation emits `approved_question_set`; a failing validation must not.
6. If validation fails, repair only the owning stage, then revalidate.
7. **Build all documents** with `agents/06-document-builder.md`, using `approved_question_set` as the assessment-content source of truth.
8. **Independently release-test** with `agents/07-release-qa.md` against the brief, blueprint, approved question set and rendered artefacts.
9. Release only when the status is exactly `READY`.

Read `orchestration/pipeline.json` for routing and retry rules.

## Canonical standards

Before producing content, load:

- `standards/assessment-contract.md`
- `standards/maths-conventions.md`
- `standards/exemplar-policy.md`
- `standards/qa-barriers.md`

Explicit user instructions override defaults. Current canonical standards override older exemplars where they conflict.

## Default assessment structure

Unless the task explicitly requires another structure:

| Question | Marks |
|---|---:|
| Q1 | 1 |
| Q2 | 1 |
| Q3 | 2 |
| Q4 | 2 |
| Q5 | 3 |
| Q6 | 3 |
| Q7 | 4 |
| Q8 | 4 |

Total: **20 marks**.

Q7 and Q8 are independent complex problems. Q8 must not depend on, extend, or scaffold from Q7.

## Release law

Any identified required defect means `NOT READY`.

Do not use:
- “ready with minor changes”;
- “mostly ready”;
- “acceptable with fixes”.

A repair invalidates downstream validation for every artefact affected by that repair.

## Executable enforcement

When Python execution is available, the runtime controller is mandatory. Create a run directory and record every stage through `runtime/controller.py`; do not treat free-form agent hand-offs as authoritative state.

Typical usage:

```bash
python -m runtime.controller --run-dir run/current record 01-orchestrator-curriculum-resolver run/01-brief.json
python -m runtime.controller --run-dir run/current status
```

The controller validates schemas, stage order, content/release gates, Q7/Q8 independence and Student Test → Marking Key provenance. A controller rejection is a barrier and cannot be bypassed by an agent's qualitative judgement.
