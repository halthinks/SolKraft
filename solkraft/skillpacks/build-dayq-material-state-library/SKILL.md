---
name: build-dayq-material-state-library
description: Define reusable DayQ material regions and their environmental, damage, repair, rendering, and physical states.
---

# Build DayQ Material State Library

Share material physics and presentation without making every object respond identically.

Read [MATERIAL_STATE_CONTRACT.md](references/MATERIAL_STATE_CONTRACT.md) and the existing universal environmental-response contract. Inspect current material definitions, root materials, armor/ballistics interfaces, weather samples, fire, clothing, building and Unreal material ownership.

## Workflow

1. Define a material-region family by composition, manufacture, structure, thickness/density range, finish and intended use.
2. Separate authoritative physical state from client rendering parameters.
3. Define bounded response channels: wetting, absorption, drainage, drying, freeze/thaw, corrosion, rot, swelling, warping, heat/fire, electrical ingress, chemical/radiological contamination, mud/dust, abrasion, impact and ballistic damage where relevant.
4. Map responses to mass, center of mass, friction, strength, insulation, conductivity, visibility, noise, operation, repair and salvage.
5. Define transitions, hysteresis, recovery and irreversible loss. Avoid combinatorial textures by layering masks/parameters and promoting distinct geometry only when shape changes.
6. Define Blender authoring/baking rules and Unreal master-material/material-instance interfaces.
7. Preserve owners: weather supplies exposure; fire supplies heat/combustion; ballistics supplies impacts; each gameplay asset owns consequences through its material regions.
8. Create representative coupons and asset tests before broad adoption.
9. Version changes and migrate persisted material-region state.

## Completion

Deliver material definitions, response curves/thresholds, state graph, render parameters, physical outputs, authoring rules, test coupons, consumer mappings, performance budget, migrations and validation evidence.
