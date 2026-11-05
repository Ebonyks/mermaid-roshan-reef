from __future__ import annotations
import copy
import unittest
from pathlib import Path
from tools import design_reference as reference

ROOT=Path(__file__).resolve().parents[2]

class ChapterReferenceTests(unittest.TestCase):
    def setUp(self):
        self.canon=reference.load(ROOT,reference.CANON)
        self.chapters=reference.load(ROOT,reference.MAP)

    def test_current_references_and_generated_views(self):
        self.assertEqual([],reference.check(ROOT))

    def test_identity_hash_drift_fails(self):
        row=next(row for row in self.canon['entities'] if row['identity']['art'])
        row['identity']['art'][0]['sha256']='0'*64
        self.assertTrue(any('identity source hash drift' in issue for issue in reference.validate(ROOT,self.canon,self.chapters)))

    def test_acceptance_cannot_be_promoted_without_all_evidence(self):
        self.chapters['chapters'][0]['rung']='ACCEPTED'
        issues=reference.validate(ROOT,self.canon,self.chapters)
        for missing in ('fresh_save_route','device_session','owner_review'):
            self.assertTrue(any('lacks '+missing in issue for issue in issues), issues)

    def test_unknown_owner_decision_and_unanswered_conflict_fail(self):
        self.canon['entities'][0]['decisions'].append('ODR-INVENTED')
        self.canon['conflicts'][0].update(status='OPEN',question_id=None)
        issues=reference.validate(ROOT,self.canon,self.chapters)
        self.assertTrue(any('unknown owner decision' in issue for issue in issues))
        self.assertTrue(any('question ID' in issue for issue in issues))

    def test_book_first_correction_cannot_silently_disappear(self):
        self.canon['book_precedence']['decision']='game-first-default'
        self.assertTrue(any('book-first' in issue for issue in reference.validate(ROOT,self.canon,self.chapters)))

    def test_source_escape_is_rejected(self):
        self.assertTrue(reference.path_issues(ROOT,'../outside'))
        self.assertTrue(reference.path_issues(ROOT,'.secrets/private'))

if __name__ == '__main__': unittest.main()
