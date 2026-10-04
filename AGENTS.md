<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# SolKraft agent guide

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


This guide applies to every person and agent contributing here. SolKraft makes skills easy to discover and retrieve; the host agent remains responsible for understanding the user's goal, applying relevant procedures, and carrying out authorized work. Use these instructions together with the selected skills. A skill adds useful method, not authority.

## The work standard

Deliver the user's requested outcome with the smallest dependable change. Preserve existing work and public behavior. Inspect relevant source and tests before changing code, verify the real behavior after changing it, and tell the user what is proven, what remains uncertain, and what they can do next. Do not turn routine work into ceremony or make users name internal tools and skill IDs.

## Use skills naturally

Skills are part of how SolKraft agents work, not an optional catalog showcase. At task start and whenever the work moves to a materially different stage, silently assess whether an available skill gives a useful procedure or domain constraint. Load and follow the best match without waiting for the user to request it. Keep this selection natural; mention skill names only when useful for explaining a decision or evidence.

- Choose the primary skill for the actual deliverable: research, implementation, test/release gate, engineering study, writing, data, business, or another domain. Read that skill's `SKILL.md` and follow its procedure.
- For a substantial task with unclear or multiple stages, use the bundled SolForge selector/composer as a routing aid. For a clear specialist task or a simple request, load the obvious skill directly and skip routing overhead.
- Add a supporting skill only when it contributes distinct guidance. Do not stack equivalent wrappers or load every skill. Load referenced material only when the selected skill's conditions call for it.
- In long-running goals, continue applying the relevant skill across autonomous continuations. Reassess only when the objective, stage, evidence, or constraints change; do not wait for the user to repeat the skill name.
- Translate skill procedures into the current repository and user context. Reuse completed evidence, stop when acceptance is demonstrated or a real blocker remains, and keep progress updates focused on new findings.
- Skills guide how to do work; they do not override the user's intent, repository contracts, safety controls, or action-specific authorization. A route never authorizes deployment, sending, deletion, publishing, purchase, or other effects.
- Make collaboration accessible: write plainly, adapt detail to the user's familiarity, define unfamiliar terms when they matter, preserve the user's full request, and explain assumptions and limitations without blame. Do not make users learn SolKraft internals to get good work.

## Engineering Constraints V1

Read and apply the complete [ENGINEERING_CONSTRAINTS_V1.json](ENGINEERING_CONSTRAINTS_V1.json) before source changes, architecture work, refactors, and review. It is the authoritative procedure; the guidance below explains its application.

Apply this engineering method to source changes, architecture work, refactors, and global review. It is a set of design constraints, not a mechanical checklist. When principles conflict, prefer the choice that lowers future change cost and reduces how many concepts a maintainer must understand at once in this codebase. If a different choice is better locally, document the concrete reason and evidence in the durable review.

### Design for local reasoning

- **Separation of concerns and single responsibility:** keep one coherent reason to change in each part. Keep UI, domain rules, persistence, and infrastructure distinct unless evidence shows that a simpler local design lowers future cost.
- **Encapsulation and explicit boundaries:** expose small, stable contracts; hide implementation details. Put policy behind appropriate abstractions and have callers depend on the contract, not incidental implementation.
- **Cohesion and coupling:** keep things that change together close; connect independent parts through narrow, explicit interfaces. Prefer local knowledge and small collaborator surfaces.
- **One authority per fact:** maintain one authoritative representation of each durable fact. Derive or reference other views; cache only with explicit semantics. Do not create competing truths or copy the same domain knowledge into multiple owners.
- **DRY with judgment:** consolidate repeated knowledge, not merely similar-looking code. Avoid over-DRY designs that make independent concerns change together.
- **KISS and YAGNI:** choose the simplest design that meets demonstrated requirements. Do not add speculative features, frameworks, extension hooks, or indirection for hypothetical future use.
- **Composition and disciplined extension:** assemble behavior from focused pieces. Extend at a stable boundary when the same change axis is demonstrated; do not pre-build a framework or add inheritance depth without a proven need.
- **Make invalid states hard to represent:** use schemas, types, constraints, state transitions, contracts, and acceptance gates to enforce invariants at the boundary. Fail fast with useful errors. Correctness should not depend only on worker memory, an instruction, or a fragile call order when code can enforce it.
- **Optimize for change:** make obsolete behavior easy to remove; compose focused tools through explicit contracts.

### Change sequence when a boundary needs repair

A behavior-changing patch that needs a structural or boundary repair follows this order:

1. Identify the current behavior, the single authority, the invariant, and the caller boundary. Read relevant tests and preserve unrelated changes.
2. Write a focused failing test for the requested behavior and identify the existing behavior that must remain intact.
3. Make the smallest behavior-preserving boundary repair first. Do not add a parallel path around an abstraction merely to make the request pass; if the abstraction is wrong, repair the abstraction.
4. Verify that the refactor alone preserves existing behavior. Keep this proof independently reviewable and tied to the exact candidate source revision.
5. Implement the behavior change after that proof, then test its new observable behavior and relevant failure/boundary cases.
6. If structural and behavioral changes genuinely cannot be separated, explain the dependency and provide explicit evidence for both preserved and changed behavior. Never claim an unchanged baseline from inspection alone.

Review findings must point to the concrete boundary, competing authority, invariant, bypass path, speculative complexity, or future-change-cost impact. A principle name by itself is not evidence. Block changes that introduce a bypass around the suitable abstraction, duplicate authority, instruction-only correctness where an enforceable boundary fits, unproven structural/behavioral bundling, or speculative architecture without demonstrated need. These are evidence-based constraints, not slogans; record a reasoned exception when applying one literally would increase the cost in this codebase.

## Product and compatibility boundaries

- SolKraft is a read-only discovery and routing service. It returns skill metadata and selected instruction text; it does not execute instructions, run shells, or grant effect authority.
- Keep REST and MCP surfaces aligned. Add capabilities compatibly. Do not rename/remove existing tools, routes, fields, defaults, or error behavior without an approved migration decision.
- Preserve the publication scope and provenance for bundled skills. Do not add private skill roots or redistribute third-party material without checking rights and required notices.
- Never commit credentials, local machine paths, private evidence, or API keys.

## Architecture map

- `solkraft/catalog.py` indexes bounded `SKILL.md` frontmatter and reads a body only when requested by ID. Keep path containment, symlink, size, safe-YAML, and publication-scope protections.
- `solkraft/routing.py` composes ordered advisory routes from the bundled graph and metadata fallback. It must return `execution_authorized: false`.
- `solkraft/api.py` provides the authenticated REST interface and mounts MCP. `/healthz` is public; `/v1/*` and `/mcp` require an operator key by default.
- `solkraft/mcp_server.py` exposes `search_skills`, `route_request`, `get_skill`, `get_skill_resource`, and `get_selection_graph`.
- `solkraft/skillpacks/` contains the curated bundle. `docs/` is the static GitHub Pages console. `tests/` exercise catalog, routing, API, MCP, and bundle boundaries.

## Development and verification

1. Read the relevant implementation, tests, and contracts before changing code. Locate the real entrypoint and trace the affected caller path.
2. For behavior changes, write the failing test first, then implement the smallest coherent change. Keep tests focused on observable contracts and failure boundaries.
3. Run `python -m pytest -q` and `python -m compileall -q solkraft` for Python edits. For JavaScript changes, run `node --check docs/assets/app.js` when available and exercise the UI with the local API. Record exact commands and results.
4. Inspect `git diff --check`, the full diff, and `git status --short`. Review scope, compatibility, privacy, skill provenance, and direct evidence before calling work complete.
5. Distinguish source integration, test execution, release readiness, and a live hosted deployment. A passing local suite does not prove production availability.

Before publishing source/UI changes, run `python -m scripts.local_ci` in an environment with the development dependencies and Node.js installed. It generates the console and plugin archive, builds and exercises the installed wheel, and writes `build/local-ci.json`. Review and commit the generated static files. Automatic GitHub build/test runs are disabled; Pages uploads these files, and the verification workflow is manual. Use the same gate on Windows and Linux; only claim platforms actually executed.

Useful commands:

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
python -m compileall -q solkraft
python -m solkraft api
```

## API, MCP, and browser safety

REST endpoints: `GET /v1/skills`, `GET /v1/skills/{id}`, `POST /v1/route`, and `POST /v1/refresh`. MCP exposes the same read-only search, route, and selected-skill retrieval. Keep route caps and validation aligned. Never expose host paths in catalog metadata.

Use safe YAML parsing; never evaluate skill content. Confine resolved files to configured roots and reject unsafe symlinks and oversized entrypoints. Compare bearer credentials in constant time; do not log them. Restrict CORS to configured origins. Do not persist browser keys to storage, cookies, URLs, analytics, or issues. Render returned skill text as text, never executable HTML or Markdown. Keep UI states clear for disconnected, loading, empty, error, and cold-start conditions.

Extra skill roots are an operator-controlled trust boundary. Never point a public service at personal/private directories. The default server binds locally; use the host-provided `PORT` only for hosted services. Never ship a default key. Free hosted services may sleep and cold-start; do not promise uptime or a production SLA.

## Skill contributions

For any new or changed skill integration, follow the complete [skill contribution contract](docs/SKILL_CONTRIBUTIONS.md). A skill-only submission is incomplete: include semantic-core registration, discriminating rules/vocabulary, justified relationships, authored automatic-routing cases, provenance, procedure/helper evidence, necessary parser changes, and generated catalog/UI artifacts. Run `python -m scripts.check_contribution contributions/<manifest>.json --full` after the final source changes. Require targeted cases, the complete 100,000-request routing regression, and installed package/plugin checks to pass. Do not force the skill ID to conceal selection failures or equate routing simulations with task execution quality.

A proposed skill should describe a distinct user intent, recognizable cues, prerequisites, procedure, output, stop conditions, safety boundaries, and relation to existing skills. Keep instructions composable and concise enough to load when relevant, but complete enough to perform the work reliably. Include tests/examples for when routing should and should not select it. Review authorship, license, attribution, and redistribution rights before bundling.

## Pull request checklist

- [ ] One coherent user-visible change; existing callers and defaults remain compatible.
- [ ] Tests were added first for behavior changes and exact validation commands/results are recorded.
- [ ] REST and MCP contracts remain aligned; routing grants no execution authority.
- [ ] Engineering constraints were applied with evidence; exceptions explain local trade-offs.
- [ ] No private paths, credentials, unreviewed skill material, or unsupported release claims.
- [ ] UI treats all returned content as untrusted text.
- [ ] `git diff --check` is clean and limitations are stated.
