from pathlib import Path
from PIL import Image
import json,hashlib
B=Path(__file__).resolve().parent;W=B.parents[2];S=B/'whole_scene_revision/water_surface';O=W/'assets/sprites/sky_lagoon/whole_scene_v2'
data=json.loads((S/'PACKING.json').read_text(encoding='utf-8'))
for row in data['cards']:
 cw,ch=row['cell'];atlas=Image.new('RGBA',tuple(row['size']));scale=1/row['scale']
 for k in range(row['frames']):
  im=Image.open(S/row['id']/f'surface-{k:02d}.png').convert('RGBA');im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);atlas.alpha_composite(im,(k%row['columns']*cw+2,k//row['columns']*ch+2))
 target=O/('water_surface_'+row['id']+'.png');atlas.save(target)
 assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256'],target
print('WATER_SURFACE_PACK|two atlases reproduce recorded hashes')
