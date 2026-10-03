---
name: generate-surfable-item-prompts
description: Write Blender and engine prompts for rideable objects in a massive-wave surfing game, preserving shape-derived handling.
---

# Surfable Item Prompt Generator

Convert even a minimal request such as "make a couch" into one implementation-ready production prompt. Preserve the object's real physical identity; never produce a surfboard reskin.

## Workflow

1. Classify the request as passive rigid, deformable, conventional surf equipment, powered board, personal watercraft, boat, towed item, or body-surfing equipment.
2. Infer plausible real-world dimensions, dry and saturated mass, construction, materials, density distribution, center of mass, rotational inertia, displacement, water absorption, structural limits, and failure modes. Use ranges when exact values are not supportable.
3. Derive the unassisted hydrodynamic personality from geometry and material: buoyancy, waterline, planing surfaces, planing threshold, longitudinal and lateral drag, edge catches, pitch/roll/yaw response, directional tracking, flex, flutter, waterlogging, impact response, propulsion, and control authority.
4. Add only a bounded surfability correction envelope: limited stability assistance, wave-face attraction, self-righting, rider control bias, and recovery help. State hard limits so assistance cannot erase object-specific clumsiness.
5. Specify rider interfaces where relevant: seated and standing poses; rider, hand, foot, leash, tow, and propulsion sockets; intake, exhaust, camera, audio, foam/spray VFX, and detach conditions.
6. Specify asset production: clean hero mesh, mobile-aware LOD chain, UVs and PBR materials, collision proxies, named buoyancy/planing/drag/impact/damage regions, moving or breakable parts, dry/wet/soaked/damaged/foam-contact material states, and engine-ready export.
7. Specify runtime hydrodynamics metadata and observable validation on a standardized massive-wave course.

## Output contract

Write one polished imperative prompt, normally 220-500 words, that includes:

- identity, condition, dimensions, dry/wet mass, materials, and construction;
- center of mass, inertia, displacement, buoyancy zones, planing surfaces, drag axes, and stability;
- distinct pitch, roll, yaw, edge, flex, waterlogging, propulsion, crash, and damage behavior;
- assist limits and explicit non-goals;
- rider, hand, foot, leash, tow, propulsion, effects, and audio sockets as applicable;
- render mesh, LODs, collision, moving parts, UVs, materials, regions, metadata, export, and QA;
- runtime-engine integration and mobile performance requirements without claiming native-4K fluid simulation.

Reject generic language such as "make it realistic," "add good physics," "optimize it," or "add collisions." Replace it with named geometry, states, budgets, behaviors, and pass conditions.

Do not require full cinematic fluid simulation at runtime. Use high-quality authored assets, scalable internal resolution, dynamic resolution, upscaling, mobile LODs, simplified water interaction, and optional high-end replay rendering.

Read [surfable-item-contract.md](references/surfable-item-contract.md) whenever generating a prompt. Use its checklist and metadata fields without copying irrelevant categories into the output.

## Quality baseline

For a worn three-seat couch, require plausible full-size dimensions and mass; frame, cushion, upholstery, and water-absorption behavior; crude underside planing; high drag; poor yaw; delayed steering; cushion waterlogging; rider and hand/foot sockets; leash/tow points; compound collision; multiple buoyancy regions; wet/dry/soaked/damaged/foam-contact states; LODs; hydrodynamics metadata; and inspection, waterline, planing, crash, and performance evidence. Match or exceed that specificity for every item.
