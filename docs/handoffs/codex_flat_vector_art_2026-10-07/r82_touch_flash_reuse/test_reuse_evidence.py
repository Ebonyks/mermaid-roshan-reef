import unittest,copy
from evidence_rules import validate_trial,validate_lane,SOURCE,CANDIDATE,ASSET
class Evidence(unittest.TestCase):
 def sample(self,mode=CANDIDATE):
  blue={'class':'Panel','active_style_class':'StyleBoxFlat','size':[110.0,110.0],'corner_radius':55,'rgba':[1,.95,.5,.5],'native_rect':[45.,65.,110.,110.],'instance_id':7,'modulate_alpha':1.0,'candidate':{}}
  a=dict(blue,modulate_alpha=.95);c={'texture_path':ASSET,'source_dimensions':[512.,512.],'rect_size':[110.,110.],'native_rect':blue['native_rect'],'modulate_rgba':[1,1,1,1],'self_modulate_rgba':[1,1,1,1],'parent_panel_alpha':.95,'parent_is_original_panel':True,'mouse_filter_ignored':True,'whole_source_bitmap':True,'original_flat_style_retired':True,'production_integration':False,'visual_override_only':True}
  if mode==CANDIDATE:a.update(active_style_class='StyleBoxEmpty',candidate=c)
  return {'mode':mode,'source_blueprint':blue,'onset':a,'decay':dict(a,modulate_alpha=.4),'instance_id':7,'native_point':[100.,120.],'actual_input':True,'source_controller_unchanged':True,'freed':True,'visual_override':mode==CANDIDATE}
 def bad(self,key,value):
  t=self.sample();t['onset']['candidate'][key]=value
  with self.assertRaises(ValueError):validate_trial(t)
 def test_original(self):self.assertTrue(validate_trial(self.sample(SOURCE)))
 def test_candidate(self):self.assertTrue(validate_trial(self.sample()))
 def test_wrong_bitmap(self):self.bad('texture_path','res://wrong.png')
 def test_wrong_dimensions(self):self.bad('source_dimensions',[256,512])
 def test_wrong_rectangle(self):self.bad('native_rect',[0,0,80,110])
 def test_recolor(self):self.bad('modulate_rgba',[1,.5,1,1])
 def test_wrong_parent(self):self.bad('parent_is_original_panel',False)
 def test_input_owner(self):self.bad('mouse_filter_ignored',False)
 def test_flat_residue(self):self.bad('original_flat_style_retired',False)
 def test_production_claim(self):self.bad('production_integration',True)
 def test_no_fade(self):
  t=self.sample();t['decay']['modulate_alpha']=1.0
  with self.assertRaises(ValueError):validate_trial(t)
 def test_no_free(self):
  t=self.sample();t['freed']=False
  with self.assertRaises(ValueError):validate_trial(t)
 def test_wrong_source_blueprint(self):
  t=self.sample();t['source_blueprint']['rgba']=[0,0,0,1]
  with self.assertRaises(ValueError):validate_trial(t)
 def test_candidate_context_credit(self):
  with self.assertRaises(ValueError):validate_lane(CANDIDATE,'BOUNDED_CURRENT_ORIGINAL_TOUCH_FLASH')
if __name__=='__main__':unittest.main(verbosity=2)
