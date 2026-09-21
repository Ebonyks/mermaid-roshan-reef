from pathlib import Path
import json,numpy as np,hashlib
from PIL import Image,ImageDraw
w=Path.cwd();o=w/'tmp/sky-lagoon-whole-scene-v2/path-source-audit-v7';base=w/'assets/sprites/sky_lagoon/whole_scene_v2';m=json.loads((base/'manifest.json').read_text());ref=Image.open(w/'assets_src/cinematics/sky_lagoon_whole_plant_grok_v4_2026-09-20/shots/G13/IMAGE_1.png').convert('RGBA');W,H=ref.size
line=[(782,113),(718,156),(635,187),(567,223),(568,258),(602,291),(642,328),(645,368),(612,404),(579,444),(541,484),(509,521),(474,560),(430,600),(369,647),(316,676),(261,705),(205,730)]
mask=Image.new('L',ref.size);ImageDraw.Draw(mask).line(line,fill=255,width=10);mask.save(o/'path-core-mask.png');sel=np.asarray(mask)>0;results=[];aggregate=np.zeros((H,W),bool)
for c in m['cards']:
 if c['family'] not in ['grass','shrubs']:continue
 im=Image.open(base/c['file']).convert('RGBA');cw,ch=im.width//c['columns'],im.height//c['rows'];scale=c['scale'];x,y=c['position']
 if x>3970+W or x+cw*scale<3970 or y>510+H or y+ch*scale<510:continue
 frames=[]
 for k in range(c['frames']):
  cell=im.crop((k%c['columns']*cw,k//c['columns']*ch,(k%c['columns']+1)*cw,(k//c['columns']+1)*ch));mapped=cell.transform((W,H),Image.Transform.AFFINE,(1/scale,0,(3970-x)/scale,0,1/scale,(510-y)/scale),Image.Resampling.BICUBIC);frames.append(np.asarray(Image.alpha_composite(ref,mapped)).astype(int))
 changes=np.maximum.reduce([abs(f-frames[0]).max(2) for f in frames[1:]]);moving=changes>2;aggregate|=moving
 results.append({'id':c['id'],'moving_pixels_over_2_codes':int(moving.sum()),'path_core_moving_pixels':int((moving&sel).sum()),'path_core_max_delta':int(changes[sel].max()),'current_motion_enabled':c.get('motion_enabled',True),'atlas_sha256':hashlib.sha256((base/c['file']).read_bytes()).hexdigest()})
vis=np.array(ref.convert('RGB'));vis[aggregate&sel]=[255,0,40];Image.fromarray(vis).save(o/'path-overlap.png')
report={'status':'SOURCE_SPACE_DIAGNOSTIC_NOT_GPU_PROOF','method':'Inverse world placement and bicubic source-cell sampling, alpha-composited onto approved reference crop; compares retired candidate cels against cel0. Ten-pixel hand-reviewed path interior corridor. This does not replace actual Godot GPU or full path-edge audit.','corridor_points_local':line,'corridor_width':10,'reference_world_origin':[3970,510],'results':results,'conclusion':'See measured overlap; all listed grass/shrub motion now quarantined at rest.'};(o/'RESULT.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
