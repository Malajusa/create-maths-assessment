# Create Maths Assessment v4 — Criterion Evidence Envelope

## Purpose

`create-maths-assessment` remains an assessment-construction skill. Its job is to create curriculum-aligned mathematics assessments whose raw score provides a strong **indicative A–E estimate for the assessed component** because the marks themselves have been deliberately engineered around standards of mathematical evidence.

The skill does **not** determine a student's semester/reporting Mathematics grade. Teacher moderation, reflection on assessment efficacy, re-attempt decisions and synthesis with other evidence remain teacher responsibilities.

## Scope

This v4 default applies to new Years 3–10 grade-estimating mathematics assessments unless the user explicitly requests another structure.

It does not silently replace:

- Pre-primary–Year 2 age-appropriate structures;
- Years 11–12/WACE course-specific assessment and grade-setting requirements;
- exact supplied assessments used for key-only requests;
- equivalent Version B/re-attempt requests, which preserve the source assessment's architecture unless migration is explicitly requested.

## Canonical evidence envelope

New default total: **25 marks**.

| Evidence band | Marks |
|---|---:|
| D | 5 |
| C | 8 |
| B | 5 |
| A | 7 |
| **Total** | **25** |

Default indicative component estimates:

| Score | Indicative standard on this assessed component |
|---|---|
| 0–4 | E |
| 5–9 | D |
| 10–15 | C |
| 16–20 | B |
| 21–25 | A |

These are not universal percentage bands. They are valid only because the assessment is constructed and validated against the evidence envelope below.

## Structural proof

The raw score must itself force meaningful target-standard evidence; no separate post-hoc grading rule is required.

- **C:** only 5 D marks exist. Reaching 10 therefore requires at least **5 C-or-higher marks**.
- **B:** D+C total 13. Reaching 16 therefore requires at least **3 B-or-higher marks**.
- **A:** D+C+B total 18. Reaching 21 therefore requires at least **3 A marks**.

The skill must reject any proposed architecture whose cut-offs fail equivalent structural proofs.

## Evidence-band definitions

### D — limited but meaningful evidence

A D mark represents meaningful progress towards the same year-level construct while demanding less independence, completeness or complexity than satisfactory C-standard evidence. Typical examples include recognising a basic relationship, completing a simple familiar instance, or demonstrating part of an expected procedure.

A D mark is not merely an easy mark and must not assess irrelevant prerequisite content.

### C — expected-standard anchor

A C mark represents satisfactory, independent demonstration of the mathematics expected at the resolved year level for the assessed content. Typical examples include applying a taught procedure in a familiar form, interpreting a familiar representation, selecting a routinely practised method, or giving a straightforward expected explanation.

C is the anchor for all other band decisions.

### B — transfer and stronger independent application

A B mark requires evidence beyond routine C performance, such as meaningful transfer, independent strategy selection, connection, interpretation, reverse process, comparison, or explanation.

A student must not be able to earn a B mark merely by competently performing the routine year-level procedure when the method or relationship is already supplied.

### A — flexible, non-routine and justified reasoning

An A mark requires qualitatively stronger evidence such as non-obvious inference, adaptation, interacting constraints, evaluation, sustained reasoning, reconciliation of information or representations, or mathematical justification.

A evidence remains within the authorised curriculum. It is not created by importing later-year content.

## Prohibited band inflation

An evidence band must never be assigned merely because of:

- question number;
- arithmetic size;
- decimals instead of whole numbers;
- number of operations;
- more words;
- longer response length;
- more subparts;
- an unfamiliar story context;
- a visually complicated diagram;
- a routine step occurring inside Q7 or Q8.

The band belongs to the **observable evidence earning an individual mark**, not to the question as a whole.

## Default question architecture

Default question marks:

`1, 1, 1, 2, 4, 5, 5, 6 = 25`

Default mark-band placement:

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

This per-question allocation is a default implementation, not a licence to relabel routine evidence. Marks may move across Q5–Q8 when the mathematics genuinely warrants it, provided the whole assessment remains exactly **5D / 8C / 5B / 7A**.

If the topic cannot support the envelope without mechanical mark splitting, artificial difficulty or unauthorised content, return an **architecture barrier** rather than inventing band labels.

## Mark-level evidence contract

Every mark must record:

- `evidence_band`: D, C, B or A;
- `observable_evidence`: what the student must visibly demonstrate;
- `band_rationale`: why that evidence belongs at the claimed band;
- `why_not_lower_band`: why the next lower band is insufficient.

Every A mark must additionally identify at least one A-demand feature from:

- inference;
- adaptation;
- interacting constraints;
- evaluation;
- sustained reasoning;
- justification.

## Scoring model

The model is compensatory. All earned marks contribute to the total; students do not have to 'pass' lower bands before higher-band marks count.

The assessment is intentionally a robust component estimate rather than a perfect psychometric classifier of every unusual response profile. Borderline and atypical patterns remain visible in the marked paper and are interpreted by the teacher alongside other evidence.

## Q7 and Q8

Preserve the existing project rules:

- Q7 and Q8 are independent and self-contained;
- Q7 remains principally a B-level complex problem;
- Q8 remains principally an A-level complex problem;
- both preserve strategy choice and meaningful mathematical reasoning;
- Q8 must not continue, scaffold from or depend on Q7;
- complexity must come from mathematics, not literacy load or artificial procedure.

Routine intermediate calculations inside Q7/Q8 retain their true evidence band.

## Re-attempt and Version B equivalence

A v4 equivalent/re-attempt must preserve:

- 25 total marks;
- 5D / 8C / 5B / 7A evidence envelope;
- 0–4 / 5–9 / 10–15 / 16–20 / 21–25 cut-offs;
- curriculum constructs;
- cognitive demand;
- representation type where material;
- mark criteria and evidence-band demand.

Numbers, names and contexts may change, but the evidence architecture must remain equivalent.

## Student-facing and teacher-facing outputs

The Student Test must not display internal D/C/B/A evidence labels.

The Marking Key should include a compact indicative score table.

The Curriculum Rationale should explain:

- the evidence envelope;
- the band definitions as applied to the assessed curriculum;
- the structural cut-off proof;
- that the estimate applies to the assessed component and is not the student's reporting grade.

## Deterministic validation requirements

The preflight validator must verify:

1. total marks = 25 for new Years 3–10 v4 assessments;
2. whole-assessment evidence totals = 5D / 8C / 5B / 7A;
3. every mark has complete evidence-band metadata;
4. C/B/A boundaries structurally force at least 5/3/3 target-or-higher marks respectively;
5. all possible earned-band profiles preserve monotonicity;
6. Student Test output contains no internal evidence-band labels;
7. key and rationale agree exactly with the approved question set and envelope.

A controller, validator or audit rejection cannot be bypassed qualitatively.

## Authority and compatibility

Authority remains:

1. explicit user instruction;
2. current/user-supplied WA curriculum authority;
3. current canonical assessment standards;
4. this evidence-envelope specification;
5. 2016 Judging Standards as loose calibration only;
6. older exemplars.

This v4 change strengthens the assessment's component-grade estimation without turning the skill into a reporting-grade allocation system.