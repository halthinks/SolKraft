<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolKraft Skill-Contract Architecture Roadmap

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
- The six-sprint contract architecture program is implemented through interoperability/hardening; this file is retained as architecture/history and acceptance criteria.

<!-- END SOLKRAFT CURRENT SYSTEM -->


Status: proposed implementation roadmap derived from the skill-contract research review and current merged PR #1 behavior.

## Purpose

SolKraft should evolve from a semantic skill router into a semantic skill operating system whose nodes are typed, composable, constrainable, and verifiable capability components.

The target pipeline is:

```text
objective
  -> semantic retrieval
  -> contract admissibility
  -> composition
  -> route-level validation
  -> advisory route with required capabilities
  -> host-side runtime mediation
  -> external execution
  -> evidence
  -> contract verification
```

SolKraft must remain advisory. It may describe required authority, but it must never mint or imply authority. `execution_authorized` remains `false`.

## Non-negotiable invariants

1. Semantic relevance, admissibility, execution authority, and verification remain separate layers.
2. Missing metadata means unknown, never safe.
3. Contracts constrain selection; they do not grant permission.
4. Full `SKILL.md` bodies remain lazily loaded after selection.
5. Contract evaluation must not execute arbitrary code.
6. Explicit structured policy outranks natural-language inference.
7. A rejected skill may invalidate a route; post-filter deletion alone is not sufficient.
8. Unknown contract majors fail closed to `unsupported` or `opaque`.
9. Procedure and contract digests must bind reviewed metadata to the exact skill body.
10. SolKraft remains a capability-discovery/composition system, not a general authorization platform.

## Current state

PR #1 introduced:
- `solkraft/contracts.py`
- compact contract fields: inputs, side effects, auth scope, test contract
- natural-language exclusion detection
- an auth ceiling
- post-composition skill rejection
- `execution_authorized: false`
- contract tests for quoted exclusions, read-only inference, side-effect rejection, and auth ceilings

That prototype is useful, but it has four important architectural defects to correct before expanding it:

- `catalog_graph()` currently manufactures harmless defaults for graph-unknown mounted skills.
- `AUTH_ORDER` treats orthogonal powers as a total ordering.
- post-composition deletion can leave invalid or incomplete routes.
- fixed effect verbs risk becoming a rigid global ontology.

## Target data model

A v1 skill contract should be a versioned sidecar:

```text
my-skill/
  SKILL.md
  contract.yaml
  references/
  scripts/
  assets/
```

Core fields:

```yaml
schema_version: "1.0"
skill_id: repository-inspect
contract_revision: 1

inputs:
  - name: repository
    required: true
    schema:
      type: string

outputs:
  - name: inspection_report
    schema:
      type: object

effects: []

authority:
  capabilities:
    - fs.read
    - repo.read
  resources:
    - "repo:${repository}"
  requires_confirmation: false

risk:
  external: false
  destructive: false
  idempotent: true
  reversible: true

verification:
  mode: declarative
  checks:
    - id: report-present
      type: artifact_exists
      artifact: inspection_report

provenance:
  declaration: author
  entrypoint_digest: "sha256:..."

extensions: {}
```

The canonical portable validation format should be JSON Schema, with YAML as the human-authored representation.

## Milestones

### M0 — Correct the prototype before expanding it

Goal: remove misleading safety assumptions and preserve the useful parts of PR #1.

Work:
- **SC-001** Make graph-unknown mounted skills `opaque`; stop manufacturing `side_effects: []` and `auth_scope: none`.
- **SC-002** Add explicit contract status values: `declared`, `legacy`, `opaque`, `unsupported`, `invalid`.
- **SC-003** Stop treating any `external-effect` skill as conflicting with every excluded effect.
- **SC-004** Centralize effect/exclusion parsing so `contracts.py` and the composer cannot drift.
- **SC-005** Add route status capable of `partially_blocked` / `blocked`; do not claim `matched` when a required stage is emptied.
- **SC-006** Keep `execution_authorized: false` as an invariant test across Python, REST, CLI, and MCP.

Acceptance:
- Unknown mounted skills never appear as provably harmless.
- Existing PR #1 tests remain passing.
- A denied skill can no longer silently disappear while leaving an invalid route marked matched.

Primary files:
- `solkraft/contracts.py`
- `solkraft/routing.py`
- `tests/test_contracts.py`
- routing/composer tests

### M1 — Contract v1 as a stable data product

Goal: define what a contract is independently of routing implementation.

Add:
- `solkraft/contract_schema.py`
- `solkraft/contract_loader.py`
- `solkraft/schemas/skill-contract-v1.json`
- compatibility facade in `solkraft/contracts.py`

Work:
- **SC-010** Define canonical JSON Schema for Contract v1.
- **SC-011** Add typed inputs and outputs.
- **SC-012** Add namespaced effect identifiers plus stable risk attributes.
- **SC-013** Add capability requirements and resource scopes.
- **SC-014** Add declarative verification schema.
- **SC-015** Add schema version + independent contract revision.
- **SC-016** Add contract and entrypoint SHA-256 digests.
- **SC-017** Add strict core fields with explicit `extensions` for ecosystem growth.

Acceptance:
- Every discovered skill receives exactly one contract state.
- Unknown major versions become `unsupported`, never safe.
- Invalid contracts never silently downgrade into no-effect declarations.
- JSON Schema validation is reproducible outside Python.

### M2 — Contract-aware route construction

Goal: move from post-hoc deletion to hybrid admissibility and route validation.

Target flow:

```text
retrieve candidates
  -> pre-composition contract filter
  -> compose
  -> route-level validation
  -> bounded repair/recomposition
  -> route result
```

Work:
- **SC-020** Split semantic `context` from security/authority `policy`.
- **SC-021** Add explicit request policy: granted capabilities, denied effects, opaque-skill policy.
- **SC-022** Pre-filter known inadmissible candidates before composition.
- **SC-023** Validate complete composed routes after composition.
- **SC-024** Detect broken producer/consumer chains after rejection.
- **SC-025** Add bounded recomposition with rejected candidates excluded.
- **SC-026** Add blocked-stage reporting when no admissible replacement exists.
- **SC-027** Add structured per-skill contract decision trace.
- **SC-028** Make explicit structured policy authoritative over prose inference.

Acceptance:
- A denied deployment skill does not influence composition.
- If a safe substitute exists, it is selected.
- If no valid substitute exists, the route is explicitly blocked.
- A removed producer cannot leave a consumer stage pretending to be runnable.

Primary files:
- `solkraft/routing.py`
- `solkraft/constraint_parser.py`
- `solkraft/contract_policy.py`
- `solkraft/route_validation.py`
- SolForge composer integration

### M3 — Replace scalar auth with real capability requirements

Goal: model authority as a multidimensional set, not a ladder.

Deprecate as enforcement primitive:

```text
none < read < write-local < network < external-effect
```

New model:

```text
required_capabilities <= live_granted_capabilities
and resource scopes must match
```

Work:
- **SC-030** Introduce `solkraft/capabilities.py`.
- **SC-031** Define core capabilities such as `fs.read`, `repo.read`, `local.write`, `net.connect`, `deployment.write`.
- **SC-032** Add resource selectors such as `repo:...`, `host:...`, `environment:...`.
- **SC-033** Add aggregate route capability requirements.
- **SC-034** Keep `AUTH_ORDER` only as a legacy compatibility adapter.
- **SC-035** Add host-facing capability grant format.
- **SC-036** Test grant revocation/staleness assumptions: route selection is never treated as runtime permission.

Acceptance:
- Network read no longer implies local-write authority.
- New contracts never depend on `AUTH_ORDER`.
- Runtime hosts can compare contract requirements against a concrete live grant.

### M4 — Typed dataflow composition

Goal: make contracts a capability multiplier, not only a safety layer.

Work:
- **SC-040** Normalize typed input declarations.
- **SC-041** Normalize typed output declarations.
- **SC-042** Add producer/consumer compatibility checks.
- **SC-043** Allow composition based on compatible outputs feeding downstream inputs.
- **SC-044** Distinguish missing-required-input from semantically irrelevant.
- **SC-045** Mark inputs as available, elicitable, or unavailable.
- **SC-046** Preserve graph relationships while augmenting them with typed dataflow.
- **SC-047** Add route explanation for why one skill satisfies another skill's input.

Acceptance:
- SolKraft can build valid chains from typed artifacts even when every relationship is not manually hard-coded as an edge.
- A route with unsatisfied required input is blocked or requests elicitation rather than pretending to be runnable.

### M5 — Verification, evidence, provenance, and trust

Goal: make success machine-checkable without turning contracts into executable code.

Add:
- `solkraft/contract_verify.py`
- `solkraft/evidence.py`
- `solkraft/audit.py`
- `solkraft/sandbox.py` as an interface only

Work:
- **SC-050** Replace prose-only test contracts with structured declarative checks.
- **SC-051** Preserve human-readable verification descriptions alongside machine checks.
- **SC-052** Define evidence bundles returned by execution hosts.
- **SC-053** Add result states: selected, blocked, executed-unverified, verified, verification-failed.
- **SC-054** Add observed-effect evidence.
- **SC-055** Add trust states: bundled-reviewed, signed, operator-trusted, local-unreviewed, legacy-inferred, opaque, invalid.
- **SC-056** Bind trust to contract and procedure digests.
- **SC-057** Record route/policy/contract/evidence digests in audit events.
- **SC-058** Ensure untrusted contract declarations cannot relax operator policy.
- **SC-059** Keep executable verification behind a separately trusted sandbox host interface.
- **SC-060** Add timeout, mount, network, output-size, and secret-inheritance requirements for any future executable verifier adapter.

Acceptance:
- Core SolKraft verification never shells out because a contract says to.
- Procedure changes invalidate stale reviewed contract trust.
- A skill claiming no effects is treated as an assertion with a trust level, not proof.

### M6 — API, CLI, MCP, contribution workflow, and CI

Goal: make contract-aware behavior the ordinary developer workflow.

API:
- **SC-070** Add structured `policy` to `POST /v1/route`.
- **SC-071** Add `GET /v1/skills/{id}/contract`.
- **SC-072** Add `POST /v1/contracts/validate`.
- **SC-073** Add `GET /v1/contract-schema`.

CLI:
- **SC-074** Add `solkraft contract init`.
- **SC-075** Add `contract validate`, `lint`, `show`, `schema`, `migrate`.
- **SC-076** Add route flags `--grant`, `--deny-effect`, `--strict-contracts`.

MCP:
- **SC-077** Return compact contract summaries in structured route results.
- **SC-078** Publish accurate read-only/risk annotations for SolKraft's own MCP tools where the SDK supports them.
- **SC-079** Preserve read-only MCP semantics; do not add skill execution to SolKraft MCP.

Contribution + CI:
- **SC-080** Extend `scripts.check_contribution` with contract cases.
- **SC-081** Update `docs/SKILL_CONTRIBUTIONS.md` for `contract.yaml`.
- **SC-082** Add contract/schema drift to `scripts.local_ci`.
- **SC-083** Add PR-triggered CI for contract and schema changes.
- **SC-084** Generate contract sections in skill documentation pages.

Acceptance:
- Python, REST, MCP, and CLI expose the same policy semantics.
- Contract validation never executes the skill.
- Contract drift fails before merge.

### M7 — Scale and interoperability

Goal: keep routing cheap as the catalog grows from hundreds to thousands of skills.

Work:
- **SC-090** Add compact contract index.
- **SC-091** Add inverted effect index.
- **SC-092** Add inverted capability index.
- **SC-093** Add typed input/output indexes.
- **SC-094** Add trust-state index.
- **SC-095** Cache by contract digest and graph generation.
- **SC-096** Incrementally refresh only changed contracts/skills.
- **SC-097** Export/import contract metadata without loading procedure bodies.
- **SC-098** Map MCP/OpenAPI/tool-schema metadata into SolKraft contract summaries where semantics are trustworthy enough to translate.

Acceptance:
- Full procedure bodies remain out of the routing hot path.
- Route cost is dominated by a candidate subset rather than total catalog size.
- External metadata is treated as declarations, not authority.

### M8 — Migration, hardening, and cleanup

Goal: retire prototype shortcuts after the replacement architecture is proven.

Migration modes:
- `legacy`: selectable without explicit safety constraints; status is visible.
- `warn`: selectable with warnings, cannot claim harmlessness.
- `strict`: opaque/legacy skills cannot satisfy explicit authority/effect requirements.
- future hardened default: reviewed bundled skills declared; untrusted mounted skills opaque.

Work:
- **SC-100** Generate initial sidecars for bundled skills from existing graph metadata where defensible.
- **SC-101** Mark inferred contracts `legacy-inferred`, not reviewed.
- **SC-102** Add migration tooling and reports for all bundled skills.
- **SC-103** Remove duplicated effect parsing after the shared parser is live.
- **SC-104** Remove `AUTH_ORDER` from new-contract enforcement after capability-set parity is proven.
- **SC-105** Remove manufactured harmless defaults from catalog graph permanently.
- **SC-106** Remove post-hoc-only filtering path after hybrid routing is proven.
- **SC-107** Require reviewed bundled skills to carry valid v1 contracts before hardened mode becomes default.

Acceptance:
- No current skill silently changes from unknown to safe.
- Legacy compatibility remains explicit and measurable.
- Deprecated prototype mechanisms have replacement tests before removal.

## Effect model

Do not keep a single closed enum such as:

```text
deploy, send, merge, purchase, ...
```

Use a small stable core plus namespaced identifiers:

```text
fs.write
fs.delete
repo.commit
repo.push
repo.merge
deployment.release
deployment.rollback
messaging.send
billing.purchase
identity.revoke
secret.rotate
artifact.publish
```

Each effect may also declare broad attributes:

```text
read
mutation
external
destructive
reversible
idempotent
open-world
```

Policy can therefore deny a precise identity (`deployment.*`) or a broad risk property (`external=true`).

## Route result contract

The route result should evolve toward:

```json
{
  "selection_status": "partially_blocked",
  "selected": ["repository-inspect"],
  "blocked_stages": [
    {
      "stage": 2,
      "reason": "No deployment-free implementation satisfies the request"
    }
  ],
  "required_capabilities": ["fs.read", "repo.read"],
  "denied_effects": ["deployment.*"],
  "contract_decisions": {
    "repository-inspect": {
      "status": "allowed",
      "contract_digest": "..."
    },
    "deploy-release": {
      "status": "denied",
      "reasons": ["effect deployment.release denied by policy"]
    }
  },
  "execution_authorized": false
}
```

## Test and evaluation matrix

Every milestone must add tests to the public routing boundary, not only internal helpers.

Required suites:

- schema: valid v1, missing fields, unknown major, malformed YAML, excessive size, duplicate capability, extension preservation
- legacy conversion: `effect:false`, `exit_evidence`, opaque mounted skill behavior
- capability policy: exact subset, resource mismatch, revoked grant, no scalar-order assumptions
- effects: namespaced/wildcard/category denies, unknown effect handling
- natural-language constraints: quoted/code immunity, negation, double negative, Unicode punctuation, long-distance negation
- explicit policy precedence over NLP inference
- composition: rejected producer, downstream invalidation, safe alternative, no-alternative blocked stage
- inputs/outputs: required/optional, producer satisfies consumer, elicitable input
- verification: pass/fail/missing/malformed evidence, unsupported verifier, false-success prevention
- sandbox adapter contract: timeout, output cap, denied network, path traversal, secret inheritance
- trust: body digest drift, untrusted contract cannot relax policy
- boundary parity: Python/REST/MCP/CLI
- regression: preserve existing 100,000-request routing battery and add orthogonal contract-policy cases

Important distinction:

```text
routing tests prove selection behavior
verification tests prove declared postconditions over evidence
real task demonstrations prove procedural usefulness
none of these alone proves operational safety
```

## CI target

The gate should become:

```text
schema validation
-> semantic contract lint
-> unit tests
-> contract policy matrix
-> routing tests
-> contribution targeted cases
-> existing 100,000-route regression
-> package build
-> installed MCP test
-> generated artifact drift check
```

External-effect skills must be tested using mocks, emulators, fixtures, or evidence samples. CI must not perform the real effect merely to validate metadata.

## Contribution workflow target

A complete skill contribution should eventually include:

- `SKILL.md`
- `contract.yaml`
- provenance/license record
- semantic graph registration
- routing rules/examples
- contract policy cases
- meaningful task tests
- generated docs/catalog artifacts
- candidate hashes and receipts

Review should separately ask:
- Is this skill semantically selected correctly?
- Is the contract complete and believable?
- Does the procedure actually work?
- Do runtime claims have evidence?
- Is the declaration trusted enough for the intended policy?

## File map

Planned new modules:

```text
solkraft/contract_schema.py
solkraft/contract_loader.py
solkraft/effects.py
solkraft/capabilities.py
solkraft/constraint_parser.py
solkraft/contract_policy.py
solkraft/route_validation.py
solkraft/contract_verify.py
solkraft/evidence.py
solkraft/audit.py
solkraft/sandbox.py
solkraft/schemas/skill-contract-v1.json
```

Planned major modifications:

```text
solkraft/contracts.py
solkraft/routing.py
solkraft/catalog.py
solkraft/api.py
solkraft/mcp_server.py
solkraft/__main__.py
solkraft/skillpacks/solforge/references/selection-graph.json
scripts/check_contribution.py
scripts/local_ci.py
docs/SKILL_CONTRIBUTIONS.md
VALIDATION.md
.github/workflows/tests.yml
```

## Deprecation ledger

Do not remove anything until its replacement is proven.

| Existing mechanism | Disposition |
|---|---|
| `AUTH_ORDER` | keep as compatibility adapter, then remove from new-contract enforcement |
| fixed `EFFECTS` tuple | replace with namespaced registry + attributes |
| duplicate exclusion/effect parsing | consolidate into one normalized parser |
| graph-unknown skills defaulted to harmless | remove immediately; replace with `opaque` |
| post-composition deletion as sole enforcement | replace with pre-filter + route validation + recomposition |
| prose-only `test_contract` as machine contract | retain as description, add declarative checks |
| policy hidden inside generic `context` | split into typed semantic context + typed policy |
| contract metadata as implicit authority | prohibited permanently |
| executable verification inside core SolKraft | prohibited; sandbox host adapter only |

## Definition of done for the program

The program is complete when all of the following are true:

1. Every skill is in an explicit contract state.
2. Unknown metadata never becomes an affirmative no-effect claim.
3. Contracts are versioned, portable, digest-bound, and validated by JSON Schema.
4. Routing performs pre-admissibility, composition, full-route validation, and repair/recomposition.
5. Scalar auth is no longer the enforcement model for new contracts.
6. Typed inputs/outputs participate in composition.
7. Effects are extensible and namespaced.
8. Verification is declarative by default and consumes structured evidence.
9. Trust/provenance are visible and cannot be self-elevated by a skill.
10. API, CLI, MCP, contribution tooling, generated docs, and CI expose consistent semantics.
11. Existing routing behavior remains regression-tested.
12. Lazy loading of `SKILL.md` is preserved.
13. Runtime execution remains outside SolKraft.
14. `execution_authorized` remains false at the SolKraft boundary.
15. Deprecated PR #1 shortcuts are removed only after replacements are proven.

## External design references captured by the research

The roadmap is informed by:
- Agent Skills progressive disclosure and skill-directory conventions
- Model Context Protocol tool schemas and behavioral annotations
- JSON Schema Draft 2020-12
- Saltzer & Schroeder protection principles, especially least privilege, fail-safe defaults, and complete mediation
- capability-security literature separating authority possession from capability description
- Hoare-style precondition/postcondition reasoning for verification contracts
- OpenAPI extension/namespace patterns
- Zanzibar as an example of why SolKraft should not become a full centralized authorization service

The architectural rule that ties these together is:

> Contracts describe what a skill requires and promises. Policy decides whether the route is admissible. The host decides whether execution is authorized. Evidence decides whether success can be claimed.
