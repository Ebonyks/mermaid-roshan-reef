#!/usr/bin/env python3
"""Extract isolated, row-major character cells from a chroma-keyed imp sheet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def sha256(path: Path) -> str:
	hash_value = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			hash_value.update(chunk)
	return hash_value.hexdigest()


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", type=Path, required=True)
	parser.add_argument("--family", required=True)
	parser.add_argument("--sheet", choices=("a", "b", "c", "d"), required=True)
	parser.add_argument("--candidates-dir", type=Path, required=True)
	parser.add_argument("--report", type=Path, required=True)
	args = parser.parse_args()

	if args.sheet == "a":
		states = ("idle", "windup", "charge", "slash", "recover", "guard")
		rows = 2
	elif args.sheet == "b":
		states = ("stagger", "flee", "bopped", "bow", "hop_a", "hop_b", "taunt")
		rows = 3
	elif args.sheet == "c":
		states = ("stagger", "bopped", "bow")
		rows = 1
	else:
		states = ("stagger", "flee", "bopped")
		rows = 1
	image = Image.open(args.input).convert("RGBA")
	pixels = np.asarray(image)
	visible = pixels[:, :, 3] >= 16
	labels, count = ndimage.label(visible, structure=np.ones((3, 3), dtype=np.uint8))
	components: list[dict[str, object]] = []
	for label_id in range(1, count + 1):
		positions = np.argwhere(labels == label_id)
		if positions.shape[0] < 2000:
			continue
		y0, x0 = positions.min(axis=0)
		y1, x1 = positions.max(axis=0) + 1
		cy, cx = positions.mean(axis=0)
		components.append({
			"label": label_id,
			"area": int(positions.shape[0]),
			"bbox": [int(x0), int(y0), int(x1), int(y1)],
			"centroid": [float(cx), float(cy)],
		})

	height, width = pixels.shape[:2]
	groups: dict[tuple[int, int], list[dict[str, object]]] = {}
	for component in components:
		cx, cy = component["centroid"]
		cell = (
			min(int(cy / (height / rows)), rows - 1),
			min(int(cx / (width / 3)), 2),
		)
		groups.setdefault(cell, []).append(component)
	ordered_groups = [groups[cell] for cell in sorted(groups)]
	if len(ordered_groups) != len(states):
		raise SystemExit(
			f"expected {len(states)} occupied grid cells, found {len(ordered_groups)}: {groups}"
		)
	args.candidates_dir.mkdir(parents=True, exist_ok=True)
	outputs: list[dict[str, object]] = []
	for state, group in zip(states, ordered_groups, strict=True):
		label_ids = [int(component["label"]) for component in group]
		primary = np.isin(labels, label_ids)
		support = ndimage.binary_dilation(primary, structure=np.ones((3, 3)), iterations=3)
		support &= pixels[:, :, 3] > 0
		positions = np.argwhere(support)
		y0, x0 = positions.min(axis=0)
		y1, x1 = positions.max(axis=0) + 1
		pad = 8
		x0 = max(0, int(x0) - pad)
		y0 = max(0, int(y0) - pad)
		x1 = min(width, int(x1) + pad)
		y1 = min(height, int(y1) + pad)
		crop_pixels = pixels[y0:y1, x0:x1].copy()
		crop_support = support[y0:y1, x0:x1]
		crop_pixels[~crop_support] = 0
		stem = args.family if state == "idle" else f"{args.family}_{state}"
		output = args.candidates_dir / f"{stem}_sheet_{args.sheet}_attempt01_alpha_crop_native.png"
		Image.fromarray(crop_pixels, "RGBA").save(output)
		outputs.append({
			"state": state,
			"source_components": group,
			"crop_bbox": [x0, y0, x1, y1],
			"output": str(output),
			"output_sha256": sha256(output),
		})

	report = {
		"pass": True,
		"method": "grid-cell grouping of 8-connected alpha components; 3px matte support; 8px crop padding",
		"input": str(args.input),
		"input_sha256": sha256(args.input),
		"sheet": args.sheet,
		"states": list(states),
		"component_count": len(components),
		"occupied_grid_cells": len(ordered_groups),
		"outputs": outputs,
	}
	args.report.parent.mkdir(parents=True, exist_ok=True)
	args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(report, indent=2))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
