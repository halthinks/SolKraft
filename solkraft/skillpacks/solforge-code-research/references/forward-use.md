# Code Research forward-use guide

Use fresh, minimally primed evaluators for substantial skill releases.

Before using a not-yet-installed checkout, run the noninteractive contract harness from the repository root with `node --test tests/code-research.test.mjs`. Run the complete local MCP lifecycle from the `plugin` directory with `node scripts/mcp-discovery-smoke.mjs`. A production forward use must reconcile `registeredTools`, `modelCallableTools`, `appOnlyDecisionTools`, and `chatDecisionTool` through `get_capabilities`. UI transitions remain app-callable, while exact user-authored chat commands use `solforge_apply_chat_decision`; both must produce the same server cursor, graph, contract, and receipt lineage.

## Total-completion case

Give the evaluator:

- the raw path to the new Code Research skill;
- the raw path to one complex primary code or skill package;
- raw paths to its named companion packages; and
- a user-style request to reconstruct intended and latent design, find every material inconsistency and completion gap, define the target system, and produce the remediation plan.

Do not provide the intended findings or a prebuilt answer. Evaluate whether the artifact reconstructs design from evidence, finds cross-package contracts, distinguishes latent from implemented capability, preserves uncertainty, covers every accepted layer, and produces callable dependency-ordered remediation.

## Focused-mastery case

Give a bounded module, feature, or defect request and the raw repository path. Evaluate whether the skill reduces breadth and effort while retaining evidence IDs, inferred-design confidence, contrary evidence, regression boundaries, coverage, falsification, and a separately governed handoff.

## Failure probes

At minimum test local-only forward navigation, acceptance before all Next confirmations, stale source fingerprints, whitepaper drift, forged acceptance receipts, missing evidence references, phantom contrary-evidence IDs, an absence or empty contrary-evidence claim without a boundary, generic evidence reused across coverage layers, insufficient distinct coverage evidence, a missing focused scope/regression boundary, missing critic/falsification/regression artifacts, a critical open gap paired with `qualified_complete`, undeclared mutations, unregistered skill/routes, phantom remediation gaps, repository-path escape, case-colliding repository identities, a missing or unsafe focused command, unsafe optional broader commands, embedded absolute-path and non-executing collect/import command options, package-script and generic-output spoofing, Node file-wrapper passes without registered `node:test` cases, caller-forged test results, persisted failing output, exact failed replay without re-execution, same-program/cycle failure-receipt repair binding, caller-claimed paths that differ from repository snapshots, real unplanned changed paths or effects, renewable-lease concurrent retries, replay-intent drift, an implementation-authorized handoff, and replay with a different result hash.

Also run a table-driven routing matrix through both workflow classification surfaces. Positive cases cover natural total-completion and focused-mastery requests. Negative and mixed cases cover ordinary diagnosis, implementation, security, README transformation, Launcher, and Blender requests containing one incidental phrase such as “intended design” or “completion gap.” Both routers must select the same capability family and must reserve Code Research for explicit mastery intent or multiple independent mastery signals.
