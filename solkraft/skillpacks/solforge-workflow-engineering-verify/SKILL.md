---
name: solforge-workflow-engineering-verify
description: Test requirements, tolerances, failure modes, safety assumptions, and reproducibility against evidence.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Verify engineering requirements against evidence

Use the [native execution contract](../solforge/references/native-execution.md) once per task.

Establish the requirements under test, their acceptance criteria and tolerances, the exact artifact and configuration being verified, and the environmental and load conditions that apply. Reuse valid prior evidence when the configuration still matches; when a requirement is ambiguous or untestable as written, flag that before substituting a weaker criterion. Inventory the evidence already available — calculations, simulations, prior test data — and state what each piece actually covers.

Trace each requirement to a verification method — inspection, analysis, simulation, demonstration, or physical test — chosen by what the requirement demands and what evidence is admissible. Exercise nominal behavior plus the corners: worst-case loads, tolerance stack-up, interface extremes, degraded operation, and the safety assumptions the design depends on. Probe failure modes deliberately — single-point failures, common-cause coupling, out-of-range inputs, and recovery behavior — not just the intended path. A nominal-only pass does not establish margin against a tolerance limit.

Hold evidence to its kind. Measured data carries units, instrument, configuration, and conditions; simulation or analysis results are labeled as such with their model assumptions stated, and never reported as measurements. Do not present a surrogate component or emulated environment as evidence for the real one, do not average away an out-of-spec corner result, and do not rerun a failed check until it passes without recording each outcome. Confirm reproducibility by repeating the procedure on the stated configuration and reporting the observed variance.

Report per requirement: verdict, supporting evidence and conditions, observed margin against limits, failure modes found with severity, and what remains untested or assumed. Create the verification report or failure-mode audit artifact only when requested or required. Use [research execution](../solforge-run-research/SKILL.md) when verification needs sourced external evidence — standards, failure rates, material properties — not already in the supplied documentation.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
