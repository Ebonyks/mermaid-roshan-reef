from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time,re
from PIL import Image
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geology_painted_mount_v1_20261001';assert not out.exists();out.mkdir()
def rel(p):return p.relative_to(r).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
(out/'.gdignore').write_text('')
base=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
selected=json.loads((base/'REVIEW.json').read_text(encoding='utf-8'))['technical_derivatives']
paths={p['path'].split('/')[-3]:p['path'] for p in selected}
boxes={}
for key,path in paths.items():
 a=Image.open(r/path).getchannel('A');b=a.point(lambda p:255 if p>=16 else 0).getbbox();boxes[key]=list(b)
prefix='res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/'
source=r/'audit/job_vector_mount_review_v1_20261001/attempt_02/capture.gd';code=source.read_text(encoding='utf-8')
start=code.index('const CANDIDATES := {');end=code.index('\nvar main:',start)
maps={"res://assets/opera/worlds/hotspots/geologist_fossil.svg":'res://'+paths['fossil'],"res://assets/opera/worlds/hotspots/geologist_layered_rock.svg":'res://'+paths['layered_rock'],"res://assets/opera/worlds/props/goal_geologist.svg":'res://'+paths['crystal_reward']}
consts='const StudySurface := preload("res://'+rel(out/'study_surface.gd')+'")\nconst CANDIDATES := '+json.dumps(maps,indent=1)+'\nconst PAINTED_PATHS := '+json.dumps({k:'res://'+v for k,v in paths.items()},indent=1)+'\nconst SOURCE_BOXES := '+json.dumps(boxes,indent=1)
code=code[:start]+consts+code[end:];code=code.replace('tmp/vector_mount_v87/native_views','tmp/geology_painted_mount_v95/native_views')
code=code.replace('var candidate_textures: Dictionary = {}','var candidate_textures: Dictionary = {}\nvar painted_textures: Dictionary = {}\nvar study_background: TextureRect\nvar original_presentations: Dictionary = {}')
code=code.replace('for use_new: bool in [false, true]:\n\t\t_use_candidates(world, use_new)', 'for lane: String in ["original", "literal_raster", "painted_staging"]:\n\t\tvar use_new := lane != "original"\n\t\t_use_candidates(world, use_new)\n\t\tvar study := world.surface as StudySurface\n\t\tstudy.painted_study = lane == "painted_staging"\n\t\tstudy_background.visible = study.painted_study\n\t\tworld.backdrop_node.visible = not study.painted_study\n\t\tif study.painted_study:\n\t\t\tstudy.fossil_texture = painted_textures["fossil"] as Texture2D\n\t\t\tstudy.rock_texture = painted_textures["layered_rock"] as Texture2D\n\t\t\tstudy.crystals_texture = painted_textures["crystal_reward"] as Texture2D\n\t\t\tstudy.pan_texture = painted_textures["washing_pan"] as Texture2D\n\t\t\tvar active := world._active_hotspot()\n\t\t\tvar prop_key := "layered_rock"\n\t\t\tif phase_now == "FOSSIL":\n\t\t\t\tprop_key = "fossil"\n\t\t\telif phase_now == "PAN":\n\t\t\t\tprop_key = "washing_pan"\n\t\t\telif phase_now == "GEODE":\n\t\t\t\tprop_key = "closed_geode"\n\t\t\tactive.object_texture = painted_textures[prop_key] as Texture2D\n\t\t\tactive.presentation = "overlay"\n\t\t\tactive.queue_redraw()\n\t\tstudy.queue_redraw()')
code=code.replace('"candidate" if use_new else "original"','lane')
code=code.replace('"fixture": "Phase selected via existing _arm_phase, then actual viewport invitation approach. Candidate texture injection into existing owners only; complete job/training-to-story sequence not represented."','"fixture": "Phase-selected disposable inherited-input fixture with current source, literal raster injection and explicit painted drawing/layout study. Painted staging uses undersize room as REFERENCE_ONLY, not runtime art; no complete career/story/device/child/owner pass."')
code=code.replace('\t_use_candidates(world, false)\n\tassert(before', '\t_use_candidates(world, false)\n\t(world.surface as StudySurface).painted_study = false\n\tstudy_background.visible = false\n\tworld.backdrop_node.visible = true\n\tfor raw_hot: Control in world.station_nodes:\n\t\tvar reset_hot := raw_hot as OperaWorldHotspot2D\n\t\treset_hot.presentation = String(original_presentations[reset_hot])\n\t\treset_hot.queue_redraw()\n\tassert(before')
code=code.replace('\t\tsurface.queue_redraw()','\t\tsurface.pan_texture = painted_textures["washing_pan"] as Texture2D if use_new else null\n\t\tsurface.queue_redraw()',1)
code=code.replace('\tmain = (load(', '\tfor key: String in PAINTED_PATHS:\n\t\tvar img := Image.load_from_file(String(PAINTED_PATHS[key]))\n\t\tvar texture := ImageTexture.create_from_image(img)\n\t\tvar b := SOURCE_BOXES[key] as Array\n\t\tvar atlas := AtlasTexture.new()\n\t\tatlas.atlas = texture\n\t\tatlas.region = Rect2(float(b[0]), float(b[1]), float(b[2]) - float(b[0]), float(b[3]) - float(b[1]))\n\t\tpainted_textures[key] = atlas\n\tmain = (load(',1)
code=code.replace('for career: String in ["teacher", "geologist"]:', 'for career: String in ["geologist"]:')
needle='\t\t\t\tvar chosen := -1'
replacement='''\t\t\t\tvar old_surface := world.surface
\t\t\t\tvar study := StudySurface.new()
\t\t\t\tstudy.name = "PaintedGeologyDisposableSurface"
\t\t\t\tstudy.position = old_surface.position
\t\t\t\tstudy.size = old_surface.size
\t\t\t\tstudy.mouse_filter = old_surface.mouse_filter
\t\t\t\tstudy.bop_texture = old_surface.bop_texture
\t\t\t\tstudy.bop_captain_texture = old_surface.bop_captain_texture
\t\t\t\tstudy.gesture.connect(Callable(world, "_on_gesture"))
\t\t\t\tstudy.progress_changed.connect(Callable(world, "_on_geology_progress_changed"))
\t\t\t\tvar child_index := old_surface.get_index()
\t\t\t\tworld.action_panel.remove_child(old_surface)
\t\t\t\told_surface.queue_free()
\t\t\t\tworld.action_panel.add_child(study)
\t\t\t\tworld.action_panel.move_child(study, child_index)
\t\t\t\tworld.surface = study
\t\t\t\tstudy.work_texture = painted_textures["work_surface"] as Texture2D
\t\t\t\tstudy.geode_texture = painted_textures["closed_geode"] as Texture2D
\t\t\t\tvar open_source := ImageTexture.create_from_image(Image.load_from_file(String(PAINTED_PATHS["open_geode"])))
\t\t\t\tvar left_half := AtlasTexture.new()
\t\t\t\tleft_half.atlas = open_source
\t\t\t\tleft_half.region = Rect2(104, 213, 409, 602)
\t\t\t\tvar right_half := AtlasTexture.new()
\t\t\t\tright_half.atlas = open_source
\t\t\t\tright_half.region = Rect2(526, 213, 396, 602)
\t\t\t\tstudy.open_left_texture = left_half
\t\t\t\tstudy.open_right_texture = right_half
\t\t\t\tstudy_background = TextureRect.new()
\t\t\t\tstudy_background.name = "UNDERSIZE_REFERENCE_ONLY_ROOM"
\t\t\t\tstudy_background.texture = ImageTexture.create_from_image(Image.load_from_file("res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/grotto/attempt_01/native.png"))
\t\t\t\tstudy_background.position = Vector2.ZERO
\t\t\t\tstudy_background.size = Vector2(1280, 720)
\t\t\t\tstudy_background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
\t\t\t\tstudy_background.stretch_mode = TextureRect.STRETCH_SCALE
\t\t\t\tstudy_background.mouse_filter = Control.MOUSE_FILTER_IGNORE
\t\t\t\tstudy_background.visible = false
\t\t\t\tworld.root.add_child(study_background)
\t\t\t\tworld.root.move_child(study_background, world.backdrop_node.get_index())
\t\t\t\toriginal_presentations.clear()
\t\t\t\tfor raw_hot: Control in world.station_nodes:
\t\t\t\t\tvar hot_prop := raw_hot as OperaWorldHotspot2D
\t\t\t\t\toriginal_presentations[hot_prop] = hot_prop.presentation
\t\t\t\tvar chosen := -1'''
assert needle in code;code=code.replace(needle,replacement)
code=code.replace('\t\t\t\tif phase_name == "FOSSIL":','\t\t\t\tif phase_name == "RIVER":\n\t\t\t\t\tawait _partial_river(world)\n\t\t\t\tif phase_name == "PAN":\n\t\t\t\t\tawait _partial_pan(world)\n\t\t\t\tif phase_name == "FOSSIL":')
extra='''
func _partial_river(world: OperaCareerWorld2D) -> void:
\tvar surface := world.surface as OperaGeologySurface
\tvar start := surface.river_path_point(0)
\tawait _surface_touch(surface, start, true)
\tfor index: int in range(1, 4):
\t\tvar next := surface.river_path_point(index)
\t\tawait _surface_drag(surface, start, next)
\t\tstart = next
\tawait _surface_touch(surface, start, false)
\tassert(not surface._completion_emitted and not surface._river_connected())
\tawait _capture_pair(world, "partial_connected_river")

func _partial_pan(world: OperaCareerWorld2D) -> void:
\tvar surface := world.surface as OperaGeologySurface
\tvar start := OperaGeologySurface.PAN_RECT.get_center()
\tawait _surface_touch(surface, start, true)
\tfor offset: float in [80.0, -80.0, 80.0, -80.0]:
\t\tvar next := OperaGeologySurface.PAN_RECT.get_center() + Vector2(offset, 0)
\t\tawait _surface_drag(surface, start, next)
\t\tstart = next
\tawait _surface_touch(surface, start, false)
\tassert(surface.pan_reversals > 0 and surface.pan_reversals < 9)
\tassert(not surface._completion_emitted)
\tawait _capture_pair(world, "partial_panning_reversals")
'''
code=code.replace('func _run() -> void:',extra+'\nfunc _run() -> void:')
code=code.replace('records.size() == 76','records.size() == 78').replace('76_NATIVE_PHASE_FIXTURE_COMPARISONS_CAPTURED','78_NATIVE_PAINTED_GEOLOGY_FIXTURE_COMPARISONS_CAPTURED').replace('76_CAPTURED','78_CAPTURED').replace('VECTOR_MOUNT','PAINTED_GEOLOGY_MOUNT')
(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n');shutil.copyfile(Path(__file__).with_name('geology_painted_study_surface_v95.gd'),out/'study_surface.gd');shutil.copyfile(__file__,out/'executed_run_geology_painted_mount_v95.py')
bound=json.loads((r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text(encoding='utf-8'))
before={x['path']:sha(r/x['path']) for x in bound};write(out/'SOURCE_BEFORE.json',before)
write(out/'PROFILE.json',dict(status='PREPARED_REVIEW_ONLY_NATIVE_PAINTED_STAGING',baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),variant_lanes=['original','literal_raster','painted_staging'],planned_views=78,viewports=[[1280,720],[1600,720]],source_paths=paths,source_atlas_boxes=boxes,qualification='StudySurface only overrides work/geode drawing; all actual touch/progress remains inherited. Painted staging explicitly reveals new invitation objects and uses undersize room as style/layout reference only. Original325 literal production files, saves and star awards must remain unchanged. No runtime binding, complete career/training/story/device/child/owner acceptance.'))
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['scope']+=' Add a disposable native three-lane painted staging comparison with inherited production touch/progress, named source/atlas regions, four real partial gestures and explicit reference-only undersize room; no production drawing/input changes.';d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(r),'--script','res://'+rel(out/'capture.gd')])]
rows=[]
for name,cmd in cmds:
 start=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:
  try:p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,timeout=900 if name=='native' else 240,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timeout=False
  except subprocess.TimeoutExpired:code=None;timeout=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timeout,seconds=time.monotonic()-start,stdout=rel(out/(name+'.stdout.log')),stderr=rel(out/(name+'.stderr.log'))));print(name,code,flush=True)
 if code!=0:print((out/(name+'.stdout.log')).read_text(encoding='utf-8',errors='replace')[-1000:],(out/(name+'.stderr.log')).read_text(encoding='utf-8',errors='replace')[-2500:],flush=True);break
after={p:sha(r/p) for p in before};passed=len(rows)==len(cmds) and all(x['process_exit']==0 for x in rows) and before==after
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_NATIVE_PAINTED_STAGING_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_source_hashes_unchanged=before==after,qualification='Machine capture only. Every native view needs direct individual review; undersize painted room remains reference-only. No production, full route/action, child/device/owner pass.'))
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});d['validation'].append(dict(command='Official4.7.2 native inherited-input three-lane geology study and325-file unchanged-source guard',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d)
raise SystemExit(0 if passed else 1)
