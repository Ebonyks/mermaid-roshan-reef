from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image
B=Path('assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20');G=B/'whole_scene_revision/grass';tmp=Path('tmp/sky-lagoon-whole-scene-v2/grass-export-check');tmp.mkdir(exist_ok=True)
rows=json.loads((G/'SOURCE.json').read_text())['regions'];results=[]
for row in rows:
 p=G/row['id'];sheet_path=tmp/(row['id']+'.png');json_path=tmp/(row['id']+'.json')
 subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b',str(p/'grass-four-cels.aseprite'),'--sheet',str(sheet_path),'--sheet-columns','2','--data',str(json_path),'--format','json-array'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 sheet=Image.open(sheet_path).convert('RGBA');frames=json.loads(json_path.read_text())['frames'];errors=[]
 for i,frame in enumerate(frames):
  r=frame['frame'];export=np.array(sheet.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h'])));expected=np.array(Image.open(p/f'frame-{i:02d}.png'));errors.append(int(np.abs(export.astype(int)-expected.astype(int)).max()))
 assert len(errors)==4 and max(errors)<=1,(row['id'],errors)
 results.append({'id':row['id'],'frames':4,'max_errors':errors})
(G/'ASEPRITE_EXPORT_CHECK.json').write_text(json.dumps({'result':'PASS','regions':results,'scope':'All 28 timeline exports differ by at most one 8-bit channel level due to Pillow/Aseprite alpha compositing rounding. Does not prove visual quality or broad coverage.'},indent=2)+'\n',encoding='utf-8')
print('GRASS_EXPORT|28 Aseprite cels within one channel level|PASS')
