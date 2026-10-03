"""Command-line entry point for SolKraft's REST API and MCP stdio server."""
from __future__ import annotations

import argparse
import os
import json

import uvicorn

from .api import _configured_roots, app, create_app
from .catalog import SkillCatalog
from .mcp_server import build_mcp_server
from .routing import route_request, get_graph, catalog_graph, BUNDLE_ROOT


def main() -> None:
    parser = argparse.ArgumentParser(prog="solkraft")
    parser.add_argument("mode", choices=("api", "mcp", "search", "route", "get", "resource", "graph"), nargs="?", default="api")
    parser.add_argument("value", nargs="?")
    parser.add_argument("resource_path", nargs="?")
    parser.add_argument("--max-skills", type=int, default=10)
    parser.add_argument("--skills", nargs="*", default=[])
    parser.add_argument("--context-stage")
    parser.add_argument("--installed", action="store_true", help="Include local installed skill roots")
    args = parser.parse_args()
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
            result = route_request(catalog, args.value, args.max_skills, explicit=args.skills,
                                   context={"stage": args.context_stage} if args.context_stage else None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if args.mode == "mcp":
        build_mcp_server(SkillCatalog(_configured_roots(args.installed), preferred_root=BUNDLE_ROOT)).run(transport="stdio")
        return
    host = os.getenv("SOLKRAFT_HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
    port = int(os.getenv("SOLKRAFT_PORT", os.getenv("PORT", "8765")))
    if args.installed and host not in {'127.0.0.1', 'localhost', '::1'}:
        parser.error('--installed API mode requires a localhost bind')
    application = create_app(SkillCatalog(_configured_roots(True), preferred_root=BUNDLE_ROOT)) if args.installed else app
    uvicorn.run(application, host=host, port=port, proxy_headers=False)


if __name__ == "__main__":
    main()
