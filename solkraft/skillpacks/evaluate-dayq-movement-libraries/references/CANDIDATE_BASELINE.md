# Candidate Baseline — 2026-07-19

Reverify every version and status before a bakeoff.

## DayQ Character Movement control

- Current runtime uses `ACharacter` and `UCharacterMovementComponent`.
- Use as the production control and initial owner-compatible path.
- Evaluate a project subclass, saved moves, custom modes and root-motion sources before replacement.

## Unreal Motion Matching / Pose Search

- UE 5.8 built-in animation stack.
- Candidate for animation selection, not movement authority.
- Requires DayQ animation data, trajectory/context adapter and representative cost testing.

## Game Animation Sample

- Epic reference project demonstrates capsule-driven Motion Matching, Choosers, ledges and vaulting.
- Use as reference and lawful source of migratable assets after verifying current terms.
- Its gameplay/traversal examples do not replace DayQ rules.

## Motion Warping

- UE 5.8 built-in Beta plugin.
- Candidate for bounded server-approved alignment actions.
- Reject any use that hides impossible geometry or bypasses movement authority.

## Control Rig / Full Body IK / IK Rig

- Built-in presentation tools for ground alignment, reaches, retargeting and equipment contacts.
- Do not let IK create authoritative contact or transform.

## Physical Animation / Chaos

- Built-in candidate for partial body response and deliberate ragdoll transitions.
- Requires stability, multiplayer, collision, recovery and performance evidence.

## Mover

- UE 5.8 documentation labels Mover experimental and warns against shipping without caution.
- Evaluate as a future rollback-networking movement backend only in isolation.
- Default disposition before live bakeoff: `blocked-environment` for production adoption.

## ALS Refactored

- MIT-licensed C++ community project with multiplayer-oriented movement and animation features.
- Published version table currently lists UE 5.7 as latest supported, not UE 5.8.
- Evaluate only if an exact UE 5.8 port builds and passes; never import directly into production first.
- Default disposition before port/evidence: `blocked-environment`.
