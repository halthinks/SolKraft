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
        response = client.post("/mcp/", headers=headers, json={"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "route_request", "arguments": {"objective": "Do not deploy or delete anything."}}})
        assert response.status_code == 200
        import json
        result = json.loads(response.json()["result"]["content"][0]["text"])
        assert result["selected"] == []
        assert result["execution_authorized"] is False
        assert client.post("/mcp/", json={}).status_code == 401
