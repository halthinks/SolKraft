import pytest

from solkraft.adapters import from_mcp_tool, from_openapi_operation
from solkraft.contracts import contract_from_node
from solkraft.interchange import export_portable_contract, import_portable_contract


def test_mcp_read_only_annotation_maps_to_untrusted_declaration():
    node = from_mcp_tool({
        "name": "inspect",
        "description": "Inspect metadata",
        "inputSchema": {
            "type": "object",
            "properties": {"repository": {"type": "string"}},
            "required": ["repository"],
        },
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "openWorldHint": False,
        },
    })
    contract = contract_from_node(node)
    assert contract["status"] == "declared"
    assert contract["side_effects"] == []
    assert node["trust"]["trusted"] is False
    assert node["execution_authorized"] is False


def test_mcp_unknown_effect_tool_stays_opaque():
    node = from_mcp_tool({"name": "do-something", "inputSchema": {"type": "object"}})
    contract = contract_from_node(node)
    assert contract["status"] == "opaque"
    assert contract["side_effects"] is None


def test_openapi_get_is_declaration_only_and_post_is_opaque():
    get_node = from_openapi_operation(
        {"operationId": "readWidget", "parameters": []},
        method="GET",
        path="/widgets/{id}",
    )
    post_node = from_openapi_operation(
        {"operationId": "createWidget", "parameters": []},
        method="POST",
        path="/widgets",
    )
    assert contract_from_node(get_node)["side_effects"] == []
    assert get_node["trust"]["trusted"] is False
    assert contract_from_node(post_node)["status"] == "opaque"
    assert contract_from_node(post_node)["side_effects"] is None


def test_portable_roundtrip_preserves_declaration_without_authority():
    entry = {
        "id": "demo",
        "status": "declared",
        "schema_version": "1.0",
        "contract_revision": 1,
        "inputs": [],
        "outputs": [],
        "effects": [],
        "capabilities": ["repo.read"],
        "resources": ["repo:demo"],
        "risk": {},
        "verification": {
            "mode": "declarative",
            "checks": [{"id": "result", "type": "field_present", "field": "result"}],
        },
        "provenance": {},
        "trust": {"state": "bundled-reviewed"},
    }
    portable = export_portable_contract(entry)
    imported = import_portable_contract(portable)
    assert imported["contract"]["authority"]["capabilities"] == ["repo.read"]
    assert imported["trust"]["state"] == "local-unreviewed"
    assert imported["authority_granted"] is False
    assert imported["execution_authorized"] is False


def test_opaque_export_fails_closed():
    with pytest.raises(ValueError):
        export_portable_contract({
            "id": "opaque",
            "effects": None,
            "status": "opaque",
        })
