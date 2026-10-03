---
name: simulate-dayq-fire-campcraft
description: Implement DayQ fire, heat, smoke, cooking, drying, campcraft, and suppression gameplay.
---

# Simulate DayQ Fire and Campcraft

Read [FULL_CONTRACT.md](references/FULL_CONTRACT.md) and [INTEGRATION.md](references/INTEGRATION.md) completely. Extend existing inventory, crafting, building, health, survival, weather, AI, damage, authority, persistence, economy, and asset owners; never duplicate them.

## Workflow

1. Classify ignition, fuel/material regions, geometry, enclosure/airflow, exposure, heat/smoke/toxic outputs, spread candidates, suppression, construction, ownership, offline rules, and evidence.
2. Use server-owned physically motivated bounded state. Client Niagara/audio/materials are presentation, never fire truth.
3. Connect heat to body-region/clothing exposure, cooking/boiling/drying/processes, sensors/AI, structures, utilities, and sleep interruption through explicit adapters.
4. Reserve and conserve physical fuel, tools, extinguishers, water, outputs, byproducts, repairs, and salvage through existing transactions.
5. Implement through `$dayq-unreal-mcp-production-validation`; run dry/wet/weather/enclosure/spread/suppression/two-client/restart/offline/density routes.
6. Apply the GameDevBench loop and leave every unproven live gate open in the no-skip ledger.

Ask before changing survival cadence, persistent/offline fire destruction, anti-grief/raid rules, scientific fidelity, performance budgets, or existing system ownership.
