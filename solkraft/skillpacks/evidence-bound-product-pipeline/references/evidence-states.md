<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Evidence states

Use these states consistently. Add project-specific states only when their meaning is equally unambiguous.

| State | Meaning | Does not prove |
|---|---|---|
| `HISTORICAL` | Preserved prior input; not current authority | Current selection or compatibility |
| `CANDIDATE` | Plausible option with recorded source | Order selection, fit, electrical behavior |
| `SOURCE_BOUND` | Exact first-party source hash and allowed use are recorded | Receipt, fabrication, measurement, performance |
| `LOGICALLY_MAPPED_UNROUTED` | All relevant source contacts have controlled endpoints/reservations | Schematic, footprint, PCB layout, function |
| `DIGITALLY_CLOSED` | Current assembly/BOM/analysis closure gates passed | Received article or physical performance |
| `FABRICATION_READY` | Reviewed production package is released for build | A built, passing article |
| `PHYSICALLY_INSPECTED` | Serialized received item/article has controlled inspection evidence | System-level performance |
| `INSTRUMENTED_VALIDATED` | Measured scenario meets its stated acceptance criteria | Unmeasured scenarios or release approval |
| `RELEASE_READY` | All declared release evidence and independent validation are complete | Future revision performance |

## Minimum evidence record

For a claim, include: claim ID; product/revision; source path and SHA-256; owner; test or inspection method; date; equipment/fixture when physical; acceptance criterion; observed result; uncertainty/limitations; disposition; and the next blocking gate.

## Non-substitutions

- A public product page does not replace an exact drawing.
- A supplier family archive does not replace the exact order code.
- A package drawing does not replace a full schematic or footprint approval.
- A render does not replace CAD, BOM, or a physical inspection.
- A test plan does not replace test results.
- A simulation or development-host benchmark does not replace an instrumented target-board benchmark.
- A passed static scan does not replace a completed dependency advisory, system verification, or physical validation.
