# Mr Leahy's mathematics assessment specification

## 1. Assessment purpose

Build a shared source of curriculum evidence, not merely a worksheet or collection of routine sums. For new Years 3–10 grade-estimating assessments, the raw score should provide a strong **indicative A–E estimate for the assessed component** because the marks have been deliberately allocated to D/C/B/A evidence. The result is not the student's semester/reporting grade.

Begin with:

1. current WA Curriculum content description;
2. relevant current achievement expectation;
3. observable evidence students must produce;
4. question and mark design;
5. independent validation and moderation use.

Quality principles:

- **Aligned:** assess the nominated curriculum.
- **Accessible:** remove irrelevant barriers without revealing the strategy.
- **Criterion-referenced:** define evidence relative to the expected standard, not cohort rank or arbitrary percentages.
- **Evidentiary:** require visible calculations, representations, explanations or justifications.
- **Markable:** connect every mark to one distinct observable criterion.
- **Diagnostic:** incorrect responses should expose useful misconceptions.
- **Manageable:** support classroom marking, moderation and equivalent re-attempts.

Read `evidence-band-standard.md` for the normative D/C/B/A definitions.

## 2. Default Years 3–10 criterion structure

For a new assessment using `criterion_component_estimate_v1`:

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

Mark sequence: **1, 1, 1, 2, 4, 5, 5, 6 = 25 marks**.

Whole-assessment evidence envelope: **5D / 8C / 5B / 7A**.

Indicative standard on the assessed component:

| Raw score | Indicative standard |
|---|---|
| 0–4 | E |
| 5–9 | D |
| 10–15 | C |
| 16–20 | B |
| 21–25 | A |

These are not universal percentage bands. They are valid because the evidence envelope structurally guarantees that:

- C at 10 requires at least 5 C-or-higher marks;
- B at 16 requires at least 3 B-or-higher marks;
- A at 21 requires at least 3 A marks.

The default per-question band placement may change when the mathematics genuinely warrants it, but the whole assessment remains 5D / 8C / 5B / 7A unless the user explicitly authorises an architecture exception.

## 3. Page structure

Default page sequence remains:

- Page 1: Q1–Q6 in six cells ordered Q1 top-left, Q2 top-right, Q3 middle-left, Q4 middle-right, Q5 bottom-left and Q6 bottom-right;
- Page 2: Q7;
- Page 3: Q8.

Use more pages only when accessibility, large diagrams or an explicit requested format requires it. The Student Test must not display internal D/C/B/A evidence labels.

## 4. Evidence bands

### D — meaningful limited evidence

D represents meaningful but limited/partial evidence towards the same year-level construct. It may use simpler familiar instances, recognition of essential relationships or partial completion of the expected process. D is not merely an easy mark and must not be filled with irrelevant prerequisite content.

### C — the expected-standard anchor

C represents satisfactory, independent evidence of the current year-level expectation for the assessed subset. Design C evidence first. A student meeting the year-level expectation should reasonably be able to earn these marks without extension content or artificial puzzle demands.

### B — transfer and stronger independent application

B requires something beyond routine C performance: transfer, independent method selection, reverse process, meaningful comparison, connection, interpretation or explanation where the method is not already supplied.

### A — flexible, non-routine and justified reasoning

A requires qualitatively stronger reasoning within authorised curriculum: non-obvious inference, adaptation, interacting constraints, evaluation, sustained reasoning, reconciliation of information or representations, or mathematical justification.

Above-standard evidence means depth and flexibility, not next-year curriculum.

## 5. Mark-level evidence contract

The individual mark criterion is the authoritative evidence-band unit. Each mark must record:

- observable evidence;
- `evidence_band` D/C/B/A;
- `band_rationale`;
- `why_not_lower_band`;
- `a_demand_feature` for A marks.

Do not infer evidence band from question number. A routine calculation in Q8 remains routine evidence unless the calculation itself genuinely requires higher-order reasoning.

Do not create marks by mechanically splitting one act across digits, vertices, rows, objects or written steps. Allocate marks to distinct concepts, decisions, representations, dependencies, accurate completion, comparison or justification.

## 6. Question architecture

Before writing student-facing wording, complete the design matrix in `assessment-quality-gates.md`.

For every question define:

- curriculum concept;
- observable evidence;
- mathematical action;
- representation;
- diagnostic purpose;
- dependency/follow-through;
- response form and space;
- mark evidence and evidence-band rationale.

Student clarity remains non-negotiable. Use age-appropriate Australian English, direct action verbs, clear response endpoints and only necessary context. Do not confuse difficult mathematics with difficult reading.

### Q1–Q4

Provide five meaningful D marks in total. These questions should expose limited or partial access to the same curriculum construct rather than unrelated prerequisite trivia.

### Q5

Normally provides four direct C marks. It should demonstrate satisfactory independent performance on the year-level expectation through familiar but meaningful mathematics.

### Q6

Normally provides four C marks plus one B opportunity. It should consolidate expected-standard performance and introduce legitimate transfer/interpretation without artificially increasing reading load.

### Q7

Q7 is an independent main problem, principally B-level. Use the architecture in `q7-q8-problem-solving-standard.md`. Students should extract relevant information, select a strategy and communicate reasoning. The default allocation is four B marks plus one A mark only when that A mark genuinely requires deeper reasoning.

### Q8

Q8 is an independent extension-level problem, principally A-level. It must not extend or depend on Q7. Require a planned chain of reasoning with at least three substantive demand features, including an inference, dependency or interacting constraint, and a justified conclusion. The default allocation is six A marks, but each mark must independently satisfy the A definition.

If the mathematics cannot support the default placement honestly, redesign or redistribute legitimate bands while preserving the whole 5D / 8C / 5B / 7A envelope. Do not relabel routine evidence to fill a quota.

## 7. Q7/Q8 demand rules

Q7 and Q8 are not merely harder sums.

Useful higher-demand features include:

- independent strategy selection;
- information extraction from natural prose;
- multiple interacting constraints;
- missing values that must be inferred;
- reversing a process;
- combining representations;
- comparing/evaluating possible conclusions;
- reasonableness checks;
- justified conclusions.

Reject difficulty created solely by larger numbers, decimals, more words, unfamiliar response protocols, exhaustive-search conventions or decorative complexity.

Q7 and Q8 are self-contained and independent. Q8 must be understandable and solvable without reading or completing Q7.

## 8. Curriculum alignment

Record:

- year level;
- content code and exact current description;
- relevant achievement-standard language;
- intended evidence;
- question numbers and mark criteria producing that evidence.

Do not claim complete curriculum coverage from one short assessment. State the assessed subset accurately.

The 2016 Judging Standards may be used only as loose calibration where applicable. They do not override current curriculum or user-supplied authority.

## 9. Page design

Page 1 uses the six-cell grid, but cells need not be equal. Allocate space according to the expected response.

Use:

- clear question numbers and mark values;
- built-up symbolic fractions with horizontal vincula;
- large, accurate and editable mathematical diagrams;
- visible units and labels;
- sufficient blank, unlined working space;
- consistent typography and margins;
- uncluttered student-facing language.

Avoid decorative graphics, slash-form fractions, tiny diagrams, duplicated instructions, redundant working boxes, ruled reasoning lines, arbitrary response labels and ambiguous visual scale.

A visual central to the construct must be mathematically purposeful and must not reveal the strategy intended to be assessed.

## 10. Marking and component estimate

Write the answer key while writing each question. For every mark identify:

- evidence required;
- acceptable alternatives;
- unit/label expectations;
- partial credit;
- follow-through where appropriate;
- minimum sufficient explanation;
- evidence band and rationale.

The score-to-standard estimate is deliberately simple **after** the assessment has been engineered correctly. No extra post-hoc grade gate is required for the canonical envelope.

The Marking Key may state, for example:

> 18/25 — indicative B-standard performance on this assessed component.

It must not state or imply:

> The student's Mathematics reporting grade is B.

Teacher moderation, re-attempt decisions, reflection on item efficacy and synthesis with other evidence remain outside this task-level classification.

## 11. Accessibility and administration

Where suitable, accept written answers, drawings, concrete materials, oral explanations, teacher notes or photographs of models when these preserve the intended construct.

Neutral prompts may ask a student to show or explain thinking. Prompts must not identify the operation, relevant numbers, information to ignore, correction required or solution strategy.

Adjustments should remove irrelevant barriers without changing the mathematics being assessed.

## 12. Mixed-year assessments

Use a combined assessment only when adjacent year levels have genuine curriculum overlap. Align evidence separately to each year. Do not treat higher-year content as automatic evidence of a lower-year A.

Where a mixed-year assessment uses the v4 envelope, C must still be anchored explicitly to the resolved expected standard for each assessed cohort; if one shared envelope cannot support valid interpretation for both year levels, use parallel assessments instead.

## 13. Re-attempts and equivalent versions

For a v4 equivalent Version B/re-attempt preserve:

- 25 total marks;
- 5D / 8C / 5B / 7A;
- component cut-offs;
- curriculum constructs;
- representation type where material;
- cognitive demand;
- mark criteria and evidence-band demand.

Change values, names or contexts only in ways that preserve equivalence. Independently solve all changed values.

For an uploaded legacy assessment, preserve its original structure unless the user explicitly requests migration to v4.

## 14. Moderation and instructional use

These assessments are primarily moderation-quality evidence instruments, not canonical report-grade allocators. After administration teachers may:

1. independently mark samples;
2. compare mark interpretation;
3. inspect boundary responses;
4. identify wording/item problems;
5. reflect on whether the assessment elicited the intended evidence;
6. offer an equivalent re-attempt where appropriate;
7. combine this evidence with other valid evidence for reporting.

The skill does not automate those teacher judgements.

## 15. Final checks

Before content approval confirm:

- current curriculum codes/descriptions are exact;
- total marks and envelope are correct;
- each individual mark has observable, distinct evidence;
- every band classification is justified from evidence rather than question position;
- C marks represent the expected year-level standard;
- B marks genuinely require transfer/selection/interpretation/connection/explanation;
- A marks genuinely require non-obvious inference/adaptation/constraints/evaluation/sustained reasoning/justification;
- no grade boundary can be crossed without the structurally required target-band evidence;
- Q7/Q8 remain independent and meaningful;
- no marked response is supplied by the stem/stimulus;
- wording reads naturally aloud;
- response space matches demand;
- visuals preserve demand and follow mathematical conventions;
- the Marking Key can be applied consistently;
- the Student Test contains no internal evidence-band metadata;
- teacher-facing outputs describe results as indicative evidence for the assessed component, not a reporting grade.

Every identified correction is a release barrier under `assessment-quality-gates.md`.
