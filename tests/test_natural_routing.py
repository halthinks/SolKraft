"""Authored everyday requests, independent of metadata-token generation.

Exact routes protect precision as well as recall. These are regression examples,
not a statistical claim about arbitrary language or actual skill execution.
"""
import pytest
from solkraft.catalog import SkillCatalog
from solkraft.routing import BUNDLE_ROOT, route_request

CASES = [
    ('Inspect the codebase', ['codebase']),
    ('Run regression tests, then verify the release build', ['software-test']),
    ('Inspect the repository and trace the login code', ['codebase']),
    ('Diagnose why our API crashes under load', ['software-diagnose']),
    ('Implement CSV export in this application', ['software-build']),
    ('Run regression tests for the pending patch', ['software-test']),
    ('Audit unsafe input handling in our software', ['software-security']),
    ('Audit whether our application supports Linux and Windows', ['software-portability-audit']),
    ('Write a short email about the deployment failure', ['writing-draft']),
    ('Create an outline for my article', ['writing-outline']),
    ('Review this manuscript for clarity and consistency', ['writing-review']),
    ('Check the citations and unsupported claims in this article', ['writing-factcheck']),
    ('Validate the dataset for missing rows and duplicate records', ['data-validate']),
    ('Analyze sales data to explain the decline', ['data-analyze']),
    ('Build a dashboard with plots of monthly revenue', ['data-visualize']),
    ('Train the agent model on the cleaned examples', ['data-model']),
    ('Compare the business options for our company', ['business-compare']),
    ('Build a business model with pricing scenarios', ['business-model']),
    ('Research demand in the commercial market', ['business-market']),
    ('Conduct business diligence on investment risks', ['business-diligence']),
    ('Develop a business strategy and roadmap', ['business-strategy']),
    ('Prove the theorem for all positive integers', ['math-prove']),
    ('Find a counterexample to this mathematical conjecture', ['math-counterexample']),
    ('Compute a numerical solution to the equation', ['math-compute']),
    ('Verify every step of the mathematical proof', ['math-verify']),
    ('Explain the intuition behind the theorem', ['math-explain']),
    ('Solve the equation symbolically', ['math-solve']),
    ('Research the scientific literature on this mechanism', ['science-literature']),
    ('Derive a falsifiable hypothesis for this scientific result', ['science-hypothesis']),
    ('Design a controlled experiment to test the hypothesis', ['science-experiment']),
    ('Reproduce the published scientific claim', ['science-replication']),
    ('Write the scientific report with methods and results', ['science-report']),
    ('Define testable requirements for the CAD enclosure', ['engineering-requirements']),
    ('Create a CAD enclosure prototype', ['engineering-prototype']),
    ('Compare CAD enclosure design alternatives', ['engineering-trade']),
    ('Verify CAD tolerances and failure modes', ['engineering-verify']),
    ('Research authoritative sources for the privacy law', ['legal-research']),
    ('Compare the legal jurisdictions', ['legal-compare']),
    ('Draft a legal memo', ['legal-draft']),
    ('Assess compliance obligations and legal exposure', ['legal-risk']),
    ('Write a prompt for the implementation agent', ['@solforge-prompt']),
    ('Create the release matrix', ['@solforge-release-matrix']),
    ('Generate provenance evidence and artifact checksums', ['@solforge-sign-and-prove']),
    ('Prepare a verified handoff', ['@solforge-finalize']),
    ('Inspect the repository, diagnose the CI failure, implement a fix, run regression tests, and write the PR description',
     ['codebase', 'software-diagnose', 'software-build', 'software-test', 'writing-draft']),
    ('Build a business model, compare the business alternatives, and develop a business strategy',
     ['business-model', 'business-compare', 'business-strategy']),
    ('Do not audit software security', []),
    ('Audit software security tomorrow', []),
    ('Explain this quotation: "audit software security"', []),
    ('Explain what a business model means in a product strategy class', []),
]

@pytest.fixture(scope='module')
def catalog():
    return SkillCatalog([BUNDLE_ROOT])

@pytest.mark.parametrize('prompt,labels', CASES)
@pytest.mark.parametrize('context', ['', '. Context notes: preserve the user requirements and candidate revision.'])
def test_authored_requests(catalog, prompt, labels, context):
    expected = [s[1:] if s.startswith('@') else 'solforge-workflow-' + s for s in labels]
    result = route_request(catalog, prompt + context, policy={'contract_mode': 'hardened'})
    assert result['selected'] == expected
    assert result['execution_authorized'] is False

def test_explanation_does_not_shift_later_stage(catalog):
    result = route_request(catalog, 'Explain what a business model means. Then run regression tests.')
    assert result['selected'] == ['solforge-workflow-software-test']
    assert result['stages'][0]['stage'] == 2

def test_explicit_limit_applies_to_public_semantic_route(catalog):
    result = route_request(catalog, 'Investigate a problem centered on proof, mathematical, theorem', max_skills=1)
    assert len(result['selected']) <= 1

def test_semantic_cache_observes_metadata_changes():
    from solkraft.routing import _graph_identity_rank
    graph = {'nodes': {'first': {'description': 'quasar orbit'}, 'second': {'description': 'granite strata'}}}
    assert _graph_identity_rank(graph, 'quasar')[0]['id'] == 'first'
    graph['nodes']['first']['description'] = 'granite strata'
    graph['nodes']['second']['description'] = 'quasar orbit'
    assert _graph_identity_rank(graph, 'quasar')[0]['id'] == 'second'

def test_inline_exclusion_is_not_an_extra_stage(catalog):
    result = route_request(catalog, 'Inspect the repository without implementing fixes.')
    assert result['selected'] == ['solforge-workflow-codebase']
    assert any(row['reason'] == 'excluded scope' for row in result['selection_trace']['ignored_clauses'])


@pytest.mark.parametrize('closing', [
    'Give me the next steps and the evidence for each.',
    'Call out assumptions that could alter the recommendation.',
    'Make completion criteria observable for the maintainer.',
    'Show important failure cases and how the result should be validated.',
])
def test_delivery_constraints_do_not_add_capabilities(catalog, closing):
    result = route_request(catalog, 'Inspect the repository. ' + closing)
    assert result['selected'] == ['solforge-workflow-codebase']
    assert len(result['stages']) == 1
