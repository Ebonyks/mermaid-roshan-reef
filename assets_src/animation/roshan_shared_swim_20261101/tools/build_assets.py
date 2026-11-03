"""Compile a single shared 2D actor and data-only garments from native Aseprite cuts.

Pixel edits/export run in Aseprite. Python inventories alpha, records registration,
builds geometry and checks the resulting RGBA data; original source sheets survive.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PREFIX = ROOT.relative_to(REPO).as_posix()
ASEPRITE = Path('C:/Program Files/Aseprite/Aseprite.exe')
VIEW = 'swim_right_quarter'


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8', newline='\n')


def reference(path: Path) -> dict:
    return {'path': path.relative_to(REPO).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def components(path: Path):
    rgba = np.asarray(Image.open(path).convert('RGBA'))
    labels, _ = ndimage.label(rgba[:, :, 3] > 8)
    slices = ndimage.find_objects(labels)
    # Assign faint edge antialiasing to its nearest substantial component.
    distance, nearest = ndimage.distance_transform_edt(labels == 0, return_indices=True)
    ownership = labels[tuple(nearest)]
    ownership[(rgba[:, :, 3] == 0) | (distance > 4)] = 0
    parts = []
    for identity, region in enumerate(slices, 1):
        if region is None or np.count_nonzero(labels[region] == identity) < 500:
            continue
        ys, xs = np.nonzero(ownership == identity)
        box = [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]
        parts.append((identity, box))
    return rgba, ownership, parts


def make_cut_spec() -> list[dict]:
    specs = []
    for source_name, filename in [('base', 'shared_view_parts_take01.png'),
                                  ('ballet', 'ballet_parts_take01.png'),
                                  ('magician', 'magician_parts_take01.png'),
                                  ('neck', 'neck_yoke_take01.png')]:
        source = ROOT/'art_source'/filename
        rgba, ownership, pieces = components(source)
        for identity, box in pieces:
            x0, y0, x1, y1 = box
            cx, cy = (x0+x1)/2, (y0+y1)/2
            if source_name == 'base':
                if cy < 450 and cx < 550:
                    name = 'head_hair'
                elif cy < 450 and cx < 1000:
                    continue  # Alternative free-hair painting is not duplicated on the actor.
                elif cy < 450:
                    name = 'arm_far' if cy < 235 else 'arm_near'
                    x0 = max(x0, 1172)  # Skin-only region, excluding the painted default sleeve.
                elif cx < 400:
                    continue  # Default pink shirt is a registration reference, not anatomy.
                elif cx < 1100:
                    continue  # Default tail surface is replaced by the selected garment.
                else:
                    name = 'fin_broad' if cy < 650 else ('fin_edge' if cy < 755 else 'fin_cup')
                output = ROOT/'textures/anatomy'/(name+'.png')
            elif source_name == 'neck':
                name = 'neck_yoke'
                output = ROOT/'textures/anatomy'/(name+'.png')
            else:
                if cx < 570:
                    name = 'body'
                elif cy > 420:
                    name = 'tail'
                elif cx > 1080:
                    name = 'headwear'
                else:
                    name = 'sleeve_far' if cx < 850 else 'sleeve_near'
                output = ROOT/'textures/garments'/(source_name+'_'+name+'.png')
            mask = ownership[y0:y1, x0:x1] == identity
            runs = []
            for y, row in enumerate(mask):
                starts = np.flatnonzero(np.diff(np.r_[False, row, False].astype(np.int8)) == 1)
                ends = np.flatnonzero(np.diff(np.r_[False, row, False].astype(np.int8)) == -1)
                runs.append([[int(a), int(b)] for a, b in zip(starts, ends)])
            size = [x1-x0, y1-y0]
            factor = min(1.0, 1024/max(size))
            exported = [max(1, round(v*factor)) for v in size]
            expected = rgba[y0:y1, x0:x1].copy()
            expected[~mask] = 0
            specs.append({'name': source_name+'_'+name, 'source': str(source),
                          'output': str(output), 'box': [x0, y0, x1, y1],
                          'size': exported, 'rows': runs,
                          'source_rgba_after_matte_sha256': hashlib.sha256(expected.tobytes()).hexdigest(),
                          'source_ref': reference(source),
                          'source_scale': [exported[0]/size[0], exported[1]/size[1]],
                          'master': str(ROOT/'masters'/(source_name+'_parts.aseprite'))})
    assert len(specs) == 17, [(x['name'], x['box']) for x in specs]
    return specs


def isolate(specs: list[dict]) -> None:
    write(ROOT/'rig/cut_spec.json', specs)
    command = [str(ASEPRITE), '-b', '--script-param', 'spec='+str(ROOT/'rig/cut_spec.json'),
               '--script', str(ROOT/'tools/isolate_parts.lua')]
    result = subprocess.run(command, capture_output=True, timeout=180)
    (ROOT/'evidence/aseprite_isolation.log').write_bytes(result.stdout+result.stderr)
    assert result.returncode == 0, result.stdout+result.stderr
    for spec in specs:
        im = Image.open(spec['output'])
        assert im.mode == 'RGBA' and list(im.size) == spec['size'], spec['name']
        raw = np.asarray(im)
        if spec['source_scale'] == [1.0, 1.0]:
            assert hashlib.sha256(raw.tobytes()).hexdigest() == spec['source_rgba_after_matte_sha256'], spec['name']
    write(ROOT/'evidence/isolation_receipt.json', {'pass': True, 'method': 'Aseprite native RGBA crop/matte; no recoloring or character reconstruction',
          'edge_rule': 'Alpha>8 component with original faint antialiasing within4px; unrelated components and remote faint noise cleared',
          'parts': [{k: v for k, v in s.items() if k != 'rows'} | {'output_ref': reference(Path(s['output']))} for s in specs]})


def similarity(source_a, source_b, target_a, target_b):
    a, b, c, d = map(lambda p: np.asarray(p, float), (source_a, source_b, target_a, target_b))
    u, v = b-a, d-c
    angle = math.atan2(v[1], v[0])-math.atan2(u[1], u[0])
    scale = np.linalg.norm(v)/np.linalg.norm(u)
    matrix = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])*scale
    offset = c-matrix@a
    return matrix, offset


def affine(scale, angle, source_pivot, target):
    a = math.radians(angle)
    matrix = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])*scale
    return matrix, np.asarray(target)-matrix@np.asarray(source_pivot)


TAIL = np.array([[580., 360.], [478., 478.], [363., 550.], [252., 576.], [137., 550.]])
BODY_ROOT = np.array([580., 360.])
NECK = np.array([725., 308.])
HEAD = np.array([735., 295.])
FIT: dict = {}
BONES: list[dict] = []
PARTS: dict = {}


def add_bone(name, parent, head, tail):
    BONES.append({'name': name, 'parent': parent, 'head': np.asarray(head).tolist(), 'tail': np.asarray(tail).tolist()})


def chain_weights(t, names):
    x = np.clip(t, 0, 1)*(len(names)-1)
    return {name: np.clip(1-np.abs(x-i), 0, 1) for i, name in enumerate(names)}


def near_polyline(points, line):
    lengths = np.linalg.norm(np.diff(line, axis=0), axis=1)
    cumul = np.r_[0, np.cumsum(lengths)]
    distances = []
    ts = []
    for i, (a, b) in enumerate(zip(line[:-1], line[1:])):
        s = np.clip(((points-a)@(b-a))/np.dot(b-a, b-a), 0, 1)
        q = a+(b-a)*s[:, None]
        distances.append(np.sum((points-q)**2, axis=1))
        ts.append((cumul[i]+lengths[i]*s)/cumul[-1])
    # A hard nearest-segment switch creates a discontinuous weight crease on
    # the inside of the curved painted tail. Blend projected arc coordinates
    # over a 45px neighbourhood; both costumes use this same canonical field.
    distance = np.stack(distances)
    influence = np.exp(-(distance-distance.min(axis=0))/(2*45.0**2))
    influence /= influence.sum(axis=0)
    return np.sum(np.stack(ts)*influence, axis=0)


def field(points, kind, source_points=None):
    if kind == 'body':
        direction = NECK-BODY_ROOT
        t = ((points-BODY_ROOT)@direction)/np.dot(direction, direction)
        return chain_weights(t, ['Hips', 'Spine', 'Chest'])
    if kind == 'tail':
        return chain_weights(near_polyline(points, TAIL), ['TailA', 'TailB', 'TailC', 'TailD', 'Fin'])
    if kind == 'head_hair':
        # Face and scalp remain entirely Head-owned. Only the trailing ponytail bends.
        x, y = source_points[:, 0], source_points[:, 1]
        strength = np.clip((275-x)/95, 0, 1)*np.clip((390-y)/95, 0, 1)
        out = chain_weights(np.clip((260-x)/210, 0, 1), ['HairRoot', 'HairA', 'HairB'])
        out = {n: v*strength for n, v in out.items()}
        out['Head'] = 1-strength
        return out
    if kind == 'neck':
        t = np.clip((points[:, 0]-675)/65, 0, 1)
        return {'Chest': 1-t, 'Neck': t}
    if kind in ['arm_far', 'arm_near']:
        side = 'Left' if kind == 'arm_far' else 'Right'
        t = np.clip((source_points[:, 0]-1172)/(1492-1172), 0, 1)
        return chain_weights(t, [side+'Upper', side+'Fore', side+'Hand'])
    return {kind: np.ones(len(points))}


def mesh(texture: Path, matrix, offset, kind, spec=None):
    rgba = np.asarray(Image.open(texture).convert('RGBA'))
    h, w = rgba.shape[:2]
    xx = np.unique(np.r_[np.arange(0, w, 12), w]).astype(float)
    yy = np.unique(np.r_[np.arange(0, h, 12), h]).astype(float)
    uv = np.array([(x, y) for y in yy for x in xx])
    triangles = []
    for iy in range(len(yy)-1):
        for ix in range(len(xx)-1):
            x0, x1, y0, y1 = int(xx[ix]), int(xx[ix+1]), int(yy[iy]), int(yy[iy+1])
            if not np.any(rgba[y0:y1, x0:x1, 3]):
                continue
            a = iy*len(xx)+ix
            b = a+1
            c = a+len(xx)
            d = c+1
            triangles.extend([[a, b, d], [a, d, c]])
    used = np.unique(np.array(triangles).ravel())
    remap = {v: i for i, v in enumerate(used)}
    uv = uv[used]
    points = uv@matrix.T+offset
    if spec is not None:
        source_points = uv/np.asarray(spec['source_scale'])+np.asarray(spec['box'][:2])
    else:
        source_points = uv
    weights = field(points, kind, source_points)
    return {'format': 'roshan.attachment-mesh/1', 'space': 'canonical_canvas_px',
            'vertices': np.round(points, 6).tolist(), 'uv': uv.tolist(),
            'triangles': [[remap[x] for x in t] for t in triangles],
            'weights': {n: np.round(values, 9).tolist() for n, values in weights.items()}}


def component_transform(spec, transform):
    matrix, offset = transform
    return matrix@np.diag(1/np.asarray(spec['source_scale'])), matrix@np.asarray(spec['box'][:2])+offset


def build(specs):
    global PARTS
    byname = {s['name']: s for s in specs}
    skin_refs = []
    core = []
    add_bone('Hips', None, BODY_ROOT, BODY_ROOT+[48, -17])
    add_bone('Spine', 'Hips', [630, 342], [675, 325])
    add_bone('Chest', 'Spine', [675, 325], NECK)
    add_bone('Neck', 'Chest', NECK, HEAD)
    add_bone('Head', 'Neck', HEAD, HEAD+[0, -100])
    head_transform = affine(.68, 0, [369, 378], HEAD)
    hair_points = [head_transform[0]@np.asarray(p)+head_transform[1] for p in [[276, 135], [220, 205], [150, 250], [85, 270]]]
    for i, name in enumerate(['HairRoot', 'HairA', 'HairB']):
        add_bone(name, 'Head' if i == 0 else ['HairRoot', 'HairA'][i-1], hair_points[i], hair_points[i+1])
    for i, name in enumerate(['TailA', 'TailB', 'TailC', 'TailD']):
        add_bone(name, 'Hips' if i == 0 else ['TailA', 'TailB', 'TailC'][i-1], TAIL[i], TAIL[i+1])
    add_bone('Fin', 'TailD', TAIL[-1], TAIL[-1]+[-130, -30])
    body_transform = similarity([350, 730], [355, 285], BODY_ROOT, NECK)
    shoulders = [body_transform[0]@np.asarray(p)+body_transform[1] for p in [[205, 240], [482, 236]]]
    arm_transforms = {}
    for side, kind, shoulder, source_y, angle in [('Left', 'arm_far', shoulders[0], 163, 151), ('Right', 'arm_near', shoulders[1], 323, 140)]:
        transform = affine(.48, angle, [1172, source_y], shoulder)
        arm_transforms[kind] = transform
        points = [transform[0]@np.asarray(p)+transform[1] for p in [[1172, source_y], [1298, source_y+9], [1409, source_y+7], [1480, source_y+19]]]
        for i, name in enumerate([side+'Upper', side+'Fore', side+'Hand']):
            add_bone(name, 'Chest' if i == 0 else [side+'Upper', side+'Fore'][i-1], points[i], points[i+1])
    write(ROOT/'rig/skeleton.json', {'format': 'roshan.native-skeleton/1', 'view': VIEW, 'bones': BONES})

    def add_core(name, kind, transform, z):
        spec = byname['base_'+name] if name != 'neck_yoke' else byname['neck_neck_yoke']
        m, o = component_transform(spec, transform)
        geometry = mesh(Path(spec['output']), m, o, kind, spec)
        path = ROOT/'geometry'/('anatomy_'+name+'.json')
        write(path, geometry)
        core.append({'id': name, 'texture': reference(Path(spec['output'])), 'geometry': reference(path), 'layer': z})
        FIT[name] = {'source_pivot_transform': {'matrix': transform[0].tolist(), 'offset': transform[1].tolist()}, 'source_box': spec['box']}

    add_core('head_hair', 'head_hair', head_transform, 40)
    for name, z in [('arm_far', 8), ('arm_near', 32)]:
        add_core(name, name, arm_transforms[name], z)
    neck_spec = byname['neck_neck_yoke']
    box = neck_spec['box']
    neck_pivot = np.asarray([box[0]+.74*(box[2]-box[0]), box[1]+.10*(box[3]-box[1])])
    add_core('neck_yoke', 'neck', affine(.14, -5, neck_pivot, HEAD+[0, -3]), 9)
    tangent = TAIL[-1]-TAIL[-2]
    fin_angle = math.degrees(math.atan2(tangent[1], tangent[0]))-180
    for name, pivot in [('fin_broad', [1463, 536]), ('fin_edge', [1472, 723]), ('fin_cup', [1440, 870])]:
        add_core(name, 'Fin', affine(.52, fin_angle, pivot, TAIL[-1]), 1)
    write(ROOT/'rig/anatomy.json', {'parts': core, 'fin_states': ['fin_broad', 'fin_edge', 'fin_cup'],
          'note': 'Canonical head/hair, arms, neck/shoulder and authored fin states. All body/tail clothing is exclusively skin-owned; default pink shirt/tail source pieces are not rendered.'})
    identity = [reference(ROOT/'rig/anatomy.json')]
    for p in core:
        identity.extend([p['texture'], p['geometry']])
    slots = {'body_front': {'required': True, 'modes': ['weighted'], 'layer': 20},
             'tail_cover': {'required': True, 'modes': ['weighted'], 'layer': 2},
             'sleeve_left': {'required': True, 'modes': ['weighted'], 'layer': 21},
             'sleeve_right': {'required': True, 'modes': ['weighted'], 'layer': 34},
             'headwear_front': {'required': True, 'modes': ['weighted'], 'layer': 45}}
    rig = {'format': 'roshan.rig-binding/1', 'rig_id': 'roshan.canvas.shared.swim', 'version': '0.1.0',
           'status': 'prototype', 'skeleton': reference(ROOT/'rig/skeleton.json'), 'bones': [b['name'] for b in BONES],
           'views': {VIEW: {'canvas': [1024, 720], 'slots': slots}},
           'sockets': {'headwear': {'bone': 'Head', 'offset': [0, 0]},
                       'grip_left': {'bone': 'LeftHand', 'offset': [0, 0]},
                       'grip_right': {'bone': 'RightHand', 'offset': [0, 0]}},
           'identity_assets': list({x['path']: x for x in identity}.values()), 'templates': {}}
    write(ROOT/'rig/rig_binding.json', rig)
    rig_sha = hashlib.sha256((ROOT/'rig/rig_binding.json').read_bytes()).hexdigest()
    tail_sources = {'ballet': [[1300, 494], [1110, 707], [889, 877], [683, 918], [518, 852]],
                    'magician': [[1305, 487], [1112, 708], [890, 875], [680, 915], [513, 851]]}
    catalog = {'format': 'roshan.skin-catalog/1', 'view': VIEW, 'skins': {}, 'stable_wardrobe_ids': {}}
    for theme in ['ballet', 'magician']:
        attachments = []
        coverage = {}
        body_source = [[350, 730], [355, 285]] if theme == 'ballet' else [[350, 730], [352, 283]]
        torso_fit = similarity(*body_source, BODY_ROOT, NECK)
        # One explicit, garment-only fit per skin; no anatomical geometry or bone change.
        tail_fit = similarity(tail_sources[theme][-1], tail_sources[theme][0], TAIL[-1], TAIL[0])
        mappings = [('body', 'body_front', 'body', torso_fit),
                    ('tail', 'tail_cover', 'tail', tail_fit),
                    ('sleeve_far', 'sleeve_left', 'LeftUpper', affine(.25, 151, [660, 267], shoulders[0])),
                    ('sleeve_near', 'sleeve_right', 'RightUpper', affine(.25, 140, [962, 263], shoulders[1])),
                    ('headwear', 'headwear_front', 'Head', affine(.38, 0, [1290, 340], [745, 100]))]
        for name, slot, kind, transform in mappings:
            spec = byname[theme+'_'+name]
            m, o = component_transform(spec, transform)
            data = mesh(Path(spec['output']), m, o, kind, spec)
            path = ROOT/'geometry'/(theme+'_'+name+'.json')
            write(path, data)
            identity_name = theme+'_'+slot
            attachments.append({'id': identity_name, 'view': VIEW, 'slot': slot, 'mode': 'weighted',
                                'texture': reference(Path(spec['output'])), 'geometry': reference(path)})
            coverage[slot] = identity_name
            FIT[theme+'_'+name] = {'matrix': m.tolist(), 'offset': o.tolist(), 'bone_field': kind,
                                  'registration': 'Uniform similarity fit; actual garment contour retained, never clipped to prior clothing alpha.'}
        skin = {'format': 'roshan.skin/1', 'skin_id': theme,
                'rig': {'id': rig['rig_id'], 'version': rig['version'], 'contract_sha256': rig_sha},
                'views': [VIEW], 'attachments': attachments, 'coverage': {VIEW: coverage},
                'provenance': {'sources': [{'asset': reference(ROOT/'art_source'/(theme+'_parts_take01.png')),
                                           'license': 'Project-commissioned built-in image_gen derivative of existing project Fashion Designer costume art; provider revision/seed unexposed',
                                           'role': 'garment_source', 'acceptance_scope': 'New source view candidate only; no visual, runtime, device, child or owner acceptance'}],
                               'edits': ['Named garment-only perspective view; Aseprite component isolation and matte cleanup; explicit recorded uniform registration; shared canonical bone field binding'],
                               'generator_calls': 1}}
        path = ROOT/'skins'/(theme+'.json')
        write(path, skin)
        catalog['skins'][theme] = path.relative_to(ROOT).as_posix()
        catalog['stable_wardrobe_ids'][theme] = {slot: f'{slot}_{theme}_v1' for slot in ['head', 'body', 'tail']}
        skin_refs.append(path)
    write(ROOT/'skins/catalog.json', catalog)
    write(ROOT/'rig/registration.json', FIT)
    sys.path.insert(0, str(REPO/'tools'))
    from validate_costume_skin import validate_skin
    reports = [validate_skin(p, ROOT/'rig/rig_binding.json', REPO) for p in skin_refs]
    write(ROOT/'evidence/format_validation.json', {'pass': True, 'skins': reports,
          'pose_state_scope': 'Only the common anatomical fin changes authored state. Garment parts keep one supported view/binding throughout this prototype; no unsupported per-costume pose selectors added to v1.'})
    write(ROOT/'rig/action_contract.json', {'format': 'roshan.action-library/1', 'fps': 30, 'bake_hz': 120,
          'cycle_seconds': 1.9, 'sequence_seconds': 7.6, 'phase_order': ['load', 'power', 'extend', 'glide', 'recover'],
          'fin_states_are_shared_anatomy': True, 'costume_cannot_override_actions': True,
          'source_floors': {'visible_strain': [.8, 1.2], 'visible_flips': 0,
                            'angular_speed_deg_s': 140, 'angular_acceleration_deg_s2': 650},
          'supported': ['one right-quarter view', 'start', 'stroke/glide cycle', 'brake/settle'],
          'not_established': ['facing turns', 'opposite view', 'grasp/tool contact', 'complete wardrobe', 'actual device/child/owner acceptance']})
    print('ASSETS_COMPILED', len(BONES), 'bones', len(core), 'shared anatomical states', '2 data-only skins', flush=True)


def main():
    specs = make_cut_spec()
    isolate(specs)
    build(specs)


if __name__ == '__main__':
    main()
