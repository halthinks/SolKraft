"""Translate external tool metadata into SolKraft declarations.

Adapters are intentionally conservative. They never create host grants or
trusted status, and uncertain effects remain unknown instead of being assumed
safe.
"""
from __future__ import annotations

from .effects import normalize_effects


def _bindings_from_json_schema(schema: object, *, source: str) -> list[dict]:
    if not isinstance(schema, dict):
        return []
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return []
    required = set(schema.get("required") or [])
    result = []
    for name, value in properties.items():
        result.append({
            "name": str(name),
            "required": name in required,
            "source": source,
            "schema": dict(value) if isinstance(value, dict) else {},
        })
    return result


def from_mcp_tool(tool: dict, *, skill_id: str | None = None) -> dict:
    if not isinstance(tool, dict):
        raise ValueError("MCP tool metadata must be an object")
    name = skill_id or tool.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("MCP tool requires a name")

    annotations = tool.get("annotations") or {}
    read_only = annotations.get("readOnlyHint") is True
    destructive = annotations.get("destructiveHint") is True
    open_world = annotations.get("openWorldHint") is True

    effects = [] if read_only else None
    status = "declared" if read_only else "opaque"
    return {
        "id": name,
        "contract_status": status,
        "schema_version": "1.0" if read_only else None,
        "contract_revision": 1 if read_only else None,
        "inputs": _bindings_from_json_schema(
            tool.get("inputSchema") or tool.get("input_schema"),
            source="user",
        ),
        "outputs": [],
        "side_effects": effects,
        "authority": {"capabilities": [], "resources": []},
        "risk": {
            "external": open_world,
            "destructive": destructive,
            "open_world": open_world,
        },
        "verification": {},
        "provenance": {
            "adapter": "mcp",
            "external_declaration": True,
        },
        "trust": {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "MCP annotations are declarations only",
        },
        "execution_authorized": False,
    }


def from_openapi_operation(
    operation: dict,
    *,
    method: str,
    path: str,
    skill_id: str | None = None,
) -> dict:
    if not isinstance(operation, dict):
        raise ValueError("OpenAPI operation must be an object")
    method_name = method.casefold()
    name = skill_id or operation.get("operationId") or f"{method_name}:{path}"
    parameters = {}
    required = []
    for parameter in operation.get("parameters") or []:
        if not isinstance(parameter, dict):
            continue
        pname = parameter.get("name")
        if not isinstance(pname, str):
            continue
        parameters[pname] = dict(parameter.get("schema") or {})
        if parameter.get("required") is True:
            required.append(pname)

    request_schema = {
        "type": "object",
        "properties": parameters,
        "required": required,
    }
    safe_method = method_name in {"get", "head", "options"}
    effects = [] if safe_method else None
    return {
        "id": name,
        "contract_status": "declared" if safe_method else "opaque",
        "schema_version": "1.0" if safe_method else None,
        "contract_revision": 1 if safe_method else None,
        "inputs": _bindings_from_json_schema(request_schema, source="user"),
        "outputs": [],
        "side_effects": effects,
        "authority": {"capabilities": [], "resources": []},
        "risk": {
            "external": True,
            "destructive": method_name == "delete",
            "open_world": True,
        },
        "verification": {},
        "provenance": {
            "adapter": "openapi",
            "method": method_name.upper(),
            "path": path,
            "external_declaration": True,
        },
        "trust": {
            "state": "local-unreviewed",
            "trusted": False,
            "reason": "OpenAPI metadata is a declaration only",
        },
        "execution_authorized": False,
    }


def external_effects(node: dict) -> list[str] | None:
    value = node.get("side_effects")
    return normalize_effects(value) if value is not None else None
