import pytest

from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request


@pytest.fixture
def catalog():
    return SkillCatalog([BUNDLE_ROOT])


@pytest.mark.parametrize('objective', [
    'Do not deploy, publish, or delete anything.',
    'Explain what a business model means in a product strategy class.',
])
def test_preserves_intentional_abstention(catalog, objective):
    result = route_request(catalog, objective)
    assert result['selected'] == []
    assert result['selection_status'] == 'abstained'
    assert 'selection_trace' in result
    assert 'unselected_requested_stages' in result


def test_explicit_skills_and_context_are_preserved(catalog):
    result = route_request(catalog, 'Draft PR', explicit=['solforge-codebase'],
                           context={'stage': 'repository-release-gate', 'domain': 'software'})
    assert 'solforge-codebase' in result['selected']
    assert 'solforge-workflow-software-test' in result['selected']
    assert result['execution_authorized'] is False


def test_supporting_reference_is_retrievable(catalog):
    result = catalog.get_resource('solforge', 'references/matcher-guide.md')
    assert 'matcher' in result['content'].lower()
    with pytest.raises(KeyError):
        catalog.get_resource('solforge', '../../../AGENTS.md')


def test_graph_includes_every_catalog_skill(catalog):
    from solkraft.routing import catalog_graph
    graph = catalog_graph(catalog)
    assert set(graph['nodes']) == {record.id for record in catalog.records()}


def test_explicit_catalog_specialist_is_callable(catalog):
    result = route_request(catalog, 'Use the selected procedure',
                           explicit=['audit-git-worktrees'])
    assert result['selected'] == ['audit-git-worktrees']
