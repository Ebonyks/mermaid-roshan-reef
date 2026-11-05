from pathlib import Path
from hashlib import sha256
import json, math, subprocess, argparse
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
R=P.parents[2]
def sha(p):return sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--production-base',default='5003d421b0de8771a59eafdcb2aadffd818a7246');args=parser.parse_args()
 d=json.loads((P/'derivation.json').read_text());entries=json.loads((P/'demo_project/items.json').read_text())
 for e in d['source_files'].values():assert sha(R/e['path'])==e['sha256'],e['path']
 cels=0
 for e in entries:
  atlas=Image.open(P/'demo_project'/e['atlas']).convert('RGBA');assert sha(P/'demo_project'/e['atlas'])==e['atlas_sha256']
  for i in range(40):
   cel=atlas.crop(((i%8)*256,(i//8)*256,(i%8+1)*256,(i//8+1)*256));assert sha256(cel.tobytes()).hexdigest()==e['frame_rgba_sha256'][i]
   master=Image.open(P/'evidence/roundtrip'/f'{e["id"]}_{i:02}.png').convert('RGBA');assert master.tobytes()==cel.tobytes(),(e['id'],i)
   a=np.asarray(cel);assert not a[[0,-1],:,3].any();assert not a[:,[0,-1],3].any()
   if e['id'] in ['fir','huckleberry','hydrangea','bellflower']:
    rest=Image.open(P/'stills'/f'{e["id"]}.png').convert('RGBA');assert cel.crop((0,228,256,256)).tobytes()==rest.crop((0,228,256,256)).tobytes()
   cels+=1
 for file in P.glob('*.gif'):
  with Image.open(file) as im:
   duration=0
   for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info['duration']
   assert im.info['loop']==0 and duration==4000,file.name
 first=np.asarray(Image.open(P/'captures/engine/000.png').convert('RGB')).astype(int)
 assert first.shape==(720,1280,3)
 mask=np.zeros((720,1280),bool);placements=json.loads((P/'demo_project/placements.json').read_text())
 for k,x,y,w,h in placements:
  x0=max(0,math.floor(x*2/3)-3);x1=min(1280,math.ceil((x+w)*2/3)+3)
  y0=max(0,math.floor(156.6666667+y*2/3)-3);y1=min(720,math.ceil(156.6666667+(y+h)*2/3)+3);mask[y0:y1,x0:x1]=True
 changed=[]
 for i in range(40):
  a=np.asarray(Image.open(P/'captures/engine'/f'{i:03}.png').convert('RGB')).astype(int);diff=np.any(a!=first,axis=2)
  assert not diff[~mask].any(),('background/camera movement',i,int(diff[~mask].sum()))
  changed.append(int(diff.sum()))
 assert max(changed)>1000
 runtime_diff=subprocess.check_output(['git','diff',args.production_base,'--name-only','--','scripts','scenes','assets','project.godot'],cwd=R,text=True).strip();assert not runtime_diff
 glass=Image.open(P/'demo_project/items/glass.png').convert('RGBA');g0=np.asarray(glass.crop((0,0,256,256))).astype(int);g39=np.asarray(glass.crop((1792,1024,2048,1280))).astype(int);seam_jump=int(np.abs(g0-g39).max());assert seam_jump<=2,('window glint seam',seam_jump)
 receipt={'result':'PASS','production_baseline':subprocess.check_output(['git','rev-parse',args.production_base],cwd=R,text=True).strip(),'window_glint_seam_max_channel_jump':seam_jump,'source_files_unchanged':len(d['source_files']),'master_and_atlas_cels_exact_rgba':cels,'master_frame_ms':100,'all_gif_loops_ms':4000,'root_band_pixels':'exact in all plant frames','clipped_border_pixels':0,'engine_frames_checked':40,'background_pixels_checked_per_frame':int((~mask).sum()),'changed_background_pixels':0,'max_changed_item_pixels':max(changed),'camera_translation_pixels':0,'atlas_base_rgba_mib':144,'native_background_base_rgba_mib':48,'device_memory_timing':'PENDING; these are base texture estimates, not GPU/device measurements','historical_topic_ci':'https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/41998350733','human_device_child_owner_acceptance':'PENDING'}
 (P/'evidence/machine-verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print('ITEM_PACKET_VERIFY PASS',json.dumps(receipt))
if __name__=='__main__':main()
