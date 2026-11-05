from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[1]
rig=json.loads((R/'seed/rig.json').read_text());
for m in rig['meshes']:m['texture']='art/'+{'Body':'body.png','UpperArm':'upper_arm.png','Forearm':'forearm.png','Headwear':'ballet_head.png'}[m['name']]
old=rig['meshes'][0];support=np.zeros((1024,1024),dtype=bool)
for p in (R/'demo/art').glob('*_composed.png'):support|=np.asarray(Image.open(p).convert('RGBA'))[:,:,3]>0
support|=np.asarray(Image.open(R/'demo/art/body.png'))[:,:,3]>0
support=maximum_filter(support,size=27)
axis=np.r_[np.arange(0,1024,6),1024];width=len(axis);pts=np.array([(x,y) for y in axis for x in axis]);tris=[]
for row in range(width-1):
 for col in range(width-1):
  a=row*width+col;b=a+1;c=a+width;d=c+1
  for tri in [(a,b,d),(a,d,c)]:
   q=pts[list(tri)];samples=np.vstack([q,q.mean(axis=0),(.5*q+.5*np.roll(q,1,axis=0))]).astype(int).clip(0,1023)
   if support[samples[:,1],samples[:,0]].any():tris.append(tri)
lookup={tuple(v):i for i,v in enumerate(pts)};oldglobal=[lookup[tuple(v)] for v in old['vertices']];tris=list(dict.fromkeys(tris+[tuple(oldglobal[k] for k in tri) for tri in old['triangles']]))
used=np.unique(np.array(tris));points=pts[used];remap=np.full(len(pts),-1);remap[used]=np.arange(len(used));triangles=remap[np.array(tris)]
old_points=np.array(old['vertices']);tree=cKDTree(old_points);d,near=tree.query(points,k=4);blend=1/np.maximum(d,.00001)**2;blend/=blend.sum(axis=1,keepdims=True);index={tuple(v):i for i,v in enumerate(old['vertices'])};weights={}
for name,v in old['weights'].items():
 arr=(np.array(v)[near]*blend).sum(axis=1)
 for j,p in enumerate(points):
  if tuple(p) in index:arr[j]=v[index[tuple(p)]]
 weights[name]=arr.tolist()
rig['meshes'][0]=dict(old,vertices=points.tolist(),triangles=triangles.tolist(),weights=weights)
(R/'demo/rig.json').write_text(json.dumps(rig,separators=(',',':'))+'\n')
checks={'seed_bones_exact':rig['bones']==json.loads((R/'seed/rig.json').read_text())['bones'],'original_vertices_retained':len(set(index)&set(map(tuple,points)))==len(index),'common_weights_exact':all(all(weights[n][j]==old['weights'][n][index[tuple(p)]] for n in weights) for j,p in enumerate(points) if tuple(p) in index)}
(R/'evidence/mesh_derivation.json').write_text(json.dumps({'checks':checks,'old_vertices':len(old_points),'new_vertices':len(points),'method':'Expanded support grid only. Old common vertices/weights remain exact; new vertices interpolate four nearest old weights. Bone topology/rest immutable.'},indent=2)+'\n');print(checks)
