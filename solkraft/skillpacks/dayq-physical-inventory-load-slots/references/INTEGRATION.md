# Integration ownership

Extend the existing authoritative fast-array inventory, item identity, movement, equipment, vehicle cargo, UI, journaling, and migrations. Add data and adapters; never create a second inventory source of truth. Treat adoption of physical packing/access as a conceptual change requiring confirmation.

## Clothing adapter

Garment pockets, pouches, straps, slings, holsters, plate pockets, and frame connectors are ordinary existing container/attachment nodes under the garment item ID. `build-dayq-clothing` supplies localized closure, seam, retention, access, fit, and wet-mass factors; this skill remains authoritative for contents, capacity, access transactions, load paths, hand occupancy, spill commits, and replication. Aggregate garment state must never overwrite localized pocket state.
