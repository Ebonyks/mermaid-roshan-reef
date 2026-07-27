#!/usr/bin/env python3
"""Static QA for the craft-studio creature layer sheets (assets/mg).

Contract: the three layers of every CREATURE_LAYERS creature (accent, body,
line) MUST share one canvas. Every consumer - craft_studio.gd's preview,
companion.gd's den paint sheets, main.gd's _make_creature_node Sprite3D
fallback (also used by sky_lagoon crafted friends) - scales each layer
independently into the same box, so differing canvases render misregistered
(art pass 3.5 shipped fish fins floating detached below the fish and the
old 400x400 line art stretched huge over the new body).

The trios are parsed from CREATURE_LAYERS in scripts/main.gd so a new
creature is guarded the moment it is added. Exit 1 on any violation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MG = ROOT / "assets" / "mg"
MAIN = ROOT / "scripts" / "main.gd"


def creature_layers() -> dict[str, list[str]]:
	source = MAIN.read_text(encoding="utf-8")
	match = re.search(r"const CREATURE_LAYERS\s*:?=\s*(\{.*?\})", source, re.DOTALL)
	if match is None:
		raise SystemExit("audit_craft_layers: CREATURE_LAYERS not found in scripts/main.gd")
	trios: dict[str, list[str]] = {}
	for kind, body in re.findall(r'"(\w+)"\s*:\s*\[([^\]]*)\]', match.group(1)):
		trios[kind] = re.findall(r'"([\w]+)"', body)
	return trios


def main() -> int:
	failures: list[str] = []
	trios = creature_layers()
	if not trios:
		failures.append("CREATURE_LAYERS parsed empty")
	for kind, layers in trios.items():
		sizes: dict[str, tuple[int, int]] = {}
		for name in layers:
			path = MG / f"{name}.png"
			if not path.is_file():
				failures.append(f"{kind}: missing layer {path.relative_to(ROOT)}")
				continue
			with Image.open(path) as image:
				sizes[name] = image.size
				width, height = image.size
			power_of_two = (width & (width - 1) == 0) and (height & (height - 1) == 0)
			if max(width, height) > 1024 and not power_of_two:
				failures.append(f"{kind}: {name}.png {width}x{height} breaks the <=1024-or-POT texture rule")
		if len(set(sizes.values())) > 1:
			detail = ", ".join(f"{n} {w}x{h}" for n, (w, h) in sizes.items())
			failures.append(f"{kind}: layers on mismatched canvases ({detail}) - "
				"all three must share one canvas (tools/build_craft_layer_canvases.py)")
	for failure in failures:
		print(f"FAIL craft-layers: {failure}")
	if not failures:
		print(f"craft-layers OK: {len(trios)} creatures, shared canvas per trio")
	return 1 if failures else 0


if __name__ == "__main__":
	sys.exit(main())
