import unittest
from scan_promenade_owner import scan
class OwnerExtraction(unittest.TestCase):
 def audit(self,text):return scan(text,'fixture.gd')
 def test_wall_array_declaration(self):
  d=self.audit('var wall_pics: Array = []\n');self.assertEqual(d['field_references'][0]['name'],'wall_pics')
 def test_wall_append_owner(self):
  d=self.audit('func _hang_portrait():\n\twall_pics.append({"art":"p_slide"})\n');self.assertEqual(d['field_references'][0]['function'],'_hang_portrait')
 def test_member_clear_is_recorded(self):
  d=self.audit('func _build_pearl_castle():\n\tm.wall_pics = []\n');self.assertEqual(len(d['field_references']),1);self.assertIn('assnmnt_expr',d['field_references'][0]['ancestor_kinds'])
 def test_comment_and_string_not_caller(self):
  d=self.audit('func f():\n\t# _build_pearl_castle()\n\tvar text = "_hang_portrait()"\n');self.assertEqual(d['named_calls'],[])
 def test_selector_guard_retained(self):
  d=self.audit('func _tick_level2():\n\tif phase == "promenade":\n\t\t_touch_open_picture(0)\n');self.assertIn('promenade',d['named_calls'][0]['guards'][0]['condition_AST'])
 def test_no_inferred_call_from_reference(self):
  d=self.audit('func f():\n\tvar cb = _enter_level2_now.bind()\n');self.assertEqual(d['named_calls'],[]);self.assertEqual(d['target_references'][0]['name'],'_enter_level2_now')
 def test_reflected_object_selector(self):
  d=self.audit('func f():\n\tcall_deferred("_build_pearl_castle", origin)\n');self.assertEqual(len(d['literal_reflective_calls']),1)
 def test_callable_payload_stays_ambiguous(self):
  d=self.audit('func f():\n\tcb.call("_build_pearl_castle")\n');self.assertEqual(d['literal_reflective_calls'],[]);self.assertEqual(len(d['ambiguous_literal_dispatch_arguments']),1)
 def test_dynamic_property_set_retained(self):
  d=self.audit('func f():\n\tset("wall_pics", [])\n');self.assertEqual(len(d['field_literal_property_access']),1)
 def test_function_scope_excludes_next_header(self):
  d=self.audit('func _enter_level2_now():\n\tpass\nfunc other():\n\tpass\n');self.assertNotIn('func other',d['function_bodies'][0]['text'])
if __name__=='__main__':unittest.main(verbosity=2)