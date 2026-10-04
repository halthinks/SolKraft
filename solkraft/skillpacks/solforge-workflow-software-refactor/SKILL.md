---
name: solforge-workflow-software-refactor
description: "Refactor code structure, duplication, or boundaries while preserving required behavior and compatibility. Use for requested restructuring or cleanup."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Refactor software structure

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requested scope precisely: the paths that may change, the behavior and public surfaces that must not, and the acceptance criteria. Identify external constraints before moving anything — public APIs, serialized formats, configuration keys, database schemas, and call sites outside the refactor boundary — since those fix what "behavior-preserving" means here. Read the target code and its existing tests before planning; a refactor sized from a directory listing is guesswork.

Characterize current behavior before changing structure. Run the existing checks on the intended checkout and record the baseline; where the code to be moved has no coverage, add characterization tests that pin the behavior being preserved, not the implementation statements. Decompose the work into small, individually verifiable steps in dependency order — extract before rename, move before reshape, introduce the seam before rerouting callers. Keep mechanical moves (rename, extract, inline) separate from semantic adjustments, and never bundle a behavior change into a refactor step: a red check then tells you nothing about which step broke.

Apply the steps and re-run the same checks after each meaningful step, on the same configuration as the baseline. Verify preserved behavior with evidence that actually exercises the moved code: a green suite that never covered the touched paths, or a clean compile, is weak evidence of preservation. Diff the public interfaces, exported symbols, and observable outputs before and after where they can be enumerated. Preserve reversibility — commits or patches scoped so any single step can be reverted without taking the rest down — and do not widen the diff into unrelated cleanup beyond the requested paths.

Report what moved and why, the verification performed and its results, any behavior the available checks do not pin, and follow-up risks such as uncovered call sites or pending deprecation steps. Read the [run-refactor method](../solforge-run-refactor/SKILL.md) when the request needs its full underlying procedure detail.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
