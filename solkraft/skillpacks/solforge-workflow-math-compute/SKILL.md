---
name: solforge-workflow-math-compute
description: Design reproducible symbolic or numerical experiments that inform—but do not substitute for—proof.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Run mathematical experiments

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the statement or question the experiment addresses, its definitions and assumptions, the allowed methods and tools, and what the computation is meant to establish — supporting evidence, a parameter sweep, asymptotic behavior, or a candidate counterexample. Decide up front which outcome would change the conclusion, so the experiment discriminates rather than decorates. Reuse existing valid computations and scale the search to the claim.

Choose the computational mode deliberately: exact symbolic arithmetic for identities and small cases, certified or arbitrary-precision numerics whenever floating point is in play, and stochastic search only with recorded seeds. Validate the setup on cases with known answers before trusting it on unknown ones, and cross-check results with an independent method — symbolic against numeric, a direct algorithm against a library call, refinement of a mesh or step size — before treating agreement as evidence. Probe boundaries, degenerate inputs, and extreme parameters where conjectures usually break; track error bounds, residuals, and convergence behavior, not just the headline value.

Record everything needed to reproduce: code or notebook, tool versions, precision settings, seeds, and the actual command run. A result that changes under higher precision, a different discretization, or a second implementation is not evidence — it is a numerical artifact. Do not present a finite search as an exhaustive proof, a plot as a derivation, or a computation under one branch or normalization convention as the general case.

Report the statement tested, the methods and parameters used, what the computation supports and at what strength, and the limits — unexplored ranges, precision ceilings, failed checks. Use [math verification](../solforge-workflow-math-verify/SKILL.md) when the computed evidence must be audited as a claim — every inference, dependency, and hidden assumption — before it can stand.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- Selected by SolKraft's contract-aware router; selection is advisory and does not grant execution authority.
- Hardened routing rejects opaque or contract-inadmissible capabilities.
- Contract metadata is evaluated before full skill instructions are loaded.
- Runtime authority stays with the host; `execution_authorized` remains `false`.
- Current local acceptance: 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
