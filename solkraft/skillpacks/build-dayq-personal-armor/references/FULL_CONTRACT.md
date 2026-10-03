# DayQ Ballistic Armor, Shields, Layered Panels, and Uparmoring — Complete Handoff Prompt

Continue the existing DayQ design and implementation with a complete, data-driven ballistic protection production system.

This is a prompt and handoff for the primary DayQ task. Do not implement this skill in the source handoff workspace. Do not assume filesystem locations. Inspect the current DayQ workspace and use its established project-relative conventions.

Keep this work DayQ-only. Do not include, modify, merge, delete, or repurpose the separate wave-surfing project.

# User-locked intent

The user has directed that ballistic shields, wearable armor, armor panels, vehicle uparmoring, drone protection, exoskeleton armor, mech armor, base armor, and layered composite protection have a complete build tree.

The tree must begin with desperate improvised materials and progress through recovered industrial and advanced clan manufacturing. It must include, where appropriate:

- books and magazines bundled or taped into crude shields and inserts;
- duct tape, straps, cloth, boards, scrap, and improvised backing;
- salvaged building insulation and other real-world glass-fiber sources;
- recovered resin, adhesives, binders, epoxies, hardeners, fillers, and compatible chemistry;
- steel and other metal plate recovery, cutting, forming, pressing, heat-treatment abstraction, joining, and mounting;
- broken toilets, sinks, tiles, electrical porcelain, and other ceramic feedstock;
- ceramic fragment, tile, mosaic, cellular, honeycomb-like, or pressed composite concepts where the production capability supports them;
- backing, confinement, fiber layers, adhesive layers, spacers, liners, catches, edge protection, and protective covers;
- interchangeable and permanent armor layers;
- handheld shields;
- wearable plate carriers and modular armor;
- vehicle, drone, robotic, exoskeleton, mech, structure, turret, and bunker uparmoring;
- one-, two-, three-, or greater-layer assemblies when the carrier and mount can support them;
- higher total protection from high-quality ceramic, fiberglass, and resin systems without making layer count the only performance variable;
- explicit carrier strength, mount, payload, center-of-mass, mobility, power, heat, handling, endurance, flight, climbing, suspension, structure, and repair consequences.

These requirements are locked. Present any further conceptual change to the user before adoption.

# Required new skills

Create and integrate these five coordinated native DayQ skills:

1. `DAYQ_ARMOR_MATERIALS_AND_PANEL_MANUFACTURING_SKILL`
   - native folder: `manufacture-dayq-armor-panels`
2. `DAYQ_BALLISTIC_ARMOR_RESPONSE_DAMAGE_AND_CERTIFICATION_SKILL`
   - native folder: `validate-dayq-ballistic-armor`
3. `DAYQ_PERSONAL_ARMOR_AND_BALLISTIC_SHIELDS_SKILL`
   - native folder: `build-dayq-personal-armor`
4. `DAYQ_VEHICLE_DRONE_ROBOT_AND_BASE_UPARMORING_SKILL`
   - native folder: `uparmor-dayq-platforms`
5. `DAYQ_EXOSKELETON_AND_MECH_ARMOR_INTEGRATION_SKILL`
   - native folder: `armor-dayq-exos-and-mechs`

Every skill must contain:

- `SKILL.md` with valid YAML frontmatter containing only `name` and `description`;
- `agents/openai.yaml` with matching display metadata and a default prompt that explicitly names its native `$skill-name`;
- directly linked references for its full contracts and test matrix;
- scripts only where deterministic graph, mass, assembly, fixture, or evidence validation benefits from them;
- an explicit dependency and ownership map;
- multiplayer, persistence, migration, exploit, performance, and Unreal MCP requirements;
- no auxiliary README or installation document inside the native skill folder.

## Skill 1 ownership — materials and panel manufacturing

Own:

- material sourcing, grading, contamination, provenance, and lot identity;
- book/paper, tape, timber, cloth, rubber, scrap metal, glass fiber, resin, ceramic, porcelain, steel, advanced fiber, and hybrid-material routes;
- preprocessing, intermediate materials, layer production, panel assembly, workstations, recipes, quality, waste, repair inputs, salvage, economy, and progression;
- manufacturing validation, graph validation, material/mass balance, and batch evidence.

Do not own projectile simulation, wounds, carrier movement, vehicle physics, exo movement, mech assembly, or final hit authority.

## Skill 2 ownership — ballistic response, damage, and certification

Own:

- vendor-neutral ballistics-backend adapter requirements;
- virtual threat definitions;
- layer interaction and ordered-stack evaluation;
- impact, stop, continuation, penetration, ricochet handoff, deformation, fragment/spall, mount transfer, and retained-threat state;
- spatial panel damage, cracks, delamination, edge damage, prior-hit behavior, multi-hit behavior, environment conditioning, inspection confidence, qualification, rejection, and requalification;
- deterministic fixtures, comparative evidence, debug output, and server-authoritative impact resolution.

Do not own ammunition inventory mutation, firearm action state, wounds, vehicle/exo/mech component truth, or vendor-plugin adoption. Consume their approved interfaces.

## Skill 3 ownership — personal armor and shields

Own:

- wearable carriers, plates, soft/backing layers, coverage, fit, gaps, overlap, comfort, heat, medical access, mobility and physical-inventory integration;
- improvised book/magazine/tape inserts and shields;
- one-hand, two-hand, braced, team, sling, and exo-assisted shield operation;
- shield geometry, viewports, grips, balance, fatigue, weapon readiness, stance, climbing, door, ladder, casualty, and backpack interactions;
- wearable/shield installation, field inspection, replacement, repair, drop, theft, and persistence.

Do not own the common material recipes or ballistic solver. Reference Skills 1 and 2.

## Skill 4 ownership — platform and base uparmoring

Own:

- vehicle, drone, ground robot, turret, gate, firing position, workshop, utility room, communications room, and bunker armor mounts;
- platform-specific mass, payload, suspension, braking, acceleration, steering, rollover, flight, thrust, endurance, center of gravity, sensor, cooling, hinge, access, ventilation, structure, foundation, and collapse consequences;
- platform zone coverage, mounting, replacement, repair access, logistics, salvage, breach, capture, and raid counterplay;
- authoritative configuration and performance integration.

Do not own general vehicle/drone/building physics. Extend their existing owners through armor configuration and load adapters.

## Skill 5 ownership — exoskeleton and mech armor

Own:

- exo and mech armor zones, hardpoints, layer envelopes, joint/actuator guards, shields, cockpit/harness protection, power/controller/cooling/sensor protection, and modular arrays;
- supported load, joint torque, static/dynamic load, inertia, balance, power, heat, noise, silhouette, climbing, evasive movement, ground pressure, cooling, transport, repair-bay, and crane consequences;
- early recovered exo armor through clan-manufactured two-/three-layer composites and strategic mech armor;
- assembly validation and readable counterplay without replacing exo/mech movement or damage ownership.

Do not own common material recipes or ballistic response. Reference Skills 1 and 2 and compose with the existing exoskeleton and mech skills.

## Shared boundary rule

Definitions may be shared through versioned schemas, but authoritative state must have one owner. No skill may duplicate another skill’s material lots, armor panel identity, hit result, carrier configuration, inventory transaction, movement state, damage state, journal, or migration.

Together, the five descriptions must trigger for ballistic armor, shields, plate carriers, armor inserts, layered panels, ceramic armor, fiberglass/resin composites, steel plate, improvised armor, vehicle uparmoring, drone/robot/base armor, exoskeleton armor, mech armor, spall liners, armor repair, armor testing, and Unreal integration.

# Existing DayQ owners to extend, never replace

Inspect and map these systems before creating armor data or implementation:

- authoritative inventory and persistent item identity;
- physical mass, dimensions, volume, shape, typed slots, backpacks, containers, load distribution, supported/unsupported load, bulk, snag, and hand occupancy;
- raw-material lots, provenance, grade, contamination, processing, recipes, workstations, tools, specialists, production queues, quality, repair, and salvage;
- economy, scarcity, source/sink balance, progression, faction trade, and contested industry;
- equipment, clothing, plate carriers, attachment points, character movement, stamina, injury, and animation;
- combat, firearm, projectile, material interaction, penetration, ricochet, damage, wounds, suppression, and acoustic events;
- the separate `DAYQ_UNREAL_LIBRARY_EVALUATION_AND_ADOPTION_SKILL` and vendor-neutral ballistics-backend decision;
- vehicles, suspension, handling, cargo, engine load, braking, doors, windows, and component damage;
- drones, lift, propulsion, payload, balance, power, endurance, sensors, and flight authority;
- exoskeleton frames, supported load, joint limits, power, heat, hardpoints, movement, climbing, combat, and failure;
- mech chassis, structural load paths, center of mass, locomotion, power, cooling, hardpoints, damage zones, logistics, and maintenance;
- building pieces, structural support, turrets, gates, walls, bunkers, raid/breach rules, and repair-under-fire policy;
- clans, ownership, permissions, theft, capture, sabotage, work orders, and certification authority;
- multiplayer authority, relevancy, replication, persistence, journaling, rollback, crash recovery, and schema migrations;
- Unreal MCP, Terminal, EditorToolset, PIE, dedicated-server, automation, profiling, and evidence capture;
- DayQ systemic asset generation, web-reference baseline reconstruction, Blender MCP production, and Unreal promotion.

Do not create a second health, damage, inventory, armor-hit, material, crafting, vehicle, exo, mech, construction, or persistence source of truth. Add definitions and adapters to established owners.

# Safety, publishing, and abstraction boundary

This is a game-system specification, not real-world armor fabrication or testing instruction.

Do not provide actionable real-world:

- armor recipes;
- material ratios;
- laminate schedules;
- panel thicknesses;
- pressing forces;
- cure temperatures or times;
- kiln or heat-treatment schedules;
- metallurgy procedures;
- chemical processing instructions;
- ammunition selection for real testing;
- firing distances;
- shot placement patterns;
- pass/fail claims for improvised armor;
- statements that an improvised item makes a person safe.

Represent manufacturing through fictionalized capability tags, versioned game recipes, abstract processing bands, quality formulas, and in-engine ballistic fixtures.

Never market a DayQ recipe as protective advice. Never label improvised armor with real certification. Use fictional DayQ test classes and clearly distinguish them from current real-world standards.

Use current official armor standards only to inform the need for controlled threat definitions, conditioning, repeatable laboratory practices, perforation and deformation measurements, multi-hit behavior, and certification discipline. Do not reproduce restricted test details.

# Player purpose and intended feeling

Armor must create these experiences:

- desperate improvisation can be better than nothing, but is bulky, inconsistent, fragile, and uncertain;
- scavenging ordinary ruins can reveal valuable material feedstocks rather than generic “armor scrap”;
- workshop growth visibly improves repeatability, weight efficiency, coverage, repair, and confidence;
- armor protects only the zones it covers;
- every kilogram and layer has a carrier consequence;
- a shield changes movement, weapon readiness, field of view, noise, fatigue, and teamwork;
- vehicles, drones, exoskeletons, and mechs can be specialized through uparmoring rather than receiving a flat armor stat;
- high-tier composite armor is powerful because of controlled materials, layer interaction, manufacturing quality, mounting, and inspection—not because it has a fantasy label;
- damage, delamination, cracking, corrosion, water ingress, fire exposure, and prior hits matter;
- an armor shop, press, composite room, ceramic facility, inspection bay, and test lab are strategic clan infrastructure worth raiding and defending.

# Explicit non-goals

- no universal armor points detached from physical zones;
- no automatic protection from carrying armor in a backpack;
- no unlimited stacking;
- no linear “three layers equals three times protection” rule;
- no protection determined only by material name;
- no cosmetic-only uparmoring;
- no weightless vehicle or exo armor;
- no paper shield defeating every firearm because it is thick;
- no broken toilet magically becoming high-performance ceramic armor;
- no scavenged insulation magically becoming structural fiberglass without processing;
- no client-authoritative hit, penetration, armor damage, installation, repair, or production result;
- no vendor ballistics-plugin types in DayQ persistent armor data.

# Armor architecture

Treat armor as a physical assembly attached to a carrier and covering one or more spatial zones.

An assembly may contain:

- outer cover or weather skin;
- strike face;
- fragmenting or sacrificial layer;
- confinement layer;
- spacer or stand-off layer;
- reinforcement layer;
- fiber/composite backing;
- energy-absorbing layer;
- fragment/spall catch layer;
- comfort/trauma interface;
- edge protection;
- mounting frame;
- fasteners, straps, hinges, brackets, rails, bolts, adhesive bonds, or clamps;
- replaceable tiles or modules;
- inspection markers and serial identity.

The role of each layer must be data-defined. A material can perform differently as a strike face, backing, spacer, liner, or structural mount.

Armor performance must derive from:

- threat class and impact state supplied through the vendor-neutral ballistics boundary;
- impact location and angle;
- covered area and gaps;
- layer order;
- material family, grade, density, toughness, hardness abstraction, stiffness, brittleness, fiber quality, and bond quality;
- total areal mass and thickness envelope;
- backing/support condition;
- edge distance and panel geometry abstraction;
- mount rigidity or compliance;
- temperature, moisture, chemical, UV, corrosion, and fire exposure where relevant;
- age, manufacturing quality, inspection state, delamination, cracks, prior hits, and repairs;
- separation/spacing where present;
- carrier movement and panel orientation;
- multi-hit location and damage field.

Do not collapse this into a single hidden random roll. Expose understandable causes through inspection and after-action evidence.

# Material and production tree

## T0 — Desperate improvised protection

Support:

- books and magazines;
- paper bundles;
- cardboard and packaging;
- duct tape and other tape classes;
- cloth wraps;
- backpacks or improvised carriers;
- plywood, boards, doors, tabletops, and furniture panels;
- scrap sheet metal;
- appliance panels;
- rubber layers;
- improvised straps and handles;
- mixed-material barricade panels.

Books/magazines must vary by size, paper density, moisture, compression, orientation, binding, and condition. Tape holds an assembly together but does not become a magical ballistic material.

These builds are heavy and bulky for their protection, poor in rain, inconsistent between lots, difficult to inspect, likely to obstruct movement and view, and vulnerable to repeated impacts and edge failure.

Allow them as:

- emergency shield cores;
- inserts against low-energy fragments or approved low-tier threats;
- door/barricade reinforcement;
- vehicle interior packing;
- temporary backing or spacing;
- environmental storytelling and early survival experimentation.

Do not promise real-life protection.

## T1 — Field workshop laminates and scrap armor

Support:

- sorted cloth and webbing;
- canvas;
- tire or belt reinforcement;
- recovered polymer sheets;
- low-grade glass fiber from compatible sources;
- scavenged building insulation after contamination-aware processing abstraction;
- recovered resin/adhesive systems;
- timber laminates;
- corrugated and formed sheet;
- improved steel scrap;
- basic backing and spall liners;
- riveted, bolted, clamped, strapped, and bonded assemblies;
- basic shield frames and carriers.

Building insulation may be dirty, wet, degraded, biologically contaminated, chemically contaminated, or composed of fibers unsuitable for structural reinforcement. Require sorting, cleaning/quarantine, compatible-fiber classification, mat/preform preparation abstraction, resin compatibility, compression/cure capability, and quality inspection.

Recovered resin and adhesive lots must track family, age, contamination, storage history, compatibility, cure reliability abstraction, temperature/moisture sensitivity, toxicity hazard class, and bond quality.

## T2 — Industrial recovered armor

Support:

- graded steel plate;
- recovered armor plate where legitimately found;
- structural, tool, spring, stainless, and unknown steel classes with different behavior;
- cutting and forming capability;
- plate curvature and geometry abstraction;
- edge finishing;
- controlled joining and mounting;
- industrial glass-fiber laminates;
- reliable resin systems;
- layered steel/composite assemblies;
- ceramic tile mosaics;
- porcelain fragment/aggregate composites;
- improved spall liners;
- vehicle and exo mount frames;
- repairable modular panels.

Steel grade, provenance, corrosion, heat history, weld/edge damage abstraction, forming damage, thickness band, hardness/toughness balance, and quality must matter. More steel creates mass, inertia, center-of-mass, suspension, hinge, joint, braking, and mobility consequences.

## T2 porcelain and sanitary-ceramic route

Broken toilets, sinks, tiles, electrical porcelain, laboratory ceramics, and industrial ceramic scrap may enter a feedstock route.

Track:

- ceramic family;
- glaze and foreign material;
- cracks and weathering;
- contamination;
- fragment size distribution abstraction;
- sorting confidence;
- crush/grade state;
- compatible binder and backing;
- tile, mosaic, aggregate, cellular-fill, or other approved geometry;
- voids, bond quality, edge confinement, and backing quality;
- damage and multi-hit behavior.

A smashed toilet does not automatically create a honeycomb. It may supply graded ceramic pieces or feedstock for a mosaic or composite. A true cellular/honeycomb backing requires a separate core-forming or recovered-core production capability. High-performance armor ceramics require later controlled manufacturing.

Porcelain-based armor may be brittle, variable, heavy for its protection, sensitive to assembly quality, and poor under repeated nearby hits. It can still be a meaningful middle-tier path when paired with suitable backing and confinement.

## T3 — Precision composite and formed-armor manufacturing

Support:

- controlled glass-fiber cloth/mat production or reliable recovered stock;
- compatible high-quality resin systems;
- vacuum/pressure-assisted processing abstraction without real parameters;
- controlled curing environment abstraction;
- shaped composite shells;
- advanced fiber backings from recovered or manufactured sources;
- formed and treated metal armor families;
- purpose-made ceramic tiles or plates;
- controlled ceramic pressing/firing abstraction;
- cellular/honeycomb cores;
- graded backing systems;
- replaceable strike-face modules;
- environmental sealing;
- nondestructive inspection abstraction;
- batch qualification and serial identity.

This tier should produce reliable two- and three-layer armor assemblies for combat exoskeletons, vehicles, robots, shields, and high-value base positions.

## T4 — Secure robotics and advanced armor systems

Support:

- high-quality engineered ceramics;
- advanced fiber composites;
- hybrid metal/ceramic/composite modules;
- spaced and reactive-looking systems only if implemented as safe original fiction and balanced against actual DayQ threats;
- sensor-integrated armor-health monitoring;
- modular damage-isolation zones;
- drone/light-robot weight-efficient armor;
- exoskeleton articulation protection;
- vehicle crew-capsule concepts;
- armor protecting power, cooling, communications, trusted controllers, and suppression equipment;
- recovered enclave/bunker manufacturing data and secure material standards.

## T5 — Mech and strategic armor industry

Support:

- large modular arrays;
- replaceable outer tiles;
- structural armor;
- internal liners;
- spaced modules;
- joint and actuator guards;
- cockpit/capsule armor;
- power, ammunition, cooling, sensor, and control-zone protection;
- field-replaceable panels;
- transport racks, cranes, presses, composite rooms, ceramic production, inspection cells, and repair bays;
- multiple viable weight/protection doctrines.

Mech armor remains constrained by chassis rating, joint torque, ground pressure, locomotion, power, heat, recoil paths, cooling airflow, sensor visibility, transport envelope, and repair logistics.

# Armor layer model

Every armor assembly must declare:

- minimum and maximum layer count permitted by its design;
- layer slot types;
- total thickness envelope;
- areal mass;
- total mass;
- curvature/shape envelope;
- coverage polygon or zone map;
- edge and overlap behavior;
- compatible backing/support;
- mount family;
- mount static and dynamic load;
- center-of-mass offset;
- flex/rigidity class;
- environmental seal;
- inspection access;
- replaceability;
- threat-response curves;
- multi-hit damage field;
- repairability;
- salvage rule.

Layer count is not independently authoritative. The assembly validator must reject stacks that exceed:

- carrier mass budget;
- mount rating;
- thickness/envelope;
- joint or hinge load;
- mobility clearance;
- weapon/tool clearance;
- sensor field;
- cooling/airflow requirements;
- structural support;
- power or propulsion reserve;
- balance/center-of-mass envelope;
- approved material compatibility;
- production/certification limits.

Two top-tier layers can outperform three poor layers. Three top-tier layers can improve protection only when their functions complement one another and the carrier can bear the complete assembly. Adjacent redundant brittle layers may perform worse than a properly ordered strike-face/backing/liner stack.

# Carrier-specific integration

## Human wearable armor

Model:

- plate carrier or garment compatibility;
- front, rear, side, shoulder, neck, groin, limb, and optional zones;
- gaps and overlap;
- body size and fit;
- supported and unsupported mass;
- load distribution;
- heat and ventilation;
- prone, crouch, vault, climb, swim, squeeze, vehicle-seat, and medical-access effects;
- backpack/weapon interference;
- plate access and replacement;
- blunt/deformation injury through existing wound systems;
- spall/fragment effects;
- audible rattle;
- water absorption and contamination;
- quick removal and casualty treatment.

## Handheld shields

Model:

- shield size, geometry, and coverage;
- mass and center of mass;
- one-hand, two-hand, sling, brace, team, or exo-assisted grip;
- view port and sensor integration;
- weapon-use compatibility;
- stance and movement;
- fatigue and arm injury;
- recoil/impact transfer;
- edge exposure;
- ground brace or deployable mode;
- carried/stowed slot;
- door, ladder, rope, climbing, healing, and inventory interaction;
- drop, capture, repair, and panel replacement.

Improvised book shields, wooden shields, sheet-metal shields, composite shields, exo-assisted shields, and mech shields must feel distinct.

## Vehicles

Armor must affect:

- curb and payload mass;
- front/rear/left/right/high/low balance;
- suspension and axle load abstraction;
- acceleration;
- braking;
- steering;
- rollover risk;
- fuel or energy consumption;
- cooling;
- door/hinge operation;
- window visibility;
- tire load;
- frame stress;
- amphibious behavior where relevant;
- passenger/cargo capacity;
- repair access;
- transport routes and bridge/floor limits.

Define zone mounts for cabin, engine, fuel, battery, wheels, radiator, cargo, turret, sensors, and underbody. Additional layers must attach to specific mounts and protect specific zones.

## Drones and robots

Armor must consume payload and thrust/power reserve, alter center of gravity, endurance, maneuverability, noise, heat, range, sensor view, cooling, landing stress, and crash severity.

Light drones may choose localized protection for controller, battery, camera, propulsion, payload, or communications rather than full coverage. A heavy-lift drone may carry more layers but becomes slower, louder, shorter-ranged, and easier to intercept.

## Exoskeletons

Integrate with frame:

- hardpoint count and type;
- supported-load rating;
- joint static/dynamic limits;
- actuator authority;
- power draw;
- heat;
- inertia;
- balance;
- silhouette;
- noise;
- climbing clearance;
- fall arrest;
- evasive movement;
- weapon bracing;
- emergency release;
- unpowered failure state.

Armor zones include torso, back, hips, limbs, joints, power, controller, cabling, sensors, and optional shield mounts. A frame may permit multiple panel layers on torso mounts but fewer or none around joints and climbing surfaces.

## Mech suits

Use the mech assembly validator. Armor components must declare structural connections, mass, volume, center-of-mass shift, protection zones, layer stack, power/thermal consequences, sensor occlusion, maintenance access, and damage behavior.

Support role builds including scout, climber, shield/breacher, anti-robotic assault, fire support, cargo/engineering, and command. No build may maximize armor, speed, climbing, firepower, endurance, stealth, cooling, and sensors.

## Bases and structures

Support modular armor for:

- firing positions;
- gates;
- doors;
- windows;
- guard towers;
- generator rooms;
- fuel and hydrogen storage separation;
- communications rooms;
- workshops;
- turrets;
- vehicle bays;
- safe rooms;
- bunker breach repairs.

Armor adds weight and may require stronger frames, foundations, hinges, cranes, or supports. It affects line of sight, ventilation, fire behavior, access, evacuation, and structural collapse.

# Data contracts

Create versioned data equivalent to:

```yaml
armor_material_lot:
  lot_id: persistent_guid
  material_definition_id: stable_id
  mass_kg: number
  grade: enum
  provenance: reference
  contamination_tags: []
  moisture_state: enum
  processing_state: enum
  condition: normalized
  quality_inputs: map
  compatible_roles: []
  hazard_class: enum
  schema_revision: integer

armor_layer_definition:
  layer_id: stable_id
  role: cover|strike_face|sacrificial|confinement|spacer|reinforcement|backing|absorber|spall_liner|comfort|mount
  material_requirements: []
  areal_mass_band: enum
  thickness_band: enum
  stiffness_class: enum
  flex_class: enum
  environmental_sensitivity: []
  threat_response_curve_ref: stable_id
  multi_hit_rule_ref: stable_id
  compatible_adjacent_roles: []
  repair_rule_ref: optional

armor_panel_instance:
  instance_id: persistent_guid
  panel_definition_id: stable_id
  layer_instances: []
  material_lot_refs: []
  mass_kg: number
  dimensions_and_shape: reference
  coverage_geometry_ref: stable_id
  condition_map_ref: persistent_data
  prior_impact_refs: []
  delamination_state: normalized
  crack_state: normalized
  corrosion_state: normalized
  moisture_state: enum
  inspection_state: unknown|field_checked|shop_checked|qualified|rejected
  quality_grade: enum
  owner_id: entity
  repair_history_refs: []
  persistence_revision: integer

armor_mount_definition:
  mount_id: stable_id
  carrier_family: human|shield|vehicle|drone|robot|exo|mech|structure
  zone_id: stable_id
  compatible_panel_tags: []
  max_layers: integer
  max_mass_kg: number
  max_thickness_band: enum
  max_static_load: abstract_value
  max_dynamic_load: abstract_value
  envelope_ref: stable_id
  attachment_family: enum
  mobility_clearance_rules: []
  sensor_cooling_access_rules: []

armor_installation_instance:
  installation_id: persistent_guid
  carrier_instance_id: guid
  mount_id: stable_id
  panel_instance_ids: []
  fastener_or_bond_instance_refs: []
  installation_quality: normalized
  balance_offset: vector
  current_load_state: map
  permissions: reference
  journal_revision: integer
```

Use actual DayQ schema conventions. Do not duplicate item identity or carrier configuration.

# Recipe contract

Every armor recipe must extend the existing raw-material crafting contract with:

- material lots and minimum grades;
- accepted substitutions and explicit penalties;
- consumables;
- workstation capabilities;
- tools and condition;
- specialists and proficiency;
- schematic/research revision;
- power and environment;
- ventilation and contamination control;
- security;
- staged intermediate outputs;
- interruptibility;
- quality formula;
- batch identity;
- inspection and qualification step;
- byproducts and waste;
- repair recipe;
- salvage rule;
- installation requirements;
- carrier compatibility;
- Unreal evidence fixture.

Do not encode recipes as Blueprint-local constants.

# Manufacturing infrastructure

Support progressive assets such as:

- cutting and preparation bench;
- sewing/webbing station;
- shield jig;
- material sorting station;
- contamination-control station;
- shred/grade station;
- resin/adhesive storage and mixing abstraction;
- composite layup/forming room abstraction;
- press;
- forming equipment;
- metal cutting and finishing;
- controlled heat-treatment abstraction;
- ceramic grading and preparation;
- ceramic pressing/firing abstraction;
- honeycomb/cellular-core forming capability;
- coating and sealing;
- nondestructive-inspection abstraction;
- panel qualification station;
- mounting/fit jig;
- vehicle lift and armor bay;
- exo rack;
- mech armor crane and service bay;
- protected virtual test lab.

Workstations have condition, calibration, tooling, queue, power, ventilation, contamination, noise, heat, maintenance, sabotage, permissions, and persistence.

# Armor quality

Derive quality from:

- input grade and provenance;
- contamination and moisture;
- sorting confidence;
- recipe revision;
- workstation capability and calibration;
- tool condition;
- specialist proficiency;
- environmental control;
- layer alignment and compatibility abstraction;
- bond/confinement quality;
- geometry;
- interruption history;
- inspection result;
- repair history.

Quality affects:

- consistency;
- mass efficiency;
- multi-hit durability;
- crack/delamination growth;
- edge performance;
- water/environment resistance;
- mount reliability;
- spall/fragment containment;
- service life;
- inspectability;
- salvage value.

Low quality should have readable causes, not arbitrary hidden failure.

# Damage and ballistic-backend boundary

The armor skill must consume vendor-neutral results from the DayQ ballistics interface. It must not depend directly on BulletForge, EasyBallistics, Terminal Ballistics, or another vendor’s types.

The ballistics boundary supplies, at minimum:

- authoritative shot/impact identifier;
- impact location and direction;
- threat/projectile definition reference;
- velocity and retained-energy/momentum abstraction;
- impact angle;
- material/layer interaction query;
- ricochet, penetration, stop, or continuation state;
- remaining projectile/fragment state;
- evidence/debug identifier.

The armor system supplies:

- spatial zone and coverage;
- ordered layers;
- current condition field;
- material and mount definitions;
- prior-hit damage;
- environment state;
- backing/support state;
- armor-derived fragment/spall events;
- deformation/blunt-transfer inputs to the existing wound or component-damage system;
- updated persistent damage.

The server owns impact resolution and persistent mutation. Client effects display authorized results only.

# Spatial damage model

Do not reduce a whole panel to one health value.

Support an efficient damage field containing:

- hit location;
- affected radius/zone abstraction;
- cracked or fragmented strike face;
- delamination;
- dent/deformation;
- perforation;
- spall-liner damage;
- mount/fastener damage;
- edge damage;
- water/fire/corrosion damage;
- remaining coverage uncertainty;
- inspection confidence.

Nearby repeated hits should interact with existing damage. Distant zones may retain protection. Use a performant spatial representation appropriate to each carrier and relevance tier.

# Repair, replacement, and salvage

Support:

- field patching of covers, straps, mounts, and minor backing damage;
- replacement of tiles or modular strike elements;
- replacement of fasteners and brackets;
- drying and decontamination where allowed;
- corrosion treatment abstraction;
- composite patch abstraction;
- shop-level rebonding only when the recipe permits;
- panel rejection after unrepairable damage;
- requalification after structural repair;
- cannibalization;
- controlled salvage by material layer;
- damaged armor retained as lower-tier protection only when explicitly reclassified.

Repair must not erase impact history or restore protection without materials, capability, inspection, and loss. Some ceramic or heavily delaminated panels are replace-only.

Repair-under-fire must obey existing combat and base-raid rules. Large vehicle/exo/mech panels require lifting, support, access, tools, and time.

# Physical inventory and logistics

Every panel, shield, liner, carrier, resin lot, ceramic lot, plate, mount, and tool must define mass, dimensions, shape, volume, grip, access, noise, hazard, stack/nesting, and transport rules.

Support:

- one-hand, two-hand, team, exo, hoist, crane, and vehicle handling;
- racks and protected panel storage;
- brittle-panel handling;
- contamination isolation;
- wet mass;
- panel carts;
- vehicle and mech armor pallets;
- dropped-panel damage;
- sling and external-carry consequences;
- theft and capture;
- convoy logistics.

Nested containers and panel racks cannot remove mass or create volume.

# Progression and balance

Armor progression improves repeatability, weight efficiency, coverage, durability, integration, and repair—not absolute safety.

Balance:

- solo improvised builds;
- small-group workshop builds;
- clan industrial armor;
- elite/enclave recovered systems;
- exo and vehicle specialization;
- mech-scale strategic production;
- armor-specific counters;
- logistics and maintenance;
- salvage and battlefield recovery;
- market scarcity;
- regional sources of steel, ceramics, fiber, resin, presses, kilns, tools, and specialists.

Model material sources and sinks so the world neither starves immediately nor saturates with perfect armor.

# Unreal MCP implementation guidance

Use the existing DayQ Unreal MCP production and validation skill.

Before editing:

1. verify Unreal MCP, Terminal, EditorToolset, build, PIE, logs, tests, and evidence capture;
2. inspect the actual project and system owners;
3. map overlap and schemas;
4. confirm current ballistics-backend interface status;
5. present any conceptual change to the user;
6. create bounded work orders.

Prefer:

- versioned Data Assets/Data Tables for material, layer, panel, carrier, mount, recipe, and threat-response definitions;
- persistent unique panel and installation instances;
- reusable armor-zone, armor-mount, condition, inspection, repair, inventory, ownership, permissions, construction, and persistence components;
- a server-authoritative armor-resolution subsystem or adapter to the existing damage owner;
- spatial coverage/impact data sized by carrier class;
- configuration replication separate from high-frequency hit events;
- C++ for authoritative assembly validation, impact resolution, transaction integrity, persistence boundaries, and performance-critical spatial damage;
- Blueprints for composition and presentation without authoritative truth in client graphs;
- debug views for coverage, gaps, layer stacks, mass, mounts, center of mass, damage fields, threat response, and server/client authority.

After Unreal MCP or EditorToolset changes, re-read affected properties. Compile, run automated tests, launch PIE, execute the live route, capture evidence, repair failures, and rerun regressions.

# Multiplayer and persistence

The server authoritatively validates:

- crafting reservation and completion;
- quality generation;
- inspection and qualification;
- panel installation/removal;
- carrier compatibility;
- mass, balance, and movement consequences;
- hit location and impact resolution;
- armor, mount, carrier, wound, and component damage;
- repair and salvage;
- ownership, theft, permissions, capture, and work orders.

Persist:

- unique panel IDs;
- layer and material-lot provenance;
- quality;
- coverage and shape definition;
- spatial damage field;
- prior impacts;
- environment damage;
- inspection state;
- repair history;
- owner;
- installed carrier and mount;
- fastener/bond state;
- carrier balance/load effects;
- active crafting/repair jobs;
- recipe/schema revision.

Test late join, concurrent installation, simultaneous pickup, disconnect during transfer, death/drop, vehicle destruction, exo power loss, mech abandonment, carrier capture, server restart during impact and repair, rollback, journal replay, migration, and candidate ballistics-backend replacement.

# Exploit analysis

Prevent:

- client-forged armor or protection;
- stacking beyond mount limits;
- installing the same panel on multiple carriers;
- backpack armor counting as worn coverage unless explicitly modeled;
- zero-mass or zero-volume panels;
- nested-container mass bypass;
- cancel/refund duplication;
- repair resetting impact history for free;
- uninstall/reinstall healing armor;
- rotation exploiting coverage or thickness;
- clipping armor inside carrier geometry;
- client-supplied impact zones;
- logout avoiding panel damage;
- rollback restoring armor while retaining salvaged outputs;
- obsolete clients loading old high-protection definitions;
- invulnerable bases through overlapping panels;
- repair-under-fire abuse;
- drone armor bypassing payload/flight limits;
- exo armor bypassing joint, power, heat, or climbing limits;
- mech armor bypassing structure, center of mass, cooling, or transport limits.

# Required validation tools

Create deterministic validators for:

- crafting graph cycles and unreachable nodes;
- material mass balance and declared waste;
- panel layer compatibility;
- maximum layers;
- areal/total mass calculations;
- mount and carrier budgets;
- envelope/clearance;
- center-of-mass changes;
- coverage gaps and overlap;
- material/threat response references;
- missing repair/salvage paths;
- persistent schema versions;
- duplicate IDs;
- ballistics-adapter neutrality;
- authoritative replication ownership.

# Required integrated vertical slice

Build and validate this route:

1. A survivor scavenges books, magazines, tape, cloth, boards, sheet metal, insulation, resin/adhesive lots, broken sanitary ceramics, steel plate, straps, fasteners, and repair tools.
2. Physical inventory enforces mass, volume, bulk, contamination, brittle handling, hand occupancy, and transport.
3. The survivor builds a crude book-and-tape insert and handheld shield.
4. Rain/moisture, bulk, fatigue, weapon access, visibility, and low-tier impact behavior create observable limitations.
5. A field workshop builds a glass-fiber/resin backing from compatible processed feedstock and rejects unsuitable contaminated insulation.
6. An industrial shop sorts and grades broken porcelain, then builds a backed ceramic mosaic panel through abstract staged production.
7. The shop creates a steel/composite panel and demonstrates its higher mass and carrier consequences.
8. A precision facility produces qualified two-layer and three-layer ceramic/fiber/resin armor assemblies.
9. The same panel families are installed on a human carrier, handheld shield, vehicle, drone, combat exoskeleton, and mech test chassis through carrier-specific mounts.
10. The assembly validator rejects excessive layers, mass, thickness, bad mounts, blocked joints, sensor occlusion, cooling obstruction, flight overload, and unsafe center-of-mass changes.
11. The accepted exo two- and three-layer configurations demonstrate better protection but different movement, power, heat, climbing, noise, and endurance costs.
12. Vehicle uparmoring affects suspension/load, acceleration, braking, handling, doors, cooling, fuel use, and cargo capacity.
13. Drone armor affects payload, endurance, stability, heat, range, and sensor coverage.
14. Mech armor affects structure, ground pressure, joint authority, power, heat, sensors, maintenance, and transport.
15. Server-authoritative virtual impacts exercise coverage gaps, angles, layer ordering, penetration/stop/continuation, deformation, spall, multi-hit damage, edge damage, mount failure, and component/wound transfer.
16. Damaged panels are inspected, field repaired where valid, shop repaired, requalified, rejected, replaced, and salvaged.
17. Two or more clients repeat crafting, installation, combat, removal, transfer, capture, repair, and salvage under latency and packet loss.
18. The server restarts during crafting, installation, impact resolution, and repair.
19. Persistence, journal replay, rollback, and migration recover material lots, panel identity, installation, condition, impact history, and carrier effects without duplication or healing.
20. Representative armored squads, vehicles, drones, exos, mechs, bases, and simultaneous impacts meet performance budgets.

# Acceptance gates

Do not mark complete unless:

1. every armor output traces to valid raw sources, tools, workstations, specialists, power, and staged jobs;
2. graph analysis finds no free output, accidental cycle, or unreachable capability;
3. mass balances include declared waste and salvage loss;
4. every panel has physical mass, dimensions, coverage, layers, mounts, condition, and persistent identity;
5. improvised materials remain inconsistent, bulky, degradable, and bounded;
6. insulation and ceramic salvage routes reject unsuitable lots;
7. porcelain and honeycomb/cellular concepts are represented accurately enough for gameplay without magical conversion;
8. layer order and quality matter independently of layer count;
9. all carrier layer maxima derive from mount, mass, envelope, balance, structure, mobility, power, heat, propulsion, and clearance constraints;
10. two- and three-layer exo examples create real protection/cost tradeoffs;
11. coverage gaps and spatial damage work;
12. repeated impacts affect damaged regions;
13. repair does not silently restore protection or erase history;
14. vehicle, drone, exo, mech, and base performance changes are observable;
15. ballistics integration remains vendor-neutral;
16. server authority rejects forged hits, panels, installations, repairs, and salvage;
17. late join, disconnect, transfer conflict, restart, journal replay, rollback, and migrations pass;
18. representative CPU, memory, physics, replication, save, and streaming budgets pass;
19. assets have correct scale, pivots, sockets, collision, LODs, damage states, materials, and metadata;
20. logs, screenshots/video, debug overlays, state dumps, test reports, and profiles exist;
21. no real-world safety claim or actionable armor recipe appears in deliverables;
22. unresolved live-project gates are reported as blocked, not passed.

# Required asset-production coverage

Use the DayQ systemic asset factory and reference-baseline-to-canonical workflow for:

- books, magazines, tape, cloth, carriers, straps, handles, and pouches;
- improvised shields;
- steel, ceramic, composite, and layered panels;
- plate carriers;
- shield frames and viewports;
- vehicle brackets and armor zones;
- drone shells and localized panels;
- exo plates, joint guards, shield hardpoints, and racks;
- mech tiles, modules, mounting frames, cranes, and service racks;
- presses, forming machines, composite workstations, inspection equipment, and repair tools.

Web image search may establish legal common-object references and baseline proportions. It does not establish hidden construction, protection, canon, licensing, gameplay, or final acceptance. Produce original DayQ assets and record provenance.

# Current evidence baseline

Use current official evidence only to frame the virtual validation discipline:

- NIJ Standard 0101.07 defines minimum performance requirements and standardized testing for law-enforcement body armor: <https://nij.ojp.gov/topics/equipment-and-technology/ballistic-resistance-body-armor-nij-standard-010107>.
- NIJ documentation emphasizes controlled threat definitions, laboratory methods, conditioning, perforation/deformation evaluation, and compliant-product testing.
- U.S. Army materials research describes ceramic armor as part of composite systems and emphasizes the importance of material combination and controlled ceramic processing: <https://www.army.mil/article/211750/army_researchers_find_inspiration_in_nature_to_improve_body_armor>.

Do not claim NIJ compliance for game-created items. Do not reproduce operational test details. Recheck official sources when implementing.

# Required deliverables

Produce:

1. all five native DayQ armor skills;
2. an `agents/openai.yaml` for every skill;
3. shared armor architecture and ownership map;
4. material and production-tree reference;
5. carrier integration reference;
6. vendor-neutral ballistics-boundary reference;
7. repair, salvage, inspection, and qualification reference;
8. automated/live validation matrix;
9. material, layer, panel, mount, installation, damage-field, recipe, workstation, inspection, and repair schemas;
10. complete dependency graph from scavenged matter through mech armor;
11. source/sink, economy, progression, transport, and maintenance models;
12. human, shield, vehicle, drone, robot, exo, mech, and structure armor catalogs;
13. Unreal ownership map and bounded work orders;
14. multiplayer, persistence, journal, crash-recovery, migration, exploit, accessibility, and performance plans;
15. integrated vertical-slice evidence;
16. user decisions and unresolved evidence;
17. no-skip ledger updates;
18. manifest, checksums, validator results, and import report when packaging is part of the owning task.

# Completion report

Report:

- skill and references created;
- existing DayQ systems inspected;
- ownership and overlap decisions;
- conceptual decisions confirmed by the user;
- material/build graph;
- schemas and migrations;
- Unreal assets, code, Blueprints, Components, Data Assets, Data Tables, and levels affected;
- carrier assembly and layer-validation results;
- ballistics, spatial damage, repair, and salvage results;
- multiplayer, persistence, journal, rollback, crash-recovery, migration, security, exploit, and performance results;
- asset and visual-validation results;
- failures, repairs, reruns, and remaining limitations;
- exact evidence or explicit blocked status;
- final acceptance status.

Never claim armor works because its mesh looks thick. Never claim a material protects against a threat from its name alone. Never equate layer count with protection. Never let extra armor evade carrier physics. Never convert a plugin listing into ballistic proof. Never provide real-world improvised armor instructions. Never mark complete without live authoritative evidence.
