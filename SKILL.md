---
name: create-maths-assessment
description: Use when creating, revising, reviewing or marking Western Australian mathematics assessments, including equivalent versions and marking keys for an exact supplied assessment.
---

# Create Maths Assessment

## Core rule

Assessment generation is a gated pipeline. A generating agent must never certify its own work, and no required QA issue is advisory. Read `standards/project-context.md` to preserve the project's agreed decisions without turning task-specific corrections into universal rules.

For new Years 3–10 grade-estimating assessments, use `references/evidence-band-standard.md`. The assessment is engineered so its raw score provides an **indicative standard on the assessed component**. It is not a semester/reporting-grade allocation system.

## Required workflow

1. **Resolve** the request with `agents/01-orchestrator-curriculum-resolver.md`.
2. **Blueprint** the assessment with `agents/02-assessment-blueprint.md`.
3. **Generate Q1–Q6** with `agents/03-question-designer.md`.
4. **Generate Q7–Q8** independently with `agents/04-complex-problem-specialist.md`.
5. **Validate content** with `agents/05-maths-pedagogy-validator.md`. A passing validation emits `approved_question_set`; a failing validation must not.
6. If validation fails, repair only the owning stage, preserve unaffected sibling questions and revalidate affected descendants.
7. **Build all requested documents** with `agents/06-document-builder.md`, using `approved_question_set` as the assessment-content source of truth. For a key-only request, use the exact supplied assessment; do not replace it with a remembered version.
8. **Independently release-test** with `agents/07-release-qa.md` against the brief, blueprint, approved question set and every rendered page. Follow `standards/release-evidence.md`.
9. Release only when the current controller status is exactly `READY`, with verified files and evidence. Missing capability or evidence means `NOT READY`, not an invented pass.

Read `orchestration/pipeline.json` for routing and retry rules. Role labels alone do not establish independent agent execution.

## Required production references

Load references progressively, but never omit a reference required for the current stage:

- Every task: `standards/project-context.md`, `references/assessment-format.md` and `references/curriculum-index.md`, followed by only the curriculum file for each assessed year level.
- New Years 3–10 grade-estimating creation/revision/review: `references/evidence-band-standard.md`.
- Pre-primary to Year 6 creation, revision or review: `references/judging-standards-calibration.md`. Use it only as a loose grade-demand reference; it is not current curriculum authority.
- Creation, revision or review: `references/assessment-quality-gates.md`.
- Creation or revision: `references/assessment-production-contract.md`.
- Q7 or Q8 drafting/review: `references/q7-q8-problem-solving-standard.md` and `references/q7-q8-demand-2025.md`.
- Any PowerPoint deliverable: `references/powerpoint-output.md`.
- Any diagram, geometric figure, graph, number line or labelled shape: `references/mathematical-diagram-conventions.md`.
- Any visual decision or rendered visual: `standards/visual-standard.md`; also load `references/contextual-illustration-standard.md` for situated problem-solving art.
- Release, resumed delivery or maintenance-status claims: `standards/release-evidence.md`.

Task-specific curriculum documents supplied by the user override bundled curriculum references. Preserve curriculum codes and scope exactly; do not invent, merge or silently alter them.

The 2016 judging standards must never override the 2026 curriculum, current canonical standards or an explicit user instruction. Do not use them as a checklist or import superseded content merely because it appears in an older descriptor. Year 7 judging-standard work remains outside that calibration reference.

## Canonical standards

Before producing content, load:

- `standards/assessment-contract.md`
- `standards/maths-conventions.md`
- `standards/exemplar-policy.md`
- `standards/qa-barriers.md`
- `standards/visual-standard.md`

Explicit user instructions override defaults. Current canonical standards override older exemplars where they conflict.

## Default Years 3–10 assessment structure

Unless the task explicitly requires another structure, a new grade-estimating Years 3–10 assessment uses **25 marks**:

| Question | Marks | Default evidence allocation |
|---|---:|---|
| Q1 | 1 | 1D |
| Q2 | 1 | 1D |
| Q3 | 1 | 1D |
| Q4 | 2 | 2D |
| Q5 | 4 | 4C |
| Q6 | 5 | 4C + 1B |
| Q7 | 5 | 4B + 1A |
| Q8 | 6 | 6A |

Whole-assessment envelope: **5D / 8C / 5B / 7A**.

Indicative component estimate:

- **E:** 0–4
- **D:** 5–9
- **C:** 10–15
- **B:** 16–20
- **A:** 21–25

These boundaries are valid because the envelope structurally forces at least 5 C-or-higher marks at C, 3 B-or-higher marks at B and 3 A marks at A. The band belongs to each **individual mark criterion**, not to the question number. Never promote routine evidence merely because it appears in Q7 or Q8.

The default per-question placement may move when the mathematics genuinely warrants it, but the 5D / 8C / 5B / 7A envelope remains fixed unless the user explicitly authorises a structural exception. If the construct cannot support the envelope without artificial mark splitting or unauthorised content, return an architecture barrier.

Q7 and Q8 are independent complex problems. Q8 must not depend on, extend, or scaffold from Q7. Q7 remains principally B-level reasoning and Q8 principally A-level reasoning through meaningful situations, not routine exercises relabelled as complex.

## Scope compatibility

- Exact supplied assessments, key-only requests and equivalent Version B/re-attempt requests preserve the source architecture unless the user explicitly requests migration.
- Pre-primary–Year 2 remain on age-appropriate existing structures unless separately redesigned.
- Years 11–12/WACE remain governed by course-specific assessment and grade-setting requirements; the 25-mark envelope is not a WACE grading model.

## Release law

Any identified required defect means `NOT READY`. Do not use “ready with minor changes”, “mostly ready” or “acceptable with fixes”. A repair invalidates downstream validation for every artefact affected by that repair.

Every page must receive full-resolution and print-scale review. In-bounds objects and minimum font sizes do not establish good visual quality. Marking annotations must not hide diagrams, labels or student response structure.

## Executable enforcement

When Python execution is available, the runtime controller is mandatory. Create a run directory and record every stage through `runtime/controller.py`; do not treat free-form hand-offs as authoritative state.

```bash
python -m runtime.controller --run-dir run/current record 01-orchestrator-curriculum-resolver run/01-brief.json
python -m runtime.controller --run-dir run/current status
```

The controller validates schemas, dependency order, content/release gates, Q7/Q8 independence and Student Test → Marking Key provenance. Before READY it checks current artefact/evidence hashes and page-review coverage, executes the real package audit, and rejects missing or stale evidence. Reopening a READY run rechecks that evidence. A controller rejection cannot be bypassed by qualitative judgement.

Use the complete command interface in `standards/release-evidence.md`. Always run `scripts/validate_assessment_spec.py`; for `criterion_component_estimate_v1` packages use `scripts/audit_assessment_package_v4.py`, while legacy/source-preservation packages use `scripts/audit_assessment_package.py`. Both auditors require named flags rather than a lone positional specification path.

On interruption, inspect the last recorded stage and existing files, then resume from valid evidence. Do not claim background progress or completion without deliverables. Before delivery, verify and link to the exact current files.

Use `assets/` and `examples/benchmarks/` only for their assigned quality dimensions. A skill test pass, GitHub push or package build is not assessment READY and is not proof of installation. Report implemented, tested, merged and installed separately.
