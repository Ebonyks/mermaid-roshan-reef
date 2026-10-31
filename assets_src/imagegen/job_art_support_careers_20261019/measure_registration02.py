from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from skimage.feature import SIFT,match_descriptors
from skimage.measure import ransac
from skimage.transform import SimilarityTransform
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019'
def landmarks(name,kind):
 im=Image.open(s/(name+'_native.png')).convert('RGBA');a=np.asarray(im.resize((512,512),Image.Resampling.LANCZOS));gray=(a[:,:,:3].mean(axis=2)/255)*(a[:,:,3]/255)
 f=SIFT();f.detect_and_extract(gray);p=f.keypoints[:,::-1];mask=np.ones(len(p),dtype=bool)
 if kind=='patient':mask &= ~((p[:,0]>355)&(p[:,1]<295))
 if kind=='pig':mask &= ~((p[:,0]>155)&(p[:,0]<370)&(p[:,1]<290))
 if kind=='portal':mask &= ((p[:,0]-256)**2/(190**2)+(p[:,1]-275)**2/(184**2)>1)
 if kind=='basin':mask &= ~((p[:,0]>135)&(p[:,0]<385)&(p[:,1]>175)&(p[:,1]<350))
 if kind=='hands':mask &= p[:,1]>280
 if kind=='gate':mask &= (p[:,1]<150)|((p[:,0]<105)|(p[:,0]>405))
 return p[mask],f.descriptors[mask],im.size
groups=[('patient','doctor_patient_base',['doctor_cast_1_retry','doctor_cast_2_retry','doctor_cast_3','doctor_bandage_1','doctor_bandage_2','doctor_bandage_3']),('basin','doctor_basin_off',['doctor_basin_running','doctor_basin_foamy']),('pig','farmer_pig_catch',['farmer_pig_chew','farmer_pig_happy']),('portal','magician_portal_closed',['magician_portal_quarter','magician_portal_half','magician_portal_open']),('scanner','doctor_scanner_idle',['doctor_scanner_found_retry']),('gate','farmer_barn_gate_closed',['farmer_barn_gate_open']),('hands','doctor_hands_ready_retry',['doctor_hands_wet','doctor_hands_rub_palms','doctor_hands_rub_backs'])]
rows=[]
for kind,ref,names in groups:
 p0,d0,sz0=landmarks(ref,kind)
 for name in names:
  p1,d1,sz1=landmarks(name,kind);matches=match_descriptors(d1,d0,max_ratio=.65,cross_check=True)
  if len(matches)<6:rows.append({'source':name,'reference':ref,'matches':len(matches),'status':'INSUFFICIENT_FIXED_FEATURES'});continue
  a=p1[matches[:,0]];b=p0[matches[:,1]]
  model,inliers=ransac((a,b),SimilarityTransform,min_samples=3,residual_threshold=2.0,max_trials=1000,rng=9)
  a=a[inliers];b=b[inliers];matrix=np.zeros((len(a)*2,3));matrix[::2,0]=a[:,0];matrix[1::2,0]=a[:,1];matrix[::2,1]=1;matrix[1::2,2]=1
  v=np.linalg.lstsq(matrix,b.reshape(-1),rcond=None)[0];pred=a*v[0]+v[1:];err=np.linalg.norm(pred-b,axis=1)
  row={'source':name,'reference':ref,'source_sha256':hashlib.sha256((s/(name+'_native.png')).read_bytes()).hexdigest(),'reference_sha256':hashlib.sha256((s/(ref+'_native.png')).read_bytes()).hexdigest(),'matches':len(matches),'inliers':len(a),'fixed_feature_domain':kind,'uniform_scale':float(v[0]),'translation_at_512':v[1:].tolist(),'rotation_diagnostic_degrees':float(np.degrees(model.rotation)),'median_residual_at_512':float(np.median(err)),'p95_residual_at_512':float(np.quantile(err,.95)),'landmarks_source_at_512':a.tolist(),'landmarks_reference_at_512':b.tolist(),'status':'MEASURED_GLOBAL_UNIFORM_ONLY_NOT_VISUAL_ACCEPTANCE'};rows.append(row);print(name,len(a),'scale',round(v[0],5),'tx/ty',v[1:].round(2),'p95',round(float(np.quantile(err,.95)),3),flush=True)
(s/'registration02.json').write_text(json.dumps({'method':'SIFT fixed source features -> robust similarity diagnostic -> constrained whole-picture uniform scale+translation fit. No part deformation/paint/alpha cleanup. Measured feature residual is not motion/identity/context acceptance.','records':rows},indent=2)+'\n')
