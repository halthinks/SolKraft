<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolKraft Skill-Contract Program — 6-Sprint Implementation Plan

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
- The six-sprint contract architecture program is implemented through interoperability/hardening; this document now serves as architecture/history and acceptance criteria.

<!-- END SOLKRAFT CURRENT SYSTEM -->


This plan converts the 9-milestone / 81-task roadmap into six execution sprints. It preserves the roadmap's dependencies and architectural invariants while creating a smaller number of gated delivery increments.

## Ownership model

These are **subsystem owner roles**, not invented individual assignees. Each role should map to one accountable engineer/agent lane when work is materialized.

| Owner | Scope |
|---|---|
| **Contract Core** | contract schema, loader, versions, effects, legacy adapters, contract state |
| **Router / SolForge** | semantic routing, composition, route validation, recomposition, dataflow |
| **Capability & Policy** | capability sets, resource scopes, request policy, grants, constraint semantics |
| **Verification & Trust** | evidence, verification, provenance, trust, audit, sandbox boundary |
| **Interfaces** | Python boundary parity, REST, CLI, MCP, generated user-facing contract surfaces |
| **Catalog / CI** | indexing, contribution gates, CI, migration tooling, performance, rollout |

Cross-subsystem changes require the primary owner plus the owner of the boundary being changed. No subsystem may weaken `execution_authorized: false`.

## Priority rules

1. **Correctness before expansion.** Unknown metadata must stop appearing safe before new contract features are added.
2. **Policy before composition optimization.** SolKraft must know which candidates are admissible before using contracts to make richer routes.
3. **Capability sets before auth deprecation.** `AUTH_ORDER` remains compatibility-only until replacement behavior is proven.
4. **Verification before trust claims.** A contract can describe success before SolKraft can claim it verified success.
5. **Stable semantics before interface proliferation.** REST/CLI/MCP are productized only after contract/routing semantics are stable.
6. **Replacement before removal.** Prototype shortcuts are removed only after their replacement has passing evidence.

---

# Sprint 1 — Make contracts truthful

**Goal:** Correct PR #1's unsafe assumptions and establish the stable contract envelope.

**Primary owners:** Contract Core, Router / SolForge  
**Supporting owners:** Interfaces

### Work

**Contract Core**
- SC-001 Make unknown mounted skills opaque
- SC-002 Add explicit contract status model
- SC-003 Remove coarse external-effect exclusion rule
- SC-010 Define Contract v1 JSON Schema
- SC-015 Separate schema version from contract revision
- SC-017 Add sidecar loader and legacy adapter

**Router / SolForge**
- SC-004 Centralize constraint parsing
- SC-005 Add blocked route semantics

**Interfaces**
- SC-006 Enforce `execution_authorized: false` across Python/REST/MCP/CLI

### Sequencing

1. SC-001 → SC-002
2. SC-004 can run in parallel with SC-001/002.
3. SC-010 → SC-015 → SC-017.
4. SC-005 depends on truthful contract state from SC-001.
5. SC-006 runs after route status semantics are stable enough to assert at every boundary.

### Exit criteria

Sprint 1 is not complete until:

- graph-unknown mounted skills are **opaque**, never synthesized as harmless;
- every discovered skill can be classified as declared / legacy / opaque / unsupported / invalid;
- unknown major contract versions fail closed to unsupported;
- denied required stages produce blocked/partially-blocked route states rather than a false matched route;
- quoted/code/deferred constraints still behave compatibly through one parser;
- Python, REST, CLI, and MCP all preserve `execution_authorized: false`;
- all pre-existing routing tests plus new Sprint 1 contract tests pass.

**Gate to Sprint 2:** no new policy-aware routing work lands until unknown skills and route status are truthful.

---

# Sprint 2 — Build Contract v1 and policy-aware routing

**Goal:** Make compact contracts rich enough to constrain selection and move from post-hoc deletion to real admissibility-aware routing.

**Primary owners:** Contract Core, Capability & Policy, Router / SolForge

### Work

**Contract Core**
- SC-011 Add typed inputs and outputs
- SC-012 Introduce namespaced effect model
- SC-013 Add capability and resource requirements
- SC-014 Define declarative verification schema
- SC-016 Bind contracts to procedure digests

**Capability & Policy**
- SC-021 Add structured policy model
- SC-028 Make explicit policy authoritative

**Router / SolForge**
- SC-020 Split semantic context from route policy
- SC-022 Pre-filter inadmissible candidates before composition
- SC-023 Validate complete composed route
- SC-024 Detect producer/consumer breakage
- SC-025 Bounded repair and recomposition
- SC-026 Report blocked stages explicitly
- SC-027 Add structured decision trace

### Sequencing

1. SC-011/012/013/014/016 establish the complete Contract v1 data needed by routing.
2. SC-020 separates semantic context from security/policy data.
3. SC-021 + SC-028 define authoritative policy semantics.
4. SC-022 pre-filters known-invalid candidates.
5. SC-023 validates the whole route.
6. SC-024 handles dependency breakage.
7. SC-025 attempts bounded repair/recomposition.
8. SC-026 produces truthful blocked-stage output.
9. SC-027 exposes the complete decision trace.

### Exit criteria

- structured policy and natural-language inference are separate;
- explicit policy always outranks prose inference;
- a denied skill cannot influence composition;
- a rejected producer cannot leave downstream consumers appearing runnable;
- a safe alternative is selected when one exists;
- no alternative yields an explicit blocked stage;
- route results explain allow/deny/opaque decisions with contract digest and reasons;
- contract evaluation still never grants execution authority;
- public routing tests cover safe alternative, no alternative, broken dependency, explicit policy precedence, unknown effect, and opaque-skill behavior.

**Gate to Sprint 3:** routing must be contract-aware end-to-end before scalar auth is replaced or typed dataflow affects composition.

---

# Sprint 3 — Replace scalar auth and add typed composition

**Goal:** Turn contracts from a safety filter into a capability-composition system.

**Primary owners:** Capability & Policy, Router / SolForge  
**Supporting owner:** Contract Core

### Work

**Capability & Policy**
- SC-030 Create capability model
- SC-031 Define core capability namespace
- SC-032 Implement resource selectors
- SC-033 Aggregate route capability requirements
- SC-034 Demote `AUTH_ORDER` to legacy adapter
- SC-035 Define host capability grant format
- SC-036 Model runtime mediation boundary

**Contract Core**
- SC-040 Normalize input contracts
- SC-041 Normalize output contracts

**Router / SolForge**
- SC-042 Add producer-consumer compatibility
- SC-043 Compose using typed dataflow
- SC-044 Distinguish missing input from irrelevant skill
- SC-045 Represent available / elicitable / unavailable inputs
- SC-046 Augment rather than replace graph relationships
- SC-047 Explain dataflow selection

### Sequencing

1. SC-030/031/032 establish capability/resource semantics.
2. SC-033 aggregates route requirements.
3. SC-034 moves `AUTH_ORDER` out of new-contract enforcement.
4. SC-035/036 formalize the host/runtime permission boundary.
5. SC-040/041 normalize typed artifacts.
6. SC-042 validates producer/consumer compatibility.
7. SC-043 introduces typed compatibility into composition.
8. SC-044/045 make missing prerequisites explicit.
9. SC-046 preserves the semantic graph as evidence rather than replacing it with inferred dependencies.
10. SC-047 exposes why dataflow edges were selected.

### Exit criteria

- new Contract v1 enforcement uses capability/resource sets, not scalar auth ordering;
- network-read does not imply write-local, and unrelated authorities remain orthogonal;
- route output includes aggregate capability/resource requirements;
- host grants are described but never minted by SolKraft;
- typed output from one skill can satisfy a compatible downstream input;
- unsatisfied required inputs block or elicit rather than masquerading as execution-ready;
- graph relationships remain intact and typed dataflow only augments them;
- routing explanations show the producer/output that satisfies downstream inputs;
- existing 100,000-request routing regression remains passing.

**Gate to Sprint 4:** SolKraft must know what a route requires and how stages connect before it can verify route outcomes.

---

# Sprint 4 — Make outcomes verifiable and trust explicit

**Goal:** Add evidence-based verification, provenance, and trust without turning SolKraft into an execution engine.

**Primary owner:** Verification & Trust  
**Supporting owners:** Contract Core, Catalog / CI

### Work

**Verification & Trust**
- SC-050 Implement declarative verifier
- SC-051 Preserve human verification descriptions
- SC-052 Define structured evidence bundle
- SC-053 Add execution/verification result states
- SC-054 Record observed effects
- SC-055 Add trust/provenance states
- SC-056 Bind trust to digests
- SC-057 Add audit events
- SC-058 Prevent trust self-elevation
- SC-059 Define sandbox verifier interface only
- SC-060 Specify executable verifier sandbox requirements

**Catalog / CI migration bootstrap**
- SC-100 Generate initial bundled sidecars
- SC-101 Never promote inferred contracts to reviewed automatically
- SC-102 Add migration report tooling

### Sequencing

1. SC-050/051 define verification semantics.
2. SC-052 creates the evidence envelope.
3. SC-053/054 define result and observed-effect states.
4. SC-055/056 attach trust to exact procedure+contract digests.
5. SC-058 prevents skill-authored self-elevation.
6. SC-057 records immutable-ish decision/evidence references.
7. SC-059/060 establish the future executable-verifier boundary while keeping core SolKraft non-executing.
8. Once trust states exist, SC-100/101/102 can safely bootstrap bundled sidecars as legacy-inferred rather than reviewed.

### Exit criteria

- core verification consumes structured evidence and does not shell out;
- unsupported verification modes fail safely;
- selected / blocked / executed-unverified / verified / verification-failed are distinct states;
- observed effects can be compared with declared effects;
- trust states are visible and bound to contract + procedure digests;
- procedure drift invalidates prior reviewed binding;
- untrusted contracts cannot relax operator policy or promote their own trust;
- bundled migration reports distinguish reviewed from legacy-inferred contracts;
- sandbox requirements explicitly cover timeout, mounts, network, output limits, process limits, path traversal, and secret inheritance;
- no executable verification capability is added to SolKraft core.

**Gate to Sprint 5:** user-facing interfaces may not imply verification/trust semantics until those semantics exist in core.

---

# Sprint 5 — Productize the contract system and enforce it in CI

**Goal:** Make the contract system ordinary and consistent across all user/developer surfaces, while preparing the catalog for scale.

**Primary owners:** Interfaces, Catalog / CI  
**Supporting owners:** all subsystem owners for parity review

### Work

**Interfaces**
- SC-070 Add policy to route API
- SC-071 Expose skill contract endpoint
- SC-072 Expose contract validation endpoint
- SC-073 Expose contract schema endpoint
- SC-074 Add `contract init` CLI
- SC-075 Add validate/lint/show/schema/migrate CLI
- SC-076 Add route grant/deny/strict flags
- SC-077 Return contract summaries over MCP
- SC-078 Publish accurate MCP risk annotations
- SC-079 Preserve read-only MCP boundary
- SC-084 Generate contract metadata in skill docs

**Catalog / CI**
- SC-080 Extend contribution checker with contract cases
- SC-081 Update skill contribution documentation
- SC-082 Add contract checks to local CI
- SC-083 Enable PR CI for contract/schema changes
- SC-090 Build compact contract index
- SC-091 Index effects
- SC-092 Index capabilities
- SC-093 Index input/output types
- SC-094 Index trust state
- SC-095 Cache by contract digest and graph generation
- SC-096 Incremental refresh

### Parallel execution lanes

Sprint 5 is intentionally the widest sprint because the core semantics are already stable. Run in parallel:

- **Lane A — API/CLI:** SC-070–076
- **Lane B — MCP/docs:** SC-077–079, SC-084
- **Lane C — contribution/CI:** SC-080–083
- **Lane D — indexing/performance:** SC-090–096

Each lane must consume the same Contract v1/policy implementation; no interface gets its own semantics.

### Exit criteria

- Python, REST, CLI, and MCP expose the same policy and contract semantics;
- contract validation endpoints/tools are metadata-only and execute nothing;
- MCP remains read-only and does not grow a skill-execution tool;
- contribution PRs can prove contract cases alongside routing cases;
- local CI fails on invalid/schema-drifted contracts;
- GitHub PR CI automatically runs the contract gate for relevant changes;
- generated skill pages separate procedure, inputs/outputs, effects, capabilities, risk, trust, and verification;
- contract/effect/capability/dataflow/trust indexes are compact and lazy-body-safe;
- unchanged contracts avoid reparsing through digest/generation caching;
- incremental refresh only reindexes changed skills/contracts;
- full local CI, installed MCP verification, and 100,000-route regression pass together.

**Gate to Sprint 6:** deprecations are forbidden until every replacement path has CI evidence and boundary parity.

---

# Sprint 6 — Interoperate, harden, and remove prototype shortcuts

**Goal:** Finish scale/interoperability, migrate the system to the replacement architecture, and delete obsolete prototype mechanisms only after proof.

**Primary owners:** Catalog / CI, Contract Core, Router / SolForge  
**Supporting owners:** Interfaces, Capability & Policy, Verification & Trust

### Work

**Interoperability**
- SC-097 Add compact contract export/import
- SC-098 Interoperate with MCP/OpenAPI/tool metadata

**Cleanup / hardening**
- SC-103 Remove duplicate effect parsing
- SC-104 Remove `AUTH_ORDER` from new-contract enforcement
- SC-105 Remove harmless defaults permanently
- SC-106 Retire post-hoc-only filter path
- SC-107 Adopt hardened default after coverage

### Sequencing

1. SC-097/098 prove portable metadata and external declaration adapters.
2. SC-103 removes duplicated parser logic only after shared-parser parity is proven.
3. SC-104 removes scalar auth enforcement only after capability-set parity is proven.
4. SC-105 removes all manufactured harmless defaults after bundled migration coverage is known.
5. SC-106 removes post-hoc-only contract filtering after hybrid routing is the proven sole path.
6. SC-107 flips the hardened default only after reviewed bundled contract coverage and migration reports meet target.

### Exit criteria

The six-sprint program is complete only when:

- every discovered skill has an explicit contract state;
- unknown metadata never becomes an affirmative no-effect claim;
- Contract v1 is portable, versioned, digest-bound, and JSON-Schema validated;
- routing performs pre-admissibility, composition, full-route validation, and bounded repair/recomposition;
- new contracts use capability/resource sets rather than scalar auth;
- typed inputs/outputs participate in composition;
- effects are namespaced and extensible;
- verification is declarative by default and consumes structured evidence;
- trust/provenance are visible and cannot be self-elevated;
- external MCP/OpenAPI/tool metadata is imported as declaration only, never authority;
- API, CLI, MCP, contribution tooling, generated docs, and CI share one semantic model;
- existing 100,000-request routing regression remains passing;
- lazy `SKILL.md` loading remains intact;
- runtime execution remains outside SolKraft;
- `execution_authorized` remains false;
- `AUTH_ORDER`, manufactured harmless defaults, duplicated parsing, and post-hoc-only filtering have been retired from new-contract enforcement;
- hardened mode defaults untrusted mounted skills to opaque and requires reviewed bundled contracts for strong claims.

---

## Program critical path

```text
Truthful unknown state
  -> Contract v1 schema/loader
  -> Structured policy
  -> Pre-filter + route validation + repair
  -> Capability/resource model
  -> Typed composition
  -> Evidence + verification
  -> Trust/digest binding
  -> Interface + CI parity
  -> Migration coverage
  -> Prototype deprecation
  -> Hardened default
```

## Work that can safely run in parallel

- schema fixtures and parser normalization in Sprint 1;
- effect/capability schema and policy model in Sprint 2;
- capability model and typed artifact normalization in Sprint 3;
- verifier/evidence work and trust-state work in Sprint 4 once digests exist;
- all four Sprint 5 productization lanes after core semantics freeze;
- interoperability adapters in Sprint 6 while replacement-path evidence is being collected.

## Work that must remain sequential

- opaque unknown state before hardened policy;
- schema/versioning before sidecar migration;
- structured policy before pre-filtering;
- pre-filtering before recomposition;
- capability model before `AUTH_ORDER` deprecation;
- typed input/output normalization before typed composition;
- evidence schema before verification claims;
- digest binding before reviewed trust;
- replacement CI evidence before any prototype removal;
- migration coverage before hardened default.
