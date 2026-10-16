from pathlib import Path
import unittest,json,copy
from evidence_rules import validate_lane,validate_card
P=Path(__file__).resolve().parent
class EvidenceSeparation(unittest.TestCase):
 def card(self):return copy.deepcopy(json.loads((P/'CANDIDATE_GEOMETRY.json').read_text(encoding='utf-8'))['measurements'][0])
 def test_recorded_card_contract(self):self.assertTrue(validate_card(self.card()))
 def test_prototype_cannot_gain_source_context(self):
  with self.assertRaises(ValueError):validate_lane('LOCAL_NONRUNTIME_STAR_REUSE','BOUNDED_CURRENT_ORIGINAL_CUE_INPUT')
 def test_unknown_mode_not_silently_accepted(self):
  with self.assertRaises(ValueError):validate_lane('accepted','BOUNDED_CURRENT_ORIGINAL_CUE_INPUT')
 def test_rgb_recolor_rejected(self):
  row=self.card();row['rgba'][0]=.7
  with self.assertRaises(ValueError):validate_card(row)
 def test_leftover_polygon_rejected(self):
  row=self.card();row['original_pointer_child_count']=1
  with self.assertRaises(ValueError):validate_card(row)
 def test_outside_hit_disk_rejected(self):
  row=self.card();row['native_corners'][0][0]+=400
  with self.assertRaises(ValueError):validate_card(row)
 def test_wrong_generic_radius_rejected(self):
  row=self.card();row['consumer']='swing';row['native_hit_radius']=118
  with self.assertRaises(ValueError):validate_card(row)
 def test_production_acceptance_rejected(self):
  row=self.card();row['production_integration']=True
  with self.assertRaises(ValueError):validate_card(row)
if __name__=='__main__':unittest.main(verbosity=2)