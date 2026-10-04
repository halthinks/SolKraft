"""Validate the bundled compact contract index and emit a CI receipt."""
from __future__ import annotations

import json
from pathlib import Path

from solkraft.catalog import SkillCatalog
from solkraft.contract_verify import SUPPORTED_CHECKS
from solkraft.routing import BUNDLE_ROOT, contract_index, get_graph, graph_generation


ROOT = Path(__file__).resolve().parents[1]


def main():
    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    index = contract_index(catalog)
    first = index.public()
    graph = get_graph()
    second_refresh = index.refresh(
        catalog.records(),
        legacy_nodes=graph.get("nodes", {}),
        graph_generation=graph_generation(graph),
    )

    errors = []
    for entry in first["entries"]:
        if entry["status"] in {"invalid", "unsupported"}:
            errors.append(f"{entry['id']}: contract status {entry['status']}")
        if entry["status"] == "declared":
            checks = (entry.get("verification") or {}).get("checks") or []
            if not checks:
                errors.append(f"{entry['id']}: declared contract lacks verification checks")
            for check in checks:
                if check.get("type") not in SUPPORTED_CHECKS:
                    errors.append(f"{entry['id']}: unsupported verification type {check.get('type')}")

    receipt = {
        "schema": "solkraft/contract-index-check/v1",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "generation": first["generation"],
        "count": first["count"],
        "last_refresh": first["last_refresh"],
        "second_refresh": second_refresh,
        "incremental_cache_reused_all": (
            not second_refresh["changed"]
            and len(second_refresh["reused"]) == first["count"]
        ),
        "index_counts": {
            name: len(values)
            for name, values in first["indexes"].items()
        },
    }
    target = ROOT / "build" / "contract-index.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    if not receipt["incremental_cache_reused_all"]:
        raise SystemExit("contract index did not reuse unchanged entries")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
