#!/usr/bin/env python3
"""Package the owner's complete Merfolk Embrace image as a castle painting."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/castle/merfolk_embrace_20261027/source.png"
OUTPUT = ROOT / "assets/flats/castle/rooms/merfolk_embrace_painting.png"
MANIFEST = SOURCE.with_name("provenance.json")


def build() -> tuple[bytes, dict]:
	with Image.open(SOURCE) as original:
		assert original.size == (1024, 1536), original.size
		# Uniform reduction retains the complete composition without any crop.
		portrait = original.convert("RGB").resize((384, 576), Image.Resampling.LANCZOS)
	# A narrow, quiet gilded frame and cream mat; the artwork is unchanged.
	framed = Image.new("RGB", (448, 640), "#574466")
	draw = ImageDraw.Draw(framed)
	for inset, color in [(3, "#b77b48"), (7, "#f4d494"),
			(12, "#ca975b"), (19, "#795332"), (22, "#fff0cf"),
			(29, "#574466")]:
		draw.rectangle((inset, inset, 447-inset, 639-inset), fill=color)
	framed.paste(portrait, (32, 32))
	buffer = io.BytesIO()
	framed.save(buffer, format="PNG", optimize=False)
	payload = buffer.getvalue()
	manifest = {
		"source": SOURCE.relative_to(ROOT).as_posix(),
		"original_filename": "20250612_2032_Merfolk Embrace_remix_01jxkej325fe2arn4hdt9c4r0w.png",
		"source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
		"source_dimensions": [1024, 1536],
		"authority": "Owner supplied this exact image and requested its use as a painting in the castle on 2026-10-27.",
		"license_provenance": "Owner-supplied AI artwork authorized for this project use; generation provider/model and broader license were not supplied. No third-party license or public-domain status asserted.",
		"output": OUTPUT.relative_to(ROOT).as_posix(),
		"output_sha256": hashlib.sha256(payload).hexdigest(),
		"output_dimensions": [448, 640],
		"artwork_rect": [32, 32, 384, 576],
		"modifications": "Full image uniformly reduced to 384x576 with Lanczos; added a 32px gilded frame/mat outside its bounds. No crop, repaint, generation, recoloring, or source overwrite.",
		"builder": "python -B tools/build_castle_embrace_painting.py",
		"pillow_version": pillow_version,
		"runtime": {"room": "royal_bedroom", "role": "noninteractive_wall_painting", "source_art_rect": [806, 104, 140, 200]},
	}
	return payload, manifest


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	payload, manifest = build()
	if args.check:
		assert OUTPUT.read_bytes() == payload, "Runtime painting differs from source recipe"
		assert json.loads(MANIFEST.read_text(encoding="utf-8")) == manifest, "Provenance drift"
		print("CASTLE_PAINTING|PASS|complete source, uniform fit, 448x640 lossless texture, exact hashes")
	else:
		OUTPUT.parent.mkdir(parents=True, exist_ok=True)
		OUTPUT.write_bytes(payload)
		MANIFEST.write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
