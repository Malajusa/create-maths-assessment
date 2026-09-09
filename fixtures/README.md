# Regression Fixtures

Fixtures turn known assessment-quality failures into executable regression cases.

## Structural fixture (historically called gold)

`gold/minimal-run/` contains structurally valid stage payloads, but no real produced documents or independent review evidence. Stages 01–06 can be recorded; its legacy stage-07 READY claim **must now be rejected**. The runner checks that rejection. This fixture is not a classroom-quality benchmark or evidence of end-to-end release.

## Failures

Each failure fixture represents behaviour the skill must reject:

- `q8-dependency` — Q8 depends on Q7;
- `ready-with-barrier` — release claims READY while a barrier remains;
- `key-provenance` — marking key source hash does not match the final Student Test.

`tests/test_project_context_runtime.py` additionally covers unsupported READY, resumption, dependency-aware repair, unresolved sibling barriers and invalid-replacement state preservation. `tests/test_release_evidence.py` checks evidence integrity and audit wiring with an explicitly labelled stub auditor; it does not claim independent model or real assessment acceptance.

Add a regression test whenever a real review exposes a recurring failure. Keep deterministic test results, model-level pressure tests and genuine rendered-assessment review results separate.
