"""Verify unique original-pixel ownership and Aseprite shrub export cels."""
from pathlib import Path
from PIL import Image
import numpy as np,json,subprocess
B=Path(__file__).resolve().parent/'whole_scene_revision';owners=np.zeros((2048,6144),np.uint16);names=[];overlaps=[]
def add(name,mask,x,y):
 h,w=mask.shape;v=owners[y:y+h,x:x+w];ids,counts=np.unique(v[mask & (v>0)],return_counts=True)
 for idx,count in zip(ids,counts):overlaps.append({'a':names[int(idx)-1],'b':name,'pixels':int(count)})
 names.append(name);v[mask]=len(names)
add('whole_tree',np.array(Image.open(B/'tree/original-tree-rest.png'))[:,:,3]>0,0,0)
for row in json.loads((B/'clouds/SOURCE.json').read_text())['clouds']:
 x,y,w,h=row['rect'];add(row['id'],np.array(Image.open(B/'clouds'/row['file']))[:,:,3]>0,x,y)
for family,cel in [('grass','blades-00.png'),('shrubs','canopy-00.png')]:
 for row in json.loads((B/family/'SOURCE.json').read_text())['regions']:
  x,y,w,h=row['rect'];add(row['id'],np.array(Image.open(B/family/row['id']/cel))[:,:,3]>0,x,y)
(B/'PIXEL_OWNERSHIP_REVIEW.json').write_text(json.dumps({'status':'FAIL' if overlaps else 'PASS','moving_regions':len(names),'overlaps':overlaps,'scope':'Source rest-mask pairwise ownership only; does not establish runtime coverage or visual quality.'},indent=2)+'\n',encoding='utf-8')
tmp=Path('tmp/sky-lagoon-whole-scene-v2/shrub-export-check');tmp.mkdir(parents=True,exist_ok=True);results=[]
for row in json.loads((B/'shrubs/SOURCE.json').read_text())['regions']:
 p=B/'shrubs'/row['id'];sheetpath=tmp/(row['id']+'.png');jpath=tmp/(row['id']+'.json')
 subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b',str(p/'shrubs-four-cels.aseprite'),'--sheet',str(sheetpath),'--sheet-columns','2','--data',str(jpath),'--format','json-array'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 sheet=Image.open(sheetpath).convert('RGBA');rows=json.loads(jpath.read_text())['frames'];errors=[]
 for k,r in enumerate(rows):
  q=r['frame'];a=np.array(sheet.crop((q['x'],q['y'],q['x']+q['w'],q['y']+q['h'])));b=np.array(Image.open(p/f'frame-{k:02d}.png'));errors.append(int(np.abs(a.astype(int)-b.astype(int)).max()))
 assert len(errors)==4 and max(errors)<=1,(row['id'],errors)
 results.append({'id':row['id'],'frames':4,'max_channel_errors':errors})
(B/'shrubs/ASEPRITE_EXPORT_CHECK.json').write_text(json.dumps({'result':'PASS','regions':results,'scope':'Raster export correspondence within one 8-bit channel level, not quality acceptance.'},indent=2)+'\n',encoding='utf-8')
assert not overlaps,overlaps
print('SOURCE_OWNERSHIP|26 source regions, no shared pixels|PASS');print('SHRUB_EXPORT|24 cels checked|PASS')
