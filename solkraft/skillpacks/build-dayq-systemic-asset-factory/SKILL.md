---
name: build-dayq-systemic-asset-factory
description: Promote DayQ production assets through canon, provenance, Blender, Unreal, and live acceptance. Excludes ordinary graybox placeholders.
---

# DayQ Systemic Asset Factory

Create one traceable production-asset job. Never substitute prose, a generated model, import success, or compilation for live acceptance. Grayboxes, primitives, starter materials, labels, and temporary audio may prove gameplay without a factory job until the mechanic stabilizes or geometry becomes mechanic-critical.

Read all of these before acting:

- [asset-factory-contract.md](references/asset-factory-contract.md)
- [environmental-response-contract.md](references/environmental-response-contract.md)
- [provider-provenance-security-contract.md](references/provider-provenance-security-contract.md)
- [img2threejs-production-contract.md](references/img2threejs-production-contract.md)
- [blender-inspection-repair-contract.md](references/blender-inspection-repair-contract.md)
- [unreal-asset-acceptance-contract.md](references/unreal-asset-acceptance-contract.md)
- [reference-baseline-to-canonical-contract.md](references/reference-baseline-to-canonical-contract.md)

Use `$generate-dayq-systemic-asset-prompts` to form the canon/systemic brief, `$produce-dayq-assets` for reconstruction and Blender promotion, and `$dayq-unreal-mcp-production-validation` for Unreal work and evidence.

## Mandatory executable route

Do not create or accept a DayQ production asset outside the project runner. Prototype gameplay placeholders are outside this production acceptance claim and may be created directly. When promoting an asset, resolve the DayQ workspace root from a valid `DAYQ_ROOT`, the nearest current-directory ancestor, or the runner's verified physical location; require `dayq/scripts/dayq_asset_factory.py`, `dayq/asset_factory/pipeline.json`, and `tools/img2threejs/SKILL.md`, and stop if resolution fails. An explicitly configured but invalid `DAYQ_ROOT` is an error. From the resolved root:

1. Run `python dayq/scripts/dayq_asset_factory.py doctor`; stop if any native skill, upstream tool, Blender MCP socket, Unreal MCP, or UE 5.8 check fails.
2. Create the immutable job with `python dayq/scripts/dayq_asset_factory.py new ...` before authoring a prompt, downloading a source, opening Blender, or importing into Unreal.
3. Execute the stages in `dayq/asset_factory/pipeline.json` in order. Read and apply every skill named by the current stage. For an img2threejs route, also read and apply the pinned `tools/img2threejs/SKILL.md` and its routed references.
4. Keep every source, spec, render, `.blend`, export, Unreal work order, test result, screenshot, repair record, and receipt inside that job workspace. Record a stage only with `dayq_asset_factory.py record`; it hashes real files and rejects artifacts outside the job.
5. Run `dayq_asset_factory.py status` after every stage and `dayq_asset_factory.py validate` before reporting completion.

For hard-surface `img2threejs_then_blender` jobs, the accepted procedural model must be machine-promoted rather than manually rebuilt. Compile/export the accepted `THREE.Group` to a hashed GLB or express reviewed corrections as declarative `parts` in the job's Blender production spec. Run `dayq/scripts/dayq_blender_promoter.py` only through `dayq/scripts/dayq_blender_mcp.py` using the pinned Blender MCP environment. The promoter may interpret governed primitive types, import an accepted GLB, apply materials, generate LODs/UVs/sockets/collision, render, save, and export; it must not contain asset-specific shape coordinates or branches.

Import into a versioned Unreal staging package, then run `dayq/scripts/dayq_unreal_asset_promoter.py` through Unreal MCP. Do not destructively overwrite a loaded production StaticMesh package. Bind the accepted version through the existing DayQ runtime owner, compile, run PIE, inspect the live mesh path, exercise the interaction, and capture `unreal/evidence/live-pie.png`. Preserve failed imports/crashes as evidence and retry through a new versioned staging package.

Engine cubes, starter shapes, grayboxes, labels, compilation, import success, and prose are never production-asset evidence. They may remain in a gameplay harness without a factory job while visibly treated as prototypes. Once promoted to production, they cannot close visual, Blender, Unreal, or live-acceptance gates and must follow the governed job route.

## Workflow

1. Create the authoritative systemic prompt before source discovery. Classify the asset A-E, choose exactly one primary route, and record originality, rights, hidden-geometry, functional-accuracy, and decision-authority risks.
2. Create a unique job manifest and record the request, canon dependency, category, intended gameplay, search plan, source route, and acceptance route.
3. Classify every environmental channel as `applicable`, `not-applicable`, or `unknown-needs-evidence`; never omit one silently.
4. Record license, commercial/modification/redistribution rights, attribution, content hash, quarantine, and security disposition before importing anything.
5. Produce a baseline uncertainty record, then either a DayQ Canon Delta for Class B or original concept/similarity record for Class C/D.
6. If img2threejs is suitable, require detail inventory, ObjectSculptSpec, strict-quality gate, locked pass order, fixed renders, comparisons, scores, and exactly one decision per review.
7. Promote through Blender. Inspect, log defects, repair, rerender, and accept only when the production contract is met.
8. Integrate through Unreal. Validate interaction, environment, collision, replication, persistence, performance, PIE route, and automated tests.
9. Run `python dayq/skills/build-dayq-systemic-asset-factory/scripts/validate_asset_factory_job.py <job.json>`. An accepted job must have hashed Blender and live Unreal evidence.
10. Report `accepted`, `failed`, or `blocked` with the exact unmet gate and remediation. Never fabricate unavailable tool results.

## Output

Deliver the versioned job manifest, source/provenance record, systemic brief, environmental contract, reconstruction evidence when used, Blender evidence, Unreal evidence, defects and repairs, validation output, and final disposition.
