"""Verify Sprint 6 hardening invariants and emit an inspectable receipt."""
from __future__ import annotations

import json
from pathlib import Path

from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, contract_index


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main():
    errors = []

    contracts = _text("solkraft/contracts.py")
    policy = _text("solkraft/contract_policy.py")
    routing = _text("solkraft/routing.py")
    composer = _text("solkraft/skillpacks/solforge/scripts/compose_route.py")
    api = _text("solkraft/api.py")
    mcp = _text("solkraft/mcp_server.py")
    cli = _text("solkraft/__main__.py")
    interchange = _text("solkraft/interchange.py")

    forbidden = {
        "solkraft/contracts.py": ("AUTH_ORDER", "def apply_contracts(", "def violates("),
        "solkraft/contract_policy.py": ("AUTH_ORDER", "def _auth_rank("),
        "solkraft/routing.py": ("apply_contracts(",),
    }
    for path, patterns in forbidden.items():
        source = _text(path)
        for pattern in patterns:
            if pattern in source:
                errors.append(f"{path} still contains retired prototype symbol {pattern}")

    if "from solkraft.constraint_parser import" not in composer:
        errors.append("SolForge composer is not using the shared constraint parser")
    if "legacy_scope_allows" not in policy:
        errors.append("legacy scalar compatibility is not isolated behind capability adapter")
    if '{"contract_mode": "hardened"}' not in api:
        errors.append("REST routing does not default to hardened policy")
    if '{"contract_mode": "hardened"}' not in mcp:
        errors.append("MCP routing does not default to hardened policy")
    if 'else "hardened"' not in cli:
        errors.append("CLI routing does not default to hardened policy")
    if "opaque/unknown effects cannot be exported" not in interchange:
        errors.append("portable export does not explicitly fail closed on unknown effects")

    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    index = contract_index(catalog)
    entries = index.entries()
    counts = {}
    trust_counts = {}
    for entry in entries:
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
        state = (entry.get("trust") or {}).get("state", "unknown")
        trust_counts[state] = trust_counts.get(state, 0) + 1
        if entry["status"] in {"invalid", "unsupported"}:
            errors.append(f"{entry['id']} has non-usable status {entry['status']}")

    reviewed = sum(
        trust_counts.get(state, 0)
        for state in ("bundled-reviewed", "signed", "operator-trusted")
    )
    receipt = {
        "schema": "solkraft/hardening/v1",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "public_hardened_default": True,
        "post_hoc_filter_retired": "def apply_contracts(" not in contracts,
        "scalar_auth_order_retired": "AUTH_ORDER" not in contracts and "AUTH_ORDER" not in policy,
        "shared_constraint_parser": "from solkraft.constraint_parser import" in composer,
        "portable_unknown_effects_fail_closed": "opaque/unknown effects cannot be exported" in interchange,
        "contract_status_counts": counts,
        "trust_state_counts": trust_counts,
        "reviewed_bundled_count": reviewed,
        "bundled_contract_count": len(entries),
        "reviewed_bundled_coverage_complete": reviewed == len(entries) and len(entries) > 0,
        "execution_authorized": False,
    }

    target = ROOT / "build" / "hardening.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
