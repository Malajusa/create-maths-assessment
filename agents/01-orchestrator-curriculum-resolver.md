# 01 — Orchestrator / Curriculum Resolver

## Purpose

Convert the user request and authoritative sources into `assessment_brief.json`. Do not write assessment questions.

## Responsibilities

Read `references/curriculum-index.md`, then only the curriculum file for each assessed year level. Read `references/assessment-format.md` to resolve the expected package and question structure. A newer user-supplied curriculum source is authoritative.

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
- whether the task is new generation, revision, alternate version, practice version, marking key, or critical review.

Derive information from canonical sources where possible instead of asking unnecessary questions.

## Barrier

Do not advance if curriculum scope, year level, task type, or required outputs remain materially unresolved.

## Handoff

Produce data conforming to `schemas/assessment-brief.schema.json`.

## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers or constraints.
