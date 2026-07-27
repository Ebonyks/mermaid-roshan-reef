#!/usr/bin/env python3
"""Shell-orientation gate for authored GLB kits.

Blender's viewport and EEVEE flip the shading normal on a backface, so an
inside-out mesh looks perfect in a QA turntable and only fails in-engine.
Godot does not flip: `assets/shaders/cel.gdshader` clamps dot(NORMAL, LIGHT)
to zero, so an inverted shell loses ALL diffuse light and renders BLACK,
while its Fresnel rim saturates into white edge fizz.  That is exactly how
the Sky Lagoon PNW woody set shipped (audit 2026-07-27).

The check is geometric, not stylistic: weld every primitive of an asset by
position, split into connected components, and require the signed volume of
each closed component to be positive (outward-facing).  Open components —
banners, cards, single-sided decals — have no meaningful sign and are
reported as `open`, never failed.

Usage:
    python3 tools/audit_glb_shell_orientation.py <glob> [<glob> ...]
Exits nonzero if any closed shell faces inward.
"""

from __future__ import annotations

import glob
import json
import struct
import sys
from collections import defaultdict

COMPONENT_FORMAT = {5121: ("B", 1), 5123: ("H", 2), 5125: ("I", 4), 5126: ("f", 4)}
COMPONENT_COUNT = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}
# Shells thinner than this in their smallest dimension are treated as open
# ribbons: their signed volume is numerically meaningless.
MINIMUM_CLOSED_VOLUME = 1.0e-6


def load(path: str) -> tuple[dict, bytes]:
	data = open(path, "rb").read()
	offset, document, binary = 12, None, b""
	while offset < len(data):
		length, kind = struct.unpack_from("<II", data, offset)
		chunk = data[offset + 8:offset + 8 + length]
		if kind == 0x4E4F534A:
			document = json.loads(chunk)
		elif kind == 0x004E4942:
			binary = chunk
		offset += 8 + length
	if document is None:
		raise ValueError("missing glTF JSON chunk")
	return document, binary


def read_accessor(document: dict, binary: bytes, index: int) -> list[tuple]:
	accessor = document["accessors"][index]
	view = document["bufferViews"][accessor["bufferView"]]
	fmt, size = COMPONENT_FORMAT[accessor["componentType"]]
	count = COMPONENT_COUNT[accessor["type"]]
	base = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
	stride = view.get("byteStride") or size * count
	return [struct.unpack_from("<" + fmt * count, binary, base + i * stride)
		for i in range(accessor["count"])]


def audit(path: str) -> tuple[int, int, int]:
	"""Return (inward shells, closed shells, open components) for one GLB."""
	document, binary = load(path)
	# Exporters split one authored shell into one primitive per material, so
	# every primitive in the file has to be welded together before the walk.
	welded: dict[tuple, int] = {}
	positions: list[tuple] = []
	triangles: list[tuple[int, int, int]] = []
	for mesh in document.get("meshes", []):
		for primitive in mesh.get("primitives", []):
			if "indices" not in primitive:
				continue
			points = read_accessor(document, binary, primitive["attributes"]["POSITION"])
			local: list[int] = []
			for point in points:
				key = (round(point[0], 5), round(point[1], 5), round(point[2], 5))
				if key not in welded:
					welded[key] = len(positions)
					positions.append(point)
				local.append(welded[key])
			indices = [value[0] for value in read_accessor(document, binary, primitive["indices"])]
			for start in range(0, len(indices) - 2, 3):
				triangles.append((local[indices[start]], local[indices[start + 1]],
					local[indices[start + 2]]))

	parent = list(range(len(positions)))

	def find(node: int) -> int:
		while parent[node] != node:
			parent[node] = parent[parent[node]]
			node = parent[node]
		return node

	def union(a: int, b: int) -> None:
		a, b = find(a), find(b)
		if a != b:
			parent[a] = b

	edges: dict[int, defaultdict] = {}
	for a, b, c in triangles:
		union(a, b)
		union(b, c)
	volume: defaultdict = defaultdict(float)
	boundary: defaultdict = defaultdict(int)
	edge_use: defaultdict = defaultdict(int)
	for a, b, c in triangles:
		A, B, C = positions[a], positions[b], positions[c]
		signed = (A[0] * (B[1] * C[2] - B[2] * C[1])
			- A[1] * (B[0] * C[2] - B[2] * C[0])
			+ A[2] * (B[0] * C[1] - B[1] * C[0])) / 6.0
		volume[find(a)] += signed
		for edge in ((a, b), (b, c), (c, a)):
			edge_use[(find(a), frozenset(edge))] += 1
	for (component, _edge), uses in edge_use.items():
		if uses != 2:
			boundary[component] += 1

	inward = closed = open_parts = 0
	for component, signed in volume.items():
		if boundary[component] or abs(signed) < MINIMUM_CLOSED_VOLUME:
			open_parts += 1
			continue
		closed += 1
		if signed < 0.0:
			inward += 1
	return inward, closed, open_parts


def main() -> None:
	patterns = sys.argv[1:]
	if not patterns:
		raise SystemExit("usage: audit_glb_shell_orientation.py <glob> [<glob> ...]")
	failures = 0
	checked = 0
	for pattern in patterns:
		for path in sorted(glob.glob(pattern)):
			checked += 1
			inward, closed, open_parts = audit(path)
			status = "FAIL" if inward else "OK"
			if inward:
				failures += 1
			print(f"GLBNORMALS|{status}|{path}|inward={inward}|closed={closed}|open={open_parts}")
	if failures:
		print(f"GLBNORMALS|RESULT|FAIL|assets={checked}|inverted_assets={failures}")
		raise SystemExit(1)
	print(f"GLBNORMALS|RESULT|OK|assets={checked}")


if __name__ == "__main__":
	main()
