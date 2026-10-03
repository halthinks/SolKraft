---
name: design-dayq-agent-printed-weapons
description: Implement DayQ fictional printed-weapon catalogs, build-file loot, agent unlocks, and manufacturing progression.
---

# Design DayQ Agent-Printed Weapons

Read [PRINTED_WEAPON_DESIGN_CONTRACT.md](references/PRINTED_WEAPON_DESIGN_CONTRACT.md) completely before acting.

## Workflow

1. Inspect current weapon, inventory, crafting, Glentech, agent, progression, asset, multiplayer, persistence, economy, and validation owners.
2. Select a catalog family through `dayq/data/DAYQ_AGENT_WEAPON_COMPANION_DEPENDENCY_GRAPH.json`. Confirm every companion-node reference, maintenance-profile reference, manufacturing gate, specialist owner, Blender stage and Unreal stage resolves before issuing a work order.
3. Treat a found complete build file as the recipe unlock for its base model. A damaged file needs an agent repair job. An advanced agent can later create variant recipes from weapons the player has actually used and maintained.
4. Resolve the family’s `maintenance_profile_ref` through `dayq/data/DAYQ_FIREARM_MAINTENANCE_PROFILE_INDEX.json`, then route the unlocked model through asset production and the existing crafting owner. The manufactured weapon is immediately usable and enters the existing condition, fouling, lubrication, wear, cleaning and repair loop.
5. Preserve persistent family, revision, weapon-instance, component, material-lot, work-order, build-file, and recipe-unlock identities.
6. Integrate through adapters. Existing owners retain weapon operation, ballistics, damage, inventory, fabrication, progression, authority, persistence, acoustics, movement, maintenance, and assets.
7. Run `python dayq/scripts/build_agent_weapon_companion_dependency_graph.py` and `python dayq/scripts/validate_agent_weapon_maintenance_profiles.py`, then validate schemas, recipe graphs, anti-duplication, restart, two-client authority, performance, visual quality, handling, maintenance integration and technical runtime evidence. Crafting produces a usable weapon without a second approval activity.

## Non-operational boundary

Create original fictional game definitions and production-asset contracts only. Do not produce real firearm CAD, STL, chamber or pressure-bearing dimensions, tolerances, toolpaths, ammunition construction, conversion instructions, or usable manufacturing procedures.

## Required output

Produce a family/revision contract, build-file loot placement, unlock rules, gameplay tradeoffs, abstract manufacturing gates, systemic asset work order, Unreal work order, test matrix, evidence list, and exact acceptance status.

## Hard boundaries

- The active DayQ builder hold is external authority. Never request, imply, or communicate a release.
- Do not acquire or bind ballistics plugins; the separate library-evaluation owner controls that decision.
- Keep all work DayQ-only. Never touch the wave-surfing project.
