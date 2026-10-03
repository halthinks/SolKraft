---
name: propagate-dayq-proximity-audio
description: Implement DayQ proximity voice, acoustic events, AI hearing, privacy, and radio or intercom routing.
---

# Propagate DayQ Proximity Audio

Read [FULL_CONTRACT.md](references/FULL_CONTRACT.md) and [INTEGRATION.md](references/INTEGRATION.md). The approved initial foundation is Unreal Voice Chat Interface with EOS provisionally behind a provider-neutral wrapper; Sound Attenuation and MetaSounds render audio. DayQ owns gameplay propagation, radio, privacy, and AI-hearing truth. Do not adopt or evaluate plugins owned by the separate library bakeoff.

1. Create one server-authorized acoustic event used by appropriate player rendering, AI evidence, debug, and privacy-safe telemetry.
2. Separate physical acoustics from radio/network transport. Authorize recipients server-side; never send unauthorized voice and attenuate it client-side.
3. Model bounded distance/directivity/air/terrain/room/portal/occlusion/transmission/reflection/masking and listener condition with budgets and uncertainty.
4. Keep raw voice out of AI and ordinary logs; add moderation/retention/consent/accessibility only through approved policy.
5. Test voice modes, structures/terrain/vehicles, radios, unauthorized listeners, disconnect/late join/death/spectator, combat/fire/weather/masking, AI localization error, outage recovery, density, and regressions.
