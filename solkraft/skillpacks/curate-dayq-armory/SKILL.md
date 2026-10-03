---
name: curate-dayq-armory
description: Build and validate DayQ weapon, ammunition, optic, attachment, and condition-state catalogs and assets.
---

# Curate DayQ Armory

Read [ARMORY_CONTRACT.md](references/ARMORY_CONTRACT.md) and the package `DAYQ_ARMORY_CATALOG.json` before changing the roster.

1. Inspect the current DayQ content catalog, weapon owner, inventory identities, attachment keys, ammunition definitions, `IBallisticsBackend`, damage/wounds, acoustics, locomotion, authority, persistence, economy, and asset-factory jobs. Extend them; never replace them silently.
2. Treat cataloged real-world names as reference families. Before shipping, apply the approved naming, trademark, serial-number, and trade-dress review. Preserve mechanical identity and factual compatibility without copying protected game assets or tuning.
3. Use one production master per materially distinct receiver/action/feeding/rig family. Build variants from bounded barrels, stocks, furniture, feeds, sights, mounts, muzzle devices, condition states, repairs, and DayQ canon deltas. Do not create a full Cartesian product.
4. Create the systemic prompt before searching. Collect lawful reference sets: principal views, verified dimensions, controls/action states, field-stripped arrangements, compatible magazines/ammunition, sight and attachment interfaces, wear/damage/repair examples, and public manuals/specifications. Record URLs, rights, hashes, attribution, uncertainty, and quarantine status.
5. Use img2threejs only for a reviewable hard-surface blockout when the source set is adequate. Promote the approved baseline through the existing DayQ Blender/Unreal asset factory. Require metric scale, separated moving components, magazine, action, safety/selector, sockets, pivots, collision/obstruction, LODs, UV/PBR, condition states, animations, and Unreal-ready metadata.
6. Define optics and mounts as physical components. Validate footprint/rail/ring standard, slot length, clearance, height-over-bore, eye relief, mass/balance, zero retention, power/battery, damage, wet/mud/fog states, backup-sight conflicts, and allowed/forbidden combinations.
7. Bind assets only through existing DayQ weapon/item interfaces. Server-authorize identity, configuration, ammunition/chamber/action, firing, impacts, damage, attachments, condition, repair, transfer, and persistence. Vendor types never cross the project-owned ballistics adapter.
8. Validate representative families in Unreal: scale, pivots, control animations, reload interruption, obstruction, stance/support, optics, sound, VFX, AI hearing, condition/malfunction, two clients, latency/loss, restart/migration, performance, and live PIE evidence.
9. Report catalog deltas, sources, masters, variants, compatibility, unresolved rights/geometry, work orders, evidence, and exact acceptance status. A catalog entry or Blender file is not a playable accepted weapon.
