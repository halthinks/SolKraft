"""Whole-route validation after contract-aware composition."""
from __future__ import annotations


def _selected_in_stages(result: dict) -> list[str]:
    ordered = []
    for stage in result.get("stages", []):
        for skill in stage.get("selected", []):
            if skill not in ordered:
                ordered.append(skill)
    for skill in result.get("selected", []):
        if skill not in ordered:
            ordered.append(skill)
    return ordered


def _append_blocked(blocked_stages, item):
    key = (item.get("stage"), item.get("text"), tuple(item.get("rejected") or ()))
    existing = {
        (row.get("stage"), row.get("text"), tuple(row.get("rejected") or ()))
        for row in blocked_stages
    }
    if key not in existing:
        blocked_stages.append(item)


def validate_route(
    result: dict,
    graph: dict,
    decisions: dict[str, dict],
    *,
    policy_public: dict,
    original_selected: list[str] | None = None,
) -> dict:
    """Apply route policy and report any route that is no longer complete."""
    original_selected = list(original_selected or result.get("selected", []))
    denied = {
        skill for skill in original_selected
        if decisions.get(skill, {}).get("status") == "denied"
    }

    blocked_stages = list(result.get("blocked_stages", []))
    for stage in result.get("stages", []):
        before = list(stage.get("selected", []))
        kept = [skill for skill in before if skill not in denied]
        removed = [skill for skill in before if skill in denied]
        stage["selected"] = kept
        if before and not kept and removed:
            _append_blocked(blocked_stages, {
                "stage": stage.get("stage"),
                "text": stage.get("text"),
                "reason": "all selected skills denied by route policy",
                "rejected": removed,
            })

    # A prefiltered mapped candidate that could not be repaired is an explicit
    # blocked stage, not an ordinary abstention.
    for unresolved in result.get("unselected_requested_stages", []):
        candidate = unresolved.get("candidate")
        if (
            unresolved.get("reason") == "candidate inadmissible by contract policy"
            and candidate
        ):
            _append_blocked(blocked_stages, {
                "stage": unresolved.get("stage"),
                "text": unresolved.get("text"),
                "reason": "candidate denied by route policy and no admissible replacement was found",
                "rejected": [candidate],
            })

    # Dependency invalidation is conservative: it applies only where both
    # endpoints were actually members of this composed route.
    broken_dependencies = []
    route_members = set(original_selected)
    newly_blocked = set(denied)
    changed = True
    while changed:
        changed = False
        for edge in graph.get("edges", []):
            left = edge.get("from")
            right = edge.get("to")
            if left not in route_members or right not in route_members:
                continue
            blocked = left if left in newly_blocked else right if right in newly_blocked else None
            survivor = right if blocked == left else left if blocked == right else None
            if not survivor or survivor in newly_blocked:
                continue
            newly_blocked.add(survivor)
            broken_dependencies.append({
                "blocked": survivor,
                "because": blocked,
                "type": edge.get("type"),
                "condition": edge.get("condition"),
            })
            changed = True

    if newly_blocked - denied:
        for stage in result.get("stages", []):
            before = list(stage.get("selected", []))
            removed = [skill for skill in before if skill in newly_blocked]
            stage["selected"] = [skill for skill in before if skill not in newly_blocked]
            if before and not stage["selected"] and removed:
                _append_blocked(blocked_stages, {
                    "stage": stage.get("stage"),
                    "text": stage.get("text"),
                    "reason": "selected dependency was denied by route policy",
                    "rejected": removed,
                })

    selected = [
        skill for skill in _selected_in_stages(result)
        if skill not in newly_blocked
    ]
    result["selected"] = selected
    result["blocked_stages"] = blocked_stages
    result["broken_dependencies"] = broken_dependencies
    result["route_policy"] = policy_public
    result["denied_effects"] = list(policy_public.get("denied_effects") or [])

    touched = set(selected) | newly_blocked
    for unresolved in result.get("unselected_requested_stages", []):
        candidate = unresolved.get("candidate")
        if candidate:
            touched.add(candidate)
    for repair in result.get("selection_trace", {}).get("contract_repair", {}).get("repaired", []):
        if repair.get("rejected"):
            touched.add(repair["rejected"])
        if repair.get("replacement"):
            touched.add(repair["replacement"])
    result["contract_decisions"] = {
        skill: decisions[skill] for skill in sorted(touched)
        if skill in decisions
    }

    required_capabilities = set()
    required_resources = set()
    for skill in selected:
        decision = decisions.get(skill, {})
        required_capabilities.update(decision.get("capabilities") or [])
        required_resources.update(decision.get("resources") or [])
    result["required_capabilities"] = sorted(required_capabilities)
    result["required_resources"] = sorted(required_resources)

    if blocked_stages or broken_dependencies:
        result["selection_status"] = "partially_blocked" if selected else "blocked"
    else:
        result["selection_status"] = "matched" if selected else "abstained"
    result["execution_authorized"] = False
    return result
