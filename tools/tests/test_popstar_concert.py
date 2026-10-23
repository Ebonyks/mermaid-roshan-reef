"""Mutation tests for the musical score contract, independent of runtime judge."""
import copy,json,sys,unittest,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import build_popstar_concert as concert
class ScoreTests(unittest.TestCase):
 def setUp(self):
  self.score=json.loads((ROOT/concert.SCORE).read_text())
  self.sections=[dict(s,cues=concert.emit(s)) for s in self.score['sections']]
 def test_final_child_crash_cannot_be_replaced_by_passive_call(self):
  self.sections[-1]['cues'][-1]['role']='call'
  with self.assertRaises(AssertionError):concert.validate(self.score,self.sections)
 def test_calls_and_answers_must_match_instrument_and_bar(self):
  cue=next(c for c in self.sections[1]['cues'] if c['role']=='answer')
  cue['target']=(cue['target']+1)%3
  with self.assertRaises(AssertionError):concert.validate(self.score,self.sections)
 def test_overlapping_windows_rejected_even_on_musical_grid(self):
  child=self.sections[2]['cues'];child[1]['beat']=child[0]['beat']+1
  with self.assertRaises(AssertionError):concert.validate(self.score,self.sections)
 def test_first_two_post_countin_beats_cannot_request_input(self):
  self.sections[0]['cues'][0]['beat']=5
  with self.assertRaises(AssertionError):concert.validate(self.score,self.sections)
 def test_mic_is_only_a_crowd_lead_target(self):
  self.sections[2]['cues'][0]['target']=3
  with self.assertRaises(AssertionError):concert.validate(self.score,self.sections)
 def test_checkout_newlines_do_not_change_source_authority(self):
  with tempfile.TemporaryDirectory() as folder:
   a=Path(folder)/'lf.py';b=Path(folder)/'crlf.py'
   a.write_bytes(b'a=1\n');b.write_bytes(b'a=1\r\n')
   self.assertEqual(concert.source_sha(a),concert.source_sha(b))
   self.assertNotEqual(concert.sha(a),concert.sha(b))
 def test_original_score_and_media_are_bound(self):
  concert.build(check=True)
if __name__=='__main__':unittest.main()
