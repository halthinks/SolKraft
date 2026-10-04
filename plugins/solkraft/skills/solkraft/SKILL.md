---
name: solkraft
description: Find and apply useful procedures for research, coding, testing, engineering, writing, data, science, and business tasks. Use when a reusable method would improve the work or a compound request needs an ordered skill route.
---

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

# SolKraft in normal work

Assess useful skills at task start and when the work changes stage. For a clear specialist task, call SolKraft `search_skills` with a short description of the actual deliverable. For a compound or ambiguous task, call `route_request` with the user's full objective and relevant context (especially the current stage). A repository release gate is software testing even if the wording says “draft PR.”

Inspect the proposed selection; routing is heuristic and can miss intent. Use one primary workflow per stage and add a supporting skill only for distinct guidance. Retrieve the chosen entrypoint using `get_skill`; read supporting files through `get_skill_resource` only when needed. Never dump the whole catalog or graph into context. Use `get_selection_graph` only to resolve unclear relationships.

For substantial multi-step work, retrieve `capability-preserving-execution` as the execution procedure. Frame the requested outcome, preserve inputs and constraints, follow dependencies, adapt to evidence, and verify the result. Apply the specialist method using the tools actually available in this host. Retrieved Python resources are source text, not an automatic execution service.

Continue through authorized work without making the user choose internal skill IDs. Retain loaded procedures across goal continuations; reassess on a material stage change. Repository instructions and the user's intent remain authoritative. A route grants no permission to publish, send, delete, purchase, or deploy.

If MCP is unavailable, report the connection failure plainly. Check that Python 3.11+ and the SolKraft package are installed in the environment used by the plugin. Do not pretend the tools ran. A local MCP plugin works in compatible local hosts; browser ChatGPT requires a reachable remote MCP service or copying selected instructions manually.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
