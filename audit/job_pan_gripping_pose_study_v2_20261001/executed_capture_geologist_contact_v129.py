from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old=b/'audit/job_pan_actor_contact_study_v1_20261001';out=b/'audit/job_pan_gripping_pose_study_v2_20261001';out.mkdir(exist_ok=False)
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
src='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/panning_contact/attempt_01/whole_canvas_1024.png'
code=(old/'capture.gd').read_text().replace('tmp/pan_actor_contact_v124/native_views','tmp/pan_gripping_pose_v129/native_views').replace('res://'+rel(old/'study_surface.gd'),'res://'+rel(out/'study_surface.gd'))
code=code.replace('var actor_z_before := world.player_actor.z_index','var actor_z_before := world.player_actor.z_index\n\tvar actor_visible_before := world.player_actor.visible')
code=code.replace('world.player_actor.position = Vector2(373.0 + study.pan_visual_x, 270.0)\n\t\t\tworld.player_actor.z_index = 1','world.player_actor.visible = false')
code=code.replace('world.player_actor.z_index = actor_z_before','world.player_actor.z_index = actor_z_before\n\tworld.player_actor.visible = actor_visible_before')
code=code.replace('study.grain_texture = painted_textures["pan_grain"] as Texture2D','study.grain_texture = painted_textures["pan_grain"] as Texture2D\n\t\t\t\tstudy.contact_texture = ImageTexture.create_from_image(Image.load_from_file("res://'+src+'"))')
code=code.replace('"actor_canvas_z": world.player_actor.z_index,','"actor_canvas_z": world.player_actor.z_index,\n\t\t\t"inherited_actor_visible": world.player_actor.visible,\n\t\t\t"generated_contact_source": "'+src+'",\n\t\t\t"generated_contact_sha256": FileAccess.get_sha256("res://'+src+'"),\n\t\t\t"contact_card_width": 700.0,\n\t\t\t"authored_water_center_native": [1090, 689],')
code=code.replace('unchanged geologist whole-card actor contact study. No new anatomy or source pixels; static contact only, not timed acting acceptance.','new generated static two-hand pan contact study. Legacy actor temporarily hidden only in phase-selected captures. Whole connected card uses pan_visual_x; this does not supply articulated panning motion, travel, pickup or release.')
(out/'.gdignore').write_text('');(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n')
surface=(old/'study_surface.gd').read_text();surface=surface[:surface.index('func _draw_pan()')]
surface=surface.replace('var grain_texture: Texture2D','var grain_texture: Texture2D\nvar contact_texture: Texture2D')
surface+='''func _draw_pan() -> void:
	if not painted_study:
		super._draw_pan()
		return
	# A complete generated static contact pose; no isolated limb repair.
	var ratio := contact_texture.get_width() / float(contact_texture.get_height())
	var fit_size := Vector2(700.0, 700.0 / ratio)
	var water_center := PAN_RECT.get_center() + Vector2(pan_visual_x, 0.0)
	var source_water := Vector2(1090.0 / 1536.0, 689.0 / 1024.0)
	var position := water_center - fit_size * source_water
	draw_texture_rect(contact_texture, Rect2(position, fit_size), false)
	var grain_count := maxi(3, 20 - floori(pan_wash * 17.0))
	for index: int in range(grain_count):
		var angle := float(index) * 2.399
		var radial := sqrt((float(index) + 0.5) / float(grain_count))
		var grain_pos := water_center + Vector2(cos(angle) * 100.0, sin(angle) * 17.0) * radial
		grain_pos.x += pan_visual_x * 0.08 + sin(float(index)) * 3.0
		var grain_size := Vector2(12.0 * grain_texture.get_width() / float(grain_texture.get_height()), 12.0)
		draw_texture_rect(grain_texture, Rect2(grain_pos - grain_size * 0.5, grain_size), false)
	for index: int in range(pan_minerals):
		var mineral_size := Vector2(48.0 * crystals_texture.get_width() / float(crystals_texture.get_height()), 48.0)
		var base := water_center + Vector2(-58.0 + float(index) * 58.0, 10.0)
		_draw_ellipse(base + Vector2(0.0, -2.0), Vector2(16.0, 4.0), Color(0.22, 0.60, 0.65, 0.50), Color(0.57, 0.89, 0.88, 0.85), 1.0)
		draw_texture_rect(crystals_texture, Rect2(base - Vector2(mineral_size.x * 0.5, mineral_size.y), mineral_size), false)
'''
(out/'study_surface.gd').write_text(surface,encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'executed_capture_geologist_contact_v129.py')
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];before={x['path']:sha(b/x['path']) for x in snapshot};assert len(before)==325 and all(before[x['path']]==x['sha256'] for x in snapshot);write(out/'SOURCE_BEFORE.json',before)
write(out/'PROFILE.json',dict(status='NEW_GENERATED_STATIC_CONTACT_REVIEW_ONLY',views=6,baseline='dea7425a1e09752bd5102fc445bd2f84b96c0010',source=src,source_sha256=sha(b/src),changes='Complete connected character/pan card700w uniformly drawn with water centre at inherited PAN_RECT centre and visual offset. Separate interactive grains/minerals resized/contained. Legacy actor hidden/restored during static capture only. Touch/rewards/save remain inherited. No articulated motion/full ordinary route claim.'))
impact=b/'design/audit_impacts/job-pan-painted-placement-20261001.json'
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
cover();native=b/'tmp/pan_gripping_pose_v129/native_views';native.mkdir(parents=True)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(b),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(b),'--script','res://'+rel(out/'capture.gd')])];rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as c:
  try:p=subprocess.run(cmd,cwd=b,stdout=a,stderr=c,timeout=240 if name!='native' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(se.read_text(encoding='utf-8',errors='replace')[-1400:],flush=True);break
passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and all(sha(b/p)==h for p,h in before.items())
if passed:shutil.copytree(native,out/'native_views')
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_MACHINE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_sources_unchanged=all(sha(b/p)==h for p,h in before.items()),qualification='Machine static capture only. Every native view requires direct audit; articulated motion/full ordinary route/device/child/owner remain open.'))
cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='New static contact source official4.7.2 analyzer and6-view native inherited-input capture',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d);raise SystemExit(0 if passed else 1)
