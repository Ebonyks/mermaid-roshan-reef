extends SceneTree
## Configured current room, real GUI input. Not a natural-route, device,
## child, owner or canonical QA11 acceptance session.
const OUT := "res://assets_src/imagegen/job_art_chef_20261019/review_baseline/"
var m: ReefMain
var world: OperaCareerWorld2D
var surface: OperaGestureSurface
var records: Array[Dictionary] = []
var failures: Array[String] = []
var phase_id := ""
var width_now := 1280
func _initialize() -> void:
	call_deferred("_run")
func _ck(label: String, ok: bool) -> void:
	if not ok:
		failures.append(label)
		push_error("AST_ART_CAPTURE " + label)
func _shot(state: String) -> void:
	await create_timer(0.045).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d" % [phase_id,state,width_now]
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"hud":true,"phase_progress":world.phase_progress,
		"widget_fill":surface.widget_fill,"pipe_round":surface.pipe_round,
		"fixture":"configured current Castle career phase; routed GUI input"})
func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * at
	event.pressed = pressed
	root.push_input(event)
	await process_frame
func _drag(at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * at
	root.push_input(event)
	await process_frame
func _place(tile: String, cell: int) -> void:
	var slot: int = surface.pipe_tray.find(tile)
	_ck("tray has " + tile,slot >= 0)
	if slot < 0:
		return
	await _touch(surface._pipe_tray_rect(slot).get_center(),true)
	await _drag(surface._pipe_cell_rect(cell).get_center())
	await _touch(surface._pipe_cell_rect(cell).get_center(),false)
	_ck("placed " + tile + " in " + str(cell),String(surface.pipe_grid[cell]) == tile)
func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(2.0).timeout
	m._start_menu_ref()._dismiss_menu()
	m._skip_intro()
	m._day_one_ref().restore_state({"day_one_active":false})
	m.chapter2_story_complete = true
	m.pearl_count = m.PEARL_TOTAL
	m.level2_done_once = true
	m._enter_level2_now(true,false,false)
	await create_timer(0.5).timeout
	m._enter_castle_interior_now(false)
	await create_timer(0.5).timeout
	var act_index := -1
	for index: int in range(OperaHouse.ACTS.size()):
		if OperaHouse.ACTS[index].get("costume", "") == "chef":
			act_index = index
	assert(act_index >= 0)

	for aspect: int in [1280,1600]:
		width_now = aspect
		root.size = Vector2i(aspect,720)
		DisplayServer.window_set_size(root.size)
		var room := CastleCareerRoutes.room_for_act(act_index)
		m._castle_rooms_ref().show_room(room,false)
		await create_timer(0.8).timeout
		m._start_opera_from_room(act_index,room)
		for _frame: int in range(600):
			await process_frame
			if m.opera_game != null and m.opera_game.act != null and m.opera_game.act.career_world_2d != null:
				break
		world = m.opera_game.act.career_world_2d
		assert(world != null)
		for requested_mode: String in ["pourt","circle","oven","swipe","tap"]:
			var phase := -1
			for index: int in range(world.phases.size()):
				if String(world.phases[index].get("mode", "")) == requested_mode:
					phase = index
					break
			assert(phase >= 0)
			world.active = true
			world.phase_index = phase
			world._show_phase()
			world.phase_gap = 0.0
			world._open_task()
			await create_timer(0.6).timeout
			surface = world.surface as OperaGestureSurface
			assert(surface != null and world.task_open)
			phase_id = String(world.phases[phase].get("name", requested_mode)).to_lower()
			await _shot("ready")
			if requested_mode == "tap":
				for index: int in range(3):
					var at := surface._target_anchor_point(index)
					await _touch(at,true)
					await _touch(at,false)
				await create_timer(0.5).timeout
				await _shot("three-toppings")
			world.task_open = false
			world.action_panel.visible = false
			await process_frame
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"baseline":"6fb96aeb441952c1053cc5ce18435fc57fc1d1ab","scope":"Current unchanged runtime baseline; configured phases, no acceptance"},"\t"))
	file.close()
	print("CHEF_BASELINE_CAPTURE|PASS|",records.size(),"frames")
	quit()
