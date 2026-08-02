#!/usr/bin/env python3
"""Normalize and audit generated imp combat-pose sprites.

Native generated and alpha-matted candidates remain untouched. This tool
uniformly scales and translates the complete flattened subject into the
runtime 512x512 canvas, then measures the binding gates from
CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


CANVAS = 512
SOLID_ALPHA = 240
VISIBLE_ALPHA = 16
SKIN_ANCHOR = (208, 112, 240)

STATE_GATES: dict[str, dict[str, tuple[int, int] | None]] = {
	"idle": {"height": (480, 492), "bottom_gap": (6, 10)},
	"windup": {"height": (390, 460), "bottom_gap": (6, 10)},
	"charge": {"height": None, "bottom_gap": (40, 70)},
	"slash": {"height": (480, 492), "bottom_gap": (6, 10)},
	"recover": {"height": (415, 470), "bottom_gap": (6, 10)},
	"guard": {"height": (480, 500), "bottom_gap": (6, 10)},
	"stagger": {"height": (480, 492), "bottom_gap": (6, 10)},
	"flee": {"height": (480, 492), "bottom_gap": (6, 10)},
	"taunt": {"height": (480, 492), "bottom_gap": (6, 10)},
	"hop_a": {"height": (390, 460), "bottom_gap": (6, 10)},
	"hop_b": {"height": None, "bottom_gap": (40, 70)},
	"bopped": {"height": None, "bottom_gap": (40, 70)},
	"bow": {"height": (390, 470), "bottom_gap": (6, 10)},
}


def _harden_alpha(image: Image.Image) -> Image.Image:
	"""Raise the cleaned visible matte to the contract's solid-alpha threshold."""
	result = image.copy()
	alpha = result.getchannel("A").point(
		lambda value: 0 if value < VISIBLE_ALPHA else max(SOLID_ALPHA, value))
	result.putalpha(alpha)
	return result


def _retain_largest_alpha_component(image: Image.Image) -> Image.Image:
	"""Remove only resize-created detached matte specks from an isolated source component."""
	components = _components(_mask(image, SOLID_ALPHA), image.width, image.height)
	if len(components) <= 1:
		return image
	keep = set(max(components, key=len))
	result = image.copy()
	alpha = list(result.getchannel("A").getdata())
	for index, value in enumerate(alpha):
		if value >= SOLID_ALPHA and index not in keep:
			alpha[index] = 0
	result.putalpha(Image.frombytes("L", result.size, bytes(alpha)))
	return result


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _mask(image: Image.Image, threshold: int) -> bytearray:
	return bytearray(1 if alpha >= threshold else 0 for alpha in image.getchannel("A").getdata())


def _bounds(mask: bytearray, width: int, height: int) -> tuple[int, int, int, int] | None:
	xs: list[int] = []
	ys: list[int] = []
	for index, present in enumerate(mask):
		if present:
			xs.append(index % width)
			ys.append(index // width)
	if not xs:
		return None
	return min(xs), min(ys), max(xs), max(ys)


def _components(mask: bytearray, width: int, height: int) -> list[list[int]]:
	seen = bytearray(width * height)
	components: list[list[int]] = []
	for start, present in enumerate(mask):
		if not present or seen[start]:
			continue
		seen[start] = 1
		queue: deque[int] = deque([start])
		component: list[int] = []
		while queue:
			index = queue.popleft()
			component.append(index)
			x = index % width
			y = index // width
			for dy in (-1, 0, 1):
				for dx in (-1, 0, 1):
					if dx == 0 and dy == 0:
						continue
					nx = x + dx
					ny = y + dy
					if 0 <= nx < width and 0 <= ny < height:
						other = ny * width + nx
						if mask[other] and not seen[other]:
							seen[other] = 1
							queue.append(other)
		components.append(component)
	return components


def _interior_holes(solid: bytearray, width: int, height: int) -> list[int]:
	outside = bytearray(width * height)
	queue: deque[int] = deque()
	for x in range(width):
		for y in (0, height - 1):
			index = y * width + x
			if not solid[index] and not outside[index]:
				outside[index] = 1
				queue.append(index)
	for y in range(height):
		for x in (0, width - 1):
			index = y * width + x
			if not solid[index] and not outside[index]:
				outside[index] = 1
				queue.append(index)
	while queue:
		index = queue.popleft()
		x = index % width
		y = index // width
		for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
			nx = x + dx
			ny = y + dy
			if 0 <= nx < width and 0 <= ny < height:
				other = ny * width + nx
				if not solid[other] and not outside[other]:
					outside[other] = 1
					queue.append(other)
	holes = bytearray(1 if not solid[index] and not outside[index] else 0
		for index in range(width * height))
	return sorted((len(component) for component in _components(holes, width, height)), reverse=True)


def _longest_run(row: list[int]) -> int:
	best = current = 0
	for value in row:
		if value:
			current += 1
			best = max(best, current)
		else:
			current = 0
	return best


def _dominant_skin(image: Image.Image, solid: bytearray) -> tuple[tuple[int, int, int] | None, float | None]:
	buckets: Counter[tuple[int, int, int]] = Counter()
	for index, pixel in enumerate(image.getdata()):
		if not solid[index]:
			continue
		r, g, b = pixel[:3]
		if r > 100 and b > 100 and r > g + 20 and b > g + 20:
			buckets[((r // 16) * 16 + 8, (g // 16) * 16 + 8, (b // 16) * 16 + 8)] += 1
	if not buckets:
		return None, None
	eligible = [colour for colour, count in buckets.items() if count >= 32]
	colour = min(eligible, key=lambda candidate:
		sum((candidate[i] - SKIN_ANCHOR[i]) ** 2 for i in range(3)))
	distance = sum((colour[i] - SKIN_ANCHOR[i]) ** 2 for i in range(3)) ** 0.5
	return colour, round(distance, 3)


def _checker(size: tuple[int, int]) -> Image.Image:
	image = Image.new("RGBA", size, (238, 236, 247, 255))
	draw = ImageDraw.Draw(image)
	step = 24
	for y in range(0, size[1], step):
		for x in range(0, size[0], step):
			if (x // step + y // step) % 2:
				draw.rectangle((x, y, min(size[0], x + step), min(size[1], y + step)),
					fill=(215, 220, 238, 255))
	return image


def _write_qa(candidate: Image.Image, idle: Image.Image, qa_dir: Path, stem: str) -> dict[str, str]:
	qa_dir.mkdir(parents=True, exist_ok=True)
	checker = _checker((CANVAS, CANVAS))
	checker.alpha_composite(candidate)
	checker_path = qa_dir / f"{stem}_checker.png"
	checker.convert("RGB").save(checker_path, optimize=True)

	solid = _mask(candidate, SOLID_ALPHA)
	silhouette = Image.new("RGBA", (CANVAS, CANVAS), (245, 235, 209, 255))
	silhouette_pixels = silhouette.load()
	for index, present in enumerate(solid):
		if present:
			silhouette_pixels[index % CANVAS, index // CANVAS] = (17, 16, 30, 255)
	silhouette_path = qa_dir / f"{stem}_silhouette.png"
	silhouette.save(silhouette_path, optimize=True)

	phone = checker.resize((128, 128), Image.Resampling.LANCZOS)
	phone_path = qa_dir / f"{stem}_phone_25pct.png"
	phone.save(phone_path, optimize=True)

	comparison = _checker((CANVAS * 2, CANVAS))
	comparison.alpha_composite(idle, (0, 0))
	comparison.alpha_composite(candidate, (CANVAS, 0))
	comparison_path = qa_dir / f"{stem}_idle_comparison.png"
	comparison.convert("RGB").save(comparison_path, optimize=True)
	return {
		"checker": str(checker_path),
		"silhouette": str(silhouette_path),
		"phone_25pct": str(phone_path),
		"idle_comparison": str(comparison_path),
	}


def _normalize(source: Image.Image, target_height: int, bottom_gap: int,
	target_centroid: float = 256.0) -> Image.Image:
	image = source.convert("RGBA")
	solid = _mask(image, SOLID_ALPHA)
	visible = _mask(image, VISIBLE_ALPHA + 1)
	solid_bounds = _bounds(solid, image.width, image.height)
	visible_bounds = _bounds(visible, image.width, image.height)
	if solid_bounds is None or visible_bounds is None:
		raise ValueError("candidate contains no visible solid subject")
	solid_height = solid_bounds[3] - solid_bounds[1] + 1
	scale = target_height / solid_height
	vx0, vy0, vx1, vy1 = visible_bounds
	crop = image.crop((vx0, vy0, vx1 + 1, vy1 + 1))
	resized = crop.resize((max(1, round(crop.width * scale)),
		max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)
	resized_solid = _mask(resized, SOLID_ALPHA)
	resized_bounds = _bounds(resized_solid, resized.width, resized.height)
	if resized_bounds is None:
		raise ValueError("resizing removed the solid subject")
	x0, y0, x1, y1 = resized_bounds
	x_values = [index % resized.width for index, present in enumerate(resized_solid) if present]
	centroid = sum(x_values) / len(x_values)
	target_max_y = CANVAS - bottom_gap - 1
	offset_x = round(target_centroid - centroid)
	offset_y = target_max_y - y1
	visible_left = offset_x
	visible_top = offset_y
	visible_right = offset_x + resized.width - 1
	visible_bottom = offset_y + resized.height - 1
	# The explicit grounded baseline gate (6-10px) overrides the general 12px
	# clear-margin sentence at the bottom edge. Keep 12px on the other three
	# edges and allow one antialias-fringe pixel below the solid sole.
	if min(visible_left, visible_top, CANVAS - 1 - visible_right) < 12 or \
			CANVAS - 1 - visible_bottom < max(0, bottom_gap - 2):
		raise ValueError(
			"normalized subject cannot preserve target scale with 12px margins: "
			f"bounds={(visible_left, visible_top, visible_right, visible_bottom)}")
	canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
	canvas.alpha_composite(resized, (offset_x, offset_y))
	return canvas


def _audit(candidate: Image.Image, idle: Image.Image, state: str,
	allowed_large_holes: int) -> dict[str, object]:
	failures: list[str] = []
	if candidate.size != (CANVAS, CANVAS):
		failures.append(f"canvas must be 512x512, got {candidate.size}")
	if candidate.mode != "RGBA":
		failures.append(f"mode must be RGBA, got {candidate.mode}")
	candidate = candidate.convert("RGBA")
	idle = idle.convert("RGBA").resize((CANVAS, CANVAS), Image.Resampling.LANCZOS)
	solid = _mask(candidate, SOLID_ALPHA)
	visible = _mask(candidate, VISIBLE_ALPHA + 1)
	idle_solid = _mask(idle, SOLID_ALPHA)
	bounds = _bounds(solid, CANVAS, CANVAS)
	if bounds is None:
		return {"pass": False, "failures": ["no solid subject"]}
	x0, y0, x1, y1 = bounds
	height = y1 - y0 + 1
	bottom_gap = CANVAS - 1 - y1
	left_gap = x0
	right_gap = CANVAS - 1 - x1
	visible_bounds = _bounds(visible, CANVAS, CANVAS)
	components = _components(solid, CANVAS, CANVAS)
	holes = _interior_holes(solid, CANVAS, CANVAS)
	large_holes = [area for area in holes if area > 200]
	alpha = list(candidate.getchannel("A").getdata())
	semi_count = sum(VISIBLE_ALPHA < value < SOLID_ALPHA for value in alpha)
	solid_count = sum(solid)
	semi_ratio = semi_count / max(1, solid_count)
	x_values = [index % CANVAS for index, present in enumerate(solid) if present]
	centroid_x = sum(x_values) / max(1, len(x_values))
	intersection = sum(1 for a, b in zip(solid, idle_solid) if a and b)
	union = sum(1 for a, b in zip(solid, idle_solid) if a or b)
	iou = intersection / max(1, union)
	bottom_row = [solid[y1 * CANVAS + x] for x in range(CANVAS)]
	bottom_run = _longest_run(bottom_row)
	skin_colour, skin_distance = _dominant_skin(candidate, solid)
	gate = STATE_GATES[state]
	height_gate = gate["height"]
	bottom_gate = gate["bottom_gap"]
	if height_gate is not None and not height_gate[0] <= height <= height_gate[1]:
		failures.append(f"solid height {height} outside {height_gate}")
	if bottom_gate is not None and not bottom_gate[0] <= bottom_gap <= bottom_gate[1]:
		failures.append(f"bottom gap {bottom_gap} outside {bottom_gate}")
	if min(x0, y0, CANVAS - 1 - x1, CANVAS - 1 - y1) <= 2:
		failures.append("solid pixels occur within 2px of a canvas edge")
	if visible_bounds is not None:
		visible_bottom_gap = CANVAS - 1 - visible_bounds[3]
		if min(visible_bounds[0], visible_bounds[1],
				CANVAS - 1 - visible_bounds[2]) < 12 or \
				visible_bottom_gap < max(0, bottom_gap - 2):
			failures.append(f"visible margin outside allowed baseline envelope: {visible_bounds}")
	if bottom_run >= 100:
		failures.append(f"bottom-row solid run {bottom_run} must be <100")
	if semi_ratio >= 0.15:
		failures.append(f"semi-alpha ratio {semi_ratio:.4f} must be <0.15")
	if len(components) != 1:
		failures.append(f"solid connected components {len(components)} must equal 1")
	if len(large_holes) > allowed_large_holes:
		failures.append(
			f"large interior holes {large_holes} exceed {allowed_large_holes} reviewed exemptions")
	if skin_distance is None or skin_distance > 90.0:
		failures.append(f"dominant purple distance {skin_distance} exceeds 90")
	if state != "idle" and iou >= 0.75:
		failures.append(f"silhouette IoU {iou:.4f} must be <0.75")
	if abs(centroid_x - 256.0) > 24.0:
		failures.append(f"horizontal centroid {centroid_x:.2f} outside 256+/-24")
	return {
		"pass": not failures,
		"failures": failures,
		"state": state,
		"canvas": list(candidate.size),
		"mode": candidate.mode,
		"solid_bbox": [x0, y0, x1, y1],
		"visible_bbox": list(visible_bounds) if visible_bounds else None,
		"solid_height": height,
		"gaps": {"left": left_gap, "right": right_gap, "bottom": bottom_gap},
		"bottom_row_longest_solid_run": bottom_run,
		"semi_alpha_pixels": semi_count,
		"solid_pixels": solid_count,
		"semi_alpha_to_solid_ratio": round(semi_ratio, 6),
		"solid_connected_components": len(components),
		"interior_hole_areas": holes,
		"reviewed_large_hole_exemptions": allowed_large_holes,
		"dominant_purple_rgb": list(skin_colour) if skin_colour else None,
		"dominant_purple_distance_from_d070f0": skin_distance,
		"silhouette_iou_against_idle": round(iou, 6),
		"solid_centroid_x": round(centroid_x, 3),
	}


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	parser.add_argument("--idle", type=Path, required=True)
	parser.add_argument("--state", choices=sorted(STATE_GATES), required=True)
	parser.add_argument("--target-height", type=int, required=True)
	parser.add_argument("--bottom-gap", type=int, required=True)
	parser.add_argument("--target-centroid-x", type=float, default=256.0)
	parser.add_argument("--allow-large-holes", type=int, default=0)
	parser.add_argument("--harden-alpha", action="store_true")
	parser.add_argument("--report", type=Path, required=True)
	parser.add_argument("--qa-dir", type=Path, required=True)
	args = parser.parse_args()

	with Image.open(args.input) as raw:
		prepared = _harden_alpha(raw.convert("RGBA")) if args.harden_alpha else raw.convert("RGBA")
		candidate = _normalize(prepared, args.target_height, args.bottom_gap, args.target_centroid_x)
	if args.harden_alpha:
		candidate = _retain_largest_alpha_component(_harden_alpha(candidate))
	with Image.open(args.idle) as raw_idle:
		idle = raw_idle.convert("RGBA")
	args.output.parent.mkdir(parents=True, exist_ok=True)
	candidate.save(args.output, optimize=True, compress_level=9)
	report = _audit(candidate, idle, args.state, args.allow_large_holes)
	report.update({
		"input": str(args.input),
		"input_sha256": _sha256(args.input),
		"output": str(args.output),
		"output_sha256": _sha256(args.output),
		"idle_reference": str(args.idle),
		"idle_sha256": _sha256(args.idle),
		"normalization": {
			"method": "uniform whole-subject Lanczos scale and translation on transparent canvas",
			"target_solid_height": args.target_height,
			"target_bottom_gap": args.bottom_gap,
			"target_solid_centroid_x": args.target_centroid_x,
		},
		"qa_renders": _write_qa(candidate, idle, args.qa_dir, args.output.stem),
	})
	args.report.parent.mkdir(parents=True, exist_ok=True)
	args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(report, indent=2))
	if not report["pass"]:
		raise SystemExit(1)


if __name__ == "__main__":
	main()
