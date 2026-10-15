import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('domains49',p/'audit_callback_domains.py');A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
def rows(text):return A.Facts(text,'fixture.gd').rows
class CallbackDomainStress(unittest.TestCase):
 def test_comment_and_string_are_not_writes(self):
  self.assertFalse(rows('extends Node\n# ui.world_press_probe = cb\nvar s = "encounter_cancel = cb"\n'))
 def test_member_write_remains_receiver_unproved(self):
  r=rows('extends Node\nfunc f(ui, cb):\n ui.world_press_probe = cb\n');self.assertEqual(r[0]['field'],'world_press_probe');self.assertEqual(r[0]['owner_evidence'],'UNPROVEN_MEMBER_OR_ALIAS')
 def test_bracket_named_write(self):
  r=rows('extends Node\nfunc f(ui, cb):\n ui["world_press_release"] = cb\n');self.assertEqual(r[0]['field'],'world_press_release')
 def test_computed_index_is_not_silently_safe(self):
  r=rows('extends Node\nfunc f(ui, key, cb):\n ui[key] = cb\n');self.assertEqual(r[0]['kind'],'COMPUTED_INDEX_WRITE')
 def test_local_shadow_is_not_owner_field(self):
  r=rows('extends Node\nvar world_press_probe: Callable\nfunc f(world_press_probe: Callable, cb: Callable):\n world_press_probe = cb\n');r=[x for x in r if x['kind']=='NAMED_WRITE'];self.assertEqual(r[0]['owner_evidence'],'LOCAL_OR_SHADOWED_SYMBOL')
 def test_class_field_assignment(self):
  r=rows('extends Node\nvar world_press_probe: Callable\nfunc f(cb: Callable):\n world_press_probe = cb\n');r=[x for x in r if x['kind']=='NAMED_WRITE'];self.assertEqual(r[0]['owner_evidence'],'CLASS_FIELD')
 def test_alias_write_stays_unproved(self):
  r=rows('extends Node\nfunc f(ui, cb):\n var alias = ui\n alias.encounter_press = cb\n');self.assertEqual(r[0]['owner_evidence'],'UNPROVEN_MEMBER_OR_ALIAS')
 def test_named_native_setter_candidate(self):
  r=rows('extends Node\nfunc f(ui, cb):\n ui.set("encounter_cancel", cb)\n');self.assertTrue(r[0]['selected_field']);self.assertEqual(r[0]['kind'],'PROPERTY_MUTATOR')
 def test_nodepath_nested_property_retains_candidate(self):
  r=rows('extends Node\nfunc f(ui, cb):\n ui.set_indexed(NodePath("child:encounter_motion"), cb)\n');self.assertTrue(r[0]['selected_field'])
 def test_unknown_setter_name_retains_risk(self):
  r=rows('extends Node\nfunc f(ui, key, cb):\n ui.set_deferred(key, cb)\n');self.assertIsNone(r[0]['property']);self.assertIsNone(r[0]['selected_field'])
 def test_object_dispatch_setter_indirection_retained(self):
  r=rows('extends Node\nfunc f(ui, cb):\n ui.call("set", "encounter_press", cb)\n');self.assertEqual(r[0]['kind'],'DISPATCH_INVOCATION_CANDIDATE');self.assertEqual(r[0]['first_argument_literal'],'set');self.assertFalse(r[0]['target_method_inferred'])
 def test_callable_payload_not_promoted_to_method_edge(self):
  r=rows('extends Node\nfunc f(cb: Callable):\n cb.call("world_press_probe")\n');self.assertEqual(r[0]['first_argument_literal'],'world_press_probe');self.assertFalse(r[0]['target_method_inferred'])
 def test_stored_setter_reference_retained(self):
  r=rows('extends Node\nfunc f(ui):\n var cb = ui.set\n');self.assertEqual(r[0]['kind'],'MUTATOR_METHOD_REFERENCE')
 def test_callable_native_setter_constructor_retained(self):
  r=rows('extends Node\nfunc f(ui):\n var cb = Callable(ui, "set")\n');self.assertEqual(r[0]['kind'],'CALLABLE_MUTATOR_OR_COMPUTED_SELECTOR')
 def test_computed_constructor_selector_retained(self):
  r=rows('extends Node\nfunc f(ui, name):\n var cb = Callable(ui, name)\n');self.assertIsNone(r[0]['selector_literal'])
 def test_api_empty_reset_is_a_caller(self):
  r=rows('extends Node\nfunc f(ui):\n ui.set_encounter_controls()\n');self.assertEqual(r[0]['arguments_AST'],[])
 def test_overridden_mutator_not_certified_native(self):
  r=rows('extends Node\nfunc set(a, b):\n pass\nfunc f(cb):\n set("encounter_press", cb)\n');self.assertIn('override',r[0]['scope_limit'])
 def test_stable_ids_unique_across_repeated_sites(self):
  s='extends Node\nfunc f(ui, cb):\n ui.encounter_press = cb\n ui.encounter_press = cb\n';a=rows(s);b=rows(s);self.assertEqual(a,b);self.assertEqual(len({x['id'] for x in a}),2)
if __name__=='__main__':unittest.main()
