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
