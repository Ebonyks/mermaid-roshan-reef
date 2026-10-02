from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=b/'audit/job_pan_painted_mount_v3_20261001';assert not out.exists();out.mkdir()
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
baseline=subprocess.run(['git','rev-parse','HEAD'],cwd=b,capture_output=True,check=True).stdout.decode().strip()
assert baseline=='dea7425a1e09752bd5102fc445bd2f84b96c0010'
previous=b/'audit/job_pan_painted_mount_v2_20261001'
impact=b/'design/audit_impacts/job-pan-painted-placement-20261001.json'
write(impact,dict(id='job-pan-painted-placement-20261001',scope='Reversible pan fixture layout repair: reuse the existing source4.6 pan and crystal cluster, preserve authored pan/slab proportions, contain grains and mineral bases inside the water, and compare all18 inherited-input partial views at two native widths. Preserve all earlier reports and exact published remote receipt. No production source edits.',baseline=baseline,rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-06','DL-MED-01','DL-INT-02','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08','DL-QA-03'],findings=['MA-VIS-006','MA-PLAY-004'],files=[],validation=[dict(command='18 native inherited-input static views and unchanged325 production-source guard',result='PENDING',evidence=rel(out/'PROCESS_RECEIPT.json'))],acceptance_gaps='Complete naturally timed training/story route, connected hands, finished panning, target-device/child/owner approval and comprehensive final report remain open. Undersize room remains reference-only; no global or strict2D satisfaction.'))
code=(previous/'capture.gd').read_text().replace('tmp/pan_painted_mount_v107/native_views','tmp/pan_geometry_v112/native_views').replace('res://audit/job_pan_painted_mount_v2_20261001/study_surface.gd','res://'+rel(out/'study_surface.gd'))
code=code.replace('var original_presentations: Dictionary = {}','var original_presentations: Dictionary = {}\nvar original_object_sizes: Dictionary = {}')
code=code.replace('original_presentations[hot_prop] = hot_prop.presentation','original_presentations[hot_prop] = hot_prop.presentation\n\t\t\t\t\toriginal_object_sizes[hot_prop] = hot_prop.object_size')
code=code.replace('original_presentations.clear()','original_presentations.clear()\n\t\t\t\toriginal_object_sizes.clear()')
code=code.replace('var use_new := lane != "original"','var use_new := lane != "original"\n\t\tfor raw_hot: Control in world.station_nodes:\n\t\t\tvar lane_hot := raw_hot as OperaWorldHotspot2D\n\t\t\tlane_hot.object_size = original_object_sizes[lane_hot] as Vector2')
code=code.replace('active.presentation = "overlay"','active.presentation = "overlay"\n\t\t\tvar fit_width := active.object_size.x\n\t\t\tvar ratio := active.object_texture.get_width() / float(active.object_texture.get_height())\n\t\t\tactive.object_size = Vector2(fit_width, fit_width / ratio)')
code=code.replace('reset_hot.presentation = String(original_presentations[reset_hot])','reset_hot.presentation = String(original_presentations[reset_hot])\n\t\treset_hot.object_size = original_object_sizes[reset_hot] as Vector2')
code=code.replace('PAINTED_PAN_REFINEMENT|24_CAPTURED','PAINTED_PAN_GEOMETRY|18_CAPTURED')
code=code.replace('explicit painted drawing/layout study.','explicit aspect-preserving pan/slab drawing and safe water-region grain/mineral layout study.')
(out/'.gdignore').write_text('');(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n')
surface=(previous/'study_surface.gd').read_text()
surface=surface.replace('draw_texture_rect(work_texture, Rect2(330, 130, 860, 560), false)','var ratio := work_texture.get_width() / float(work_texture.get_height())\n\tvar fit_size := Vector2(860.0, 860.0 / ratio)\n\tdraw_texture_rect(work_texture, Rect2(WORK_RECT.get_center() - fit_size * 0.5, fit_size), false)')
surface+='''
func _draw_pan() -> void:
	if not painted_study:
		super._draw_pan()
		return
	var ratio := pan_texture.get_width() / float(pan_texture.get_height())
	var fit_size := Vector2(PAN_RECT.size.x, PAN_RECT.size.x / ratio)
	var rect := Rect2(PAN_RECT.get_center() + Vector2(pan_visual_x, 0.0) - fit_size * 0.5, fit_size)
	draw_texture_rect(pan_texture, rect, false)
	# The authored water basin occupies this normalized region; keep the source
	# and its alpha intact. Only game prop placement changes in this fixture.
	var water_center := rect.position + fit_size * Vector2(0.50, 0.44)
	var grain_count := maxi(3, 20 - floori(pan_wash * 17.0))
	for index: int in range(grain_count):
		var angle := float(index) * 2.399
		var radial := sqrt((float(index) + 0.5) / float(grain_count))
		var grain_pos := water_center + Vector2(cos(angle) * 122.0, sin(angle) * 31.0) * radial
		grain_pos.x += pan_visual_x * 0.12 + sin(float(index) + pan_visual_x * 0.02) * 6.0
		draw_circle(grain_pos, 6.0, Color("#d5a761"))
	for index: int in range(pan_minerals):
		var mineral_size := Vector2(68.0 * crystals_texture.get_width() / float(crystals_texture.get_height()), 68.0)
		var base := water_center + Vector2(-82.0 + float(index) * 82.0, 20.0)
		draw_texture_rect(crystals_texture, Rect2(base - Vector2(mineral_size.x * 0.5, mineral_size.y), mineral_size), false)
'''
(out/'study_surface.gd').write_text(surface,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'executed_capture_pan_geometry_v112.py')
remote=b/'audit/job_review_v2_20261001/geology_remote_verified_v3';assert not remote.exists();remote.mkdir()
for p in (b/'tmp/geology_supplement_remote_v111').iterdir():
 if p.is_file():shutil.copyfile(p,remote/p.name)
for p in (b/'tmp/geology_supplement_publish_v110').iterdir():
 if p.is_file():shutil.copyfile(p,remote/('publish_'+p.name))
shutil.copyfile(Path(__file__).parent/'verify_geology_remote_v111.py',remote/'executed_verify_geology_remote_v111.py')
shutil.copyfile(Path(__file__).parent/'publish_geology_supplement_v110.py',remote/'executed_publish_geology_supplement_v110.py')
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files']
before={x['path']:sha(b/x['path']) for x in snapshot};assert len(before)==325 and all(before[x['path']]==x['sha256'] for x in snapshot)
write(out/'SOURCE_BEFORE.json',before)
write(out/'PROFILE.json',dict(status='PREPARED_REVERSIBLE_SOURCE_REUSE_PLACEMENT_STUDY',baseline=baseline,views=18,pan='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/washing_pan/attempt_02/whole_canvas_1024.png',mineral='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/crystal_reward/attempt_01/whole_canvas_1024.png',whole_image_pixels_changed=False,production_bindings_changed=False,qualification='Mineral cluster reuse only in panning. Geode reveal continues to use embedded crystals in new opened-half image, never this detached cluster.'))
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for folder in [out,remote] for p in folder.rglob('*') if p.is_file()});write(impact,d)
cover()
native=b/'tmp/pan_geometry_v112/native_views';native.mkdir(parents=True)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(b),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(b),'--script','res://'+rel(out/'capture.gd')])]
rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as c:
  try:p=subprocess.run(cmd,cwd=b,stdout=a,stderr=c,timeout=240 if name!='native' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(se.read_text(encoding='utf-8',errors='replace')[-1400:],flush=True);break
passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and all(sha(b/p)==h for p,h in before.items())
if passed:shutil.copytree(native,out/'native_views')
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_MACHINE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_sources_unchanged=all(sha(b/p)==h for p,h in before.items()),qualification='Direct visual review pending; partial inherited panning fixture only, no production or final owner acceptance.'))
cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='Parser/inference/official4.7.2 analyzer/native18-view capture and325-source guard',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d)
raise SystemExit(0 if passed else 1)
