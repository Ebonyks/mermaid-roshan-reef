import unittest
from pathlib import Path

from tools.build_day_one_grok_fourth_pass import PACKET, EXPECTED, frame_plan, read


class FourthPassTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.shots={s['shot']:s for s in read(PACKET/'SHOT_DESIGN.json')['shots']}

	def test_only_intended_jobs(self):
		self.assertEqual(list(self.shots),EXPECTED)
		self.assertIn('C11-S02',self.shots)
		self.assertNotIn('C09-S04',self.shots)
		self.assertNotIn('C10-S02',self.shots)
		self.assertNotIn('C01-S02',self.shots)
		for key in ['C13-S01','C13-S02','C13-S03']:self.assertNotIn(key,self.shots)

	def test_all_target_frames_exist_once(self):
		for shot in self.shots.values():
			plan=frame_plan(shot)
			self.assertEqual([f['target_frame'] for f in plan['frames']],list(range(shot['duration_s']*24)))

	def test_visual_slate_has_current_castle_and_suds_openings(self):
		visuals=read(PACKET/'VISUAL_SELECTIONS.json')
		self.assertEqual(list(visuals),EXPECTED)
		for selected in visuals.values():
			self.assertTrue((PACKET/selected['first_frame']).is_file())
			self.assertTrue((PACKET/selected['storyboard']).is_file())
			self.assertEqual(selected['human_decision'],'pending')
		self.assertIn('OWNER_C11_S01_LAYOUT_candidate02',visuals['C11-S01']['first_frame'])
		self.assertIn('PORTAL_APPROACH_candidate02',visuals['C11-S02']['first_frame'])
		self.assertIn('SUDS_OPENING',visuals['C13-S04']['first_frame'])
		self.assertIn('SUDSY_OPENING_candidate02',visuals['C13-S05']['first_frame'])

	def test_no_target_is_accepted_generation(self):
		for shot in self.shots.values():
			for frame in frame_plan(shot)['frames']:
				self.assertIsNone(frame['candidate_sha256'])
				self.assertEqual(frame['accepted_neighbors'],[])
				self.assertFalse(frame['delivery_accepted'])

	def test_holds_are_declared_not_hidden_motion(self):
		for key,shot in self.shots.items():
			frames=frame_plan(shot)['frames']
			self.assertTrue(all(f['action_state']=='intentional_hold' for f in frames[-18:]))
			if key not in ['C09-S03','C11-S03']:self.assertTrue(any(f['action_state']=='action' for f in frames[:-18]))

	def test_c01_daddy_not_rumi(self):
		for key in ['C01-S04']:
			self.assertIn('Daddy',self.shots[key]['end_state'])
			self.assertNotIn('Rumi',self.shots[key]['end_state'])

	def test_team_finish_is_shared_and_localized(self):
		prompt=self.shots['C13-S04']['prompt']
		for name in ['Roshan','Daddy','Eagle','Rumi']:self.assertIn(name,prompt)
		self.assertEqual(self.shots['C13-S04']['camera_move_count'],1)
		self.assertIn('overlap',prompt)
		self.assertIn('room dust',prompt)
		self.assertIn('behind the gold ferrule',prompt)
		self.assertIn('cyan-white bristles face and touch Puff',prompt)
		self.assertIn('suds',prompt)
		self.assertIn('withdraws the bristles with grip unchanged',self.shots['C13-S05']['prompt'])
		for key in ['C13-S04','C13-S05']:
			self.assertLess(len(self.shots[key]['prompt'].split()),250)
			self.assertTrue(all('grip' in f['reconstruction_prompt'] or 'both hands around the handle' in f['reconstruction_prompt'] for f in frame_plan(self.shots[key])['frames']))

	def test_missing_shots_have_no_fabricated_source(self):
		for key in ['C01-S04','C03-S02','C06-S05','C13-S05']:
			self.assertIsNone(self.shots[key]['original_source'])
			self.assertEqual(self.shots[key]['weak_source_frames'],[])

	def test_reveal_allows_only_declared_new_friend(self):
		frames=frame_plan(self.shots['C13-S05'])['frames']
		self.assertIn('No baby is visible',frames[0]['reconstruction_prompt'])
		self.assertIn('one tiny rainbow friend',frames[132]['reconstruction_prompt'])
		self.assertNotIn('No HUD, text or additional characters',frames[24]['reconstruction_prompt'])
		self.assertIn('undeclared characters',frames[24]['reconstruction_prompt'])

	def test_suds_build_then_recede_before_friend(self):
		self.assertEqual(self.shots['C13-S04']['duration_s'],5)
		self.assertEqual(self.shots['C13-S05']['duration_s'],8)
		self.assertIn('covered in suds',self.shots['C13-S04']['end_state'])
		phases=self.shots['C13-S05']['phases']
		self.assertEqual([p['range'] for p in phases],[[0,24],[24,96],[96,132],[132,156],[156,174],[174,192]])
		self.assertIn('final gentle wipe/rinse contacts',phases[2]['instruction'])
		self.assertIn('no tool has withdrawn yet',phases[2]['instruction'])
		self.assertIn('peek',phases[3]['instruction'])
		self.assertIn('low front-left',self.shots['C13-S04']['camera'])
		self.assertIn('elevated front-right',self.shots['C13-S05']['camera'])

	def test_hall_uses_live_redraw_and_open_arch(self):
		for key in ['C11-S01','C11-S02']:
			shot=self.shots[key]
			self.assertTrue(any('castle_main_hall_redraw_2026-08-03' in p for p in shot['game_references']))
			self.assertFalse(any('main_hall_2screen' in p for p in shot['game_references']))
			self.assertIn('open',shot['end_state'])
			self.assertNotIn('door remains closed',shot['prompt'])

	def test_prompt_ends_with_sound(self):
		for shot in self.shots.values():
			self.assertTrue(shot['prompt'].splitlines()[-1].startswith('Sound:'))
			for forbidden in ['sha256','ARCHIVE_COMPLETE','DELIVERY_ACCEPTED','PROPOSED owner']:
				self.assertNotIn(forbidden,shot['prompt'])

	def test_invalid_phase_gap_is_rejected(self):
		import copy
		shot=copy.deepcopy(self.shots['C01-S04']);shot['phases'][1]['range'][0]+=1
		with self.assertRaises(AssertionError):frame_plan(shot)
		shot=copy.deepcopy(self.shots['C13-S05']);shot['phases'][5]['range'][0]+=1
		with self.assertRaises(AssertionError):frame_plan(shot)

	def test_reveal_removes_giant_before_final_hold(self):
		shot=self.shots['C13-S05']
		self.assertIn('Giant Puff is gone',shot['prompt'])
		self.assertIn('giant body, face and ears completely',shot['prompt'])
		self.assertIn('two shell-topped side windows',shot['prompt'])
		self.assertIn('exactly four helpers and one happy rainbow friend',shot['prompt'])
		visuals=read(PACKET/'VISUAL_SELECTIONS.json')['C13-S05']
		self.assertIn('ONE_FRIEND_REVEAL',visuals['storyboard'])
		self.assertTrue((PACKET/visuals['endpoint_candidate']).is_file())

	def test_every_game_authority_is_in_archive(self):
		from tools.build_day_one_grok_fourth_pass import digest
		root=Path(__file__).resolve().parents[2]
		for shot in self.shots.values():
			card=read(PACKET/f"shots/D1-{shot['shot']}/SHOT_PACKET.json")
			refs={r['source_path']:r['path'] for r in card['game_asset_comparison']}
			for path in shot['game_references']:
				self.assertIn(path,refs)
				copy=PACKET/refs[path]
				self.assertTrue(copy.is_file(),path)
				if (root/path).is_file():self.assertEqual(digest(root/path),digest(copy))


if __name__=='__main__':unittest.main()
