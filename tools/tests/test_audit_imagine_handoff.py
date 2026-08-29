from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.audit_imagine_handoff import audit_handoff


class ImagineHandoffAuditTest(unittest.TestCase):
	def _ready_packet(self, root: Path) -> tuple[Path, Path]:
		packet = root / "packet"
		shot_dir = packet / "shots" / "S0"
		shot_dir.mkdir(parents=True)
		for name in ("first.png", "identity.png"):
			(shot_dir / name).write_bytes(name.encode("utf-8"))
		prompt = "locked camera.\n0.0–2.0s: the cloth wipes once.\nend: cloth rests.\nSound: soft cloth on porcelain.\n"
		(shot_dir / "PROMPT.txt").write_text(prompt, encoding="utf-8")

		def digest(path: Path) -> str:
			return hashlib.sha256(path.read_bytes()).hexdigest()

		card = {
			"schema": "imagine-shot-packet-v1",
			"movie_id": "movie",
			"shot_id": "S0",
			"mode": "image_to_video",
			"output_disposition": "motion_reference_only",
			"duration_seconds": 2,
			"aspect_ratio": "16:9",
			"delivery_size": [1280, 720],
			"bound_references": [
				{"id": "IMAGE_1", "path": "shots/S0/first.png", "sha256": digest(shot_dir / "first.png"), "role": "approved_clean_first_frame", "hud_present": False, "human_decision": "accepted"},
				{"id": "IMAGE_2", "path": "shots/S0/identity.png", "sha256": digest(shot_dir / "identity.png"), "role": "subject_identity", "hud_present": False, "human_decision": "accepted"},
			],
			"non_pixel_references": [],
			"camera": {"verb": "locked", "move_count": 0},
			"must_move": ["cloth"],
			"must_not_move": ["fixtures"],
			"end_state": "cloth rests",
			"negative_constraints": ["no HUD"],
			"prompt_path": "shots/S0/PROMPT.txt",
			"prompt_sha256": digest(shot_dir / "PROMPT.txt"),
		}
		(shot_dir / "SHOT_PACKET.json").write_text(json.dumps(card), encoding="utf-8")
		handoff = {
			"schema": "imagine-handoff-v1",
			"handoff_id": "movie",
			"archive_status": "complete",
			"generation_status": "ready",
			"delivery_status": "not_accepted",
			"blocking_findings": [],
			"shot_packets": ["shots/S0/SHOT_PACKET.json"],
			"archive_remote": {
				"commit": "a" * 40,
				"tree": "https://github.com/example/project/tree/" + "a" * 40 + "/packet",
				"manifest": "https://raw.githubusercontent.com/example/project/" + "a" * 40 + "/packet/HANDOFF_PACKET.json",
				"verified_via": "test",
				"verified_at": "2026-08-29",
			},
		}
		(packet / "IMAGINE_HANDOFF.json").write_text(json.dumps(handoff), encoding="utf-8")
		return packet, shot_dir / "SHOT_PACKET.json"

	def test_ready_packet_passes(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			packet, _card = self._ready_packet(Path(temporary))
			self.assertEqual([], audit_handoff(packet, require_ready=True))

	def test_blocked_packet_is_truthful_but_not_ready(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			packet = Path(temporary)
			(packet / "IMAGINE_HANDOFF.json").write_text(json.dumps({
				"schema": "imagine-handoff-v1",
				"handoff_id": "draft",
				"archive_status": "complete",
				"generation_status": "blocked",
				"delivery_status": "not_accepted",
				"blocking_findings": ["missing clean first frame"],
				"shot_packets": [],
				"archive_remote": {
					"commit": "b" * 40,
					"tree": "https://github.com/example/project/tree/" + "b" * 40 + "/packet",
					"manifest": "https://raw.githubusercontent.com/example/project/" + "b" * 40 + "/packet/HANDOFF_PACKET.json",
					"verified_via": "test",
					"verified_at": "2026-08-29",
				},
			}), encoding="utf-8")
			self.assertEqual([], audit_handoff(packet))
			self.assertTrue(audit_handoff(packet, require_ready=True))

	def test_hud_reference_and_archive_prompt_fail(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			packet, card_path = self._ready_packet(Path(temporary))
			card = json.loads(card_path.read_text(encoding="utf-8"))
			card["bound_references"][0]["path"] = "shots/S0/runtime_anchor.png"
			(card_path.parent / "runtime_anchor.png").write_bytes(b"runtime")
			card["bound_references"][0]["sha256"] = hashlib.sha256(b"runtime").hexdigest()
			prompt_path = card_path.parent / "PROMPT.txt"
			prompt_path.write_text(prompt_path.read_text(encoding="utf-8") + "sha256 metadata\n", encoding="utf-8")
			card["prompt_sha256"] = hashlib.sha256(prompt_path.read_bytes()).hexdigest()
			card_path.write_text(json.dumps(card), encoding="utf-8")
			errors = audit_handoff(packet, require_ready=True)
			self.assertTrue(any("forbidden bound pixel reference" in error for error in errors))
			self.assertTrue(any("metadata token leaked" in error for error in errors))


if __name__ == "__main__":
	unittest.main()
