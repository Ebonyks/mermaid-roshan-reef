"""Check actual native captures against preserved source-study floors."""
from pathlib import Path
import importlib.util
import json
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
helper = HERE.parent / 'tools/seed_audit.py'
spec = importlib.util.spec_from_file_location('seed', helper)
seed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)
rig = json.loads((HERE/'view_binding.json').read_text())
samples = json.loads((HERE/'samples.json').read_text())
mesh = rig['meshes'][0]
points, triangles = np.array(mesh['vertices']), np.array(mesh['triangles'])
weights = mesh['weights']
inverse = np.array([np.linalg.inv(seed.affine(samples[0]['bones'][n])) for n in weights])
alpha = np.array(Image.open(HERE/'approved_swim_atlas.png').crop((512,512,768,768)))[:,:,3]
centers = points[triangles].mean(1).astype(int)
visible = alpha[np.clip(centers[:,1],0,255),np.clip(centers[:,0],0,255)] > 192
low, high, flips = 1., 1., 0
bad = []
for row in samples:
    _, determinant, strain = seed.geometry(points, triangles, weights, inverse, row)
    a, b = float(strain[visible].min()), float(strain[visible].max())
    f = int((determinant[visible] <= 0).sum())
    low, high, flips = min(low,a), max(high,b), flips+f
    if a < .8 or b > 1.2 or f:
        bad.append(row['index'])
reference = seed.pixel_checks(Image.open(HERE/'rgba/0000.png').convert('RGBA'))
alpha_bad = []
for row in samples:
    value = seed.pixel_checks(Image.open(HERE/f"rgba/{row['index']:04d}.png").convert('RGBA'))
    if not seed.seam_pass(value, reference):
        alpha_bad.append({'frame':row['index'], **value})
motion = {}
for name in samples[0]['bones']:
    a = np.unwrap([np.arctan2(x['bones'][name][1],x['bones'][name][0]) for x in samples])
    speed = np.diff(a)*30*180/np.pi
    acceleration = np.diff(speed)*30
    motion[name] = {'speed':float(abs(speed).max()), 'acceleration':float(abs(acceleration).max()),
                    'pass':bool(abs(speed).max() <= 140 and abs(acceleration).max() <= 650)}
report = {'frames':len(samples), 'min_visible_strain':low, 'max_visible_strain':high,
          'flipped_visible_triangles':flips, 'geometry_failed_frames':bad,
          'alpha_reference':reference, 'alpha_failed_frames':alpha_bad, 'motion':motion,
          'root_rotation_zero':all(x['actor_rotation'] == 0 for x in samples),
          'constant_scale':all(x['scale'] == samples[0]['scale'] for x in samples),
          'original_floors':{'strain':[.8,1.2], 'flips':0, 'speed':140, 'acceleration':650},
          'acceptance':'SOURCE_ONLY; geometry, causal-motion ablation and silhouette do not establish acting or fluid-dynamics acceptance'}
(HERE/'inspection.json').write_text(json.dumps(report,indent=2)+'\n')
print('Frames',len(samples),'geometry failures',len(bad),'alpha failures',len(alpha_bad),
      'motion failures',[n for n,v in motion.items() if not v['pass']])
