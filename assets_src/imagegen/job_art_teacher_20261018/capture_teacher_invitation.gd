extends SceneTree
## Configured real-world fixture with routed GUI touch. No natural-route,
## device, child, owner or canonical QA11 certification claim.
const OUT := "res://assets_src/imagegen/job_art_teacher_20261018/review/"
var m: ReefMain
var act: OperaAct
var world: OperaCareerWorld2D
var surface: OperaTeacherSurface
var records: Array[Dictionary] = []
var phase_id := ""
var width_now := 1280
var failures: Array[String] = []
func _initialize() -> void:
	call_deferred("_run")
func _shot(state: String) -> void:
	await create_timer(0.08).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d" % [phase_id, state, width_now]
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"hud":true,"runtime":true,"fixture":"configured current Opera world; routed GUI input"})
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
		var value: Dictionary = OperaHouse.ACTS[index]
		if value.get("costume", "") == "teacher":
			act_index = index
	assert(act_index >= 0)
	for aspect: int in [1280,1600]:
		# Each aspect is a fresh private-save fixture, not a resume of the
		# previous aspect's completed career.
		m.save_data["teacher_lesson_checkpoint"] = {}
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
		assert(m.opera_game != null and m.opera_game.act != null)
		act = m.opera_game.act
		world = act.career_world_2d
		assert(world != null)


		await create_timer(0.5).timeout
		phase_id = "invitation"
		var hotspot := world._active_hotspot()
		assert(hotspot != null and hotspot.motion == "painted_still")
		var original_position := hotspot.position
		var original_size := hotspot.object_size
		var period := TAU / OperaWorldHotspot2D.Affordance.pulse_speed(OperaWorldHotspot2D.Affordance.INTERACTION,false)
		for step: int in range(9):
			await _shot("idle-%d" % step)
			assert(hotspot.position == original_position and hotspot.object_size == original_size)
			await create_timer(maxf(0.01,period/8.0-0.08)).timeout
		var point := hotspot.get_global_transform_with_canvas() * hotspot.object_center
		for pressed: bool in [true,false]:
			var event := InputEventScreenTouch.new()
			event.index = 0
			event.position = point
			event.pressed = pressed
			root.push_input(event)
			await process_frame
		var opening_samples := 0
		for _frame: int in range(600):
			await process_frame
			if hotspot.opening and opening_samples < 4:
				await _shot("opening-%d" % opening_samples)
				opening_samples += 1
			if world.task_open:
				break
		if not world.task_open or opening_samples == 0:
			failures.append("Actual GUI station failed: "+str(aspect))
		await _shot("lesson-open")
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture_invitation.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"failures":failures,
		"scope":"Actual-time complete idle opacity cycle, opening and raw GUI station activation; fixed object geometry checked. No physical device/child/owner acceptance."},"\t"))
	file.close()
	print("TEACHER_INVITATION_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|", records.size())
	quit(0 if failures.is_empty() else 1)
