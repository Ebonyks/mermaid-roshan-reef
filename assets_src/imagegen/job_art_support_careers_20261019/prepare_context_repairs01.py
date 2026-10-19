"""Whole-canvas registration/downsampling only; no pixel painting or matte repair."""
from pathlib import Path
import hashlib,json,importlib.util
import numpy as np
from PIL import Image
from skimage.feature import SIFT,match_descriptors
from skimage.measure import ransac
from skimage.transform import SimilarityTransform
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';out=r/'assets/opera/worlds/support_quality_20261019'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('measure',r/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
reference=r/'assets/opera/worlds/widgets/widget_magic_cabinet_reveal.png'
target=s/'magician_cabinet_painted_lamb_native.png'
def features(p):
 im=np.asarray(Image.open(p).convert('RGBA').resize((512,512),Image.Resampling.LANCZOS));gray=im[:,:,:3].mean(axis=2)/255*im[:,:,3]/255
 f=SIFT();f.detect_and_extract(gray);pts=f.keypoints[:,::-1];mask=~((pts[:,0]>140)&(pts[:,0]<365)&(pts[:,1]>175)&(pts[:,1]<350))
 return pts[mask],f.descriptors[mask]
p0,d0=features(reference);p1,d1=features(target);matches=match_descriptors(d1,d0,max_ratio=.65,cross_check=True)
a=p1[matches[:,0]];b=p0[matches[:,1]];model,inside=ransac((a,b),SimilarityTransform,min_samples=3,residual_threshold=2,max_trials=1000,rng=9);a=a[inside];b=b[inside];assert len(a)>20
matrix=np.zeros((len(a)*2,3));matrix[::2,0]=a[:,0];matrix[1::2,0]=a[:,1];matrix[::2,1]=1;matrix[1::2,2]=1
v=np.linalg.lstsq(matrix,b.reshape(-1),rcond=None)[0];err=np.linalg.norm(a*v[0]+v[1:]-b,axis=1)
registration={'reference':reference.relative_to(r).as_posix(),'source':target.relative_to(r).as_posix(),'fixed_domain':'Cabinet outside original rectangular lamb opening only','inliers':len(a),'uniform_scale':float(v[0]),'translation_at512':v[1:].tolist(),'p95_residual_at512':float(np.quantile(err,.95)),'limits':'Whole-canvas global registration only; no source patching or alpha cleanup; human/context/motion review separate.'}
(s/'cabinet_registration01.json').write_text(json.dumps(registration,indent=2)+'\n',encoding='utf-8')
records=json.loads((s/'runtime_provenance03.json').read_text())['records']
new=[]
for name,src,side,scale,tx,ty in [('widget_lamba_magician',s/'magician_lamba_painted_native.png',512,1,0,0),('widget_stamp_painter',s/'painter_stamp_coral_native.png',256,1,0,0),('widget_cabinet_magician_reveal',target,512,float(v[0]),float(v[1]),float(v[2]))]:
 im=Image.open(src).convert('RGBA');factor=side/im.width*scale;sz=(round(im.width*factor),round(im.height*factor));pos=(round(tx*side/512),round(ty*side/512));assert min(pos)>=0 and pos[0]+sz[0]<=side and pos[1]+sz[1]<=side,(name,pos,sz)
 dest=Image.new('RGBA',(side,side));dest.alpha_composite(im.resize(sz,Image.Resampling.LANCZOS),pos);p=out/(name+'.png');assert not p.exists();dest.save(p)
 row={'path':p.relative_to(r).as_posix(),'sha256':sha(p),'dimensions':[side,side],'source':src.relative_to(r).as_posix(),'source_sha256':sha(src),'source_dimensions':list(im.size),'technical_derivation':{'method':'Whole native canvas uniform downsample and global translation only; no crop/paint/matte/part warp.','source_scale_at512':scale,'translation_at512':[tx,ty],'output_whole_size':list(sz),'output_origin':list(pos),'registration_record':'cabinet_registration01.json' if 'cabinet' in name else None},'cutout':m.cutout_profile(p.read_bytes()),'acceptance':'PENDING_CURRENT_CONTEXT_AND_MOTION_4.5_REVIEW'};records.append(row);new.append(row)
(s/'runtime_provenance04.json').write_text(json.dumps({'model_revision':'Availablebuiltin unexposed ownerapproved','records':records},indent=2)+'\n',encoding='utf-8')
(s/'technical04.json').write_text(json.dumps({'runtime_pictures':len(records),'decoded_RGBA_bytes':sum(x['dimensions'][0]*x['dimensions'][1]*4 for x in records),'profile_failures':[x['path'] for x in records if x['cutout']['verdict']!='CUTOUT_OK'],'limits':'Inventory/alpha only; no actualdeviceVRAM/FPS or visual acceptance.'},indent=2)+'\n',encoding='utf-8')
p=r/'ASSET_LICENSES.md';t=p.read_text(encoding='utf-8')
for x in new:
 assert '| `'+x['path']+'` |' not in t
 t+='\n| `'+x['path']+'` | '+x['source']+'; nativeSHA256 '+x['source_sha256']+' | Project/reference rights and OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Whole uniform technical derivation runtime_provenance04.json; SHA256 '+x['sha256']+'. Pending currentcontext/motion/device/owner. |'
p.write_text(t+'\n',encoding='utf-8')
print('Cabinetregistration',registration,'runtime',len(records),'profiles',[(x['path'],x['cutout']['verdict']) for x in new])
