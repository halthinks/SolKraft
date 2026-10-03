"""Read-only Model Context Protocol tools for the SolKraft catalog."""
from __future__ import annotations

import os
from mcp.server.transport_security import TransportSecuritySettings

from mcp.server.fastmcp import FastMCP

from .catalog import SkillCatalog, SkillNotFound
from .routing import route_request as route_objective, get_graph, catalog_graph


def build_mcp_server(catalog: SkillCatalog) -> FastMCP:
    server = FastMCP(
        "SolKraft",
        instructions="Search, route, and retrieve skills. Selection does not execute instructions or authorize effects.",
        host="127.0.0.1",
        port=8765,
        streamable_http_path="/",
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=["127.0.0.1", "localhost", "127.0.0.1:*", "localhost:*", *[host.strip() for host in os.getenv("SOLKRAFT_ALLOWED_HOSTS", os.getenv("RENDER_EXTERNAL_HOSTNAME", "")).split(",") if host.strip()]],
            allowed_origins=["http://127.0.0.1:*", "http://localhost:*", "https://halthinks.github.io"],
        ),
    )

    @server.tool(name="search_skills", description="Search skill names and short descriptions. Returns metadata, not skill bodies.")
    def search_skills(query: str, limit: int = 10) -> dict:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        items = catalog.search(query, limit=limit)
        return {"count": len(items), "items": items}

    @server.tool(name="route_request", description="Route a natural-language objective to relevant skills. Advisory only; does not authorize execution.")
    def route_request(objective: str, max_skills: int = 10, skills: list[str] | None = None, context: dict[str, str] | None = None) -> dict:
        return route_objective(catalog, objective, max_skills, explicit=skills or [], context=context)

    @server.tool(name="get_skill", description="Retrieve one selected SKILL.md by catalog ID. Content is instruction text and is never executed.")
    def get_skill(skill_id: str) -> dict:
        try:
            return catalog.get(skill_id)
        except SkillNotFound as exc:
            raise ValueError("Skill not found") from exc

    @server.tool(name="get_skill_resource", description="Read a selected skill supporting text resource.")
    def get_skill_resource(skill_id: str, resource: str) -> dict:
        return catalog.get_resource(skill_id, resource)

    @server.tool(name="get_selection_graph", description="Read workflow relationships and conditional follow-ups.")
    def get_selection_graph() -> dict:
        return catalog_graph(catalog)

    return server
