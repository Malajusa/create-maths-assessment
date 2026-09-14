# Create Maths Assessment Skill

Canonical repository for the **Create Maths Assessment** agent pipeline.

The skill creates Western Australian mathematics assessments through a gated multi-agent workflow rather than a single generation prompt. Classroom release requires actual assessment-level evidence, not merely passing code tests.

## Output contract

A normal assessment run produces:

1. Student Test — PowerPoint, A4 portrait
2. Marking Key — PowerPoint duplicated from the final Student Test and annotated with worked solutions and marks
3. Curriculum Rationale — PDF based on the final assessment

Respect a narrower explicit request, such as a key for an exact uploaded test. No package is release-ready unless the independent release gate reports `READY` with zero open barriers and verified current evidence.

## v4.0 criterion evidence envelope

For a new Years 3–10 grade-estimating assessment, v4 uses a **25-mark criterion-referenced evidence architecture** rather than the historical 20-mark progression.

Canonical evidence envelope:

| Evidence band | Marks |
|---|---:|
| D | 5 |
| C | 8 |
| B | 5 |
| A | 7 |
| **Total** | **25** |

Indicative standard on the **assessed component**:

| Score | Indicative standard |
|---|---|
| 0–4 | E |
| 5–9 | D |
| 10–15 | C |
| 16–20 | B |
| 21–25 | A |

These are not universal WA percentage bands. They are meaningful only because the assessment is deliberately constructed so that:

- 10/25 requires at least **5 C-or-higher marks**;
- 16/25 requires at least **3 B-or-higher marks**;
- 21/25 requires at least **3 A marks**.

Every individual mark carries observable D/C/B/A evidence metadata. C is the expected-standard anchor; D is meaningful limited evidence towards the same construct; B requires stronger transfer/selection/interpretation/connection/explanation; A requires non-obvious, flexible or justified reasoning within the authorised curriculum.

The Student Test does not display internal evidence bands. The Marking Key may show teacher-facing evidence annotations and the indicative score table. The Curriculum Rationale explains the envelope and structural boundary proof.

The v4 score is a strong **task/component estimate**, not the student's official Mathematics reporting grade. Teacher moderation, re-attempt decisions, reflection on assessment efficacy and synthesis with other evidence remain teacher responsibilities.

See `references/evidence-band-standard.md` and `docs/superpowers/specs/2026-09-14-criterion-evidence-envelope-design.md`.

### Default v4 question architecture

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

The per-question distribution is a default, not permission to inflate evidence bands. Individual mark evidence is authoritative. If honest mathematical classification requires a different placement across Q5–Q8, the blueprint may redistribute marks while preserving the whole **5D / 8C / 5B / 7A** envelope. If the curriculum cannot support the envelope without artificial splitting or unauthorised content, the pipeline must return an architecture barrier.

### Compatibility

The new envelope is the default only for new Years 3–10 grade-estimating assessments.

- Exact supplied assessments and key-only requests preserve their source architecture.
- Equivalent Version B/re-attempt requests preserve the source architecture unless migration is explicitly requested.
- Pre-primary–Year 2 retain age-appropriate structures unless separately redesigned.
- Years 11–12/WACE remain governed by course-specific assessment and grade-setting requirements.
- The historical 20-mark architecture remains valid for legacy/source-preservation workflows; it is not silently rewritten as v4.

## Architecture

Seven agents have separate authority:

1. Orchestrator / Curriculum Resolver
2. Assessment Blueprint Agent
3. Question Designer (Q1–Q6)
4. Complex Problem-Solving Specialist (Q7–Q8)
5. Maths + Pedagogy Validator
6. Document Builder
7. Independent Release QA Agent

Generation agents cannot certify their own work. Failed checks route back to the responsible stage and invalidate affected descendants, not valid independent sibling questions.

There is deliberately **no separate grading stage**. The score-to-component-estimate relationship is engineered during assessment construction and validated before release.

## Repository map

- `SKILL.md` — skill entrypoint and mandatory workflow
- `agents/` — role-specific instructions
- `orchestration/pipeline.json` — machine-readable stage graph and repair routing
- `runtime/controller.py` — schema/dependency/evidence-binding state machine
- `runtime/release_evidence.py` — current-file, rendered-review and fresh-audit release guard
- `scripts/evidence_envelope.py` — canonical v4 score/evidence invariants
- `scripts/audit_assessment_package.py` — legacy/source-preservation package auditor
- `scripts/audit_assessment_package_v4.py` — v4 package wrapper adding dynamic mark and criterion-output checks
- `schemas/` — contracts passed between agents
- `standards/` — assessment, maths, exemplar, project-context and QA requirements
- `references/evidence-band-standard.md` — normative v4 evidence-band rules
- `assets/maths-visuals/` — versioned, validated canonical SVG assets and provenance manifest
- `assets/visual-tokens/` — shared visual tokens for assessment diagrams and illustrations
- `tests/` — deterministic repository/contract tests
- `tests/scenarios/` — adversarial pressure scenarios for model-level skill testing
- `docs/superpowers/specs/` — approved architecture specifications
- `docs/superpowers/plans/` — implementation plans

## Validation

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/validate_visual_assets.py
python scripts/validate_repository.py
python scripts/run_regression_fixtures.py
```

All must pass before changes are considered structurally valid. Model-level pressure tests in `tests/scenarios/` and a genuine rendered-assessment acceptance run remain separate requirements; do not claim they ran from deterministic results.

For a v4 package, the release guard selects `scripts/audit_assessment_package_v4.py`. Legacy/source-preservation packages continue to use the mature legacy auditor.

## Versioning

`VERSION` is the canonical skill version. Behaviour-changing updates require a corresponding test/scenario update, deterministic validation, review of affected barriers and a version increment. Implemented, tested, pushed, merged, packaged and installed are separate statuses.

## v3.6 project context and evidence-bound release

The project decisions are consolidated in `standards/project-context.md`, including the exact-source marking-key requirement, independent prose-first B/A problems, approved visual standards, loose 2016 judging-standard calibration and truthful recovery/delivery.

READY requires current files and hashes, specification, QA ledger, unchanged design manifest, real independent-review execution records and full-resolution page coverage. The controller executes the appropriate package auditor and rechecks consumed file hashes. Reopening READY reruns its evidence checks. See `standards/release-evidence.md` for the production interface and limitations.

Repairs use producer/consumer dependencies to preserve unaffected sibling work, keep unrelated barriers open and reject invalid replacements before state changes. The historical 'gold' fixture is explicitly structural-only: its unsupported READY claim must be rejected. Stub-auditor unit tests are not real assessment acceptance tests.

Old v3.x run state is not silently migrated. Start a new run/revalidation boundary; never change its version field to pretend it was revalidated. Repository code changes alone do not prove any user's local installation changed.

## v3.2 approved question set contract

Agent 05 emits an immutable `approved_question_set` only when content validation passes. Agent 06 must build from that exact Q1–Q8 artefact, and Agent 07 verifies the final package against the original brief, blueprint and approved set. The runtime rejects altered approved questions, PASS without an approved set, and FAIL with one.

## v3.4 combined skill distribution

Version 3.4 packaged the enforced agent pipeline together with the production resources required to generate assessments:

- Western Australian curriculum references from Pre-primary to Year 10;
- assessment format, quality-gate and production contracts;
- Q7/Q8 problem-solving and demand standards;
- PowerPoint and mathematical-diagram conventions;
- benchmark assessments and machine-readable regression cases;
- deterministic assessment-specification and package-audit scripts.

`SKILL.md` and each stage-agent file route to the relevant resources. The `approved_question_set` gate and runtime protections remain mandatory.

## v3.5 assessment visual system

Version 3.5 added an assessment-native visual standard derived from supplied quality references without copying protected artwork:

- a dual-mode standard for exact mathematical figures and restrained contextual illustrations;
- shared colour, line, spacing, accessibility and scale tokens;
- validated, versioned SVG assets for the square, circle and equilateral triangle;
- per-question `visual_spec` decisions covering purpose, information, removal effect, source, scale, accessibility and strategy-reveal risk;
- Q7/Q8 safeguards that reject solution-ready illustrations;
- design-manifest evidence for resource hashes, printed dimensions, greyscale safety and demand preservation; and
- release-audit checks plus original proof sheets for visual calibration.

Run `python scripts/validate_visual_assets.py` whenever an asset or its manifest changes. The validator rejects altered geometry, unapproved provenance, forbidden raster/text effects and stale hashes.

## v3.1 executable enforcement

The repository includes an executable state-machine controller rather than relying only on agent compliance with Markdown.

```bash
python -m runtime.controller --run-dir run/example record 01-orchestrator-curriculum-resolver brief.json
python -m runtime.controller --run-dir run/example status
```

Each recorded stage is schema-validated and persisted to the run directory. The controller blocks stage skipping, failed content gates, invalid release claims, Q8 dependency on Q7 and marking keys whose recorded source hash differs from the final Student Test.

`fixtures/` contains structural examples and known failure cases. GitHub Actions runs the unit tests, structural validator, visual-asset validator and fixture suite on every push and pull request.