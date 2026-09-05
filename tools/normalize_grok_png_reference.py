"""Re-encode a PNG reference without changing its decoded pixels.

This creates a separate generator-compatible derivative and never overwrites
the project authority. A JSON sidecar records both hashes and verifies exact
decoded-pixel equality after the round trip.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


def digest(path: Path) -> str:
	hasher = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			hasher.update(chunk)
	return hasher.hexdigest()


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("source", type=Path)
	parser.add_argument("destination", type=Path)
	parser.add_argument("--max-edge", type=int, default=None)
	args = parser.parse_args()
	if args.source.resolve() == args.destination.resolve():
		raise SystemExit("refusing to overwrite the source authority")
	args.destination.parent.mkdir(parents=True, exist_ok=True)
	with Image.open(args.source) as source_image:
		source_image.load()
		decoded = source_image.copy()
		original_size = decoded.size
		if args.max_edge and max(decoded.size) > args.max_edge:
			scale = args.max_edge / max(decoded.size)
			decoded = decoded.resize((round(decoded.width * scale), round(decoded.height * scale)), Image.Resampling.LANCZOS)
		decoded.save(args.destination, format="PNG", optimize=False, compress_level=6)
	with Image.open(args.destination) as normalized:
		normalized.load()
		if normalized.mode != decoded.mode or normalized.size != decoded.size or ImageChops.difference(normalized, decoded).getbbox() is not None:
			raise SystemExit("normalized PNG does not preserve decoded pixels exactly")
	record = {
		"schema": "grok-generator-compatible-png-v1",
		"source_path": args.source.as_posix(),
		"source_sha256": digest(args.source),
		"normalized_path": args.destination.as_posix(),
		"normalized_sha256": digest(args.destination),
		"source_dimensions": list(original_size),
		"dimensions": list(decoded.size),
		"mode": decoded.mode,
		"transform": "whole-canvas resize then PNG re-encode; output round-trip pixels verified exactly" if decoded.size != original_size else "PNG re-encode only; decoded pixels verified exactly equal",
		"appearance_changed": False,
		"source_overwritten": False,
	}
	sidecar = args.destination.with_suffix(args.destination.suffix + ".json")
	sidecar.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
	print(f"NORMALIZED|{args.destination}|{record['normalized_sha256']}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
