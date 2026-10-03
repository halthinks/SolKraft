# Closure and evidence model

## Closure levels

| Level | Required evidence |
|---|---|
| `CONCEPT` | Requirements and candidate architecture only. |
| `DIGITAL_PACKAGING_CLOSED` | Valid master CAD; supplier or controlled nominal envelopes; clearances, cable bends, thermal paths, collision screens, calculated mass/balance, BOM, and traceable render meshes. |
| `EVT_RELEASE_CANDIDATE` | Digital closure plus released drawings, reviewed schematic/PCB, cleared fabrication holds, inspection plan, and ordered exact parts. |
| `PHYSICALLY_VERIFIED` | Serialized articles, received-part reconciliation, calibrated measurements, raw test records, and resolved deviations. |
| `PRODUCTION_RELEASED` | Qualified design, manufacturing controls, compliance evidence, approved suppliers, production test, and signed release. |

## Evidence classes

- `RECEIVED_MEASURED`: identified physical sample plus dated instrument record.
- `SUPPLIER_EXACT`: exact supplier STEP/drawing for the exact ordered revision.
- `SUPPLIER_DRAWING`: manufacturer drawing, but geometry or revision remains incomplete.
- `SELECTED_NOMINAL`: selected order code represented by published dimensions.
- `DESIGN_TO_SPEC`: controlled custom design geometry.
- `PRESENTATION_ONLY`: visually useful but never dimensional evidence.

## Non-substitution rules

- A render cannot prove clearance, mass, thermal performance, or fit.
- An envelope cannot replace received measurement for a custom mating footprint.
- A calculation cannot become a measured result.
- A DRC pass cannot clear incomplete connectivity, SI/PI, stackup, DFM, or review holds.
- Unit tests cannot prove optical, radar, detector, BB tracking, runtime, ingress, or drop performance.
- Generated imagery cannot become CAD authority even when it closely resembles the CAD.

## Required configuration accounting

List each supported state independently: internal power only; every single external source; all simultaneous-source combinations; direct and remote accessories; optic installed or absent; and every service configuration that changes mass, balance, collision, sealing, or cable routing.
