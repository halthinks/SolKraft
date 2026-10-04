<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Verification and trust

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
- Trust remains external and digest-bound; imported declarations, inferred sidecars, and metadata adapters never self-elevate to trusted execution authority.

<!-- END SOLKRAFT CURRENT SYSTEM -->


SolKraft separates five different claims that agent systems often collapse together:

1. **Selected** — the router thinks a capability belongs in the route.
2. **Admissible** — the contract and route policy allow that capability to sit on the route.
3. **Executed** — an external host says it actually ran the skill.
4. **Verified** — declarative checks pass over evidence bound to the exact selected contract and procedure.
5. **Trusted** — an external digest-bound review record says the contract/procedure pair has been reviewed to a stated trust level.

None of these grants execution authority. SolKraft remains advisory and continues to return `execution_authorized: false`.

## Evidence envelope

An execution host can return structured evidence containing:

- skill ID
- selected contract SHA-256
- selected `SKILL.md` SHA-256
- artifact metadata
- observed effects
- named host checks
- structured result fields
- an optional opaque host receipt

The verifier consumes that object only. It does not read arbitrary paths, run commands, access the network, or inherit host secrets.

## Declarative checks

Core check types are intentionally small:

- `artifact_exists`
- `field_present`
- `field_equals`
- `check_equals`
- `observed_effects_subset`

Unsupported check types fail verification. A contract with no machine checks can still carry a human-readable verification description, but execution evidence for it is reported as `executed-unverified`, not `verified`.

## Result states

The shared state vocabulary is:

- `selected`
- `blocked`
- `executed-unverified`
- `verified`
- `verification-failed`

A digest mismatch is a verification failure because the evidence no longer proves the exact capability definition that was selected.

## Trust

Trust states are:

- `bundled-reviewed`
- `signed`
- `operator-trusted`
- `local-unreviewed`
- `legacy-inferred`
- `opaque`
- `invalid`

A skill cannot elevate its own trust with frontmatter, `provenance`, or contract fields. Trusted states come only from `solkraft/trust-bindings.json`, and each entry must match both the contract digest and entrypoint digest. Editing either file automatically makes the binding stop matching.

## Audit receipts

Route audit receipts deterministically bind:

- objective
- selected skill IDs
- selection status
- normalized policy
- contract and procedure digests
- trust states
- capability/resource requirements
- blocked stages

Verification receipts additionally bind the evidence digest and declarative check results.

## Executable verifier boundary

Core SolKraft intentionally has no executable verifier runner. `solkraft.sandbox` defines the requirements any future independently trusted host adapter must enforce: bounded timeout, network off by default, no inherited secrets, bounded output/processes, and explicit mounts.

Adding an executable adapter later must not turn a contract string into a shell command inside core SolKraft.


## Hardened public defaults

REST, MCP, and the CLI now default to the `hardened` contract mode. Hardened mode rejects opaque contracts while continuing to expose legacy-inferred bundled contracts as warnings so existing proven routing remains usable. The Python library keeps legacy-compatible defaults unless the caller explicitly supplies a stricter policy.

This is different from claiming every bundled procedure has been reviewed. The CI receipt `build/hardening.json` reports digest-bound reviewed coverage separately. A generated or inferred sidecar never counts as reviewed, and hardened public routing does not fabricate that evidence.
