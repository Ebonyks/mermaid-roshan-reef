#!/usr/bin/env python3
"""Numbers for the g1 repair and outfit redraw handoff (no images are written).

Reads committed repository files only and writes:
  data/g1_frames.json        per-frame g1 record: Claude's frame verdict and defects, latent block,
                             hand state, fitted and guide arm joints, a starting mask box and hashes
  data/g1_sources.json       exact bytes of every g1 file Codex binds (native frames, game cells, job,
                             latents, receipt, guides, pose)
  data/outfit_measurements.json  how the current outfit builder sizes clothes on each sprite

    python -I docs/handoffs/codex_roshan_wave_g1_repair_and_outfits_2026-10-07/tools/build_handoff_data.py
"""
import hashlib, json, math
from pathlib import Path
import numpy as np, cv2
from PIL import Image

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
PILOT = ROOT / 'assets_src/cinematics/claude_rig_pilot_20261007'
TAKE = PILOT / 'run2/g1_slowwave'
CELL_SCALE, OFFSET = 3.2025, (-216.95 + 40, 33.85)      # g1 canvas is shifted 40 px right (run 7)
CONTRACT = {'upper_arm': 25.5, 'forearm': 24.5, 'hand': 20.5, 'rest_hand': 16.2}

# Claude's frame-by-frame review of the native g1 frames (2026-10-07). "weak" frames need repair.
REVIEW = {
    5: 'hand soft; fingers fused into a fist-like smudge as the rise starts',
    6: 'hand a brown-grey smudge, fingers unreadable; 3 px ghost speck left at the old rest-hand position',
    7: 'open hand blurred, fingers smeared sideways',
    8: 'hand a brushy grey-brown smear; forearm soft',
    9: 'hand a grey smear with motion streaks',
    10: 'hand a grey ball-shaped blob with no fingers',
    11: 'fingers soft and partly fused; reads as a hand',
    12: 'hand smudged; dark streaks along the forearm and hand edge',
    25: 'hand smudged grey, fingers unreadable',
    26: 'hand smudged; speckled forearm; 33 px detached dark speck below the elbow',
    27: 'fingers rough and doubled; dark speckles along the forearm',
    28: 'hand a brown speckled blob; dark forearm texture',
    29: 'hand a brown blob with no fingers',
    30: 'hand a grey-brown blob',
    31: 'fingers soft and doubled',
    32: 'hand a blob, fingers fused',
    33: 'returning hand a soft smudge beside the hip',
}
MARGINAL = {13: 'hand readable; faint ghost trail to the left of the hand'}
PHASES = [('rest', 0, 4), ('rise', 5, 13), ('wave', 14, 24), ('lower', 25, 33), ('settle', 34, 40)]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).relative_to(ROOT)).replace('\\', '/')


def specks(path):
    a = np.array(Image.open(path).convert('RGB')).astype(int)
    bg = np.median(np.r_[a[:12].reshape(-1, 3), a[-12:].reshape(-1, 3)], 0)
    fg = (np.abs(a - bg).max(2) > 20).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg, connectivity=8)
    big = int(np.argmax(st[1:, 4])) + 1
    return [{'center_canvas_px': [int(cen[k][0]), int(cen[k][1])], 'area_px': int(st[k, 4])}
            for k in range(1, n) if k != big and st[k, 4] >= 3]


def guide_tip_speed(pose):
    """Fingertip speed of the guide arm, cell px per frame, centred on each frame (mean of in and out)."""
    s = (120.0, 103.0)                                   # K0 shoulder, 256 px cell
    tips = []
    for f in pose:
        a = f['arm_world_angles_rad']
        x = s[0] + sum(CONTRACT[k] * math.cos(v) for k, v in zip(('upper_arm', 'forearm', 'hand'), a))
        y = s[1] + sum(CONTRACT[k] * math.sin(v) for k, v in zip(('upper_arm', 'forearm', 'hand'), a))
        tips.append((x, y))
    step = [math.dist(tips[i], tips[i + 1]) for i in range(len(tips) - 1)]
    return [round(((step[i - 1] if i > 0 else 0) + (step[i] if i < len(step) else 0)) / 2, 1) for i in range(len(tips))]


def g1_frames():
    fit = json.loads((TAKE / 'arm_joints.json').read_text())['frames']
    guide = json.loads((PILOT / 'data/run7_joints.json').read_text())['frames']
    pose = json.loads((PILOT / 'data/rig_pose_run7.json').read_text())['frames']
    eyes = json.loads((TAKE / 'summary.json').read_text())['eyes_mostly_closed_frames']
    speed = guide_tip_speed(pose)
    rows = []
    for f, g, p in zip(fit, guide, pose):
        i = f['index']
        pts = np.array([f['wrist'], f['tip'], g['wrist'], g['tip']], float)
        lo = np.maximum(np.floor(pts.min(0) - 36), 0).astype(int)
        hi = np.minimum(np.ceil(pts.max(0) + 36), [640, 896]).astype(int)
        verdict = 'weak' if i in REVIEW else ('marginal' if i in MARGINAL else 'good')
        rows.append({
            'index': i, 'phase': next(n for n, a, b in PHASES if a <= i <= b),
            'latent_block': 0 if i == 0 else (i - 1) // 8 + 1,
            'verdict': verdict, 'defects': REVIEW.get(i) or MARGINAL.get(i) or '',
            'hand_state': p['hand_drawing'], 'eyes_open': i not in eyes, 'guide_fingertip_speed_cell_px': speed[i],
            'fit_joints_canvas_px': {k: [round(v, 1) for v in f[k]] for k in ('shoulder', 'elbow', 'wrist', 'tip')},
            'guide_joints_canvas_px': {k: [round(v, 1) for v in g[k]] for k in ('shoulder', 'elbow', 'wrist', 'tip')},
            'starting_mask_box_canvas_px': [int(lo[0]), int(lo[1]), int(hi[0]), int(hi[1])] if verdict != 'good' else None,
            'detached_specks': specks(TAKE / f'refined_frames/{i:04d}.png'),
            'native_frame': rel(TAKE / f'refined_frames/{i:04d}.png'),
            'native_sha256': sha(TAKE / f'refined_frames/{i:04d}.png'),
            'game_cell': rel(TAKE / f'clip/cells/{i:04d}.png'),
            'game_cell_sha256': sha(TAKE / f'clip/cells/{i:04d}.png')})
    weak = [r['index'] for r in rows if r['verdict'] == 'weak']
    return {
        'take': 'g1_slowwave', 'reviewer': 'Claude, frame-by-frame at native 640x896, 2026-10-07; agent review only',
        'canvas': [640, 896], 'canvas_to_cell': 'cell = (canvas - offset) / cell_scale',
        'cell_scale': CELL_SCALE, 'offset': list(OFFSET),
        'hand_length_targets_canvas_px': {
            'open': round(CONTRACT['hand'] * CELL_SCALE, 1), 'open_tolerance_5pct': [round(CONTRACT['hand'] * CELL_SCALE * .95, 1), round(CONTRACT['hand'] * CELL_SCALE * 1.05, 1)],
            'rest': round(CONTRACT['rest_hand'] * CELL_SCALE, 1),
            'upper_arm': round(CONTRACT['upper_arm'] * CELL_SCALE, 1), 'forearm': round(CONTRACT['forearm'] * CELL_SCALE, 1)},
        'latent_blocks': 'LTX-2.5 packs frame 0 alone, then 8 frames per latent block: 1-8, 9-16, 17-24, 25-32, 33-40',
        'speed_finding': 'Every weak or marginal frame has a guide fingertip speed of 10.7 to 15.1 cell px per frame '
                         '(centred); every good frame has 4.4 or less, including the crisp wave frames 14 to 24. '
                         'Smear tracks hand speed inside the 8-frame latent blocks.',
        'weak_frames': weak, 'marginal_frames': sorted(MARGINAL), 'weak_spans': [[5, 12], [25, 33]],
        'clean_anchor_frames': {'rise': [4, 14], 'lower': [24, 34]},
        'eye_boxes_canvas_px': [[round(x * CELL_SCALE + OFFSET[0], 1), round(y * CELL_SCALE + OFFSET[1], 1)] for x, y in ((132, 61), (152, 61))],
        'eye_box_note': 'K0 iris centres mapped to the g1 canvas; each iris is about 9 cell px (29 canvas px) across',
        'mask_note': 'Starting mask box = union of the fitted and guide hand (wrist and fingertip) plus 36 px. The fit is loose on '
                     'smeared frames; refine the mask on the frame itself and include any ghost trail or speck.',
        'frames': rows}


def g1_sources():
    files = sorted([*TAKE.glob('refined_frames/*.png'), *TAKE.glob('stage1_frames/*.png'), *TAKE.glob('clip/cells/*.png'),
                    TAKE / 'clip/atlas.png', TAKE / 'clip/cells_report.json', TAKE / 'clip/pose_fit_clip.json',
                    *TAKE.glob('clip/outfits/*.png'), TAKE / 'receipt.json', TAKE / 'job.json', TAKE / 'workflow.api.json',
                    TAKE / 'refined_latent/refined_video_00001_.latent', TAKE / 'stage1_latent/stage1_video_00001_.latent',
                    TAKE / 'summary.json', TAKE / 'measure.json', TAKE / 'arm_joints.json', TAKE / 'review.mp4',
                    PILOT / 'jobs/g1_slowwave.json', PILOT / 'data/rig_pose_run7.json', PILOT / 'data/run7_joints.json',
                    PILOT / 'run7/identity_shift40.png', PILOT / 'run7/guide_plan.json',
                    *PILOT.glob('run7/guide_half/*.png'), *PILOT.glob('run7/guide_quarter/*.png'),
                    ROOT / 'assets/characters/roshan_25d/roshan_gesture_a.png'])
    return {'files': [{'path': rel(p), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files]}


def outfit_measurements():
    fit = json.loads((ROOT / 'assets_src/fashion_designer/party_garment_v1/pose_fit.json').read_text())
    native = Image.open(ROOT / 'assets_src/fashion_designer/party_garment_v1/native.png')
    bbox = native.getbbox(); nw, nh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cells = []
    for base, spec in fit['sources'].items():
        for k, c in enumerate(spec['cells']):
            w, h = c[2] - c[0], c[3] - c[1]
            gw, gh = max(28, round(w * 1.7)), max(48, round(h * 1.42))
            cells.append({'atlas': base, 'cell': k, 'bodice_box': c, 'garment_px': [gw, gh], 'garment_aspect': round(gw / gh, 2),
                          'aspect_vs_native': round((gw / gh) / (nw / nh), 2), 'downscale_from_native': round(nh / gh, 1)})
    ratios = [c['aspect_vs_native'] for c in cells]
    others = {'rumi_eight_pose_runtime': ('assets/characters/rumi/rumi_eight_pose_runtime.png', 256, 384, 34),
              'rumi_pool_idle_swim_atlas': ('assets/characters/rumi/rumi_pool_idle_swim_atlas.png', 256, 256, 34),
              'baby_eagle': ('assets/characters/companions/baby_eagle.png', 290, 512, 44),
              'daddy': ('assets/characters/friends/daddy.webp', 725, 1024, 92),
              'rainbow_friend': ('assets/sprites/dust_bunnies/rainbow_friend.png', 512, 512, 92),
              'roshan_gesture_a (K0)': ('assets/characters/roshan_25d/roshan_gesture_a.png', 256, 256, 26)}
    bows = {}
    for name, (p, cw, ch, bw) in others.items():
        a = np.array(Image.open(ROOT / p).convert('RGBA'))[0:ch, 0:cw, 3] > 127
        ys, xs = np.nonzero(a); fh = int(ys.max() - ys.min())
        bows[name] = {'source': p, 'sha256': sha(ROOT / p), 'first_cell_figure_height_px': fh, 'bow_width_px': bw,
                      'bow_width_pct_of_figure_height': round(100 * bw / fh, 1)}
    return {
        'builder': {'path': 'tools/build_fashion_outfits.gd', 'sha256': sha(ROOT / 'tools/build_fashion_outfits.gd')},
        'party_garment': {'path': 'assets_src/fashion_designer/party_garment_v1/native.png',
                          'sha256': sha(ROOT / 'assets_src/fashion_designer/party_garment_v1/native.png'),
                          'cropped_px': [nw, nh], 'aspect': round(nw / nh, 2), 'views_drawn': ['front'],
                          'placement_rule': 'width = max(28, 1.7 x bodice box width), height = max(48, 1.42 x box height); '
                                            'Lanczos resize; one front drawing for every cell, including back and side views'},
        'party_on_roshan_cells': {'count': len(cells), 'aspect_vs_native_min': min(ratios), 'aspect_vs_native_max': max(ratios),
                                  'downscale_min': min(c['downscale_from_native'] for c in cells),
                                  'downscale_max': max(c['downscale_from_native'] for c in cells),
                                  'back_view_cells': ['roshan_directional 3, 4, 5', 'roshan_swim_back 0-15'],
                                  'side_view_cells': ['roshan_directional 2, 6'], 'cells': cells},
        'garden_and_disguise': 'Recolour of the source bodice pixels (r > 0.54, b > 0.49, b > 1.11 g, r > 0.99 b) to green, plus a '
                               'procedural bow; disguise uses the same recolour with a larger green bow',
        'bows': {'method': 'procedural: two triangles and an ellipse knot, flat fill, navy ink, no painting',
                 'per_character': bows},
        'pose_fit': {'path': 'assets_src/fashion_designer/party_garment_v1/pose_fit.json',
                     'sha256': sha(ROOT / 'assets_src/fashion_designer/party_garment_v1/pose_fit.json'), 'status': fit['status']}}


def main():
    (HERE / 'data').mkdir(exist_ok=True)
    for name, fn in (('g1_frames.json', g1_frames), ('g1_sources.json', g1_sources), ('outfit_measurements.json', outfit_measurements)):
        (HERE / 'data' / name).write_text(json.dumps(fn(), indent=1) + '\n')
        print('wrote', name)


if __name__ == '__main__':
    main()
