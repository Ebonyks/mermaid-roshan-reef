"""Integrity/readiness boundaries for the bounded Roshan motion-reference archive."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import build_roshan_grok_auditions as builder
import roshan_grok_video_first as dispatch
from audit_imagine_handoff import audit_handoff, audit_shot


class RoshanGrokAuditionsTests(unittest.TestCase):
    def test_video_first_and_no_still_fallback(self):
        start = (builder.PACKET / "START_HERE.txt").read_text(encoding="utf-8")
        self.assertIn("VIDEO_TOOL_UNAVAILABLE", start)
        self.assertIn("no still-board fallback", start)
        self.assertIn("No RSW-02 through RSW-08 until", start)
        self.assertLess(len(start.split()), 450)
        for path in (builder.PACKET / "shots").glob("*/SHOT_PACKET.json"):
            card = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(card["execution"]["fallback_to_stills"])
            self.assertEqual(card["execution"]["deliverable"], "original_continuous_video")
            self.assertIsNone(card["execution"]["actual_tool_mode"])
            for ref in card["bound_references"]:
                self.assertTrue(ref["remote_url"].startswith(dispatch.SOURCE_BASE))
                self.assertEqual(ref["input_binding_status"], "NOT_VERIFIED_IN_VIDEO_TOOL")

    def test_unknown_capability_not_fabricated(self):
        cap = json.loads((builder.PACKET / "CAPABILITY_CHECK.template.json").read_text(encoding="utf-8"))
        self.assertIsNone(cap["session_video_tool"])
        self.assertIsNone(cap["pilot_video_sha256"])
        self.assertFalse(cap["continue_batch"])
        self.assertEqual(cap["actual_attached_inputs"], [])
        self.assertEqual(cap["status"], "NOT_CHECKED")

    def test_refresh_preserves_pixels_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = Path(temp) / "packet"
            shutil.copytree(builder.PACKET, packet)
            before = {p.relative_to(packet): builder.sha(p) for p in packet.rglob("*.png")}
            dispatch.refresh(packet)
            first = {p.relative_to(packet): builder.sha(p) for p in packet.rglob("*") if p.is_file()}
            dispatch.refresh(packet)
            self.assertEqual(first, {p.relative_to(packet): builder.sha(p) for p in packet.rglob("*") if p.is_file()})
            self.assertEqual(before, {p.relative_to(packet): builder.sha(p) for p in packet.rglob("*.png")})

    def test_publication_binds_payload_but_not_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = Path(temp) / "packet"
            shutil.copytree(builder.PACKET, packet)
            def response(url, **kwargs):
                return io.BytesIO((packet / url.split(builder.REL.as_posix() + "/", 1)[1]).read_bytes())
            with patch.object(builder, "PACKET", packet), patch.object(builder.urllib.request, "urlopen", side_effect=response), contextlib.redirect_stdout(io.StringIO()):
                builder.bind_remote("a" * 40)
                self.assertTrue(builder.verify())
                handoff = json.loads((packet / "IMAGINE_HANDOFF.json").read_text(encoding="utf-8"))
                self.assertEqual(handoff["archive_status"], "complete")
                self.assertEqual(handoff["generation_status"], "blocked")
                self.assertFalse(handoff["claims"]["GENERATION_READY"])
                receipt = json.loads((packet / "PUBLICATION.json").read_text(encoding="utf-8"))
                receipt["files"].pop()
                builder.write_json(packet / "PUBLICATION.json", receipt)
                self.assertFalse(builder.verify())

    def test_failed_remote_hash_never_marks_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = Path(temp) / "packet"
            shutil.copytree(builder.PACKET, packet)
            dispatch.refresh(packet)
            with patch.object(builder, "PACKET", packet):
                builder.refresh_manifest()
                with patch.object(builder.urllib.request, "urlopen", side_effect=lambda *a, **k: io.BytesIO(b"wrong")), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(ValueError, "remote hash mismatch"):
                        builder.bind_remote("a" * 40)
            handoff = json.loads((packet / "IMAGINE_HANDOFF.json").read_text(encoding="utf-8"))
            self.assertEqual(handoff["archive_status"], "incomplete")

    def test_excluded_controls_cannot_hide_creative_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = Path(temp) / "packet"
            shutil.copytree(builder.PACKET, packet)
            (packet / "unregistered-prompt.txt").write_text("different art", encoding="utf-8")
            with patch.object(builder, "PACKET", packet), contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(builder.verify())

    def test_archive_and_drafts_integrity(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(builder.verify())

    def test_ready_gate_must_fail(self):
        self.assertTrue(any("GENERATION_READY is required" in e for e in audit_handoff(builder.PACKET, True)))

    def test_each_opening_requires_actual_human_approval(self):
        manifest = json.loads((builder.PACKET / "IMAGINE_HANDOFF.json").read_text(encoding="utf-8"))
        for path in manifest["draft_shot_packets"]:
            errors = audit_shot(builder.PACKET, builder.PACKET / path, manifest)
            self.assertEqual(len(errors), 1)
            self.assertIn("IMAGE_1 must be human accepted", errors[0])

    def test_intake_has_no_fabricated_reviews(self):
        data = json.loads((builder.PACKET / "RETURN_MANIFEST.template.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["candidates"]), 8)
        for c in data["candidates"]:
            self.assertIsNone(c["sha256"])
            self.assertFalse(c["normal_speed_reviewed"])
            self.assertIsNone(c["owner_selection"])
            self.assertTrue(all(v is None for v in c["scores"].values()))

    def test_loop_and_matched_pair_contracts(self):
        brief = json.loads(builder.BRIEF.read_text(encoding="utf-8"))
        samples = brief["samples"]
        self.assertEqual(samples[0]["comparison_group"], samples[1]["comparison_group"])
        self.assertEqual(samples[0]["end"], samples[1]["end"])
        for sample in samples[6:]:
            self.assertEqual(sample["requested_cycles"], [[1, 4], [4, 7]])
        for sample in samples:
            self.assertEqual(sample["beats"][0][0], 0)
            self.assertEqual(sample["beats"][-1][1], 8)
            for a, b in zip(sample["beats"], sample["beats"][1:]):
                self.assertEqual(a[1], b[0])

    def test_tampered_payload_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = Path(temp) / "packet"
            shutil.copytree(builder.PACKET, packet)
            path = packet / "shots/RSW-01/PROMPT.txt"
            path.write_bytes(path.read_bytes() + b"tampered")
            with patch.object(builder, "PACKET", packet), contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(builder.verify())

    def test_board_links_are_self_contained(self):
        from html.parser import HTMLParser
        links = []
        class Parser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                for name, value in attrs:
                    if name in ("src", "href"):
                        links.append(value)
        board = (builder.PACKET / "SHOT_BOARD.html").read_text(encoding="utf-8")
        self.assertLess(board.index("Video-first revision:"), board.index('<div class="openings">'))
        Parser().feed(board)
        self.assertGreater(len(links), 25)
        for link in links:
            self.assertFalse("://" in link)
            self.assertTrue((builder.PACKET / link).is_file(), link)


if __name__ == "__main__":
    unittest.main()
