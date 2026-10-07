#!/usr/bin/env python3
"""Bring one rig-pilot LTX take home from the PC runner, measure it, and test the game outfits on it.

  1. copy results/rig_pilot/<job> (staged from the PC) into run2/<job>/, checking every output hash
     against the runner receipt;
  2. track the take (track_ltx.py, arm search seeded from the rig guide) and run measure_wave.py:
     W2 figure/head scale, W3 upper arm and forearm (the fit holds the hand at the contract length,
     so the hand row is not a measurement);
  3. end frames: frames 0, 1, 39 and 40 against the approved K0 cell (silhouette IoU, colour error);
  4. whole-frame game cells (clip_cells.py), clip clothing fit (clip_pose_fit.py), the four game outfits
     baked by the production builder (bake_clip_outfits.sh) and their consistency (cosmetics_review.py);
  5. run2/<job>/review.mp4: rig guide | this take | Union take 1, 24 fps (viewing copy).
Writes run2/<job>/summary.json.

    python -I scripts/process_take.py <job_id> <staged results dir> [--godot PATH]
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import *

S = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(*cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode not in (0, 1):
        raise SystemExit(f'{cmd[1] if len(cmd) > 1 else cmd[0]} failed:\n{r.stdout}\n{r.stderr}')
    return r.stdout


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('job'); ap.add_argument('staged'); ap.add_argument('--godot', default='godot')
    v = ap.parse_args(); src = Path(v.staged); out = PILOT / 'run2' / v.job
    receipt = json.loads((src / 'receipt.json').read_text())
    assert receipt['status'] == 'EXECUTION_PASS', receipt.get('error')
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)
    bad = [k for k, h in receipt['output_files'].items() if sha(out / k) != h]
    assert not bad, f'output hash mismatch {bad[:3]}'
    frames = out / 'refined_frames'
    assert len(list(frames.glob('*.png'))) == FRAMES
    pat = str(frames / '%04d.png')
    # 2. track + measure
    tracks = f'data/{v.job}_tracks.json'
    run(sys.executable, '-I', S / 'track_ltx.py', '--frames', pat, '--seed-guide', 'run2', '--out', tracks)
    T = load_json(PILOT / tracks)
    joints = [{'index': f['index'], **f['arm_canvas'], 'hand_open': f['rig_arm_fit']['hand_drawing'] == 'open'} for f in T['frames']]
    save_json(out / 'arm_joints.json', {'note': 'arm joints fitted to the take (canvas px); hand held at contract length', 'frames': joints})
    rep = run(sys.executable, '-I', MEASURE, '--frames', pat, '--count', FRAMES, '--cell-scale', CELL_SCALE, '--offset', *OFFSET,
              '--joints', out / 'arm_joints.json', '--label', f'Claude rig pilot run 2 {v.job}', '--out', out / 'measure.json')
    M = load_json(out / 'measure.json')
    arm = M['arm_length_vs_contract_pct']
    w3 = {k: max((abs(r[k]) for r in arm if k in r), default=None) for k in ('upper_arm', 'forearm')}
    ious = [f['rig_arm_fit']['iou_vs_take_arm_mask'] for f in T['frames']]
    # 4. cells, clothing fit, outfits
    clip = out / 'clip'
    run(sys.executable, '-I', S / 'clip_cells.py', pat, clip)
    name = f'roshan_wave_{v.job}'
    run(sys.executable, '-I', S / 'clip_pose_fit.py', clip, name)
    env = dict(os.environ, GODOT=v.godot)
    run('bash', S / 'bake_clip_outfits.sh', str(clip.relative_to(ROOT)), env=env)
    run(sys.executable, '-I', S / 'cosmetics_review.py', clip, name)
    # 3. end frames vs K0
    k0 = np.array(Image.open(ATLAS).convert('RGBA'))[0:256, 0:256].astype(np.float32)
    ends = {}
    for i in (0, 1, 39, 40):
        c = np.array(Image.open(clip / 'cells' / f'{i:04d}.png')).astype(np.float32)
        a, b = k0[..., 3] > 127, c[..., 3] > 127; both = a & b
        ends[i] = {'silhouette_iou_vs_K0': round(float((a & b).sum() / (a | b).sum()), 4),
                   'rgb_mean_abs_error_vs_K0': round(float(np.abs(c[both, :3] - k0[both, :3]).mean()), 2)}
    # 5. review video
    with tempfile.TemporaryDirectory() as t:
        for i in range(FRAMES):
            g = cv2.resize(np.array(Image.open(PILOT / f'run2/guide_half/{i:04d}.png').convert('RGB')), (640, 896), interpolation=cv2.INTER_NEAREST)
            x = np.array(Image.open(pat % i).convert('RGB')); u = np.array(Image.open(str(TAKE1) % i).convert('RGB'))
            row = []
            for im, s in ((g, 'rig guide'), (x, v.job), (u, 'Union take 1')):
                im = im.copy(); cv2.putText(im, f'{s} {i:02d}', (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2, cv2.LINE_AA); row.append(im)
            Image.fromarray(np.concatenate(row, 1)).save(f'{t}/{i:04d}.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', f'{t}/%04d.png', '-c:v', 'libx264', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out / 'review.mp4')], check=True)
    cos = load_json(clip / 'cosmetics_report.json'); fit = load_json(clip / 'pose_fit_report.json')
    summary = {'job': v.job, 'receipt': {k: receipt.get(k) for k in ('status', 'prompt_id', 'elapsed_seconds', 'sampled_card_peak_mib',
                                                                       'workflow_sha256', 'take_number')},
               'W2': {k: M['checks'][k] for k in ('figure_scale_pp_pct', 'head_scale_pp_pct')},
               'W3_worst_abs_pct': w3, 'W3_pass_5pct': all(x is not None and x <= 5 for x in w3.values()),
               'arm_fit_iou': {'min': round(min(ious), 3), 'median': round(float(np.median(ious)), 3)},
               'end_frames_vs_K0': ends,
               'cosmetics': {k: {x: r[x] for x in ('frames_with_clothing', 'changed_px_spread_pct', 'centroid_vs_box_drift_px')}
                             for k, r in cos['outfits'].items()},
               'bodice_travel_px': fit['bodice_travel_px'], 'bodice_rotation_range_deg': fit['rotation_range_deg'],
               'clothing_slip_px': fit['clothing_slip_px'], 'used_as_delivery_pixels': False}
    save_json(out / 'summary.json', summary)
    print(rep)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
