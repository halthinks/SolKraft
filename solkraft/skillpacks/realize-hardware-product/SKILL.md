---
name: realize-hardware-product
description: Convert a hardware-product concept or source-bound architecture into a compact, dimensionally closed, supplier-evidence-bound realization package. Use for exact component/order selection, supplier STEP and sample control, custom PCB/carrier placement and routing, batteries and protection, connectors and cable bends, mechanisms and seals, thermal paths, representative collision and balance studies, assembly CAD/renders, BOMs, and first-article acceptance. Also use to audit whether a hardware package is truly digitally closed or physically verified.
---

<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Realize Hardware Product

## Purpose

Turn software-driven product requirements into one coherent electrical,
mechanical, thermal, manufacturing, and acceptance package. Keep the result
small enough for the intended user and honest about the boundary between
supplier evidence, calculation, digital fit, received-sample measurement, and
physical test.

This skill is an execution method. The working agent performs the engineering,
research, CAD/PCB work, calculations, validation, and reporting. Do not hand
the outcome to an autonomous product generator or replace missing evidence with
generic research prose.

## Required closure ladder

Use exactly these levels in manifests and status reports:

1. `CONCEPT`: requirements exist; selections and geometry may be provisional.
2. `SOURCE_BOUND`: each critical bought part has an exact manufacturer identity,
   order path, controlled source, revision/date, and dimensional evidence.
3. `DIGITAL_CLOSED`: the selected supplier geometry and controlled custom parts
   form a dimensionally closed assembly; interfaces, cable bends, keep-outs,
   collisions, thermal paths, mass assumptions, and route status are checked.
4. `FIRST_ARTICLE_READY`: fabrication outputs, assembly sequence, inspection
   plan, acceptance limits, and procurement holds are complete enough to build.
5. `PHYSICALLY_VERIFIED`: received samples and the assembled article have passed
   recorded inspections and tests. Instrument IDs, sample IDs, operator/date,
   raw evidence, deviations, and dispositions are mandatory.

Never promote supplier nominal dimensions or CAD-derived mass to measured
results. Never promote a render, DRC pass, simulation, calculation, or component
datasheet to physical proof.

Read [closure-model.md](references/closure-model.md) before setting a closure
level. Read [electrical-mechanical-evidence.md](references/electrical-mechanical-evidence.md)
when selecting power, connectors, PCB routes, thermal paths, or sealing.

## Workflow

### 1. Establish product authority and the user journey

- Locate the latest product lock, software behavior, mode/control contract, and
  prior design assets.
- State the product's job, carried context, mounting context, interaction
  sequence, and upgrade/standalone behavior in plain language.
- Create a requirements table linking each physical requirement to the software
  behavior or user need that creates it.
- Preserve valuable prior work, but treat superseded dimensions and concept
  renders as visual language—not geometric authority.

### 2. Inventory evidence before selecting parts

- Record each candidate by manufacturer, exact model/order code, revision,
  lifecycle/availability, interface, envelope, mass, power, temperature, and
  controlled URL or local source.
- Prefer manufacturer product pages, drawings, datasheets, STEP/DXF, reference
  designs, and received measurements. Record SHA-256 for downloaded files.
- If a public order code, exact geometry, or production option is absent, open a
  procurement/measurement gate. Do not fabricate the missing identifier.
- Reject malformed, stale, conflicting, or reseller-only evidence explicitly.

Use `assets/component-register.template.csv` as the minimum source register.

### 3. Select the architecture from the full simultaneous workload

- Budget the worst admitted software workload: sensors, vision, inference,
  rendering, radio, learning, storage, display, controls, and transitions.
- Partition application compute, deterministic supervision, acceleration, and
  bounded live learning by measured or source-bound capability.
- Define all rails, peak/continuous loads, sequencing, protection, telemetry,
  brownout behavior, and thermal loss. Avoid bare parallel batteries; isolate,
  regulate, share, and prioritize sources deliberately.
- Select exact interfaces and pinouts before freezing enclosure joints.

### 4. Close geometry from the inside out

- Import exact supplier STEP/DXF where available. Otherwise create a controlled
  drawing-derived envelope and label it as such until sample inspection.
- Define a single coordinate system, datums, body splits, joint gaps, wall
  thicknesses, gasket lands, fasteners, service paths, and assembly order.
- Model connector insertion/removal space, flex and cable bend volumes, battery
  swell allowance, antenna/RF zones, optical/radar cones, thermal interfaces,
  controls under gloves/hands, and tooling access.
- Separate structural load paths from cosmetic shells. Mount rails and optics to
  a controlled structural member, not an unsupported shell.
- Export a master assembly plus manufacturing-neutral STEP for each custom body
  or mechanism. Record the exact generated files in the manifest.

### 4A. Turn the closed package into a product body

- Treat rectangular supplier envelopes and early keep-out blocks as constraints,
  not as the finished industrial design. Once those constraints close, shape the
  external shells with deliberate section changes, tapers, facets, radii,
  protective brows, grip/control relief, and coherent family language.
- Preserve the exact internal clearances, structural datums, service paths,
  optical/RF apertures, thermal contact areas, fastener access, and joint
  definitions while shaping the exterior. Re-run geometry and collision checks
  after every surface change.
- When the product is modular, make every body split functional: assign each
  module an owned subsystem, connector/bus boundary, retention method, sealing
  method, assembly direction, and field/depot service rule. Do not disguise one
  monolithic body as modular by drawing decorative seam lines.
- Use prior concept art only as an explicitly named visual-language reference.
  Never import its apparent proportions as dimensions unless controlled evidence
  independently supports them.
- Reject a final body that still reads as stacked packaging boxes unless the
  product authority explicitly requires that form. Compactness, carry balance,
  snag behavior, and the intended user's motion remain release requirements.

### 5. Complete the carrier and harness package

- Provide schematic/net ownership, stack-up, exact footprints, board outline,
  mounting datums, connector orientations, keep-outs, controlled-impedance
  classes, length/skew rules, power/ground strategy, thermal copper, test points,
  and fabrication notes.
- Route all released nets. Distinguish `mechanically routed`, `electrically
  routed`, `DRC clean`, `SI reviewed`, and `fabrication released`; these are not
  synonyms.
- Bind each FPC/harness to exact connectors, pinout, conductor size, shielding,
  length tolerance, minimum installed bend radius, retention, strain relief,
  service loop, abrasion control, and assembly step.

### 6. Prove fit, balance, heat, power, and interaction digitally

- Check product/product and product/fixture interference. Fixtures must include
  all representative hosts and user envelopes requested for the product.
- Run zero/one/two-accessory mass configurations and report total mass, center of
  gravity, assumption class, and sensitivity to unmeasured masses.
- Calculate power-path limits, contact derating, fuse/protection coordination,
  expected runtime ranges, and thermal paths. Mark runtime and temperature as
  predicted until instrumented tests pass.
- Verify button reach/guarding, viewing line, optic placement, cable snag paths,
  maintenance access, and mode/control mapping.

Use `scripts/check_aabb_collisions.py` and `scripts/compute_balance.py` for early
checks. For assemblies containing intended mating overlaps, optical/RF volumes,
or multiple fixtures, provide explicit `check_pairs` and a purpose for each
pair instead of treating every possible pair as a prohibited collision. Mesh/
solid interference and physical fixtures remain required before final release.

### 6A. Produce presentation imagery from geometry authority

- Export render meshes from the released master assembly or its controlled
  custom/supplier parts. Keep a machine-readable mesh/export report and hashes
  so the presentation geometry can be traced back to the assembly revision.
- Build high-end materials, labels, glass, lighting, camera composition, and
  display/UI artwork around those meshes. These presentation layers may improve
  readability and realism but must not move apertures, joints, controls, rails,
  pods, connectors, optics, or overall proportions.
- Render the views needed to judge the product, not only a flattering hero:
  front aperture view, rear/viewer/control view, both sides, zero/one/two
  accessory configurations, remote-cable routing when applicable, and at least
  one representative mounted/user-context view.
- If a generative image tool is used for mood or background, composite the
  unchanged CAD-derived product into it and label the result as presentation
  imagery. A generated product silhouette is never geometry evidence.
- Record every released render in `assets/render-lineage.template.json` and run
  `scripts/validate_render_lineage.py`. A valid lineage proves file/hash ancestry,
  not physical manufacture or pixel-level geometric equivalence; visual review
  against the master assembly is still required.

### 7. Produce first-article gates before claiming completion

- Create receiving inspection for every critical purchased part: model/revision,
  measured bounding dimensions, connector location, mass, and deviations from
  supplier geometry.
- Create assembly inspection, electrical bring-up, power fault injection,
  calibration, optical/radar alignment, display readability, thermal, ingress,
  shock/vibration, cable flex/snags, retention, zero repeatability, and user-fit
  tests as applicable.
- Include exact method, equipment, sample count, condition, limit, raw artifact,
  result, deviation, and disposition fields.
- Keep unexecuted rows `PENDING`; never pre-fill them as passing.

Use `assets/physical-acceptance.template.csv` as the minimum ledger.

### 8. Validate and report

- Copy `assets/product-realization-manifest.template.json` and fill every field.
- Run `scripts/validate_realization.py MANIFEST --root PRODUCT_ROOT`.
- Run project-native CAD, PCB, software, packaging, and test checks.
- Compare the final package against the original user journey and product-size
  intent. A technically valid assembly that is cumbersome or fragmented is a
  failed product decision.
- Report achieved closure, exact open gates, and the evidence that would close
  each gate. Do not describe pending procurement or physical tests as complete.

## Minimum deliverables

- authority and requirement-to-physical traceability;
- exact component/source register and BOM;
- supplier-evidence register with hashes and revision state;
- interface-control and power-tree documents;
- carrier schematic/layout/routing status and manufacturing notes;
- battery/protection and charger definition;
- mechanism, seal, contact, cable, and thermal definitions;
- dimensioned master assembly, custom-part STEP, and assembly-bound renders;
- render-lineage record binding every released presentation view to the master
  assembly and controlled mesh exports;
- host/user/accessory collision inputs and results;
- mass properties and all requested balance configurations;
- first-article receiving/acceptance ledger;
- machine-readable realization manifest and passing validation report.

## Stop conditions

Pause promotion—not useful engineering work—when any of these is true:

- the chosen component has no controlled order path or dimensional evidence;
- a critical interface pinout or connector orientation conflicts across sources;
- the assembly cannot fit without violating optical/RF, bend, thermal, hand,
  service, or structural keep-outs;
- a battery path lacks independent protection, current limiting, temperature
  sensing, fault isolation, or safe charging ownership;
- a claimed physical result lacks an actual article, method, instrument, and raw
  evidence.

Record the blocked gate, safe work that can continue, and the exact evidence or
decision needed to resume promotion.

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- Current local acceptance covers 100,000 unique 250-word requests, 100 ask families per skill, and 100% eligible target recall. See repository `VALIDATION.md`.

<!-- END SOLKRAFT SKILL INTEGRATION -->
