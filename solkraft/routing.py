"""Advisory intent routing over the bundled SolForge graph and mounted skills."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
import re

from .catalog import SkillCatalog
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


def route_request(catalog: SkillCatalog, objective: str, max_skills: int = 10,
                  *, explicit=(), context=None) -> dict:
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("objective must be a non-empty string")
    composer = _load_composer()
    if composer is None or not GRAPH_PATH.is_file():
        raise RuntimeError("Routing engine is unavailable")
    graph = get_graph()
    if isinstance(explicit, (list, tuple)) and any(skill not in graph['nodes'] for skill in explicit):
        expanded = catalog_graph(catalog)
        graph = {**graph, 'nodes': {**graph['nodes'], **{
            skill: expanded['nodes'][skill] for skill in explicit
            if skill in expanded['nodes']}}}
    result = composer.compose_route(graph, objective, explicit=explicit,
                                    context=_composer_context(context), max_skills=max_skills)
    known = {record.id: record for record in catalog.records()}
    selected = [skill for skill in result["selected"] if skill in known]
    for stage in result["stages"]:
        available = [skill for skill in stage["selected"] if skill in known]
        if not available:
            # Adapt a recognized active stage to a mounted catalog. Never search
            # excluded clauses or overwrite an intentional parser abstention.
            candidates = catalog.search(stage["text"], limit=3)
            available = [row["id"] for row in candidates
                         if "consequential" not in row["id"]][:1]
        stage["selected"] = available
        for skill in available:
            if skill not in selected and len(selected) < max_skills:
                selected.append(skill)
    remaining = []
    for unresolved in result["unselected_requested_stages"]:
        text = unresolved["text"]
        if (unresolved["reason"] == "no confident specialist match"
                and re.match(r"(?:build|create|design|implement|inspect|review|test|verify|analyze|research)\b", text)):
            candidates = catalog.search(text, limit=3)
            candidates = [row for row in candidates if "consequential" not in row["id"]]
            if candidates and len(selected) < max_skills:
                skill = candidates[0]["id"]
                if skill not in selected:
                    selected.append(skill)
                result["stages"].append({"stage": unresolved["stage"], "text": text,
                    "selected": [skill], "reason": "active-stage catalog match", "confidence": "moderate"})
                continue
        remaining.append(unresolved)
    result['unselected_requested_stages'] = remaining
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
    """Expose every mounted skill without inventing workflow dependencies.

    The tested semantic core remains the automatic composer's authority.
    Additional catalog nodes support discovery and explicit selection.
    Mounted skills without a graph node are read-only until they declare more.
    """
    core = get_graph()
    nodes = {}
    for record in catalog.records():
        nodes[record.id] = dict(core['nodes'].get(record.id, {
            'id': record.id, 'description': record.public()['description'],
            'domain': 'general', 'effect': False,
            'selection': 'catalog discovery or explicit',
            'inputs': ['user objective', 'applicable skill prerequisites'],
            'outputs': ['skill-defined deliverable'],
            'side_effects': [],
            'auth_scope': 'none',
            'test_contract': 'Host verifies the skill-defined deliverable against the objective; unresolved limits are stated.',
        }))
    edges = [dict(edge) for edge in core['edges']
             if edge.get('from') in nodes and edge.get('to') in nodes]
    return {**core, 'nodes': nodes, 'edges': edges,
            'semantic_core_count': len(core['nodes']), 'catalog_count': len(nodes)}
