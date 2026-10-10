---
name: solforge-code-research
description: Audit a whole codebase or ecosystem for intended architecture, hidden capabilities, inconsistencies, and completion gaps.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# SolForge Code Research

Audit a whole codebase or ecosystem for intended architecture, hidden capabilities, inconsistencies, and completion gaps.

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Define the exact question, source or repository boundaries, decision criteria, required freshness, and requested output. Read the actual implementations or primary sources rather than treating summaries as proof.

Trace material claims to concrete evidence. Search competing explanations and contrary findings, distinguish explicit intent from inference, and label inaccessible or untested behavior.

Compare alternatives on symmetric criteria. Order remediation recommendations by dependencies and decisive acceptance checks; research or comparison does not itself authorize implementation or merging.

Return the requested synthesis with source locators, uncertainties, scope limits, and practical consequences. Stop when the question is supported or the remaining evidence is genuinely unavailable.

For a substantial repository investigation, apply the evidence and coverage contract: [mastery-contract.md](references/mastery-contract.md).

When an implementation handoff is requested, use the result contract: [result-contract.md](references/result-contract.md).

When findings will drive a later repair, use the verification and handoff guidance: [forward-use.md](references/forward-use.md).

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
