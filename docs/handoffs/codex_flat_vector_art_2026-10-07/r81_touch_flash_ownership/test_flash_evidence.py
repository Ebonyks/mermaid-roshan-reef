import unittest,copy
from evidence_rules import validate_trial,validate_lane
from scan_flash_owner import scan
class FlashEvidence(unittest.TestCase):
 def fixture(self):
  a={'instance_id':7,'class':'Panel','size':[110.0,110.0],'corner_radius':55,'rgba':[1.0,.95,.5,.5],'native_rect':[45.0,65.0,110.0,110.0],'modulate_alpha':.95};b=dict(a,modulate_alpha=.45)
  return {'actual_input':True,'visual_override':False,'source_controller_unchanged':True,'freed':True,'native_point':[100.0,120.0],'instance_id':7,'onset':a,'decay':b}
 def test_source_flash(self):self.assertTrue(validate_trial(self.fixture()))
 def test_recolor(self):
  t=self.fixture();t['onset']['rgba'][0]=.2
  with self.assertRaises(ValueError):validate_trial(t)
 def test_geometry(self):
  t=self.fixture();t['onset']['size']=[220.0,220.0]
  with self.assertRaises(ValueError):validate_trial(t)
 def test_wrong_input(self):
  t=self.fixture();t['native_point']=[300.0,300.0]
  with self.assertRaises(ValueError):validate_trial(t)
 def test_no_fade(self):
  t=self.fixture();t['decay']['modulate_alpha']=1.0
  with self.assertRaises(ValueError):validate_trial(t)
 def test_not_freed(self):
  t=self.fixture();t['freed']=False
  with self.assertRaises(ValueError):validate_trial(t)
 def test_visual_override(self):
  t=self.fixture();t['visual_override']=True
  with self.assertRaises(ValueError):validate_trial(t)
 def test_candidate_cannot_count_as_source(self):
  with self.assertRaises(ValueError):validate_lane('LOCAL_NONRUNTIME_STAR_REUSE','BOUNDED_CURRENT_ORIGINAL_TOUCH_FLASH')
class SourceAST(unittest.TestCase):
 def test_local_named(self):
  d=scan('extends Node\nfunc tap(p):\n\t_flash(p)\n','scripts/touch_ui.gd');self.assertEqual([x['receiver_AST']for x in d['named_calls']],['self'])
 def test_other_receiver_stays_other(self):
  d=scan('extends Node\nfunc tap(p):\n\tother._flash(p)\n','scripts/touch_ui.gd');self.assertIn('other',d['named_calls'][0]['receiver_AST']);self.assertNotEqual(d['named_calls'][0]['receiver_AST'],'self')
 def test_comments_strings_not_calls(self):
  d=scan('extends Node\nfunc tap(p):\n\t# _flash(p)\n\tvar text = "_flash(p)"\n','scripts/touch_ui.gd');self.assertEqual(d['named_calls'],[])
 def test_literal_reflection_separate(self):
  d=scan('extends Node\nfunc tap(p):\n\tcall("_flash",p)\n','scripts/touch_ui.gd');self.assertEqual(d['named_calls'],[]);self.assertEqual(d['literal_reflective_calls'][0]['selector'],'_flash')
 def test_guard_retained(self):
  d=scan('extends Node\nfunc tap(p):\n\tif enabled:\n\t\t_flash(p)\n','scripts/touch_ui.gd');self.assertEqual(len(d['named_calls'][0]['guards']),1)
 def test_invalid_source_fails(self):
  with self.assertRaises(Exception):scan('func ???\n','scripts/touch_ui.gd')
if __name__=='__main__':unittest.main(verbosity=2)
