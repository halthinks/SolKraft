---
name: implement-dayq-ground-locomotion
description: Implement DayQ ground movement, gait, posture, terrain, load, and authoritative locomotion behavior.
---

# Implement DayQ Ground Locomotion

Read [GROUND_LOCOMOTION_CONTRACT.md](references/GROUND_LOCOMOTION_CONTRACT.md). Consume physical-load, clothing, survival, health, weather and weapon projections. Preserve the chosen movement authority.

## Workflow

1. Establish an internal Character Movement control with deterministic fixtures.
2. Define stances, gaits, transition permissions and capability curves.
3. Map input intent through acceleration, braking, turn response, inertia, traction and current body capability.
4. Integrate load, pain, wounds, fatigue, surface, slope, footwear, wetness, wind, assistance and hand occupancy.
5. Keep gameplay motion capsule-driven; project it into animation through a vendor-neutral trajectory.
6. Add custom movement modes only with server validation, saved-move support and correction evidence.
7. Test first/third-person, keyboard/controller, latency/loss, slopes/stairs, moving bases and representative density.

## Rules

- Avoid twitch-speed direction reversal under heavy load.
- Avoid random stumbles; every failure must have a readable physical cause.
- Do not let visual root motion bypass authoritative collision or cost.
- Keep climbing and ropes under the traversal owner.

## Output

Deliver movement states, curves, surface profiles, capability inputs, network prediction fields, tests, telemetry, performance, evidence and acceptance status.
