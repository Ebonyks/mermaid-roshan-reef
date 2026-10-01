extends SceneTree
## Native timed diagnostic: selected fixture phase, then real viewport touch
## events and unmodified production processing. No progress/acting setters.

const OUT := "res://audit/day2_action_continuity_20261001/"
const CANDIDATE := "res://assets_src/imagegen/day2_refinement_20261001/selected/D2A-0446.png"
var main: ReefMain
var receipts: Array[Dictionary] = []
var input_log: Array[Dictionary] = []
var shots: Array[Dictionary] = []
var current_id := ""
var world: OperaCareerWorld2D

func _init() -> void:
	call_deferred("_run")

func frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame

func event(at: Vector2, kind: String, time: float) -> void:
	var input: InputEvent
	if kind == "drag":
		var drag := InputEventScreenDrag.new()
		drag.index = 0
		drag.position = at
		input = drag
	else:
		var touch := InputEventScreenTouch.new()
		touch.index = 0
		touch.position = at
		touch.pressed = kind == "down"
		input = touch
	root.push_input(input, true)
	input_log.append({"t": time, "kind": kind, "finger": 0,
		"viewport_xy": [at.x, at.y], "phase": world.phase_index,
		"progress_after_dispatch": world.phase_progress})

func shot(frame: int, time: float) -> void:
	await RenderingServer.frame_post_draw
	var path := OUT + "captures/" + current_id + "/%04d.webp" % frame
	var image: Image = root.get_texture().get_image()
	var result: Error = image.save_webp(path, false)
	var state := {"frame": frame, "t": time, "image": path.trim_prefix(OUT),
		"sha256": FileAccess.get_sha256(path), "save_error": result,
		"snapshot": world.scene_snapshot(),
		"surface": {"mode": world.surface.mode, "fill": world.surface.widget_fill,
			"crank_rotation": world.surface.crank_rotation,
			"pour_tilt": world.surface.pour_tilt, "pour_level": world.surface.pour_level,
			"pour_reserve": world.surface.pour_reserve,
			"completion_accepted": world.surface.completion_accepted},
		"strawberry_mask": main.chapter2_strawberry_mask}
	if world.nursery_catch != null:
		var catch: OperaNurseryCatch = world.nursery_catch
		state["nursery"] = {"caught": catch.caught, "missed": catch.missed,
			"catcher_x": catch.catcher_x, "fallers": catch.fallers.duplicate(true),
			"safe_landings": catch.safe_landings.duplicate(true), "settled": catch.settled.duplicate()}
	shots.append(state)

func _config(career: String) -> Dictionary:
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume", "")) == career:
			return act.duplicate(true)
	return {}

func _case(career: String, phase: int, recipe: String,
		duration: float, candidate: bool = false) -> void:
	main.clear_dialogue()
	input_log.clear()
	shots.clear()
	current_id = "%s-p%02d-%s%s-%dx%d" % [career, phase, recipe,
		"-candidate" if candidate else "-baseline", root.size.x, root.size.y]
	DirAccess.make_dir_recursive_absolute(OUT + "captures/" + current_id)
	var config := _config(career)
	if recipe == "berries":
		main.chapter2_active = true
		main.chapter2_active_objective = ChapterTwoDirector.OBJECTIVE_PARTY_PREP
		main.chapter2_skill_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
		main.chapter2_strawberry_mask = 0
		config["reward_policy"] = "chapter2_story"
		config["run_context"] = {"chapter": "chapter2"}
		config["phase_overrides"] = ChapterTwoCareerSceneAdapter.phase_set(career)["phases"]
		config["scene_adapter"] = ChapterTwoCareerSceneAdapter.adapter_config(career)
	var competition := OperaCompetition.new()
	competition.configure(career)
	world = OperaCareerWorld2D.new()
	main.add_child(world)
	world.setup(main, config, competition, Callable())
	if world.root == null or world.phases.is_empty():
		push_error("ACTIONTRACE: world setup failed for " + current_id)
		quit(2)
		return
	world.set_process(false)
	world.phase_index = phase
	world.active = true
	world.reveal_t = 0.0
	world.phase_advance_pending = false
	world.phase_gap = 0.0
	world._arm_phase()
	world._open_task()
	await frames(4)
	if candidate and world.nursery_catch != null:
		var native := Image.load_from_file(CANDIDATE)
		world.nursery_catch.cradle_texture = ImageTexture.create_from_image(native)
	world.set_process(true)
	var surface: OperaGestureSurface = world.surface
	var recipe_phase := (world.phases[phase] as Dictionary).duplicate(true)
	var down := false
	var last_at := Vector2.ZERO
	var image_index := 0
	var total_steps := int(duration * 30.0)
	for step: int in range(total_steps):
		var time := float(step) / 30.0
		var local := surface.size * 0.5
		var at := surface.get_global_transform_with_canvas() * local
		if time >= 0.5 and world.phase_index == phase and not world.phase_advance_pending:
			if recipe == "circle":
				local = surface._circle_pivot() + Vector2.from_angle(time * TAU / 2.0) \
					* minf(surface.size.x, surface.size.y) * 0.26
				at = surface.get_global_transform_with_canvas() * local
			elif recipe == "pour":
				local = surface._pour_pitcher_rect().get_center()
				at = surface.get_global_transform_with_canvas() * local
			elif recipe == "berries":
				var pick := int((time - 0.5) / 0.8)
				var slice := (step - 15) % 24
				if pick < world.chapter2_strawberry_pickups.size() and slice in [0, 2]:
					at = world.chapter2_strawberry_pickups[pick].get_global_rect().get_center()
					event(at, "down" if slice == 0 else "up", time)
			elif recipe == "catch" and world.nursery_catch != null:
				var catch: OperaNurseryCatch = world.nursery_catch
				var x := catch.lowest_baby_x()
				local = Vector2(maxf(0.1, x) * catch.size.x, catch.size.y * 0.8)
				at = catch.get_global_transform_with_canvas() * local
			if recipe != "berries":
				event(at, "drag" if down else "down", time)
				down = true
				last_at = at
		elif down:
			event(last_at, "up", time)
			down = false
		await process_frame
		if step % 4 == 0:
			await shot(image_index, time)
			image_index += 1
	if down:
		event(last_at, "up", duration)
	var receipt := {"id": current_id, "recipe": recipe, "initial_phase": recipe_phase,
		"method": "Direct phase/open fixture followed by genuine finger0 viewport push_input; unmodified world/surface process at fixed30fps. No gesture signals or progress setters after opening.",
		"candidate": candidate, "candidate_path": CANDIDATE.trim_prefix("res://") if candidate else "",
		"candidate_sha256": FileAccess.get_sha256(CANDIDATE) if candidate else "",
		"capture_fps": 7.5, "dimensions": [root.size.x, root.size.y],
		"events": input_log.duplicate(true), "frames": shots.duplicate(true),
		"acceptance": "TIMED_DIAGNOSTIC_ONLY; normal room launch, continuous60fps contact, device/child/owner acceptance pending"}
	var file := FileAccess.open(OUT + current_id + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t"))
	file.close()
	receipts.append({"id": current_id, "receipt": current_id + ".json",
		"frames": shots.size(), "inputs": input_log.size()})
	print("ACTIONTRACE|", current_id, "|frames=", shots.size(), "|inputs=", input_log.size())
	world.close()
	world.queue_free()
	await frames(3)

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, "res://tmp/day2_action_capture_save.json")
	root.add_child(main)
	await frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.set_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(root.size)
	await frames(5)
	await _case("chef", 0, "pour", 9.0)
	await _case("chef", 1, "circle", 7.0)
	await _case("candymaker", 2, "circle", 7.0)
	await _case("doctor", 3, "circle", 7.0)
	await _case("farmer", 0, "berries", 5.0)
	await _case("nursery", 1, "catch", 15.0)
	await _case("nursery", 1, "catch", 15.0, true)
	var file := FileAccess.open(OUT + "capture_index.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info(),
		"renderer": RenderingServer.get_current_rendering_method(),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_action_continuity.gd"),
		"receipts": receipts, "owner_accepted": false}, "\t"))
	file.close()
	main.queue_free()
	await frames(2)
	quit()
