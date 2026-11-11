"""Rebind the registered anatomy on the existing Rigby2D skeleton.

Writes a separate archive; source images, bones, UVs, topology, slots,
attachments, and animation keys stay intact. No renderer audit changes.
"""
import argparse
from collections import Counter
from copy import copy
from hashlib import sha256
import json
import math
from pathlib import Path
from zipfile import ZipFile


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def clamp(t):
    return max(0.0, min(1.0, t))


def world_rest(bones):
    world = []
    for bone in bones:
        x, y = bone['x'], bone['y']
        a = math.radians(bone['rotation'])
        if 'parent' in bone:
            px, py, pa = world[bone['parent']]
            c, s = math.cos(pa), math.sin(pa)
            x, y = px + c*x - s*y, py + s*x + c*y
            a += pa
        world.append((x, y, a))
    return world


def rebind(rig):
    index = {bone['name']: i for i, bone in enumerate(rig['bones'])}
    world = world_rest(rig['bones'])
    right = [index['screen_right_' + name] for name in ('upper_arm', 'forearm', 'hand')]
    left = [index['screen_left_' + name] for name in ('upper_arm', 'forearm', 'hand')]
    pony = [index[name] for name in ('head', 'ponytail_base', 'ponytail_tip')]
    anatomy = next(i for i, slot in enumerate(rig['slots']) if slot['name'] == 'anatomy')
    meshes = {'Original': rig['slots'][anatomy]['attachments'][0]}
    for skin in rig['skins']:
        item = next(row for row in skin['slots'] if row['slot'] == anatomy)
        meshes[skin['name']] = item['attachments'][0]
    sx, sy, _ = world[right[0]]
    ex, ey, _ = world[right[1]]
    wx, wy, _ = world[right[2]]
    wrist = math.hypot(wx - sx, wy - sy)
    dx, dy = (wx - sx) / wrist, (wy - sy) / wrist
    elbow = (ex - sx) * dx + (ey - sy) * dy
    counts = {}
    for name, mesh in meshes.items():
        counts[name] = Counter()
        for vertex, source in enumerate(mesh['weights']):
            u, v = mesh['uvs'][2*vertex:2*vertex + 2]
            x, y = u * 256.0, -v * 256.0
            x_img, y_img = u * 1024.0, v * 1024.0
            t = (x - sx) * dx + (y - sy) * dy
            cross = -(x - sx) * dy + (y - sy) * dx
            old = {row['bone']: row for row in source}
            weights = [old.get(i, {}).get('weight', 0.0) for i in range(len(world))]
            # Axial gradients remove lateral pinching on the painted forearm.
            # The first 5 rest units and all the neck retain the native binding.
            arm = smooth((t - 5.0) / 8.0) * smooth((14.0 - abs(cross)) / 5.0)
            if arm > 0:
                f = clamp((t - elbow + 10.5) / 21.0)
                h = clamp((t - wrist + 7.0) / 14.0)
                weights = [w * (1.0 - arm) for w in weights]
                for i, ratio in zip(right, ((1-f)*(1-h), f*(1-h), h)):
                    weights[i] += arm * ratio
                counts[name]['right_arm_vertices'] += 1
            # Reduce inadvertent arm pull at the ponytail/arm fringe. The
            # taper and head/pony threshold confine the change to the fringe.
            total = sum(weights[i] for i in pony)
            hair = 0.2 * smooth((680.0 - .625*x_img - y_img) / 24.0)
            hair *= smooth((488.0 - x_img) / 32.0) * smooth((y_img - 285.0) / 35.0)
            hair *= smooth((total - .04) / .22)
            if hair > 0:
                removed = sum(weights[i] for i in left) * hair
                for i in left:
                    weights[i] *= 1.0 - hair
                for i in pony:
                    weights[i] += removed * weights[i] / total
                counts[name]['hair_fringe_vertices'] += 1
            if arm <= 0 and hair <= 0:
                continue
            counts[name]['changed_vertices'] += 1
            assert abs(sum(weights) - 1.0) < 1e-10, (name, vertex, sum(weights))
            bound = []
            for i, weight in enumerate(weights):
                if weight <= 0:
                    continue
                if i in old:
                    local_x, local_y = old[i]['x'], old[i]['y']
                else:
                    bx, by, angle = world[i]
                    c, s = math.cos(angle), math.sin(angle)
                    local_x = (x - bx) * c + (y - by) * s
                    local_y = -(x - bx) * s + (y - by) * c
                bound.append({'bone': i, 'x': local_x, 'y': local_y, 'weight': weight})
            mesh['weights'][vertex] = bound
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source', type=Path)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    if args.source.resolve() == args.output.resolve():
        ap.error('Use a separate output archive.')
    with ZipFile(args.source) as original:
        rig = json.loads(original.read('project.json'))
        counts = rebind(rig)
        with ZipFile(args.output, 'w') as out:
            for info in original.infolist():
                data = json.dumps(rig, separators=(',', ':'), ensure_ascii=False).encode('utf-8') if info.filename == 'project.json' else original.read(info)
                out.writestr(copy(info), data, compress_type=info.compress_type, compresslevel=6)
    print(json.dumps({'source_sha256': sha256(args.source.read_bytes()).hexdigest(),
                      'output_sha256': sha256(args.output.read_bytes()).hexdigest(),
                      'changed': counts}, indent=2))


if __name__ == '__main__':
    main()
