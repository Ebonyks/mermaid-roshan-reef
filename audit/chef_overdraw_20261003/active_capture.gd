extends SceneTree
const MAIN_SCENE := preload("res://scenes/main.tscn")
const WORLD_SCRIPT := preload("res://scripts/opera_career_world_2d.gd")
var main: ReefMain
var failures := 0
func check(label: String, ok: bool) -> void:
	print("CHEF_ACTIVE|", "PASS" if ok else "FAIL", "|", label)
	if not ok:
		failures += 1
func _init() -> void:
	call_deferred("_run")
func touch(surface: OperaGestureSurface, at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.position = at
	event.index = 0
	event.pressed = pressed
	surface._gui_input(event)
func drag(surface: OperaGestureSurface, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.position = at
	event.index = 0
	surface._gui_input(event)
func capture(out: String, label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var path := out.path_join(label + ".png")
	var result := get_root().get_texture().get_image().save_png(path)
	print("CHEF_ACTIVE_CAPTURE|", path, "|", result)
func _run() -> void:
	main = MAIN_SCENE.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	if main.start_menu_layer != null:
		main.start_menu_layer.visible = false
	main.start_menu_active = false
	main.clear_dialogue()
	main.hud_msg.visible = false
	main.chapter2_active = true
	main.chapter2_strawberry_mask = 0x1F
	main.set_process(false)
	var width := int(OS.get_environment("CHEF_CAPTURE_WIDTH"))
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_size(Vector2i(width, 720))
	await process_frame
	var out := OS.get_environment("CHEF_CAPTURE_OUT")
	DirAccess.make_dir_recursive_absolute(out)
	for phase in range(5):
		main.chapter2_cake_piece_mask = [0, 1, 3, 7, 15][phase]
		var competition := OperaCompetition.new()
		competition.configure("chef")
		var world := WORLD_SCRIPT.new() as OperaCareerWorld2D
		main.add_child(world)
		world.setup(main, {"costume": "chef", "chapter": "chapter2",
			"phase_overrides": ChapterTwoCareerSceneAdapter.phase_set("chef").get("phases", []),
			"finale_start": 5, "chapter2_resume_phase_index": phase}, competition,
			Callable(), [], ChapterTwoCareerSceneAdapter.adapter_config("chef"),
			{"chapter": "chapter2"})
		await process_frame
		world.set_process(false)
		world.reveal_t = 0.0
		world.phase_gap = 0.0
		var station_index := int(world.station_for_phase.get(phase, -1))
		check("phase %d has a physical station" % phase, station_index >= 0)
		var feet: Vector2 = world.station_list[station_index].get("approach_pos", Vector2.ZERO)
		world.wander_feet = feet
		world._place_on_stage(world.player_actor, feet)
		world._open_task()
		await create_timer(0.36).timeout
		world.reveal_t = 0.0
		var surface := world.surface as OperaChefSurface
		check("phase %d uses one native kitchen surface" % phase, surface != null)
		check("phase %d suppresses the duplicate persistent prop" % phase, not world.chapter2_cake_scene.visible)
		check("phase %d has no broad activity alpha lens" % phase, world.action_panel.scale == Vector2.ONE)
		for frame in range(8):
			await process_frame
		world.player_animator.set_process(false)
		surface.set_process(false)
		world.backdrop_node.set_process(false)
		var initial := world.phase_progress
		for frame in range(30):
			surface._process(1.0 / 30.0)
		check("phase %d passive demo earns no progress" % phase, is_equal_approx(initial, world.phase_progress))
		if phase == 0:
			check("empty bowl is a native transparent asset", surface._art(surface.EMPTY_BOWL) != null)
			touch(surface, surface._pour_pitcher_rect().get_center(), true)
			for frame in range(60):
				surface._pour_tick(1.0 / 30.0)
			check("pour turns toward the measured left lip", surface._pour_pitcher_rotation() < 0.0)
			check("pour stream stays on its visible bowl", surface._pour_bowl_rect().has_point(surface._pour_landing_point()))
		elif phase == 1:
			var center := surface._circle_pivot()
			touch(surface, center + Vector2(42, 0), true)
			for sample in range(37):
				drag(surface, center + Vector2.from_angle(float(sample) * TAU / 36.0) * 42.0)
		elif phase == 2:
			surface.oven_t = 0.62
		elif phase == 3:
			var at := surface._target_anchor_point(0) - Vector2(0, 17)
			touch(surface, at, true)
			touch(surface, at, false)
			touch(surface, at, true)
			touch(surface, at, false)
			check("repeated rack tap cannot duplicate a moved tier pair", world.phase_progress == 1.0)
		elif phase == 4:
			touch(surface, surface._trace_demo_point(0), true)
			for sample in range(1, 17):
				drag(surface, surface._trace_demo_point(float(sample) / 32.0))
			check("one half trace earns one half of the phase", absf(world.phase_progress - 3.0) < 0.001)
		await capture(out, "phase_%d_work" % phase)
		if phase == 0:
			for frame in range(600):
				surface._pour_tick(1.0 / 30.0)
				if world.phase_advance_pending:
					break
			touch(surface, surface._pour_pitcher_rect().get_center(), false)
		elif phase == 1:
			for sample in range(1, 39):
				drag(surface, surface._circle_pivot() + Vector2.from_angle(float(sample) * TAU / 36.0) * 42.0)
				if world.phase_advance_pending:
					break
		elif phase == 2:
			touch(surface, surface._oven_handle_rect().get_center(), true)
			touch(surface, surface._oven_handle_rect().get_center(), false)
		elif phase == 3:
			for index in range(1, 3):
				var at := surface._target_anchor_point(index) - Vector2(0, 17)
				touch(surface, at, true)
				touch(surface, at, false)
				if index == 1:
					await capture(out, "phase_3_two_pairs")
		elif phase == 4:
			for sample in range(17, 33):
				drag(surface, surface._trace_demo_point(float(sample) / 32.0))
			touch(surface, surface._trace_demo_point(1), false)
		check("phase %d real gesture reaches the exact world endpoint" % phase, world.phase_advance_pending)
		await capture(out, "phase_%d_done" % phase)
		world.free()
		await process_frame
	main.free()
	print("CHEF_ACTIVE|RESULT|", "ALL OK" if failures == 0 else "%d FAILURES" % failures)
	quit(0 if failures == 0 else 1)
