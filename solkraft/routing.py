"""Advisory intent routing over the bundled SolForge graph and mounted skills."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
import re

from .catalog import SkillCatalog
from .contract_loader import load_skill_contract
from .contract_policy import RoutePolicy, evaluate_graph
from .route_validation import validate_route


BUNDLE_ROOT = Path(__file__).resolve().parent / "skillpacks"
GRAPH_PATH = BUNDLE_ROOT / "solforge" / "references" / "selection-graph.json"
_ACTIVE_STAGE_RE = re.compile(
    r"(?:build|create|design|implement|inspect|review|test|verify|analyze|research|"
    r"diagnose|investigate|debug|draft|write|compare|validate|audit)\b"
)


def _load_composer():
    try:
        from .skillpacks.solforge.scripts import compose_route
        return compose_route
    except (ImportError, ModuleNotFoundError):
        return None


def _composer_context(context):
    """Only semantic context reaches the semantic composer."""
    if not isinstance(context, dict):
        return context
    allowed = {key: context[key] for key in ("domain", "stage") if key in context}
    return allowed or None


def _effective_policy(policy, context):
    """Preserve legacy context auth ceilings while keeping policy separate."""
    if not isinstance(context, dict) or "auth_scope" not in context:
        return policy
    legacy = context.get("auth_scope")
    if isinstance(policy, RoutePolicy):
        if policy.legacy_auth_scope is not None:
            return policy
        return {
            **policy.public(),
            "legacy_auth_scope": legacy,
        }
    value = dict(policy or {})
    value.setdefault("legacy_auth_scope", legacy)
    return value


def _enrich_core_with_contracts(core: dict, expanded: dict) -> dict:
    nodes = {}
    for skill, node in core["nodes"].items():
        nodes[skill] = dict(expanded.get("nodes", {}).get(skill, node))
    return {**core, "nodes": nodes}


def _decision_allows(decisions: dict, skill: str) -> bool:
    return decisions.get(skill, {}).get("status") != "denied"


def _repair_candidate(catalog, decisions, text, selected):
    for row in catalog.search(text, limit=6):
        skill = row["id"]
        if "consequential" in skill or skill in selected:
            continue
        if _decision_allows(decisions, skill):
            return skill
    return None


def route_request(
    catalog: SkillCatalog,
    objective: str,
    max_skills: int = 10,
    *,
    explicit=(),
    context=None,
    policy=None,
) -> dict:
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("objective must be a non-empty string")
    composer = _load_composer()
    if composer is None or not GRAPH_PATH.is_file():
        raise RuntimeError("Routing engine is unavailable")

    expanded = catalog_graph(catalog)
    effective_policy = _effective_policy(policy, context)
    normalized_policy, decisions = evaluate_graph(expanded, objective, effective_policy)

    graph = _enrich_core_with_contracts(get_graph(), expanded)
    if isinstance(explicit, (list, tuple)) and any(skill not in graph["nodes"] for skill in explicit):
        graph = {**graph, "nodes": {**graph["nodes"], **{
            skill: expanded["nodes"][skill] for skill in explicit
            if skill in expanded["nodes"]
        }}}

    blocked_skills = {
        skill for skill in graph["nodes"]
        if decisions.get(skill, {}).get("status") == "denied"
    }
    result = composer.compose_route(
        graph,
        objective,
        explicit=explicit,
        context=_composer_context(context),
        max_skills=max_skills,
        blocked_skills=blocked_skills,
    )

    known = {record.id: record for record in catalog.records()}
    selected = [skill for skill in result["selected"] if skill in known]

    # Adapt selected semantic stages to the mounted catalog without selecting a
    # contract-denied replacement.
    for stage in result["stages"]:
        available = [
            skill for skill in stage["selected"]
            if skill in known and _decision_allows(decisions, skill)
        ]
        if not available:
            candidate = _repair_candidate(catalog, decisions, stage["text"], selected)
            available = [candidate] if candidate else []
        stage["selected"] = available
        for skill in available:
            if skill not in selected and len(selected) < max_skills:
                selected.append(skill)

    # One bounded repair pass for unresolved active stages, including a mapped
    # candidate that prefiltering rejected. We do not recursively recompose.
    remaining = []
    repaired = []
    repairable_reasons = {
        "no confident specialist match",
        "candidate inadmissible by contract policy",
    }
    for unresolved in result["unselected_requested_stages"]:
        stage_text = unresolved["text"]
        stage_number = unresolved.get("stage")
        if (
            stage_number is not None
            and unresolved["reason"] in repairable_reasons
            and _ACTIVE_STAGE_RE.match(stage_text)
            and len(selected) < max_skills
        ):
            skill = _repair_candidate(catalog, decisions, stage_text, selected)
            if skill:
                selected.append(skill)
                result["stages"].append({
                    "stage": stage_number,
                    "text": stage_text,
                    "selected": [skill],
                    "reason": "contract-safe catalog repair",
                    "confidence": "moderate",
                })
                repaired.append({
                    "stage": stage_number,
                    "rejected": unresolved.get("candidate"),
                    "replacement": skill,
                })
                continue
        remaining.append(unresolved)

    for skill in selected:
        if skill not in graph["nodes"] and skill in expanded["nodes"]:
            graph["nodes"][skill] = expanded["nodes"][skill]

    result["unselected_requested_stages"] = remaining
    result["stages"].sort(key=lambda stage: (stage.get("stage") is None, stage.get("stage") or 0))
    result["selected"] = selected
    result.setdefault("selection_trace", {})["contract_repair"] = {
        "attempted": any(
            row.get("reason") in repairable_reasons
            for row in [*remaining, *result.get("unselected_requested_stages", [])]
        ) or bool(repaired),
        "repaired": repaired,
        "bounded_passes": 1,
    }

    original_selected = list(selected)
    result = validate_route(
        result,
        graph,
        decisions,
        policy_public=normalized_policy.public(),
        original_selected=original_selected,
    )
    result["skills"] = [
        known[skill].public() for skill in result["selected"]
        if skill in known
    ]
    result["excluded_effects"] = list(normalized_policy.denied_effects)
    result["execution_authorized"] = False
    return result


@lru_cache(maxsize=1)
def get_graph() -> dict:
    """Return portable selection relationships, never host filesystem paths."""
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def catalog_graph(catalog: SkillCatalog) -> dict:
    """Expose mounted skills with compact contract metadata, never authority."""
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
        base["effects"] = contract["side_effects"]
        base["auth_scope"] = contract["auth_scope"]
        base["test_contract"] = contract["test_contract"]
        base["contract_digest"] = contract.get("contract_digest")
        base["entrypoint_digest"] = contract.get("entrypoint_digest")
        base["verification"] = contract.get("verification", {})
        base["risk"] = contract.get("risk", {})
        if contract.get("source") == "sidecar":
            base["inputs"] = contract.get("inputs", [])
            base["outputs"] = contract.get("outputs", [])
        if contract.get("schema_version") is not None:
            base["schema_version"] = contract["schema_version"]
        if contract.get("contract_revision") is not None:
            base["contract_revision"] = contract["contract_revision"]
        if (
            contract.get("capabilities")
            or contract.get("resources")
            or contract.get("auth_scope") is not None
        ):
            base["authority"] = {
                "capabilities": contract.get("capabilities", []),
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
