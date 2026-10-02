extends SceneTree
const OUT := "res://audit/job_river_join_study_v1_20261001/attempt_07/"
const StudySurface := preload("res://audit/job_river_join_study_v1_20261001/join_surface_v7.gd")
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
	if a == b:
		finish += Vector2(12.0,0.0)
	await _event(start,true)
	for step: int in range(1,9):
		var event := InputEventScreenDrag.new()
		event.index=0
		event.position=surface.get_global_transform_with_canvas()*start.lerp(finish,float(step)/8.0)
		Input.parse_input_event(event)
		await _wait(2)
	await _event(finish,false)

func _run() -> void:
	Engine.max_fps = 30
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--width="):
			width_now=int(arg.trim_prefix("--width="))
	root.size=Vector2i(width_now,720)
	DisplayServer.window_set_size(root.size)
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
	await _line(Vector2i(4,0),Vector2i(5,0))
	await _capture("isolated_dry_straight")
	await _line(Vector2i(5,0),Vector2i(5,1))
	await _capture("isolated_dry_corner")
	await _line(Vector2i(5,0),Vector2i(6,0))
	await _capture("isolated_dry_t")
	await _line(Vector2i(5,1),Vector2i(6,1))
	await _line(Vector2i(5,1),Vector2i(4,1))
	await _line(Vector2i(5,1),Vector2i(5,2))
	await _capture("isolated_dry_cross")
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
	file.store_string(JSON.stringify({"status":"INHERITED_INPUT_FLOW_CASES_PASS_VISUAL_PENDING","views":records,"parent_script":"res://scripts/opera_geology_surface.gd","subclass":"res://audit/job_river_join_study_v1_20261001/join_surface_v7.gd","qualifications":"No production binding; actual source scores4.6 do not pass joints/flatbed/full actor-work context. Passive,isolateddry,sourcewetting,corner,branch,cross,JSONrestore and singlecompletion checked."},"\t"))
	file.close()
	print("RIVER_JOIN_CAPTURE|PASS|",width_now,"|",records.size(),"views|ONE_COMPLETION|VISUAL_PENDING")
	quit(0)
