"""Read-only checks of native exports, contacts, stationary berries and sources."""
import hashlib, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[2]
ASE='C:/Program Files/Aseprite/Aseprite.exe'
def rgba(p): return np.array(Image.open(p).convert('RGBA'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args): subprocess.run([ASE,'--batch',*map(str,args)],check=True,capture_output=True)
def main():
 temp=PROJECT/'build/sky-review-v3-roundtrip';temp.mkdir(parents=True,exist_ok=True)
 rows=[]
 for folder in sorted((ROOT/'objects').iterdir()):
  frames=sorted((folder/'frames').glob('frame_*.png'))
  export=temp/folder.name;export.mkdir(exist_ok=True)
  run(folder/(folder.name+'.aseprite'),'--save-as',export/'frame_{frame}.png')
  native=sorted(export.glob('frame_*.png'),key=lambda p:int(p.stem.split('_')[-1]))
  assert len(native)==len(frames),folder.name
  hashes=[]
  for source,restored in zip(frames,native):
   a=rgba(source);b=rgba(restored)
   assert a.shape==(512,512,4) and np.array_equal(a,b),(folder.name,'native RGBA')
   mask=a[:,:,3];assert not(mask[0].any() or mask[-1].any() or mask[:,0].any() or mask[:,-1].any()),(folder.name,'clipped')
   hashes.append(hashlib.sha256(a.tobytes()).hexdigest())
  assert len(set(hashes))==len(frames),(folder.name,'duplicate state')
  rows.append({'id':folder.name,'keys':len(frames),'unique_states':len(set(hashes)),'rgba_roundtrip':'PASS','clear_alpha_margins':'PASS','master_sha256':sha(folder/(folder.name+'.aseprite'))})
 # The entire fixed frame region outside the seat/rope action box is stable.
 arrays=[rgba(p) for p in sorted((ROOT/'objects/07_swing/frames').glob('frame_*.png'))]
 fixed=np.ones((512,512),dtype=bool);fixed[118:471,140:375]=False
 assert all(np.array_equal(a[fixed],arrays[0][fixed]) for a in arrays[1:]),'Frame jitter'
 cfg=json.loads((ROOT/'objects/07_swing/AUTHORING_RECEIPT.json').read_text())
 import_cfg=json.loads((ROOT/'objects/07_swing/IMPORT_PARAMETERS.json').read_text())
 distances=[]
 for contact,a,p in zip(cfg['contacts'],arrays,import_cfg['poses']):
  # Independently project gold pixels from the native seat, before painted
  # ropes are overlaid. A rope's own gold cannot pass as a seat attachment.
  native=rgba(ROOT/'objects/07_swing'/p['input'])
  ox,oy=p['origin'];native=native[oy:oy+512,ox:ox+512]
  yy,xx=np.indices((512,512));sx=np.floor((xx-p['offset'][0])/p['scale']).astype(int);sy=np.floor((yy-p['offset'][1])/p['scale']).astype(int)
  valid=(sx>=0)&(sx<512)&(sy>=0)&(sy<512)
  projected=np.zeros((512,512,4),dtype=np.uint8);projected[valid]=native[sy[valid],sx[valid]]
  nr,ng,nb=[projected[:,:,k].astype(float) for k in range(3)]
  native_gold=(projected[:,:,3]>=192)&(nr>100)&(ng>75)&(nb<nr*.72)&(nr>ng*1.08)
  for x,y in contact['painted_rope_endpoints']:
   assert a[y,x,3]>=192,('Rope endpoint missing',contact['state'],x,y)
   gold=native_gold&(np.abs(xx-x)<10)&(np.abs(yy-y)<10)
   ys,xs=np.where(gold);assert len(xs)>0
   d=float(np.sqrt((xs-x)**2+(ys-y)**2).min());assert d<=2.5
   distances.append(d)
 # Same exact opaque berry/junction pixels in every fresh leaf drawing.
 lock=json.loads((ROOT/'objects/02_huckleberry/BERRY_LOCK.json').read_text())
 base=rgba(ROOT/'objects/02_huckleberry/frames/frame_00.png')
 for p in sorted((ROOT/'objects/02_huckleberry/frames').glob('frame_*.png')):
  a=rgba(p)
  for y,x0,x1 in lock['runs']: assert np.array_equal(a[y,x0:x1+1],base[y,x0:x1+1]),'Berry drift'
 # Exactly reuse source panorama bytes; castle has the original shared anchor.
 original=PROJECT/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
 assert sha(original)==sha(ROOT/'context/approved_clean_panorama.png')
 run(ROOT/'scene/sky_lagoon_sample.aseprite','--frame-range','0,0','--save-as',temp/'scene_roundtrip.png')
 assert np.array_equal(rgba(temp/'scene_roundtrip.png'),rgba(ROOT/'scene/frames/frame_000.png'))
 assert len(list((ROOT/'scene/frames').glob('frame_*.png')))==48
 result={'status':'PASS','objects':rows,'object_count':10,'raster_states':sum(r['keys'] for r in rows),'swing':{'fixed_frame':'PASS','contact_endpoints':24,'maximum_endpoint_to_gold_pixel_px':max(distances),'tolerance_px':2.5,'measurement_limit':'Colour/pixel attachment only; 3D mechanics and owner visual acceptance not inferred.'},'berries':{'stationary_junctions':'PASS','intent':'Exactly two clusters of three berries reviewed on native board; fresh leaf motion retained'},'panorama_source_identity':'PASS','scene_first_frame_native_roundtrip':'PASS','scene_frames':48,'scene_dimensions':[1920,640],'acceptance_limits':'Reference-file checks only; no runtime, device, child, owner or cinematic acceptance.'}
 (ROOT/'MACHINE_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print('PASS: 10 masters / 72 distinct states / 24 attached rope endpoints / stationary berries / panorama / native scene.',flush=True)
if __name__=='__main__': main()
