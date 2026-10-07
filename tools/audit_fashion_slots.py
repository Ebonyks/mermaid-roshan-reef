"""Read-only slot-layer geometry/source gate. Does not accept visual fit or device behavior."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run():
 record=ROOT/'assets_src/fashion_designer/slots_v1/derivations.json'
 data=json.loads(record.read_text(encoding='utf-8'));catalog=data['catalog'];checks=[]
 old=json.loads((ROOT/'assets_src/fashion_designer/skin_engine_v2/derivations.json').read_text(encoding='utf-8'))['families']
 for e in data['outputs']:
  path=ROOT/e['path'].removeprefix('res://');source=ROOT/e['source'].removeprefix('res://')
  assert sha(path)==e['sha256'] and sha(source)==e['source_sha256'],('hash',e['path'])
  spec=old[e['family']];src=np.array(Image.open(source).convert('RGBA'));layer=np.array(Image.open(path).convert('RGBA'))
  assert src.shape==layer.shape,('geometry',path)
  cw,ch=map(int,spec['cell']);cols=src.shape[1]//cw;mask=np.zeros(src.shape[:2],bool);count=0
  for i,b in enumerate(e['fit']):
   x0,y0,x1,y1=map(int,b);assert 0<=x0<x1<=cw and 0<=y0<y1<=ch,(e['family'],e['item_id'],i,b)
   x=i%cols*cw;y=i//cols*ch;mask[y+y0:y+y1,x+x0:x+x1]=True
   assert np.any(layer[y+y0:y+y1,x+x0:x+x1,3]),('empty fitted cell',e['family'],e['item_id'],i)
   count+=1
  assert not np.any(layer[~mask,3]),('outside slot',path)
  for b in spec.get('protected_boxes',[]):
   x0,y0,x1,y1=map(int,b);assert not np.any(layer[y0:y1,x0:x1,3]),('protected hand',path)
  if e['slot']!='head':
   active=layer[:,:,3]>0
   assert np.all(layer[:,:,3][active]==255) and np.all(src[:,:,3][active]==255),('source contour alpha',path)
  checks.append({'family':e['family'],'item':e['item_id'],'slot':e['slot'],'cells':count,'painted_pixels':int((layer[:,:,3]>0).sum()),'sha256':e['sha256']})
 assert len(checks)==260 and len(catalog['items'])==22
 for path in (ROOT/'assets/fashion/slots_v1').rglob('*.png'):
  w,h=Image.open(path).size;assert max(w,h)<=1024 or (w&(w-1)==0 and h&(h-1)==0),path
 return {'schema':1,'status':'PASS','checks':checks,'cells_checked':sum(e['cells'] for e in checks),'layer_count':len(checks),'items':len(catalog['items']),'derivations_sha256':sha(record),'human_identity_fit_motion_device_child_owner':'PENDING'}
if __name__=='__main__':
 result=run();print('FASHION_SLOTS_AUDIT|ALL OK|',result['layer_count'],'layers;',result['cells_checked'],'slot/cell checks')
 (ROOT/'assets_src/fashion_designer/slots_v1/geometry_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
