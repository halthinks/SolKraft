# DayQ Batch Orchestration Contract

The batch manifest records:

- stable batch ID/version, objective, region/milestone and frozen input hashes;
- catalog/family IDs and one existing asset-factory job ID per production master;
- dependency edges and critical path;
- route, skill lock, source/provenance state and decision authority;
- exclusive/shared tool resources and concurrency limits;
- stage status, receipt hashes, retry lineage and failure classification;
- Unreal staging package, binding owner and regression group;
- performance budget and measured aggregate cost;
- catalog, world-placement and release coverage affected;
- final accepted, failed, blocked or partial disposition.

Rules:

- A batch cannot override an asset job's status.
- A retry creates new stage evidence or a new versioned job where identity changed.
- Family-level validation supplements rather than replaces per-master evidence.
- Batch success requires all required jobs accepted; optional failures remain disclosed.
- Do not run heavy Unreal commandlets concurrently with an interactive editor unless the user explicitly accepts the resource impact.
