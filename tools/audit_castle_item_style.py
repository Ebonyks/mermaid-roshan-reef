"""Inventory and score Pearl Castle item art against the 4.5/5 style gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ROOM_DIR = ROOT / "assets" / "flats" / "castle" / "rooms"
AUDIT_DIR = ROOT / "audit" / "castle_sprite3d"
JSON_PATH = AUDIT_DIR / "castle_item_style_audit.json"
MARKDOWN_PATH = ROOT / "FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md"
CONTACT_PATH = AUDIT_DIR / "castle_item_style_accepted_contact.png"
MAIN_HALL_PROOF_PATH = AUDIT_DIR / "main_hall_item_style_replacement_composite.png"
THRESHOLD = 4.5

# Scores are visual-review judgments against the approved Pearl Castle room
# set, not image-quality metrics. Each final score averages palette harmony,
# navy/gold outline language, rounded shell/pearl shapes, painted texture, and
# room/perspective fit.
SCORES: dict[tuple[str, str], tuple[float, str]] = {
	("bubble_bath", "bathtub"): (4.8, "Strong shell silhouette and aqua/coral finish."),
	("bubble_bath", "sink"): (4.7, "Matches the bathtub material and gold-trim language."),
	("bubble_bath", "toilet"): (4.7, "Readable child-scale prop with the same pearl finish."),
	("craft_room", "idea_board"): (4.8, "Excellent shell frame, pastel notes, and room fit."),
	("craft_room", "paint_table"): (4.6, "Consistent rounded furniture and paint palette."),
	("craft_room", "palette"): (4.6, "Rich craft detail; broad source-pixel ownership is intentional."),
	("kitchen", "sink"): (4.7, "Shell basin and coral dressing match the castle vocabulary."),
	("kitchen", "pan_1"): (4.7, "Distinct copper pan silhouette remains readable at touch scale."),
	("kitchen", "pan_2"): (4.7, "Distinct copper pan silhouette remains readable at touch scale."),
	("kitchen", "pan_3"): (4.7, "Distinct copper pan silhouette remains readable at touch scale."),
	("kitchen", "pan_4"): (4.7, "Distinct copper pan silhouette remains readable at touch scale."),
	("kitchen", "oven"): (4.8, "Large cream-and-gold oven is a clear child-readable cooking prop."),
	("kitchen", "fridge"): (4.9, "Mint shell refrigerator is a strong focal portal with coherent materials."),
	("library", "magic_book"): (4.8, "Excellent magical focal object with restrained glow."),
	("library", "pearl_lamp"): (4.6, "Shell light and lavender chair fragment remain coherent."),
	("library", "pearl_table"): (4.7, "Rounded pearl furniture with matching cream/gold edgework."),
	("main_hall", "throne"): (4.8, "Approved throne identity retained exactly."),
	("main_hall", "fountain_left"): (3.3, "Legacy flat white pedestal lacks the newer shell detail and finish."),
	("main_hall", "fountain_right"): (3.3, "Legacy flat white pedestal lacks the newer shell detail and finish."),
	("mermaid_pool", "seahorse_fountain"): (4.9, "Readable seahorse fountain replaces the ambiguous pipe fixture."),
	("mermaid_pool", "flower_float"): (4.6, "Simple but coherent pastel flower and painted water."),
	("mermaid_pool", "waterfall"): (4.8, "High-detail shell arch and rainbow water focal object."),
	("opera_hall", "chandelier"): (4.7, "Gold/pearl lighting motif matches Main Hall architecture."),
	("opera_hall", "curtains"): (4.8, "Strong rainbow-shell entrance and navy arch language."),
	("opera_hall", "stage_star"): (4.5, "Minimal prop, but silhouette and gold/navy palette meet the gate."),
	("playroom", "blocks"): (4.5, "Small readable toy using the room's shell-pastel palette."),
	("playroom", "stacking_toy"): (4.7, "Rounded silhouette, clear value grouping, child-readable scale."),
	("playroom", "stuffie_nook"): (4.9, "Best-in-set characterful shell alcove with cohesive stuffies."),
}

REPLACEMENTS = {
	("main_hall", "fountain_left"): {
		"path": "room_main_hall_item_fountain_left_v2.png",
		"score": 4.7,
		"reason": (
			"Tight-alpha extraction of the richer shell fountain already "
			"painted in the approved dressed Main Hall concept; downsampled "
			"once to the established 1024-wide runtime scale."),
	},
	("main_hall", "fountain_right"): {
		"path": "room_main_hall_item_fountain_right_v2.png",
		"score": 4.7,
		"reason": (
			"Mirrored copy of the same existing dressed Main Hall fountain "
			"extraction; no new object design."),
	},
}

FOREGROUND_PAIR_SCORES = {
	"bubble_bath": 4.7,
	"craft_room": 4.6,
	"kitchen": 4.8,
	"library": 4.7,
	"main_hall": 4.5,
	"mermaid_pool": 4.8,
	"opera_hall": 4.8,
	"playroom": 4.8,
}


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _asset_record(path: Path) -> dict[str, object]:
	with Image.open(path) as image:
		rgba = image.convert("RGBA")
		alpha = rgba.getchannel("A")
		bounds = alpha.getbbox()
		alpha_pixels = sum(alpha.histogram()[1:])
		return {
			"path": path.relative_to(ROOT).as_posix(),
			"dimensions": list(image.size),
			"mode": rgba.mode,
			"alpha_bounds": list(bounds) if bounds else None,
			"alpha_pixels": alpha_pixels,
			"sha256": _sha256(path),
		}


def _build_contact(records: list[dict[str, object]]) -> None:
	columns = 4
	rows = (len(records) + columns - 1) // columns
	cell_width = 300
	cell_height = 240
	title_height = 44
	canvas = Image.new(
		"RGB", (columns * cell_width, title_height + rows * cell_height),
		(246, 244, 255))
	draw = ImageDraw.Draw(canvas)
	font = ImageFont.load_default()
	draw.text(
		(10, 12),
		"PEARL CASTLE TOUCH ITEMS - EFFECTIVE 4.5/5+ RUNTIME SET",
		fill=(35, 31, 91), font=font)
	for index, record in enumerate(records):
		row, column = divmod(index, columns)
		x_pos = column * cell_width
		y_pos = title_height + row * cell_height
		path = ROOT / str(record["effective"]["path"])
		image = Image.open(path).convert("RGBA")
		max_width = cell_width - 20
		max_height = cell_height - 42
		scale = min(max_width / image.width, max_height / image.height, 1.5)
		preview = image.resize(
			(max(1, round(image.width * scale)),
			 max(1, round(image.height * scale))),
			Image.Resampling.LANCZOS)
		checker = Image.new("RGB", (max_width, max_height), (236, 232, 248))
		checker_draw = ImageDraw.Draw(checker)
		for check_y in range(0, max_height, 16):
			for check_x in range(0, max_width, 16):
				if (check_x // 16 + check_y // 16) % 2:
					checker_draw.rectangle(
						(check_x, check_y, check_x + 15, check_y + 15),
						fill=(220, 215, 239))
		checker.paste(
			preview,
			((max_width - preview.width) // 2,
			 (max_height - preview.height) // 2),
			preview)
		canvas.paste(checker, (x_pos + 10, y_pos))
		label = (
			f"{record['room']} / {record['item']}  "
			f"{record['effective_score']:.1f}")
		draw.text(
			(x_pos + 10, y_pos + max_height + 6), label,
			fill=(35, 31, 91), font=font)
	canvas.save(CONTACT_PATH, optimize=True)


def _build_main_hall_proof() -> None:
	"""Reconstruct the current Main Hall resting layers for visual QA only."""
	canvas = Image.open(
		ROOM_DIR / "room_main_hall_background_v2.png").convert("RGBA")
	for filename, position in (
			("room_main_hall_item_throne.png", (430, 150)),
			("room_main_hall_front_left.png", (0, 0)),
			("room_main_hall_front_right.png", (750, 0)),
			("room_main_hall_item_fountain_left_v2.png", (88, 371)),
			("room_main_hall_item_fountain_right_v2.png", (722, 371)),
	):
		layer = Image.open(ROOM_DIR / filename).convert("RGBA")
		canvas.alpha_composite(layer, position)
	canvas.convert("RGB").save(MAIN_HALL_PROOF_PATH, optimize=True)


def main() -> None:
	AUDIT_DIR.mkdir(parents=True, exist_ok=True)
	records: list[dict[str, object]] = []
	for (room, item), (score, finding) in SCORES.items():
		legacy_path = ROOM_DIR / f"room_{room}_item_{item}.png"
		replacement = REPLACEMENTS.get((room, item))
		effective_path = (
			ROOM_DIR / str(replacement["path"])
			if replacement else legacy_path)
		effective_score = (
			float(replacement["score"]) if replacement else score)
		records.append({
			"room": room,
			"item": item,
			"legacy_score": score,
			"legacy_finding": finding,
			"legacy": _asset_record(legacy_path),
			"decision": "replace" if replacement else "reuse",
			"replacement_reason": (
				str(replacement["reason"]) if replacement else None),
			"effective_score": effective_score,
			"effective": _asset_record(effective_path),
			"passes_4_5": effective_score >= THRESHOLD,
		})
	records.sort(key=lambda record: (str(record["room"]), str(record["item"])))

	foreground_records: list[dict[str, object]] = []
	for room, pair_score in FOREGROUND_PAIR_SCORES.items():
		for side in ("left", "right"):
			path = ROOM_DIR / f"room_{room}_front_{side}.png"
			foreground_records.append({
				"room": room,
				"side": side,
				"pair_score": pair_score,
				"pair_passes_4_5": pair_score >= THRESHOLD,
				"note": (
					"Score applies to the composited left/right depth-dressing "
					"pair. Cards use non-overlapping source-pixel ownership and "
					"are not independent decorative objects."),
				**_asset_record(path),
			})

	replacement_evidence = [
		_asset_record(
			ROOM_DIR / "room_main_hall_item_fountain_left_v2.png"),
		_asset_record(
			ROOM_DIR / "room_main_hall_item_fountain_right_v2.png"),
		_asset_record(
			ROOM_DIR / "room_main_hall_background_v2.png"),
	]
	_build_contact(records)
	_build_main_hall_proof()
	manifest = {
		"schema": 1,
		"threshold": THRESHOLD,
		"rubric": [
			"palette harmony with approved Pearl Castle rooms",
			"navy/gold outline and edge language",
			"rounded shell/pearl shape language",
			"soft hand-painted texture and lighting",
			"room perspective, scale, and function fit",
		],
		"summary": {
			"logical_touch_items": len(records),
			"legacy_items_below_gate": sum(
				float(record["legacy_score"]) < THRESHOLD
				for record in records),
			"replacements": sum(
				record["decision"] == "replace" for record in records),
			"effective_items_below_gate": sum(
				not bool(record["passes_4_5"]) for record in records),
			"foreground_cards_inventoried": len(foreground_records),
			"all_effective_items_pass": all(
				bool(record["passes_4_5"]) for record in records),
			"all_foreground_pairs_pass": all(
				bool(record["pair_passes_4_5"])
				for record in foreground_records),
		},
		"items": records,
		"foreground_depth_dressing": foreground_records,
		"main_hall_clean_plate_repair": {
			"source": _asset_record(
				ROOM_DIR / "room_main_hall_background.png"),
			"effective": _asset_record(
				ROOM_DIR / "room_main_hall_background_v2.png"),
			"method": (
				"Deterministic same-source biharmonic fill restricted to the "
				"padded legacy fountain alpha silhouettes; original plate "
				"preserved."),
			"runtime_native_2k_gate": (
				"Still legacy 1024x576 and does not change the blocked "
				"environment-master gate."),
		},
		"contact_sheet": CONTACT_PATH.relative_to(ROOT).as_posix(),
		"main_hall_replacement_composite": (
			MAIN_HALL_PROOF_PATH.relative_to(ROOT).as_posix()),
	}
	JSON_PATH.write_text(
		json.dumps(manifest, indent=2, sort_keys=True) + "\n",
		encoding="utf-8")

	lines = [
		"# Fable Castle item style audit — 2026-07-28",
		"",
		"## Verdict",
		"",
		(
			f"All {len(records)} effective touch-item sprites now meet the subjective "
			"4.5/5 Pearl Castle style gate. The audit found two legacy "
			"outliers—the paired Main Hall pedestal fountains—and replaced "
			"them with existing approved bubble-fountain pixels. The original "
			"fountain files remain preserved."
		),
		"",
		"## Rubric",
		"",
		(
			"The score averages palette harmony, outline/edge language, "
			"rounded shell/pearl shape language, hand-painted texture, and "
			"room perspective/scale/function fit. A score below 4.5 is not "
			"eligible for runtime."
		),
		"",
		"## Touch-item inventory",
		"",
		"| Room | Item | Legacy | Decision | Effective | Runtime file |",
		"|---|---|---:|---|---:|---|",
	]
	for record in records:
		lines.append(
			f"| {record['room']} | {record['item']} | "
			f"{float(record['legacy_score']):.1f} | {record['decision']} | "
			f"{float(record['effective_score']):.1f} | "
			f"`{record['effective']['path']}` |")
	lines.extend([
		"",
		"## Replacement notes",
		"",
		(
			"- `fountain_left_v2` is a tight-alpha extraction of the richer "
			"shell fountain already present in the approved dressed Main Hall "
			"concept. It is downsampled once to the established 1024-wide "
			"runtime scale; it is not enlarged."
		),
		(
			"- `fountain_right_v2` mirrors that same existing extraction; it "
			"does not introduce a new object design."
		),
		(
			"- `scripts/arena/castle_rooms_25d.gd` selects these two explicit "
			"textures while keeping item IDs, touch mapping, foreground-band "
			"behavior, animation, sound, and save behavior unchanged. Their "
			"Z=4.15 placement sits just ahead of Z=4.0 side dressing and avoids "
			"coplanar sorting."
		),
		(
			"- `room_main_hall_background_v2.png` repairs only the two vacated "
			"legacy-fountain silhouettes from surrounding pixels in the "
			"immutable room composite. The original clean plate is preserved. "
			"This remains a legacy 1024×576 structural plate and does not "
			"claim to pass the blocked native-2K environment gate."
		),
		"",
		"## Replacement asset evidence",
		"",
		"| File | Dimensions | SHA-256 |",
		"|---|---:|---|",
	])
	for evidence in replacement_evidence:
		lines.append(
			f"| `{evidence['path']}` | "
			f"{evidence['dimensions'][0]}×{evidence['dimensions'][1]} | "
			f"`{evidence['sha256']}` |")
	lines.extend([
		"",
		"## Foreground/depth-dressing consistency",
		"",
		(
			"All 16 foreground Sprite3D card files were inventoried. They are "
			"scored as eight composited room pairs because their masks divide "
			"non-overlapping source-pixel ownership; a single card (especially "
			"Craft-left) is not intended to read as a standalone prop."
		),
		"",
		"| Room | Pair score | Result |",
		"|---|---:|---|",
	])
	for room, score in FOREGROUND_PAIR_SCORES.items():
		lines.append(
			f"| {room} | {score:.1f} | "
			f"{'PASS' if score >= THRESHOLD else 'REPLACE'} |")
	lines.extend([
		"",
		"## Evidence",
		"",
		f"- Machine inventory: `{JSON_PATH.relative_to(ROOT).as_posix()}`",
		f"- Accepted contact sheet: `{CONTACT_PATH.relative_to(ROOT).as_posix()}`",
		(
			"- Main Hall resting-layer proof: "
			f"`{MAIN_HALL_PROOF_PATH.relative_to(ROOT).as_posix()}`"
		),
		(
			"- Exact dimensions, alpha bounds, alpha-pixel counts, and SHA-256 "
			"hashes are recorded for every item and foreground card."
		),
		"",
	])
	MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")
	print(json.dumps(manifest["summary"], indent=2))


if __name__ == "__main__":
	main()
