# v4.0.1 readiness remediation

This release addresses repository-side findings from the v4.0.0 Skill Craft readiness review.

Implemented here:

- broader ChatGPT/Codex invocation metadata for create, revise, review, marking, exact-source and equivalent-version workflows;
- a tag-driven GitHub Release workflow;
- a package manifest binding release version, source commit and packaged-file hashes;
- an installed-package verifier;
- tests for package provenance and release workflow contracts; and
- a target-environment acceptance matrix plus evidence-presence preflight.

Not claimed here:

- that a genuine v4 target-environment assessment acceptance run has passed;
- that an independently executed reviewer has approved such a run; or
- that any user's currently installed skill already matches this branch or a future v4.0.1 release package.

Those are evidence and deployment steps, not source-code changes. They remain open until real execution records exist.
