# Assessment design and quality gates

## Contents

0. Binary release rule
1. Quality hierarchy
2. Mandatory design matrix
3. Coherence and variation rules
4. Mark-allocation rules
5. Transformations benchmark
6. Pre-production rejection gates
7. Rendered-package release gates
8. Required evidence and audit execution

## 0. Binary release rule

Readiness is binary: **READY** or **NOT READY**.

- Any identified correction affecting curriculum alignment, mathematical accuracy, question meaning, natural wording, cognitive demand, diagnostic value, notation, visual representation, accessibility, response space, print legibility, marking reliability, file consistency or package completeness is a release barrier.
- Do not use `minor`, `non-barrier`, `acceptable for now` or similar language to permit delivery while a known correction remains open. These terms may describe the effort required to fix an issue, never its readiness status.
- An optional stylistic preference is non-blocking only when no correction is recommended and it has no effect on use, interpretation, marking or print quality.
- For a creation or revision task, fix every identified issue within scope and repeat the affected checks plus the complete rendered-package release pass.
- For a review-only task, return **NOT READY** whenever any correction is required. Do not call the assessment ready with reservations.
- Do not deliver, publish or save a final package until the release ledger contains zero open issues.

Maintain the JSON release ledger defined in `assessment-production-contract.md` during authoring and review. Every gate must record `PASS`. A warning, conditional pass, unverified assumption or promised future print check counts as `FAIL` until resolved. A prose claim that checks passed is not a substitute for the ledger or the deterministic audit report.

## 1. Quality hierarchy

Judge assessment quality in this order:

1. exact alignment to the taught curriculum;
2. intentional balance across the essential concepts in the topic;
3. coherent cumulative progression from accessible evidence to transfer and evaluation;
4. diagnostic value for identifying specific misconceptions and next teaching steps;
5. purposeful variation in mathematical action and representation;
6. readable, consistent and printable page design.

Do not reverse this order. A collection of visibly different task formats is not stronger merely because it looks varied. A coherent sequence of recognition, construction, description, discrimination and composition can provide better evidence than unrelated task novelties.

## 2. Mandatory design matrix

Complete all eight rows of this matrix before authoring slides. Keep it as an internal planning artefact unless the user requests it, then adapt its evidence into the curriculum-rationale table.

| Q | Marks | Curriculum concept | Observable evidence | Mathematical action | Representation | Diagnostic purpose | Dependency and follow-through | Mark evidence |
|---|---:|---|---|---|---|---|---|---|
| Q1 | 1 |  |  |  |  |  |  |  |
| Q2 | 1 |  |  |  |  |  |  |  |
| Q3 | 2 |  |  |  |  |  |  |  |
| Q4 | 2 |  |  |  |  |  |  |  |
| Q5 | 3 |  |  |  |  |  |  |  |
| Q6 | 3 |  |  |  |  |  |  |  |
| Q7 | 4 |  |  |  |  |  |  |  |
| Q8 | 4 |  |  |  |  |  |  |  |

Use precise actions such as identify, construct, calculate, represent, describe, compare, infer, critique, reverse and justify. In the last column, list the distinct evidence for every allocated mark.

Before approval, also list the topic's essential concepts and record whether each is:

- directly assessed;
- indirectly assessed through a connected question; or
- intentionally omitted, with a reason.

Do not let one convenient representation or procedure dominate merely because it is easy to lay out or mark.

Before slide production, add a short readiness record for each question covering:

- a plain-language restatement of what the student must determine;
- the independently verified answer and solution path;
- why the wording has only one reasonable mathematical interpretation;
- whether a visual model is mathematically purposeful, intentionally omitted or required;
- the exact evidence earning each mark; and
- for Q7 and Q8, the information students must extract from the prose and the demand features that prevent the task from being a routine Q5/Q6 item.

## 3. Coherence and variation rules

Plan for cumulative evidence:

- Q1-Q2 establish accessible foundations or distinguish essential properties.
- Q3-Q4 require accurate construction, calculation, representation or interpretation.
- Q5-Q6 connect procedures with descriptions, verification, comparison or a second representation.
- Q7 establishes one clear main problem and interrupts routine application through inference, comparison, reverse process or transfer.
- Q8 presents one independent, self-contained A-level problem and deepens the mathematics through a changed value, condition or target, a missing relationship, a reverse process or a connected evaluation. It must not extend or depend on Q7.

Use variety to expose different mathematical evidence, not to decorate the assessment.

Accept repeated mathematical actions when they:

- deliberately contrast two concepts;
- reveal whether a student preserves an invariant;
- isolate a known misconception;
- extend one process into a more demanding connected process; or
- create a coherent sequence that prepares for Q7 and Q8.

Reject or revise repetition when adjacent questions merely change the numbers, shapes, names or context while eliciting the same evidence. As a warning sign, review any draft where more than half of Q1-Q6 use the same mathematical action without an explicit diagnostic rationale.

Across the complete assessment, require several substantive actions such as recognition, construction, description, comparison, inference, evaluation and justification. Do not maximise the action count at the expense of topic coherence.

## 4. Mark-allocation rules

Assign marks to meaningful mathematical evidence:

- the correct concept or relationship;
- a viable model, construction or strategy;
- an important intermediate dependency;
- accurate completion;
- verification, comparison or justification.

Do not split one routine act mechanically across vertices, digits, rows, objects or written steps. For example, a three-mark rotation construction should normally distinguish:

1. correct centre and angle or a valid construction method;
2. correct direction/orientation and preservation of the figure;
3. complete accurate final image.

Award one mark per vertex only when locating individual image points is itself the explicitly intended evidence.

## 5. Transformations benchmark

For Year 6 transformations, inspect `../assets/year-6-transformations-quality-benchmark.pptx`. Treat it as a benchmark for curriculum coverage, diagram quality and page hierarchy. Do not copy its misconception-critique or transformation-card response formats into unrelated topics, and do not let it override the direct problem-solving architecture.

The benchmark is strong because it:

- balances translation, reflection and rotation;
- builds from recognition through construction and description to discrimination and composition;
- uses Q7 to expose misconceptions about transformation type, rotation angle, centre and orientation;
- uses Q8 to determine an unknown order of transformations, construct the intermediate image, verify with coordinates, reverse the order and explain why the result changes;
- uses the Cartesian plane as mathematical evidence rather than decoration, provided coordinates were part of the taught unit;
- keeps diagrams at a consistent functional scale and reserves substantial space for the task.

Use this progression as the Year 6 transformations design target:

| Stage | Evidence |
|---|---|
| Q1-Q2 | Recognise and distinguish essential transformation properties |
| Q3-Q5 | Accurately construct translation, reflection and rotation |
| Q6 | Describe or connect transformations precisely |
| Q7 | Diagnose and correct a misconception using centre, angle and orientation evidence |
| Q8 | Determine, test and justify the order of composed transformations |

Do not copy the benchmark mechanically. Adapt the progression to the exact content taught. Omit coordinate verification when Cartesian coordinates have not been taught as part of the unit.

## 6. Pre-production rejection gates

Reject the draft before PowerPoint production if any answer is no:

1. Does the concept list show intentional topic coverage rather than accidental emphasis?
2. Does every question have a distinct diagnostic purpose?
3. Can the progression be stated as one coherent cumulative sequence?
4. Does any repeated action have an explicit contrast, diagnostic or progression reason?
5. Does every mark represent meaningful mathematical evidence rather than mechanical task fragments?
6. Do Q7 and Q8 meet the cognitive-demand reference without relying on untaught content?
7. Will incorrect responses identify useful reteaching needs?
8. Can a student at the assessed year level tell exactly what to do, how many responses to give, where to record them and what evidence is required without teacher paraphrasing?
9. Does the proposed page layout give the required diagram, construction, working and explanation enough blank, unlined space, with no generic ruled lines or pre-divided working steps?
10. Do all mathematical diagrams follow `mathematical-diagram-conventions.md`, including whole-shape placement, triangle vertices and transformed-image labels?
11. Does every symbolic fraction and mixed numeral use a built-up numerator-over-denominator form with a horizontal vinculum, with no forward-slash, diagonal-slash or vulgar-fraction substitute?
12. Does each upper question use a response structure students have practised or that the user has explicitly approved, and has any rejected question family been replaced rather than cosmetically rewritten?
13. Are Q7 and Q8 independent, self-contained complex problems, with Q7 targeting B-level reasoning and Q8 targeting A-level reasoning?
14. Does Q8 deepen the mathematics without switching to an exhaustive-search proof, person-claim critique, unfamiliar response protocol or prescribed solution pathway?
15. Can Q8 be understood and solved without reading or completing Q7?
16. Are Q7 and Q8 prose-first word problems in which students must extract the relevant quantities, conditions and relationships from sentences, rather than receiving a pre-organised solution table, list or labelled data display?
17. If a table, diagram, graph, number line or model appears in Q7 or Q8, is it itself mathematical evidence to interpret rather than a device that removes the need to unpack the written situation?
18. Does every sentence read naturally aloud as age-appropriate classroom English, without compressed pseudo-table wording, awkward repetition or an artificial list disguised as a sentence?
19. Where a visual representation is central to the concept or needed to vary the evidence, does the draft include a meaningful, editable mathematical model rather than relying only on symbols and prose?
20. For every fraction, is there planned visible white space between the numerator and the vinculum, with no contact or perceived contact at normal A4 viewing size?
21. Does Q8 satisfy at least three substantive demand features, including at least one inference, dependency or interacting constraint, and require a justified conclusion? Conceptual subtlety or extra arithmetic alone is insufficient.
22. Has every item been independently solved, with all values, units, diagrams, conclusions and mark allocations checked against the exact question wording?
23. Is the exact Page 1 order fixed as Q1 top-left, Q2 top-right, Q3 middle-left, Q4 middle-right, Q5 bottom-left and Q6 bottom-right?
24. Can the marking key be added to an exact duplicate of the final test without shrinking, obscuring or changing any student-facing element?
25. Does the rationale describe the actual questions, answers, demand and mark evidence without overstating curriculum coverage or achievement-level demand?
26. Does every marked response require the student to interpret, derive, construct, decide or justify something that is not already stated or made automatic by the stem or stimulus?
27. Is each question's mark value proportional to the mathematical work demanded, so Q5-Q6 do not award three marks for three supplied or obvious observations?
28. Is every response label, final-answer box, table, ruled area or other scaffold mathematically necessary, explicitly justified in the specification and proportionate to the response? Blank, unlined space is the default.
29. Does a validated `assessment-spec.json` contain the exact prompt, independently checked answer, solution path, mark evidence, representation purpose, response-space decision and curriculum alignment for every question, including every user-authorised extension or exception?

## 7. Rendered-package release gates

After authoring, apply **all 29 pre-production gates again** to the rendered student test, rendered marking key and rendered rationale. Then reject the package if any answer below is no:

1. Are both PowerPoints exactly A4 portrait and exactly three slides in the required page sequence?
2. Does rendered Page 1 use the exact `1–2 / 3–4 / 5–6` cell order?
3. Are the test and marking key identical in slide order, question wording, diagrams, original marks, response spaces and page geometry, with only teacher answers and annotations added?
4. Is `MARKING KEY` visible on every marking-key page, with no dropped headers or export omissions?
5. Are all student instructions and response expectations readable at actual A4 size, with student body text at least 10.5 pt unless a larger mathematical label standard applies?
6. Are all marking-key answers, worked solutions and mark annotations readable at actual A4 size, high contrast and at least 10 pt? Shorten or reposition annotations instead of reducing their type.
7. Does a 100%-scale A4 render show no clipping, overflow, collisions, crowding, weak contrast, tiny diagrams or insufficient response space? A zoomed digital view alone is not evidence of print legibility.
8. Does every fraction show clear numerator-to-vinculum white space at both normal page view and zoomed inspection, with no numerator touching or appearing to touch the bar?
9. Are required visual models large, accurate, editable, greyscale-safe and genuinely useful for eliciting the intended mathematics?
10. Do Q7 and Q8 still present their information through natural prose sentences, with supporting visuals only where those visuals are part of the mathematics?
11. Does the marking key show the independently verified answer, four distinct marks for Q7 and Q8, acceptable alternatives, units and follow-through where appropriate, without covering the task?
12. Do the rationale, test and key agree exactly on curriculum codes, question descriptions, values, answers, mark totals and demand claims?
13. Does the rationale have no blank, unnecessary spill page, clipped table, orphaned heading or unreadably dense text?
14. Have the overflow checker, package-integrity checks and slide/page count checks passed without treating automated success as a substitute for visual or pedagogical review?
15. Does a final student-perspective read-through find every question natural, unambiguous and solvable without teacher paraphrasing?
16. Does the release ledger contain zero failures, warnings, conditional passes or deferred fixes?
17. Do the source specification, stable element names and package audit prove the required page positions, fraction-component clearances, response-space choices, font minimums and test/key duplication rather than leaving them to memory or visual estimation alone?
18. Have both the authoring QA pass and the fresh artifact-only review passed, with their evidence and review mode recorded separately in the release ledger?

A file that passes automated overflow checks can still fail release because its mathematics, demand, wording, visuals, notation, annotations, response space, test/key fidelity or rationale alignment is below standard. Fix the issue and rerun the complete rendered-package release pass; do not deliver with a caveat.

## 8. Required evidence and audit execution

For creation and revision, retain these working artefacts until release:

- the validated `assessment-spec.json`;
- the JSON release ledger with `P01`-`P29` and `R01`-`R18` all recorded as `PASS`;
- the final deterministic audit report;
- rendered images or PDFs used for the 100%-scale visual inspection.

The specification validator and package auditor are compulsory controls. Run them as described in `assessment-production-contract.md`. Automated checks do not judge natural language, curriculum validity, mathematical demand or visual usefulness; those remain human-review gates and must be supported by specific evidence in both review passes.
