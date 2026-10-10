---
name: solforge-workflow-science-report
description: Produce a configured scientific package with methods, results, visuals, limitations, review, and reproducibility assets.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Produce a scientific report package

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the research question or hypothesis, the supplied papers, data, methods, and conditions, and the requested package configuration: audience, format, export targets, and which of methods, results, visuals, limitations, and reproducibility assets are in scope. Reuse completed literature, analysis, or replication work rather than repeating it; where inputs are missing, state plainly what the report can and cannot claim without them.

Write methods so a competent reader could repeat the work: data provenance, inclusion criteria, instrument or code versions, parameters, and every deviation from a prior protocol. Report results against the stated hypotheses with confirmed, inconclusive, and contrary outcomes kept distinct; a results section reporting only hypothesis-confirming outcomes is weak evidence. Choose figures that expose the data behind each claim — distributions, uncertainty intervals, sample sizes — over summary graphics that hide them, and tie every figure and table to the specific claim it supports.

Verify before delivery: recompute headline numbers from the underlying data or analysis outputs rather than trusting an intermediate draft, check that every citation resolves to a real inspected source, and confirm significance language matches the tests actually run. Do not present a literature claim as an experimental finding, an exploratory correlation as a tested prediction, or a simulation as a measurement. Where the package promises reproducibility assets, inspect or run the environment, seeds, and scripts enough to confirm they regenerate the reported results; an unrun reproducibility bundle is not evidence of reproducibility.

Deliver the report in the requested format with its evidence: what was verified and how, remaining limitations, and any claim left unsupported. Use [report production](../solforge-run-report-write/SKILL.md) when the package needs the full source-check and export procedure beyond this workflow.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by the contract-aware router; selection is advisory.
- Hardened routing rejects opaque or inadmissible capabilities.
- Contract metadata is evaluated before loading the full instruction body.
- Execution authority stays with the host.
- Validation evidence and limits: see the repository VALIDATION.md and docs/SEMANTIC_ROUTER_PROOF.md for the completed local semantic corpus, source identity, precision limits, and rerun instructions. A selected route does not prove execution or perfect matching.

<!-- END SOLKRAFT SKILL INTEGRATION -->
