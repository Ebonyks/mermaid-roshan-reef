#!/usr/bin/env python3
"""Machine-check visual congruency for the Sky Lagoon promenade.

This gate implements the seven-criterion contract in the owner's Claude
artifact.  Pixel criteria are measured from source PNGs; displayed density is
derived from the actual 720p camera and Sprite3D world heights; contact shadows
are verified structurally in the stage script.  It writes a detailed JSON
ledger when requested and exits non-zero until every audited element passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
PLATE = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
STAGE = ROOT / "scripts/arena/sky_lagoon_promenade.gd"
ROSHAN_LOOP = ROOT / "scripts/roshan_sprite_loop.gd"
CASTLE_PALETTE_REFERENCE = (
	ROOT / "assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png"
)
ROSHAN_PALETTE_REFERENCE = (
	ROOT / "assets/characters/roshan_25d/roshan_base.png"
)
CANVAS_HEIGHT = 720.0
CAM_DIST = 47.0
CAM_FOV = 38.0
BACKDROP_Z = -18.0
TOL = {
	"c1_delta_lab": 18.0,
	"c2_median_l": 16.0,
	"c2_black_l": 14.0,
	"c2_white_l": 14.0,
	"c3_key_degrees": 45.0,
	"c4_specular_over_plate": 0.025,
	"c5_contrast_min": 0.53,
	# The v5 clean plate intentionally carries softer distant foliage; crisp
	# interactive cards may be up to 2.5x its local contrast while remaining
	# inside the established outline/value language.
	"c5_contrast_max": 2.50,
	"c6_ratio_min": 1.0,
	"c6_ratio_max": 2.5,
	"c6_plate_multiplier": 2.0,
}


@dataclass(frozen=True)
class Element:
	name: str
	path: str
	world_height: float
	z: float
	band: str = "ground"
	shadow_mode: str = "card"
	palette_band: str = ""
	atlas_rows: int = 1
	runtime_paths: tuple[str, ...] = ()
	runtime_sha256: tuple[str, ...] = ()
	density_max_override: float | None = None


ELEMENTS = (
	Element("cloud_single_drift", "assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png", 3.104, -16.0, "sky", "painted_underside"),
	Element("plane", "assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png", 10.732, -11.0),
	# Owner-reviewed 2026-08-01: the accepted runtime swing is this two-card
	# assembly. Measure the active frame in Roshan's foreground play band and
	# exact-hash lock both runtime layers so the density exception cannot
	# silently authorize different art. The 1024x719 frame displays at 3.375x
	# source density on the 720p lens, hence the narrow 3.4x ceiling.
	Element(
		"swing",
		"assets/props/story/play_swing_frame.png",
		10.8,
		-6.0,
		"roshan",
		"card",
		"accent",
		1,
		(
			"assets/props/story/play_swing_frame.png",
			"assets/props/story/play_swing_seat.png",
		),
		(
			"a2098346be89be32ff1b559a8db96fbc95a9ab29c7ef3d7bb451059e2ef05592",
			"b3e6933400d83ece5e58ff62f23a052b3e1a5ce3ef788f66752e1f8f8fd0db7b",
		),
		3.4,
	),
	Element("slide", "assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png", 11.4, -6.0),
	Element("castle_four_tower", "assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png", 28.431, -11.0, "castle", "painted_underside", "castle"),
	Element("roshan_idle_directional", "assets/characters/roshan_25d/roshan_directional.png", 7.8, 0.2, "roshan", "card", "roshan", 2),
	Element("roshan_swim_front", "assets/characters/roshan_25d/roshan_swim_front.png", 7.8, 0.2, "roshan", "card", "roshan", 4),
	Element("seesaw", "assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png", 4.5, -6.0),
	Element("pnw_tree_sticker_tall", "assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png", 8.197, -9.0, "ground", "painted_underside"),
)


def srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
	value = rgb.astype(np.float64) / 255.0
	value = np.where(value <= 0.04045, value / 12.92, ((value + 0.055) / 1.055) ** 2.4)
	matrix = np.array(
		[[0.4124564, 0.3575761, 0.1804375],
		 [0.2126729, 0.7151522, 0.0721750],
		 [0.0193339, 0.1191920, 0.9503041]]
	)
	xyz = value @ matrix.T
	xyz /= np.array([0.95047, 1.0, 1.08883])
	delta = 6.0 / 29.0
	limit = delta ** 3
	f = np.where(xyz > limit, np.cbrt(xyz), xyz / (3 * delta ** 2) + 4.0 / 29.0)
	return np.stack((116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])), axis=-1)


def masked_pixels(image: Image.Image, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
	rgb = np.asarray(image.convert("RGB"))
	lab = srgb_to_lab(rgb)
	return rgb[mask], lab[mask]


def key_direction(l_channel: np.ndarray, mask: np.ndarray) -> tuple[float, float]:
	soft = np.asarray(
		Image.fromarray(np.clip(l_channel * 2.55, 0, 255).astype(np.uint8)).filter(
			ImageFilter.GaussianBlur(3.0)
		),
		dtype=np.float64,
	) / 2.55
	dy, dx = np.gradient(soft)
	interior = mask.copy()
	for shift_y, shift_x in ((-1, 0), (1, 0), (0, -1), (0, 1)):
		interior &= np.roll(mask, (shift_y, shift_x), axis=(0, 1))
	magnitude = np.hypot(dx, dy)
	threshold = np.percentile(magnitude[interior], 55) if np.any(interior) else 0.0
	weight = np.where(interior & (magnitude >= threshold), magnitude, 0.0)
	vector_x = float(np.sum(dx * weight))
	vector_y = float(np.sum(dy * weight))
	total = float(np.sum(magnitude * weight)) + 1e-9
	confidence = math.hypot(vector_x, vector_y) / total
	angle = math.degrees(math.atan2(-vector_y, vector_x)) % 360.0
	return angle, confidence


def angular_delta(a: float, b: float) -> float:
	return abs((a - b + 180.0) % 360.0 - 180.0)


def image_metrics(
		path: Path,
		band_crop: tuple[float, float] | None = None,
		box_crop: tuple[float, float, float, float] | None = None,
) -> dict[str, float]:
	image = Image.open(path).convert("RGBA")
	if box_crop is not None:
		image = image.crop(
			(
				round(image.width * box_crop[0]),
				round(image.height * box_crop[1]),
				round(image.width * box_crop[2]),
				round(image.height * box_crop[3]),
			)
		)
	if band_crop is not None:
		top = round(image.height * band_crop[0])
		bottom = round(image.height * band_crop[1])
		image = image.crop((0, top, image.width, bottom))
	alpha = np.asarray(image.getchannel("A"))
	mask = alpha >= 48
	if np.count_nonzero(mask) < 64:
		raise ValueError(f"{path} has too few opaque pixels")
	_, lab = masked_pixels(image, mask)
	l_all = srgb_to_lab(np.asarray(image.convert("RGB")))[..., 0]
	l_values = lab[:, 0]
	blur = np.asarray(
		Image.fromarray(np.clip(l_all * 2.55, 0, 255).astype(np.uint8)).filter(
			ImageFilter.GaussianBlur(2.0)
		),
		dtype=np.float64,
	) / 2.55
	high = l_all - blur
	specular = (high > 8.0) & (l_all > 78.0) & mask
	angle, confidence = key_direction(l_all, mask)
	return {
		"a": float(np.median(lab[:, 1])),
		"b": float(np.median(lab[:, 2])),
		"median_l": float(np.median(l_values)),
		"black_l": float(np.percentile(l_values, 5)),
		"white_l": float(np.percentile(l_values, 95)),
		"specular": float(np.count_nonzero(specular) / np.count_nonzero(mask)),
		"contrast": float(np.sqrt(np.mean(np.square(high[mask])))),
		"key_angle": angle,
		"key_confidence": confidence,
	}


def displayed_height(element: Element) -> float:
	focal = (CANVAS_HEIGHT * 0.5) / math.tan(math.radians(CAM_FOV * 0.5))
	return element.world_height * focal / (CAM_DIST - element.z)


def contact_shadow_ok(element: Element, metrics: dict[str, float], source: str) -> bool:
	if element.shadow_mode == "painted_underside":
		return metrics["white_l"] - metrics["black_l"] >= 8.0
	required = (
		"const CONTACT_SHADOW_TEX" in source
		and "func _add_contact_shadow" in source
		and "func _sync_contact_shadow" in source
	)
	runtime_paths = element.runtime_paths or (element.path,)
	required = required and all(Path(path).name in source for path in runtime_paths)
	if not required:
		return False
	if element.runtime_sha256:
		if len(element.runtime_sha256) != len(runtime_paths):
			return False
		for relative_path, expected_hash in zip(
			runtime_paths, element.runtime_sha256, strict=True
		):
			asset_path = ROOT / relative_path
			if not asset_path.is_file():
				return False
			actual_hash = hashlib.sha256(asset_path.read_bytes()).hexdigest()
			if actual_hash != expected_hash:
				return False
	return True


def evaluate(element: Element, bands: dict[str, dict[str, float]],
		plate_ratio: float, source: str) -> dict[str, Any]:
	path = ROOT / element.path
	metrics = image_metrics(path)
	target = bands[element.band]
	palette_target = bands[element.palette_band or element.band]
	delta_lab = math.hypot(metrics["a"] - palette_target["a"], metrics["b"] - palette_target["b"])
	key_delta = angular_delta(metrics["key_angle"], target["key_angle"])
	displayed = displayed_height(element)
	with Image.open(path) as authored:
		authored_height = authored.height / max(1, element.atlas_rows)
	density = authored_height / displayed
	density_max = (
		element.density_max_override
		if element.density_max_override is not None
		else min(TOL["c6_ratio_max"], plate_ratio * TOL["c6_plate_multiplier"])
	)
	criteria = {
		"C1": delta_lab <= TOL["c1_delta_lab"],
		"C2": (
			abs(metrics["median_l"] - target["median_l"]) <= TOL["c2_median_l"]
			and abs(metrics["black_l"] - target["black_l"]) <= TOL["c2_black_l"]
			and abs(metrics["white_l"] - target["white_l"]) <= TOL["c2_white_l"]
		),
		"C3": metrics["key_confidence"] < 0.18 or key_delta <= TOL["c3_key_degrees"],
		"C4": metrics["specular"] <= target["specular"] + TOL["c4_specular_over_plate"],
		"C5": (
			metrics["contrast"] >= target["contrast"] * TOL["c5_contrast_min"]
			and metrics["contrast"] <= target["contrast"] * TOL["c5_contrast_max"]
		),
		"C6": density >= TOL["c6_ratio_min"] and density <= density_max + 0.02,
		"C7": contact_shadow_ok(element, metrics, source),
	}
	return {
		"element": asdict(element),
		"metrics": metrics,
		"derived": {
			"delta_lab": delta_lab,
			"key_delta": key_delta,
			"displayed_height": displayed,
			"authored_height": authored_height,
			"density": density,
			"density_max": density_max,
		},
		"criteria": criteria,
		"pass": all(criteria.values()),
	}


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--json", type=Path)
	args = parser.parse_args()
	# The stage owns the contact shadow and the shared animator owns its atlas
	# paths. Both scripts form the runtime contract for the Sky Lagoon card.
	source = STAGE.read_text(encoding="utf-8") \
		+ ROSHAN_LOOP.read_text(encoding="utf-8")
	ground = image_metrics(PLATE, (0.52, 1.0))
	sky = image_metrics(PLATE, (0.0, 0.43))
	# Keep the established approved castle as a fixed palette/value baseline.
	# A replacement castle must be evaluated against it, never grade itself or
	# silently move the acceptance target for other purple landmark cards.
	castle = image_metrics(CASTLE_PALETTE_REFERENCE)
	with Image.open(PLATE).convert("RGBA") as plate:
		plate_lab = srgb_to_lab(np.asarray(plate.convert("RGB")))
		accent_mask = (
			(plate_lab[..., 0] >= 28.0)
			& (plate_lab[..., 0] <= 88.0)
			& (plate_lab[..., 1] >= -4.0)
			& (plate_lab[..., 2] >= -25.0)
			& (plate_lab[..., 2] <= 22.0)
		)
		accent_lab = plate_lab[accent_mask]
	accent = dict(ground)
	accent["a"] = float(np.median(accent_lab[:, 1]))
	accent["b"] = float(np.median(accent_lab[:, 2]))
	roshan = image_metrics(ROSHAN_PALETTE_REFERENCE)
	bands = {
		"ground": ground,
		"sky": sky,
		"castle": castle,
		"accent": accent,
		"roshan": roshan,
	}
	plate_displayed = 48.0 * ((CANVAS_HEIGHT * 0.5) / math.tan(math.radians(CAM_FOV * 0.5))) / (CAM_DIST - BACKDROP_Z)
	with Image.open(PLATE) as plate_image:
		plate_ratio = plate_image.height / plate_displayed
	results = [evaluate(element, bands, plate_ratio, source) for element in ELEMENTS]
	payload = {
		"scene": "sky_lagoon_promenade",
		"plate": str(PLATE.relative_to(ROOT)).replace("\\", "/"),
		"plate_metrics": {**bands, "authored_to_displayed": plate_ratio},
		"tolerances": TOL,
		"results": results,
		"summary": {
			"passed": sum(1 for result in results if result["pass"]),
			"total": len(results),
		},
	}
	if args.json:
		args.json.parent.mkdir(parents=True, exist_ok=True)
		args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
	for result in results:
		failed = [name for name, passed in result["criteria"].items() if not passed]
		status = "OK" if not failed else "FAIL " + ",".join(failed)
		print(
			f"{result['element']['name']:<24} {status:<20} "
			f"LabDelta={result['derived']['delta_lab']:.1f} "
			f"keyDelta={result['derived']['key_delta']:.0f}deg "
			f"density={result['derived']['density']:.2f}x"
		)
	print(f"SCENE_CONGRUENCY {payload['summary']['passed']}/{payload['summary']['total']}")
	raise SystemExit(0 if payload["summary"]["passed"] == payload["summary"]["total"] else 1)


if __name__ == "__main__":
	main()
