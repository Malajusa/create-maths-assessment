# Create Maths Assessment Skill

Canonical repository for the **Create Maths Assessment** agent pipeline.

The skill creates classroom-ready Western Australian mathematics assessments through a gated multi-agent workflow rather than a single generation prompt.

## Output contract

A normal assessment run produces:

1. Student Test — PowerPoint, A4 portrait
2. Marking Key — PowerPoint duplicated from the final Student Test and annotated with worked solutions and marks
3. Curriculum Rationale — PDF based on the final assessment

No package is release-ready unless the independent release gate reports `READY` with zero open barriers.

## Architecture

Seven agents have separate authority:

1. Orchestrator / Curriculum Resolver
2. Assessment Blueprint Agent
3. Question Designer (Q1–Q6)
4. Complex Problem-Solving Specialist (Q7–Q8)
5. Maths + Pedagogy Validator
6. Document Builder
7. Independent Release QA Agent

Generation agents cannot certify their own work. Failed checks route back to the responsible stage and invalidate downstream validation.

## Repository map

- `SKILL.md` — skill entrypoint and mandatory workflow
- `agents/` — role-specific instructions
- `orchestration/pipeline.json` — machine-readable stage graph and repair routing
- `schemas/` — contracts passed between agents
- `standards/` — assessment, maths, exemplar and QA requirements
- `tests/` — deterministic repository/contract tests
- `tests/scenarios/` — adversarial pressure scenarios for model-level skill testing
- `docs/superpowers/specs/` — approved architecture specification
- `docs/superpowers/plans/` — implementation plan

## Validation

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

Both must pass before changes are considered structurally valid.

Model-level pressure tests in `tests/scenarios/` should also be run whenever the skill behaviour changes.

## Versioning

`VERSION` is the canonical skill version. Behaviour-changing updates require:

- a corresponding test/scenario update;
- deterministic validation;
- review of affected barriers;
- version increment.

## v3.1 executable enforcement

The repository includes an executable state-machine controller rather than relying only on agent compliance with Markdown.

```bash
python -m pip install -r requirements.txt
python -m runtime.controller --run-dir run/example record 01-orchestrator-curriculum-resolver brief.json
python -m runtime.controller --run-dir run/example status
```

Each recorded stage is schema-validated and persisted to the run directory. The controller blocks stage skipping, failed content gates, invalid release claims, Q8 dependency on Q7 and marking keys whose recorded source hash differs from the final Student Test.

`fixtures/` contains one complete gold run and known failure cases. GitHub Actions runs the unit tests, structural validator and fixture suite on every push and pull request.
