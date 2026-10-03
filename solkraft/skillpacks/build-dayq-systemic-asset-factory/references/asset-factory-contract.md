# Asset Factory Contract

The asset factory owns one immutable lineage from request to acceptance. The job ID and hashes connect the user request, canon/systemic brief, sources, reconstruction spec, Blender file/export, Unreal assets/data, test evidence, repairs, and final disposition.

Required routes are `img2threejs_then_blender`, `direct_blender`, `licensed_source_then_blender`, `generated_source_then_blender`, `original_concept_then_blender`, and `dedicated_character_or_organic_pipeline`. Route choice must cite suitability and hidden-geometry risk.

An asset cannot be accepted until:

- requested gameplay and DayQ canon are represented;
- all environmental channels have applicability and justification;
- every source passes rights/provenance/security gates;
- applicable reconstruction stages pass;
- Blender issues are resolved or explicitly waived by the decision authority;
- Unreal automated, visual, multiplayer/persistence, and performance gates pass with evidence;
- manifest hashes and identifiers resolve to the delivered products.

Use `DAYQ_ASSET_FACTORY_JOB.schema.json` and `DAYQ_ASSET_CONTRACT_V2.schema.json`. Preserve V1 through an explicit adapter; never silently reinterpret it as V2.
