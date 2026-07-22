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
SEAM_BLEND = 32
COMMON_TINT = (116, 181, 197)

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


def _ramp_palette(continuation: Image.Image, reference: Image.Image) -> Image.Image:
	continuation_mean = ImageStat.Stat(continuation).mean
	reference_mean = ImageStat.Stat(reference).mean
	target_scale = [reference_mean[index] / max(1.0, continuation_mean[index]) for index in range(3)]
	result = Image.new("RGB", continuation.size)
	for row_index in range(continuation.height):
		t = row_index / float(continuation.height - 1)
		t = t * t * (3.0 - 2.0 * t)
		scales = [1.0 + (target_scale[index] - 1.0) * t for index in range(3)]
		luts = [[min(255, round(value * scale)) for value in range(256)] for scale in scales]
		row = continuation.crop((0, row_index, continuation.width, row_index + 1))
		result.paste(row.point(luts[0] + luts[1] + luts[2]), (0, row_index))
	return result


def _join_pair(first: Image.Image, second: Image.Image) -> tuple[Image.Image, Image.Image]:
	width, height = first.size
	continuation_height = SEAM_HOLD + SEAM_BLEND
	# Mirror the preceding edge across the plane join.  The first row of the
	# next plate therefore exactly matches the last row of the previous plate,
	# and bank/ripple shapes remain crisp instead of becoming a double exposure.
	continuation = ImageOps.flip(first.crop((0, height - continuation_height, width, height)))
	reference = second.crop((0, 0, width, continuation_height))
	continuation = _ramp_palette(continuation, reference)
	joined_second = second.copy()
	joined_second.paste(continuation.crop((0, 0, width, SEAM_HOLD)), (0, 0))
	original_blend = second.crop((0, SEAM_HOLD, width, continuation_height))
	continued_blend = continuation.crop((0, SEAM_HOLD, width, continuation_height))
	mask = Image.new("L", (1, SEAM_BLEND))
	mask.putdata([round(255.0 * row / float(SEAM_BLEND - 1)) for row in range(SEAM_BLEND)])
	mask = mask.resize((width, SEAM_BLEND), Image.Resampling.NEAREST)
	transition = Image.composite(original_blend, continued_blend, mask)
	joined_second.paste(transition, (0, SEAM_HOLD))
	return first, joined_second


def main() -> None:
	images: list[Image.Image] = []
	for source_name, _target_name, luminance, saturation in PLATES:
		source = SOURCE_DIR / source_name
		if not source.exists():
			raise FileNotFoundError(source)
		images.append(_prepare(source, luminance, saturation))
	images[0], images[1] = _join_pair(images[0], images[1])
	images[1], images[2] = _join_pair(images[1], images[2])
	RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
	for image, (_source_name, target_name, _luminance, _saturation) in zip(images, PLATES):
		target = RUNTIME_DIR / target_name
		image.save(target, format="PNG", optimize=True)
		print(f"wrote {target.relative_to(ROOT)} luminance={_mean_luminance(image):.2f}")


if __name__ == "__main__":
	main()
