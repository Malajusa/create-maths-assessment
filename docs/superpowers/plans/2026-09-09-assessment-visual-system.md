# Assessment Visual System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a versioned, executable visual standard with approved assets, semantic visual specifications and fail-closed validation to the Create Maths Assessment skill.

**Architecture:** Extend the existing v3.4 visual-profile system with a separate token set, asset manifest and reusable `visual_spec` contract. Question design declares visual purpose and demand effects; the document builder resolves registered assets or constructors; repository, specification and package validators enforce asset integrity, problem-solving semantics and rendered evidence.

**Tech Stack:** Markdown skill contracts, JSON Schema 2020-12, JSON manifests, SVG assets, Python 3.12 validation, `unittest`, `jsonschema`, existing PowerPoint XML auditor.

**Spec:** `docs/superpowers/specs/2026-09-09-assessment-visual-system-design.md`

## Global Constraints

- Preserve A4 portrait output, Q1-Q6 page-one order, Q7/Q8 page positions and the 20-mark structure.
- Q7 and Q8 remain independent, prose-first problems.
- Main problem cards calibrate Q7 demand; extension cards calibrate Q8 demand; source artwork is not redistributed.
- The Junior Illustrated Maths Dictionary and NAPLAN papers supply principles only; no protected artwork enters the repository.
- SVG is authoritative for canonical assets.
- Colour must not be the only answer-critical cue.
- Every required visual defect is a release barrier.
- Implement the representative proof set incrementally; do not attempt the full Pre-primary-to-Year-7 catalogue in this change.

---

### Task 1: Canonical visual contracts and versioned tokens

**Files:**
- Create: `standards/visual-standard.md`
- Create: `references/contextual-illustration-standard.md`
- Create: `assets/visual-tokens/assessment-visual-tokens-v1.json`
- Modify: `references/mathematical-diagram-conventions.md`
- Modify: `references/powerpoint-output.md`
- Modify: `assets/visual-profiles/classic-assessment-v1.json`
- Modify: `schemas/visual-profile.schema.json`
- Test: `tests/test_visual_system_contract.py`

**Interfaces:**
- Consumes: existing `classic-assessment-v1` profile and A4 production contract.
- Produces: `token_set` path/hash reference and canonical purpose, colour, line, scale, accessibility and contextual-illustration rules.

- [ ] **Step 1: Write failing contract tests**

```python
def test_default_profile_resolves_visual_tokens(self):
    profile = load_json("assets/visual-profiles/classic-assessment-v1.json")
    self.assertEqual(
        "assets/visual-tokens/assessment-visual-tokens-v1.json",
        profile["token_set"],
    )
    tokens = load_json(profile["token_set"])
    self.assertEqual("#1F2937", tokens["colours"]["primary_outline"])
    self.assertTrue(tokens["accessibility"]["greyscale_required"])
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `python -m unittest tests.test_visual_system_contract -v`  
Expected: FAIL because the token set and canonical standards do not exist.

- [ ] **Step 3: Add standards, tokens and profile/schema references**

Implement a versioned token document with `colours`, `strokes`, `markers`, `svg`, `print_minimums_mm`, `accessibility` and `marking_overlay`. Add `token_set` and `asset_manifest` URI fields to the visual-profile schema and default profile.

- [ ] **Step 4: Run the focused test**

Run: `python -m unittest tests.test_visual_system_contract -v`  
Expected: PASS for token and standards assertions.

- [ ] **Step 5: Commit**

```bash
git add standards references assets/visual-tokens assets/visual-profiles schemas/visual-profile.schema.json tests/test_visual_system_contract.py
git commit -m "feat: define canonical assessment visual standard"
```

### Task 2: Approved asset manifest and exact starter assets

**Files:**
- Create: `schemas/visual-asset-manifest.schema.json`
- Create: `assets/maths-visuals/v1/manifest.json`
- Create: `assets/maths-visuals/v1/canonical-figures/square.svg`
- Create: `assets/maths-visuals/v1/canonical-figures/circle.svg`
- Create: `assets/maths-visuals/v1/canonical-figures/equilateral-triangle.svg`
- Create: `scripts/validate_visual_assets.py`
- Modify: `tests/test_visual_system_contract.py`

**Interfaces:**
- Consumes: visual tokens from Task 1.
- Produces: `validate_manifest(root: Path, manifest_path: Path) -> list[dict[str, str]]` and stable asset IDs `shape.square.v1`, `shape.circle.v1`, `shape.equilateral-triangle.v1`.

- [ ] **Step 1: Write failing asset and geometry tests**

```python
def test_starter_asset_manifest_and_geometry(self):
    issues = validate_manifest(ROOT, ROOT / "assets/maths-visuals/v1/manifest.json")
    self.assertEqual([], issues)
    manifest = load_json("assets/maths-visuals/v1/manifest.json")
    self.assertEqual(3, len(manifest["assets"]))
    self.assertEqual(
        {"shape.square.v1", "shape.circle.v1", "shape.equilateral-triangle.v1"},
        {asset["asset_id"] for asset in manifest["assets"]},
    )
```

- [ ] **Step 2: Run the test and verify failure**

Run: `python -m unittest tests.test_visual_system_contract.VisualSystemContractTests.test_starter_asset_manifest_and_geometry -v`  
Expected: FAIL because the manifest and validator do not exist.

- [ ] **Step 3: Add the schema, assets, manifest and validator**

`validate_manifest` must validate JSON Schema, resolve every SVG, check SHA-256, require original-source provenance and a distributable licence declaration, reject embedded raster images, gradients, filters, shadows and text in canonical figures, verify a `0 0 1000 1000` view box and test declared square/circle/equilateral geometry within `1e-6` relative tolerance.

- [ ] **Step 4: Run asset tests**

Run: `python -m unittest tests.test_visual_system_contract -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add schemas/visual-asset-manifest.schema.json assets/maths-visuals scripts/validate_visual_assets.py tests/test_visual_system_contract.py
git commit -m "feat: add validated canonical maths assets"
```

### Task 3: Semantic visual specification and demand-preservation validation

**Files:**
- Create: `schemas/visual-spec.schema.json`
- Modify: `schemas/question.schema.json`
- Modify: `scripts/validate_assessment_spec.py`
- Modify: `references/q7-q8-problem-solving-standard.md`
- Modify: `tests/test_visual_system_contract.py`
- Modify: `examples/benchmarks/year5-fractions-percentages-release-spec.json`
- Modify: `fixtures/gold/minimal-run/03-q1-q6.json`
- Modify: `fixtures/gold/minimal-run/04-q7-q8.json`
- Modify: `fixtures/gold/minimal-run/05-validation.json`

**Interfaces:**
- Consumes: asset IDs, visual families and visual purpose rules.
- Produces: `_validate_visual_spec(errors, visual_spec, representation, qid, path)` and error codes `E_VISUAL_PURPOSE`, `E_VISUAL_SCALE`, `E_VISUAL_STRATEGY`, `E_VISUAL_SOURCE`, `E_VISUAL_ACCESSIBILITY`, `E_VISUAL_DEMAND`.

- [ ] **Step 1: Write failing semantic tests**

```python
def test_q8_rejects_solution_ready_visual(self):
    spec = valid_spec()
    q8 = spec["questions"][7]
    q8["visual_spec"] = valid_visual_spec()
    q8["visual_spec"]["strategy_reveal_risk"] = "preorganises_solution"
    codes = {issue["code"] for issue in validate_spec(spec)}
    self.assertIn("E_VISUAL_STRATEGY", codes)

def test_visual_can_be_omitted_with_specific_reason(self):
    spec = valid_spec()
    spec["questions"][7]["visual_spec"] = None
    self.assertNotIn("E_VISUAL_PURPOSE", {e["code"] for e in validate_spec(spec)})
```

- [ ] **Step 2: Run focused tests and verify failure**

Run: `python -m unittest tests.test_visual_system_contract -v`  
Expected: FAIL because semantic visual validation is absent.

- [ ] **Step 3: Implement the strict visual-spec schema and validator**

Valid families are `canonical_figure`, `mathematical_diagram`, `data_display`, `contextual_illustration`, `response_surface`, `marking_overlay`. Valid scale states are `exact`, `to_scale`, `not_to_scale`, `schematic`. Source kinds are `approved_asset`, `registered_constructor`, `original_contextual`, `none`. Reject empty purpose/removal fields, decorative-only purpose, solution-ready Q7/Q8 organisation, missing accessibility cues and undeclared assets.

- [ ] **Step 4: Update positive fixtures with explicit visual decisions**

Every question with a required representation gains a non-null `visual_spec`. Questions without visuals retain a specific representation omission reason. Q7/Q8 fixtures record demand-preservation decisions.

- [ ] **Step 5: Run specification and regression tests**

Run: `python -m unittest tests.test_visual_system_contract tests.test_regression_runner tests.test_contracts -v`  
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add schemas scripts/validate_assessment_spec.py references/q7-q8-problem-solving-standard.md tests examples fixtures
git commit -m "feat: validate visual purpose and problem-solving demand"
```

### Task 4: Agent routing and build-manifest evidence

**Files:**
- Modify: `SKILL.md`
- Modify: `agents/02-assessment-blueprint.md`
- Modify: `agents/03-question-designer.md`
- Modify: `agents/04-complex-problem-specialist.md`
- Modify: `agents/05-maths-pedagogy-validator.md`
- Modify: `agents/06-document-builder.md`
- Modify: `agents/07-release-qa.md`
- Modify: `schemas/design-manifest.schema.json`
- Modify: `standards/qa-barriers.md`
- Modify: `references/assessment-quality-gates.md`
- Modify: `references/assessment-production-contract.md`
- Modify: `tests/test_skill_package_completeness.py`
- Modify: `tests/test_visual_system_contract.py`

**Interfaces:**
- Consumes: semantic `visual_spec`, visual profile, tokens and asset manifest.
- Produces: build evidence containing `visual_profile_sha256`, `token_set_sha256`, `asset_manifest_sha256`, per-question asset/constructor IDs, scale states, printed dimensions, greyscale evidence and demand-preservation evidence.

- [ ] **Step 1: Write failing routing and manifest-schema tests**

```python
def test_visual_standard_is_routed_to_every_visual_owner(self):
    for path in VISUAL_OWNER_FILES:
        self.assertIn("standards/visual-standard.md", (ROOT / path).read_text())

def test_design_manifest_requires_visual_evidence(self):
    schema = load_json("schemas/design-manifest.schema.json")
    self.assertIn("visual_system", schema["required"])
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run: `python -m unittest tests.test_visual_system_contract tests.test_skill_package_completeness -v`  
Expected: FAIL because agent routes and evidence fields are absent.

- [ ] **Step 3: Update agents, standards and schemas**

Add explicit ownership: blueprint decides need; designer declares information role; complex-problem specialist checks demand preservation; pedagogy validator verifies representation choice; builder resolves registered assets and records evidence; release QA checks purpose, greyscale, legibility, provenance and test/key identity.

- [ ] **Step 4: Run contract tests**

Run: `python -m unittest tests.test_visual_system_contract tests.test_skill_package_completeness -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add SKILL.md agents schemas/design-manifest.schema.json standards references tests
git commit -m "feat: route visual governance through assessment pipeline"
```

### Task 5: Proof artefacts and package audit integration

**Files:**
- Create: `assets/visual-benchmarks/README.md`
- Create: `assets/visual-benchmarks/canonical-figures-proof.svg`
- Create: `assets/visual-benchmarks/problem-page-proof.svg`
- Create: `examples/benchmarks/visual-semantic-cases.json`
- Modify: `scripts/audit_assessment_package.py`
- Modify: `tests/test_visual_system_contract.py`
- Modify: `examples/benchmarks/regression-cases.json`

**Interfaces:**
- Consumes: design-manifest visual evidence and registered assets.
- Produces: `_audit_visual_system(spec, design_manifest, test, key, issues)` and rendered proof references for exact and contextual modes.

- [ ] **Step 1: Write failing audit tests**

```python
def test_package_audit_requires_greyscale_and_asset_evidence(self):
    source = (ROOT / "scripts/audit_assessment_package.py").read_text()
    self.assertIn("E_VISUAL_GREYSCALE", source)
    self.assertIn("E_VISUAL_ASSET_HASH", source)
    self.assertIn("E_VISUAL_DEMAND", source)
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `python -m unittest tests.test_visual_system_contract -v`  
Expected: FAIL because the package audit does not enforce visual-system evidence.

- [ ] **Step 3: Add proof artefacts and audit checks**

The figure proof shows the three approved assets at normal/minimum size plus annotation examples. The problem-page proof shows an exact patio diagram integrated with concise prose and a greyscale-safe marking overlay; it is an original proof, not copied source artwork. Audit the design manifest hashes, asset IDs, scale status, printed dimensions, greyscale evidence and Q7/Q8 demand evidence.

- [ ] **Step 4: Run package and visual tests**

Run: `python -m unittest tests.test_visual_system_contract tests.test_runtime_controller tests.test_contracts -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add assets/visual-benchmarks examples/benchmarks scripts/audit_assessment_package.py tests/test_visual_system_contract.py
git commit -m "feat: add visual proof artefacts and release checks"
```

### Task 6: Repository validation, versioning and final documentation

**Files:**
- Modify: `scripts/validate_repository.py`
- Modify: `tests/test_skill_package_completeness.py`
- Modify: `README.md`
- Modify: `VERSION`
- Modify: `orchestration/pipeline.json`
- Modify: `.github/workflows/validate-skill.yml`

**Interfaces:**
- Consumes: all files and validators from Tasks 1-5.
- Produces: v3.5.0 repository contract and CI execution of visual asset validation.

- [ ] **Step 1: Write failing completeness/version tests**

```python
def test_visual_system_resources_are_packaged(self):
    for path in REQUIRED_VISUAL_RESOURCES:
        self.assertTrue((ROOT / path).is_file(), path)

def test_version_is_visual_system_release(self):
    self.assertEqual("3.5.0", (ROOT / "VERSION").read_text().strip())
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest tests.test_skill_package_completeness -v`  
Expected: FAIL until v3.5.0 and required resources are registered.

- [ ] **Step 3: Update repository validation, CI, README and version**

`scripts/validate_repository.py` imports and runs `validate_manifest`, verifies all canonical visual resources and requires version `3.5.0`. CI runs repository validation, unit tests, regression fixtures and visual asset validation.

- [ ] **Step 4: Run the complete validation suite**

Run:

```bash
python scripts/validate_visual_assets.py
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python scripts/run_regression_fixtures.py
```

Expected: every command exits `0`; repository and visual validators report success; all unit and regression tests pass.

- [ ] **Step 5: Inspect repository state and commit**

```bash
git diff --check
git status --short
git add .github README.md VERSION orchestration scripts tests
git commit -m "release: complete v3.5 visual system contract"
```

### Task 7: Final verification

**Files:**
- Verify only; no planned modifications.

**Interfaces:**
- Consumes: committed v3.5.0 repository.
- Produces: evidence that the branch is clean and all contracts pass.

- [ ] **Step 1: Run final verification from a clean index**

```bash
git status --short
python scripts/validate_visual_assets.py
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python scripts/run_regression_fixtures.py
```

Expected: clean status before and after verification; all commands exit `0`.

- [ ] **Step 2: Report branch and commits**

Run: `git --no-pager log --oneline -8`  
Expected: the specification, task commits and v3.5 completion commit appear on `improve/visual-production-v3.4`.
