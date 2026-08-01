#!/usr/bin/env python3
"""Audit Sky Lagoon animal cards against their exact in-game backgrounds.

The animal probe captures paired Mobile-renderer frames with the pooled animal
visible and hidden. This script isolates the changed pixels, compares them with
the surrounding scene, and writes reproducible metrics plus a compact review
sheet. It intentionally audits the final in-game composite rather than the
source atlas in isolation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


REFERENCE_VIEWPORT = (1280.0, 720.0)
DIFF_THRESHOLD = 4


def _sha256(path: Path) -> str:
	hash_object = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			hash_object.update(chunk)
	return hash_object.hexdigest()


def _luminance(rgb: np.ndarray) -> np.ndarray:
	linear = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
	return 0.2126 * linear[..., 0] + 0.7152 * linear[..., 1] + 0.0722 * linear[..., 2]


def _saturation(rgb: np.ndarray) -> np.ndarray:
	maximum = rgb.max(axis=-1)
	minimum = rgb.min(axis=-1)
	result = np.zeros_like(maximum)
	np.divide(maximum - minimum, maximum, out=result, where=maximum > 0.0)
	return result


def _mean(values: np.ndarray) -> float:
	return round(float(values.mean()), 4) if values.size else 0.0


def _analyze_capture(capture_dir: Path, entry: dict[str, object]) -> tuple[dict[str, object], Image.Image]:
	with_path = capture_dir / str(entry["with"])
	without_path = capture_dir / str(entry["without"])
	with_image = Image.open(with_path).convert("RGB")
	without_image = Image.open(without_path).convert("RGB")
	if with_image.size != without_image.size:
		raise ValueError(f"Capture size mismatch: {with_path.name} / {without_path.name}")

	with_rgb = np.asarray(with_image, dtype=np.float32) / 255.0
	without_rgb = np.asarray(without_image, dtype=np.float32) / 255.0
	difference = np.max(np.abs(with_rgb - without_rgb), axis=-1)

	scale_x = with_image.width / REFERENCE_VIEWPORT[0]
	scale_y = with_image.height / REFERENCE_VIEWPORT[1]
	screen_point = entry["screen_point"]
	point_x = int(round(float(screen_point[0]) * scale_x))
	point_y = int(round(float(screen_point[1]) * scale_y))
	# Constrain isolation to the actor neighborhood so unrelated UI particles
	# cannot influence the lighting result.
	left = max(0, point_x - int(145 * scale_x))
	right = min(with_image.width, point_x + int(145 * scale_x))
	top = max(0, point_y - int(150 * scale_y))
	bottom = min(with_image.height, point_y + int(40 * scale_y))
	local_mask = difference[top:bottom, left:right] * 255.0 > DIFF_THRESHOLD
	mask = np.zeros(difference.shape, dtype=bool)
	mask[top:bottom, left:right] = local_mask
	y_indices, x_indices = np.nonzero(mask)
	if x_indices.size < 64:
		raise ValueError(f"Could not isolate {entry['lighting']} {entry['id']} from paired captures")

	bbox = [int(x_indices.min()), int(y_indices.min()), int(x_indices.max() + 1), int(y_indices.max() + 1)]
	margin = int(round(20 * min(scale_x, scale_y)))
	ring_left = max(0, bbox[0] - margin)
	ring_top = max(0, bbox[1] - margin)
	ring_right = min(with_image.width, bbox[2] + margin)
	ring_bottom = min(with_image.height, bbox[3] + margin)
	ring_mask = np.zeros(mask.shape, dtype=bool)
	ring_mask[ring_top:ring_bottom, ring_left:ring_right] = True
	ring_mask &= ~mask

	foreground = with_rgb[mask]
	background = without_rgb[ring_mask]
	with_luma = _luminance(with_rgb)
	without_luma = _luminance(without_rgb)
	pixel_luma_change = np.abs(with_luma[mask] - without_luma[mask])
	foreground_luma = _luminance(foreground)
	background_luma = _luminance(background)
	foreground_saturation = _saturation(foreground)
	background_saturation = _saturation(background)
	foreground_temperature = foreground[:, 0] - foreground[:, 2]
	background_temperature = background[:, 0] - background[:, 2]
	foreground_luma_mean = _mean(foreground_luma)
	background_luma_mean = _mean(background_luma)
	contrast = round(abs(foreground_luma_mean - background_luma_mean), 4)
	silhouette_contrast = _mean(pixel_luma_change)
	silhouette_contrast_p90 = round(float(np.percentile(pixel_luma_change, 90)), 4)
	saturation_delta = round(_mean(foreground_saturation) - _mean(background_saturation), 4)
	temperature_delta = round(_mean(foreground_temperature) - _mean(background_temperature), 4)
	dark_outline_fraction = round(float((foreground_luma < 0.09).mean()), 4)

	# These gates reject cards that disappear into foliage, clip into neon, or
	# lose their authored dark outline. Mean animal/background color equality is
	# not a useful gate: brown fur should remain brown beside blue water. The
	# paired day/night response below audits scene-light integration instead.
	checks = {
		"readable_silhouette": 0.012 <= silhouette_contrast <= 0.42 and silhouette_contrast_p90 >= 0.035,
		"not_luminance_clipped": 0.03 <= foreground_luma_mean <= 0.72,
		"not_neon_saturated": _mean(foreground_saturation) <= 0.85,
		"outline_retained": dark_outline_fraction >= 0.025,
	}
	metrics: dict[str, object] = {
		"id": entry["id"],
		"lighting": entry["lighting"],
		"habitat": entry["habitat"],
		"screen_point_1280x720": [round(float(screen_point[0]), 2), round(float(screen_point[1]), 2)],
		"isolated_bbox_pixels": bbox,
		"isolated_pixels": int(mask.sum()),
		"foreground_luminance": foreground_luma_mean,
		"local_background_luminance": background_luma_mean,
		"local_luminance_contrast": contrast,
		"mean_silhouette_luminance_change": silhouette_contrast,
		"p90_silhouette_luminance_change": silhouette_contrast_p90,
		"foreground_saturation": _mean(foreground_saturation),
		"local_background_saturation": _mean(background_saturation),
		"saturation_delta": saturation_delta,
		"foreground_warm_cool": _mean(foreground_temperature),
		"local_background_warm_cool": _mean(background_temperature),
		"warm_cool_delta": temperature_delta,
		"dark_outline_fraction": dark_outline_fraction,
		"checks": checks,
		"passed": all(checks.values()),
		"capture_sha256": {"with": _sha256(with_path), "without": _sha256(without_path)},
	}

	context_margin_x = int(round(70 * scale_x))
	context_margin_y = int(round(52 * scale_y))
	crop_box = (
		max(0, bbox[0] - context_margin_x),
		max(0, bbox[1] - context_margin_y),
		min(with_image.width, bbox[2] + context_margin_x),
		min(with_image.height, bbox[3] + context_margin_y),
	)
	return metrics, with_image.crop(crop_box)


def _make_contact_sheet(rows: list[tuple[dict[str, object], Image.Image]], output: Path) -> None:
	cell_width = 420
	cell_height = 300
	sheet = Image.new("RGB", (cell_width * 5, cell_height * 2), (28, 31, 52))
	draw = ImageDraw.Draw(sheet)
	font = ImageFont.load_default(size=22)
	small_font = ImageFont.load_default(size=16)
	order = {name: index for index, name in enumerate(("otter", "frog", "hare", "squirrel", "raccoon"))}
	for metrics, crop in rows:
		column = order[str(metrics["id"])]
		row = 0 if metrics["lighting"] == "day" else 1
		x = column * cell_width
		y = row * cell_height
		crop.thumbnail((cell_width - 16, cell_height - 72), Image.Resampling.LANCZOS)
		image_x = x + (cell_width - crop.width) // 2
		image_y = y + 42 + (cell_height - 72 - crop.height) // 2
		sheet.paste(crop, (image_x, image_y))
		status = "PASS" if metrics["passed"] else "FAIL"
		draw.text((x + 10, y + 8), f"{str(metrics['id']).title()} - {metrics['lighting']} - {status}", fill=(242, 244, 255), font=font)
		draw.text(
			(x + 10, y + cell_height - 24),
			f"L {metrics['foreground_luminance']:.3f}/{metrics['local_background_luminance']:.3f}  "
			f"Sil {metrics['mean_silhouette_luminance_change']:.3f}  "
			f"S {metrics['foreground_saturation']:.3f}  Temp {metrics['warm_cool_delta']:+.3f}",
			fill=(205, 213, 238),
			font=small_font,
		)
	output.parent.mkdir(parents=True, exist_ok=True)
	sheet.save(output, quality=91, optimize=True)


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("capture_dir", type=Path)
	parser.add_argument("--json-out", type=Path, required=True)
	parser.add_argument("--sheet-out", type=Path, required=True)
	args = parser.parse_args()
	manifest_path = args.capture_dir / "capture_manifest.json"
	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	rows = [_analyze_capture(args.capture_dir, entry) for entry in manifest["captures"]]
	results = [metrics for metrics, _crop in rows]
	lighting_response: list[dict[str, object]] = []
	for animal_id in ("otter", "frog", "hare", "squirrel", "raccoon"):
		day = next(result for result in results if result["id"] == animal_id and result["lighting"] == "day")
		night = next(result for result in results if result["id"] == animal_id and result["lighting"] == "night")
		luminance_ratio = round(float(night["foreground_luminance"]) / float(day["foreground_luminance"]), 4)
		checks = {
			"dims_with_scene": 0.25 <= luminance_ratio <= 0.72,
			"cools_with_scene": float(night["warm_cool_delta"]) < float(day["warm_cool_delta"]),
			"saturation_remains_controlled": float(night["foreground_saturation"]) <= float(day["foreground_saturation"]) + 0.08,
			"night_background_is_darker": float(night["local_background_luminance"]) < float(day["local_background_luminance"]),
		}
		lighting_response.append({
			"id": animal_id,
			"night_to_day_luminance_ratio": luminance_ratio,
			"day_relative_warm_cool": day["warm_cool_delta"],
			"night_relative_warm_cool": night["warm_cool_delta"],
			"checks": checks,
			"passed": all(checks.values()),
		})
	report = {
		"capture_manifest": str(manifest_path.as_posix()),
		"capture_manifest_sha256": _sha256(manifest_path),
		"reference_viewport": [1280, 720],
		"renderer": "Godot Mobile",
		"gates": {
			"mean_silhouette_luminance_change": [0.012, 0.42],
			"p90_silhouette_luminance_change_min": 0.035,
			"foreground_luminance": [0.03, 0.72],
			"foreground_saturation_max": 0.85,
			"dark_outline_fraction_min": 0.025,
			"night_to_day_luminance_ratio": [0.25, 0.72],
		},
		"captures": results,
		"lighting_response": lighting_response,
		"passed": all(bool(result["passed"]) for result in results) and all(bool(result["passed"]) for result in lighting_response),
	}
	args.json_out.parent.mkdir(parents=True, exist_ok=True)
	args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
	_make_contact_sheet(rows, args.sheet_out)
	for result in results:
		print(
			f"LIGHTING|{result['lighting']}|{result['id']}|"
			f"{'OK' if result['passed'] else 'FAIL'}|"
			f"silhouette={result['mean_silhouette_luminance_change']:.4f}|"
			f"sat_delta={result['saturation_delta']:+.4f}|"
			f"temp_delta={result['warm_cool_delta']:+.4f}"
		)
	for result in lighting_response:
		print(
			f"LIGHTING_RESPONSE|{result['id']}|{'OK' if result['passed'] else 'FAIL'}|"
			f"night_day_luma={result['night_to_day_luminance_ratio']:.4f}|"
			f"day_temp={result['day_relative_warm_cool']:+.4f}|night_temp={result['night_relative_warm_cool']:+.4f}"
		)
	print(f"SKY_LAGOON_ANIMAL_LIGHTING|{'ALL OK' if report['passed'] else 'FAIL'}")
	return 0 if report["passed"] else 1


if __name__ == "__main__":
	raise SystemExit(main())
