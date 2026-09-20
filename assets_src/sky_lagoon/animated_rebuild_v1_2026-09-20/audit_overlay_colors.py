from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
W=Path.cwd();B=Path(__file__).resolve().parent;O=B/'whole_scene_revision/color_audit';A='assets/sprites/sky_lagoon/animated_v1/'
specs=[('grass',A+'grass_breeze.png',2,2,4),('bellflower',A+'bellflower_breeze.png',4,2,8),('huckleberry',A+'huckleberry_breeze.png',4,2,8),('conifer',A+'conifer_breeze.png',3,2,6),('bridge',A+'bridge_contact.png',4,3,12),('chains',A+'bridge_chains.png',4,3,12),('arrival_highlights',A+'water_arrival_highlights.png',4,3,12),('castle_highlights',A+'water_castle_highlights.png',4,4,12),('arrival_shore',A+'water_arrival_shore.png',4,2,8),('castle_shore',A+'water_castle_shore.png',4,2,8),('touch_ripple','assets/sprites/fx_water/fx_water_ripple_ring_atlas.png',4,2,8)]
rows=[]
for name,path,cols,rws,count in specs:
 im=Image.open(W/path).convert('RGBA');cw,ch=im.width//cols,im.height//rws;frames=[]
 for k in range(count):
  cel=im.crop((k%cols*cw,k//cols*ch,(k%cols+1)*cw,(k//cols+1)*ch));a=np.asarray(cel)/255.;rgb=a[:,:,:3];alpha=a[:,:,3];hsv=np.asarray(cel.convert('HSV'))/255.;mass=float(alpha.sum());linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4);lum=linear@np.array([.2126,.7152,.0722]);weight=max(mass,1e-9)
  frames.append({'frame':k,'alpha_mass':round(mass,2),'alpha_weighted_HSV_saturation':round(float((hsv[:,:,1]*alpha).sum()/weight),5),'alpha_weighted_linear_luminance':round(float((lum*alpha).sum()/weight),5),'visible_rgb_mean':[round(float(v),5) for v in (rgb*alpha[:,:,None]).sum(axis=(0,1))/weight]})
 nonempty=[f for f in frames if f['alpha_mass']>0];ranges={key:round(max(f[key] for f in nonempty)-min(f[key] for f in nonempty),5) for key in ['alpha_weighted_HSV_saturation','alpha_weighted_linear_luminance']}
 rows.append({'id':name,'path':path,'sha256':hashlib.sha256((W/path).read_bytes()).hexdigest(),'grid':[cols,rws],'active_frames':count,'frames':frames,'ranges':ranges})
r={'status':'SOURCE_OVERLAY_MEASUREMENTS_NOT_COLOR_ACCEPTANCE','active_atlases':len(rows),'active_cels':sum(x['active_frames'] for x in rows),'method':'Alpha-weighted source RGB/HSV and linear luminance per active cel; no transparent RGB or unused atlas cells included. These are source statistics, not rendered color judgments.','overlays':rows,'limits':['Intentional water opacity and changing visible leaf coverage can change these statistics without color drift','Static castle/playground/sky/mountain materials and protected actor contrast need rendered review','Do not recolor protected art or equalize material distributions based on averages'],'next':'Use measured high-contrast material groups to guide local before/after rendered comparisons, including daylight foliage intensity.'};(O/'OVERLAY_COLORS.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
for row in rows:print(row['id'],row['active_frames'],row['ranges'])
