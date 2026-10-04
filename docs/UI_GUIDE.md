<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Using SolKraft

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
- The site includes a recorded 100k validation reenactment and terminal-style system changelog; both are presentation layers, not live tests.

<!-- END SOLKRAFT CURRENT SYSTEM -->


SolKraft gives a host agent reusable procedures and a way to select them for a request. Its console makes those procedures inspectable to people. It is not a hosted autonomous job runner.

## The three layers

`solforge` owns the native selection entrypoint, Python selector/composer, domain indexes, and selection graph. It also appears as a node in that graph. `capability-preserving-execution` supplies the adaptive execution procedure: frame, map, wave, synthesize, act, verify, and finish or escalate. It has decision references rather than a Python scheduler. Specialist skills provide the detailed methods for particular work. The host agent composes these layers within its own available tools and governing instructions.

The service adapters live separately in `solkraft/catalog.py`, `routing.py`, `api.py`, and `mcp_server.py`. They index the packs and expose discovery, routing, and retrieval over Python, REST, and MCP. Capability-preserving execution is currently a catalog node available through discovery or explicit selection; the graph has no conditional edges attached to it. Its application comes from the host's execution instructions, rather than an automatic graph scheduling rule.

## Each UI tab

**Discover skills:** keyword-filter the bundled skill names and descriptions, browse in pages, inspect instructions, view the pack's Python files and supporting references, and copy the procedure. An API connection switches discovery to the server catalog and its ranked search. Search starts at page one; the page indicator states which range is visible.

**Compose a route:** load the worked example without a connection, or connect your server and submit a custom objective. Review the ordered stages and their reasons. Open each selected skill to retrieve its instructions. Expand the parser output to see selection traces, exclusions, and unresolved stages. Copy the request to use with your agent. The example is generated at build time by the real Python router and is explicitly labelled; custom routing is a live server request.

**Explore the graph:** inspect conditional relationships between workflow nodes. Filtering reduces the displayed relationship set; it does not reduce the catalog. The display reports how many relationships are shown. Catalog-only nodes are available for discovery and explicit selection without invented dependencies.

## How the semantic parser works

The native Python engine is deterministic. It uses scoped clauses, action rules, concept aliases, domain context, and lexical ranking rather than an LLM call. It separates requested stages from recognised exclusions, completed or deferred work, and quoted instructions. Context helps resolve subject matter and established work stages; it does not invent a requested action.

The selector matches eligible workflows in the semantic core. The composer preserves requested stage order and bounds selection to the requested maximum, up to 50 skills. The service checks selected IDs against the mounted catalog and can adapt recognised unmatched active stages through catalog matching. It retains unresolved stages when the request cannot be confidently matched. Explicit IDs provide direct selection.

Graph relationships recommend supporting methods or subsequent work only when their conditions apply. The graph does not grant authority, execute tools, or create a background hook into an agent's internal skill picker. Scores are relative rankings, not confidence probabilities. Complex unfamiliar wording may require review or explicit selection.

For example, “draft pull request” is ambiguous by itself. A request to verify a release before a draft PR belongs to software verification; a request to write the PR description belongs to writing. Established repository-release-gate context can resolve a short follow-up.

## From selection to execution

A human can copy a procedure, or an agent can retrieve it through REST or the five MCP tools: search, route, get skill, get resource, and graph. Retrieve supporting references only when their conditions apply. A copied entrypoint does not magically include its linked files; install the skill pack or retrieve those resources when needed.

The host agent applies capability-preserving execution for substantial work: preserve inputs and scope, map dependencies, batch safe independent operations, keep successful evidence, retry only invalidated work, and inspect the real result. Product-specific and repository contracts remain authoritative. A selected route is advisory and never authorizes publishing, deployment, deletion, sending, or any other effect.

The static site requires no key for browsing, inspection, or the worked example. A custom request requires a running SolKraft server with the applicable API key and CORS configuration. The key stays in the current tab. See [client setup](CLIENTS.md).

The current walkthrough uses large vertical HTML cards. Cards reveal in order once when entering view, and a light pulse travels along each connector before the next stage appears. There is no pause control or continuously looping diagram; reduced-motion users see the complete static flow.
