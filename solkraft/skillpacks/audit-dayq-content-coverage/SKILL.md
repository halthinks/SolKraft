---
name: audit-dayq-content-coverage
description: Audit DayQ content catalogs, asset pipelines, runtime coverage, and evidence for missing or inconsistent content.
---

# Audit DayQ Content Coverage

Measure coverage across design, production, runtime and playable-world layers. Do not treat file existence as acceptance.

Read [COVERAGE_AUDIT_CONTRACT.md](references/COVERAGE_AUDIT_CONTRACT.md). Use the bundled validator only against copies or user-authorized project paths.

## Workflow

1. Freeze catalog, family, skill, schema, factory, Unreal, region, progression and ledger versions.
2. Validate schemas, stable IDs, references, paths and version adapters.
3. Build graphs for acquisition, dismantling, crafting, repair, progression, family/master/variant, production lineage, runtime definition and world placement.
4. Detect cycles, orphans, missing sources/sinks, unreachable unlocks, impossible substitutions, duplicate semantic identities and variants that should be states.
5. Verify every production master has a governed job and every accepted job resolves to catalog, Blender, Unreal and evidence hashes.
6. Verify every gameplay catalog entry has an owner, authority, persistence and migration mapping.
7. Verify every active region/milestone has the required functional, ordinary, narrative, traversal, threat and resource coverage.
8. Aggregate geometry, textures, materials, animation, physics, audio/VFX, replication, save and density budgets.
9. Separate statuses: specified, queued, in-progress, accepted, failed, blocked, deferred and obsolete.
10. Emit deterministic findings with severity, owner, remediation, invalidated claims and ledger links.

## Completion

Return machine-readable findings plus a concise coverage report. Only passed evidence may close production or release coverage; placeholders may close explicitly labeled prototype-only requirements.
