<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolKraft plugin

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


Install Python 3.11+ and the runtime first:

```sh
python -m pip install "git+https://github.com/halthinks/SolKraft.git"
codex plugin marketplace add halthinks/SolKraft --sparse .agents/plugins --sparse plugins/solkraft
codex plugin add solkraft@solkraft
```

Launch Codex with `solkraft` on PATH and start a new session. This package contains a supported Codex manifest, a local stdio MCP connection, and a compact integration skill. The separately installed Python runtime contains the catalog and router. The plugin does not require a hosted API, user account, or service key. Your agent's existing model and tooling costs still apply.

Ask normally, for example: “Investigate this bug, implement the fix, and verify the release build.” The integration skill helps the host search or route, retrieve useful methods, apply them through its own tools, and verify its work. SolKraft tools are read-only; they never run your repository themselves.

Full setup, verification, and troubleshooting: https://github.com/halthinks/SolKraft/blob/main/docs/PLUGIN.md
