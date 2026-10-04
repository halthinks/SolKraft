from solkraft.capabilities import (
    CapabilityGrant,
    missing_capabilities,
    missing_resources,
    normalize_grant,
)
from solkraft.catalog import SkillCatalog
from solkraft.contract_policy import evaluate_contract, normalize_policy
from solkraft.contracts import contract_from_node
from solkraft.dataflow import schema_compatible
from solkraft.routing import route_request


def _write_skill(root, skill_id, description, contract):
    folder = root / skill_id
    folder.mkdir()
    entrypoint = folder / "SKILL.md"
    entrypoint.write_text(
        f"---\nname: {skill_id}\ndescription: {description}\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(contract.strip() + "\n", encoding="utf-8")


def test_capabilities_are_sets_not_scalar_authority():
    assert missing_capabilities(["local.write"], ["net.connect"]) == ["local.write"]
    assert missing_capabilities(["repo.read"], ["repo.*"]) == []


def test_resource_selectors_are_independent():
    assert missing_resources(["environment:production"], ["environment:staging"]) == [
        "environment:production"
    ]
    assert missing_resources(["environment:production"], ["environment:*"]) == []


def test_expired_host_grant_denies_required_capability():
    grant = normalize_grant({
        "grant_id": "old",
        "capabilities": ["deployment.write"],
        "resources": ["environment:production"],
        "expires_at": "2000-01-01T00:00:00Z",
    })
    assert isinstance(grant, CapabilityGrant)
    contract = contract_from_node({
        "contract_status": "declared",
        "side_effects": [],
        "authority": {
            "capabilities": ["deployment.write"],
            "resources": ["environment:production"],
        },
    })
    decision = evaluate_contract(
        contract,
        normalize_policy({"grant": grant.public()}, "Deploy."),
    )
    assert decision["status"] == "denied"
    assert "host grant expired" in decision["reasons"]


def test_host_grant_matches_capability_and_resource():
    contract = contract_from_node({
        "contract_status": "declared",
        "side_effects": [],
        "authority": {
            "capabilities": ["repo.read"],
            "resources": ["repo:example/project"],
        },
    })
    decision = evaluate_contract(
        contract,
        normalize_policy({
            "grant": {
                "grant_id": "snapshot-1",
                "capabilities": ["repo.*"],
                "resources": ["repo:example/*"],
            }
        }, "Inspect the repository."),
    )
    assert decision["status"] == "allowed"
    assert decision["grant_id"] == "snapshot-1"


def test_schema_compatibility_is_conservative():
    assert schema_compatible({"type": "object"}, {"type": "object"})
    assert not schema_compatible({"type": "string"}, {"type": "object"})
    assert not schema_compatible({}, {"type": "object"})


def test_public_route_adds_unique_typed_producer(tmp_path):
    _write_skill(
        tmp_path,
        "producer",
        "Prepare a normalized dataset artifact.",
        """
schema_version: "1.0"
skill_id: producer
contract_revision: 1
outputs:
  - name: dataset
    schema:
      type: object
effects: []
verification:
  mode: declarative
  checks:
    - id: dataset-present
      type: artifact_exists
""",
    )
    _write_skill(
        tmp_path,
        "consumer",
        "Analyze a normalized dataset artifact.",
        """
schema_version: "1.0"
skill_id: consumer
contract_revision: 1
inputs:
  - name: dataset
    required: true
    source: skill-output
    schema:
      type: object
effects: []
verification:
  mode: declarative
  checks:
    - id: analysis-present
      type: artifact_exists
""",
    )
    result = route_request(
        SkillCatalog([tmp_path]),
        "Analyze the normalized dataset.",
        explicit=["consumer"],
        policy={"contract_mode": "strict"},
    )
    assert result["selected"] == ["producer", "consumer"]
    assert result["dataflow"]["explanations"][0]["producer"] == "producer"
    assert result["dataflow"]["explanations"][0]["consumer"] == "consumer"
    assert result["selection_status"] == "matched"
    assert result["execution_authorized"] is False


def test_required_user_input_is_elicitable_until_supplied(tmp_path):
    _write_skill(
        tmp_path,
        "consumer",
        "Analyze an uploaded dataset.",
        """
schema_version: "1.0"
skill_id: consumer
contract_revision: 1
inputs:
  - name: dataset
    required: true
    source: user
    schema:
      type: object
effects: []
verification:
  mode: declarative
  checks:
    - id: analysis-present
      type: artifact_exists
""",
    )
    catalog = SkillCatalog([tmp_path])
    blocked = route_request(
        catalog,
        "Analyze the uploaded dataset.",
        explicit=["consumer"],
        policy={"contract_mode": "strict"},
    )
    assert blocked["selection_status"] == "partially_blocked"
    assert blocked["dataflow"]["inputs"]["consumer:dataset"]["status"] == "elicitable"

    ready = route_request(
        catalog,
        "Analyze the uploaded dataset.",
        explicit=["consumer"],
        context={"available_inputs": ["dataset"]},
        policy={"contract_mode": "strict"},
    )
    assert ready["selection_status"] == "matched"
    assert ready["dataflow"]["inputs"]["consumer:dataset"]["status"] == "available"
