# Assessment design and quality gates

## Contents

0. Binary release rule
1. Quality hierarchy
2. Mandatory design matrix
3. Coherence and variation rules
4. Evidence-band and mark-allocation rules
5. Transformations benchmark
6. Pre-production rejection gates
7. Rendered-package release gates
8. Required evidence and audit execution

## 0. Binary release rule

Readiness is binary: **READY** or **NOT READY**.

- Any identified correction affecting curriculum alignment, mathematical accuracy, question meaning, natural wording, cognitive demand, evidence-band validity, diagnostic value, notation, visual representation, accessibility, response space, print legibility, marking reliability, file consistency or package completeness is a release barrier.
- Do not use `minor`, `non-barrier`, `acceptable for now` or similar language to permit delivery while a known correction remains open. These terms may describe effort, never readiness.
- An optional stylistic preference is non-blocking only when no correction is recommended and it has no effect on use, interpretation, marking or print quality.
- For creation/revision, fix every identified issue within scope and repeat the affected checks plus the complete rendered-package release pass.
- For review-only, return **NOT READY** whenever any correction is required.
- Do not deliver a final package until the release ledger contains zero open issues.

Maintain the JSON release ledger defined in `assessment-production-contract.md`. Every gate must record `PASS`. A warning, conditional pass, unverified assumption or promised future check counts as `FAIL` until resolved. Prose claims are not substitutes for the ledger or deterministic audit.

## 1. Quality hierarchy

Judge assessment quality in this order:

1. exact alignment to the taught/current curriculum;
2. valid criterion evidence relative to the resolved expected standard;
3. intentional balance across essential concepts;
4. coherent cumulative progression from limited evidence through expected-standard evidence to transfer/evaluation;
5. diagnostic value for misconceptions and next teaching steps;
6. purposeful mathematical action and representation;
7. readable, consistent and printable page design.

Do not reverse this order. A nominal 5D / 8C / 5B / 7A envelope is invalid if its mark labels do not match the mathematics actually elicited.

## 2. Mandatory design matrix

Complete all eight rows before authoring slides. For v4 the default matrix is:

| Q | Marks | Default band distribution | Curriculum concept | Observable evidence | Mathematical action | Representation | Diagnostic purpose | Dependency/follow-through | Mark evidence |
|---|---:|---|---|---|---|---|---|---|---|
| Q1 | 1 | 1D |  |  |  |  |  |  |  |
| Q2 | 1 | 1D |  |  |  |  |  |  |  |
| Q3 | 1 | 1D |  |  |  |  |  |  |  |
| Q4 | 2 | 2D |  |  |  |  |  |  |  |
| Q5 | 4 | 4C |  |  |  |  |  |  |  |
| Q6 | 5 | 4C + 1B |  |  |  |  |  |  |  |
| Q7 | 5 | 4B + 1A |  |  |  |  |  |  |  |
| Q8 | 6 | 6A |  |  |  |  |  |  |  |

Use precise actions such as identify, construct, calculate, represent, describe, compare, infer, critique, reverse, evaluate and justify.

For each individual v4 mark record `evidence`, `evidence_band`, `band_rationale`, `why_not_lower_band`, and an `a_demand_feature` for every A mark.

Before approval, list essential concepts and record whether each is directly assessed, indirectly assessed or intentionally omitted with a reason. Do not let one convenient representation/procedure dominate because it is easy to lay out or mark.

Before slide production add a readiness record for each question covering task restatement, independently verified answer/solution, one reasonable interpretation, visual purpose/omission, exact mark evidence and band rationale, and Q7/Q8 prose-extraction/demand features.

## 3. Coherence and variation rules

For v4, design **C first** as satisfactory independent evidence of the resolved year-level expectation, then legitimate D evidence below that anchor and B/A evidence through deeper application.

Plan for cumulative evidence:

- Q1–Q4 provide five meaningful D marks towards the same current-year construct rather than unrelated prerequisite trivia.
- Q5 normally provides direct C evidence.
- Q6 normally consolidates C and introduces a legitimate B opportunity.
- Q7 is one clear main problem, principally B, interrupting routine application through transfer, inference, comparison, reverse process or explanation.
- Q8 is one independent A-level problem deepening the mathematics through connected conditions, missing relationships, reverse process, evaluation or justification. It must not extend or depend on Q7.

Use variety to expose different mathematical evidence, not decoration. Accept repeated actions only where they deliberately contrast concepts, reveal an invariant, isolate a misconception or build a coherent progression.

## 4. Evidence-band and mark-allocation rules

Read `evidence-band-standard.md`.

**D:** meaningful but limited/partial evidence towards the current year-level construct.

**C:** satisfactory independent evidence of the current year-level expectation; the anchor band.

**B:** transfer, independent strategy selection, connection, interpretation, comparison, reverse process or explanation beyond routine C performance.

**A:** non-obvious inference, adaptation, interacting constraints, evaluation, sustained reasoning, reconciliation or justification within the authorised curriculum.

Never assign a higher band merely because of question position, arithmetic size, decimals, number of operations, more words, response length, subpart count or unfamiliar story context.

Assign marks to meaningful mathematical evidence: concept/relationship, viable model/strategy, important intermediate dependency, accurate completion, verification, comparison, evaluation or justification. Do not split one routine act mechanically across vertices, digits, rows, objects or written steps.

For v4 the complete validated mark set must total **25 marks** and **5D / 8C / 5B / 7A**. Score bands are E 0–4, D 5–9, C 10–15, B 16–20, A 21–25. The structure must force at least 5 C+, 3 B+ and 3 A marks at the C/B/A boundaries. If honest banding prevents this envelope, redesign; do not reclassify weak evidence.

## 5. Transformations benchmark

For Year 6 transformations inspect `../assets/year-6-transformations-quality-benchmark.pptx`. Treat it as a benchmark for curriculum coverage, diagram quality and page hierarchy, not as authority for v4 mark values or response formats. Re-blueprint a v4 transformations assessment so every mark satisfies the current evidence-band definitions.

## 6. Pre-production rejection gates

The release ledger retains **P01–P29**. For v4, the new evidence checks are incorporated into these gates rather than adding new gate IDs.

Reject the draft if any answer is no:

1. **P01:** Does the concept list show intentional topic coverage rather than accidental emphasis?
2. **P02:** Does every question have a distinct diagnostic purpose?
3. **P03:** Can the progression be stated as one coherent cumulative sequence, with C explicitly anchored to satisfactory current-year achievement when v4 applies?
4. **P04:** Does any repeated action have an explicit contrast, diagnostic or progression reason?
5. **P05:** Does every mark represent meaningful distinct evidence; and for v4 do the 25 marks carry valid `evidence_band`, `band_rationale`, `why_not_lower_band`, required A-demand features, and total exactly 5D / 8C / 5B / 7A with E/D/C/B/A bands 0–4/5–9/10–15/16–20/21–25 and structural 5/3/3 boundary proof?
6. **P06:** Do Q7/Q8 meet cognitive-demand requirements without untaught content, with Q7 principally B and Q8 principally A under honest individual-mark classification?
7. **P07:** Will incorrect responses identify useful reteaching needs?
8. **P08:** Can a student tell exactly what to do, response count/location and required evidence without teacher paraphrasing?
9. **P09:** Does layout provide sufficient blank, unlined space without generic pre-divided working steps?
10. **P10:** Do all diagrams follow `mathematical-diagram-conventions.md`?
11. **P11:** Does every symbolic fraction/mixed numeral use built-up horizontal-vinculum notation with visible clearance?
12. **P12:** Does each upper question use a practised/approved response structure, and has any rejected question family been genuinely replaced?
13. **P13:** Are Q7/Q8 independent, self-contained complex problems with genuine B/A reasoning rather than band inflation from question position?
14. **P14:** Does Q8 deepen mathematics without unfamiliar puzzle protocol, exhaustive-search proof or prescribed pathway?
15. **P15:** Can Q8 be understood/solved without reading/completing Q7?
16. **P16:** Are Q7/Q8 prose-first, requiring extraction of relevant quantities/conditions/relationships from sentences?
17. **P17:** If Q7/Q8 uses a display, is it mathematical evidence rather than a solution organiser?
18. **P18:** Does every sentence read naturally aloud as age-appropriate classroom English?
19. **P19:** Where a visual is central, is it meaningful, editable and large enough to use?
20. **P20:** Does every fraction have planned numerator-to-vinculum white space?
21. **P21:** Does Q8 have at least three substantive demand features including inference/dependency/interacting constraint and a justified conclusion, and do claimed A marks actually depend on valid A-demand features?
22. **P22:** Has every item been independently solved, including values, units, diagrams, conclusions, mark allocation and evidence-band allocation?
23. **P23:** Is Page 1 fixed Q1 top-left, Q2 top-right, Q3 middle-left, Q4 middle-right, Q5 bottom-left, Q6 bottom-right?
24. **P24:** Can the Marking Key be added to an exact duplicate of the final test without shrinking/obscuring/changing student-facing elements?
25. **P25:** Does the rationale describe actual questions, answers, demand and mark evidence; and for v4 the 5D / 8C / 5B / 7A envelope, structural boundary proof and task-level indicative interpretation without overstating curriculum/reporting-grade claims?
26. **P26:** Does every marked response require the student to derive, construct, decide, interpret or justify something not supplied by the stem/stimulus?
27. **P27:** Is each mark proportional to actual mathematical evidence, with no mechanical splitting or band inflation from arithmetic size/literacy/question position?
28. **P28:** Is every response label/box/table/ruled area mathematically necessary, justified and proportionate?
29. **P29:** Does validated `assessment-spec.json` contain exact prompt, answer, solution, mark evidence, representation purpose, response-space decision, curriculum alignment and, where v4 applies, complete evidence-model/envelope/indicative-band/mark-band metadata; and does legacy/source-preservation routing remain explicit where v4 does not apply?

## 7. Rendered-package release gates

The release ledger retains **R01–R18**. Apply all P01–P29 gates again to rendered artefacts, then reject if any answer is no:

1. **R01:** Are both PowerPoints A4 portrait and exactly three slides in required sequence unless an approved exception exists?
2. **R02:** Does Page 1 use exact `1–2 / 3–4 / 5–6` cell order?
3. **R03:** Are test/key identical in slide order, question wording, diagrams, original marks, response spaces and base geometry, with only teacher material added?
4. **R04:** Is `MARKING KEY` visible on every key page?
5. **R05:** Are student instructions/response expectations readable at actual A4 size and above required floors?
6. **R06:** Are key answers/solutions/criteria readable at actual A4 size and above required floors?
7. **R07:** Does a 100%-scale render show no clipping, collisions, crowding, weak contrast, tiny diagrams or insufficient response space?
8. **R08:** Do fractions retain clear numerator-to-vinculum spacing?
9. **R09:** Are required visual models large, accurate, editable, greyscale-safe and mathematically useful?
10. **R10:** Do Q7/Q8 remain natural prose-first tasks with supporting visuals only where mathematically necessary?
11. **R11:** Does the Marking Key show one distinct usable criterion for every allocated mark, acceptable alternatives/units/follow-through; and for v4 an exact indicative score table E 0–4, D 5–9, C 10–15, B 16–20, A 21–25 without obscuring the task?
12. **R12:** Do rationale/test/key agree exactly on curriculum, values, answers, totals and demand; and for v4 does the rationale accurately show 5D / 8C / 5B / 7A, structural 5/3/3 proof and 'indicative assessed component, not reporting grade' limitation while the Student Test exposes no internal band metadata?
13. **R13:** Does the rationale have no blank spill page, clipped table, orphaned heading or unreadably dense text?
14. **R14:** Have overflow/package-integrity/page-count checks passed without substituting for visual/pedagogical review?
15. **R15:** Does a final student-perspective read-through find every question natural, unambiguous and solvable without teacher paraphrasing?
16. **R16:** Does the release ledger contain zero failures, warnings, conditional passes or deferred fixes, including evidence-envelope defects?
17. **R17:** Do source spec, stable names and package audit prove required page positions, fraction clearances, response-space choices, font minimums, test/key duplication and, for v4, final mark/envelope/teacher-output agreement rather than leaving them to memory?
18. **R18:** Have both authoring QA and fresh artifact-only review passed with separately recorded evidence/review mode?

A file can pass automation and still fail because mathematics, evidence bands, demand, wording, visuals, notation, annotations, response space, test/key fidelity or rationale alignment is below standard. Fix and rerun the full release pass.

## 8. Required evidence and audit execution

For creation/revision retain until release:

- validated `assessment-spec.json`;
- JSON release ledger with exactly `P01`–`P29` and `R01`–`R18` recorded once each as `PASS`;
- final deterministic audit report;
- full-resolution rendered images/PDFs used for visual inspection;
- for v4, approved question set containing mark-level evidence-band metadata.

The specification validator and package auditor are compulsory controls. Automated checks do not judge natural language, curriculum validity, mathematical demand or visual usefulness; those remain review gates supported by specific evidence.

## Visual evidence gate

Apply `standards/visual-standard.md` to every visual. Confirm purpose/removal effect matches the construct, mathematical information is accurate, colour is not the sole cue, print dimensions are legible and Q7/Q8 demand is preserved. Decorative, untraceable or solution-ready visuals fail the content gate.