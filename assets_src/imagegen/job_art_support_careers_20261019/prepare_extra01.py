from pathlib import Path
import json,hashlib,importlib.util,shutil
import numpy as np
from PIL import Image
from skimage.feature import SIFT,match_descriptors
from skimage.measure import ransac
from skimage.transform import SimilarityTransform
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';out=r/'assets/opera/worlds/support_quality_20261019';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('measure',r/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old=s/'runtime_provenance01.json';d=json.loads(old.read_text('utf-8'));assert len(d['records'])==45;assert not (s/'runtime_provenance_pre_extra01.json').exists();shutil.copyfile(old,s/'runtime_provenance_pre_extra01.json')
new=[];registration=[]
def save(name,src,im,details):
 p=out/(name+'.png');assert not p.exists();im.save(p);row={'path':p.relative_to(r).as_posix(),'sha256':sha(p),'dimensions':list(im.size),'source':src.relative_to(r).as_posix(),'source_sha256':sha(src),'source_dimensions':list(Image.open(src).size),'technical_derivation':details,'cutout':m.cutout_profile(p.read_bytes()),'acceptance':'CANDIDATE_PENDING_CURRENT_CONTEXT_MOTION_4.5_DEVICE_OWNER'};new.append(row)
def features(src,kind):
 im=Image.open(src).convert('RGBA');assert im.width==im.height;ar=np.asarray(im.resize((512,512),Image.Resampling.LANCZOS));gray=ar[:,:,:3].mean(2)/255*ar[:,:,3]/255;f=SIFT();f.detect_and_extract(gray);xy=f.keypoints[:,::-1]
 mask=(xy[:,1]<330) if kind=='herd' else ((xy[:,1]>120)&~((xy[:,0]>140)&(xy[:,0]<365)&(xy[:,1]>160)&(xy[:,1]<345)))
 return xy[mask],f.descriptors[mask]
def register(src,ref,kind):
 a,da=features(src,kind);b,db=features(ref,kind);pairs=match_descriptors(da,db,max_ratio=.65,cross_check=True);assert len(pairs)>=12
 a=a[pairs[:,0]];b=b[pairs[:,1]];model,inside=ransac((a,b),SimilarityTransform,min_samples=3,residual_threshold=2,max_trials=1000,rng=11);a=a[inside];b=b[inside];mat=np.zeros((len(a)*2,3));mat[::2,0]=a[:,0];mat[1::2,0]=a[:,1];mat[::2,1]=1;mat[1::2,2]=1;v=np.linalg.lstsq(mat,b.reshape(-1),rcond=None)[0];errors=np.linalg.norm(a*v[0]+v[1:]-b,axis=1);row={'source':src.relative_to(r).as_posix(),'reference':ref.relative_to(r).as_posix(),'fixed_feature_domain':kind,'fixed_inliers':len(a),'uniform_scale':float(v[0]),'translation_at_512':v[1:].tolist(),'p95_residual_at_512':float(np.quantile(errors,.95)),'rotation_diagnostic_degrees':float(np.degrees(model.rotation)),'method':'Fixed-parts SIFT/ransac diagnostic; constrained whole-picture uniform scale+translation only. No perpart warp/paint/alpha cleanup.'};registration.append(row);print(src.stem,'inliers',len(a),'p95',row['p95_residual_at_512'],flush=True);return v
def whole(name,source,reference,kind):
 src=s/(source+'_native.png');ref=s/(reference+'_native.png');v=np.array([1.0,0,0]) if source==reference else register(src,ref,kind);im=Image.open(src).convert('RGBA');fit=.84;factor=512/im.width*v[0]*fit;size=(round(im.width*factor),round(im.height*factor));pos=(round(40.96+v[1]*fit),round(40.96+v[2]*fit));assert min(pos)>=0 and pos[0]+size[0]<=512 and pos[1]+size[1]<=512
 dest=Image.new('RGBA',(512,512));dest.alpha_composite(im.resize(size,Image.Resampling.LANCZOS),pos);save(name,src,dest,{'method':'Whole native canvas uniform downsample and common family padding/translation only. No clipping/source paint or alpha removal.','uniform_native_scale':factor,'output_whole_size':list(size),'output_origin':list(pos),'reference':reference,'registration_uniform_scale':float(v[0]),'registration_translation_at_512':v[1:].tolist()})
for state in ['concerned','sleepy','happy_cap']:whole('widget_find_doctor_'+state,'doctor_find_'+state,'doctor_patient_base','patient')
for state in ['a','b']:whole('widget_herd_farmer_'+state,'farmer_herd_step_'+state,'farmer_herd_step_a','herd')
original=r/'assets/opera/worlds/hotspots/magician_rope.png'
def caps(src):
 ar=np.asarray(Image.open(src).convert('RGBA')).astype(float);yy,xx=np.indices(ar.shape[:2]);mask=(ar[:,:,0]>180)&(ar[:,:,1]>100)&(ar[:,:,0]>ar[:,:,2]+20)&(ar[:,:,3]>200);pts=[]
 for region in [xx<ar.shape[1]*.15,xx>ar.shape[1]*.85]:
  selected=mask&region;assert selected.sum()>80;pts.append([float(xx[selected].mean()),float(yy[selected].mean())])
 return np.array(pts)
refcaps=caps(original)+[0,64]
im=Image.new('RGBA',(512,256));im.alpha_composite(Image.open(original).convert('RGBA'),(0,64));save('widget_rope_magician_0',original,im,{'method':'Exact source pixels padded vertically64px above/below; no resampling/alpha/paint changes.','output_origin':[0,64],'reference_body_canvas':[512,128]})
for key,source in [(1,'magician_rope_half'),(2,'magician_rope_untied')]:
 src=s/(source+'_native.png');pts=caps(src);mat=np.zeros((4,3));mat[::2,0]=pts[:,0];mat[1::2,0]=pts[:,1];mat[::2,1]=1;mat[1::2,2]=1;v=np.linalg.lstsq(mat,refcaps.reshape(-1),rcond=None)[0];im=Image.open(src).convert('RGBA');size=(round(im.width*v[0]),round(im.height*v[0]));pos=(round(v[1]),round(v[2]));assert min(pos)>=0 and pos[0]+size[0]<=512 and pos[1]+size[1]<=256,(source,size,pos,v)
 dest=Image.new('RGBA',(512,256));dest.alpha_composite(im.resize(size,Image.Resampling.LANCZOS),pos);save('widget_rope_magician_'+str(key),src,dest,{'method':'Whole native canvas uniformly resized/translated by two measured original goldshell cap sockets; padded512x256 contains every native source pixel, no paint/mask/clipping/warp. Original512x128body coordinates sit at y+64.','uniform_scale':float(v[0]),'output_whole_size':list(size),'output_origin':list(pos),'source_cap_centres':pts.tolist(),'reference_cap_centres_padded':refcaps.tolist(),'cap_residual_at_native_runtime':np.linalg.norm(pts*v[0]+v[1:]-refcaps,axis=1).tolist()})
assert len(new)==8;d['records']+=new;assert len(d['records'])==53;(s/'runtime_provenance02.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');(s/'extra_registration01.json').write_text(json.dumps({'records':registration,'limits':'Machine fixed-feature fit only; exact identity/topology/acting/contact/style/motion review separate.'},indent=2)+'\n',encoding='utf-8')
technical={'runtime_pictures':len(d['records']),'decoded_RGBA_bytes':sum(x['dimensions'][0]*x['dimensions'][1]*4 for x in d['records']),'profile_failures':[{'path':x['path'],'cutout':x['cutout']} for x in d['records'] if x['cutout']['verdict']!='CUTOUT_OK'],'records':[{'path':x['path'],'sha256':x['sha256'],'cutout':x['cutout']} for x in d['records']],'limits':'Inventory/alpha only, not deviceVRAM/FPS/motion/context acceptance.'};(s/'technical02.json').write_text(json.dumps(technical,indent=2)+'\n',encoding='utf-8')
p=r/'ASSET_LICENSES.md';t=p.read_text('utf-8')
for x in new:t+='\n| `'+x['path']+'` | '+x['source']+'; SHA256 '+x['source_sha256']+' | Original project source/reference rights and OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Technical whole uniform registration/padding only, runtime_provenance02.json. FinalSHA256 '+x['sha256']+'. Currentcontext/motion/owner pending. |'
p.write_text(t+'\n',encoding='utf-8');p=r/'design/audit_impacts/job-art-support-careers-20261019.json';impact=json.loads(p.read_text('utf-8'));impact['files']=sorted(set(impact['files']+[x['path'] for x in new]+[x.relative_to(r).as_posix() for x in s.rglob('*') if x.is_file()]));p.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8');print('Prepared53runtimePNGs; C2failures',[(x['path'],x['cutout']['verdict']) for x in d['records'] if x['cutout']['verdict']!='CUTOUT_OK'],flush=True)
