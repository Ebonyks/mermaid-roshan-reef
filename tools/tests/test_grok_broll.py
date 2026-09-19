import copy
import unittest
from tools import validate_grok_broll as v

class BrollTests(unittest.TestCase):
    def setUp(self):
        self.packet=v.DEFAULT
        self.plan=v.read(self.packet/'shots/SHOT-BATH-TUB-B01/PLAN.json')
        self.parent=v.read(self.packet/'source_plans/SHOT-BATH-TUB/CARD.json')
        self.prompt=(self.packet/'shots/SHOT-BATH-TUB-B01/PROMPT.txt').read_bytes()
    def bad(self,change):
        p=copy.deepcopy(self.plan);change(p)
        self.assertTrue(v.validate_plan(p,self.parent,self.prompt))
    def test_valid_planning_control(self):self.assertEqual([],v.validate_plan(self.plan,self.parent,self.prompt))
    def test_full_packet(self):self.assertEqual([],v.validate(self.packet)['errors'])
    def test_not_generation_ready(self):self.assertTrue(v.validate(self.packet,True)['errors'])
    def test_wrong_pair(self):self.bad(lambda p:p.update(parent_shot_id='SHOT-BATH-SINK'))
    def test_state_reset(self):self.bad(lambda p:p['room_state'].update(sink='dirty'))
    def test_premature_drain(self):self.bad(lambda p:p['end_room_state'].update(drain='open_empty'))
    def test_extra_character(self):self.bad(lambda p:p['exact_cast'].append('CHAR-DADDY'))
    def test_wrong_count(self):self.bad(lambda p:p['exact_prop_counts'].update(tubs=2))
    def test_hold_cannot_change(self):self.bad(lambda p:p.update(inherited_hold=True))
    def test_attempt_reset(self):self.bad(lambda p:p['attempt_lineage'].update(reset_allowed=True))
    def test_consumed_attempts(self):self.bad(lambda p:p['attempt_lineage'].update(attempts_used=0))
    def test_drop_dependency(self):self.bad(lambda p:p.update(depends_on=[]))
    def test_mirrored_room(self):self.bad(lambda p:p['camera'].update(mirror_allowed=True))
    def test_zoom_not_angle(self):self.bad(lambda p:p['camera'].update(digital_crop_is_new_angle=True))
    def test_second_camera_move(self):self.bad(lambda p:p['camera'].update(move_count=2))
    def test_unseen_wall(self):self.bad(lambda p:p['camera'].update(unseen_reverse_wall_allowed=True))
    def test_board_not_pixels(self):self.bad(lambda p:p['board'].update(used_as_generation_pixels=True))
    def test_fake_opening_approval(self):self.bad(lambda p:p['suggested_bindings'][0].update(owner_approved=True))
    def test_extra_binding(self):self.bad(lambda p:p['suggested_bindings'].extend([{'id':'IMAGE_4'},{'id':'IMAGE_5'}]))
    def test_gap_in_frame_spans(self):self.bad(lambda p:p['beats'][1].update(frames_half_open=[20,78]))
    def test_replay_action(self):self.bad(lambda p:p['editorial'].update(replace_span_not_append_repeat=False))
    def test_fabricated_measured_timecodes(self):self.bad(lambda p:p['editorial'].update(mapping_basis='MEASURED'))
    def test_missing_sound(self):self.assertTrue(v.validate_plan(self.plan,self.parent,self.prompt.rsplit(b'Sound:',1)[0]))
    def test_modified_prompt_hash(self):self.assertTrue(v.validate_plan(self.plan,self.parent,self.prompt+b'changed'))

if __name__=='__main__':unittest.main()
