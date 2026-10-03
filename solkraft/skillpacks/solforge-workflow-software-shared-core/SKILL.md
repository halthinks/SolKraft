---
name: solforge-workflow-software-shared-core
description: Separate portable behavior from target-specific UI, lifecycle, storage, permissions, and native integration.
---

# Create a shared core and platform shells

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish which behaviors must be portable, which targets are in scope, and what may differ per platform. Before moving code, inventory the existing coupling: trace where business logic touches UI frameworks, filesystem and process APIs, storage, permissions, and application lifecycle, and separate accidental coupling (an import used once for convenience) from genuine platform divergence. "Runs on Windows, macOS, and Linux with identical model behavior" is a criterion; "make it portable" is not.

Define the core's contract from observed behavior, not from an aspirational abstraction. Extract the portable logic behind explicit interfaces sized to actual divergence across the scoped targets, and keep the shells thin: each owns its UI, lifecycle, storage, permission, and native-integration code and nothing the core already decides. Decide per boundary whether to inject the dependency, expose a capability query, or accept a documented per-platform behavior — do not force one mechanism everywhere. Keep platform imports, build flags, and conditional compilation out of the core; if a difference needs conditional code, it belongs behind the boundary, not sprinkled through core logic.

Verify mechanically, not by inspection. Build the core standalone with no platform dependency present, or against a headless test shell, and run the same behavioral checks through at least two real shells so the boundary is exercised from more than one side. An interface with one real implementation and one mock is weak evidence of portability — a "portable" API that merely mirrors one platform's idioms leaks that platform into every shell, and compile-only success says nothing about behavioral equivalence. Distinguish defects in the core from defects in a shell when a check fails, and rerun affected shells after any boundary change.

Report the boundary contract, what moved into the core, each shell's remaining surface, the verification commands and their results, and residual coupling or documented per-platform divergence. Use [platform adapter](../solforge-platform-adapter/SKILL.md) when implementing the individual shell adapters themselves.
