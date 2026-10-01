"""Build corrected reference drawings. All pixel writes use Aseprite Lua."""
import hashlib, importlib.util, json, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
ASE = Path('C:/Program Files/Aseprite/Aseprite.exe')

def write(p,d): p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args):
 r=subprocess.run([str(ASE),'--batch',*map(str,args)],capture_output=True,text=True)
 if r.stdout.strip(): print(r.stdout.strip(),flush=True)
 if r.stderr.strip(): print(r.stderr.strip(),flush=True)
 r.check_returncode()

def main():
 scene_lua=ROOT/'production/assemble_scene.lua'
 text=scene_lua.read_text(encoding='utf-8')
 if 'Painted contact shadows' not in text:
  text=text.replace('local layers={}','''local shadows=sprite:newLayer();shadows.name='Painted contact shadows';shadows.isContinuous=true
local shadow=Image(cfg.width,cfg.height,ColorMode.RGB)
for _,s in ipairs(cfg.shadow_contacts or {}) do
 for y=math.floor(s.center[2]-s.radius[2]),math.ceil(s.center[2]+s.radius[2]) do
  for x=math.floor(s.center[1]-s.radius[1]),math.ceil(s.center[1]+s.radius[1]) do
   local d=((x-s.center[1])/s.radius[1])^2+((y-s.center[2])/s.radius[2])^2
   if d<1 then shadow:drawPixel(x,y,pc.rgba(36,74,69,math.floor(62*(1-d)))) end
  end
 end
end
local layers={}''')
  text=text.replace('local t=tick%total','local t=(tick+(item.phase or 0))%total')
  text=text.replace('local phase=(tick%24)/2','local phase=(tick%48)/4')
  text=text.replace('if tick==0 then sprite:newCel(background,frame,base,Point(0,0)) end','if tick==0 then sprite:newCel(background,frame,base,Point(0,0));sprite:newCel(shadows,frame,shadow,Point(0,0)) end')
  text=text.replace("if tick==0 then flat:saveAs(root..'/scene/sky_lagoon_sample.png') end",'''if tick==0 then
  flat:saveAs(root..'/scene/sky_lagoon_sample.png')
  for panel=0,2 do
   local crop=Image(640,640,ColorMode.RGB)
   for y=0,639 do for x=0,639 do crop:drawPixel(x,y,flat:getPixel(panel*640+x,y)) end end
   crop:saveAs(root..'/review/screen_'..panel..'.png')
  end
 end''')
  scene_lua.write_text(text,encoding='utf-8')
 spec=importlib.util.spec_from_file_location('source_build',ROOT/'production/build.py')
 builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
 # Multipage native import and exact separate left/right rope endpoints.
 lua=ROOT/'production/import_pose_sheet.lua'
 s=lua.read_text(encoding='utf-8')
 if 'local natives=' not in s:
  s=s.replace("local native=Image{fromFile=dir..'/'..cfg.input}","local native=Image{fromFile=dir..'/'..cfg.input}\nlocal natives={[cfg.input]=native}")
 if 'local source=natives[input]' not in s:
  s=s.replace("local p=cfg.poses[n+1];local keep=mask(p.keep_runs,cfg.cell_width)","local p=cfg.poses[n+1];local keep=mask(p.keep_runs,cfg.cell_width)\n local input=p.input or cfg.input\n if not natives[input] then natives[input]=Image{fromFile=dir..'/'..input} end\n local source=natives[input]")
 s=s.replace('local color=native:getPixel(p.origin[1]+sx,p.origin[2]+sy)','local color=source:getPixel(p.origin[1]+sx,p.origin[2]+sy)')
 s=s.replace('local yy=cfg.socket_target_y[n]\n  rope(out,193,118,math.floor(lx),yy);rope(out,320,118,math.floor(rx),yy)', 'local ly=p.offset[2]+p.scale*cfg.seat_sockets[n][2]\n  local ry=p.offset[2]+p.scale*cfg.seat_sockets[n][4]\n  rope(out,193,118,math.floor(lx+.5),math.floor(ly+.5));rope(out,320,118,math.floor(rx+.5),math.floor(ry+.5))')
 if '-- Front ropes remain visibly attached' not in s:
  s=s.replace('poses[n]=out','''-- Front ropes remain visibly attached; the shell back must not hide them.
  rope(out,193,118,math.floor(lx+.5),math.floor(ly+.5));rope(out,320,118,math.floor(rx+.5),math.floor(ry+.5))
  poses[n]=out''')
 lua.write_text(s,encoding='utf-8')
 folder=ROOT/'objects/07_swing'
 cfg={'id':'07_swing','kind':'swing','input':'near_native.png','cell_width':512,'cell_height':512,
      'poses':[],'frame_scale':480/1338,'seat_sockets':[], 'duration_units':[2]*12,
      'method':'Twelve fresh rigid-seat pitch drawings; Aseprite pixel isolation, registration, fixed original frame and newly painted attached ropes. No blended or deformed source pose.'}
 angles=[0,4,8,12,8,4,0,-4,-8,-12,-8,-4]
 contacts=[]
 for n,angle in enumerate(angles):
  name='near_native.png' if n<6 else 'far_native.png';i=n%6
  origin=[i%2*512,i//2*512]
  a=np.array(Image.open(folder/name).convert('RGBA'))[origin[1]:origin[1]+512,origin[0]:origin[0]+512]
  core,keep,b=builder.main_component(a)
  rr,gg,bb=[a[:,:,k].astype(float) for k in range(3)]
  yy,xx=np.indices(core.shape)
  gold=core&(rr>100)&(gg>75)&(bb<rr*.72)&(rr>gg*1.08)&(yy<400)
  sockets=[]
  for side in [xx<180,xx>332]:
   lab,count=ndimage.label(gold&side);sizes=np.bincount(lab.ravel());sizes[0]=0
   assert count and sizes.max()>10,(n,'eyelet missing')
   ys,xs=np.where(lab==sizes.argmax())
   sockets.extend([float((xs.min()+xs.max())/2),float(ys.min()+3)])
  scale=.455
  center=(sockets[0]+sockets[2])/2
  dx=(sockets[2]-sockets[0])*scale/2-63.5
  target_y=118+math.sqrt((227*math.cos(math.radians(angle)))**2-dx**2)
  offset=[256-scale*center,target_y-scale*(sockets[1]+sockets[3])/2]
  cfg['poses'].append({'input':name,'origin':origin,'keep_runs':builder.runs(keep),'scale':scale,'offset':offset,'native_bounds':b,'pitch_direction_degrees':angle})
  cfg['seat_sockets'].append(sockets)
  targets=[[round(offset[0]+scale*sockets[k]),round(offset[1]+scale*sockets[k+1])] for k in [0,2]]
  contacts.append({'state':n,'native_eyelet_top':sockets,'painted_rope_endpoints':targets,'fixed_hooks':[[193,118],[320,118]],'tolerance_px':2.5,'pitch':'fore/aft; no roll or yaw','nominal_pitch_degrees':angle})
 write(folder/'IMPORT_PARAMETERS.json',cfg)
 run('--script-param','root='+ROOT.as_posix(),'--script-param','id=07_swing','--script',lua)
 run(folder/'07_swing.aseprite','--sheet',folder/'spritesheet.png','--data',folder/'spritesheet.json','--format','json-array','--sheet-type','rows','--sheet-width','2048','--sheet-height','2048')
 frames=sorted((folder/'frames').glob('frame_*.png'))
 write(folder/'AUTHORING_RECEIPT.json',{'id':'07_swing','status':'REFERENCE_SAMPLE','frame_canvas':[512,512],'unique_generated_pose_drawings':12,
   'method':cfg['method'],'loop_order':list(range(12)),'playback_duration_units_12fps':[2]*12,'state_rgba_sha256':[hashlib.sha256(Image.open(p).convert('RGBA').tobytes()).hexdigest() for p in frames],
   'inputs':{name:sha(folder/name) for name in ['near_native.png','far_native.png','identity_source.png']},'contacts':contacts,'limits':'Measured attachment and source-sheet topology review, not owner, runtime, device or cinematic acceptance. Nominal pitch is direction intent, not a calibrated 3D model.'})
 # Replace the defective bush drawings; preserve v2 originals in their archive.
 huck=ROOT/'objects/02_huckleberry'
 padded=huck/'padded_native.png'
 if padded.exists(): padded.unlink()
 builder.ROOT=ROOT
 builder.build_object(huck,True)
 # Freeze only the two berry clusters and their small local junction pixels.
 # The six fresh leaf silhouettes remain independent authored drawings.
 arrays=[np.array(Image.open(p).convert('RGBA')) for p in sorted((huck/'frames').glob('frame_*.png'))]
 berry=np.zeros((512,512),dtype=bool)
 for a in arrays:
  r,g,b=[a[:,:,k].astype(float) for k in range(3)]
  berry|=(a[:,:,3]>0)&(r>60)&(r>g*1.3)&(b>g*1.4)
 berry=ndimage.binary_dilation(berry,iterations=3)
 write(huck/'BERRY_LOCK.json',{'source_frame':'frames/frame_00.png','role':'Stationary berries and junction cleanup only; no animated pixels synthesized','source_rgba_sha256':hashlib.sha256(arrays[0].tobytes()).hexdigest(),'runs':builder.runs(berry)})
 run('--script-param','root='+ROOT.as_posix(),'--script',ROOT/'production/berry_lock.lua')
 run(huck/'02_huckleberry.aseprite','--sheet',huck/'spritesheet.png','--data',huck/'spritesheet.json','--format','json-array','--sheet-type','rows','--sheet-width','2048','--sheet-height','1024')
 receipt=json.loads((huck/'AUTHORING_RECEIPT.json').read_text())
 receipt['state_rgba_sha256']=[hashlib.sha256(Image.open(p).convert('RGBA').tobytes()).hexdigest() for p in sorted((huck/'frames').glob('frame_*.png'))]
 receipt['method']+=' Aseprite keeps exactly two three-berry clusters fixed while fresh leaf drawings flutter.'
 write(huck/'AUTHORING_RECEIPT.json',receipt)
 entries=json.loads((ROOT/'SAMPLES.json').read_text(encoding='utf-8'))
 phase={'02_huckleberry':7,'03_hydrangea':19,'04_bellflower':31,'05_cloud':3,'06_smoke':5,'08_seesaw':11}
 for e in entries:
  ident=e['id'];receipt=json.loads((ROOT/'objects'/ident/'AUTHORING_RECEIPT.json').read_text())
  e.update(count=len(receipt['state_rgba_sha256']),order=receipt['loop_order'],phase=phase.get(ident,0))
  e['durations']=[2]*12 if ident=='07_swing' else [2]*6 if ident=='06_smoke' else [4]*12 if ident=='10_glass' else [18,2,2,2,2,12,2,2,2,4] if ident=='09_gate' else [8]*6
  receipt['playback_duration_units_12fps']=e['durations'];receipt['reference_phase_units_12fps']=e['phase']
  write(ROOT/'objects'/ident/'AUTHORING_RECEIPT.json',receipt)
 write(ROOT/'SAMPLES.json',entries)
 run('--script-param','root='+ROOT.as_posix(),'--script',ROOT/'production/retime_keys.lua')
 cfg=json.loads((ROOT/'scene/SCENE_PARAMETERS.json').read_text())
 byid={e['id']:e for e in entries}
 for c in cfg['cards']:
  if c['id'] in byid:
   e=byid[c['id']];c.update(frames=e['count'],order=e['order'],durations=e['durations'],phase=e['phase'])
  if c['id']=='06_smoke':
   # Place emission on the visible upper cabin roof, with readable narrow smoke.
   scale=.18;a=np.array(Image.open(ROOT/'objects/06_smoke/frames/frame_00.png').convert('RGBA'))[:,:,3]
   ys,xs=np.where(a>0);c.update(scale=scale,x=1474-256*scale,y=136-int(ys.max())*scale)
 cfg['gate'].update(order=byid['09_gate']['order'],durations=byid['09_gate']['durations'])
 cfg['review_revision']='v3: fresh 12-state swing; stable two-cluster bush; independent phases and grounded equipment'
 cfg['shadow_contacts']=[{'id':'slide','center':[796.875,436],'radius':[77,6]}, {'id':'07_swing','center':[1000,433],'radius':[83,6]}, {'id':'08_seesaw','center':[1195.625,467],'radius':[28,5]}]
 write(ROOT/'scene/SCENE_PARAMETERS.json',cfg)
 run('--script-param','root='+ROOT.as_posix(),'--script',ROOT/'production/assemble_scene.lua')
 ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
 subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-framerate','12','-i',str(ROOT/'scene/frames/frame_%03d.png'),'-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'scene/sky_lagoon_sample.mp4')],check=True)
 print('v3 rebuilt: 72 isolated states and 48 context frames.',flush=True)

if __name__=='__main__': main()
