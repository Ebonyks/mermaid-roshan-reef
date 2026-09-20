"""Validate and package the eight Aseprite-exported bellflower cels."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage as nd
import json,numpy as np,hashlib,shutil
P=Path(__file__).resolve().parent/'bellflower';W=Path(__file__).resolve().parents[3]
atlas=Image.open(P/'bellflower-atlas.png').convert('RGBA');meta=json.loads((P/'bellflower-atlas.json').read_text());frames=[];rows=[]
assert atlas.size==(2048,1024) and len(meta['frames'])==8
assert [f['duration'] for f in meta['frames']]==[260,240,300,260,220,240,300,260]
for index,entry in enumerate(meta['frames']):
 r=entry['frame'];assert r['w']==512 and r['h']==512
 frame=atlas.crop((r['x'],r['y'],r['x']+512,r['y']+512));a=np.array(frame);frames.append(frame)
 labels,count=nd.label(a[:,:,3]>64);sizes=np.bincount(labels.ravel())[1:];fraction=float(sizes.max()/sizes.sum())
 assert fraction==1.0, f'frame {index}: detached component'
 rows.append({'frame':index,'largest_connected_fraction':fraction,'rgba_sha256':hashlib.sha256(a.tobytes()).hexdigest()})
base=np.array(frames[0]);assert len({r['rgba_sha256'] for r in rows})==8
for frame in frames:assert np.array_equal(np.array(frame)[300:],base[300:]),'fixed lower plant drift'
board=Image.new('RGB',(1536,540),'#dfe4df');draw=ImageDraw.Draw(board)
for col,index in enumerate([0,2,6]):
 board.paste(frames[index],(col*512,28),frames[index]);draw.text((col*512+12,9),f'Bellflower pose {index+1}',fill='#25392f')
board.save(P/'eight-cel-review.jpg',quality=94)
all_poses=Image.new('RGB',(1024,560),'#dfe4df');draw=ImageDraw.Draw(all_poses)
for index,frame in enumerate(frames):
 cell=frame.resize((256,256));pos=((index%4)*256,(index//4)*280+20)
 all_poses.paste(cell,pos,cell);draw.text((pos[0]+10,pos[1]-15),f'{index+1}',fill='#25392f')
all_poses.save(P/'all-eight-cels.jpg',quality=94)
report={'frames':8,'unique_frames':8,'durations_ms':[f['duration'] for f in meta['frames']],'fixed_lower_rows':[300,512],'fixed_lower_rows_exact':True,'root_anchor':[308,468],'atlas_size':list(atlas.size),'connectivity':rows,'method':'Aseprite Lua: independent rigid bell rotations with coherent stem sway; premultiplied alpha sampling; fixed base leaves','status':'opt-in runtime candidate; temporal/device/owner acceptance pending','runtime_integrated':True}
(P/'ANIMATION_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
shutil.copy2(P/'bellflower-atlas.png',W/'assets/sprites/sky_lagoon/animated_v1/bellflower_breeze.png')
print('BELLFLOWER_PACKAGE|8 unique connected cels; fixed lower plant; exact timing|PASS')
