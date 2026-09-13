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
from audit_imagine_handoff import audit_handoff, audit_shot


class RoshanGrokAuditionsTests(unittest.TestCase):
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
        Parser().feed((builder.PACKET / "SHOT_BOARD.html").read_text(encoding="utf-8"))
        self.assertGreater(len(links), 25)
        for link in links:
            self.assertFalse("://" in link)
            self.assertTrue((builder.PACKET / link).is_file(), link)


if __name__ == "__main__":
    unittest.main()
