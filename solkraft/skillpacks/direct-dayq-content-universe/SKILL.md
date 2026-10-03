---
name: direct-dayq-content-universe
description: Govern DayQ’s content catalog and dependency graph, including progression, production, and runtime coverage.
---

# Direct DayQ Content Universe

Treat the content catalog as the authoritative design index, not as an art wishlist.

Read [CONTENT_UNIVERSE_CONTRACT.md](references/CONTENT_UNIVERSE_CONTRACT.md) before editing catalog structure. Inspect the current DayQ skill registry, system index, root-component catalog, manufacturing catalog, construction recipes, asset-factory schemas, Unreal Data Assets, and validation ledger before adding identities.

## Workflow

1. Establish the requested region, milestone, system family, progression tier, and player purpose.
2. Inventory existing catalog identities and runtime owners. Reuse stable IDs; never create a duplicate because an asset has a new visual state.
3. Classify every entry as family, component, material lot, consumable, recipe output, buildable, character/creature, environment set, presentation resource, or unique strategic asset.
4. Link acquisition sources, dismantling outputs, recipes, stations, tools, skills, power, labor, transport, repair, degradation, sinks, spawning, world placement, production master, Unreal definition, persistence owner, and acceptance evidence.
5. Build the directed dependency graph. Reject impossible recipes, source-free requirements, sink-free abundance, inaccessible progression, circular unlocks, and catalog entries with no gameplay purpose.
6. Route new geometry families to $generate-dayq-asset-families. Route production masters to $build-dayq-systemic-asset-factory. Route batches to $orchestrate-dayq-batch-assets. Route placement to $populate-dayq-world-content.
7. Preserve existing authority: root components own material abstraction; crafting owns jobs and conservation; inventory owns item identities/transfers; economy owns circulation; persistence owns durable state; Unreal owners apply gameplay.
8. Version schemas and adapters. Never silently reinterpret an accepted ID or save payload.
9. Emit coverage requirements and work orders with explicit evidence gates.

## Completion

Return the versioned catalog delta, dependency graph, unresolved decisions, compatibility impact, orphan/cycle/source/sink results, production routes, runtime-owner map, migration needs, and validation status. Catalog completeness is not production acceptance.
