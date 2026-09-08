# Agent Execution Rules

These instructions apply to every agent operating in this repository.

## Authority

1. Explicit user instructions are highest priority.
2. `SKILL.md` defines pipeline order.
3. `standards/` contains canonical quality requirements.
4. `orchestration/pipeline.json` defines ownership, retries and invalidation.
5. Exemplars guide only the dimensions assigned to them and cannot override newer canonical rules.

## Separation of authority

Generating agents may propose and repair content but cannot mark their own work as valid.

Only:
- `05-maths-pedagogy-validator` may pass the content gate;
- `07-release-qa` may issue the final `READY` status.

## No silent changes

If an approved question changes after content validation:
- re-run mathematical validation;
- synchronise the marking key;
- update the rationale if affected;
- re-render the changed page;
- re-run release QA.

## Repair discipline

Repair the smallest owning component. Do not regenerate the whole assessment when a targeted repair is sufficient.

After three failed repairs of the same barrier, discard the approach and replace it with a materially different one.

## Evidence

Agents must report concrete defects, not vague quality impressions. Every failure record needs:
- question or artefact;
- category;
- description;
- owner;
- required fix.
