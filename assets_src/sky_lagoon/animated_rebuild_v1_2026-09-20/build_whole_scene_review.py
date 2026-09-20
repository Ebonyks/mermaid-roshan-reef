from pathlib import Path
import json,subprocess,io,zipfile
import numpy as np
from PIL import Image
from xml.etree import ElementTree as ET
B=Path('assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20');G=B/'whole_scene_revision/grass';data=json.loads((G/'SOURCE.json').read_text());ase='C:/Program Files/Aseprite/Aseprite.exe'
for row in data['regions']:
 p=G/row['id'];w,h=row['rect'][2:]
 lua=f"local p=app.params.base\nlocal s=Sprite({w},{h},ColorMode.RGB)\nlocal soil=s.layers[1];soil.name='fixed_soil';local blades=s:newLayer();blades.name='painted_blades'\nfor k=0,3 do if k>0 then s:newEmptyFrame() end;s.frames[k+1].duration=.35\nfor j,name in ipairs({{'soil-fixed.png',string.format('blades-%02d.png',k)}}) do local t=app.open(p..'/'..name);local c=t.cels[1];local im=Image({w},{h},ColorMode.RGB);im:drawImage(c.image,c.position);t:close();s:newCel(j==1 and soil or blades,k+1,im,Point(0,0)) end end\napp.activeSprite=s;s:newTag(1,4).name='painted_grass_breeze';s:saveAs(p..'/grass-four-cels.aseprite');s:close()\n"
 (p/'assemble.lua').write_text(lua,encoding='utf-8');subprocess.run([ase,'-b','--script-param','base='+str(p.resolve()).replace('\\','/'),'--script',str(p/'assemble.lua')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
# Preview only: source stage composition, not a Godot capture.
O=Path('tmp/sky-lagoon-whole-scene-review');O.mkdir(parents=True,exist_ok=True)
C=B/'whole_scene_revision/clouds';T=B/'whole_scene_revision/tree';clouds=json.loads((C/'SOURCE.json').read_text())['clouds'];clean=Image.open(C/'sky-clouds-removed-candidate.png').convert('RGBA');treebase=Image.open(T/'underpaint-candidate.png').convert('RGBA');clean.paste(treebase,(0,0),Image.open(T/'original-tree-rest.png').getchannel('A'))
overlays=[]
for name in ['arrival','meadow','castle']:
 overlay=Image.new('RGBA',(2048,2048))
 with zipfile.ZipFile(B/'stage_masters'/(name+'-editable.ora')) as z:
  layers=list(ET.fromstring(z.read('stack.xml')).iter('layer'))
  for n in reversed(layers):
   nm=n.attrib['name']
   if nm.startswith('Original') or 'ArrivalBoughCels' in nm or 'RearCloud' in nm or 'GrassCels' in nm:continue
   overlay.alpha_composite(Image.open(io.BytesIO(z.read(n.attrib['src']))).convert('RGBA'),(int(n.attrib.get('x',0)),int(n.attrib.get('y',0))))
 overlays.append(overlay)
S=B/'whole_scene_revision/shrubs';shrubs=json.loads((S/'SOURCE.json').read_text())['regions']
for k in range(12):
 frame=clean.copy()
 for i,row in enumerate(clouds):
  x,y,w,h=row['rect'];dx=round(np.sin(k*2*np.pi/12)*(14+(i%3)*5));frame.alpha_composite(Image.open(C/row['file']).convert('RGBA'),(x+dx,y))
 frame.alpha_composite(Image.open(T/f'frame-{k:02d}.png').convert('RGBA'),(0,0))
 for row in data['regions']:
  x,y,w,h=row['rect'];frame.paste(Image.open(G/row['id']/f'frame-{k//3:02d}.png').convert('RGBA'),(x,y))
 for row in shrubs:
  x,y,w,h=row['rect'];frame.paste(Image.open(S/row['id']/f'frame-{k//3:02d}.png').convert('RGBA'),(x,y))
 for j,name in enumerate(['arrival','meadow','castle']):
  stage=frame.crop((j*2048,0,(j+1)*2048,2048));stage.alpha_composite(overlays[j]);stage.resize((896,896)).convert('RGB').save(O/f'{name}-{k:02d}.jpg',quality=94)
html='''<!doctype html><meta charset="utf-8"><title>Sky Lagoon whole-scene motion study</title><style>body{background:#17232b;color:#edf5f7;font:17px system-ui;margin:24px}button,input{font:inherit}main{display:flex;gap:12px;flex-wrap:wrap}figure{margin:0;flex:1;min-width:350px}img{width:100%}p{max-width:1000px}strong{color:#ffd289}</style><h1>Whole-scene source motion study</h1><p><strong>Unaccepted source preview, not a Godot capture.</strong> Original full visible tree: 12 baked poses. Twelve separated clouds: drift study. Painted grass: four poses across seven regions. Other objects are held at rest. Six shrub groups now have four-pose canopy studies. Mountain-overlap clouds remain unfinished; other objects are held at rest.</p><p><button id="play">Pause</button> <button id="rest">Rest pose</button> <input id="frame" type="range" min="0" max="11" value="0"> <span id="count"></span></p><main>'''
for name in ['arrival','meadow','castle']:html+=f'<figure><figcaption>{name.title()}</figcaption><img id="{name}" src="{name}-00.jpg"></figure>'
html+='''</main><p>Review full-object motion, grass shimmer, exposed fill and path clarity. No quality score is asserted. Source artwork and rollback remain preserved.</p><script>let k=0,playing=true;function show(){for(const n of ['arrival','meadow','castle'])document.getElementById(n).src=n+'-'+String(k).padStart(2,'0')+'.jpg';frame.value=k;count.textContent='Frame '+(k+1)+' / 12'}play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};rest.onclick=()=>{playing=false;k=0;play.textContent='Play';show()};frame.oninput=()=>{playing=false;k=+frame.value;play.textContent='Play';show()};setInterval(()=>{if(playing){k=(k+1)%12;show()}},300);show()</script>'''
(O/'index.html').write_text(html,encoding='utf-8');print('PREVIEW',O/'index.html')
