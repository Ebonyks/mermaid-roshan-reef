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

		for tier: int in [0,2]:
			for phase: int in range(4):
				m.save_data["teacher_lesson_checkpoint"] = {}
				world.active = true
				world.phase_index = phase
				world.phase_gap = 0.0
				world._show_phase()
				world._open_task()
				await create_timer(0.6).timeout
				surface = world.surface as OperaTeacherSurface
				if surface == null or not world.task_open:
					push_error("Teacher capture failed to open lesson")
					quit(1)
					return
				var kind: String = TeacherLessonPlan.KINDS[phase]
				var progress := {"kinds": {kind:{"tier":tier,"rounds":4}}}
				surface.set_lesson(TeacherLessonPlan.make_lesson(kind,progress))
				phase_id = "%s-tier%d" % [kind,tier]
				for _frame: int in range(300):
					if not surface.armed_only:
						break
					await process_frame
				if surface.armed_only:
					failures.append(phase_id+": remains armed")
				await _shot("ready")
				if kind == "add":
					await _tap(OperaTeacherSurface.JOIN_CENTER)
					await create_timer(0.45).timeout
					if not surface.joined:
						failures.append(phase_id+": GUI join failed")
					await _shot("joined")
				for index: int in range(surface.counted.size()):
					await _tap(surface.counter_position(index))
					if not surface.counted[index]:
						failures.append(phase_id+": GUI pearl failed"+str(index))
					if index == 0:
						await _shot("part-counted")
				if not surface.counted.is_empty():
					await _shot("all-counted")
				var choices: Array = surface.lesson["choices"]
				var wrong := (surface.answer_index()+1)%choices.size()
				await _tap(surface.choice_rect(wrong).get_center())
				if surface.wrong_attempts != 1 or surface.solved:
					failures.append(phase_id+": incorrect-answer behavior changed")
				await _shot("chosen-help")
				await _tap(surface.choice_rect(surface.answer_index()).get_center())
				if not surface.solved:
					failures.append(phase_id+": GUI answer failed")
				await _shot("correct")
				world.task_open = false
				world.action_panel.visible = false
				await process_frame
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"failures":failures,
		"scope":"Configured actual-room Mobile/HUD fixture and routed GUI actions; no natural-route/device/child/owner/canonicalQA11 acceptance"},"\t"))
	file.close()
	print("TEACHER_ART_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size()," frames; ",failures)
	quit(0 if failures.is_empty() else 1)

func _tap(at: Vector2) -> void:
	await _touch(at,true)
	await _touch(at,false)
