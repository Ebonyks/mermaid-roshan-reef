"""Fast non-media regression checks for the executable editorial selection."""
import json
import tempfile
import unittest
from pathlib import Path

from tools import assemble_day_one_davinci as assembler


ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "assets_src/cinematics/day_one_davinci_draft_2026-09-04"


class DraftEditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assembly = json.loads((PACKET / "ASSEMBLY_MANIFEST.json").read_text(encoding="utf-8"))
        cls.movies = {m["id"]: m for m in cls.assembly["movies"]}

    def test_incomplete_events_remain_disabled(self):
        for mid in ["D1-C07", "D1-C08", "D1-C13"]:
            self.assertFalse(self.movies[mid]["runtime_preview_eligible"], mid)
        self.assertEqual(self.movies["D1-C08"]["shots"], [])

    def test_v02_removes_wrong_state_and_wrong_room(self):
        for mid, excluded, frames, version in [("D1-C04", "D1-C04-S02", 144, "V02"), ("D1-C12", "D1-C12-S03", 192, "V03")]:
            movie = self.movies[mid]
            self.assertEqual(movie["edit_version"], version)
            self.assertEqual(movie["frames"], frames)
            self.assertNotIn(excluded, [s["shot"] for s in movie["shots"]])
            self.assertIn(excluded, [s["shot"] for s in movie["excluded_shots"]])

    def test_final_recap_uses_room_correct_existing_endpoints(self):
        shots = {s["shot"]: s for s in self.movies["D1-C12"]["shots"]}
        self.assertEqual(shots["D1-C12-S01"]["source"], "C04_S04_v1_clean_endpoint.mp4")
        self.assertEqual(shots["D1-C12-S04"]["source"], "C10_S04_v1_desk_wake_OFFICIAL.mp4")
        self.assertNotIn("D1-C12-S05", shots)

    def test_native_ranges_and_gapless_record_accounting(self):
        for movie in self.movies.values():
            cursor = 0
            for shot in movie["shots"]:
                source = self.assembly["sources"][shot["source"]]
                start, end = shot["source_start"], shot["source_end_exclusive"]
                self.assertGreaterEqual(start, 0)
                self.assertGreater(end, start)
                self.assertLessEqual(end, source["native_frames"])
                self.assertEqual(shot["record_start"], cursor)
                cursor += end - start
                self.assertEqual(shot["record_end_exclusive"], cursor)
            self.assertEqual(cursor, movie["frames"])

    def test_downloads_are_explicit_not_fake_github_sources(self):
        local = [s for s in self.assembly["sources"].values() if s["kind"] == "local_user_supplied"]
        self.assertEqual(len(local), 3)
        for source in local:
            self.assertIsNone(source["source_url"])
            self.assertIsNone(source["source_commit"])
            self.assertEqual(len(source["sha256"]), 64)

    def test_editorial_claim_cannot_accept_delivery(self):
        self.assertTrue(self.assembly["claims"]["editorial_reference_only"])
        self.assertFalse(self.assembly["claims"]["delivery_accepted"])

    def _reuse_fixture(self):
        source = {"clip.mp4": {"sha256": "a" * 64}}
        movie = {
            "id": "D1-C99",
            "edit_version": "V01",
            "shots": [{
                "source": "clip.mp4",
                "source_start": 0,
                "source_end_exclusive": 48,
            }],
        }
        return source, movie

    def test_same_duration_changed_range_rejects_existing_render_reuse(self):
        source, current = self._reuse_fixture()
        previous = {"movies": [{**current, "shots": [{
            "source": "clip.mp4",
            "source_start": 48,
            "source_end_exclusive": 96,
        }]}], "sources": source}
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "D1-C99.mp4"
            output.touch()
            with self.assertRaisesRegex(RuntimeError, "bump edit_version"):
                assembler.guard_existing_render_reuse(
                    previous, [current], source, Path(temp))

    def test_same_duration_changed_source_rejects_existing_render_reuse(self):
        previous_source = {"old.mp4": {"sha256": "b" * 64}}
        current_source = {"new.mp4": {"sha256": "c" * 64}}
        previous = {"movies": [{
            "id": "D1-C99", "edit_version": "V01", "shots": [{
                "source": "old.mp4", "source_start": 0,
                "source_end_exclusive": 48,
            }]}], "sources": previous_source}
        current = {"id": "D1-C99", "edit_version": "V01", "shots": [{
            "source": "new.mp4", "source_start": 0,
            "source_end_exclusive": 48,
        }]}
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, "D1-C99.mp4").touch()
            with self.assertRaisesRegex(RuntimeError, "bump edit_version"):
                assembler.guard_existing_render_reuse(
                    previous, [current], current_source, Path(temp))

    def test_metadata_only_change_allows_existing_render_reuse(self):
        source, current = self._reuse_fixture()
        previous_movie = {**current, "status": "old", "shots": [{
            **current["shots"][0], "edit_note": "old note"}]}
        current_movie = {**current, "status": "new", "runtime_preview_eligible": True,
                         "shots": [{**current["shots"][0], "edit_note": "new note"}]}
        previous = {"movies": [previous_movie], "sources": source}
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, "D1-C99.mp4").touch()
            assembler.guard_existing_render_reuse(
                previous, [current_movie], source, Path(temp))

    def test_changed_source_hash_rejects_existing_render_reuse(self):
        source, current = self._reuse_fixture()
        previous = {"movies": [current], "sources": {"clip.mp4": {"sha256": "b" * 64}}}
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, "D1-C99.mp4").touch()
            with self.assertRaisesRegex(RuntimeError, "bump edit_version"):
                assembler.guard_existing_render_reuse(previous, [current], source, Path(temp))

    def test_render_without_prior_authority_is_not_reused(self):
        source, current = self._reuse_fixture()
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, "D1-C99.mp4").touch()
            with self.assertRaisesRegex(RuntimeError, "bump edit_version"):
                assembler.guard_existing_render_reuse({}, [current], source, Path(temp))

    def test_unused_new_version_is_allowed(self):
        source, current = self._reuse_fixture()
        previous = {"movies": [current], "sources": source}
        updated = {**current, "edit_version": "V02"}
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, "D1-C99.mp4").touch()
            assembler.guard_existing_render_reuse(previous, [updated], source, Path(temp))


if __name__ == "__main__":
    unittest.main()
