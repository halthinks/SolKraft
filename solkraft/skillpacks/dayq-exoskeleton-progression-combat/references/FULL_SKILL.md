---
name: dayq-exoskeleton-progression-and-combat
description: Design, implement, balance, and validate DayQ exoskeletons from early recovered walk and carry assist through scout, climbing, evasive, industrial, medical, and combat systems. Use for exoskeleton frames, modules, progression, locomotion, load support, combat, damage, power, crafting, networking, persistence, and Unreal MCP implementation.
---

# DayQ Exoskeleton Progression and Combat

## Mission

Make exoskeletons an early visible aspiration and core gameplay layer. Players should recover, repair, improvise, specialize, fight over, and eventually manufacture powered frames. Exoskeletons amplify capability while adding mass, inertia, noise, heat, power demand, maintenance, compatibility, and new failure modes.

Do not treat an exoskeleton as a flat stat buff, cosmetic skin, universal armor, or prerequisite-free class selection.

## Family taxonomy

Support overlapping frame families:

- **Walk assist:** fatigue relief, rehabilitation, injury compensation, long patrols.
- **Carry assist:** supported load, lifting, hauling, recoil bracing, logistics.
- **Industrial:** tools, welding, cutting, demolition, hazard protection.
- **Scout:** low noise, sensors, endurance, observation, communications.
- **Climber:** grip assistance, ascenders, anchors, fall arrest, load transfer.
- **Evasive:** burst acceleration, lateral recovery, impact mitigation, rapid stance changes.
- **Combat:** armor interfaces, weapon bracing, protected actuation, tactical power.
- **Medical/rescue:** casualty carry, stabilization, extraction, contaminated-zone support.

Permit hybrid builds within frame ratings. Preserve strong tradeoffs so one build cannot maximize armor, stealth, speed, endurance, climbing, payload, and firepower.

## Exoskeleton data contract

Define each frame and module with stable IDs and versioned data:

```yaml
frame_id: stable.identifier
body_coverage: [legs, hips, torso, arms, hands]
dry_mass_kg: number
supported_load_kg: number
joint_limits: {}
actuation: passive|spring|electric|hydraulic|hybrid
power_bus: []
control_bus: []
hardpoints: []
thermal_capacity: number
noise_profile: curve
protection: {}
mobility_envelope: curve_set
compatibility_tags: []
maintenance: {}
failure_modes: []
```

Modules require mass, volume, power/peak draw, heat, bandwidth, mounting points, software/firmware trust, calibration, condition, armor, exposure, repair parts, crafting origin, and persistence identity when rare.

## Progression doctrine

- **E0 Encounter:** see elite/AI/faction exos; recover damaged assist parts early.
- **E1 Field recovery:** operate unreliable walk/carry frames with improvised power and limited modules.
- **E2 Specialization:** build scout, climber, industrial, rescue, or combat variants from shared standards.
- **E3 Clan manufacture:** fabricate frames, joints, harnesses, armor, controllers, and service bays.
- **E4 Secure systems:** integrate trusted sensors, autonomy, suppression shielding, and advanced control.
- **E5 Mech bridge:** powered armor frames become cockpit/harness and subsystem ancestors of mech suits.

Early access must be playable but constrained by repair, batteries, fit, noise, and incomplete protection. Do not postpone all exoskeleton gameplay to endgame.

## Fit, control, and operation

Require body fit, harness adjustment, calibration, boot sequence, safety checks, and control mode. Model user strength/injury only where it creates decisions. Support powered, passive, degraded, emergency-release, limp-home, locked-joint, overload, thermal-limited, and unpowered states.

Movement is derived from character ability plus frame envelope plus load plus terrain plus damage. Assistance changes acceleration and force but does not delete total mass or momentum. Evasive systems require ground contact, available power, joint authority, and recovery time.

## Inventory and load integration

Read the physical inventory skill. Exoskeletons can transfer supported load to the ground and expose typed hardpoints, but backpack volume, balance, snag profile, hand occupancy, and module geometry remain relevant. Power loss converts supported mass into an emergency load and may force dropping cargo or releasing the frame.

## Crafting and base integration

Read the raw-material crafting skill. Every exosystem needs an acquisition path: salvage, repair, licensed schematic, reverse engineering, fabrication, calibration, and service. Require benches, lifts, diagnostics, stable power, specialists, consumables, spare actuators, seals, lubricants, cells, armor materials, and secure controllers according to tier.

Bases need exo racks, charging, maintenance clearance, cranes, parts storage, security, and emergency fire response. Frames are valuable persistent assets subject to theft, permissions, sabotage, and capture.

## Combat doctrine

Exos affect recoil, weapon mass tolerance, melee force, shield use, casualty carry, exposure, noise, heat, silhouette, and armor mounting. They do not automatically increase aim skill, situational awareness, or weapon reliability.

Model component damage: sensor loss, actuator leak, joint drag, cable damage, armor breach, battery fire, controller fault, hardpoint jam, and harness injury transfer. Give attackers readable counters: joints, power, cooling, exposed cables, terrain, EMP/electronic effects only where canonically valid, traps, armor-specific ammunition, and logistics attrition.

Prevent evasive frames from becoming latency-breaking teleporters. Use bounded impulses, telegraphed energy state, server authority, collision sweeps, and recovery windows.

## Vertical traversal integration

Climber frames must consume the vertical traversal contracts. Validate rated anchors, surface grip, tool contact, tether, load, wind, power, thermal state, and damage. Support wall work, facade infiltration, shaft ascent, rooftop logistics, casualty lowering, and vertical combat without granting universal surface adhesion.

## Unreal MCP implementation

Inspect character, equipment, animation, IK, GAS, movement, damage, inventory, crafting, vehicles, networking, and save frameworks. Implement frames/modules as data-driven composition. Prefer reusable components and gameplay tags; keep authoritative physics/combat logic in appropriate C++ or validated server systems.

Use Unreal MCP/EditorToolset for Skeletal Meshes, Control Rigs, sockets, components, Data Assets, abilities, effects, animation graphs, collision, and test actors. Use Terminal for builds, data validation, automation, network tests, and profiling. Test each frame in PIE under real load and failure states.

## Multiplayer and persistence

Server-authoritatively validate equip, calibration, power, module state, movement envelope, attacks, damage, emergency release, repair, and ownership. Replicate necessary pose/mode/module effects without broadcasting high-frequency actuator internals.

Persist unique frame/module IDs, ownership, fit/calibration, configuration, condition by component, power/fuel, firmware/trust state, repair history, loaded cargo links, location, and permissions. Test late join, possession change, theft, disconnect mid-climb, death in frame, server restart, destroyed module, schema migration, and recovery.

## Validation gates

1. Each family creates a distinct useful play style and counterplay.
2. Early damaged frames are obtainable and usable without bypassing later industry.
3. All assistance respects power, heat, load, geometry, and component condition.
4. Unsupported mass and failure transitions remain physically coherent.
5. Combat advantages have observable costs and counters.
6. Climber variants pass the vertical traversal gates.
7. Craft/repair paths trace to raw materials and valid workstations.
8. Two clients see identical authoritative configuration, damage, and movement mode.
9. Save/load preserves configuration and component condition.
10. Representative exo squads meet animation, physics, CPU, memory, and bandwidth budgets.

## Required output

Produce frame families, module contracts, progression graph, crafting dependencies, movement/combat curves, failure matrix, Unreal changes, network/persistence design, test routes, evidence, performance, balance risks, repairs, and acceptance status.
