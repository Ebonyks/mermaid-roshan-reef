import unittest
from scan_game_payload import scan
class PayloadExtraction(unittest.TestCase):
 def audit(self,t):return scan(t,"fixture.gd")
 def test_direct_call_argument(self):
  d=self.audit('func f():\n\t_start_game(fr)\n');self.assertEqual(len(d['named_calls']),1);self.assertEqual(d['named_calls'][0]['argument_AST'],['fr'])
 def test_comments_strings_headers_are_not_calls(self):
  d=self.audit('func _start_game(fr):\n\t# _start_game(fr)\n\tvar s = "_start_game(fr)"\n');self.assertEqual(d['named_calls'],[]);self.assertEqual(d['target_references'],[])
 def test_method_bind_is_ref_not_entry_call(self):
  d=self.audit('func f():\n\tvar cb = _start_game_now.bind(fr)\n');self.assertEqual(d['named_calls'],[]);self.assertEqual(d['target_references'][0]['name'],'_start_game_now')
 def test_reflective_selector_and_payload(self):
  d=self.audit('func f():\n\tcall_deferred("_start_game", fr)\n\tcb.call("_start_game")\n');self.assertEqual(len(d['literal_reflective_calls']),1);self.assertEqual(len(d['ambiguous_literal_dispatch_arguments']),1);self.assertIn('callback payload',d['ambiguous_literal_dispatch_arguments'][0]['classification'])
 def test_callable_first_argument_not_selector(self):
  d=self.audit('func f():\n\tCallable("_start_game")\n\tCallable(self, "_start_game")\n');self.assertEqual(len(d['literal_reflective_calls']),1);self.assertEqual(d['literal_reflective_calls'][0]['method'],'Callable')
 def test_self_reflective_object_selector(self):
  d=self.audit('func f():\n\tself.call_deferred("_start_game", fr)\n');self.assertEqual(len(d['literal_reflective_calls']),1)
 def test_function_extent_excludes_next_header(self):
  d=self.audit('func _start_game(fr):\n\tpass\nfunc following():\n\tpass\n');self.assertNotIn('following',d['function_bodies'][0]['text'])
 def test_other_receivers_preserved(self):
  d=self.audit('func f():\n\tother._start_game(fr)\n');self.assertIn('other',d['named_calls'][0]['receiver_AST'])
 def test_branch_guard_retained(self):
  d=self.audit('func f():\n\tif ready:\n\t\t_start_game(fr)\n');self.assertIn('ready',d['named_calls'][0]['guards'][0]['condition_AST'])
 def test_field_initializer_literal(self):
  d=self.audit('var fairy_fr = {"game": "fairyshoot", "won": true}\n');self.assertEqual(d['declarations'][0]['literal_string_pairs'],{'game':'fairyshoot'})
 def test_local_initializer_only_named_function(self):
  d=self.audit('func other():\n\tvar fr = {"game":"bad"}\nfunc _l2_start_slide():\n\tvar fr = {"game":"race"}\n');self.assertEqual(len(d['declarations']),1);self.assertEqual(d['declarations'][0]['literal_string_pairs']['game'],'race')
 def test_field_indexed_write_is_reference(self):
  d=self.audit('func f():\n\tfairy_fr["game"] = "changed"\n');self.assertEqual(len(d['field_references']),1);self.assertIn('assnmnt_expr',d['field_references'][0]['ancestor_kinds'])
 def test_literal_property_write_retained(self):
  d=self.audit('func f():\n\tset("fairy_fr", {})\n');self.assertEqual(len(d['field_literal_property_access']),1)
 def test_dynamic_selector_not_invented(self):
  d=self.audit('func f():\n\tcall_deferred(selector, fr)\n');self.assertEqual(d['literal_reflective_calls'],[])
 def test_nested_dictionary_not_constant_proof(self):
  d=self.audit('var fairy_fr = {"other":{"game":"fake"}, "game":"fairyshoot"}\n');self.assertEqual(d['declarations'][0]['literal_string_pairs'],{})
if __name__=='__main__':unittest.main(verbosity=2)
