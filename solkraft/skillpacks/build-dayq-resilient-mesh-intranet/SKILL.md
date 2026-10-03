---
name: build-dayq-resilient-mesh-intranet
description: Implement DayQ resilient mesh messaging, repeaters, gateways, base intranets, and capture or outage behavior.
---

# Build DayQ Resilient Mesh and Intranet

Read [FULL_CONTRACT.md](references/FULL_CONTRACT.md) and [INTEGRATION.md](references/INTEGRATION.md). Preserve existing acoustic/radio, inventory, crafting, power, building, clan, authority, persistence, and cyber owners.

1. Keep LoRa-class mesh low-bandwidth data only: compact text, orders, acknowledgements, position uncertainty, alerts, sensors, telemetry, summaries, authentication, and delayed bundles—not live voice.
2. Treat DayQ mesh as an original LoRa-PHY/Meshtastic-like decentralized protocol; do not label it standard LoRaWAN mesh.
3. Model physical persistent nodes, antennas, power, queues, routing, congestion, uncertainty, trust, capture, compromise, revocation, and intranet services.
4. Resolve routes and recipients on the server; replicate only authorized relevant presentation. Bound queues, retries, searches, history, debug, and unloaded-region simulation.
5. Implement through Unreal MCP and validate direct/multihop/store-forward/partition/capture/revoke/restart/migration/privacy/density routes with GameDevBench evidence.
