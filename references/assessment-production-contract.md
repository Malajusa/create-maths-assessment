# Assessment production contract

Use this fail-closed workflow for every assessment creation or revision. The source specification, all three deliverables and the release ledger form one package. If any control reports `NOT READY`, correct the source, rebuild the affected files and repeat the complete audit.

## 1. Create one source of truth

Before authoring slides, create `assessment-spec.json` with `schema_version: 1`. Start from `examples/benchmarks/year5-fractions-percentages-release-spec.json`; replace its content rather than copying its mathematics into an unrelated assessment.

Resolve a visual profile before document construction. Visual profiles control presentation
only and never override the validated assessment content. The default is
`assets/visual-profiles/classic-assessment-v1.json` unless the brief contains an approved
typed `visual_profile`.

The specification must contain:

- assessment title, assessed year levels and exact curriculum entries;
- each curriculum entry classified as `direct` or `authorised_extension`;
- the user's explicit authorisation and affected question IDs for every extension;
- total marks, topic subtotals and exact Page 1 positions;
- Q1-Q8 prompt, answer, solution path, mathematical action, diagnostic purpose and observable evidence;
- one distinct evidence statement for every mark;
- the response-space type and the mathematical justification for every field, label, table or scaffold;
- the purpose or defensible omission of each representation;
- every displayed fraction instance that must be built from named numerator, bar and denominator elements;
- student-clarity, natural-wording, self-answering, independent-solution and proportional-mark review assertions;
- Q7/Q8 prose extraction, independence, demand features and justified-conclusion evidence; and
- expected package and rationale page counts.

Do not use the assertions to excuse weak content. They are explicit reviewer decisions that must be rechecked against the rendered artefacts.

## 2. Run preflight before authoring

Run:

```bash
python scripts/validate_assessment_spec.py assessment-spec.json
```

The validator rejects, among other failures:

- wrong mark totals, missing topic subtotals or an incorrect `1–2 / 3–4 / 5–6` layout;
- missing, duplicated or disproportionate mark evidence;
- unjustified response labels, answer boxes, tables or scaffolds;
- a fraction item in Q1-Q6 without a purposeful visual model;
- unregistered fraction instances;
- Q7/Q8 that are not independent prose-first word problems;
- a Q8 with fewer than three substantive demand features, no inference/dependency/interacting constraint, or no justified conclusion;
- undeclared or unauthorised higher-year content; and
- any unverified wording, solution or self-answering assertion.

Treat every error code as a release barrier. Do not begin PowerPoint construction until preflight reports `READY`.

## 3. Build all outputs from the specification

Use the specification as the content source for the student test, marking key and rationale. Do not maintain separate prompt, answer or mark-allocation copies.

- Place Page 1 questions directly into the final six cells.
- Create the marking key by duplicating the completed test, then add only `qN-key-*` elements.
- Use the stable names in `powerpoint-output.md` so geometry, fonts, fractions and duplication can be audited.
- Use blank, unlined response space unless the specification records a mathematical reason for another structure.
- Reserve contiguous response space before diagrams and decoration. Reflow a layout that
  cannot satisfy the profile; do not silently shrink essential mathematical text to the
  safety floor.
- Page 1 question elements must remain inside their own question-cell region even when they
  remain within overall slide bounds.
- Treat required diagram scale, hierarchy and page balance as positive production
  requirements, not merely the absence of clipping.
- Keep curriculum codes, extensions, marks, answers and demand claims identical across all three files.

## 4. Complete two review passes

### Authoring QA

Solve every question independently and review the source and rendered output against P01-P29 and R01-R18. Record the exact evidence inspected, not only `looks correct`.

### Fresh artifact-only review

Begin from the final renders, specification and curriculum references without using the author's intended interpretation as evidence. Use an independent reviewer when available and authorised. Otherwise run a deliberately separate artifact-only pass. Record the review mode as `independent_reviewer` or `fresh_artifact_only`.

The second pass must specifically attempt to find:

- wording that needs teacher paraphrasing;
- a stem or stimulus that supplies its own marked answer;
- marks unsupported by distinct mathematical evidence;
- routine Q7/Q8 demand;
- decorative or missing representations;
- unnecessary labels, answer boxes or tables;
- fraction collisions;
- sub-minimum marking annotations; and
- disagreement among the test, key and rationale.

## 5. Maintain the release ledger

Use JSON with this structure:

```json
{
  "assessment_spec_sha256": "<sha256 of assessment-spec.json>",
  "reviews": [
    {"role": "authoring_qa", "reviewer": "<identifier>", "mode": "authoring_qa", "completed": true},
    {"role": "fresh_review", "reviewer": "<identifier>", "mode": "fresh_artifact_only", "completed": true}
  ],
  "gates": [
    {"gate": "P01", "evidence_inspected": "<specific evidence>", "status": "PASS", "correction_made": "none"}
  ],
  "open_items": []
}
```

Include every gate from `P01` to `P29` and `R01` to `R18` exactly once. The package audit rejects missing gates, duplicate gates, non-specific evidence, any status other than `PASS`, incomplete reviews, identical reviewer records or open items.

## 6. Run the package audit

After final rendering and visual inspection, run:

```bash
python scripts/audit_assessment_package.py \
  --spec assessment-spec.json \
  --test Topic_Test.pptx \
  --key Topic_Marking_Key.pptx \
  --rationale Topic_Curriculum_Rationale.pdf \
  --ledger release-ledger.json \
  --design-manifest design-manifest.json \
  --report assessment-audit.json
```

The auditor verifies the source preflight again, file integrity, A4 dimensions, slide/page counts, Page 1 positions, original test/key identity, stable names, explicit font minimums, mark labels, key coverage, `MARKING KEY` headers, fraction-component clearance, banned slash fractions, response-space agreement, prohibited unexplained labels, Q7/Q8 table use, page bounds, rationale tokens and the complete release ledger.

It does not replace mathematical or pedagogical judgement. `READY` requires both the recorded review gates and the mechanical audit to pass.

The Document Builder must also emit `design-manifest.json`, conforming to
`schemas/design-manifest.schema.json`. Fresh review must compare that manifest with the
actual render; a manifest assertion is evidence to inspect, not proof by itself.

## 7. Regression control

Run before committing a skill change:

```bash
python scripts/test_assessment_workflow.py
```

The regression suite must accept the controlled positive specification and reject cases representing the failures that prompted this contract: swapped Page 1 cells, missing fraction visuals, self-answering or artificial wording, routine Q8 demand, undeclared extension content, redundant response scaffolds, touching fractions and sub-10 pt marking annotations.

When a new defect reaches review, add a failing fixture before changing the rule or script. Keep the fixture focused on the invariant that failed; do not turn one topic-specific preference into a universal rule.
# Visual-system evidence

The builder must resolve the selected visual profile, token set and asset manifest before layout. `design_manifest.visual_system` records their SHA-256 hashes and one entry for every rendered question visual: asset IDs or constructor ID, family, scale state, measured printed dimensions, greyscale review and demand-preservation review. Student-test and marking-key base visuals must remain identical; marking overlays are additive.
