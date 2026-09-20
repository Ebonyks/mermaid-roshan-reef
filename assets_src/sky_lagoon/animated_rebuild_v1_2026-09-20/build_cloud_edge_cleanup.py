from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage as nd
import numpy as np,json,hashlib
W=Path.cwd();src=W/'assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/clouds';out=src/'cleaned';out.mkdir(exist_ok=True)
rows=json.loads((src/'SOURCE.json').read_text(encoding='utf-8'))['clouds'];records=[];board=Image.new('RGB',(1000,180*len(rows)),(48,48,60));draw=ImageDraw.Draw(board)
for i,row in enumerate(rows):
 im=Image.open(src/row['file']).convert('RGBA');a=np.asarray(im).astype(float);rgb=a[:,:,:3];mask=a[:,:,3]>0;inside=nd.distance_transform_edt(mask);core=inside>=6
 _,fi=nd.distance_transform_edt(~core,return_indices=True);_,bi=nd.distance_transform_edt(mask,return_indices=True);fg=rgb[fi[0],fi[1]];bg=rgb[bi[0],bi[1]];v=fg-bg
 alpha=np.clip(((rgb-bg)*v).sum(2)/(v*v).sum(2).clip(1),0,1);alpha[core]=1;alpha[~mask]=0
 color=np.clip((rgb-bg*(1-alpha[:,:,None]))/np.maximum(alpha[:,:,None],.001),0,255);color[core]=rgb[core];rgba=np.dstack((np.rint(color),np.rint(alpha*255))).astype('uint8');rgba[~mask,:3]=0
 clean=Image.fromarray(rgba);clean.save(out/row['file'])
 coreerror=int(np.abs(rgba[:,:,:3].astype('int16')[core]-rgb.astype('int16')[core]).max());assert coreerror==0
 oldcyan=mask&((rgb[:,:,1]-rgb[:,:,0])>45)&((rgb[:,:,2]-rgb[:,:,0])>65);newcyan=(rgba[:,:,3]>127)&((rgba[:,:,1].astype(int)-rgba[:,:,0])>45)&((rgba[:,:,2].astype(int)-rgba[:,:,0])>65)
 records.append({'id':row['id'],'rect':row['rect'],'file':row['file'],'protected_core_pixels':int(core.sum()),'core_rgb_max_error':coreerror,'old_opaque_cyan_pixels':int(oldcyan.sum()),'new_majority_alpha_cyan_pixels':int(newcyan.sum()),'source_sha256':hashlib.sha256((src/row['file']).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((out/row['file']).read_bytes()).hexdigest()})
 for j,variant in enumerate([im,clean]):
  bgim=Image.new('RGBA',variant.size,(48,48,60,255));bgim.alpha_composite(variant);bgim.thumbnail((480,140));board.paste(bgim.convert('RGB'),(j*500,i*180+30));draw.text((j*500+8,i*180+8),row['id']+(' - original edge' if j==0 else ' - matte cleanup'),fill='white')
board.save(out/'all-cloud-edges.jpg',quality=94)
report={'status':'SOURCE_EDGE_CLEANUP_CANDIDATE','method':'Boundary-only color unmixing against nearest exterior sky and protected interior cloud pixels; existing silhouette support retained, no new generation','runtime_changed':False,'clouds':records,'limits':['Low cloud sea and mountain-overlap clouds not included','Exterior sky estimate can be imperfect where silhouettes are very thin','Runtime drift and rest-recomposition review remains required; no acceptance claim']}
(out/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('CLOUD_EDGE',len(records),'core exact',all(r['core_rgb_max_error']==0 for r in records),'cyan before',sum(r['old_opaque_cyan_pixels'] for r in records),'after',sum(r['new_majority_alpha_cyan_pixels'] for r in records))
