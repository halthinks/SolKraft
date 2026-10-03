---
name: build-selected-hardware-product
description: Build an evidence-backed hardware product from preserved real-part and architecture selections, carrying them through exact BOM, supplier geometry, pinouts, schematics, routed PCB, target firmware, CAD, enclosure, assembly, first article, measurements, renders, and release evidence. Use when Codex must turn an established engineering baseline into procurement-, fabrication-, prototype-, integration-, or release-ready deliverables without losing selection rationale or substituting parts merely to close gaps.
---

# Build Selected Hardware Product

Use `$select-and-validate-hardware-parts` to create new decisions and `$preserve-engineering-selections` whenever a prior selection baseline exists. Treat their register and authority decisions as build inputs.

## Set the claimed readiness target

Choose one target and state its evidence threshold before building:

- `DESIGN_COMPLETE`: requirements, selections, interfaces, calculations, and complete artifact plan reconcile.
- `PROCUREMENT_READY`: every purchased line is exact, orderable, sourced, quantified, and alternates are controlled.
- `FABRICATION_READY`: ECAD/MCAD, drawings, outputs, tolerances, materials, and assembly data pass their native checks.
- `PROTOTYPE_READY`: build package, firmware, provisioning, fixtures, inspection, and acceptance procedures are executable.
- `INTEGRATION_READY`: assembled hardware has passed subsystem measurements and interface tests.
- `RELEASE_READY`: representative articles and complete scenarios have observed, reviewable evidence.

Never use evidence from a lower level to claim a higher level.

## Generate the build closure matrix

Run:

```text
python scripts/build_closure_matrix.py selection-register.json --output build-closure-matrix.json
```

The matrix must retain every selection ID and expose all required realization layers. Do not remove an open row to improve completion metrics.

## Execute in dependency order

### 1. Requirements and budgets

Freeze functional behavior, interfaces, timing, compute, memory, radio, power, thermal, optical, mechanical, environmental, service, and validation requirements. Give each requirement an evidence-producing acceptance method.

### 2. Exact component realization

For every purchased component, close manufacturer, exact MPN/order code, quantity, lifecycle/availability, approved alternate state, datasheet revision, pinout, package, footprint, public manufacturer STEP or measured sample, electrical limits, thermal limits, and evidence hashes. Preserve conditional selections until their named tests resolve them.

### 3. Electrical design

Create real hierarchical schematics—not title-block shells. Include every selected part, passive, protection device, connector, test point, net, rail, sequencing circuit, strap, programming interface, and DNP. Reconcile pin maps with datasheets and firmware. Run ERC and resolve or explicitly waive each finding.

Recalculate and close the selected architecture at circuit level: complete rail/load/transient and battery budgets; regulator stability and stress; protection coordination; logic thresholds and unpowered states; clock, reset, strap and sequencing behavior; bus bandwidth and timing; memory/DMA load; analog and ADC/reference error; RF link/coexistence; SI/PI constraints; decoupling and PDN; junction temperatures and derating; fault propagation, diagnostics, calibration, programming, and production-test coverage. Bind every calculated requirement to schematic nets, PCB rules, firmware behavior, and a bench measurement.

### 4. PCB realization

Select stack-up and fabrication rules. Place exact footprints and STEP-linked occurrences. Enforce antenna, optical, connector, cable-bend, creepage, current, impedance, thermal, assembly, and service keep-outs. Route all nets. Run DRC. Produce Gerbers/ODB++, drills, IPC netlist, pick-and-place, assembly drawings, paste, fabrication notes, impedance tables, and revision hashes as applicable.

### 5. Target firmware and software

Build the actual target project with its SDK/toolchain, entrypoint, drivers, assigned pins, device initialization, state machines, fault behavior, telemetry, provisioning, update/rollback, and reproducible image hash. Reuse validated host algorithms, but do not call host tests target execution. Compile, flash, capture logs, and measure workload on selected hardware.

### 6. Mechanical and industrial design

Import exact manufacturer STEP or measured geometry. Build the complete assembly around real boards, cells, optics, antennas, displays, connectors, fasteners, seals, thermal materials, controls, mounts, cable paths, and service clearances. Close wall thickness, tolerance stack, sealing, cooling, fastening, assembly order, removal paths, collisions, balance, and human interaction. Keep exterior styling constrained by the closed internal geometry without reducing the product to a generic box.

### 7. First article

Procure or fabricate the controlled revision. Record incoming inspection, substitutions, serials/lots, assembly deviations, firmware hash, calibration, photos, measurements, faults, rework, and disposition. A planned or rendered article is not a first article.

### 8. Measurement and validation

Run native electrical, RF, thermal, optical, mechanical, runtime, latency, memory, power, charging, fault, degraded-mode, collision, balance, environmental, and full-scenario tests required by the product. Attach raw captures and test setup. Mark failures without hiding them; reopen only selections implicated by evidence.

### 9. Geometry-traceable rendering

Render from the released or declared CAD revision. Reconcile visible components, seams, fasteners, apertures, rails, connectors, vents, controls, cable routes, human interaction, materials, and proportions. Reject CAD screenshots, placeholder bricks, impossible geometry, and render-only features.

### 10. Release reconciliation

Reconcile requirements, selection register, BOM, schematic, PCB, firmware, CAD, assembly, renders, tests, deviations, known limitations, and readiness claim. Hash final artifacts. Run an independent challenge. Release only to the highest level supported by observed evidence.

## Build rules

- Implement missing downstream layers before reopening upstream selections.
- Use exact supplier geometry when publicly available; otherwise require a received and measured sample.
- Keep product profiles and revisions separate.
- Do not import historical candidates to fill current gaps.
- Never convert a candidate, host test, generated preview, empty shell, or planned test into physical evidence.
- Make every artifact machine-reconcilable through stable IDs, refdes, CAD occurrences, firmware owners, revisions, and hashes.
- If tooling is missing, install or configure it when authorized; do not replace the deliverable with prose.
- Continue safe in-scope work while external physical evidence remains pending, but keep the readiness ceiling explicit.
- Close tolerance/derating, lifecycle/PCN, authorized sourcing, counterfeit control, EMI/EMC and RF coexistence, DFM/DFA/DFT, calibration, provisioning, traceability, reliability, environmental, inspection, rework, service, and end-of-life gaps where the readiness claim requires them.

## Definition of built

Call the product built only at the declared readiness level and only when every mandatory matrix cell for that level is closed with an artifact and evidence record, quantities and identities reconcile across all layers, native checks pass, deviations are dispositioned, and no claim exceeds observation.
