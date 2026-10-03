import argparse
import json
from pathlib import Path

LAYERS = [
    "requirements", "source_evidence", "exact_order_code", "pinout",
    "supplier_step_or_measured_sample", "ecad_symbol", "ecad_footprint",
    "schematic_occurrence", "pcb_occurrence", "pcb_routing",
    "firmware_owner", "target_build", "cad_occurrence", "assembly_occurrence",
    "procurement_evidence", "first_article_evidence", "measured_validation",
    "render_lineage", "tolerance_and_derating", "rf_emi_coexistence",
    "dfm_dfa_dft", "calibration_and_provisioning", "lifecycle_and_pcn",
    "authorized_source_and_counterfeit_control", "environmental_and_reliability",
    "inspection_rework_and_service", "release_disposition"
]

def build(data):
    selections = data.get("selections", data if isinstance(data, list) else [])
    rows = []
    for selection in selections:
        sid = selection.get("selection_id")
        if not sid:
            raise ValueError("every selection requires selection_id")
        layers = {}
        for layer in LAYERS:
            value = selection.get(layer)
            layers[layer] = {
                "status": "CLOSED" if value not in (None, "", [], {}) else "OPEN",
                "evidence": value,
            }
        rows.append({
            "selection_id": sid,
            "product": selection.get("product"),
            "profile": selection.get("profile"),
            "revision": selection.get("revision"),
            "selection_state": selection.get("state"),
            "selection_reason": selection.get("selection_reason"),
            "layers": layers,
        })
    closed = sum(cell["status"] == "CLOSED" for row in rows for cell in row["layers"].values())
    total = len(rows) * len(LAYERS)
    return {"schema": "build-closure-matrix.v1", "rows": rows,
            "summary": {"selections": len(rows), "closed_cells": closed,
                        "open_cells": total - closed, "total_cells": total}}

def main():
    parser = argparse.ArgumentParser(description="Expand an engineering selection register into a build closure matrix.")
    parser.add_argument("register")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = build(json.loads(Path(args.register).read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")

if __name__ == "__main__":
    main()
