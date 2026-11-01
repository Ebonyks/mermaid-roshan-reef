"""Add uncovered Canvas garment cells, preserving all seed geometry and weights."""
from pathlib import Path
import json
import numpy as np
from scipy.spatial import cKDTree

P = Path(__file__).resolve().parents[1]
r = json.loads((P/'fixtures/seed_scripts/rig.json').read_text())
for mesh in r['meshes']:
    mesh['texture'] = mesh['texture'].replace('../../../native_rig_stress_20261031/art/','../fixtures/seed_art/')
(P/'godot/seed_rig.json').write_text(json.dumps(r,separators=(',',':')))
m = r['meshes'][0]
v = np.array(m['vertices']); w = np.array(list(m['weights'].values())).T
lookup = {tuple(x):i for i,x in enumerate(v)}
cells = {}
for t in m['triangles']:
    q = v[t]; cell = (int(q[:,0].min()),int(q[:,1].min()))
    assert np.all(np.ptp(q,axis=0)==[6,6]), 'Unexpected seed triangle, do not overlap it'
    cells.setdefault(cell,[]).append(t)
points = v.tolist(); weights = w.tolist(); tree = cKDTree(v)
for y in range(78,931,6):
    for x in range(204,793,6):
        if (x,y) not in lookup:
            dist, ix = tree.query([x,y], k=4)
            iw = 1/np.maximum(dist,1e-5)**2; iw /= iw.sum()
            new = (w[ix]*iw[:,None]).sum(axis=0); new /= new.sum()
            lookup[(x,y)] = len(points); points.append([x,y]); weights.append(new.tolist())
extra = []
for y in range(78,925,6):
    for x in range(204,787,6):
        ids = [lookup[(x,y)],lookup[(x+6,y)],lookup[(x,y+6)],lookup[(x+6,y+6)]]
        prior = cells.get((x,y),[])
        if len(prior)==2:
            continue
        if len(prior)==1:
            missing = next(i for i in ids if i not in set(prior[0]))
            diagonal = next((a,b) for a in prior[0] for b in prior[0]
                if a<b and abs(points[a][0]-points[b][0])==6 and abs(points[a][1]-points[b][1])==6)
            tri = [missing,*diagonal]; q = np.array([points[i] for i in tri])
            a,b = q[1]-q[0],q[2]-q[0]
            extra.append(tri if a[0]*b[1]-a[1]*b[0]>0 else [tri[0],tri[2],tri[1]])
        else:
            extra.extend([[ids[0],ids[1],ids[3]],[ids[0],ids[3],ids[2]]])
used = sorted({i for t in extra for i in t}); remap = {old:new for new,old in enumerate(used)}
wa = np.array(weights)
r['meshes'].append(dict(name='GarmentExtension',texture='../art/blank.png',z=m['z'],
    vertices=[points[i] for i in used],triangles=[[remap[i] for i in t] for t in extra],
    weights={name:wa[used,k].tolist() for k,name in enumerate(m['weights'])}))
(P/'godot/rig.json').write_text(json.dumps(r,separators=(',',':')))
(P/'evidence/mesh_extension.json').write_text(json.dumps(dict(
    reason='The complete astronaut hem extends outside the seed carrier. Fill only uncovered six-pixel triangle cells.',
    existing_body_vertices_weights_triangles='UNCHANGED',new_mesh='GarmentExtension',
    vertices=len(used),triangles=len(extra),
    interpolation='Four nearest seed field values, inverse-distance blend at additional coordinates; exact copied weights at every common coordinate.',
    overlap='Original triangles stay intact; only the missing half-cell or completely uncovered cells are added.',
    skin_slot_rule='Only new painter/astronaut clothing and neck pixels. Blank for all other slots; no original outfit underlay.'
),indent=2)+'\n')
print('GARMENT EXTENSION',len(used),'vertices',len(extra),'triangles; seed geometry unchanged')
