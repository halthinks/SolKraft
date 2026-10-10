---
name: solforge-workflow-legal-risk
description: Identify obligations, exposure, controls, evidence gaps, and questions requiring qualified professional review.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Assess legal and compliance risk

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the question, the jurisdictions and effective dates in scope, the parties and activities involved, and the artifact under review — a contract, policy, product behavior, marketing claim, or process. Frame the work as risk analysis, not legal advice, and record early which questions exceed it and require qualified professional review.

Derive the applicable obligations from controlling sources: statutes and regulations, executed agreements and license terms, binding commitments, and authoritative interpretations, ranked by authority rather than convenience of access. For each obligation, compare it against the actual current text or observed practice, not a description of them. Assess exposure as likelihood and consequence with the basis for each rating, evaluate existing controls against the obligation they are meant to satisfy, and map the gaps where obligation and practice diverge.

Verify every material claim against an inspected source. Do not rely on remembered statute or regulation text without checking its currency — law changes, and an outdated citation is a false control. Do not treat a paraphrase of a clause as the contract language, rate a risk with no identified obligation behind it, or accept a compliance checklist passed by assertion as evidence of conformity. Keep facts, inferences, and open questions distinct.

Report the risk analysis and compliance gap map: obligations with sources, exposure ratings with basis, control adequacy, evidence gaps, and the specific questions reserved for qualified counsel, with jurisdictions and dates not covered stated as limits. Use [legal research](../solforge-workflow-legal-research/SKILL.md) when the controlling sources themselves are not yet identified or authority-ranked.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Validation evidence and limits: see repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
