# Universal Environmental Response Contract

Every asset must classify: wetting, saturation, drainage, drying, freezing/thawing, corrosion, rot, swelling, warping, electrical ingress, chemical contamination, radiological contamination, mud/dust, heat/fire, and immersion. Values are `applicable`, `not-applicable`, or `unknown-needs-evidence`, each with material/geometry justification.

## Exposure sampling

Sample roof and cover fraction, enclosure/seal state, damaged openings, wind-driven rain, splash, pooling, ground contact, immersion depth, ambient temperature/humidity, sun/wind drying, contaminant deposition, cleaning, and elapsed world time. Cover attenuates exposure; it does not erase splash, ground moisture, leaks, condensation, or damaged seals.

## Material regions and state

Partition meaningful materials: absorbent textiles/wood/filter media, ferrous and nonferrous metals, coatings, polymers, glass/ceramic, electronics, lubricants/fuels, seals, and contents. Persist region wetness, absorbed water, pooled water, temperature, corrosion/rot/contamination, seal damage, and last-simulated time. Offline simulation must be bounded and deterministic.

## Derived consequences

Where physically relevant, update mass, center of mass, friction, structural strength, insulation, conductivity, noise, visibility, operation, repair steps/cost, and salvage yield/quality. Each applicable channel needs an input, response rule or curve, derived output, threshold/failure state, recovery/repair path, persistence field, and validation method.

Powered assets require ingress paths, isolation/trip behavior, short/fire risk, dry-out/cleaning/diagnosis, damaged-seal behavior, and safe restart. Absorbent assets require uptake, added mass, center-of-mass movement, drying, rot/swelling/warping, and salvage effects. A sealed asset may mark a channel not applicable only with a seal rating, damage exceptions, and test evidence.
