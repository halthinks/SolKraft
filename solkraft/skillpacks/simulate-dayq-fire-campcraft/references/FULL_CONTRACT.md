# Fire, Heat, Combustion, and Campcraft Contract

## Experience and taxonomy

Fire supplies warmth, cooking, boiling, drying, light, signals, concealment tradeoffs, industry, sabotage, defense, hazards, firefighting, smoke exposure, and persistent consequences. It is not a Niagara loop with a fuel timer. Support physical ignition sources; solid/liquid/gas/electrical/battery/chemical fuels; campfires, stoves, hearths, ovens, forges, kilns, boilers, generators, vehicles, electrical systems, buildings, vegetation, and industrial hazards; and portable/placeable/constructed/installed/damaged/improvised/faction variants.

## Authoritative state

Each stable fire has state (`unlit`, `igniting`, `smoldering`, `flaming`, `fully_involved`, `starved`, `suppressed`, `extinguished`, `cooling`), fuel components and available mass, surface/arrangement, moisture, oxygen/ventilation, heat release and temperature, ember energy, smoke/toxic products, light, wind/enclosure, spread candidates, revision, and last simulated time. Values use units and versioned provisional curves rather than invented precision.

Ignition accounts for energy/duration, tinder, fuel geometry/volatility/moisture/temperature, airflow, shelter, altitude, precipitation, immersion, contamination, preparation, and consumable loss. Sustained burning requires a credible fuel bed. Adding/removing/splitting/rearranging/drying/smothering/overloading are atomic server actions.

## Heat, smoke, spread, and damage

Heat integrates ambient conditions, distance/orientation, shielding, enclosure, convection/radiation abstractions, clothing regions/wetness/insulation, wounds, fatigue, activity, hypothermia/frostbite/heat/dehydration/burn/smoke outcomes, cooking/boiling/sterilization/drying/thawing/workshops, and thermal signatures. No universal circular buff.

Smoke distinguishes visible soot from carbon monoxide, oxygen depletion, irritants, and material-specific toxic products. Model buoyancy, wind, accumulation, ventilation, openings/shafts, coughing, vision, incapacitation, residue, alarms, concealment, AI, and sensors with bounded cells/portals or strategic aggregation.

Spread uses material regions, separation, flux/contact/embers/wind/openings/coatings/wetness/resistance and can reach surfaces, cavities, ducts, vegetation, stored resources, ammunition, batteries, and cables. Structural weakening/collapse, debris, blocked routes, utilities, salvage loss, firebreaks, compartments, doors/shutters/sprinklers and suppression are server-owned. Offline simulation is deterministic, capped, journaled, and cannot erase bases from numerical instability; raid/offline/anti-grief rules remain authoritative elsewhere.

## Campcraft and suppression

Support emergency, concealed/low-signature, wet-weather, reflector, cooking, shelter-heater, permanent hearth/chimney, forge/kiln/oven, industrial, and containment families. Each declares inputs, tools, placement/terrain/ventilation/cover, stages, sound/light/smoke/heat, operation, failure, repair, salvage, ownership, and persistence.

Support water, sand/soil, blankets/lids, extinguishers, foam, dry chemical, isolation/shutoff, electrical isolation, firebreaks, ventilation, alarms, and specialist systems. Method/fuel mismatch can spread liquid fire, create steam injury, preserve electrical risk, or release hazards; keep real-world hazardous instructions abstract.

## Unreal, authority, persistence, and scale

Evaluate Niagara, Chaos, material parameters, MetaSounds/audio, GAS effects, environmental queries, world partition, data-driven material/fuel definitions, significance, pooling, and server strategic simulation. Never replicate particles. Server owns ignition, transitions, spread, damage, resources, construction, permissions, repair, salvage, journal, offline catch-up, and conflict resolution. Test concurrent fuel/suppression/sabotage, disconnect/restart/crash/migration/rollback, world streaming, safe-zone/raid rules, dense bases, and wildfire budgets.

## Acceptance route

Test dry/wet ignition, wind/rain, cooking/boiling, clothing/fuel drying, enclosed smoke/ventilation, burns/exposure, structure/vegetation spread, correct/incorrect suppression, AI light/smoke/heat/sound perception, two clients, sabotage, restart/offline catch-up, dense performance, and infinite-fuel/duplicate-salvage/logout/safe-zone exploits. Capture build/configuration, units, logs, visual evidence, state/network/persistence/performance, defects, repairs, reruns, and regressions. Status remains `testing` until live evidence passes.
