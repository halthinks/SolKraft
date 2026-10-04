from pathlib import Path

import yaml

from scripts.migrate_contracts import inferred_contract
from solkraft.contract_loader import load_skill_contract
from solkraft.trust import resolve_trust


def test_inferred_sidecar_is_typed_but_remains_legacy(tmp_path):
    node = {
        "effect": False,
        "domain": "software",
        "selection": "automatic",
        "inputs": ["repository"],
        "outputs": ["inspection report"],
        "exit_evidence": "Report cites inspected files.",
        "path": "../demo/SKILL.md",
    }
    data = inferred_contract("demo", node)
    assert data["effects"] == []
    assert data["inputs"][0]["schema"] == {}
    assert data["provenance"]["inferred"] is True

    folder = tmp_path / "demo"
    folder.mkdir()
    entrypoint = folder / "SKILL.md"
    entrypoint.write_text(
        "---\nname: demo\ndescription: Inspect a repository.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        yaml.safe_dump(data, sort_keys=False),
        encoding="utf-8",
    )
    contract = load_skill_contract(entrypoint, expected_skill_id="demo")
    assert contract["status"] == "legacy"
    trust = resolve_trust("demo", contract, registry={})
    assert trust["state"] == "legacy-inferred"


def test_effectful_or_unknown_legacy_node_requires_manual_contract():
    assert inferred_contract("danger", {"effect": True}) is None
    assert inferred_contract("unknown", {}) is None
