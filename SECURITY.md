<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Security policy

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Contract-aware routing uses semantic capability identity plus typed `contract.yaml` metadata: inputs/outputs, effects, capability/resource requirements, verification, provenance, trust, and exact digests.
- REST, MCP, and CLI default to hardened policy; opaque/inadmissible capabilities fail closed. The Python library remains compatibility-oriented unless stricter policy is requested.
- SolKraft is advisory and non-executing: runtime authority stays with the host and `execution_authorized` remains `false`.
- `ContractIndex` supplies compact metadata to routing/API/MCP/docs without loading every full `SKILL.md` body.
- Read-only MCP tools: `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, `get_selection_graph`, `get_skill_contract`, `get_contract_index`.
- Reusable CI and pre-PR validation share contract/schema, routing, package/wheel, installed-MCP, index/hardening, and evidence gates.
- Latest local acceptance: **100,000 / 100,000** unique 250-word requests passed with **100 ask families per skill**, **100% eligible target recall**, **100% hardened blocking**, and **100% consequential-boundary correctness**; no explicit skill IDs were injected.
- The public Validation display is a clearly labeled recorded reenactment, not live browser CI.

<!-- END SOLKRAFT CURRENT SYSTEM -->


SolKraft is an early open-source project. Please do not report exploitable vulnerabilities in public issues. Use GitHub's private vulnerability reporting for `halthinks/SolKraft` if enabled, or contact the repository owner through the verified GitHub profile. Include affected version, impact, reproduction and a safe mitigation when known. Do not include live API keys or private skill content.

The API is designed for hobby deployments. Operators are responsible for key distribution, rate limiting, monitoring and choosing safe skill roots. Do not expose a personal skill directory on a public service.
