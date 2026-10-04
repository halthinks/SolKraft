from solkraft.catalog import SkillCatalog
from solkraft.contract_loader import load_skill_contract
from solkraft.contract_policy import evaluate_contract, normalize_policy
from solkraft.contract_schema import validate_v1_document
from solkraft.contracts import contract_from_node
from solkraft.route_validation import validate_route
from solkraft.routing import route_request
from solkraft.skillpacks.solforge.scripts.compose_route import compose_route


def _write_skill(root, folder_name, skill_id, description, contract=None):
    folder = root / folder_name
    folder.mkdir()
    entrypoint = folder / "SKILL.md"
    entrypoint.write_text(
        f"---\nname: {skill_id}\ndescription: {description}\n---\n",
        encoding="utf-8",
    )
    if contract is not None:
        (folder / "contract.yaml").write_text(contract.strip() + "\n", encoding="utf-8")
    return entrypoint


def test_contract_v1_requires_typed_bindings_and_namespaced_effects():
    errors = validate_v1_document({
        "schema_version": "1.0",
        "skill_id": "demo",
        "contract_revision": 1,
        "inputs": ["repository"],
        "effects": ["deploy"],
    })
    assert "inputs[0] must be an object" in errors
    assert "invalid namespaced effect: 'deploy'" in errors


def test_contract_and_entrypoint_digests_are_independent(tmp_path):
    entrypoint = _write_skill(
        tmp_path,
        "deploy",
        "deploy-skill",
        "Deploy a release.",
        """
schema_version: "1.0"
skill_id: deploy-skill
contract_revision: 1
inputs:
  - name: repository
    required: true
    schema:
      type: string
outputs:
  - name: receipt
    schema:
      type: object
effects:
  - deployment.release
authority:
  capabilities:
    - deployment.write
  resources:
    - environment:staging
verification:
  mode: declarative
  checks:
    - id: receipt-present
      type: artifact_exists
""",
    )
    first = load_skill_contract(entrypoint, expected_skill_id="deploy-skill")
    entrypoint.write_text(
        "---\nname: deploy-skill\ndescription: Deploy a release.\n---\nchanged\n",
        encoding="utf-8",
    )
    second = load_skill_contract(entrypoint, expected_skill_id="deploy-skill")
    assert first["contract_digest"] == second["contract_digest"]
    assert first["entrypoint_digest"] != second["entrypoint_digest"]
    assert first["capabilities"] == ["deployment.write"]


def test_structured_policy_denies_effect_and_missing_capability():
    contract = contract_from_node({
        "contract_status": "declared",
        "side_effects": ["deployment.release"],
        "authority": {
            "capabilities": ["deployment.write"],
            "resources": ["environment:production"],
        },
        "verification": {
            "mode": "declarative",
            "checks": [{"id": "healthy", "type": "health_check"}],
        },
    })
    policy = normalize_policy(
        {
            "denied_effects": ["deployment.*"],
            "granted_capabilities": ["repo.read"],
        },
        "Deploy the release.",
    )
    decision = evaluate_contract(contract, policy)
    assert decision["status"] == "denied"
    assert any("deployment.release" in reason for reason in decision["reasons"])
    assert any("deployment.write" in reason for reason in decision["reasons"])


def test_objective_constraints_add_to_structured_policy():
    policy = normalize_policy(
        {"denied_effects": ["repo.merge"]},
        "Inspect it and do not deploy anything.",
    )
    assert "repo.merge" in policy.denied_effects
    assert "deployment.release" in policy.denied_effects


def test_strict_policy_rejects_opaque_contract():
    decision = evaluate_contract(
        contract_from_node({}),
        normalize_policy({"contract_mode": "strict"}, "Inspect it."),
    )
    assert decision["status"] == "denied"
    assert "opaque contract rejected by strict policy" in decision["reasons"]


def test_composer_reports_prefiltered_candidate():
    graph = {
        "nodes": {
            "solforge-workflow-writing-draft": {
                "id": "solforge-workflow-writing-draft",
                "effect": False,
            }
        },
        "edges": [],
    }
    result = compose_route(
        graph,
        "Write a memo document.",
        blocked_skills={"solforge-workflow-writing-draft"},
    )
    assert result["selected"] == []
    assert result["unselected_requested_stages"][0]["candidate"] == "solforge-workflow-writing-draft"
    assert result["unselected_requested_stages"][0]["reason"] == "candidate inadmissible by contract policy"


def test_route_validation_invalidates_selected_dependency():
    result = {
        "selected": ["producer", "consumer"],
        "stages": [
            {"stage": 1, "text": "produce", "selected": ["producer"]},
            {"stage": 2, "text": "consume", "selected": ["consumer"]},
        ],
        "unselected_requested_stages": [],
    }
    decisions = {
        "producer": {"status": "allowed", "capabilities": [], "resources": []},
        "consumer": {"status": "denied", "capabilities": [], "resources": []},
    }
    graph = {
        "edges": [{
            "from": "producer",
            "to": "consumer",
            "type": "method",
            "condition": "selected together for this route",
        }]
    }
    validated = validate_route(
        result,
        graph,
        decisions,
        policy_public={"denied_effects": [], "contract_mode": "strict"},
        original_selected=["producer", "consumer"],
    )
    assert validated["selected"] == []
    assert validated["selection_status"] == "blocked"
    assert validated["broken_dependencies"][0]["blocked"] == "producer"


def test_public_route_strict_policy_blocks_opaque_explicit_skill(tmp_path):
    _write_skill(tmp_path, "mystery", "mystery", "Inspect a mystery repository.")
    result = route_request(
        SkillCatalog([tmp_path]),
        "Inspect the mystery repository.",
        explicit=["mystery"],
        policy={"contract_mode": "strict"},
    )
    assert result["selected"] == []
    assert result["selection_status"] == "blocked"
    assert result["contract_decisions"]["mystery"]["status"] == "denied"
    assert result["execution_authorized"] is False


def test_public_route_repairs_denied_mapped_skill_once(tmp_path):
    _write_skill(
        tmp_path,
        "blocked-writing",
        "solforge-workflow-writing-draft",
        "Write a memo document.",
        """
schema_version: "1.0"
skill_id: solforge-workflow-writing-draft
contract_revision: 1
effects:
  - messaging.send
verification:
  mode: declarative
  checks:
    - id: draft-present
      type: artifact_exists
""",
    )
    _write_skill(
        tmp_path,
        "safe-writing",
        "safe-writing",
        "Write a memo document safely.",
        """
schema_version: "1.0"
skill_id: safe-writing
contract_revision: 1
effects: []
verification:
  mode: declarative
  checks:
    - id: draft-present
      type: artifact_exists
""",
    )
    result = route_request(
        SkillCatalog([tmp_path]),
        "Write a memo document.",
        policy={"denied_effects": ["messaging.send"], "contract_mode": "strict"},
    )
    assert result["selected"] == ["safe-writing"]
    repair = result["selection_trace"]["contract_repair"]
    assert repair["bounded_passes"] == 1
    assert repair["repaired"][0]["rejected"] == "solforge-workflow-writing-draft"
    assert repair["repaired"][0]["replacement"] == "safe-writing"
    assert result["execution_authorized"] is False
