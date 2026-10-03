import importlib.util,json,unittest,os
from pathlib import Path
R=Path(__file__).parent
P=Path(os.environ.get('SOLFORGE_TEST_ROOT',str(R/'staged')))/'solforge'/'scripts'/'select_workflow.py'
spec=importlib.util.spec_from_file_location('selector',P)
selector=importlib.util.module_from_spec(spec);spec.loader.exec_module(selector)
G=json.loads((P.parent.parent/'references'/'selection-graph.json').read_text(encoding='utf-8'))
class SelectionTests(unittest.TestCase):
 def selected(self,text,explicit=None):return selector.route(G,text,explicit or [])['selected']
 def test_research(self):self.assertIn('sol-search',self.selected('Research current database options with primary sources'))
 def test_debug(self):self.assertIn('solforge-workflow-software-diagnose',self.selected('Debug why saving a document crashes the app'))
 def test_build(self):self.assertIn('solforge-workflow-software-build',self.selected('Implement CSV export in this repository'))
 def test_proof(self):self.assertIn('solforge-workflow-math-prove',self.selected('Prove this theorem rigorously'))
 def test_review(self):self.assertIn('solforge-workflow-writing-review',self.selected('Review and revise this draft article'))
 def test_security(self):self.assertIn('solforge-workflow-software-security',self.selected('Audit this API for security vulnerabilities'))
 def test_literature(self):self.assertIn('solforge-workflow-science-literature',self.selected('Conduct a scientific literature review of these papers'))
 def test_data(self):self.assertIn('solforge-workflow-data-validate',self.selected('Validate this dataset for missing values and leakage'))
 def test_port(self):self.assertIn('solforge-workflow-software-native-port',self.selected('Port this Linux app to Windows'))
 def test_mvp(self):self.assertIn('solforge-workflow-software-mvp-create',self.selected('Build an MVP with a working vertical slice'))
 def test_readme(self):self.assertIn('solforge-workflow-whitepaper-to-readme',self.selected('Turn this whitepaper into a README'))
 def test_market(self):self.assertIn('solforge-workflow-business-market',self.selected('Research the market and competitors for this product'))
 def test_claims(self):self.assertIn('solforge-workflow-writing-factcheck',self.selected('Fact-check the claims in this article'))
 def test_legal(self):self.assertIn('solforge-workflow-legal-compare',self.selected('Compare these laws across jurisdictions'))
 def test_engineering(self):self.assertIn('solforge-workflow-engineering-requirements',self.selected('Define engineering requirements and interfaces'))
 def test_continuation(self):
  result=selector.route(G,'Implement CSV export in this repository')
  self.assertTrue(any(e['to']=='solforge-build' for e in result['followups']))
  result=selector.route(G,'Execute this implementation',['solforge-build'])
  self.assertTrue(any(e['to']=='solforge-result-validator' for e in result['followups']))
 def test_no_effects(self):
  for text in ['Draft an email; do not send it','Explain how deployment works','Compare these repositories; should we merge this?','Document how to delete records safely','Publish a report next month, but only draft it now']:
   self.assertFalse(any(G['nodes'][s]['effect'] for s in self.selected(text)),text)
 def test_effects_are_explicit_only(self):
  self.assertFalse(any(G['nodes'][s]['effect'] for s in self.selected('Deploy this release')))
  r=selector.route(G,'Deploy this release',['solforge-workflow-consequential-deploy'])
  self.assertEqual(r['execution_authorized'],False)
 def test_ordinary(self):self.assertEqual(self.selected('What time is it?'),[])
 def test_prompt_is_not_execution(self):self.assertIn('solforge-prompt',self.selected('Write a prompt for researching a codebase'))
 def test_every_skill_reachable(self):
  self.assertGreater(len(G['nodes']), 100)
  self.assertNotIn('solforge-run-ultra', G['nodes'])
  self.assertNotIn('solforge-prompt-ultra', G['nodes'])
  for name in G['nodes']:self.assertIn(name,self.selected('Use the selected workflow',[name]))
 def test_unknown_rejected(self):
  with self.assertRaises(ValueError):self.selected('hello',['does-not-exist'])
 def test_edges_resolve(self):
  for e in G['edges']:self.assertIn(e['from'],G['nodes']);self.assertIn(e['to'],G['nodes'])
 def test_no_duplicate_selection(self):
  r=self.selected('Research, compare, implement and test this repository');self.assertEqual(len(r),len(set(r)))
 def test_plan_paths_exist(self):
  for n in G['nodes'].values():self.assertTrue((P.parent.parent/n['path']).resolve().is_file(),n['path'])
if __name__=='__main__':unittest.main()
