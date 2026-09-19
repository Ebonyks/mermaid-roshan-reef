"""Regression tests for the previously accepted malformed cards."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import validate_v2 as v

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/'canon').mkdir()
        for p in (v.ROOT/'canon').glob('*.json'):
            (self.root/'canon'/p.name).write_bytes(p.read_bytes())
        self.path=self.root/'shots/SHOT-BATH-TUB/CARD.json'
        self.path.parent.mkdir(parents=True)
        self.base=v.read(v.ROOT/'shots/SHOT-BATH-TUB/CARD.json')
        self.prompt=self.path.parent/'PROMPT.txt'
        self.prompt.write_bytes((v.ROOT/'shots/SHOT-BATH-TUB/PROMPT.txt').read_bytes())
    def tearDown(self):self.tmp.cleanup()
    def errors(self,c=None):
        self.path.write_text(json.dumps(self.base if c is None else c),encoding='utf-8')
        errors=[];v.check_card(self.path,errors,self.root);return errors
    def test_valid_blocked_plan(self):self.assertEqual([],self.errors())
    def test_current_all_plans(self):
        e,count,ready=v.validate();self.assertEqual([],e);self.assertEqual((36,0),(count,ready))
    def test_require_ready_fails(self):self.assertTrue(v.validate(require_ready=True)[0])
    def test_blocker_cannot_enable_generation(self):
        self.base.update(generation_allowed=True,opening_approved=True);self.assertTrue(self.errors())
    def test_duplicate_bindings(self):
        self.base['binds'][2]['id']='IMAGE_2';self.assertTrue(self.errors())
    def test_missing_identity_hash(self):
        self.base['binds'][1]['sha256']=None;self.assertTrue(self.errors())
    def test_missing_identity_url(self):
        self.base['binds'][1]['remote_url']=None;self.assertTrue(self.errors())
    def test_mutable_url(self):
        self.base['binds'][1]['remote_url']=self.base['binds'][1]['remote_url'].replace('34ca6928d4c7c3fe107650d3202408d00232c288','main');self.assertTrue(self.errors())
    def test_unregistered_cast(self):
        self.base['exact_cast']=['CHAR-UNKNOWN'];self.assertTrue(self.errors())
    def test_empty_prop_counts(self):
        self.base['exact_prop_counts']={};self.assertTrue(self.errors())
    def test_placeholder_state(self):
        self.base['room_state']={'note':'set later'};self.assertTrue(self.errors())
    def test_wrong_progressive_state(self):
        self.base['room_state']['sink']='dirty';self.assertTrue(self.errors())
    def test_duplicate_instance(self):
        self.base['cast_instances']*=2;self.assertTrue(self.errors())
    def test_two_camera_moves(self):
        self.base['camera']['move_count']=2;self.assertTrue(self.errors())
    def test_boolean_duration(self):
        self.base['duration_seconds']=True;self.assertTrue(self.errors())
    def test_sound_not_final(self):
        self.prompt.write_text(self.prompt.read_text()+'new action after Sound\n');self.base['prompt_sha256']=v.filehash(self.prompt);self.assertTrue(self.errors())
    def test_stale_prompt_hash(self):
        self.base['prompt_sha256']='0'*64;self.assertTrue(self.errors())
    def test_stale_canon_hash(self):
        self.base['canon_sha256']='0'*64;self.assertTrue(self.errors())
    def test_missing_slot_cannot_fallback(self):
        self.base['binds'][0]['sha256']='a'*64;self.assertTrue(self.errors())
    def test_endpoint_hold_not_acted_opening(self):
        self.base['opening_approved']=True;self.base['opening_candidate']={'kind':'endpoint_hold','sha256':'a'*64};self.assertTrue(self.errors())
    def test_cap_not_reset(self):
        self.base.update(attempts_used=6,hold=False);self.assertTrue(self.errors())
    def test_no_delivery_acceptance(self):
        self.base['delivery_accepted']=True;self.assertTrue(self.errors())
    def test_prompt_traversal(self):
        self.base['prompt_path']='../../../outside.txt';self.assertTrue(self.errors())
    def test_request_wrong_hash(self):
        p=self.root/'request.json';p.write_text(json.dumps({'request_sha256':'bogus'}))
        self.base['request']={'path':'request.json','sha256':v.filehash(p)};self.assertTrue(self.errors())
    def test_plan_fingerprint_changes_on_action(self):
        h=v.fingerprint(self.base);self.base['action']='Different action';self.assertNotEqual(h,v.fingerprint(self.base))
    def test_plan_fingerprint_not_circular(self):
        h=v.fingerprint(self.base);self.base['request']={'path':'request.json','sha256':'a'*64};self.assertEqual(h,v.fingerprint(self.base))
    def test_draft_compile_does_not_export(self):
        import compile_v2
        output=self.root/'export'
        with self.assertRaises(ValueError):compile_v2.compile_shot(v.ROOT,'SHOT-BATH-TUB',output)
        self.assertFalse(output.exists())
    def ready_fixture(self):
        c=copy.deepcopy(self.base)
        c.update(blocking_findings=[],blocking_reason=None,hold=False,opening_approved=True,generation_allowed=True)
        c['binds'][0]={'id':'IMAGE_1','role':'approved_clean_first_frame','reference_id':None,
            'path':'handoff_art/opening.png','remote_url':'https://github.com/example/fixture/blob/'+'a'*40+'/opening.png',
            'sha256':'b'*64,'human_decision':'accepted','hud_present':False}
        for b in c['binds']:b.update(human_decision='accepted',hud_present=False)
        c['opening_candidate']={'kind':'complete_acted_first_frame','sha256':'b'*64,
            'cast_instances':c['cast_instances'],'room_state':c['room_state']}
        def receipt(name,data):
            p=self.root/name;p.write_text(json.dumps(data),encoding='utf-8')
            return {'path':name,'sha256':v.filehash(p)}
        # Synthetic receipts test structure only. They are not actual owner approval.
        c['approval_receipt']=receipt('approval.json',{'actor':'owner','decision':'accepted',
            'opening_sha256':'b'*64,'plan_sha256':v.fingerprint(c),'source_url':'https://example.test/owner-fixture','reviewed_at':'2026-09-19T00:00:00Z'})
        hashes={b['id']:b['sha256'] for b in c['binds']}
        c['access_receipt']=receipt('access.json',{'kind':'ACCESS_ACK','recipient':'grok',
            'bind_sha256s':hashes,'source_url':'https://example.test/access-fixture','checked_at':'2026-09-19T00:00:00Z'})
        req={'kind':'MOTION_REQUEST','request_id':'TEST-ONLY','shot_id':c['shot_id'],
            'plan_sha256':v.fingerprint(c),'prompt_sha256':c['prompt_sha256'],'bind_sha256s':hashes,
            'attempt':2,'remote_url':'https://github.com/example/fixture/blob/'+'a'*40+'/REQUEST.json'}
        req['request_sha256']=v.digest(req);c['request']=receipt('request.json',req)
        return c
    def test_complete_structural_fixture_can_pass(self):
        c=self.ready_fixture();self.assertEqual([],self.errors(c));self.assertEqual([],v.readiness(c,self.root))
    def test_stale_owner_receipt_fails(self):
        c=self.ready_fixture();c['action']='changed after approval';self.assertTrue(v.readiness(c,self.root))
    def test_coverage_opening_fails_even_with_other_receipts(self):
        c=self.ready_fixture();c['opening_candidate']['kind']='empty_coverage';self.assertTrue(v.readiness(c,self.root))
    def test_codex_access_is_not_grok_access(self):
        c=self.ready_fixture();c['access_receipt']=None;self.assertTrue(v.readiness(c,self.root))
    def test_pilot_preparation_request_valid(self):
        self.assertEqual([],v.check_preparation(v.ROOT/'preparation/PREP-BATH-TUB-20260919/REQUEST.json',v.ROOT))
    def test_pilot_cannot_authorize_motion(self):
        self.errors()  # Write the current card to isolated root.
        folder=self.root/'preparation/PILOT';folder.mkdir(parents=True)
        source=v.ROOT/'preparation/PREP-BATH-TUB-20260919'
        (folder/'STILL_PROMPT.txt').write_bytes((source/'STILL_PROMPT.txt').read_bytes())
        (self.path.parent/'FIRST_FRAME_BRIEF.txt').write_bytes((v.ROOT/'shots/SHOT-BATH-TUB/FIRST_FRAME_BRIEF.txt').read_bytes())
        req=v.read(source/'REQUEST.json');req['motion_authorized']=True
        req['request_sha256']=v.digest({k:x for k,x in req.items() if k!='request_sha256'})
        (folder/'REQUEST.json').write_text(json.dumps(req),encoding='utf-8')
        self.assertTrue(v.check_preparation(folder/'REQUEST.json',self.root))
    def test_event_dependencies_cannot_be_invented(self):
        self.base['depends_on_events']=['EV-INVENTED'];self.assertTrue(self.errors())
    def test_all_original_holds_preserved(self):
        for sid in ('SHOT-BUNNY-LAND','SHOT-C2-02','SHOT-C2-06','SHOT-C2-07'):
            self.assertTrue(v.read(v.ROOT/f'shots/{sid}/CARD.json')['hold'])
    def test_continuous_action_needs_exact_endpoint(self):
        c=self.ready_fixture();c['continuity'].update(kind='continuous_action',previous_end_sha256=None)
        self.assertTrue(v.readiness(c,self.root))

if __name__=='__main__':unittest.main()
