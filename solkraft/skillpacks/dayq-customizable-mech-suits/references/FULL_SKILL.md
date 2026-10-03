---
name: dayq-customizable-mech-suit-system
description: Design, implement, balance, and validate DayQ's late-progression customizable mech-warrior-class suits as persistent modular vehicles descended from exoskeleton technology. Use for mech chassis, cockpits, locomotion, reactors and batteries, armor, sensors, weapons, hardpoints, damage, customization, logistics, networking, persistence, crafting, and Unreal MCP implementation.
---

# DayQ Customizable Mech Suit System

## Mission

Build the top of DayQ's exoskeleton progression: pilot-operated, mech-warrior-class suits assembled from deeply variable interoperable components. Treat each suit as a persistent industrial war asset with crew, fabrication, transport, maintenance, ammunition, power, heat, signature, terrain, and counterplay—not as a character skin or unrestricted power fantasy.

Use original DayQ names, silhouettes, interfaces, lore, and rules. `Mech-warrior-class` describes scale and fantasy only; do not copy protected names, factions, designs, terminology, or assets from other franchises.

## Relationship to exoskeletons

Require mature exoskeleton frames, control systems, joints, actuators, balance software, power buses, armor standards, and maintenance capability before mech manufacture. Permit rare captured prototype suits before clan manufacture, but make operation and sustainment difficult.

Carry forward the same principles: physical load, component condition, power, heat, hardpoints, calibration, ownership, salvage, and server authority. A mech is a vehicle-scale extension of DayQ systems, not a disconnected minigame.

## Suit architecture

Model a suit as a validated assembly graph:

- chassis/core frame;
- cockpit or pilot harness and life support;
- hip/torso rotation unit;
- locomotion set: biped, digitigrade, heavy biped, tracked auxiliary, or other approved platform;
- left/right legs, feet, stabilizers, and jump/assist modules;
- left/right arms, manipulators, shields, tools, and weapon adapters;
- power source, storage, conversion, and distribution;
- cooling, heat sinks, pumps, radiators, and emergency venting;
- control computer, trusted root, actuator controllers, and fallback controls;
- sensor mast, optics, radar/acoustic suites, communications, and countermeasures;
- armor zones, structure zones, internal bays, and external racks;
- weapon hardpoints, ammunition feeds, magazines, and recoil paths;
- utility hardpoints for cargo, rescue, engineering, climbing, suppression, or drone support.

## Component contract

Every component must declare:

```yaml
component_id: stable.identifier
category: chassis|locomotion|power|thermal|control|sensor|armor|weapon|utility
mass_kg: number
volume_or_envelope: {}
mount_tags: []
required_connections: [structural, power, coolant, control, ammo]
provided_capabilities: []
static_and_dynamic_loads: {}
power: {idle_kw, active_kw, peak_kw}
heat: {idle, active, peak, capacity}
bandwidth: number
armor_and_structure: {}
signature: {visual, thermal, acoustic, electromagnetic}
maintenance: {}
failure_modes: []
crafting_reference: stable.identifier
replication_class: configuration|state|event
```

Validate mount geometry, mass budget, center of mass, structural load path, power peak, cooling capacity, control bandwidth, recoil path, ammunition feed, pilot clearance, ground pressure, and transport envelope. Refuse invalid assemblies with specific reasons.

## Customization space

Support many meaningful variations per subsystem. Examples include:

- light, standard, reinforced, articulated, stealth-treated, or improvised armor;
- electric, hybrid, turbine-generator, fuel-cell, or recovered secure power;
- endurance, burst, silent-watch, or high-output energy tuning;
- passive, liquid, phase-change, expendable, or exposed radiator cooling;
- scout optics, artillery sensing, urban acoustic mapping, defense-grid analysis, or drone control;
- manipulators, breaching tools, shields, cargo lifters, winches, climbing claws, or rescue rigs;
- ballistic, missile, directed-energy only if canonically supported, melee, suppression, and utility weapons;
- software doctrine, pilot assist, stabilization, targeting, autonomy limits, and trust hardware.

Variation must change performance, handling, logistics, signature, maintenance, or tactical role. Reject cosmetic-only component proliferation from the functional system.

## Role families

Enable emergent builds rather than fixed classes, while test-balancing recognizable roles:

- scout/recon;
- urban climber and vertical assault;
- cargo/engineering and base construction;
- rescue and recovery;
- anti-robotic/defense-grid assault;
- bunker breacher;
- close-combat shield unit;
- fire support;
- anti-mech hunter;
- command, sensors, and drone coordination.

No build may dominate all ranges and logistics contexts. Terrain, bridges, floors, doors, elevators, mud, rubble, slope, building load, sensors, maintenance, and supply must constrain deployment.

## Pilot and operation

Require entry/exit, startup, authentication, calibration, pilot fit, visibility, control modes, emergency shutdown, fire suppression, ejection or escape where supported, incapacitation, and capture. A pilot's inventory transfers only through defined cockpit, rack, or cargo interfaces.

Model acceleration, inertia, ground pressure, turning, bracing, recoil, stability, falling, collision, crush risk, step-up, slope, wading, and vertical interaction. Do not animate a massive suit like an enlarged human.

## Combat, damage, and counterplay

Use zone and component damage, penetration path, spall/secondary damage, heat, fire, leaks, jams, sensor occlusion, actuator loss, leg collapse, power-bus fault, ammunition cookoff, controller degradation, and pilot injury. Preserve useful disabled/captured states; destruction need not always erase the asset.

Provide infantry, exoskeleton, vehicle, robotic-defense, and mech counters through ambush, mines, terrain denial, joints, sensors, cooling, power, ammunition, mobility kills, boarding, traps, artillery, and logistics. Make signature and noise strategically important.

## Climbing and vertical play

Read the vertical traversal skill. Only suitably designed suits may climb, anchor, rappel, brace between structures, use industrial lifts, or cross roofs. Validate building structural capacity, contact points, ground pressure, handholds, anchor loads, power, heat, and fall consequences. A climbing mech creates new routes but may also collapse them.

## Crafting, transport, and bases

Read the raw-material crafting skill. Require clan-scale dry docks/bays, cranes, precision tooling, secure storage, high-quality power, coolant service, diagnostics, ammunition production, specialists, and guarded supply chains. Parts must be transported physically; complete suits may require carriers, heavy trailers, repaired rail, or walking deployment.

Support field repair, cannibalization, controlled salvage, component provenance, captured parts, incompatible standards, and reverse engineering. Never craft a complete suit from a single abstract resource total.

## Unreal MCP implementation

Inspect existing vehicle/character movement, physics, Chaos, animation, Control Rig, GAS, weapons, inventory, crafting, damage, AI, camera, input, world partition, networking, and save systems. Choose a server-authoritative movement architecture and document it before implementation.

Use a composition model driven by versioned Data Assets. Separate assembly validation, authoritative simulation, damage, presentation, audio/VFX, and UI. Use Unreal MCP/EditorToolset to configure meshes, skeletons, sockets, physics assets, components, hardpoints, cameras, Data Assets, abilities, effects, and maps. Use Terminal for builds, validators, automation, network emulation, replay comparison, and profiling.

Do not implement runtime code from this skill when the work order is documentation-only. Produce contracts and integration guidance for the owning runtime task.

## Multiplayer and persistence

Server-authoritatively validate assembly, equip/unequip, movement, aiming, firing, ammunition, heat, power, damage, entry/exit, ownership, repair, capture, and salvage. Replicate configuration once, continuous state at budgeted rates, and discrete events reliably. Use prediction only within an approved correction model.

Persist suit ID, chassis, every installed component ID and condition, calibration, software/trust versions, power/fuel, ammunition, coolant, heat-safe state, cargo, owner/clan/permissions, pilot link, location/transform, repair history, captured provenance, and active production/repair jobs. Test crash recovery, migration, late join, disconnect while piloting, abandoned suit, capture, cross-cell travel, and simultaneous service operations.

## AI and strategic simulation

Give AI roles, doctrine, target selection, heat/ammunition awareness, retreat, surrender/abandon, recovery, and navigation constraints. At distance, preserve position, route feasibility, fuel/power, damage, ammunition, and mission outcome without simulating every joint.

## Validation gates

1. Assembly validator rejects structural, mount, power, cooling, recoil, clearance, and control incompatibilities.
2. At least five materially different viable configurations emerge from shared components.
3. No configuration maximizes speed, armor, range, firepower, stealth, endurance, and climbing.
4. Damage to each critical subsystem produces readable degradation and recoverable state where intended.
5. Crafting and repair trace to valid raw materials, workstations, specialists, and transport.
6. Vertical actions obey the traversal and structure contracts.
7. Infantry/exo/vehicle counterplay succeeds under designed conditions.
8. Multiplayer configuration, movement, damage, and firing remain authoritative under latency and loss.
9. Save/load and crash recovery preserve the complete suit without duplication.
10. Representative battles and dense bases meet server, client, memory, physics, animation, and bandwidth budgets.

## Required output

Produce assembly schema, component catalog, compatibility rules, role builds, progression/crafting graph, movement and damage architecture, counterplay matrix, Unreal integration plan, networking/persistence design, test scenarios, evidence, performance risks, repairs, and acceptance status.
