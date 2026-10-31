extends SceneTree
## Configured current room, real GUI input. Not a natural-route, device,
## child, owner or canonical QA11 acceptance session.
const OUT := "res://assets_src/imagegen/job_art_chef_20261019/review_current_02/"
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
			world.set_process(false)
			surface.set_process(false)
			await _shot("ready")
			if requested_mode == "pourt":
				var at := surface._pour_pitcher_rect().get_center()
				await _touch(at,true)
				for tick in range(900):
					surface._process(1.0/30.0)
					if tick == 80:
						await _shot("earned-mid-pour")
					if surface.pour_level >= 0.999:
						break
				await _touch(at,false)
				_ck("pour earns filled bowl",surface.pour_level >= 0.999)
				await _shot("earned-full-pour")
			if requested_mode == "circle":
				var pivot := surface._circle_pivot()
				await _touch(pivot+Vector2(42,0),true)
				for sample in range(1,121):
					await _drag(pivot+Vector2.from_angle(float(sample)*TAU/36.0)*42.0)
					if sample in [9,18,27,36]:
						await _shot("whisk-angle-"+str(sample))
				await _touch(pivot+Vector2(42,0),false)
				_ck("stir earns progress",world.phase_progress > 0.0)
				await _shot("earned-stir")
			if requested_mode == "oven":
				for heat: float in [0.44,0.45,0.62,0.80,0.81]:
					surface.oven_t=heat
					surface.queue_redraw()
					await _shot("diagnostic-heat-"+str(heat))
				surface.oven_t=0.62
				var at := surface._oven_handle_rect().get_center()
				await _touch(at,true)
				await _touch(at,false)
				_ck("handle tap earns baked result",world.phase_progress > 0.0)
				await _shot("earned-door-open")
			if requested_mode == "swipe":
				await _touch(surface._trace_demo_point(0),true)
				for sample in range(1,65):
					await _drag(surface._trace_demo_point(float(sample)/64.0))
					if sample in [16,32,48]:
						await _shot("earned-frost-"+str(sample))
				await _touch(surface._trace_demo_point(1),false)
				_ck("source-aligned frosting earns completion",surface.trace_journey >= 0.99)
				await _shot("earned-frost-complete")
			if requested_mode == "tap":
				for index: int in range(7):
					var at := surface._target_anchor_point(index)
					await _touch(at,true)
					await _touch(at,false)
				await create_timer(0.5).timeout
				await _shot("seven-toppings")
				_ck("seven toppings earn seven goals",world.phase_progress >= 6.99)
			world.set_process(true)
			world.task_open = false
			world.action_panel.visible = false
			await process_frame
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"baseline":"6fb96aeb441952c1053cc5ce18435fc57fc1d1ab","scope":"Configured current painted phases, raw GUI earning and explicit diagnostic heat fixtures; physical device/owner acceptance separate"},"\t"))
	file.close()
	print("CHEF_CURRENT_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size(),"frames")
	quit(0 if failures.is_empty() else 1)
