import copy
import pytest
from scripts.check_contribution import validate, simulate
from solkraft.routing import get_graph, BUNDLE_ROOT
from solkraft.catalog import SkillCatalog


def manifest():
    return {'schema': 'solkraft/contribution/v1', 'skill': 'solforge-workflow-software-security',
            'provenance': {'author': 'SolKraft contributors', 'license': 'MIT', 'source': 'https://github.com/halthinks/SolKraft'},
            'cases': [
                {'objective': 'Audit software security trust boundaries and unsafe input handling', 'selected': ['solforge-workflow-software-security']},
                {'objective': 'Do not audit software security', 'selected': []},
                {'objective': 'Audit software security tomorrow', 'selected': []},
                {'objective': 'Explain this quotation: "audit software security"', 'selected': []},
            ]}


def test_registered_skill_and_negative_cases_are_checked():
    catalog = SkillCatalog([BUNDLE_ROOT])
    assert not validate(manifest(), get_graph(), catalog)
    result = simulate(manifest(), catalog, variants=2)
    assert result['total'] == 12
    assert result['unique'] == 12
    assert result['passed'] == 12


def test_catalog_only_or_missing_rule_cannot_pass_registration():
    graph = copy.deepcopy(get_graph())
    graph['rules'] = [r for r in graph['rules'] if r['id'] != manifest()['skill']]
    assert any('rule' in e for e in validate(manifest(), graph, SkillCatalog([BUNDLE_ROOT])))


def test_wrong_expected_route_fails_and_missing_negative_cases_rejected():
    data = manifest()
    data['cases'][0]['selected'] = []
    assert simulate(data, SkillCatalog([BUNDLE_ROOT]), variants=0)['passed'] < 4
    data['cases'] = data['cases'][:1]
    assert any('negative' in e for e in validate(data, get_graph(), SkillCatalog([BUNDLE_ROOT])))
