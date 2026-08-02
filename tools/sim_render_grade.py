#!/usr/bin/env python3
"""Simulate the game's Environment grade over a painted flat.

Painted 2.5D flats are drawn UNSHADED, so no light touches them — but they are
still HDR-composited, glow-bled, ACES-tonemapped and BCS-adjusted by the
WorldEnvironment before the child sees them. This reproduces that chain offline
so an approved PNG can be compared against its actual on-screen result.

Order matches Godot 4's tonemap pass: exposure -> glow composite -> tonemap ->
brightness/contrast/saturation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None

# Grade profiles lifted from scripts/main.gd::_apply_scene_grade and
# scripts/arena/castle_rooms_25d.gd::_sync_castle_environment.
PROFILES = {
	# name: exposure, white, brightness, contrast, saturation,
	#       glow_threshold, glow_intensity, glow_bloom, glow_hdr_scale
	"castle_hall_lit": (0.92, 1.35, 1.12, 1.20, 0.50, 0.58, 1.28, 0.30, 4.20),
	"castle_hall_dark": (0.92, 1.35, 0.84, 1.12, 0.66, 0.98, 0.24, 0.02, 4.20),
	"castle_room": (0.92, 1.62, 0.98, 1.02, 1.02, 0.90, 0.66, 0.09, 2.40),
	"sky_lagoon": (0.72, 1.55, 1.00, 1.04, 1.10, 0.90, 0.95, 0.40, 2.40),
	"bright_pastel": (0.88, 1.62, 0.97, 1.03, 1.04, 0.90, 0.95, 0.40, 2.40),
	"reef_default": (1.15, 1.20, 0.96, 1.03, 0.98, 0.90, 0.95, 0.40, 2.40),
	# Pre-2026-08-02 values, kept so the retune stays demonstrable. Not shipped.
	"legacy_castle_room": (0.92, 1.35, 0.94, 1.10, 1.08, 0.90, 0.66, 0.09, 2.40),
	"legacy_sky_lagoon": (0.72, 1.55, 0.94, 1.16, 1.10, 0.90, 0.95, 0.40, 2.40),
	"legacy_bright_pastel": (0.88, 1.40, 0.95, 1.12, 1.04, 0.90, 0.95, 0.40, 2.40),
	# Reference: what a near-identity "show the painting as painted" pipeline
	# would put on screen. Used to bracket how far the shipped grade travels.
	"neutral": (1.0, 1.0, 1.0, 1.0, 1.0, 4.0, 0.0, 0.0, 4.0),
}

RGB_TO_RRT = np.array([
	[0.59719, 0.35458, 0.04823],
	[0.07600, 0.90834, 0.01566],
	[0.02840, 0.13383, 0.83777],
])
ODT_TO_RGB = np.array([
	[1.60475, -0.53108, -0.07367],
	[-0.10208, 1.10813, -0.00605],
	[-0.00327, -0.07276, 1.07602],
])


def srgb_to_linear(c):
	return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
	c = np.clip(c, 0.0, 1.0)
	return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def tonemap_aces(color, white):
	bias = 1.8
	A, B, C, D, E = 0.0245786, 0.000090537, 0.983729, 0.432951, 0.238081
	c = color @ RGB_TO_RRT.T * bias
	wt = (white * (white + A) - B) / (white * (C * white + D) + E)
	c = (c * (c + A) - B) / (c * (C * c + D) + E)
	c = c @ ODT_TO_RGB.T
	return c / wt


def apply_bcs(color, brightness, contrast, saturation):
	color = color * brightness
	color = 0.5 + (color - 0.5) * contrast
	grey = (color.sum(axis=-1, keepdims=True)) / 3.0
	return grey + (color - grey) * saturation


def render(img: Image.Image, profile: str, light=None):
	exp, white, bri, con, sat, gthr, gint, gbloom, ghdr = PROFILES[profile]
	rgb = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
	lin = srgb_to_linear(rgb) * exp
	if light is not None:
		# shaded=true cards multiply albedo by incoming light before the grade
		lin = lin * np.asarray(light, dtype=np.float32)

	# glow: threshold on HDR luminance, wide blur, SCREEN composite (+ bloom
	# feeds the unthresholded image in, matching _wind_waker_bloom).
	lum = lin @ np.array([0.2126, 0.7152, 0.0722])
	over = np.clip((lum - gthr) / max(1e-3, ghdr - gthr), 0.0, 1.0)[..., None]
	bright = lin * over
	glow_src = bright + lin * gbloom
	gi = Image.fromarray(np.clip(glow_src * 255.0, 0, 255).astype(np.uint8))
	blurred = np.asarray(
		gi.filter(ImageFilter.GaussianBlur(radius=max(2, img.width / 90.0))),
		dtype=np.float32,
	) / 255.0
	glow = srgb_to_linear(blurred) * gint
	lit = 1.0 - (1.0 - np.clip(lin, 0, 1)) * (1.0 - np.clip(glow, 0, 1))  # screen

	mapped = tonemap_aces(lit, white)
	graded = apply_bcs(np.clip(mapped, 0.0, 4.0), bri, con, sat)
	out = linear_to_srgb(graded)
	stats = {
		"frac_over_glow_threshold": float((lum > gthr).mean()),
		"src_mean_lum": float(lum.mean() / max(exp, 1e-6)),
		"out_mean_lum": float((srgb_to_linear(out) @ np.array([0.2126, 0.7152, 0.0722])).mean()),
	}
	return Image.fromarray(np.clip(out * 255.0, 0, 255).astype(np.uint8)), stats


def main(argv):
	ap = argparse.ArgumentParser()
	ap.add_argument("image")
	ap.add_argument("profile", choices=sorted(PROFILES))
	ap.add_argument("--out", required=True)
	ap.add_argument("--side-by-side", action="store_true")
	ap.add_argument("--light", default="", help="r,g,b light multiply for shaded cards")
	a = ap.parse_args(argv)

	src = Image.open(a.image).convert("RGB")
	if max(src.size) > 900:
		src.thumbnail((900, 900), Image.LANCZOS)
	light = [float(x) for x in a.light.split(",")] if a.light else None
	out, stats = render(src, a.profile, light)
	if a.side_by_side:
		combo = Image.new("RGB", (src.width * 2 + 8, src.height), (20, 20, 24))
		combo.paste(src, (0, 0))
		combo.paste(out, (src.width + 8, 0))
		combo.save(a.out)
	else:
		out.save(a.out)
	print(a.profile, {k: round(v, 4) for k, v in stats.items()})
	return 0


if __name__ == "__main__":
	raise SystemExit(main(sys.argv[1:]))
