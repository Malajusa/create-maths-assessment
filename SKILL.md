---
name: create-maths-assessment
description: Create, revise, review or mark curriculum-aligned mathematics assessments in Mr Leahy's preferred 20-mark format, including an A4 portrait PowerPoint test, duplicate worked marking key and curriculum-rationale PDF, using a fail-closed multi-agent pipeline for Western Australian classroom assessment.
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

## Required production references

Load references progressively, but never omit a reference required for the current stage:

- Every task: `references/assessment-format.md` and `references/curriculum-index.md`, followed by only the curriculum file for each assessed year level.
- Creation, revision or review: `references/assessment-quality-gates.md`.
- Creation or revision: `references/assessment-production-contract.md`.
- Q7 or Q8 drafting/review: `references/q7-q8-problem-solving-standard.md` and `references/q7-q8-demand-2025.md`.
- Any PowerPoint deliverable: `references/powerpoint-output.md`.
- Any diagram, geometric figure, graph, number line or labelled shape: `references/mathematical-diagram-conventions.md`.

Task-specific curriculum documents supplied by the user override bundled curriculum references. Preserve curriculum codes and scope exactly; do not invent, merge or silently alter them.

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

Run the deterministic production validators where applicable:

```bash
python scripts/validate_assessment_spec.py <assessment-spec.json>
python scripts/audit_assessment_package.py <assessment-spec.json>
```

Use `assets/` and `examples/benchmarks/` only for the quality dimensions assigned to them. An exemplar never overrides the current user request, curriculum or canonical standards.
