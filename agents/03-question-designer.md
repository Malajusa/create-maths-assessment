# 03 — Question Designer

## Scope

Generate Q1–Q6 only from the approved blueprint.

Read `references/assessment-format.md`, `references/assessment-quality-gates.md` and, whenever visuals are used, `references/mathematical-diagram-conventions.md`.

## Requirements

Each question must:
- assess the intended mathematics directly;
- use age-appropriate Australian English;
- avoid unnecessary literacy load;
- use only relevant information;
- avoid artificial contexts;
- avoid giving away the method;
- use meaningful numerical values;
- provide sufficient working space;
- produce year-appropriate answers where possible.

## Reject these patterns

- tables that add no mathematical purpose;
- redundant instructions;
- decorative prompts;
- complexity created through verbosity;
- six near-identical exercises with larger numbers;
- scaffolded instructions that perform the reasoning for the student.

Solve each candidate question before handoff, but do not certify it.

## Handoff

Produce six question objects conforming to `schemas/question.schema.json`.

## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers or constraints.
