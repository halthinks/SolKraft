---
name: select-and-validate-hardware-parts
description: Select real orderable hardware components through source-bound requirements, candidate comparison, calculations, geometry, supply evidence, and validation planning, and prove why the winner is preferable to alternatives. Use for component down-selection, architecture closure, exact MPN choice, supplier STEP and pinout research, make-versus-buy decisions, or when a hardware product needs defensible selections before BOM, schematic, PCB, firmware, CAD, or prototype work.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Select and Validate Hardware Parts

Produce decisions that `$preserve-engineering-selections` can protect and `$build-selected-hardware-product` can realize.

## Start from requirements

Assign stable requirement IDs. Separate hard gates from weighted preferences. Cover function, interfaces, compute/memory, timing, power, thermal, RF/EMI, optical, mechanical envelope, mass/balance, environment, lifetime, calibration, service, manufacturing, testability, availability, cost, compliance, and software/toolchain support.

Do not choose a familiar part and backfill rationale.

## Close the electronic architecture before comparing MPNs

Create an electronic requirements and budget package. Selection is invalid without the applicable calculations and interface contracts.

### Power tree and energy

- Define every source, rail, load, return path, ground domain, always-on domain, and switched domain.
- Budget minimum/nominal/maximum voltage; continuous, peak, startup, inrush, transmit, display, actuator, and fault current; duty cycle; conversion loss; quiescent current; battery aging; contact and cable loss; and required margin.
- Define sequencing, ramp rate, power-good, enable ownership, reset thresholds, brownout response, back-power prevention, discharge, hot-plug, reverse polarity, overvoltage, undervoltage, overcurrent, short-circuit, ESD, surge, and thermal protection.
- For batteries, define exact chemistry/configuration, finished pack, cell limits, charger profile, termination, power-path ownership, BMS/protection, NTC, fuel gauge, source sharing, charge-while-operating behavior, and fault isolation. Never directly parallel packs without a designed sharing path.
- Calculate regulator dissipation, inductor saturation/RMS current, diode and MOSFET stress, capacitor ripple/RMS current, loop components, transient response, rail tolerance, and worst-case efficiency before selection.

### Digital interfaces and timing

- Define logic high/low thresholds across PVT, voltage domains, input leakage, output drive, pull-ups/pull-downs, boot straps, reset states, and unpowered behavior.
- Budget bus bandwidth, protocol overhead, frame rate, latency, jitter, buffering, DMA, memory bandwidth, CPU load, interrupt rate, and error recovery for the simultaneous worst workload.
- Define clock source, accuracy, phase noise/jitter, startup, load capacitance, trace/load limits, and synchronization requirements.
- For SPI, I2C, UART, USB, Ethernet, MIPI, RGB, SDIO, CAN, I2S, and parallel buses, close topology, controller instance, exact pins, voltage, speed, loading, termination, impedance, skew/length constraints, connector path, ESD parts, and target-driver support.
- Reserve programming, debug, recovery, manufacturing test, and boundary-observation access. Prove that pin allocation includes boot and fault states, not only normal operation.

### Analog and sensing

- Build an end-to-end error budget including sensor accuracy, offset, drift, noise, reference error, ADC INL/DNL/ENOB, gain/filter tolerance, quantization, layout/parasitics, calibration residual, temperature, and aging.
- Define signal range, common-mode range, input impedance, source impedance, bandwidth, anti-aliasing, sample rate, settling time, protection leakage/capacitance, reference drive, grounding, shielding, and calibration method.
- Validate saturation, clipping, aliasing, multiplex settling, crosstalk, and fault inputs at worst-case component tolerances.

### RF and wireless

- Define band, channel plan, conducted/radiated power, receiver sensitivity, link budget, antenna type/efficiency/pattern, feed and matching network, ground clearance, enclosure detuning, polarization, coexistence, desense, harmonics/spurs, regulatory region, and test connector/mode.
- Analyze simultaneous radios, switching converters, displays, high-speed buses, radar, clocks, and enclosure materials. A frequency label alone is not coexistence evidence.
- Preserve module certification assumptions only when the exact antenna, layout, power, firmware, and integration constraints remain valid.

### Signal and power integrity

- Define stack-up assumptions, reference planes, return-current continuity, impedance classes, via transitions, termination, crosstalk limits, decoupling targets, bulk capacitance, plane/trace current density, connector/contact derating, and PDN impedance targets.
- Estimate or simulate critical nets and rails before layout freeze; measure them on the first article with named probes, bandwidth, points, and limits.

### Thermal and reliability

- Calculate junction temperatures from worst-case loss, theta values or compact thermal models, copper/thermal-via path, interface materials, enclosure conduction/convection, ambient range, solar/user heat, neighboring sources, and duty cycle.
- Apply voltage, current, power, temperature, capacitor-bias, battery, contact, and mechanical derating. Define component tolerance, aging, wear, write endurance, connector cycles, battery cycles, and expected service life.
- Identify single-point failures, fault propagation, watchdog/reset ownership, safe/degraded states, diagnostics, telemetry, and repair disposition.

### PCB, assembly, and test constraints

- Require exact symbol, land pattern, courtyard, paste, package height, exposed-pad/via rules, moisture sensitivity, reflow profile, assembly-side restrictions, inspection access, rework feasibility, and X-ray/AOI implications.
- Define antenna, optical, magnetic, thermal, creepage/clearance, noisy/sensitive, connector, fastener, cable-bend, and programming keep-outs before accepting a candidate.
- Define test points, fixtures, rails and signals measured, calibration/provisioning flow, serial identity, firmware loading, and production pass/fail limits.

For every budget, retain nominal, worst-case, margin, assumption, source, calculation artifact, and validation method. A part that lacks adequate margin remains `CONDITIONAL` even if nominal figures look acceptable.

## Build the candidate set

Use current manufacturer pages and primary documentation. Record exact manufacturer and MPN/order code, lifecycle state, authorized sources, lead-time/availability snapshot, minimum order, package, variants, datasheet revision, errata, reference design, pinout, footprint, public manufacturer STEP/3D model, and development hardware.

Include credible alternatives and the existing incumbent. State why any obvious candidate was excluded before detailed scoring.

## Apply hard gates first

Reject candidates that cannot satisfy a non-negotiable requirement. Record the exact requirement, source evidence, calculation or test, and rejection reason. Never allow weighted scoring to rescue a hard-gate failure.

Typical gates include voltage/current limits, interface compatibility, throughput/latency, memory, operating temperature, package/envelope, RF band, antenna rules, optical geometry, supply continuity, target SDK support, required geometry, and manufacturability.

Also hard-gate parts that fail worst-case rail/transient stress, logic thresholds, pin/boot behavior, regulator stability, bandwidth/latency, analog error, ADC/reference range, RF link/coexistence, junction temperature, signal/power integrity, protection coordination, derating, PCB assembly, or test access.

## Compare surviving candidates

Create a decision matrix with unnormalized facts, units, source and uncertainty before assigning scores. Compare:

- functional and performance margin;
- electrical and power-path compatibility, peaks, startup, sleep, derating, and protection;
- compute, memory, bus bandwidth, latency, and software maturity;
- RF coexistence, antenna/keep-out, certification inheritance, and interference risk;
- thermal dissipation, junction/case limits, cooling path, and enclosure impact;
- exact geometry, connector orientation, cable bend, optical path, mounting, mass, and center of gravity;
- lifecycle, authorized supply, alternates, counterfeit/change-notification risk, and second-source reality;
- symbol/footprint/STEP quality, reference designs, SDK/drivers, licensing, and toolchain ownership;
- DFM, DFA, DFT, inspection, rework, calibration, provisioning, service, and repair;
- unit and landed cost at realistic quantities;
- environmental, reliability, ESD/EMC, battery/protection, and applicable compliance evidence.

Weight preferences only after hard gates. Run sensitivity analysis: show whether reasonable weight changes alter the winner.

## Validate before locking

Use the cheapest evidence that can falsify the decision, then advance maturity:

1. manufacturer evidence and exact geometry;
2. calculation and interface-budget checks;
3. evaluation-board or module bench test;
4. representative workload and coexistence benchmark;
5. prototype circuit and mechanical fit;
6. first-article measurement;
7. representative integration and environmental validation.

Define pass/fail thresholds, fixtures, instruments, raw outputs, sample count, conditions, and uncertainty before testing. Keep the selection `CONDITIONAL` until its decisive test passes.

## Issue the selection decision

For each winner, record:

- stable selection ID and owning product/profile/revision;
- selected exact MPN/order code and role;
- requirements satisfied and margin;
- alternatives considered, hard-gate failures, scores, sensitivity, and rejection reasons;
- selection reason in engineering terms;
- primary evidence paths/URLs and hashes;
- public manufacturer STEP or measured-sample gate;
- constraints inherited by schematic, PCB, firmware, CAD, enclosure, manufacturing, and validation;
- electronic requirement IDs plus power, timing, memory, analog, RF, SI/PI, thermal, protection, derating, reliability, PCB, and test-budget artifacts;
- state: `SELECTED`, `CONDITIONAL`, or `BLOCKED`;
- validation gates, fallback trigger, and approved alternate policy;
- evidence maturity and maximum readiness claim.

Run `scripts/validate_part_decision.py decision.json`. Feed the resulting selection register to `$preserve-engineering-selections`, then `$build-selected-hardware-product`.

## Prohibitions

- Do not select solely from distributor filters, search snippets, generated summaries, popularity, price, or availability.
- Do not confuse a family datasheet with the exact orderable variant.
- Do not treat community CAD as manufacturer geometry without provenance.
- Do not label pin-compatible parts as approved alternates without behavioral and physical validation.
- Do not hide uncertainty or supplier dependence inside a score.
- Do not claim validation from a plan, simulation, host test, preview, or unmeasured sample.

## Completion

Finish when the winner and rejected alternatives are traceable to requirements and primary evidence, decisive uncertainties have explicit validation gates, sensitivity does not hide a fragile choice, inherited constraints are handed downstream, and the claim ceiling matches observed evidence.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
