---
name: design-dayq-game-ordnance
description: Design DayQ ordnance and explosive gameplay as safe game abstractions, without real construction instructions.
---

# Design DayQ Game Ordnance

Read [ORDNANCE_CONTRACT.md](references/ORDNANCE_CONTRACT.md) and the package `DAYQ_GAME_ORDNANCE_CATALOG.json` before adding an item or recipe.

1. Classify the request as military salvage, launcher ammunition, signaling/obscuration, breaching, demolition, area denial, vehicle/drone payload, distraction, training, or disposal. Distinguish found service ordnance from fictional player-assembled DayQ devices.
2. Keep crafting non-operational. Use abstract root-component classes, quality grades, station capability, specialist/agent skill, risk, time, power, reliability, concealment, transport load, and salvage sinks. Never provide real chemical identities in combination, ratios, dimensions, circuitry, timing, pressure, or procedural assembly.
3. Make the gameplay causal: payload class, delivery method, arming state, safety state, fuse behavior as a game parameter, blast/fragment/heat/smoke/flash/noise/electronic effects, cover/material response, failure modes, dud state, disposal, weather response, signature, legality/rarity, and consequences.
4. Route real-world military items as scarce found/captured stock with deterioration, provenance, compatibility, and safe/unsafe-to-use inspection states. Crafting restores or packages only through fictionalized jobs; it does not teach real reconditioning.
5. Route improvised items through a bounded progression tree: distraction and signals; smoke and area denial; low-tier breaching; directional defense; vehicle/drone payloads; clan demolition; agent-assisted precision systems. Unlock capability, reliability, and control--not real-world construction knowledge.
6. Preserve owners: inventory owns stable item/lot identities; crafting owns reservation and conservation; combat owns damage/wounds; construction owns structural effects; vehicles/drones/exos own mounts; acoustics owns sound events; AI owns perception; server authority and persistence own state. Extend through adapters.
7. Model multiplayer abuse resistance: server-owned placement/arming/trigger/detonation, range/LOS checks, duplicate-request rejection, ownership/permissions, disconnect, late join, raid-window policy, persistence, restart, crash recovery, rollback, tombstones, rate limits, and audit trails.
8. Validate in isolated ranges and representative raids: safe handling states, readable threat/counterplay, occlusion/cover, material response, fragmentation abstraction, fire/smoke/weather, AI hearing, two clients under latency/loss, restart/dud recovery, performance at worst-case density, accessibility, and clear non-operational UI.
9. Report the exact catalog delta, abstract recipe, progression dependencies, asset jobs, runtime owners, test evidence, remaining hazards, and acceptance status. Never treat effects or a successful detonation as proof of authority, fairness, persistence, or performance.
