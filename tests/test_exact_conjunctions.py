from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request
import pytest
from scripts.semantic_router_benchmark import TONE_PREFIXES, DELIVERABLES


@pytest.fixture(scope='module')
def catalog():
    import solkraft.routing as routing
    mounted = SkillCatalog([BUNDLE_ROOT])
    graph = routing.catalog_graph(mounted); core = routing.get_graph(); index = routing.contract_index(mounted)
    originals = routing.catalog_graph, routing.get_graph, routing.contract_index
    routing.catalog_graph = lambda _: graph
    routing.get_graph = lambda: core
    routing.contract_index = lambda _: index
    try:
        yield mounted
    finally:
        routing.catalog_graph, routing.get_graph, routing.contract_index = originals


def test_unique_topic_conjunction_selects_one_skill_and_resolves_stage(catalog):
    route = route_request(catalog,
        'Help me figure out the engineering part involving candidate, repositories, decisions. '
        'Then investigate the software part involving untested, modes, plans.',
        policy={'contract_mode': 'hardened'})
    assert route['selected'] == ['sol-merge-report', 'solforge-independent-challenger']
    assert route['unselected_requested_stages'] == []


def test_ambiguous_topics_request_clarification_instead_of_selecting_neighbors(catalog):
    route = route_request(catalog,
        'Show me how to approach the data part involving analysis, definitions, data.',
        policy={'contract_mode': 'hardened'})
    assert route['selected'] == []
    assert any('clarification' in row['reason'] for row in route['unselected_requested_stages'])
    assert route['execution_authorized'] is False


@pytest.mark.parametrize('tone', TONE_PREFIXES)
@pytest.mark.parametrize('delivery', DELIVERABLES)
def test_framing_and_acceptance_instructions_do_not_add_work(tone, delivery, catalog):
    route = route_request(catalog,
        tone + 'Help me figure out the engineering part involving candidate, repositories, decisions. ' + delivery,
        policy={'contract_mode': 'hardened'})
    assert route['selected'] == ['sol-merge-report']
    assert route['unselected_requested_stages'] == []


@pytest.mark.parametrize('context', [
    'There is adjacent context involving inspect, repositories, but do not let that replace the primary need around adoption, reuse, candidate, repositories.',
    'Someone suggested treating this mainly as products, repositories; check that interpretation rather than assuming it is the right route.',
])
def test_explicitly_subordinate_interpretations_do_not_add_stages(context, catalog):
    route = route_request(catalog,
        'Help me figure out a problem centered on adoption, reuse, candidate, repositories. ' + context,
        policy={'contract_mode': 'hardened'})
    assert route['selected'] == ['sol-merge-report']
    assert route['unselected_requested_stages'] == []


def test_possessive_apostrophes_are_not_quotation_boundaries(catalog):
    route = route_request(catalog,
        "Help me figure out a problem centered on repository's, owned, install, native. "
        "There is adjacent context involving routing, native, but do not let that replace the primary need around repository's, owned, install, native.",
        policy={'contract_mode': 'hardened'})
    assert route['selected'] == ['solforge-workflow-solforge-plugin-development']
    assert route['unselected_requested_stages'] == []

def test_composer_keeps_one_typed_policy_failure(catalog):
    import solkraft.routing as routing
    result = routing._load_composer().compose_route(
        routing.catalog_graph(catalog), 'Prepare a verified handoff.',
        blocked_skills={'solforge-finalize'})
    assert result['selected'] == []
    assert result['unselected_requested_stages'] == [{
        'stage': 1, 'text': 'prepare a verified handoff',
        'candidate': 'solforge-finalize',
        'reason': 'candidate inadmissible by contract policy'}]


def test_semantic_recovery_clears_unavailable_provisional_stage(catalog, monkeypatch):
    import solkraft.routing as routing
    graph = routing.catalog_graph(catalog)
    monkeypatch.setitem(graph['nodes']['solforge-finalize'], 'effect', True)
    route = route_request(catalog,
        'Prepare a verified handoff involving candidate, repositories, decisions.',
        policy={'contract_mode': 'hardened'})
    assert route['selected'] == ['sol-merge-report']
    assert route['unselected_requested_stages'] == []
    assert route['execution_authorized'] is False


def test_composer_reports_unavailable_match_as_repairable():
    import solkraft.routing as routing
    graph = {'nodes': {'solforge-finalize': {'id': 'solforge-finalize', 'description': 'Deliver a verified handoff.', 'effect': True}}, 'edges': []}
    result = routing._load_composer().compose_route(graph, 'Prepare a verified handoff.')
    assert result['selected'] == []
    assert result['unselected_requested_stages'][0]['reason'] == 'no confident specialist match'
