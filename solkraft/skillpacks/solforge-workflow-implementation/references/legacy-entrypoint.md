---
name: solforge-workflow-implementation
description: "Apply the selected Single, Multi, or Ultra runner to a bounded implementation task with explicit writes, tests, rollback, and verification. Use the Build or Change workflow alone or combine it with any other compatible capability."
---

# SolForge Workflow: Implementation

Apply the selected Single, Multi, or Ultra runner to a bounded implementation task with explicit writes, tests, rollback, and verification.

## Native workflow

- Domain: `general`
- Action family: `implement`
- Environment: `available_execution_environment`
- Typical outputs: `implementation_plan`, `reviewable_patch`, `verified_change`, `operational_artifact`.
- Suggested starting skill: `$solforge-build`

1. Translate the objective and supplied inputs into concrete work for this workflow.
2. Load the suggested starting skill and any other useful native skills. The suggestion is not exclusive.
3. Inspect dependencies and group independent work into safe parallel waves when useful.
4. Execute with real tools and preserve unrelated user work.
5. Verify every material output and state any unsupported or incomplete claim plainly.
6. Return the result directly; do not substitute a routing artifact for the requested outcome.

## Composition behavior

- This workflow may run alone, alongside other workflows, or as part of an include-all route.
- Add, remove, reorder, repeat, or parallelize compatible capabilities as the objective requires.
- Apply direct user Pause, Resume, and Stop instructions immediately.
