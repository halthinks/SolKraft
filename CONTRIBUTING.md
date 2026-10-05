<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Contributing to SolKraft

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
- Declared Contract v1 sidecars require supported declarative verification checks; run `python -m scripts.preflight_contribution contributions/<skill>.json` before PR submission.

<!-- END SOLKRAFT CURRENT SYSTEM -->


Thanks for contributing. Keep changes focused and add tests for behavior changes.

## Issue or pull request?

Open a **support issue** when you need help, have a setup or connection problem, have a question, or can report reproducible unexpected behavior but are not submitting a finished repository change. Use the site's Support link or the repository's Support request issue form.

Open a **pull request** when you already have a concrete code, documentation, test, contract, routing, or skill change ready for review. A PR should include the implementation and the evidence needed to review it; do not open a support issue merely to hold finished contribution work.

Security vulnerabilities belong in GitHub Security Advisories, not public issues or PR descriptions. Never submit API keys, tokens, passwords, private skill content, customer data, proprietary code, or other secrets. Sanitize logs, screenshots, paths, prompts, and reproductions before posting.

Start with [Add a skill the system can actually use](docs/SKILL_CONTRIBUTIONS.md). It includes a copyable agent task, exact file/graph parameters, an executable manifest example, and the local full gate. Submit the complete integration, including routing and generated catalog changes, rather than only a skill file. The website's **Contribute a skill** walkthrough explains each step for first-time contributors.

## Skill contribution provenance

A skill contribution must include:

- the author or upstream project and a stable source URL when available;
- the applicable license and confirmation that redistribution is allowed;
- attribution and notices required by that license;
- a concise purpose-oriented description in frontmatter;
- tests or examples showing when routing should and should not select it.

First-party skill contributions must be submitted under the repository license. Do not copy plugin cache content into the repository based only on local availability. Keep contributions within the repository's published scope and follow its agent and engineering contracts.

## One-command skill integration and free CI

A new skill must update the router proof as part of the same contribution. Run `python -m scripts.prepare_skill_contribution contributions/<skill>.json` to verify that the production catalog sees it and to derive its exact-recall or ambiguity coverage automatically. Then run `python -m scripts.preflight_contribution contributions/<skill>.json`; preflight invokes the planner itself, so contributors cannot accidentally omit semantic-proof registration.

The benchmark is catalog-driven: adding a valid skill changes the generated semantic corpus automatically. Contributors do not maintain a separate phrase list. See [the skill contribution guide](docs/SKILL_CONTRIBUTIONS.md#free-ci-with-floot-and-automatic-semantic-proof-updates) for the free Floot runner path, 16-shard proof commands, aggregation, and what must be included in a clean PR.

## Development checks

```powershell
pip install -e ".[dev]"
python -m pytest -q
```

The REST API and MCP server may return skill instructions as text. They must never execute them. New tools must preserve that read-only boundary and must not expose absolute server paths.
