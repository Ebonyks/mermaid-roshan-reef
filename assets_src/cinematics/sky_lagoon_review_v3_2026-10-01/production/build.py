"""Analyze native alpha/anchors, then import and paint every output in Aseprite.

Pillow/numpy/scipy are read-only image-analysis tools here. Image edits, isolation,
registration, tiny border repairs and light states are authored by Aseprite Lua.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ASEPRITE = Path('C:/Program Files/Aseprite/Aseprite.exe')
ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runs(mask):
    result = []
    for y, row in enumerate(mask):
        values = np.diff(np.r_[False, row, False].astype(np.int8))
        for x0, x1 in zip(np.flatnonzero(values == 1), np.flatnonzero(values == -1)):
            result.append([y, int(x0), int(x1 - 1)])
    return result


def main_component(cell):
    labels, _ = ndimage.label(cell[:, :, 3] > 64)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    core = labels == sizes.argmax()
    keep = ndimage.binary_dilation(core, iterations=2) & (cell[:, :, 3] > 0)
    ys, xs = np.where(core)
    bounds = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    return core, keep, bounds


def edge_caps(core):
    caps = []
    for side, column in [('left', 0), ('right', -1)]:
        row = core[:, column]
        values = np.diff(np.r_[False, row, False].astype(np.int8))
        for y0, y1 in zip(np.flatnonzero(values == 1), np.flatnonzero(values == -1)):
            caps.append([side, int(y0), int(y1 - 1)])
    return caps


def analyze_object(folder):
    ident = folder.name
    cfg = {'id': ident, 'kind': ident.split('_', 1)[1], 'cell_width': 512,
           'cell_height': 512, 'poses': [], 'duration_units': [2, 2, 4, 2, 2, 4],
           'lane': 'MOTION_REFERENCE_ONLY',
           'method': 'Fresh generated pose drawings; Aseprite alpha cleanup and anchor registration. No deformation of the old source supplies motion.'}
    if ident == '10_glass':
        cfg.update(kind='glass', input='window_identity_source.png', duration_units=[2] * 12,
                   method='Reuse the higher-resolution owner-supplied portrait without pose changes. Aseprite isolates the existing arch and paints twelve restrained moving light-band states; no identity redraw.')
        array = np.array(Image.open(folder / cfg['input']).convert('RGBA'))
        barrier = (array[:, :, :3].max(axis=2) < 45) & (array[:, :, 3] > 64)
        filled = ndimage.binary_fill_holes(barrier)
        labels, _ = ndimage.label(filled)
        sizes = np.bincount(labels.ravel()); sizes[0] = 0
        core = labels == sizes.argmax()
        keep = ndimage.binary_dilation(core, iterations=1)
        ys, xs = np.where(core)
        scale = 440 / (int(ys.max()) + 1 - int(ys.min()))
        cfg.update(cell_width=array.shape[1], cell_height=array.shape[0])
        cfg['poses'] = [{'origin': [0, 0], 'keep_runs': runs(keep), 'scale': scale,
                         'offset': [256 - scale * (xs.min() + xs.max()) / 2,
                                    466 - scale * ys.max()],
                         'native_bounds': [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]}]
        return cfg
    cfg['input'] = 'padded_native.png' if (folder / 'padded_native.png').exists() else 'generated_native.png'
    array = np.array(Image.open(folder / cfg['input']).convert('RGBA'))
    assert array.shape == (1536, 1024, 4), (ident, array.shape)
    scale = {'01_fir': 1.0, '02_huckleberry': .875, '03_hydrangea': .9,
             '04_bellflower': .95, '05_cloud': .9, '06_smoke': 1.0,
             '07_swing': .5, '08_seesaw': 1.0, '09_gate': .95}[ident]
    sockets = [[125, 341, 387, 341], [125, 326, 387, 326], [125, 288, 387, 288],
               [125, 309, 387, 309], [125, 270, 387, 270], [125, 274, 387, 274]]
    swing_y = [345, 337, 319, 345, 337, 319]
    for n in range(6):
        origin = [(n % 2) * 512, (n // 2) * 512]
        cell = array[origin[1]:origin[1] + 512, origin[0]:origin[0] + 512]
        core, keep, bounds = main_component(cell)
        ys, xs = np.where(core)
        lower_y, lower_x = np.where(core & (np.indices(core.shape)[0] >= bounds[3] - 10))
        anchor = [float(lower_x.mean()), float(ys.max())]
        target = [256, 464]
        if ident == '02_huckleberry': target[1] = 440
        if ident == '05_cloud':
            anchor = [float(xs.mean()), float(ys.mean())]; target[1] = 256
        if ident == '08_seesaw':
            red, green, blue = [cell[:, :, k].astype(int) for k in range(3)]
            grid_y, grid_x = np.indices(core.shape)
            axle = core & (green > 160) & (blue > 150) & (blue-red > 40) & (grid_x > 205) & (grid_x < 305) & (grid_y > 200) & (grid_y < 312)
            ay, ax = np.where(axle)
            assert len(ax) > 100, (ident, n, 'axle not found')
            anchor = [(float(ax.min()) + float(ax.max())) / 2, (float(ay.min()) + float(ay.max())) / 2]
            target = [256, 275]
        offset = [target[0] - scale * anchor[0], target[1] - scale * anchor[1]]
        if ident == '07_swing': offset = [128, swing_y[n] - scale * sockets[n][1]]
        pose = {'origin': origin, 'keep_runs': runs(keep), 'scale': scale, 'offset': offset,
                'native_bounds': bounds, 'native_anchor': anchor, 'target_anchor': target,
                'border_caps': edge_caps(core) if ident == '02_huckleberry' else []}
        assert not ((core[0].any() or core[-1].any()) and ident != '02_huckleberry'), (ident, n, 'native vertical clipping')
        cfg['poses'].append(pose)
    if ident not in ('07_swing', '08_seesaw'):
        # Fit the union of all registered poses, rather than clipping a wide
        # leaf because its root is not at the center of the native cell.
        left = max(p['native_anchor'][0] - p['native_bounds'][0] for p in cfg['poses'])
        right = max(p['native_bounds'][2] - p['native_anchor'][0] for p in cfg['poses'])
        fitted = min(scale, 228 / max(left, right))
        for p in cfg['poses']:
            p['scale'] = fitted
            p['offset'] = [p['target_anchor'][0] - fitted * p['native_anchor'][0],
                           p['target_anchor'][1] - fitted * p['native_anchor'][1]]
    if ident == '01_fir': cfg['fixed_bottom_y'] = 395
    if ident == '04_bellflower': cfg['fixed_bottom_y'] = 421
    if ident == '07_swing':
        cfg.update(kind='swing', frame_scale=480 / 1338, seat_sockets=sockets, socket_target_y=swing_y,
                   swing_contract={'axis': 'horizontal suspension beam; fore/aft pitch',
                                   'hooks': [[193, 118], [320, 118]],
                                   'camera': 'fixed approximately frontal/orthographic reference projection',
                                   'contact_review': 'Sockets are manually authored pose registration; production physical/contact acceptance remains open.'})
    if ident == '08_seesaw': cfg['fixed_base_rect'] = [182, 355, 331, 398]
    if ident == '09_gate':
        cfg['kind'] = 'gate'
        cfg['duration_units'] = [3, 2, 2, 2, 3, 4]
        cell = array[:512, :512]; red, green, blue = [cell[:, :, k].astype(int) for k in range(3)]
        yy, xx = np.indices((512, 512))
        door = (red > 130) & (red > green * 1.25) & (red > blue * 1.12) & (xx >= 190) & (xx <= 325) & (yy >= 212) & (yy <= 435)
        door = ndimage.binary_fill_holes(ndimage.binary_closing(door, iterations=2))
        door = ndimage.binary_dilation(door, iterations=2)
        p = cfg['poses'][0]
        # Geometry-analysis mask expressed in target pixels; Aseprite paints it.
        sy = np.floor((yy - p['offset'][1]) / p['scale']).astype(int)
        sx = np.floor((xx - p['offset'][0]) / p['scale']).astype(int)
        valid = (sx >= 0) & (sx < 512) & (sy >= 0) & (sy < 512)
        outmask = np.zeros((512, 512), dtype=bool)
        outmask[valid] = door[sy[valid], sx[valid]]
        cfg['door_runs'] = runs(outmask)
    return cfg


def run(*args):
    result = subprocess.run([str(ASEPRITE), '--batch', *map(str, args)], capture_output=True, text=True, check=True)
    if result.stdout.strip(): print(result.stdout.strip(), flush=True)


def build_object(folder, overwrite):
    ident = folder.name
    master = folder / (ident + '.aseprite')
    if master.exists() and not overwrite: raise RuntimeError('Existing editable master; use explicit --overwrite only for authorized rebuilds: ' + str(master))
    cfg = analyze_object(folder)
    (folder / 'IMPORT_PARAMETERS.json').write_text(json.dumps(cfg, indent=2), encoding='utf-8')
    (folder / 'frames').mkdir(exist_ok=True)
    run('--script-param', 'root=' + ROOT.as_posix(), '--script-param', 'id=' + ident,
        '--script', ROOT / 'production/import_pose_sheet.lua')
    height = 2048 if ident == '10_glass' else 1024
    run(master, '--sheet', folder / 'spritesheet.png', '--data', folder / 'spritesheet.json',
        '--format', 'json-array', '--sheet-type', 'rows', '--sheet-width', '2048', '--sheet-height', str(height))
    frames = sorted((folder / 'frames').glob('frame_*.png'))
    count = 12 if ident == '10_glass' else 6
    assert len(frames) == count
    proof = {'id': ident, 'status': 'REFERENCE_SAMPLE', 'frame_canvas': [512, 512],
             'unique_generated_pose_drawings': 0 if ident == '10_glass' else 6,
             'authored_light_states': 12 if ident == '10_glass' else 0,
             'method': cfg['method'], 'input': cfg['input'], 'input_sha256': digest(folder / cfg['input']),
             'state_rgba_sha256': [hashlib.sha256(Image.open(p).convert('RGBA').tobytes()).hexdigest() for p in frames],
             'pose_native_bounds': [p['native_bounds'] for p in cfg['poses']],
             'border_cap_repairs': [p.get('border_caps', []) for p in cfg['poses']],
             'fixed_bottom_y': cfg.get('fixed_bottom_y'), 'fixed_base_rect': cfg.get('fixed_base_rect'),
             'edge_cleanup': {'alpha_cutoff': 64 if ident == '06_smoke' else 192,
                              'opaque_contours': ident != '06_smoke',
                              'method': 'Largest connected subject mask; Aseprite rejects stray semi-transparent border noise, nearest-neighbor native pose registration.'},
             'loop_order': list(range(count)) if ident != '09_gate' else [0,1,2,3,4,5,4,3,2,1],
             'duration_units_12fps': cfg['duration_units'],
             'limits': 'Six-key acting examples remain coarse. AI detail/topology continuity and manual contacts require owner/production review. Not human hand drawing, accepted runtime art or full-frame cinematic delivery.'}
    if ident == '09_gate': proof['playback_duration_units_12fps'] = [3,2,2,2,3,4,2,2,2,2]
    else: proof['playback_duration_units_12fps'] = cfg['duration_units']
    (folder / 'AUTHORING_RECEIPT.json').write_text(json.dumps(proof, indent=2), encoding='utf-8')
    print(ident + ': native import and ' + str(count) + ' saved raster states ready.', flush=True)


def main():
    p = argparse.ArgumentParser();p.add_argument('--id');p.add_argument('--overwrite', action='store_true');args=p.parse_args()
    folders = [ROOT / 'objects' / args.id] if args.id else sorted((ROOT / 'objects').iterdir())
    for folder in folders:
        if folder.is_dir(): build_object(folder, args.overwrite)


if __name__ == '__main__': raise SystemExit('Use production/refine.py; this module supplies read-only source analysis and bounded import helpers.')
