#!/usr/bin/env python3
"""Contract tests for the first-draft character geometry (no Blender needed).

    python3 tools/tests/test_npc_draft.py

Guards the properties the runtime depends on: the shell is closed and
correctly wound, the figure is normalised to exactly 1.0 tall so
main.fit_model() can scale it to any call site's height, UVs stay inside
their own half of the two-panel atlas, and every skin weight sums to 1 over
the declared bone contract.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from npc_draft_lib import (  # noqa: E402
	DRAFT_BONES,
	DraftSpec,
	build_mask,
	build_mesh,
	chain_joints,
	distance_transform,
	height_field,
	skin_weights,
)

FAILURES: list[str] = []


def check(label, cond, detail=""):
	if cond:
		print(f"  ok   {label}")
	else:
		print(f"  FAIL {label} {detail}")
		FAILURES.append(label)


def blob_alpha(w=64, h=96):
	"""A synthetic figure: a round head over a tapering body."""
	yy, xx = np.mgrid[0:h, 0:w]
	head = ((xx - w * 0.5) ** 2 + (yy - h * 0.22) ** 2) < (w * 0.20) ** 2
	body = (np.abs(xx - w * 0.5) < w * 0.30 * (1.0 - (yy - h * 0.4) / (h * 1.4))) & (yy > h * 0.32)
	return np.where(head | body, 255, 0).astype(np.uint8)


def test_distance_transform():
	m = np.zeros((9, 9), dtype=bool)
	m[3:6, 3:6] = True
	d = distance_transform(m)
	check("DT is zero outside the shape", d[0, 0] == 0.0)
	check("DT peaks at the centre", abs(d[4, 4] - 2.0) < 1e-6, f"got {d[4, 4]}")
	check("DT is 1 on the shape's border ring", abs(d[3, 4] - 1.0) < 1e-6, f"got {d[3, 4]}")


def test_height_field():
	mask = build_mask(blob_alpha())
	hf = height_field(mask, 0.2)
	check("height is zero off the figure", float(hf[~mask].max()) == 0.0)
	check("height never exceeds the requested depth", float(hf.max()) <= 0.2 + 1e-6)
	check("height is positive somewhere on the figure", float(hf.max()) > 0.05)


def test_mesh_is_a_closed_shell():
	mask = build_mask(blob_alpha())
	dm = build_mesh(mask, DraftSpec("t", "-", "test", grid=48, depth=0.18))

	# every edge shared by exactly two faces == watertight manifold
	edges: dict[tuple[int, int], int] = {}
	for face in dm.faces:
		for i in range(len(face)):
			a, b = face[i], face[(i + 1) % len(face)]
			edges[(min(a, b), max(a, b))] = edges.get((min(a, b), max(a, b)), 0) + 1
	bad = [e for e, n in edges.items() if n != 2]
	check("shell is watertight (every edge used twice)", not bad, f"{len(bad)} bad edges")

	groups = set(dm.face_group)
	check("mesh has front, back and rim faces", groups == {0, 1, 2}, str(groups))
	check("uv list is parallel to the face list", len(dm.face_uvs) == len(dm.faces))


def test_normalisation():
	mask = build_mask(blob_alpha())
	dm = build_mesh(mask, DraftSpec("t", "-", "test", grid=48, depth=0.18))
	z = dm.verts[:, 2]
	check("figure is exactly 1.0 tall", abs(float(z.max() - z.min()) - 1.0) < 1e-5,
		  f"got {float(z.max() - z.min())}")
	check("figure stands on z=0", abs(float(z.min())) < 1e-5, f"got {float(z.min())}")
	x = dm.verts[:, 0]
	check("figure is centred in x", abs(float(x.max() + x.min())) < 1e-5)


def test_atlas_uv_split():
	mask = build_mask(blob_alpha())
	dm = build_mesh(mask, DraftSpec("t", "-", "test", grid=48, depth=0.18))
	for group, lo, hi, label in ((0, 0.0, 0.5, "front"), (1, 0.5, 1.0, "rear")):
		us = [u for g, corners in zip(dm.face_group, dm.face_uvs) if g == group
			  for u, _v in corners]
		check(f"{label} faces stay in the {label} atlas panel",
			  us and min(us) >= lo - 1e-6 and max(us) <= hi + 1e-6,
			  f"[{min(us):.3f}, {max(us):.3f}]" if us else "no faces")
	# the rim wraps the illustration, so it must read the FRONT panel
	rim_us = [u for g, corners in zip(dm.face_group, dm.face_uvs) if g == 2
			  for u, _v in corners]
	check("rim samples the front panel (its own outline colour)",
		  rim_us and max(rim_us) <= 0.5 + 1e-6)
	vs = [v for corners in dm.face_uvs for _u, v in corners]
	check("all v coordinates are inside the atlas", min(vs) >= -1e-6 and max(vs) <= 1 + 1e-6)


def test_rig_and_weights():
	joints = chain_joints(0.55)
	names = [n for n, _p, _z in joints]
	check("rig matches the declared bone contract", names == DRAFT_BONES or
		  sorted(names) == sorted(DRAFT_BONES), str(names))
	check("only root is parentless", sum(1 for _n, p, _z in joints if p is None) == 1)
	heights = {n: z for n, _p, z in joints}
	check("tail descends below the pivot", heights["tail8"] < heights["tail1"] < 0.55)
	check("head sits above the pivot", heights["head"] > heights["chest"] > 0.55)

	verts = np.zeros((200, 3), dtype=np.float32)
	verts[:, 2] = np.linspace(0.0, 1.0, 200)
	weights = skin_weights(verts, 0.55)
	check("every vertex is weighted", all(w for w in weights))
	sums = [sum(w.values()) for w in weights]
	check("weights are normalised", max(abs(s - 1.0) for s in sums) < 1e-5)
	used = {b for w in weights for b in w}
	check("weights only reference contract bones", used <= set(DRAFT_BONES),
		  str(used - set(DRAFT_BONES)))


def main():
	for fn in (test_distance_transform, test_height_field, test_mesh_is_a_closed_shell,
			   test_normalisation, test_atlas_uv_split, test_rig_and_weights):
		print(f"{fn.__name__}:")
		fn()
	print()
	if FAILURES:
		print(f"FAIL: {len(FAILURES)} check(s) failed")
		sys.exit(1)
	print("ALL OK")


if __name__ == "__main__":
	main()
