---
name: build-dayq-glentech-fabrication
description: Implement DayQ Glentech printers, foundries, PCB cells, manufacturing progression, and machine qualification.
---

# Build DayQ Glentech Fabrication

Read [the Glentech fabrication contract](references/GLENTECH_FABRICATION_CONTRACT.md) before acting.

## Workflow

1. Inspect existing crafting, item, building, power, fire, inventory/load, worker, agent, economy, and persistence owners.
2. Resolve the required R, P, G, and M levels independently; a displayed tier never substitutes for installed capabilities and condition.
3. Build machines physically by upgrading the serialized current cell or building/recovering a visibly newer model. Take the machine offline, install components, calibrate, produce qualification coupons, inspect, and sign the new capability record.
4. Gate every recipe by process modules, material form/grade, size, precision, post-processes, inspections, recovered seed components, power, and cooling.
5. Keep the R1 forge concise. Track only station-level operational state; do not turn furnace internals into an engineering minigame.
6. Treat Thermal-Gradient Jet Deposition as fictional, power/cooling/material/inspection constrained, and non-actionable in real-world detail.
7. Preserve jobs, reservations, lots, machine identities, upgrades, wear, calibration, qualifications, outputs, and failures through authority, restart, rollback, migration, and crash recovery.
8. Require schema/graph/conservation tests, asset-factory jobs, Unreal automation, PIE/multiplayer routes, performance, and visible evidence.
