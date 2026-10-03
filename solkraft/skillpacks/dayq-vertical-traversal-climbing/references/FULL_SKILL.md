---
name: dayq-vertical-traversal-and-climbing
description: Design, implement, and validate DayQ's vertical world, manual and assisted climbing, rappelling, traversal routes, fall systems, tall-building gameplay, traversal AI, and multiplayer movement. Use for urban verticality, climber exoskeletons, route design, movement mechanics, traversal equipment, world partition, and Unreal MCP implementation.
---

# DayQ Vertical Traversal and Climbing

## Mission

Make height a core survival, combat, logistics, scouting, and base-building dimension. Tall structures must be navigable systems with readable routes, risks, resources, defensive value, and alternate approaches—not decorative towers or linear climbing cutscenes.

## Traversal vocabulary

Support deliberate combinations of:

- step-up, mantle, vault, squeeze, slide, crawl, balance, and gap crossing;
- ladder, pipe, ledge, frame, rubble, facade, cable, and free climbing;
- rope ascent/descent, rappelling, belaying, hauling, zipline, and controlled lowering;
- window entry, ledge traverse, elevator shaft, stairwell, service duct, crane, rooftop, bridge, and facade routes;
- fall arrest, catch, swing, pendulum, slip, stumble, controlled drop, and rescue;
- improvised anchors, permanent anchors, grapnels, ascenders, descenders, winches, and climbing exos.

Do not grant universal magnetic hands. Every grip surface requires an authored or generated traversal classification and capacity.

## Surface and anchor contract

Define traversable surfaces and anchors with:

```yaml
surface_id: stable.identifier
traversal_tags: []
grip_quality: 0..1
load_rating_kg: number
condition: intact|wet|icy|corroded|burned|loose|contaminated
failure_curve: versioned.reference
noise: profile
tool_requirements: []
exo_compatibility: []
ai_support: none|strategic|full
```

Anchors also require direction of load, occupancy, attachment type, degradation, placement authority, ownership, visibility, removal, and persistence. Dynamic destruction must invalidate routes and navigation links.

## Character traversal state

Track contact state, hands occupied, grip reserve, stamina, load distribution, injury, surface condition, weather, fear/stress effects if adopted, equipment, tether state, exoskeleton mode, and available fall arrest.

Use deterministic movement envelopes with server validation. Preserve momentum where it creates readable risk. Avoid random falls: slips should result from observable overload, exhaustion, damage, bad surface, impact, or failed technique.

## Load integration

Read the physical inventory skill. Long weapons and bulky packs snag; poor load balance changes swing and mantle behavior; two-hand cargo prevents ordinary climbing; wet gear adds mass; unsupported weight accelerates grip drain. Allow hauling, staged caches, team relays, elevators, winches, and powered frames to solve logistical climbs.

## Climber exoskeleton integration

Climber exos may provide assisted grip, powered ascenders, joint bracing, anchor deployment, fall arrest, load transfer, and surface sensing. They must still obey contact geometry, rated loads, energy, heat, noise, damage, calibration, and failure states.

Define failure safely and legibly: degraded assistance, locked joint, bad sensor cue, anchor overload, tether cut, thermal shutdown, or battery exhaustion. Never teleport a failed climber to safety.

## Tall-building design doctrine

For each major tall structure, create a route graph with:

- ground approaches and exterior exposure;
- at least three route families when scope permits: public/internal, service/technical, and improvised/exterior;
- vertical safe points and defensible staging areas;
- power, fire, flooding, structural, weather, contamination, and defense-grid hazards;
- broken elevators and restorable lift infrastructure;
- material hauling routes distinct from solo infiltration routes;
- ranged sightlines, sound propagation, ambush, escape, and rescue options;
- rooftop connections, cranes, skybridges, adjacent structures, and underground links;
- high-value reasons to ascend: signals, solar access, rare equipment, observation, bases, or raid routes.

No route may require knowledge visible only to its designer. Establish visual, audio, environmental, map, or faction-intelligence cues.

## Combat rules

Support one-handed fire, braced fire, blind fire, melee shove, cutting ropes, damaging anchors, suppression, falling debris, and vertical flanking only where animations and balance support them. Accuracy, recoil control, reloading, and weapon access must reflect hand occupancy, support, exo stabilization, and load.

Protect against unavoidable spawn kills and indefinite rooftop dominance through multiple approaches, limited supplies, exposed silhouettes, drone reconnaissance, structural routes, and extract constraints—not invisible walls.

## Base building at height

Require structural load paths, anchor points, access routes, hauling, wind exposure, lightning, drainage, fire egress, power/water routing, repair reach, and siege access. Persist player ropes, ladders, anchors, bridges, hoists, and destroyed traversal elements. Rebuild navigation when construction changes a route.

## AI

Give AI explicit traversal capability profiles. Ordinary humans choose stairs/ladders and may fear exposed paths; trained climbers use ropes and advanced routes; exo units use rated assisted routes; robots use platform-specific affordances. Support pursuit abandonment, ambush, retreat, rescue, investigation of climbing noise, and strategic relocation across streamed cells.

Do not fake distant AI through impossible vertical transitions. Strategic simulation must preserve access constraints and travel time.

## Unreal MCP implementation

Inspect Character Movement, Motion Warping, animation, IK, GAS, navigation, Smart Objects, State Trees/behavior, collision, world partition, networking, and existing traversal plugins. Extend existing frameworks when safe.

Prefer tagged traversal affordances, reusable movement abilities/components, data-driven surface profiles, and authoritative state transitions. Use root motion or controlled procedural movement consistently. Bind hands/feet with IK only after movement authority and collision are stable.

Use Unreal MCP and EditorToolset to inspect actors, components, collision, nav links, animation assets, properties, world-partition settings, and test levels. Use Terminal for builds, map validators, route-graph checks, automation, network emulation, and profiling. Re-read modified properties and test in PIE.

## Multiplayer and persistence

Validate server authority for start surface, destination, path envelope, stamina/grip costs, anchor load, fall result, and exo assistance. Replicate compact state and critical contacts; do not stream every IK correction.

Test latency, packet loss, prediction correction, moving/destroyed surfaces, two climbers on one anchor, rescue tether, disconnect while suspended, late join near climbers, world-cell transition, and server restart. Persist placed traversal equipment, condition, ownership, load state when occupied, and route-affecting destruction.

## Validation gates

1. Every required route is physically continuous and signposted.
2. Traversal never crosses blocking geometry or ignores hand/load constraints.
3. Light, heavy, injured, wet, and exo-assisted states produce expected movement differences.
4. Anchor overload and structural destruction update all affected users and navigation.
5. Falls have consistent causes, trajectories, damage, and recovery rules.
6. Network corrections stay inside the approved visual/positional budget.
7. AI can use, reject, and reroute around vertical affordances appropriately.
8. A player can ascend, haul a critical component, fight, descend, save/restart, and retain world changes.
9. Tall-building traversal works from unanticipated entry direction and after streaming.
10. Worst-case climbers, ropes, AI, and destruction meet client/server budgets.

## Required output

Produce route graphs, surface/anchor contracts, ability/state changes, movement curves, equipment dependencies, Unreal assets changed, network/persistence design, PIE routes, captured evidence, performance data, failures, repairs, and acceptance status.
