from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, catalog_graph

from scripts.semantic_router_benchmark import (
    DEV_PROMPTS_PER_SKILL,
    HOLDOUT_PROMPTS_PER_SKILL,
    SINGLE_PROMPTS_PER_SKILL,
    build_profiles,
    leakage_violations,
    shared_anchor_prompt,
    shared_anchor_skills,
    single_prompt,
)


def test_semantic_single_skill_corpus_shape_and_leakage():
    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    graph = catalog_graph(catalog)
    profiles = build_profiles(records, graph)

    assert SINGLE_PROMPTS_PER_SKILL == 1000
    assert DEV_PROMPTS_PER_SKILL == 800
    assert HOLDOUT_PROMPTS_PER_SKILL == 200
    assert DEV_PROMPTS_PER_SKILL + HOLDOUT_PROMPTS_PER_SKILL == SINGLE_PROMPTS_PER_SKILL

    # Check the full 1,000-prompt surface for several deterministic catalog
    # positions, plus at least one prompt for every skill.
    probe_records = [
        records[0],
        records[len(records) // 3],
        records[(2 * len(records)) // 3],
        records[-1],
    ]

    for record in probe_records:
        prompts = [
            single_prompt(record, profiles[record.id], profiles, case_index)
            for case_index in range(SINGLE_PROMPTS_PER_SKILL)
        ]
        assert len(set(prompts)) == SINGLE_PROMPTS_PER_SKILL
        for prompt in prompts:
            assert not leakage_violations(prompt, record.id, record.description)

    for index, record in enumerate(records):
        prompt = single_prompt(record, profiles[record.id], profiles, index % SINGLE_PROMPTS_PER_SKILL)
        assert prompt.strip()
        assert not leakage_violations(prompt, record.id, record.description)


def test_semantic_router_composition_regression_probe():
    """A fast guard for the exact failure mode caught by the full proof."""
    import json
    import solkraft.routing as routing_module
    from solkraft.routing import contract_index, route_request
    from scripts.semantic_router_benchmark import (
        composition_prompt,
        composition_targets,
        selectable_ids,
    )

    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    records_by_id = {record.id: record for record in records}
    graph = catalog_graph(catalog)
    index = contract_index(catalog)
    entries = {entry["id"]: entry for entry in index.entries()}
    profiles = build_profiles(records, graph)
    selectable = selectable_ids(records, graph, entries)

    frozen_graph = graph
    frozen_core = routing_module.get_graph()
    frozen_index = index
    old_catalog_graph = routing_module.catalog_graph
    old_get_graph = routing_module.get_graph
    old_contract_index = routing_module.contract_index
    routing_module.catalog_graph = lambda _catalog: frozen_graph
    routing_module.get_graph = lambda: frozen_core
    routing_module.contract_index = lambda _catalog: frozen_index
    try:
        failures = []
        for case_id in range(32):
            targets = composition_targets(selectable, case_id)
            prompt = composition_prompt(records_by_id, profiles, targets, case_id)
            route = route_request(catalog, prompt, max_skills=50, policy={"contract_mode": "hardened"})
            selected = route.get("selected") or []
            cursor = 0
            for skill in selected:
                if cursor < len(targets) and skill == targets[cursor]:
                    cursor += 1
            coverage = set(targets).issubset(set(selected))
            ordered = cursor == len(targets)
            if not coverage or not ordered:
                failures.append({
                    "case": case_id,
                    "prompt": prompt,
                    "targets": targets,
                    "target_anchors": {skill: profiles[skill]["anchors"] for skill in targets},
                    "selected": selected,
                    "semantic_clause_order": route.get("selection_trace", {}).get("semantic_clause_order"),
                    "semantic_rank": route.get("selection_trace", {}).get("semantic_capability_rank"),
                    "stages": route.get("stages"),
                    "coverage": coverage,
                    "ordered": ordered,
                })
                if len(failures) >= 3:
                    break
        assert not failures, json.dumps(failures, indent=2, sort_keys=True)
    finally:
        routing_module.catalog_graph = old_catalog_graph
        routing_module.get_graph = old_get_graph
        routing_module.contract_index = old_contract_index


def test_semantic_router_low_skill_rate_regression_probe():
    """Fast sample for skills that were below the full-proof 0.90 gate."""
    import json
    import solkraft.routing as routing_module
    from solkraft.routing import contract_index, route_request

    watched = [
        "solforge-mvp-create",
        "solforge-code-mastery",
        "solforge-prompt",
        "solforge-finalize",
        "solforge-plugin-skill-release",
        "solforge-report",
        "solforge-package-build",
        "solforge-release-matrix",
        "solforge-portability-audit",
        "solforge-run-refactor",
        "solforge-target-verify",
        "solforge-propose",
        "solforge-run-single",
        "solforge-research-mastery-perfection",
        "solforge-cross-build",
    ]

    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    records_by_id = {record.id: record for record in records}
    graph = catalog_graph(catalog)
    index = contract_index(catalog)
    profiles = build_profiles(records, graph)

    frozen_graph = graph
    frozen_core = routing_module.get_graph()
    frozen_index = index
    old_catalog_graph = routing_module.catalog_graph
    old_get_graph = routing_module.get_graph
    old_contract_index = routing_module.contract_index
    routing_module.catalog_graph = lambda _catalog: frozen_graph
    routing_module.get_graph = lambda: frozen_core
    routing_module.contract_index = lambda _catalog: frozen_index
    try:
        failures = {}
        for skill_id in watched:
            if skill_id not in records_by_id:
                continue
            record = records_by_id[skill_id]
            passed = 0
            samples = []
            for local_case in range(100):
                prompt = single_prompt(record, profiles[skill_id], profiles, local_case)
                route = route_request(catalog, prompt, max_skills=50, policy={"contract_mode": "hardened"})
                selected = route.get("selected") or []
                ok = skill_id in selected
                passed += int(ok)
                if not ok and len(samples) < 3:
                    samples.append({
                        "case": local_case,
                        "prompt": prompt,
                        "anchors": profiles[skill_id]["anchors"],
                        "selected": selected[:20],
                        "semantic_rank": route.get("selection_trace", {}).get("semantic_capability_rank"),
                    })
            rate = passed / 100
            if rate < 0.90:
                failures[skill_id] = {"rate": rate, "samples": samples}
        assert not failures, json.dumps(failures, indent=2, sort_keys=True)
    finally:
        routing_module.catalog_graph = old_catalog_graph
        routing_module.get_graph = old_get_graph
        routing_module.contract_index = old_contract_index


def test_single_skill_prompts_preserve_distinguishing_anchor():
    """Exact-recall cases must contain evidence that distinguishes the target."""
    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    graph = catalog_graph(catalog)
    profiles = build_profiles(records, graph)

    for record in records:
        profile = profiles[record.id]
        distinctive = set(profile.get("distinguishing_anchors") or ())
        if not distinctive:
            continue
        for case_index in range(100):
            prompt_tokens = set(prompt.casefold() for prompt in __import__("re").findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", single_prompt(record, profile, profiles, case_index)))
            assert prompt_tokens & distinctive, {
                "skill": record.id,
                "case": case_index,
                "distinguishing": sorted(distinctive),
            }


def test_shared_anchor_prompt_is_treated_as_ambiguous_not_exact_recall():
    """Shared-anchor prompts are ambiguity cases, not hidden-label recall cases."""
    import solkraft.routing as routing_module
    from solkraft.routing import contract_index, route_request

    catalog = SkillCatalog([BUNDLE_ROOT], preferred_root=BUNDLE_ROOT)
    records = list(catalog.records())
    graph = catalog_graph(catalog)
    index = contract_index(catalog)
    profiles = build_profiles(records, graph)

    frozen_graph = graph
    frozen_core = routing_module.get_graph()
    frozen_index = index
    old_catalog_graph = routing_module.catalog_graph
    old_get_graph = routing_module.get_graph
    old_contract_index = routing_module.contract_index
    routing_module.catalog_graph = lambda _catalog: frozen_graph
    routing_module.get_graph = lambda: frozen_core
    routing_module.contract_index = lambda _catalog: frozen_index
    try:
        entries = {entry["id"]: entry for entry in index.entries()}
        selectable = {
            record.id for record in records
            if graph["nodes"][record.id].get("effect") is not True
            and entries[record.id].get("status") not in {"opaque", "invalid", "unsupported"}
        }
        shared = [
            (anchor, [skill for skill in shared_anchor_skills(profiles, anchor) if skill in selectable])
            for anchor in sorted({a for p in profiles.values() for a in p["anchors"]})
        ]
        shared = [(anchor, skills) for anchor, skills in shared if len(skills) >= 3][:12]
        assert shared
        for case_index, (anchor, candidates) in enumerate(shared):
            prompt = shared_anchor_prompt(anchor, case_index)
            route = route_request(catalog, prompt, max_skills=50, policy={"contract_mode": "hardened"})
            selected = set(route.get("selected") or [])
            # Ambiguity succeeds when routing preserves more than one plausible
            # *admissible* shared-anchor candidate. Consequential/blocked skills
            # are intentionally excluded from the ambiguity expectation.
            assert len(selected & set(candidates)) >= 2, {
                "anchor": anchor,
                "candidates": candidates,
                "selected": route.get("selected") or [],
                "prompt": prompt,
            }
    finally:
        routing_module.catalog_graph = old_catalog_graph
        routing_module.get_graph = old_get_graph
        routing_module.contract_index = old_contract_index
