---
name: progress-dayq-companion-agent
description: Implement DayQ companion progression, dialogue, combat guidance, evidence-based learning, and design unlocks.
---

# Progress DayQ Companion Agent

Read [COMPANION_AGENT_PROGRESSION_CONTRACT.md](references/COMPANION_AGENT_PROGRESSION_CONTRACT.md) completely before acting.

## Workflow

1. Inspect existing agent identity/checkpoint, training, research, Edge Interface, player progression, weapons, sensors, comms, exo/mech, authority, persistence, economy, UI, and audio owners.
2. Resolve the selected node through `dayq/data/DAYQ_AGENT_WEAPON_COMPANION_DEPENDENCY_GRAPH.json`. Its owner adapter must map to registered specialist skills, and every linked weapon family must resolve its maintenance profile, manufacturing gates, Blender stage and Unreal stage.
3. Keep physical A0-A6 capability bands separate from branch competency, certification, trust, doctrine, equipment, and field evidence.
4. Accept only server-signed novel combat, repair, production, research, and mission evidence. Field use creates episodes and hypotheses, never a permanent live self-rewrite.
5. Let the companion present evidence, uncertainties, and two or three meaningful development choices through conversation. The player chooses a branch; secured base training consumes compute, power, cooling, time, curated data, trainer attention, and evaluator capacity.
6. Run held-out evaluation, certification, signed checkpoint revision, deployment, rollback, backup, and recertification.
7. Route design insights to agent research and the owning physical system. A skill node may improve proposal quality or unlock a research route; it never creates materials, recipes, items, targets, or authority.
8. Implement combat voice as evidence-bound warnings and advice with confidence, age, priority, interruption, privacy, channel, accessibility, cooldown, and counterplay.
9. Run `python dayq/scripts/build_agent_weapon_companion_dependency_graph.py`, then validate anti-farming, privacy, late join, capture, revocation, restart, rollback, migration, two-client projection, degraded/offline operation, UI usability, audio clarity, and performance.

## Required output

Produce branch/node definitions, evidence and training contracts, dialogue states, voice-event rules, authority adapters, persistence/migration requirements, Unreal work orders, test matrices, and exact evidence status.

## Hard boundaries

- The companion has no hidden information, wall tracking, automatic lethal authority, recoil cancellation, free schematics, or live permanent self-rewrite.
- The active DayQ builder hold is external authority. Never request, imply, or communicate a release.
- Keep all work DayQ-only. Never touch the wave-surfing project.
