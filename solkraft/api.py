"""REST API and Streamable HTTP MCP mount."""
from __future__ import annotations

import os
from pathlib import Path
import secrets

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .catalog import SkillCatalog, SkillNotFound
from .mcp_server import build_mcp_server
from .contract_schema import load_contract_schema, validate_v1_document
from .interchange import export_portable_contract, import_portable_contract
from .routing import BUNDLE_ROOT, route_request, get_graph, catalog_graph, contract_index


def _configured_roots(include_installed: bool = False) -> list[Path]:
    roots = [BUNDLE_ROOT]
    value = os.getenv("SOLKRAFT_SKILL_ROOTS", "")
    roots.extend(Path(item.strip()) for item in value.split(os.pathsep) if item.strip())
    if include_installed:
        home = Path.home()
        roots.extend([home / '.codex/skills', home / '.agents/skills', home / '.codex/plugins/cache'])
    return roots


class RoutePolicyBody(BaseModel):
    denied_effects: list[str] = Field(default_factory=list, max_length=100)
    granted_capabilities: list[str] | None = None
    granted_resources: list[str] | None = None
    grant: dict | None = None
    legacy_auth_scope: str | None = None
    contract_mode: str = "hardened"


class ContractValidationBody(BaseModel):
    contract: dict


class PortableContractBody(BaseModel):
    document: dict


class RouteBody(BaseModel):
    objective: str = Field(min_length=1, max_length=20_000)
    max_skills: int = Field(default=10, ge=1, le=50)
    skills: list[str] = Field(default_factory=list, max_length=50)
    context: dict[str, object] | None = None
    policy: RoutePolicyBody | None = None


def _policy_payload(policy: RoutePolicyBody | None):
    if policy is None:
        return {"contract_mode": "hardened"}
    if hasattr(policy, "model_dump"):
        return policy.model_dump(exclude_none=True)
    return policy.dict(exclude_none=True)


def create_app(catalog: SkillCatalog | None = None, *, api_key: str | None = None, require_api_key: bool = True) -> FastAPI:
    catalog = catalog or SkillCatalog(_configured_roots())
    api_key = api_key if api_key is not None else os.getenv("SOLKRAFT_API_KEY")
    from contextlib import asynccontextmanager
    mcp = build_mcp_server(catalog)

    @asynccontextmanager
    async def lifespan(app):
        async with mcp.session_manager.run():
            yield

    app = FastAPI(lifespan=lifespan, title="SolKraft API", version="0.1.0", description="Read-only skill catalog and router.")
    origins = [item.strip() for item in os.getenv("SOLKRAFT_CORS_ORIGINS", "https://halthinks.github.io").split(",") if item.strip()]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Authorization", "Content-Type"], max_age=600)

    @app.middleware("http")
    async def protect_api(request: Request, call_next):
        protected = request.url.path.startswith("/v1/") or request.url.path == "/mcp" or request.url.path.startswith("/mcp/")
        if protected and request.method != "OPTIONS" and require_api_key:
            authorization = request.headers.get("authorization", "")
            supplied = authorization[7:] if authorization.startswith("Bearer ") else ""
            if not api_key or not secrets.compare_digest(supplied, api_key):
                return JSONResponse(status_code=401, content={"detail": "A valid bearer API key is required."}, headers={"WWW-Authenticate": "Bearer"})
        return await call_next(request)

    @app.get("/healthz")
    async def health():
        return {"status": "ok", "service": "solkraft"}

    @app.get("/v1/graph")
    async def graph():
        return catalog_graph(catalog)

    @app.get("/v1/skills")
    async def list_skills(q: str = Query(default="", max_length=500), limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0)):
        available = catalog.search(q, limit=len(catalog.records())) if q else catalog.list(limit=len(catalog.records()))
        items = available[offset:offset + limit]
        return {"count": len(items), "total": len(available), "items": items}

    @app.get("/v1/skills/{skill_id}")
    async def get_skill(skill_id: str):
        try:
            return catalog.get(skill_id)
        except SkillNotFound as exc:
            raise HTTPException(status_code=404, detail="Skill not found") from exc

    @app.get("/v1/skills/{skill_id}/contract")
    async def get_skill_contract(skill_id: str):
        try:
            return contract_index(catalog).get(skill_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Skill contract not found") from exc

    @app.get("/v1/contract-schema")
    async def get_contract_schema():
        return load_contract_schema()

    @app.post("/v1/contracts/validate")
    async def validate_contract(body: ContractValidationBody):
        errors = validate_v1_document(body.contract)
        return {"valid": not errors, "errors": errors}

    @app.get("/v1/skills/{skill_id}/contract/export")
    async def export_contract(skill_id: str):
        try:
            return export_portable_contract(contract_index(catalog).get(skill_id))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Skill contract not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/v1/contracts/import")
    async def import_contract(body: PortableContractBody):
        try:
            return import_portable_contract(body.document)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/v1/contracts")
    async def list_contracts(
        effect: str | None = None,
        capability: str | None = None,
        input_name: str | None = None,
        output_name: str | None = None,
        trust: str | None = None,
    ):
        index = contract_index(catalog)
        items = index.filter(
            effect=effect,
            capability=capability,
            input_name=input_name,
            output_name=output_name,
            trust=trust,
        )
        return {"count": len(items), "generation": index.generation, "items": items}

    @app.post("/v1/route")
    async def route(body: RouteBody):
        try:
            return route_request(
                catalog,
                body.objective,
                body.max_skills,
                explicit=body.skills,
                context=body.context,
                policy=_policy_payload(body.policy),
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/v1/skills/{skill_id}/resources/{resource:path}")
    async def get_resource(skill_id: str, resource: str):
        try:
            return catalog.get_resource(skill_id, resource)
        except SkillNotFound as exc:
            raise HTTPException(status_code=404, detail="Resource not found") from exc

    @app.post("/v1/refresh")
    async def refresh():
        count = catalog.refresh()
        index = contract_index(catalog)
        return {
            "count": count,
            "status": "refreshed",
            "contract_index": {
                "generation": index.generation,
                **index.last_refresh,
            },
        }

    app.mount("/mcp", mcp.streamable_http_app())
    app.state.skill_catalog = catalog
    app.state.mcp_server = mcp
    return app


app = create_app()
