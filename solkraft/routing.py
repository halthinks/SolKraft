"""Advisory intent routing over the bundled SolForge graph and mounted skills."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
import re

from .catalog import SkillCatalog
from .contract_loader import load_skill_contract
from .contracts import apply_contracts


BUNDLE_ROOT = Path(__file__).resolve().parent / "skillpacks"
GRAPH_PATH = BUNDLE_ROOT / "solforge" / "references" / "selection-graph.json"


def _load_composer():
    try:
        from .skillpacks.solforge.scripts import compose_route
        return compose_route
    except (ImportError, ModuleNotFoundError):
        return None


def _composer_context(context):
    """Keep composer context limited to fields it already validates."""
    if not isinstance(context, dict):
        return context
    allowed = {key: context[key] for key in ("domain", "stage") if key in context}
    return allowed or None


def _enrich_core_with_contracts(core: dict, expanded: dict) -> dict:
    nodes = {}
    for skill, node in core["nodes"].items():
        nodes[skill] = dict(expanded.get("nodes", {}).get(skill, node))
    return {**core, "nodes": nodes}


def route_request(catalog: SkillCatalog, objective: str, max_skills: int = 10,
                  *, explicit=(), context=None) -> dict:
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("objective must be a non-empty string")
    composer = _load_composer()
    if composer is None or not GRAPH_PATH.is_file():
        raise RuntimeError("Routing engine is unavailable")

    expanded = catalog_graph(catalog)
    graph = _enrich_core_with_contracts(get_graph(), expanded)
    if isinstance(explicit, (list, tuple)) and any(skill not in graph["nodes"] for skill in explicit):
        graph = {**graph, "nodes": {**graph["nodes"], **{
            skill: expanded["nodes"][skill] for skill in explicit
            if skill in expanded["nodes"]
        }}}

    result = composer.compose_route(
        graph,
        objective,
        explicit=explicit,
        context=_composer_context(context),
        max_skills=max_skills,
    )
    known = {record.id: record for record in catalog.records()}
    selected = [skill for skill in result["selected"] if skill in known]

    for stage in result["stages"]:
        available = [skill for skill in stage["selected"] if skill in known]
        if not available:
            candidates = catalog.search(stage["text"], limit=3)
            available = [row["id"] for row in candidates
                         if "consequential" not in row["id"]][:1]
        stage["selected"] = available
        for skill in available:
            if skill not in selected and len(selected) < max_skills:
                selected.append(skill)

    remaining = []
    for unresolved in result["unselected_requested_stages"]:
        stage_text = unresolved["text"]
        if (
            unresolved["reason"] == "no confident specialist match"
            and re.match(
                r"(?:build|create|design|implement|inspect|review|test|verify|analyze|research)\b",
                stage_text,
            )
        ):
            candidates = catalog.search(stage_text, limit=3)
            candidates = [row for row in candidates if "consequential" not in row["id"]]
            if candidates and len(selected) < max_skills:
                skill = candidates[0]["id"]
                if skill not in selected:
                    selected.append(skill)
                result["stages"].append({
                    "stage": unresolved["stage"],
                    "text": stage_text,
                    "selected": [skill],
                    "reason": "active-stage catalog match",
                    "confidence": "moderate",
                })
                continue
        remaining.append(unresolved)

    for skill in selected:
        if skill not in graph["nodes"] and skill in expanded["nodes"]:
            graph["nodes"][skill] = expanded["nodes"][skill]

    result["unselected_requested_stages"] = remaining
    result["stages"].sort(key=lambda stage: stage["stage"])
    result["selected"] = selected
    result["skills"] = [known[skill].public() for skill in selected]
    allowed_auth = context.get("auth_scope") if isinstance(context, dict) else None
    result = apply_contracts(result, graph, objective, allowed_auth=allowed_auth)
    result["skills"] = [known[skill].public() for skill in result["selected"] if skill in known]
    result["execution_authorized"] = False
    return result


@lru_cache(maxsize=1)
def get_graph() -> dict:
    """Return portable selection relationships, never host filesystem paths."""
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def catalog_graph(catalog: SkillCatalog) -> dict:
    """Expose mounted skills without inventing safety or workflow claims."""
    core = get_graph()
    nodes = {}
    for record in catalog.records():
        legacy_node = core["nodes"].get(record.id)
        base = dict(legacy_node or {
            "id": record.id,
            "description": record.public()["description"],
            "domain": "general",
            "effect": None,
            "selection": "catalog discovery or explicit",
            "inputs": ["user objective", "applicable skill prerequisites"],
            "outputs": ["skill-defined deliverable"],
        })
        contract = load_skill_contract(
            record.entrypoint,
            legacy_node=legacy_node,
            expected_skill_id=record.name,
        )
        base["contract_status"] = contract["status"]
        base["contract_source"] = contract.get("source")
        base["contract_validation_errors"] = contract.get("validation_errors", [])
        base["side_effects"] = contract["side_effects"]
        base["auth_scope"] = contract["auth_scope"]
        base["test_contract"] = contract["test_contract"]
        if contract.get("schema_version") is not None:
            base["schema_version"] = contract["schema_version"]
        if contract.get("contract_revision") is not None:
            base["contract_revision"] = contract["contract_revision"]
        if contract.get("capabilities"):
            base["authority"] = {
                "capabilities": contract["capabilities"],
                "resources": contract.get("resources", []),
                "legacy_scope": contract.get("auth_scope"),
            }
        nodes[record.id] = base

    edges = [
        dict(edge) for edge in core["edges"]
        if edge.get("from") in nodes and edge.get("to") in nodes
    ]
    return {
        **core,
        "nodes": nodes,
        "edges": edges,
        "semantic_core_count": len(core["nodes"]),
        "catalog_count": len(nodes),
    }
