from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time,datetime
from PIL import Image
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geode_embedded_mount_v2_20261001';assert not out.exists();out.mkdir()
def rel(p):return p.relative_to(r).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
(out/'.gdignore').write_text('')
previous=r/'audit/job_geology_painted_mount_v1_20261001/attempt_02'
code=(previous/'capture.gd').read_text(encoding='utf-8')
code=code.replace('tmp/geology_painted_mount_v96/native_views','tmp/geode_embedded_mount_v98/native_views').replace('audit/job_geology_painted_mount_v1_20261001/attempt_02/study_surface.gd',rel(out/'study_surface.gd'))
code=code.replace('open_geode/attempt_01/whole_canvas_1024.png','open_geode/attempt_02/whole_canvas_1024.png')
code=code.replace('names.assign(["RIVER", "FOSSIL", "PAN", "GEODE"])','names.assign(["GEODE"])')
code=code.replace('study.crystals_texture = painted_textures["crystal_reward"] as Texture2D','study.crystals_texture = painted_textures["crystal_reward"] as Texture2D\n\t\t\tstudy.geode_texture = painted_textures["closed_geode"] as Texture2D')
code=code.replace('study_background.visible = study.painted_study','study_background.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)\n\t\tstudy_background.position = Vector2.ZERO\n\t\tstudy_background.size = Vector2(1280, 720)\n\t\tstudy_background.visible = study.painted_study')
source=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001/open_geode/attempt_02/whole_canvas_1024.png'
im=Image.open(source);alpha=im.getchannel('A');regions=[]
for left,right in [(0,im.width//2),(im.width//2,im.width)]:
 b=alpha.crop((left,0,right,im.height)).point(lambda p:255 if p>=16 else 0).getbbox();regions.append((b[0]+left,b[1],b[2]-b[0],b[3]-b[1]))
code=code.replace('Rect2(104, 213, 409, 602)','Rect2('+', '.join(str(n) for n in regions[0])+')').replace('Rect2(526, 213, 396, 602)','Rect2('+', '.join(str(n) for n in regions[1])+')')
code=code.replace('records.size() == 78','records.size() == 24').replace('78_NATIVE_PAINTED_GEOLOGY_FIXTURE_COMPARISONS_CAPTURED','24_NATIVE_EMBEDDED_GEODE_FIXTURE_COMPARISONS_CAPTURED').replace('78_CAPTURED','24_CAPTURED').replace('PAINTED_GEOLOGY_MOUNT','EMBEDDED_GEODE_MOUNT')
needle='\tassert(not surface._completion_emitted)\n\n\nfunc _partial_river'
assert needle in code
endpoint='''\tassert(not surface._completion_emitted)
\t# Isolate only the completion callbacks for this disposable endpoint review.
\t# Production input determines the end state; career award/save cannot run.
\tsurface.gesture.disconnect(Callable(world, "_on_gesture"))
\tsurface.progress_changed.disconnect(Callable(world, "_on_geology_progress_changed"))
\tvar continued := surface.geode_half_center()
\tawait _surface_touch(surface, continued, true)
\tawait _surface_drag(surface, continued, continued + Vector2(55.0, 0.0))
\tawait _surface_touch(surface, continued + Vector2(55.0, 0.0), false)
\tassert(surface.geode_pull >= OperaGeologySurface.GEODE_PULL_DISTANCE)
\tassert(surface._completion_emitted and world.task_open)
\tawait _capture_pair(world, "fully_open_embedded_interior")


func _partial_river'''
code=code.replace(needle,endpoint)
code=code.replace('Individually selected phases followed by real viewport approach and partial fossil/geode touch input. Current and temporary candidate textures paired at same state. No completed career, uninterrupted training/story route, cinematic, device, child or owner acceptance.','GEODE phase selected followed by actual viewport approach, five seam taps,65px partial pull and continuation to120px full surface opening. Only endpoint completion callbacks are disconnected in this disposable fixture so no career award/save can run. Three drawing lanes paired at identical inherited progress. No full career/training/story, cinematic, device, child or owner acceptance.')
study=(previous/'study_surface.gd').read_text(encoding='utf-8')
start=study.index('\tdraw_texture_rect(open_left_texture,')
study=study[:start]+'''\t# The crystals are authored inside each half: no detached reward layer.
\tvar half_height := 350.0
\tvar left_size := open_left_texture.get_size()
\tvar right_size := open_right_texture.get_size()
\tvar left_width := half_height * left_size.x / left_size.y
\tvar right_width := half_height * right_size.x / right_size.y
\tdraw_texture_rect(open_left_texture,
\t\tRect2(center + Vector2(-left_width, -half_height * 0.5),
\t\t\tVector2(left_width, half_height)), false)
\tdraw_texture_rect(open_right_texture,
\t\tRect2(center + Vector2(geode_pull, -half_height * 0.5),
\t\t\tVector2(right_width, half_height)), false)
'''
(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n');(out/'study_surface.gd').write_text(study,encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'executed_run_geode_embedded_mount_v98.py')
bound=json.loads((r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text(encoding='utf-8'))['source_files'];before={x['path']:sha(r/x['path']) for x in bound};write(out/'SOURCE_BEFORE.json',before)
write(out/'PROFILE.json',dict(status='PREPARED_DISPOSABLE_EMBEDDED_GEODE_ENDPOINT',baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),planned_views=24,original_production_inputs=True,endpoint_callbacks_disconnected=True,native_open_source=rel(source),native_open_sha256=sha(source),runtime_atlas_regions=regions,preserved_half_aspect=True,detached_reward_drawn=False,background_resolution='REFERENCE_ONLY_NATIVE1672x941_FAILED',production_bindings_changed=False,qualification='Source and surface endpoint drafting review only. Closed-to-open silhouette width grows as faces turn outward; transition continuity still requires independent review.'))
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['scope']+=' Add separate disposable embedded-geode endpoint captures: preserve half aspect, repair the study-only closed texture reset, use inherited seam/pull input, disconnect only fixture endpoint completion callbacks to prevent career awards/save writes.';d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(r),'--script','res://'+rel(out/'capture.gd')])]
rows=[]
for name,cmd in cmds:
 start=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:
  try:p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,timeout=600 if name=='native' else 240,creationflags=subprocess.CREATE_NO_WINDOW);exit_code=p.returncode;timed_out=False
  except subprocess.TimeoutExpired:exit_code=None;timed_out=True
 rows.append(dict(name=name,command=cmd,process_exit=exit_code,timed_out=timed_out,seconds=time.monotonic()-start,stdout=rel(out/(name+'.stdout.log')),stderr=rel(out/(name+'.stderr.log'))));print(name,exit_code,flush=True)
 if exit_code!=0:print((out/(name+'.stderr.log')).read_text(encoding='utf-8',errors='replace')[-3000:],flush=True);break
after={p:sha(r/p) for p in before};passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and before==after
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_MACHINE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_source_hashes_unchanged=before==after,qualification='Machine capture only, direct review pending. No production binding or complete route/device/child/owner pass.'))
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});d['validation'].append(dict(command='Official4.7.2 native embedded-geode disposable endpoint fixture and325-file unchanged-source guard',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d)
raise SystemExit(0 if passed else 1)
