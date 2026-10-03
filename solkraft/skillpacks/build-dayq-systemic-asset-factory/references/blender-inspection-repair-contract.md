# Blender Inspection and Repair Contract

Blender MCP must import only cleared sources into a project-scoped scene, establish metric scale and axes, preserve component hierarchy, and create production topology, UVs, baked/PBR materials, environmental material regions/states, LODs, collision, sockets, pivots, damage/repair/salvage states, and export metadata.

Required loop: checkpoint → inspect scene and source → render fixed views/debug overlays → log defects with severity → repair the highest-impact defect → rerender/reinspect → repeat → accept or block. Inspect scale, silhouette, hidden geometry, normals, nonmanifold geometry, topology density, UVs, texture rights/resolution, material response, LOD transitions, collision fit, pivots/sockets, moving parts, environment states, damage/repair variants, naming, exports, and performance budgets.

Acceptance requires hashed `.blend` and export products, inspection renders, resolved issue records, and an explicit result. Blender success does not imply Unreal success.
