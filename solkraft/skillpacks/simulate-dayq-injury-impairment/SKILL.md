---
name: simulate-dayq-injury-impairment
description: Implement DayQ localized injuries and their effects on movement, grip, treatment, equipment, and animation.
---

# Simulate DayQ Injury and Impairment

Read [INJURY_IMPAIRMENT_CONTRACT.md](references/INJURY_IMPAIRMENT_CONTRACT.md). Extend the existing health/combat owners; never create a parallel hit-point or wound authority.

## Workflow

1. Map approved rig regions to health regions and protection layers.
2. Convert authoritative damage inputs into tissue trauma, bleeding, fracture, pain, shock and consciousness state.
3. Project health state into mobility, grip, balance, exertion, weapon handling, interaction and traversal capability.
4. Make symptoms legible through motion, breath, posture, blood, interaction speed and inspection—not only meters.
5. Integrate treatment reservations, interruption, carried-body handling, exoskeleton support and long-term recovery.
6. Persist lasting state through death/incapacitation rules, disconnect, restart and migration.
7. Validate combinations and prevent animation cancel, treatment duplication, friendly farming and client-authored impairment.

## Rules

- Injuries constrain capability; animation depicts the result.
- Avoid binary limb deletion unless the game explicitly adopts it.
- Do not make every wound a permanent movement tax; use staged severity and treatment opportunities.
- Exoskeletons may support a damaged body but cannot erase shock, blood loss, pain, fit or interface injury.

## Output

Deliver region mappings, wound state, impairment projections, treatment/recovery rules, animation hooks, persistence schema, tests, telemetry and evidence.
