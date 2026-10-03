---
name: dayq-physical-inventory-load-and-slot-dynamics
description: Design, implement, and validate DayQ's server-authoritative physical inventory, backpacks, containers, attachment slots, carried-load biomechanics, packing, access time, encumbrance, and cargo transfer. Use for item dimensions, weight and volume, equipment layouts, backpack behavior, exoskeleton carry assistance, traversal load effects, multiplayer inventory, and Unreal MCP implementation.
---

# DayQ Physical Inventory, Load, and Slot Dynamics

## Mission

Make carried equipment a physical tactical choice. Inventory must account for mass, occupied volume, shape class, access, balance, attachment compatibility, containment, noise, and exposure. Avoid both unrestricted grid magic and tedious millimeter packing.

## Item physical contract

Require each carriable item to define:

```yaml
item_id: stable.identifier
mass_kg: number
packed_dimensions_cm: [x, y, z]
shape_class: rigid|compressible|folding|liquid|irregular|long|bulky
volume_l: number
stack: {max_count, nesting_rule}
grip_requirement: zero|one_hand|two_hand|team|lift_aid
attachment_tags: []
access_class: immediate|quick|stowed|secured|cargo
noise_profile: quiet|rattle|sloshing|loud
hazards: []
condition_affects_geometry: boolean
replication_class: aggregate|individual|unique
```

Give weapons, ammunition, batteries, fluids, armor plates, long tools, and rare secure hardware explicit geometry or attachment rules.

## Container and backpack contract

Define containers with:

- empty mass and exterior dimensions;
- usable internal volume and opening size;
- supported shape/size classes;
- named quick-access, internal, external, weapon, hydration, battery, and utility slots;
- mass rating and tear/break thresholds;
- closure, lock, seal, waterproofing, insulation, shielding, and contamination retention;
- compression, expansion, strap, frame, and modular-panel behavior;
- access posture and access time;
- center-of-load offset and sway;
- wet mass and durability;
- ownership, search, theft, drop, and persistent identity.

Slots are typed physical affordances, not universal squares. A canteen loop, magazine pouch, rifle sling, battery cradle, and internal compartment must behave differently.

## Packing rules

Use hybrid packing:

- enforce total internal volume;
- enforce opening and longest-dimension constraints;
- enforce typed attachment slots;
- use shape classes instead of full 3D bin packing for ordinary items;
- reserve exact footprints for tactical quick slots, armor plates, weapons, and mech/exo modules;
- allow automatic packing with a visible explanation when an item cannot fit.

Disallow impossible nesting and container recursion exploits. Liquids require compatible sealed capacity. Hazardous or contaminated items can foul a container and adjacent contents.

## Carried-load dynamics

Separate five values:

1. **Total carried mass.**
2. **Supported mass:** transferred through frame, belt, vehicle, exoskeleton, or mech hardpoint.
3. **Unsupported mass:** borne directly by the body.
4. **Load distribution:** front/back/left/right/high/low offset.
5. **Bulk and snag profile:** effect on gaps, climbing, stealth, and cover.

Drive movement from curves rather than hard thresholds. Load affects acceleration, sprint duration, turn response, vault height, jump reliability, climb speed, grip drain, fall arrest, swimming, prone transitions, stamina recovery, noise, footprint/track visibility, injury risk, and stumble response.

Do not make exoskeleton assistance erase inertia, bulk, structural ratings, battery draw, heat, joint limits, or poor balance.

## Hands and temporary carry

Track hand occupancy. Two-handed or team-lift items restrict weapon readiness, climbing, door use, healing, and fall arrest. Support dragging, shouldering, slinging, handing off, dropping, hoisting, tethering, vehicle loading, and exoskeleton-assisted lifting.

## Access and combat

Immediate slots permit direct use. Quick slots take a short animation. Stowed contents require the appropriate posture and container access. Secured cargo may require placing the container down or opening a closure. Being hit, moving, climbing, or falling may interrupt access.

Reloading must draw from compatible accessible magazines/ammunition, not any nested container. Make player intent readable and controller-friendly through search, filters, auto-sort policies, loadout templates, and clear failure reasons.

## Progression

- improvised pockets and hand carry;
- belts, slings, pouches, and civilian packs;
- framed expedition and tactical packs;
- powered carry-assist frames and cargo harnesses;
- climber/scout/combat exo integration;
- mech hardpoints, racks, magazines, and external cargo.

Progression adds capacity and specialization but also visibility, cost, heat, maintenance, and target value.

## Unreal MCP implementation

Inspect existing item, equipment, GAS, animation, movement, replication, save, and UI systems. Use versioned item definitions, container definitions, slot-tag compatibility, and encumbrance curves. Keep authoritative state separate from client presentation.

Use components for inventory ownership, containers, equipment slots, carried load, hand occupancy, contamination, and persistence. Use sockets for visible equipment and attachment points. Use Unreal MCP/EditorToolset to wire Data Assets, animation notifies, properties, and test actors. Use Terminal for validators, transaction tests, builds, and profiling.

## Multiplayer and persistence

Make transfers atomic and server-authoritative. Validate simultaneous pickup, trade, nested-container movement, dropped packs, corpse inventory, vehicle cargo, clan storage, theft, disconnect, reconnect, and server crash. Persist unique IDs, container tree, slot, orientation/shape state when relevant, condition, contamination, ownership, and current access state.

Aggregate common stacks only when provenance and condition rules permit. Never trust client-reported capacity, item creation, or final slot placement.

## Validation gates

1. Every item has valid mass, size, volume, and carry rules.
2. No item passes through an opening or slot it cannot physically use.
3. Nested containers cannot create volume or bypass mass.
4. Total mass, supported load, and balance reproduce after save/load.
5. Movement and climbing respond monotonically to tested loads unless an explicit assist changes the curve.
6. Quick versus stowed access produces observable timing and interruption differences.
7. A backpack tear/drop cannot duplicate or delete contents.
8. Two clients racing for one item yield one authoritative owner.
9. Exoskeleton battery failure immediately recomputes supported load without corrupting inventory.
10. UI remains usable with controller and keyboard/mouse under combat pressure.
11. Representative 100-item containers meet replication and UI performance budgets.

## Required test routes

Run at minimum: light load, balanced heavy load, badly offset load, over-rated pack, wet pack, climbing with long weapon, two-hand cargo handoff, exoskeleton assist loss, vehicle transfer, death/drop/recovery, late join, and restart persistence.

## Required output

Report contracts, capacity and movement curves, slot taxonomy, Unreal assets/components changed, network transaction design, persistence migration, evidence, performance, failures, and acceptance status.
