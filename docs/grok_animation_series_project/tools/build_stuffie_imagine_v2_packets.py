#!/usr/bin/env python3
"""Build the two narrative Stuffie Room boards and draft Imagine shot packets."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs" / "grok_animation_series_project"
GENERATED = Path.home() / ".codex" / "generated_images" / "01a02c53-b5a7-7090-9081-65bde45909c2"
OUTPUT = ROOT / "assets_src" / "cinematics"
DATE = "2026-08-29"


@dataclass(frozen=True)
class Shot:
	shot_id: str
	label: str
	duration: int
	result_file: str
	perspective: str
	refs: tuple[str, ...]
	camera: str
	prompt: str
	end_state: str


COMMON_REFS = {
	"dirty_front": "locations/stuffie_room/STUFFIE_ROOM_DIRTY_GEOGRAPHY.png",
	"clean_front": "locations/stuffie_room/STUFFIE_ROOM_CLEAN_GEOGRAPHY.png",
	"p01": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_01_LEFT_DOORWAY.png",
	"p02": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_02_RIGHT_DOORWAY.png",
	"p03": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_03_LOW_FLOOR.png",
	"p04": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_04_BALCONY.png",
	"p05": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_05_LEFT_BASKET.png",
	"p06": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_06_RIGHT_BASKET.png",
	"p07": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_07_CENTER_LIGHT.png",
	"p08": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_08_TENT_PEEK.png",
	"p09": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_09_REVERSE_ENTRANCE.png",
	"p10": "locations/stuffie_room/perspectives_dirty/STUFFIE_ROOM_DIRTY_ANGLE_10_REAR_RIGHT.png",
	"roshan": "characters/roshan/ROSHAN_FRONT_IDENTITY.png",
	"roshan_rear": "characters/roshan/ROSHAN_REAR_POSE_SHEET.png",
	"eagle_pinned": "characters/baby_eagle/BABY_EAGLE_PINNED_STATE.png",
	"eagle_standing": "characters/baby_eagle/BABY_EAGLE_STANDING_IDENTITY.png",
	"bunny_hop": "characters/playroom_dust_bunny/PLAYROOM_DUST_BUNNY_HOP_IDENTITY.png",
	"bunny_light": "characters/playroom_dust_bunny/MOTION_LIGHT_SWING.png",
}


MOVIES = {
	"day_one_stuffie_discovery_v2": {
		"movie_id": "SQ030_DIRTY_DISCOVERY_V2",
		"title": "MOVIE A — DIRTY ROOM DISCOVERY",
		"shots": (
			Shot("A00_TENT_ORIENTATION", "tent orientation", 3, "exec-1a445514-a614-4e14-ac1d-4794412447b4.png", "P08 tent peek", ("p08", "dirty_front"), "locked", """locked wide view from inside the plush tent on image_1.\n\n0.0–1.5s: the tent flap and one loose ribbon settle gently while dust motes drift through the dirty room.\n1.5–3.0s: the movement becomes still enough to read both overflowing baskets and the cluttered floor.\n\nkeep all room geometry and fixtures locked. preserve the dirty pastel room from image_1 and the lighting from image_2. no hud, no text, no characters, no dust bunnies, no extra fixtures, no camera drift, no morphing.\n\nend: the empty dirty room holds, with both foreground baskets readable.\nSound: soft fabric rustle and quiet playroom room tone; no protected voice synthesis.\n""", "The empty dirty room holds with both baskets readable."),
			Shot("A01_ROSHAN_ENTERS", "Roshan enters left", 4, "exec-c2800250-1a75-41f6-b6db-9cea78b35a16.png", "P01 left doorway", ("p01", "roshan"), "slow push-in", """slow push-in on the dirty stuffie room from image_1.\n\n0.0–2.0s: mermaid roshan takes two small steps in from screen-left, staying left of center.\n2.0–4.0s: she stops, her eyes widen, and one hand lifts toward her mouth as she sees the mess.\n\nkeep the room geometry, baskets, lights, and clutter locked. preserve roshan from image_2. no hud, no text, no baby eagle, no dust bunnies, no extra fixtures, no morphing, no identity or costume changes.\n\nend: roshan holds shocked at screen-left with the room fully visible.\nSound: two soft steps, a tiny surprised breath, and quiet room tone; no protected voice synthesis.\n""", "Roshan holds shocked at screen-left with the room visible."),
			Shot("A02_SHOCK_REVERSE", "shock reverse", 3, "exec-df1cc99c-9555-49d9-9e0d-907cd3ad0091.png", "P09 reverse entrance", ("p09", "roshan"), "locked", """locked reverse view toward the entrance from image_1.\n\n0.0–1.5s: roshan turns her face from the overflowing left basket toward the scattered stuffies.\n1.5–3.0s: her shoulders lift and her worried expression settles as she listens.\n\nkeep the doorway, baskets, shelves, lights, and clutter locked. preserve roshan from image_2. no hud, no text, no baby eagle, no dust bunnies, no extra fixtures, no camera drift, no morphing.\n\nend: roshan is still and alert between the two dirty baskets.\nSound: a faint toy rattle and quiet room tone; no protected voice synthesis.\n""", "Roshan is still and alert between the dirty baskets."),
			Shot("A03_CENTER_LIGHT_SWINGER", "one light swinger", 3, "exec-09e57218-d204-4e3d-b364-f1ff676bda0c.png", "P07 center light", ("p07", "roshan", "bunny_light"), "locked", """locked upward view of the center light from image_1.\n\n0.0–1.5s: exactly one lavender dust bunny swings once beneath the center light, gripping securely with its long ears.\n1.5–3.0s: roshan at lower-left tilts her chin up and follows the bunny with wide eyes.\n\nkeep all three lights and ceiling geometry locked. preserve roshan from image_2 and the lavender light-swing bunny from image_3. no hud, no text, no baby eagle, no additional bunnies, no extra fixtures, no camera drift, no morphing.\n\nend: the single bunny hangs beneath the center light while roshan looks up.\nSound: a soft ropey swish, a tiny fluffy squeak, and room tone; no protected voice synthesis.\n""", "One bunny hangs under the center light while Roshan looks up."),
			Shot("A04_GAZE_TO_FLOOR", "gaze to floor", 3, "exec-e1f45841-bfa8-4f37-94cc-3701a87a7cec.png", "P03 low floor", ("p03", "roshan", "eagle_pinned"), "gentle tilt down", """gentle tilt down through the low floor view from image_1.\n\n0.0–1.5s: roshan lowers her gaze from above toward a small golden wing tip entering the lower-right edge.\n1.5–3.0s: her shocked face softens into concern as the camera settles near floor level.\n\nkeep the dirty floor, baskets, shelves, and room geometry locked. preserve roshan from image_2 and the bag-free baby eagle from image_3. no hud, no text, no backpack, no visible dust bunnies, no extra fixtures, no morphing.\n\nend: roshan looks down with concern toward baby eagle just beyond frame-right.\nSound: a quiet feather rustle and softened room tone; no protected voice synthesis.\n""", "Roshan looks down toward Baby Eagle just beyond frame-right."),
			Shot("A05_PINNED_EAGLE_REVEAL", "pinned Eagle reveal", 4, "exec-c3310784-166e-40f7-9af3-6a609f5ee846.png", "P10 rear-right", ("p10", "eagle_pinned", "bunny_hop"), "slow push-in", """slow push-in on baby eagle low on the dirty floor from image_1.\n\n0.0–2.0s: the bag-free baby eagle blinks sadly with both wings spread on the rug.\n2.0–4.0s: exactly two lavender dust bunnies make small playful bounces, one on each separate wing, while eagle strains gently without injury.\n\nkeep the floor, furniture, and room geometry locked. preserve baby eagle from image_2 and both same-family lavender bunnies from image_3. no hud, no text, no backpack, no light bunny in frame, no additional bunnies, no injury, no morphing.\n\nend: baby eagle remains sad but safe, with one bunny on each wing.\nSound: two soft fluff boings, feather rustle, and quiet room tone; no protected voice synthesis.\n""", "Baby Eagle remains safe with one bunny on each wing."),
		),
	},
	"day_one_stuffie_basket_clean_v2": {
		"movie_id": "SQ040_BASKET_CLEAN_V2",
		"title": "MOVIE B — BASKET WAVE AND CLEAN REVEAL",
		"shots": (
			Shot("B01_DIRTY_CALM", "dirty calm", 3, "exec-9b415483-a158-4579-9b6b-7aecc48123ae.png", "P02 right doorway", ("p02", "roshan", "eagle_standing"), "locked", """locked wide view of the still-dirty room from image_1.\n\n0.0–1.5s: baby eagle stands upright and takes one relieved breath while roshan smiles from screen-left.\n1.5–3.0s: both characters hear a faint rustle and turn toward the foreground baskets.\n\nkeep the dirty room, clutter, baskets, lights, and geometry locked. preserve roshan from image_2 and the bag-free standing baby eagle from image_3. no hud, no text, no dust bunnies, no backpack, no extra fixtures, no morphing.\n\nend: roshan and baby eagle look toward the baskets in the still-dirty room.\nSound: soft feather settle, faint basket rustle, and room tone; no protected voice synthesis.\n""", "Roshan and Eagle look toward the baskets in the dirty room."),
			Shot("B02_LEFT_BASKET_WARNING", "left basket warning", 3, "exec-4a50e833-aab0-4f14-81f3-bd0919b08d2d.png", "P05 left basket", ("p05", "roshan", "eagle_standing"), "slow push-in", """slow push-in on the left foreground basket from image_1.\n\n0.0–1.5s: the stuffed toys and folded fabric in the left basket wiggle twice from something hidden underneath.\n1.5–3.0s: roshan and baby eagle turn toward the movement, but nothing emerges yet.\n\nkeep the basket position, dirty room, lights, and surrounding clutter locked. preserve roshan from image_2 and baby eagle from image_3. no hud, no text, no visible dust bunnies, no extra fixtures, no morphing.\n\nend: the left basket quivers once more while both heroes watch.\nSound: soft wicker creak, plush rustle, and room tone; no protected voice synthesis.\n""", "The left basket quivers while Roshan and Eagle watch."),
			Shot("B03_RIGHT_BASKET_WARNING", "right basket warning", 3, "exec-d8c11f80-473a-452e-abda-69f0e1fad7b8.png", "P06 right basket", ("p06", "roshan", "eagle_standing"), "slow push-in", """slow push-in on the right foreground basket from image_1.\n\n0.0–1.5s: the stuffed toys and folded fabric in the right basket wiggle twice from something hidden underneath.\n1.5–3.0s: roshan and baby eagle turn toward the movement, but nothing emerges yet.\n\nkeep the basket position, dirty room, lights, and surrounding clutter locked. preserve roshan from image_2 and baby eagle from image_3. no hud, no text, no visible dust bunnies, no extra fixtures, no morphing.\n\nend: the right basket quivers once more while both heroes watch.\nSound: soft wicker creak, plush rustle, and room tone; no protected voice synthesis.\n""", "The right basket quivers while Roshan and Eagle watch."),
			Shot("B04_FOUR_BUNNIES_EMERGE", "four emerge", 5, "exec-68fdf2db-2d69-4726-af7f-afa17932733a.png", "P04 balcony", ("p04", "eagle_standing", "bunny_hop"), "locked", """locked balcony view of both foreground baskets from image_1.\n\n0.0–2.0s: exactly two lavender dust bunnies spring from the left basket and exactly two spring from the right basket.\n2.0–5.0s: one bunny from each basket arcs upward toward separate lights while one from each basket arcs down toward opposite floor sides.\n\nkeep the room geometry, lights, baskets, and baby eagle locked. preserve baby eagle from image_2 and all four same-family lavender bunnies from image_3. no hud, no text, no fifth bunny, no wing bunnies, no bunny duplication, no extra fixtures, no morphing.\n\nend: all four individual bunnies are airborne on readable, separate paths.\nSound: four soft fluff pops, wicker rustle, and airy boings; no protected voice synthesis.\n""", "Four individual bunnies are airborne on separate paths."),
			Shot("B05_EAGLE_SETS_WINGS", "two lights, two floor", 3, "exec-1ec7b8f7-9d72-4131-86bc-95054ccfe7f6.png", "P01 left doorway", ("p01", "eagle_standing", "bunny_hop", "bunny_light"), "locked", """locked wide view of the exact four-bunny formation from image_1.\n\n0.0–1.5s: two lavender bunnies settle on separate lights and two settle on opposite floor sides, with no other bunnies present.\n1.5–3.0s: baby eagle plants both feet and draws both wings back for one broad flap.\n\nkeep the dirty room, fixtures, and exact two-light two-floor bunny split locked until eagle prepares. preserve baby eagle from image_2, floor bunnies from image_3, and light bunnies from image_4. no hud, no text, no fifth bunny, no bunny duplication, no extra fixtures, no morphing.\n\nend: baby eagle holds both wings drawn back against exactly four bunnies.\nSound: two soft landing poofs, feather draw, and room tone; no protected voice synthesis.\n""", "Eagle holds both wings back against exactly four bunnies."),
			Shot("B06_WING_BLAST_CLEAN_REVEAL", "wing gust cleans", 6, "exec-c0ba6c81-3955-4cde-a859-529df9fffa95.png", "matched front dirty and clean", ("dirty_front", "eagle_standing", "bunny_hop", "clean_front"), "locked", """locked front-wide view of the dirty room from image_1.\n\n0.0–2.0s: baby eagle completes one broad playful wing flap and a soft spiral gust catches exactly four intact lavender dust bunnies.\n2.0–4.0s: all four bunnies tumble safely together and fully exit through the upper-right edge before any room cleanup begins.\n4.0–6.0s: the trailing gust lifts loose scraps and dust, revealing the same room in its clean state from image_4.\n\nkeep the room geometry, windows, shelves, baskets, tent, and lights aligned. preserve baby eagle from image_2 and the four same-family bunnies from image_3. no hud, no text, no fifth bunny, no injury, no impact, no explosion, no extra fixtures, no camera drift, no morphing of characters.\n\nend: all four bunnies are off-screen and the room is fully clean.\nSound: broad feather whoosh, four soft surprised squeaks, paper flutter, and a gentle sparkle settle; no protected voice synthesis.\n""", "All four bunnies are off-screen and the room is fully clean."),
			Shot("B07_CLEAN_RESOLVE", "clean resolve", 3, "exec-4237233e-9bca-4d72-836c-0c3ef48c0449.png", "clean front", ("clean_front", "roshan", "eagle_standing"), "locked", """locked front-wide view of the fully clean room from image_1.\n\n0.0–1.5s: roshan claps once at screen-left while baby eagle stands proudly near center-right.\n1.5–3.0s: baby eagle gives one small happy wing flutter and both characters settle into a calm idle.\n\nkeep the clean room geometry, organized baskets, shelves, tent, and lights locked. preserve roshan from image_2 and baby eagle from image_3. no hud, no text, no dust bunnies, no clutter returning, no backpack, no extra fixtures, no morphing.\n\nend: roshan and baby eagle hold happily in the clean room with zero bunnies.\nSound: one soft clap, happy feather flutter, and bright room tone; no protected voice synthesis.\n""", "Roshan and Eagle hold happily in the clean room with zero bunnies."),
		),
	},
}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
	name = "arialbd.ttf" if bold else "arial.ttf"
	try:
		return ImageFont.truetype(name, size)
	except OSError:
		return ImageFont.load_default()


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def build_board(packet: Path, title: str, shots: tuple[Shot, ...]) -> Path:
	columns = 3 if len(shots) == 6 else 4
	rows = 2
	cell_w, image_h, caption_h = 640, 360, 54
	margin, title_h = 24, 72
	board = Image.new("RGB", (columns * cell_w + (columns + 1) * margin, title_h + rows * (image_h + caption_h) + (rows + 1) * margin), "#1f1635")
	draw = ImageDraw.Draw(board)
	draw.text((margin, 18), title, fill="#fff4df", font=font(30, True))
	for index, shot in enumerate(shots):
		row, column = divmod(index, columns)
		x = margin + column * (cell_w + margin)
		y = title_h + margin + row * (image_h + caption_h + margin)
		panel = Image.open(packet / "storyboards" / "panels" / f"{shot.shot_id}.png").convert("RGB")
		panel = ImageOps.fit(panel, (cell_w, image_h), method=Image.Resampling.LANCZOS)
		board.paste(panel, (x, y))
		draw.rectangle((x, y + image_h, x + cell_w, y + image_h + caption_h), fill="#fff4df")
		draw.text((x + 12, y + image_h + 8), f"{shot.shot_id} — {shot.label}", fill="#25183d", font=font(20, True))
	path = packet / "storyboards" / ("SQ030_DISCOVERY_SHOT_BOARD.png" if len(shots) == 6 else "SQ040_BASKET_CLEAN_SHOT_BOARD.png")
	board.save(path, format="PNG", optimize=True)
	return path


def build_packet(handoff_id: str, spec: dict[str, object]) -> None:
	packet = OUTPUT / handoff_id
	shots = spec["shots"]
	assert isinstance(shots, tuple)
	for directory in (packet / "handoff_art", packet / "storyboards" / "native_panels", packet / "storyboards" / "panels", packet / "shots"):
		directory.mkdir(parents=True, exist_ok=True)

	used_refs = sorted({key for shot in shots for key in shot.refs})
	for key in used_refs:
		source = DOCS / COMMON_REFS[key]
		destination = packet / "handoff_art" / f"{key.upper()}_{source.name}"
		shutil.copy2(source, destination)

	for shot in shots:
		source = GENERATED / shot.result_file
		native = packet / "storyboards" / "native_panels" / f"{shot.shot_id}_NATIVE.png"
		panel = packet / "storyboards" / "panels" / f"{shot.shot_id}.png"
		shutil.copy2(source, native)
		with Image.open(source) as image:
			ImageOps.fit(image.convert("RGB"), (1024, 576), method=Image.Resampling.LANCZOS).save(panel, format="PNG", optimize=True)
		shot_dir = packet / "shots" / shot.shot_id
		shot_dir.mkdir(parents=True, exist_ok=True)
		(shot_dir / "PROMPT.txt").write_text(shot.prompt, encoding="utf-8")
		bindings = []
		for index, key in enumerate(shot.refs, start=1):
			ref_source = DOCS / COMMON_REFS[key]
			ref_name = f"{key.upper()}_{ref_source.name}"
			bindings.append({
				"id": f"IMAGE_{index}",
				"role": "approved_clean_first_frame" if index == 1 else ("subject_identity" if key in {"roshan", "roshan_rear", "eagle_pinned", "eagle_standing"} else "object_or_material_identity"),
				"path": f"handoff_art/{ref_name}",
				"sha256": sha256(packet / "handoff_art" / ref_name),
				"hud_present": False,
				"human_decision": "pending",
			})
		write_json(shot_dir / "SHOT_PACKET_DRAFT.json", {
			"schema": "imagine-shot-packet-draft-v1",
			"movie_id": spec["movie_id"],
			"shot_id": shot.shot_id,
			"status": "DRAFT",
			"duration_seconds": shot.duration,
			"aspect_ratio": "16:9",
			"delivery_size": [1280, 720],
			"mode": "image_to_video",
			"output_disposition": "motion_reference_only",
			"bound_references": bindings,
			"camera": {"verb": shot.camera, "move_count": 0 if shot.camera == "locked" else 1},
			"end_state": shot.end_state,
			"prompt_path": f"shots/{shot.shot_id}/PROMPT.txt",
			"prompt_sha256": sha256(shot_dir / "PROMPT.txt"),
			"blocking_findings": ["IMAGE_1 is a layout candidate, not an owner-approved complete first frame", "all bound references require GitHub-open and human acceptance", "materialize SHOT_PACKET.json only after both findings are cleared"],
		})

	board_path = build_board(packet, str(spec["title"]), shots)
	plan_lines = [f"# {spec['title']} — one-shot Grok plan", "", "The board is narrative-only. Do not upload it as an image reference. Each row below is one independent image-to-video job.", "", "| Shot | Duration | Camera | Narrative beat |", "|---|---:|---|---|"]
	for shot in shots:
		plan_lines.append(f"| `{shot.shot_id}` | {shot.duration}s | {shot.camera} | {shot.label}; end: {shot.end_state} |")
	plan_lines.extend(["", "## Current gate", "", "The prose prompts and role-labeled reference candidates are prepared. Generation is intentionally blocked until the owner approves a complete, UI-free first frame for each shot and every referenced image is opened from its immutable GitHub URL. At that point, rename/materialize each `SHOT_PACKET_DRAFT.json` as a validator-compliant `SHOT_PACKET.json` and add it to `IMAGINE_HANDOFF.json`.", "", "Grok output remains motion reference only; delivery frames still require individual full-frame generation and review.", ""])
	(packet / "SHOT_PLAN.md").write_text("\n".join(plan_lines), encoding="utf-8")

	record_lines = [f"# {spec['title']} — storyboard generation record", "", f"- Generated: {DATE}", "- Method: OpenAI built-in ImageGen, complete flattened narrative panels", "- Use: narrative storyboard only; never a bound Grok pixel reference", "- Native generations are preserved unchanged; 1024×576 panels are whole-canvas Lanczos normalizations.", "- The result PNGs did not embed prompt metadata. The action/continuity direction used for each generation is preserved below with the tool result identifier.", "", "| Shot | Result identifier | Perspective authority | Direction |", "|---|---|---|---|"]
	for shot in shots:
		record_lines.append(f"| `{shot.shot_id}` | `{shot.result_file}` | {shot.perspective} | {shot.label}; {shot.end_state} |")
	record_lines.extend(["", "## Shared generation direction", "", "Create one complete, flattened 16:9 polished 2D storybook frame. Preserve the Stuffie Room geography and child-safe dirty or clean state from the named screenshot; preserve Mermaid Roshan, bag-free Baby Eagle, and lavender Playroom Dust Bunny identities from their approved references. Keep anatomy, costume, room fixtures, light count, basket count, and bunny count exact. No HUD, text, borders, captions, photorealism, 3D render, backpack eagle, new characters, extra bunnies, injury, impact, or explosion.", ""])
	(packet / "STORYBOARD_GENERATION_RECORD.md").write_text("\n".join(record_lines), encoding="utf-8")

	assets = []
	for path in sorted(packet.rglob("*")):
		if path.is_file() and path.name not in {"HANDOFF_PACKET.json", "IMAGINE_HANDOFF.json"}:
			assets.append({"path": path.relative_to(packet).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
	write_json(packet / "HANDOFF_PACKET.json", {
		"schema": "grok-storyboard-archive-v2",
		"handoff_id": handoff_id,
		"movie_id": spec["movie_id"],
		"created": DATE,
		"storyboard_disposition": "narrative_only_not_pixel_reference",
		"shot_count": len(shots),
		"storyboard_board": board_path.relative_to(packet).as_posix(),
		"assets": assets,
	})
	write_json(packet / "IMAGINE_HANDOFF.json", {
		"schema": "imagine-handoff-v1",
		"handoff_id": handoff_id,
		"archive_status": "incomplete",
		"generation_status": "blocked",
		"delivery_status": "not_accepted",
		"shot_packets": [],
		"blocking_findings": [
			"each storyboard panel is narrative-only and cannot be a bound pixel reference",
			"each shot still needs an owner-approved complete clean UI-free first frame",
			"all two-to-four role-labeled image bindings must be opened from immutable GitHub URLs and human accepted",
			"draft cards must be materialized as SHOT_PACKET.json only after those approvals",
		],
		"archive_remote": {},
	})


def main() -> None:
	missing = [str(GENERATED / shot.result_file) for spec in MOVIES.values() for shot in spec["shots"] if not (GENERATED / shot.result_file).is_file()]
	if missing:
		raise SystemExit("missing generated panels:\n" + "\n".join(missing))
	for handoff_id, spec in MOVIES.items():
		build_packet(handoff_id, spec)
	print("built", ", ".join(MOVIES))


if __name__ == "__main__":
	main()
