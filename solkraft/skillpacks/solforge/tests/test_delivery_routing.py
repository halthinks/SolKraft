import importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parent.parent
s=importlib.util.spec_from_file_location('selector',R/'scripts/select_workflow.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
g=json.loads((R/'references/selection-graph.json').read_text())
class DeliveryRoutingTests(unittest.TestCase):
 def test_delivery_scenarios(self):
  for c in json.loads((R/'tests/delivery-routing.json').read_text()):
   for text in [c['text'],c['text'].upper(),'Could you '+c['text']]:
    with self.subTest(text=text):
     result=m.route(g,text,context=c.get('context'))
     self.assertEqual(result['selected'],c['want'])
     self.assertFalse(result['execution_authorized'])
 def test_stage_is_not_authority(self):
  for text in ['hello','Deploy this release','Merge this PR','Send an email','Do not run the release gate']:
   result=m.route(g,text,context={'stage':'repository-release-gate'})
   self.assertEqual(result['selected'],[])
   self.assertFalse(result['execution_authorized'])
   self.assertFalse(any(g['nodes'][x]['effect'] for x in result['selected']))
 def test_invalid_stage(self):
  for stage in ['deploy',[],{}]:
   with self.assertRaises(ValueError):m.route(g,'work',context={'stage':stage})
if __name__=='__main__':unittest.main()
