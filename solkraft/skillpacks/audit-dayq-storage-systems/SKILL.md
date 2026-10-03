---
name: audit-dayq-storage-systems
description: Audit DayQ storage systems, authority, persistence, assets, and performance before milestone acceptance.
---

# Audit DayQ Storage Systems

Read [STORAGE_AUDIT_CONTRACT.md](references/STORAGE_AUDIT_CONTRACT.md). Never repair production data implicitly.

## Workflow

1. Freeze storage catalog, components, families, assets, runtime definitions, stocking profiles and ledger versions.
2. Validate unique IDs, references, schemas, compatibility and reachable recipes.
3. Detect impossible capacity, opening violations, recursive volume creation, invalid slots, unsupported load, missing closures/components and unsafe content mixing.
4. Trace every storage master through mass-content family, asset-factory, Blender, Unreal and evidence.
5. Trace every runtime container to inventory authority and persistence/migration.
6. Trace every stocking profile to catalog identities, physical fit and economy caps.
7. Test transactions, contention, spill, damage, theft, disconnect, restart, migration and representative 100-item/dense-base performance.
8. Emit blocker/high/medium/low findings and exact remediation.

## Completion

Return machine-readable findings and a concise report. Only passed evidence closes production/runtime coverage.
