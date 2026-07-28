#!/usr/bin/env python3
"""Build the three continuous Fairy Pond background plates.

The V3 image-generation masters share one authored texture language.  This
finishing pass keeps their phase lighting gradual and crossfades the horizontal
join bands so the three adjacent Godot floor planes read as one long pond.

Usage:
	python tools/process_fairy_background_flow.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "fairy_v3" / "concepts"
RUNTIME_DIR = ROOT / "assets" / "fairy"
EDGE = 1024
SEAM_HOLD = 128
SEAM_BLEND = 192
COMMON_TINT = (116, 181, 197)
GRADIENT_START_LUMINANCE = 184.0
GRADIENT_END_LUMINANCE = 164.0
GRADIENT_TOP_TINT = (123, 193, 201)
GRADIENT_BOTTOM_TINT = (112, 164, 194)
PROFILE_RADIUS = 48

PLATES = [
	("background_dawn_master.png", "pond_dawn.png", 182.0, 0.90),
	("background_twilight_continuation.png", "pond_twilight.png", 170.0, 0.84),
	("background_boss_continuation.png", "pond_boss_clearing.png", 166.0, 0.84),
]


def _mean_luminance(image: Image.Image) -> float:
	r, g, b = ImageStat.Stat(image.convert("RGB")).mean
	return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _match_luminance(image: Image.Image, target: float) -> Image.Image:
	result = image
	for _step in range(3):
		current = _mean_luminance(result)
		if current <= 0.0:
			break
		result = ImageEnhance.Brightness(result).enhance(target / current)
	return result


def _prepare(source: Path, target_luminance: float, saturation: float) -> Image.Image:
	image = Image.open(source).convert("RGB")
	image = image.resize((EDGE, EDGE), Image.Resampling.LANCZOS)
	# Keep normalized, ungraded generated masters in the repo.  The original
	# full-size outputs remain in the Codex generated-image store.
	image.save(source, format="PNG", optimize=True)
	image = ImageEnhance.Color(image).enhance(saturation)
	tint = Image.new("RGB", image.size, COMMON_TINT)
	image = Image.blend(image, tint, 0.06)
	return _match_luminance(image, target_luminance)


def _join_runtime_pair(first: Image.Image, second: Image.Image) -> tuple[Image.Image, Image.Image]:
	"""Feather the edges that touch after Sprite3D's screen-facing orientation.

	The camera's +Z up vector means the first plate's top image edge touches
	the second plate's bottom image edge. Continue the first texture across the
	join for 128px, then spend 192px dissolving into the next stage. This makes
	bank, ripple, and watercolor-grain direction continuous at the join instead
	of merely matching one boundary row.
	"""
	width, height = first.size
	continuation_height = SEAM_HOLD + SEAM_BLEND
	# Target rows run from the far side of stage two to its touching edge, so
	# flip the first stage's near-edge crop into that same image-space order.
	continuation = ImageOps.flip(first.crop((0, 0, width, continuation_height)))
	original = second.crop((0, height - continuation_height, width, height))
	mask_values = [
		round(255.0 * _smoothstep(row / float(SEAM_BLEND - 1)))
		for row in range(SEAM_BLEND)
	] + [255] * SEAM_HOLD
	mask = Image.new("L", (1, continuation_height))
	mask.putdata(mask_values)
	mask = mask.resize((width, continuation_height), Image.Resampling.NEAREST)
	bridge = Image.composite(continuation, original, mask)
	joined_second = second.copy()
	joined_second.paste(bridge, (0, height - continuation_height))
	# Keep the touching texels identical under linear filtering.
	joined_second.paste(first.crop((0, 0, width, 1)), (0, height - 1))
	return first, joined_second


def _smoothstep(value: float) -> float:
	return value * value * (3.0 - 2.0 * value)


def _apply_global_gradient(images: list[Image.Image]) -> list[Image.Image]:
	"""Grade all three plates as one continuous texture ribbon.

	The local watercolor texture remains intact.  Only the low-frequency row
	profile is corrected, preventing any plate from reading like a separate
	screenshot while dawn eases gently into the boss clearing.
	"""
	# Build the grade in the same low-Z to high-Z orientation the player sees.
	# Sprite3D displays each source image upside-down along that world axis.
	stack = Image.new("RGB", (EDGE, EDGE * len(images)))
	for index, image in enumerate(images):
		stack.paste(ImageOps.flip(image), (0, index * EDGE))
	row_luminance = [_mean_luminance(stack.crop((0, y, EDGE, y + 1))) for y in range(stack.height)]
	prefix = [0.0]
	for value in row_luminance:
		prefix.append(prefix[-1] + value)
	smoothed: list[float] = []
	for y in range(stack.height):
		start = max(0, y - PROFILE_RADIUS)
		end = min(stack.height, y + PROFILE_RADIUS + 1)
		smoothed.append((prefix[end] - prefix[start]) / float(end - start))
	graded = Image.new("RGB", stack.size)
	for y in range(stack.height):
		t = _smoothstep(y / float(stack.height - 1))
		target_luminance = (
			GRADIENT_START_LUMINANCE
			+ (GRADIENT_END_LUMINANCE - GRADIENT_START_LUMINANCE) * t
		)
		tint = tuple(
			round(GRADIENT_TOP_TINT[channel] + (GRADIENT_BOTTOM_TINT[channel] - GRADIENT_TOP_TINT[channel]) * t)
			for channel in range(3)
		)
		row = stack.crop((0, y, EDGE, y + 1))
		row = Image.blend(row, Image.new("RGB", row.size, tint), 0.035)
		factor = max(0.86, min(1.14, target_luminance / max(1.0, smoothed[y])))
		lut = [min(255, round(value * factor)) for value in range(256)]
		graded.paste(row.point(lut * 3), (0, y))
	# Keep each boundary pixel-identical.  The surrounding 320px bridge still
	# carries the watercolor texture, so this lock is invisible and robust to
	# linear filtering on adjacent Sprite3D cards.
	for boundary in range(1, len(images)):
		y = boundary * EDGE
		graded.paste(graded.crop((0, y - 1, EDGE, y)), (0, y))
	return [
		ImageOps.flip(graded.crop((0, index * EDGE, EDGE, (index + 1) * EDGE)))
		for index in range(len(images))
	]


def main() -> None:
	images: list[Image.Image] = []
	for source_name, _target_name, luminance, saturation in PLATES:
		source = SOURCE_DIR / source_name
		if not source.exists():
			raise FileNotFoundError(source)
		images.append(_prepare(source, luminance, saturation))
	images[0], images[1] = _join_runtime_pair(images[0], images[1])
	images[1], images[2] = _join_runtime_pair(images[1], images[2])
	images = _apply_global_gradient(images)
	RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
	for image, (_source_name, target_name, _luminance, _saturation) in zip(images, PLATES):
		target = RUNTIME_DIR / target_name
		image.save(target, format="PNG", optimize=True)
		print(f"wrote {target.relative_to(ROOT)} luminance={_mean_luminance(image):.2f}")


if __name__ == "__main__":
	main()
