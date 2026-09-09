# Evidence-bound release protocol (v3.6)

`record 07-release-qa` is the release-authorisation operation. Schema validation, a fixture PASS, an auditor's standalone output or a prose READY claim is not a substitute. No synthetic 'gold' fixture proves a classroom-ready assessment.

## Run boundary

Store the three deliverables, evidence and full-resolution page renders inside the run directory. File records use `path` (relative to the run directory, or an absolute path within it) and the actual lowercase SHA-256 of the current bytes. External paths, missing files, empty files and stale hashes are rejected.

Record stages 01–06 first. The controller binds review to the exact recorded stage-05 content-validation artefact (which contains the approved question set) and stage-06 build manifest. Persist the build's `design_manifest` unchanged as a separate JSON file.

## Release payload

The existing `status`, `open_barrier_count` and `barriers` fields remain. A READY payload additionally needs an `evidence` object containing exactly these file records:

| Field | Current file |
|---|---|
| `assessment_spec` | Assessment specification consumed by the production auditor |
| `qa_ledger` | Completed P01–P29 and R01–R18 ledger, bound to the specification |
| `design_manifest` | The same design-manifest object recorded by the builder |
| `render_review` | Independent, page-by-page review record described below |

A NOT READY payload does not need fabricated evidence. Record the missing check as a barrier with an executable stage owner and an actionable fix.

## Render-review object

Required fields:

- `status`: `PASS`; `review_mode`: `independent_reviewer`.
- `generator_execution_id` and `reviewer_execution_id`: real, non-empty, distinct execution identifiers. Do not invent a second identity for one execution.
- `review_record`: a file record for the actual reviewer execution record/tool output. This must document the reviewer context and inspection, not be a retrospective invented transcript.
- `assessment_spec_sha256`, `content_validation_sha256` and `build_manifest_sha256`: hashes of the exact current files.
- `pages`: one record for every page of the Student Test, Marking Key and Curriculum Rationale, with no duplicates or missing pages.

Each page record contains `artifact` (`student_test`, `marking_key` or `curriculum_rationale`), one-based integer `page`, `source_sha256`, an `image` PNG file record, `inspection: full_resolution_and_print_scale`, `findings: []`, and specific `evidence_inspected` text of at least 20 characters. Resolve any finding before recording PASS; do not delete a finding without repairing and reviewing its source.

Use a separate full-page PNG for each page, at least 1240 × 1754 pixels (A4 portrait at approximately 150 dpi). This is the executable minimum, not a claim that this resolution alone ensures quality. A contact sheet can help navigation but cannot replace individual page inspection. Review readable labels, question-cell boundaries, response space, marking overlays, mathematical interpretation, positive visual quality and greyscale safety.

Different role names are not proof of independent execution. The runtime checks the presence, consistency and hashes of records; it cannot prove a reviewer was honest, actually independent, or pedagogically correct. Never manufacture records to satisfy this gate. A fresh same-agent review can help authoring but is not the independent release review.

## Actual audit execution

The controller invokes the repository's auditor with `sys.executable`, fixed arguments and no shell. It creates a fresh report, requires exit code 0, `status: READY` and an empty `issues` array, then rechecks every consumed file hash. It saves `artifacts/package-audit.json` only after these checks succeed. A cached report or a printed READY string cannot authorise release.

The supported manual preflight is:

```bash
python scripts/validate_assessment_spec.py run/current/assessment-spec.json
python scripts/audit_assessment_package.py \
  --spec run/current/assessment-spec.json \
  --test run/current/Student_Test.pptx \
  --key run/current/Marking_Key.pptx \
  --rationale run/current/Curriculum_Rationale.pdf \
  --ledger run/current/qa-ledger.json \
  --design-manifest run/current/design-manifest.json \
  --report run/current/preflight-audit.json
python -m runtime.controller --run-dir run/current record 07-release-qa run/current/release.json
python -m runtime.controller --run-dir run/current status
```

Use actual filenames; these paths illustrate the interface. Install `requirements.txt` before auditing. Missing dependencies, rendering capability or independent-review capability are barriers, not permission to skip a check.

The existing production auditor supports the canonical assessment format. An explicit alternative structure needs an appropriate validated production route; do not silently change the request to fit the default or bypass validation.

## Resume and delivery

Reopening a stored READY run revalidates its evidence and reruns the audit. Missing or changed evidence blocks reuse of that claim. A pipeline-version mismatch requires an explicit new run/revalidation boundary; never edit the version in old state to pretend migration occurred.

After any relevant content, document, rendering or evidence change, rebuild/review the affected artefacts and re-record the affected stages. Do not reuse old hashes or reviews. Check current controller status immediately before providing exact file links.

## Verification scope

Deterministic tests cover state transitions, hashes, paths, report wiring, render coverage and dependency-aware repair. Tests using a stub auditor are labelled as such. They do not demonstrate real curriculum alignment, independent model behaviour or classroom-quality visuals. A genuine end-to-end assessment run and independent review are still needed to establish those outcomes.
