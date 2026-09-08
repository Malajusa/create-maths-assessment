# Regression Fixtures

Fixtures turn known assessment-quality failures into executable regression cases.

## Gold

`gold/minimal-run/` is a complete structurally valid seven-stage run that must reach `READY`.

## Failures

Each failure fixture represents behaviour the skill must reject:

- `q8-dependency` — Q8 depends on Q7;
- `ready-with-barrier` — release claims READY while a barrier remains;
- `key-provenance` — marking key source hash does not match the final Student Test.

Add a fixture whenever a real assessment review exposes a new recurring failure mode. A fixed issue is not considered institutionalised until a regression fixture protects it.
