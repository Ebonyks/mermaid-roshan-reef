#!/usr/bin/env python3
"""Rebuild the craft-studio creature layer sheets on ONE shared canvas each.

Why: every consumer of CREATURE_LAYERS (craft_studio.gd preview,
companion.gd den paint sheets, main.gd _make_creature_node Sprite3D
fallback, sky_lagoon crafted friends) scales each layer independently into
the same box, so the three layers of a creature only register if they share
a single canvas. Art pass 3.5 (b99998ff) shipped fish_body 1024x387,
fish_fins 985x1024 (a loose parts sheet) and left fish_line as the 400x400
outline of the PRE-pass-3.5 fish design - fins floated detached below the
fish and the old line art rendered huge over the new body.

This tool composes the pass-3.5 fin parts onto the pass-3.5 body on one
512x512 canvas (fish) and stamps matching fully-transparent line canvases
(the pass-3.5 style bakes its ink lines into the art; cat/bird have shipped
line-less since day one). Sources are archived under
assets_src/craft_layers_pass35/ so this build is reproducible.

Run from the repo root:  python3 tools/build_craft_layer_canvases.py
Verify with:             python3 tools/audit_craft_layers.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets_src", "craft_layers_pass35")
MG = os.path.join(ROOT, "assets", "mg")

CANVAS = 1024          # working resolution; halved on export
EXPORT = 512           # final canvas (power of two, <=1024 texture rule)

# fin components inside fish_fins_src.png (x0, y0, x1, y1) - measured from
# the alpha channel of the pass-3.5 sheet
FIN_DORSAL = (66, 17, 926, 481)     # big sail fan, base along its bottom edge
FIN_PECTORAL = (344, 524, 669, 703)  # small side fin, cuff at its left
FIN_PELVIC = (589, 749, 967, 1006)   # flowing fin, cuff at its left
FIN_ANAL = (17, 747, 394, 1004)      # mirror twin, cuff at its right

# placement spec on the 1024 working canvas: (scale, rotate_deg_ccw,
# center_x, center_y) per fin, tuned against rendered previews so every fin
# base tucks under the body silhouette (body strip pasted at y 340..727)
PLACE = [
	(FIN_DORSAL, 0.56, 0.0, 512, 302),    # along the back, raked toward the tail
	(FIN_PECTORAL, 0.62, -20.0, 400, 590),  # flank, behind the cheek
	(FIN_PELVIC, 0.50, -46.0, 468, 700),   # hanging under the mid belly
	(FIN_ANAL, 0.44, 42.0, 630, 666),      # second ventral, further aft
]


def compose_fish() -> None:
	body_src = Image.open(os.path.join(SRC, "fish_body_src.png")).convert("RGBA")
	fins_src = Image.open(os.path.join(SRC, "fish_fins_src.png")).convert("RGBA")

	body = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
	body.alpha_composite(body_src, (0, (CANVAS - body_src.size[1]) // 2 + 27))

	fins = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
	for (box, scale, rot, cx, cy) in PLACE:
		part = fins_src.crop(box)
		part = part.resize((max(1, int(part.size[0] * scale)),
			max(1, int(part.size[1] * scale))), Image.LANCZOS)
		if rot:
			part = part.rotate(rot, expand=True, resample=Image.BICUBIC)
		fins.alpha_composite(part, (cx - part.size[0] // 2, cy - part.size[1] // 2))

	line = Image.new("RGBA", (EXPORT, EXPORT), (0, 0, 0, 0))

	body.resize((EXPORT, EXPORT), Image.LANCZOS).save(os.path.join(MG, "fish_body.png"))
	fins.resize((EXPORT, EXPORT), Image.LANCZOS).save(os.path.join(MG, "fish_fins.png"))
	line.save(os.path.join(MG, "fish_line.png"))
	print("fish: body/fins/line exported at %dx%d" % (EXPORT, EXPORT))


def stamp_transparent_lines() -> None:
	# cat and bird body+accent already share a canvas; only their 8x8 line
	# placeholders violate the shared-canvas contract
	for kind in ("cat", "bird"):
		w, h = Image.open(os.path.join(MG, "%s_body.png" % kind)).size
		Image.new("RGBA", (w, h), (0, 0, 0, 0)).save(
			os.path.join(MG, "%s_line.png" % kind))
		print("%s_line: transparent %dx%d canvas" % (kind, w, h))


def main() -> None:
	compose_fish()
	stamp_transparent_lines()


if __name__ == "__main__":
	main()
