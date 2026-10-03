---
name: orchestrate-dayq-batch-assets
description: Execute and resume related DayQ asset-factory jobs with per-asset provenance and acceptance evidence.
---

# Orchestrate DayQ Batch Assets

Batch planning may increase throughput; it may never weaken one-job lineage or acceptance.

Read [BATCH_ORCHESTRATION_CONTRACT.md](references/BATCH_ORCHESTRATION_CONTRACT.md). Inspect the current catalog, family contracts, asset-factory runner/pipeline, skill registry, production capacity, and Unreal staging rules.

## Workflow

1. Select an evidence-bounded batch objective: one playable route, location kit, asset family, or progression milestone.
2. Freeze catalog/family versions and calculate the dependency DAG.
3. Create one batch manifest and one immutable existing-factory job per production master. Never hide multiple masters inside one receipt.
4. Group compatible work by route, source search, material library, skeleton, modular kit, Blender scene, Unreal staging package and validation route.
5. Enforce concurrency limits for Blender, Unreal, GPU rendering, browser reconstruction and source acquisition.
6. Run preflight: skills, schemas, rights, source quarantine, disk, tools, Unreal version, MCP connectivity and existing production-owner conflicts.
7. Execute only dependency-ready jobs. Preserve failures and continue unrelated branches when safe.
8. Resume from hashed receipts; never infer a passed stage from files alone.
9. Promote versioned Unreal staging assets, bind through existing owners, and run family-level plus per-master acceptance.
10. Reconcile catalog/economy/world-placement status only after accepted receipts exist.
11. Report throughput, failure causes, rework, budget use and remaining coverage without converting blocked jobs into success.

## Completion

Produce a validated batch manifest, immutable job map, dependency order, resource locks, per-job status/evidence, catalog deltas, Unreal staging/binding record, performance totals, failures/retries and exact acceptance disposition.
