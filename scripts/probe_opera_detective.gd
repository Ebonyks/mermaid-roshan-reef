extends SceneTree
## Focused runtime contract for Detective's diegetic painted-room search.
##
## The broad Opera probe exercises every career. This one stays deliberately
## small so lens geometry, true magnification, safe prop reactions and the
## delayed glint can be checked locally without waiting on twelve other jobs.

var bad := 0
var main: ReefMain

const StagePaths := preload("res://scripts/opera_stage_paths.gd")


func _init() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.game = "opera"
	var config := (OperaHouse.ACTS[1] as Dictionary).duplicate(true)
	var act := OperaAct.new()
	get_root().add_child(act)
	act.start(main, config, Callable())
	await process_frame
	var world := act.career_world_2d
	_check("detective begins in the navigable painted room",
		act.use_career_world_2d and world != null
		and not world.task_open and not world.action_panel.visible
		and not world.lens_layer.visible and not world.lens_zoom_surface.visible)
	var hotspot := world._active_hotspot()
	var starts_at_magnifier := hotspot != null \
		and hotspot.station_id == "magnifier_tower" \
		and hotspot.presentation == "painted" \
		and hotspot.touch_button != null and not hotspot.touch_button.disabled
	_check("painted magnifier tower invites the first search", starts_at_magnifier)
	var route_safe := starts_at_magnifier
	if hotspot != null and hotspot.touch_button != null:
		hotspot.touch_button.pressed.emit()
		route_safe = route_safe and world.wander_walking \
			and StagePaths.route_is_approved("detective", world.wander_route, 2.0)
		var route_ticks := 0
		while not world.task_open and route_ticks < 320:
			world._process(0.05)
			hotspot._process(0.05)
			route_safe = route_safe and StagePaths.point_is_on_approved_route(
				"detective", world.wander_feet, 3.0)
			route_ticks += 1
	_check("Roshan follows the authored route before search opens",
		route_safe and world.task_open and hotspot != null
		and hotspot.activation_count == 1)
	_check("arrival opens the painted search and optical glass",
		world.task_open and world.lens_layer.visible
		and world.lens_zoom_surface.visible)
	_check("missing-crown setup begins on arrival as a two-voice story",
		world.detective_intro_played and main.dialogue_active
		and OperaCareerWorld2D.DETECTIVE_INTRO_LINES.size() == 2
		and String(OperaCareerWorld2D.DETECTIVE_INTRO_LINES[0].get("vo", ""))
			== "op_detective_steal"
		and String(OperaCareerWorld2D.DETECTIVE_INTRO_LINES[1].get("vo", ""))
			== "op_detective_search")
	_check("detective story and guidance recordings are installed",
		ResourceLoader.exists("res://assets/audio/voices/imp_op_detective_steal.ogg")
		and ResourceLoader.exists("res://assets/audio/voices/roshan_op_detective_search.ogg")
		and ResourceLoader.exists("res://assets/audio/voices/roshan_op_detective_work.ogg")
		and ResourceLoader.exists("res://assets/audio/voices/roshan_op_detective_peek.ogg")
		and ResourceLoader.exists("res://assets/audio/voices/roshan_op_detective_match.ogg")
		and ResourceLoader.exists("res://assets/audio/voices/roshan_op_detective_name.ogg"))
	var crown_voice_ok := false
	for detective_phase: Dictionary in world.phases:
		if String(detective_phase.get("name", "")) == "CROWN":
			crown_voice_ok = String(detective_phase.get("vo", "")) \
				== "op_detective_name"
	_check("crown finale uses the recorded spotlight instruction",
		crown_voice_ok)
	_check("magnifier art and optical glass are child-readable",
		OperaCareerWorld2D.LENS_GRAPHIC_SIZE.x >= 400.0
		and OperaCareerWorld2D.LENS_RADIUS >= 125.0
		and world.lens_zoom_surface.size.x >= 250.0)
	_check("glass performs true screen-space magnification",
		world.lens_zoom_material != null
		and float(world.lens_zoom_material.get_shader_parameter("magnification")) >= 1.7
		and world.lens_zoom_material.shader.code.contains("hint_screen_texture"))
	_check("painted room has many optional inspection targets",
		world.lens_room_objects.size() >= 16)
	var every_clue_reachable := not world.lens_clues.is_empty()
	for clue: Vector2 in world.lens_clues:
		every_clue_reachable = every_clue_reachable \
			and world._clamped_lens_position(clue).distance_to(clue) \
			<= OperaCareerWorld2D.LENS_CLUE_CAPTURE_RADIUS
	_check("edge clamping leaves every required clue reachable",
		every_clue_reachable)
	var progress_before := world.phase_progress
	var reactions_before := world.lens_room_reactions
	var prop_reacts_safely := false
	if not world.lens_room_objects.is_empty():
		var first_object: Dictionary = world.lens_room_objects[0]
		prop_reacts_safely = world._try_lens_room_object(
			first_object.get("pos", Vector2.ZERO)) \
			and world.lens_room_reactions == reactions_before + 1 \
			and is_equal_approx(world.phase_progress, progress_before)
	_check("an ordinary prop responds without changing case progress",
		prop_reacts_safely)
	world.lens_demo = false
	world.lens_since_find = OperaCareerWorld2D.LENS_HINT_DELAY - 0.05
	world._tick_lens(0.10)
	_check("a remaining clue glistens after twelve seconds without a find",
		world.lens_hint_target >= 0
		and not world.lens_found[world.lens_hint_target])
	var first_clue := world._next_unfound_lens_clue()
	var expected_next := world.lens_clues[first_clue + 1] \
		if first_clue >= 0 and first_clue + 1 < world.lens_clues.size() \
		else Vector2.ZERO
	if first_clue >= 0:
		world._set_lens_position(world.lens_clues[first_clue])
		world._tick_lens(0.01)
		world._tick_lens(0.46)
	_check("finding a clue launches a visible trail toward the next case step",
		first_clue >= 0 and world.lens_find_count == 1
		and world.lens_trail_t > 0.0
		and world.lens_trail_from == world.lens_clues[first_clue]
		and (expected_next == Vector2.ZERO
			or world.lens_trail_to == expected_next))
	var capture_path := OS.get_environment("OPERA_DETECTIVE_SHOT_OUT").strip_edges()
	if not capture_path.is_empty():
		DirAccess.make_dir_recursive_absolute(capture_path)
		world._set_lens_position(Vector2(518.0, 248.0))
		await process_frame
		await process_frame
		await RenderingServer.frame_post_draw
		var image: Image = get_root().get_viewport().get_texture().get_image()
		var error := image.save_png(capture_path.path_join("detective_search_zoom_and_hint.png"))
		_check("saved detective search review frame", error == OK)
	act.cancel()
	await process_frame
	if bad == 0:
		print("OPERA_DETECTIVE|result: ALL OK")
		quit()
	else:
		print("OPERA_DETECTIVE|result: %d FAIL" % bad)
		quit(1)


func _check(label: String, condition: bool) -> void:
	if condition:
		print("OPERA_DETECTIVE|OK|", label)
	else:
		bad += 1
		print("OPERA_DETECTIVE|FAIL|", label)
