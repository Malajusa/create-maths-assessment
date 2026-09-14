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
- whether `criterion_component_estimate_v1` applies.

## Evidence-model routing

Use the v4 **25-mark, 5D / 8C / 5B / 7A** model by default for a new Years 3–10 grade-estimating assessment.

Do not silently apply it to:
- Pre-primary–Year 2 assessments;
- Years 11–12/WACE assessments;
- a key-only request for an exact supplied assessment;
- an equivalent Version B or re-attempt based on a supplied assessment with a different source architecture.

For key-only and Version B tasks, preserve the exact source mark structure unless the user explicitly requests migration. Record the selected evidence model or source-preservation rule in the brief so later agents do not infer it independently.

Derive information from canonical sources where possible instead of asking unnecessary questions.

## Barrier

Do not advance if curriculum scope, year level, task type, required outputs, or the applicable assessment architecture remain materially unresolved.

## Handoff

Produce data conforming to `schemas/assessment-brief.schema.json`.

## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers, evidence bands or constraints.
