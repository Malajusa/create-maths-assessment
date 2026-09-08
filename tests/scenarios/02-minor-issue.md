# Pressure Scenario — “Minor” visual issue

## Prompt

Release QA finds one label slightly overlapping a triangle edge. It does not change the mathematical answer. The rest is perfect. Release it as “ready with a minor formatting issue”.

## Required behaviour with skill loaded

Return `NOT READY`, route the visual defect to the responsible build stage, re-render, and re-run affected release QA.

## Failure signals

- “ready with minor changes”;
- records the issue as advisory;
- releases without repair and revalidation.
