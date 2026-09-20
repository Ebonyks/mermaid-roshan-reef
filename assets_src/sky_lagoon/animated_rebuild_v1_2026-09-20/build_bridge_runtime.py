"""Package Aseprite-exported gameplay bridge cels; fail on rest drift or escaped motion."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json
W=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parent/'bridge'
D=W/'assets/sprites/sky_lagoon/animated_v1'
atlas=Image.open(P/'planks-full-atlas.png').convert('RGBA')
meta=json.loads((P/'planks-full-atlas.json').read_text())
source=Image.open(P/'reference_locked.png').convert('RGBA')
a=np.array(source); sheet=Image.new('RGBA',(1024,576)); frames=[]; proof=[]
assert len(meta['frames'])==12
for index,frame in enumerate(meta['frames']):
 r=frame['frame']; image=atlas.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h']))
 b=np.array(image); diff=np.any(a!=b,axis=2)&((a[:,:,3]>0)|(b[:,:,3]>0))
 outside=diff.copy(); outside[832:1024,64:320]=False
 assert not outside.any(), f'frame {index}: motion exceeds owned patch'
 patch=image.crop((64,832,320,1024)); sheet.paste(patch,((index%4)*256,(index//4)*192));frames.append(patch)
 proof.append({'frame':index,'duration_ms':frame['duration'],'changed_pixels':int(diff.sum()),'outside_patch_changed':0})
assert proof[0]['changed_pixels']==0 and proof[-1]['changed_pixels']==0
D.mkdir(parents=True,exist_ok=True);sheet.save(D/'bridge_contact.png')
fixed=source.copy();fixed.paste((0,0,0,0),(64,832,320,1024))
rail=Image.open(P/'front-rail-full.png').convert('RGBA');rail_array=np.array(rail);owned=rail_array[:,:,3]>0
fixed_array=np.array(fixed);fixed_array[owned]=0;fixed=Image.fromarray(fixed_array);fixed.save(D/'castle_fixed.png')
rest=fixed.copy();rest.paste(frames[0],(64,832));rest=Image.alpha_composite(rest,rail)
assert np.array_equal(np.array(rest)[:,:,3],a[:,:,3])
assert np.array_equal(np.array(rest)[a[:,:,3]>0],a[a[:,:,3]>0])
assert not np.any((fixed_array[:,:,3]>0)&owned)

board=Image.new('RGB',(1536,420),'#d8e2e5');draw=ImageDraw.Draw(board)
for col,index in enumerate([0,4,8]):
 board.paste(frames[index].resize((512,384)),(col*512,28));draw.text((col*512+8,8),f'Cel {index+1}',fill='#202b34')
board.save(P/'planks-v3-review.jpg',quality=94)
report={'status':'rigid-board candidate in opt-in runtime; visual/device/owner acceptance pending','frame_count':12,'rest_first_exact':True,'rest_last_exact':True,'method':'Aseprite six rigid board layers; integer cel translations; fixed structure and concealed joint-shadow backing','poses':proof,'crop':[64,832,256,192],'atlas_size':[1024,576],'source_pixel_ownership':'runtime castle_fixed has transparent animation crop and near-rail mask; patch and foreground rail own their pixels once','runtime_integrated':True}
(P/'PLANKS_V3.json').write_text(json.dumps(report,indent=2)+'\n')
print('BRIDGE_PACKAGE|12 cels; bounded motion; exact rest; single crop owner|PASS')
