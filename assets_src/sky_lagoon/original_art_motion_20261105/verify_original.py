"""Fail-closed checks for original-v5 appearance, timing, roots and native playback."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageFilter

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
MASTER=ROOT/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
EXPECTED='017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rgb(p):return np.asarray(Image.open(p).convert('RGB'))
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def verify():
 assert sha(MASTER)==EXPECTED,'Original master changed'
 original=Image.open(MASTER).convert('RGBA')
 configs=json.loads((P/'demo_project/targets.json').read_text(encoding='utf-8'))
 assert len(configs)==3
 assert {(c['id'],tuple(c['xy'])) for c in configs}=={('lake_foxtails',(5632,1344)),('meadow_spikes',(2400,900)),('arrival_bells',(1520,1000))},'Unexpected target/placement'
 assert all(0<c['amplitude']<=2.25 for c in configs),'Excessive motion requested'
 assert {x.name for x in (P/'sources').glob('*.png')}=={c['id']+'.png' for c in configs},'Unexpected appearance input'
 base=Image.new('RGBA',original.size)
 for row in range(2):
  for col in range(6):
   tile=Image.open(P/f'demo_project/background/{row}_{col}.png').convert('RGBA')
   assert tile.size==(1024,1024)
   base.paste(tile,(col*1024,row*1024))
 reconstructed=base.copy();master_data=np.asarray(original)
 all_frames=0;roundtrip=0;results=[]
 for c in configs:
  name=c['id'];x,y=c['xy'];box=(x,y,x+512,y+512)
  source=Image.open(P/f'sources/{name}.png').convert('RGB')
  assert np.array_equal(np.asarray(source),np.asarray(original.crop(box).convert('RGB'))),'Appearance crop differs'
  assert sha(P/f'sources/{name}.png')==sha(P/f'demo_project/patches/{name}.png'),'Runtime appearance differs from exact source crop'
  assert sha(P/f'fields/{name}.png')==sha(P/f'demo_project/patches/{name}_field.png')
  field=np.asarray(Image.open(P/f'fields/{name}.png').convert('L'))
  assert not field[0].any() and not field[-1].any() and not field[:,0].any() and not field[:,-1].any()
  assert not field[max(0,min(512,c['root']-y)):].any(),'Root support field must be zero'
  reconstructed.paste(source,(x,y))
  raw=np.asarray(source)
  for i in range(60):
   f=rgb(P/f'frames/{name}/{i:03d}.png')
   assert not np.any(f[field==0]!=raw[field==0]),(name,i,'fixed source changed')
   assert np.array_equal(f,rgb(P/f'roundtrip/{name}/{i:03d}.png')),(name,i,'Aseprite roundtrip differs')
   all_frames+=1;roundtrip+=1
  assert np.array_equal(raw,rgb(P/f'frames/{name}/000.png'))
  decoded=[];duration=[]
  with Image.open(P/f'{name}.gif') as gif:
   assert gif.n_frames==60
   for i in range(gif.n_frames):
    gif.seek(i);f=np.asarray(gif.convert('RGB'));decoded.append(f.copy());duration.append(gif.info.get('duration',0))
  assert duration==[30,30,40]*20 and sum(duration)==2000,'GIF timing differs from60frames/2000ms30fps schedule'
  assert all(np.array_equal(f[field==0],decoded[0][field==0]) for f in decoded),'GIF fixed pixels shimmer'
  results.append({'id':name,'gif_frames':60,'gif_duration_ms':2000,'gif_distinct_images':len({hashlib.sha256(f.tobytes()).hexdigest() for f in decoded}),'aseprite_roundtrip_frames':60,'fixed_source_and_roots_exact':True})
 assert np.array_equal(np.asarray(reconstructed),master_data),'Rest reconstruction differs from original'
 for name in ['original-flowers-closeup.gif','original-lagoon-fixed.gif']:
  with Image.open(P/name) as gif:
   duration=[]
   for i in range(gif.n_frames):gif.seek(i);duration.append(gif.info.get('duration',0))
   assert gif.n_frames==60 and sum(duration)==2000,(name,gif.n_frames,sum(duration))
 mobile=json.loads((P/'evidence/mobile-verification.json').read_text(encoding='utf-8'))
 assert mobile['renderer']=='mobile' and not mobile['errors']
 for name,digest in mobile['input_hashes'].items():assert sha(P/'demo_project'/name.removeprefix('res://'))==digest,('Stale native evidence',name)
 master_receipt=json.loads((P/'evidence/aseprite-roundtrip-receipt.json').read_text(encoding='utf-8'))
 for name,digest in master_receipt['masters'].items():assert sha(P/name)==digest,('Master changed after round-trip',name)
 assert mobile['engine']['major']==4 and mobile['engine']['minor']==7 and mobile['engine']['patch']==2 and mobile['engine']['status']=='stable'
 captures=[rgb(P/f'evidence/capture_frames/{i:03d}.png') for i in range(60)]
 rest=captures[0];h,w=rest.shape[:2]
 control=rgb(P/'evidence/mobile-pristine-control.png')
 delta=np.abs(rest.astype(int)-control.astype(int))
 # GPU local-vs-world texture coordinates can round to adjacent RGB codes.
 assert delta.max()<=2,('Original GPU comparison',int(delta.max()),int((delta.max(axis=2)>2).sum()))
 mask=Image.new('L',(6144,2048))
 for c in configs:mask.paste(Image.open(P/f'fields/{c["id"]}.png'),tuple(c['xy']))
 factor=w/6144;scene_h=2048*factor
 top=(h-scene_h)*.5+16*(w/1280)
 small=mask.resize((w,math.ceil(scene_h)),Image.Resampling.BILINEAR).filter(ImageFilter.MaxFilter(9))
 full=Image.new('L',(w,h));full.paste(small,(0,math.floor(top)))
 allowed=np.asarray(full)>0
 changed=np.logical_or.reduce([np.any(f!=rest,axis=2) for f in captures])
 assert not changed[~allowed].any(),('Fixed GPU scenery moved',int(changed[~allowed].sum()))
 native={'actual_mobile_frames':60,'capture_size':[w,h],'stage_transform_physical':{'scale':factor,'top':top},'changed_pixels_union':int(changed.sum()),'fixed_pixels_every_frame':int((~allowed).sum()),'fixed_pixels_unchanged':True,'pristine_control_max_rgb_error':int(delta.max()),'pristine_control_mean_rgb_error':float(delta.mean()),'tolerance_reason':'Independent tile-only source control vs local shader coordinates; at most2RGB codes allowed, no larger seam allowed.','allowed_mask':'Projected authored field, conservative4screen-pixel dilation for raster filtering and flower excursion','device_performance':'NOT_MEASURED'}
 write(P/'evidence/mobile-fixed-scenery.json',native)
 result={'status':'PASS','source_sha256':sha(MASTER),'native_rest_reconstruction_exact':True,'only_original_appearance':True,'new_items':0,'master_roundtrip_frames':roundtrip,'targets':results,'native_mobile':native,'human_device_child_owner':'PENDING'}
 write(P/'evidence/independent-verification.json',result)
 print(json.dumps(result,indent=2))

if __name__=='__main__':verify()
