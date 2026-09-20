from pathlib import Path
import ast,json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
w=Path.cwd(); b=w/'assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20'; a=b/'whole_scene_revision/ambient_motion_v3'; out=a/'rendered_color_audit'; cap=w/'tmp/sky-lagoon-whole-scene-v2/ambient-v3-gpu'
tree=ast.parse((b/'build_six_screen_color_audit.py').read_text()); ns={'np':np}
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATCHES' for t in node.targets): exec(compile(ast.Module(body=[node],type_ignores=[]),'patches','exec'),ns)
 if isinstance(node,ast.FunctionDef) and node.name=='measure': exec(compile(ast.Module(body=[node],type_ignores=[]),'measure','exec'),ns)
names=['AUDIT.json','day-night-board.jpg','sample-map.jpg','capture.gd','capture.log','reproduce.py']+[f'{s}_{m}.png' for s in ns['PATCHES'] for m in ['day','night']]
impact=w/'design/audit_impacts/sky-lagoon-animated-rebuild-20260920.json'; d=json.loads(impact.read_text()); d['files']=sorted(set(d['files']+[str((out/n).relative_to(w)).replace('\\','/') for n in names])); impact.write_text(json.dumps(d,indent=2)+'\n')
out.mkdir(parents=True,exist_ok=True)
board=Image.new('RGB',(1280,1140),'#202830'); marked=Image.new('RGB',(1280,2160)); rows=[]; sources=[]
for i,(stage,patches) in enumerate(ns['PATCHES'].items()):
 data={}
 for col,mode in enumerate(['day','night']):
  pattern=f'canvas_screen_{i+1}_day_0_*.png' if mode=='day' else f'canvas_screen_3_night_{i}_*.png'
  paths=sorted(cap.glob(pattern)); assert len(paths)==48,(pattern,len(paths))
  data[mode]={key:[] for key in patches}
  for p in paths:
   im=Image.open(p).convert('RGB'); sources.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
   for key,box in patches.items(): data[mode][key].append(ns['measure'](im,box))
  first=Image.open(paths[0]).convert('RGB'); first.save(out/f'{stage}_{mode}.png'); board.paste(first.resize((640,360)),(col*640,i*380)); ImageDraw.Draw(board).text((col*640+8,i*380+363),f'{stage} / {mode}',fill='white')
  if mode=='day':
   draw=ImageDraw.Draw(first)
   for key,box in patches.items(): draw.rectangle(box,outline='red',width=2);draw.text((box[0],box[1]-12),key,fill='red',stroke_width=1,stroke_fill='white')
   marked.paste(first,(0,i*720))
 for key,box in patches.items():
  row={'stage':stage,'material':key,'rect_xyxy':box}
  for mode in ['day','night']:
   samples=data[mode][key]; row[mode]={k:{'median':round(float(np.median([s[k] for s in samples])),5),'min':min(s[k] for s in samples),'max':max(s[k] for s in samples)} for k in ['luminance_median','HSV_saturation_median']}
  rows.append(row)
board.save(out/'day-night-board.jpg',quality=94); marked.save(out/'sample-map.jpg',quality=94)
shutil.copy2(cap/'capture.gd',out/'capture.gd'); shutil.copy2(cap/'stdout.txt',out/'capture.log'); shutil.copy2(Path(__file__),out/'reproduce.py')
report={'status':'OPEN_COLOR_REVIEW_NOT_VISUAL_ACCEPTANCE','coverage':'288 actual Mobile-rendered captures, three stages x day/night x 48 samples over 4.7 seconds; 31 fixed material patches. All declared whole-scene card cels observed. Not a full 48-second cloud drift loop or all interactive states.','method':'Linear-light Rec.709 luminance and HSV saturation in fixed unmasked rectangles. Temporal min/max includes movement and mixed materials, so is not a direct palette-flicker measurement. Original images remain unchanged; corrections stay opt-in.','rollback_commit':'5ac764729fe0f6fc2152afcc37aa83fd6df7a400','capture_hashes':sources,'samples':rows,'findings':[{'priority':'P1','issue':'Foreground/background foliage coherence','action':'Compare matching plant families and painted highlight/shadow bands; selectively compress foreground highlights and align hue only where contextual review supports it. Do not globally equalize saturation or remove atmospheric depth.'},{'priority':'P1','issue':'Arrival foliage differs from meadow/castle','action':'Review matching species at camera seams; existing source samples show larger arrival saturation, but different species/shade prevent a universal numeric target.'},{'priority':'P1','issue':'Animation coverage remains incomplete','action':'Remaining eight cloud cards have one cel plus drift; low cloud sea and broad lawn remain insufficiently animated. New pointed tuft covers only one foreground accent.'},{'priority':'P2','issue':'Night emission and interaction colors','action':'Separate windows/glints from opaque prop ambient grade; capture water ripple peak/fade, bridge contact, actors, animals and touch cues before claiming complete color coverage.'}],'acceptance':'No quality score assigned. Last owner score remains 3.5/5. Device performance, owner visual acceptance, all interactions and complete material isolation remain open.'}
(out/'AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
licensefile=w/'ASSET_LICENSES.md'
with licensefile.open('a',encoding='utf-8') as f:
 for n in names:
  if Path(n).suffix in ['.png','.jpg']: f.write(f'\n- `{(out/n).relative_to(w).as_posix()}` — Local Godot Mobile render of existing project Sky Lagoon assets; inherited source provenance/licenses; URL: local project; modification: diagnostic capture/board only, non-runtime.\n')
for stage in ns['PATCHES']:
 r={x['material']:x for x in rows if x['stage']==stage}; print(stage,'pale/rear luminance',round(r['pale_foreground_clump']['day']['luminance_median']['median']/r['rear_hedge']['day']['luminance_median']['median'],3))
print(out)
