# A4 portrait PowerPoint output

Use this workflow for a complete assessment package or whenever the user requests PowerPoint.

## Set the output contract

- Deliver three separate files for a complete package: `<Topic>_Test.pptx`, `<Topic>_Marking_Key.pptx` and `<Topic>_Curriculum_Rationale.pdf`.
- Use true A4 portrait dimensions for both PowerPoints: 210 mm wide by 297 mm high.
- Treat each PowerPoint as a printable assessment, not as a widescreen projector deck.
- Put one printable assessment page on each slide in both PowerPoints.
- Keep student pages uncluttered, greyscale-safe and economical to print.

## Use the canonical assessment layout

Use one consistent visual system across every run:

- A4 portrait with balanced outer margins and a compact header;
- one clear sans-serif family throughout;
- consistent question-number, instruction, mark-label and final-answer-field styles;
- restrained black, grey and blue only, with blue reserved for marking-key annotations;
- diagrams at a consistent functional scale unless the mathematics requires a deliberate change;
- diagram labels placed consistently according to `mathematical-diagram-conventions.md`;
- thin, unobtrusive cell borders and no heavy answer panels;
- page numbering, student name fields and total marks in consistent positions.

Page 1 must read as one organised assessment page rather than six unrelated cards. Use a two-column by three-row grid, but vary internal response space where a construction or explanation needs more room. Keep Q1-Q2 concise so Q3-Q6 are not compressed.
The grid order is fixed: Q1 top-left, Q2 top-right, Q3 middle-left, Q4 middle-right, Q5 bottom-left and Q6 bottom-right. Place each question directly into its final cell from the validated specification; do not build a topic-column layout and reorder it later. Any other ordering is a release failure.

On Pages 2 and 3, give the mathematical diagram, model or working area visual priority. Place instructions close to the relevant representation and reserve a blank, unlined explanation area sized for the expected response.

Keep calculation, reasoning and explanation working areas blank and unlined. Do not add ruled lines, dotted writing guides, repeated underscores or pre-divided step boxes. A label such as `Working and check` or `Answer:` and any bordered final-answer field require a question-specific mathematical justification in `assessment-spec.json`; omit them when blank space already makes the response location clear. Use tables, grids or labelled fields only when that structure is part of the mathematics being assessed.

When reviewing a proposed layout, compare its hierarchy and use of space with `../assets/year-6-transformations-quality-benchmark.pptx`. Use that file as a quality reference, not as a topic-independent content template.

## Build the test PowerPoint

1. Student page 1: Q1-Q6 in the required readable six-cell grid.
2. Student page 2: Q7 only.
3. Student page 3: Q8 only.

For parallel or mixed-year versions, keep each student paper self-contained and keep year-specific alignment and judgement criteria separate.

Do not include worked answers, curriculum rationale, administration guidance or teacher-only slides in the test.

## Build the marking-key PowerPoint

1. Finish and verify the test PowerPoint first.
2. Duplicate the finished test so every slide, page break, question, diagram, mark label and response space begins identical.
3. Add the correct answer and sufficient model working directly in the relevant response or blank working space.
4. Show each allocated mark beside the exact mathematical evidence that earns it. Make the mark-by-mark breakdown explicit for multi-mark items.
5. Add concise notes for acceptable alternatives, units, labels and partial credit without obscuring the original question.
6. Keep the original question wording and total marks unchanged. Confirm that the allocations total 20 marks.

Keep annotations concise enough to preserve the assessment's visual hierarchy. If an answer explanation is cramped, reposition or shorten the teacher annotation while retaining the original test elements; do not shrink the underlying student question, diagram or response area.
Use at least 10 pt for every marking-key answer, worked-solution label and mark annotation at A4 print size. Do not solve crowding by dropping below this minimum. Confirm `MARKING KEY` is visible on all three pages after export.

Do not replace the duplicated assessment with answer tables or additional marking-guide slides. Use a consistent, high-contrast annotation colour so the worked solutions remain visibly distinct from the original test.

## Build the curriculum-rationale PDF

Load and follow the PDF skill. Include:

- assessment purpose, year level and topic;
- exact curriculum codes and relevant content-description wording;
- relationship to the complete year-level Achievement Standard;
- a question-by-question table mapping curriculum, observable evidence, demand and marks;
- explanation of the progression from Q1 to Q8;
- specific justification for the reasoning and transfer demands in Q7 and Q8;
- any previous-year overlap or higher-year content used, with the reason it is valid;
- administration conditions, permitted adjustments and neutral prompts;
- moderation notes and guidance for interpreting the pattern of evidence.

Keep the rationale separate from both PowerPoints.

## Author the PowerPoints

- Load and follow the Presentations skill.
- Use the presentation authoring library required by that skill; do not use `python-pptx`.
- Prefer native, editable PowerPoint text, shapes, tables and diagrams for newly created assessments.
- Preserve diagrams, grids, working space and mathematical notation accurately.
- Build every symbolic fraction as a numerator above a denominator separated by a horizontal vinculum. Prefer a reliable native equation object; otherwise compose the numerator, denominator and bar from aligned editable elements. For a mixed numeral, place the whole-number part beside the built-up fraction with clear baseline alignment and spacing. Never display fractions using a forward slash, diagonal fraction slash or single-character vulgar-fraction glyph.
- Leave visible white space between each numerator and its vinculum. If the numerator touches or appears to touch the bar in a normal A4 page render, rebuild the fraction; recognisability is not enough.
- Use full-page rendered images only when converting an already approved fixed-layout source and exact visual preservation is more important than editability. Tell the user when the delivered slides are image-based.
- Keep diagrams functional rather than decorative.
- Use type sizes suitable for a legible A4 print assessment. Treat this print-layout form factor as distinct from an on-screen presentation.
- Use at least 10.5 pt for student-facing body text and at least 10 pt for marking-key annotations. Larger type remains preferable where space permits.
- Add the required `[Sources]` block to speaker notes on each slide.

Use stable element names so the package can be audited. Apply these exact patterns:
- `qN-student-cell` for each Page 1 question-cell audit region;
- `qN-student-title` for an extended-response task title;
- `qN-student-prompt` for the principal student prompt block;
- `qN-student-dimension-<id>` for every essential geometric dimension label;

- `qN-student-anchor` for the question-number anchor;
- `qN-student-mark` for the original mark label;
- `qN-student-representation-<id>` for the auditable anchor of every purposeful model, diagram, table, graph or number line listed in the specification;
- `qN-student-response-blank`, `qN-student-response-final`, `qN-student-response-structured` or `qN-student-response-none` for the response-space anchor;
- `qN-student-frac-<id>-num`, `qN-student-frac-<id>-bar` and `qN-student-frac-<id>-den` for every student-facing built-up fraction;
- `qN-key-answer` and `qN-key-mark-<number>` for teacher answers and mark annotations;
- `qN-key-frac-<id>-num`, `qN-key-frac-<id>-bar` and `qN-key-frac-<id>-den` for fractions introduced only in the key.

Use a transparent, unbordered response-space anchor when the response area is intentionally blank. Names are audit metadata; they must not add visible scaffolding. Keep every student-named element unchanged when creating the marking key.

## Verify the artifact

1. Confirm both PowerPoints are exactly A4 portrait. In each PowerPoint package, `p:sldSz` should be `cx="7560000"` and `cy="10692000"`.
2. Confirm the test and marking key have the same slide count, slide order, questions, diagrams and original mark labels.
3. Render every slide in both PowerPoints individually.
4. Inspect every rendered slide for overflow, clipping, distortion, small type, weak contrast, unclear student instructions, insufficient response space and any ruled or over-scaffolded working area.
5. Run the presentation overflow and out-of-bounds checks required by the Presentations skill on both PowerPoints.
6. Compare the rendered files against the validated `assessment-spec.json`, repeat every pre-production gate and apply every rendered-package release gate in `assessment-quality-gates.md`; automated overflow success is not a pedagogical quality pass.
7. Render and inspect every page of the curriculum-rationale PDF.
8. Inspect labels visually at normal page view and zoomed view. Confirm whole-shape identifiers, triangle vertices, transformed images, sides, angles and coordinates follow `mathematical-diagram-conventions.md` and do not obscure relevant mathematics.
9. Inspect every fraction and mixed numeral visually at normal page view and zoomed view. Confirm each has a clear horizontal vinculum, readable numerator and denominator, correct alignment and no slash-form substitute. Check the test, marking key and curriculum-rationale PDF, including answer choices, diagrams, tables, number lines, labels, worked solutions and teacher annotations.
10. Read every question from the target student's perspective and independently confirm that the required action, response count, response location and visible evidence are unambiguous without teacher paraphrasing.
11. Independently confirm that all question text, worked solutions, marks, curriculum statements and teacher guidance match the approved assessment content.
12. Deliver all three final files, not only preview images or intermediate exports.
13. Inspect a 100%-scale A4 render of every page. A zoomed view alone does not establish print legibility; any unreadable or crowded element blocks release.
14. Confirm the release ledger has zero failures, warnings, conditional passes or deferred corrections before delivery.
15. Run `scripts/audit_assessment_package.py` with the final specification, test, key, rationale and ledger. Release only when it reports `READY`.
