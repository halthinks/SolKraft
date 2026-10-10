---
name: realize-cad-bound-product
description: Convert a hardware product concept or existing iteration into a physically credible, dimensionally closed, CAD-bound product realization. Use for modular product architecture, selected supplier geometry, electronics packaging, power and thermal paths, mechanical interfaces, collision and balance analysis, photoreal renders that preserve CAD silhouette, BOM and evidence ledgers, and reusable product-line development without inventing received measurements or fabrication readiness.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Realize a CAD-bound product

Own the design work. Use orchestration only to expose alternatives or validate evidence; never let it replace product judgment.

## Establish authority

1. Inventory the dirty tree without overwriting prior work.
2. Separate four authorities:
   - product and user-experience requirements;
   - approved industrial-design references;
   - selected hardware and supplier geometry;
   - current physical evidence.
3. Record explicit locks and rejected directions. Treat old styling as a language, not automatically as the new body.
4. Classify every input as `RECEIVED_MEASURED`, `SUPPLIER_EXACT`, `SUPPLIER_DRAWING`, `SELECTED_NOMINAL`, `DESIGN_TO_SPEC`, or `PRESENTATION_ONLY`.

Read [references/closure-model.md](references/closure-model.md) before declaring an assembly closed or a claim supported. Read [references/render-lineage.md](references/render-lineage.md) before creating or accepting presentation imagery.

## Run the dependency pipeline

Proceed in this order; loop backward whenever a downstream check fails:

1. Translate user experience into software, sensing, control, power, compute, display, radio, and mounting requirements.
2. Select real orderable parts and capture order code, source, revision, geometry class, mass, power, heat, connector, cable, optical, RF, and service constraints.
3. Create component envelopes and keep-outs before exterior surfaces.
4. Partition the system into the fewest useful service modules. Preserve structural load paths, connector access, cable bend, seals, thermal conduction, and assembly order.
5. Shape the enclosure around those constraints using the approved style grammar. Reject uniform slabs, gratuitous rails, false vents, decorative seams, and visual bulk that does not express a real function.
6. Build master CAD plus configuration-specific assemblies. Include representative host, hand, accessory, cable, magazine, and power-module collision fixtures when applicable.
7. Calculate mass properties and balance for every supported configuration. Label calculations as calculations until serialized hardware is weighed.
8. Produce the carrier placement, connector, routing, bend, SI/PI, thermal-via, and fabrication-hold contract. A zero-DRC constraint model is not a released production board.
9. Generate evidence artifacts and validate them with `scripts/validate_realization.py`.
10. Produce two image classes:
    - CAD-bound proof renders derived directly from released meshes;
    - presentation studies whose material, lighting, and context may vary but whose geometry is not evidence.

## Minimum deliverable set

- architecture and interface contract;
- selected BOM with source and evidence class;
- master assembly and module exports;
- geometry and keep-out report;
- power, thermal, balance, and collision reports;
- carrier release-status package;
- render-lineage manifest with hashes;
- physical acceptance ledger with unexecuted gates left open;
- machine-readable product-realization manifest;
- rejection archive for materially different discarded directions.

## Completion rule

Do not say `production-ready`, `fabrication-ready`, `measured`, `verified`, or `qualified` unless the corresponding physical records exist. State the strongest truthful closure level: `CONCEPT`, `DIGITAL_PACKAGING_CLOSED`, `EVT_RELEASE_CANDIDATE`, `PHYSICALLY_VERIFIED`, or `PRODUCTION_RELEASED`.

Run:

```powershell
python scripts/validate_realization.py <realization-root>
```

Fix every error. Warnings may remain only when they identify explicit physical or supplier gates rather than missing digital work.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
