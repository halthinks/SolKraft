---
name: preserve-engineering-selections
description: Preserve evidence-backed real-part selections, engineering rationale, constraints, and validation gates while carrying a hardware product through requirements, BOM, schematic, PCB, firmware, CAD, prototype, and release. Use when substantial engineering work already selected components or architecture for reasons; when closing design gaps without arbitrary substitutions; when reconciling supplier STEP, pinouts, ECAD, MCAD, code, and physical evidence; or when a project risks treating selected parts as generic TBD fields.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Preserve Engineering Selections

Treat prior engineering choices as a design baseline, not blank fields. Accept new decisions from `$select-and-validate-hardware-parts`; hand preserved selections to `$build-selected-hardware-product`.

## Establish authority

1. Inspect source artifacts, code, commits, BOMs, calculations, manufacturer documents, STEP files, tests, and decision records.
2. Read implementation code directly. Do not infer implementation maturity from summaries.
3. Recover for every choice: purpose, alternatives considered, selection reason, constraints, evidence, dependencies, and unresolved validation.
4. Separate current profiles and historical iterations. Never pool parts across profiles to fill gaps.

## Classify every selection

Use exactly one state:

- `SELECTED`: preserve and realize through downstream layers.
- `CONDITIONAL`: preserve pending a named measurement or evidence gate.
- `BLOCKED`: preserve pending an external sample, geometry, document, or dependency.
- `REOPENED`: measured evidence invalidated the selection; comparison is required.
- `SUPERSEDED`: an explicit authority decision adopted a replacement with lineage.
- `REJECTED`: evaluated and deliberately not adopted.

Never change `SELECTED`, `CONDITIONAL`, or `BLOCKED` merely to make a gap appear closed.

## Build the selection register

Record one row per component, module, fabricated assembly, interface, and architectural choice with:

- stable selection ID and owning product/profile/revision;
- manufacturer, exact MPN/order code, quantity, refdes/assembly role;
- state and readiness claim;
- selection reason and rejected alternatives;
- electrical, optical, RF, thermal, mechanical, software, supply, and regulatory constraints as applicable;
- supplier/source URLs or local evidence paths and hashes;
- exact public manufacturer STEP or measured-sample status;
- pinout, ECAD footprint, schematic occurrence, PCB occurrence, CAD occurrence, and firmware owner;
- dependencies, validation gates, observed evidence, and open gaps;
- replacement decision and predecessor/successor lineage when applicable.
- candidate comparison, hard-gate failures, sensitivity, evidence maturity, claim ceiling, lifecycle and authorized-source status;
- derating, tolerance, RF/EMI, environmental, DFM/DFA/DFT, calibration, provisioning, service, supplier-change, counterfeit, and obsolescence constraints when applicable.

Run `scripts/validate_selection_register.py <register.json>` after creating or changing a register.

## Close gaps by realization

Carry a selected choice forward:

```text
requirement -> selected part -> source evidence -> pin/power/interface contract
-> schematic -> footprint -> placement/routing -> CAD occurrence
-> firmware/driver -> prototype -> measured validation -> release claim
```

If a downstream layer is missing, implement that layer. Do not automatically reopen the upstream selection.

Examples:

- Missing schematic: create the real circuit around selected parts; do not select easier parts by default.
- Missing PCB: route and verify selected interfaces, power, RF, keep-outs, and service access.
- Missing firmware: bind the selected pins and devices to the target SDK; host adapters are not device firmware.
- Missing CAD: import manufacturer STEP or measured geometry and close the dimension chain.
- Failed benchmark: retain the measured evidence, reopen only affected choices, compare replacements, and log the decision.

## Change-control gate

Before replacing a selected choice, require:

1. named failing requirement or evidence gate;
2. observed evidence, not preference;
3. impact analysis across BOM, schematic, PCB, firmware, CAD, enclosure, thermal, validation, renders, procurement, and compatibility;
4. comparison with the current selection and viable alternatives;
5. explicit authority decision;
6. updated lineage and regenerated downstream artifacts.

Never silently substitute, rename, consolidate, or delete a selection.

## Evidence and claim boundaries

Distinguish:

- manufacturer/source evidence;
- analytical or simulated evidence;
- host tests;
- target compilation;
- bench measurements;
- assembled first article;
- representative physical integration;
- release validation.

Passing tests validate only what they execute. A placeholder ECAD/CAD file is not a design. A render is not physical evidence. A selected part is not procurement-ready until its order code, quantity, alternates, footprint, geometry, and assembly disposition reconcile.

## Completion gate

Finish only when every selection is traceable through all layers required by the claimed readiness level, all replacements have explicit lineage, all remaining gaps are visible with terminal disposition, and BOM, ECAD, PCB, firmware, CAD, renders, prototype evidence, and release claims agree.

Report both preserved progress and remaining gaps. Do not describe legitimate source-bound selection work as random assignments merely because later realization is incomplete.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
