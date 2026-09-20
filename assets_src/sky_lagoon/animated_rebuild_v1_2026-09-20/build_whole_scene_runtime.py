"""Pack source trials into versioned, opt-in runtime resources; original art stays intact."""
from pathlib import Path
from PIL import Image
import json,math,hashlib
B=Path(__file__).resolve().parent;R=B.parents[2];S=B/'whole_scene_revision';O=R/'assets/sprites/sky_lagoon/whole_scene_v2';O.mkdir(parents=True,exist_ok=True)
base=Image.open(S/'clouds/sky-clouds-removed-candidate.png').convert('RGBA');cards=[]
ambient=S/'ambient_motion_v3';motion=json.loads((ambient/'SOURCE.json').read_text(encoding='utf-8'));cloud_motion={r['id']:r for r in motion['clouds']}
def pack(name,frames,rect,cycle,family):
 x,y,w,h=rect;n=len(frames)
 if n==1:
  image=frames[0];cw,ch=image.size;cols=rows=1;scale=1
 else:
  cw,ch=(256,1024) if family=='tree' else (512,256)
  if family=='cloud': cw,ch=2**math.ceil(math.log2(min(w+4,512))),2**math.ceil(math.log2(min(h+4,256)))
  scale=min((cw-4)/w,(ch-4)/h,1);size=(round(w*scale),round(h*scale));cols=4 if n>4 else 2;rows=4 if n>4 else 2
  if family=='foreground': cols,rows=2,(4 if n>4 else 2)
  image=Image.new('RGBA',(cw*cols,ch*rows))
  for k,frame in enumerate(frames):image.alpha_composite(frame.resize(size,Image.Resampling.LANCZOS),(k%cols*cw+2,k//cols*ch+2))
 if n>1: x-=2/scale;y-=2/scale
 filename=name+'.png';image.save(O/filename)
 cards.append({'id':name,'file':filename,'size':list(image.size),'position':[x,y],'scale':1/scale,'columns':cols,'rows':rows,'frames':n,'cycle':cycle,'family':family,'drift':24 if family=='cloud' else 0})
# Replace only pixels owned by each extracted source, never overlapping rectangular plates.
tree=Image.open(S/'tree/original-tree-rest.png').convert('RGBA');base.paste(Image.open(S/'tree/underpaint-candidate.png').convert('RGBA'),(0,0),tree.getchannel('A'))
pack('arrival_whole_tree',[Image.open(S/'tree'/f'frame-{k:02d}.png').convert('RGBA') for k in range(12)],[0,0,400,1152],4.8,'tree')
for family,cel,under,cycle in [('grass','blades','soil-fixed.png',2.8),('shrubs','canopy','fixed-surroundings.png',3.6)]:
 for row in json.loads((S/family/'SOURCE.json').read_text())['regions']:
  if row['id']=='arrival_front_edge':
   definition=motion['grass'];factor=definition['world_scale'];w,h=definition['source_size'];px,py=definition['root'];wx,wy=definition['world_root']
   pack(row['id'],[Image.open(ambient/'grass'/f'cel-{k:02d}.png').convert('RGBA') for k in range(4)],[wx-px*factor,wy-py*factor,w*factor,h*factor],definition['cycle'],'foreground')
   continue
  p=S/family/row['id'];frames=[Image.open(p/f'{cel}-{k:02d}.png').convert('RGBA') for k in range(4)];x,y,w,h=row['rect'];base.paste(Image.open(p/under).convert('RGBA'),(x,y),frames[0].getchannel('A'));pack(row['id'],frames,row['rect'],cycle,family)
for row in json.loads((S/'clouds/SOURCE.json').read_text())['clouds']:
 if row['id'] in cloud_motion:
  definition=cloud_motion[row['id']];x,y,w,h=row['rect'];ox,oy=definition['position_offset'];folder=ambient/definition['source_dir']
  pack(row['id'],[Image.open(folder/f'cel-{k:02d}.png').convert('RGBA') for k in range(definition['frames'])],[x+ox,y+oy,w,h-oy],48,'cloud')
  cards[-1]['pose_cycle']=definition['pose_cycle']
 else:
  pack(row['id'],[Image.open(S/'clouds/cleaned'/row['file']).convert('RGBA')],row['rect'],48,'cloud')
# Remove the old painted rosette only within its reviewed ownership mask.
# This repair and its six-cel card are one transaction at runtime.
rosette=S/'foreground_rosette/palette_trial'
mask=Image.open(rosette/'removal-mask.png').convert('L')
backing=Image.open(rosette/'generated-backing-native.png').convert('RGBA').resize(mask.size,Image.Resampling.LANCZOS)
base.paste(backing,(4500,1680),mask)
pack('castle_foreground_rosette',[Image.open(rosette/f'cel-{k:02d}.png').convert('RGBA') for k in range(6)],[4527,1689,396,312],2.28,'foreground')
# The meadow plant crosses x2048: heal the continuous master before tile slicing.
meadow=S/'meadow_berry_fan/palette_trial'
mask=Image.open(meadow/'removal-mask.png').convert('L')
backing=Image.open(meadow/'generated-backing-native.png').convert('RGBA').resize(mask.size,Image.Resampling.LANCZOS)
base.paste(backing,(1750,1560),mask)
pack('meadow_boundary_berry_fan',[Image.open(meadow/f'cel-{k:02d}.png').convert('RGBA') for k in range(8)],[1785,1590,516,395],2.4,'foreground')
tiles=[]
for r in range(2):
 for c in range(6):
  name=f'base_r{r}_c{c}.png';base.crop((c*1024,r*1024,(c+1)*1024,(r+1)*1024)).save(O/name);tiles.append({'file':name,'size':[1024,1024],'node':f'SkyLagoonBackdrop_r{r}_c{c}'})
for row in tiles+cards:row['sha256']=hashlib.sha256((O/row['file']).read_bytes()).hexdigest()
manifest={'schema':1,'status':'OPT_IN_UNACCEPTED_TRIAL','tiles':tiles,'cards':cards,'raw_rgba_mib':sum(r['size'][0]*r['size'][1]*4 for r in tiles+cards)/1048576,'limits':'Twelve separated clouds have three or four cels with independent pose/drift clocks; eight use direct Aseprite deformation of original paint. Low cloud sea is incomplete. One new foreground grass accent does not solve broad lawn coverage. Owner/device acceptance pending.'}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');print('WHOLE_PACK',len(tiles),'tiles',len(cards),'cards',manifest['raw_rgba_mib'],'MiB')
