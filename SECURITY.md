<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Security policy

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Contract-aware routing uses semantic capability identity plus machine-readable `contract.yaml` metadata for typed inputs/outputs, namespaced effects, capability/resource requirements, declarative verification, provenance, trust, and exact digests.
- Public REST, MCP, and CLI routing default to **hardened** policy. Opaque or otherwise inadmissible capabilities fail closed; the Python library stays compatibility-oriented unless stricter policy is requested.
- SolKraft is advisory and non-executing. Runtime authority remains with the host and `execution_authorized` remains `false`.
- The compact `ContractIndex` supplies routing/API/MCP/docs metadata without loading every full `SKILL.md` body into the hot path.
- Read-only MCP tools: `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, `get_selection_graph`, `get_skill_contract`, and `get_contract_index`.
- Reusable CI and pre-PR contribution validation share contract/schema, routing, packaging, installed-MCP, index/hardening, and evidence gates.
- Latest local acceptance: **100,000 / 100,000** unique 250-word requests passed with **100 ask families per skill**, **100% eligible target recall**, **100% hardened blocking**, and **100% consequential-boundary correctness**; no explicit skill IDs were injected.
- The public Validation display is a clearly labeled **recorded reenactment**, not live browser CI.
- Contracts and imported MCP/OpenAPI metadata never create credentials, runtime grants, or trust; trust is external and digest-bound, and executable verification stays outside core SolKraft.

<!-- END SOLKRAFT CURRENT SYSTEM -->


SolKraft is an early open-source project. Please do not report exploitable vulnerabilities in public issues. Use GitHub's private vulnerability reporting for `halthinks/SolKraft` if enabled, or contact the repository owner through the verified GitHub profile. Include affected version, impact, reproduction and a safe mitigation when known. Do not include live API keys or private skill content.

The API is designed for hobby deployments. Operators are responsible for key distribution, rate limiting, monitoring and choosing safe skill roots. Do not expose a personal skill directory on a public service.
