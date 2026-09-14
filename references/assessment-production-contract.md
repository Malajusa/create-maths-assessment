# Assessment production contract

Use this fail-closed workflow for every assessment creation or revision. The source specification, deliverables and release ledger form one package. If any control reports `NOT READY`, correct the source, rebuild affected files and repeat the complete audit.

## 1. Create one source of truth

Before authoring slides, create `assessment-spec.json` with `schema_version: 1`.

For a new Years 3–10 assessment using the v4 criterion model, set:

```json
"evidence_model": "criterion_component_estimate_v1"
```

and record:

- total marks = 25;
- evidence envelope = `{"D":5,"C":8,"B":5,"A":7}`;
- indicative component bands = E 0–4, D 5–9, C 10–15, B 16–20, A 21–25.

Legacy/source-preservation tasks omit this model unless explicitly migrated. Exact supplied assessments, key-only requests and equivalent Version B tasks preserve the source architecture.

Resolve a visual profile before document construction. Visual profiles control presentation only and never override validated mathematics/content. Default: `assets/visual-profiles/classic-assessment-v1.json` unless the brief contains an approved typed `visual_profile`.

The specification must contain:

- assessment title, assessed year levels and exact curriculum entries;
- each curriculum entry classified `direct` or `authorised_extension`;
- user authorisation and affected question IDs for every extension;
- total marks, topic subtotals and exact Page 1 positions;
- Q1–Q8 prompt, answer, solution path, mathematical action, diagnostic purpose and observable evidence;
- one distinct evidence statement for every mark;
- for v4, each mark's `evidence_band`, `band_rationale`, `why_not_lower_band` and A-demand feature where required;
- for v4, whole 5D / 8C / 5B / 7A envelope and indicative bands;
- response-space type and mathematical justification for every field/label/table/scaffold;
- purpose or defensible omission of each representation;
- every displayed fraction instance built from named numerator/bar/denominator elements;
- student-clarity, natural-wording, self-answering, independent-solution and proportional-mark review assertions;
- Q7/Q8 prose extraction, independence, demand features and justified-conclusion evidence;
- expected package/rationale page counts.

Do not use assertions to excuse weak content. They are reviewer decisions that must be rechecked against rendered artefacts.

## 2. Run preflight before authoring

Run:

```bash
python scripts/validate_assessment_spec.py assessment-spec.json
```

The validator rejects, among other failures:

- wrong mark totals, topic subtotals or Page 1 layout;
- for v4, missing/wrong `criterion_component_estimate_v1` evidence data, wrong 5D / 8C / 5B / 7A totals, wrong indicative bands, missing mark-level evidence metadata or A-demand feature;
- for v4, failure of the structural boundary proof that C/B/A force the required target-standard evidence;
- missing, duplicated or disproportionate mark evidence;
- unjustified response labels/boxes/tables/scaffolds;
- required fraction items without purposeful visual models;
- unregistered fraction instances;
- Q7/Q8 that are not independent prose-first word problems;
- Q8 with insufficient substantive demand, no inference/dependency/interacting constraint or no justified conclusion;
- undeclared/unauthorised higher-year content;
- unverified wording, solution or self-answering assertions.

Treat every error code as a release barrier. Do not begin PowerPoint construction until preflight reports `READY`.

## 3. Build all outputs from the specification

Use the validated specification/approved question set as the content source for Student Test, Marking Key and Curriculum Rationale. Do not maintain separate prompt/answer/mark-allocation copies.

- Place Page 1 questions directly into final six cells.
- Create the key by duplicating the completed test, then add only `qN-key-*` elements.
- Use stable names in `powerpoint-output.md` so geometry/fonts/fractions/duplication can be audited.
- Use blank, unlined response space unless a mathematical reason for another structure is recorded.
- Reserve contiguous response space before diagrams/decoration.
- Keep Page 1 question elements within their own question-cell region.
- Treat diagram scale/hierarchy/page balance as positive production requirements.
- Keep curriculum codes, extensions, marks, answers and demand claims identical across outputs.

### v4 output rules

The Student Test must not display internal evidence-band metadata, band rationales or cut-off proof.

The Marking Key should include:

- exact mark criteria;
- teacher-facing evidence-band annotation where useful/readable;
- compact indicative standard table: E 0–4, D 5–9, C 10–15, B 16–20, A 21–25;
- wording that this is an **indicative standard on the assessed component**, not the student's reporting grade.

The Curriculum Rationale must explain:

- **5D / 8C / 5B / 7A**;
- how D/C/B/A apply to the resolved curriculum;
- structural proof: 5 C+, 3 B+, 3 A forced at the C/B/A cut-offs;
- task/component estimate limitation and teacher responsibility for broader reporting judgement.

## 4. Complete two review passes

### Authoring QA

Solve every question independently and review source/rendered output against P01–P29 and R01–R18. Record exact evidence inspected, not merely `looks correct`.

For v4 explicitly review every mark's evidence band against `evidence-band-standard.md`; do not allow question position to substitute for demand evidence.

### Fresh artifact-only review

Begin from final renders, specification and curriculum references without using author intent as evidence. Use an independent reviewer when available/authorised; otherwise use a deliberately separate artifact-only pass. Record `independent_reviewer` or `fresh_artifact_only`.

Specifically attempt to find:

- wording needing teacher paraphrase;
- a stem/stimulus supplying its own marked answer;
- marks unsupported by distinct evidence;
- v4 band inflation or envelope disagreement;
- routine Q7/Q8 demand;
- decorative/missing representations;
- unnecessary labels/answer boxes/tables;
- fraction collisions;
- sub-minimum marking annotations;
- disagreement among test/key/rationale.

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

Include every gate from `P01` to `P29` and `R01` to `R18` exactly once. The package audit rejects missing/duplicate gates, non-specific evidence, any status other than `PASS`, incomplete reviews, invalid reviewer reuse or open items.

## 6. Run the package audit

After final rendering/visual inspection, run:

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

The auditor verifies source preflight again, file integrity, A4 dimensions, slide/page counts, Page 1 positions, test/key identity, stable names, font minimums, mark labels, key coverage, `MARKING KEY` headers, fraction clearance, banned slash fractions, response-space agreement, prohibited unexplained labels, Q7/Q8 table use, page bounds, rationale tokens and release ledger.

For v4 it must also verify mechanically available agreement on 25 total marks, approved evidence envelope/indicative bands and required teacher-facing rationale/key tokens, while rejecting internal grade metadata on the Student Test where detectable.

The audit does not replace mathematical/pedagogical judgement. `READY` requires both recorded review gates and mechanical audit.

The Document Builder must emit `design-manifest.json` conforming to `schemas/design-manifest.schema.json`. Fresh review compares manifest with actual render; a manifest assertion is evidence to inspect, not proof by itself.

## 7. Regression control

Run before committing a skill change:

```bash
python scripts/test_assessment_workflow.py
```

The regression suite must accept controlled positive specifications and reject known failure classes, including:

- swapped Page 1 cells;
- missing fraction visuals;
- self-answering/artificial wording;
- routine Q8 demand;
- undeclared extension content;
- redundant response scaffolds;
- touching fractions;
- sub-10 pt marking annotations;
- v4 wrong total/envelope/cut-offs;
- v4 missing evidence-band rationale or A-demand feature;
- v4 band inflation/architecture inconsistencies;
- accidental migration of legacy/source-preservation tasks.

When a new defect reaches review, add a focused failing fixture before changing the rule/script. Do not turn one topic-specific preference into a universal rule.

## Visual-system evidence

The builder resolves visual profile, token set and asset manifest before layout. `design_manifest.visual_system` records hashes and one entry for every rendered visual: asset/constructor ID, family, scale state, printed dimensions, greyscale review and demand-preservation review. Student-test and marking-key base visuals remain identical; marking overlays are additive.