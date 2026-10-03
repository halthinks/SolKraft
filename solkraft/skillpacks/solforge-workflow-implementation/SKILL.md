---
name: solforge-workflow-implementation
description: Apply the selected Single, Multi, or Ultra runner to a bounded implementation task with explicit writes, tests, rollback, and verification.
---

# Implement a bounded change

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the objective, the supplied plan or evidence, the change boundaries, and the acceptance criteria before writing. Confirm the runner fits the scope: Single for a change one agent can hold end to end, Multi when the work splits into separately owned pieces with explicit handoffs, Ultra for sustained multi-stage work that needs user checkpoints. Reuse completed stages and valid inputs rather than restarting; resolve missing inputs with targeted reads of the actual code, not assumptions.

Read the code, configuration, and existing test commands you intend to touch before writing, and match the repository's conventions and toolchain instead of importing new defaults. Work in the smallest coherent increments, each leaving the tree buildable, and keep a rollback path for every write — a clean baseline, scoped commits, or an explicit revert procedure. Do not fold unrelated edits, refactors, or formatting sweeps into the requested change; surface discovered side-work separately.

Verify against the intended checkout and configuration using the repository's own build and test commands, and inspect the real output or artifact when tests alone do not establish the requested behavior. A written plan, a plausible diff, or a dry run is not evidence of a working change, and a green run against the wrong checkout or a stale artifact proves nothing. Record the actual commands, results, and environment; rerun any checks invalidated by later edits.

Report what changed, the verification evidence, the rollback path, and any remaining limits or follow-up. Use [solforge-build](../solforge-build/SKILL.md) when the task is a concrete feature or fix in working code that needs no runner orchestration.
