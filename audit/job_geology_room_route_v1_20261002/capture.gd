extends SceneTree
## Actual production surface and all four ordinary career phases. Only entry
## fixture and isolated test save home are supplied; no phase forcing, source
## injection, replacement surface, background overlay or completion callback patch.
const OUT := "res://audit/job_geology_room_route_v1_20261002/attempt_01/"
var main: ReefMain
var width_now := 1280
var records: Array[Dictionary] = []
var events: Array[Dictionary] = []
var motion_world: OperaCareerWorld2D
var record_motion := false
var motion_frames: Array[Dictionary] = []

func _initialize() -> void:
	_run.call_deferred()

func _wait(count: int) -> void:
	for _i: int in range(count):
		await process_frame
		if record_motion:
			await RenderingServer.frame_post_draw
			_motion_frame()

func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = at
	event.pressed = pressed
	Input.parse_input_event(event)
	await _wait(2)

func _surface_touch(surface: Control, at: Vector2, pressed: bool) -> void:
	await _touch(surface.get_global_transform_with_canvas() * at, pressed)

func _drag(surface: Control, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * at
	Input.parse_input_event(event)
	await _wait(2)

func _segment(surface: Control, start: Vector2, end: Vector2) -> void:
	for step: int in range(1, 11):
		await _drag(surface, start.lerp(end, float(step) / 10.0))

func _motion_frame() -> void:
	var index := motion_frames.size()
	var path := OUT + "native_frames/geode_%d_%04d.webp" % [width_now,index]
	var image := root.get_texture().get_image()
	assert(image.save_webp(path,true) == OK)
	var phase := -1
	var state: Dictionary = {}
	if is_instance_valid(motion_world):
		phase = motion_world.phase_index
		if is_instance_valid(motion_world.surface):
			state = (motion_world.surface as OperaGeologySurface).progress_snapshot()
	motion_frames.append({"index":index,"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
		"width":width_now,"time_msec":Time.get_ticks_msec(),"surface":state,
		"phase_index":phase,"game":main.game,"room":main.castle_room_id,"act_active":main.opera_game != null,
		"direct_review":false,"scores":{},"owner_acceptance":null})

func _capture(world: OperaCareerWorld2D, state_name: String) -> void:
	await RenderingServer.frame_post_draw
	var name := "geologist_%d_phase%d_%s.webp" % [width_now,world.phase_index,state_name]
	var path := OUT + "native_views/" + name
	var image := root.get_texture().get_image()
	assert(image.save_webp(path,true) == OK)
	records.append({"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
		"phase_index":world.phase_index,"state":state_name,"viewport":[width_now,720],
		"surface":(world.surface as OperaGeologySurface).progress_snapshot(),"direct_review":false,"scores":{}})

func _screen(state_name: String) -> void:
	await RenderingServer.frame_post_draw
	var path := OUT + "native_views/geologist_%d_%s.webp" % [width_now,state_name]
	var image := root.get_texture().get_image()
	assert(image.save_webp(path,true) == OK)
	records.append({"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
		"state":state_name,"viewport":[width_now,720],"game":main.game,"room":main.castle_room_id,
		"act_active":main.opera_game != null,"direct_review":false,"scores":{}})

func _tap_control(control: Control) -> void:
	var at := control.get_global_transform_with_canvas() * (control.size * 0.5)
	await _touch(at,true)
	await _touch(at,false)

func _open(world: OperaCareerWorld2D) -> void:
	for tick: int in range(300):
		var candidate := world._active_hotspot()
		if candidate != null and candidate.visible:
			break
		await _wait(1)
	var hot := world._active_hotspot()
	assert(hot != null and hot.visible and not world.task_open)
	await _capture(world, "invitation")
	var at := hot.touch_button.get_global_transform_with_canvas() * (hot.touch_button.size * 0.5)
	await _touch(at, true)
	await _touch(at, false)
	for tick: int in range(360):
		if world.task_open:
			break
		await _wait(1)
	assert(world.task_open)
	await _wait(8)
	await _capture(world, "task_open")
	events.append({"event":"viewport_invitation_arrival_open","phase_index":world.phase_index,"task_open":world.task_open})

func _work(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as OperaGeologySurface
	match surface.mode:
		"geology_river":
			await _surface_touch(surface, surface.river_path_point(0), true)
			for point: int in range(1, OperaGeologySurface.RIVER_PATH.size()):
				await _segment(surface, surface.river_path_point(point - 1), surface.river_path_point(point))
			await _surface_touch(surface, surface.pointer_pos, false)
		"geology_fossil":
			var cell := Vector2(OperaGeologySurface.FOSSIL_RECT.size.x / OperaGeologySurface.FOSSIL_GRID_COLS,
				OperaGeologySurface.FOSSIL_RECT.size.y / OperaGeologySurface.FOSSIL_GRID_ROWS)
			var at := OperaGeologySurface.FOSSIL_RECT.position + cell * 0.5
			await _surface_touch(surface, at, true)
			for row: int in range(OperaGeologySurface.FOSSIL_GRID_ROWS):
				var column := OperaGeologySurface.FOSSIL_GRID_COLS - 1 if row % 2 == 0 else 0
				var next := OperaGeologySurface.FOSSIL_RECT.position + (Vector2(column,row) + Vector2(0.5,0.5)) * cell
				await _segment(surface, at, next)
				at = next
				if row == 0:
					await _capture(world, "partial_brush")
			await _surface_touch(surface, at, false)
			assert(surface.fossil_stage == 1)
			await _capture(world, "brushed")
			for piece: int in range(3):
				await _surface_touch(surface, surface.fossil_piece_home(piece), true)
				await _segment(surface, surface.fossil_piece_home(piece), surface.fossil_piece_target(piece))
				await _surface_touch(surface, surface.fossil_piece_target(piece), false)
				if piece < 2:
					await _capture(world, "one_piece" if piece == 0 else "two_pieces")
		"geology_pan":
			var center := OperaGeologySurface.PAN_RECT.get_center()
			var at := center
			await _surface_touch(surface, at, true)
			for swing: int in range(OperaGeologySurface.PAN_REQUIRED_REVERSALS + 1):
				var direction := 1.0 if swing % 2 == 0 else -1.0
				var next := center + Vector2(direction * 150.0, 0.0)
				await _segment(surface, at, next)
				at = next
				if swing < 2:
					await _capture(world, "pan_right" if swing == 0 else "pan_left")
				if swing == 3:
					await _capture(world, "partial_pan")
			await _surface_touch(surface, at, false)
		"geology_geode":
			await _wait(120)
			assert(is_zero_approx(surface.progress()) and not world.phase_advance_pending)
			events.append({"event":"passive_open_no_progress","phase_index":world.phase_index})
			for seam: int in range(OperaGeologySurface.GEODE_SEAM_SPOTS.size()):
				var at := surface.geode_seam_spot(seam)
				await _surface_touch(surface, at, true)
				await _surface_touch(surface, at, false)
			await _capture(world, "five_seams_ready")
			motion_world = world
			record_motion = true
			var at := surface.geode_half_center()
			await _surface_touch(surface, at, true)
			await _segment(surface, at, at + Vector2(25,0))
			await _surface_touch(surface, at + Vector2(25,0), false)
			assert(is_equal_approx(surface.geode_pull,25))
			await _capture(world, "early_crack")
			for target: float in [65.0,95.0,120.0]:
				at = surface.geode_half_center()
				var amount := target - surface.geode_pull
				await _surface_touch(surface, at, true)
				await _segment(surface, at, at + Vector2(amount,0))
				await _surface_touch(surface, at + Vector2(amount,0), false)
				assert(is_equal_approx(surface.geode_pull,target))
				if target < 120.0:
					await _capture(world, "middle_open" if target == 65.0 else "full_interior_before_award")
	assert(surface._completion_emitted and world.phase_advance_pending)
	assert(world.player_actor.position.x < 310.0,
		"Celebration actor must remain outside the opaque work panel")
	await _capture(world, "earned_completion")
	events.append({"event":"intentional_completed","phase_index":world.phase_index,"progress":surface.progress()})

func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--width="):
			width_now = arg.trim_prefix("--width=").to_int()
	root.size = Vector2i(width_now,720)
	DisplayServer.window_set_size(root.size)
	assert(DirAccess.make_dir_recursive_absolute(OUT + "native_views/") == OK)
	assert(DirAccess.make_dir_recursive_absolute(OUT + "native_frames/") == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main._enter_castle_interior_now(false)
	await _wait(20)
	main._chapter_two_ref().restore_state({})
	main.save_data["opera_geology_checkpoint"] = {}
	var rooms := main._castle_rooms_ref()
	rooms.show_room("library",false)
	await _wait(12)
	var routes := main._castle_career_routes_ref()
	routes.sync()
	var slot := -1
	for index: int in range(OperaHouse.ACTS.size()):
		if String((OperaHouse.ACTS[index] as Dictionary).get("costume","")) == "geologist":
			slot = index
	assert(slot >= 0 and CastleCareerRoutes.room_for_act(slot) == "library")
	assert(not ChapterTwoCareerSceneAdapter.CAREER_ORDER.has("geologist"))
	assert(not OperaPerformancePlan.ENABLED.has("geologist"))
	var card := routes.button_for_act(slot)
	assert(card != null and card.is_visible_in_tree())
	await _screen("normal_library_card")
	await _tap_control(card)
	for tick: int in range(900):
		if main.opera_game != null and main.opera_game.act != null:
			break
		await _wait(1)
	assert(main.opera_game != null and main.opera_game.act != null)
	var world: OperaCareerWorld2D = main.opera_game.act.career_world_2d
	assert(world != null and world.phase_index == 0 and world.phases.size() == 4)
	assert(not world.using_chapter_two_phases and not world.two_act_enabled)
	events.append({"event":"actual_library_picture_card_entry","slot":slot})
	for phase: int in range(4):
		assert(world.phase_index == phase)
		await _open(world)
		await _work(world)
		if phase < 3:
			for tick: int in range(300):
				if world.phase_index == phase + 1:
					break
				await _wait(1)
			assert(world.phase_index == phase + 1)
	for tick: int in range(600):
		if main.opera_game == null:
			break
		await _wait(1)
	assert(main.opera_game == null and main.game == "level2" and main.castle_room_id == "library")
	await _wait(20)
	record_motion = false
	assert(main.castle_room_layer.visible)
	await _screen("actual_earned_library_return")
	events.append({"event":"actual_earned_completion_library_return","stars":main.opera_stars})
	rooms.show_room("opera_hall",false)
	await _wait(12)
	routes.sync()
	assert(routes.open_opera_venue())
	await _wait(12)
	var venue := routes.opera_venue
	await _screen("actual_opera_venue")
	var elevator := venue.get_node("OperaLeftElevatorPlaytest") as Button
	await _tap_control(elevator)
	await _wait(8)
	var menu := venue.job_playtest_menu
	assert(menu.session_open and menu.visible)
	await _screen("actual_elevator_menu")
	var dev_card: Button = null
	for button: Button in menu.job_buttons:
		if int(button.get_meta("act_index",-1)) == slot:
			dev_card = button
	assert(dev_card != null)
	await _tap_control(dev_card)
	await _wait(20)
	assert(main.opera_game != null and main.opera_game.dev_playtest)
	await _screen("actual_dev_geologist_entry")
	await _tap_control(main.global_navigation_button)
	await _wait(12)
	assert(main.opera_game == null and menu.visible and menu.session_open)
	await _screen("actual_dev_back_menu")
	var file := FileAccess.open(OUT + "CAPTURE_%d.json" % width_now,FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"ACTUAL_LIBRARY_ALL4_PHASES_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING",
		"views":records,"events":events,"motion_frames":motion_frames,"width":width_now,
		"qualification":"Isolated main/Castle entry fixture and save home; actual Library card/elevator touch, normal phase inputs, production OperaAct callback and earned room return. No forced phases/results/callback patches or source replacement. Geologist has no separate ChapterTwo story set or two-act stage rollout. Not device/child/owner acceptance. Native capture readback slows wall clock."},"\t"))
	file.close()
	print("GEOLOGY_ROOM_ROUTE|ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK|",width_now,"|PASS_CAPTURE_REVIEW_PENDING")
	quit(0)
