from pathlib import Path
from hashlib import sha256
import json, math, shutil, time
import numpy as np
from scipy.ndimage import map_coordinates, binary_fill_holes
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parent
R=P.parents[2]
D=P/'demo_project'
N=40; S=256
SWAY_GAIN=0.08
SHAPE_GAIN=0.04
ROTATION_GAIN=0.05
LIGHT_GAIN=0.12
Y,X=np.mgrid[:S,:S].astype(float)
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
SOURCES={
'fir':'assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway_v2.png',
'huckleberry':'assets_src/cinematics/sky_lagoon_garden_motion_v2_2026-09-16/native/huckleberry-foreground.png',
'hydrangea':'assets_src/cinematics/sky_lagoon_garden_motion_v2_2026-09-16/native/hydrangea.png',
'bellflower':'assets_src/cinematics/sky_lagoon_garden_motion_v2_2026-09-16/native/cream-bellflower.png',
'cloud':'assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png',
'smoke':'assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png',
'seesaw':'assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png',
'gate':'assets/sprites/sky_lagoon/sky_lagoon_castle_gate_v3.png',
'glass':'assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png',
'swing':'assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png'}
TITLES={'fir':'Fir sways lightly','huckleberry':'Leaves stir gently','hydrangea':'A very light flower sway','bellflower':'Tiny bellflower nod','cloud':'Soft cloud movement','smoke':'Faint smoke curl','seesaw':'Seesaw barely rocks','gate':'Subtle gate movement','glass':'Faint window glint'}
def sha(p):return sha256(p.read_bytes()).hexdigest()
def visible_sha(im):
 a=np.asarray(im).copy();a[a[:,:,3]==0]=0;return sha256(a.tobytes()).hexdigest()
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def norm(p,longest=196):
 im=Image.open(p).convert('RGBA'); im=im.crop(im.getbbox()); im.thumbnail((longest,longest),Image.Resampling.LANCZOS)
 canvas=Image.new('RGBA',(S,S));canvas.alpha_composite(im,((S-im.width)//2,234-im.height));return canvas

def warp(im,sx,sy):
 a=np.asarray(im).astype(float)/255; pre=a.copy();pre[:,:,:3]*=a[:,:,3:4]
 out=np.stack([map_coordinates(pre[:,:,c],[sy,sx],order=1,mode='constant',cval=0) for c in range(4)],axis=-1)
 out[:,:,:3]/=np.maximum(out[:,:,3:4],1/65536)
 return Image.fromarray(np.uint8(np.clip(np.rint(out*255),0,255)))

def frame(im,k,i):
 if i%N==0 or k=='swing':return im.copy()
 t=math.tau*i/N;s=math.sin(t);h=np.clip((228-Y)/190,0,1)
 if k in ['fir','huckleberry','hydrangea','bellflower']:
  amp={'fir':16,'huckleberry':20,'hydrangea':28,'bellflower':28}[k]
  if k=='huckleberry':h=np.clip((228-Y)/90,0,1)
  dx=amp*SWAY_GAIN*s*h**1.5+5*SHAPE_GAIN*math.sin(2*t)*np.sin((Y-32)/24)*h
  dy=3*SHAPE_GAIN*math.sin(2*t)*np.sin((X-128)/50)*h
  a=np.asarray(warp(im,X-dx,Y-dy)).copy();a[Y>=228]=np.asarray(im)[Y>=228];return Image.fromarray(a)
 if k=='cloud':return warp(im,X-8*SHAPE_GAIN*s*np.sin((X-128)/55),Y-6*SHAPE_GAIN*s*np.cos((X-128)/45)*np.clip((234-Y)/65,0,1))
 if k=='smoke':return warp(im,X-17*SWAY_GAIN*h*(np.sin(t+(Y-234)/27)-np.sin((Y-234)/27)),Y-3*SHAPE_GAIN*s*h)
 if k=='seesaw':
  a=np.asarray(im).copy();fixed=(Y>=199)|((X-128)**2+(Y-193)**2<=49)
  beam=a.copy();beam[fixed]=0;base=a.copy();base[~fixed]=0
  th=math.radians(10)*ROTATION_GAIN*s;cx=128;cy=193
  out=warp(Image.fromarray(beam),cx+(X-cx)*math.cos(th)+(Y-cy)*math.sin(th),cy-(X-cx)*math.sin(th)+(Y-cy)*math.cos(th));out.alpha_composite(Image.fromarray(base));return out
 if k=='gate':
  a=np.asarray(im).copy();rgb=a[:,:,:3].astype(float)
  mask=(rgb[:,:,0]>rgb[:,:,1]*1.22)&(rgb[:,:,0]>rgb[:,:,2]*1.08)&(X>=94)&(X<=160)&(Y>=125)&(Y<=227)
  mask=binary_fill_holes(mask);u=(1-math.cos(t))/2;sc=1-.82*ROTATION_GAIN*u
  base=a.copy();base[mask,:3]=[51,29,63];out=Image.fromarray(base)
  for left,hinge in [(True,104),(False,151)]:
   leaf=a.copy();leaf[~(mask&((X<127) if left else (X>=127)))]=0;out.alpha_composite(warp(Image.fromarray(leaf),hinge+(X-hinge)/sc,Y))
  return out
 if k=='glass':
  a=np.asarray(im).copy();rgb=a[:,:,:3].astype(float)
  mask=(((X-128)/24)**2+((Y-112)/36)**2<1)&(Y<153)
  light=np.exp(-((X-(128+20*SWAY_GAIN*math.sin(t)))/9)**2)*mask*math.sin(t/2)**2
  rgb+=light[:,:,None]*np.array([32,38,20])*LIGHT_GAIN;a[:,:,:3]=np.uint8(np.clip(np.rint(rgb),0,255));return Image.fromarray(a)
 raise ValueError(k)

def gif(path,frames):
 board=Image.new('RGB',(frames[0].width,frames[0].height*len(frames)))
 for i,im in enumerate(frames):board.paste(im.convert('RGB'),(0,i*im.height))
 palette=board.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
 indexed=[im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
 indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=100,loop=0,optimize=True)
 with Image.open(path) as check:
  ms=0
  for i in range(check.n_frames):check.seek(i);check.load();ms+=check.info['duration']
  assert ms==4000

def main():
 start=time.perf_counter()
 for sub in ['sources','jobs','stills','evidence','demo_project','demo_project/items','demo_project/background','captures']:(P/sub).mkdir(exist_ok=True)
 sources={};loops={};entries=[]
 for k,rel in SOURCES.items():
  src=R/rel;target=P/'sources'/f'{k}.png';shutil.copyfile(src,target)
  sources[k]={'path':rel,'sha256':sha(src),'dimensions':Image.open(src).size,'role':'identity_still_only','copy':str(target.relative_to(P)).replace('\\','/'),'license':'Project art; inherits exact source terms in ASSET_LICENSES.md','acceptance_scope':'Identity still only. Garden separated art remains review-only. No prior animation frames reused.'}
  write(P/'jobs'/f'{k}.json',{'id':k,'revision':1,'date':'2026-11-05','lane':'isolated reference demo','source':sources[k],'intention':TITLES.get(k,'Static swing; changing fore/aft surfaces missing'),'fixed':'Camera/background, plant root bands, seesaw pedestal, gate masonry, swing frame','entry_exit':'Exact normalized source at t=0 and t=4 seconds','method':'Local keyed 2D deformation/layer articulation; premultiplied RGBA sampling; Aseprite master','geometry':'256 padded canvas; plant root y>=228; seesaw axle (128,193); gate hinges x104/x151','tolerances':'Plant displacement <=3px from rest; vertical deformation <=0.12px; seesaw <=0.5deg; fixed support; no clipping; periodic endpoint exact','limits':{'generated_take_cap':2,'generated_calls':0,'money_cap':0,'local_trial_minutes':90,'cleanup_minutes_cap':30,'aggregate_task_minutes':180},'stop_fallback':'Stop on drift/contact failure; no rejected-frame reuse. Swing remains missing-view gap.','human_review':'PENDING','device_review':'PENDING','owner_review':'PENDING'})
  im=norm(target,206 if k=='smoke' else 196);im.save(P/'stills'/f'{k}.png')
  frames=[frame(im,k,i) for i in range(N if k!='swing' else 1)];loops[k]=frames
  if k=='swing':im.save(D/'items/swing.png');continue
  for i,f in enumerate(frames):
   a=np.asarray(f);assert not a[[0,-1],:,3].any(),(k,i,'vertical clipping');assert not a[:,[0,-1],3].any(),(k,i,'horizontal clipping')
  assert frame(im,k,N).tobytes()==im.tobytes()
  if k in ['fir','huckleberry','hydrangea','bellflower']:
   for f in frames:assert f.crop((0,228,256,256)).tobytes()==im.crop((0,228,256,256)).tobytes()
  atlas=Image.new('RGBA',(2048,2048))
  for i,f in enumerate(frames):atlas.paste(f,((i%8)*S,(i//8)*S))
  atlas.save(D/'items'/f'{k}.png')
  previews=[]
  for f in frames:
   canvas=Image.new('RGBA',(S,S),'#edf2e6');canvas.alpha_composite(f);previews.append(canvas.convert('RGB'))
  gif(P/f'{k}.gif',previews)
  entries.append({'id':k,'title':TITLES[k],'atlas':f'items/{k}.png','columns':8,'frames':N,'fps':10,'period_seconds':4,'frame_rgba_sha256':[sha256(f.tobytes()).hexdigest() for f in frames],'frame_visible_rgba_sha256':[visible_sha(f) for f in frames],'atlas_sha256':sha(D/'items'/f'{k}.png'),'unique_frames':len({f.tobytes() for f in frames}),'source':sources[k]})
  print(k,'complete',flush=True)
 write(D/'items.json',entries)
 for r in range(2):
  for c in range(6):
   rel=f'assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r{r}_c{c}.png';shutil.copyfile(R/rel,D/'background'/f'{r}_{c}.png');sources[f'background_{r}_{c}']={'path':rel,'sha256':sha(R/rel),'role':'unchanged_background_tile'}
 master=Image.open(R/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png').convert('RGB').resize((1920,640),Image.Resampling.LANCZOS)
 placements=[['glass',1400,36,495,495],['cloud',670,-40,330,220],['smoke',1423,6,150,140],['seesaw',820,392,340,240],['huckleberry',170,370,360,300],['hydrangea',440,360,280,280],['bellflower',660,348,280,292],['hydrangea',1660,370,280,270]]
 write(D/'placements.json',placements)
 worlds=[];boards=[];flowers=[]
 for i in range(N):
  world=master.convert('RGBA')
  for k,x,y,w,h in placements:
   side=min(w,h);px=round(x+(w-side)/2);py=round(y+(h-side)*234/256)
   world.alpha_composite(loops[k][i].resize((side,side),Image.Resampling.LANCZOS),(px,py))
  worlds.append(world.convert('RGB'));world.convert('RGB').save(P/'captures'/f'{i:03}.png')
  board=Image.new('RGB',(960,900),'#153a43');draw=ImageDraw.Draw(board)
  for j,k in enumerate(TITLES):
   bx=(j%3)*320;by=(j//3)*300;draw.rounded_rectangle((bx+6,by+6,bx+314,by+292),12,fill='#eef2e6');board.paste(loops[k][i],(bx+32,by+3),loops[k][i]);draw.text((bx+15,by+261),TITLES[k],font=FONT,fill='#193e43')
  boards.append(board)
  canvas=Image.new('RGBA',(800,420),'#e4eddc');canvas.alpha_composite(loops['hydrangea'][i].resize((400,400),Image.Resampling.LANCZOS),(0,0));canvas.alpha_composite(loops['bellflower'][i].resize((400,400),Image.Resampling.LANCZOS),(400,0));flowers.append(canvas.convert('RGB'))
 gif(P/'flowers-closeup.gif',flowers)
 gif(P/'fixed-camera-items.gif',[im.resize((1280,426),Image.Resampling.LANCZOS) for im in worlds]);gif(P/'individual-items.gif',[im.resize((768,720),Image.Resampling.LANCZOS) for im in boards])
 worlds[0].save(P/'fixed-camera-rest.png');worlds[10].save(P/'fixed-camera-breeze.png');boards[10].save(P/'item-board.png')
 lua=['local root=app.params["packet"]','local only=app.params["only"]','local built=0']
 for k in TITLES:
  lua += [f'if only==nil or only=="{k}" then',f'do local sheet=Image{{fromFile=root.."/demo_project/items/{k}.png"}}','local s=Sprite(256,256,ColorMode.RGB)',f'local layer=s.layers[1];layer.name="{k}"','for i=0,39 do if i>0 then s:newEmptyFrame() end','local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))','s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end',f's:saveAs(root.."/{k}.aseprite");s:close() end','built=built+1 end']
 lua.append('local f=io.open(root.."/evidence/aseprite-build.txt","w");f:write("Aseprite "..tostring(app.version).."; masters_built="..built.."; 40 cels each at 100ms");f:close()')
 (P/'build_masters.lua').write_text('\n'.join(lua)+'\n')
 write(P/'derivation.json',{'status':'CANDIDATE_DEMO_ONLY','owner_correction':'2026-11-05: scrolling preview rejected; stationary item motion required','source_files':sources,'items':entries,'old_rejected_motion_frames_used':0,'generated_calls':0,'paid_cost':0,'method':'Local source-still 2D deformation and layer articulation. No generated new artwork. No character acting.','gaps':{'swing':'NOT_ANIMATED: accepted fore/aft views and changing seat surfaces missing.','gate':'Dark flat interior is a declared unpainted gap.','fir':'Standalone board only; excluded from panorama to preserve mountain path.','integration':'Illustrative demo foreground positions; production sockets unchanged.'},'tests':{'periodic_endpoint':'PASS','plant_support_bands_exact':'PASS','no_canvas_clipping':'PASS','source_bytes_unchanged':'PASS','camera_translation_pixels':0},'build_seconds':round(time.perf_counter()-start,3),'acceptance':'Human full-speed/frame-step, owner, device and child review pending'})
 print('ITEM_BUILD PASS: nine loops, stationary scene, zero rejected animation frames',flush=True)
if __name__=='__main__':main()
