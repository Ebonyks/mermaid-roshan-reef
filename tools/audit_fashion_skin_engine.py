"""Fail closed on frame/identity regressions in the authored skin catalog.
Metrics are not human art, animation, device or child acceptance.
"""
import hashlib,json,argparse
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(p):return np.array(Image.open(p).convert('RGBA'))
def run():
 record=ROOT/'assets_src/fashion_designer/skin_engine_v2/derivations.json'
 data=json.loads(record.read_text(encoding='utf-8'));checks=[]
 for key,spec in data['families'].items():
  original=ROOT/spec['source'];assert digest(original)==spec['source_sha256'],key
  base=ROOT/spec.get('pixel_source',spec['source']).removeprefix('res://')
  src=image(base);h,w,_=src.shape
  assert [w,h]==spec['dimensions'],key
  cw,ch=map(int,spec['cell']);cols=w//cw
  mask=np.zeros((h,w),dtype=bool)
  for i,b in enumerate(spec['boxes']):
   x,y=i%cols*cw,i//cols*ch;x0,y0,x1,y1=map(int,b)
   assert 0<=x0<x1<=cw and 0<=y0<y1<=ch,(key,i,b)
   mask[y+y0:y+y1,x+x0:x+x1]=True
  for bounds in spec.get('protected_boxes',[]):
   x0,y0,x1,y1=map(int,bounds);mask[y0:y1,x0:x1]=False
  for kind,path in spec['variants'].items():
   if kind=='original':continue
   out=ROOT/path.removeprefix('res://');dst=image(out)
   assert dst.shape==src.shape,(key,kind,'dimensions')
   assert np.array_equal(dst[:,:,3],src[:,:,3]),(key,kind,'alpha')
   assert np.array_equal(dst[~mask],src[~mask]),(key,kind,'identity/hand/outside-clothing')
   assert np.any(dst!=src),(key,kind,'no visible garment')
   checks.append({'family':key,'kind':kind,'path':path.removeprefix('res://'),'sha256':digest(out),'pixel_baseline':base.relative_to(ROOT).as_posix(),'dimensions_and_alpha':'PASS','protected_identity_pixels':'PASS','changed_clothing_pixels':int(np.any(dst!=src,axis=2).sum())})
 assert len(checks)==55
 for p in (ROOT/'assets/fashion/skin_engine_v2').rglob('*.png'):
  w,h=Image.open(p).size
  assert max(w,h)<=1024 or (w&(w-1)==0 and h&(h-1)==0),p
 result={'schema':'reef.fashion_skin_identity/2','status':'PASS','checks':checks,'derivations_sha256':digest(record),'daddy_source_exception':'Original WEBP and PNG preserved. Daddy compares with separately registered clean PNG-master derivative; corrupt WEBP alpha is not claimed identical.','human_pose_style_motion':'PENDING; these metrics do not accept art or animation','device_child_owner':'PENDING'}
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args();result=run()
 if args.record:(ROOT/'assets_src/fashion_designer/skin_engine_v2/identity_geometry_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
 print('FASHION_SKIN_AUDIT|ALL OK|55 complete variant atlases; dimensions, alpha, outside-clothing and protected hand pixels match declared baselines')
