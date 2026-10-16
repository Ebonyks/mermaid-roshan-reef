from pathlib import Path
import unittest
P=Path(__file__).resolve().parent
scope={"__file__":str(P/"scan_intro_entry.py"),"__name__":"r77_scan_functions_only"}
text=(P/"scan_intro_entry.py").read_text(encoding="utf-8");exec(compile(text[:text.index("paths=[")],str(P/"scan_intro_entry.py"),"exec"),scope);scan=scope["scan"]
class IntroEntryExtraction(unittest.TestCase):
 def calls(self,body):return scan("extends Node\n"+body,"synthetic.gd")
 def test_headless_if_and_display_else_have_distinct_guards(self):
  c,_,_=self.calls('func f():\n\tif DisplayServer.get_name() == "headless":\n\t\t_build_intro()\n\telse:\n\t\t_build_start_menu()\n');self.assertEqual(c[0]['guards'][0]['kind'],'if_branch');self.assertIn('headless',c[0]['guards'][0]['condition_AST']);self.assertEqual(c[1]['guards'][0]['kind'],'else_branch');self.assertNotIn('headless',c[1]['guards'][0]['condition_AST'])
 def test_nested_condition_retained(self):
  c,_,_=self.calls('func f():\n\tif a:\n\t\tif b:\n\t\t\t_build_intro()\n');self.assertEqual(len(c[0]['guards']),2)
 def test_comment_and_plain_string_not_call(self):
  c,_,_=self.calls('func f():\n\t# _build_intro()\n\tvar s = "_build_intro()"\n');self.assertEqual(c,[])
 def test_definition_not_call(self):
  c,_,_=self.calls('func _build_intro():\n\tpass\n');self.assertEqual(c,[])
 def test_callback_reference_not_invocation(self):
  c,r,_=self.calls('func f():\n\tbutton.pressed.connect(_build_intro)\n');self.assertEqual(c,[]);self.assertEqual(r[0]['name'],'_build_intro')
 def test_other_receiver_retained_not_assumed_Main(self):
  c,_,_=self.calls('func f():\n\tother._build_intro()\n');self.assertIn('other',c[0]['receiver_AST']);self.assertEqual(c[0]['function'],'f')
 def test_reflective_selector_separate_from_direct_call(self):
  c,_,d=self.calls('func f():\n\tobj.call("_build_intro")\n');self.assertEqual(c,[]);self.assertEqual(d[0]['literal_selector_or_payload'],'_build_intro')
 def test_empty_callable_and_payload_stay_raw(self):
  c,_,d=self.calls('func f():\n\tvar empty = Callable()\n\tcb.call("")\n');self.assertEqual(c,[]);self.assertEqual(len(d),2);self.assertTrue(all(x['semantic_classification'].startswith('RAW_SYNTAX_ONLY')for x in d))
 def test_callback_data_not_claimed_selector_closure(self):
  _,_,d=self.calls('func f():\n\tcb.call("_build_intro")\n');self.assertTrue(d[0]['semantic_classification'].startswith('RAW_SYNTAX_ONLY'))
 def test_different_functions_keep_ownership(self):
  c,_,_=self.calls('func a():\n\t_build_intro()\nfunc b():\n\t_build_start_menu()\n');self.assertEqual([x['function']for x in c],['a','b'])
if __name__=="__main__":unittest.main()
