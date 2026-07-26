#!/usr/bin/env python3
"""Blender first-draft 3D characters for the whole 2D cast.

    python3 tools/build_npc_draft.py --all
    python3 tools/build_npc_draft.py huluu kareem --preview

Runs against the pip `bpy` module (pip install bpy) so it works in a headless
session with no Blender binary, and equally under
`blender --background --python tools/build_npc_draft.py -- --all`.

WHAT IT MAKES
-------------
For each character: a closed, rigged, idle-animated GLB whose front face is
the untouched book art. See tools/npc_draft_lib.py for the geometry idea.
Materials are unlit — the art direction forbids re-lighting the book art, and
the shipped Sprite3D cutouts are unshaded today, so the models drop in with
the same colour read and no lighting pop.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not invent geometry the single source view cannot support: no guessed
back-of-head, no separated limbs, no split of the intertwined pair sheets
(Evie+Lamb-a', Harper+Fiona, Faron+baby, Wacky+Chuck are each ONE figure here,
exactly as the art and the game's own friend entries treat them). Those are
first drafts to be replaced per-character by sculpt/Meshy work later; the
loader already prefers whatever .glb is present, so replacing one is a
one-file operation.
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import numpy as np                                    # noqa: E402
from PIL import Image                                 # noqa: E402

from npc_draft_lib import (                           # noqa: E402
	DRAFT_BONES,
	DraftSpec,
	build_mask,
	build_mesh,
	chain_joints,
	prepare_texture,
	skin_weights,
)

FRIENDS = "assets/characters/friends"
BOOK = "assets/book"

# ---------------------------------------------------------------- the roster
# Every figure the audit found living as a 2D cutout. `key` is the stem the
# runtime loader looks for, so it must match the sprite name it replaces.
ROSTER: list[DraftSpec] = [
	# ---- reef friends (main.gd FRIEND_DEFS) -----------------------------
	DraftSpec("pearl_friend", f"{FRIENDS}/pearl_friend.png", "Evie and Lamb-a'",
			  pivot=0.52, depth=0.17, sway=0.85,
			  figures=["Evie", "Lamb-a'"],
			  notes="Evie hugs Lamb-a'; the two overlap in the art and stay one figure."),
	DraftSpec("two_friends", f"{FRIENDS}/two_friends.png", "Harper and Fiona",
			  pivot=0.50, depth=0.16, sway=0.9,
			  figures=["Harper", "Fiona"],
			  notes="Sisters embracing, tails crossed - inseparable in this view."),
	DraftSpec("mama_baby", f"{FRIENDS}/mama_baby.png", "Faron and baby",
			  pivot=0.50, depth=0.16, sway=0.95,
			  figures=["Faron", "baby"]),
	DraftSpec("wacky_chuck", f"{FRIENDS}/wacky_chuck.png", "Wacky and Chuck",
			  pivot=0.46, depth=0.17, sway=0.8,
			  figures=["Wacky", "Chuck"],
			  notes="Chuck the poodle is held; a separate chuck_poodle_rigged.glb exists."),
	# ---- story / supporting NPCs ----------------------------------------
	DraftSpec("huluu", f"{FRIENDS}/huluu.png", "Princess Huluu",
			  pivot=0.55, depth=0.13, sway=1.1),
	DraftSpec("kareem", f"{FRIENDS}/kareem.png", "Kareem",
			  pivot=0.46, depth=0.15, sway=0.25, kind="land",
			  notes="Seated in an armchair in the source art; the chair is part of the figure."),
	DraftSpec("flower_friend", f"{FRIENDS}/flower_friend.png", "Flower Friend",
			  pivot=0.52, depth=0.15, sway=1.0,
			  notes="Art exists but no runtime call site yet."),
	# ---- book-art figures used as characters (kart grid, nursery) -------
	# These are photographed/painted toys cropped at the frame edge, so the
	# relief has an honest flat base where the art itself stops.
	DraftSpec("baby_eagle", f"{BOOK}/baby_eagle.png", "Sparkle the baby eagle",
			  pivot=0.44, depth=0.16, sway=0.7, kind="land", tri_budget=6000),
	DraftSpec("doll_bunny", f"{BOOK}/doll_bunny.png", "Bunny doll",
			  pivot=0.45, depth=0.15, sway=0.5, kind="land", grid=120, tri_budget=4500),
	DraftSpec("doll_cat", f"{BOOK}/doll_cat.png", "Kitty doll",
			  pivot=0.45, depth=0.15, sway=0.5, kind="land", grid=120, tri_budget=4500),
	DraftSpec("baby_doll", f"{BOOK}/baby_doll.png", "Baby Doll",
			  pivot=0.45, depth=0.16, sway=0.5, kind="land", tri_budget=6000),
	DraftSpec("baby_doll2", f"{BOOK}/baby_doll2.png", "Dolly",
			  pivot=0.45, depth=0.16, sway=0.5, kind="land", tri_budget=6000),
	DraftSpec("baby_doll3", f"{BOOK}/baby_doll3.png", "Sleepy",
			  pivot=0.45, depth=0.16, sway=0.5, kind="land", tri_budget=6000),
	DraftSpec("chuck_solo", f"{BOOK}/chuck_solo.png", "Chuck (solo book art)",
			  pivot=0.42, depth=0.17, sway=0.45, kind="land", tri_budget=6000,
			  notes="No runtime call site yet; chuck_poodle_rigged.glb is the shipped Chuck."),
]
# assets/book/flower_girl.png is deliberately NOT in this roster. It is a
# broken export of the same character as flower_friend: alpha is fully opaque
# and the transparency checkerboard is baked into the RGB, so its silhouette
# is the whole rectangle. It has no runtime call site either. Recorded in
# CHARACTER_2D_AUDIT_2026-07-26.md rather than silently converted.
# Daddy Mermaid is intentionally absent: the owner has a 3D Daddy to import
# later (2026-07-26) and asked for no draft effort on that character. The
# loader already prefers friends/daddy.glb the moment it lands.

BY_KEY = {s.key: s for s in ROSTER}
OUT_DIR = os.path.join(ROOT, FRIENDS)


# --------------------------------------------------------------- blender bits

def _reset_scene(bpy):
	bpy.ops.wm.read_factory_settings(use_empty=True)
	bpy.context.scene.render.fps = 24


def _make_material(bpy, name, color, image=None):
	mat = bpy.data.materials.new(name)
	mat.use_nodes = True
	nt = mat.node_tree
	for n in list(nt.nodes):
		nt.nodes.remove(n)
	out = nt.nodes.new("ShaderNodeOutputMaterial")
	# Background feeding the surface is what the glTF exporter reads as unlit;
	# we also stamp KHR_materials_unlit onto the file afterwards so the result
	# does not depend on exporter heuristics.
	emit = nt.nodes.new("ShaderNodeEmission")
	emit.inputs["Strength"].default_value = 1.0
	if image is not None:
		tex = nt.nodes.new("ShaderNodeTexImage")
		tex.image = image
		tex.interpolation = "Linear"
		nt.links.new(tex.outputs["Color"], emit.inputs["Color"])
	else:
		emit.inputs["Color"].default_value = (*color, 1.0)
	nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
	mat.diffuse_color = (*color, 1.0)
	return mat


def _build_object(bpy, spec, dm, image, back_col):
	mesh = bpy.data.meshes.new(spec.key)
	mesh.from_pydata([tuple(v) for v in dm.verts.tolist()], [], dm.faces)
	mesh.validate(verbose=False)
	uv = mesh.uv_layers.new(name="UVMap")
	for poly, corners in zip(mesh.polygons, dm.face_uvs):
		poly.use_smooth = True
		for li, st in zip(poly.loop_indices, corners):
			uv.data[li].uv = (float(st[0]), float(st[1]))
	obj = bpy.data.objects.new(spec.key, mesh)
	bpy.context.collection.objects.link(obj)
	# one unlit material for the whole figure: front cap, rear cap and rim all
	# read the same two-panel atlas, so a character costs one draw call and
	# decimation has no material seam to smear
	obj.data.materials.append(_make_material(bpy, f"{spec.key}_skin", (1, 1, 1), image))
	return obj


def _build_armature(bpy, spec):
	from mathutils import Vector
	arm_data = bpy.data.armatures.new(f"{spec.key}_rig")
	arm = bpy.data.objects.new(f"{spec.key}_rig", arm_data)
	bpy.context.collection.objects.link(arm)
	bpy.context.view_layer.objects.active = arm
	bpy.ops.object.mode_set(mode="EDIT")
	joints = chain_joints(spec.pivot)
	heights = {n: z for n, _p, z in joints}
	made = {}
	for name, parent, z in joints:
		b = arm_data.edit_bones.new(name)
		b.head = Vector((0.0, 0.0, z))
		# point each bone at its first child so the chain is continuous
		kids = [n for n, p, _z in joints if p == name]
		tz = heights[kids[0]] if kids else (z + (0.05 if z >= spec.pivot else -0.05))
		b.tail = Vector((0.0, 0.0, tz))
		if abs(b.tail.z - b.head.z) < 1e-4:
			b.tail = Vector((0.0, 0.0, z + 0.04))
		if parent:
			b.parent = made[parent]
			b.use_connect = False
		made[name] = b
	bpy.ops.object.mode_set(mode="OBJECT")
	return arm


def _decimate(bpy, obj, tri_budget):
	"""Collapse-decimate down to the phone budget, then apply.

	Runs BEFORE skinning: the grid mesh is uniformly dense, so collapse keeps
	the silhouette and outline rim while dissolving the flat interior. Weights
	are computed afterwards from the surviving vertices, so nothing has to be
	interpolated through the decimator.
	"""
	bpy.context.view_layer.objects.active = obj
	# triangulate first: collapse on quads sweeps whole grid rows out at once
	# and leaves long horizontal slivers that smear the projected art
	tri = obj.modifiers.new("Triangulate", "TRIANGULATE")
	tri.quad_method = "SHORTEST_DIAGONAL"
	bpy.ops.object.modifier_apply(modifier=tri.name)
	tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
	if tris <= tri_budget:
		return tris
	mod = obj.modifiers.new("Decimate", "DECIMATE")
	mod.decimate_type = "COLLAPSE"
	mod.ratio = float(tri_budget) / float(tris)
	mod.use_collapse_triangulate = True
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=mod.name)
	return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def _bind(bpy, obj, arm, spec):
	# read positions back off the (possibly decimated) mesh
	verts = np.array([tuple(v.co) for v in obj.data.vertices], dtype=np.float32)
	# skin_weights wants (x, y, z) with z as height, which is what we have
	weights = skin_weights(verts, spec.pivot)
	groups = {n: obj.vertex_groups.new(name=n) for n in DRAFT_BONES}
	for vi, w in enumerate(weights):
		for bone, val in w.items():
			if val > 1e-4:
				groups[bone].add([vi], float(val), "REPLACE")
	mod = obj.modifiers.new("Armature", "ARMATURE")
	mod.object = arm
	obj.parent = arm


def _swing_axis(pose_bone):
	"""Euler index whose local axis best matches world Y (the depth axis).

	Rotating about world Y swings the bone left/right in the art plane, which
	is the readable underwater sway. Bone local axes depend on roll, so we
	measure instead of assuming.
	"""
	basis = pose_bone.bone.matrix_local.to_3x3()
	best, bi = -1.0, 0
	for i, axis in enumerate((0, 1, 2)):
		v = basis.col[axis]
		score = abs(v.y)
		if score > best:
			best, bi = score, i
	return bi


def _author_idle(bpy, arm, spec):
	"""One looping 'idle': travelling sway down the tail, bob and breath up top."""
	import math

	frames = 48                      # 2.0 s at 24 fps; frame 48 == frame 0
	scene = bpy.context.scene
	scene.frame_start = 0
	scene.frame_end = frames
	bpy.context.view_layer.objects.active = arm
	bpy.ops.object.mode_set(mode="POSE")

	arm.animation_data_create()
	action = bpy.data.actions.new("idle")
	arm.animation_data.action = action

	chain = [n for n, _p, _z in chain_joints(spec.pivot)]
	amp = {}
	for name in chain:
		if name.startswith("tail"):
			i = int(name[4:])
			amp[name] = math.radians(1.6 + 1.5 * i) * spec.sway
		elif name == "root":
			amp[name] = 0.0
		else:
			depth = UPPER_ORDER.index(name) if name in UPPER_ORDER else 0
			amp[name] = math.radians(1.4 - 0.25 * depth) * spec.sway

	for pb in arm.pose.bones:
		pb.rotation_mode = "XYZ"
	axes = {pb.name: _swing_axis(pb) for pb in arm.pose.bones}

	for f in range(frames + 1):
		scene.frame_set(f)
		t = f / frames                      # 0..1 inclusive, seamless
		ph = t * math.tau
		for pb in arm.pose.bones:
			name = pb.name
			if name == "root":
				# gentle vertical bob; buoyancy, not a bounce
				pb.location = (0.0, 0.0, 0.012 * math.sin(ph) * spec.sway)
				pb.keyframe_insert("location", frame=f)
				pb.rotation_euler = (0.0, 0.0, 0.0)
				pb.keyframe_insert("rotation_euler", frame=f)
				continue
			if name.startswith("tail"):
				lag = int(name[4:]) * 0.42   # wave travels down the tail
			else:
				lag = -0.5 - 0.2 * (UPPER_ORDER.index(name) if name in UPPER_ORDER else 0)
			rot = [0.0, 0.0, 0.0]
			rot[axes[name]] = amp[name] * math.sin(ph - lag)
			if name == "head":
				# a slow nod on the perpendicular axis so she looks alive
				other = (axes[name] + 2) % 3
				rot[other] = math.radians(1.1) * math.sin(ph * 0.5) * spec.sway
			pb.rotation_euler = tuple(rot)
			pb.keyframe_insert("rotation_euler", frame=f)

	# Blender 5 moved f-curves behind slotted actions; the default bezier
	# interpolation is what we want anyway, so nothing to retune here.
	scene.frame_set(0)
	bpy.ops.object.mode_set(mode="OBJECT")
	return action


UPPER_ORDER = ["spine1", "chest", "neck", "head"]


PREVIEW_DIR = os.path.join(ROOT, "tools", "out", "npc_draft")


def _render_preview(bpy, obj, arm, spec):
	"""Three-quarter / side / back turntable stills, so the draft can be eyeballed.

	Cycles on CPU with a handful of samples: every material is pure emission,
	so there is nothing for a path tracer to converge on and 8 samples is
	already noise-free.
	"""
	import math
	from mathutils import Vector

	scene = bpy.context.scene
	scene.render.engine = "CYCLES"
	scene.cycles.device = "CPU"
	scene.cycles.samples = 8
	scene.cycles.use_denoising = False
	scene.render.resolution_x = 300
	scene.render.resolution_y = 460
	scene.render.film_transparent = False
	scene.world = bpy.data.worlds.new("preview")
	scene.world.use_nodes = True
	scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.90, 0.94, 1.0, 1.0)

	cam_data = bpy.data.cameras.new("cam")
	cam_data.lens = 60
	cam = bpy.data.objects.new("cam", cam_data)
	scene.collection.objects.link(cam)
	scene.camera = cam

	os.makedirs(PREVIEW_DIR, exist_ok=True)
	# figure is 1.0 tall with its base at z=0; front faces -Y
	target = Vector((0.0, 0.0, 0.5))
	for label, ang, frame in (("front", 0.0, 0), ("threequarter", 42.0, 12),
							  ("side", 90.0, 24), ("back", 180.0, 36)):
		scene.frame_set(frame)
		rad = math.radians(ang)
		dist = 2.1
		cam.location = Vector((math.sin(rad) * dist, -math.cos(rad) * dist, 0.62))
		direction = target - cam.location
		cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
		scene.render.filepath = os.path.join(PREVIEW_DIR, f"{spec.key}_{label}.png")
		bpy.ops.render.render(write_still=True)
	scene.frame_set(0)


# ------------------------------------------------------------- glb post-pass

def _patch_unlit(path):
	"""Stamp KHR_materials_unlit on every material of an exported GLB.

	Godot maps the extension straight to shading_mode = UNSHADED, which is
	what keeps the book art off the lighting rig.
	"""
	with open(path, "rb") as f:
		data = f.read()
	magic, _ver, _length = struct.unpack("<4sII", data[:12])
	if magic != b"glTF":
		raise ValueError(f"{path} is not a GLB")
	jlen, jtype = struct.unpack("<II", data[12:20])
	if jtype != 0x4E4F534A:
		raise ValueError(f"{path} first chunk is not JSON")
	js = json.loads(data[20:20 + jlen])
	rest = data[20 + jlen:]

	for mat in js.get("materials", []):
		mat.setdefault("extensions", {})["KHR_materials_unlit"] = {}
		mat["doubleSided"] = False
		pbr = mat.setdefault("pbrMetallicRoughness", {})
		pbr["metallicFactor"] = 0.0
		pbr["roughnessFactor"] = 1.0
	used = js.setdefault("extensionsUsed", [])
	if "KHR_materials_unlit" not in used:
		used.append("KHR_materials_unlit")

	blob = json.dumps(js, separators=(",", ":")).encode("utf-8")
	blob += b" " * ((4 - len(blob) % 4) % 4)
	head = struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(blob) + len(rest))
	with open(path, "wb") as f:
		f.write(head)
		f.write(struct.pack("<II", len(blob), 0x4E4F534A))
		f.write(blob)
		f.write(rest)


def _export(bpy, path):
	kwargs = dict(
		filepath=path,
		export_format="GLB",
		export_yup=True,
		export_skins=True,
		export_animations=True,
		export_image_format="JPEG",
		export_apply=False,
		use_selection=False,
	)
	try:
		bpy.ops.export_scene.gltf(**kwargs)
	except TypeError:
		kwargs.pop("export_jpeg_quality", None)
		bpy.ops.export_scene.gltf(**{k: v for k, v in kwargs.items()
									 if k in bpy.ops.export_scene.gltf.get_rna_type().properties})


# ------------------------------------------------------------------- driver

def build(spec: DraftSpec, preview: bool = False) -> dict:
	import bpy

	src = os.path.join(ROOT, spec.source)
	img = Image.open(src).convert("RGBA")
	alpha = np.array(img.getchannel("A"))
	mask = build_mask(alpha)
	# trim to the figure so texels are spent on the character, not the matte
	ys, xs = np.where(mask)
	pad = 2
	y0, y1 = max(0, ys.min() - pad), min(mask.shape[0], ys.max() + 1 + pad)
	x0, x1 = max(0, xs.min() - pad), min(mask.shape[1], xs.max() + 1 + pad)
	mask = mask[y0:y1, x0:x1]
	img = img.crop((x0, y0, x1, y1))

	tex, back_col = prepare_texture(img, mask, spec.tex_max)
	dm = build_mesh(mask, spec)

	_reset_scene(bpy)
	with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
		tex_path = tf.name
	tex.save(tex_path)
	image = bpy.data.images.load(tex_path)
	image.name = f"{spec.key}_atlas"
	image.pack()

	obj = _build_object(bpy, spec, dm, image, back_col)
	tris = _decimate(bpy, obj, spec.tri_budget)
	arm = _build_armature(bpy, spec)
	_bind(bpy, obj, arm, spec)
	_author_idle(bpy, arm, spec)

	out = os.path.join(OUT_DIR, f"{spec.key}.glb")
	if preview:
		_render_preview(bpy, obj, arm, spec)
	_export(bpy, out)
	_patch_unlit(out)
	os.unlink(tex_path)

	info = {
		"key": spec.key,
		"title": spec.title,
		"source": spec.source,
		"tris": tris,
		"texture": f"{tex.size[0]}x{tex.size[1]}",
		"bytes": os.path.getsize(out),
		"out": os.path.relpath(out, ROOT),
	}
	print(f"[ok] {spec.key:14s} {tris:6d} tris  tex {tex.size[0]}x{tex.size[1]}"
		  f"  {info['bytes']/1e6:5.2f} MB  -> {info['out']}")
	return info


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("keys", nargs="*", help="character keys (default: --all)")
	ap.add_argument("--all", action="store_true")
	ap.add_argument("--list", action="store_true")
	ap.add_argument("--preview", action="store_true",
					help="also render turntable stills to tools/out/npc_draft/")
	args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else None)

	if args.list:
		for s in ROSTER:
			print(f"{s.key:16s} {s.kind:8s} {s.title}")
		return

	keys = list(BY_KEY) if (args.all or not args.keys) else args.keys
	bad = [k for k in keys if k not in BY_KEY]
	if bad:
		sys.exit(f"unknown character key(s): {bad}\nknown: {sorted(BY_KEY)}")

	os.makedirs(OUT_DIR, exist_ok=True)
	report = [build(BY_KEY[k], preview=args.preview) for k in keys]
	total = sum(r["bytes"] for r in report)
	print(f"\n{len(report)} model(s), {total/1e6:.1f} MB total")


if __name__ == "__main__":
	main()
