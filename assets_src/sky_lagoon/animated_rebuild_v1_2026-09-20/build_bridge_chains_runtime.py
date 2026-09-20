from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
P=Path(__file__).resolve().parent/'bridge';W=Path(__file__).resolve().parents[3];D=W/'assets/sprites/sky_lagoon/animated_v1';atlas=Image.open(P/'chains-atlas.png').convert('RGBA');assert atlas.size==(896,576)
source=np.array(Image.open(P/'chain-patch-source.png').convert('RGBA'));frames=[];rows=[];moving=np.zeros(224,dtype=bool)
for lo,hi in [(6,76),(121,139),(173,214)]:moving[lo+1:hi]=True
for n in range(12):
 f=atlas.crop(((n%4)*224,(n//4)*192,(n%4+1)*224,(n//4+1)*192));a=np.array(f);frames.append(f)
 assert np.array_equal(a[:,~moving,3],source[:,~moving,3]);visible=source[:,~moving,3]>0;assert np.array_equal(a[:,~moving][visible],source[:,~moving][visible])
 rows.append({'frame':n,'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'post_and_attachment_columns_exact':True})
for n in [0,1,11]:
 a=np.array(frames[n]);assert np.array_equal(a[:,:,3],source[:,:,3]);assert np.array_equal(a[source[:,:,3]>0],source[source[:,:,3]>0])
 fixed=Image.open(D/'bridge_front_rail_fixed.png').convert('RGBA');fixed.alpha_composite(frames[0],(48,28));orig=np.array(Image.open(D/'bridge_front_rail.png').convert('RGBA'));a=np.array(fixed);assert np.array_equal(a[:,:,3],orig[:,:,3]);assert np.array_equal(a[orig[:,:,3]>0],orig[orig[:,:,3]>0])
board=Image.new('RGB',(896,420),'#5d5269');draw=ImageDraw.Draw(board)
for col,n in enumerate([0,4,7,11]):
 full=Image.open(D/'bridge_front_rail_fixed.png').convert('RGBA');full.alpha_composite(frames[n],(48,28));full=full.resize((224,211));board.paste(full,(col*224,28),full);draw.text((col*224+8,8),f'Rail pose {n+1}',fill='white')
board.crop((0,0,896,245)).save(P/'chains-review.jpg',quality=95)
(P/'CHAINS_VALIDATION.json').write_text(json.dumps({'frames':rows,'rest_reassembly_exact':True,'intentional_rest_frames':[0,1,11],'rest_reason':'secondary response begins after deck contact and returns to exact rest','max_displacement_source_px':2.4,'runtime_atlas_size':[896,576],'status':'candidate; in-scene temporal acceptance pending'},indent=2)+'\n')
shutil.copyfile(P/'chains-atlas.png',D/'bridge_chains.png');print('CHAINS|fixed posts and attachments; exact rest reassembly|PASS')
