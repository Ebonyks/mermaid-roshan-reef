from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001';a=s/'dry_attempt_02';f=b/'audit/job_river_join_study_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-ca5cade5-9e1d-4fc9-ac15-2ddb6060855b.png');dst=a/'native_generated.png';assert not dst.exists();shutil.copyfile(src,dst);assert sha(src)==sha(dst)
with Image.open(dst) as im:assert im.mode=='RGBA' and im.size==(1254,1254)
p=read(a/'GENERATION_PENDING.json');p.update(status='EXACT_GENERATED_NATIVE_PRESERVED_DIRECT_SOURCE4_6',generator_original_path=str(src),native_path=dst.relative_to(b).as_posix(),native_sha256=sha(dst),native_dimensions=[1254,1254],pixel_modifications='None; exact complete generated RGBA original.');write(a/'PROVENANCE.json',p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();components=[]
for name,region in [('ENDCAP',[53,119,556,423]),('ELBOW',[756,60,448,485]),('TEE',[47,688,544,424]),('CROSS',[686,653,511,519])]:
 components.append(dict(id='GEO-RIVER-JUNCTION-DRY-A02-'+name,path=dst.relative_to(b).as_posix(),sha256=sha(dst),region=region,source_dimensions=[1254,1254],source_score=4.6,direct_review=True,runtime_bound=False,mounted_score=None,complete_action_score=None,owner_acceptance=None,evaluation='Individually visible '+name.lower()+' retains complete rounded ochre bank silhouette and open port topology. Calm medium-light golden recessed floor with low-contrast broad pigment bands removes the old directional shadow gradient. Local plum wall edge keeps excavation depth. Source4.6 only; repeat-join/native mounting still pending.',qualification='Each of four separate source shapes directly inspected in complete generated atlas. Region is an annotation only; no new delivery pixels or production/full-action approval.',reviewed_utc=now))
write(a/'REVIEW.json',dict(native_path=dst.relative_to(b).as_posix(),sha256=sha(dst),source_dimensions=[1254,1254],source_score=4.6,direct_review=True,components=components,qualification='Complete native raster original directly inspected, each four-source silhouette/material4.6 only. Calm golden floor; actual repeated-port depth/value fit remains pending.'))
out=a/'whole_canvas_1024.png';assert not out.exists();cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','warning','-i',str(dst),'-vf','scale=1024:1024:flags=lanczos','-frames:v','1','-pix_fmt','rgba',str(out)];q=subprocess.run(cmd,capture_output=True,timeout=90);(a/'normalization.stdout.log').write_bytes(q.stdout);(a/'normalization.stderr.log').write_bytes(q.stderr);assert q.returncode==0
write(a/'TECHNICAL_DERIVATIVE.json',dict(path=out.relative_to(b).as_posix(),sha256=sha(out),source_path=dst.relative_to(b).as_posix(),source_sha256=sha(dst),dimensions=[1024,1024],method='UNIFORM_COMPLETE_CANVAS1254_TO1024_RGBA_LANCZOS',command=cmd,pixel_repair=False,alpha_cleanup=False,direct_review=False,source_score=None,runtime_bound=False))
code=(f/'join_surface_v6.gd').read_text(encoding='utf-8').replace('else "dry_attempt_01/"','else "dry_attempt_02/"');assert 'dry_attempt_02/' in code;(f/'join_surface_v7.gd').write_text(code,encoding='utf-8',newline='\n')
code=(f/'capture_join_study_v6.gd').read_text(encoding='utf-8').replace('join_surface_v6.gd','join_surface_v7.gd').replace('attempt_06','attempt_07');(f/'capture_join_study_v7.gd').write_text(code,encoding='utf-8',newline='\n')
code=(f/'run_river_join_capture_v208.py').read_text(encoding='utf-8').replace('attempt_06','attempt_07').replace('capture_join_study_v6.gd','capture_join_study_v7.gd').replace('v6.','v7.').replace('v208','v210');(f/'run_river_join_capture_v210.py').write_text(code,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,s/Path(__file__).name)
for name,folder in [('job-geology-river-junction-source-20261001',s),('job-geology-river-join-study-20261001',f)]:
 ip=b/('design/audit_impacts/'+name+'.json');d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in folder.rglob('*') if x.is_file()});write(ip,d)
print('Dry native SHA',sha(dst),'derivative',sha(out),'V7 drawing-only study prepared.')
