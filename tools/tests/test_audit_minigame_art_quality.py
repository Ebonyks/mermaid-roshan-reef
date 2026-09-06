from __future__ import annotations

import copy
import hashlib
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from tools.audit_minigame_art_quality import DIMENSIONS, audit_data


def tiny_png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
	"""Create a deterministic tiny RGB PNG fixture without image tooling."""
	rows = b"".join(b"\x00" + bytes(rgb) * width for _ in range(height))
	def chunk(kind: bytes, payload: bytes) -> bytes:
		return struct.pack(">I", len(payload)) + kind + payload \
			+ struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
	ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
	return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) \
		+ chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


class MinigameArtQualityAuditTest(unittest.TestCase):
	def setUp(self) -> None:
		self.temp = tempfile.TemporaryDirectory()
		self.root = Path(self.temp.name)
		(self.root / "art.png").write_bytes(b"art")
		(self.root / "capture.png").write_bytes(tiny_png(1280, 720, (20, 40, 80)))
		sha = lambda name: hashlib.sha256((self.root / name).read_bytes()).hexdigest()
		self.data = {
			"schema": "minigame-art-quality-v1", "candidate_revision": "a" * 40,
			"scope": {"games": ["seek"], "coverage_complete": True,
				"surfaces": [{"game": "seek", "id": "meadow", "live_asset_ids": ["evie"]}]},
			"assets": [{"id": "evie", "game": "seek", "surface": "meadow",
				"role": "actor", "states": ["idle"],
				"source": {"path": "art.png", "sha256": sha("art.png")},
				"reviews": {"prior": None, "candidate": {
					"dimensions": dict.fromkeys(DIMENSIONS, 4.5), "na_reasons": {},
					"score": 4.5, "reviewer": {"kind": "ai", "id": "reviewer-1"},
					"evidence": [{"path": "capture.png", "sha256": sha("capture.png"),
						"context": {"runtime": True, "candidate_revision": "a" * 40,
							"renderer": "mobile", "viewport": [1280, 720], "hud": True,
							"state": "idle"}}]}},
				"defects": [], "replacement_history": []}],
			"approvals": {"owner": {"approved": False}, "device": {"approved": False},
				"child": {"approved": False}},
		}

	def tearDown(self) -> None:
		self.temp.cleanup()

	def test_valid_complete_candidate_passes(self) -> None:
		self.assertEqual(([], []), audit_data(self.data, self.root))

	def test_utf8_lf_source_hash_accepts_crlf_and_lf_but_changed_code_fails(self) -> None:
		path = self.root / "logic.gd"
		lf = b"extends Node\nfunc run():\n\tpass\n"
		path.write_bytes(lf.replace(b"\n", b"\r\n"))
		digest = hashlib.sha256(lf).hexdigest()
		data = copy.deepcopy(self.data)
		data["assets"][0]["source"] = {
			"path": "logic.gd", "sha256": digest, "hash_normalization": "utf8_lf"
		}
		self.assertEqual(([], []), audit_data(data, self.root))
		path.write_bytes(lf.replace(b"run", b"changed").replace(b"\n", b"\r\n"))
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("file hash mismatch" in item for item in errors))

	def test_code_hash_is_exact_bytes_without_opt_in(self) -> None:
		path = self.root / "logic.py"
		lf = b"print('ok')\n"
		path.write_bytes(lf.replace(b"\n", b"\r\n"))
		data = copy.deepcopy(self.data)
		data["assets"][0]["source"] = {"path": "logic.py", "sha256": hashlib.sha256(lf).hexdigest()}
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("file hash mismatch" in item for item in errors))

	def test_normalization_rejects_unknown_binary_and_invalid_utf8(self) -> None:
		for record, expected in (
			({"path": "logic.gd", "sha256": "0" * 64, "hash_normalization": "utf8_crlf"}, "unknown hash_normalization"),
			({"path": "art.png", "sha256": hashlib.sha256((self.root / "art.png").read_bytes()).hexdigest(), "hash_normalization": "utf8_lf"}, ".gd/.py source files"),
		):
			data = copy.deepcopy(self.data)
			data["assets"][0]["source"] = record
			errors, _ = audit_data(data, self.root)
			self.assertTrue(any(expected in item for item in errors))
		bad = self.root / "bad.gd"
		bad.write_bytes(b"\xff\xfe")
		data = copy.deepcopy(self.data)
		data["assets"][0]["source"] = {"path": "bad.gd", "sha256": "0" * 64, "hash_normalization": "utf8_lf"}
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("valid UTF-8" in item for item in errors))

	def test_evidence_hash_normalization_is_rejected(self) -> None:
		data = copy.deepcopy(self.data)
		data["assets"][0]["reviews"]["candidate"]["evidence"][0]["hash_normalization"] = "utf8_lf"
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("only on asset source records" in item for item in errors))

	def test_low_critical_dimension_blocks_despite_high_mean(self) -> None:
		data = copy.deepcopy(self.data)
		dims = data["assets"][0]["reviews"]["candidate"]["dimensions"]
		dims.update(dict.fromkeys(DIMENSIONS, 5.0))
		dims["edges"] = 4.0
		data["assets"][0]["reviews"]["candidate"]["score"] = 4.88
		errors, blockers = audit_data(data, self.root)
		self.assertFalse(errors)
		self.assertTrue(any("below 4.5" in item for item in blockers))

	def test_unresolved_blocking_defect_blocks(self) -> None:
		data = copy.deepcopy(self.data)
		data["assets"][0]["defects"] = [
			{"rule_id": "DL-MOT-01", "blocking": True, "resolved": False}
		]
		self.assertTrue(audit_data(data, self.root)[1])

	def test_stale_runtime_context_blocks_high_score(self) -> None:
		data = copy.deepcopy(self.data)
		context = data["assets"][0]["reviews"]["candidate"]["evidence"][0]["context"]
		context["candidate_revision"] = "b" * 40
		self.assertTrue(any(">=4.5" in item for item in audit_data(data, self.root)[1]))

	def test_fresh_state_does_not_legalize_stale_second_state(self) -> None:
		data = copy.deepcopy(self.data)
		asset = data["assets"][0]
		asset["states"] = ["idle", "payoff"]
		stale = copy.deepcopy(asset["reviews"]["candidate"]["evidence"][0])
		stale["context"]["state"] = "payoff"
		stale["context"]["candidate_revision"] = "b" * 40
		asset["reviews"]["candidate"]["evidence"].append(stale)
		_, blockers = audit_data(data, self.root)
		self.assertTrue(any("payoff" in item for item in blockers))

	def test_fresh_state_does_not_legalize_nonruntime_second_state(self) -> None:
		data = copy.deepcopy(self.data)
		asset = data["assets"][0]
		asset["states"] = ["idle", "payoff"]
		diagnostic = copy.deepcopy(asset["reviews"]["candidate"]["evidence"][0])
		diagnostic["context"]["state"] = "payoff"
		diagnostic["context"]["runtime"] = False
		asset["reviews"]["candidate"]["evidence"].append(diagnostic)
		_, blockers = audit_data(data, self.root)
		self.assertTrue(any("payoff" in item for item in blockers))

	def test_identical_current_image_cannot_be_relabelled_for_second_state(self) -> None:
		data = copy.deepcopy(self.data)
		asset = data["assets"][0]
		asset["states"] = ["idle", "payoff"]
		payoff = copy.deepcopy(asset["reviews"]["candidate"]["evidence"][0])
		payoff["context"]["state"] = "payoff"
		asset["reviews"]["candidate"]["evidence"].append(payoff)
		_, blockers = audit_data(data, self.root)
		self.assertTrue(any("identical current PNG" in item for item in blockers))

	def test_distinct_current_state_images_pass(self) -> None:
		data = copy.deepcopy(self.data)
		asset = data["assets"][0]
		asset["states"] = ["idle", "payoff"]
		payoff_path = self.root / "payoff.png"
		payoff_path.write_bytes(tiny_png(1280, 720, (220, 80, 40)))
		payoff = copy.deepcopy(asset["reviews"]["candidate"]["evidence"][0])
		payoff["path"] = "payoff.png"
		payoff["sha256"] = hashlib.sha256(payoff_path.read_bytes()).hexdigest()
		payoff["context"]["state"] = "payoff"
		asset["reviews"]["candidate"]["evidence"].append(payoff)
		self.assertEqual(([], []), audit_data(data, self.root))

	def test_current_evidence_requires_decodable_png_and_dimensions(self) -> None:
		data = copy.deepcopy(self.data)
		capture = data["assets"][0]["reviews"]["candidate"]["evidence"][0]
		bad_capture = self.root / "bad_capture.png"
		bad_capture.write_bytes(tiny_png(3, 3, (20, 40, 80)))
		capture["path"] = "bad_capture.png"
		capture["sha256"] = hashlib.sha256(bad_capture.read_bytes()).hexdigest()
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("valid 8-bit PNG matching context.viewport" in item for item in errors))

	def test_hash_and_repository_escape_are_invalid(self) -> None:
		data = copy.deepcopy(self.data)
		data["assets"][0]["source"] = {"path": "../outside.png", "sha256": "0" * 64}
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("escapes repository" in item for item in errors))

	def test_claimed_owner_approval_requires_hashed_evidence(self) -> None:
		data = copy.deepcopy(self.data)
		data["approvals"]["owner"] = {"approved": True}
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("approvals.owner.evidence" in item for item in errors))

	def test_five_requires_all_external_acceptance(self) -> None:
		data = copy.deepcopy(self.data)
		review = data["assets"][0]["reviews"]["candidate"]
		review["dimensions"] = dict.fromkeys(DIMENSIONS, 5.0)
		review["score"] = 5.0
		_, blockers = audit_data(data, self.root)
		self.assertTrue(any("score 5" in item for item in blockers))

	def test_missing_scope_asset_is_invalid(self) -> None:
		data = copy.deepcopy(self.data)
		data["scope"]["surfaces"][0]["live_asset_ids"] = ["missing"]
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("cover every asset exactly once" in item for item in errors))

	def test_null_dimension_needs_reason_and_does_not_auto_score(self) -> None:
		data = copy.deepcopy(self.data)
		review = data["assets"][0]["reviews"]["candidate"]
		review["dimensions"]["animation"] = None
		review["score"] = 4.5
		errors, _ = audit_data(data, self.root)
		self.assertTrue(any("NA reason" in item for item in errors))
		review["na_reasons"]["animation"] = "static background"
		data["assets"][0]["role"] = "static prop"
		review["object_classification"] = "static_object"
		self.assertEqual(([], []), audit_data(data, self.root))

	def test_candidate_na_is_restricted_to_static_animation(self) -> None:
		data = copy.deepcopy(self.data)
		review = data["assets"][0]["reviews"]["candidate"]
		review["dimensions"]["finish"] = None
		review["na_reasons"]["finish"] = "not applicable"
		self.assertTrue(any("candidate NA is allowed only" in item for item in audit_data(data, self.root)[1]))


if __name__ == "__main__":
	unittest.main()
