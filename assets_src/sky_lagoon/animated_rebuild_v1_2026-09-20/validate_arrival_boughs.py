"""Verify source ownership, fixed seams and independently reopened ORA layers."""
from pathlib import Path
import hashlib
import io
import json
import zipfile
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image

W = Path(__file__).resolve().parents[3]
P = Path(__file__).resolve().parent / 'arrival_boughs'
source = json.loads((P / 'SOURCE.json').read_text())
native_path = W / source['source']
assert hashlib.sha256(native_path.read_bytes()).hexdigest() == source['source_sha256']
original = Image.open(native_path).convert('RGBA').crop((0, 448, 512, 704))
atlas = Image.open(P / 'tip-atlas.png').convert('RGBA')
assert atlas.size == (1024, 512)
metadata = json.loads((P / 'tip-atlas.json').read_text())
assert len(metadata['frames']) == 3
assert all(row['duration'] == 500 and not row['trimmed'] for row in metadata['frames'].values())
rest = np.array(Image.open(P / 'tip-rest.png').convert('RGBA'))
under = Image.open(P / 'tip-underpaint.png').convert('RGBA')
y, x = np.indices((256, 512))
fixed = (x < 8) | (y < 32) | (y >= 224) | (abs(x - 120) <= 24)
original_array = np.array(original)
rows = []
board = Image.new('RGB', (1536, 512))
for index in range(3):
    cel = atlas.crop(((index % 2) * 512, (index // 2) * 256, (index % 2 + 1) * 512, (index // 2 + 1) * 256))
    pixels = np.array(cel)
    assert np.array_equal(pixels[fixed, 3], rest[fixed, 3])
    visible_fixed = fixed & (rest[:, :, 3] > 0)
    assert np.array_equal(pixels[visible_fixed], rest[visible_fixed])
    composite = Image.alpha_composite(under, cel)
    frame = np.array(composite)
    if index == 0:
        assert np.array_equal(frame, original_array)
    assert np.array_equal(frame[224:], original_array[224:])
    assert np.array_equal(frame[:32], original_array[:32])
    assert np.array_equal(frame[:, :8], original_array[:, :8])
    delta = np.abs(frame[:, :, :3].astype(float) - original_array[:, :, :3]).max(axis=2)
    board.paste(composite.convert('RGB'), (index * 512, 0))
    heat = np.zeros((256, 512, 3), dtype='uint8')
    heat[:, :, 0] = np.minimum(255, delta * 4)
    board.paste(Image.fromarray(heat), (index * 512, 256))
    rows.append({'frame': index, 'rgba_sha256': hashlib.sha256(pixels.tobytes()).hexdigest(), 'fixed_stem_and_patch_seams_exact': True})
assert len({row['rgba_sha256'] for row in rows}) == 3
with zipfile.ZipFile(P / 'arrival-boughs-editable.ora') as archive:
    stack = ET.fromstring(archive.read('stack.xml')).find('stack')
    assert len(stack) == 4
    result = Image.new('RGBA', (512, 256))
    for layer in reversed(list(stack)):
        result = Image.alpha_composite(result, Image.open(io.BytesIO(archive.read(layer.attrib['src']))).convert('RGBA'))
    assert np.array_equal(np.array(result), original_array)
board.save(P / 'three-cel-review.jpg', quality=97)
# The prepared tile owns no duplicate painted bough pixels in the preview.
tile_path = W / 'assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c0.png'
tile = Image.open(tile_path).convert('RGBA')
assert np.array_equal(np.array(tile.crop((0, 448, 512, 704))), original_array)
tile.paste(under, (0, 448))
tile.save(P / 'arrival-base-with-tips-removed.png')
(P / 'VALIDATION.json').write_text(json.dumps({
    'frames': rows, 'cell_size': [512, 256], 'atlas_size': [1024, 512],
    'frame_ms': 500, 'ora_layers': 4, 'ora_reopened_reconstruction_exact': True,
    'rest_scene_exact': True, 'top_and_bottom_patch_seams_exact_all_frames': True,
    'original_tile': tile_path.relative_to(W).as_posix(),
    'original_tile_sha256': hashlib.sha256(tile_path.read_bytes()).hexdigest(),
    'status': 'source candidate; Mobile/runtime and device review pending',
    'limits': 'one visible lower bough tier only; no full-tree separation or 4.9 claim',
}, indent=2) + '\n')
print('ARRIVAL_BOUGHS|three distinct cels; fixed stem/seams; ORA exact; original tile bound|PASS')
