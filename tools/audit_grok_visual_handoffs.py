"""Blocking audit for the 13 Day One Grok visual handoff archives."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = ROOT / "assets_src" / "cinematics"
PACKETS = [
	"d1_c00_opening_flight_visual_v1",
	"d1_c01_lagoon_landing_castle_approach_visual_v1",
	"d1_c02_first_dirty_castle_discovery_visual_v1",
	"d1_c03_bathroom_dirty_entry_visual_v1",
	"d1_c04_bathroom_restored_visual_v1",
	"d1_c05_pool_dirty_discovery_visual_v1",
	"d1_c06_pool_purification_rumi_hug_visual_v1",
	"d1_c07_stuffie_dirty_discovery_visual_v1",
	"d1_c08_stuffie_restoration_visual_v1",
	"d1_c09_art_room_dirty_discovery_visual_v1",
	"d1_c10_art_room_restored_visual_v1",
	"d1_c11_grand_puff_reveal_visual_v1",
"d1_c12_restored_castle_finale_visual_v1",
"d1_c13_grand_puff_friendship_completion_visual_v1",
]
REQUIRED = [
	"README.md",
	"HANDOFF_PACKET.json",
	"IMAGINE_HANDOFF.json",
	"written_guide/SHARED_STYLE_AND_CHARACTER_GUIDE.txt",
	"written_guide/SCENE_GUIDE.txt",
	"written_guide/SOURCE_DOCUMENTS.json",
	"storyboards/ENVIRONMENT_PERSPECTIVES.png",
	"storyboards/SCENE_SHOT_BOARD.png",
	"storyboards/PERSPECTIVE_PROMPT.txt",
	"storyboards/STORYBOARD_PROMPT.txt",
	"storyboards/GENERATION_RESULTS.json",
	"storyboards/VISUAL_REVIEW.json",
]


def digest(path: Path) -> str:
	h = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			h.update(chunk)
	return h.hexdigest()


def main() -> int:
	errors: list[str] = []
	for name in PACKETS:
		packet = PACKET_ROOT / name
		for relative in REQUIRED:
			if not (packet / relative).is_file():
				errors.append(f"{name}: missing {relative}")
		if errors and any(item.startswith(f"{name}:") for item in errors):
			continue
		manifest = json.loads((packet / "HANDOFF_PACKET.json").read_text(encoding="utf-8"))
		by_path = {item.get("path"): item for item in manifest.get("assets", []) if isinstance(item, dict)}
		for relative in ("storyboards/ENVIRONMENT_PERSPECTIVES.png", "storyboards/SCENE_SHOT_BOARD.png"):
			item = by_path.get(relative)
			if not item:
				errors.append(f"{name}: manifest omits {relative}")
				continue
			if item.get("sha256") != digest(packet / relative):
				errors.append(f"{name}: hash mismatch for {relative}")
			for flag in ("appearance_authority", "bound_reference_eligible", "used_as_delivery_pixels"):
				if item.get(flag) is not False:
					errors.append(f"{name}: {relative} must set {flag}=false")
		readme = (packet / "README.md").read_text(encoding="utf-8")
		for token in ("ENVIRONMENT_PERSPECTIVES.png", "SCENE_SHOT_BOARD.png", "SCENE_GUIDE.txt", "Character reference guide"):
			if token not in readme:
				errors.append(f"{name}: README omits {token}")
		results = json.loads((packet / "storyboards" / "GENERATION_RESULTS.json").read_text(encoding="utf-8"))
		disposition = results.get("output_disposition", results.get("storyboard_disposition"))
		if disposition is None:
			review_record = json.loads((packet / "storyboards" / "VISUAL_REVIEW.json").read_text(encoding="utf-8"))
			disposition = review_record.get("disposition")
		if isinstance(disposition, dict):
			disposition = disposition.get("role")
		if disposition not in {"narrative_reference_only", "narrative_only_not_pixel_reference"}:
			errors.append(f"{name}: generation results must declare narrative_reference_only")
		selected_records = results.get("selected", [])
		if not selected_records:
			selected_records = []
			for section_name in ("environment", "storyboard"):
				section = results.get(section_name)
				if isinstance(section, dict):
					selected_records.append({"path": section.get("accepted_path"), "sha256": section.get("sha256"), "prompt_path": section.get("prompt_path"), "prompt_sha256": section.get("prompt_sha256")})
		for selected in selected_records:
			if not isinstance(selected, dict):
				errors.append(f"{name}: malformed selected generation record")
			continue
			for key in ("path", "prompt_path"):
				relative = selected.get(key)
				if not isinstance(relative, str) or not (packet / relative).is_file():
					errors.append(f"{name}: selected record has missing {key} {relative!r}")
				continue
				expected_key = "sha256" if key == "path" else "prompt_sha256"
				if selected.get(expected_key) != digest(packet / relative):
					errors.append(f"{name}: selected record hash mismatch for {relative}")
		review = json.loads((packet / "storyboards" / "VISUAL_REVIEW.json").read_text(encoding="utf-8"))
		if review.get("agent_prescreen") != "accepted":
			errors.append(f"{name}: agent prescreen is not accepted")
		if review.get("human_decision") not in {"pending", "accepted"}:
			errors.append(f"{name}: human_decision must be pending or accepted")
		for asset in manifest.get("assets", []):
			if not isinstance(asset, dict):
				continue
			relative = asset.get("path")
			if not isinstance(relative, str) or not (packet / relative).is_file():
				errors.append(f"{name}: manifest asset missing {relative!r}")
				continue
			if not re.fullmatch(r"[0-9a-f]{64}", str(asset.get("sha256", ""))) or asset.get("sha256") != digest(packet / relative):
				errors.append(f"{name}: manifest asset hash invalid for {relative}")
		print(f"GROK_VISUAL|PACKET|{name}|{'PASS' if not any(item.startswith(name + ':') for item in errors) else 'FAIL'}")
	if errors:
		for error in errors:
			print(f"GROK_VISUAL|ERROR|{error}")
		print("GROK_VISUAL|RESULT|FAIL")
		return 1
	print("GROK_VISUAL|RESULT|ALL OK")
	return 0


if __name__ == "__main__":
	sys.exit(main())
