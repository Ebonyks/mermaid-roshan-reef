from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');prefix='audit/job_river_join_study_v1_20261001';f=b/prefix
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=b,text=True).strip();assert base=='40b1c7bfe025f284507c586fea61b9dd76b61423'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert not f.exists();f.mkdir()
impact=b/'design/audit_impacts/job-geology-river-join-study-20261001.json'
write(impact,{'id':'job-geology-river-join-study-20261001','baseline':base,'scope':'Continue owner-requested reversible job artwork refinement. Test the four selected4.6 painted river source components through the inherited9x5 excavation, source-connected wetting, arbitrary paths, branches, JSON restore, cancel and single completion. Non-runtime subclass changes drawing only; actual parent input/flow/save remain inherited. Preserve every candidate and failed join view; no production binding, room/actor/full-route/action/device/child/owner/whole-game acceptance. Existing old flat work bed is deliberately retained as separately scored context. Inventory before any new generation: complete ring nodes and open channel strips may overlap at branch centres, a concrete geometry gap to measure before regenerating.','rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-INT-01','DL-INT-02','DL-INT-03','DL-INT-04','DL-INT-06','DL-MED-01','DL-MOT-02','DL-QA-03','DL-QA-06','DL-READ-02','DL-READ-05','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-07','DL-VIS-08'],'findings':['MA-PLAY-004','MA-VIS-006'],'files':[],'validation':[{'command':'Selected river source inventory','result':'PASS','evidence':'assets_src/imagegen/geologist_river_components_v1_20261001/REVIEW.json: four selected source-only4.6; closed channels4.0 rejected. No runtime pass.'}],'acceptance_gaps':'Native join study and individual scores pending. Sources remain unbound; actual game still3.5/3.8. Room/contact/ordinary routes/training/story/fulltimed action/device/child/owner/global open.'})
(f/'.gdignore').write_text('',encoding='utf-8')
source=b/'assets_src/imagegen/geologist_river_components_v1_20261001/REVIEW.json';r=read(source)
write(f/'SOURCE_INVENTORY.json',{'baseline':base,'review_path':source.relative_to(b).as_posix(),'review_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'selected':[x for x in r['components'] if x['source_score']==4.6],'native_derivatives':r['technical_derivatives'],'reuse_decision':'Reuse all four selected exact painted regions without editing pixels. Review overlap before authoring corner/T/cross pieces or a replacement bed. No suitable connected junction component yet identified.','ordinary_parent_mechanics':'9columns/5rows,88x76 centres; brush46; source-connected flooding, arbitrary connected path valid.'})
gd=r'''extends OperaGeologySurface
## Non-runtime source join study. Input, saves and flow stay on the actual parent.
const SOURCE := "res://assets_src/imagegen/geologist_river_components_v1_20261001/"
var dry_node: Texture2D
var wet_node: Texture2D
var dry_channel: Texture2D
var wet_channel: Texture2D

func _load_textures() -> void:
	super._load_textures()
	dry_node = _native_region("attempt_01/whole_canvas_1024.png", Rect2(44,167,560,547))
	wet_node = _native_region("attempt_01/whole_canvas_1024.png", Rect2(655,167,560,547))
	dry_channel = _native_region("attempt_02/whole_canvas_1024.png", Rect2(38,310,1180,300))
	wet_channel = _native_region("attempt_02/whole_canvas_1024.png", Rect2(37,734,1181,302))

func _native_region(path: String, native_rect: Rect2) -> Texture2D:
	var source := Image.load_from_file(SOURCE + path)
	assert(source != null and source.get_size() == Vector2i(1024,1024))
	var atlas := AtlasTexture.new()
	atlas.atlas = ImageTexture.create_from_image(source)
	atlas.region = Rect2(native_rect.position * 1024.0 / 1254.0,
		native_rect.size * 1024.0 / 1254.0)
	return atlas

func _draw_node(texture: Texture2D, center: Vector2, art_width: float) -> void:
	var art_size := Vector2(art_width, art_width * texture.get_height() / float(texture.get_width()))
	draw_texture_rect(texture, Rect2(center - art_size * 0.5, art_size), false)

func _draw_channel(texture: Texture2D, start: Vector2, finish: Vector2) -> void:
	var length_now := start.distance_to(finish)
	var height_now := length_now * texture.get_height() / float(texture.get_width())
	draw_set_transform((start + finish) * 0.5, (finish - start).angle())
	draw_texture_rect(texture, Rect2(Vector2(-length_now,-height_now) * 0.5,
		Vector2(length_now,height_now)), false)
	draw_set_transform(Vector2.ZERO)

func _draw_river() -> void:
	var flowing := _river_flow_indices()
	# Nodes first and complete open strips afterward: the study audits these joins.
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS, index / RIVER_COLS)
		_draw_node(wet_node if flowing.has(index) else dry_node,
			river_path_cell_center(cell), 60.0)
	_draw_node(wet_node,river_path_point(0),86.0)
	_draw_node(wet_node if _river_connected() else dry_node,
		river_path_point(RIVER_PATH.size()-1),94.0)
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS, index / RIVER_COLS)
		for step: Vector2i in [Vector2i.RIGHT,Vector2i.DOWN]:
			var next := cell + step
			if next.x < RIVER_COLS and next.y < RIVER_ROWS \
					and river_wet[next.y * RIVER_COLS + next.x]:
				_draw_channel(wet_channel if flowing.has(index) else dry_channel,
					river_path_cell_center(cell),river_path_cell_center(next))
	if held:
		_draw_brush(pointer_pos)
'''
(f/'join_surface.gd').write_text(gd,encoding='utf-8',newline='\n')
capture=r'''extends SceneTree
const OUT := "res://audit/job_river_join_study_v1_20261001/attempt_01/"
const StudySurface := preload("res://audit/job_river_join_study_v1_20261001/join_surface.gd")
var surface: OperaGeologySurface
var width_now := 1280
var records: Array[Dictionary] = []
var completions := 0

func _initialize() -> void:
	_run.call_deferred()

func _wait(count: int) -> void:
	for tick: int in range(count):
		await process_frame

func _gesture(_kind: String,_amount: float,_quality: float) -> void:
	completions += 1

func _capture(label: String) -> void:
	surface.set_process(false)
	surface.queue_redraw()
	await _wait(3)
	var image := root.get_texture().get_image()
	var path := OUT + "native_views/river_%d_%s.webp" % [width_now,label]
	assert(image.save_webp(path,true)==OK)
	records.append({"state":label,"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),"dimensions":[width_now,720],"cleared_cells":surface.river_wet.count(true),"flowing_cells":surface._river_flow_indices().size(),"connected":surface._river_connected(),"completions":completions,"snapshot":surface.progress_snapshot(),"direct_review":false,"qualification":"Non-runtime subclass, actual inherited9x5 input/flow. Isolated component/network drawing study; absent actor/room/route not scored."})
	surface.set_process(true)

func _event(at: Vector2,pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index=0
	event.position=surface.get_global_transform_with_canvas()*at
	event.pressed=pressed
	Input.parse_input_event(event)
	await _wait(2)

func _line(a: Vector2i,b: Vector2i) -> void:
	var start := surface.river_path_cell_center(a)
	var finish := surface.river_path_cell_center(b)
	await _event(start,true)
	for step: int in range(1,9):
		var event := InputEventScreenDrag.new()
		event.index=0
		event.position=surface.get_global_transform_with_canvas()*start.lerp(finish,float(step)/8.0)
		Input.parse_input_event(event)
		await _wait(2)
	await _event(finish,false)

func _run() -> void:
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--width="):
			width_now=int(arg.trim_prefix("--width="))
	root.size=Vector2i(width_now,720)
	RenderingServer.set_default_clear_color(Color("#dbe9ec"))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT+"native_views"))
	surface=StudySurface.new()
	surface.size=Vector2(1280,720)
	surface.position=Vector2((width_now-1280)*0.5,0)
	root.add_child(surface)
	surface.configure("geology_river",Color.WHITE)
	surface.armed_only=false
	surface.demo_active=false
	surface.gesture.connect(_gesture)
	await _wait(120)
	assert(surface.river_wet.count(true)==0 and completions==0)
	await _capture("dry_initial")
	await _line(Vector2i(4,0),Vector2i(4,0))
	assert(surface.river_wet.count(true)==1 and surface._river_flow_indices().is_empty())
	await _capture("isolated_dry")
	await _line(Vector2i(0,2),Vector2i(2,2))
	assert(surface._river_flow_indices().size()==3 and completions==0)
	await _capture("connected_straight")
	await _line(Vector2i(2,2),Vector2i(2,1))
	await _capture("connected_corner")
	await _line(Vector2i(2,2),Vector2i(3,2))
	await _capture("connected_t_branch")
	await _line(Vector2i(2,2),Vector2i(2,3))
	await _capture("connected_cross")
	var saved := surface.progress_snapshot()
	surface.cancel_input()
	surface.configure("geology_river",Color.WHITE)
	surface.restore_progress(JSON.parse_string(JSON.stringify(saved)) as Dictionary)
	surface.demo_active=false
	assert(surface.touch_owner==-1 and completions==0)
	await _capture("partial_json_restored")
	await _line(Vector2i(2,1),Vector2i(4,1))
	assert(surface._river_flow_indices().has(4))
	await _capture("formerly_isolated_now_wet")
	await _line(Vector2i(4,1),Vector2i(4,3))
	await _line(Vector2i(4,3),Vector2i(6,3))
	await _line(Vector2i(6,3),Vector2i(6,2))
	await _line(Vector2i(6,2),Vector2i(8,2))
	assert(surface._river_connected() and completions==1)
	await _capture("connected_complete")
	await _line(Vector2i(0,2),Vector2i(8,2))
	assert(completions==1)
	await _capture("quiet_single_completion")
	var file := FileAccess.open(OUT+"MANIFEST_%d.json"%width_now,FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"INHERITED_INPUT_FLOW_CASES_PASS_VISUAL_PENDING","views":records,"parent_script":"res://scripts/opera_geology_surface.gd","subclass":"res://audit/job_river_join_study_v1_20261001/join_surface.gd","qualifications":"No production binding; actual source scores4.6 do not pass joints/flatbed/full actor-work context. Passive,isolateddry,sourcewetting,corner,branch,cross,JSONrestore and singlecompletion checked."},"\t"))
	file.close()
	print("RIVER_JOIN_CAPTURE|PASS|",width_now,"|",records.size(),"views|ONE_COMPLETION|VISUAL_PENDING")
	quit(0)
'''
(f/'capture_join_study.gd').write_text(capture,encoding='utf-8',newline='\n')
(f/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Painted river join study — pending</title><h1>Painted river joins: pending native review</h1><p>Isolated non-runtime subclass tests selected painted sources with inherited9×5 input/flow. Source4.6 does not approve network joins, flat work bed, absent actor or full job.</p><a href="SOURCE_INVENTORY.json">Reuse inventory</a></html>',encoding='utf-8')
shutil.copyfile(__file__,f/Path(__file__).name)
# Preserve completed checkpoint receipt/journal separately from its immutable revision.
remote=f/'painted_work_remote_verified_i';remote.mkdir()
for src,name in [(b/'tmp/geology_work_remote_v183/RESULT.json','RESULT.json'),(b/'tmp/geology_work_remote_v183/VERIFICATION_JOURNAL.jsonl','VERIFICATION_JOURNAL.jsonl'),(b/'tmp/geology_work_publish_v183/RECEIPT.json','PUBLISH_RECEIPT.json'),(b/'tmp/geology_work_publish_v183/COMMIT_MESSAGE.txt','COMMIT_MESSAGE.txt'),(b/'tmp/geology_work_resume_v192/RECEIPT.json','SEAL_RECEIPT.json')]:
 assert src.is_file();shutil.copyfile(src,remote/name)
d=read(impact);d['files']=sorted({p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(impact,d)
print('Isolated river join study prepared; current production checkpoint untouched.')
