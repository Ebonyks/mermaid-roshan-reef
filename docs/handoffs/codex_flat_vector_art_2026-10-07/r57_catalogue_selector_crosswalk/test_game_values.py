import unittest
from audit_game_values import Facts
class OwnershipTests(unittest.TestCase):
 def facts(self,body,head='class_name ReefMain\nextends Node\nvar game := ""\n'):
  return Facts(head+body,'fixture.gd').rows
 def vals(self,body,head='class_name ReefMain\nextends Node\nvar game := ""\n'):
  return [r['literal_string_value']for r in self.facts(body,head)if r['full_literal_write']]
 def test_main_literal(self):self.assertEqual(self.vals('func f():\n\tgame = "fetch"\n'),['','fetch'])
 def test_empty(self):self.assertEqual(self.vals('func f():\n\tgame = ""\n'),['',''])
 def test_string_comment(self):self.assertEqual(self.vals('func f():\n\tvar s = "game = fake"\n\t# game = "no"\n\tpass\n'),[''])
 def test_parameter_shadow(self):self.assertEqual(self.vals('func f(game: String):\n\tgame = "no"\n'),[''])
 def test_local_shadow(self):self.assertEqual(self.vals('func f():\n\tvar game = "no"\n\tgame = "still_no"\n'),[''])
 def test_future_shadow(self):self.assertEqual(self.vals('func f():\n\tgame = "no"\n\tvar game = "later"\n'),[''])
 def test_self_qualified(self):self.assertEqual(self.vals('func f(game: String):\n\tself.game = "yes"\n'),['','yes'])
 def test_other_class(self):self.assertEqual(self.vals('func f():\n\tgame = "no"\n','extends Node\nvar game = ""\n'),[])
 def test_nested_class(self):self.assertEqual(self.vals('class Inner:\n\tvar game = "inner"\n\tfunc f():\n\t\tgame = "no"\n'),[''])
 def test_typed_member(self):self.assertEqual(self.vals('var m: ReefMain\nfunc f():\n\tm.game = "yes"\n','extends RefCounted\n'),['yes'])
 def test_typed_parameter(self):self.assertEqual(self.vals('func f(m: ReefMain):\n\tm.game = "yes"\n','extends RefCounted\n'),['yes'])
 def test_object_receiver(self):self.assertEqual(self.vals('func f(m: Object):\n\tm.game = "no"\n','extends RefCounted\n'),[])
 def test_alias(self):self.assertEqual(self.vals('var m: ReefMain\nfunc f():\n\tvar a = m\n\ta.game = "no"\n','extends RefCounted\n'),[])
 def test_deep_receiver(self):self.assertEqual(self.vals('func f(m: ReefMain):\n\tm.other.game = "no"\n','extends RefCounted\n'),[])
 def test_dynamic(self):self.assertEqual(self.vals('func f(x):\n\tgame = x\n'),[''])
 def test_compound(self):self.assertEqual(self.vals('func f():\n\tgame += "not_full"\n'),[''])
 def test_concat(self):self.assertEqual(self.vals('func f():\n\tgame = "a" + "b"\n'),[''])
 def test_indexed(self):self.assertEqual(self.vals('func f():\n\tvar d = {}\n\td["game"] = "no"\n'),[''])
 def test_reflective(self):
  rows=self.facts('func f():\n\tset("game", "not_bound")\n');self.assertEqual(sum(r['kind']=='REFLECTIVE_GAME_WRITE_SPELLING_CANDIDATE'for r in rows),1);self.assertEqual([r['literal_string_value']for r in rows if r['full_literal_write']],[''])
 def test_similar_name(self):self.assertEqual(self.vals('func f():\n\tvar game_name = "no"\n'),[''])
 def test_ids_unique(self):
  rows=self.facts('func f():\n\tgame = "a"\n\tgame = "b"\n');self.assertEqual(len({r['id']for r in rows}),3)
 def test_stringname(self):self.assertEqual(self.vals('func f():\n\tgame = &"typed"\n'),['','typed'])
if __name__=='__main__':unittest.main()
