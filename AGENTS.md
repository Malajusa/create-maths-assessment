# Agent Execution Rules

These instructions apply to every agent operating in this repository.

## Authority

1. Explicit user instructions are highest priority.
2. `SKILL.md` defines pipeline order.
3. `standards/` contains canonical quality requirements.
4. `orchestration/pipeline.json` defines ownership, retries and invalidation.
5. Exemplars guide only the dimensions assigned to them and cannot override newer canonical rules.

Read `standards/project-context.md` before each stage. Preserve its general/scoped distinction; do not turn an earlier one-question correction into a new universal requirement. Pass required visual, response-space, cognitive-demand and evidence-band decisions through the existing structured contracts before layout.

For new Years 3–10 v4 assessments, read `references/evidence-band-standard.md`. Treat the **individual mark criterion** as the evidence-band authority. Do not infer D/C/B/A from question number, arithmetic size, wording length or an expected quota.

## Separation of authority

Generating agents may propose and repair content but cannot mark their own work as valid.

Only:
- `05-maths-pedagogy-validator` may pass the content gate;
- `07-release-qa` may issue the final `READY` status.

Different role labels in one execution are not independent agents. Do not invent execution identities, review records, source facts or audit results. Missing independent review is a barrier. Read `standards/release-evidence.md` before release or resumed delivery.

## No silent changes

If an approved question changes after content validation:
- re-run mathematical and evidence-band validation;
- synchronise the marking key;
- update the rationale if affected;
- re-render the changed page;
- re-run release QA.

Do not silently migrate an exact legacy assessment, key-only request, PP–Y2 task or WACE task into the v4 25-mark envelope.

## V4 criterion evidence integrity

When `criterion_component_estimate_v1` applies:

- total marks = 25;
- whole-assessment evidence = 5D / 8C / 5B / 7A;
- indicative task/component bands = E 0–4, D 5–9, C 10–15, B 16–20, A 21–25;
- C/B/A boundaries must structurally force at least 5 C+, 3 B+ and 3 A marks respectively;
- C is the current year-level expected-standard anchor;
- if honest mathematics cannot realise the envelope, return an architecture barrier rather than inflate bands.

The v4 result is an indicative standard on the assessed component, not the student's reporting grade.

## Repair discipline

Repair the smallest owning component. Do not regenerate the whole assessment when a targeted repair is sufficient. Invalidate affected descendants using the dependency graph; preserve unaffected sibling questions and unrelated open barriers. Reject invalid replacements before changing recorded state.

After three failed repairs of the same barrier, discard the approach and replace it with a materially different one.

## Evidence

Agents must report concrete defects, not vague quality impressions. Every failure record needs:
- question or artefact;
- category;
- description;
- owner;
- required fix.

For v4 evidence-band defects, identify the exact mark criterion and why its claimed band exceeds the observable evidence.

## Runtime enforcement

When the Python runtime is available, every structured hand-off must be recorded through `runtime/controller.py`. Do not advance based only on prose claims that an earlier stage passed. The controller state is authoritative for stage completion and gate status.

READY additionally requires current file hashes, an independent page-review record, full-resolution renders and a newly executed package audit. A saved or synthetic READY string cannot substitute for evidence. Reopening READY rechecks it.

On interruption, inspect the actual run directory before reporting progress. Verify exact deliverable paths before linking. Keep implemented, tested, pushed, merged and installed status separate; never change unrelated sibling skills to make a repository appear clean.
