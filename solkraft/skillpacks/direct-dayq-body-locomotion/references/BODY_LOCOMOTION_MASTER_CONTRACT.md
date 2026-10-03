# Body and Locomotion Master Contract

## Canonical layers

1. **Body identity:** stable survivor/body ID, anthropometric profile, skeleton standard, gameplay regions, collision profile and lasting state.
2. **Movement truth:** authoritative transform, velocity, acceleration, stance, gait, contact mode, movement mode, support surface and constraints.
3. **Capability projection:** health, fatigue, load, clothing, weather, footwear, skills, assistance and equipment produce bounded capability values.
4. **Animation projection:** skeletal pose, motion matching, warping, IK, additive reactions, facial/breath presentation and equipment alignment.
5. **Physical response:** impacts, stumbles, falls, partial simulation, ragdoll, recovery and carried-body interactions.
6. **Persistence and audit:** lasting injuries, body identity, equipment/body attachments and durable interaction state; transient pose is not saved.

## Ownership

- Movement owner resolves transform and movement modes.
- Health owner resolves tissue damage, bleeding, fractures, pain, shock and consciousness.
- Survival owner resolves stamina/fatigue/thermal/hydration inputs.
- Inventory owner resolves carried items, hands, supported/unsupported mass and load distribution.
- Clothing owner resolves garment-local restriction, traction, wet mass and protection.
- Traversal owner resolves affordances, contacts, anchors, tethers and route legality.
- Combat/weapon owner resolves attacks, recoil inputs and authoritative damage requests.
- Exoskeleton/mech owner resolves actuator assistance, power, heat, faults and frame limits.
- Animation never becomes gameplay authority.
- Persistence owner journals durable state and migrations.

## Required shared projections

Use versioned vendor-neutral values for stance, gait, desired motion, actual motion, surface, slope, traction, supported mass, unsupported mass, load offsets, snag/bulk, stamina, fatigue, pain, mobility by limb, grip, balance, consciousness, assistance, hands, weapon posture, weather exposure and movement restriction reasons.

## Completion

Do not claim complete body mechanics until production skeletons and assets, representative locomotion, injuries, reactions, equipment, traversal, multiplayer, persistence, migration, performance and human playtests pass together.
