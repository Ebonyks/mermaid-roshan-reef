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


if __name__=='__main__':
    unittest.main()
