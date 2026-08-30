from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.audit_imagine_handoff import audit_handoff


class ImagineHandoffAuditTest(unittest.TestCase):
	def _ready_v2_packet(self, root: Path) -> tuple[Path, Path]:
		packet = root / "packet_v2"
		shot_dir = packet / "shots" / "S0"
		shot_dir.mkdir(parents=True)
		first = shot_dir / "first.png"
		identity = packet / "handoff_art" / "roshan.png"
		identity.parent.mkdir()
		first.write_bytes(b"approved room and first frame")
		identity.write_bytes(b"canonical roshan")
		prompt = (
			"locked camera on the approved room from IMAGE_1.\n"
			"0.0–2.0s: Roshan wipes the fixture once.\n"
			"preserve Roshan child identity. no legs. keep giant pool geometry locked.\n"
			"end: Roshan holds beside the clean fixture.\n"
			"Sound: soft cloth and room tone.\n"
		)
		prompt_path = shot_dir / "PROMPT.txt"
		prompt_path.write_text(prompt, encoding="utf-8")

		def digest(path: Path) -> str:
			return hashlib.sha256(path.read_bytes()).hexdigest()

		commit = "c" * 40
		card = {
			"schema": "imagine-shot-packet-v2",
			"movie_id": "movie_v2",
			"shot_id": "S0",
			"sequence_position": 0,
			"beat_ids": ["B01"],
			"mode": "image_to_video",
			"output_disposition": "motion_reference_only",
			"duration_seconds": 2,
			"aspect_ratio": "16:9",
			"delivery_size": [1280, 720],
			"bound_references": [
				{
					"id": "IMAGE_1",
					"path": "shots/S0/first.png",
					"sha256": digest(first),
					"role": "approved_clean_first_frame",
					"authority_domain": "location layout and exact opening pixels",
					"source_kind": "approved_master",
					"remote_url": f"https://raw.githubusercontent.com/example/project/{commit}/packet/shots/S0/first.png",
					"hud_present": False,
					"human_decision": "accepted",
				},
				{
					"id": "IMAGE_2",
					"path": "handoff_art/roshan.png",
					"sha256": digest(identity),
					"role": "subject_identity",
					"authority_domain": "Roshan identity, age, costume, and mer-tail anatomy",
					"remote_url": f"https://raw.githubusercontent.com/example/project/{commit}/packet/handoff_art/roshan.png",
					"hud_present": False,
					"human_decision": "accepted",
				},
			],
			"exact_cast": ["roshan"],
			"character_locks": [{
				"character_id": "roshan",
				"reference_id": "IMAGE_2",
				"identity_invariants": ["child age", "brown rainbow-streaked hair", "pink shell top"],
				"anatomy_invariants": ["one continuous mer-tail"],
				"forbidden_changes": ["no legs", "no costume drift"],
				"screen_role": "screen-left cleaner",
				"start_state": "hand on cloth",
				"end_state": "beside clean fixture",
				"required_prompt_phrases": ["preserve Roshan child identity", "no legs"],
			}],
			"location_lock": {
				"reference_id": "IMAGE_1",
				"immutable_features": ["one giant pool", "fixed fixture positions"],
				"forbidden_geometry": ["no local basin"],
				"required_prompt_phrases": ["keep giant pool geometry locked"],
			},
			"causal_chain": {
				"trigger": "cloth contacts grime",
				"visible_change": "grime clears",
				"end_confirmation": "fixture is visibly clean",
			},
			"continuity": {
				"kind": "new_setup",
				"previous_shot_id": None,
				"inherited_state": ["same room and lighting"],
				"allowed_changes": ["cloth and Roshan arm move"],
			},
			"non_pixel_references": [],
			"camera": {"verb": "locked", "move_count": 0},
			"must_move": ["Roshan's wiping arm"],
			"must_not_move": ["pool geometry"],
			"end_state": "Roshan holds beside the clean fixture.",
			"negative_constraints": ["no HUD", "no identity drift", "no local basin"],
			"prompt_path": "shots/S0/PROMPT.txt",
			"prompt_sha256": digest(prompt_path),
		}
		card_path = shot_dir / "SHOT_PACKET.json"
		card_path.write_text(json.dumps(card), encoding="utf-8")
		handoff = {
			"schema": "imagine-handoff-v2",
			"handoff_id": "movie_v2",
			"archive_status": "complete",
			"generation_status": "ready",
			"delivery_status": "not_accepted",
			"blocking_findings": [],
			"story_contract": {
				"one_sentence_promise": "Roshan visibly cleans one fixture.",
				"ordered_beats": [{"beat_id": "B01", "trigger": "cloth contact", "visible_result": "fixture clean"}],
				"forbidden_events": ["no montage", "no invented character"],
				"final_state": "Roshan holds beside the clean fixture.",
			},
			"character_authorities": [{
				"character_id": "roshan",
				"path": "handoff_art/roshan.png",
				"sha256": digest(identity),
				"status": "approved",
				"immutable_traits": ["child age", "brown rainbow-streaked hair", "pink shell top"],
				"anatomy_traits": ["one continuous mer-tail"],
				"forbidden_drift": ["no legs", "no costume drift"],
			}],
			"location_authority": {
				"path": "shots/S0/first.png",
				"sha256": digest(first),
				"immutable_features": ["one giant pool", "fixed fixture positions", "same room architecture"],
				"forbidden_geometry": ["no local basin"],
			},
			"shot_packets": ["shots/S0/SHOT_PACKET.json"],
			"archive_remote": {
				"commit": commit,
				"tree": f"https://github.com/example/project/tree/{commit}/packet",
				"manifest": f"https://raw.githubusercontent.com/example/project/{commit}/packet/HANDOFF_PACKET.json",
				"verified_via": "test",
				"verified_at": "2026-08-30",
			},
		}
		(packet / "IMAGINE_HANDOFF.json").write_text(json.dumps(handoff), encoding="utf-8")
		return packet, card_path

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

	def test_ready_v2_packet_passes_character_and_causality_contract(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			packet, _card = self._ready_v2_packet(Path(temporary))
			self.assertEqual([], audit_handoff(packet, require_ready=True))

	def test_v2_character_prompt_drift_and_authority_mismatch_fail(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			packet, card_path = self._ready_v2_packet(Path(temporary))
			card = json.loads(card_path.read_text(encoding="utf-8"))
			card["character_locks"][0]["required_prompt_phrases"].append("exact violet crown")
			card["bound_references"][1]["sha256"] = "d" * 64
			card_path.write_text(json.dumps(card), encoding="utf-8")
			errors = audit_handoff(packet, require_ready=True)
			self.assertTrue(any("bound identity hash differs" in error for error in errors))
			self.assertTrue(any("character lock phrase is missing" in error for error in errors))

	def test_v2_continuous_action_requires_previous_end(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			packet, card_path = self._ready_v2_packet(Path(temporary))
			card = json.loads(card_path.read_text(encoding="utf-8"))
			card["continuity"]["kind"] = "continuous_action"
			card_path.write_text(json.dumps(card), encoding="utf-8")
			errors = audit_handoff(packet, require_ready=True)
			self.assertTrue(any("accepted_previous_end" in error for error in errors))


if __name__ == "__main__":
	unittest.main()
