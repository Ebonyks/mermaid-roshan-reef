#!/usr/bin/env python3
"""Static texture, transition, alpha, and readability QA for Fairy Pond art."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets" / "fairy"
SUBJECT_ART = ART / "sprites"
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
	"helpful_flower_gate.png",
	"danger_thorn_halo.png",
]
RETIRED_ARENA_MODELS = [
	"fairy_bank_0.glb",
	"fairy_bank_1.glb",
	"fairy_flower_gate.glb",
	"fairy_lily_cluster.glb",
	"fairy_shadow_beetle.glb",
	"fairy_shadow_eel.glb",
	"fairy_shadow_jellyfish.glb",
]


def _mean_luminance(image: Image.Image) -> float:
	r, g, b = ImageStat.Stat(image.convert("RGB")).mean
	return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _mean_rgb(image: Image.Image) -> tuple[float, float, float]:
	r, g, b = ImageStat.Stat(image.convert("RGB")).mean
	return r, g, b


def _alpha_weighted_rgb(image: Image.Image) -> tuple[float, float, float]:
	rgba = image.convert("RGBA")
	totals = [0.0, 0.0, 0.0]
	weight = 0.0
	pixels = rgba.get_flattened_data() if hasattr(rgba, "get_flattened_data") else rgba.getdata()
	for r, g, b, alpha in pixels:
		a = alpha / 255.0
		weight += a
		totals[0] += r * a
		totals[1] += g * a
		totals[2] += b * a
	return tuple(value / max(weight, 1.0) for value in totals)


def main() -> None:
	bad = 0
	thumbs: list[tuple[str, Image.Image]] = []
	background_images: list[tuple[str, Image.Image]] = []
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
			alpha_values = alpha.get_flattened_data() if hasattr(alpha, "get_flattened_data") else alpha.getdata()
			coverage = sum(1 for value in alpha_values if value > 12) / float(image.width * image.height)
			if not 0.08 <= coverage <= 0.78:
				print(f"FAIL implausible coverage {name}: {coverage:.3f}")
				bad += 1
			else:
				print(f"OK {name}: {image.size[0]}x{image.size[1]} RGBA coverage={coverage:.3f}")
			if name in {"helpful_flower_gate.png", "danger_thorn_halo.png"}:
				center = alpha.crop((384, 384, 640, 640))
				center_values = center.get_flattened_data() if hasattr(center, "get_flattened_data") else center.getdata()
				center_alpha = sum(center_values) / float(255 * center.width * center.height)
				mean_rgb = _alpha_weighted_rgb(image)
				if center_alpha > 0.01:
					print(f"FAIL cue center must stay empty {name}: alpha={center_alpha:.3f}")
					bad += 1
				if name.startswith("helpful") and not (mean_rgb[1] > mean_rgb[0] and mean_rgb[2] > mean_rgb[0]):
					print(f"FAIL helpful cue palette {name}: rgb={mean_rgb}")
					bad += 1
				if name.startswith("danger") and not (mean_rgb[0] > mean_rgb[1] and mean_rgb[2] > mean_rgb[1]):
					print(f"FAIL danger cue palette {name}: rgb={mean_rgb}")
					bad += 1
			checker = Image.new("RGBA", image.size, (191, 222, 226, 255))
			checker.alpha_composite(image)
			preview = checker.convert("RGB")
		else:
			if image.size != (1024, 1024) or image.mode != "RGB":
				print(f"FAIL background contract {name}: size={image.size} mode={image.mode}")
				bad += 1
			print(f"OK {name}: {image.size[0]}x{image.size[1]} {image.mode}")
			preview = image.convert("RGB")
			background_images.append((name, preview.copy()))
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
	for index in range(len(background_images) - 1):
		name_a, image_a = background_images[index]
		name_b, image_b = background_images[index + 1]
		luminance_a = _mean_luminance(image_a)
		luminance_b = _mean_luminance(image_b)
		luminance_delta = abs(luminance_a - luminance_b)
		rgb_a = _mean_rgb(image_a)
		rgb_b = _mean_rgb(image_b)
		palette_delta = math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb_a, rgb_b)))
		# Runtime Sprite3D orientation joins the first plate's top image edge
		# to the second plate's bottom image edge.
		edge_a = image_a.crop((0, 0, image_a.width, 1))
		edge_b = image_b.crop((0, image_b.height - 1, image_b.width, image_b.height))
		seam_delta = sum(ImageStat.Stat(ImageChops.difference(edge_a, edge_b)).mean) / 3.0
		ok = luminance_delta <= 16.0 and palette_delta <= 48.0 and seam_delta <= 2.0
		print(
			f"{'OK' if ok else 'FAIL'} flow {name_a}->{name_b}: "
			f"luminance_delta={luminance_delta:.2f} palette_delta={palette_delta:.2f} seam_delta={seam_delta:.2f}"
		)
		if not ok:
			bad += 1
	if len(background_images) == 3:
		stack = Image.new("RGB", (1024, 3072))
		for index, (_name, image) in enumerate(background_images):
			stack.paste(ImageOps.flip(image), (0, index * 1024))
		gradient_samples = [
			_mean_luminance(stack.crop((0, y, 1024, min(y + 64, stack.height))))
			for y in range(0, stack.height, 256)
		]
		increases = [
			gradient_samples[index + 1] - gradient_samples[index]
			for index in range(len(gradient_samples) - 1)
		]
		max_jump = max(abs(value) for value in increases)
		max_increase = max(increases)
		gradient_ok = max_jump <= 5.0 and max_increase <= 1.5
		print(
			f"{'OK' if gradient_ok else 'FAIL'} global_gradient: "
			f"samples={[round(value, 2) for value in gradient_samples]} "
			f"max_jump={max_jump:.2f} max_increase={max_increase:.2f}"
		)
		if not gradient_ok:
			bad += 1
	OUT.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(OUT, format="PNG", optimize=True)
	print(f"contact sheet: {OUT}")
	models = list((ART / "models").glob("*.glb")) if (ART / "models").exists() else []
	if models:
		print(f"FAIL retired Fairy Pond 3D models still present: {[path.name for path in models]}")
		bad += 1
	arena_dir = ROOT / "assets" / "art35" / "arena"
	arena_models = [arena_dir / name for name in RETIRED_ARENA_MODELS if (arena_dir / name).exists()]
	if arena_models:
		print(f"FAIL retired Fairy Pond arena models still present: {[path.name for path in arena_models]}")
		bad += 1
	if bad:
		raise SystemExit(1)


if __name__ == "__main__":
	main()
