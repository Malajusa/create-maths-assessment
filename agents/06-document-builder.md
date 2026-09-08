# 06 — Document Builder

## Preconditions

Build only from `approved_question_set` emitted by Agent 05.

`approved_question_set` is the source of truth for assessment content. Do not reconstruct questions from the blueprint, validation prose, or earlier generator outputs.

Do not materially rewrite validated questions.

Read `references/assessment-production-contract.md` and `references/powerpoint-output.md` before building. Use the deterministic preflight tools in `scripts/` and stop if either rejects the package.

## Student Test

Create PowerPoint in A4 portrait using the canonical visual hierarchy. It must be print-safe, unclipped, readable, mathematically accurate and provide appropriate working space.

## Marking Key

The completed Student Test is the source of truth.

Create the key by duplicating the final test and adding:
- answers;
- worked reasoning where appropriate;
- mark allocation;
- acceptable alternative strategies where appropriate.

Never reconstruct the assessment independently.

## Curriculum Rationale

Create the rationale from the final assessment, not from the original plan. Include curriculum links, question mapping, difficulty progression, assessment coverage and Q7/Q8 rationale.

## Render requirement

Render every page/slide for downstream visual inspection.
## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers or constraints.
