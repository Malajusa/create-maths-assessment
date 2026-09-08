# Create Maths Assessment Skill Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone repository implementing the approved seven-agent Create Maths Assessment pipeline.

**Architecture:** The repository uses a concise `SKILL.md` entrypoint that delegates responsibilities to seven agent instruction files. Shared JSON contracts, canonical standards, deterministic repository validation and adversarial model-pressure scenarios prevent quality requirements from being hidden inside one monolithic prompt.

**Tech Stack:** Markdown, JSON Schema, Python standard library `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-08-agent-pipeline-design.md`

## Global Constraints

- Standard complete output: Student Test PPTX, Marking Key PPTX, Curriculum Rationale PDF.
- Default assessment: eight questions, 20 marks, allocation `1,1,2,2,3,3,4,4`.
- Q7 and Q8 are independent complex problems.
- Generating agents cannot certify their own work.
- Every required QA defect is a release barrier.
- Marking Key uses the final Student Test as source of truth.
- Maximum targeted repairs per barrier: 3.

---

### Task 1: Repository contracts

**Files:** `SKILL.md`, `AGENTS.md`, `standards/*`, `orchestration/pipeline.json`

- [x] Define the skill trigger and mandatory gated workflow.
- [x] Encode authority separation and binary release semantics.
- [x] Encode canonical assessment, maths, exemplar and QA rules.
- [x] Encode repair routing, invalidation and retry limits.

### Task 2: Agent boundaries

**Files:** `agents/01-*.md` through `agents/07-*.md`

- [x] Define one clear responsibility for each agent.
- [x] Separate Q1–Q6 generation from Q7–Q8 complex problem generation.
- [x] Restrict content certification to Agent 05.
- [x] Restrict final release certification to Agent 07.

### Task 3: Structured handoffs

**Files:** `schemas/*.schema.json`

- [x] Define assessment brief contract.
- [x] Define blueprint contract.
- [x] Define question contract.
- [x] Define validation and release-status contracts.

### Task 4: Behavioural safeguards

**Files:** `tests/scenarios/*.md`, `tests/test_contracts.py`

- [x] Add pressure scenarios for self-certification, minor defects, Q7/Q8 dependency and key reconstruction.
- [x] Add deterministic tests for seven-agent separation, binary release, Q7/Q8 independence, key source-of-truth and retry limit.

### Task 5: Repository verification

**Files:** `scripts/validate_repository.py`, `README.md`, `VERSION`

- [x] Add standalone structural validator.
- [x] Document repository use and validation.
- [x] Set initial pipeline version to `3.0.0`.
- [x] Run deterministic tests and structural validation.
