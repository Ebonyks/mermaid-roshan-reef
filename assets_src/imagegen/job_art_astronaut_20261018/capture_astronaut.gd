extends SceneTree
## Configured current room, real GUI input. Not a natural-route, device,
## child, owner or canonical QA11 acceptance session.
const OUT := "res://assets_src/imagegen/job_art_astronaut_20261018/review/"
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
		if OperaHouse.ACTS[index].get("costume", "") == "astronaut":
			act_index = index
	assert(act_index >= 0)
	for aspect: int in [1280,1600]:
		m.opera_progress = 0
		m.opera_done = false
		m.opera_stars = 0
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
		for requested_mode: String in ["pipe","tap","circle","hold"]:
			var phase := -1
			for index: int in range(world.phases.size()):
				if String(world.phases[index].get("mode", "")) == requested_mode:
					phase = index
					break
			assert(phase >= 0)
			world.active = true
			world.phase_index = phase
			world.phase_gap = 0.0
			world._show_phase()
			world.phase_gap = 0.0
			world._open_task()
			await create_timer(0.6).timeout
			surface = world.surface as OperaGestureSurface
			assert(surface != null and world.task_open)
			phase_id = {"pipe":"pipes","tap":"patch","circle":"valve","hold":"launch"}[requested_mode]
			await _shot("ready")
			match requested_mode:
				"pipe":
					await _place("H",5)
					await _shot("one-pipe")
					await _place("H",6)
					await create_timer(0.45).timeout
					await _shot("fuel-moving")
					await create_timer(1.0).timeout
					await _shot("round-one-intake-filled")
					await create_timer(2.0).timeout
					_ck("first pipe round earned",surface.pipe_round == 1)
					await _shot("round-two-napping-imp")
					for pair: Array in [["SE",0],["H",1],["SW",2],["NE",6]]:
						await _place(String(pair[0]),int(pair[1]))
					await _shot("elbows-connected")
					await create_timer(0.85).timeout
					await _shot("elbows-fueled")
					await create_timer(1.0).timeout
					await _shot("round-two-intake-filled")
					await create_timer(2.0).timeout
					_ck("second pipe round earned",surface.pipe_round == 2)
					await _shot("round-three")
				"tap":
					for index: int in range(surface._target_anchor_count()):
						var at := surface._target_anchor_point(index)
						await _touch(at,true)
						await _touch(at,false)
						_ck("patch earned " + str(index),surface.target_placed[index])
						await _shot("patch-%d-bounce" % index)
						await create_timer(0.43).timeout
						await _shot("patch-%d-settled" % index)
				"circle":
					var center := surface._crank_action_rect().get_center()
					var radius := surface._crank_action_rect().size.x * 0.36
					await _touch(center + Vector2(radius,0),true)
					for index: int in range(1,37):
						await _drag(center + Vector2.from_angle(float(index)*TAU/24.0)*radius)
						if index % 18 == 0:
							await _shot("turn-%d" % index)
					await _touch(center + Vector2(radius,0),false)
					_ck("valve GUI circles earn progress",world.phase_progress > 0.5)
				"hold":
					var at := surface._charge_action_rect().get_center()
					await _touch(at,true)
					for index: int in range(1,10):
						await create_timer(0.43).timeout
						await _shot("hold-%d" % index)
					_ck("launch hold earns progress",world.phase_progress > 3.0)
					await _touch(at,false)
			world.task_open = false
			world.action_panel.visible = false
			await process_frame
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"failures":failures,
		"scope":"Configured current world, live GUI input; no natural route/external/canonical QA11 acceptance"},"\t"))
	file.close()
	print("AST_ART_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size()," Mobile/HUD frames")
	quit(0 if failures.is_empty() else 1)
