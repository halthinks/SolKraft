---
name: solforge-platform-adapter
description: Implement platform-specific filesystem, process, UI, storage, permissions, and lifecycle adapters.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Platform Adapter

Implement platform-specific filesystem, process, UI, storage, permissions, and lifecycle adapters.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Define the source and requested target platform, architecture, versions, exact artifact, and meaning of compatibility. Establish baseline behavior and inspect OS APIs, native dependencies, paths, permissions, processes, lifecycle, and packaging.

Classify concrete coupling points and choose a narrow adapter, shared core, platform shell, or bounded redesign. Preserve existing behavior and public interfaces while changing the requested boundary.

Build with the actual target toolchain and run relevant checks on each available target. Record command, configuration, artifact hash, environment, and observed results; distinguish source inspection, cross-build, emulator, and real-target execution.

Report verified, buildable, adapter-required, redesign-required, unsupported, or unknown status per target, together with remaining checks and rollback. Do not inherit another target result or require a retired route receipt.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
