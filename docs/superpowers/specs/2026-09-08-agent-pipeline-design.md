# Create Maths Assessment Agent Pipeline Design

**Date:** 2026-09-08  
**Status:** Approved for implementation

## Goal

Replace monolithic assessment generation with a deterministic, gated seven-agent workflow that maintains assessment quality across models and runs.

## Output contract

A standard complete run produces:
1. Student Test PPTX, A4 portrait;
2. Marking Key PPTX duplicated from the final Student Test and annotated with worked solutions and marks;
3. Curriculum Rationale PDF based on the final assessment.

## Architecture

The seven roles are:
1. Orchestrator / Curriculum Resolver
2. Assessment Blueprint Agent
3. Question Designer (Q1–Q6)
4. Complex Problem-Solving Specialist (Q7–Q8)
5. Maths + Pedagogy Validator
6. Document Builder
7. Independent Release QA Agent

The content and release gates are independent of generation. Generating agents cannot certify their own work.

## Default assessment shape

The default 20-mark structure is `1, 1, 2, 2, 3, 3, 4, 4` across Q1–Q8.

Q7 and Q8 are independent complex problems. Q7 typically targets B-level transfer/reasoning and Q8 typically targets A-level transfer/reasoning.

## Quality model

All required defects are barriers. There is no advisory-only defect class.

Content validation covers mathematics, ambiguity, construct purity, accessibility, calibration, conventions and mark validity.

Release validation covers semantics, independent re-solving, cross-file integrity, rendered visual QA, marking usability and rationale integrity.

## Repair

A failure routes back to its owning stage. Only the affected component should be regenerated where possible. Any repair invalidates downstream validation that depends on it.

The same barrier may receive at most three targeted repairs. A fourth attempt must use a materially different problem or design approach.

## Exemplars

Exemplars govern only explicitly assigned dimensions. Current user instructions and canonical standards override older exemplar details where they conflict.

## Model independence

Critical requirements are represented in structured contracts, explicit ownership, binary gates and machine-readable routing rather than relying on a model remembering long prose instructions.
