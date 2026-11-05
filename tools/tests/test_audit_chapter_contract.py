from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from tools import audit_chapter_contract as chapter

ROOT = Path(__file__).resolve().parents[2]

class ChapterContractTests(unittest.TestCase):
    def test_live_bindings(self):
        self.assertEqual([], chapter.audit(ROOT))

    def mutate(self, before, after):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (chapter.ADAPTER, chapter.WORLD, chapter.PATHS, chapter.PLAN):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                text = (ROOT / name).read_text(encoding="utf-8")
                if name == chapter.ADAPTER:
                    self.assertIn(before, text)
                    text = text.replace(before, after, 1)
                path.write_text(text, encoding="utf-8")
            return chapter.audit(root)

    def test_unbound_step_fails_in_real_registry(self):
        issues = self.mutate('"MIX": {"station_id": "mixing_bowl"', '"MISSING MIX": {"station_id": "mixing_bowl"')
        self.assertTrue(any("chef/MIX: unbound" in issue for issue in issues), issues)

    def test_other_room_object_fails_in_real_registry(self):
        issues = self.mutate('"MIX": {"station_id": "mixing_bowl"', '"MIX": {"station_id": "treasure_dais"')
        self.assertTrue(any("chef/MIX: object outside its own room" in issue for issue in issues), issues)

    def test_parser_fails_closed(self):
        with self.assertRaises(ValueError): chapter.constant("const X := runtime_call()", "X")
        with self.assertRaises(ValueError): chapter.literal("{broken", 0)

if __name__ == "__main__": unittest.main()
