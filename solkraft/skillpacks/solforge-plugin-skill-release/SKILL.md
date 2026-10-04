---
name: solforge-plugin-skill-release
description: Create, update, install, and validate SolForge-owned native skills and their routing metadata.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolForge Plugin Skill Release

Create, update, install, and validate SolForge-owned native skills and their routing metadata.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Identify the actual skill, routing, packaging, service, or plugin source surface being changed. Inspect its existing development contracts, ownership, installation path, and redistribution license.

Make the change in authoritative source. Keep discovery metadata, invocation cues, resource links, prerequisites, procedures, outputs, and stop conditions consistent with real capabilities. Do not assume a retired SolForge MCP runtime exists.

Test useful positive, negative, and ambiguous selection cases, then package and inspect the installed artifact through the real host interface. Preserve existing public callable behavior unless a migration is authorized.

Report source, package, installation, and runtime verification separately. A cache edit, source-tree test, or host restart alone does not establish a working release.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
