---
name: solforge-package-detect
description: Inspect a repository for runtimes, entrypoints, build systems, dependencies, and packaging options.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Package Detect

Inspect a repository for runtimes, entrypoints, build systems, dependencies, and packaging options.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Inspect existing manifests, lockfiles, build definitions, entrypoints, and release artifacts before choosing a packaging strategy. Distinguish declared dependencies from installed tools and runnable outputs. Return the detected formats, reproducible commands, target requirements, and actual gaps; discovery alone does not authorize packaging changes.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
