from contextlib import closing
import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.audit_grok_builder import validate, rebuild


class BuilderDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root/'source.png').write_bytes(b'fixture source')
        self.data = dict(entities=[dict(id='CHAR-A', type='character', name='A', reference_ids=['REF-A'])],
            references=[dict(id='REF-A', path='source.png', sha256=hashlib.sha256(b'fixture source').hexdigest(), role='identity', appearance_authority=True)],
            events=[dict(id='EV-A', name='A', location_id='CHAR-A', character_ids=['CHAR-A'], depends_on=[])],
            shots=[dict(id='SHOT-A', name='A', event_id='EV-A', location_id='CHAR-A', status='DRAFT', depends_on=[], generation_ready=False)],
            storyboards=[])

    def tearDown(self):
        self.tmp.cleanup()

    def test_sqlite_preserves_foreign_keys_and_canonical_records(self):
        self.assertEqual(validate(self.root,self.data),[])
        rebuild(self.root,self.data)
        with closing(sqlite3.connect(self.root/'DATABASE.sqlite')) as db:
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])
            self.assertEqual(db.execute('SELECT event_id FROM shots').fetchone()[0],'EV-A')

    def test_missing_event_and_dependency_cycle_fail(self):
        self.data['shots'][0]['event_id']='missing'
        self.data['events'][0]['depends_on']=['EV-A']
        errors=validate(self.root,self.data)
        self.assertTrue(any('unresolved events' in x for x in errors))
        self.assertTrue(any('cycle' in x for x in errors))

    def test_modified_reference_cannot_keep_old_hash(self):
        (self.root/'source.png').write_bytes(b'changed identity')
        self.assertTrue(any('hash mismatch' in x for x in validate(self.root,self.data)))

    def test_review_board_cannot_be_opening_or_grant_readiness(self):
        self.data['references'][0]['role']='runtime board evidence'
        self.data['shots'][0].update(opening_reference_id='REF-A',generation_ready=True)
        errors=validate(self.root,self.data)
        self.assertTrue(any('prohibited opening' in x for x in errors))
        self.assertTrue(any('cannot grant' in x for x in errors))

    def test_retired_identity_is_rejected(self):
        self.data['superseded_reference_hashes']=[self.data['references'][0]['sha256'][:10]]
        self.assertTrue(any('superseded identity' in x for x in validate(self.root,self.data)))

    def test_historical_clip_decision_is_not_delivery_acceptance(self):
        self.data['clips']=[dict(id='CLIP-A',sha256='a'*64,source_url='https://example.com/clip',delivery_accepted=True)]
        self.assertTrue(any('historical clip' in x for x in validate(self.root,self.data)))
        self.data['clips'][0]['delivery_accepted']=False
        rebuild(self.root,self.data)
        with closing(sqlite3.connect(self.root/'DATABASE.sqlite')) as db:
            self.assertEqual(db.execute('SELECT id FROM clips').fetchone()[0],'CLIP-A')

    def test_corrupt_scene_shot_orphan_fails(self):
        self.data['scenes']=[dict(id='SCENE-A', name='Scene', location_id='CHAR-A', event_id='EV-A', shot_ids=['missing-shot'], depends_on=[])]
        errors=validate(self.root,self.data)
        self.assertTrue(any('SCENE-A: unresolved shots ID missing-shot' in x for x in errors))
        self.assertTrue(any('not assigned to a scene' in x for x in errors))

    def test_duplicate_jobs_and_retired_tombstone_acts_fail(self):
        self.data['jobs']=[
            dict(id='JOB-A', name='First', key='first', act_index=1, runtime_source='runtime/a', roster=['CHAR-A']),
            dict(id='JOB-A', name='Duplicate', key='duplicate', act_index=2, runtime_source='runtime/b', roster=[]),
            dict(id='JOB-ACTIVE-4', name='Active tombstone 4', key='active-4', act_index=4, active=True, runtime_source='runtime/4', roster=[]),
            dict(id='JOB-ACTIVE-9', name='Active tombstone 9', key='active-9', act_index=9, active=True, runtime_source='runtime/9', roster=[]),
            dict(id='JOB-ACTIVE-14', name='Active tombstone 14', key='active-14', act_index=14, active=True, runtime_source='runtime/14', roster=[]),
            dict(id='JOB-RET', name='Retired tombstone', key='retired', act_index=4, retired=True, runtime_source='runtime/retired', roster=[]),
        ]
        errors=validate(self.root,self.data)
        self.assertTrue(any('Duplicate ID in jobs' in x for x in errors))
        for act_index in (4, 9, 14):
            self.assertTrue(any(f'act_index {act_index} retired tombstone cannot be a career job' in x for x in errors))

    def test_jobs_sidecar_must_mirror_database(self):
        self.data['jobs']=[dict(id='JOB-A', name='First', canon_key='first', act_index=1, runtime_source='runtime/a', roster=['CHAR-A'])]
        (self.root/'JOBS.json').write_text('''{"jobs": [], "chapter2_variants": []}''', encoding='utf-8')
        errors=validate(self.root,self.data)
        self.assertTrue(any('JOBS.json does not mirror DATABASE.json' in x for x in errors))

    def test_job_variant_base_event_and_reference_foreign_keys_fail(self):
        self.data['jobs']=[dict(id='JOB-A', name='First', key='first', act_index=1, runtime_source='runtime/a', roster=['CHAR-A'])]
        self.data['job_variants']=[dict(id='JOBVAR-C2-A', name='Variant', base_job_id='missing-job', event_id='missing-event', reference_ids=['REF-A'])]
        errors=validate(self.root,self.data)
        self.assertTrue(any('JOBVAR-C2-A: unresolved jobs ID missing-job' in x for x in errors))
        self.assertTrue(any('JOBVAR-C2-A: unresolved events ID missing-event' in x for x in errors))

    def test_sqlite_mirrors_jobs_scenes_and_scene_shots(self):
        self.data['jobs']=[dict(id='JOB-A', name='First', canon_key='first', act_index=1, runtime_source='runtime/a', roster=['CHAR-A'])]
        self.data['job_variants']=[dict(id='JOBVAR-C2-A', name='Variant', canon_key='variant', base_job_id='JOB-A', act_index=1, event_id='EV-A', scene_id='SCENE-A', reference_ids=['REF-A'])]
        self.data['scenes']=[dict(id='SCENE-A', name='Scene', location_id='CHAR-A', event_id='EV-A', shot_ids=['SHOT-A'], depends_on=[])]
        self.assertEqual(validate(self.root,self.data),[])
        rebuild(self.root,self.data)
        with closing(sqlite3.connect(self.root/'DATABASE.sqlite')) as db:
            self.assertEqual(db.execute('SELECT id,name,"key",act_index,runtime_source,roster FROM jobs').fetchone(), ('JOB-A','First','first',1,'runtime/a','["CHAR-A"]'))
            self.assertEqual(db.execute('SELECT id,base_job_id,event_id,scene_id FROM job_variants').fetchone(), ('JOBVAR-C2-A','JOB-A','EV-A','SCENE-A'))
            self.assertEqual(db.execute('SELECT id,name,location_id,event_id FROM scenes').fetchone(), ('SCENE-A','Scene','CHAR-A','EV-A'))
            self.assertEqual(db.execute('SELECT scene_id,shot_id,shot_index FROM scene_shots').fetchone(), ('SCENE-A','SHOT-A',0))
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])


if __name__=='__main__':
    unittest.main()
