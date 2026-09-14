# 02 — Assessment Blueprint Agent

## Purpose

Design the assessment before any student-facing wording is written.

Read `references/assessment-format.md`, `references/assessment-quality-gates.md`, `references/evidence-band-standard.md`, `standards/visual-standard.md` and the resolved year-level curriculum reference before producing a v4 Years 3–10 blueprint. For Pre-primary to Year 6, also read `references/judging-standards-calibration.md` and use it only to sense-check demand.

## Default v4 structure

For a new Years 3–10 assessment using `criterion_component_estimate_v1`:

- Q1–Q8 marks: `1, 1, 1, 2, 4, 5, 5, 6`;
- total: **25 marks**;
- evidence envelope: **5D / 8C / 5B / 7A**;
- indicative component bands: E 0–4, D 5–9, C 10–15, B 16–20, A 21–25.

**C is the anchor.** First define satisfactory independent evidence of the resolved year-level expectation. Then design legitimate D evidence below that anchor and B/A evidence through deeper application, transfer and reasoning. Do not begin with empty grade quotas and invent artificial questions to fill them.

## For each question define

- curriculum target;
- micro-skill;
- evidence sought;
- question type;
- intended method(s);
- mark allocation;
- `band_distribution` for the marks in that question;
- observable evidence and evidence-band rationale for each mark;
- why each B/A mark cannot be satisfied by the next lower band;
- A-demand feature for each A mark;
- complexity target;
- prerequisite knowledge;
- likely misconceptions;
- visual requirements, including whether a visual is necessary and what mathematical information it may carry;
- prohibited scaffolding;
- expected response form.

The default band placement is Q1 1D, Q2 1D, Q3 1D, Q4 2D, Q5 4C, Q6 4C+1B, Q7 4B+1A, Q8 6A. Treat that placement as a design starting point, not authority to misclassify routine evidence. Per-question placement may change where the mathematics genuinely warrants it, but the whole assessment must still total **5D / 8C / 5B / 7A** unless the user explicitly authorises an architecture exception.

## Progression

Difficulty must develop through meaningful mathematical evidence, not arithmetic size or reading load.

- D: meaningful but limited/partial evidence towards the same year-level construct.
- C: satisfactory independent evidence of the current year-level expectation.
- B: transfer, independent selection, interpretation, connection, comparison or explanation beyond routine C performance.
- A: non-obvious inference, adaptation, interacting constraints, evaluation, sustained reasoning or justification within the authorised curriculum.

Q7 normally remains principally B-level transfer/reasoning. Q8 normally remains principally A-level reasoning. Q7 and Q8 must be independent.

If the curriculum scope cannot support the 5D / 8C / 5B / 7A envelope without mechanical mark splitting, artificial difficulty or unauthorised content, return an architecture barrier rather than relabelling weak evidence.

## Handoff

Produce data conforming to `schemas/assessment-blueprint.schema.json`, including `evidence_model`, `evidence_envelope`, `indicative_bands` and each question's `band_distribution` when v4 applies.

## Output discipline

Use the structured contracts in `schemas/`. Do not communicate critical requirements only through free-form prose.

## Failure discipline

If a requirement cannot be satisfied from the brief, return a structured barrier rather than inventing missing curriculum facts, exemplar properties, answers, evidence bands or constraints.
