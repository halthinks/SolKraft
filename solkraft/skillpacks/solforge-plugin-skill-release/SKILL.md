---
name: solforge-plugin-skill-release
description: Create, update, install, and validate SolForge-owned native skills and their routing metadata.
---

# SolForge Plugin Skill Release

Create, update, install, and validate SolForge-owned native skills and their routing metadata.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Identify the actual skill, routing, packaging, service, or plugin source surface being changed. Inspect its existing development contracts, ownership, installation path, and redistribution license.

Make the change in authoritative source. Keep discovery metadata, invocation cues, resource links, prerequisites, procedures, outputs, and stop conditions consistent with real capabilities. Do not assume a retired SolForge MCP runtime exists.

Test useful positive, negative, and ambiguous selection cases, then package and inspect the installed artifact through the real host interface. Preserve existing public callable behavior unless a migration is authorized.

Report source, package, installation, and runtime verification separately. A cache edit, source-tree test, or host restart alone does not establish a working release.
