---
name: solforge-install-plan
description: Design installation, launch, update, uninstall, troubleshooting, and rollback for a software product.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Install Plan

Design installation, launch, update, uninstall, troubleshooting, and rollback for a software product.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Identify the requested versions, source revision, target platforms and architectures, package formats, entrypoints, dependency pins, and existing build or install path. Separate demonstrated support from aspiration.

Inspect acquisition integrity, prerequisite detection, installation scope, first launch, updates, uninstall, and recovery. Implement or build only the distribution surfaces requested, using the repository toolchain.

Validate the exact artifact through its consumer path where available. Bind checksums, signatures, provenance, installation, and runtime evidence to its bytes; report missing tools, credentials, or targets.

Deliver the requested inventory, plan, artifact, or release matrix. Distinguish planned, built, installed, tested, signed, and published; local build success does not authorize or prove publication.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
