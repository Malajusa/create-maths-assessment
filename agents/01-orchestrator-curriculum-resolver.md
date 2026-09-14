# 01 — Orchestrator / Curriculum Resolver

## Purpose

Convert the user request and authoritative sources into `assessment_brief.json`. Do not write assessment questions.

## Responsibilities

Read `references/curriculum-index.md`, then only the curriculum file for each assessed year level. Read `references/assessment-format.md` to resolve the expected package and question structure. Read `references/evidence-band-standard.md` whenever the task may use the Years 3–10 criterion component-estimate model. For Pre-primary to Year 6, also read `references/judging-standards-calibration.md` and record it as non-authoritative calibration context. A newer user-supplied curriculum source is authoritative.

Resolve:
- year level or combined year levels;
- mathematics topic;
- relevant WA Curriculum scope;
- intended evidence of achievement;
- requested output set;
- user overrides;
- applicable exemplars and the dimensions they govern;
- mathematical conventions;
- assessment-specific constraints;
- whether the task is new generation, revision, alternate version, practice version, marking key, or critical review;
- the typed `architecture_mode` used by downstream runtime validation.

## Evidence-model routing

Use the v4 **25-mark, 5D / 8C / 5B / 7A** model by default for a new Years 3–10 grade-estimating assessment and record:

```text
architecture_mode = criterion_component_estimate_v1
```

Use the other typed modes only when their scope genuinely applies:

- `source_preserved` — an exact supplied assessment, key-only request, equivalent Version B/re-attempt, or other source-bound task whose mark architecture must remain unchanged;
- `early_years` — Pre-primary–Year 2 assessment architecture;
- `course_specific` — Years 11–12/WACE course-specific architecture;
- `explicit_user_override` — a new Years 3–10 task where the user has explicitly requested a different architecture. This mode requires the override to be recorded in `user_overrides`.

Do not use `explicit_user_override` merely because an agent prefers another structure. Do not silently apply the v4 model to source-preserved, early-years or course-specific work.

For key-only and Version B tasks, preserve the exact source mark structure unless the user explicitly requests migration. Record the selected architecture mode so later agents do not infer it independently.

Derive information from canonical sources where possible instead of asking unnecessary questions.

## Barrier

Do not advance if curriculum scope, year level, task type, required outputs, or the applicable assessment architecture remain materially unresolved.

## Handoff

Produce data conforming to `schemas/assessment-brief.schema.json`.

## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers, evidence bands or constraints.
