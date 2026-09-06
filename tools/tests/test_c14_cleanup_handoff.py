from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_c14_cleanup_handoff import build, digest, validate


class C14CleanupHandoffTests(unittest.TestCase):
	def setUp(self):
		self.temp = tempfile.TemporaryDirectory()
		self.root = Path(self.temp.name)
		self.packet = self.root / "assets_src/cinematics/d1_c14_castle_team_cleanup_v1"
		self.packet.mkdir(parents=True)
		template = self.root / "design/templates/IMAGINE_SHOT_CARD_V1.md"
		template.parent.mkdir(parents=True, exist_ok=True)
		template.write_text("# Imagine shot card v1\n", encoding="utf-8")
		for relative in ("CINEMATIC_DIRECTION.md", "RUNTIME_SEAM_PLAN.md", "CHARACTER_LOCKS.json", "audit/DOWNLOADS_REUSE_REVIEW.md", "audit/SOL_VISUAL_REVIEW.md"):
			path = self.packet / relative
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_text("{}\n" if path.suffix == ".json" else "# Fixture\n", encoding="utf-8")
		assets = []
		for name, color in (("hall", "purple"), ("hero", "pink"), ("prop", "cyan")):
			path = self.root / "source" / f"{name}.png"
			path.parent.mkdir(parents=True, exist_ok=True)
			Image.new("RGB", (32, 18), color).save(path)
			assets.append({"id": name, "path": path.relative_to(self.root).as_posix(), "role": f"{name}_identity"})
		self._write("SOURCE_ASSETS.json", {"assets": assets})
		shots = []
		visuals = {}
		for index, duration in enumerate((5, 4, 5, 5, 6, 6), 1):
			sid = f"C14-S{index:02d}"
			count = duration * 24
			shots.append({"shot": sid, "title": f"shot {index}", "duration_s": duration,
				"phases": [{"range": [0, count // 2], "instruction": "the team begins one cleaning action", "state": "action"},
					{"range": [count // 2, count], "instruction": "the team settles at the clean endpoint", "state": "hold"}],
				"camera": "locked child-height oblique camera", "invariants": ["hall geometry fixed", "identities fixed"],
				"start": "one localized mess remains", "end": "that localized mess is clean", "cast": ["Roshan", "Daddy"],
				"zone": "hall", "sound": "gentle cleaning foley; no synthesized family voice",
				"negative": "HUD, text, extra cast, morphing, camera drift", "binding_ids": ["hall", "hero"],
				"editorial_start_s": sum((5, 4, 5, 5, 6, 6)[:index - 1])})
			first = self.packet / "first_frames" / f"{sid}.png"
			board = self.packet / "storyboards" / f"{sid}.png"
			first.parent.mkdir(parents=True, exist_ok=True); board.parent.mkdir(parents=True, exist_ok=True)
			Image.new("RGB", (64, 36), (index * 20, 20, 40)).save(first)
			Image.new("RGB", (64, 36), (20, index * 20, 40)).save(board)
			visuals[sid] = {"first_frame": first.relative_to(self.packet).as_posix(),
				"board": board.relative_to(self.packet).as_posix(), "review": "audit/reviews.json"}
		self._write("DESIGN.json", {"shots": shots})
		self._write("VISUALS.json", {"shots": visuals})
		reviews = {"assets": [{"path": row["first_frame"], "sha256": digest(self.packet / row["first_frame"]),
			"sol_decision": "RECOMMEND_APPROVAL", "human_decision": "pending"} for row in visuals.values()]}
		self._write("audit/reviews.json", reviews)
		for sid, selected in visuals.items():
			for kind, relative in (("OPENING", selected["first_frame"]), ("BOARD", selected["board"])):
				self._write(f"generation_records/{sid}_{kind}.json", {"output_path": relative,
					"output_sha256": digest(self.packet / relative), "prompt": f"generate {sid} {kind}",
					"prompt_sha256": __import__("hashlib").sha256(f"generate {sid} {kind}".encode()).hexdigest(),
					"input_images": [{"path": "source/hall.png", "sha256": digest(self.root / "source/hall.png")}],
					"attempt": 1, "generation_method": "test_fixture", "human_decision": "pending"})

	def tearDown(self):
		self.temp.cleanup()

	def _write(self, relative: str, value) -> None:
		path = self.packet / relative
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

	def test_build_is_deterministic_and_strictly_valid(self):
		first = build(self.packet, self.root, develop=True)
		self.assertTrue(first["ok"], first["findings"])
		manifest_hash = digest(self.packet / "HANDOFF_PACKET.json")
		second = build(self.packet, self.root, develop=True)
		self.assertTrue(second["ok"], second["findings"])
		self.assertEqual(manifest_hash, digest(self.packet / "HANDOFF_PACKET.json"))
		strict = validate(self.packet, self.root, strict=True)
		self.assertTrue(strict["ok"], strict["findings"])
		manifest = json.loads((self.packet / "HANDOFF_PACKET.json").read_text())
		self.assertEqual((manifest["shot_count"], manifest["duration_seconds"], manifest["target_frame_count"]), (6, 31, 744))
		self.assertFalse(manifest["archive_complete"] or manifest["generation_ready"] or manifest["delivery_accepted"])
		self.assertEqual(digest(self.root / "design/templates/IMAGINE_SHOT_CARD_V1.md"), digest(self.packet / "written_guide/IMAGINE_SHOT_CARD_V1.md"))

	def test_cards_bind_first_frame_plus_sources_never_board(self):
		build(self.packet, self.root, develop=True)
		for sid in (f"C14-S{i:02d}" for i in range(1, 7)):
			card = json.loads((self.packet / "shots" / sid / "SHOT_PACKET.json").read_text())
			self.assertEqual([r["id"] for r in card["bound_references"]], ["IMAGE_1", "IMAGE_2", "IMAGE_3"])
			self.assertTrue(all("storyboard" not in r["role"] for r in card["bound_references"]))
			self.assertFalse(card["generation_ready"] or card["delivery_accepted"])
			self.assertTrue((self.packet / "shots" / sid / "PROMPT.txt").read_text().rstrip().splitlines()[-1].startswith("Sound:"))

	def test_develop_allows_missing_visual_but_strict_fails(self):
		missing = self.packet / "storyboards/C14-S06.png"
		missing.unlink()
		result = build(self.packet, self.root, develop=True)
		self.assertTrue(result["ok"], result["findings"])
		strict = validate(self.packet, self.root, strict=True)
		self.assertFalse(strict["ok"])
		self.assertTrue(any("C14-S06: missing board" in finding for finding in strict["findings"]))

	def test_review_hash_mismatch_fails_closed(self):
		reviews = json.loads((self.packet / "audit/reviews.json").read_text())
		reviews["assets"][0]["sha256"] = "0" * 64
		self._write("audit/reviews.json", reviews)
		build(self.packet, self.root, develop=True)
		strict = validate(self.packet, self.root, strict=True)
		self.assertFalse(strict["ok"])
		self.assertTrue(any("C14-S01: exact output path/hash absent" in finding for finding in strict["findings"]))

	def test_repo_prefixed_generation_output_path_is_normalized(self):
		path = self.packet / "generation_records/C14-S02_OPENING.json"
		record = json.loads(path.read_text())
		record["output_path"] = "assets_src/cinematics/d1_c14_castle_team_cleanup_v1/" + record["output_path"]
		path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
		result = build(self.packet, self.root, develop=True)
		self.assertTrue(result["ok"], result["findings"])

	def test_changed_source_copy_is_rejected(self):
		build(self.packet, self.root, develop=True)
		Image.new("RGB", (32, 18), "red").save(self.root / "source/hall.png")
		with self.assertRaises(ValueError):
			build(self.packet, self.root, develop=True)

	def test_binding_count_fails_closed(self):
		design = json.loads((self.packet / "DESIGN.json").read_text())
		design["shots"][0]["binding_ids"] = ["hall"]
		self._write("DESIGN.json", design)
		with self.assertRaises(ValueError):
			build(self.packet, self.root, develop=True)

	def test_broken_generated_markdown_link_fails(self):
		build(self.packet, self.root, develop=True)
		with (self.packet / "APPROVAL_GALLERY.md").open("a", encoding="utf-8") as handle:
			handle.write("\n[broken](../first_frames/not-there.png)\n")
		result = validate(self.packet, self.root, strict=True)
		self.assertFalse(result["ok"])
		self.assertTrue(any("broken local markdown link" in finding for finding in result["findings"]))


if __name__ == "__main__":
	unittest.main()
