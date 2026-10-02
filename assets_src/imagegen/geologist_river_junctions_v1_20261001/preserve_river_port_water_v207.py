from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001';a=s/'wet_attempt_02'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-57fa7989-661a-4491-a327-c88f47962cd3.png');dst=a/'native_generated.png';assert not dst.exists();shutil.copyfile(src,dst);assert sha(src)==sha(dst)
im=Image.open(dst);assert im.mode=='RGBA' and im.size==(1254,1254)
p=read(a/'GENERATION_PENDING.json');p.update(status='EXACT_GENERATED_NATIVE_PRESERVED_DIRECT_SOURCE4_6',generator_original_path=str(src),native_path=dst.relative_to(b).as_posix(),native_sha256=sha(dst),native_dimensions=list(im.size),pixel_modifications='None; exact complete generated RGBA original.');write(a/'PROVENANCE.json',p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
regions=[('ENDCAP',[53,119,556,423]),('ELBOW',[756,60,448,485]),('TEE',[47,688,544,424]),('CROSS',[686,653,511,519])]
components=[]
for name,region in regions:
 components.append(dict(id='GEO-RIVER-JUNCTION-WET-A02-'+name,path=dst.relative_to(b).as_posix(),sha256=sha(dst),region=region,source_dimensions=list(im.size),source_score=4.6,direct_review=True,runtime_bound=False,mounted_score=None,complete_action_score=None,owner_acceptance=None,evaluation='Individually inspectable '+name.lower()+' retains rounded ochre banks, plum outlines and continuous aqua interior. Bright white glints removed; calm broad painted water remains raster storybook material. All closed contours and open ports visible in complete native atlas; source4.6 only, actual repeated-port values and fit still pending.',qualification='Each of four objects directly inspected in complete generated atlas. Region is a review window annotation only, not new delivery pixels. No production/assembled-network/full-action acceptance.',reviewed_utc=now))
write(a/'REVIEW.json',dict(native_path=dst.relative_to(b).as_posix(),sha256=sha(dst),source_dimensions=list(im.size),source_score=4.6,direct_review=True,components=components,qualification='Complete native generated atlas directly inspected. Calm painted water removes source glints without vector substitution; bank silhouette and actual joint fit require independent comparison. Source-only4.6, unbound.'))
out=a/'whole_canvas_1024.png';assert not out.exists();cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','warning','-i',str(dst),'-vf','scale=1024:1024:flags=lanczos','-frames:v','1','-pix_fmt','rgba',str(out)];q=subprocess.run(cmd,capture_output=True,timeout=90);(a/'normalization.stdout.log').write_bytes(q.stdout);(a/'normalization.stderr.log').write_bytes(q.stderr);assert q.returncode==0
write(a/'TECHNICAL_DERIVATIVE.json',dict(path=out.relative_to(b).as_posix(),sha256=sha(out),source_path=dst.relative_to(b).as_posix(),source_sha256=sha(dst),dimensions=[1024,1024],method='UNIFORM_COMPLETE_CANVAS1254_TO1024_RGBA_LANCZOS',command=cmd,pixel_repair=False,alpha_cleanup=False,direct_review=False,source_score=None,runtime_bound=False))
# Read-only alpha comparison. Never use this measurement to claim exact image registration.
old=Image.open(b/p['reference_paths'][0]);metrics=[]
for name,region in regions:
 x,y,w,h=region;bounds=(x,y,x+w,y+h);x1=list(old.getchannel('A').crop(bounds).getdata());x2=list(im.getchannel('A').crop(bounds).getdata());inter=sum(u>4 and v>4 for u,v in zip(x1,x2));union=sum(u>4 or v>4 for u,v in zip(x1,x2));metrics.append(dict(component=name,region=region,alpha_gt4_iou=inter/union,qualification='Read-only alpha overlap, not pixel identity, actual fit, animation or visual acceptance.'))
write(a/'PAIR_GEOMETRY.json',dict(old_sha256=sha(b/p['reference_paths'][0]),new_sha256=sha(dst),measurements=metrics));im.close();old.close()
straight_folder=s/'straight_attempt_02';straight_folder.mkdir(exist_ok=False)
prompt='''Use case: precise-object-edit
Asset type: transparent 2D storybook straight river-channel atlas.
Image1 is the EDIT TARGET: two matching horizontal open-ended straight earth channels, upper dry, lower aqua wet. Preserve the exact layout, silhouettes, native positions, sizes, widths, transparent background, rounded ochre banks and lavender/plum outlines. Preserve the upper dry object as closely as possible.
Image2 is the matching corrected WATER MATERIAL REFERENCE: the existing endcap/elbow/T/cross with calm aqua water and no white glints. Change only the water paint in the lower straight channel to this same medium-light turquoise aqua base and quiet broad low-contrast pigment variation. Remove every white or cream specular glint and every diagonal pale streak; use the same aqua value at the left port, centre and right port. Keep a softly painted aqua waterline and broad storybook brush character. No directional bright-to-dark gradient across the channel. The lower strip must join the reference branch water calmly at any rotation.
Only two intact horizontal strips, both open at both ends. No sealing bank at either port. Full complete contours, warm painted earth, restrained lavender shadows, deep plum lines, transparent exterior. Polished 2D children’s storybook raster, no vector replacement, photorealistic noise, 3D, added props or labels. This is a targeted water-lighting correction, not an object redesign.
'''
pp=s/'PROMPT_STRAIGHT_ATTEMPT_02.txt';pp.write_text(prompt,encoding='utf-8',newline='\n')
refs=['assets_src/imagegen/geologist_river_components_v1_20261001/attempt_02/native_generated.png',dst.relative_to(b).as_posix()]
write(straight_folder/'GENERATION_PENDING.json',dict(status='PRE_GENERATION_NAMED_GAP',attempt=2,method='BUILTIN_CODEX_IMAGEGEN_TARGETED_STRAIGHT_WATER_LIGHTING_EDIT',prompt_path=pp.relative_to(b).as_posix(),prompt_sha256=sha(pp),reference_paths=refs,reference_sha256=[sha(b/x) for x in refs],transparent_background=True,runtime_bound=False,named_gap='Every106 isolated native states directly reviewed: old straight/new branch water highlights produce visible port seams4.4. Matching old straight-water material must change alongside the individually inspected corrected branch family; existing dry bank layout stays stable.',review_evidence='audit/job_river_join_study_v1_20261001/REVIEW_V5.json'))
shutil.copyfile(__file__,s/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-river-junction-source-20261001.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in s.rglob('*') if x.is_file()});write(ip,d)
print('Exact new native SHA',sha(dst),'and derivative SHA',sha(out));print('Geometry',json.dumps(metrics));print(prompt)
