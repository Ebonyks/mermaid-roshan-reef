from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
from scipy import ndimage
r=Path.cwd();s=r/'assets_src/imagegen/job_art_boxer_20261019';o=r/'assets/opera/worlds/boxer_quality_20261019';o.mkdir(exist_ok=True);props=r/'assets/opera/worlds/props';ui=r/'assets/ui';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
def emit(im,dest,source,method,extra=None):
 assert im.mode=='RGBA';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);row={'path':dest.relative_to(r).as_posix(),'sha256':sha(dest),'dimensions':list(im.size),'source':source.relative_to(r).as_posix(),'source_sha256':sha(source),'modifications':method};row.update(extra or {});rows.append(row)
for side in ['left','right']:
 p=s/('boxing_glove_'+side+'_native.png');im=Image.open(p).convert('RGBA');im.thumbnail((512,512),Image.Resampling.LANCZOS);emit(im,o/('glove_'+side+'.png'),p,'Whole original canvas uniformly downsampled1024to512; no crop, flip, paint or warp. Separate original left/right sources preserve coral/teal cuffs.')
# The circular source fixtures share a single crop/scale/placement: no per-state
# stretch, outline jump or code-colored fill. Current family includes one reject.
for name,native in [('empty','pearl_empty_retry'),('filling','pearl_filling_retry'),('full','pearl_full')]:
 p=s/(native+'_native.png');im=Image.open(p).convert('RGBA').crop((104,108,1152,1144));im.thumbnail((116,116),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(128,128));place=((128-im.width)//2,(128-im.height)//2);canvas.paste(im,place);emit(canvas,ui/('pearl_'+name+'.png'),p,'Common native crop104,108,1152,1144; uniform fit<=116px and transparent128padding, no paint/warp.',{'placement':place})
# Measure opaque connected ring body separately from sparse opening glints.
def ring_geometry(im):
 alpha=np.asarray(im.getchannel('A'));labels,n=ndimage.label(alpha>=128);areas=np.bincount(labels.ravel());areas[0]=0;which=int(areas.argmax());ys,xs=np.where(labels==which);return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
normalized={};geometry={}
for name in ['invite_ring','invite_open']:
 p=s/(name+'_native.png');im=Image.open(p).convert('RGBA');b=ring_geometry(im);scale=232.0/(b[2]-b[0]);center=((b[0]+b[2])*0.5,(b[1]+b[3])*0.5);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);place=(round(128-center[0]*scale),round(128-center[1]*scale));canvas=Image.new('RGBA',(256,256));canvas.paste(im,place);normalized[name]=canvas;geometry[name]={'alpha128_main_body_bbox':b,'uniform_scale':scale,'body_native_center':center,'placement':place};
 if name=='invite_open':emit(canvas,props/'fx_invite_open.png',p,'Uniform measured opaque-ring-body registration with transparent256canvas; preserve all glints and source pixels; no recolor/paint/warp.',geometry[name])
for i,factor in enumerate([0.94,1.0,1.04,1.0]):
 im=normalized['invite_ring'];size=round(256*factor);im=im.resize((size,size),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(256,256));canvas.paste(im,((256-size)//2,(256-size)//2));emit(canvas,props/('fx_invite_ring_'+str(i)+'.png'),s/'invite_ring_native.png','Declared whole-object uniform breathing scale on registered source, transparent256canvas. Four named technical scale keys, not four generated frames.',{'body_registration':geometry['invite_ring'],'scale_key':factor})
for name in ['focus_mitt','impact_puff']:
 p=s/(name+'_native.png');im=Image.open(p).convert('RGBA');im.thumbnail((512,512),Image.Resampling.LANCZOS);emit(im,o/(name+'.png'),p,'Whole native canvas uniformly downsampled to512; transparent margins and all authored contours retained. No crop/paint/warp.')
(s/'runtime_provenance.json').write_text(json.dumps({'records':rows,'source_roles':'All appearance pixels are original/recovered ImageGen raster. Python only technical sampling/padding/translation and diagnostic mask measurement; no RGB repaint or code-art substitution.','guide_reuse':'Exact published Teacher guide_hand.png used by Boxer, no regeneration or protected-source modification.','attempts':'9new calls:2ring/open,5pearl states including first empty/filling readability rejects,1focusmitt and1cleanpuff. Native/prompts/hashes preserved. No paid API/CLI; revision unexposed.','lane':'Static object keys and rigid whole-object local effects; fulltime/contact/human/device/child/owner acceptance separate.'},indent=2)+'\n')
p=r/'ASSET_LICENSES.md';text=p.read_text('utf-8')
for row in rows:
 name=row['path'];new='| `'+name+'` | ImageGen paintedP5/shared object; runtime_provenance.json binds exact native/recovered source | Source/OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | '+row['modifications']+' SHA256'+row['sha256']+'; source/current/device/owner acceptance separate. |';lines=text.splitlines();matched=False
 for i,line in enumerate(lines):
  if line.startswith('| `'+name+'` |'):lines[i]=new;matched=True
 text='\n'.join(lines)
 if not matched:text+='\n'+new
p.write_text(text+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[f.relative_to(r).as_posix() for f in s.rglob('*') if f.is_file()]+[x['path'] for x in rows]+['scripts/painted_feedback_art.gd']));p.write_text(json.dumps(d,indent=2)+'\n')
print('Prepared',len(rows),'painted runtime objects/scale keys; original natives/rejects preserved')
