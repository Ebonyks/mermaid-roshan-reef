#!/usr/bin/env python3
"""Static texture and alpha QA for Fairy Pond V2 art."""

from __future__ import annotations

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets" / "fairy"
SUBJECT_ART = ROOT / "assets_src" / "fairy_v2" / "runtime_textures"
OUT = ROOT / "tmp" / "fairy_v2" / "qa_contact_sheet.png"

BACKGROUNDS = ["pond_dawn.png", "pond_twilight.png", "pond_boss_clearing.png"]
SUBJECTS = [
	"bug_jewel.png",
	"bug_moth.png",
	"bug_firefly.png",
	"boss_leaf.png",
	"boss_seed.png",
	"boss_sprout.png",
	"boss_bud.png",
	"boss_opening.png",
	"boss_bloom.png",
]
MODELS = [Path(name).with_suffix(".glb").name for name in SUBJECTS]


def _audit_glb(path: Path) -> tuple[bool, str]:
	data = path.read_bytes()
	if len(data) < 28:
		return False, "truncated header"
	magic, version, total = struct.unpack_from("<4sII", data, 0)
	if magic != b"glTF" or version != 2 or total != len(data):
		return False, f"bad header magic={magic!r} version={version} total={total}/{len(data)}"
	json_length, json_kind = struct.unpack_from("<I4s", data, 12)
	if json_kind != b"JSON":
		return False, "missing JSON chunk"
	json_start = 20
	document = json.loads(data[json_start : json_start + json_length].decode("utf-8"))
	bin_header = json_start + json_length
	bin_length, bin_kind = struct.unpack_from("<I4s", data, bin_header)
	if bin_kind != b"BIN\x00":
		return False, "missing BIN chunk"
	declared = int(document["buffers"][0]["byteLength"])
	if declared > bin_length or bin_header + 8 + bin_length != len(data):
		return False, f"bad BIN length declared={declared} chunk={bin_length}"
	for view in document.get("bufferViews", []):
		offset = int(view.get("byteOffset", 0))
		length = int(view["byteLength"])
		if offset < 0 or length < 0 or offset + length > declared:
			return False, f"buffer view outside declared buffer: {offset}+{length}>{declared}"
	triangles = 0
	for primitive in document["meshes"][0]["primitives"]:
		accessor = document["accessors"][int(primitive["indices"])]
		triangles += int(accessor["count"]) // 3
	role = str(document["nodes"][0].get("extras", {}).get("role", ""))
	if not role or triangles <= 0:
		return False, f"missing role or triangles role={role!r} triangles={triangles}"
	return True, f"role={role} triangles={triangles} bytes={len(data)}"


def main() -> None:
	bad = 0
	thumbs: list[tuple[str, Image.Image]] = []
	for name in BACKGROUNDS + SUBJECTS:
		path = (SUBJECT_ART if name in SUBJECTS else ART) / name
		if not path.exists():
			print(f"FAIL missing {path}")
			bad += 1
			continue
		image = Image.open(path)
		if max(image.size) > 1024:
			print(f"FAIL oversize {name}: {image.size}")
			bad += 1
		if name in SUBJECTS:
			image = image.convert("RGBA")
			alpha = image.getchannel("A")
			corners = [alpha.getpixel((0, 0)), alpha.getpixel((1023, 0)), alpha.getpixel((0, 1023)), alpha.getpixel((1023, 1023))]
			if any(corners):
				print(f"FAIL opaque corner {name}: {corners}")
				bad += 1
			coverage = sum(1 for value in alpha.get_flattened_data() if value > 12) / float(image.width * image.height)
			if not 0.08 <= coverage <= 0.78:
				print(f"FAIL implausible coverage {name}: {coverage:.3f}")
				bad += 1
			else:
				print(f"OK {name}: {image.size[0]}x{image.size[1]} RGBA coverage={coverage:.3f}")
			checker = Image.new("RGBA", image.size, (191, 222, 226, 255))
			checker.alpha_composite(image)
			preview = checker.convert("RGB")
		else:
			print(f"OK {name}: {image.size[0]}x{image.size[1]} {image.mode}")
			preview = image.convert("RGB")
		preview.thumbnail((256, 256), Image.Resampling.LANCZOS)
		thumbs.append((name, preview.copy()))

	cell_w, cell_h = 280, 292
	cols = 4
	rows = (len(thumbs) + cols - 1) // cols
	sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), (225, 242, 245))
	draw = ImageDraw.Draw(sheet)
	for index, (name, preview) in enumerate(thumbs):
		x = (index % cols) * cell_w + (cell_w - preview.width) // 2
		y = (index // cols) * cell_h
		sheet.paste(preview, (x, y))
		draw.text(((index % cols) * cell_w + 8, y + 262), name, fill=(34, 46, 68))
	OUT.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(OUT, format="PNG", optimize=True)
	print(f"contact sheet: {OUT}")
	for name in MODELS:
		path = ART / "models" / name
		if not path.exists():
			print(f"FAIL missing {path}")
			bad += 1
			continue
		ok, detail = _audit_glb(path)
		print(f"{'OK' if ok else 'FAIL'} {name}: {detail}")
		if not ok:
			bad += 1
	if bad:
		raise SystemExit(1)


if __name__ == "__main__":
	main()
