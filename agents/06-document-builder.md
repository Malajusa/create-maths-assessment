# 06 — Document Builder

## Preconditions

Build only from `approved_question_set` emitted by Agent 05.

`approved_question_set` is the source of truth for assessment content. Do not reconstruct questions from the blueprint, validation prose, or earlier generator outputs.

Do not materially rewrite validated questions.

Read `references/assessment-production-contract.md`, `references/powerpoint-output.md`, `references/evidence-band-standard.md`, `standards/visual-standard.md`, `standards/project-context.md` and `standards/release-evidence.md` before building. Use the deterministic preflight tools in `scripts/` and stop if either rejects the package.

Resolve one `visual_profile` before layout. Prefer a user-approved profile in the brief; otherwise use `assets/visual-profiles/classic-assessment-v1.json`. The profile is visual-only authority and may not change validated mathematics, curriculum, answers or difficulty.

## Student Test

Create PowerPoint in A4 portrait using the resolved visual profile. Treat typography target ranges as design intent and floors as emergency safety barriers, not normal targets. Reserve response space before placing diagrams or decoration. For Page 1, keep every question-owned element within its assigned cell. Q7/Q8 must use the profile's extended-response recipes and give required mathematical diagrams visual prominence.

The Student Test **must not display** D/C/B/A evidence-band metadata, band rationales, internal cut-off proof or any teacher-only component-estimate logic.

## Marking Key

The completed Student Test is the source of truth.

Create the key by duplicating the final test and adding:
- answers;
- worked reasoning where appropriate;
- mark allocation;
- acceptable alternative strategies where appropriate;
- teacher-facing evidence-band annotation where it aids moderation and can be added without obscuring the duplicated student layout.

For a v4 assessment, also include a compact **indicative standard on this assessed component** table:

- E: 0–4
- D: 5–9
- C: 10–15
- B: 16–20
- A: 21–25

State that this is an indicative task/component estimate, not the student's reporting grade.

Never reconstruct the assessment independently. For a key-only request, use the exact supplied presentation and record its filename and hash; do not substitute another version.

Keep marking annotations integrated with the duplicated student layout. Do not cover essential diagrams, labels or response structure with large generic solution panels.

## Curriculum Rationale

Create the Curriculum Rationale from the final assessment, not from the original plan. Include curriculum links, question mapping, assessment coverage and Q7/Q8 rationale.

For v4, also include:
- the **5D / 8C / 5B / 7A evidence envelope**;
- the 0–4 / 5–9 / 10–15 / 16–20 / 21–25 indicative component bands;
- the structural proof that C/B/A boundaries force 5/3/3 target-or-higher marks respectively;
- a concise explanation of how D/C/B/A evidence is defined for the assessed curriculum;
- an explicit statement that the result estimates performance on the assessed component and does not determine the semester/reporting grade.

## Render requirement

Render every page/slide for downstream visual inspection, including the rationale. Keep each full-page PNG inside the run directory at no less than 1240 × 1754 pixels; thumbnails and contact sheets alone are insufficient. Hash the final source files and renders after the last edit.

Emit `design_manifest` conforming to `schemas/design-manifest.schema.json` and persist the same object as `design-manifest.json` with the package. Record the exact visual-profile hash, slide recipes and measured typography/area metrics. Do not claim a visual rule was applied unless it can be evidenced in the rendered package.

Resolve every visual from its `visual_spec`. Record visual-profile, token-set and asset-manifest hashes; per-question asset or constructor IDs; scale state; printed dimensions; greyscale evidence; and demand-preservation evidence in `design_manifest.visual_system`.

Persist the assessment specification and authoring QA ledger for Agent 07. Do not fill in independent-review evidence on the reviewer's behalf. Recording a build is not release authorisation.

## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers, evidence bands or constraints.
