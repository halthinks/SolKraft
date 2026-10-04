"""Command-line entry point for SolKraft."""
from __future__ import annotations

import argparse
import json
import os

import uvicorn

from .api import _configured_roots, app, create_app
from .catalog import SkillCatalog
from .contract_cli import (
    init_contract,
    migrate_contracts,
    schema_document,
    validate_contract_path,
)
from .mcp_server import build_mcp_server
from .routing import BUNDLE_ROOT, catalog_graph, contract_index, route_request


def _route_policy(args) -> dict | None:
    mode = "strict" if args.strict_contracts else "warn" if args.warn_contracts else "legacy"
    grant = None
    if args.grant_capability or args.grant_resource or args.grant_id or args.grant_identity or args.grant_expires_at:
        grant = {
            "capabilities": args.grant_capability,
            "resources": args.grant_resource,
        }
        if args.grant_id:
            grant["grant_id"] = args.grant_id
        if args.grant_identity:
            grant["identity"] = args.grant_identity
        if args.grant_expires_at:
            grant["expires_at"] = args.grant_expires_at
    if not (args.deny_effect or grant or mode != "legacy" or args.legacy_auth_scope):
        return None
    return {
        "denied_effects": args.deny_effect,
        "grant": grant,
        "contract_mode": mode,
        "legacy_auth_scope": args.legacy_auth_scope,
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="solkraft")
    parser.add_argument(
        "mode",
        choices=("api", "mcp", "search", "route", "get", "resource", "graph", "contract"),
        nargs="?",
        default="api",
    )
    parser.add_argument("value", nargs="?")
    parser.add_argument("resource_path", nargs="?")
    parser.add_argument("--max-skills", type=int, default=10)
    parser.add_argument("--skills", nargs="*", default=[])
    parser.add_argument("--context-stage")
    parser.add_argument("--available-input", action="append", default=[])
    parser.add_argument("--deny-effect", action="append", default=[])
    parser.add_argument("--grant-capability", action="append", default=[])
    parser.add_argument("--grant-resource", action="append", default=[])
    parser.add_argument("--grant-id")
    parser.add_argument("--grant-identity")
    parser.add_argument("--grant-expires-at")
    parser.add_argument("--legacy-auth-scope")
    parser.add_argument("--strict-contracts", action="store_true")
    parser.add_argument("--warn-contracts", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--report")
    parser.add_argument("--installed", action="store_true", help="Include local installed skill roots")
    args = parser.parse_args()

    if args.strict_contracts and args.warn_contracts:
        parser.error("--strict-contracts and --warn-contracts are mutually exclusive")

    if args.mode == "contract":
        action = args.value or "schema"
        if action == "init":
            if not args.resource_path:
                parser.error("contract init requires a skill directory, SKILL.md, or contract.yaml path")
            result = init_contract(args.resource_path)
        elif action in {"validate", "lint"}:
            if not args.resource_path:
                parser.error(f"contract {action} requires a contract path")
            result = validate_contract_path(args.resource_path, lint=action == "lint")
        elif action == "schema":
            result = schema_document()
        elif action == "migrate":
            result = migrate_contracts(write=args.write, report=args.report)
        elif action == "show":
            if not args.resource_path:
                parser.error("contract show requires a skill ID")
            catalog = SkillCatalog(_configured_roots(args.installed), preferred_root=BUNDLE_ROOT)
            try:
                result = contract_index(catalog).get(args.resource_path)
            except KeyError as exc:
                parser.error(f"unknown skill: {args.resource_path}")
        else:
            parser.error("contract action must be init, validate, lint, show, schema, or migrate")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.mode not in {"api", "mcp"}:
        catalog = SkillCatalog(_configured_roots(args.installed), preferred_root=BUNDLE_ROOT)
        if args.mode == "graph":
            result = catalog_graph(catalog)
        elif args.mode == "search":
            result = catalog.search(args.value or "")
        elif args.mode == "get":
            result = catalog.get(args.value)
        elif args.mode == "resource":
            result = catalog.get_resource(args.value, args.resource_path)
        else:
            context = {}
            if args.context_stage:
                context["stage"] = args.context_stage
            if args.available_input:
                context["available_inputs"] = args.available_input
            result = route_request(
                catalog,
                args.value,
                args.max_skills,
                explicit=args.skills,
                context=context or None,
                policy=_route_policy(args),
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.mode == "mcp":
        build_mcp_server(
            SkillCatalog(_configured_roots(args.installed), preferred_root=BUNDLE_ROOT)
        ).run(transport="stdio")
        return

    host = os.getenv("SOLKRAFT_HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
    port = int(os.getenv("SOLKRAFT_PORT", os.getenv("PORT", "8765")))
    if args.installed and host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("--installed API mode requires a localhost bind")
    application = (
        create_app(SkillCatalog(_configured_roots(True), preferred_root=BUNDLE_ROOT))
        if args.installed else app
    )
    uvicorn.run(application, host=host, port=port, proxy_headers=False)


if __name__ == "__main__":
    main()
