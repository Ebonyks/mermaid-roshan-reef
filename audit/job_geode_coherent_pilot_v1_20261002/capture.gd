extends SceneTree
## Non-runtime inherited seven-state visual pilot; ordinary four-phase touch work.
## Surface replacement and initial phase0 rebind are explicit fixtures.
## No later phase forcing, background overlay or completion callback patch.
const OUT := "res://audit/job_geode_coherent_pilot_v1_20261002/attempt_01/"
const StudySurface := preload("res://audit/job_geode_coherent_pilot_v1_20261002/study_surface.gd")
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
	var path := OUT + "native_views/geode_%d_%04d.webp" % [width_now,index]
	var image := root.get_texture().get_image()
	assert(image.save_webp(path,true) == OK)
	var surface := motion_world.surface as OperaGeologySurface
	motion_frames.append({"index":index,"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
		"width":width_now,"time_msec":Time.get_ticks_msec(),"pull":surface.geode_pull,
		"surface":surface.progress_snapshot(),"actor_position":[motion_world.player_actor.position.x,motion_world.player_actor.position.y],
		"phase_index":motion_world.phase_index,"authored_state":(surface as StudySurface).authored_state_index(),"direct_review":false,"scores":{},"owner_acceptance":null})

func _capture(world: OperaCareerWorld2D, state_name: String) -> void:
	var surface := world.surface as OperaGeologySurface
	records.append({"phase_index":world.phase_index,"state":state_name,"motion_frame_index":motion_frames.size(),
		"surface":surface.progress_snapshot(),"qualification":"No capture freeze; timeline marker only."})

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
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	main.save_data["opera_geology_checkpoint"] = {}
	var config: Dictionary = {}
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume","")) == "geologist":
			config = act.duplicate(true)
	assert(not config.is_empty())
	var competition := OperaCompetition.new()
	competition.configure("geologist")
	var world := OperaCareerWorld2D.new()
	main.add_child(world)
	world.setup(main,config,competition,Callable())
	var old_surface := world.surface
	var study := StudySurface.new()
	study.name = "CoherentGeodeNonRuntimePilot"
	study.position = old_surface.position
	study.size = old_surface.size
	study.mouse_filter = old_surface.mouse_filter
	study.bop_texture = old_surface.bop_texture
	study.bop_captain_texture = old_surface.bop_captain_texture
	study.gesture.connect(Callable(world,"_on_gesture"))
	study.progress_changed.connect(Callable(world,"_on_geology_progress_changed"))
	var child_index := old_surface.get_index()
	world.action_panel.remove_child(old_surface)
	old_surface.queue_free()
	world.action_panel.add_child(study)
	world.action_panel.move_child(study,child_index)
	world.surface = study
	world._arm_phase()

	await _wait(20)
	assert(world.phase_index == 0 and world.phases.size() == 4)
	for phase: int in range(4):
		assert(world.phase_index == phase)
		await _open(world)
		await _work(world)
		if phase < 3:
			for tick: int in range(240):
				if world.phase_index == phase + 1:
					break
				await _wait(1)
			assert(world.phase_index == phase + 1)
			events.append({"event":"ordinary_advance_after_hold","phase_index":world.phase_index})
	await _wait(60)
	record_motion = false
	var checkpoint: Dictionary = main.save_data.get("opera_geology_checkpoint",{}) as Dictionary
	var file := FileAccess.open(OUT + "CAPTURE_%d.json" % width_now,FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"ORDINARY_FOUR_PHASE_NATIVE_ROUTE_CAPTURED_REVIEW_PENDING",
		"views":records,"events":events,"motion_frames":motion_frames,"final_checkpoint":checkpoint,
		"qualification":"Main entry and scripted touch intervals are a fixture. Actual production renderer and normal four-phase advancement; no capture freezes or restore interruption; non-runtime inherited surface subclass and initial phase0 rebind supply seven source paintings. Every rendered geode opening/earned completion frame preserved. Not physical device/child/owner/castle/training/story or human touch pacing evidence."},"\t"))
	file.close()
	print("GEODE_RUNTIME_ROUTE|ALL4_INTENTIONAL_PHASES|",width_now,"|",records.size(),"|PASS_CAPTURE_REVIEW_PENDING")
	quit(0)
