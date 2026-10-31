extends SceneTree
## Configured current room with routed GUI input. Not canonical QA11/device/owner evidence.
const OUT := "res://assets_src/imagegen/job_art_nursery_20261019/review_current01/"
var m: ReefMain
var world: OperaCareerWorld2D
var surface: OperaGestureSurface
var input_surface: Control
var records: Array[Dictionary] = []
var failures: Array[String] = []
var phase_id := ""
var width_now := 1280
func _initialize() -> void:
	call_deferred("_run")
func _ck(label: String, ok: bool) -> void:
	if not ok:
		failures.append(label)
		push_error("NURSERY_CAPTURE " + label)
func _shot(state: String) -> void:
	await create_timer(0.045).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d" % [phase_id,state,width_now]
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"hud":true,"phase_progress":world.phase_progress,
		"widget_fill":surface.widget_fill,"roshan_world_visible":world.player_actor.visible,
		"roshan_source":world.player_actor.texture.resource_path if world.player_actor.texture != null else "",
		"partner_visible":world.rival_actor.visible,
		"fixture":"configured current Castle career phase; routed GUI input"})
func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = input_surface.get_global_transform_with_canvas() * at
	event.pressed = pressed
	root.push_input(event)
	await process_frame
func _drag(at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = input_surface.get_global_transform_with_canvas() * at
	root.push_input(event)
	await process_frame
func _hold_steps() -> void:
	var at: Vector2 = surface._demo_finger_pose().get("at",surface.size * 0.5)
	await _touch(at,true)
	var marks := [0.17,0.34,0.50,0.68,0.84,0.99]
	var next_mark := 0
	for tick: int in range(400):
		world._process(0.025)
		if next_mark < marks.size() and surface.widget_fill >= float(marks[next_mark]):
			await _shot("earned-hold-"+str(next_mark))
			next_mark += 1
		if world.phase_advance_pending:
			break
	await _touch(at,false)
	_ck("hold reaches exact phase goal",world.phase_advance_pending and surface.completion_accepted)
	await _shot("earned-complete")
func _run() -> void:
	var expected := ProjectSettings.globalize_path("res://tmp/nursery_capture_appdata_current01/Roaming").replace("\\", "/")
	if not OS.get_user_data_dir().replace("\\", "/").begins_with(expected + "/"):
		push_error("USERDATA_ISOLATION_FAILED_BEFORE_GAME_INITIALIZATION")
		quit(2)
		return
	print("USERDATA_ISOLATION|PASS|", OS.get_user_data_dir())
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
		if OperaHouse.ACTS[index].get("costume", "") == "nursery":
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
		for requested_name: String in ["WASH HANDS","CATCH BABIES","FEED","BURP","BEDTIME"]:
			var phase := -1
			for index: int in range(world.phases.size()):
				if String(world.phases[index].get("name", "")) == requested_name:
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
			input_surface = surface
			phase_id = requested_name.to_lower().replace(" ","-")
			world.set_process(false)
			surface.set_process(false)
			_ck("Faron remains visible",world.rival_actor.visible)
			await _shot("ready")
			if requested_name in ["WASH HANDS","FEED"]:
				world._process(0.2)
				_ck("passive hold pays nothing",is_zero_approx(world.phase_progress))
				if requested_name == "WASH HANDS":
					_ck("connected wash owns the sole Roshan picture",not world.player_actor.visible)
				else:
					_ck("world Roshan restored for care",world.player_actor.visible)
				await _hold_steps()
			elif requested_name == "CATCH BABIES":
				var catcher := world.nursery_catch
				input_surface = catcher
				catcher.set_process(false)
				for tick: int in range(600):
					catcher._process(1.0/30.0)
					if not catcher.safe_landings.is_empty():
						break
				_ck("miss remains safe with no passive catch",catcher.missed > 0 and catcher.caught == 0 and world.phase_progress == 0)
				await _shot("passive-safe-pillow")
				await _touch(Vector2(catcher.size.x*0.5,catcher.size.y*0.8),true)
				var prior_caught := 0
				for tick: int in range(3600):
					if tick % 6 == 0:
						var target := catcher.lowest_baby_x()
						await _drag(Vector2((target if target >= 0 else 0.5)*catcher.size.x,catcher.size.y*0.8))
					catcher._process(1.0/30.0)
					if catcher.caught != prior_caught:
						prior_caught=catcher.caught
						await _shot("earned-catch-"+str(prior_caught))
					if catcher.caught >= 5:
						break
				await _touch(Vector2(catcher.size.x*0.5,catcher.size.y*0.8),false)
				_ck("fresh GUI steering earns all five",catcher.caught == 5 and world.phase_advance_pending)
				input_surface=surface
			elif requested_name == "BURP":
				var at := surface._nursery_burp_hand_point(1)
				for pat: int in range(4):
					await _touch(at,true)
					await _touch(at,false)
					surface._process(0.105)
					await _shot("pat-approach-"+str(pat))
					surface._process(0.105)
					await _shot("pat-contact-"+str(pat))
					surface._process(0.21)
					await _shot("pat-settle-"+str(pat))
					if pat < 3:
						world._process(0.56)
				_ck("four paced GUI pats earn exact goal",world.phase_advance_pending and is_equal_approx(world.phase_progress,4.0))
			elif requested_name == "BEDTIME":
				var first := surface._nursery_bedtime_grab_point(0)
				await _touch(Vector2(5,5),true)
				await _drag(Vector2(5,120))
				await _touch(Vector2(5,120),false)
				await _touch(first,true)
				await _drag(first+Vector2.UP*70)
				await _touch(first+Vector2.UP*70,false)
				_ck("outside/upwards swipe does not tuck",world.phase_progress==0 and surface._nursery_bedtime_next_blanket()==0)
				await _shot("wrong-direction-unearned")
				for baby: int in range(3):
					var at := surface._nursery_bedtime_grab_point(baby)
					var length := surface._nursery_bedtime_required_travel()
					await _touch(at,true)
					for step: int in range(1,11):
						await _drag(at+Vector2.DOWN*(length*float(step)/10.0+0.1))
						if step in [2,5,8]:
							_ck("partial cloth is not earned",not surface.nursery_blankets_tucked[baby])
							await _shot("quilt-"+str(baby)+"-partial-"+str(step))
					await _touch(at+Vector2.DOWN*(length+1),false)
					await _shot("quilt-"+str(baby)+"-earned")
				_ck("three unique tucks earn exact goal",surface.nursery_blankets_tucked==[true,true,true] and is_equal_approx(world.phase_progress,3.0) and world.phase_advance_pending)
			world.set_process(true)
			world.task_open=false
			world.action_panel.visible=false
			await process_frame
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"baseline":"e90c0daa83cf05644f0e9942e85c1198ed7901f7","failures":failures,"scope":"Configured current nursery; raw GUI earning and explicit passive/wrong/partial negatives; source/frame receipts separate from canonical/device/child/owner acceptance"},"\t"))
	file.close()
	print("NURSERY_CURRENT_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size(),"frames")
	quit(0 if failures.is_empty() else 1)
