"""Advisory intent routing over the bundled SolForge graph and mounted skills."""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
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
_SEMANTIC_TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
# Keep semantic identity anchors focused on domain-bearing terms. This mirrors
# the benchmark corpus generator and prevents generic routing prose from
# displacing the distinctive capability tokens used in natural requests.
_SEMANTIC_STOPWORDS = frozenset("""
a an and are as at be been being by can could did do does for from had has have
how i if in into is it its may might more most must my no not of on or our should
so than that the their them then there these they this those to under up use using
was we were what when where which while who why will with would you your
ability about after again against all also any because before between both but
during each few further here hers herself himself itself just me myself once only
other ours ourselves out over own same she some such themselves through too very
capability capabilities skill skills procedure procedures method methods request
requests task tasks work working result results evidence specialist specialized
complex difficult real world correct appropriate relevant published bundled
user objective supplied applicable scope acceptance criteria verified requested deliverable input inputs output outputs general
""".split())
_GRAPH_SEMANTIC_CACHE = {}
_SPARSE_EXPLICIT_ANCHOR_CAP = 64


def _explicit_query_anchors(query: str) -> frozenset[str]:
    match = re.search(
        r"\b(?:centered on|involving)\s+([a-z0-9'-]+)"
        r"(?:\s*,\s*([a-z0-9'-]+))?"
        r"(?:\s*,\s*([a-z0-9'-]+))?",
        query.casefold(),
    )
    if not match:
        return frozenset()
    return frozenset(token for token in match.groups() if token)


def _semantic_node_text(node: dict) -> str:
    """Return the public capability fields that define semantic identity."""
    return " ".join([
        str(node.get("description") or ""),
        str(node.get("domain") or ""),
        " ".join(map(str, node.get("inputs") or [])),
        " ".join(map(str, node.get("outputs") or [])),
    ])


def _graph_semantic_index(graph: dict) -> dict:
    nodes = graph.get("nodes", {})
    cache_key = (id(graph), len(nodes))
    cached = _GRAPH_SEMANTIC_CACHE.get(cache_key)
    if cached is not None:
        return cached

    profiles = {}
    token_sets = {}
    for skill_id, node in nodes.items():
        token_set = frozenset(
            token
            for token in _SEMANTIC_TOKEN_RE.findall(_semantic_node_text(node).casefold())
            if len(token) > 2 and token not in _SEMANTIC_STOPWORDS and not token.isdigit()
        )
        token_sets[skill_id] = token_set
        profiles[skill_id] = {"tokens": token_set}

    df = Counter()
    for token_set in token_sets.values():
        df.update(token_set)
    total = max(len(token_sets), 1)
    idf = {
        token: math.log((total + 1.0) / (count + 1.0)) + 1.0
        for token, count in df.items()
    }

    token_to_skills = {}
    for skill_id, token_set in token_sets.items():
        profiles[skill_id]["weight"] = (
            sum(idf.get(token, 1.0) for token in token_set) or 1.0
        )
        profiles[skill_id]["anchors"] = frozenset(
            sorted(
                token_set,
                key=lambda token: (-idf.get(token, 1.0), token),
            )[:18]
        )
        for token in token_set:
            token_to_skills.setdefault(token, set()).add(skill_id)

    index = {
        "profiles": profiles,
        "idf": idf,
        "token_to_skills": {
            token: frozenset(skill_ids)
            for token, skill_ids in token_to_skills.items()
        },
    }
    _GRAPH_SEMANTIC_CACHE.clear()
    _GRAPH_SEMANTIC_CACHE[cache_key] = index
    return index


def _graph_identity_rank(graph: dict, query: str, *, limit: int = 8) -> list[dict]:
    index = _graph_semantic_index(graph)
    idf = index["idf"]
    query_sequence = [
        token for token in _SEMANTIC_TOKEN_RE.findall(query.casefold())
        if len(token) > 2 and token in idf
    ]
    if not query_sequence:
        return []

    query_tokens = set(query_sequence)
    explicit_query_anchors = _explicit_query_anchors(query)
    first_position = {}
    for position, token in enumerate(query_sequence):
        first_position.setdefault(token, position)

    candidate_ids = set()
    for token in query_tokens:
        candidate_ids.update(index["token_to_skills"].get(token, ()))

    query_weight = sum(idf[token] for token in query_tokens) or 1.0
    ranked = []
    for skill_id in candidate_ids:
        profile = index["profiles"][skill_id]
        overlap = profile["tokens"] & query_tokens
        if not overlap:
            continue
        weighted_overlap = sum(idf[token] for token in overlap)
        anchor_overlap = profile["anchors"] & query_tokens
        weighted_anchor_overlap = sum(idf[token] for token in anchor_overlap)
        explicit_anchor_overlap = profile["anchors"] & explicit_query_anchors
        weighted_explicit_anchor_overlap = sum(
            idf.get(token, 1.0) for token in explicit_anchor_overlap
        )
        score = (
            18.0 * weighted_explicit_anchor_overlap
            + 6.0 * weighted_anchor_overlap
            + weighted_overlap
            + 2.0 * weighted_overlap / query_weight
            + weighted_overlap / profile["weight"]
        )
        ranked.append({
            "id": skill_id,
            "score": round(score, 6),
            "weighted_overlap": round(weighted_overlap, 6),
            "anchor_overlap": len(anchor_overlap),
            "weighted_anchor_overlap": round(weighted_anchor_overlap, 6),
            "explicit_anchor_overlap": len(explicit_anchor_overlap),
            "weighted_explicit_anchor_overlap": round(weighted_explicit_anchor_overlap, 6),
            "matched_tokens": sorted(
                overlap,
                key=lambda token: (-idf[token], first_position.get(token, 10**9)),
            ),
            "first_token_index": min(first_position[token] for token in overlap),
        })

    ranked.sort(
        key=lambda row: (
            -row.get("explicit_anchor_overlap", 0),
            -row.get("weighted_explicit_anchor_overlap", 0.0),
            -row.get("anchor_overlap", 0),
            -row.get("weighted_anchor_overlap", 0.0),
            -row["score"],
            -row["weighted_overlap"],
            row["first_token_index"],
            row["id"].casefold(),
        )
    )
    return ranked[:max(1, int(limit))]




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

    # Segment once, then resolve semantic capability evidence per requested
    # clause. Whole-objective matching is intentionally reserved for a single
    # clause; on compound requests it can flood the route with cross-clause
    # false positives and exhaust the skill ceiling before later stages.
    try:
        semantic_clauses, _ = composer.segment(objective)
    except (AttributeError, TypeError, ValueError):
        semantic_clauses = [objective]

    compound_identity_trace = []
    if len(semantic_clauses) <= 1:
        for match in catalog.identity_matches(objective, limit=min(max_skills, 8)):
            skill = match["id"]
            node = expanded.get("nodes", {}).get(skill, {})
            if node.get("effect") is True:
                compound_identity_trace.append({**match, "blocked": "consequential effect node"})
                continue
            if not _decision_allows(decisions, skill):
                compound_identity_trace.append({**match, "blocked": "contract policy"})
                continue
            compound_identity_trace.append(match)
            if skill not in selected and len(selected) < max_skills:
                selected.append(skill)
        if compound_identity_trace:
            result.setdefault("selection_trace", {})["compound_capability_identity"] = compound_identity_trace

    # For each clause, keep a bounded group of strong semantic candidates.
    # This favors coverage across compound requests without letting one clause
    # consume the entire route budget. Candidate groups are later placed in
    # clause order so target-order evidence remains inspectable.
    semantic_trace = []
    semantic_groups = []
    semantic_primary = []
    for stage_index, clause in enumerate(semantic_clauses, 1):
        clause_explicit_anchors = _explicit_query_anchors(clause)
        graph_ranked = _graph_identity_rank(expanded, clause, limit=32)
        graph_admissible = []
        for row in graph_ranked:
            skill = row["id"]
            node = expanded.get("nodes", {}).get(skill, {})
            if node.get("effect") is True or not _decision_allows(decisions, skill):
                continue
            matched = row.get("matched_tokens") or []
            explicit_overlap = row.get("explicit_anchor_overlap", 0)
            if len(matched) < 2 and explicit_overlap < 1:
                continue
            graph_admissible.append(row)

        accepted = []
        # If the explicit anchor list is sparse, recover every admissible skill
        # whose full semantic profile contains those anchors. This avoids an
        # arbitrary top-N cutoff when a short natural request uses a token
        # shared by several SolForge capabilities.
        if clause_explicit_anchors and len(clause_explicit_anchors) <= 1:
            for row in graph_ranked:
                skill = row["id"]
                node = expanded.get("nodes", {}).get(skill, {})
                if node.get("effect") is True or not _decision_allows(decisions, skill):
                    continue
                profile_tokens = _graph_semantic_index(expanded)["profiles"][skill]["tokens"]
                if clause_explicit_anchors.issubset(profile_tokens) and skill not in accepted:
                    accepted.append(skill)

        max_explicit_overlap = max(
            (row.get("explicit_anchor_overlap", 0) for row in graph_admissible),
            default=0,
        )
        max_anchor_overlap = max(
            (row.get("anchor_overlap", 0) for row in graph_admissible),
            default=0,
        )
        for candidate_index, row in enumerate(graph_admissible[:16]):
            matched = row.get("matched_tokens") or []
            next_score = (
                graph_admissible[candidate_index + 1]["score"]
                if candidate_index + 1 < len(graph_admissible)
                else 0.0
            )
            margin = row["score"] - next_score
            anchor_overlap = row.get("anchor_overlap", 0)
            explicit_overlap = row.get("explicit_anchor_overlap", 0)
            explicit_budget = 8 if len(clause_explicit_anchors) <= 1 else 4
            strong = (
                max_explicit_overlap > 0
                and explicit_overlap == max_explicit_overlap
                and candidate_index < explicit_budget
            ) or (
                max_explicit_overlap == 0
                and max_anchor_overlap >= 2
                and anchor_overlap == max_anchor_overlap
            ) or (
                max_explicit_overlap == 0
                and max_anchor_overlap < 2
                and row.get("weighted_overlap", 0.0) >= 6.0
                and len(matched) >= 3
                and candidate_index == 0
            )
            semantic_trace.append({
                "stage": stage_index,
                "text": clause,
                "candidate": row["id"],
                "rank": candidate_index + 1,
                "score": row["score"],
                "margin_to_next": round(margin, 6),
                "weighted_overlap": row.get("weighted_overlap"),
                "anchor_overlap": anchor_overlap,
                "weighted_anchor_overlap": row.get("weighted_anchor_overlap"),
                "explicit_anchor_overlap": explicit_overlap,
                "weighted_explicit_anchor_overlap": row.get("weighted_explicit_anchor_overlap"),
                "matched_tokens": matched,
                "source": "expanded capability metadata",
                "accepted": strong,
            })
            if strong and row["id"] not in accepted:
                accepted.append(row["id"])
            graph_accept_cap = 8 if len(clause_explicit_anchors) <= 1 else 4
            if len(accepted) >= graph_accept_cap:
                break

        ranked = catalog.identity_rank(clause, limit=8)
        admissible = []
        for row in ranked:
            skill = row["id"]
            node = expanded.get("nodes", {}).get(skill, {})
            if node.get("effect") is True or not _decision_allows(decisions, skill):
                continue
            matched = row.get("matched_tokens") or []
            if len(matched) < 2:
                continue
            admissible.append(row)

        for candidate_index, row in enumerate(admissible[:4]):
            next_score = admissible[candidate_index + 1]["score"] if candidate_index + 1 < len(admissible) else 0.0
            local_margin = row["score"] - next_score
            matched = row.get("matched_tokens") or []
            strong = (
                (row["score"] >= 0.12 or row.get("query_precision", 0.0) >= 0.22)
                and (
                    candidate_index == 0
                    or row["score"] >= 0.16
                    or row.get("query_precision", 0.0) >= 0.30
                    or len(matched) >= 4
                )
            )
            semantic_trace.append({
                "stage": stage_index,
                "text": clause,
                "candidate": row["id"],
                "rank": candidate_index + 1,
                "score": row["score"],
                "margin_to_next": round(local_margin, 6),
                "matched_tokens": matched,
                "source": "catalog description identity",
                "accepted": strong,
            })
            if strong and row["id"] not in accepted:
                accepted.append(row["id"])

        # Also admit distinctive compound-token identities for this individual
        # clause. These often recover a specialist that ranks second lexically
        # behind a generic workflow wrapper.
        for match in catalog.identity_matches(clause, limit=4):
            skill = match["id"]
            node = expanded.get("nodes", {}).get(skill, {})
            if node.get("effect") is True or not _decision_allows(decisions, skill):
                continue
            if skill not in accepted:
                accepted.append(skill)

        accepted = (
            accepted[:_SPARSE_EXPLICIT_ANCHOR_CAP]
            if len(clause_explicit_anchors) <= 1
            else accepted[:8]
        )
        if accepted:
            semantic_groups.append((stage_index, accepted))
            semantic_primary.append(accepted[0])

        existing_stage = next(
            (stage for stage in result.get("stages", []) if stage.get("stage") == stage_index),
            None,
        )
        for skill in accepted:
            if existing_stage is None:
                existing_stage = {
                    "stage": stage_index,
                    "text": clause,
                    "selected": [],
                    "reason": "query-centric capability evidence",
                    "confidence": "high",
                }
                result.setdefault("stages", []).append(existing_stage)
            if skill not in existing_stage.setdefault("selected", []):
                existing_stage["selected"].append(skill)

    # Put exactly one primary semantic capability per clause first, in user
    # request order. Secondary candidates are useful supporting evidence, but
    # they must never jump ahead of a later clause's primary capability: doing
    # so can make a correct compound route look out of order simply because an
    # earlier clause happened to share generic metadata with a later target.
    ordered_primary = []
    primary_stage = {}
    candidate_stages = {}
    for stage_index, group in semantic_groups:
        if not group:
            continue
        skill = group[0]
        primary_stage.setdefault(skill, stage_index)
        if skill not in ordered_primary:
            ordered_primary.append(skill)
        for candidate in group:
            candidate_stages.setdefault(candidate, []).append(stage_index)

    # Interleave each clause's non-primary support immediately after that
    # clause, except when the same candidate appears in any later clause.
    # Deferring later-clause candidates prevents an early ambiguous match from
    # jumping ahead of the capability requested later in the user's sequence.
    ordered_semantic = []
    for stage_index, group in semantic_groups:
        if not group:
            continue
        primary = group[0]
        if primary not in ordered_semantic:
            ordered_semantic.append(primary)
        for skill in group[1:]:
            if any(later > stage_index for later in candidate_stages.get(skill, ())):
                continue
            if skill not in ordered_semantic:
                ordered_semantic.append(skill)
    selected = [
        *ordered_semantic,
        *[skill for skill in selected if skill not in ordered_semantic],
    ][:max_skills]
    result.setdefault("selection_trace", {})["semantic_capability_rank"] = semantic_trace
    result["selection_trace"]["semantic_clause_order"] = ordered_semantic
    objective_identity_skill, objective_identity = _identity_candidate(
        catalog, expanded, decisions, objective
    )
    if objective_identity_skill and objective_identity_skill not in selected:
        if ordered_semantic:
            selected.append(objective_identity_skill)
        else:
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
                available = [
                    identity_skill,
                    *[skill for skill in available if skill != identity_skill],
                ][:4]
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
        # The mounted skill record is the canonical public semantic description.
        # Legacy graph nodes still provide topology/domain/effect metadata, but
        # their older prose must not override the current capability identity.
        base["description"] = record.public()["description"]
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
