"""Review-only color measurements; no asset correction or acceptance threshold."""
from pathlib import Path
import hashlib
import json
import subprocess
import numpy as np
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'project.godot').exists())
SOURCE = OUT.parent / 'lawn_material_v6/imported_review'
old = json.loads((OUT.parent / 'color_review_v3/AUDIT.json').read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stats(im):
    rgb = np.asarray(im.convert('RGB')).reshape(-1, 3).astype(float) / 255
    linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    luminance = linear @ np.array([.2126, .7152, .0722])
    high, low = rgb.max(1), rgb.min(1)
    saturation = np.divide(high-low, high, out=np.zeros_like(high), where=high > 0)
    return {'linear_luminance_p10_p50_p90': np.percentile(luminance, [10,50,90]).round(6).tolist(),
            'HSV_saturation_p10_p50_p90': np.percentile(saturation, [10,50,90]).round(6).tolist(),
            'pixel_count': len(rgb)}

images, sources = {}, []
for i, stage in enumerate(['arrival', 'meadow', 'castle']):
    for mode in ['day', 'night']:
        label = f'canvas_screen_{i+1}_day_p0' if mode == 'day' else f'canvas_screen_3_night_p{i}'
        path = SOURCE / (label + '_lawn1.png')
        images[stage, mode] = Image.open(path).convert('RGB')
        assert images[stage, mode].size == (1280, 720)
        sources.append({'stage': stage, 'mode': mode, 'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)})

samples = []
board = Image.new('RGB', (1080, 24 * 116), '#20343e')
draw = ImageDraw.Draw(board)
for i, row in enumerate(old['samples']):
    item = {key: row[key] for key in ['stage', 'material', 'sample_id', 'rect_xyxy']}
    x, y = (i // 24) * 540, (i % 24) * 116
    draw.text((x+5, y+3), row['stage'] + ' / ' + row['material'], fill='white')
    for j, mode in enumerate(['day', 'night']):
        crop = images[row['stage'], mode].crop(row['rect_xyxy'])
        item[mode] = stats(crop)
        board.paste(crop.resize((115, 70)), (x+5+j*265, y+23))
        st = item[mode]
        draw.text((x+126+j*265,y+28), f"{mode}\nL {st['linear_luminance_p10_p50_p90'][1]:.3f}\nS {st['HSV_saturation_p10_p50_p90'][1]:.3f}", fill='white')
    samples.append(item)
board.save(OUT / 'material-samples.jpg', quality=94)

findings = old['findings']
updates = [
    'Still open. Pointed berry replacements improve family consistency, but broad highlights and dark foreground masses still differ from the fine rear hedge. Use material-local corrections; no global foreground desaturation.',
    'Night-only leaf shadow lift is integrated across 63 owners. Current captures still show compressed interior detail; integration is not visual acceptance. Preserve dark roots and depth gaps.',
    'Four bounded whole-lawn material atlases are integrated, four cels each. Two misclassified castle leaf/rock fragments are held at rest. Yellow-green lawn intensity remains a priority; whole-material deformation is not independent blade drawing.',
    'Cream, pink and purple remain identity accents. Review bright repeated flower groups and supporting leaf ownership before grading; do not make all flowers equally intense.',
    'High-cloud cels and signed cloud-sea motion are integrated. Retain pale cool mountain depth; cloud pose shadows and drift extremes still need live review.',
    'Water and shoreline contrast remain readable in these stills. Ripple peak/fade and full water-cycle composite audit remain open.',
    'Paths, left castle approach and warm bridge remain distinguishable. Preserve those palettes and clearances; no global route grade justified.',
    'Separate cyan-window night material is integrated. Retain purple architecture, warm gold and protected portrait. Glass is more legible; full night appearance remains unaccepted.',
    'Aqua playground props belong to a different material family than foliage. Preserve that distinction; inspect contact and shadow consistency in motion.',
    'Protected actor and portrait colors remain unchanged. Bright actor/HUD separation at night is intentional; animal/cue event peaks and target-device presentation remain open.'
]
for item, decision in zip(findings, updates):
    item['decision'] = decision

runtime = ROOT / 'assets/sprites/sky_lagoon/whole_scene_v2'
report = {
    'status': 'COLOR_AUDIT_OPEN_NOT_ACCEPTED',
    'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'candidate': 'dirty lawn_material_v6 and castle_fragments_v6; exact capture and runtime hashes below',
    'owner_score': 3.5, 'new_score': None,
    'scope': {'rendered_views': 6, 'material_locations': len(samples), 'material_families': len(findings)},
    'method': 'Unmasked fixed scene rectangles; linear Rec709 luminance and HSV saturation distributions. Mixed materials, species, highlights and shadow coverage prevent direct equal-intensity targets. Source measurements are diagnostics, not acceptance.',
    'sources': sources, 'samples': samples, 'findings': findings,
    'runtime_hashes': {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(runtime.glob('*')) if p.suffix in ['.png', '.json']},
    'visual_review': 'Agent inspected current six-view day/night full-scene comparisons. Lawn/foliage intensity and night detail remain open; no new quality score assigned.',
    'correction_order': ['Lawn yellow highlight intensity against adjoining hedge', 'Large foreground leaf highlight width and hue by botanical family', 'Night-only leaf detail while retaining root shadows', 'Flower accent repetition and supporting plant ownership', 'Cloud/water/event temporal color continuity'],
    'limits': ['Six frozen poses do not cover all animation or interaction states.', 'Current source temporal audit from color_review_v3 is historical and is not rerun here.', 'No color edits are performed by this report.', 'Device, child and owner acceptance remain open.']
}
(OUT / 'AUDIT.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report['scope']))
