---
name: run-dayq-autopilot
description: Build DayQ autonomously in playable, dependency-ordered cycles when the user requests autonomous game development.
---

# Run DayQ Autopilot

Optimize for playable game delivered per hour. Keep building while the current route runs; do not turn routine implementation into an acceptance campaign.

Read [BUILD_FIRST_CONTRACT.md](references/BUILD_FIRST_CONTRACT.md), `dayq/data/DAYQ_SKILL_REGISTRY.json`, and the current project state. The registry is the executable routing source of truth. Route specialist skills only when their owned system enters the active playable milestone, but never bypass an applicable route.

## Mandatory route selection

Before changing the game:

1. Classify the milestone against every named registry route.
2. Run `python dayq/scripts/dayq_skill_registry.py plan --route <name>` with every applicable route. Repeat `--route` for multi-system work.
3. Read and apply every skill returned in the plan's orchestration, selected-route, and delivery-gate phases. Preserve each selected route's order. Do not substitute this orchestrator for a specialist.
4. Record the selected route names and skill IDs in the milestone work order or evidence note.
5. If no route fits, stop implementation, add the missing route and validation coverage, then continue.

`run-dayq-autopilot` owns sequencing only. Specialist skills own their domains; existing Unreal components and subsystems retain runtime authority.

## Build-first loop

1. Launch or inspect the current playable route. If it runs, continue from it instead of opening a broad audit.
2. Choose the smallest player-visible milestone that extends the route end to end.
3. Generate the registry route plan and load every selected specialist skill before implementation.
4. Implement it with existing runtime owners and project conventions. Use grayboxes, starter materials, labels, and placeholder audio freely.
5. Compile and run one focused PIE smoke route that exercises the change.
6. Fix only build failures, crashes, data loss, severe authority exploits, and defects blocking the current route.
7. Record nonblocking defects in a terse backlog and immediately build the next milestone.
8. At a coherent subsystem or integration milestone, run only the directly relevant focused automation, multiplayer, persistence, or performance checks.
9. Promote stable, mechanic-critical placeholders through the production asset factory after gameplay proves what the asset must do.

## Required gates

- Routine change: compile and one focused smoke route.
- Subsystem milestone: focused automation plus one representative PIE route.
- Integration milestone: add one two-client or save/restart route only when the changed systems touch authority or persistent state.
- Release candidate: invoke `$validate-dayq-game` for the complete validation and human-playtest program.

Never fabricate a pass. Report an unrun noncritical check as `deferred`, not `blocked`.

## Operating rules

- Do not write a large plan, evidence bundle, ledger update, or test matrix before building.
- Do not run the full suite after each edit.
- Do not stop for missing noncritical proof, art polish, optional telemetry, or deferred documentation.
- Do not require production assets to prove gameplay that a graybox can prove.
- Preserve server authority for damage, destructive actions, inventory transfer, and persistent ownership.
- Test save/restart when persistent state changes and a two-client route when authority changes.
- Stop only at a genuine external or user-authority boundary, or when no safe implementation path remains.

## Reporting

Keep updates to four facts: what changed, what is playable, the single active blocker if one exists, and what is being built next.
