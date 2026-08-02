#!/usr/bin/env python3
"""Static panorama, alpha, and readability QA for Fairy Pond art."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageStat


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets" / "fairy"
SUBJECT_ART = ART / "sprites"
OUT = ROOT / "tmp" / "fairy_v2" / "qa_contact_sheet.png"

PANORAMA = "pond_panorama.png"
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
	"ornament_lily_cluster.png",
	"ornament_lavender_reeds.png",
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
	panorama_image: Image.Image | None = None
	for name in [PANORAMA] + SUBJECTS:
		path = (SUBJECT_ART if name in SUBJECTS else ART) / name
		if not path.exists():
			print(f"FAIL missing {path}")
			bad += 1
			continue
		image = Image.open(path)
		if name in SUBJECTS and max(image.size) > 1024:
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
			if image.size != (4096, 1024) or image.mode != "RGB":
				print(f"FAIL panorama contract {name}: size={image.size} mode={image.mode}")
				bad += 1
			print(f"OK {name}: {image.size[0]}x{image.size[1]} {image.mode}")
			preview = image.convert("RGB")
			panorama_image = preview.copy()
		preview.thumbnail((512, 128), Image.Resampling.LANCZOS)
		thumbs.append((name, preview.copy()))

	cell_w, cell_h = 540, 292
	cols = 3
	rows = (len(thumbs) + cols - 1) // cols
	sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), (225, 242, 245))
	draw = ImageDraw.Draw(sheet)
	for index, (name, preview) in enumerate(thumbs):
		x = (index % cols) * cell_w + (cell_w - preview.width) // 2
		y = (index // cols) * cell_h
		sheet.paste(preview, (x, y))
		draw.text(((index % cols) * cell_w + 8, y + 262), name, fill=(34, 46, 68))
	if panorama_image is not None:
		# A dramatic palette journey is intentional, but its low-frequency
		# samples must stay continuous. One source canvas means there are no
		# authored seams or image-to-image join rows to hide.
		sample_count = 12
		palette_samples = [
			_mean_rgb(
				panorama_image.crop(
					(
						index * panorama_image.width // sample_count,
						0,
						(index + 1) * panorama_image.width // sample_count,
						panorama_image.height,
					)
				)
			)
			for index in range(sample_count)
		]
		palette_steps = [
			math.dist(palette_samples[index], palette_samples[index + 1])
			for index in range(sample_count - 1)
		]
		overall_shift = math.dist(palette_samples[0], palette_samples[-1])
		start_rgb = palette_samples[0]
		end_rgb = palette_samples[-1]
		gradient_ok = (
			max(palette_steps) <= 55.0
			and overall_shift >= 80.0
			and start_rgb[1] > start_rgb[0]
			and end_rgb[2] > end_rgb[1]
		)
		print(
			f"{'OK' if gradient_ok else 'FAIL'} panorama_gradient: "
			f"overall_shift={overall_shift:.2f} "
			f"max_local_step={max(palette_steps):.2f} "
			f"rgb={[tuple(round(value, 1) for value in sample) for sample in palette_samples]}"
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
	for retired_skin in ["fairy.glb", "fairy_v2.glb"]:
		if (ROOT / "assets" / "characters" / retired_skin).exists():
			print(f"FAIL retired Fairy skin model still present: {retired_skin}")
			bad += 1
	for retired_background in ["pond_dawn.png", "pond_twilight.png", "pond_boss_clearing.png"]:
		if (ART / retired_background).exists():
			print(f"FAIL superseded stitched background still present: {retired_background}")
			bad += 1
	if (ROOT / "tools" / "process_fairy_background_flow.py").exists():
		print("FAIL superseded background stitching pipeline still present")
		bad += 1
	if (ROOT / "assets_src" / "fairy_v3").exists():
		print("FAIL superseded multi-plate Fairy V3 sources still present")
		bad += 1
	source = (ROOT / "scripts" / "games" / "fairy.gd").read_text(encoding="utf-8")
	for forbidden in ["MeshInstance3D.new()", "CSG", ".glb"]:
		if forbidden in source:
			print(f"FAIL Fairy Pond runtime is not Sprite3D-only: {forbidden}")
			bad += 1
	for runtime_source in [
		ROOT / "scripts" / "player.gd",
		ROOT / "scripts" / "galaxy.gd",
		ROOT / "scripts" / "ember_fortress.gd",
	]:
		text = runtime_source.read_text(encoding="utf-8")
		if "assets/characters/fairy_v2.glb" in text or "assets/characters/fairy.glb" in text:
			print(f"FAIL Fairy skin model reference remains in {runtime_source.relative_to(ROOT)}")
			bad += 1
	if bad:
		raise SystemExit(1)


if __name__ == "__main__":
	main()
