#!/usr/bin/env python3
"""Build Daddy Mermaid's accepted tail-motion sprite atlases.

The accepted ImageGen sheets use a green field even though Daddy contains
green and yellow details. The bundled ImageGen chroma helper supplies keyed
and despilled intermediates. This builder accepts only the helper matte
connected to the sheet border, then extracts each complete Daddy globally so
tails crossing nominal atlas boundaries are never clipped or assigned twice.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "imagegen" / "daddy_25d_tailmotion_2026-08-01"
OUTPUT = ROOT / "assets" / "characters" / "daddy_25d"

CELL = 256
# 220-232px cannot contain the victory clip's full left/right fluke sweep while
# keeping the torso fixed. 188px leaves the final soft shadow clear of every
# cell edge; runtime may scale the Sprite3D by 232/188 to preserve apparent size.
NORMALIZED_SPAN = 188.0
TORSO_TARGET = (122.0, 50.0)
RIM_FILTER = 11
SHADOW_OFFSET = (3, 5)
MIN_ISLAND_AREA = 64
FLUKE_GAP = 12.0
VICTORY_FLUKE_GAP = 18.0

SHEETS = {
	"idle": (4, 2),
	"swim": (4, 4),
	"gesture_a": (4, 4),
	"victory": (4, 2),
}

PROTECTED_HASHES = {
	ROOT / "assets_src" / "daddy_master.png":
		"2eda6f76760b85984692dd35bf9ce69b631f6d9db4c8b7b8c013bb92cb632b77",
	ROOT / "assets" / "characters" / "friends" / "daddy.webp":
		"9031736498f05662716988b6c9a8091dc148edf92ae1e8422fb5e4f2fd17c089",
	ROOT / "assets" / "characters" / "stickers" / "daddy.png":
		"402024ac72c5365aae8562d422b9f888a6f5cdef7b6539409747e8f965cd0122",
}

ACCEPTED_SOURCE_HASHES = {
	"daddy_idle_chroma.png":
		"4134f09cf480198457e97aff99116585fd97acfbb9ba28fd191fc5353908deda",
	"daddy_swim_chroma.png":
		"13317e84f680c4c544f75be93e66f21ed251ac52eafab961c12f768268e45d6c",
	"daddy_gesture_a_chroma.png":
		"0df1cc477e2163d953a44d21df598e5f39b6bd90836fb5499c1932d4d238fae3",
	"daddy_victory_chroma.png":
		"851849de8f3a22f8acff03ca96b0dfa1f9ba5461ac5ee477b5006a2d41b896c2",
}


def sha256(path: Path) -> str:
	hash_value = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1024 * 1024), b""):
			hash_value.update(block)
	return hash_value.hexdigest()


def verify_sources() -> None:
	for path, expected in PROTECTED_HASHES.items():
		actual = sha256(path)
		if actual != expected:
			raise RuntimeError(f"protected Daddy source changed: {path} ({actual})")
	for filename, expected in ACCEPTED_SOURCE_HASHES.items():
		path = SOURCE / filename
		actual = sha256(path)
		if actual != expected:
			raise RuntimeError(f"wrong accepted tail-motion source: {path} ({actual})")


def connected_soft_key(stem: str) -> Image.Image:
	chroma = np.asarray(Image.open(SOURCE / f"{stem}_chroma.png").convert("RGBA"))
	keyed = np.asarray(Image.open(SOURCE / f"{stem}_alpha_keyed.png").convert("RGBA"))
	despilled = np.asarray(
		Image.open(SOURCE / f"{stem}_alpha_despill.png").convert("RGBA"))
	if chroma.shape != keyed.shape or chroma.shape != despilled.shape:
		raise RuntimeError(f"mismatched chroma-helper shapes for {stem}")

	eligible = keyed[:, :, 3] < 255
	labels, _count = ndimage.label(
		eligible, structure=np.ones((3, 3), dtype=np.uint8))
	border_labels = np.unique(np.concatenate((
		labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1])))
	border_labels = border_labels[border_labels != 0]
	background = np.isin(labels, border_labels)

	# Flatten the broad generated field to alpha zero. Preserve the helper's
	# antialiased/despilled matte only within 2.5px of retained foreground.
	distance = ndimage.distance_transform_edt(background)
	matte_edge = background & (distance <= 2.5) & (keyed[:, :, 3] > 0)
	result = chroma.copy()
	result[:, :, 3] = 255
	result[background, 3] = 0
	result[matte_edge, 3] = keyed[matte_edge, 3]
	result[matte_edge, :3] = despilled[matte_edge, :3]
	result[result[:, :, 3] == 0, :3] = 0

	clean = Image.fromarray(result, "RGBA")
	clean.save(SOURCE / f"{stem}_alpha_clean.png", optimize=True, compress_level=9)
	return clean


def split_bounds(length: int, parts: int) -> list[int]:
	# Bounds are ownership priors for torso centers only. They are never hard
	# image crops because the generated tails cross nominal atlas boundaries.
	return [round(index * length / parts) for index in range(parts + 1)]


def torso_anchor(main_mask: np.ndarray, nominal_height: float) -> tuple[float, float]:
	y_values, x_values = np.where(main_mask)
	if x_values.size == 0:
		raise RuntimeError("empty Daddy torso component")
	top = int(y_values.min())
	band = main_mask & (
		np.indices(main_mask.shape)[0] <= top + round(nominal_height * 0.15))
	band_y, band_x = np.where(band)
	return float(np.median(band_x)), float(np.median(band_y))


def owner_index(
		anchor: tuple[float, float],
		x_bounds: list[int],
		y_bounds: list[int],
		columns: int,
		rows: int,
) -> int:
	column = int(np.searchsorted(x_bounds, anchor[0], side="right") - 1)
	row = int(np.searchsorted(y_bounds, anchor[1], side="right") - 1)
	column = max(0, min(columns - 1, column))
	row = max(0, min(rows - 1, row))
	return row * columns + column


def extract_frames(
		clean: Image.Image,
		name: str,
		columns: int,
		rows: int,
) -> tuple[list[tuple[Image.Image, tuple[float, float]]], list[list[float]]]:
	pixels = np.asarray(clean.convert("RGBA"))
	labels, count = ndimage.label(
		pixels[:, :, 3] > 0, structure=np.ones((3, 3), dtype=np.uint8))
	sizes = np.bincount(labels.ravel())
	frame_count = columns * rows
	if count < frame_count:
		raise RuntimeError(f"{name} has only {count} foreground components")

	body_labels = sorted(
		range(1, count + 1), key=lambda label: int(sizes[label]), reverse=True
	)[:frame_count]
	x_bounds = split_bounds(clean.width, columns)
	y_bounds = split_bounds(clean.height, rows)
	nominal_height = clean.height / rows
	owners: list[dict[str, object] | None] = [None] * frame_count

	for body_label in body_labels:
		main_mask = labels == body_label
		anchor = torso_anchor(main_mask, nominal_height)
		index = owner_index(anchor, x_bounds, y_bounds, columns, rows)
		if owners[index] is not None:
			raise RuntimeError(f"{name} has two torso components in frame {index}")
		owners[index] = {
			"body": body_label,
			"anchor": anchor,
			"labels": [body_label],
			"gaps": [],
		}
	if any(owner is None for owner in owners):
		raise RuntimeError(f"{name} is missing a row-major torso component")

	body_set = set(body_labels)
	secondary = [
		label for label in range(1, count + 1)
		if label not in body_set and sizes[label] >= MIN_ISLAND_AREA
	]
	secondary_coords = {
		label: np.where(labels == label) for label in secondary
	}
	best_owner = {label: (float("inf"), -1) for label in secondary}

	# True pixel distance assigns a lobe to its nearest complete tail even when
	# that lobe crosses a nominal cell boundary.
	for index, owner_or_none in enumerate(owners):
		owner = owner_or_none
		assert owner is not None
		body_label = int(owner["body"])
		distance = ndimage.distance_transform_edt(labels != body_label)
		for label, coords in secondary_coords.items():
			gap = float(distance[coords].min())
			if gap < best_owner[label][0]:
				best_owner[label] = (gap, index)

	max_gap = VICTORY_FLUKE_GAP if name == "victory" else FLUKE_GAP
	for label, (gap, index) in best_owner.items():
		owner = owners[index]
		assert owner is not None
		component_y, _component_x = secondary_coords[label]
		anchor_y = float(owner["anchor"][1])
		is_lower = float(component_y.mean()) > anchor_y + nominal_height * 0.25
		if gap <= max_gap and is_lower:
			owner["labels"].append(label)
			owner["gaps"].append(gap)

	extracted: list[tuple[Image.Image, tuple[float, float]]] = []
	gaps: list[list[float]] = []
	for owner_or_none in owners:
		owner = owner_or_none
		assert owner is not None
		keep = np.isin(labels, owner["labels"])
		y_values, x_values = np.where(keep)
		left = int(x_values.min())
		top = int(y_values.min())
		right = int(x_values.max()) + 1
		bottom = int(y_values.max()) + 1
		crop_pixels = pixels[top:bottom, left:right].copy()
		crop_keep = keep[top:bottom, left:right]
		crop_pixels[~crop_keep] = 0
		anchor = (
			float(owner["anchor"][0]) - left,
			float(owner["anchor"][1]) - top,
		)
		extracted.append((Image.fromarray(crop_pixels, "RGBA"), anchor))
		gaps.append([float(gap) for gap in owner["gaps"]])
	return extracted, gaps


def resize_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
	return image.convert("RGBa").resize(
		size, Image.Resampling.LANCZOS).convert("RGBA")


def place_frame(
		frame: Image.Image,
		anchor: tuple[float, float],
		scale: float,
) -> Image.Image:
	width = max(1, round(frame.width * scale))
	height = max(1, round(frame.height * scale))
	content = resize_rgba(frame, (width, height))
	placed = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
	x = round(TORSO_TARGET[0] - anchor[0] * scale)
	y = round(TORSO_TARGET[1] - anchor[1] * scale)
	placed.alpha_composite(content, (x, y))
	alpha = np.asarray(placed.getchannel("A"))
	if np.any(alpha[:6, :]) or np.any(alpha[-6:, :]) or np.any(alpha[:, :6]) or np.any(alpha[:, -6:]):
		raise RuntimeError("normalized Daddy enters the sticker safety inset")
	return placed


def stickerize_frame(placed: Image.Image) -> Image.Image:
	alpha = placed.getchannel("A")
	expanded = alpha.filter(ImageFilter.MaxFilter(RIM_FILTER))
	shadow_seed = expanded.filter(ImageFilter.GaussianBlur(2.0))
	shadow_mask = Image.new("L", (CELL, CELL), 0)
	shadow_mask.paste(shadow_seed, SHADOW_OFFSET)
	shadow_mask = shadow_mask.point(lambda value: int(value * 0.48))

	result = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
	shadow = Image.new("RGBA", (CELL, CELL), (25, 30, 72, 0))
	shadow.putalpha(shadow_mask)
	result.alpha_composite(shadow)
	rim = Image.new("RGBA", (CELL, CELL), (255, 255, 252, 0))
	rim.putalpha(expanded)
	result.alpha_composite(rim)
	result.alpha_composite(placed)
	return result


def mask_anchor(frame: Image.Image) -> tuple[float, float]:
	alpha = np.asarray(frame.getchannel("A"))
	mask = alpha > 180
	y_values, _x_values = np.where(mask)
	top = int(y_values.min())
	band = mask & (np.indices(mask.shape)[0] <= top + round(CELL * 0.15))
	band_y, band_x = np.where(band)
	return float(np.median(band_x)), float(np.median(band_y))


def audit_sheet(name: str, frames: list[Image.Image]) -> None:
	tail_masks: list[np.ndarray] = []
	anchors: list[tuple[float, float]] = []
	coverage: list[int] = []
	for frame_index, frame in enumerate(frames):
		alpha = np.asarray(frame.getchannel("A"))
		if any((alpha[0, 0], alpha[0, -1], alpha[-1, 0], alpha[-1, -1])):
			raise RuntimeError(f"{name} frame {frame_index} has an opaque corner")
		edge_alpha = np.concatenate((
			alpha[0, :], alpha[-1, :], alpha[:, 0], alpha[:, -1]))
		if np.any(edge_alpha >= 8):
			raise RuntimeError(
				f"{name} frame {frame_index} has a clipped sticker edge")
		frame_coverage = int(np.count_nonzero(alpha > 8))
		if frame_coverage < 5000 or frame_coverage > 40000:
			raise RuntimeError(
				f"{name} frame {frame_index} coverage is {frame_coverage}")
		coverage.append(frame_coverage)

		components, _count = ndimage.label(
			alpha > 0, structure=np.ones((3, 3), dtype=np.uint8))
		component_sizes = np.bincount(components.ravel())[1:]
		if int(np.count_nonzero(component_sizes > 16)) != 1:
			raise RuntimeError(
				f"{name} frame {frame_index} retains a detached fragment")

		tail = alpha[100:, :] > 32
		if not np.any(tail):
			raise RuntimeError(f"{name} frame {frame_index} has no tail silhouette")
		tail_masks.append(tail)
		anchors.append(mask_anchor(frame))

	if len({hashlib.sha256(mask.tobytes()).digest() for mask in tail_masks}) != len(frames):
		raise RuntimeError(f"{name} contains a repeated/static tail silhouette")

	differences: list[float] = []
	for index in range(len(tail_masks) - 1):
		union = int(np.count_nonzero(tail_masks[index] | tail_masks[index + 1]))
		difference = int(np.count_nonzero(tail_masks[index] ^ tail_masks[index + 1]))
		differences.append(difference / max(1, union))
	if min(differences) < 0.02:
		raise RuntimeError(f"{name} tail motion is not readable in every step")

	anchor_x = [anchor[0] for anchor in anchors]
	anchor_y = [anchor[1] for anchor in anchors]
	if max(anchor_x) - min(anchor_x) > 8.0 or max(anchor_y) - min(anchor_y) > 14.0:
		raise RuntimeError(f"{name} torso anchor drift exceeds authored acting")
	print(
		f"{name}: coverage={min(coverage)}..{max(coverage)} "
		f"tail_step={min(differences):.3f}..{max(differences):.3f} "
		f"anchor_drift=({max(anchor_x) - min(anchor_x):.1f}, "
		f"{max(anchor_y) - min(anchor_y):.1f})")


def build_sheet(name: str, columns: int, rows: int) -> Image.Image:
	clean = connected_soft_key(f"daddy_{name}")
	extracted, gaps = extract_frames(clean, name, columns, rows)
	source_span = max(clean.width / columns, clean.height / rows)
	scale = NORMALIZED_SPAN / source_span
	result = Image.new("RGBA", (columns * CELL, rows * CELL), (0, 0, 0, 0))
	frames: list[Image.Image] = []
	for frame_index, (native, anchor) in enumerate(extracted):
		frame = stickerize_frame(place_frame(native, anchor, scale))
		frames.append(frame)
		column = frame_index % columns
		row = frame_index // columns
		result.alpha_composite(frame, (column * CELL, row * CELL))

	audit_sheet(name, frames)
	print(
		f"{name}: source={clean.size} scale={scale:.6f} "
		f"owned_fluke_gaps={[[round(gap, 1) for gap in item] for item in gaps]}")
	return result


def main() -> None:
	verify_sources()
	OUTPUT.mkdir(parents=True, exist_ok=True)
	for name, (columns, rows) in SHEETS.items():
		sheet = build_sheet(name, columns, rows)
		path = OUTPUT / f"daddy_{name}.png"
		sheet.save(path, optimize=True, compress_level=9)
		print(f"wrote {path.relative_to(ROOT)} {sheet.size} sha256={sha256(path)}")


if __name__ == "__main__":
	main()
