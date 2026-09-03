"""Build the Day One Grok visual-handoff archive packets.

This is intentionally deterministic. Generated bitmap work is supplied by the
image-generation workflow; this tool copies approved authorities, preserves the
written handoffs byte-for-byte, records hashes/provenance, and emits the one-link
GitHub README for each scene.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "assets_src" / "cinematics"
SOURCE_COMMIT = "e2c477f880e0a60ceb91aa32fef133b2566d4d61"
GUIDE_COMMIT = "3af5a8eb7110dab2381c7d0a73b27b880d35e84a"
REPO_URL = "https://github.com/Ebonyks/mermaid-roshan-reef"
SHARED_SOURCE = ROOT / "design" / "grok_day_one_video_handoffs_2026-08-30" / "00_SHARED_STYLE_AND_CHARACTER_REFERENCE.txt"
SLATE_SOURCE = ROOT / "design" / "day_one_cinematic_slate_2026-08-30.json"
LICENSE_PATH = ROOT / "ASSET_LICENSES.md"
LICENSE_BEGIN = "<!-- DAY_ONE_GROK_VISUAL_HANDOFFS_2026-09-02_BEGIN -->"
LICENSE_END = "<!-- DAY_ONE_GROK_VISUAL_HANDOFFS_2026-09-02_END -->"


SCENES: list[dict[str, Any]] = [
	{"id":"D1-C00","slug":"d1_c00_opening_flight_visual_v1","title":"Opening Flight — Roshan and Daddy","guide":"D1-C00_OPENING_FLIGHT.txt","location":"assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png","characters":["roshan","daddy"],"objects":["git:docs/grok_animation_series_project/modules/opening_flight_to_sky_lagoon/references/06_AIRPLANE_EXACT.png"]},
	{"id":"D1-C01","slug":"d1_c01_lagoon_landing_castle_approach_visual_v1","title":"Lagoon Landing and Castle Approach","guide":"D1-C01_LAGOON_LANDING_AND_CASTLE_APPROACH.txt","location":"assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png","characters":["roshan","daddy"],"objects":["git:docs/grok_animation_series_project/modules/opening_flight_to_sky_lagoon/references/06_AIRPLANE_EXACT.png","assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png","assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/pearl_castle_exterior_turnaround_v2.png"]},
	{"id":"D1-C02","slug":"d1_c02_first_dirty_castle_discovery_visual_v1","title":"First Dirty Castle Discovery","guide":"D1-C02_FIRST_DIRTY_CASTLE_DISCOVERY.txt","location":"assets/flats/castle/main_hall_2screen/main_hall_screen_a_room_led_master.png","characters":["roshan","daddy"],"objects":["assets/flats/castle/main_hall_2screen/main_hall_screen_b_room_led_master.png","assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_bubble_bath.png"]},
	{"id":"D1-C03","slug":"d1_c03_bathroom_dirty_entry_visual_v1","title":"Bubble Bathroom — Dirty Entry","guide":"D1-C03_BATHROOM_DIRTY_ENTRY.txt","location":"assets/flats/castle/rooms/room_bubble_bath_dirty_day_one.png","characters":["roshan","swimming_bunny"],"objects":["assets/castle/day_one_pool/activities/cleanup_basket.png","assets/castle/dirty_cleanup_2d/targets/target_sink_grime_v1.png","assets/castle/dirty_cleanup_2d/targets/target_tub_grime_v1.png"]},
	{"id":"D1-C04","slug":"d1_c04_bathroom_restored_visual_v1","title":"Bubble Bathroom — Restored","guide":"D1-C04_BATHROOM_RESTORED.txt","location":"assets/flats/castle/rooms/room_bubble_bath_background.png","characters":["roshan","swimming_bunny"],"objects":["assets/flats/castle/rooms/room_bubble_bath_dirty_day_one.png","assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png","assets/castle/day_one_art_studio/magic_cleaning_brush.png"]},
	{"id":"D1-C05","slug":"d1_c05_pool_dirty_discovery_visual_v1","title":"Sparkle Pool — Dirty Discovery","guide":"D1-C05_POOL_DIRTY_DISCOVERY.txt","location":"assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png","characters":["roshan","swimming_bunny"],"objects":["assets/castle/day_one_pool/pool_algae_trash.png","assets/castle/day_one_pool/waterfall_clogged_turgid.png","assets/castle/day_one_pool/seahorse_sick.png","assets/castle/day_one_pool/activities/seahorse_mouth_trash.png"]},
	{"id":"D1-C06","slug":"d1_c06_pool_purification_rumi_hug_visual_v1","title":"Sparkle Pool — Purification, Rumi and Hug","guide":"D1-C06_POOL_DUAL_PURIFICATION_RUMI_HUG.txt","location":"assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png","characters":["roshan","rumi"],"objects":["assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_waterfall_rest.png","assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_seahorse_fountain_rest.png","assets/castle/day_one_pool/activities/seahorse_mouth_trash.png"]},
	{"id":"D1-C07","slug":"d1_c07_stuffie_dirty_discovery_visual_v1","title":"Stuffie Room — Dirty Discovery","guide":"D1-C07_STUFFIE_DIRTY_DISCOVERY.txt","location":"assets/flats/castle/rooms/room_playroom_background.png","characters":["roshan","baby_eagle_pinned","playroom_bunny"],"objects":["assets/flats/castle/rooms/room_playroom_item_play_tent.png","assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png"]},
	{"id":"D1-C08","slug":"d1_c08_stuffie_restoration_visual_v1","title":"Stuffie Room — Basket and Wing-Blast Restoration","guide":"D1-C08_STUFFIE_RESTORATION.txt","location":"assets/flats/castle/rooms/room_playroom_background.png","characters":["roshan","baby_eagle_standing","playroom_bunny"],"objects":["assets/flats/castle/rooms/room_playroom_item_play_tent.png","assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png"]},
	{"id":"D1-C09","slug":"d1_c09_art_room_dirty_discovery_visual_v1","title":"Art Room — Spilled Supplies Discovery","guide":"D1-C09_ART_ROOM_DIRTY_DISCOVERY.txt","location":"assets/flats/castle/rooms/room_craft_room_background.png","characters":["roshan"],"objects":["assets/flats/castle/rooms/room_craft_room_front_left.png","assets/flats/castle/rooms/room_craft_room_front_right.png","assets/flats/castle/rooms/room_craft_room_item_idea_board.png","assets/flats/castle/rooms/room_craft_room_item_paint_table.png","assets/flats/castle/rooms/room_craft_room_item_palette.png","assets/flats/castle/rooms/room_craft_room_item_ribbon_rack.png","assets/castle/day_one_art_studio/loose_brush_bundle.png","assets/castle/day_one_art_studio/paint_bottle_pink.png","assets/castle/day_one_art_studio/paint_bottle_blue.png","assets/castle/day_one_art_studio/paint_cups.png","assets/castle/day_one_art_studio/grime_desk.png","assets/castle/day_one_art_studio/grime_left.png","assets/castle/day_one_art_studio/grime_right.png"]},
	{"id":"D1-C10","slug":"d1_c10_art_room_restored_visual_v1","title":"Art Room — Clean Desk Awakening","guide":"D1-C10_ART_ROOM_RESTORED.txt","location":"assets/flats/castle/rooms/room_craft_room_background.png","characters":["roshan"],"objects":["assets/flats/castle/rooms/room_craft_room_front_left.png","assets/flats/castle/rooms/room_craft_room_front_right.png","assets/flats/castle/rooms/room_craft_room_item_idea_board.png","assets/flats/castle/rooms/room_craft_room_item_paint_table.png","assets/flats/castle/rooms/room_craft_room_item_palette.png","assets/flats/castle/rooms/room_craft_room_item_ribbon_rack.png","assets/castle/day_one_art_studio/loose_brush_bundle.png","assets/castle/day_one_art_studio/paint_bottle_pink.png","assets/castle/day_one_art_studio/paint_bottle_blue.png","assets/castle/day_one_art_studio/paint_cups.png","assets/castle/day_one_art_studio/magic_cleaning_brush.png"]},
	{"id":"D1-C11","slug":"d1_c11_grand_puff_reveal_visual_v1","title":"Boss Door and Grand Puff Reveal","guide":"D1-C11_GRAND_PUFF_REVEAL.txt","location":"assets/flats/castle/main_hall_2screen/main_hall_screen_b_room_led_master.png","characters":["roshan","grand_puff"],"objects":["assets/flats/castle/main_hall_2screen/main_hall_screen_a_room_led_master.png","assets/sprites/dust_bunnies/boss/dust_bunny_boss_jump.png","assets/sprites/dust_bunnies/boss/dust_bunny_boss_laugh_vulnerable.png"]},
	{"id":"D1-C12","slug":"d1_c12_restored_castle_finale_visual_v1","title":"Day One Restored-Castle Celebration","guide":"D1-C12_RESTORED_CASTLE_FINALE.txt","location":"assets/flats/castle/main_hall_2screen/main_hall_screen_a_room_led_master.png","characters":["roshan","daddy","rumi","baby_eagle_standing","playroom_bunny","grand_puff","swimming_bunny"],"objects":["assets/flats/castle/main_hall_2screen/main_hall_screen_b_room_led_master.png"]},
	{"id":"D1-C13","slug":"d1_c13_grand_puff_friendship_completion_visual_v1","title":"Grand Puff Friendship Completion","guide":"D1-C13_GRAND_PUFF_FRIENDSHIP_COMPLETION.txt","location":"assets_src/cinematics/d1_c13_grand_puff_friendship_completion_visual_v1/location_authorities/DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png","characters":["roshan","daddy","baby_eagle_standing","rumi","grand_puff"],"objects":["assets/sprites/dust_bunnies/boss/dust_bunny_boss_laugh_vulnerable.png","assets/sprites/dust_bunnies/boss/dust_bunny_boss_implode.png"]},
]


CHARACTERS: dict[str, dict[str, Any]] = {
	"roshan":{"source":"assets/characters/roshan_25d/roshan_base.png","status":"approved_private_canon","traits":["child face and age","brown hair with rainbow section","pink top and tiara"],"anatomy":["exactly two arms and one continuous mer-tail"],"forbidden":["legs or shoes","adult redesign"]},
	"daddy":{"source":"assets_src/daddy_master.png","status":"approved_private_canon","traits":["adult crowned father","dark rectangular glasses","navy and gold clothing with teal cape"],"anatomy":["taller than Roshan with one continuous mer-tail"],"forbidden":["generic king","missing glasses or tail"]},
	"rumi":{"source":"assets_src/characters/rumi_2026-08-22/rumi_full_body_identity.png","status":"approved_private_canon","traits":["enormous violet braided ponytail","pointed ears and star-shell earrings","navy lavender gold-trim jacket"],"anatomy":["two arms and one aqua-to-violet mer-tail with coral split fin"],"forbidden":["rejected generic pool mermaid","legs or altered braid"]},
	"swimming_bunny":{"source":"assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png","status":"approved","traits":["round lavender aquatic fluff","spiral ear curls","pearl paws and large warm eyes"],"anatomy":["one coherent swimming creature without legs"],"forbidden":["land-bunny legs","duplicate or smoke form"]},
	"baby_eagle_pinned":{"source":"git:docs/grok_animation_series_project/characters/baby_eagle/BABY_EAGLE_PINNED_STATE.png","status":"approved_private_canon","traits":["turquoise yellow and pink child bird","approved beak and face","full spread wings"],"anatomy":["exactly one bird with two wings and two feet"],"forbidden":["backpack","cropped or duplicated body"]},
	"baby_eagle_standing":{"source":"git:docs/grok_animation_series_project/characters/baby_eagle/BABY_EAGLE_STANDING_IDENTITY.png","status":"approved_private_canon","traits":["turquoise yellow and pink child bird","approved beak and face","upright friendly posture"],"anatomy":["exactly one bird with two wings and two feet"],"forbidden":["backpack","cropped or duplicated body"]},
	"playroom_bunny":{"source":"git:docs/grok_animation_series_project/characters/playroom_dust_bunny/PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png","status":"approved","traits":["round lavender fluff","friendly eyes and blush","consistent curl silhouette"],"anatomy":["one intact round creature per bunny"],"forbidden":["smoke cloud","color-coded redesign"]},
	"grand_puff":{"source":"git:docs/grok_animation_series_project/characters/boss_dust_bunny/BOSS_DUST_BUNNY_IDENTITY.png","status":"approved","traits":["three-tier grey lavender body","huge spiral ears with pearl joints","plum eyes coral blush and compact grin"],"anatomy":["symmetrical ears, pearl paws and exactly two visible teeth"],"forbidden":["sharp monster teeth","missing tiers or asymmetrical ear redesign"]},
}


def sha256(path: Path) -> str:
	data = path.read_bytes()
	if path.suffix.lower() in {".json", ".md", ".txt"}:
		# Hash the canonical repository/archive form. Windows may expose these
		# tracked text files with CRLF even though Git and GitHub store LF.
		data = data.replace(b"\r\n", b"\n")
	return hashlib.sha256(data).hexdigest()


def image_dimensions(path: Path) -> list[int] | None:
	data = path.read_bytes()[:32]
	if data.startswith(b"\x89PNG\r\n\x1a\n"):
		return list(struct.unpack(">II", data[16:24]))
	try:
		from PIL import Image
		with Image.open(path) as image:
			return [image.width, image.height]
	except Exception:
		return None


def git_bytes(source: str) -> bytes:
	path = source.removeprefix("git:")
	return subprocess.check_output(["git", "show", f"{GUIDE_COMMIT}:{path}"], cwd=ROOT)


def copy_source(source: str, destination: Path) -> dict[str, Any]:
	destination.parent.mkdir(parents=True, exist_ok=True)
	if source.startswith("git:"):
		destination.write_bytes(git_bytes(source))
		return {"source_path": source.removeprefix("git:"), "source_commit": GUIDE_COMMIT}
	path = ROOT / source
	if not path.is_file():
		raise FileNotFoundError(path)
	shutil.copy2(path, destination)
	return {"source_path": source.replace("\\", "/"), "source_commit": SOURCE_COMMIT}


def safe_name(source: str) -> str:
	return Path(source.removeprefix("git:")).name


def parse_shots(text: str) -> list[dict[str, str]]:
	pattern = re.compile(r"^SHOT (D1-C\d\d-S\d\d) COPY BLOCK\s*$", re.MULTILINE)
	matches = list(pattern.finditer(text))
	shots: list[dict[str, str]] = []
	for index, match in enumerate(matches):
		end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
		body = text[match.end():end].strip()
		first = re.split(r"(?<=[.!?])\s+", body, maxsplit=1)[0]
		shots.append({"shot_id": match.group(1), "body": body, "visible_result": first})
	return shots


def asset_record(path: Path, packet: Path, role: str, source: dict[str, Any] | None = None, generation: dict[str, Any] | None = None) -> dict[str, Any]:
	rel = path.relative_to(packet).as_posix()
	record: dict[str, Any] = {
		"path": rel,
		"role": role,
		"media_type": "image/png" if path.suffix.lower() == ".png" else "text/plain",
		"dimensions": image_dimensions(path) if path.suffix.lower() in {".png", ".jpg", ".jpeg"} else None,
		"sha256": sha256(path),
		"license_provenance": "project-original generated reference art" if generation else "project-owned approved authority copied losslessly",
		"modifications": "none after generation" if generation else "lossless byte-for-byte copy",
		"appearance_authority": False if generation or "storyboard" in rel.lower() else True,
		"bound_reference_eligible": False if generation or "storyboard" in rel.lower() else True,
		"used_as_delivery_pixels": False,
	}
	if source:
		record.update(source)
	if generation:
		record["generation"] = generation
	return record


def generated_results(packet: Path) -> dict[str, Any]:
	path = packet / "storyboards" / "GENERATION_RESULTS.json"
	if not path.is_file():
		return {}
	return json.loads(path.read_text(encoding="utf-8"))


def selected_result(results: dict[str, Any], relative_path: str) -> dict[str, Any]:
	"""Return a selected generation record from either supported result schema."""
	legacy = results.get(Path(relative_path).name)
	if isinstance(legacy, dict):
		return legacy
	for item in results.get("selected", []):
		if isinstance(item, dict) and item.get("path") == relative_path:
			return item
	section_name = "environment" if relative_path.endswith("ENVIRONMENT_PERSPECTIVES.png") else "storyboard"
	section = results.get(section_name)
	if isinstance(section, dict) and section.get("accepted_path") == relative_path:
		return {
			"result_id": section.get("accepted_result_id", "unrecorded"),
			"attempt": max((item.get("attempt", 1) for item in section.get("attempts", []) if isinstance(item, dict)), default=1),
		}
	legacy_section_name = "environment_perspectives" if relative_path.endswith("ENVIRONMENT_PERSPECTIVES.png") else "storyboard"
	legacy_section = results.get(legacy_section_name)
	if isinstance(legacy_section, dict) and legacy_section.get("path") == relative_path:
		return {"result_id": legacy_section.get("result_id", "unrecorded"), "attempt": legacy_section.get("attempt", 1)}
	return {}


def build_scene(scene: dict[str, Any], slate: dict[str, Any], archive_commit: str | None) -> list[str]:
	packet = OUT_ROOT / scene["slug"]
	guide_dir = packet / "written_guide"
	story_dir = packet / "storyboards"
	ref_dir = packet / "handoff_art"
	guide_dir.mkdir(parents=True, exist_ok=True)
	story_dir.mkdir(parents=True, exist_ok=True)
	ref_dir.mkdir(parents=True, exist_ok=True)

	guide_source = SHARED_SOURCE.parent / scene["guide"]
	shared_target = guide_dir / "SHARED_STYLE_AND_CHARACTER_GUIDE.txt"
	scene_target = guide_dir / "SCENE_GUIDE.txt"
	shutil.copy2(SHARED_SOURCE, shared_target)
	shutil.copy2(guide_source, scene_target)
	guide_text = scene_target.read_text(encoding="utf-8")
	shots = parse_shots(guide_text)

	assets: list[dict[str, Any]] = []
	license_lines: list[str] = []
	location_target = ref_dir / "location" / safe_name(scene["location"])
	location_source = copy_source(scene["location"], location_target)
	assets.append(asset_record(location_target, packet, "approved_location_geography_authority", location_source))
	license_lines.append(f"- `{location_target.relative_to(ROOT).as_posix()}` — lossless packet copy of `{location_source['source_path']}`; project-owned approved location authority; protected/source original unchanged; non-runtime handoff reference only.")

	character_entries: list[dict[str, Any]] = []
	for character_id in scene["characters"]:
		definition = CHARACTERS[character_id]
		target = ref_dir / "characters" / f"{character_id}_{safe_name(definition['source'])}"
		source = copy_source(definition["source"], target)
		assets.append(asset_record(target, packet, f"approved_{character_id}_identity_authority", source))
		character_entries.append({
			"character_id": character_id,
			"status": definition["status"],
			"path": target.relative_to(packet).as_posix(),
			"sha256": sha256(target),
			"immutable_traits": definition["traits"],
			"anatomy_traits": definition["anatomy"],
			"forbidden_drift": definition["forbidden"],
		})
		license_lines.append(f"- `{target.relative_to(ROOT).as_posix()}` — lossless packet copy of `{source['source_path']}`; project-owned approved {character_id} identity authority; original unchanged; non-runtime handoff reference only.")

	for source_path in scene["objects"]:
		target = ref_dir / "objects" / safe_name(source_path)
		source = copy_source(source_path, target)
		assets.append(asset_record(target, packet, "approved_object_or_topology_authority", source))
		license_lines.append(f"- `{target.relative_to(ROOT).as_posix()}` — lossless packet copy of `{source['source_path']}`; project-owned object/topology authority; original unchanged; non-runtime handoff reference only.")

	results = generated_results(packet)
	for filename, role in (("ENVIRONMENT_PERSPECTIVES.png", "multi_angle_environment_narrative_reference_only"), ("SCENE_SHOT_BOARD.png", "shot_order_narrative_reference_only")):
		path = story_dir / filename
		if not path.is_file():
			continue
		result = selected_result(results, f"storyboards/{filename}") if isinstance(results, dict) else {}
		generation = {
			"tool": "FFmpeg deterministic contact-sheet assembly" if str(result.get("result_id", "")).startswith("runtime-") else "OpenAI built-in image generation",
			"result_id": result.get("result_id", "unrecorded"),
			"prompt_path": f"storyboards/{'PERSPECTIVE_PROMPT.txt' if filename.startswith('ENVIRONMENT') else 'STORYBOARD_PROMPT.txt'}",
			"attempt": result.get("attempt", 1),
		}
		record = asset_record(path, packet, role, generation=generation)
		if str(result.get("result_id", "")).startswith("runtime-"):
			record["license_provenance"] = "project-owned runtime capture evidence"
			record["modifications"] = "whole-frame contact-sheet assembly and labels only"
		assets.append(record)
		license_lines.append(f"- `{path.relative_to(ROOT).as_posix()}` — project-original complete flattened image generated with OpenAI built-in image generation (`{generation['result_id']}`); modifications: none after generation; narrative-reference-only, never bound generation or delivery pixels; provenance in sibling prompt/result records.")

	for target, source_path in ((shared_target, SHARED_SOURCE), (scene_target, guide_source)):
		assets.append(asset_record(target, packet, "exact_written_handoff_guide", {"source_path": source_path.relative_to(ROOT).as_posix(), "source_commit": SOURCE_COMMIT}))

	packet_slate = next(item for item in slate["movies"] if item["id"] == scene["id"])
	ordered_beats = [{"beat_id": shot["shot_id"], "trigger": "The shot begins from the authored inherited state.", "visible_result": shot["visible_result"]} for shot in shots]
	final_state = packet_slate["end_state"]
	story_contract = {
		"one_sentence_promise": f"{packet_slate['start_state']} becomes {final_state}.",
		"ordered_beats": ordered_beats,
		"forbidden_events": ["No premature payoff or scene-state transition.", "No identity, anatomy, cast-count, fixture-count, or room-topology drift."],
		"final_state": final_state,
	}

	source_documents = {
		"schema": "grok-visual-handoff-source-documents-v1",
		"movie_id": scene["id"],
		"documents": [
			{"path":"written_guide/SHARED_STYLE_AND_CHARACTER_GUIDE.txt","source_path":SHARED_SOURCE.relative_to(ROOT).as_posix(),"source_commit":SOURCE_COMMIT,"sha256":sha256(shared_target),"modifications":"lossless byte-for-byte copy"},
			{"path":"written_guide/SCENE_GUIDE.txt","source_path":guide_source.relative_to(ROOT).as_posix(),"source_commit":SOURCE_COMMIT,"sha256":sha256(scene_target),"modifications":"lossless byte-for-byte copy"},
		],
	}
	(guide_dir / "SOURCE_DOCUMENTS.json").write_text(json.dumps(source_documents, indent=2) + "\n", encoding="utf-8")
	assets.append(asset_record(guide_dir / "SOURCE_DOCUMENTS.json", packet, "written_source_provenance_and_hashes"))

	if (story_dir / "ENVIRONMENT_PERSPECTIVES.png").is_file() and (story_dir / "SCENE_SHOT_BOARD.png").is_file():
		review_path = story_dir / "VISUAL_REVIEW.json"
		if not review_path.is_file():
			review_path.write_text(json.dumps({
				"schema": "grok-visual-review-v1",
				"movie_id": scene["id"],
				"agent_prescreen": "pending",
				"human_decision": "pending",
				"perspective_gate": {"panel_count": 6, "geometry": "pending", "topology": "pending", "state": "pending"},
				"storyboard_gate": {"shot_count": len(shots), "cast_anatomy": "pending", "causality": "pending", "continuity": "pending"},
				"disposition": "narrative_only_not_pixel_reference"
			}, indent=2) + "\n", encoding="utf-8")
	for filename, role in (("PERSPECTIVE_PROMPT.txt", "exact_environment_generation_prompt"), ("STORYBOARD_PROMPT.txt", "exact_storyboard_generation_prompt"), ("ENVIRONMENT_PERSPECTIVES_PROMPT.txt", "exact_environment_generation_prompt_source_record"), ("SCENE_SHOT_BOARD_PROMPT.txt", "exact_storyboard_generation_prompt_source_record"), ("GENERATION_RESULTS.json", "generation_result_ids_and_attempts"), ("GENERATION_REVIEW.json", "luna_generation_self_review"), ("VISUAL_REVIEW.json", "sol_and_human_visual_review_record")):
		path = story_dir / filename
		if path.is_file():
			assets.append(asset_record(path, packet, role))

	# Preserve every additional non-self-referential packet file in the payload,
	# including rejected candidates and alternate exact prompt/provenance records.
	recorded_paths = {item["path"] for item in assets}
	self_files = {"README.md", "HANDOFF_PACKET.json", "IMAGINE_HANDOFF.json"}
	for path in sorted((item for item in packet.rglob("*") if item.is_file()), key=lambda item: item.relative_to(packet).as_posix()):
		rel = path.relative_to(packet).as_posix()
		if rel in recorded_paths or rel in self_files:
			continue
		if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
			if rel.startswith("handoff_art/runtime_boundary/"):
				record = asset_record(path, packet, "runtime_boundary_reference_only")
				record.update({"appearance_authority":False,"bound_reference_eligible":False,"used_as_delivery_pixels":False,"hud_present":True,"license_provenance":"project-owned Godot 4.7.2 runtime capture evidence","modifications":"whole-frame crop and normalization only; see CAPTURE_PROVENANCE.json"})
				license_lines.append(f"- `{path.relative_to(ROOT).as_posix()}` — project-owned Godot 4.7.2 runtime capture; whole-frame crop/normalization only; HUD-bearing boundary reference, never bound or delivery pixels.")
			elif path.name in {"ART_ROOM_FIXTURE_IDENTITY_SHEET.png", "FOUR_LOOSE_SUPPLY_IDENTITY_SHEET.png"}:
				record = asset_record(path, packet, "approved_derived_identity_sheet")
				record.update({"appearance_authority":True,"bound_reference_eligible":True,"used_as_delivery_pixels":False,"license_provenance":"project-owned approved source assets assembled losslessly in one identity sheet","modifications":"uniform scale, neutral padding, labels, and contact-sheet assembly only"})
				license_lines.append(f"- `{path.relative_to(ROOT).as_posix()}` — deterministic identity sheet from project-owned approved source assets; non-runtime generator reference only.")
			else:
				result_id = path.stem if path.stem.startswith("exec-") else "recorded_in_GENERATION_RESULTS.json"
				record = asset_record(path, packet, "rejected_or_supporting_generated_narrative_reference", generation={"tool":"OpenAI built-in image generation","result_id":result_id,"attempt":"see generation result record"})
				license_lines.append(f"- `{path.relative_to(ROOT).as_posix()}` — project-original complete flattened image generated with OpenAI built-in image generation; modifications: none after generation; rejected/supporting narrative-reference-only record, never bound generation or delivery pixels; provenance in packet generation records.")
		else:
			record = asset_record(path, packet, "supporting_prompt_generation_or_review_record")
			record["appearance_authority"] = False
			record["bound_reference_eligible"] = False
			record["license_provenance"] = "project-authored packet provenance record"
			record["modifications"] = "none; exact retained record"
		assets.append(record)

	payload_records = [f"{item['path']}|{item['sha256']}" for item in sorted(assets, key=lambda item: item["path"])]
	payload_sha = hashlib.sha256(("\n".join(payload_records) + "\n").encode()).hexdigest()
	packet_manifest = {
		"schema":"external-animation-visual-packet-v1",
		"packet_id":scene["slug"],
		"movie_id":scene["id"],
		"role":"self_contained_uploadable_reference_packet",
		"runtime_asset":False,
		"used_as_delivery_pixels":False,
		"payload_sha256":payload_sha,
		"payload_hash_formula":"SHA256 of UTF-8 sorted <relative_path>|<lowercase_sha256>\\n records",
		"authority_order":["approved location geography","approved character identities","approved objects/topology","generated perspective and storyboard sheets for narrative understanding only"],
		"warnings":["Generated sheets are narrative references only and may never be bound as Grok IMAGE_1 or delivery pixels.","Every motion shot still requires an approved clean first frame and accepted endpoint continuity."],
		"assets":assets,
	}
	(packet / "HANDOFF_PACKET.json").write_text(json.dumps(packet_manifest, indent=2) + "\n", encoding="utf-8")

	remote = None
	archive_status = "incomplete"
	if archive_commit:
		archive_status = "complete"
		remote = {
			"commit":archive_commit,
			"tree":f"{REPO_URL}/tree/{archive_commit}/assets_src/cinematics/{scene['slug']}",
			"manifest":f"https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/{archive_commit}/assets_src/cinematics/{scene['slug']}/HANDOFF_PACKET.json",
			"verified_via":"GitHub Contents API and immutable commit inspection",
			"verified_at":"2026-09-02",
		}
	handoff = {
		"schema":"imagine-handoff-v2",
		"handoff_id":scene["slug"],
		"archive_status":archive_status,
		"generation_status":"blocked",
		"delivery_status":"not_accepted",
		"shot_packets":[],
		"blocking_findings":["No shot has an owner-approved clean HUD-free complete opening frame.","No continuity-dependent shot binds the accepted complete end frame of its predecessor.","Generated perspective and storyboard sheets are narrative-only and cannot be bound as generation pixels."],
		"story_contract":story_contract,
		"character_authorities":character_entries,
		"location_authority":{"path":location_target.relative_to(packet).as_posix(),"sha256":sha256(location_target),"immutable_features":["fixed entrance and exit geography","fixed landmark and fixture order","consistent scale and navigable volume"],"forbidden_geometry":["no invented room, basin, doorway, platform, or fixture relocation"]},
	}
	if remote:
		handoff["archive_remote"] = remote
	(packet / "IMAGINE_HANDOFF.json").write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")

	story_image = "storyboards/SCENE_SHOT_BOARD.png"
	perspective_image = "storyboards/ENVIRONMENT_PERSPECTIVES.png"
	character_rows = "\n".join(f"| {entry['character_id']} | ![]({entry['path']}) | {'; '.join(entry['immutable_traits'])} | {'; '.join(entry['forbidden_drift'])} |" for entry in character_entries)
	shot_rows = "\n".join(f"| {shot['shot_id']} | {shot['visible_result']} |" for shot in shots)
	readme = f"""# {scene['id']} — {scene['title']}

> `ARCHIVE_COMPLETE`: {str(archive_status == 'complete').lower()}<br>
> `GENERATION_READY`: false<br>
> `DELIVERY_ACCEPTED`: false<br>
> Grok output remains motion/editorial reference until the independent full-frame delivery audit passes.

## Use this one-link handoff

1. Review the environment continuity sheet, storyboard, and character locks below.
2. Paste the shared guide once, then the scene guide.
3. Generate one shot job at a time with two to four separately approved pixel authorities.
4. Never upload either sheet below as `IMAGE_1` or as delivery pixels.

## Environment continuity and runtime state

![Environment continuity and runtime-state sheet]({perspective_image})

This sheet records the permitted location projection and state continuity. It is narrative/runtime evidence only and is not an approved shot opening frame.

## Shot-aligned storyboard

![Shot-aligned narrative storyboard]({story_image})

| Shot | Authored visible beat |
|---|---|
{shot_rows}

## Character reference guide

| Character | Approved identity | Immutable traits | Reject |
|---|---|---|---|
{character_rows}

## Location authority

![Approved location authority]({location_target.relative_to(packet).as_posix()})

- Fixed entrance/exit geography, landmark order, fixture count, and scale.
- Generated angles must describe one connected volume.
- Reject invented doors, basins, platforms, duplicated fixtures, or room rotation.

## Written guides

- [Shared style and character guide](written_guide/SHARED_STYLE_AND_CHARACTER_GUIDE.txt)
- [Exact scene setup and shot copy blocks](written_guide/SCENE_GUIDE.txt)
- [Source document hashes](written_guide/SOURCE_DOCUMENTS.json)

<details>
<summary>Exact scene guide — expand to copy</summary>

```text
{guide_text.rstrip()}
```
</details>

## Provenance and audit state

- [Archive manifest](HANDOFF_PACKET.json)
- [Imagine status contract](IMAGINE_HANDOFF.json)
- [Perspective prompt](storyboards/PERSPECTIVE_PROMPT.txt)
- [Storyboard prompt](storyboards/STORYBOARD_PROMPT.txt)
- [Generation result IDs](storyboards/GENERATION_RESULTS.json)

Both generated sheets are `appearance_authority:false`, `bound_reference_eligible:false`, and `used_as_delivery_pixels:false` in the archive manifest. Human owner review remains required before any generated angle becomes a production authority.
"""
	(packet / "README.md").write_text(readme, encoding="utf-8")
	return license_lines


def update_licenses(lines: list[str]) -> None:
	section = "\n".join([
		LICENSE_BEGIN,
		"## Day One Grok visual handoff packets (2026-09-02)",
		"",
		"Every file below is non-runtime handoff/reference material. Generated perspective and storyboard sheets are narrative-only and are never generation or delivery pixels.",
		"",
		*lines,
		LICENSE_END,
	])
	text = LICENSE_PATH.read_text(encoding="utf-8")
	if LICENSE_BEGIN in text and LICENSE_END in text:
		prefix, rest = text.split(LICENSE_BEGIN, 1)
		_, suffix = rest.split(LICENSE_END, 1)
		text = prefix.rstrip() + "\n\n" + section + suffix
	else:
		text = text.rstrip() + "\n\n" + section + "\n"
	LICENSE_PATH.write_text(text, encoding="utf-8")


def build_index(archive_commit: str | None) -> None:
	index_dir = OUT_ROOT / "day_one_grok_visual_handoffs_2026-09-02"
	index_dir.mkdir(parents=True, exist_ok=True)
	rows = []
	items = []
	for scene in SCENES:
		rows.append(f"| {scene['id']} | {scene['title']} | [Open complete visual handoff](../{scene['slug']}/README.md) |")
		items.append({"movie_id":scene["id"],"title":scene["title"],"packet":f"assets_src/cinematics/{scene['slug']}","readme":f"assets_src/cinematics/{scene['slug']}/README.md"})
	readme = """# Day One Grok visual handoffs — 2026-09-02

Each scene link is self-contained: newly generated multi-angle environment art, a newly generated shot-aligned storyboard, approved character/location/object references, exact written Grok blocks, hashes, provenance, and truthful readiness status.

| Scene | Title | Single-link handoff |
|---|---|---|
""" + "\n".join(rows) + "\n\nGenerated sheets are narrative references only. They are never Grok opening-frame authorities or delivery pixels.\n"
	(index_dir / "README.md").write_text(readme, encoding="utf-8")
	(index_dir / "INDEX.json").write_text(json.dumps({"schema":"day-one-grok-visual-handoff-index-v1","date":"2026-09-02","archive_commit":archive_commit,"claims":{"archive_complete":bool(archive_commit),"generation_ready":False,"delivery_accepted":False},"scenes":items}, indent=2) + "\n", encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--archive-commit", help="Full immutable content commit after remote verification")
	args = parser.parse_args()
	if args.archive_commit and not re.fullmatch(r"[0-9a-f]{40}", args.archive_commit):
		raise SystemExit("--archive-commit must be a full lowercase Git SHA")
	slate = json.loads(SLATE_SOURCE.read_text(encoding="utf-8"))
	license_lines: list[str] = []
	for scene in SCENES:
		license_lines.extend(build_scene(scene, slate, args.archive_commit))
	update_licenses(license_lines)
	build_index(args.archive_commit)
	print(f"BUILT|packets={len(SCENES)}|archive_commit={args.archive_commit or 'pending'}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
