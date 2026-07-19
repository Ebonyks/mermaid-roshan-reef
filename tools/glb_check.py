#!/usr/bin/env python3
"""
glb_check.py — quick glTF/GLB inspector for the character pipeline.

Reports joint count, animation count, triangles, images and size, and (for
Roshan) verifies the 26 required bone names are present so a re-exported mesh
will still bind to the procedural animator in scripts/player.gd.

Usage:
    python3 tools/glb_check.py assets/characters/roshan.glb
    python3 tools/glb_check.py assets/characters/friends/daddy.glb
"""
import json, struct, sys, os

ROSHAN_BONES = [
    "root", "spine1", "chest", "neck", "head", "hair1", "hair2", "hair3",
    "hairL1", "hairL2", "armU", "armF", "hand", "armU2", "armF2", "hand2",
    "tail1", "tail2", "tail3", "tail4", "tail5", "tail6", "tail7", "tail8",
    "finTop", "finBot",
]
# Standard NPC humanoid rig (see tools/build_npc_rig.py / CHARACTER_PIPELINE.md)
NPC_BONES = [
    "root", "hips", "spine", "chest", "neck", "head",
    "armUL", "armFL", "handL", "armUR", "armFR", "handR",
    "legUL", "legLL", "footL", "legUR", "legLR", "footR",
]
# Optional cosmetic socket bones (additive to Roshan's 26; see CHARACTER_CUSTOMIZATION.md §8)
SOCKET_BONES = ["headTop", "backL", "backR", "earL", "earR", "tailTip", "handHold"]


def load_json_chunk(p):
    with open(p, "rb") as f:
        magic, ver, length = struct.unpack("<4sII", f.read(12))
        if magic != b"glTF":
            raise ValueError("not a binary glTF (.glb)")
        clen, ctype = struct.unpack("<II", f.read(8))
        return json.loads(f.read(clen))


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    p = sys.argv[1]
    j = load_json_chunk(p)
    nodes = j.get("nodes", [])
    skins = j.get("skins", [])
    joints = {nodes[ji].get("name", "") for sk in skins for ji in sk.get("joints", [])}
    tris = 0
    acc = j.get("accessors", [])
    for m in j.get("meshes", []):
        for pr in m.get("primitives", []):
            idx = pr.get("indices")
            if idx is not None and idx < len(acc):
                tris += acc[idx].get("count", 0) // 3

    print(f"file        {os.path.basename(p)}")
    print(f"size        {os.path.getsize(p)/1e6:.2f} MB")
    print(f"meshes      {len(j.get('meshes', []))}")
    print(f"joints      {len(joints)}")
    print(f"animations  {len(j.get('animations', []))}")
    print(f"triangles   {tris}")
    print(f"images      {len(j.get('images', []))}")

    base = os.path.basename(p).lower()
    expect = ROSHAN_BONES if "roshan" in base else (NPC_BONES if joints else None)
    if expect:
        missing = [b for b in expect if b not in joints]
        label = "ROSHAN" if expect is ROSHAN_BONES else "NPC"
        if missing:
            print(f"[!] {label} rig MISSING bones: {missing}")
            sys.exit(4)
        print(f"[ok] all {len(expect)} {label} bones present.")
        if expect is ROSHAN_BONES:
            sockets = [b for b in SOCKET_BONES if b in joints]
            print(f"[i] cosmetic socket bones present: {sockets if sockets else 'none yet (optional)'}")
            strands = set()
            for b in joints:
                if b.startswith("hair_"):
                    strands.add(b.split("_")[1])   # the SS index
            print(f"[i] physics hair strands present: {len(strands)} "
                  f"({'good — 10-15+ target met' if len(strands) >= 10 else 'none/few yet (optional)'})")


if __name__ == "__main__":
    main()
