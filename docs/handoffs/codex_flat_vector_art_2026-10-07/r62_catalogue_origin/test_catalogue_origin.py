import importlib.util,json,subprocess,unittest
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[3];s=importlib.util.spec_from_file_location('catalogue_origin62',P/'audit_catalogue_origin.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
class OriginTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.text=(P/'historical_source/build_review_packet.py.txt').read_text(encoding='utf-8');c.recipe=M.constant_recipe(c.text);c.cat=json.loads(M.git(R,'show',M.D+':design/reference/games.json'));c.main=M.git(R,'show',M.D+':scripts/main.gd').decode('utf-8-sig');c.pause=M.git(R,'show',M.D+':scripts/pause_menu.gd').decode('utf-8-sig');c.collection=M.git(R,'show',M.D+':scripts/collection_system.gd').decode('utf-8-sig')
 def test_original_recipe_has_explicit_labels(self):
  self.assertEqual(len(self.recipe['ui']),12);self.assertEqual(self.recipe['game_prefix'],'game.');self.assertEqual(self.recipe['game_id_expression'],"'game.' + g['id']")
 def test_changed_prefix_is_rejected(self):
  with self.assertRaises(AssertionError):M.constant_recipe(self.text.replace("'game.'+g['id']","'route.'+g['id']"))
 def test_unknown_expression_is_rejected(self):
  with self.assertRaises(AssertionError):M.constant_recipe(self.text.replace("'game.'+g['id']","'game.'+g['id'].upper()"))
 def test_duplicate_ids_are_not_merged(self):
  cat={'games':[{'id':'critters','name':'a','family':'system'},{'id':'critters','name':'b','family':'minigame'}]}
  with self.assertRaises(AssertionError):M.reconstruct(self.recipe,'',cat,[])
 def test_comment_is_not_a_stage_row(self):
  rows=M.reconstruct({'ui':[],'game_prefix':'game.','stage_pattern':M.STAGE_PATTERN},'# ["fake", "Fake", "module"]\n',{'games':[]},[]);self.assertEqual(rows,[])
 def test_catalogue_label_does_not_become_dispatch_proof(self):
  r=M.reconstruct({'ui':[],'game_prefix':'game.','stage_pattern':M.STAGE_PATTERN},'',{'games':[{'id':'critters','name':'Critter Book collection','family':'system','sources':['scripts/collection_system.gd'],'host':['scripts/main.gd']}]},[])[0];self.assertEqual(r['id'],'game.critters');self.assertEqual(r['origin_kind'],'REFERENCE_GAME_CATALOGUE_LABEL');self.assertNotIn('runtime_game_value',r)
 def test_current_exact_book_binding_stays_partial(self):
  b=M.bind_critter(self.cat,self.main,self.pause,self.collection);self.assertTrue(b['partial_only']);self.assertFalse(b['acquisition_closed']);self.assertFalse(b['normal_route_closed']);self.assertIsNone(b['QA11'])
 def test_same_display_name_wrong_module_rejected(self):
  c=json.loads(json.dumps(self.cat));next(x for x in c['games']if x['id']=='critters')['sources']=['scripts/wardrobe_ui.gd']
  with self.assertRaises(AssertionError):M.bind_critter(c,self.main,self.pause,self.collection)
 def test_wrong_current_callback_rejected(self):
  with self.assertRaises(AssertionError):M.bind_critter(self.cat,self.main,self.pause.replace('m._collection_ref().open_book()','m._open_stickers()'),self.collection)
 def test_changed_current_preload_rejected(self):
  with self.assertRaises(AssertionError):M.bind_critter(self.cat,self.main.replace('preload("res://scripts/collection_system.gd")','preload("res://scripts/wardrobe_ui.gd")'),self.pause,self.collection)
 def test_synthetic_game_assignment_cannot_bind_alias(self):
  with self.assertRaises(AssertionError):M.bind_critter(self.cat,self.main,self.pause,self.collection.replace('func open_book() -> void:','func open_book() -> void:\n\tm.game = "critters"'))
 def test_new_navigation_token_rejected(self):
  with self.assertRaises(AssertionError):M.bind_critter(self.cat,self.main,self.pause,self.collection.replace('m._navigation_push("critter_book", self,','m._navigation_push("other_book", self,'))
if __name__=='__main__':unittest.main()
