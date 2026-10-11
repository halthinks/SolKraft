<!-- solkraft-doc-sync: contract-aware-v1 | semantic-exact-match | 2026-10 -->

# Verification and trust

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Describe an outcome in ordinary language; SolKraft discovers procedures, composes requested stages, and retrieves selected instructions. The catalog contains **173 bundled skills** across software, research, data, writing, business, mathematics, legal research, and engineering.
- Public REST, MCP, and CLI routing defaults to **hardened** contract policy. Routes expose selected methods, reasons, contract requirements, and unresolved work; review them before applying a procedure.
- SolKraft is advisory. The host supplies tools, runtime authority, and verification. `execution_authorized` remains `false`.
- Compact metadata is loaded before full instruction bodies. Seven read-only MCP tools provide search, routing, skill/resource retrieval, graph inspection, and contract metadata.
- The current acceptance gate requires **473,000 production-router calls across all 32 slices**: 173,000 single-skill cases, 100,000 clarified compound requests, 100,000 unchanged original compound diagnostics, and 100,000 stability executions.
- Acceptance requires **100% of 111,000 eligible single-skill exact selections and 62,000 hardened policy decisions**, plus **100% holdout, per-skill, compound exact-set, coverage, order, and stability results**, with **zero extra selections and zero unresolved stages** in clarified compound requests. Clarifications preserve every original topic and target; the original corpus remains a separate diagnostic.
- The historical 373,000-call run reached **27.697% compound exact matching** and is rejected as evidence of completion. Current results belong to the source-bound aggregate receipt; the October 10 full local CI passed all 22 steps and all 15 semantic gates across 32/32 receipts. Generated-corpus success does not establish perfect arbitrary-language matching, execution, or deployment.
- The console displays actual completed receipts and recorded production-router examples. It performs no simulated or live browser CI. See [semantic validation and limitations](SEMANTIC_ROUTER_PROOF.md) for source identity, methodology, and rerun instructions.

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
