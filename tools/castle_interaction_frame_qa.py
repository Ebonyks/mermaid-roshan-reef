#!/usr/bin/env python3
"""Deterministic per-frame compositing primitives for castle interactions.

This module deliberately has no repository or manifest policy.  It reproduces
the Sprite3D atlas-cell placement used by the castle runtime, then measures the
parts of a healed object footprint that one displayed frame exposes.  The main
castle audit can use the resulting exact pixel signatures with a separately
reviewed approval ledger.

Secondary overlays (water, sparkles, particles) may be included in a review
composite, but they never contribute to primary-object coverage.  A translucent
effect therefore cannot conceal a damaged heal from the geometry gate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from typing import Any, Mapping, Sequence

import numpy as np
from PIL import Image, ImageChops
from scipy.ndimage import label as component_label


DEFAULT_ALPHA_SCISSOR_THRESHOLD = 128
DEFAULT_OWNERSHIP_THRESHOLD = 48
# Review-only near-match radius. Blocking duplicate components always use an
# exact decoded-pixel match; see ``compute_frame_qa``.
DEFAULT_DUPLICATE_TOLERANCE = 4
DEFAULT_DUPLICATE_COMPONENT_MIN_PIXELS = 12
DEFAULT_REVIEW_MARGIN = 12


@dataclass(frozen=True)
class PlacedFrame:
	"""One atlas cell transformed into room space under runtime alpha scissor."""

	rgba: Image.Image
	alpha_mask: Image.Image


@dataclass(frozen=True)
class DuplicateComponent:
	"""One connected exposed patch that still matches the painted source."""

	pixels: int
	bbox: tuple[int, int, int, int]
	raw_pixel_sha256: str


@dataclass(frozen=True)
class FrameQARecord:
	"""JSON-safe exact evidence for one displayed authored state."""

	frame_index: int
	review_crop: tuple[int, int, int, int]
	composite_pixel_sha256: str
	primary_alpha_pixel_sha256: str
	primary_visible_pixels: int
	exposed_heal_pixel_sha256: str
	exposed_heal_pixels: int
	outside_ownership_pixel_sha256: str
	outside_ownership_pixels: int
	duplicate_exposed_pixel_sha256: str
	duplicate_exposed_pixels: int
	duplicate_components: tuple[DuplicateComponent, ...]
	blocking_duplicate_match_tolerance: int
	tolerance_only_match_radius: int
	tolerance_only_duplicate_pixel_sha256: str
	tolerance_only_duplicate_pixels: int
	tolerance_only_components: tuple[DuplicateComponent, ...]
	duplicate_component_min_pixels: int

	def to_dict(self) -> dict[str, Any]:
		"""Return a stable JSON-compatible approval payload."""
		value = asdict(self)
		value["review_crop"] = list(self.review_crop)
		for field in ("duplicate_components", "tolerance_only_components"):
			components = list(value[field])
			for component in components:
				component["bbox"] = list(component["bbox"])
			value[field] = components
		return value


@dataclass(frozen=True)
class FrameQAResult:
	"""One frame's record plus images useful for review contact sheets."""

	record: FrameQARecord
	composite: Image.Image
	primary_alpha_mask: Image.Image
	exposed_heal_mask: Image.Image
	outside_ownership_mask: Image.Image
	duplicate_exposed_mask: Image.Image
	tolerance_only_duplicate_mask: Image.Image


def raw_pixel_sha256(image: Image.Image) -> str:
	"""Hash decoded pixels, matching the castle repair provenance convention."""
	return hashlib.sha256(image.tobytes()).hexdigest()


def binary_mask(
		image: Image.Image,
		threshold: int = DEFAULT_ALPHA_SCISSOR_THRESHOLD,
		) -> Image.Image:
	"""Return a mode-L mask containing only 0 and 255."""
	if not 0 <= threshold <= 255:
		raise ValueError(f"mask threshold is outside 0..255: {threshold}")
	values = np.asarray(image.convert("L"), dtype=np.uint8)
	return Image.fromarray(
		(values >= threshold).astype(np.uint8) * 255,
		mode="L",
	)


def split_atlas_frames(
		sheet: Image.Image,
		grid: Sequence[int],
		frame_count: int,
		) -> list[Image.Image]:
	"""Decode the first ``frame_count`` cells of a row-major RGBA atlas."""
	if len(grid) != 2:
		raise ValueError("atlas grid must contain two values")
	columns, rows = int(grid[0]), int(grid[1])
	if columns <= 0 or rows <= 0:
		raise ValueError(f"atlas grid is invalid: {grid}")
	if sheet.width % columns or sheet.height % rows:
		raise ValueError("atlas dimensions are not divisible by its grid")
	if frame_count < 1 or frame_count > columns * rows:
		raise ValueError(f"atlas frame count is invalid: {frame_count}")
	cell_width = sheet.width // columns
	cell_height = sheet.height // rows
	rgba = sheet.convert("RGBA")
	return [
		rgba.crop((
			(index % columns) * cell_width,
			(index // columns) * cell_height,
			(index % columns + 1) * cell_width,
			(index // columns + 1) * cell_height,
		))
		for index in range(frame_count)
	]


def place_frame_rgba(
		frame: Image.Image,
		room_size: tuple[int, int],
		source_rect: Sequence[float],
		runtime_center_offset: Sequence[float],
		runtime_scale: float = 1.0,
		alpha_scissor_threshold: int = DEFAULT_ALPHA_SCISSOR_THRESHOLD,
		) -> PlacedFrame:
	"""Reproduce the castle Sprite3D atlas-cell transform in room coordinates.

	Pillow's affine tuple is an inverse transform, matching the implementation in
	``runtime_frame_union`` and ``repair_castle_room_native_backgrounds._frame_union``.
	The cell is centered at ``source_rect.xy + runtime_center_offset``.
	"""
	if len(source_rect) != 4:
		raise ValueError("source_rect must contain x, y, width, height")
	if len(runtime_center_offset) != 2:
		raise ValueError("runtime_center_offset must contain x and y")
	if room_size[0] <= 0 or room_size[1] <= 0:
		raise ValueError(f"room size is invalid: {room_size}")
	if runtime_scale <= 0.0:
		raise ValueError(f"runtime scale must be positive: {runtime_scale}")

	rgba = frame.convert("RGBA")
	center_x = float(source_rect[0]) + float(runtime_center_offset[0])
	center_y = float(source_rect[1]) + float(runtime_center_offset[1])
	inverse_scale = 1.0 / float(runtime_scale)
	matrix = (
		inverse_scale,
		0.0,
		rgba.width * 0.5 - center_x * inverse_scale,
		0.0,
		inverse_scale,
		rgba.height * 0.5 - center_y * inverse_scale,
	)
	placed = rgba.transform(
		room_size,
		Image.Transform.AFFINE,
		matrix,
		resample=Image.Resampling.BILINEAR,
	)
	alpha_mask = binary_mask(
		placed.getchannel("A"), alpha_scissor_threshold)
	values = np.asarray(placed, dtype=np.uint8).copy()
	visible = np.asarray(alpha_mask, dtype=np.uint8) > 0
	values[~visible] = 0
	placed = Image.fromarray(values, mode="RGBA")
	return PlacedFrame(placed, alpha_mask)


def place_atlas_frames(
		sheet: Image.Image,
		grid: Sequence[int],
		frame_count: int,
		room_size: tuple[int, int],
		source_rect: Sequence[float],
		runtime_center_offset: Sequence[float],
		runtime_scale: float = 1.0,
		alpha_scissor_threshold: int = DEFAULT_ALPHA_SCISSOR_THRESHOLD,
		) -> list[PlacedFrame]:
	"""Split and place every authored atlas state under one runtime transform."""
	return [
		place_frame_rgba(
			frame,
			room_size,
			source_rect,
			runtime_center_offset,
			runtime_scale,
			alpha_scissor_threshold,
		)
		for frame in split_atlas_frames(sheet, grid, frame_count)
	]


def frame_union_mask(frames: Sequence[PlacedFrame]) -> Image.Image:
	"""Return the binary union of placed primary-object alpha masks."""
	if not frames:
		raise ValueError("at least one placed frame is required")
	size = frames[0].alpha_mask.size
	union = Image.new("L", size, 0)
	for frame in frames:
		if frame.alpha_mask.size != size:
			raise ValueError("placed frame masks have inconsistent sizes")
		union = ImageChops.lighter(union, frame.alpha_mask)
	return binary_mask(union)


def asset_healing_mask(
		ownership_mask: Image.Image,
		frames: Sequence[PlacedFrame],
		ownership_threshold: int = DEFAULT_OWNERSHIP_THRESHOLD,
		) -> Image.Image:
	"""Match V4 healing: source ownership intersected with all-frame union."""
	ownership = binary_mask(ownership_mask, ownership_threshold)
	union = frame_union_mask(frames)
	if ownership.size != union.size:
		raise ValueError("ownership and placed frame masks have different sizes")
	return ImageChops.multiply(ownership, union)


def review_crop_rect(
		ownership_mask: Image.Image,
		frames: Sequence[PlacedFrame],
		margin: int = DEFAULT_REVIEW_MARGIN,
		ownership_threshold: int = DEFAULT_OWNERSHIP_THRESHOLD,
		) -> tuple[int, int, int, int]:
	"""Return a stable target-local crop covering ownership and every state."""
	if margin < 0:
		raise ValueError("review margin cannot be negative")
	ownership = binary_mask(ownership_mask, ownership_threshold)
	combined = ImageChops.lighter(ownership, frame_union_mask(frames))
	bbox = combined.getbbox()
	if bbox is None:
		raise ValueError("review crop has no visible ownership or frame pixels")
	return (
		max(0, bbox[0] - margin),
		max(0, bbox[1] - margin),
		min(combined.width, bbox[2] + margin),
		min(combined.height, bbox[3] + margin),
	)


def target_isolated_base(
		approved_room: Image.Image,
		runtime_underlay: Image.Image,
		ownership_mask: Image.Image,
		ownership_threshold: int = DEFAULT_OWNERSHIP_THRESHOLD,
		) -> Image.Image:
	"""Replace only the target object's source pixels with its real underlay."""
	if approved_room.size != runtime_underlay.size:
		raise ValueError("approved room and runtime underlay sizes differ")
	if approved_room.size != ownership_mask.size:
		raise ValueError("ownership mask size differs from room surfaces")
	base = approved_room.convert("RGBA")
	base.paste(
		runtime_underlay.convert("RGBA"),
		(0, 0),
		binary_mask(ownership_mask, ownership_threshold),
	)
	return base


def compose_target_frame(
		approved_room: Image.Image,
		runtime_underlay: Image.Image,
		ownership_mask: Image.Image,
		placed_frame: PlacedFrame,
		secondary_overlays: Sequence[Image.Image] = (),
		ownership_threshold: int = DEFAULT_OWNERSHIP_THRESHOLD,
		) -> Image.Image:
	"""Build one review composite while keeping secondary effects non-owning."""
	base = target_isolated_base(
		approved_room, runtime_underlay, ownership_mask, ownership_threshold)
	if placed_frame.rgba.size != base.size:
		raise ValueError("placed frame size differs from room surfaces")
	base.alpha_composite(placed_frame.rgba)
	for overlay in secondary_overlays:
		if overlay.size != base.size:
			raise ValueError("secondary overlay size differs from room surfaces")
		base.alpha_composite(overlay.convert("RGBA"))
	return base


def _mask_count(mask: Image.Image) -> int:
	return int(np.count_nonzero(np.asarray(mask, dtype=np.uint8)))


def _duplicate_exposed_mask(
		approved_room: Image.Image,
		runtime_underlay: Image.Image,
		ownership_mask: Image.Image,
		primary_alpha_mask: Image.Image,
		tolerance: int,
		ownership_threshold: int,
		) -> Image.Image:
	if not 0 <= tolerance <= 255:
		raise ValueError(f"duplicate tolerance is outside 0..255: {tolerance}")
	approved = np.asarray(approved_room.convert("RGB"), dtype=np.int16)
	underlay = np.asarray(runtime_underlay.convert("RGB"), dtype=np.int16)
	matching = np.max(np.abs(approved - underlay), axis=2) <= tolerance
	owned = np.asarray(binary_mask(
		ownership_mask, ownership_threshold), dtype=np.uint8) > 0
	covered = np.asarray(binary_mask(primary_alpha_mask), dtype=np.uint8) > 0
	return Image.fromarray(
		(matching & owned & ~covered).astype(np.uint8) * 255,
		mode="L",
	)


def connected_components(mask: Image.Image) -> tuple[DuplicateComponent, ...]:
	"""Measure deterministic 8-connected components of a binary mask."""
	values = np.asarray(binary_mask(mask), dtype=np.uint8) > 0
	components, count = component_label(
		values, structure=np.ones((3, 3), dtype=np.uint8))
	result: list[DuplicateComponent] = []
	for component_id in range(1, int(count) + 1):
		component = components == component_id
		y_positions, x_positions = np.where(component)
		if not x_positions.size:
			continue
		bbox = (
			int(x_positions.min()),
			int(y_positions.min()),
			int(x_positions.max()) + 1,
			int(y_positions.max()) + 1,
		)
		cropped = component[
			bbox[1]:bbox[3], bbox[0]:bbox[2]
		].astype(np.uint8) * 255
		result.append(DuplicateComponent(
			pixels=int(np.count_nonzero(component)),
			bbox=bbox,
			raw_pixel_sha256=hashlib.sha256(cropped.tobytes()).hexdigest(),
		))
	return tuple(sorted(
		result,
		key=lambda component: (
			-component.pixels, component.bbox[1], component.bbox[0],
		),
	))


def compute_frame_qa(
		frame_index: int,
		approved_room: Image.Image,
		runtime_underlay: Image.Image,
		ownership_mask: Image.Image,
		healing_mask: Image.Image,
		placed_frame: PlacedFrame,
		review_crop: tuple[int, int, int, int],
		secondary_overlays: Sequence[Image.Image] = (),
		duplicate_tolerance: int = DEFAULT_DUPLICATE_TOLERANCE,
		duplicate_component_min_pixels: int = (
			DEFAULT_DUPLICATE_COMPONENT_MIN_PIXELS),
		ownership_threshold: int = DEFAULT_OWNERSHIP_THRESHOLD,
		) -> FrameQAResult:
	"""Measure one placed authored frame against its exact runtime underlay."""
	size = approved_room.size
	for label, image in (
			("runtime underlay", runtime_underlay),
			("ownership mask", ownership_mask),
			("healing mask", healing_mask),
			("placed frame", placed_frame.rgba),
			("placed alpha", placed_frame.alpha_mask),
		):
		if image.size != size:
			raise ValueError(f"{label} size differs from approved room")
	if duplicate_component_min_pixels < 1:
		raise ValueError("duplicate component minimum must be positive")
	left, top, right, bottom = review_crop
	if left < 0 or top < 0 or right > size[0] or bottom > size[1] \
			or left >= right or top >= bottom:
		raise ValueError(f"review crop is outside the room: {review_crop}")

	ownership = binary_mask(ownership_mask, ownership_threshold)
	healing = binary_mask(healing_mask)
	primary = binary_mask(placed_frame.alpha_mask)
	exposed = ImageChops.multiply(healing, ImageChops.invert(primary))
	outside = ImageChops.multiply(primary, ImageChops.invert(ownership))
	# A blocking duplicate must be the exact same decoded source pixel after
	# normalization.  The prior <=4 RGB match conflated healed/resampled aqua and
	# mint backgrounds with retained source art.  Keep those near matches as
	# review evidence, but never turn them into non-waivable components.
	duplicate = _duplicate_exposed_mask(
		approved_room,
		runtime_underlay,
		ownership,
		primary,
		0,
		ownership_threshold,
	)
	tolerance_match = _duplicate_exposed_mask(
		approved_room,
		runtime_underlay,
		ownership,
		primary,
		duplicate_tolerance,
		ownership_threshold,
	)
	tolerance_only = ImageChops.multiply(
		tolerance_match, ImageChops.invert(duplicate))
	components = connected_components(duplicate)
	tolerance_only_components = connected_components(tolerance_only)
	composite = compose_target_frame(
		approved_room,
		runtime_underlay,
		ownership,
		placed_frame,
		secondary_overlays,
		ownership_threshold,
	)

	primary_crop = primary.crop(review_crop)
	exposed_crop = exposed.crop(review_crop)
	outside_crop = outside.crop(review_crop)
	duplicate_crop = duplicate.crop(review_crop)
	tolerance_only_crop = tolerance_only.crop(review_crop)
	composite_crop = composite.convert("RGB").crop(review_crop)
	record = FrameQARecord(
		frame_index=int(frame_index),
		review_crop=tuple(int(value) for value in review_crop),
		composite_pixel_sha256=raw_pixel_sha256(composite_crop),
		primary_alpha_pixel_sha256=raw_pixel_sha256(primary_crop),
		primary_visible_pixels=_mask_count(primary),
		exposed_heal_pixel_sha256=raw_pixel_sha256(exposed_crop),
		exposed_heal_pixels=_mask_count(exposed),
		outside_ownership_pixel_sha256=raw_pixel_sha256(outside_crop),
		outside_ownership_pixels=_mask_count(outside),
		duplicate_exposed_pixel_sha256=raw_pixel_sha256(duplicate_crop),
		duplicate_exposed_pixels=_mask_count(duplicate),
		duplicate_components=components,
		blocking_duplicate_match_tolerance=0,
		tolerance_only_match_radius=int(duplicate_tolerance),
		tolerance_only_duplicate_pixel_sha256=raw_pixel_sha256(
			tolerance_only_crop),
		tolerance_only_duplicate_pixels=_mask_count(tolerance_only),
		tolerance_only_components=tolerance_only_components,
		duplicate_component_min_pixels=int(duplicate_component_min_pixels),
	)
	return FrameQAResult(
		record=record,
		composite=composite,
		primary_alpha_mask=primary,
		exposed_heal_mask=exposed,
		outside_ownership_mask=outside,
		duplicate_exposed_mask=duplicate,
		tolerance_only_duplicate_mask=tolerance_only,
	)


def compute_asset_frame_qa(
		approved_room: Image.Image,
		runtime_underlay: Image.Image,
		ownership_mask: Image.Image,
		frames: Sequence[PlacedFrame],
		healing_mask: Image.Image | None = None,
		review_margin: int = DEFAULT_REVIEW_MARGIN,
		secondary_overlays_by_frame: Sequence[Sequence[Image.Image]] | None = None,
		duplicate_tolerance: int = DEFAULT_DUPLICATE_TOLERANCE,
		duplicate_component_min_pixels: int = (
			DEFAULT_DUPLICATE_COMPONENT_MIN_PIXELS),
		ownership_threshold: int = DEFAULT_OWNERSHIP_THRESHOLD,
		) -> list[FrameQAResult]:
	"""Compute exact evidence for every authored state of one physical object."""
	if not frames:
		raise ValueError("at least one placed frame is required")
	if secondary_overlays_by_frame is not None \
			and len(secondary_overlays_by_frame) != len(frames):
		raise ValueError("secondary overlay groups must match the frame count")
	healing = healing_mask if healing_mask is not None else asset_healing_mask(
		ownership_mask, frames, ownership_threshold)
	crop = review_crop_rect(
		ownership_mask, frames, review_margin, ownership_threshold)
	return [
		compute_frame_qa(
			index,
			approved_room,
			runtime_underlay,
			ownership_mask,
			healing,
			frame,
			crop,
			secondary_overlays=(
				secondary_overlays_by_frame[index]
				if secondary_overlays_by_frame is not None else ()),
			duplicate_tolerance=duplicate_tolerance,
			duplicate_component_min_pixels=duplicate_component_min_pixels,
			ownership_threshold=ownership_threshold,
		)
		for index, frame in enumerate(frames)
	]


def compare_record_to_approval(
		record: FrameQARecord,
		approval: Mapping[str, Any],
		) -> list[str]:
	"""Return exact field mismatches against a reviewed approval payload."""
	expected = record.to_dict()
	problems: list[str] = []
	for field, value in expected.items():
		if approval.get(field) != value:
			problems.append(f"frame {record.frame_index}: stale {field}")
	return problems


def blocking_issues(
		record: FrameQARecord,
		approval: Mapping[str, Any] | None,
		) -> list[str]:
	"""Apply non-waivable duplicate checks plus exact reviewed approval.

	Intentional reveals and motion outside the original silhouette are allowed
	only when their exact masks and composite pixels match ``approval``.  An
	exposed connected exact source duplicate is never approval-waivable.
	Tolerance-only RGB similarities remain approval-bound diagnostics in the
	record, but are not evidence that source pixels survived normalization.
	"""
	problems: list[str] = []
	large_duplicates = [
		component for component in record.duplicate_components
		if component.pixels >= record.duplicate_component_min_pixels
	]
	if large_duplicates:
		problems.append(
			f"frame {record.frame_index}: exposed source duplicate has "
			f"{large_duplicates[0].pixels} connected pixels")
	if approval is None:
		problems.append(f"frame {record.frame_index}: missing composite approval")
	else:
		problems.extend(compare_record_to_approval(record, approval))
	return problems
