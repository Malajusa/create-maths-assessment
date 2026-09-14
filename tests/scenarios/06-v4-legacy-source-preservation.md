# Scenario 06 — Legacy source preservation under v4

## Prompt pressure

The user uploads an exact 20-mark assessment created before v4 and asks only for its marking key, or asks for an equivalent Version B using the same structure with changed values.

The current default skill architecture is 25 marks with 5D / 8C / 5B / 7A.

## Required behaviour

The skill must preserve the supplied assessment's source architecture unless the user explicitly requests migration to v4.

For a key-only request it must duplicate the exact uploaded test and add answers/marks only.

For Version B it must preserve the source assessment's mark total, question architecture, constructs, demand, representation type and marking scheme while independently solving the changed values.

## Failure behaviour

Fail if the skill:

- converts the source to 25 marks without explicit authorisation;
- inserts v4 score bands into a legacy key as though they were part of the original assessment;
- rewrites Q1–Q8 merely to make the paper fit 5D / 8C / 5B / 7A;
- replaces the uploaded source with a remembered or similarly named assessment.
