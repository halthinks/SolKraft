---
name: solforge-workflow-software-portability-audit
description: Inventory platform coupling and build an evidence-bound compatibility matrix before making target claims.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Audit software portability

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the source platform, the claimed targets (operating system, architecture, runtime), the exact checkout or build under audit, and what "supported" means for each target: compiles, passes tests, or runs the real workload. Keep requested targets distinct from aspirational ones, and reuse any prior audit whose build and scope still match.

Inventory coupling systematically rather than sampling: operating-system APIs and syscall use; architecture assumptions such as word size, endianness, and alignment; toolchain and runtime versions; filesystem behavior including path separators, case sensitivity, symlinks, and locking; process, signal, and threading models; UI and display; network; permissions and sandboxing; hardware access; native libraries and their per-target availability; packaging, services, autostart, and update lifecycle. For each coupling point record where it occurs (file and symbol), what it assumes, and whether an existing portability layer isolates it. Inspect dependency manifests and build configuration for target-conditional code and per-platform dependency pins.

Build the compatibility matrix with an evidence class per cell: verified by a build, test run, or observed execution on that target; claimed by dependency or upstream documentation; inferred from source inspection; or unknown. A green compile is not evidence of correct runtime behavior, a pass on one distribution or version is not evidence for the whole family, and an emulation or translation layer is not native support — label it as such. Do not mark a target supported from source inspection alone, and do not generalize a result past the environment that produced it.

Report the coupling inventory with locations, the matrix with its evidence classes, per-target gaps ranked by remediation cost, and the unknowns that block a claim. Use the [portability audit method](../solforge-portability-audit/SKILL.md) when the audit needs fuller domain criteria than this procedure supplies.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
