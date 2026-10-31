"""Normalize registered ImageGen furniture pairs; preserve native PNGs separately."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets_src/castle/studio_furniture_20261015'
DEST = ROOT / 'assets/castle/day_one_art_studio/furniture'
NAMES = ('paint_table', 'left_counter', 'right_counter')


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    for name in NAMES:
        source = SOURCE / (name + '_native.png')
        native = Image.open(source).convert('RGBA')
        cells = [native.crop((i * native.width // 2, 0,
                             (i + 1) * native.width // 2, native.height)) for i in range(2)]
        # Decontaminate generator chroma fringe only at the silhouette. Preserve
        # painted opaque interiors and every native source separately.
        for index, cell in enumerate(cells):
            rgba = np.asarray(cell).copy()
            rgb = rgba[:, :, :3].astype('int16')
            edge = distance_transform_edt(rgba[:, :, 3] > 0) < 4
            chroma = (rgb.max(2)-rgb.min(2) > 120) & (rgb.max(2) > 200) & (rgb.min(2) < 80)
            rgba[:, :, 3][edge & chroma] = 0
            interior = (rgba[:, :, 3] >= 250) & ~chroma
            nearest = distance_transform_edt(~interior, return_distances=False, return_indices=True)
            soft = (rgba[:, :, 3] > 0) & (rgba[:, :, 3] < 250)
            rgba[:, :, :3][soft] = rgba[nearest[0][soft], nearest[1][soft], :3]
            cells[index] = Image.fromarray(rgba)
        # Ignore disconnected sub-alpha generator dust when measuring the object.
        bounds = [Image.fromarray(np.where(np.asarray(c)[:, :, 3] > 96, 255, 0).astype('uint8')).getbbox() for c in cells]
        output = []
        for cell, bbox in zip(cells, bounds):
            crop = cell.crop(bbox)
            crop.thumbnail((480, 480), Image.Resampling.LANCZOS)
            canvas = Image.new('RGBA', (512, 512))
            canvas.alpha_composite(crop, ((512-crop.width)//2, 496-crop.height))
            output.append(canvas)
        # Use one identical silhouette alpha for both states. Dirty paint may
        # change the surface, never the furniture's solid/transparent topology.
        alpha = output[0].getchannel('A')
        output[1].putalpha(alpha)
        common_bbox = alpha.getbbox()
        output = [image.crop(common_bbox) for image in output]
        states = []
        for state, image in zip(('clean', 'dirty'), output):
            target = DEST / f'{name}_{state}.png'
            image.save(target, optimize=True)
            states.append({'path': target.relative_to(ROOT).as_posix(),
                           'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        a, b = [np.asarray(i).astype('int16') for i in output]
        solid = a[:, :, 3] >= 250
        changed = np.max(abs(a[:, :, :3]-b[:, :, :3]), axis=2) > 18
        records.append({'id': name, 'source': source.relative_to(ROOT).as_posix(),
                        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                        'native_size': list(native.size), 'bounds': bounds,
                        'delivery_size': list(output[0].size), 'states': states,
                        'changed_solid_fraction': float(np.mean(changed[solid])),
                        'alpha_identical': bool(np.array_equal(a[:, :, 3], b[:, :, 3]))})
    receipt = {'method': 'Two generated states; bounded silhouette chroma removal and nearest-solid RGB decontamination for partial alpha; per-cell alpha bbox crop, uniform fit 480px, bottom-center registration, shared clean silhouette alpha. No original overwritten.', 'assets': records}
    (SOURCE / 'DELIVERY.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    build()
