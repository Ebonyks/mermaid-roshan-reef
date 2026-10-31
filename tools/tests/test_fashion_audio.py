import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.audit_audio_quality import validate_fashion_manifest

ROOT = Path(__file__).resolve().parents[2]

class FashionAudioTests(unittest.TestCase):
    def test_current_cohort_has_complete_generation_evidence(self):
        self.assertEqual(validate_fashion_manifest(ROOT), [])

    def fixture(self, root):
        directory = root / "assets/audio/fashion"
        shutil.copytree(ROOT / "assets/audio/fashion", directory)
        return directory

    def test_mismatched_caption_is_blocking(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            directory = self.fixture(root)
            path = directory / "VOICE_CATALOG.json"
            catalog = json.loads(path.read_text())
            catalog["rows"][0]["caption"] = "A wrong instruction"
            path.write_text(json.dumps(catalog))
            self.assertIn("fashion exact cue/transcript inventory mismatch", validate_fashion_manifest(root))

    def test_changed_audio_bytes_are_blocking(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            directory = self.fixture(root)
            path = next(directory.glob("*.ogg"))
            path.write_bytes(path.read_bytes() + b"tampered")
            self.assertTrue(any("fashion delivery hash mismatch" in x for x in validate_fashion_manifest(root)))

if __name__ == "__main__":
    unittest.main()
