"""Advisory intent routing over the bundled SolForge graph and mounted skills."""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
import re

from .catalog import SkillCatalog
from .contract_policy import RoutePolicy, evaluate_graph
from .dataflow import resolve_required_inputs
from .route_validation import validate_route
from .audit import route_audit_event


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
    denied_candidate = None
    for row in catalog.search(text, limit=6):
        skill = row["id"]
        if "consequential" in skill or skill in selected:
            continue
        if _decision_allows(decisions, skill):
            return skill, denied_candidate
        if denied_candidate is None:
            denied_candidate = skill
    return None, denied_candidate


def _identity_candidate(catalog, graph, decisions, text):
    """Resolve one high-confidence semantic capability identity.

    Prefer the strict identity matcher, then fall back to query-centric ranked
    evidence for natural paraphrases that contain several distinctive capability
    anchors without copying a published description.
    """
    match = catalog.identity_match(text)
    if not match:
        ranked = catalog.identity_rank(text, limit=3)
        if ranked:
            best = ranked[0]
            second_score = ranked[1]["score"] if len(ranked) > 1 else 0.0
            margin = best["score"] - second_score
            matched = best.get("matched_tokens") or []
            if (
                (len(matched) >= 3 and best["score"] >= 0.16 and margin >= 0.015)
                or (len(matched) >= 2 and best["score"] >= 0.24 and margin >= 0.035)
            ):
                match = {
                    "id": best["id"],
                    "score": best["score"],
                    "margin": round(margin, 6),
                    "reason": "query-centric capability identity",
                    "matched_tokens": matched,
                }
    if not match:
        return None, None
    skill = match["id"]
    node = graph.get("nodes", {}).get(skill, {})
    if node.get("effect") is True:
        return None, {**match, "blocked": "consequential effect node"}
    if not _decision_allows(decisions, skill):
        return None, {**match, "blocked": "contract policy"}
    return skill, match


def _enforce_dataflow_order(selected, additions):
    """Keep every typed producer before the consumer it satisfies."""
    ordered = list(selected)
    for addition in additions or ():
        producer = addition.get("producer")
        consumer = addition.get("consumer")
        if producer not in ordered or consumer not in ordered:
            continue
        producer_index = ordered.index(producer)
        consumer_index = ordered.index(consumer)
        if producer_index > consumer_index:
            ordered.pop(producer_index)
            consumer_index = ordered.index(consumer)
            ordered.insert(consumer_index, producer)
    return ordered


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

    compound_identity_trace = []
    compound_identity_skills = []
    for match in catalog.identity_matches(objective, limit=max_skills):
        skill = match["id"]
        node = expanded.get("nodes", {}).get(skill, {})
        if node.get("effect") is True:
            compound_identity_trace.append({**match, "blocked": "consequential effect node"})
            continue
        if not _decision_allows(decisions, skill):
            compound_identity_trace.append({**match, "blocked": "contract policy"})
            continue
        compound_identity_trace.append(match)
        if skill not in compound_identity_skills:
            compound_identity_skills.append(skill)

    if compound_identity_skills:
        selected = [
            *compound_identity_skills,
            *[skill for skill in selected if skill not in compound_identity_skills],
        ][:max_skills]
        result.setdefault("selection_trace", {})["compound_capability_identity"] = compound_identity_trace

    # Augment the rule-based composer with query-centric capability evidence for
    # each requested clause. This is deliberately additive: existing workflow
    # matches remain visible, while a strongly supported catalog specialist can
    # no longer be displaced merely because the request used unfamiliar wording.
    semantic_trace = []
    try:
        semantic_clauses, _ = composer.segment(objective)
    except (AttributeError, TypeError, ValueError):
        semantic_clauses = [objective]

    for stage_index, clause in enumerate(semantic_clauses, 1):
        ranked = catalog.identity_rank(clause, limit=8)
        admissible = []
        for row in ranked:
            skill = row["id"]
            node = expanded.get("nodes", {}).get(skill, {})
            if node.get("effect") is True or not _decision_allows(decisions, skill):
                continue
            admissible.append(row)

        if not admissible:
            continue

        best = admissible[0]
        second_score = admissible[1]["score"] if len(admissible) > 1 else 0.0
        margin = best["score"] - second_score
        matched = best.get("matched_tokens") or []
        strong = (
            len(matched) >= 2
            and (
                best["score"] >= 0.16
                or best.get("query_precision", 0.0) >= 0.28
            )
            and (
                margin >= 0.015
                or len(matched) >= 3
                or best.get("name_score", 0.0) >= 0.5
            )
        )
        semantic_trace.append({
            "stage": stage_index,
            "text": clause,
            "candidate": best["id"],
            "score": best["score"],
            "margin": round(margin, 6),
            "matched_tokens": matched,
            "accepted": strong,
        })
        if not strong:
            continue

        skill = best["id"]
        if skill not in selected and len(selected) < max_skills:
            selected.append(skill)

        existing_stage = next(
            (
                stage for stage in result.get("stages", [])
                if stage.get("stage") == stage_index
            ),
            None,
        )
        if existing_stage is None:
            result.setdefault("stages", []).append({
                "stage": stage_index,
                "text": clause,
                "selected": [skill],
                "reason": "query-centric capability evidence",
                "confidence": "high",
            })
        elif skill not in existing_stage.get("selected", []):
            existing_stage.setdefault("selected", []).append(skill)

    result.setdefault("selection_trace", {})["semantic_capability_rank"] = semantic_trace

    objective_identity_skill, objective_identity = _identity_candidate(
        catalog, expanded, decisions, objective
    )
    if objective_identity_skill and objective_identity_skill not in selected:
        selected.insert(0, objective_identity_skill)

    # Preserve high-confidence whole-request identity even when SolForge
    # decomposes the request into multiple supporting stages.
    identity_trace = []
    if objective_identity:
        identity_trace.append({
            "stage": None,
            "text": objective,
            **objective_identity,
        })
    for stage in result["stages"]:
        identity_skill, identity = _identity_candidate(
            catalog, expanded, decisions, stage["text"]
        )
        if objective_identity_skill and not identity_skill:
            identity_skill = objective_identity_skill
            identity = objective_identity
        available = [
            skill for skill in stage["selected"]
            if skill in known and _decision_allows(decisions, skill)
        ]
        if identity_skill:
            if identity_skill not in available:
                available = [identity_skill]
            stage["reason"] = "catalog capability identity"
            stage["confidence"] = "high"
            identity_trace.append({
                "stage": stage.get("stage"),
                "text": stage.get("text"),
                **identity,
            })
        elif identity and identity.get("blocked"):
            identity_trace.append({
                "stage": stage.get("stage"),
                "text": stage.get("text"),
                **identity,
            })

        if not available:
            candidate, denied_candidate = _repair_candidate(
                catalog, decisions, stage["text"], selected
            )
            available = [candidate] if candidate else []
            if not candidate and denied_candidate:
                result["unselected_requested_stages"].append({
                    "stage": stage.get("stage"),
                    "text": stage.get("text"),
                    "candidate": denied_candidate,
                    "reason": "candidate inadmissible by contract policy",
                })
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
            skill, _ = _repair_candidate(catalog, decisions, stage_text, selected)
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
    result["selection_trace"]["capability_identity"] = identity_trace

    allowed_skills = {
        skill for skill, decision in decisions.items()
        if decision.get("status") != "denied"
    }
    available_inputs = []
    if isinstance(context, dict):
        raw_available = context.get("available_inputs", [])
        if isinstance(raw_available, list):
            available_inputs = [
                item for item in raw_available if isinstance(item, str) and item
            ]

    dataflow_plan = resolve_required_inputs(
        expanded,
        selected,
        available_inputs=available_inputs,
        allowed_skills=allowed_skills,
    )
    for addition in dataflow_plan["additions"]:
        producer = addition["producer"]
        consumer = addition["consumer"]
        if producer in selected or producer not in known or len(selected) >= max_skills:
            continue
        try:
            index = selected.index(consumer)
        except ValueError:
            index = len(selected)
        selected.insert(index, producer)
        if producer not in graph["nodes"] and producer in expanded["nodes"]:
            graph["nodes"][producer] = expanded["nodes"][producer]

    # Re-evaluate input status after any unique producer additions.
    dataflow = resolve_required_inputs(
        expanded,
        selected,
        available_inputs=available_inputs,
        allowed_skills=allowed_skills,
    )
    result["selected"] = selected
    dataflow["additions"] = dataflow_plan["additions"]
    result["dataflow"] = dataflow
    blocked_inputs = []
    for key, status in dataflow["inputs"].items():
        if status.get("status") in {"elicitable", "unavailable"}:
            consumer, input_name = key.split(":", 1)
            blocked_inputs.append({
                "stage": None,
                "text": consumer,
                "reason": (
                    "required input requires elicitation"
                    if status["status"] == "elicitable"
                    else "required input unavailable"
                ),
                "rejected": [],
                "input": input_name,
                "input_status": status,
            })
    if blocked_inputs:
        result.setdefault("blocked_stages", []).extend(blocked_inputs)

    result.setdefault("selection_trace", {})["dataflow"] = {
        "added_producers": dataflow_plan["additions"],
        "explanations": dataflow["explanations"],
        "available_inputs": available_inputs,
    }

    original_selected = list(selected)
    result = validate_route(
        result,
        graph,
        decisions,
        policy_public=normalized_policy.public(),
        original_selected=original_selected,
    )
    result["selected"] = _enforce_dataflow_order(
        result["selected"], dataflow["explanations"]
    )
    index = contract_index(catalog)
    result["skills"] = [
        known[skill].public() for skill in result["selected"]
        if skill in known
    ]
    result["selected_contracts"] = {
        skill: index.get(skill)
        for skill in result["selected"]
        if skill in known
    }
    result["excluded_effects"] = list(normalized_policy.denied_effects)
    result["execution_authorized"] = False
    result["audit"] = route_audit_event(result)
    return result


@lru_cache(maxsize=1)
def get_graph() -> dict:
    """Return portable selection relationships, never host filesystem paths."""
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def graph_generation(graph: dict | None = None) -> str:
    graph = graph or get_graph()
    payload = json.dumps(
        {"nodes": graph.get("nodes", {}), "edges": graph.get("edges", [])},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def contract_index(catalog: SkillCatalog):
    core = get_graph()
    return catalog.contract_index(
        legacy_nodes=core.get("nodes", {}),
        graph_generation=graph_generation(core),
    )


def catalog_graph(catalog: SkillCatalog) -> dict:
    """Expose mounted skills with compact indexed contract metadata."""
    core = get_graph()
    index = contract_index(catalog)
    entries = {item["id"]: item for item in index.entries()}
    records = {record.id: record for record in catalog.records()}
    nodes = {}
    for skill_id, record in records.items():
        legacy_node = core["nodes"].get(skill_id)
        base = dict(legacy_node or {
            "id": skill_id,
            "description": record.public()["description"],
            "domain": "general",
            "effect": None,
            "selection": "catalog discovery or explicit",
            "inputs": ["user objective", "applicable skill prerequisites"],
            "outputs": ["skill-defined deliverable"],
        })
        contract = entries[skill_id]
        base["contract_status"] = contract["status"]
        base["contract_source"] = contract.get("source")
        base["contract_validation_errors"] = contract.get("validation_errors", [])
        base["side_effects"] = contract.get("effects")
        base["effects"] = contract.get("effects")
        base["auth_scope"] = contract.get("auth_scope")
        base["test_contract"] = contract.get("test_contract")
        base["contract_digest"] = contract.get("contract_digest")
        base["entrypoint_digest"] = contract.get("entrypoint_digest")
        base["verification"] = contract.get("verification", {})
        base["risk"] = contract.get("risk", {})
        base["provenance"] = contract.get("provenance", {})
        base["trust"] = contract.get("trust", {})
        if contract.get("source") == "sidecar" and contract.get("status") == "declared":
            base["inputs"] = contract.get("inputs", [])
            base["outputs"] = contract.get("outputs", [])
        if contract.get("schema_version") is not None:
            base["schema_version"] = contract["schema_version"]
        if contract.get("contract_revision") is not None:
            base["contract_revision"] = contract["contract_revision"]
        if contract.get("capabilities") or contract.get("resources"):
            base["authority"] = {
                "capabilities": contract.get("capabilities", []),
                "resources": contract.get("resources", []),
            }
        nodes[skill_id] = base

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
        "contract_index_generation": index.generation,
    }
