<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Evidence Ladder and Review Prompts

## Source screening

- Is the manufacturer identity, exact orderable configuration, revision, URL, acquisition date, SHA-256, and geometry class recorded?
- When a public manufacturer STEP/DXF/ECAD exists, was that exact original retained and used rather than a proxy?
- Is a payload really its declared type? Check magic/type, size, page/count or archive identity before classifying it as a source document.
- Does the source describe the actual selected part, not merely a product family or related part?

## Electrical and PCB boundaries

- Are all module contacts accounted, with explicit endpoints, unconnected rationale, and electrical ownership?
- Are connector orientation, pin one, mating side, flex direction, bend radius, voltage domains, signal constraints, grounding, test points, and protection defined?
- Is the record only logical mapping, or does it include schematic, placement, routed nets, DRC/ERC, stack-up, SI/PI and fabrication data? Do not collapse those statuses.

## Mechanical/CAD boundaries

- Does a single datum system transform source geometry, custom parts, host fixtures, accessories, and user envelopes?
- Are every body split, rail, latch, seal, contact, fastener, cable, thermal path, service operation, optical/RF aperture, and assembly direction physically motivated?
- Are zero/one/two accessory configurations represented in collision and balance checks? Clearly mark nominal CAD mass versus received mass.

## Render review

Reject a render if it has a generic rectangular slab, undefined rails, floating/intersecting parts, impossible wall thickness, inaccessible connector, non-removable battery, cable without a bend path, mislocated optic/sensor/control, or geometry unrelated to the controlled assembly.

Require front/rear/both-side and installed human/host context views, material/lighting readability, actual service seams, believable fasteners/vents, and a render-to-mesh-to-assembly SHA-256 lineage.

## Physical-evidence promotion

Never promote from a supplier drawing, logical map, CAD check, calculation, or rendered preview. Physical claims require received serialized parts or assembly, method, instrument IDs, calibration/uncertainty where relevant, operator/date, raw data, pass/fail limit, deviation, and disposition.
