"""Audit actual native bone samples against the rendered material's own alpha.

Source-only deformation/contour checks. A pass never substitutes for exact
human movement/identity review, device playback or owner acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PREFIX = ROOT.relative_to(REPO).as_posix()+'/'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def asset(reference):
    path = REPO/reference['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == reference['sha256'], path
    return path


def matrix(value):
    a, b, c, d, x, y = value
    return np.array([[a, c, x], [b, d, y], [0, 0, 1.]], dtype=float)


def rest_matrices():
    result = {}
    for bone in load(ROOT/'rig/skeleton.json')['bones']:
        h = np.array(bone['head']);t = np.array(bone['tail'])
        angle = math.atan2(*(t-h)[::-1]);c, s = math.cos(angle), math.sin(angle)
        result[bone['name']] = np.array([[c, -s, h[0]], [s, c, h[1]], [0, 0, 1.]])
    return result


def material(texture_ref, mesh_ref):
    data = load(asset(mesh_ref))
    rgba = np.asarray(Image.open(asset(texture_ref)).convert('RGBA'))
    vertices = np.array(data['vertices'], float)
    triangles = np.array(data['triangles'], int)
    uv = np.array(data['uv'], float)
    visible = np.zeros(len(triangles), bool)
    # Inspect all covered source texel centres, including thin painted edges.
    # A few barycentric probes would miss narrow alpha inside a large quad.
    for i, corners in enumerate(uv[triangles]):
        x0,y0 = np.maximum(np.floor(corners.min(axis=0)).astype(int),0)
        x1,y1 = np.minimum(np.ceil(corners.max(axis=0)).astype(int), [rgba.shape[1],rgba.shape[0]])
        y,x = np.mgrid[y0:y1,x0:x1]
        p = np.stack([x+.5,y+.5],axis=2)
        e = np.stack([corners[1]-corners[0],corners[2]-corners[0]],axis=1)
        b = (p-corners[0])@np.linalg.inv(e).T
        inside = (b[:,:,0]>=-1e-8)&(b[:,:,1]>=-1e-8)&(b.sum(axis=2)<=1+1e-8)
        visible[i] = np.any(inside&(rgba[y0:y1,x0:x1,3]>=32))
    triangles = triangles[visible]
    reference = vertices[triangles]
    edges = np.stack([reference[:, 1]-reference[:, 0], reference[:, 2]-reference[:, 0]], axis=2)
    assert np.all(np.abs(np.linalg.det(edges)) > 1e-8)
    return {'vertices': vertices, 'weights': {k: np.array(v) for k, v in data['weights'].items()},
            'triangles': triangles, 'inverse': np.linalg.inv(edges),
            'sign': np.sign(np.linalg.det(edges)), 'texture': texture_ref['path'], 'visible_triangles': len(triangles)}


def strain(part, transforms, inverse_rests):
    points = np.c_[part['vertices'], np.ones(len(part['vertices']))]
    deformed = np.zeros_like(points)
    for name, weights in part['weights'].items():
        delta = matrix(transforms[name])@inverse_rests[name]
        deformed += (points@delta.T)*weights[:, None]
    q = deformed[part['triangles'], :2]
    edges = np.stack([q[:, 1]-q[:, 0], q[:, 2]-q[:, 0]], axis=2)
    jacobian = edges@part['inverse']
    values = np.linalg.svd(jacobian, compute_uv=False)
    flips = int(np.count_nonzero(np.sign(np.linalg.det(edges)) != part['sign']))
    return float(values.min()), float(values.max()), flips


def alpha_observation(path):
    image = np.asarray(Image.open(path).convert('RGBA'))
    mask = image[:, :, 3] >= 32
    labels, count = ndimage.label(mask)
    sizes = np.bincount(labels.ravel())[1:]
    major = sorted((int(n) for n in sizes if n >= 32), reverse=True)
    holes = ndimage.binary_fill_holes(mask) & ~mask
    hl, _ = ndimage.label(holes)
    hsize = np.bincount(hl.ravel())[1:]
    border = int(np.count_nonzero(mask[0]))+int(np.count_nonzero(mask[-1]))+int(np.count_nonzero(mask[:, 0]))+int(np.count_nonzero(mask[:, -1]))
    return {'major_components': major, 'largest_enclosed_gap_px': int(hsize.max()) if len(hsize) else 0,
            'edge_alpha_pixels': border, 'opaque_pixels': int(mask.sum())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    inverse_rests = {n: np.linalg.inv(m) for n, m in rest_matrices().items()}
    anatomy = load(ROOT/'rig/anatomy.json')
    cores = {p['id']: material(p['texture'], p['geometry']) for p in anatomy['parts']}
    garments = {}
    for theme in ['ballet', 'magician']:
        skin = load(ROOT/'skins'/(theme+'.json'))
        garments[theme] = {p['id']: material(p['texture'], p['geometry']) for p in skin['attachments']}
    if args.preview:
        jobs = {'pose_preview': load(ROOT/'evidence/pose_preview.json')['samples']}
    else:
        jobs = {n: load(ROOT/'evidence'/(n+'_samples.json'))['samples'] for n in ['ballet', 'magician', 'live_swaps']}
    reports = {}
    all_geometry = True
    for name, samples in jobs.items():
        min_value, max_value, flips = 1., 1., 0
        failed_frames = []
        worst = []
        outlines = []
        for sample in samples:
            parts = {k: v for k, v in cores.items() if not k.startswith('fin_') or k == sample['fin_state']}
            parts.update(garments[sample['skin']])
            bad = False
            for identity, part in parts.items():
                lower, upper, flipped = strain(part, sample['bones'], inverse_rests)
                min_value, max_value, flips = min(min_value, lower), max(max_value, upper), flips+flipped
                if lower < .8 or upper > 1.2 or flipped:
                    bad = True
                    worst.append({'frame': sample['index'], 'part': identity, 'min': lower, 'max': upper, 'flips': flipped})
            if bad:
                failed_frames.append(sample['index'])
            frame = sample['frame']
            path = ROOT/frame.removeprefix('res://')
            assert path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == sample['png_sha256']
            outlines.append({'frame': sample['index'], 'skin': sample['skin'], **alpha_observation(path)})
        motion = {}
        if not args.preview:
            dt = 1/30
            for bone in samples[0]['bones']:
                angles = np.unwrap([math.atan2(s['bones'][bone][1], s['bones'][bone][0]) for s in samples])*180/math.pi
                velocity = np.diff(angles)/dt
                acceleration = np.diff(velocity)/dt
                motion[bone] = {'speed': float(np.max(np.abs(velocity))), 'acceleration': float(np.max(np.abs(acceleration)))}
            if 'fin_turn_degrees' in samples[0]:
                yaw = np.array([s['fin_turn_degrees'] for s in samples])
                motion['FinViewControl'] = {'speed':float(np.max(np.abs(np.diff(yaw)/dt))),
                                           'acceleration':float(np.max(np.abs(np.diff(yaw,n=2)/dt**2)))}
            motion_pass = all(v['speed'] <= 140 and v['acceleration'] <= 650 for v in motion.values())
        else:
            motion_pass = None
        geometry_pass = not failed_frames
        contour_pass = all(len(o['major_components'])==1 and o['edge_alpha_pixels']==0 for o in outlines)
        all_geometry &= geometry_pass and motion_pass is not False and contour_pass
        reports[name] = {'geometry_pass': geometry_pass, 'min_visible_strain': min_value,
                         'max_visible_strain': max_value, 'visible_flips': flips, 'failed_frames': failed_frames,
                         'worst': worst[:40], 'motion': motion, 'motion_pass': motion_pass, 'outlines': outlines,
                         'contour_pass':contour_pass,
                         'max_components': max(len(x['major_components']) for x in outlines),
                         'largest_gap_px': max(x['largest_enclosed_gap_px'] for x in outlines),
                         'clipped_frames': [x['frame'] for x in outlines if x['edge_alpha_pixels']]}
        print(name, 'geometry', geometry_pass, 'strain', min_value, max_value, 'motion', motion_pass,
              'max_components', reports[name]['max_components'], 'gap', reports[name]['largest_gap_px'], flush=True)
    target = ROOT/'evidence'/('pose_geometry.json' if args.preview else 'native_geometry_audit.json')
    target.write_text(json.dumps({'geometry_and_motion_pass': bool(all_geometry), 'jobs': reports,
                     'floors_unchanged': {'strain': [.8, 1.2], 'flips': 0, 'speed_deg_s': 140, 'acceleration_deg_s2': 650},
                     'alpha_rule': 'Actual native image alpha>=32; one connected component >=32px, no clipped boundary pixels. Holes are diagnostics requiring semantic review. Every source texel centre covered by a material triangle is tested for visible alpha; no whole-character mask substitution.',
                     'coverage_limit':'LBS triangle strain and declared fin-view control derivatives are measured. Source-colour/contour pose interpolation is a separate visual review lane; these numbers do not certify its appearance or natural movement.',
                     'human_review_accepted': False, 'device_verified': False, 'owner_accepted': False,
                     'production_accepted': False}, indent=2)+'\n', encoding='utf-8', newline='\n')
    return 0 if all_geometry else 1


if __name__ == '__main__':
    raise SystemExit(main())
