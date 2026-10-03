---
name: standardize-dayq-rigs-interactions
description: Standardize DayQ rigs, sockets, constraints, animation, and physical interaction interfaces across asset families.
---

# Standardize DayQ Rigs and Interactions

Make interactions reusable while preserving object-specific mechanics and physical limits.

Read [RIG_INTERACTION_CONTRACT.md](references/RIG_INTERACTION_CONTRACT.md). Inspect existing movement, inventory/load, clothing, weapon, vehicle, traversal, exoskeleton, building, interaction, animation, authority and persistence owners.

## Workflow

1. Classify the interaction family and retained gameplay owner.
2. Define participants, preconditions, approach/stance volumes, hand/tool occupancy, authoritative state machine, interruption points and recovery.
3. Define coordinate/scale conventions, skeleton or pivot hierarchy, sockets, attachment tags, constraints, collision channels and animation events.
4. Specify authored animation, procedural alignment, IK, motion warping and fallback boundaries. Never hide impossible geometry with hand sliding.
5. Map load, reach, strength, injury, clothing, weather, footing, power, condition and obstruction inputs.
6. Define multiplayer prediction/correction, contention, permissions, disconnect, late join and rollback.
7. Define persistence only for meaningful object/interaction state; animations themselves are transient.
8. Produce reference rigs and conformance tests for Blender exports and Unreal imports.
9. Require each family to declare compatible standards and object-specific deviations.

## Completion

Deliver rig/interaction IDs, hierarchies, sockets, state machines, tags, animation events, constraints, authority/persistence rules, Blender/Unreal export contract, conformance fixtures and representative PIE/multiplayer evidence.
