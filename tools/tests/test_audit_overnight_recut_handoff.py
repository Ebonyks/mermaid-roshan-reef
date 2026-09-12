"""Adversarial checks for wrong-cut, stale-map and false-readiness claims."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from audit_overnight_recut_handoff import audit

PACKET=ROOT/'assets_src/cinematics/overnight_recut_repairs_2026-09-12'


class RecutAuditTests(unittest.TestCase):
    def test_real_archive_and_readiness_are_separate(self):
        self.assertEqual(audit(PACKET),[])
        failures=audit(PACKET,True)
        self.assertEqual(len(failures),18)
        self.assertTrue(all('not an executable Imagine packet' in s for s in failures))

    def test_wrong_source_frame_is_detected_even_if_duration_matches(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.as_posix().endswith('shots/R10/SHOT_PACKET.json'):
                value=json.loads(data)
                value['source_events'][0]['source_range']=[1,133]
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            failures=audit(PACKET)
        self.assertTrue(any('source frame map does not match edit' in s for s in failures))

    def test_wrong_overnight_video_is_detected(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.name=='SOURCE_CUT.json':
                value=json.loads(data);value['sha256']='0'*64
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            self.assertIn('wrong overnight cut',audit(PACKET))

    def test_missing_later_bunny_coverage_is_detected(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.as_posix().endswith('shots/R16/SHOT_PACKET.json'):
                value=json.loads(data);value['master_ranges']=[[2943,3014]]
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            self.assertIn('incomplete visible rainbow-bunny coverage',audit(PACKET))

    def test_rejected_eagle_cannot_be_rebound(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.as_posix().endswith('shots/R18/SHOT_PACKET.json'):
                value=json.loads(data)
                value['bindings'][1]['path']='evidence/rejected_identity/90c54412aa_baby_eagle_standing_BABY_EAGLE_STANDING_IDENTITY.png'
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            self.assertIn('R18: rejected Eagle redraw is bound',audit(PACKET))

    def test_missing_daddy_binding_is_rejected(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.as_posix().endswith('shots/R10/SHOT_PACKET.json'):
                value=json.loads(data)
                value['bindings']=[b for b in value['bindings'] if b.get('path')!='references/daddy_generation_preview.jpg']
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            self.assertIn('R10: exact Daddy identity is not bound',audit(PACKET))

    def test_early_reveal_cannot_remove_hidden_little_bunny_lock(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.as_posix().endswith('shots/R09/SHOT_PACKET.json'):
                value=json.loads(data);value['little_bunny_hidden_until_jump']=False
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            self.assertIn('R09: hidden little-bunny start is not locked',audit(PACKET))

    def test_soap_and_big_bunny_form_cannot_be_dropped(self):
        original=Path.read_text
        def changed(path,*args,**kwargs):
            data=original(path,*args,**kwargs)
            if path.as_posix().endswith('shots/R09/SHOT_PACKET.json'):
                value=json.loads(data);value['cleaning_suds_required']=False
                return json.dumps(value)
            return data
        with patch.object(Path,'read_text',changed):
            self.assertIn('R09: recognizable big bunny and visible soapy cleaning required',audit(PACKET))


if __name__=='__main__':unittest.main()
