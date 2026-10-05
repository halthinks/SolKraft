from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, catalog_graph

from scripts.semantic_router_benchmark import (
    DEV_PROMPTS_PER_SKILL,
    HOLDOUT_PROMPTS_PER_SKILL,
    SINGLE_PROMPTS_PER_SKILL,
    build_profiles,
    leakage_violations,
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
                    "targets": targets,
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
