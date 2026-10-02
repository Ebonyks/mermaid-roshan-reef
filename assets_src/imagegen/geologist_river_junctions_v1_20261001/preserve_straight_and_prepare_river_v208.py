from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001';a=s/'straight_attempt_02';f=b/'audit/job_river_join_study_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-d84e78d3-a645-4b38-bf0f-d7b509e03f71.png');dst=a/'native_generated.png';assert not dst.exists();shutil.copyfile(src,dst);assert sha(src)==sha(dst)
with Image.open(dst) as im:assert im.mode=='RGBA' and im.size==(1254,1254)
p=read(a/'GENERATION_PENDING.json');p.update(status='EXACT_GENERATED_NATIVE_PRESERVED_DIRECT_SOURCE4_6',generator_original_path=str(src),native_path=dst.relative_to(b).as_posix(),native_sha256=sha(dst),native_dimensions=[1254,1254],pixel_modifications='None; exact complete generated RGBA original.');write(a/'PROVENANCE.json',p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();components=[]
for name,region in [('DRY_UNUSED',[32,309,1196,302]),('WET',[31,734,1197,303])]:
 components.append(dict(id='GEO-RIVER-STRAIGHT-A02-'+name,path=dst.relative_to(b).as_posix(),sha256=sha(dst),region=region,source_dimensions=[1254,1254],source_score=4.6,direct_review=True,runtime_bound=False,mounted_score=None,complete_action_score=None,owner_acceptance=None,evaluation='Individually visible '+name.lower()+' open horizontal channel retains complete ochre banks/plum contour and an open centre at both ports. Wet member has calm broad aqua pigment bands without white glints; dry member remains an unused edit by-product and does not replace the preserved original dry strip. Source4.6 only; actual joins pending.',qualification='Each of two separate objects directly inspected in complete generated atlas; review window only, not new pixels. No production/network/full-action acceptance.',reviewed_utc=now))
write(a/'REVIEW.json',dict(native_path=dst.relative_to(b).as_posix(),sha256=sha(dst),source_dimensions=[1254,1254],source_score=4.6,direct_review=True,components=components,qualification='Complete native source directly inspected, source4.6 only. Corrected wet surface intended for repeated-port study; dry edit by-product unused.'))
out=a/'whole_canvas_1024.png';assert not out.exists();cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','warning','-i',str(dst),'-vf','scale=1024:1024:flags=lanczos','-frames:v','1','-pix_fmt','rgba',str(out)];q=subprocess.run(cmd,capture_output=True,timeout=90);(a/'normalization.stdout.log').write_bytes(q.stdout);(a/'normalization.stderr.log').write_bytes(q.stderr);assert q.returncode==0
write(a/'TECHNICAL_DERIVATIVE.json',dict(path=out.relative_to(b).as_posix(),sha256=sha(out),source_path=dst.relative_to(b).as_posix(),source_sha256=sha(dst),dimensions=[1024,1024],method='UNIFORM_COMPLETE_CANVAS1254_TO1024_RGBA_LANCZOS',command=cmd,pixel_repair=False,alpha_cleanup=False,direct_review=False,source_score=None,runtime_bound=False))
# Actual parent input/grid/flow remains unchanged; only atlas paths change.
code=(f/'join_surface_v5.gd').read_text(encoding='utf-8');code=code.replace('("wet_attempt_01/" if wet else "dry_attempt_01/")','("wet_attempt_02/" if wet else "dry_attempt_01/")')
needle='source_path = PARTS + "attempt_02/whole_canvas_1024.png"';assert code.count(needle)==1
code=code.replace(needle,'source_path = (JUNCTIONS + "straight_attempt_02/whole_canvas_1024.png") if wet \\\n\t\t\telse (PARTS + "attempt_02/whole_canvas_1024.png")')
(f/'join_surface_v6.gd').write_text(code,encoding='utf-8',newline='\n')
code=(f/'capture_join_study_v5.gd').read_text(encoding='utf-8').replace('join_surface_v5.gd','join_surface_v6.gd').replace('attempt_05','attempt_06');(f/'capture_join_study_v6.gd').write_text(code,encoding='utf-8',newline='\n')
code=(f/'run_river_join_capture_v204.py').read_text(encoding='utf-8').replace('attempt_05','attempt_06').replace('capture_join_study_v5.gd','capture_join_study_v6.gd').replace('v5.','v6.').replace('v204','v208');(f/'run_river_join_capture_v208.py').write_text(code,encoding='utf-8',newline='\n')
write(f/'WATER_SOURCE_CHANGE_V6.json',dict(baseline='40b1c7bfe025f284507c586fea61b9dd76b61423',changed_drawing_only=['wet_attempt_02/whole_canvas_1024.png','straight_attempt_02/whole_canvas_1024.png'],original_dry_source_retained=True,grid_input_flow_save_completion_changed=False,actor_room_absent=True,source_score=4.6,assembled_score=None,qualification='Uniform complete source files and Canvas atlas fields only; same V5 anchors/scale. Independently generated geometry is not presumed identical; actual native study must earn visual acceptance.'))
shutil.copyfile(__file__,s/Path(__file__).name)
for name,folder in [('job-geology-river-junction-source-20261001',s),('job-geology-river-join-study-20261001',f)]:
 ip=b/('design/audit_impacts/'+name+'.json');d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in folder.rglob('*') if x.is_file()});write(ip,d)
print('Straight native SHA',sha(dst),'derivative',sha(out),'V6 drawing-only study prepared.')
