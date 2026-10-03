---
name: dayq-raw-materials-and-crafting-trees
description: Design, implement, balance, and validate DayQ's data-driven resource conversion, fabrication, repair, salvage, and technology trees from raw scavenged matter through exoskeleton and mech-suit production. Use for materials, recipes, workstations, specialists, manufacturing chains, resource economies, crafting progression, and Unreal MCP implementation.
---

# DayQ Raw Materials and Crafting Trees

## Mission

Turn every craftable DayQ capability into a traceable physical chain:

`source -> extraction -> transport -> sorting -> processing -> component -> assembly -> calibration -> field use -> repair/salvage`

Never grant technology from an abstract unlock alone. Knowledge permits an attempt; tools, materials, power, specialists, tolerances, and secure components make it possible.

## Required inputs

Inspect the DayQ Decision White Paper, content contract, target item/system, existing recipes, inventory rules, base capabilities, exoskeleton/mech requirements, economy data, and Unreal project conventions. Record assumptions when any input is absent.

## Material model

Represent resources at five levels:

1. **Raw:** ore, scrap, timber, stone, fiber, crude chemicals, recovered electronics.
2. **Processed:** bar, sheet, plate, wire, cable, resin, fuel, glass, textile, ceramic.
3. **Parts:** bearings, fasteners, seals, cells, motors, pumps, actuators, boards, optics.
4. **Assemblies:** drive unit, joint, controller, armor panel, sensor pod, weapon mount.
5. **Systems:** generator, climbing rig, exoskeleton, suppression drone, mech module.

Every lot must support, where relevant:

- material family and grade;
- mass, volume, dimensions, and stack geometry;
- purity, condition, contamination, corrosion, fatigue, and provenance;
- tolerance or performance class;
- compatibility standard;
- recoverable yield and irreversible loss;
- hazard class and storage requirements;
- ownership and persistent identity for rare lots.

Do not collapse unlike materials into generic `metal`, `electronics`, or `chemicals` when their properties create gameplay decisions.

## Recipe contract

Define every recipe as data, not Blueprint-local constants. Require:

```yaml
recipe_id: stable.identifier
outputs: [{item_id, quantity, quality_rule}]
inputs: [{item_or_material, quantity, minimum_grade, accepted_substitutions}]
consumables: [{item_id, quantity_or_rate}]
workstation_capabilities: []
tools: [{capability, minimum_condition}]
specialists: [{discipline, proficiency}]
knowledge: [{schematic_or_research, revision}]
power: {peak_kw, average_kw, quality, duration}
environment: {cleanliness, temperature, ventilation, security}
stages: [{id, duration, interruptible, intermediate_output}]
failure_modes: []
quality_formula: versioned_rule
byproducts: []
repair_recipe: optional.reference
salvage_rule: versioned_rule
```

Give substitutions explicit penalties: added mass, reduced endurance, heat, noise, poor tolerance, shorter life, or higher failure chance. Never make substitution a free color swap.

## Crafting-tree topology

Build a directed acyclic dependency graph for ordinary production. Permit maintenance loops and recycling loops, but detect impossible recipe cycles and orphaned prerequisites.

Use intersecting capability branches:

- shelter and structural fabrication;
- water, sanitation, and agriculture;
- power generation, storage, and distribution;
- mechanical fabrication and mobility;
- chemistry, medicine, and protective equipment;
- electronics, sensing, and communications;
- weapons, ammunition, armor, and defenses;
- robotics and autonomous systems;
- post-quantum secure hardware and suppression technology;
- exoskeleton frames, actuation, controls, power, and armor;
- mech-suit structures, locomotion, thermal management, and weapon integration.

Gate tiers with demonstrated base capability, not player level. A recovered schematic does not substitute for a precision mill, stable power, clean electronics bench, calibrated metrology, or trained operator.

## Progression bands

- **T0 Improvised:** hand separation, cutting, binding, crude repair.
- **T1 Field Workshop:** bench work, basic welding, charging, common ammunition and tools.
- **T2 Industrial Recovery:** machining, casting, controlled chemistry, motors, hydraulic repair.
- **T3 Precision Systems:** electronics fabrication, sensors, high-grade cells, servo calibration.
- **T4 Secure Robotics:** autonomous systems, trusted controllers, suppression payload support.
- **T5 Exo/Mech Industry:** structural composites, high-load joints, advanced power and thermal systems.

Allow early access to degraded exoskeletons through recovery and repair while reserving reliable manufacture and extensive customization for later capability. Preserve the user's requirement that exoskeleton play appears early without trivializing the industrial tree.

## Workstations and production

Model workstations as capability providers with condition, calibration, tooling, power quality, queue, noise, heat, hazards, maintenance, and sabotage states. Support staged jobs, material reservation, authorized operators, interrupted work, partial products, quality inspection, and provenance.

Make transport meaningful. Large stock, armor plate, batteries, actuators, and mech assemblies require carts, vehicles, cranes, exoskeletons, hoists, or teams. Integrate all transfers with the physical inventory skill.

## Quality and failure

Calculate output quality from input grade, workstation state, tool condition, specialist proficiency, environmental suitability, recipe revision, and interruption history. Expose comprehensible causes, not hidden random punishment.

Low quality may produce poor fit, inefficiency, heat, noise, reduced precision, short service life, jams, leakage, or catastrophic overload. Safety-critical parts require inspection and traceable certification.

## Economy safeguards

Balance sources and sinks across scavenging, production loss, wear, repair, destruction, contamination, base capture, and salvage. Prevent saturation through credible maintenance and loss, not arbitrary deletion. Prevent duplication by making the server authoritative over reservations, job completion, outputs, and salvage.

## Unreal MCP implementation

Inspect existing item, crafting, ability, persistence, and UI frameworks before editing. Prefer versioned Data Assets or Data Tables for materials, recipes, capability tags, workstations, and progression nodes. Use reusable components for processing, production queues, calibration, condition, power use, ownership, and persistence.

Use Unreal MCP and EditorToolset to create or modify assets and properties; use Terminal for schema checks, graph analysis, commandlets, builds, and automated tests. Re-read created data after writing it. Launch Play-in-Editor for every connected production route.

## Multiplayer and persistence

Require server-authoritative:

- inventory reservation and release;
- production start, progress, interruption, and claim;
- quality generation and provenance;
- station permissions, queues, and sabotage;
- power/resource consumption;
- repair and salvage yields.

Persist lots, jobs, intermediate products, workstation condition, calibration, queues, ownership, and recipe/schema versions. Test late join, simultaneous claims, disconnect during crafting, server restart, rollback, migration, clan permission changes, and destroyed workstation recovery.

## Validation gates

Reject implementation unless all applicable gates pass:

1. Every output traces to valid sources and capabilities.
2. Graph analysis finds no accidental cycles, unreachable nodes, or free outputs.
3. Mass and item counts balance within declared processing losses.
4. Substitutions alter observable behavior.
5. Interrupted and concurrent jobs cannot duplicate resources.
6. Crafting from raw inputs through one exoskeleton component succeeds in PIE.
7. Transport and workstation load constraints are enforced.
8. Save/load preserves jobs, lots, quality, and provenance.
9. Multiplayer clients observe identical authoritative results.
10. Economy simulation shows neither immediate starvation nor uncontrolled saturation for tested clan sizes.

## Required output

Produce a dependency graph, data-contract changes, recipes and progression nodes, source/sink assumptions, Unreal assets changed, test route, evidence, failures and repairs, balance risks, migrations, and final acceptance status.

## Locked energy-industry route

The energy graph must include dead donor batteries -> graded reusable modules/material lots -> initially empty B0-B5 batteries through six physical Battery Bench stations -> earned first charge -> donor-adapted LS0-LS4 external-heat generators -> compact crude-burner-oil conversion -> upgraded synthetic gasoline -> municipal peak generation -> controlled metalworking -> recovered-vessel-first hydrogen -> later cylinder manufacture -> surplus-electricity electrolysis and battery/fuel-cell hybrids.

Keep B, LS, P, R, F, G and M gates independent. The first plastic batch must not require LS0 output; the first LS0 must close using finite charged B0 work, F1 work, limited P0/P1 work and plausible recovered precision donors. Track explicit matter and energy losses. Avoid real hazardous procedures, chemistry chores, certificate hunts, arbitrary component tokens and carried intermediate-fraction chains.
