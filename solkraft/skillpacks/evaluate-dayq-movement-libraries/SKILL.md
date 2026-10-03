---
name: evaluate-dayq-movement-libraries
description: Evaluate DayQ movement and animation libraries against ownership, integration, and runtime requirements.
---

# Evaluate DayQ Movement Libraries

Read [MOVEMENT_LIBRARY_EVALUATION_CONTRACT.md](references/MOVEMENT_LIBRARY_EVALUATION_CONTRACT.md) and [CANDIDATE_BASELINE.md](references/CANDIDATE_BASELINE.md). Follow the existing `evaluate-dayq-unreal-libraries` acquisition, permission, isolation, evidence and disposition rules.

## Workflow

1. Inspect UE version, toolchain, licenses, source access, AI-use terms, platforms and current DayQ owners.
2. Create a vendor-neutral `IDayQMovementBackend` boundary or equivalent; vendor types may not enter persistent or gameplay-facing schemas.
3. Use the existing Character Movement implementation as the control.
4. Evaluate built-in animation/physics modules independently from movement authority.
5. Test Mover only in isolation while Epic labels it experimental.
6. Test ALS Refactored or any third-party candidate only after exact UE 5.8 compatibility and lawful source use are established.
7. Run identical movement, traversal, animation, injury, equipment, network, persistence, removal and performance fixtures.
8. Choose exactly one disposition per candidate: adopt, wrap, fork, reject, blocked-needs-acquisition, blocked-permission or blocked-environment.

## Non-negotiable gates

Authority, anti-cheat, correction quality, persistent-state independence, source/license, UE 5.8 editor/server build, platform packaging, removal, and representative performance cannot be averaged away.

## Output

Return signed candidate reports with versions, hashes, licenses, commands, metrics, defects, dispositions and the safe DayQ adapter recommendation. Never treat documentation claims as test results.
