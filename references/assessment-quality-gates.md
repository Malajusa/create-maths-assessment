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

Do not reverse this order. A visually varied paper is not stronger merely because it looks varied, and a nominal 5D / 8C / 5B / 7A envelope is invalid if its mark labels do not match the mathematics actually elicited.

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

For each individual mark record:

- `evidence` — visible mathematics that earns the mark;
- `evidence_band` — D, C, B or A;
- `band_rationale` — why the evidence belongs at that band;
- `why_not_lower_band` — why the next lower band is insufficient;
- `a_demand_feature` for every A mark.

Before approval, list the topic's essential concepts and record whether each is directly assessed, indirectly assessed through a connected question, or intentionally omitted with a reason. Do not let one convenient representation or procedure dominate merely because it is easy to lay out or mark.

Before slide production add a readiness record for each question covering:

- plain-language task restatement;
- independently verified answer/solution path;
- why wording has one reasonable mathematical interpretation;
- visual purpose/omission;
- exact evidence for every mark and its evidence band;
- for Q7/Q8, information extracted from prose and the demand features preventing routine Q5/Q6 demand.

## 3. Coherence and variation rules

For v4, design **C first** as the satisfactory independent evidence of the resolved year-level expectation, then legitimate D evidence below that anchor and B/A evidence through deeper application.

Plan for cumulative evidence:

- Q1–Q4 provide five meaningful D marks towards the same current-year construct rather than unrelated prerequisite trivia.
- Q5 normally provides direct C evidence.
- Q6 normally consolidates C and introduces a legitimate B opportunity.
- Q7 is one clear main problem, principally B, interrupting routine application through transfer, inference, comparison, reverse process or explanation.
- Q8 is one independent A-level problem deepening the mathematics through connected conditions, missing relationships, reverse process, evaluation or justification. It must not extend or depend on Q7.

Use variety to expose different mathematical evidence, not to decorate the assessment.

Accept repeated actions when they deliberately contrast concepts, reveal an invariant, isolate a misconception, extend one process into a connected process, or create coherent preparation for later reasoning. Reject repetition that merely changes numbers, shapes, names or context while eliciting the same evidence.

## 4. Evidence-band and mark-allocation rules

Read `evidence-band-standard.md`.

### Evidence-band integrity

**D:** meaningful but limited/partial evidence towards the current year-level construct.

**C:** satisfactory independent evidence of the current year-level expectation; the anchor band.

**B:** transfer, independent strategy selection, connection, interpretation, comparison, reverse process or explanation beyond routine C performance.

**A:** non-obvious inference, adaptation, interacting constraints, evaluation, sustained reasoning, reconciliation or justification within the authorised curriculum.

Never assign a higher band merely because of question position, arithmetic size, decimals, number of operations, more words, longer response, more subparts or an unfamiliar story context.

### Mark allocation

Assign marks to meaningful mathematical evidence such as:

- correct concept/relationship;
- viable model, construction or strategy;
- important intermediate dependency;
- accurate completion;
- verification, comparison, evaluation or justification.

Do not split one routine act mechanically across vertices, digits, rows, objects or written steps. Award one mark per component only when that component is itself the intended evidence.

For v4 the complete validated mark set must total **25 marks** and **5D / 8C / 5B / 7A**. The score bands must be exactly E 0–4, D 5–9, C 10–15, B 16–20, A 21–25. These boundaries must structurally force at least 5 C+, 3 B+ and 3 A marks respectively.

If honest banding prevents the envelope from being met, redesign the assessment. Do not reclassify weak evidence to make the totals work.

## 5. Transformations benchmark

For Year 6 transformations, inspect `../assets/year-6-transformations-quality-benchmark.pptx`. Treat it as a benchmark for curriculum coverage, diagram quality and page hierarchy. Do not copy its response formats mechanically or let it override the v4 evidence model/current curriculum.

The benchmark remains useful because it balances translation/reflection/rotation, progresses from recognition through construction/description to composition/reasoning, and uses diagrams as mathematics rather than decoration. Re-blueprint any v4 version so its individual marks satisfy the current evidence-band definitions; do not assume the benchmark's historical mark values are canonical.

## 6. Pre-production rejection gates

Reject the draft before PowerPoint production if any answer is no:

1. Does the concept list show intentional topic coverage rather than accidental emphasis?
2. Does every question have a distinct diagnostic purpose?
3. Can the progression be stated as one coherent cumulative sequence?
4. Does any repeated action have an explicit contrast, diagnostic or progression reason?
5. Does every mark represent meaningful mathematical evidence rather than mechanical task fragments?
6. For v4, is C explicitly anchored to satisfactory independent current-year achievement?
7. For v4, does every individual mark contain valid `evidence_band`, `band_rationale` and `why_not_lower_band` metadata?
8. For v4, does every A mark have a defensible `a_demand_feature` actually required by the task?
9. For v4, do all marks total 25 and exactly 5D / 8C / 5B / 7A?
10. For v4, are component bands exactly E 0–4, D 5–9, C 10–15, B 16–20, A 21–25?
11. For v4, do structural calculations prove at least 5 C+, 3 B+ and 3 A marks are forced at the C/B/A boundaries?
12. Is no evidence band inflated by arithmetic size, literacy load, question position or routine steps?
13. Do Q7 and Q8 meet the cognitive-demand reference without relying on untaught content?
14. Will incorrect responses identify useful reteaching needs?
15. Can a student tell exactly what to do, how many responses to give, where to record them and what evidence is required without teacher paraphrasing?
16. Does the page layout provide enough blank, unlined response space for the required mathematics?
17. Do all diagrams follow `mathematical-diagram-conventions.md`?
18. Does every symbolic fraction/mixed numeral use a built-up horizontal-vinculum form with visible clearance?
19. Does each upper question use a response structure students have practised or explicitly approved?
20. Are Q7 and Q8 independent, self-contained complex problems, Q7 principally B and Q8 principally A?
21. Does Q8 deepen the mathematics without unfamiliar puzzle protocol, exhaustive-search proof or prescribed pathway?
22. Can Q8 be understood/solved without reading or completing Q7?
23. Are Q7/Q8 prose-first, requiring extraction of relevant quantities/conditions/relationships from sentences?
24. If Q7/Q8 includes a display, is it mathematical evidence rather than a solution organiser?
25. Does every sentence read naturally aloud as age-appropriate classroom English?
26. Where a visual is central, is it meaningful, editable and large enough to use?
27. Does Q8 satisfy at least three substantive demand features including inference/dependency/interacting constraint and a justified conclusion?
28. Has every item been independently solved, with all values, units, diagrams, conclusions and mark allocations checked?
29. Is Page 1 fixed as Q1 top-left, Q2 top-right, Q3 middle-left, Q4 middle-right, Q5 bottom-left, Q6 bottom-right?
30. Can the marking key be added to an exact duplicate of the test without changing student-facing elements?
31. Does the rationale describe actual questions, answers, demand, mark evidence and evidence envelope without overstating curriculum coverage?
32. Does every marked response require the student to derive, construct, decide, interpret or justify something not already supplied?
33. Is each question's mark value proportional to the actual evidence demanded?
34. Is every response label/box/table/ruled area mathematically necessary and justified?
35. Does a validated `assessment-spec.json` contain exact prompt, answer, solution, mark evidence, band evidence where applicable, representation purpose, response-space decision and curriculum alignment?
36. For v4, does the Student Test omit internal D/C/B/A band metadata?
37. For legacy/source-preservation tasks, is the source architecture retained rather than silently migrated to v4?

## 7. Rendered-package release gates

After authoring, apply all pre-production gates again to the rendered Student Test, Marking Key and Curriculum Rationale. Then reject the package if any answer below is no:

1. Are both PowerPoints A4 portrait and exactly three slides in the required page sequence unless an approved exception exists?
2. Does Page 1 use exact `1–2 / 3–4 / 5–6` cell order?
3. Are test/key identical in slide order, question wording, diagrams, original marks, response spaces and base geometry, with only teacher material added?
4. Is `MARKING KEY` visible on every key page?
5. Are student instructions/readability adequate at actual A4 size and above required floors?
6. Are marking-key answers/criteria readable at actual A4 size and above required floors?
7. Does a 100%-scale render show no clipping, collisions, crowding, weak contrast, tiny diagrams or insufficient response space?
8. Do fractions retain clear numerator-to-vinculum spacing?
9. Are required visual models large, accurate, editable, greyscale-safe and mathematically useful?
10. Do Q7/Q8 still present information through natural prose with supporting visuals only when mathematically necessary?
11. Does the marking key show one distinct usable criterion for every allocated mark, acceptable alternatives, units and follow-through where appropriate?
12. For v4, does the key's teacher-facing score table exactly show E 0–4, D 5–9, C 10–15, B 16–20, A 21–25?
13. For v4, does the Student Test contain no internal evidence-band labels or teacher-only cut-off logic?
14. For v4, does the Curriculum Rationale accurately show 5D / 8C / 5B / 7A and the 5/3/3 structural proof?
15. For v4, do teacher-facing outputs explicitly describe the result as indicative evidence on the assessed component rather than a reporting grade?
16. Do rationale, test and key agree exactly on curriculum codes, question descriptions, values, answers, mark totals and demand claims?
17. Does the rationale have no blank spill page, clipped table, orphaned heading or unreadably dense text?
18. Have overflow/package-integrity/page-count checks passed without substituting for visual/pedagogical review?
19. Does a final student-perspective read-through find every question natural, unambiguous and solvable without teacher paraphrasing?
20. Does the release ledger contain zero failures, warnings, conditional passes or deferred fixes?
21. Do source spec, stable names and audit prove page positions, fraction clearances, response-space choices, font minimums and test/key duplication?
22. Have both authoring QA and fresh artifact-only review passed with separately recorded evidence/review mode?

A file can pass automated checks and still fail because its mathematics, evidence bands, demand, wording, visuals, notation, annotations, response space, test/key fidelity or rationale alignment is below standard. Fix and rerun the full release pass; do not deliver with a caveat.

## 8. Required evidence and audit execution

For creation/revision retain until release:

- validated `assessment-spec.json`;
- complete JSON release ledger;
- final deterministic audit report;
- full-resolution rendered images/PDFs used for visual inspection;
- for v4, the approved question set containing mark-level evidence-band metadata.

The specification validator and package auditor are compulsory controls. Automated checks do not judge natural language, curriculum validity, mathematical demand or visual usefulness; those remain review gates supported by specific evidence.

## Visual evidence gate

Apply `standards/visual-standard.md` to every visual. Confirm declared purpose/removal effect matches the construct, mathematical information is accurate, colour is not the sole cue, print dimensions are legible and Q7/Q8 demand is preserved. Decorative, untraceable or solution-ready visuals fail the content gate.