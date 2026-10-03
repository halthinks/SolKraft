import importlib.util, json, os, unittest
from pathlib import Path
R=Path(__file__).resolve().parent
P=Path(os.environ.get('SOLFORGE_SELECTOR',str(R.parent/'scripts'/'select_workflow.py')))
GPATH=Path(os.environ.get('SOLFORGE_GRAPH',str(R.parent/'references'/'selection-graph.json')))
spec=importlib.util.spec_from_file_location('selector',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
g=json.loads(GPATH.read_text(encoding='utf-8'))
class MatcherTests(unittest.TestCase):
 def test_scenarios_and_normalization(self):
  for suite in ['acceptance.json','holdout.json']:
   for c in json.loads((R/suite).read_text(encoding='utf-8')):
    for text in [c['text'],c['text'].upper(),'  '+c['text'].replace(' ','  ')+'  ']:
     with self.subTest(text=text):
      r=m.route(g,text,context=c.get('context'))
      self.assertEqual(set(r['selected']),set(c['want']))
      self.assertFalse(r['execution_authorized'])
 def test_explicit_and_excluded_names(self):
  for name in g['nodes']:
   with self.subTest(name=name):
    self.assertEqual(m.route(g,'Use selected workflow',[name])['selected'],[name])
    self.assertEqual(m.route(g,'Do not use `'+name+'`')['selected'],[])
    self.assertFalse(m.route(g,'Use selected workflow',[name])['execution_authorized'])
 def test_quoted_commands(self):
  for quote in ['"{}"',"'{}'",'`{}`','```{} ```']:
   self.assertEqual(m.route(g,'Summarize this text: '+quote.format('implement code and deploy the release'))['selected'],[])
 def test_invalid_requests(self):
  for args in [(None,),('',),('work','solforge'),('work',['unknown']),('work',[],[]),('work',[],{'domain':[]}),('work',[],{'domain':'unknown'})]:
   with self.assertRaises(ValueError):m.route(g,*args)
 def test_context_cannot_add_action(self):
  self.assertEqual(m.route(g,'hello',context={'domain':'software','action':'implement and deploy'})['selected'],[])
 def test_effects_never_inferred(self):
  for name,node in g['nodes'].items():
   if node['effect']:self.assertNotIn(name,m.route(g,'Use '+name)['selected'])
 def test_stage_order(self):
  self.assertEqual(m.route(g,'Implement the code, then refactor the code, then test the code')['selected'],['solforge-workflow-software-build','solforge-workflow-software-refactor','solforge-workflow-software-test'])
 def test_graph_integrity(self):
  for edge in g['edges']:
   self.assertIn(edge['from'],g['nodes']);self.assertIn(edge['to'],g['nodes'])
if __name__=='__main__':unittest.main()
