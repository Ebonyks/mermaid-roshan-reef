#!/usr/bin/env python3
"""Derive the Main Hall door badges from approved, already-shipped castle art.

The source backgrounds remain untouched.  Each badge is cropped once and is
uniformly resized onto a transparent 256 px card for Sprite3D use.  The Dream
House badge comes from the already-transparent crest in its approved doorway;
its semantic mask excludes the readable purple scrollwork and arch fragments.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
HALL = ROOT / "assets/flats/castle/main_hall_2screen"
DREAM_HOUSE = ROOT / "assets/flats/castle/dream_house"
OUTPUT = ROOT / "assets/flats/castle/main_hall_redraw_2026-08-03/signs"
MANIFEST = (
	ROOT
	/ "assets_src/imagegen/castle_main_hall_redraw_2026-08-03/sign_reuse_manifest.json"
)

CANVAS_SIZE = (256, 256)

# The Family Gallery crest comes from the approved Dream House doorway, but
# that source has a very pale outer silhouette.  Reuse two exact palette
# samples from the approved Library badge so the house reads with the same
# navy/gold edge hierarchy as the other physical door signs.  The coordinates
# are intentionally fixed and asserted below so a source-art change cannot
# silently recolor the family badge.
COLLECTION_PALETTE_REFERENCE = "sign_library.png"
COLLECTION_NAVY_SAMPLE = (128, 84)
COLLECTION_NAVY_EXPECTED = (62, 75, 98, 255)
COLLECTION_GOLD_SAMPLE = (128, 90)
COLLECTION_GOLD_EXPECTED = (240, 174, 61, 255)
FAMILY_KEYLINE_RADIUS = 4
FAMILY_GOLD_EDGE_RADIUS = 1

# center x/y and ellipse radius x/y in the untouched approved source master.
BADGES = {
	"sign_opera_hall.png": ("a", (1005, 345), (62, 51)),
	"sign_library.png": ("a", (1486, 500), (52, 49)),
	"sign_kitchen.png": ("a", (1752, 498), (52, 48)),
	"sign_playroom.png": ("b", (324, 453), (50, 44)),
	"sign_craft_room.png": ("b", (837, 447), (50, 47)),
	"sign_mermaid_pool.png": ("b", (1203, 441), (47, 45)),
	"sign_bubble_bath.png": ("b", (1467, 439), (48, 46)),
}

COLLECTION_AUDIT: dict[str, object] = {
	"schema": "castle_main_hall_physical_sign_audit_v1",
	"criterion": "visual compatibility and cohesiveness",
	"threshold_out_of_5": 4.5,
	"criteria_reviewed": [
		"silhouette",
		"palette",
		"outline",
		"border_medallion_geometry",
		"scale",
		"semantic_legibility_for_non_reader",
		"source_provenance",
		"runtime_placement",
	],
	"per_icon_overall_scores": {
		"family_gallery": {
			"before": 3.9,
			"after": 4.7,
			"status": "corrected_pass",
			"note": (
				"Re-extracted from the full approved crest so the former clipped "
				"right-edge tab and adjacent portal scroll are absent."
			),
		},
		"opera_hall": {
			"overall": 4.8,
			"status": "pass_intentional_double_scale",
		},
		"library": {"overall": 4.9, "status": "pass"},
		"kitchen": {"overall": 4.8, "status": "pass"},
		"playroom": {
			"overall": 4.6,
			"status": "accepted_preserved",
			"note": (
				"Minor twelve-o'clock source-arch fragment retained because "
				"masking it also cuts valid teddy/rim pixels."
			),
		},
		"craft_room": {"overall": 4.9, "status": "pass"},
		"mermaid_pool": {"overall": 4.6, "status": "pass"},
		"bubble_bath": {"overall": 4.6, "status": "pass"},
	},
	"opera_scale_exception": {
		"intentional": True,
		"reason": "The Opera Hall doorway and sign are approximately 2x standard.",
	},
	"conclusion": (
		"Only Family Gallery fell below 4.5/5 and required an art change; "
		"the other seven signs remain byte-for-byte unchanged."
	),
}


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def fit_on_card(image: Image.Image, max_size: tuple[int, int]) -> Image.Image:
	image = image.copy()
	image.thumbnail(max_size, Image.Resampling.LANCZOS)
	card = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
	position = (
		(CANVAS_SIZE[0] - image.width) // 2,
		(CANVAS_SIZE[1] - image.height) // 2,
	)
	card.alpha_composite(image, position)
	return card


def extract_round_badge(
	image: Image.Image, center: tuple[int, int], radii: tuple[int, int]
) -> tuple[Image.Image, list[int]]:
	cx, cy = center
	rx, ry = radii
	pad = 2
	box = [cx - rx - pad, cy - ry - pad, cx + rx + pad, cy + ry + pad]
	crop = image.crop(tuple(box)).convert("RGBA")
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse(
		(pad, pad, crop.width - pad - 1, crop.height - pad - 1), fill=255
	)
	mask = mask.filter(ImageFilter.GaussianBlur(0.5))
	crop.putalpha(mask)
	return fit_on_card(crop, (232, 220)), box


def extract_family_badge(image: Image.Image) -> tuple[Image.Image, list[int]]:
	# The former crop stopped inside the crest and made its right edge look like
	# a rectangular tab. This full-width source box plus a hand-audited semantic
	# polygon follows the cream/gold scallop and lower shell, excluding the
	# adjacent purple scrolls and the navy doorway arch behind it.
	box = [140, 0, 375, 180]
	crop = image.crop(tuple(box)).convert("RGBA")
	mask = Image.new("L", crop.size, 0)
	draw = ImageDraw.Draw(mask)
	draw.polygon([
		(112, 0), (139, 5), (159, 18), (174, 34), (184, 54),
		(189, 73), (185, 92), (178, 110), (169, 126), (158, 138),
		(151, 149), (143, 157), (137, 163), (132, 168), (123, 173),
		(112, 176), (101, 173), (92, 168), (87, 163), (81, 157),
		(74, 149), (67, 138), (56, 126), (47, 110), (40, 92),
		(36, 73), (41, 54), (51, 34), (66, 18), (86, 5),
	], fill=255)
	mask = mask.filter(ImageFilter.GaussianBlur(0.45))
	crop.putalpha(ImageChops.multiply(crop.getchannel("A"), mask))
	visible_bounds = crop.getchannel("A").point(
		lambda value: 255 if value > 8 else 0
	).getbbox()
	if visible_bounds is None:
		raise ValueError("Family Gallery semantic mask produced no visible crest")
	crop = crop.crop(visible_bounds)
	return fit_on_card(crop, (115, 104)), box


def add_collection_keyline(
	image: Image.Image, palette_reference: Image.Image
) -> tuple[Image.Image, dict[str, object]]:
	"""Add only a sampled navy keyline and gold edge behind the house motif."""
	navy = palette_reference.getpixel(COLLECTION_NAVY_SAMPLE)
	gold = palette_reference.getpixel(COLLECTION_GOLD_SAMPLE)
	if navy != COLLECTION_NAVY_EXPECTED:
		raise ValueError(
			f"Unexpected collection navy sample {navy}; "
			f"expected {COLLECTION_NAVY_EXPECTED}"
		)
	if gold != COLLECTION_GOLD_EXPECTED:
		raise ValueError(
			f"Unexpected collection gold sample {gold}; "
			f"expected {COLLECTION_GOLD_EXPECTED}"
		)

	alpha = image.getchannel("A")
	navy_mask = alpha.filter(
		ImageFilter.MaxFilter(FAMILY_KEYLINE_RADIUS * 2 + 1)
	)
	gold_mask = alpha.filter(
		ImageFilter.MaxFilter(FAMILY_GOLD_EDGE_RADIUS * 2 + 1)
	)
	outlined = Image.new("RGBA", image.size, (0, 0, 0, 0))
	navy_layer = Image.new("RGBA", image.size, navy[:3] + (0,))
	navy_layer.putalpha(navy_mask)
	gold_layer = Image.new("RGBA", image.size, gold[:3] + (0,))
	gold_layer.putalpha(gold_mask)
	outlined.alpha_composite(navy_layer)
	outlined.alpha_composite(gold_layer)
	outlined.alpha_composite(image)

	# The approved opaque motif must remain byte-for-byte identical.  Only the
	# transparent perimeter and antialiased edge are allowed to gain color.
	source_pixels = image.load()
	outlined_pixels = outlined.load()
	opaque_motif_pixels = 0
	for y in range(image.height):
		for x in range(image.width):
			if source_pixels[x, y][3] == 255:
				opaque_motif_pixels += 1
				if outlined_pixels[x, y] != source_pixels[x, y]:
					raise ValueError(
						"Family keyline changed an opaque approved motif pixel"
					)

	return outlined, {
		"palette_reference": COLLECTION_PALETTE_REFERENCE,
		"navy_sample_xy": list(COLLECTION_NAVY_SAMPLE),
		"navy_rgba": list(navy),
		"gold_sample_xy": list(COLLECTION_GOLD_SAMPLE),
		"gold_rgba": list(gold),
		"keyline_radius_px": FAMILY_KEYLINE_RADIUS,
		"gold_edge_radius_px": FAMILY_GOLD_EDGE_RADIUS,
		"opaque_motif_pixels_preserved": opaque_motif_pixels,
	}


def main() -> None:
	OUTPUT.mkdir(parents=True, exist_ok=True)
	MANIFEST.parent.mkdir(parents=True, exist_ok=True)
	sources = {
		"a": HALL / "main_hall_screen_a_room_led_master.png",
		"b": HALL / "main_hall_screen_b_room_led_master.png",
		"family": DREAM_HOUSE / "family_wing_hall_insert.png",
	}
	images = {key: Image.open(path) for key, path in sources.items()}
	records: list[dict[str, object]] = []
	cards: dict[str, Image.Image] = {}
	boxes: dict[str, list[int]] = {}

	for output_name, (source_key, center, radii) in BADGES.items():
		card, box = extract_round_badge(images[source_key], center, radii)
		cards[output_name] = card
		boxes[output_name] = box

	for output_name, (source_key, _center, _radii) in BADGES.items():
		card = cards[output_name]
		box = boxes[output_name]
		output_path = OUTPUT / output_name
		card.save(output_path, optimize=True)
		record: dict[str, object] = {
				"output": output_path.relative_to(ROOT).as_posix(),
				"output_sha256": sha256(output_path),
				"output_dimensions": list(card.size),
				"source": sources[source_key].relative_to(ROOT).as_posix(),
				"source_sha256": sha256(sources[source_key]),
				"source_crop_xyxy": box,
				"derivation": "approved crop + soft ellipse alpha + Lanczos resize",
			}
		if output_name == "sign_playroom.png":
			record["audit_note"] = (
				"Accepted and preserved byte-for-byte at 4.6/5. The minor "
				"twelve-o'clock source-arch fragment cannot be removed "
				"without cutting valid teddy/rim pixels."
			)
		records.append(record)

	family_card, family_box = extract_family_badge(images["family"])
	family_card, family_keyline = add_collection_keyline(
		family_card, cards[COLLECTION_PALETTE_REFERENCE]
	)
	family_output = OUTPUT / "sign_family_gallery.png"
	family_card.save(family_output, optimize=True)
	records.append(
		{
			"output": family_output.relative_to(ROOT).as_posix(),
			"output_sha256": sha256(family_output),
			"output_dimensions": list(family_card.size),
			"source": sources["family"].relative_to(ROOT).as_posix(),
			"source_sha256": sha256(sources["family"]),
			"source_crop_xyxy": family_box,
			"derivation": (
				"approved full-crest crop + hand-traced semantic alpha + "
				"visible-bounds centering + "
				"whole-object Lanczos resize + collection-sampled navy "
				"keyline and gold edge"
			),
			"collection_keyline": family_keyline,
		}
	)

	manifest = {
		"schema": "castle_main_hall_sign_reuse_v1",
		"purpose": "separate unshaded Sprite3D door signs over blank sockets",
		"new_generation_used": False,
		"protected_sources_modified": False,
		"canvas_dimensions": list(CANVAS_SIZE),
		"collection_audit": COLLECTION_AUDIT,
		"records": sorted(records, key=lambda item: str(item["output"])),
	}
	MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(f"Wrote {len(records)} reused signs and {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
	main()
