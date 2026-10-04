<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolKraft plugin

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
- The plugin exposes metadata/search/routing/retrieval only; it does not add a skill-execution MCP tool.

<!-- END SOLKRAFT CURRENT SYSTEM -->


Install Python 3.11+ and the runtime first:

```sh
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
codex plugin marketplace add halthinks/SolKraft --sparse .agents/plugins --sparse plugins/solkraft
codex plugin add solkraft@solkraft
```

Launch Codex with `solkraft` on PATH and start a new session. This package contains a supported Codex manifest, a local stdio MCP connection, and a compact integration skill. The separately installed Python runtime contains the catalog and router. The plugin does not require a hosted API, user account, or service key. Your agent's existing model and tooling costs still apply.

Ask normally, for example: “Investigate this bug, implement the fix, and verify the release build.” The integration skill helps the host search or route, retrieve useful methods, apply them through its own tools, and verify its work. SolKraft tools are read-only; they never run your repository themselves.

Full setup, verification, and troubleshooting: https://github.com/halthinks/SolKraft/blob/main/docs/PLUGIN.md
