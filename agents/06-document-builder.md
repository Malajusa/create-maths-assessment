# 06 — Document Builder

## Preconditions

Build only from `approved_question_set` emitted by Agent 05.

`approved_question_set` is the source of truth for assessment content. Do not reconstruct questions from the blueprint, validation prose, or earlier generator outputs.

Do not materially rewrite validated questions.

Read `references/assessment-production-contract.md` and `references/powerpoint-output.md` before building. Use the deterministic preflight tools in `scripts/` and stop if either rejects the package.

Resolve one `visual_profile` before layout. Prefer a user-approved profile in the brief;
otherwise use `assets/visual-profiles/classic-assessment-v1.json`. The profile is visual-only
authority and may not change validated mathematics, curriculum, answers or difficulty.

## Student Test

Create PowerPoint in A4 portrait using the resolved visual profile. Treat typography target
ranges as design intent and floors as emergency safety barriers, not normal targets.
Reserve response space before placing diagrams or decoration. For Page 1, keep every
question-owned element within its assigned cell. Q7/Q8 must use the profile's extended-
response recipes and give required mathematical diagrams visual prominence.

## Marking Key

The completed Student Test is the source of truth.

Create the key by duplicating the final test and adding:
- answers;
- worked reasoning where appropriate;
- mark allocation;
- acceptable alternative strategies where appropriate.

Never reconstruct the assessment independently.

Keep marking annotations integrated with the duplicated student layout. Do not cover
essential diagrams, labels or response structure with large generic solution panels.

## Curriculum Rationale

Create the rationale from the final assessment, not from the original plan. Include curriculum links, question mapping, difficulty progression, assessment coverage and Q7/Q8 rationale.

## Render requirement

Render every page/slide for downstream visual inspection.

Emit `design_manifest` conforming to `schemas/design-manifest.schema.json` and persist the
same object as `design-manifest.json` with the package. Record the exact visual-profile hash,
slide recipes and measured typography/area metrics. Do not claim a visual rule was applied
unless it can be evidenced in the rendered package.
## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers or constraints.
