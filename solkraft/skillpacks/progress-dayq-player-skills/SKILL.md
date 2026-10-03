---
name: progress-dayq-player-skills
description: Implement DayQ use-based player skills, faction trees, training, unlocks, and anti-grind progression.
---

# Progress DayQ Player Skills

Load [the progression contract](references/PROGRESSION_CONTRACT.md) before changing progression or grants.

## Workflow

1. Inspect the progression catalog, origin mapping, death policy, authoritative gameplay owners, persistence schema, and economy assumptions.
2. Validate practice evidence on the server. Credit novelty, challenge, contribution, quality, risk, and diagnosed learning; reject duplicate IDs, low-risk repetition, AFK activity, arranged farming, and client-authored awards.
3. Keep knowledge, proficiency, conditioning, certification, tools, item quality, agent assistance, and team contribution distinct.
4. Advance only connected tiers. T1-T5 are shared; T6 requires matching origin, T5, a signed mastery trial, and required physical inputs.
5. Grant capability tags/recipes through owner adapters. Never duplicate combat, crafting, inventory, traversal, medicine, drone, agent, cyber, exo, mech, or building truth.
6. Journal every irreversible grant with stable evidence and transaction IDs. Make replay idempotent and migration origin-safe.
7. Run schema validation, semantic catalog validation, cohort simulations, Unreal automation, persistence recovery, and client-projection tests.

## Required status language

Distinguish implemented, automation-tested, live multi-client tested, blocked-environment, and unverified. A document or schema alone is not gameplay proof.
