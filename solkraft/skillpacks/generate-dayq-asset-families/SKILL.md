---
name: generate-dayq-asset-families
description: Generate related DayQ asset families with shared contracts, provenance, and production validation.
---

# Generate DayQ Asset Families

Create physical families whose variation follows construction, components, history, condition, faction modification, and gameplay.

Read [ASSET_FAMILY_CONTRACT.md](references/ASSET_FAMILY_CONTRACT.md). Read the current content-universe entry and the existing systemic asset prompt, V2 asset contract, root-component, crafting, inventory, environmental-response, and Unreal acceptance contracts.

## Workflow

1. Define the invariant identity: purpose, silhouette class, construction method, interfaces, service access, load paths, mechanisms, dimensions and material regions.
2. Separate variation into:
   - production-master geometry;
   - optional/removable components;
   - bounded dimensional parameters;
   - material/state variants;
   - damage/repair configurations;
   - contents/spawn profiles;
   - faction/canon deltas.
3. Define compatibility keys, attachment sockets, pivots, collision envelopes, animation interfaces, inventory dimensions, damage zones and environmental material regions.
4. Identify combinations requiring distinct geometry, skeleton, collision, animation or runtime behavior. Promote those as separate masters; do not force unsafe parameterization.
5. Define allowed and forbidden configurations with player-readable reasons.
6. Link components to root materials, recipes, tools, workstations, power, skills, repair and salvage.
7. Assign asset classes and routes. Use references/img2threejs for suitable common hard-surface baselines; use original concept work for signature/fictional families; use $produce-dayq-organic-assets for deformables.
8. Generate a bounded variant matrix and representative acceptance set. Do not instantiate the full Cartesian product.
9. Route each production master through $build-dayq-systemic-asset-factory and each approved batch through $orchestrate-dayq-batch-assets.
10. Validate visual distinction, gameplay distinction, economy reachability, performance, replication and persistence.

## Completion

Deliver the family contract, master list, component graph, compatibility matrix, variant recipes, invalid examples, material/rig dependencies, catalog deltas, factory job seeds, performance budget and representative Unreal validation set.
