from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import numpy as np,json,zipfile,xml.etree.ElementTree as ET,io,hashlib,subprocess
p=Path('tmp/sky-lagoon-whole-scene-v2/grass-pointed-trial/blade-layers');frames=[Image.open(p/f'cel-{k:02d}.png').convert('RGBA') for k in range(4)];arrays=[np.asarray(f) for f in frames];assert len({a.tobytes() for a in arrays})==4
root=all(np.array_equal(a[375:],arrays[0][375:]) for a in arrays);assert root
fractions=[]
for a in arrays:
 ids,n=label(a[:,:,3]>64);sizes=np.bincount(ids.ravel())[1:];fractions.append(float(sizes.max()/sizes.sum()))
board=Image.new('RGB',(1280,900),'#334536');d=ImageDraw.Draw(board)
for k,f in enumerate(frames):
 pos=(k%2*640,k//2*450+24);board.paste(f,pos,f);d.text((pos[0]+8,pos[1]-18),['Rest','Wind right','Return left','Settle'][k],fill='white')
board.save(p/'four-poses.jpg',quality=95)
visible=[]
for f in frames:
 bg=Image.new('RGBA',f.size,'#334536');bg.alpha_composite(f);visible.append(bg.convert('RGB'))
visible[0].save(p/'four-pose-study.gif',save_all=True,append_images=visible[1:],duration=650,loop=0)
layers=json.loads((p/'LAYERS.json').read_text())['layers_front_to_back'];doc=ET.Element('image',w='640',h='426',name='Grass fan four pose alternatives',version='0.0.3');stack=ET.SubElement(doc,'stack')
with zipfile.ZipFile(p/'grass-fan-four-poses.ora','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for k in range(4):
  group=ET.SubElement(stack,'stack',name=f'Pose {k+1}',visibility='visible' if k==0 else 'hidden',opacity='1.0')
  for n in layers:
   name=f'data/{n}-{k}.png';z.writestr(name,(p/f'{n}-cel-{k:02d}.png').read_bytes());ET.SubElement(group,'layer',name=n,src=name,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(doc));z.writestr('mergedimage.png',(p/'cel-00.png').read_bytes())
script="local s=app.open(app.params.file);assert(#s.frames==4 and #s.layers==8);for k=1,4 do assert(math.abs(s.frames[k].duration-.65)<.001);local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,k);im:saveAs(app.params.out..string.format('/reopened-%02d.png',k-1)) end;s:close();print('NATIVE_GRASS|4frames8layers|PASS')"
(p/'verify.lua').write_text(script,encoding='utf-8');r=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','file='+str((p/'grass-fan-four-cels.aseprite').resolve()),'--script-param','out='+str(p.resolve()),'--script',str((p/'verify.lua').resolve())],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120);assert r.returncode==0
for k,a in enumerate(arrays):assert np.array_equal(a,np.asarray(Image.open(p/f'reopened-{k:02d}.png').convert('RGBA')))
report={'status':'SOURCE_TRIAL_NOT_RUNTIME_ACCEPTED','frames':4,'layers':8,'frame_duration_seconds':.65,'unique_frames':4,'fixed_root_rows':[375,426],'fixed_roots_exact':root,'largest_alpha_component_fraction':fractions,'native_reopen_pixel_exact':True,'ora':'Four alternative pose groups,32layers; not a native Krita animation timeline','remaining':['Inspect internal blade boundaries for borrowed neighbor pixels and cracks','Evaluate at actual foreground display scale with soil and paths','Do not reuse as cloned broad lawn coverage'],'source_hash':hashlib.sha256((p.parent/'rest-native.png').read_bytes()).hexdigest()};(p/'MOTION_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
