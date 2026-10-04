import json
import sys

from solkraft.__main__ import main
from solkraft.catalog import SkillCatalog
from solkraft.contract_loader import load_skill_contract
from solkraft.contract_schema import validate_v1_document
from solkraft.contracts import apply_contracts, contract_from_node, excluded_effects
from solkraft.routing import catalog_graph


def test_quoted_exclusion_does_not_count():
    assert excluded_effects('Inspect the repo. The log says "do not deploy" as a quote.') == []
    assert excluded_effects("Inspect the repo. Do not deploy anything.") == ["deploy"]


def test_legacy_read_only_graph_node_is_not_promoted_to_reviewed_contract():
    contract = contract_from_node({
        "effect": False,
        "inputs": ["user objective"],
        "exit_evidence": "Observed behavior matches the request.",
    })
    assert contract["declared"] is True
    assert contract["status"] == "legacy"
    assert contract["side_effects"] == []
    assert contract["auth_scope"] == "none"
    assert contract["test_contract"] == "Observed behavior matches the request."


def test_graph_unknown_skill_is_opaque_not_harmless(tmp_path):
    folder = tmp_path / "mystery"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: mystery\ndescription: Do a useful unknown thing.\n---\n",
        encoding="utf-8",
    )
    graph = catalog_graph(SkillCatalog([tmp_path]))
    node = graph["nodes"]["mystery"]
    assert node["contract_status"] == "opaque"
    assert node["effect"] is None
    assert node["side_effects"] is None
    assert node["auth_scope"] is None


def test_declared_side_effect_is_rejected_without_loading_a_body():
    graph = {"nodes": {
        "deployer": {
            "effect": True,
            "side_effects": ["deploy"],
            "auth_scope": "external-effect",
            "test_contract": "Deployment record matches the requested target.",
            "inputs": ["target"],
        },
        "reader": {
            "effect": False,
            "inputs": ["repository"],
            "exit_evidence": "Inspection cites files and revisions.",
        },
    }}
    result = apply_contracts(
        {
            "selected": ["reader", "deployer"],
            "stages": [{"stage": 1, "text": "Inspect then deploy", "selected": ["reader", "deployer"]}],
            "skills": [{"id": "reader"}, {"id": "deployer"}],
        },
        graph,
        "Inspect the repository. Do not deploy anything.",
    )
    assert result["selected"] == ["reader"]
    assert result["contract_rejections"][0]["id"] == "deployer"
    assert result["contracts"]["reader"]["test_contract"]
    assert result["execution_authorized"] is False
    assert result["stages"][0]["selected"] == ["reader"]
    assert result["selection_status"] == "matched"


def test_unrelated_external_effect_is_not_rejected_by_specific_exclusion():
    graph = {"nodes": {"sender": {
        "side_effects": ["send"],
        "auth_scope": "external-effect",
        "test_contract": "Message receipt matches the request.",
    }}}
    result = apply_contracts(
        {"selected": ["sender"], "stages": [{"stage": 1, "text": "Send the report", "selected": ["sender"]}]},
        graph,
        "Send the report. Do not deploy anything.",
    )
    assert result["selected"] == ["sender"]
    assert result["contract_rejections"] == []
    assert result["selection_status"] == "matched"


def test_required_stage_becomes_blocked_when_contract_rejects_only_skill():
    graph = {"nodes": {"deployer": {
        "side_effects": ["deploy"],
        "auth_scope": "external-effect",
        "test_contract": "Deployment is healthy.",
    }}}
    result = apply_contracts(
        {
            "selected": ["deployer"],
            "stages": [{"stage": 1, "text": "Deploy the service", "selected": ["deployer"]}],
        },
        graph,
        "Deploy the service but do not deploy anything.",
    )
    assert result["selected"] == []
    assert result["selection_status"] == "blocked"
    assert result["blocked_stages"][0]["rejected"] == ["deployer"]
    assert result["execution_authorized"] is False


def test_auth_scope_is_a_selection_constraint():
    graph = {"nodes": {"writer": {
        "side_effects": [],
        "auth_scope": "write-local",
        "test_contract": "Diff matches the requested change.",
        "inputs": ["repository"],
    }}}
    result = apply_contracts(
        {"selected": ["writer"], "stages": []},
        graph,
        "Implement the fix.",
        allowed_auth="read",
    )
    assert result["selected"] == []
    assert result["selection_status"] == "blocked"
    assert "exceeds read" in result["contract_rejections"][0]["reasons"][0]


def test_valid_sidecar_declares_contract(tmp_path):
    folder = tmp_path / "sidecar-skill"
    folder.mkdir()
    entrypoint = folder / "SKILL.md"
    entrypoint.write_text(
        "---\nname: sidecar-skill\ndescription: Deploy a release.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        """
schema_version: "1.0"
skill_id: sidecar-skill
contract_revision: 1
effects:
  - deploy
authority:
  capabilities: []
  resources: []
  legacy_scope: external-effect
verification:
  description: Deployment health check passes.
""".strip() + "\n",
        encoding="utf-8",
    )
    contract = load_skill_contract(entrypoint, expected_skill_id="sidecar-skill")
    assert contract["status"] == "declared"
    assert contract["side_effects"] == ["deploy"]
    assert contract["auth_scope"] == "external-effect"


def test_unsupported_sidecar_major_fails_closed(tmp_path):
    folder = tmp_path / "future-skill"
    folder.mkdir()
    entrypoint = folder / "SKILL.md"
    entrypoint.write_text(
        "---\nname: future-skill\ndescription: Future contract skill.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        "schema_version: \"2.0\"\nskill_id: future-skill\ncontract_revision: 1\n",
        encoding="utf-8",
    )
    contract = load_skill_contract(entrypoint, expected_skill_id="future-skill")
    assert contract["status"] == "unsupported"
    assert contract["declared"] is False


def test_contract_v1_rejects_unknown_core_fields():
    errors = validate_v1_document({
        "schema_version": "1.0",
        "skill_id": "demo",
        "contract_revision": 1,
        "surprise": True,
    })
    assert errors == ["unknown top-level fields: surprise"]


def test_cli_route_never_authorizes_execution(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["solkraft", "route", "Do not deploy or delete anything."])
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["execution_authorized"] is False
