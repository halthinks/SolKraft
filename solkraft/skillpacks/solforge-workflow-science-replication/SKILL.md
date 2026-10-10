---
name: solforge-workflow-science-replication
description: Reproduce claims independently, compare conditions, quantify divergence, and record unresolved causes.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Replicate scientific claims

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Pin down the claim being replicated, the source (paper, dataset, notebook, prior run), the stated result with its quantitative value and uncertainty, and the user's acceptance criteria for what counts as a match. Recover the original conditions before attempting anything: methods, code and dependency versions, datasets and seeds, environment, hardware, and statistical treatment. When conditions are incomplete, identify what is missing and state it; do not silently substitute modern defaults and then treat the result as a verdict on the original.

Run an independent execution rather than re-reading the claim. Distinguish re-running the original artifact from reimplementing the method, and record which was done. Reproduce the original result first; only then vary conditions deliberately — one at a time — to test robustness. Compare against the reported value with the same estimator and precision, and quantify divergence in absolute and relative terms rather than reporting "close" or "different". Match sign and direction before magnitude.

Classify every divergence before assigning blame: transcription or unit error, environment or version drift, stochastic variance within a seed sweep, underspecified method details, or a genuine failure of the claim. A single differing run is not a falsification — test whether the divergence exceeds the claim's own uncertainty band first. Do not tune parameters until the claim reproduces and then report success; do not average away failures across seeds, and do not present a positive control failure as evidence about the claim itself.

Report the claim, the conditions established and the gaps, the replicated versus reported values with divergence quantified, the classification of each unresolved divergence, and what remains unverifiable. Use [run research](../solforge-run-research/SKILL.md) for source tracking and reproducible search procedure beyond the replication runs themselves.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
