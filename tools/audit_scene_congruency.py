#!/usr/bin/env python3
"""Scene congruency gate: does every element in a stage belong to the same picture?

The 2.5D promenade composites Codex-painted murals, cutout standees and the
avatar into ONE frame. If those pieces disagree about palette, key light,
material response or authored detail scale, the child sees stickers pasted on a
painting instead of a world -- the exact gap reported on the Sky Lagoon
promenade (2026-07-27).

This tool makes that gap a number. One element per stage is the PLATE (the
mural the scene is painted on); every other element is measured against it and
must land inside the tolerance band. Elements that fail are the regeneration
work list -- rerun after each Codex batch until the gate is green.

Metrics, per element (masked to alpha > 0.5 for cutouts):
  C1 hue/chroma    -- Lab (a*,b*) centroid distance to the plate band
  C2 key           -- median L*, plus black point (p5) and white point (p95)
  C3 light         -- direction and strength of the luminance gradient
  C4 gloss         -- fraction of hot, desaturated specular pixels
  C5 contrast      -- local RMS contrast (rendering hardness)
  C6 detail scale  -- authored px vs px it actually occupies on the 720p canvas
  C7 grounding     -- does the element get a contact shadow at runtime

C6 is the one that cannot be fixed by recolouring: an element authored at 6x
the plate's detail density reads razor-sharp against a soft painting no matter
how well its palette matches.

Usage:  python3 tools/audit_scene_congruency.py [--json OUT] [--scene sky_lagoon]
Exit 0 when every element passes; 1 otherwise (so CI and the regenerate loop
share one verdict).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- tolerances
# Bands are deliberately generous: the goal is "belongs to the same picture",
# not "identical". Each is stated as the criterion Codex must hit.
TOL = {
	"hue_chroma": 18.0,      # C1  max Lab (a*,b*) centroid distance from plate
	"key_median": 16.0,      # C2  max |median L* - plate median L*|
	"black_point": 14.0,     # C2  max |p5 L* - plate p5 L*|  (shadow depth)
	"white_point": 14.0,     # C2  max |p95 L* - plate p95 L*| (highlight ceiling)
	"light_angle": 45.0,     # C3  max key-light disagreement, degrees
	"gloss_excess": 0.025,   # C4  max specular fraction above the plate's
	"contrast_ratio": 1.9,   # C5  max local-contrast ratio vs plate (either way)
	"oversample_lo": 1.0,    # C6  authored px / displayed px, minimum
	"oversample_hi": 2.5,    # C6  ... and maximum
	"oversample_ratio": 2.0, # C6  max element:plate oversample disagreement
}

# ------------------------------------------------------------------- scenes
# Runtime framing constants mirrored from scripts/arena/sky_lagoon_promenade.gd.
# Sprite world heights are parsed from that file so this table cannot go stale.
SCENES = {
	"sky_lagoon": {
		"source": "scripts/arena/sky_lagoon_promenade.gd",
		"cam_dist": 47.0,
		"cam_fov": 38.0,
		"canvas_h": 720.0,          # project.godot base canvas height
		"plate": {
			"path": "assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_1.png",
			"world_h": 48.0,
			"z": -18.0,
			# standees stand on the lower band; the sky is not the reference
			"band": (0.45, 1.0),
			# ... but a cloud belongs to the painted sky, and judging it against
			# dark foliage would demand a black point no cloud can have. Elements
			# living above the treeline are measured against this band instead.
			"sky_band": (0.0, 0.30),
		},
		"sky_elements": ["sky_lagoon_cloud_family_drift.png"],
		# elements whose world height is NOT from an _add_sprite call
		"extra": {
			"assets/sprites/sky_lagoon/sky_lagoon_activity_frame_v2.png": (12.95, -17.75),
		},
		"default_z": -17.85,
	},
}


# ------------------------------------------------------------------ colour
def srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
	"""rgb float [0,1] (...,3) -> CIE L*a*b* (D65)."""
	m = rgb > 0.04045
	lin = np.where(m, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
	mat = np.array([
		[0.4124564, 0.3575761, 0.1804375],
		[0.2126729, 0.7151522, 0.0721750],
		[0.0193339, 0.1191920, 0.9503041],
	])
	xyz = lin @ mat.T
	white = np.array([0.95047, 1.0, 1.08883])
	t = xyz / white
	d = 6.0 / 29.0
	f = np.where(t > d ** 3, np.cbrt(np.clip(t, 1e-9, None)), t / (3 * d * d) + 4.0 / 29.0)
	return np.stack([
		116.0 * f[..., 1] - 16.0,
		500.0 * (f[..., 0] - f[..., 1]),
		200.0 * (f[..., 1] - f[..., 2]),
	], axis=-1)


def load(path: Path):
	im = Image.open(path).convert("RGBA")
	a = np.asarray(im).astype(np.float32) / 255.0
	return a[..., :3], a[..., 3]


# ----------------------------------------------------------------- metrics
def measure(rgb: np.ndarray, alpha: np.ndarray) -> dict:
	mask = alpha > 0.5
	if mask.sum() < 64:
		return {}
	lab = srgb_to_lab(rgb)
	L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
	Lm = L[mask]

	chroma = np.sqrt(A[mask] ** 2 + B[mask] ** 2)
	# C4 gloss: hot AND desaturated -- a specular, not a bright colour
	gloss = float(((Lm > 92.0) & (chroma < 12.0)).mean())

	# C3 key light: least-squares luminance gradient over the masked region
	ys, xs = np.nonzero(mask)
	yn = (ys - ys.mean()) / max(1.0, ys.std())
	xn = (xs - xs.mean()) / max(1.0, xs.std())
	M = np.stack([xn, yn, np.ones_like(xn)], axis=1)
	coef, *_ = np.linalg.lstsq(M, Lm, rcond=None)
	gx, gy = float(coef[0]), float(coef[1])
	# image y grows downward; flip so 90 deg means "lit from above"
	angle = math.degrees(math.atan2(-gy, gx))
	strength = math.hypot(gx, gy)

	# C5 local contrast: RMS of (pixel - 3x3 neighbourhood mean)
	pad = np.pad(L, 1, mode="edge")
	blur = sum(pad[i:i + L.shape[0], j:j + L.shape[1]]
	           for i in range(3) for j in range(3)) / 9.0
	local = float(np.sqrt(((L - blur)[mask] ** 2).mean()))

	return {
		"pixels": int(mask.sum()),
		"lab_a": float(A[mask].mean()),
		"lab_b": float(B[mask].mean()),
		"chroma": float(chroma.mean()),
		"L_median": float(np.median(Lm)),
		"L_p5": float(np.percentile(Lm, 5)),
		"L_p95": float(np.percentile(Lm, 95)),
		"light_angle": angle,
		"light_strength": strength,
		"gloss": gloss,
		"local_contrast": local,
	}


def parse_elements(scene: dict) -> dict:
	"""World height + depth per texture, read from the stage script."""
	src = (ROOT / scene["source"]).read_text()
	# resolve `const NAME := value` so _add_sprite's z argument is usable
	consts = {n: float(v) for n, v in
	          re.findall(r"^const\s+(\w+)\s*:=\s*(-?\d+\.?\d*)\s*$", src, re.M)}
	out = {}
	def depth(z: str) -> float:
		if z in consts:
			return consts[z]
		try:
			return float(z)
		except ValueError:
			return scene["default_z"]

	# direct standees ...
	for path, z, h in re.findall(
			r'_add_sprite\(\s*\n?\s*"res://([^"]+)",\s*\n?\s*'
			r'Vector3\([^,]+,\s*[^,]+,\s*([A-Z_]+|-?[\d.]+)\),\s*([\d.]+)', src):
		out[path] = (float(h), depth(z))
	# ... and the ambient cards, which reach _add_sprite one call deeper
	for path, z, h in re.findall(
			r'_add_ambient_card\(\s*"[^"]*",\s*\n?\s*"res://([^"]+)",\s*\n?\s*'
			r'Vector3\([^,]+,\s*[^,]+,\s*([A-Z_]+|-?[\d.]+)\),\s*([\d.]+)', src):
		out[path] = (float(h), depth(z))
	for path, (h, z) in scene.get("extra", {}).items():
		out[path] = (h, z)
	return out


def displayed_px(world_h: float, z: float, scene: dict) -> float:
	"""How tall this element actually is on the 720p canvas."""
	dist = scene["cam_dist"] - z
	frustum_h = 2.0 * math.tan(math.radians(scene["cam_fov"] * 0.5)) * dist
	return world_h / frustum_h * scene["canvas_h"]


def judge(name: str, m: dict, plate: dict, authored: float, shown: float,
          plate_over: float, grounded: bool) -> tuple[list, dict]:
	over = authored / max(1.0, shown)
	fails = []
	dc = math.hypot(m["lab_a"] - plate["lab_a"], m["lab_b"] - plate["lab_b"])
	if dc > TOL["hue_chroma"]:
		fails.append(("C1", f"palette {dc:.1f} from plate (max {TOL['hue_chroma']})"))
	if abs(m["L_median"] - plate["L_median"]) > TOL["key_median"]:
		fails.append(("C2", f"key {m['L_median'] - plate['L_median']:+.1f} L*"))
	if abs(m["L_p5"] - plate["L_p5"]) > TOL["black_point"]:
		fails.append(("C2", f"black point {m['L_p5'] - plate['L_p5']:+.1f} L*"))
	if abs(m["L_p95"] - plate["L_p95"]) > TOL["white_point"]:
		fails.append(("C2", f"white point {m['L_p95'] - plate['L_p95']:+.1f} L*"))
	da = abs((m["light_angle"] - plate["light_angle"] + 180) % 360 - 180)
	if da > TOL["light_angle"] and m["light_strength"] > 1.0:
		fails.append(("C3", f"key light {da:.0f} deg off plate"))
	if m["gloss"] - plate["gloss"] > TOL["gloss_excess"]:
		fails.append(("C4", f"specular {m['gloss'] * 100:.1f}% vs plate {plate['gloss'] * 100:.1f}%"))
	cr = m["local_contrast"] / max(0.01, plate["local_contrast"])
	if cr > TOL["contrast_ratio"] or cr < 1.0 / TOL["contrast_ratio"]:
		fails.append(("C5", f"local contrast {cr:.2f}x plate"))
	if over > TOL["oversample_hi"] or over < TOL["oversample_lo"]:
		fails.append(("C6", f"authored {over:.1f}x its {shown:.0f}px display size"))
	if over / max(0.01, plate_over) > TOL["oversample_ratio"] or \
			plate_over / max(0.01, over) > TOL["oversample_ratio"]:
		fails.append(("C6", f"detail density {over / plate_over:.1f}x the plate's"))
	if not grounded:
		fails.append(("C7", "no contact shadow: floats off the painted ground"))
	row = dict(m, name=name, authored_px=authored, display_px=shown, oversample=over,
	           palette_dist=dc, light_delta=da, contrast_ratio=cr,
	           grounded=grounded, fails=[f"{c}: {t}" for c, t in fails])
	return fails, row


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("--scene", default="sky_lagoon")
	ap.add_argument("--json", default="")
	args = ap.parse_args()
	scene = SCENES[args.scene]

	prgb, palpha = load(ROOT / scene["plate"]["path"])
	h = prgb.shape[0]

	def plate_band(key: str) -> dict:
		lo, hi = scene["plate"][key]
		crop = prgb[int(h * lo):int(h * hi)]
		return measure(crop, np.ones(crop.shape[:2], np.float32))

	plate = plate_band("band")
	sky_plate = plate_band("sky_band") if "sky_band" in scene["plate"] else plate
	sky_names = set(scene.get("sky_elements", []))
	plate_shown = displayed_px(scene["plate"]["world_h"], scene["plate"]["z"], scene)
	plate_authored = float(prgb.shape[0])
	plate_over = plate_authored / plate_shown

	print(f"CONGRUENCY|scene={args.scene} plate={Path(scene['plate']['path']).name} "
	      f"authored={plate_authored:.0f}px display={plate_shown:.0f}px "
	      f"oversample={plate_over:.2f}x")
	print(f"CONGRUENCY|plate a*={plate['lab_a']:+.1f} b*={plate['lab_b']:+.1f} "
	      f"L50={plate['L_median']:.1f} L5={plate['L_p5']:.1f} L95={plate['L_p95']:.1f} "
	      f"key={plate['light_angle']:.0f}deg gloss={plate['gloss'] * 100:.1f}% "
	      f"contrast={plate['local_contrast']:.2f}")

	# C7: SideScrollStage.flat() builds a contact-shadow quad under every
	# standee; this stage's own _add_sprite does not. Detect the quad itself --
	# `cast_shadow = ...OFF` is the opposite of grounding, so a plain substring
	# search for "shadow" would false-pass.
	src = (ROOT / scene["source"]).read_text()
	body = src.split("func _add_sprite")[1].split("\nfunc ")[0]
	grounded = ("QuadMesh" in body or "MeshInstance3D" in body) and "SHADOW" not in body.upper().replace(
		"SHADOW_CASTING_SETTING_OFF", "")

	rows, failed = [], 0
	for path, (world_h, z) in sorted(parse_elements(scene).items()):
		full = ROOT / path
		if not full.exists():
			print(f"CONGRUENCY|{path}: FAIL missing")
			failed += 1
			continue
		rgb, alpha = load(full)
		m = measure(rgb, alpha)
		if not m:
			continue
		shown = displayed_px(world_h, z, scene)
		name = Path(path).name
		ref = sky_plate if name in sky_names else plate
		fails, row = judge(name, m, ref, float(rgb.shape[0]), shown,
		                   plate_over, grounded)
		row["reference_band"] = "sky" if name in sky_names else "ground"
		rows.append(row)
		if fails:
			failed += 1
			print(f"CONGRUENCY|{Path(path).name}: FAIL")
			for code, txt in fails:
				print(f"    {code}  {txt}")
		else:
			print(f"CONGRUENCY|{Path(path).name}: OK")

	print(f"CONGRUENCY|RESULT {len(rows) - failed}/{len(rows)} elements congruent")
	if args.json:
		Path(args.json).write_text(json.dumps(
			{"scene": args.scene, "plate": dict(plate, authored_px=plate_authored,
			 display_px=plate_shown, oversample=plate_over),
			 "tolerances": TOL, "elements": rows}, indent=2))
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())
