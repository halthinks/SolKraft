---
name: build-dayq-character-rig-collision
description: Build DayQ character skeletons, physics assets, collision, hit regions, and animation-compatible body rigs.
---

# Build DayQ Character Rig and Collision

Read [CHARACTER_RIG_COLLISION_CONTRACT.md](references/CHARACTER_RIG_COLLISION_CONTRACT.md). Also use `produce-dayq-organic-assets` and `standardize-dayq-rigs-interactions`.

## Workflow

1. Inspect current skeletons, meshes, body regions, hit logic, attachments, animation assets and platform budgets.
2. Define one stable gameplay skeleton standard and explicit retarget variants.
3. Separate visible mesh, movement capsule, query hit regions and physics bodies.
4. Map bones and material regions to health, armor, clothing, equipment and physical reactions.
5. Create first-person arm/body presentation without a second gameplay skeleton authority.
6. Validate deformation, extreme poses, equipment fit, IK, physical animation, ragdoll, LOD transition and crowds.
7. Version the rig and prove migration/retargeting before replacing an accepted skeleton.

## Rules

- Never use render triangles as authoritative body-region logic.
- Never permit a cosmetic body scale to alter competitive collision without an approved bounded profile.
- Keep stable socket and region IDs across visual variants.
- Preserve original DayQ character design and lawful source provenance.

## Output

Deliver rig/version, hierarchy, retarget chains, sockets, region map, Physics Asset, collision profiles, skin/correctives, body variants, LODs, budgets, conformance fixtures and Unreal evidence.
