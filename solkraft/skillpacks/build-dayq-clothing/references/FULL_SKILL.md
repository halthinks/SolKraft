# DayQ Clothing Construction, Wear, Spawning, and Repair — Complete Handoff Prompt

## Navigation

- Authority, player purpose, taxonomy, body regions, layers, and core data contracts
- Materials, construction trees, recipes, fit, pockets, spawning, and localized condition zones
- Wear, cleaning, drying, decontamination, repair tools, repair results, and salvage
- Survival, combat, traversal, exoskeleton, mech, factions, AI, economy, UI, and multiplayer
- Persistence, Unreal production, rendering, technical spikes, prototype route, acceptance, and telemetry

## Locked implementation decision: localized garment damage

The user approved localized garment damage on 2026-07-19. Treat functionally meaningful body-region, panel, seam, closure, pocket, sole, strap, insert, seal, connector, and interface zones as authoritative garment-instance state. Damage affects only the coverage and functions that traverse the damaged zone. Simple or distant garments may replicate an aggregate projection for performance, but that projection may not replace, erase, reroll, or become authoritative over localized state. Any future proposal to return to global-only garment condition is a conceptual change requiring the user's explicit approval.

Create a production-grade DayQ clothing system skill and implementation contract covering the complete lifecycle of clothing, footwear, gloves, headwear, packs, load-bearing garments, protective clothing, armor carriers, exoskeleton underlayers, and repair tools.

Keep the work exclusively DayQ. Preserve the established canon, core loop, authoritative inventory, crafting, combat, survival, contamination, traversal, exoskeleton, multiplayer, persistence, economy, and Unreal MCP architecture. Do not create parallel item identities, inventory transactions, crafting queues, damage systems, construction ownership, save systems, journals, migrations, or sources of truth.

Name the skill:

`DAYQ_CLOTHING_CONSTRUCTION_WEAR_SPAWNING_AND_REPAIR_SKILL.md`

The skill must explain how to design, implement, balance, spawn, inspect, wear, damage, maintain, clean, decontaminate, repair, alter, craft, salvage, replicate, persist, and validate every clothing category used throughout DayQ.

## Decision authority and conceptual-change gate

The user is DayQ's decision authority.

Before implementation, identify whether the proposal merely extends accepted systems or changes how the user must think about the game. Ask the user before adopting any major conceptual shift, including:

- replacing the approved localized garment-damage model with global-only condition;
- introducing body size, fit, or gender/body-shape restrictions;
- making clothing visually modular at a level that materially changes character rendering cost;
- changing loot scarcity or regional clothing distribution;
- changing inventory capacity through physical pockets and closures;
- making laundering, drying, contamination, or temperature management a major routine;
- changing armor, movement, stealth, climbing, or exoskeleton balance;
- adding irreversible degradation or maximum-condition loss;
- changing persistence schemas, item uniqueness, or spawning authority.

For each conceptual change, report the prior assumption, proposed model, affected systems, player-facing consequences, production consequences, technical risks, evidence needed, recommendation, and a reversible alternative. Do not bury a product decision inside a data migration or implementation task.

## Player purpose

Clothing must make preparation, scavenging, identity, exposure, combat, transport, and recovery more meaningful.

Players should be able to read a survivor's likely role, environment, faction history, readiness, injuries, wealth, and recent experiences from what they wear. Clothing should create decisions without becoming constant meter maintenance.

The intended loop is:

`find or produce materials -> acquire or construct clothing -> fit and configure it -> wear it into the world -> expose it to weather, labor, contamination, and combat -> clean, dry, repair, alter, reinforce, salvage, or replace it`

## Explicit non-goals

Do not create:

- purely cosmetic clothing with no systemic attributes;
- dozens of redundant condition bars that demand constant attention;
- universal clothing sizes that ignore every fit tradeoff, unless the user explicitly chooses that abstraction;
- a repair action that restores every garment to factory condition;
- arbitrary percentage bonuses disconnected from material, construction, coverage, fit, or condition;
- generic `cloth`, `armor`, or `repair kit` resources when material differences matter;
- client-authoritative loot spawning, repair completion, item creation, pocket capacity, or condition changes;
- clothing that clips through backpacks, weapons, exoskeletons, climbing equipment, or body poses without defined compatibility handling.

## Clothing taxonomy

Support at minimum:

- base layers and underwear;
- socks, liners, and foot wraps;
- shirts, sweaters, fleeces, and insulating midlayers;
- pants, shorts, skirts, coveralls, and overalls;
- jackets, coats, rain shells, ponchos, dust garments, and cold-weather shells;
- boots, shoes, sandals, gaiters, and overshoes;
- gloves, mittens, hand wraps, and protective gauntlets;
- hats, hoods, helmets, face coverings, scarves, goggles, and veils;
- belts, suspenders, chest rigs, harnesses, armor carriers, and load-bearing vests;
- backpacks and garment-integrated pockets;
- medical, industrial, welding, firefighting, chemical, biological, radiological, electrical, aquatic, desert, alpine, and storm protective wear;
- camouflage, scout, climbing, rescue, combat, faction, ceremonial, work, prisoner, bunker, elite-enclave, and improvised clothing;
- ballistic, stab, blunt, flame, heat, cut, abrasion, chemical, particulate, radiation-contamination, and weather protection layers;
- exoskeleton-compatible underlayers, harness interfaces, cooling garments, cable routing, joint-clearance garments, and emergency-release clothing;
- mech pilot suits, pressure/respiratory support where canonically appropriate, cooling garments, crash protection, fire resistance, and cockpit-interface wear.

Classify combinations by layer, body region, volume, bulk, closure, rigidity, and compatibility instead of hardcoding every outfit.

## Body regions, layers, and coverage

Define a stable body-region map appropriate to DayQ combat, weather, animation, and rendering. Include at minimum:

- head, face, eyes, neck;
- upper torso, lower torso, back;
- shoulders, upper arms, elbows, forearms, wrists, hands;
- pelvis, hips, thighs, knees, shins/calves, ankles, feet.

Define clothing layers such as:

1. skin/base;
2. insulation/midlayer;
3. uniform/work layer;
4. weather shell;
5. load-bearing layer;
6. armor/protective layer;
7. exoskeleton or external frame interface.

Each garment must declare exact coverage by region, layer occupancy, overlap behavior, allowed underlayers/overlayers, compression, bulk, joint restriction, closure state, and conflicts.

Do not let a single global armor or insulation value hide exposed body regions.

## Garment data contract

Require every garment definition to include, where relevant:

```yaml
garment_id: stable.identifier
category: stable.tag
body_regions: []
layer: stable.tag
coverage_fraction_by_region: {}
size_profile: {}
fit_tolerance: {}
dry_mass_kg: number
packed_dimensions_cm: [x, y, z]
packed_volume_l: number
shape_class: compressible|folding|rigid|irregular|long|bulky
materials_and_panels: []
seams_and_closures: []
pockets_and_attachment_slots: []
insulation: {}
air_permeability: number
water_resistance: number
water_absorption: number
drying_rate: number
wind_resistance: number
protection: {}
contamination_behavior: {}
noise_profile: {}
visibility_and_camouflage: {}
movement_restriction: {}
snag_profile: {}
exo_mech_compatibility: []
condition_zones: []
repair_families: []
salvage_rule: stable.reference
spawn_profile: stable.reference
replication_class: aggregate|individual|unique
persistence_version: integer
```

## Material and panel contract

Represent garments as panels, reinforcements, seams, closures, inserts, and attachments made from distinct materials.

Material families may include:

- cotton, wool, linen, hemp, leather, fur, felt, and other recovered natural fibers;
- nylon, polyester, aramid, elastomer, neoprene, membrane laminates, webbing, mesh, and synthetic insulation;
- rubber, plastics, foams, adhesives, sealants, coatings, waterproofing compounds, and flame retardants;
- steel, aluminum, titanium, ceramics, composites, ballistic fibers, chain, scales, plates, buckles, snaps, zippers, eyelets, hooks, and fasteners;
- improvised materials such as tarps, feed sacks, blankets, curtains, upholstery, seat belts, inner tubes, industrial filter fabric, signage, or salvaged protective equipment.

Each material must contribute inspectable properties: mass, thickness, flexibility, tensile/tear strength, abrasion, puncture/cut resistance, thermal insulation, breathability, water behavior, burn behavior, chemical compatibility, contamination retention, noise, visibility, repairability, and salvage value.

Substitution must change behavior. A tarp rain shell, wool coat, leather jacket, aramid vest, and improvised sack garment must not be equivalent skins.

## Raw-material and clothing construction tree

Integrate the existing DayQ raw-material crafting skill.

Trace every craftable garment through:

`fiber/hide/salvage source -> cleaning and sorting -> fiber, yarn, sheet, leather, laminate, webbing, or plate -> cutting pattern -> panels -> seams and closures -> fitting -> finishing/coating -> inspection -> field use -> repair/salvage`

Support these capability bands:

- **C0 Emergency:** wraps, foot cloths, cordage ties, cut blankets, tape patches, simple ponchos.
- **C1 Handcraft:** needles, thread, awls, hand stitching, leather repair, simple pockets, buttons, laces, patches.
- **C2 Field Workshop:** cutting table, patterns, heavy sewing machine, rivets, snaps, zipper repair, webbing, waterproofing, boot repair.
- **C3 Industrial Textile:** powered sewing, knitting/weaving, controlled cutting, layered protective wear, standardized sizes, quality inspection.
- **C4 Advanced Protective Systems:** sealed suits, technical laminates, ballistic carriers, sensor/cooling integration, exoskeleton underlayers.
- **C5 Exo/Mech Apparel:** load-rated harness interfaces, active cooling garments, pilot suits, fire/crash protection, secure connectors, specialized maintenance.

Progression is based on materials, patterns/schematics, workstation capabilities, tools, power, specialists, environmental controls, and quality—not an abstract player level.

## Clothing recipe contract

Every craft, alteration, cleaning, coating, and repair process must use versioned data rather than Blueprint-local constants.

Require:

```yaml
recipe_id: stable.identifier
operation: construct|alter|resize|reinforce|clean|decontaminate|dry|repair|replace_component|salvage
target_definition_or_instance: reference
inputs: [{material_or_item, amount, minimum_grade, substitutions}]
consumables: []
tools: [{capability, minimum_condition}]
workstation_capabilities: []
specialist_requirements: []
knowledge_or_pattern: []
power_and_environment: {}
stages: [{id, duration, interruptible, intermediate_state}]
affected_zones: []
quality_formula: stable.reference
maximum_recovery_rule: stable.reference
failure_modes: []
byproducts: []
```

Mass and material conservation must hold within declared waste, contamination disposal, evaporation, or irreversible damage.

## Fit and sizing

Design a fit model that produces meaningful but manageable decisions.

At minimum, distinguish:

- too tight, fitted, compatible, loose, and severely oversized;
- length/reach compatibility for sleeves, legs, footwear, gloves, armor, harnesses, and exoskeleton interfaces;
- adjustable garments using laces, belts, straps, elastic, tailoring, padding, or cut-down panels;
- swelling, bandages, injuries, and prosthetic or exoskeleton interference where relevant.

Fit can affect insulation gaps, chafing, circulation, movement, noise, snagging, pocket access, armor seating, weapon handling, climbing, swimming, drying, and exoskeleton calibration.

Do not require granular body measurements unless playtesting proves they add better decisions than broad size bands. The skill must present broad bands and detailed sizing as alternatives and ask the user before choosing a highly granular model.

## Pocket and attachment dynamics

Integrate the existing DayQ physical inventory system rather than creating a clothing-only inventory.

Every pocket and attachment must define:

- internal volume, opening size, shape and mass rating;
- supported item/attachment tags;
- closure type and closure condition;
- immediate, quick, stowed, or secured access class;
- access posture, animation, and interruption rules;
- retention during sprinting, crawling, climbing, swimming, falling, and combat;
- noise, balance offset, bulk, snag, visibility, and contamination exposure;
- whether damage can spill, trap, soak, contaminate, or destroy contents.

A torn pocket, broken zipper, missing button, damaged sling, or overloaded seam must have observable consequences. Prevent clothing pockets from creating volume or bypassing total carried mass.

## Clothing spawning and world distribution

Design a server-authoritative spawn system for clothing instances.

Spawn profiles must consider:

- region, climate, season, elevation, settlement history, pre-collapse land use, and current faction control;
- residential, retail, hospital, industrial, military, agricultural, school, prison, emergency, bunker, elite-enclave, vehicle, body, cache, trade, and base-production sources;
- twenty-eight years of use, stripping, repair, trade, looting, contamination, fire, flooding, weather, pests, mildew, and faction modification;
- plausible garment category, size band, material, color, pattern, role, condition, cleanliness, wetness, contamination, remaining components, pocket contents, ownership/provenance, and rarity;
- container protection and local environmental exposure;
- loot-economy caps, restock or migration rules, scavenger/AI use, trade circulation, player loss, salvage, and production.

Do not spawn pristine technical clothing uniformly in arbitrary houses. High-grade sealed suits, ballistic materials, exoskeleton underlayers, and mech pilot systems must trace to credible sources, faction production, secure infrastructure, or rare maintained stock.

Define whether items are authored archetypes with procedurally generated instance state, fully handcrafted uniques, or mass-produced faction items. Use deterministic server seeds or authoritative generation so clients cannot reroll condition or contents.

Prevent loot farming through distance resets, relogging, container cycling, alt accounts, predictable timers, corpse duplication, or save rollback.

## Condition-zone model

Track damage by functionally meaningful zones rather than one global percentage when the garment warrants it.

Possible zones include:

- front/back torso panels;
- shoulders, elbows, forearms, palms, fingers;
- seat, hips, knees, shins, cuffs;
- soles, heels, toes, uppers, laces;
- hood, face seal, lenses, filter interface;
- pockets, straps, buckles, zipper, buttons, seams, lining, insulation, coating, armor pockets, plates, connectors.

Each zone may track:

- structural integrity;
- abrasion and thinning;
- cuts, punctures, tears, seam failure, delamination, deformation, and missing material;
- wetness and absorbed water mass;
- dirt, mud, blood, oil, salt, soot, biological, chemical, and radiological contamination;
- burn, melt, char, frost, corrosion, rot, mildew, and UV/weather aging;
- odor and scent where gameplay supports it;
- coating/seal condition;
- insulation loft and compression;
- closure and attachment functionality;
- permanent maximum-condition loss and repair history.

Use aggregated state for simple cloth and localized zones for protective, armored, pocketed, exo/mech, or visibly damaged garments. Define the threshold that selects each replication class.

## Wear generation

Wear must arise from observable causes:

- walking/running by terrain and footwear material;
- crawling, sliding, climbing, kneeling, vaulting, squeezing, falling, and hauling;
- backpack, armor, harness, sling, weapon, exoskeleton, and mech contact points;
- overloading pockets, straps, closures, seams, and load-bearing panels;
- rain, immersion, sweat, snow, wind, dust, heat, cold, fire, chemicals, contamination, salt, and sunlight;
- melee, ballistic impact, fragmentation, blunt force, cuts, punctures, animal attack, and structural debris;
- laundering, drying, decontamination, repair, poor storage, pests, mildew, and age;
- fit problems and repeated motion at joints.

Do not tick wear uniformly every second. Accumulate exposure and apply wear at relevant events or bounded intervals. Make causes readable through inspection, audio, animation, material changes, and performance changes.

## Functional effects of condition

Condition may affect:

- warmth, wind resistance, breathability, cooling, sweat retention, waterproofing, drying, and wet mass;
- contamination barrier, retention, shedding, decontamination efficiency, filter/closure seals, and exposure pathways;
- abrasion, cut, puncture, ballistic, blunt, flame, chemical, and electrical protection;
- pocket capacity, item retention, closure time, access, load support, and attachment security;
- camouflage, reflectivity, silhouette, noise, odor, tracks, and AI detection;
- movement restriction, chafing, stamina, grip, climbing, swimming, crawling, weapon handling, and exoskeleton fit;
- infection risk from dirty material contacting wounds;
- faction recognition, disguise credibility, reputation response, and mistaken identity where adopted.

Avoid invisible arbitrary buffs. Derive outcomes from coverage, materials, layers, fit, wetness, contamination, condition, activity, and environment.

## Cleaning, drying, and decontamination

Separate these operations:

- shaking, brushing, scraping, rinsing, washing, boiling, disinfecting, solvent cleaning, laundering, drying, smoke/heat treatment, waterproofing, and specialized decontamination;
- external contamination removal versus absorbed contamination;
- ordinary dirt and odor versus biological, chemical, or radiological hazards;
- field-expedient cleaning versus controlled workstation treatment.

Require water quality, quantity, detergent, solvent, disinfectant, adsorbent, heat, time, ventilation, protective equipment, power, and waste disposal as relevant. Poor technique may spread contamination, set stains, shrink material, strip coatings, damage fibers, corrode hardware, deform armor, or expose the operator.

Drying must depend on garment material, absorbed water, airflow, humidity, temperature, heat source, wringing/pressing, garment arrangement, and shelter. Unsafe drying can burn clothing, damage membranes, reveal the base through smoke/heat, or create fire risk.

Cleaning does not repair structural damage. Repair does not automatically clean or decontaminate.

## Repair doctrine

Support field stabilization, functional repair, component replacement, alteration, reinforcement, and workshop reconstruction.

Examples:

- tie, tape, pin, clamp, stitch, patch, darn, lace, glue, weld/melt, rivet, replace seam, replace zipper, replace button/buckle/strap, replace sole, reseal seam, restore coating, replace armor plate, replace filter seal, reline, refill insulation, or reconstruct a panel;
- emergency field repair restores limited function quickly with penalties;
- compatible patching restores coverage but may add stiffness, bulk, mass, noise, poor breathability, visible contrast, or reduced maximum condition;
- high-quality workshop repair can restore more function but cannot regenerate missing original material without replacement inputs;
- repeated repairs leave scars, provenance, altered fit, and cumulative maximum-condition loss unless a full panel/component is replaced;
- contaminated or hazardous garments may require decontamination before safe repair;
- catastrophic burn, chemical damage, delamination, plate fracture, seal destruction, or rotten fibers may make a zone non-repairable except by replacement.

Repairs should reflect actual failure. Do not repair a zipper with generic cloth or restore a shattered plate with sewing thread.

## Repair tools and consumables

Define individual tools and capabilities rather than a universal repair kit.

Include when appropriate:

- hand needles by size and shape;
- heavy needles, sailmaker needles, curved needles, and upholstery needles;
- thread, waxed thread, cord, yarn, sinew substitute, wire, and specialty high-strength thread;
- awl, stitching awl, punches, hole setters, thimble, palm guard, seam ripper, scissors, shears, knives, cutters, measuring tape, chalk, rulers, patterns, pins, clips, and clamps;
- pliers, cutters, crimpers, rivet setters, snap setters, grommet tools, buckle tools, zipper sliders/pulls/stops, button tools, and small hammers;
- adhesives, solvent, primer, patches, tape, seam sealer, waterproofing, coatings, vulcanizing materials, heat patches, and curing equipment;
- leather knives, skiving tools, punches, lasts, cobbler tools, sole presses, nails/pegs, welt materials, and boot adhesives;
- manual, treadle, portable electric, heavy-duty, walking-foot, leather, overlock, bar-tack, and industrial sewing machines;
- welding or heat-sealing tools for compatible technical textiles;
- armor-carrier, plate, helmet, visor, respirator, sealed-suit, cooling-garment, exoskeleton-interface, and mech-pilot specialized tools;
- brushes, basins, wringers, drying racks, irons/presses, steam, disinfectants, detergents, solvents, dosimeters, contamination probes, controlled ventilation, and hazardous-waste containers.

Every tool must define mass, packed size, grip requirement, condition, sharpness/calibration if relevant, supported capabilities, compatible materials, power, consumables, noise, repairability, breakage, spawn sources, crafting origin, ownership, and persistence.

Poor or improvised tools must change time, quality, injury risk, material waste, seam strength, or failure probability. They must not merely slow an identical result.

## Repair recipe and result contract

Each repair must define:

```yaml
repair_id: stable.identifier
damage_families: []
compatible_materials: []
affected_zones: []
required_tools: []
consumables_and_patch_materials: []
workstation_capabilities: []
skill_or_specialist: []
environmental_requirements: {}
cleanliness_and_decon_gate: {}
time: {}
interruptibility: {}
restored_functions: {}
unrestored_functions: {}
added_mass_bulk_noise: {}
maximum_condition_change: {}
visual_result: {}
failure_modes: []
salvage_if_failed: []
```

Make the repair result inspectable before the player commits scarce materials when appropriate.

## Salvage and cannibalization

Allow players to recover usable panels, thread, webbing, buckles, zippers, buttons, plates, padding, insulation, membranes, filters, soles, laces, harnesses, and connectors according to garment condition and tools.

Salvage must be server-authoritative, conserve mass within declared waste, preserve contamination, and destroy or transform the source atomically. Prevent repair-salvage loops that create materials or reset provenance.

## Survival integration

Connect clothing to:

- ambient temperature, wind, humidity, precipitation, immersion, activity, shelter, fire, and sleep;
- skin wetness, sweat, evaporation, heat stress, hypothermia, frostbite, sun, dehydration, and fatigue;
- wounds, bleeding access, bandages, splints, burns, infection, pain, mobility, and medical examination;
- biological, chemical, and radiological exposure by route and body-region coverage;
- food, water, fuel, and base resources required for washing, drying, heating, and decontamination.

Prefer a layered heat/moisture calculation at sensible update intervals over separate arbitrary meters for every garment.

## Combat and armor integration

Connect garments to hit location, material layers, armor inserts, penetration, blunt transfer, fragmentation, cuts, burns, fire, chemical exposure, and wound access.

Ballistic or stab protection must depend on actual coverage, angle or zone where relevant, material/plate condition, backing, fit, and layer order. Pockets and carried items may be damaged without granting implausible universal armor.

Damaged armor carriers may drop or mis-seat plates. Wet, burned, torn, contaminated, or badly fitted gear may change combat handling. Repair must not reset projectile history or magically certify a compromised protective component.

## Traversal integration

Connect clothing to climbing grip, joint motion, bulk, snagging, strap security, pocket retention, rope abrasion, harness compatibility, fall arrest, boot traction, glove dexterity, weather exposure, and vertical rescue.

Climbing garments and harnesses need rated load paths and inspectable failure. Improvised belts or damaged loops must not safely substitute for climbing harnesses without severe and explicit risk.

## Exoskeleton and mech integration

Exoskeleton underlayers must define pressure distribution, chafe protection, sweat handling, heat transfer, cable/connector clearance, joint clearance, emergency release, harness fit, sensor contact, contamination, and fire behavior.

External clothing, armor, backpacks, and pockets must declare compatibility with frame geometry and moving joints. Prevent hidden clipping and impossible equipment stacking.

Mech pilot clothing may support cooling, flame resistance, crash restraint, breathing/filtration, biometric sensing, communications, catheter/hydration systems only if the user approves their simulation depth, emergency extraction, and cockpit interfaces.

An exoskeleton or mech does not eliminate clothing heat, moisture, fit, contamination, or repair concerns; it changes them.

## Factions, history, and environmental storytelling

Every authored garment should answer:

1. What was it before the collapse?
2. How could it plausibly survive twenty-eight years?
3. Who used, repaired, traded, marked, or modified it?
4. What does its material, repair pattern, color, insignia, fit, and damage communicate?
5. What practical function does it serve now?

Support faction standards, improvised uniforms, counterfeit identity, captured clothing, clan repair styles, regional materials, cartel-successor modifications, bunker stock, elite-enclave preservation, and settlement production without making every item a lore exposition device.

Use fictionalized faction and brand identities in production content.

## AI use of clothing

AI must evaluate weather protection, armor, camouflage, role, carrying capacity, contamination, condition, faction recognition, and replacement opportunity appropriate to its intelligence and resources.

AI may wear, loot, trade, repair, discard, dry, clean, decontaminate, or reserve clothing. Do not make all AI ignore environmental protection or spawn with equipment unrelated to their role and location.

Strategic offscreen simulation must preserve garment condition, role suitability, and resource costs without simulating every stitch.

## Clothing economy

Model sources and sinks:

- scavenged stock, AI use, settlement production, faction manufacture, trade, capture, bodies, caches, and rare maintained facilities;
- wear, contamination, repair consumption, cleaning consumption, loss, theft, destruction, salvage waste, faction demand, and storage damage.

Prevent server saturation with credible wear, circulation, loss, salvage inefficiency, and specialization—not arbitrary despawning of owned garments.

Simulate availability and repair burden for solo players, small groups, organized clans, industrial settlements, exoskeleton users, and mech operations. Ensure early survival clothing is obtainable while advanced protection remains strategically meaningful.

## User interface and feedback

Provide clear layered-equipment views, body-region coverage, size/fit, pocket layout, wetness, contamination, odor if adopted, warmth, breathability, protection, movement restriction, condition zones, closures, repairability, required tools, and predicted repair outcome.

Support controller and keyboard/mouse. Avoid requiring pixel-perfect drag-and-drop. Provide inspect, compare, auto-layer, loadout, quick-access, repair-target, and contamination warnings with clear reasons for invalid actions.

World and character visuals must show meaningful wetness, mud, blood, soot, tearing, patches, missing components, burns, repaired seams, faction modifications, and armor states within performance budgets. Do not rely on color alone.

## Multiplayer authority and anti-exploit rules

The server must authorize:

- clothing instance spawning and generated condition;
- pickup, equip, unequip, layer order, fit, pocket/container transfers, and attachment;
- wear events, damage zones, wetness/contamination aggregation, and protective outcomes;
- cleaning, drying, decontamination, alteration, repair, component replacement, crafting, and salvage;
- workstation reservations, materials, tools, consumables, job timing, quality, and outputs;
- ownership, permissions, theft, corpse inventory, trade, and storage.

Test:

- two clients acquiring the same garment;
- simultaneous repair/salvage/equip operations;
- moving garments with nested pocket contents;
- damaged pocket spill during combat;
- disconnect during crafting, cleaning, repair, climbing, or exoskeleton use;
- death, corpse recovery, theft, trade, and clan storage;
- late join and relevancy transitions;
- server crash during an atomic clothing transaction;
- rollback, journal replay, schema migration, and duplicate suppression;
- client attempts to alter condition, fit, pocket capacity, armor state, or spawn seed.

## Persistence contract

Persist the minimum state required to reproduce the garment exactly:

- unique item ID when instance state requires it;
- definition ID and schema version;
- size, fit alterations, material/panel variants, color/pattern, and faction markings;
- condition by relevant zone and maximum-condition changes;
- missing/replaced panels, seams, closures, pockets, straps, inserts, plates, filters, and connectors;
- wetness, dirt, odor if adopted, and contamination types/loads;
- coating, seal, insulation, and protection state;
- pocket/container tree, contents, attachment slots, and closure state;
- repair history, patch materials, quality, provenance, owner/clan/permissions, and location;
- active crafting, cleaning, drying, alteration, or repair job references.

Use existing DayQ persistence identities, journal boundaries, crash recovery, migrations, audit rules, and conflict resolution. Every schema change needs an idempotent migration and duplication/loss tests.

## Unreal MCP implementation guidance

Before editing, inspect existing:

- item definitions, authoritative fast-array inventory, equipment slots, container tree, transaction flow, and UI;
- character body meshes, modular character system, skeletal meshes, morphs, sockets, animation, IK, cloth simulation, and LOD strategy;
- survival, weather, temperature, wetness, contamination, wound, combat, armor, traversal, exoskeleton, and mech interfaces;
- crafting, workstations, loot spawning, economy, AI loadouts, persistence, journaling, migrations, replication, tests, and technical budgets.

Prefer:

- versioned Data Assets or Data Tables for garment, material, panel, spawn, recipe, repair, tool, and compatibility definitions;
- reusable components for garment condition, wetness/contamination, pockets, protection, fit, repairability, and persistence adapters;
- gameplay tags for layers, body regions, materials, damage, contamination, slots, capabilities, and states;
- authoritative C++/server logic for valuable transactions, protection, damage, crafting, spawning, and persistence-critical state;
- material instances, masks, decals, geometry variants, or modular panels selected according to measured performance;
- bounded Chaos Cloth or equivalent simulation only where it materially improves the result and remains within platform/network budgets;
- cosmetic cloth simulation on clients while gameplay coverage and collision remain authoritative and deterministic.

Use Unreal MCP and EditorToolset to inspect and configure Actors, Components, Skeletal Meshes, Physics Assets, cloth data, materials, sockets, gameplay tags, Data Assets, Data Tables, Blueprints, properties, loot tables, test characters, and levels. Re-read modified properties.

Use Terminal for schema validators, recipe-graph analysis, deterministic spawn tests, builds, Blueprint compilation, automated tests, persistence/migration tests, network emulation, performance profiling, and packaging checks.

Do not implement runtime code when the work order is only to create the skill, design sheet, or contracts.

## Rendering and animation requirements

Define:

- modular body coverage and hidden-body-section rules;
- clipping prevention across poses, sizes, armor, backpacks, climbing, prone, swimming, exoskeletons, and mech entry/exit;
- material layers for clean, wet, muddy, bloody, dusty, sooty, burned, contaminated, repaired, and faction-modified states;
- localized damage masks or geometry swaps for tears, holes, patches, missing closures, and exposed layers;
- cloth-simulation eligibility, collision capsules, tether points, wind response, fallback animation, and LOD disable thresholds;
- first-person arms/body requirements and third-person consistency;
- character LOD, texture, material-slot, draw-call, skinning, morph, memory, and streaming budgets;
- readable state at gameplay distance without requiring cinematic rendering.

Avoid generating a separate full texture set for every combinatorial condition. Use controlled masks, shared materials, decals, overlays, palette variation, or modular components where validation supports them.

## Required technical spikes

Before large-scale content production, prove:

1. modular clothing layering across representative body types, poses, backpacks, armor, climbing gear, and exoskeletons;
2. localized damage state with acceptable replication and persistence cost;
3. wetness, contamination, and thermal aggregation at target player/AI counts;
4. deterministic server-authoritative spawning with economy caps and no reroll exploit;
5. atomic pocket/container transactions and damaged-pocket spill without duplication;
6. repair/crafting jobs across disconnect, restart, journal replay, and migration;
7. representative character crowds within animation, cloth, material, memory, draw-call, CPU, GPU, and bandwidth budgets;
8. first-person/third-person equipment consistency;
9. exoskeleton and mech compatibility without unacceptable clipping or asset multiplication.

Record the tested build, configuration, hardware/server target, player/AI count, garments per character, raw metrics, threshold, result, evidence, and design consequence. A design assertion is not technical-spike evidence.

## Prototype route

Build one narrow but complete vertical slice:

1. Spawn in poor weather with damaged ordinary clothing.
2. Inspect layer coverage, fit, pockets, wetness, contamination, and condition zones.
3. Scavenge a believable garment and repair-tool source.
4. Move items through physical pockets and a backpack.
5. Tear or abrade a specific region through traversal.
6. Become wet and contaminated through an environmental event.
7. Stabilize the garment with a field repair.
8. Return to base, clean/decontaminate and dry it using resources.
9. Replace or reconstruct the damaged zone at a workstation.
10. Observe changed mass, fit, warmth, noise, protection, appearance, and maximum condition.
11. Use the repaired garment while climbing and with an early exoskeleton.
12. Save, restart, reconnect, and verify every persistent state and pocket content.
13. Repeat with a protective garment that cannot safely be restored by ordinary sewing.

## Acceptance gates

Reject the implementation unless all applicable gates pass:

1. Every garment has valid materials, coverage, layers, mass, packed dimensions, volume, fit, pockets, condition, repair, spawn, and persistence rules.
2. Clothing effects derive from material, coverage, layering, fit, wetness, contamination, and condition rather than arbitrary bonuses.
3. Spawn locations and condition are historically and environmentally plausible.
4. Loot generation is authoritative and cannot be rerolled or duplicated.
5. Wear has observable causes and does not become constant background decay.
6. Damage to a region changes only relevant functions and visuals.
7. Cleaning, decontamination, drying, repair, and replacement remain distinct operations.
8. Repair inputs and tools match the damage and materials.
9. Repair and salvage conserve material and cannot generate value loops.
10. Pockets obey physical capacity, opening, access, load, closure, and damage rules.
11. Movement, climbing, combat, stealth, survival, and exoskeleton integration respond coherently.
12. Multiplayer clients observe the same authoritative clothing, pocket, protection, and repair state.
13. Save/load, journal replay, crash recovery, and migrations reproduce every material persistent state without duplication or loss.
14. AI uses clothing appropriate to weather, role, faction, and resources.
15. UI communicates decisions without turning clothing care into opaque chores.
16. Representative worst cases meet client, server, memory, rendering, animation, cloth, save, and bandwidth budgets.
17. The user has approved every conceptual change identified by the gate.

## Telemetry

Instrument:

- garment acquisition, equip, discard, trade, theft, loss, and salvage;
- time spent managing clothing and inventory;
- exposure, wetness, contamination, damage, repair, cleaning, and drying frequency;
- causes of garment failure and player injury/death related to clothing;
- repair-tool and material scarcity;
- pocket use, access failures, overloads, spills, and lost items;
- clothing-family usage, ignored items, dominant combinations, and faction/region distribution;
- exoskeleton/mech compatibility failures;
- server transaction failures, persistence mismatches, migration failures, and suspected duplication;
- performance cost by garment complexity and character density.

Define thresholds for identifying chore behavior, useless categories, dominant protection stacks, impossible scarcity, saturation, and technical-budget failures.

## Required deliverables

Produce:

1. the complete DayQ clothing skill;
2. a system decision sheet following the DayQ system-sheet contract;
3. garment, material, panel, pocket, spawn, condition-zone, recipe, repair, repair-tool, and persistence data contracts;
4. clothing construction and repair progression trees;
5. spawn-source and loot-distribution rules;
6. body-region, layer, coverage, fit, pocket, and compatibility matrices;
7. wear, wetness, contamination, protection, and repair formulas or curve definitions with provisional values clearly labeled;
8. cross-system dependency and ownership map;
9. exploit and mitigation register;
10. Unreal MCP implementation plan that reconciles with existing systems;
11. migration and crash-recovery plan;
12. technical-spike plan with measurable pass/fail gates;
13. PIE and automated validation plan;
14. unresolved evidence list;
15. conceptual changes requiring the user's decision;
16. final acceptance report template.

## Completion report

Report:

- request and scope;
- existing systems inspected and their owners;
- locked decisions and provisional assumptions;
- conceptual changes presented to and decided by the user;
- contracts and progression trees created;
- gameplay, survival, combat, inventory, crafting, traversal, exoskeleton, mech, AI, faction, economy, multiplayer, persistence, and Unreal dependencies;
- files/assets/data/tests created or proposed;
- migrations required;
- technical-spike evidence;
- tests run and evidence captured;
- failures and repairs;
- unresolved questions and risks;
- no-skip ledger additions or explicit not-applicable evidence;
- final acceptance status.

Do not declare completion because the document is detailed, a garment renders correctly, a Blueprint compiles, or a test passes in an empty map. Completion requires accepted rules, integration with existing system ownership, representative gameplay evidence, authoritative multiplayer behavior, persistent recovery, performance evidence, and the user's approval of conceptual changes.
