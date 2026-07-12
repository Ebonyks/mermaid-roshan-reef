#!/usr/bin/env python3
"""
fit_roshan_rig.py — fit the 26-bone Roshan rig to the NEW Meshy multi-view mesh.

Self-calibrating: detects the character's facing direction from face-skin
texture, rotates her to the game convention (face -> glTF -Z after export),
places all bones from texture+geometry landmarks, binds with bone-heat and
falls back to analytic region-gated weights if heat fails, then separates
hair weights onto physics strand chains (hair_SS_J) for scripts/hair.gd.

Run headless:
    blender --background --python tools/fit_roshan_rig.py -- \
        --mesh ../meshy_rebuild/roshan_multiview_30k.glb \
        --out  ../meshy_rebuild/roshan_v2_rigged.glb
"""
import sys, os
from math import pi, atan2, degrees

import bpy
import numpy as np
from mathutils import Vector, Matrix, Quaternion as MQuaternion


def parse_args(argv):
    # lower_arms: radians to rotate each shoulder down (about model Z, opposite
    # signs per side) AFTER weighting, baked into rest pose + mesh, so winged
    # A/T-pose generations export with a natural hang and the game's
    # animation/verb library applies unchanged.
    a = {"mesh": "", "out": "", "strands": "8", "segs": "3", "lower_arms": "0"}
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        i = 0
        while i < len(rest):
            k = rest[i].lstrip("-")
            if k in a and i + 1 < len(rest):
                a[k] = rest[i + 1]; i += 2
            else:
                i += 1
    return a


def mesh_positions(obj):
    me = obj.data
    n = len(me.vertices)
    co = np.empty(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    mw = np.array(obj.matrix_world)
    co_h = np.concatenate([co, np.ones((n, 1))], 1)
    return (co_h @ mw.T)[:, :3]


def vertex_colors_from_texture(obj):
    """Per-vertex base-color by sampling the material texture through UVs."""
    me = obj.data
    img = None
    for mat_slot in obj.material_slots:
        m = mat_slot.material
        if m and m.use_nodes:
            for node in m.node_tree.nodes:
                if node.type == "TEX_IMAGE" and node.image and "normal" not in node.image.name.lower():
                    # prefer the one linked to Base Color
                    for link in m.node_tree.links:
                        if link.from_node == node and "Base Color" in link.to_socket.name:
                            img = node.image
                    img = img or node.image
    if img is None:
        raise RuntimeError("no base color image found")
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:, :, :3] * 255.0
    n = len(me.vertices)
    uv_acc = np.zeros((n, 2)); uv_cnt = np.zeros(n)
    uvl = me.uv_layers.active.data
    li = np.empty(len(me.loops), dtype=np.int64)
    me.loops.foreach_get("vertex_index", li)
    uvs = np.empty(len(uvl) * 2)
    uvl.foreach_get("uv", uvs)
    uvs = uvs.reshape(-1, 2)
    np.add.at(uv_acc, li, uvs)
    np.add.at(uv_cnt, li, 1)
    uv = uv_acc / np.maximum(uv_cnt[:, None], 1)
    # blender image origin is bottom-left; uv v is already bottom-up
    ui = np.clip((uv[:, 0] % 1.0) * (w - 1), 0, w - 1).astype(int)
    vi = np.clip((uv[:, 1] % 1.0) * (h - 1), 0, h - 1).astype(int)
    return px[vi, ui]


def main():
    args = parse_args(sys.argv)
    out = os.path.abspath(args["out"])
    n_str, segs = int(args["strands"]), int(args["segs"])

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(args["mesh"]))
    mesh_obj = next(o for o in bpy.data.objects if o.type == "MESH")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    C = vertex_colors_from_texture(mesh_obj)
    r, g, b = C[:, 0], C[:, 1], C[:, 2]
    mx = C.max(1); mn = C.min(1)
    sat = (mx - mn) / np.maximum(mx, 1)
    skin = (r > 170) & (r > g) & (g > b) & (g > 110) & (g < 215) & (b > 90) & (b < 190) & \
           ((r - b) > 25) & ((r - b) < 95)
    brown = (r > 60) & (r < 190) & (r > g) & (g > b) & ((r - b) > 30) & (g < 150)
    gold = (r > 185) & (g > 150) & (b < 150) & (r >= g) & (g > b)

    # ---- orientation: face-skin centroid direction -> +Y ------------------------
    P = mesh_positions(mesh_obj)
    zmin, zmax = P[:, 2].min(), P[:, 2].max(); H = zmax - zmin
    head_m = P[:, 2] > zmin + 0.75 * H
    hc = P[head_m].mean(0)
    face_m = head_m & skin
    fd = P[face_m][:, :2].mean(0) - hc[:2]
    ang = atan2(fd[0], fd[1])          # current facing angle from +Y (Blender)
    print(f"[i] face dir {fd.round(3)}  rotating {degrees(ang):.1f} deg about Z")
    for o in list(bpy.data.objects):
        if o.parent is None:
            o.matrix_world = Matrix.Rotation(ang, 4, 'Z') @ o.matrix_world
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    P = mesh_positions(mesh_obj)     # front is now +Y, up +Z, lateral X

    # ---- landmarks ----------------------------------------------------------------
    NS = 60
    zs = np.linspace(zmin, zmax, NS + 1)
    prof = []
    for i in range(NS):
        m = (P[:, 2] >= zs[i]) & (P[:, 2] < zs[i + 1])
        if m.sum() < 5:
            prof.append(0.0); continue
        Q = P[m]
        prof.append(float(np.percentile(np.linalg.norm(Q[:, :2] - Q[:, :2].mean(0), axis=1), 80)))
    prof = np.array(prof)
    b0, b1 = int(NS * 0.55), int(NS * 0.85)
    neck_i = b0 + int(np.argmin(prof[b0:b1]))
    neck_z = 0.5 * (zs[neck_i] + zs[neck_i + 1])
    chest_z = neck_z - 0.13 * H
    hips_z = zmin + 0.46 * H
    if hips_z > chest_z - 0.06 * H:
        hips_z = chest_z - 0.10 * H
    spine1_z = 0.5 * (hips_z + chest_z)

    # skull: core of the head band (trim hair by horizontal-distance percentile)
    hb = P[P[:, 2] > neck_z + 0.02 * H]
    hcz = hb[:, 2].mean()
    hxy = hb[:, :2]
    core_c = np.median(hxy, 0)
    dxy = np.linalg.norm(hxy - core_c, axis=1)
    keep = dxy < np.percentile(dxy, 60)
    skull_c = np.array([*hxy[keep].mean(0), hb[keep][:, 2].mean()])
    skull_r = float(np.percentile(np.linalg.norm(hb[keep] - skull_c, axis=1), 75))
    print(f"[i] H={H:.3f} neck={neck_z:.3f} chest={chest_z:.3f} hips={hips_z:.3f} "
          f"skull_c={skull_c.round(3)} r={skull_r:.3f}")

    def centroid_at(zq, hw=0.02):
        m = (P[:, 2] > zq - hw * H) & (P[:, 2] < zq + hw * H)
        return P[m].mean(0) if m.sum() > 5 else np.array([0, 0, zq])

    root_p = centroid_at(hips_z)
    spine1_p = centroid_at(spine1_z)
    chest_p = centroid_at(chest_z)
    neck_p = centroid_at(neck_z, 0.015)
    head_p = skull_c.copy()

    d_skull = np.linalg.norm(P - skull_c, axis=1)

    # ---- region masks ---------------------------------------------------------------
    rainbow = (sat > 0.30) & ~skin & ~gold & ~brown
    hair_all = (brown | (rainbow & (d_skull < skull_r * 3.2))) & (P[:, 2] > chest_z) & ~gold
    hair_deform = hair_all & (d_skull > skull_r * 1.12)
    arm_band = (P[:, 2] > hips_z - 0.06 * H) & (P[:, 2] < neck_z - 0.01 * H) & skin & ~hair_all
    armL_skin = arm_band & (P[:, 0] > 0.03 * H)
    armR_skin = arm_band & (P[:, 0] < -0.03 * H)
    print(f"[i] hair {hair_all.sum()} (deform {hair_deform.sum()})  "
          f"armL skin {armL_skin.sum()}  armR skin {armR_skin.sum()}")

    def arm_chain(m):
        """Order the arm cluster along its own principal axis (works for
        hanging, A-pose, and horizontal T-pose arms); the end closest to the
        spine axis (|x| smallest) is the shoulder."""
        A = P[m]
        c = A.mean(0)
        cov = np.cov((A - c).T)
        evals, evecs = np.linalg.eigh(cov)
        axis = evecs[:, -1]
        t = (A - c) @ axis
        lo_end = A[t < np.percentile(t, 8)].mean(0)
        hi_end = A[t > np.percentile(t, 92)].mean(0)
        if abs(lo_end[0]) > abs(hi_end[0]):
            axis = -axis
            t = -t
        o = np.argsort(t); A, t = A[o], t[o]
        t -= t[0]
        tmax = max(t[-1], 1e-6)
        def seg(f0, f1):
            mm = (t >= f0 * tmax) & (t <= f1 * tmax)
            return A[mm].mean(0) if mm.sum() > 3 else A[min(len(A)-1, int(f0*len(A)))]
        return [seg(0, 0.15), seg(0.40, 0.60), seg(0.75, 0.9), seg(0.95, 1.0)]

    def tucked_chain(sgn, good_shoulder):
        """Arm bent across the chest (hand near centre-front): fit from the
        front-centre skin cluster on this side; shoulder mirrored from the
        exposed arm (shoulder joints are symmetric even when the pose isn't)."""
        sh = good_shoulder * np.array([-1, 1, 1])
        hand_m = skin & (P[:, 0] * sgn > -0.02 * H) & (P[:, 0] * sgn < 0.12 * H) & \
                 (P[:, 1] > 0.03 * H) & (P[:, 2] > chest_z - 0.10 * H) & \
                 (P[:, 2] < neck_z) & ~hair_all
        if hand_m.sum() > 20:
            hand = P[hand_m].mean(0)
        else:
            hand = np.array([sgn * 0.05 * H, 0.08 * H, chest_z])
        el = np.array([sh[0] + sgn * 0.02 * H, 0.5 * (sh[1] + hand[1]) + 0.02 * H,
                       0.55 * sh[2] + 0.45 * hand[2] - 0.05 * H])
        wr = hand + (hand - el) * 0.15
        tip = hand + (hand - el) * 0.4
        return [sh, el, wr, tip]

    # detect the better-exposed arm; fit the occluded side as a tucked arm
    if armR_skin.sum() >= armL_skin.sum() and armR_skin.sum() > 150:
        chainR = arm_chain(armR_skin)
        chainL = arm_chain(armL_skin) if armL_skin.sum() > 200 else \
            tucked_chain(+1, chainR[0])
    elif armL_skin.sum() > 150:
        chainL = arm_chain(armL_skin)
        chainR = arm_chain(armR_skin) if armR_skin.sum() > 200 else \
            tucked_chain(-1, chainL[0])
    else:
        raise RuntimeError("neither arm found by skin mask — check texture thresholds")
    shL, elL, wrL, tipL = chainL
    shR, elR, wrR, tipR = chainR
    print(f"[i] armL chain {np.array(chainL).round(3).tolist()}")
    print(f"[i] armR chain {np.array(chainR).round(3).tolist()}")

    # capsule-based arm regions: near the chain AND clearly lateral of the spine axis
    def capsule_mask(chain, r):
        d = np.full(len(P), np.inf)
        for a, b2 in zip(chain[:-1], chain[1:]):
            ab = b2 - a
            ab2 = max(float(ab @ ab), 1e-9)
            t = np.clip(((P - a) @ ab) / ab2, 0, 1)
            d = np.minimum(d, np.linalg.norm(P - a - t[:, None] * ab, axis=1))
        return d < r
    spine_x = 0.5 * (chest_p[0] + root_p[0])
    r_arm = 0.045 * H
    armL_m = capsule_mask(chainL, r_arm) & (P[:, 0] > spine_x + 0.045 * H) & ~hair_deform
    armR_m = capsule_mask(chainR, r_arm) & (P[:, 0] < spine_x - 0.045 * H) & ~hair_deform
    print(f"[i] arm regions (capsule): L {armL_m.sum()}  R {armR_m.sum()}")

    # ---- tail ------------------------------------------------------------------------
    tail_m = (P[:, 2] <= hips_z) & ~hair_all
    T = P[tail_m]
    tail_bot = T[:, 2].min()
    samples = [root_p]
    for k in range(1, 9):
        f = k / 8.0
        zq = hips_z + (tail_bot - hips_z) * f
        hw = 0.03 * H
        m = (T[:, 2] > zq - hw) & (T[:, 2] < zq + hw)
        samples.append(T[m].mean(0) if m.sum() > 5 else np.array([0, 0, zq]))
    fl = T[T[:, 2] < tail_bot + 0.20 * (hips_z - tail_bot)]
    zmed = np.median(fl[:, 2])
    lobeT = fl[fl[:, 2] > zmed]; lobeB = fl[fl[:, 2] <= zmed]
    finT = (samples[-1], lobeT.mean(0))
    finB = (samples[-1], lobeB.mean(0))

    # ---- hair strand clustering (angular sectors, equal population) --------------------
    HP = P[hair_deform]
    hang = np.arctan2(HP[:, 1] - skull_c[1], HP[:, 0] - skull_c[0])
    edges = np.percentile(hang, np.linspace(0, 100, n_str + 1))
    strand_pts, strand_sector = [], []
    for s in range(n_str):
        m = (hang >= edges[s]) & (hang <= edges[s + 1])
        S = HP[m]
        if len(S) < 30:
            strand_pts.append(None); strand_sector.append((edges[s], edges[s+1])); continue
        dd = np.linalg.norm(S - skull_c, axis=1)
        o = np.argsort(dd); Ss = S[o]
        idxs = [int((len(Ss) - 1) * f) for f in np.linspace(0.02, 0.97, segs + 1)]
        w = max(2, len(Ss) // 12)
        pts = [Ss[max(0, i - w):i + w + 1].mean(0) for i in idxs]
        strand_pts.append(pts); strand_sector.append((edges[s], edges[s+1]))
    lens = [0 if sp is None else np.linalg.norm(sp[-1] - sp[0]) for sp in strand_pts]
    big = int(np.argmax(lens)); opp = (big + n_str // 2) % n_str

    # ---- armature -----------------------------------------------------------------------
    arm_data = bpy.data.armatures.new("RoshanRig")
    arm = bpy.data.objects.new("RoshanRig", arm_data)
    bpy.context.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm_data.edit_bones

    def add(name, head, tail, parent=None, deform=True):
        bn = eb.new(name)
        bn.head = Vector(head); bn.tail = Vector(tail)
        if (Vector(tail) - Vector(head)).length < 1e-4:
            bn.tail = Vector(head) + Vector((0, 0, 0.02))
        if parent:
            bn.parent = eb[parent]
        bn.use_deform = deform
        return bn

    add("root", root_p, spine1_p)
    add("spine1", spine1_p, chest_p, "root")
    add("chest", chest_p, neck_p, "spine1")
    mid_head = (neck_p + head_p) / 2
    add("neck", neck_p, mid_head, "chest")
    add("head", mid_head, head_p + np.array([0, 0, skull_r]), "neck")
    add("armU", shL, elL, "chest"); add("armF", elL, wrL, "armU"); add("hand", wrL, tipL, "armF")
    add("armU2", shR, elR, "chest"); add("armF2", elR, wrR, "armU2"); add("hand2", wrR, tipR, "armF2")
    prev = "root"
    for k in range(8):
        add(f"tail{k+1}", samples[k], samples[k + 1], prev)
        prev = f"tail{k+1}"
    add("finTop", *finT, "tail8")
    add("finBot", *finB, "tail8")

    def legacy_chain(names, sp):
        if sp is None:
            sp = [head_p + np.array([0, -0.02 * H * i, -0.03 * H * i]) for i in range(len(names) + 1)]
        parent = "head"
        for i, nm in enumerate(names):
            h = sp[min(i, len(sp) - 2)]; t = sp[min(i + 1, len(sp) - 1)]
            add(nm, h, t, parent, deform=False)
            parent = nm
    legacy_chain(["hair1", "hair2", "hair3"], strand_pts[big])
    legacy_chain(["hairL1", "hairL2"], strand_pts[opp])

    for s, sp in enumerate(strand_pts):
        if sp is None:
            continue
        parent = "head"
        for j in range(segs):
            add(f"hair_{s:02d}_{j}", sp[j], sp[j + 1], parent)
            parent = f"hair_{s:02d}_{j}"

    sock = {
        "headTop": (head_p + np.array([0, 0, skull_r * 1.05]), "head"),
        "backL": (chest_p + np.array([0.06 * H, -0.05 * H, 0.02 * H]), "chest"),
        "backR": (chest_p + np.array([-0.06 * H, -0.05 * H, 0.02 * H]), "chest"),
        "earL": (head_p + np.array([0.07 * H, 0, 0]), "head"),
        "earR": (head_p + np.array([-0.07 * H, 0, 0]), "head"),
        "tailTip": (samples[-1], "tail8"),
        "handHold": (wrL, "hand"),
    }
    for nm, (p0, par) in sock.items():
        add(nm, p0, np.array(p0) + np.array([0, 0, -0.03 * H]), par, deform=False)
    bpy.ops.object.mode_set(mode="OBJECT")

    # ---- weights: bone heat, else analytic ----------------------------------------------
    bpy.ops.object.select_all(action="DESELECT")
    mesh_obj.select_set(True); arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    heat_ok = True
    try:
        bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    except Exception as e:
        heat_ok = False
        print("[!] bone heat threw:", e)
    weighted = sum(1 for v in mesh_obj.data.vertices if v.groups)
    cover = weighted / len(mesh_obj.data.vertices)
    print(f"[i] heat coverage: {cover:.2%}")
    if cover < 0.95:
        heat_ok = False
    if not heat_ok:
        print("[i] falling back to analytic region-gated weights")
        if mesh_obj.parent != arm:
            mesh_obj.parent = arm
            mesh_obj.modifiers.new("Armature", "ARMATURE").object = arm
        else:
            if not any(md.type == "ARMATURE" for md in mesh_obj.modifiers):
                mesh_obj.modifiers.new("Armature", "ARMATURE").object = arm
        for vg in list(mesh_obj.vertex_groups):
            mesh_obj.vertex_groups.remove(vg)
        bones = {bn.name: (np.array(bn.head_local), np.array(bn.tail_local))
                 for bn in arm.data.bones if bn.use_deform}
        # region gates
        names = list(bones.keys())
        region = np.full(len(P), 0, int)   # 0 torso/tail core
        region[armL_m] = 1; region[armR_m] = 2; region[hair_deform] = 3
        gate = {}
        for nm in names:
            if nm.startswith(("armU2", "armF2", "hand2")):
                gate[nm] = 2
            elif nm.startswith(("armU", "armF", "hand")):
                gate[nm] = 1
            elif nm.startswith("hair_"):
                gate[nm] = 3
            else:
                gate[nm] = 0
        seg_a = np.stack([bones[nm][0] for nm in names])
        seg_b = np.stack([bones[nm][1] for nm in names])
        ab = seg_b - seg_a
        ab2 = (ab * ab).sum(1)
        Wmat = np.zeros((len(P), len(names)))
        for j, nm in enumerate(names):
            ap = P - seg_a[j]
            t = np.clip((ap @ ab[j]) / max(ab2[j], 1e-9), 0, 1)
            d = np.linalg.norm(ap - t[:, None] * ab[j], axis=1)
            sigma = 0.06 * H if gate[nm] == 0 else 0.035 * H
            w = np.exp(-(d / sigma) ** 2)
            w[region != gate[nm]] = 0.0
            Wmat[:, j] = w
        # every vert needs some weight: fall back to nearest core bone
        rowsum = Wmat.sum(1)
        dead = rowsum < 1e-8
        if dead.any():
            core_js = [j for j, nm in enumerate(names) if gate[nm] == 0]
            dcore = np.full((dead.sum(), len(core_js)), np.inf)
            Pd = P[dead]
            for k, j in enumerate(core_js):
                ap = Pd - seg_a[j]
                t = np.clip((ap @ ab[j]) / max(ab2[j], 1e-9), 0, 1)
                dcore[:, k] = np.linalg.norm(ap - t[:, None] * ab[j], axis=1)
            nearest = np.argmin(dcore, 1)
            di = np.where(dead)[0]
            for k in range(len(di)):
                Wmat[di[k], core_js[nearest[k]]] = 1.0
        # top-4, normalize
        top4 = np.argsort(-Wmat, 1)[:, :4]
        vgs = {nm: mesh_obj.vertex_groups.new(name=nm) for nm in names}
        for vi in range(len(P)):
            ws = Wmat[vi, top4[vi]]
            s = ws.sum()
            if s <= 0:
                continue
            for k in range(4):
                if ws[k] / s > 0.01:
                    vgs[names[top4[vi, k]]].add([vi], float(ws[k] / s), "REPLACE")
        print("[ok] analytic weights applied")
    else:
        # post-clean hair/body separation
        hair_idx = set(np.where(hair_deform)[0].tolist())
        for v in mesh_obj.data.vertices:
            is_hair = v.index in hair_idx
            for grp in list(v.groups):
                gname = mesh_obj.vertex_groups[grp.group].name
                if gname.startswith("hair_") and not is_hair:
                    mesh_obj.vertex_groups[grp.group].remove([v.index])
                if is_hair and not gname.startswith("hair_") and gname not in ("head", "neck"):
                    mesh_obj.vertex_groups[grp.group].remove([v.index])
        print("[ok] heat weights kept + hair separation")

    assert mesh_obj.find_armature() is not None, "mesh not bound to armature"

    # ---- optional: bake winged arms down into a natural hanging rest ---------------
    lower = float(args["lower_arms"])
    if lower != 0.0:
        print(f"[i] lowering arms by {lower:.2f} rad and baking as rest pose")
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="POSE")
        for nm, sgn in (("armU", -1.0), ("armU2", 1.0)):
            pb = arm.pose.bones.get(nm)
            if pb is None:
                continue
            rq = pb.bone.matrix_local.to_quaternion()
            axis_local = (rq.inverted() @ Vector((0, 0, 1))).normalized()
            pb.rotation_mode = "QUATERNION"
            pb.rotation_quaternion = MQuaternion(axis_local, sgn * lower)
        bpy.ops.object.mode_set(mode="OBJECT")
        # bake deformed vertices onto the base mesh (evaluated capture --
        # modifier_apply/transform_apply are unreliable in --background)
        dg = bpy.context.evaluated_depsgraph_get()
        me_eval = mesh_obj.evaluated_get(dg).to_mesh()
        co = np.empty(len(me_eval.vertices) * 3)
        me_eval.vertices.foreach_get("co", co)
        mesh_obj.evaluated_get(dg).to_mesh_clear()
        mesh_obj.data.vertices.foreach_set("co", co)
        mesh_obj.data.update()
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="POSE")
        bpy.ops.pose.armature_apply(selected=False)
        bpy.ops.object.mode_set(mode="OBJECT")
        print("[ok] arms-down rest baked")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB",
                              export_yup=True, use_selection=True,
                              export_skins=True, export_animations=False)
    print(f"[ok] wrote {out}")


if __name__ == "__main__":
    main()
