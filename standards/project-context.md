# Project decisions and regression lessons

These are enduring decisions from the Maths assessments project, not a new curriculum or permission to infer teacher requirements. Read this with the existing canonical standards. Apply the current explicit request first; preserve the distinction between a general rule and a correction to one assessment.

## Authority and scope

| Decision source in project context | Requirement retained | Boundary |
|---|---|---|
| 29 July 2026: output and key requests | Student Test and Marking Key in A4 portrait PowerPoint; Curriculum Rationale in PDF. The key duplicates the exact final test and adds solutions and marks. | A key-only request for an uploaded presentation does not authorise a replacement assessment or three unnecessary new documents. |
| 29 July 2026: quality comparison and labelling | Use the user-approved benchmark dimensions, not the model's preferred aesthetic. Observe mathematical labelling conventions; put a shape identifier centrally unless that obstructs the mathematics. | Do not infer which similarly named upload was preferred. Vertex labels and shape identifiers have different purposes. |
| 13–18 August 2026: Q7/Q8 corrections | Two independent, meaningful, prose-first problems. Q7 targets B-level reasoning and Q8 A-level reasoning. Students extract information and choose a strategy. | Q8 does not extend Q7, reuse its required answer, or depend on its model. Intended demand is not an automatic grade conversion. |
| 25 August 2026: repeated reviews | Previously dismissed 'non-barrier' defects are release barriers. Remove unnecessary instructions, labels, boxes and artificial wording. | A question is not complex merely because it is wordy, worth four marks or uses larger numbers. |
| 8–9 September 2026: failed deliveries and false READY | Require real files, current evidence, complete rendered inspection and actual audit execution. Report missing or failed stages truthfully. | A plan, a fixture, a source-code test pass or a document existing is not classroom-release approval. |
| 9 September 2026: visual-system approval | Preserve the newer correctness/QA architecture while restoring the approved assessment-native visual standard. Use the visual specifications, profile, tokens and geometry/provenance checks already in the repository. | Older exemplars are visual-only where designated; do not import their old curriculum or weaker assessment demand. |
| 9 September 2026: judging standards | Use the supplied 2016 judging standards as loose calibration for Pre-primary to Year 6, alongside current curriculum. | They are not a strict checklist, not 2026 curriculum authority, and not a reason to import superseded content. Year 7 judging-standard work was deferred, not Year 7 assessment creation. |

## Generation requirements

Preserve the default eight-question, 20-mark structure: 1, 1, 2, 2, 3, 3, 4, 4. Follow the canonical Page 1 six-cell placement and separate Q7/Q8 pages, rather than inventing a new reading order. Match demand, mark allocation and response space; do not turn varied tasks into repeated calculation templates.

Before layout, Agents 02–04 must carry the intended evidence, response-space needs, visual purpose and demand-preservation decisions in the existing blueprint/question/visual contracts. The document builder must not invent these to fill an empty template.

Q7/Q8 must begin with a situation students can interpret. A useful supporting diagram or number line is permitted, but a solution-ready table, forced decomposition or instruction-by-instruction recipe must not do the intended reasoning for them. Routine conversions with a story attached, or an abstract factor-pair exercise labelled 'complex', do not establish the required demand. Explain the actual inference, interacting constraints, transfer or justified conclusion in the teacher-facing evidence.

Use Australian English. Preserve the requested mathematical scope and verified curriculum codes. Make the rationale describe the final questions rather than the original ambition. Do not invent curriculum claims, prerequisite requirements, classroom conditions or teacher instructions.

## Visual and marking-key floor

Check at full page resolution and at intended print scale. Being inside slide bounds and above a minimum font size is not sufficient: hierarchy, balance, diagram prominence and usable writing space must also meet the approved profile.

Every question-owned element stays in its own cell. Reject misaligned right-column content, lines crossing cell boundaries, mark badges crossing labels, tiny dimension text, ambiguous prism edges, or flat/ambiguous object representations. Assess what the rendered diagram actually communicates, not what its author intended.

The marking key must preserve student wording, numbers, diagrams, order and base layout. Add integrated, readable worked solutions and distinct observable mark criteria. Reject solution panels that obscure the student diagram or response structure, cramped explanations, overlapping criteria, and marking instructions requiring a teacher to invent the allocation.

For an uploaded assessment, record the exact source filename and hash and work from that file, not a remembered or similarly named version. For an equivalent Version B, retain structure, constructs, demand, representation type and mark scheme while changing the requested values; independently solve the new values and update the exact matching key and rationale where requested.

## Topic-specific precedents, not universal templates

The ordering/comparing-fractions work required comparison, not an unrequested test of adding fractions. Its approved problem ideas included friends disputing which fraction is greatest and a separate named-walker number-line problem from 0 to 3 in sevenths, without telling students the partition size. These illustrate interpretation and strategy choice; do not paste them into unrelated topics.

The request to replace one Q6 with finding 10% of a quantity applied to that assessment. It does not require Q6 in every topic to assess percentages. Likewise, do not silently generalise a one-question correction into a new curriculum prohibition.

## Execution, repair and truthful delivery

Run the controller when Python is available. Separate actual agent executions from a single model adopting role labels. Do not call a self-review independent; absent required independent review, record NOT READY with the missing evidence. See `standards/release-evidence.md`.

Repair the smallest owning component. Use the dependency graph to invalidate affected descendants while preserving valid independent sibling questions. Keep unrelated unresolved barriers open. An invalid repair must not destroy the last recorded state. After the third failed targeted repair, replace the approach rather than repeating cosmetic changes.

On interruption, inspect the current run state and files. Report the last completed stage, existing deliverables and remaining barrier. Resume from valid evidence; do not infer progress from an earlier promise, claim background work, silently regenerate unaffected work or report completion with no output.

Before delivery, verify each exact file path, current hash and final audit, then link to those actual files. Do not hand-type a different filename or invent a sandbox path from a document title. Changes to the final files invalidate their previous review evidence.

Keep maintenance status separate from assessment status: implemented, tested, pushed, merged, packaged, installed and deployment-verified are different claims. State the actual commit and verified installation target when known. A workspace copy is not proof that the user's installed skill changed. Never clean, overwrite or commit unrelated sibling skills to make a surrounding repository appear clean.
