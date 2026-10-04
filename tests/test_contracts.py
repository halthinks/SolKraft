import json
import sys

from solkraft.__main__ import main
from solkraft.catalog import SkillCatalog
from solkraft.constraint_parser import excluded_effects
from solkraft.contract_fixtures import run_contract_fixtures
from solkraft.contract_loader import load_skill_contract
from solkraft.contract_policy import evaluate_contract, normalize_policy
from solkraft.contract_schema import validate_v1_document
from solkraft.contracts import contract_from_node
from solkraft.routing import catalog_graph, route_request


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


def test_specific_effect_policy_rejects_matching_declared_effect_only():
    deploy = contract_from_node({
        "contract_status": "declared",
        "side_effects": ["deployment.release"],
        "authority": {"capabilities": [], "resources": []},
    })
    send = contract_from_node({
        "contract_status": "declared",
        "side_effects": ["messaging.send"],
        "authority": {"capabilities": [], "resources": []},
    })
    policy = normalize_policy(
        {"denied_effects": ["deployment.*"], "contract_mode": "strict"},
        "Send the report. Do not deploy anything.",
    )
    assert evaluate_contract(deploy, policy)["status"] == "denied"
    assert evaluate_contract(send, policy)["status"] == "allowed"


def test_declared_v1_contract_ignores_legacy_scalar_ceiling():
    contract = contract_from_node({
        "contract_status": "declared",
        "side_effects": [],
        "auth_scope": "external-effect",
        "authority": {
            "capabilities": ["repo.read"],
            "resources": [],
        },
    })
    decision = evaluate_contract(
        contract,
        normalize_policy(
            {
                "legacy_auth_scope": "read",
                "grant": {"capabilities": ["repo.read"], "resources": []},
            },
            "Inspect.",
        ),
    )
    assert decision["status"] == "allowed"


def test_legacy_scalar_compatibility_still_blocks_old_metadata():
    contract = contract_from_node({
        "effect": False,
        "auth_scope": "write-local",
        "exit_evidence": "Diff exists.",
    })
    decision = evaluate_contract(
        contract,
        normalize_policy({"legacy_auth_scope": "read"}, "Implement the fix."),
    )
    assert decision["status"] == "denied"
    assert "legacy auth scope" in decision["reasons"][0]


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
  - deployment.release
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
    assert contract["side_effects"] == ["deployment.release"]
    assert contract["auth_scope"] == "external-effect"
    assert contract["contract_digest"].startswith("sha256:")
    assert contract["entrypoint_digest"].startswith("sha256:")


def test_unsupported_sidecar_major_fails_closed(tmp_path):
    folder = tmp_path / "future-skill"
    folder.mkdir()
    entrypoint = folder / "SKILL.md"
    entrypoint.write_text(
        "---\nname: future-skill\ndescription: Future contract skill.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        'schema_version: "2.0"\nskill_id: future-skill\ncontract_revision: 1\n',
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


def test_python_library_remains_legacy_compatible_by_default(tmp_path):
    folder = tmp_path / "opaque"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: opaque\ndescription: Inspect an opaque thing.\n---\n",
        encoding="utf-8",
    )
    result = route_request(
        SkillCatalog([tmp_path]),
        "Inspect the opaque thing.",
        explicit=["opaque"],
    )
    assert result["selected"] == ["opaque"]
    assert result["execution_authorized"] is False


def test_cli_route_defaults_to_hardened_policy(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["solkraft", "route", "Do not deploy or delete anything."])
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["route_policy"]["contract_mode"] == "hardened"
    assert result["execution_authorized"] is False


def test_contract_v1_validates_executable_fixture_shape():
    errors = validate_v1_document({
        "schema_version": "1.0",
        "skill_id": "demo",
        "contract_revision": 1,
        "fixtures": {
            "selection": [
                {
                    "id": "select-demo",
                    "objective": "Use the demo capability.",
                    "expected_selected": ["demo"],
                }
            ],
            "policy": [
                {
                    "id": "deny-demo",
                    "policy": {"contract_mode": "hardened"},
                    "expected_status": "denied",
                }
            ],
        },
    })
    assert errors == []


def test_contract_v1_rejects_malformed_fixture():
    errors = validate_v1_document({
        "schema_version": "1.0",
        "skill_id": "demo",
        "contract_revision": 1,
        "fixtures": {
            "selection": [{"id": "bad", "objective": "", "expected_selected": "demo"}],
        },
    })
    assert "fixtures.selection[0].objective must be a non-empty string" in errors
    assert "fixtures.selection[0].expected_selected must be a list of skill IDs" in errors


def test_bundled_declared_contract_fixtures_execute():
    catalog = SkillCatalog([__import__("solkraft.routing", fromlist=["BUNDLE_ROOT"]).BUNDLE_ROOT])
    record = next(
        item for item in catalog.records()
        if item.id == "solforge-workflow-software-security"
    )
    contract = load_skill_contract(
        record.entrypoint,
        legacy_node=catalog_graph(catalog)["nodes"].get(record.id),
        expected_skill_id=record.name,
    )
    assert contract["status"] == "declared"
    receipt = run_contract_fixtures(catalog, record.id, contract)
    assert receipt["total"] == 3
    assert receipt["failed"] == 0
