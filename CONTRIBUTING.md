<!-- solkraft-doc-sync: contract-aware-v1 | semantic-exact-match | 2026-10 -->

# Contributing to SolKraft

<!-- BEGIN SOLKRAFT CURRENT SYSTEM -->
## Current SolKraft system — October 2026

- Describe an outcome in ordinary language; SolKraft discovers procedures, composes requested stages, and retrieves selected instructions. The catalog contains **173 bundled skills** across software, research, data, writing, business, mathematics, legal research, and engineering.
- Public REST, MCP, and CLI routing defaults to **hardened** contract policy. Routes expose selected methods, reasons, contract requirements, and unresolved work; review them before applying a procedure.
- SolKraft is advisory. The host supplies tools, runtime authority, and verification. `execution_authorized` remains `false`.
- Compact metadata is loaded before full instruction bodies. Seven read-only MCP tools provide search, routing, skill/resource retrieval, graph inspection, and contract metadata.
- The current acceptance gate requires **473,000 production-router calls across all 32 slices**: 173,000 single-skill cases, 100,000 clarified compound requests, 100,000 unchanged original compound diagnostics, and 100,000 stability executions.
- Acceptance requires **100% of 111,000 eligible single-skill exact selections and 62,000 hardened policy decisions**, plus **100% holdout, per-skill, compound exact-set, coverage, order, and stability results**, with **zero extra selections and zero unresolved stages** in clarified compound requests. Clarifications preserve every original topic and target; the original corpus remains a separate diagnostic.
- The historical 373,000-call run reached **27.697% compound exact matching** and is rejected as evidence of completion. Current results belong to the source-bound aggregate receipt; the October 10 full local CI passed all 22 steps and all 15 semantic gates across 32/32 receipts. Generated-corpus success does not establish perfect arbitrary-language matching, execution, or deployment.
- The console displays actual completed receipts and recorded production-router examples. It performs no simulated or live browser CI. See [semantic validation and limitations](docs/SEMANTIC_ROUTER_PROOF.md) for source identity, methodology, and rerun instructions.

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
