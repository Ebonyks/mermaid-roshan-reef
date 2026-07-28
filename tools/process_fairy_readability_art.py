#!/usr/bin/env python3
"""Build the Fairy Pond 2D sprite-card runtime family.

The original illustrated subjects and the V4 readability cues remain as
export-excluded source art.  This pass crops transparent padding, scales each
subject consistently, and writes 1024px RGBA cards for Godot's Sprite3D nodes.

Usage:
	python tools/process_fairy_readability_art.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
V2_SOURCE = ROOT / "assets_src" / "fairy_v2" / "runtime_textures"
V4_SOURCE = ROOT / "assets_src" / "fairy_v4" / "runtime_textures"
V5_SOURCE = ROOT / "assets_src" / "fairy_v5" / "runtime_textures"
RUNTIME = ROOT / "assets" / "fairy" / "sprites"
EDGE = 1024
SUBJECT_EDGE = 960

SUBJECTS = {
	"bug_jewel.png": V2_SOURCE / "bug_jewel.png",
	"bug_moth.png": V2_SOURCE / "bug_moth.png",
	"bug_firefly.png": V2_SOURCE / "bug_firefly.png",
	"boss_leaf.png": V2_SOURCE / "boss_leaf.png",
	"boss_seed.png": V2_SOURCE / "boss_seed.png",
	"boss_sprout.png": V2_SOURCE / "boss_sprout.png",
	"boss_bud.png": V2_SOURCE / "boss_bud.png",
	"boss_opening.png": V2_SOURCE / "boss_opening.png",
	"boss_bloom.png": V2_SOURCE / "boss_bloom.png",
	"helpful_flower_gate.png": V4_SOURCE / "helpful_flower_gate.png",
	"danger_thorn_halo.png": V4_SOURCE / "danger_thorn_halo.png",
	"ornament_lily_cluster.png": V5_SOURCE / "ornament_lily_cluster.png",
	"ornament_lavender_reeds.png": V5_SOURCE / "ornament_lavender_reeds.png",
}


def _write_card(source: Path, target: Path) -> None:
	image = Image.open(source).convert("RGBA")
	bounds = image.getchannel("A").getbbox()
	if bounds is None:
		raise ValueError(f"no opaque subject found in {source}")
	image = image.crop(bounds)
	image.thumbnail((SUBJECT_EDGE, SUBJECT_EDGE), Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", (EDGE, EDGE), (0, 0, 0, 0))
	canvas.alpha_composite(
		image,
		((EDGE - image.width) // 2, (EDGE - image.height) // 2),
	)
	target.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(target, format="PNG", optimize=True)


def main() -> None:
	for target_name, source in SUBJECTS.items():
		if not source.exists():
			raise FileNotFoundError(source)
		target = RUNTIME / target_name
		_write_card(source, target)
		print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
	main()
