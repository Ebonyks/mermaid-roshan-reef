extends SceneTree
## Configured current rooms + routed GUI earning; separate from canonical route/device/owner review.
const OUT := "res://assets_src/imagegen/job_art_support_careers_20261019/review_current04/"
var m: ReefMain
var world: OperaCareerWorld2D
var surface: OperaGestureSurface
var records: Array[Dictionary] = []
var failures: Array[String] = []
var phase_id := ""
var width_now := 1280
var serial := 0

func _initialize() -> void:
	call_deferred("_run")

func _ck(label: String, ok: bool) -> void:
	if not ok:
		failures.append(phase_id + ": " + label)
		push_error("SUPPORT_CAPTURE " + phase_id + ": " + label)

func _shot(state: String) -> void:
	surface.queue_redraw()
	await create_timer(0.045).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d-%03d" % [phase_id,state,width_now,serial]
	serial += 1
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"hud":true,"phase_progress":world.phase_progress,
		"phase_goal":world.phases[world.phase_index].get("goal",0.0),"phase_index":world.phase_index,
		"part":world.phases[world.phase_index].get("performance_part","room"),
		"widget_fill":surface.widget_fill,"context":surface.visual_context,"mode":surface.mode,
		"route":surface.get_meta("support_painted_route",""),"key":surface.get_meta("support_painted_key",-1),
		"surface_origin":[surface.global_position.x,surface.global_position.y],"surface_size":[surface.size.x,surface.size.y],
		"canvas_origin":[surface.get_global_transform_with_canvas().origin.x,surface.get_global_transform_with_canvas().origin.y],
		"canvas_scale":[surface.get_global_transform_with_canvas().get_scale().x,surface.get_global_transform_with_canvas().get_scale().y],
		"roshan_visible":world.player_actor.visible,"partner_visible":world.rival_actor.visible,
		"fixture":"Configured current career phase, live Mobile rendering and routed GUI touch, not canonical natural-route/device acceptance"})

	var interim := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	interim.store_string(JSON.stringify({"captures":records,"failures":failures,"status":"IN_PROGRESS_CONFIGURED_GUI"},"\t"))
	interim.close()

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

func _tick(delta: float) -> void:
	surface._process(delta)
	world._process(delta)

func _earn() -> void:
	var mode := surface.mode
	var goal := float(world.phases[world.phase_index].get("goal",1.0))
	if mode == "hold":
		var at: Vector2 = surface._demo_finger_pose().get("at",surface.size * 0.5)
		await _touch(at,true)
		var marks := [0.12,0.31,0.45,0.57,0.69,0.80,0.91]
		var next := 0
		for tick in range(300):
			_tick(0.04)
			if next < marks.size() and surface.widget_fill >= float(marks[next]):
				await _shot("hold-"+str(next))
				next += 1
			if world.phase_advance_pending:
				break
		await _touch(at,false)
	elif mode == "xray_scan":
		await _touch(surface.xray_scanner_pos,true)
		for index in range(2):
			var target := surface._xray_target_center(index)
			var start := surface.xray_scanner_pos
			for step in range(1,5):
				await _drag(start.lerp(target,float(step)/4.0))
			await _shot("found-"+str(index))
		await _touch(surface.xray_scanner_pos,false)
	elif mode == "circle":
		var center := surface._circle_pivot()
		var radius := minf(surface.size.x,surface.size.y) * 0.25
		await _touch(center+Vector2.RIGHT*radius,true)
		var next := 0
		for step in range(1,360):
			await _drag(center+Vector2.from_angle(float(step)*TAU/40.0)*radius)
			_tick(0.015)
			if next < 3 and world.phase_progress / goal >= [0.16,0.54,0.85][next]:
				await _shot("circle-"+str(next))
				next += 1
			if world.phase_advance_pending:
				break
		await _touch(surface.pointer_pos,false)
	elif mode == "swipe" and surface._uses_authored_trace_context():
		await _touch(Vector2(5,5),true)
		await _drag(Vector2(100,5))
		await _touch(Vector2(100,5),false)
		_ck("off-object trace pays nothing",is_zero_approx(world.phase_progress))
		await _touch(surface._trace_demo_point(0),true)
		for step in range(1,81):
			await _drag(surface._trace_demo_point(float(step)/80.0))
			if step in [20,40,60]:
				_ck("partial prefix does not finish",not world.phase_advance_pending)
			if step in [8,24,44,64]:
				await _shot("trace-"+str(step))
		await _touch(surface._trace_demo_point(1),false)
	elif mode == "swipe" and surface._uses_long_push_context():
		var start := surface._long_push_start()
		var finish := surface._long_push_end()
		await _touch(start,true)
		for step in range(1,61):
			await _drag(start.lerp(finish,float(step)/60.0))
			if step in [15,30,45]:
				await _shot("herd-"+str(step))
		await _touch(finish,false)
	elif mode == "garden_plant":
		for index in range(5):
			var start := surface.garden_seed_pos
			var target := surface._garden_hole_point(index)
			await _touch(start,true)
			for step in range(1,13):
				await _drag(start.lerp(target,float(step)/12.0))
			await _touch(target,false)
			surface._process(0.12)
			await _shot("sprout-"+str(index))
			surface._process(0.5)
			await _shot("flower-"+str(index))
	elif mode == "farm_lob":
		for index in range(4):
			var anchor := surface._farm_anchor_point()
			var pull := surface._farm_demo_pull_point()
			await _touch(anchor,true)
			await _drag(pull)
			await _touch(pull,false)
			for tick in range(200):
				surface._process(0.025)
				if surface.farm_munch_t > 0 or surface.farm_complete:
					break
			await _shot("chew-"+str(index))
			surface._process(0.42)
			await _shot("happy-"+str(index))
			surface._process(0.8)
	elif mode == "magic_cabinet":
		var at := surface._cabinet_handle_rect().get_center()
		await _touch(at,true)
		var length := surface._cabinet_required_travel()
		for step in range(1,13):
			await _drag(at+Vector2.DOWN*(length*float(step)/12.0+0.1))
		await _touch(at+Vector2.DOWN*(length+1),false)
		surface._process(0.4)
		await _shot("opening")
		surface._process(0.8)
	elif mode == "paint_reveal":
		var canvas := surface._paint_canvas_rect()
		var cell := canvas.size / Vector2(10,6)
		for row in range(6):
			var at := canvas.position + Vector2(0.5,float(row)+0.5)*cell
			await _touch(at,true)
			for col in range(1,20):
				await _drag(canvas.position+Vector2(0.5+float(col)*0.5,float(row)+0.5)*cell)
			await _touch(surface.pointer_pos,false)
			await _shot("wipe-row-"+str(row))
	elif mode == "choice":
		if surface.visual_context == "lanes_magician":
			surface.start_shuffle((surface.target_choice+1)%surface.choice_count)
			for step in range(5):
				await _shot("shuffle-"+str(step))
				surface._process(0.375)
		for pick in range(30):
			var at := surface._lane_center(surface.target_choice)
			await _touch(at,true)
			await _touch(at,false)
			_tick(0.10)
			if world.phase_advance_pending:
				break
	elif mode == "tap":
		for index in range(30):
			var at := surface._target_anchor_point(surface._target_next_unplaced()) if surface._uses_anchored_targets() else surface.size*0.5
			await _touch(at,true)
			await _touch(at,false)
			_tick(0.10)
			if world.phase_advance_pending:
				break
	print("GUI_EARN_DIAG|",phase_id,"|progress=%.17f|goal=%.17f|journey=%.17f|fill=%.17f|found=%d|scancomplete=%s|pending=%s|accepted=%s" % [world.phase_progress,goal,surface.trace_journey,surface.widget_fill,surface.xray_found_count,str(surface.xray_complete),str(world.phase_advance_pending),str(surface.completion_accepted)])
	_ck("fresh GUI input earns phase",world.phase_advance_pending and surface.completion_accepted)
	await _shot("earned-end" if world.phase_advance_pending else "UNFINISHED")

func _run() -> void:
	var expected := ProjectSettings.globalize_path("res://tmp/support_capture_appdata_current04/Roaming").replace("\\", "/")
	if not OS.get_user_data_dir().replace("\\", "/").begins_with(expected + "/"):
		push_error("USERDATA_ISOLATION_FAILED_BEFORE_GAME_INITIALIZATION")
		quit(2)
		return
	print("USERDATA_ISOLATION|PASS|",OS.get_user_data_dir())
	DirAccess.make_dir_recursive_absolute(OUT)
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(2).timeout
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
	for aspect in [1280,1600]:
		width_now = aspect
		root.size = Vector2i(aspect,720)
		DisplayServer.window_set_size(root.size)
		for career: String in ["doctor","farmer","magician","painter"]:
			var act_index := -1
			for index in range(OperaHouse.ACTS.size()):
				if OperaHouse.ACTS[index].get("costume","") == career:
					act_index = index
			assert(act_index >= 0)
			var room := CastleCareerRoutes.room_for_act(act_index)
			m._castle_rooms_ref().show_room(room,false)
			await create_timer(0.6).timeout
			m._start_opera_from_room(act_index,room)
			for frame in range(600):
				await process_frame
				if m.opera_game != null and m.opera_game.act != null and m.opera_game.act.career_world_2d != null:
					break
			world = m.opera_game.act.career_world_2d
			assert(world != null)
			m.opera_game.act.set_process(false)
			for phase in range(world.phases.size()):
				world.active = true
				world.phase_index = phase
				world._show_phase()
				world.phase_gap = 0
				world._open_task()
				await create_timer(0.45).timeout
				surface = world.surface as OperaGestureSurface
				assert(surface != null and world.task_open)
				phase_id = career+"-"+str(phase)+"-"+String(world.phases[phase].get("name","")).to_lower()
				world.set_process(false)
				surface.set_process(false)
				await _shot("ready")
				_tick(0.20)
				_ck("passive wait earns nothing",is_zero_approx(world.phase_progress))
				await _earn()
				world.task_open = false
				world.action_panel.visible = false
				await process_frame
			world.set_process(true)
			m.opera_game._leave_early()
			await process_frame
			await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"failures":failures,"scope":"Configured current rooms/stage + real GUI earning; static/context candidate, canonical route/fullmotion/device/child/owner separate"},"\t"))
	file.close()
	print("SUPPORT_CURRENT_CAPTURE|","PASS" if failures.is_empty() else "FAIL","|",records.size(),"frames")
	quit(0 if failures.is_empty() else 1)
