#!/usr/bin/env python3
"""
build_roshan_cosmetics.py — Blender-side assembler for Roshan's cosmetic parts.

ROLE
----
The runtime (scripts/cosmetics.gd) COMPOSES cosmetics at play time. This tool is
the AUTHORING side: it validates that the base rig carries the cosmetic SOCKET
bones, checks each part in the library, and can pre-bake a merged "preview" GLB
per loadout so an artist can eyeball a whole look in one file.

It reads the SAME catalog the game reads
(assets/characters/cosmetics/catalog.json) so the tooling and the runtime never
drift.

SOCKET BONES (additive to Roshan's 26-bone rig — keep all originals too):
    headTop   crowns / bows / hats
    backL, backR   wings (mirror pair)
    earL, earR     fairy ears (or use the 'fairy_ears' morph instead)
    tailTip   fin variants
    handHold  hand props (wand, shell)
Add these when (re)rigging; build_roshan_rig.py keeps the core 26, this extends them.

PARTS LIBRARY layout:
    assets/characters/cosmetics/parts/<name>.glb   one mesh each, +Y up, small
    (a socket part is authored at the origin in the socket bone's local space)

USAGE (needs a real Blender; none in the headless web session):
    blender --background --python tools/build_roshan_cosmetics.py -- \
        --base assets/characters/roshan.glb \
        --catalog assets/characters/cosmetics/catalog.json \
        --loadout fairy \
        --out /tmp/roshan_fairy_preview.glb
"""
import sys, os, json

SOCKET_BONES = ["headTop", "backL", "backR", "earL", "earR", "tailTip", "handHold"]


def parse_args(argv):
    a = {
        "base": "assets/characters/roshan.glb",
        "catalog": "assets/characters/cosmetics/catalog.json",
        "loadout": "fairy",
        "out": "/tmp/roshan_loadout_preview.glb",
    }
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        i = 0
        while i < len(rest):
            key = rest[i].lstrip("-")
            if key in a and i + 1 < len(rest):
                a[key] = rest[i + 1]; i += 2
            else:
                i += 1
    return a


def load_catalog(path):
    with open(path) as f:
        return json.load(f)


def resolve_loadout(catalog, loadout):
    cosmetics = catalog.get("cosmetics", {})
    out = []
    for cid in catalog.get("loadouts", {}).get(loadout, []):
        if cid in cosmetics:
            out.append((cid, cosmetics[cid]))
        else:
            print(f"  [!] loadout '{loadout}' references unknown cosmetic '{cid}'")
    return out


def res_to_fs(path):
    # "res://assets/..." -> repo-relative "assets/..."
    return path.replace("res://", "")


def main():
    args = parse_args(sys.argv)
    catalog = load_catalog(args["catalog"])
    parts = resolve_loadout(catalog, args["loadout"])
    print(f"[i] loadout '{args['loadout']}' -> {len(parts)} cosmetic(s):")
    for cid, c in parts:
        print(f"    - {cid:16s} type={c.get('type')} layer={c.get('layer')}")

    try:
        import bpy
    except ImportError:
        print(__doc__)
        print("\n[!] Run inside Blender:")
        print("    blender --background --python tools/build_roshan_cosmetics.py -- "
              "--loadout %s --out %s" % (args["loadout"], args["out"]))
        print("[i] No Blender in the Claude Code web session; run where Blender exists.")
        # still useful headless: report which part assets are missing
        print("\n[i] Part-asset presence check:")
        for cid, c in parts:
            if c.get("type") == "socket":
                fs = res_to_fs(c.get("asset", ""))
                print(f"    {'OK ' if os.path.exists(fs) else 'MISSING'}  {fs}")
        sys.exit(1)

    # --- Blender path ---
    bpy.ops.wm.read_factory_settings(use_empty=True)
    base = os.path.abspath(args["base"])
    bpy.ops.import_scene.gltf(filepath=base)
    arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
    if arm is None:
        print("[!] no armature in base"); sys.exit(2)

    bones = {b.name for b in arm.data.bones}
    have_sockets = [s for s in SOCKET_BONES if s in bones]
    missing_sockets = [s for s in SOCKET_BONES if s not in bones]
    print(f"[i] socket bones present: {have_sockets or 'NONE'}")
    if missing_sockets:
        print(f"[!] socket bones MISSING (add when re-rigging): {missing_sockets}")

    # Import each socket part, parent to its bone. Material/morph cosmetics are
    # runtime-only (the game applies them); here we just assemble geometry preview.
    for cid, c in parts:
        if c.get("type") != "socket":
            print(f"  [skip] {cid}: type {c.get('type')} is applied at runtime, not baked")
            continue
        fs = os.path.abspath(res_to_fs(c.get("asset", "")))
        if not os.path.exists(fs):
            print(f"  [!] {cid}: part asset missing -> {fs}"); continue
        prev = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=fs)
        new_objs = [o for o in bpy.data.objects if o not in prev]
        socket = c.get("socket", "")
        if socket not in bones:
            print(f"  [!] {cid}: socket bone '{socket}' not in rig — left unparented")
            continue
        # Parts are authored at the origin in the socket bone's local space
        # (see PARTS LIBRARY above), so bone-parent each imported root and
        # zero its local transform. Blender hangs bone children off the bone
        # TAIL, so shift back -Y by the bone length to land on the head.
        bone_len = arm.data.bones[socket].length
        roots = [o for o in new_objs if o.parent is None or o.parent in prev]
        for o in roots:
            o.parent = arm
            o.parent_type = "BONE"
            o.parent_bone = socket
            o.matrix_parent_inverse.identity()
            o.location = (0.0, -bone_len, 0.0)
            if o.rotation_mode == "QUATERNION":
                o.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
            else:
                o.rotation_euler = (0.0, 0.0, 0.0)
            o.scale = (1.0, 1.0, 1.0)
        print(f"  [ok] {cid} ({os.path.basename(fs)}): "
              f"{len(roots)} root(s) bone-parented to '{socket}'")

    out = os.path.abspath(args["out"])
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB")
    print(f"[ok] wrote loadout preview: {out}")
    print("[i] validate:  python3 tools/glb_check.py %s" % out)


if __name__ == "__main__":
    main()
