from pathlib import Path
from PIL import Image
import json,hashlib,shutil
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';o=r/'assets/opera/worlds/nursery_quality_20261019';o.mkdir(parents=True,exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
def emit(name,source,side=None,crop=None,canvas=None,place=None):
 im=Image.open(source).convert('RGBA');original=list(im.size)
 if crop:im=im.crop(crop)
 if side:im.thumbnail(side,Image.Resampling.LANCZOS)
 if canvas:
  c=Image.new('RGBA',canvas);c.paste(im,place or ((canvas[0]-im.width)//2,(canvas[1]-im.height)//2));im=c
 dest=o/(name+'.png');im.save(dest)
 rows.append({'id':name,'source':source.relative_to(r).as_posix(),'source_sha256':sha(source),'native_dimensions':original,'crop':list(crop) if crop else None,'runtime_dimensions':list(im.size),'placement':place,'path':dest.relative_to(r).as_posix(),'sha256':sha(dest),'modifications':'RGBA technical crop/uniform Lanczos downsample/transparent padding/translation only; no RGB paint, warp or guide pixels.'})
emit('cradle',s/'recovered/refinement_v1/cradle.png',(512,512))
p=s/'recovered/refinement_v1/pillows.png';im=Image.open(p).convert('RGBA');b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();b=(max(0,b[0]-4),max(0,b[1]-4),min(im.width,b[2]+4),min(im.height,b[3]+4));emit('pillows',p,(1024,256),b)
for p in sorted((s/'recovered/wash_connected_v1_20261002').glob('*.png')):emit('wash_'+p.stem,p,(512,512))
for p in sorted((s/'recovered/refinement_v2').glob('*.png')):
 dest=o/p.name;shutil.copyfile(p,dest);rows.append({'id':p.stem,'source':p.relative_to(r).as_posix(),'source_sha256':sha(p),'path':dest.relative_to(r).as_posix(),'sha256':sha(dest),'runtime_dimensions':[512,512],'modifications':'Exact original bytes, no edit; Nursery-only owner use-as-is decision.'})
for name,native in [('crib','crib_native'),('pat_hand','pat_hand_retry_native')]:
 p=s/(native+'.png');im=Image.open(p).convert('RGBA');b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();b=(max(0,b[0]-8),max(0,b[1]-8),min(im.width,b[2]+8),min(im.height,b[3]+8));emit(name,p,(504,504) if name=='crib' else(248,248),b,(512,512) if name=='crib' else(256,256))
# Same width and upper-edge coordinate for all three cloth keys, preserving each natural shape.
for name in ['folded','half_retry','tucked']:
 p=s/('quilt_'+name+'_native.png');im=Image.open(p).convert('RGBA');b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();b=(max(0,b[0]-4),max(0,b[1]-4),min(im.width,b[2]+4),min(im.height,b[3]+4));c=im.crop(b);c.thumbnail((504,248),Image.Resampling.LANCZOS);place=((512-c.width)//2,4)
 emit('quilt_'+name.replace('_retry',''),p,(504,248),b,(512,256),place)
# Uniformly register the empty source to the original256-square bottle; half-level rejects stay source-only.
reg=json.loads((s/'bottle_registration_diagnostic.json').read_text())['records'][1];p=s/'bottle_empty_native.png';b=reg['native_crop'];scale=reg['uniform_scale'];pad=4;crop=(b[0]-pad,b[1]-pad,b[2]+pad,b[3]+pad);size=(round((crop[2]-crop[0])*scale),round((crop[3]-crop[1])*scale));place=(reg['placement'][0]-round(pad*scale),reg['placement'][1]-round(pad*scale));emit('bottle_empty',p,size,crop,(256,256),place)
# Existing approved-art reuse, no generation needed for this already-good object.
for name,path in [('mobile','assets/opera/worlds/props/goal_nursery.png'),('guide_hand','assets/opera/worlds/teacher/guide_hand.png')]:emit(name,r/path,(512,512))
(s/'runtime_provenance.json').write_text(json.dumps({'schema':'reef.nursery_painted_derivation/1','records':rows,'all_pixels':'Native ImageGen/existing authored raster appearance only. Python performs technical transformations, no visual redraw. Rejected half bottles/hand/quilt remain outside runtime.','bottle_method_change':'Stop at4aggregate bottle generations. Selected empty state + existing full source are composed in disjoint native rows at runtime; fixed exterior/nipple remains original, milk transition reviewed separately. No half-full generation accepted.','older_identity':'Owner-approved older Nursery wash/care poses used only in this career; source/protected originals preserved.'},indent=2)+'\n')
lic=r/'ASSET_LICENSES.md';t=lic.read_text('utf-8')
for row in rows:
 p=row['path']
 if '| `'+p+'` |' not in t:t+='\n| `'+p+'` | Available builtin ImageGen or recovered approved project ImageGen; runtime_provenance.json binds exact source | Existing source/OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | '+row['modifications']+' SHA256 '+row['sha256']+'; no owner/device acceptance. |'
lic.write_text(t+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[f.relative_to(r).as_posix() for f in s.rglob('*') if f.is_file()]+[f.relative_to(r).as_posix() for f in o.rglob('*') if f.is_file()]+['scripts/nursery_painted_art.gd','scripts/opera_gesture_surface.gd','scripts/opera_nursery_catch.gd','scripts/opera_career_world_2d.gd','scripts/opera_roshan_actor.gd']))
d['scope']+=' After4bottle calls miss the half-level, stop generation and change to declared Canvas compositing of the registered empty and original full painted sources; retain all rejects/position-guide limits. Source-state wash replaces the duplicated world actor only during the wash activity; original actor restores between phases. Whole8care poses are selected by existing progress in Nursery only. Source-based nipple/contact/crib/quilt registration and no nonuniform squash, no new game progress or saved key.'
p.write_text(json.dumps(d,indent=2)+'\n')
print('Prepared',len(rows),'uniform/exact runtime sources; original/protected/source bytes preserved')
