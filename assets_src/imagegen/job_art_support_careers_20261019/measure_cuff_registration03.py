from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019'
names=['doctor_hands_ready_retry','doctor_hands_wet','doctor_hands_rub_palms','doctor_hands_rub_backs'];points={};rows=[]
for name in names:
 im=Image.open(s/(name+'_native.png')).convert('RGBA').resize((512,512),Image.Resampling.LANCZOS);a=np.asarray(im).astype(int);yy,xx=np.indices(a.shape[:2]);mask=(a[:,:,0]>225)&(a[:,:,0]-a[:,:,1]>95)&(a[:,:,1]>75)&(a[:,:,1]<155)&(abs(a[:,:,2]-a[:,:,1])<18)&(a[:,:,3]>240)&(yy>290)
 centres=[]
 for side in [xx<256,xx>=256]:
  lab,count=label(mask&side);areas=np.bincount(lab.ravel());areas[0]=0;assert count>0;chosen=lab==np.argmax(areas);assert chosen.sum()>120
  centres.append([float(xx[chosen].mean()),float(yy[chosen].mean())])
 points[name]=np.array(centres)
ref=points[names[0]]
for name in names:
 a=points[name];mat=np.zeros((4,3));mat[::2,0]=a[:,0];mat[1::2,0]=a[:,1];mat[::2,1]=1;mat[1::2,2]=1;v=np.linalg.lstsq(mat,ref.reshape(-1),rcond=None)[0];errors=np.linalg.norm(a*v[0]+v[1:]-ref,axis=1)
 row={'source':name,'reference':names[0],'source_sha256':hashlib.sha256((s/(name+'_native.png')).read_bytes()).hexdigest(),'uniform_scale':float(v[0]),'translation_at_512':v[1:].tolist(),'cuff_centres_at_512':a.tolist(),'reference_cuff_centres_at_512':ref.tolist(),'residual_per_cuff_at_512':errors.tolist(),'method':'Two separately measured original coral cuff stripe largest connected components; whole-pair uniform scale+translation only, no part warp/alpha/paint change. Source pixels merely measured, never changed. SIFT hands low confidence/left-right near-identical texture matches rejected; original measurement retained.','status':'MEASURED_REGISTRATION_NOT_MOTION_ACCEPTANCE'};rows.append(row);print(name,'centres',a.round(2),'scale',round(v[0],5),'translation',v[1:].round(2),'errors',errors.round(3),flush=True)
(s/'cuff_registration03.json').write_text(json.dumps({'records':rows},indent=2)+'\n')
