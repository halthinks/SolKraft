---
name: integrate-dayq-body-equipment-exos
description: Integrate DayQ movement with clothing, loads, armor, weapons, traversal equipment, exoskeletons, and mechs.
---

# Integrate DayQ Body, Equipment, and Exos

Read [BODY_EQUIPMENT_EXO_CONTRACT.md](references/BODY_EQUIPMENT_EXO_CONTRACT.md). Consume existing inventory/load, clothing, armor, traversal, exoskeleton, energy and weapon state.

## Workflow

1. Resolve body, garment, armor, pack and frame attachment compatibility.
2. Compute supported/unsupported mass, load offsets, bulk, snag, restriction, traction, protection and hand occupancy through existing owners.
3. Project those values into movement capability and animation contexts.
4. Add exoskeleton actuator assistance bounded by sensors, power, heat, condition, calibration, fit, frame rating and body contact.
5. Define power/fault transitions without teleporting mass or erasing inertia.
6. Align visible equipment through stable sockets and IK; authoritative attachments remain item identities.
7. Test equip/unequip, damage, spill, power loss, disconnect, restart, climbing, combat and recovery.

## Rules

- Do not let an exoskeleton make carried mass disappear.
- Do not let visual sockets author inventory or protection.
- Do not duplicate clothing, armor, inventory, energy or exoskeleton state.
- Recompute capability immediately after strap, pack, armor, actuator, battery or interface failure.

## Output

Deliver adapter fields, attachment/fit matrix, movement and animation projections, failure state machine, network/persistence mapping, fixtures, evidence and open gates.
