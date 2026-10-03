---
name: integrate-dayq-motion-animation
description: Integrate DayQ locomotion animation, motion matching, IK, root motion, overlays, and gameplay synchronization.
---

# Integrate DayQ Motion and Animation

Read [MOTION_ANIMATION_CONTRACT.md](references/MOTION_ANIMATION_CONTRACT.md). Treat Unreal's Game Animation Sample as a reference/baseline, not gameplay authority.

## Workflow

1. Inspect the approved skeleton, movement trajectory, stances, gaits, weapons, traversal actions and animation budgets.
2. Build Pose Search schemas/databases and Chooser routing for compatible contexts.
3. Project authoritative motion through Motion Matching; tune pose selection against actual DayQ speeds and accelerations.
4. Use orientation/stride warping and IK to improve contact, not conceal mismatched motion.
5. Use Motion Warping only for bounded actions with server-approved start, target, path envelope and cost.
6. Layer aim, weapon, injury, fatigue, load, breathing and physical reactions without multiplying state authorities.
7. Validate first/third-person parity, remote proxies, LODs, crowds, frame-rate variation and network corrections.

## Rules

- Animation notifies may request authoritative events but cannot commit gameplay state.
- Root motion must participate in the selected movement networking path.
- Foot locking and IK cannot alter authoritative actor transform.
- Provide fallbacks when animation data is absent or mismatched.

## Output

Deliver animation architecture, databases, Choosers, AnimBP/layers, motion-warps, Control Rigs, IK, montage/event contracts, budgets, debug captures and evidence.
