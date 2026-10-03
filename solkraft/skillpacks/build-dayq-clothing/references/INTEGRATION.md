# DayQ clothing integration ownership

## Authoritative owners

| Concern | Existing owner | Clothing integration |
|---|---|---|
| Item identity and transfers | Authoritative fast-array inventory and transaction flow | Add definition/instance adapters, equipment relationships, pocket nodes, closure state, and zone references; never create a clothing inventory. |
| Physical pockets and carried load | Physical inventory/load/slot contract | Consume volume, opening, shape, mass, access, balance, retention, hand/posture, spill, and snag rules. |
| Materials and jobs | Raw-material crafting and current crafting authority | Add fibers, hides, sheets, panels, seams, closures, recipes, tools, workstations, quality, byproducts, and conservation data. |
| Damage and protection | Combat/damage and armor authorities | Clothing supplies ordered coverage/material/condition layers and receives authoritative localized outcomes; it does not resolve hits independently. |
| Exposure and health | Survival, weather, water, fire, contamination, health, and wounds | Clothing supplies layered heat/moisture/barrier responses and zone access; those systems own body outcomes. |
| Movement and traversal | Character movement and vertical traversal | Clothing supplies fit, joint restriction, traction, grip, bulk, snag, retention, and abrasion outputs. |
| Exoskeleton and mech | Existing exoskeleton/mech equipment owners | Clothing supplies underlayer, harness, connector, cooling, joint-clearance, pilot, and emergency-release compatibility. |
| Loot and economy | Loot, scavenging, AI loadouts, factions, and economy | Clothing supplies authoritative spawn profiles and instance generation inputs; existing systems own population/caps/circulation. |
| Persistence | Stable IDs, snapshots, journals, migrations, crash recovery | Persist versioned clothing extension records keyed to existing item IDs; no new save source of truth. |
| Visual assets | Systemic asset factory, Blender MCP, modular-character pipeline | Produce meshes/material regions/damage masks/LODs/cloth data; visuals never author gameplay condition. |
| Runtime evidence | DayQ Unreal MCP production and validation | Compile, PIE, multiplayer, restart, migration, rendering, and performance acceptance remain mandatory. |

## Project contracts

- System sheet: `systems/clothing.md`
- Decision record: `decisions/CLOTHING_CONCEPTUAL_DECISIONS.md`
- Implementation contract: `docs/clothing/DAYQ_CLOTHING_IMPLEMENTATION_CONTRACT.md`
- Schemas: `schemas/DAYQ_GARMENT_DEFINITION.schema.json`, `DAYQ_GARMENT_INSTANCE.schema.json`, `DAYQ_CLOTHING_RECIPE.schema.json`, `DAYQ_CLOTHING_REPAIR.schema.json`, `DAYQ_CLOTHING_SPAWN_PROFILE.schema.json`, and `DAYQ_CLOTHING_REPAIR_TOOL.schema.json`
- Fixtures and report: `validation/clothing/`
- Ledger: `../docs/DAYQ_REQUIREMENTS_LEDGER.md`

## Current evidence boundary

Skill, schema, contract, and deterministic validation pass locally. The UE 5.8 x64 C++ toolchain is installed and the DayQ editor build is in progress. Live MCP, PIE, network, persistence, migration, rendering, cloth, and performance acceptance remain open until representative garment assets and gameplay routes run successfully.
