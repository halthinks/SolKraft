from pathlib import Path

from fastapi.testclient import TestClient

from solkraft.api import create_app
from solkraft.catalog import SkillCatalog


def test_catalog_pagination_preserves_search_order_and_total(tmp_path):
    for index in range(25):
        folder = tmp_path / f"skill-{index:02}"
        folder.mkdir()
        (folder / "SKILL.md").write_text(
            f"---\nname: skill-{index:02}\ndescription: Review release artifacts.\n---\n", encoding="utf-8")
    with TestClient(create_app(SkillCatalog([tmp_path]), api_key="test-key")) as client:
        headers = {"Authorization": "Bearer test-key"}
        first = client.get('/v1/skills?q=release&limit=12&offset=0', headers=headers).json()
        last = client.get('/v1/skills?q=release&limit=12&offset=24', headers=headers).json()
        assert first['total'] == last['total'] == 25
        assert first['count'] == 12 and last['count'] == 1
        assert first['items'][0]['id'] == 'skill-00'
        assert last['items'][0]['id'] == 'skill-24'


def test_api_lists_routes_and_returns_selected_skill_only(tmp_path):
    root = tmp_path / "skills"
    folder = root / "data-chart"
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text("---\nname: data-chart\ndescription: Build charts from customer data.\n---\n\n# Data chart skill\n", encoding="utf-8")
    (folder / "contract.yaml").write_text(
        """
schema_version: "1.0"
skill_id: data-chart
contract_revision: 1
effects: []
verification:
  mode: declarative
  checks:
    - id: chart-present
      type: field_present
      field: result
""".strip() + "\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([root]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-key"}

    assert client.get("/healthz").status_code == 200
    assert client.get("/v1/skills", headers=headers).json()["count"] == 1
    detail = client.get("/v1/skills/data-chart", headers=headers).json()
    assert "# Data chart skill" in detail["content"]
    route = client.post("/v1/route", headers=headers, json={"objective": "Build charts from customer data"}).json()
    assert route["selected"] == ["data-chart"]
    assert route["execution_authorized"] is False


def test_api_rejects_missing_or_invalid_api_key(tmp_path):
    app = create_app(SkillCatalog([]), api_key="test-key", require_api_key=True)
    client = TestClient(app)

    assert client.get("/v1/skills").status_code == 401
    assert client.get("/v1/skills", headers={"Authorization": "Bearer wrong"}).status_code == 401


def test_mcp_http_initializes_and_calls_router():
    with TestClient(create_app(api_key="test-key"), base_url="http://127.0.0.1") as client:
        headers = {"Authorization": "Bearer test-key", "Accept": "application/json, text/event-stream"}
        response = client.post("/mcp/", headers=headers, json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "integration", "version": "1"}}})
        assert response.status_code == 200
        assert response.json()["result"]["serverInfo"]["name"] == "SolKraft"
        response = client.post("/mcp/", headers=headers, json={"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "route_request", "arguments": {"objective": "Do not deploy or delete anything.", "policy": {"contract_mode": "strict"}}}})
        assert response.status_code == 200
        import json
        result = json.loads(response.json()["result"]["content"][0]["text"])
        assert result["selected"] == []
        assert result["execution_authorized"] is False
        assert result["route_policy"]["contract_mode"] == "strict"
        assert client.post("/mcp/", json={}).status_code == 401



def test_api_separates_policy_from_semantic_context(tmp_path):
    folder = tmp_path / "mystery"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: mystery\ndescription: Inspect a mystery repository.\n---\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([tmp_path]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-key"}
    response = client.post(
        "/v1/route",
        headers=headers,
        json={
            "objective": "Inspect the mystery repository.",
            "skills": ["mystery"],
            "context": {"stage": "inspect"},
            "policy": {"contract_mode": "strict"},
        },
    )
    assert response.status_code == 200
    route = response.json()
    assert route["selection_status"] == "blocked"
    assert route["contract_decisions"]["mystery"]["status"] == "denied"
    assert route["route_policy"]["contract_mode"] == "strict"
    assert route["execution_authorized"] is False



def test_api_accepts_host_grant_and_available_inputs(tmp_path):
    folder = tmp_path / "consumer"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: consumer\ndescription: Analyze a supplied dataset.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
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
authority:
  capabilities:
    - repo.read
  resources:
    - repo:example/project
verification:
  mode: declarative
  checks:
    - id: analysis-present
      type: artifact_exists
""".strip() + "\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([tmp_path]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    response = client.post(
        "/v1/route",
        headers={"Authorization": "Bearer test-key"},
        json={
            "objective": "Analyze the supplied dataset.",
            "skills": ["consumer"],
            "context": {"available_inputs": ["dataset"]},
            "policy": {
                "contract_mode": "strict",
                "grant": {
                    "grant_id": "snapshot-api",
                    "capabilities": ["repo.*"],
                    "resources": ["repo:example/*"]
                }
            }
        },
    )
    assert response.status_code == 200
    route = response.json()
    assert route["selection_status"] == "matched"
    assert route["route_policy"]["grant"]["grant_id"] == "snapshot-api"
    assert route["required_capabilities"] == ["repo.read"]
    assert route["required_resources"] == ["repo:example/project"]
    assert route["dataflow"]["inputs"]["consumer:dataset"]["status"] == "available"
    assert route["execution_authorized"] is False



def test_contract_api_surface(tmp_path):
    folder = tmp_path / "demo"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Inspect a demo repository.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        """
schema_version: "1.0"
skill_id: demo
contract_revision: 1
inputs: []
outputs: []
effects: []
authority:
  capabilities:
    - repo.read
  resources:
    - repo:demo
verification:
  mode: declarative
  checks:
    - id: report
      type: field_present
      field: result
""".strip() + "\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([tmp_path]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-key"}

    contract = client.get("/v1/skills/demo/contract", headers=headers)
    assert contract.status_code == 200
    assert contract.json()["status"] == "declared"
    assert contract.json()["capabilities"] == ["repo.read"]

    schema = client.get("/v1/contract-schema", headers=headers)
    assert schema.status_code == 200
    assert schema.json()["title"] == "SolKraft Skill Contract v1"

    valid = client.post(
        "/v1/contracts/validate",
        headers=headers,
        json={"contract": {
            "schema_version": "1.0",
            "skill_id": "x",
            "contract_revision": 1,
        }},
    )
    assert valid.json()["valid"] is True

    filtered = client.get(
        "/v1/contracts?capability=repo.read",
        headers=headers,
    ).json()
    assert filtered["count"] == 1
    assert filtered["items"][0]["id"] == "demo"



def test_api_defaults_to_hardened_policy(tmp_path):
    folder = tmp_path / "opaque"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: opaque\ndescription: Inspect an opaque thing.\n---\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([tmp_path]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    route = client.post(
        "/v1/route",
        headers={"Authorization": "Bearer test-key"},
        json={"objective": "Inspect the opaque thing.", "skills": ["opaque"]},
    ).json()
    assert route["route_policy"]["contract_mode"] == "hardened"
    assert route["selection_status"] == "blocked"
    assert route["contract_decisions"]["opaque"]["status"] == "denied"


def test_portable_contract_api_roundtrip(tmp_path):
    folder = tmp_path / "demo"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Inspect a demo.\n---\n",
        encoding="utf-8",
    )
    (folder / "contract.yaml").write_text(
        """
schema_version: "1.0"
skill_id: demo
contract_revision: 1
inputs: []
outputs: []
effects: []
authority:
  capabilities:
    - repo.read
  resources: []
verification:
  mode: declarative
  checks:
    - id: report
      type: field_present
      field: result
""".strip() + "\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([tmp_path]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-key"}
    exported = client.get("/v1/skills/demo/contract/export", headers=headers)
    assert exported.status_code == 200
    assert exported.json()["execution_authorized"] is False
    imported = client.post(
        "/v1/contracts/import",
        headers=headers,
        json={"document": exported.json()},
    )
    assert imported.status_code == 200
    assert imported.json()["trust"]["trusted"] is False
    assert imported.json()["authority_granted"] is False


def test_opaque_contract_cannot_be_exported_as_safe(tmp_path):
    folder = tmp_path / "opaque"
    folder.mkdir()
    (folder / "SKILL.md").write_text(
        "---\nname: opaque\ndescription: Unknown effects.\n---\n",
        encoding="utf-8",
    )
    app = create_app(SkillCatalog([tmp_path]), api_key="test-key", require_api_key=True)
    client = TestClient(app)
    response = client.get(
        "/v1/skills/opaque/contract/export",
        headers={"Authorization": "Bearer test-key"},
    )
    assert response.status_code == 422
