# DayQ Material State Contract

Each material family records:

- stable ID/version, composition, process, density and relevant thickness range;
- surface/volume structure, coating, joints and failure modes;
- root-material and reclamation mappings;
- environmental/contamination/fire/impact response channels;
- authoritative inputs, state variables, cadence, thresholds and hysteresis;
- derived physical/gameplay outputs and owning consumer;
- repair, cleaning, replacement, salvage and irreversible loss;
- Blender shader/bake contract and Unreal master-material parameters;
- LOD/state simplification and density budget;
- persistence fields and migration;
- coupon, component and representative-asset acceptance tests.

Do not put gameplay authority in a material shader. Do not make a wetness mask change item mass unless the authoritative material-region state changed first.
