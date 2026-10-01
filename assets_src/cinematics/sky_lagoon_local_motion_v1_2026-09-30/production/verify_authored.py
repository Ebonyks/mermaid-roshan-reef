import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
items=json.loads((ROOT/'OBJECTS.json').read_text(encoding='utf-8'));results=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for item in items:
 folder=ROOT/'authored'/item['id'];source=np.array(Image.open(folder/'source.png').convert('RGBA'));source[source[:,:,3]==0,:3]=0
 frames=[np.array(Image.open(p).convert('RGBA')) for p in sorted((folder/'frames').glob('frame_*.png'))]
 unique=len({hashlib.sha256(a.tobytes()).hexdigest() for a in frames})
 assert len(frames)==32 and unique>=12,item['id']
 assert sha(REPO/item['source'])==item['source_sha256'],item['id']+' original changed'
 assert Image.open(folder/'spritesheet.png').size==(2048,1024)
 assert len(json.loads((folder/'spritesheet.json').read_text())['frames'])==32
 receipt=json.loads((folder/'AUTHORING_RECEIPT.json').read_text());assert receipt['exact_round_trip']=='PASS'
 for a in frames:
  assert a.shape==(256,256,4)
  assert not np.any(a[:,:,:3][a[:,:,3]==0]),item['id']+' RGB under transparency'
  assert np.any(a[:,:,3]>128)
 ys,xs=np.nonzero(source[:,:,3]>128);top=int(ys.min());bottom=int(ys.max());limit=top+int((bottom-top)*.5)
 centers=[];silhouettes=[];light_centers=[]
 for a in frames:
  m=a[:,:,3]>128;silhouettes.append(m)
  yy,xx=np.nonzero(m& (np.indices(m.shape)[0]<limit));centers.append([float(xx.mean()),float(yy.mean())])
  if item['id']=='10_glass':
   delta=np.maximum(0,a[:,:,:3].astype(float)-source[:,:,:3].astype(float)).sum(axis=2)
   if delta.sum()>250:light_centers.append(float((delta*np.indices(delta.shape)[1]).sum()/delta.sum()))
 span=np.ptp(np.array(centers),axis=0).tolist()
 boundary_steps=[float(np.mean(np.abs(frames[(i+1)%32].astype(float)-frames[i].astype(float)))) for i in range(32)]
 checks={'source_hash_unchanged':True,'rgba_transparency':True,'32_timed_editable_states':True,'pot_atlas':True,'exact_aseprite_round_trip':True}
 locked_error=None
 if item['id'] in ['01_fir','02_huckleberry','03_hydrangea','04_bellflower','06_smoke']:
  y=receipt['root_lock_y'];locked_error=max(int(np.max(np.abs(a[y:].astype(int)-source[y:].astype(int)))) for a in frames)
  assert locked_error==0,(item['id'],'root drift',locked_error)
  assert span[0]>=6,(item['id'],'insufficient visible displacement',span)
  checks['fixed_root_pixels']=True;checks['visible_silhouette_displacement']=True
 if item['id']=='07_swing':
  assert max(int(np.max(np.abs(a[:65].astype(int)-source[:65].astype(int)))) for a in frames)==0
  checks['fixed_top_beam_and_hooks']=True
 if item['id']=='08_seesaw':
  yy,xx=np.indices(source.shape[:2]);mask=((yy>=140)&(xx>=96)&(xx<=159))|((xx-128)**2+(yy-128)**2<=10**2)
  assert max(int(np.max(np.abs(a[mask].astype(int)-source[mask].astype(int)))) for a in frames)==0
  checks['fixed_pedestal_and_pivot']=True
 if item['id']=='09_gate':
  mask=np.ones(source.shape[:2],bool);mask[108:224,102:159]=False
  assert max(int(np.max(np.abs(a[mask].astype(int)-source[mask].astype(int)))) for a in frames)==0
  checks['fixed_architecture']=True
 if item['id']=='10_glass':
  assert all(np.array_equal(a[:,:,3],source[:,:,3]) for a in frames)
  assert max(light_centers)-min(light_centers)>20
  checks['fixed_pane_geometry']=True;checks['traveling_glint_not_global_flicker']=True
 result={'id':item['id'],'checks':checks,'unique_raster_poses':unique,'cycle_note':'Symmetric back-and-forth source studies revisit the same pose on the return. Timed states are not claimed to be independent full-frame generations.','upper_silhouette_centroid_span_px':span,'root_pixel_error':locked_error,
         'glint_centroid_span_px':max(light_centers)-min(light_centers) if light_centers else None,
         'wrap_transition_mean_rgba_delta':boundary_steps[-1],'maximum_adjacent_mean_rgba_delta':max(boundary_steps),
         'master_sha256':sha(folder/(item['id']+'.aseprite')),'status':'MACHINE_PASS_REFERENCE_ONLY'}
 results.append(result)
out={'status':'PASS','objects':10,'frames':320,'checks':results,'method':'Source-based scripted motion, not generated or hand-painted action frames.',
     'acceptance_limit':'Structural pixels, source preservation, declared anchors and movement measurements only. Owner, production art, engine, device and child acceptance pending.'}
(ROOT/'authored/MACHINE_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('Ten/ten reference masters, 320 states, declared fixed regions and measurable motion PASS; human acceptance pending.')
