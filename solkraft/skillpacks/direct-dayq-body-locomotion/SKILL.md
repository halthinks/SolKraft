---
name: direct-dayq-body-locomotion
description: Reconcile DayQ body, movement, animation, injury, equipment, and traversal architecture without duplicate authority.
---

# Direct DayQ Body and Locomotion

Read [BODY_LOCOMOTION_MASTER_CONTRACT.md](references/BODY_LOCOMOTION_MASTER_CONTRACT.md). Inspect current movement, health, combat, survival, inventory/load, clothing, traversal, weapons, exoskeleton, animation, AI, authority, persistence, and asset owners before planning.

## Workflow

1. Record the current implementation and evidence boundary.
2. Preserve one movement authority, one health/wound authority, and one persistent body identity.
3. Classify the request into rig/collision, ground locomotion, animation, injury/impairment, reactions/ragdoll, equipment/exos, traversal, or library evaluation.
4. Route to the narrowest downstream skill and every required upstream contract.
5. Require a vendor-neutral body and movement data boundary before adopting a library.
6. Implement in vertical slices: movement truth, animation projection, physical reaction, injury coupling, then equipment and traversal.
7. Gate progression on two-client authority, restart, migration, performance, first/third-person readability, and player testing.

## Rules

- Treat animation as presentation of authoritative movement and body state, except bounded server-approved root-motion actions.
- Never let an animation notify author damage, inventory, stamina, wounds, or persistent state.
- Keep capsule-driven locomotion as the control until a tested replacement passes every required gate.
- Keep Mover experimental and third-party libraries unadopted until isolated UE 5.8 bakeoffs pass.
- Route climbing/anchors/ropes to `dayq-vertical-traversal-climbing`; integrate through shared movement state rather than duplicating traversal.

## Output

Deliver ownership map, selected architecture, routed work orders, data contracts, dependency graph, migration plan, test matrix, evidence, blockers, and claim status.
