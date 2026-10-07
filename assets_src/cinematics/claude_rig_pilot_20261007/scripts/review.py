#!/usr/bin/env python3
"""Measure both runs and write the review copies.

  data/run1_joints.json   run-1 rig arm joints (512 px render canvas) in measure_wave.py's format
  data/run1_measure.json  measure_wave.py on the Godot-rendered run-1 frames (figure/head scale, W3 arm)
  data/run2_measure.json  W3 arm lengths of the run-2 guides vs the Union take-1 guides and the take itself
  run1/review.mp4         take 1 (registered to the same cell scale) | run 1 Godot render, 24 fps
  run2/review.mp4         Union guide | rig guide | take 1, 24 fps
The MP4s are H.264 viewing copies; the PNG frames are authoritative.

    python -I scripts/review.py
"""
import math, subprocess, sys, tempfile
import numpy as np, cv2
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import *

R1 = 2.0   # run-1 render scale: 512 px canvas = 2 x the 256 px cell


def run1_joints(pose, rig):
    B = {b['name']: b for b in rig['bones']}
    waist = np.array(B['Root']['head']); sh = np.array(K0_ARM['shoulder'])
    L1, L2 = dist(K0_ARM['shoulder'], K0_ARM['elbow']), dist(K0_ARM['elbow'], K0_ARM['wrist'])
    hl = {'rest': dist(K0_ARM['wrist'], K0_ARM['tip']), 'open': CONTRACT['hand']}
    out = []
    for f in pose['frames']:
        d = f['body_delta']; c, s = math.cos(d['torso']), math.sin(d['torso'])
        v = sh - waist; S = waist + np.array([d['root_dx'], d['root_dy']]) + np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])
        S = S + np.array(f['shoulder_offset_cell']); A = f['arm_world_angles_rad']
        E = S + L1 * np.array([math.cos(A[0]), math.sin(A[0])]); W = E + L2 * np.array([math.cos(A[1]), math.sin(A[1])])
        T = W + hl[f['hand_drawing']] * np.array([math.cos(A[2]), math.sin(A[2])])
        out.append({'index': f['index'], **{k: (R1 * p).tolist() for k, p in zip(('shoulder', 'elbow', 'wrist', 'tip'), (S, E, W, T))},
                    'hand_open': f['hand_drawing'] == 'open'})
    return out


def w3(J, scale):
    L = {'upper_arm': dist(J['shoulder'], J['elbow']), 'forearm': dist(J['elbow'], J['wrist']), 'hand': dist(J['wrist'], J['tip'])}
    return {k: round(100 * (v / (CONTRACT[k] * scale) - 1), 1) for k, v in L.items()}


def worst(rows, keys=('upper_arm', 'forearm', 'hand')):
    w = {}
    for r in rows:
        for k in keys:
            if k in r and (k not in w or abs(r[k]) > abs(w[k]['pct'])):
                w[k] = {'frame': r['frame'], 'pct': r[k]}
    return w


def video(frames, out):
    with tempfile.TemporaryDirectory() as t:
        for i, im in enumerate(frames):
            Image.fromarray(im).save(f'{t}/{i:04d}.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', f'{t}/%04d.png', '-c:v', 'libx264',
                        '-crf', '15', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)], check=True)


def label(im, text):
    im = im.copy(); cv2.putText(im, text, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 40, 40), 1, cv2.LINE_AA); return im


def main():
    pose = load_json(PILOT / 'data/rig_pose.json'); rig = load_json(PILOT / 'run1_godot/rig.json')
    J1 = run1_joints(pose, rig)
    save_json(PILOT / 'data/run1_joints.json', {'note': 'run-1 rig arm joints, 512 px render canvas (2 x cell)', 'frames': J1})
    r = subprocess.run([sys.executable, '-I', str(MEASURE), '--frames', str(PILOT / 'run1/frames/%04d.png'), '--count', '41',
                        '--cell-scale', str(R1), '--offset', '0', '0', '--joints', str(PILOT / 'data/run1_joints.json'),
                        '--label', 'Claude rig pilot run 1 (rules off): Godot 4.7.2 skinned/cutout rig, LTX take-1 motion',
                        '--out', str(PILOT / 'data/run1_measure.json')], capture_output=True, text=True)
    print('run 1 measure_wave:\n' + r.stdout)
    # Run 2: W3 on the guides (joints are exact), against the Union take-1 guides and the take's own arm.
    rig2 = load_json(PILOT / 'data/run2_joints.json')['frames']
    tr = load_json(PILOT / 'data/take1_tracks.json')['frames']
    rows = {'rig_guide_run2': [], 'union_guide_take1': [], 'ltx_take1_arm_fit': []}
    for i in range(FRAMES):
        rows['rig_guide_run2'].append({'frame': i, **w3(rig2[i], CELL_SCALE)})
        g = guide_arm_joints(i); rows['union_guide_take1'].append({'frame': i, **w3(g, CELL_SCALE)})
        k = tr[i]['rig_arm_fit']['segment_scale_vs_contract']
        rows['ltx_take1_arm_fit'].append({'frame': i, 'upper_arm': round(100 * (k[0] - 1), 1), 'forearm': round(100 * (k[1] - 1), 1)})
    summary = {n: {'worst': worst(v), 'pass_5pct': all(abs(x[k]) <= 5 for x in v for k in ('upper_arm', 'forearm', 'hand') if k in x)}
               for n, v in rows.items()}
    save_json(PILOT / 'data/run2_measure.json', {
        'contract_cell_px': CONTRACT, 'canvas_px_per_cell_px': CELL_SCALE, 'limit_pct': 5.0,
        'notes': {'rig_guide_run2': 'exact joints of the rendered run-2 guides',
                  'union_guide_take1': 'joints from guide.lua math (hand = wrist (0,18) to longest tip (1,-35)); the hand outline is the same at rest',
                  'ltx_take1_arm_fit': 'segment lengths the analysis-by-synthesis fit found in the generated take (hand fixed at contract); smeared frames are low confidence'},
        'summary': summary, 'frames': rows})
    for n, v in summary.items():
        print(n, 'PASS' if v['pass_5pct'] else 'FAIL', v['worst'])
    # Review videos.
    M = np.array([[R1 / CELL_SCALE, 0, -R1 * OFFSET[0] / CELL_SCALE], [0, R1 / CELL_SCALE, -R1 * OFFSET[1] / CELL_SCALE]])
    v1 = []
    for i in range(FRAMES):
        t = np.array(Image.open(str(TAKE1) % i).convert('RGB'))
        t = cv2.warpAffine(t, M, (512, 512), flags=cv2.INTER_AREA, borderValue=(238, 238, 238))
        g = np.array(Image.open(PILOT / f'run1/frames/{i:04d}.png').convert('RGB'))
        v1.append(np.concatenate([label(t, f'LTX take 1  {i:02d}'), label(g, f'Run 1 rig (Godot)  {i:02d}')], 1))
    video(v1, PILOT / 'run1/review.mp4')
    v2 = []
    for i in range(FRAMES):
        u = np.array(Image.open(UNION / f'guide_half/{i:04d}.png').convert('RGB'))
        g = np.array(Image.open(PILOT / f'run2/guide_half/{i:04d}.png').convert('RGB'))
        t = np.array(Image.open(str(TAKE1) % i).convert('RGB').resize((320, 448), Image.LANCZOS))
        lab = lambda im, s: cv2.putText(im.copy(), s, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, .45, (200, 200, 200), 1, cv2.LINE_AA)
        v2.append(np.concatenate([lab(u, f'Union guide {i:02d}'), lab(g, f'Rig guide (run 2) {i:02d}'), label(t, f'LTX take 1 {i:02d}')], 1))
    video(v2, PILOT / 'run2/review.mp4')
    print('videos written')


if __name__ == '__main__':
    main()
