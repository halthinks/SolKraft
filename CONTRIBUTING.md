<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Contributing to SolKraft

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
- Declared Contract v1 sidecars need supported declarative verification checks; run `python -m scripts.preflight_contribution contributions/<skill>.json` before PR submission.

<!-- END SOLKRAFT CURRENT SYSTEM -->


Thanks for contributing. Keep changes focused and add tests for behavior changes.

Start with [Add a skill the system can actually use](docs/SKILL_CONTRIBUTIONS.md). It includes a copyable agent task, exact file/graph parameters, an executable manifest example, and the local full gate. Submit the complete integration, including routing and generated catalog changes, rather than only a skill file. The website's **Contribute a skill** walkthrough explains each step for first-time contributors.

## Skill contribution provenance

A skill contribution must include:

- the author or upstream project and a stable source URL when available;
- the applicable license and confirmation that redistribution is allowed;
- attribution and notices required by that license;
- a concise purpose-oriented description in frontmatter;
- tests or examples showing when routing should and should not select it.

First-party skill contributions must be submitted under the repository license. Do not copy plugin cache content into the repository based only on local availability. Keep contributions within the repository's published scope and follow its agent and engineering contracts.

## Development checks

```powershell
pip install -e ".[dev]"
python -m pytest -q
```

The REST API and MCP server may return skill instructions as text. They must never execute them. New tools must preserve that read-only boundary and must not expose absolute server paths.
