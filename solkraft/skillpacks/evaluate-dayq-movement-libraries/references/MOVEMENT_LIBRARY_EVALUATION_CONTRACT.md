# Movement Library Evaluation Contract

## Common fixture matrix

- idle/start/stop/pivot/turn; walk/jog/sprint; crouch/prone; jump/fall/land;
- slopes, stairs, ledges, moving bases, low ceilings, narrow gaps and collision recovery;
- light, heavy, offset, wet and exoskeleton-assisted loads;
- fatigue, pain, one-arm/one-leg impairment, stumble, knockdown and recovery;
- weapon-ready movement, recoil, hand occupancy and equipment changes;
- approved mantle/vault sample through the traversal owner;
- 0/50/100/200 ms RTT, jitter, loss, reorder, disconnect, reconnect and late join;
- speed/time manipulation, impossible acceleration, collision bypass and replay attempts;
- 1/16/60 representative characters, animation LODs and dedicated-server cost;
- save/restart/migration/removal with no vendor types in saved state.

Measure input-to-motion latency, acceleration/turn fidelity, foot slide, capsule/mesh divergence, collision error, correction count/magnitude, bandwidth, server/client frame time, animation cost, memory, traversal failures, physical-reaction stability and state determinism.

## Adapter boundary

Accept vendor-neutral input intent, movement/body capability, stance/mode request, environment/contact sample, platform/base motion and tick context. Return proposed move, authoritative result, correction data, movement events and debug evidence. Do not return vendor-owned persistent objects.

## Decision rule

Default to the smallest passing stack. A visually impressive candidate that fails authority, removal, performance or maintainability is rejected.
