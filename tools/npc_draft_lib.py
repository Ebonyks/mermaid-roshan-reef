#!/usr/bin/env python3
"""Geometry + texture maths for the first-draft NPC character models.

Pure numpy/Pillow — no Blender import here, so the shape work can be unit
tested and previewed without spinning up bpy (tools/tests/test_npc_draft.py).
tools/build_npc_draft.py owns the Blender half (rig, skin, idle, GLB).

THE IDEA
--------
Every friend in this game is a piece of irreplaceable book art: a flat RGBA
cutout with a hand-painted face. We are not allowed to redesign it and we
have no second view of it, so a "3D model" here means the one honest
reconstruction a single view supports — a *pressed toy figure*:

    alpha silhouette -> euclidean distance transform -> dome height field

The distance transform makes the figure thickest along its medial axis and
thin at the outline, so a tail fin comes out as a thin rounded blade and a
torso as a full rounded mass. Front surface carries the original art, back
surface is a flat painted pastel, and the two are joined by a thin ink-dark
rim wall that reads as the pre-drawn outline the art direction asks for.

Nothing is invented: every colour on the figure is sampled from the book art.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageFilter

# alpha above this counts as "figure"; the book cutouts are cleanly matted so
# a mid threshold avoids both halo fringes and eaten-away soft edges
ALPHA_THRESHOLD = 110
# nearest power-of-two texture sizes we are willing to emit (hard rule:
# <=1024 longest side OR power-of-two — these are both)
POT_SIZES = (256, 512, 1024)


@dataclass
class DraftSpec:
	"""One character's conversion recipe."""

	key: str                    # output stem, matches the sprite `tex` name
	source: str                 # repo-relative RGBA book art
	title: str                  # human name for docs/licences
	depth: float = 0.26         # front dome depth, in figure-height units
	back_ratio: float = 0.42    # back dome depth as a fraction of the front
	pivot: float = 0.55         # height (0=base, 1=top) where tail meets torso
	sway: float = 1.0           # idle sway amplitude multiplier
	grid: int = 150             # sampling columns across the figure's width
	tri_budget: int = 9000      # decimated triangle target (3-4 year old phone)
	tex_max: int = 1024         # longest texture side, rounded to a power of two
	kind: str = "merfolk"       # merfolk | land — picks the idle flavour
	notes: str = ""
	# characters whose art contains more than one figure; recorded so the
	# audit and later per-figure work orders stay honest about it
	figures: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# distance transform (Felzenszwalb & Huttenlocher, exact, no scipy)
# --------------------------------------------------------------------------

def _dt_1d(f: np.ndarray) -> np.ndarray:
	"""Squared euclidean distance transform of a 1D sampled function."""
	n = f.shape[0]
	d = np.empty(n, dtype=np.float64)
	v = np.zeros(n, dtype=np.int64)
	z = np.empty(n + 1, dtype=np.float64)
	k = 0
	v[0] = 0
	z[0] = -np.inf
	z[1] = np.inf
	for q in range(1, n):
		while True:
			p = v[k]
			s = ((f[q] + q * q) - (f[p] + p * p)) / (2.0 * q - 2.0 * p)
			if s <= z[k]:
				k -= 1
				if k < 0:
					k = 0
					break
			else:
				break
		k += 1
		v[k] = q
		z[k] = s
		z[k + 1] = np.inf
	k = 0
	for q in range(n):
		while z[k + 1] < q:
			k += 1
		p = v[k]
		d[q] = (q - p) * (q - p) + f[p]
	return d


def distance_transform(mask: np.ndarray) -> np.ndarray:
	"""Euclidean distance from every True pixel to the nearest False pixel."""
	big = 1e12
	f = np.where(mask, big, 0.0)
	# columns, then rows — separable
	for x in range(f.shape[1]):
		f[:, x] = _dt_1d(f[:, x])
	for y in range(f.shape[0]):
		f[y, :] = _dt_1d(f[y, :])
	return np.sqrt(np.maximum(f, 0.0))


# --------------------------------------------------------------------------
# silhouette clean-up
# --------------------------------------------------------------------------

def _largest_components(mask: np.ndarray, keep_frac: float = 0.004) -> np.ndarray:
	"""Drop speckle: keep every blob holding at least `keep_frac` of the ink.

	Iterative flood fill would be slow at 1k²; a label-propagation sweep over
	a boolean array is plenty for the handful of blobs these cutouts have.
	"""
	h, w = mask.shape
	labels = np.zeros((h, w), dtype=np.int32)
	nxt = 0
	stack: list[tuple[int, int]] = []
	sizes: dict[int, int] = {}
	for sy in range(h):
		row = mask[sy]
		for sx in range(w):
			if not row[sx] or labels[sy, sx]:
				continue
			nxt += 1
			labels[sy, sx] = nxt
			stack.append((sy, sx))
			count = 0
			while stack:
				cy, cx = stack.pop()
				count += 1
				for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
					if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not labels[ny, nx]:
						labels[ny, nx] = nxt
						stack.append((ny, nx))
			sizes[nxt] = count
	if not sizes:
		return mask
	total = sum(sizes.values())
	keep = {i for i, c in sizes.items() if c >= max(24, total * keep_frac)}
	out = np.zeros_like(mask)
	for i in keep:
		out |= labels == i
	return out


def build_mask(alpha: np.ndarray) -> np.ndarray:
	"""Binary figure mask from the art's alpha channel."""
	mask = alpha >= ALPHA_THRESHOLD
	return _largest_components(mask)


# --------------------------------------------------------------------------
# texture prep
# --------------------------------------------------------------------------

def _nearest_pot(value: int) -> int:
	return min(POT_SIZES, key=lambda p: abs(math.log(p / max(value, 1))))


def bleed_edges(rgb: np.ndarray, mask: np.ndarray, rounds: int = 24) -> np.ndarray:
	"""Push figure colour outward into the matte.

	The mesh silhouette is a polygonal approximation of the mask, so boundary
	triangles can sample a texel just outside it. Without bleed those texels
	are white paper and the figure gets a bright fringe.
	"""
	out = rgb.astype(np.float32).copy()
	filled = mask.copy()
	for _ in range(rounds):
		if filled.all():
			break
		# 4-neighbour average of already-filled pixels
		acc = np.zeros_like(out)
		cnt = np.zeros(filled.shape, dtype=np.float32)
		for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
			shifted = np.roll(filled, (dy, dx), axis=(0, 1))
			vals = np.roll(out, (dy, dx), axis=(0, 1))
			acc += vals * shifted[..., None]
			cnt += shifted
		grow = (~filled) & (cnt > 0)
		if not grow.any():
			break
		safe = np.maximum(cnt, 1.0)[..., None]
		out[grow] = (acc / safe)[grow]
		filled |= grow
	return np.clip(out, 0, 255).astype(np.uint8)


def dominant_back_color(rgb: np.ndarray, mask: np.ndarray) -> tuple[float, float, float]:
	"""A soft pastel for the unpainted back of the figure.

	Median of the figure's own pixels, lifted toward white so the back reads
	as painted resin rather than a black hole — every channel still comes
	from the book art, nothing is invented.
	"""
	pix = rgb[mask]
	if pix.size == 0:
		return (0.80, 0.78, 0.86)
	med = np.median(pix.astype(np.float32), axis=0) / 255.0
	lifted = med * 0.78 + 0.16
	return tuple(float(min(1.0, max(0.0, c))) for c in lifted)


def prepare_texture(img: Image.Image, mask: np.ndarray,
					longest: int = 1024) -> tuple[Image.Image, tuple[float, float, float]]:
	"""Build the two-panel character atlas.

	    | front art | blurred rear |

	The rear panel is the same art pushed through a heavy blur: at the back of
	the figure you read hair colour over dress colour over tail colour in the
	right places, but no facial features survive, so the model never looks
	two-faced. It is still 100% book-art pixels — no rear view is invented,
	only defocused. Both panels share one power-of-two image and one material.
	"""
	rgb = np.array(img.convert("RGB"))
	bled = bleed_edges(rgb, mask)
	back = dominant_back_color(rgb, mask)
	h, w = mask.shape
	# the two panels sit side by side, so a panel may be half the atlas wide
	# and the full atlas tall; never upscale past the source art
	cap_w, cap_h = max(128, longest // 2), longest
	scale = min(cap_h / float(h), cap_w / float(w), 1.0)
	tw = min(_nearest_pot(int(round(w * scale))), cap_w)
	th = min(_nearest_pot(int(round(h * scale))), cap_h)
	front = Image.fromarray(bled).resize((tw, th), Image.LANCZOS)
	# a whisper of blur kills resampling crunch on the line art
	front = front.filter(ImageFilter.GaussianBlur(0.35))

	rear = front.filter(ImageFilter.GaussianBlur(max(4.0, tw / 22.0)))
	rear = Image.blend(rear, Image.new("RGB", rear.size,
									   tuple(int(c * 255) for c in back)), 0.35)

	atlas = Image.new("RGB", (tw * 2, th), (255, 255, 255))
	atlas.paste(front, (0, 0))
	atlas.paste(rear, (tw, 0))
	return atlas, back


# --------------------------------------------------------------------------
# height field + mesh
# --------------------------------------------------------------------------

def height_field(mask: np.ndarray, depth: float) -> np.ndarray:
	"""Rounded dome over the silhouette, in the same units as the mask height."""
	dist = distance_transform(mask)
	inside = dist[mask]
	if inside.size == 0:
		return np.zeros_like(dist)
	# p92 rather than max: one fat blob (a torso) shouldn't flatten every
	# thinner limb in the figure to a sliver
	ref = max(float(np.percentile(inside, 92.0)), 1.0)
	nd = np.clip(dist / ref, 0.0, 1.0)
	dome = np.sqrt(np.clip(1.0 - (1.0 - nd) ** 2, 0.0, 1.0))
	return dome * depth * mask


@dataclass
class DraftMesh:
	verts: np.ndarray            # (N,3) float32, Blender Z-up, figure 1.0 tall
	faces: list[tuple[int, ...]]
	face_uvs: list[list[tuple[float, float]]]   # per-loop, parallel to `faces`
	face_group: list[int]        # 0 front, 1 back, 2 rim
	height: float                # normalised, always 1.0
	tri_count: int


def build_mesh(mask: np.ndarray, spec: DraftSpec) -> DraftMesh:
	"""Turn the silhouette into a closed front/back/rim shell.

	Geometry lives on *cells*: a cell is solid when all four of its corner
	samples are inside the mask. Front and back caps get one quad per solid
	cell; every cell edge facing a hollow neighbour gets a rim quad. That is
	watertight by construction and handles interior holes (the gap under an
	arm) with no special casing.
	"""
	h, w = mask.shape
	gx = max(16, int(spec.grid))
	gy = max(16, int(round(gx * h / max(w, 1))))

	# corner samples on a (gy+1) x (gx+1) lattice
	ys = np.linspace(0, h - 1, gy + 1)
	xs = np.linspace(0, w - 1, gx + 1)
	yi = np.clip(np.round(ys).astype(int), 0, h - 1)
	xi = np.clip(np.round(xs).astype(int), 0, w - 1)
	corner_in = mask[np.ix_(yi, xi)]

	field = height_field(mask, spec.depth)
	corner_h = field[np.ix_(yi, xi)]

	# solid cells: all four corners inside
	solid = (corner_in[:-1, :-1] & corner_in[1:, :-1]
			 & corner_in[:-1, 1:] & corner_in[1:, 1:])
	if not solid.any():
		raise ValueError(f"{spec.key}: silhouette vanished at grid {gx}")

	# a corner is used when it touches a solid cell
	used = np.zeros_like(corner_in)
	used[:-1, :-1] |= solid
	used[1:, :-1] |= solid
	used[:-1, 1:] |= solid
	used[1:, 1:] |= solid

	# a used corner is on the rim when any of its four cells is hollow
	padded = np.zeros((solid.shape[0] + 2, solid.shape[1] + 2), dtype=bool)
	padded[1:-1, 1:-1] = solid
	cells_around = (padded[:-1, :-1].astype(int) + padded[1:, :-1]
					+ padded[:-1, 1:] + padded[1:, 1:])
	rim = used & (cells_around < 4)

	# normalised object space: figure exactly 1.0 tall, centred in X, base at 0
	unit = 1.0 / max(h - 1, 1)
	rim_thickness = 0.006

	front_idx = -np.ones(corner_in.shape, dtype=np.int64)
	back_idx = -np.ones(corner_in.shape, dtype=np.int64)
	verts: list[tuple[float, float, float]] = []
	art_uv: dict[tuple[int, int], tuple[float, float]] = {}
	cx = (w - 1) * 0.5

	for r in range(corner_in.shape[0]):
		for c in range(corner_in.shape[1]):
			if not used[r, c]:
				continue
			px, py = xs[c], ys[r]
			ox = (px - cx) * unit
			oz = (h - 1 - py) * unit          # art top -> +Z
			hh = rim_thickness if rim[r, c] else max(float(corner_h[r, c]), rim_thickness)
			art_uv[(r, c)] = (px / max(w - 1, 1),
							  1.0 - py / max(h - 1, 1))   # glTF UV origin is top-left
			front_idx[r, c] = len(verts)
			verts.append((ox, -hh, oz))       # front faces -Y
			back_idx[r, c] = len(verts)
			verts.append((ox, hh * spec.back_ratio, oz))

	# atlas is | front art | blurred rear |, so each cap owns half of u.
	# UVs are per-loop, which lets the rim wall sample the FRONT panel on both
	# of its edges: the wall then wraps the illustration's own outline colour
	# instead of introducing a second material. That matters because collapse
	# decimation does not respect material boundaries — a separate ink rim
	# material bleeds into the caps as black blotches.
	def _front(rc):
		u, v = art_uv[rc]
		return (u * 0.5, v)

	def _rear(rc):
		u, v = art_uv[rc]
		return (0.5 + u * 0.5, v)

	faces: list[tuple[int, ...]] = []
	face_uvs: list[list[tuple[float, float]]] = []
	group: list[int] = []
	sh, sw = solid.shape
	for r in range(sh):
		for c in range(sw):
			if not solid[r, c]:
				continue
			quad = ((r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c))
			faces.append(tuple(int(front_idx[k]) for k in quad))
			face_uvs.append([_front(k) for k in quad])
			group.append(0)
			faces.append(tuple(int(back_idx[k]) for k in reversed(quad)))
			face_uvs.append([_rear(k) for k in reversed(quad)])
			group.append(1)
			# rim walls against hollow neighbours
			for dr, dc, p, q in ((-1, 0, (r, c), (r, c + 1)),
								 (1, 0, (r + 1, c + 1), (r + 1, c)),
								 (0, -1, (r + 1, c), (r, c)),
								 (0, 1, (r, c + 1), (r + 1, c + 1))):
				nr, nc = r + dr, c + dc
				if 0 <= nr < sh and 0 <= nc < sw and solid[nr, nc]:
					continue
				faces.append((int(front_idx[p]), int(front_idx[q]),
							  int(back_idx[q]), int(back_idx[p])))
				face_uvs.append([_front(p), _front(q), _front(q), _front(p)])
				group.append(2)

	varr = np.array(verts, dtype=np.float32)
	# rest on the ground plane and centre horizontally
	varr[:, 2] -= varr[:, 2].min()
	span = max(float(varr[:, 2].max()), 1e-6)
	varr /= span                                  # exactly 1.0 tall
	varr[:, 0] -= (varr[:, 0].max() + varr[:, 0].min()) * 0.5

	return DraftMesh(
		verts=varr,
		faces=faces,
		face_uvs=face_uvs,
		face_group=group,
		height=1.0,
		tri_count=sum(len(f) - 2 for f in faces),
	)


# --------------------------------------------------------------------------
# rig
# --------------------------------------------------------------------------

# The draft chain. Roshan's shipped rig uses the same spine/tail vocabulary
# (tools/glb_check.py ROSHAN_BONES), so a later hand-rig or Meshy retarget can
# map onto these names instead of starting from nothing.
UPPER_CHAIN = ["spine1", "chest", "neck", "head"]
LOWER_CHAIN = [f"tail{i}" for i in range(1, 9)]
DRAFT_BONES = ["root"] + UPPER_CHAIN + LOWER_CHAIN


def chain_joints(pivot: float) -> list[tuple[str, str | None, float]]:
	"""(bone, parent, height) for the draft chain, heights in 0..1."""
	out: list[tuple[str, str | None, float]] = [("root", None, pivot)]
	span_up = max(1.0 - pivot, 0.05)
	prev = "root"
	for i, name in enumerate(UPPER_CHAIN):
		out.append((name, prev, pivot + span_up * (i + 1) / (len(UPPER_CHAIN) + 1)))
		prev = name
	span_dn = max(pivot, 0.05)
	prev = "root"
	for i, name in enumerate(LOWER_CHAIN):
		out.append((name, prev, pivot - span_dn * (i + 1) / len(LOWER_CHAIN)))
		prev = name
	return out


def skin_weights(verts: np.ndarray, pivot: float) -> list[dict[str, float]]:
	"""Blend each vertex between the two chain joints bracketing its height.

	Deterministic and anatomy-free — which is the honest choice when the only
	input is a silhouette. Bone-heat weighting would guess at limbs that the
	relief does not actually separate.
	"""
	joints = chain_joints(pivot)
	ordered = sorted(joints, key=lambda j: j[2])
	names = [j[0] for j in ordered]
	heights = np.array([j[2] for j in ordered], dtype=np.float32)
	out: list[dict[str, float]] = []
	for z in verts[:, 2]:
		idx = int(np.searchsorted(heights, z))
		lo = max(0, min(idx - 1, len(names) - 1))
		hi = max(0, min(idx, len(names) - 1))
		if lo == hi:
			out.append({names[lo]: 1.0})
			continue
		span = float(heights[hi] - heights[lo]) or 1.0
		t = float(np.clip((z - heights[lo]) / span, 0.0, 1.0))
		# smoothstep keeps the seam between segments from creasing
		t = t * t * (3.0 - 2.0 * t)
		out.append({names[lo]: 1.0 - t, names[hi]: t})
	return out
