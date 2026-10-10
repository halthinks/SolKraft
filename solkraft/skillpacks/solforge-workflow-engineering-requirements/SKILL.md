---
name: solforge-workflow-engineering-requirements
description: Translate intent into testable requirements, interfaces, constraints, hazards, and verification.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Specify engineering requirements

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the intent, user scope, and acceptance criteria first: the operating environment, the stakeholders, applicable standards or regulations, and the constraints already fixed (cost, mass, power, schedule, existing interfaces). Separate stated needs from assumed solutions; when a request embeds a design, extract the underlying need before specifying, and reuse any valid requirements work already completed rather than regenerating it.

Write each requirement as a single testable statement with a measurable threshold, units, and the conditions under which it holds, and give it an identifier, a source, and a rationale. Define interfaces by what crosses the boundary — signals, power, mechanical fit, data and protocol versions — with tolerances, not by internal implementation. Keep fixed constraints distinct from performance requirements. Identify hazards and failure modes with the method the domain expects (FMEA, fault tree, HAZOP, threat model) and derive safety requirements from those hazards rather than retrofitting them onto a chosen design.

Pair every requirement with a verification method — inspection, analysis, demonstration, or test — in a traceability matrix; a requirement with no feasible method is untestable and must be rewritten or flagged. Check for conflicts (two requirements that cannot both hold), gaps (an interface with only one side owned), and unquantified language: "shall be user-friendly" or "shall be fast" is not a requirement, and a matrix row whose method merely restates the requirement is not verification. Escalate missing quantities as open items instead of inventing them.

Return the requirements specification and verification matrix, the assumptions and unresolved values, any conflicts found, and the sources for constraints inherited from standards or prior work. Use [engineering trade study](../solforge-workflow-engineering-trade/SKILL.md) when the requirements leave competing alternatives unresolved and selection needs evidence.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
