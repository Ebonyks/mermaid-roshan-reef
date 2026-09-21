"""Repack overlapping painted subjects without resizing or recoloring them."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'project.godot').exists())
SOURCE=ROOT/'assets/sprites/sky_lagoon/animals'
OUTPUT=ROOT/'assets/sprites/sky_lagoon/whole_scene_v2'
NAMES=['frog_startle','hare_startle','otter_startle','raccoon_idle','squirrel_startle']
records=[]
board=Image.new('RGB',(1280,280*len(NAMES)),'#65776d');draw=ImageDraw.Draw(board)
for index,name in enumerate(NAMES):
 path=SOURCE/(name+'_atlas.png');a=np.array(Image.open(path).convert('RGBA'))
 assert a.shape==(512,512,4)
 labels,n=ndimage.label(a[:,:,3]>8,structure=np.ones((3,3)));sizes=np.bincount(labels.ravel())
 major=np.argsort(sizes[1:])[::-1][:4]+1;seeds=np.zeros(labels.shape,int);owners=set()
 for label in major:
  ys,xs=np.where(labels==label);frame=int(np.mean(ys))//256*2+int(np.mean(xs))//256
  assert frame not in owners;owners.add(frame);seeds[labels==label]=frame+1
 assert owners=={0,1,2,3}
 _,indices=ndimage.distance_transform_edt(seeds==0,return_indices=True);ownership=seeds[tuple(indices)]
 reconstructed=np.zeros_like(a);atlas=Image.new('RGBA',(640,512));frames=[]
 for frame in range(4):
  ys,xs=np.where((ownership==frame+1)&(a[:,:,3]>0));tx=xs-frame%2*256+32;ty=ys-frame//2*256
  assert tx.min()>=2 and tx.max()<318 and ty.min()>=2 and ty.max()<254
  cel=np.zeros((256,320,4),np.uint8);cel[ty,tx]=a[ys,xs];reconstructed[ys,xs]=cel[ty,tx]
  image=Image.fromarray(cel);image.save(HERE/f'{name}-cel-{frame}.png');atlas.paste(image,(frame%2*320,frame//2*256))
  tile=Image.new('RGBA',image.size,'#65776d');tile.alpha_composite(image);board.paste(tile.convert('RGB'),(frame*320,index*280+22))
  draw.text((frame*320+6,index*280+5),f'{name} / pose {frame+1}',fill='white')
  frames.append({'frame':frame,'bounds':[int(tx.min()),int(ty.min()),int(tx.max()+1),int(ty.max()+1)],'centered_body_position_delta':[0,0]})
 assert np.array_equal(reconstructed[:,:,3],a[:,:,3])
 assert np.array_equal(reconstructed[a[:,:,3]>0],a[a[:,:,3]>0])
 target=OUTPUT/(name+'_padded.png');atlas.save(target)
 records.append({'id':name,'source':path.relative_to(ROOT).as_posix(),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'runtime':target.relative_to(ROOT).as_posix(),'runtime_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'visible_rgba_reconstruction_exact':True,'frames':frames})
board.save(HERE/'comparison.jpg',quality=95)
(HERE/'MANIFEST.json').write_text(json.dumps({'status':'SOURCE_EXACT_INTEGRATED_SAMPLING_PENDING','method':'Four large connected subject seeds, nearest-owner assignment for original alpha fringe,32px symmetric horizontal cell padding; no resampling, regeneration, anatomy or palette changes.','grid':[2,2],'cell_size':[320,256],'source_checkpoint':'d26f1af526892b4847edc6755f1ff011ce743ef9','atlases':records,'limits':['Original atlas paths retained for default mode and rollback','Runtime startle/idle sampling and contact tests required','Not newly authored motion or additional frames']},indent=2)+'\n')
print('Five padded atlases: all original visible RGBA pixels reconstruct exactly.')
