#!/usr/bin/env python3
"""Audit every shipped raster asset for *baked lighting* properties.

The 2.5D promenade redesign makes painted flats the primary art channel, which
means most of the game's lighting is now painted into the PNGs rather than
computed by the renderer. This tool measures what is already baked in, so the
runtime lighting can be designed to agree with it instead of fighting it.

Per image (measured over the opaque region only, when an alpha channel exists):

  value range      p01/p50/p99 luminance, crushed and blown pixel fractions
  bake direction   top-vs-bottom and left-vs-right luminance bias, normalised
  shadow colour    hue/saturation of the darkest decile vs the brightest decile
  ink              fraction of near-black low-saturation pixels (outline mass)
  alpha            coverage and soft-edge fraction (cutout vs full-bleed plate)

Writes JSON (machine readable) and a grouped Markdown summary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ANALYSIS_MAX_SIDE = 256
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def _srgb_to_linear(c: np.ndarray) -> np.ndarray:
	return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _luminance(rgb: np.ndarray) -> np.ndarray:
	lin = _srgb_to_linear(rgb)
	return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def _hue_sat(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
	"""Vectorised HSV hue (degrees) and saturation from sRGB in 0..1."""
	mx = rgb.max(axis=-1)
	mn = rgb.min(axis=-1)
	d = mx - mn
	sat = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0.0)
	r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
	hue = np.zeros_like(mx)
	safe = d > 1e-6
	with np.errstate(invalid="ignore", divide="ignore"):
		h_r = ((g - b) / np.maximum(d, 1e-6)) % 6.0
		h_g = ((b - r) / np.maximum(d, 1e-6)) + 2.0
		h_b = ((r - g) / np.maximum(d, 1e-6)) + 4.0
	hue = np.where(mx == r, h_r, np.where(mx == g, h_g, h_b))
	hue = np.where(safe, hue * 60.0, 0.0)
	return hue, sat


def _circular_mean_hue(hue_deg: np.ndarray, weights: np.ndarray | None = None) -> float:
	if hue_deg.size == 0:
		return float("nan")
	rad = np.deg2rad(hue_deg)
	if weights is None:
		x, y = np.cos(rad).mean(), np.sin(rad).mean()
	else:
		w = weights.sum()
		if w <= 0:
			return float("nan")
		x = (np.cos(rad) * weights).sum() / w
		y = (np.sin(rad) * weights).sum() / w
	return float(np.rad2deg(np.arctan2(y, x)) % 360.0)


def _hue_delta(a: float, b: float) -> float:
	"""Signed shortest angular distance a -> b in degrees, -180..180."""
	if np.isnan(a) or np.isnan(b):
		return float("nan")
	return float(((b - a + 180.0) % 360.0) - 180.0)


def analyse(path: Path) -> dict | None:
	try:
		with Image.open(path) as im:
			full_w, full_h = im.size
			fmt = im.format
			mode = im.mode
			im = im.convert("RGBA")
			scale = max(full_w, full_h) / ANALYSIS_MAX_SIDE
			if scale > 1.0:
				im = im.resize(
					(max(1, int(full_w / scale)), max(1, int(full_h / scale))),
					Image.BILINEAR,
				)
			arr = np.asarray(im, dtype=np.float32) / 255.0
	except Exception as exc:  # unreadable / truncated art still needs reporting
		return {"path": str(path), "error": f"{type(exc).__name__}: {exc}"}

	h, w = arr.shape[0], arr.shape[1]
	rgb = arr[..., :3]
	alpha = arr[..., 3]

	has_alpha = mode in ("RGBA", "LA", "PA") or (fmt == "PNG" and float(alpha.min()) < 0.999)
	coverage = float((alpha > 0.5).mean())
	soft_edge = float(((alpha > 0.02) & (alpha < 0.98)).mean())

	mask = alpha > 0.5
	if mask.sum() < 16:
		mask = np.ones_like(alpha, dtype=bool)
		coverage_used = "full"
	else:
		coverage_used = "opaque"

	lum = _luminance(rgb)
	hue, sat = _hue_sat(rgb)

	m_lum = lum[mask]
	m_sat = sat[mask]
	m_hue = hue[mask]

	p01, p10, p50, p90, p99 = np.percentile(m_lum, [1, 10, 50, 90, 99])

	# Baked light direction: luminance bias between opposing thirds of the
	# *masked* region, normalised by overall mean so it reads as a ratio.
	ys, xs = np.nonzero(mask)
	y0, y1 = ys.min(), ys.max()
	x0, x1 = xs.min(), xs.max()
	bh = max(1, (y1 - y0 + 1))
	bw = max(1, (x1 - x0 + 1))
	third_y = max(1, bh // 3)
	third_x = max(1, bw // 3)

	def _region_mean(sl_y, sl_x) -> float:
		sub_mask = mask[sl_y, sl_x]
		if sub_mask.sum() < 8:
			return float("nan")
		return float(lum[sl_y, sl_x][sub_mask].mean())

	top = _region_mean(slice(y0, y0 + third_y), slice(x0, x1 + 1))
	bot = _region_mean(slice(y1 - third_y + 1, y1 + 1), slice(x0, x1 + 1))
	left = _region_mean(slice(y0, y1 + 1), slice(x0, x0 + third_x))
	right = _region_mean(slice(y0, y1 + 1), slice(x1 - third_x + 1, x1 + 1))

	base = max(float(m_lum.mean()), 1e-4)
	vert_bias = (top - bot) / base if not (np.isnan(top) or np.isnan(bot)) else float("nan")
	horiz_bias = (left - right) / base if not (np.isnan(left) or np.isnan(right)) else float("nan")

	# Shadow vs light colour: darkest and brightest deciles inside the mask.
	dark_cut = np.percentile(m_lum, 12)
	light_cut = np.percentile(m_lum, 88)
	dark_sel = m_lum <= dark_cut
	light_sel = m_lum >= light_cut
	shadow_hue = _circular_mean_hue(m_hue[dark_sel], m_sat[dark_sel])
	light_hue = _circular_mean_hue(m_hue[light_sel], m_sat[light_sel])
	shadow_sat = float(m_sat[dark_sel].mean()) if dark_sel.any() else float("nan")
	light_sat = float(m_sat[light_sel].mean()) if light_sel.any() else float("nan")

	ink = float(((m_lum < 0.03) & (m_sat < 0.4)).mean())

	return {
		"path": str(path),
		"w": full_w,
		"h": full_h,
		"format": fmt,
		"mode": mode,
		"bytes": path.stat().st_size,
		"pot": (full_w & (full_w - 1)) == 0 and (full_h & (full_h - 1)) == 0,
		"has_alpha": bool(has_alpha),
		"alpha_coverage": round(coverage, 4),
		"soft_edge_frac": round(soft_edge, 4),
		"measured_over": coverage_used,
		"lum_mean": round(float(m_lum.mean()), 4),
		"lum_p01": round(float(p01), 4),
		"lum_p10": round(float(p10), 4),
		"lum_p50": round(float(p50), 4),
		"lum_p90": round(float(p90), 4),
		"lum_p99": round(float(p99), 4),
		"dyn_range": round(float(p99 - p01), 4),
		"frac_crushed": round(float((m_lum < 0.005).mean()), 4),
		"frac_blown": round(float((m_lum > 0.95).mean()), 4),
		"sat_mean": round(float(m_sat.mean()), 4),
		"vert_bias": None if np.isnan(vert_bias) else round(float(vert_bias), 4),
		"horiz_bias": None if np.isnan(horiz_bias) else round(float(horiz_bias), 4),
		"shadow_hue": None if np.isnan(shadow_hue) else round(shadow_hue, 1),
		"light_hue": None if np.isnan(light_hue) else round(light_hue, 1),
		"hue_shift": None if np.isnan(_hue_delta(light_hue, shadow_hue)) else round(_hue_delta(light_hue, shadow_hue), 1),
		"shadow_sat": None if np.isnan(shadow_sat) else round(shadow_sat, 4),
		"light_sat": None if np.isnan(light_sat) else round(light_sat, 4),
		"ink_frac": round(ink, 4),
	}


def _fmt(v, nd=2):
	if v is None:
		return "-"
	if isinstance(v, float):
		return f"{v:.{nd}f}"
	return str(v)


def main(argv: list[str]) -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("roots", nargs="*", default=["assets"])
	ap.add_argument("--json-out", default="tools/out/lighting_image_audit.json")
	ap.add_argument("--md-out", default="tools/out/lighting_image_audit.md")
	args = ap.parse_args(argv)

	files: list[Path] = []
	for root in args.roots:
		rp = Path(root)
		if rp.is_file():
			files.append(rp)
			continue
		for p in sorted(rp.rglob("*")):
			if p.is_file() and p.suffix.lower() in EXTS:
				files.append(p)

	rows = []
	for i, p in enumerate(files):
		r = analyse(p)
		if r:
			rows.append(r)
		if (i + 1) % 200 == 0:
			print(f"  ... {i + 1}/{len(files)}", file=sys.stderr)

	out_json = Path(args.json_out)
	out_json.parent.mkdir(parents=True, exist_ok=True)
	out_json.write_text(json.dumps(rows, indent=1))

	ok = [r for r in rows if "error" not in r]
	groups: dict[str, list[dict]] = {}
	for r in ok:
		parts = Path(r["path"]).parts
		key = "/".join(parts[:3]) if len(parts) > 3 else "/".join(parts[:-1])
		groups.setdefault(key, []).append(r)

	lines = [
		"# Lighting image audit (generated)",
		"",
		f"{len(rows)} files scanned, {len(rows) - len(ok)} unreadable.",
		"",
		"| group | n | lum p50 | dyn range | crushed% | blown% | vert bias | horiz bias | hue shift | ink% |",
		"|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
	]
	for key in sorted(groups, key=lambda k: -len(groups[k])):
		g = groups[key]

		def col(name):
			vals = [r[name] for r in g if r.get(name) is not None]
			return float(np.median(vals)) if vals else None

		lines.append(
			"| `{}` | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
				key,
				len(g),
				_fmt(col("lum_p50")),
				_fmt(col("dyn_range")),
				_fmt((col("frac_crushed") or 0) * 100, 1),
				_fmt((col("frac_blown") or 0) * 100, 1),
				_fmt(col("vert_bias")),
				_fmt(col("horiz_bias")),
				_fmt(col("hue_shift"), 0),
				_fmt((col("ink_frac") or 0) * 100, 1),
			)
		)
	Path(args.md_out).parent.mkdir(parents=True, exist_ok=True)
	Path(args.md_out).write_text("\n".join(lines) + "\n")
	print(f"wrote {out_json} and {args.md_out} ({len(rows)} rows)")
	return 0


if __name__ == "__main__":
	raise SystemExit(main(sys.argv[1:]))
