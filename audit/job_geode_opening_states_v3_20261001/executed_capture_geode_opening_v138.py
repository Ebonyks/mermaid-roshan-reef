from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');old=b/'audit/job_geode_embedded_mount_v2_20261001/attempt_02';out=b/'audit/job_geode_opening_states_v3_20261001';out.mkdir(exist_ok=False)
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
code=(old/'capture.gd').read_text().replace('tmp/geode_embedded_review_v99/native_views','tmp/geode_opening_v138/native_views').replace('res://'+rel(old/'study_surface.gd'),'res://'+rel(out/'study_surface.gd'))
assert 'tmp/geode_embedded_review_v99/native_views' not in code
code=code.replace('["original", "literal_raster", "painted_staging"]','["painted_staging"]')
before='''	await _surface_drag(surface, start, start + Vector2(65.0, 0.0))
	await _surface_touch(surface, start + Vector2(65.0, 0.0), false)'''
after='''	await _surface_drag(surface, start, start + Vector2(25.0, 0.0))
	await _surface_touch(surface, start + Vector2(25.0, 0.0), false)
	assert(surface.geode_pull > 0.0 and surface.geode_pull < 40.0)
	await _capture_pair(world, "early_crack_rooted_glimpse")
	var midway := surface.geode_half_center()
	await _surface_touch(surface, midway, true)
	await _surface_drag(surface, midway, midway + Vector2(40.0, 0.0))
	await _surface_touch(surface, midway + Vector2(40.0, 0.0), false)'''
assert before in code;code=code.replace(before,after)
for key,box in [('early_crack',[77,85,947,826]),('middle_open',[99,70,944,639])]:
 path='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/opening_geode/'+key+'/attempt_01/whole_canvas_1024.png'
 code=code.replace('study.geode_texture = painted_textures["closed_geode"] as Texture2D','study.geode_texture = painted_textures["closed_geode"] as Texture2D\n\t\t\tstudy.'+key+'_texture = _opening_texture("res://'+path+'", Rect2('+', '.join(str(v) for v in [box[0],box[1],box[2]-box[0],box[3]-box[1]])+'))',1)
code=code.replace('func _initialize() -> void:', '''func _opening_texture(path: String, region: Rect2) -> AtlasTexture:
	var texture := ImageTexture.create_from_image(Image.load_from_file(path))
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = region
	return atlas

func _initialize() -> void:''')
code=code.replace('Phase-selected disposable inherited-input fixture','Phase-selected four-authored-state static opening review using actual inherited seam taps and25/40/55px pull segments')
code=code.replace('"goal_visible": world.prop_rect.visible if world.prop_rect != null else false,','"goal_visible": world.prop_rect.visible if world.prop_rect != null else false,\n\t\t\t"geode_pull": study.geode_pull,\n\t\t\t"authored_opening_state": "closed" if study.geode_pull <= 0.0 else "early_crack" if study.geode_pull < 40.0 else "middle_open" if study.geode_pull < 90.0 else "fully_open",')
# Only the ignored review fixture changes; production remains unchanged.
(out/'.gdignore').write_text('');(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n')
surface=(old/'study_surface.gd').read_text().replace('var open_left_texture: Texture2D','var early_crack_texture: Texture2D\nvar middle_open_texture: Texture2D\nvar open_left_texture: Texture2D')
old_work=surface[surface.index('func _draw_work_surface()'):surface.index('func _draw_geode()')];new_work=(b/'audit/job_pan_painted_mount_v3_20261001/attempt_04/study_surface.gd').read_text();new_work=new_work[new_work.index('func _draw_work_surface()'):new_work.index('func _draw_geode()')];surface=surface.replace(old_work,new_work)
mark='\t# The crystals are authored inside each half: no detached reward layer.'
assert mark in surface;surface=surface.replace(mark,'''\tif geode_pull < 90.0:
		var texture := early_crack_texture if geode_pull < 40.0 else middle_open_texture
		var height := 350.0
		var fit := Vector2(height * texture.get_width() / float(texture.get_height()), height)
		draw_texture_rect(texture, Rect2(center + Vector2(geode_pull * 0.5, 0.0) - fit * 0.5, fit), false)
		return
'''+mark)
(out/'study_surface.gd').write_text(surface,encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'executed_capture_geode_opening_v138.py')
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];before={x['path']:sha(b/x['path']) for x in snapshot};assert len(before)==325 and all(before[x['path']]==x['sha256'] for x in snapshot);write(out/'SOURCE_BEFORE.json',before)
write(out/'PROFILE.json',dict(status='FOUR_AUTHORED_STATIC_GEODE_STATES_REVIEW_ONLY',expected_views=10,baseline='edbf2a60e4a73ca149ee53b7f8d01990afd32198',states=['existing_closed','new_early_crack','new_middle_open','existing_fully_open_embedded_halves'],selection={'closed':'pull0','early_crack':'0<pull<40','middle_open':'40<=pull<90','fully_open':'90<=pull<=120'},changes='Uniform aspect-preserving350h intermediate AtlasTexture cards. Existing full endpoint halves remain320h, all native source pixels and actual inherited input retained. Aspect-preserving approved drafting slab reused. Endpoint completion callbacks disconnected solely to prevent award/save in this disposable capture.',qualification='Static native state/semantic inspection, not naturally timed articulated opening/actor/full ordinary route/device/child/owner acceptance.'))
impact=b/'design/audit_impacts/job-geode-opening-continuity-20261001.json'
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
cover();native=b/'tmp/geode_opening_v138/native_views';native.mkdir(parents=True)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(b),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(b),'--script','res://'+rel(out/'capture.gd')])];rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as c:
  try:p=subprocess.run(cmd,cwd=b,stdout=a,stderr=c,timeout=240 if name!='native' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(so.read_text(encoding='utf-8',errors='replace')[-1400:],se.read_text(encoding='utf-8',errors='replace')[-1400:],flush=True);break
passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and all(sha(b/p)==h for p,h in before.items())
if passed:shutil.copytree(native,out/'native_views')
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_MACHINE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_sources_unchanged=all(sha(b/p)==h for p,h in before.items()),qualification='Only machine capture; every native source/frame and mounted state requires direct inspection. No full ordinary career/training/story/device/child/owner pass.'));cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='Official4.7.2 analyzer, parser/inference and both-width inherited-input geode opening captures',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d);raise SystemExit(0 if passed else 1)
