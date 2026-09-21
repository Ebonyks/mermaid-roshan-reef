"""Extract original lower bough pixels; prepare concealed fill and editable ORA."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
import hashlib
import io
import json
import zipfile

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as nd

W = Path(__file__).resolve().parents[3]
P = Path(__file__).resolve().parent / 'arrival_boughs'
P.mkdir(exist_ok=True)
source = W / 'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
image = Image.open(source).convert('RGB').crop((0, 0, 512, 720))
pixels = np.array(image)
hsv = np.array(image.convert('HSV'))
seed = np.full((720, 512), cv2.GC_PR_BGD, dtype='uint8')
seed[(hsv[:, :, 0] < 118) & (hsv[:, :, 1] > 60)] = cv2.GC_FGD
seed[(hsv[:, :, 2] < 175) & (hsv[:, :, 1] > 60)] = cv2.GC_PR_FGD
seed[:, 400:] = cv2.GC_BGD
seed[:38, :] = cv2.GC_BGD
seed[(hsv[:, :, 0] > 120) & (hsv[:, :, 2] > 180)] = cv2.GC_BGD
cv2.setRNGSeed(0)
cv2.grabCut(pixels, seed, None, np.zeros((1, 65)), np.zeros((1, 65)), 5, cv2.GC_INIT_WITH_MASK)
mask = nd.binary_fill_holes((seed == cv2.GC_FGD) | (seed == cv2.GC_PR_FGD))

# This lower bough tier is below the menu in the playable arrival view.
# Only a two-pixel contour band can be revealed; broad hidden fill is not an
# accepted clean background plate and must never be exposed independently.
mask = nd.binary_dilation(mask, iterations=3)
healed = cv2.inpaint(pixels, mask.astype('uint8') * 255, 5, cv2.INPAINT_TELEA)
mask = mask[448:704, :512]
native = pixels[448:704, :512]
underpaint = healed[448:704, :512].copy()
# Identical fixed-border overlap prevents minification from exposing a cut edge.
underpaint[:32] = native[:32]
underpaint[224:] = native[224:]
underpaint[:, :8] = native[:, :8]
cutout = np.dstack([native, mask.astype('uint8') * 255])
Image.fromarray(cutout).save(P / 'tip-rest.png')
Image.fromarray(underpaint).save(P / 'tip-underpaint.png')
Image.fromarray(native).save(P / 'tip-original.png')
Image.fromarray(mask.astype('uint8') * 255).save(P / 'tip-mask.png')
y, x = np.indices((256, 512))
groups = np.where((x < 8) | (y < 32) | (y >= 224) | (abs(x - 120) <= 24), 0, np.where(x < 120, 1, 2))
parts = [('fixed_background_and_concealed_fill', Image.fromarray(underpaint).convert('RGBA'))]
for n, name in enumerate(['central_stem_and_lower_tier_fixed', 'left_outer_tips', 'right_outer_tips']):
    part = cutout.copy()
    part[groups != n] = 0
    parts.append((name, Image.fromarray(part)))
merged = Image.new('RGBA', (512, 256))
for _, part in parts:
    merged = Image.alpha_composite(merged, part)
assert np.array_equal(np.array(merged)[:, :, :3], native)
tree = Element('image', w='512', h='256', name='Arrival original boughs', version='0.0.3')
stack = SubElement(tree, 'stack')
with zipfile.ZipFile(P / 'arrival-boughs-editable.ora', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('mimetype', 'image/openraster', compress_type=zipfile.ZIP_STORED)
    for name, part in reversed(parts):
        buffer = io.BytesIO()
        part.save(buffer, format='PNG')
        path = 'data/' + name + '.png'
        archive.writestr(path, buffer.getvalue())
        SubElement(stack, 'layer', name=name, src=path, x='0', y='0', opacity='1.0', visibility='visible', **{'composite-op': 'svg:src-over'})
    archive.writestr('stack.xml', tostring(tree, encoding='utf-8'))
    buffer = io.BytesIO()
    merged.save(buffer, format='PNG')
    archive.writestr('mergedimage.png', buffer.getvalue())
(P / 'SOURCE.json').write_text(json.dumps({
    'source': source.relative_to(W).as_posix(),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'master_rect': [0, 448, 512, 256], 'cv2_version': cv2.__version__, 'rng_seed': 0,
    'method': 'original-pixel extraction; concealed contour-local inpaint only; broad hidden fill is not an accepted plate; direct Aseprite fallback',
    'layers': [name for name, _ in parts], 'frame_count': 3,
    'scope': 'one visible lower bough tier; central trunk, left8 columns and first/last32 rows fixed; this is not full-tree separation',
    'edge_guard': '3 native scene-colour pixels around antialiased edge; bounded 2px motion only; static native edge guard retained below patch to prevent filtered seams',
    'exact_rest_reconstruction': True, 'runtime_accepted': False,
    'limits': 'source candidate; remaining tree/background decomposition and runtime/device review open',
}, indent=2) + '\n')
print('ARRIVAL_BOUGHS|four editable source layers; exact original rest|PASS')
