---
name: solforge-workflow-software-build
description: "Build or fix a software feature with scoped implementation and verification. Use for requested code changes with a concrete behavior to deliver."
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Build or fix a software feature

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requested behavior, acceptance criteria, target checkout, and scope boundaries before writing. Locate the code that owns the behavior and read its surroundings first: existing patterns, naming, error handling, and test conventions set the shape of the change. Reuse valid existing work and inputs. If the request rests on an unexplained failure rather than a specified behavior, diagnose the cause before building on top of it.

Implement the smallest change that delivers the behavior. Prefer extending an existing module over adding parallel structure; introduce a new dependency, configuration knob, or abstraction layer only when the change genuinely requires it. Keep unrelated user work and out-of-scope refactors untouched. When the change alters a public interface, data format, or stored state, handle compatibility or migration explicitly rather than leaving existing callers broken. Scale ceremony to the request: a one-line fix needs no plan document.

Verify on the intended checkout with the project's own build and test commands, then demonstrate the requested behavior end-to-end with real calls — a clean compile or a successful import is not evidence the behavior works. For a fix, reproduce the original failure before correcting it when feasible, and follow repository red/green requirements. Do not weaken or delete a failing check to reach green, do not present a mock as evidence for an untested real dependency, and do not claim a change is reversible unless the prior state is actually preserved. After each correction, rerun the checks the edit invalidates.

Report what changed and where, the verification commands and their results, the demonstrated behavior, and any unverified limits. Use [result validation](../solforge-result-validator/SKILL.md) when acceptance requires evidence beyond the build's own verification.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, 100% eligible target recall.

<!-- END SOLKRAFT SKILL INTEGRATION -->
