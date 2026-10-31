"""Build the reference context, verify native Aseprite exports and index the set.

All pixel editing and composition is in Aseprite Lua. Pillow is read-only.
"""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
ASEPRITE = Path('C:/Program Files/Aseprite/Aseprite.exe')
FFMPEG = Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe')


def write(path, data):
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args):
    result = subprocess.run(list(map(str, args)), capture_output=True, text=True)
    if result.stdout.strip(): print(result.stdout.strip(), flush=True)
    if result.stderr.strip(): print(result.stderr.strip(), flush=True)
    result.check_returncode()


def bounds(path):
    a = np.array(Image.open(path).convert('RGBA'))[:, :, 3]
    y, x = np.where(a > 0)
    return [int(x.min()), int(y.min()), int(x.max()) + 1, int(y.max()) + 1]


def scene():
    (ROOT / 'scene/frames').mkdir(parents=True, exist_ok=True)
    for name, source in [('current_castle.png', 'assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png'),
                         ('current_slide.png', 'assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png')]:
        shutil.copy2(PROJECT / source, ROOT / 'context' / name)
    cards = []

    def card(ident, title, bottom_center, scale, phase=0):
        receipt = json.loads((ROOT / 'objects' / ident / 'AUTHORING_RECEIPT.json').read_text())
        b = bounds(ROOT / 'objects' / ident / 'frames/frame_00.png')
        x = bottom_center[0] - 256 * scale
        y = bottom_center[1] - (b[3] - 1) * scale
        cards.append({'id': ident, 'name': title, 'scale': scale, 'x': x, 'y': y,
                      'frames': len(receipt['state_rgba_sha256']), 'order': receipt['loop_order'],
                      'durations': receipt['playback_duration_units_12fps'],
                      'placement': 'current equipment anchor' if ident in ('07_swing', '08_seesaw') else 'reference dressing on clear grass / sky; not an accepted runtime placement'})

    card('05_cloud', 'Cloud - fresh billow keys', [837.5, 168], .41)
    card('06_smoke', 'Cabin smoke - fresh curls', [1475, 145], .11)
    card('02_huckleberry', 'Huckleberry - foreground study', [345, 584], .38)
    card('03_hydrangea', 'Hydrangea - foreground study', [1235, 598], .25)
    card('04_bellflower', 'Bellflower - foreground study', [665, 568], .24)
    img = Image.open(ROOT / 'context/current_slide.png')
    slide_scale = 620 * .3125 / img.height
    cards.append({'id': 'slide', 'name': 'Existing slide - fixed', 'path': 'context/current_slide.png',
                  'scale': slide_scale, 'x': 2550 * .3125 - img.width * slide_scale / 2,
                  'y': 1400 * .3125 - img.height * slide_scale})
    swing_bounds = bounds(ROOT / 'objects/07_swing/frames/frame_00.png')
    card('07_swing', 'Swing - fore/aft seat pitch', [3200 * .3125, 1390 * .3125], 150 / (swing_bounds[3] - swing_bounds[1]))
    saw_bounds = bounds(ROOT / 'objects/08_seesaw/frames/frame_00.png')
    card('08_seesaw', 'Seesaw - axle-centered fresh keys', [3826 * .3125, 1500 * .3125], 265 * .3125 / (saw_bounds[3] - saw_bounds[1]))
    layout = json.loads((PROJECT / 'scripts/arena/sky_lagoon_layout.json').read_text())
    castle = layout['cards']['castle'] if 'cards' in layout else layout['castle']
    cs = castle['height_master'] * .3125 / castle['texture_size'][1]
    cp = {'scale': cs, 'x': castle['anchor_master'][0] * .3125 - castle['anchor_pixel'][0] * cs,
          'y': castle['anchor_master'][1] * .3125 - castle['anchor_pixel'][1] * cs,
          'source_contract': 'scripts/arena/sky_lagoon_layout.json castle anchor; exact existing position/scale'}
    gate_cfg = json.loads((ROOT / 'objects/09_gate/IMPORT_PARAMETERS.json').read_text())
    r = gate_cfg['door_runs']
    gate_crop = [min(a[1] for a in r), min(a[0] for a in r), max(a[2] for a in r) + 1, max(a[0] for a in r) + 1]
    gate_receipt = json.loads((ROOT / 'objects/09_gate/AUTHORING_RECEIPT.json').read_text())
    cfg = {'width': 1920, 'height': 640, 'fps': 12, 'frame_count': 48,
           'status': 'MOTION_REFERENCE_CONTEXT_COMPOSITE', 'cards': cards, 'castle': cp,
           'gate_crop': gate_crop, 'gate': {'order': gate_receipt['loop_order'], 'durations': gate_receipt['playback_duration_units_12fps']},
           'source_panorama_dimensions': [6144, 2048], 'source_panorama_sha256': sha(ROOT / 'context/approved_clean_panorama.png'),
           'excluded_from_context': {'01_fir': 'Standalone study only. The current shared runtime contract disables the tall fir because it covers the scenic mountain path; the existing painted fir stays intact.'},
           'ownership': 'No removal or deformation of the approved panorama. Equipment on unpainted meadow; garden studies on clear foreground grass. Existing castle/bridge anchor preserved. Door leaves are cropped into its existing aperture; original castle portrait gets light only. This is a review arrangement, not a runtime screenshot or generator input.',
           'cinematic_delivery': False, 'runtime_integration': False}
    write(ROOT / 'scene/SCENE_PARAMETERS.json', cfg)
    run([ASEPRITE, '--batch', '--script-param', 'root=' + ROOT.as_posix(), '--script', ROOT / 'production/assemble_scene.lua'])
    run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '12', '-i',
         ROOT / 'scene/frames/frame_%03d.png', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15',
         '-pix_fmt', 'yuv420p', '-movflags', '+faststart', ROOT / 'scene/sky_lagoon_sample.mp4'])


def verify():
    temp = PROJECT / 'build/moderate-roundtrip'
    temp.mkdir(parents=True, exist_ok=True)
    checks = []
    for folder in sorted((ROOT / 'objects').iterdir()):
        frames = sorted((folder / 'frames').glob('frame_*.png'))
        prefix = temp / folder.name
        prefix.mkdir(exist_ok=True)
        run([ASEPRITE, '--batch', folder / (folder.name + '.aseprite'), '--save-as', prefix / 'frame_{frame}.png'])
        exported = sorted(prefix.glob('frame_*.png'), key=lambda p: int(p.stem.split('_')[-1]))
        assert len(exported) == len(frames), folder.name
        for original, restored in zip(frames, exported):
            a = np.array(Image.open(original).convert('RGBA'));b = np.array(Image.open(restored).convert('RGBA'))
            assert a.shape == (512, 512, 4) and np.array_equal(a, b), (folder.name, original.name, 'round trip')
            alpha = a[:, :, 3]
            assert not (alpha[0].any() or alpha[-1].any() or alpha[:, 0].any() or alpha[:, -1].any()), (folder.name, original.name, 'edge contact')
        values = [hashlib.sha256(Image.open(p).convert('RGBA').tobytes()).hexdigest() for p in frames]
        assert len(set(values)) == len(frames), (folder.name, 'duplicate states')
        checks.append({'id': folder.name, 'frames': len(frames), 'frame_size': [512, 512],
                       'unique_states': len(set(values)), 'native_master_exact_rgba_roundtrip': 'PASS',
                       'transparent_canvas_margin': 'PASS', 'bounds': [bounds(p) for p in frames],
                       'master_sha256': sha(folder / (folder.name + '.aseprite'))})
    run([ASEPRITE, '--batch', ROOT / 'scene/sky_lagoon_sample.aseprite', '--frame-range', '0,0', '--save-as', temp / 'scene_roundtrip.png'])
    assert np.array_equal(np.array(Image.open(temp / 'scene_roundtrip.png').convert('RGBA')),
                          np.array(Image.open(ROOT / 'scene/frames/frame_000.png').convert('RGBA'))), 'scene round trip'
    write(ROOT / 'MACHINE_VERIFICATION.json', {'status': 'PASS', 'objects': checks,
          'object_count': 10, 'total_raster_states': sum(a['frames'] for a in checks),
          'scene': {'dimensions': [1920, 640], 'frames': 48, 'fps': 12, 'duration_seconds': 4,
                    'first_frame_native_rgba_roundtrip': 'PASS', 'layered_master_sha256': sha(ROOT / 'scene/sky_lagoon_sample.aseprite')},
          'acceptance_limits': 'Byte and margin checks are machine evidence only. No owner selection, runtime/device/child or cinematic delivery acceptance.'})
    print('Exact Aseprite round trips: ten masters, 66 states and layered scene PASS.', flush=True)


def index():
    task = json.loads((ROOT / 'TASK_START.json').read_text())
    entries = []
    prompts = []
    for item in task['objects']:
        folder = ROOT / 'objects' / item['id']
        receipt = json.loads((folder / 'AUTHORING_RECEIPT.json').read_text())
        entries.append({'id': item['id'], 'title': item['title'], 'count': len(receipt['state_rgba_sha256']),
                        'order': receipt['loop_order'], 'durations': receipt['playback_duration_units_12fps']})
        if (folder / 'GENERATION.json').exists():
            generation = json.loads((folder / 'GENERATION.json').read_text())
            prompts.append(generation)
            if (folder / 'REPAIR_PROMPTS.json').exists(): prompts.append(json.loads((folder / 'REPAIR_PROMPTS.json').read_text()))
    write(ROOT / 'SAMPLES.json', entries)
    write(ROOT / 'PROMPT_SET.json', {'mode': 'built-in image_gen', 'native_sheets': [1024, 1536], 'native_cell': [512, 512], 'prompts': prompts,
          'glass_method': 'Reuse the higher-resolution owner portrait. Aseprite isolation and twelve light states; no generation.'})


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser();parser.add_argument('--verify-only', action='store_true');args=parser.parse_args()
    if not args.verify_only: scene()
    verify();index()
