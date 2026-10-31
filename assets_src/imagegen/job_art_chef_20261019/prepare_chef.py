"""Prepare retained painted sources: crop, uniform sampling and padding only."""
from pathlib import Path
import hashlib
import json
import subprocess

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = Path(__file__).resolve().parent
OUT = ROOT / 'assets/opera/worlds/chef_quality_20261019'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
prompts = {row['id']: row for row in json.loads((SRC / 'prompts.json').read_text('utf-8'))}
records = []


def native(name):
    row = prompts[name]
    path = ROOT / row['native_path']
    assert sha(path) == row['native_sha256']
    image = Image.open(path)
    assert image.mode == 'RGBA' and image.getchannel('A').getextrema()[0] == 0
    return path, image


def bounds(image, pad=4):
    box = image.getchannel('A').point(lambda alpha: 255 if alpha >= 16 else 0).getbbox()
    assert box
    return (max(0, box[0] - pad), max(0, box[1] - pad),
            min(image.width, box[2] + pad), min(image.height, box[3] + pad))


def export(name, source, image, size, crop=None, family=None, whole_canvas=False):
    if crop is None:
        if whole_canvas:
            crop = (0, 0, image.width, image.height)
        elif family:
            boxes = [bounds(native(item)[1]) for item in family]
            crop = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                    max(b[2] for b in boxes), max(b[3] for b in boxes))
        else:
            crop = bounds(image)
    cut = image.crop(crop)
    gutter = 0 if whole_canvas else 8
    factor = min((size[0] - gutter * 2) / cut.width,
                 (size[1] - gutter * 2) / cut.height)
    small = cut.resize((round(cut.width * factor), round(cut.height * factor)),
                       Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', size)
    xy = ((size[0] - small.width) // 2, (size[1] - small.height) // 2)
    canvas.alpha_composite(small, xy)
    output = OUT / (name + '.png')
    canvas.save(output, compress_level=9)
    records.append({'id': name, 'source': source.relative_to(ROOT).as_posix(),
                    'source_sha256': sha(source), 'output': output.relative_to(ROOT).as_posix(),
                    'output_sha256': sha(output), 'dimensions': list(size),
                    'source_crop': list(crop), 'uniform_scale': factor,
                    'placement': list(xy), 'whole_source_canvas': whole_canvas,
                    'method': 'Uniform Lanczos downsample, literal source region and transparent padding only; no painting, recolor, warp or rotation.'})
    return canvas, crop, factor, xy


oven_ids = ['oven_cool_raw', 'oven_warm_risen', 'oven_open_risen']
oven_geometry = None
for name, parent in zip(['oven_cool', 'oven_warm', 'oven_open'], oven_ids):
    source, image = native(parent)
    result = export(name, source, image, (512, 512), family=oven_ids)
    if oven_geometry is None:
        _, crop, factor, xy = result
        oven_geometry = {'closed_handle_uv': [(627 - crop[0]) * factor / 512 + xy[0] / 512,
                                               (922 - crop[1]) * factor / 512 + xy[1] / 512]}

for name in ['thermometer_empty', 'thermometer_full']:
    source, image = native(name)
    export(name, source, image, (128, 512), family=['thermometer_empty', 'thermometer_full'])

# Preserve the approved full cup's original256-square coordinate system.
source, image = native('pitcher_empty')
strong = bounds(image, 0)
crop = bounds(image, 4)
factor = min(213 / (strong[2] - strong[0]), 163 / (strong[3] - strong[1]))
offset = np.array([127.5, 127.5]) - np.array([(strong[0] + strong[2]) / 2,
                                           (strong[1] + strong[3]) / 2]) * factor
small = image.crop(crop).resize((round((crop[2] - crop[0]) * factor),
                                round((crop[3] - crop[1]) * factor)), Image.Resampling.LANCZOS)
canvas = Image.new('RGBA', (256, 256))
xy = tuple(round(n) for n in offset + np.array(crop[:2]) * factor)
canvas.alpha_composite(small, xy)
output = OUT / 'pitcher_empty.png'
canvas.save(output, compress_level=9)
records.append({'id': 'pitcher_empty', 'source': source.relative_to(ROOT).as_posix(),
                'source_sha256': sha(source), 'output': output.relative_to(ROOT).as_posix(),
                'output_sha256': sha(output), 'dimensions': [256, 256],
                'source_crop': list(crop), 'uniform_scale': factor,
                'translation': offset.tolist(), 'placement': list(xy),
                'method': 'Uniform registration to measured original alpha16bbox21,46,234,209; no nonuniform fit. Renderer uses generated interior inside the original cup cavity, retaining every original exterior pixel.'})

for name, parent, size in [('chocolate_strawberry', 'chocolate_strawberry_retry', (256, 256)),
                           ('batter_stream', 'batter_stream', (64, 512)),
                           ('batter_drop', 'batter_drop', (64, 64)),
                           ('batter_splash', 'batter_splash', (128, 128)),
                           ('piping_bag', 'piping_bag', (512, 512))]:
    source, image = native(parent)
    export(name, source, image, size)

source, image = native('frosting_segment_retry')
left, top, right, bottom = bounds(image, 0)
side = max(bottom - top + 16, 384)
cy = (top + bottom) // 2
for name, cx in [('frosting_cap_start', left - 4 + side // 2),
                 ('frosting_segment', (left + right) // 2),
                 ('frosting_cap_end', right + 4 - side // 2)]:
    export(name, source, image, (128, 128),
           crop=(cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2))

for name in ['stack_two', 'stack_four']:
    source, image = native(name)
    export(name, source, image, (512, 512), whole_canvas=True)

# Consumer-specific downsampling preserves the approved originals and prevents
# five1024textures accumulating in the small freeplay activity's cache.
for name, filename in [('bowl_empty', 'chef_empty_shell_bowl_v1.png'),
                       ('bowl_unstirred', 'chapter2_chef_batter_unstirred.png'),
                       ('bowl_stirred', 'chapter2_chef_batter_stirred.png'),
                       ('cake_unfrosted', 'chapter2_chef_stacked_unfrosted_cake.png'),
                       ('cake_frosted', 'chapter2_chef_frosted_rainbow_cake.png')]:
    source = ROOT / 'assets/chapter2/birthday' / filename
    export(name, source, Image.open(source).convert('RGBA'), (512, 512), whole_canvas=True)

guide = json.loads((SRC / 'guide_reuse.json').read_text('utf-8'))
assert sha(ROOT / guide['output']) == guide['output_sha256']
records.append({'id': 'guide_hand', **guide})

# Existing deterministic TOP gate still owns the delivered chocolate path.
source = OUT / 'chocolate_strawberry.png'
target = ROOT / 'assets/opera/worlds/widgets/widget_target_chef_piece_2.png'
target.write_bytes(source.read_bytes())
prepared_copy = SRC / 'chocolate_strawberry_prepared.png'
source.replace(prepared_copy)
for row in records:
    if row['id'] == 'chocolate_strawberry':
        row['output'] = prepared_copy.relative_to(ROOT).as_posix()
source = prepared_copy
records.append({'id': 'target_chef_piece_2', 'source': source.relative_to(ROOT).as_posix(),
                'source_sha256': sha(source), 'output': target.relative_to(ROOT).as_posix(),
                'output_sha256': sha(target), 'dimensions': [256, 256],
                'method': 'Exact byte replacement of the commissioned ambiguous chocolate placeholder with the painted dipped strawberry; historic source retained in baseline6fb.'})

bag = next(row for row in records if row['id'] == 'piping_bag')
source, image = native('piping_bag')
arr = np.asarray(image)
mask = ((arr[:, :, 3] > 64) & (arr[:, :, 0] > 140)
        & (arr[:, :, 1] > 70) & (arr[:, :, 1] < 210) & (arr[:, :, 2] < 130))
ys, xs = np.nonzero(mask)
index = np.argmax(ys - xs)
tip = np.array([xs[index], ys[index]])
bag_uv = ((tip - np.array(bag['source_crop'][:2])) * bag['uniform_scale']
          + np.array(bag['placement'])) / 512
stream = Image.open(OUT / 'batter_stream.png')
geometry = {'oven': oven_geometry, 'piping_bag_nozzle_uv': bag_uv.tolist(),
             'piping_bag_outward_direction': [-1, 1],
             'stream_alpha16_bbox': list(bounds(stream, 0)),
             'cup_cavity_native256': [[65, 98], [69, 90], [80, 84], [98, 80],
                                       [123, 78], [148, 82], [165, 89], [175, 99],
                                       [167, 105], [144, 111], [119, 113], [92, 109], [74, 104]],
             'limits': 'Candidate calibration only; actual Mobile/HUD touch/contact/transition review and4.5per applicable dimension required.'}
(SRC / 'geometry.json').write_text(json.dumps(geometry, indent=2) + '\n', encoding='utf-8')
(SRC / 'provenance.json').write_text(json.dumps({'baseline': '6fb96aeb441952c1053cc5ce18435fc57fc1d1ab',
    'provider': 'Available builtin ImageGen, model revision unexposed with owner approval',
    'records': records, 'source_generation_calls': 22,
    'limits': 'Preparation only; no source or runtime acceptance inferred. Protected originals unchanged.'}, indent=2) + '\n', encoding='utf-8')

p = ROOT / 'ASSET_LICENSES.md'
text = p.read_text('utf-8')
for row in records:
    path = row['output']
    if '| `' + path + '` | 2026-10-19' not in text:
        text += '\n| `' + path + '` | 2026-10-19 painted Chef source/derivative | Original source licenses and OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Current SHA256 ' + row['output_sha256'] + '; source hashes and uniform preparation in assets_src/imagegen/job_art_chef_20261019/provenance.json. |'
native_guide = SRC / 'guide_hand_reused_native.png'
if '| `assets_src/imagegen/job_art_chef_20261019/guide_hand_reused_native.png` |' not in text:
    text += '\n| `assets_src/imagegen/job_art_chef_20261019/guide_hand_reused_native.png` | Exact published Teacher ImageGen native, commit e90c0daa | OpenAI output terms | https://openai.com/policies/terms-of-use/ | SHA256 ' + sha(native_guide) + '; exact reuse, no new generation or identity change. |\n'
p.write_text(text, encoding='utf-8')
p = ROOT / 'design/audit_impacts/job-art-chef-20261019.json'
data = json.loads(p.read_text('utf-8'))
data['files'] = sorted(set(data['files'] + ['ASSET_LICENSES.md']
                           + [p.relative_to(ROOT).as_posix() for p in SRC.rglob('*') if p.is_file()]
                           + [row['output'] for row in records]))
p.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'prepared': len(records), 'geometry': geometry}, indent=2))
