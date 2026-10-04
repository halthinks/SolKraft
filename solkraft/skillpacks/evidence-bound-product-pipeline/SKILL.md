---
name: evidence-bound-product-pipeline
description: Realize or audit a hardware/software product line that needs source-bound requirements, exact supplier geometry and pinouts, PCB mapping, CAD, renders, BOMs, and physical validation. Use for product recovery, first-article planning, hardware selection, power/thermal/mechanical closure, or release claims where proxy geometry, generated imagery, documentation, and test plans must not be confused with fabricated or measured evidence.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Evidence-Bound Product Pipeline

Use this workflow to turn a product concept or fragmented repository into a traceable, repeatable realization package. Preserve historical work; classify it before adopting it.

## Start with authority, not a render

1. Create or locate one authority directory with a decision log, source index, legacy-identity map, conflict register, requirements traceability, and release-acceptance matrix.
2. Freeze each customer product name, ownership boundary, physical deployment, interfaces, and readiness claim. Keep historical names through explicit adapters or maps; never global-replace them.
3. State the active architecture and exclusions before reusing candidate CAD, BOMs, images, or software.
4. Treat a selection as a candidate until its exact revision, evidence, and closure gate are recorded.

## Derive the physical product from behavior

For each product, define the user experience, local sensing/actuation, publishing/consuming interfaces, latency, power states, degraded behavior, calibration, service, and health evidence. Then derive sensor, compute, display, radio, storage, power, thermal, mounting, and interaction requirements.

For spatial or aiming products, define every coordinate frame, calibration revision, timestamp, uncertainty, and owner. A projected reticle must use the calibrated bore transform; never substitute a generic screen-center reticle.

## Use first-party supplier evidence

For every advancing component, record manufacturer, exact orderable part, official URL, revision, local path, SHA-256, source type, availability state, and permitted use.

- Import the original manufacturer STEP/DXF/ECAD archive unchanged whenever it is publicly exposed.
- When no public original geometry exists, record that result and require a serialized received sample plus a controlled metrology record before closing its interface.
- Use exact published pinouts for source-contact accounting. Record every pin/contact, its logical endpoint, allocation state, voltage domain, return/EMI considerations, and release gate.
- Do not turn a datasheet, package drawing, evaluation board, partner-library footprint, generic RMR pattern, image-scaled model, or family STEP into an exact selected-part geometry claim.

Read [references/evidence-states.md](references/evidence-states.md) before changing a readiness status.

## Keep PCB mapping and PCB release separate

Produce a logical pin/connector/PCB map before a schematic. It must show what is source-verified, selected, reserved, unrouted, and prohibited.

Do not call a PCB routed or fabrication-ready until all of these are present: selected parts; exact package/land-pattern control; reviewed schematic and netlist; ERC; stack-up; placement; routing; DRC; SI/PI, current, thermal, fault, ESD/EMC review as applicable; connector/cable-bend keep-outs; fabrication outputs; and received-board or article evidence. Never derive physical current, radio, thermal, or hot-swap claims from a logical map.

## Close mechanisms and power as systems

For batteries, pods, docks, latches, or contacts, define the mechanical admission sequence separately from electrical admission. Record load paths, seals, service removal, partial insertion, interlocks, contact order, and fault states.

For multiple batteries, use a protected power-path architecture. Explicitly prohibit raw pack paralleling unless a separately qualified architecture says otherwise. Require evidence for every supported source combination, insertion/removal behavior, charge termination/maintenance, current limiting, reverse current, thermal limits, and user-visible health state.

## CAD and render gate

Only make customer-facing, geometry-traceable renders after a current assembly has a dimension chain, bought-part geometry/metrology, connector and cable bends, access/seal/service paths, thermal path, collision checks, balance study, and BOM reconciliation.

Before that gate, label CAD as a source-geometry review, envelope study, or historical candidate. Reject rectangular placeholders, hidden collisions, unremovable batteries, inaccessible controls, unsupported fasteners, unverified interfaces, and visual styles unrelated to the product direction.

## Validate and report honestly

Validate the authority hashes, product registry, contract tests, compatibility mappings, evidence references, BOM-to-assembly reconciliation, and claim boundaries. Use an independent challenge pass to look for stale identity, duplicate capability, unsupported part assumptions, render/BOM mismatch, hidden uncertainty, and false readiness.

At every handoff, report three things separately:

1. Evidence newly closed and its exact paths/hashes.
2. Work that is implemented or digitally validated.
3. Physical, supplier, fabrication, instrumented, and received-article gates still open.

Never mark a product physically verified, prototype-ready, or release-ready from plans, software tests, source PDFs, CAD, BOMs, simulated benchmarks, or generated renders alone.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
