<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Using SolKraft

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Describe an outcome in ordinary language; SolKraft discovers procedures, composes requested stages, and retrieves selected instructions. The catalog contains **173 bundled skills** across software, research, data, writing, business, mathematics, legal research, and engineering.
- Public REST, MCP, and CLI routing defaults to **hardened** contract policy. Routes expose selected methods, reasons, contract requirements, and unresolved work; review them before applying a procedure.
- SolKraft is advisory. The host supplies tools, runtime authority, and verification. `execution_authorized` remains `false`.
- Compact metadata is loaded before full instruction bodies. Seven read-only MCP tools provide search, routing, skill/resource retrieval, graph inspection, and contract metadata.
- The full local semantic run completed **373,000 routing calls across all 32 slices** and passed its configured gates. Single-skill decisions: **99.961%**; compound target coverage: **100%**; ordering: **99.655%**; stability: **100%**.
- Exact compound skill sets: **27.697%**, with **233,968 extra selections** and **60,000/100,000 requests without unresolved stages**. Coverage is not precision; passing this generated corpus does not prove perfect arbitrary-language matching, execution, or deployment.
- The console displays actual completed receipts and recorded production-router examples. It performs no simulated or live browser CI. See [semantic validation and limitations](SEMANTIC_ROUTER_PROOF.md) for source identity, methodology, and rerun instructions.

<!-- END SOLKRAFT CURRENT SYSTEM -->


SolKraft gives a host agent reusable procedures and a way to select them for a request. Its console makes those procedures inspectable to people. It is not a hosted autonomous job runner.

## The three layers

`solforge` owns the native selection entrypoint, Python selector/composer, domain indexes, and selection graph. It also appears as a node in that graph. `capability-preserving-execution` supplies the adaptive execution procedure: frame, map, wave, synthesize, act, verify, and finish or escalate. It has decision references rather than a Python scheduler. Specialist skills provide the detailed methods for particular work. The host agent composes these layers within its own available tools and governing instructions.

The service adapters live separately in `solkraft/catalog.py`, `routing.py`, `api.py`, and `mcp_server.py`. They index the packs and expose discovery, routing, and retrieval over Python, REST, and MCP. Capability-preserving execution is currently a catalog node available through discovery or explicit selection; the graph has no conditional edges attached to it. Its application comes from the host's execution instructions, rather than an automatic graph scheduling rule.

## Each UI tab

**Validation:** inspect the completed local semantic receipt and its exact source
identity. Metrics are loaded from `assets/semantic-proof.json`; missing, failed,
or incomplete evidence shows an unavailable state with a retry button. Nothing
counts upward or simulates PASS rows. Select a recorded regression request to
inspect actual production-router output, including a deliberately excluded task.
The button transfers that request to Compose a route; it does not silently call
a server. Custom routing still requires the console's API connection.

The six metrics distinguish calls completed, single-skill decisions, compound
target coverage, target order, stability, and exact skill sets. The precision
note exposes extras and unresolved work. Download the JSON for per-skill detail
or expand the methodology section for gates, limitations, and the local command.

**Discover skills:** keyword-filter the bundled skill names and descriptions, browse in pages, inspect instructions, view the pack's Python files and supporting references, and copy the procedure. An API connection switches discovery to the server catalog and its ranked search. Search starts at page one; the page indicator states which range is visible.

**Compose a route:** load the worked example without a connection, or connect your server and submit a custom objective. Review the ordered stages and their reasons. Open each selected skill to retrieve its instructions. Expand the parser output to see selection traces, exclusions, and unresolved stages. Copy the request to use with your agent. The example is generated at build time by the real Python router and is explicitly labelled; custom routing is a live server request.

**Explore the graph:** inspect conditional relationships between workflow nodes. Filtering reduces the displayed relationship set; it does not reduce the catalog. The display reports how many relationships are shown. Catalog-only nodes are available for discovery and explicit selection without invented dependencies.

## How the semantic parser works

The native Python engine is deterministic rather than an LLM call. It still parses scoped clauses, action rules, concept aliases, domain context, exclusions, quoted instructions, and completed or deferred work, but current routing adds a capability-identity matcher over published capability descriptions and distinctive/unique signatures. Capability identity is evaluated against active clauses; excluded, quoted, deferred, and delivery-only text must not introduce additional capabilities.

Under hardened routing, the compact ContractIndex prefilters candidates before composition using declared contract state, effects, capabilities/resources, typed inputs/outputs, trust, and policy. The composer then preserves requested stage order and bounds selection to the requested maximum, up to 50 skills. After composition, whole-route validation checks contract admissibility, dependencies, and typed dataflow; bounded repair can recompose or repair broken dataflow while retaining unresolved stages when a safe route cannot be formed. Explicit IDs remain available for direct selection.

Graph relationships recommend supporting methods or subsequent work only when their conditions apply. The graph does not grant authority, execute tools, or create a background hook into an agent's internal skill picker. Scores are relative rankings, not confidence probabilities. Complex unfamiliar wording may require review or explicit selection.

For example, “draft pull request” is ambiguous by itself. A request to verify a release before a draft PR belongs to software verification; a request to write the PR description belongs to writing. Established repository-release-gate context can resolve a short follow-up.

## From selection to execution

A human can copy a procedure, or an agent can retrieve it through REST or the seven read-only MCP tools: search, route, get skill, get resource, graph, get skill contract, and get contract index. Retrieve supporting references only when their conditions apply. A copied entrypoint does not magically include its linked files; install the skill pack or retrieve those resources when needed.

The host agent applies capability-preserving execution for substantial work: preserve inputs and scope, map dependencies, batch safe independent operations, keep successful evidence, retry only invalidated work, and inspect the real result. Product-specific and repository contracts remain authoritative. A selected route is advisory and never authorizes publishing, deployment, deletion, sending, or any other effect.

The static site requires no key for browsing, inspection, or the worked example. A custom request requires a running SolKraft server with the applicable API key and CORS configuration. The key stays in the current tab. See [client setup](CLIENTS.md).

The current walkthrough uses large vertical HTML cards. Cards reveal in order once when entering view, and a light pulse travels along each connector before the next stage appears. There is no pause control or continuously looping diagram; reduced-motion users see the complete static flow.
