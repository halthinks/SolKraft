
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

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

## What users can do after this change

Describe the concrete outcome and why existing behavior was insufficient.

## Evidence

Record exact local commands, results, candidate source/manifest hashes, and remaining limits. For behavior changes, include the failing test before implementation and the passing result.

## Skill integration (when applicable)

- [ ] Useful procedure, supporting resources and executable helper tests included.
- [ ] Author, source, license and required notices reviewed.
- [ ] Semantic-core node, precise routing rules/vocabulary and justified relationships included.
- [ ] Authored positive, neighboring, excluded, quoted, deferred and compound cases included; automatic selection tested without forced IDs.
- [ ] `python -m scripts.check_contribution contributions/<manifest>.json --full` passed on this candidate: targeted cases, 100,000/100,000 routing requests, local build and installed MCP checks.
- [ ] Generated catalog, graph, skill pages and plugin archive reviewed.
- [ ] Realistic task evidence supplied separately from synthetic routing results.
- [ ] Existing public behavior, read-only API/MCP boundary, and privacy preserved.
