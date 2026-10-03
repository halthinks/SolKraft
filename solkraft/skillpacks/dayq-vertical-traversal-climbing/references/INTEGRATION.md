# Integration ownership

Integrate with existing character movement, combat, physical-load outputs, building/destruction, AI navigation, world partition, authority, and persistence. Do not introduce a parallel damage or save model. Treat verticality as core map topology only after explicit confirmation.

## Clothing adapter

Traversal emits authoritative contact, snag, abrasion, puncture, load, water, and fall events keyed to body/garment zones. `build-dayq-clothing` resolves those inputs against materials, seams, closures, soles, gloves, straps, fit, wetness, and prior repairs, then returns traction, grip, restriction, snag, retained-load, exposure, and failure projections. Traversal owns route and motion truth; clothing owns only garment-local state.
