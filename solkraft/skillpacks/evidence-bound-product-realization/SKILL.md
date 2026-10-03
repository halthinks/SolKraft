---
name: evidence-bound-product-realization
description: Realize a physical product line from user experience and software requirements through exact supplier selection, pinouts, logical PCB mapping, CAD-bound enclosure work, render lineage, and first-article gates. Use for hardware products or product families that need a repeatable path from concept to source-bound, digitally closed, and physically verified evidence without proxy geometry, invented dimensions, or false readiness claims.
---

# Evidence-Bound Product Realization

Turn a product intent into an executable, source-traceable realization package.
Preserve existing work as evidence, never as automatic current authority.

## Frame the authority

1. Identify the product name, customer capability, user journey, software behaviors, size/mounting constraints, and approved exterior-language references.
2. Freeze explicit locks, rejected directions, historical identities, and the strongest truthful current readiness level.
3. Inventory the workspace before writing. Classify every input as `RECEIVED_MEASURED`, `SUPPLIER_EXACT`, `SUPPLIER_DRAWING`, `SELECTED_NOMINAL`, `DESIGN_TO_SPEC`, `PRESENTATION_ONLY`, historical, or rejected.
4. Create or update one authority record, source index with SHA-256 hashes, conflict register, and release/acceptance matrix. Do not globally rename legacy surfaces; use explicit compatibility maps.

## Execute the dependency order

1. **Behavior → requirements.** Derive sensing, compute, display, controls, power, thermal, radio, storage, service, mounting, calibration, and degraded-mode requirements from concrete software/user behavior.
2. **Requirements → exact sources.** Select each critical bought part only from a manufacturer-controlled identity, revision/order path, and geometry/pinout source. If a manufacturer public product page exposes STEP/DXF/ECAD, retain that original source, hash it, and use it. Do not replace it with a generic model.
3. **Sources → electrical interface.** Account every selected module contact. Create connector orientation, logical net owner, endpoint, voltage domain, high-speed/RF/control constraint, unused-contact disposition, and open-routing status. A pin map is not a schematic, layout, DRC, or fabricable board.
4. **Interfaces → internal package.** Define datums, exact/source-drawing component envelopes, optical/RF zones, cable and FPC bend volumes, connector insertion/removal, battery swell and protection, thermal interfaces, service access, structural load paths, and assembly order.
5. **Internal package → product exterior.** Shape only after the internal constraints are controlled. Give each modular body a real subsystem boundary, retention, sealing, connector boundary, assembly direction, and service rule. Do not accept a rectangular packaging block, decorative seam, unsupported rail, or fake vent.
6. **Package → verified digital outputs.** Produce controlled CAD/STEP, collision and balance inputs/results, power/thermal calculations marked as predictions, BOM reconciliation, and render meshes. Create photoreal presentation renders from controlled geometry; materials and context may change, but product geometry may not.
7. **Digital package → first article.** Write receiving, metrology, assembly, electrical, calibration, thermal, balance, interaction, ingress, retention, and workload test records. Keep unexecuted rows `PENDING`.

Read [references/evidence-ladder.md](references/evidence-ladder.md) before selecting a completion label or issuing an external-facing product claim.

## Critical evidence rules

- Use public original STEP/DXF/ECAD when the manufacturer exposes it. If the source is missing, access-rejected, malformed, or an HTML response named `.pdf`, record the failure, retain it only as negative evidence when useful, and leave the dependent geometry gate open.
- Do not infer a mechanical standard, footprint, lens datum, rail profile, contact pitch, battery cavity, or measured mass from images, a generic library model, a related part, a blog, or an earlier product revision.
- Do not call cells "parallel" merely because two power pods exist. Define protected multi-input sharing, source isolation, charge ownership, limits, hot-removal behavior, telemetry, and faults. Keep raw battery paralleling prohibited unless a specific qualified electrical architecture says otherwise.
- Keep local observations distinguishable from remote, stale, degraded, or lower-confidence reports. An association must preserve provenance and uncertainty; it cannot manufacture sensor truth.
- Render lineage proves ancestry to a controlled mesh, not physical manufacture, optical alignment, or human fit.

## Closure decision

Use the strongest evidence level that is actually supported:

| Level | Required evidence | Not implied |
|---|---|---|
| `CONCEPT` | Requirements and provisional architecture | selected parts, fit, CAD, or performance |
| `SOURCE_BOUND` | Exact identities and controlled source/pinout/geometry evidence for admitted parts | closed assembly, routing, or physical result |
| `DIGITAL_CLOSED` | Dimension chain, controlled assembly, interfaces, routing status, service/collision/balance/thermal analyses | fabricated or measured hardware |
| `FIRST_ARTICLE_READY` | Fabrication outputs, inspection plans, limits, acquisition/assembly sequence | received/working article |
| `PHYSICALLY_VERIFIED` | Serialized article, instrument/sample/operator/date/raw evidence, disposition | production qualification |

## Validate every increment

1. Run focused source/hash/schema validators after each source or contract change.
2. Run product-specific software, pinout, PCB-map, CAD, collision, render-lineage, and release-matrix checks affected by the change.
3. Rebuild and test shipped runtime packages when production source changes; refresh audit receipts only against the exact changed inputs.
4. Run an independent challenge for proxy geometry, stale names, false merges, unclosed routes, impossible service/bend/thermal assumptions, render-to-BOM mismatch, and exaggerated claims.
5. Update the evidence index only after the artifacts are validated. State exact open gates and the evidence needed to close each one.

## Output contract

Deliver an authority package containing the product registry, source manifest, requirement traceability, component register/BOM, interface and pinout maps, PCB status, CAD/assembly and render lineage, first-article acceptance matrix, validation reports, compatibility map, and known-limitations report. Keep the physical claim boundary visible in every release index.
