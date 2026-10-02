extends SceneTree
## Phase-selected disposable fixtures followed by actual viewport approach/input.
## Source candidates only; original runtime files and persisted rewards unchanged.
const OUT := "res://tmp/vector_mount_v86/native_views/"
const CANDIDATES := {
	"res://assets/opera/worlds/hotspots/geologist_fossil.svg": "res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/geologist_fossil_v2.svg",
	"res://assets/opera/worlds/hotspots/geologist_layered_rock.svg": "res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/geologist_layered_rock_v2.svg",
	"res://assets/opera/worlds/hotspots/teacher_lesson_board.svg": "res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/teacher_lesson_board_v2.svg",
	"res://assets/opera/worlds/props/goal_geologist.svg": "res://assets_src/vector/job_geology_teacher_refinement_v1_20261001/goal_geologist_v1.svg",
}
var main: ReefMain
var records: Array[Dictionary] = []
var width_now := 1280
var phase_now := ""
var original_textures: Dictionary = {}
var candidate_textures: Dictionary = {}

func _initialize() -> void:
	_run.call_deferred()

func _wait(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.pressed = pressed
	event.position = at
	Input.parse_input_event(event)

func _drag(at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = at
	Input.parse_input_event(event)

func _surface_touch(surface: Control, at: Vector2, pressed: bool) -> void:
	_touch(surface.get_global_transform_with_canvas() * at, pressed)
	await _wait(2)

func _surface_drag(surface: Control, start: Vector2, end: Vector2) -> void:
	for step: int in range(1, 11):
		_drag(surface.get_global_transform_with_canvas() * start.lerp(end, float(step) / 10.0))
		await _wait(2)

func _freeze(node: Node, states: Dictionary) -> void:
	states[node] = [node.is_processing(), node.is_physics_processing()]
	node.set_process(false)
	node.set_physics_process(false)
	for child: Node in node.get_children():
		_freeze(child, states)

func _thaw(states: Dictionary) -> void:
	for raw_node: Variant in states:
		var node := raw_node as Node
		var state := states[raw_node] as Array
		node.set_process(bool(state[0]))
		node.set_physics_process(bool(state[1]))

func _use_candidates(world: OperaCareerWorld2D, use_new: bool) -> void:
	var family := candidate_textures if use_new else original_textures
	for raw_hotspot: Control in world.station_nodes:
		var hotspot := raw_hotspot as OperaWorldHotspot2D
		if family.has(hotspot.source_path):
			hotspot.object_texture = family[hotspot.source_path] as Texture2D
			hotspot.queue_redraw()
	if world.prop_rect != null:
		var goal_path := "res://assets/opera/worlds/hotspots/teacher_lesson_board.svg" \
			if world.career_id == "teacher" else "res://assets/opera/worlds/props/goal_geologist.svg"
		world.prop_rect.texture = family[goal_path] as Texture2D
	if world.surface is OperaGeologySurface:
		var surface := world.surface as OperaGeologySurface
		surface.fossil_texture = family["res://assets/opera/worlds/hotspots/geologist_fossil.svg"] as Texture2D
		surface.rock_texture = family["res://assets/opera/worlds/hotspots/geologist_layered_rock.svg"] as Texture2D
		surface.crystals_texture = family["res://assets/opera/worlds/props/goal_geologist.svg"] as Texture2D
		surface.queue_redraw()

func _capture_pair(world: OperaCareerWorld2D, state_name: String) -> void:
	var states: Dictionary = {}
	_freeze(world, states)
	var before := _snapshot(world)
	for use_new: bool in [false, true]:
		_use_candidates(world, use_new)
		await _wait(2)
		await RenderingServer.frame_post_draw
		var pixels: Image = root.get_texture().get_image()
		var ident := "%s_%d_%s_%s_%s" % [world.career_id, width_now, phase_now.to_lower(),
			state_name, "candidate" if use_new else "original"]
		var path := OUT + ident + ".webp"
		assert(pixels.save_webp(path, true) == OK)
		var hot := world._active_hotspot()
		records.append({"id": ident, "path": ident + ".webp", "sha256": FileAccess.get_sha256(path),
			"viewport": [pixels.get_width(), pixels.get_height()], "career": world.career_id,
			"phase": phase_now, "phase_index": world.phase_index, "state": state_name,
			"variant": "candidate" if use_new else "original", "task_open": world.task_open,
			"phase_progress": world.phase_progress, "surface_progress": before,
			"hotspot_source": hot.source_path if hot != null else "",
			"hotspot_visible": hot.visible if hot != null else false,
			"hotspot_size": [hot.object_size.x, hot.object_size.y] if hot != null else [],
			"goal_visible": world.prop_rect.visible if world.prop_rect != null else false,
			"fixture": "Phase selected via existing _arm_phase, then actual viewport invitation approach. Candidate texture injection into existing owners only; complete job/training-to-story sequence not represented."})
	_use_candidates(world, false)
	assert(before == _snapshot(world))
	_thaw(states)

func _snapshot(world: OperaCareerWorld2D) -> Dictionary:
	if world.surface is OperaGeologySurface:
		return (world.surface as OperaGeologySurface).progress_snapshot()
	if world.surface is OperaTeacherSurface:
		return (world.surface as OperaTeacherSurface).progress_snapshot()
	return {}

func _partial_fossil(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as OperaGeologySurface
	var cell := Vector2(70.0, 60.0)
	var start := OperaGeologySurface.FOSSIL_RECT.position + cell * 0.5
	var end := start + Vector2(7.0 * cell.x, 0.0)
	await _surface_touch(surface, start, true)
	await _surface_drag(surface, start, end)
	assert(surface.fossil_stage == 0 and surface._cleared_count() > 0)
	await _capture_pair(world, "partial_brush_contact")
	var current := end
	for row: int in range(1, 5):
		var next := OperaGeologySurface.FOSSIL_RECT.position \
			+ (Vector2(0 if row % 2 == 1 else 7, row) + Vector2(0.5, 0.5)) * cell
		await _surface_drag(surface, current, next)
		current = next
		if surface.fossil_stage == 1:
			break
	await _surface_touch(surface, current, false)
	assert(surface.fossil_stage == 1 and surface._snapped_count() == 0)
	await _capture_pair(world, "natural_assembly_ready")
	assert(not surface._completion_emitted)

func _partial_geode(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as OperaGeologySurface
	for seam: int in range(5):
		var at := surface.geode_seam_spot(seam)
		await _surface_touch(surface, at, true)
		await _surface_touch(surface, at, false)
	assert(surface._seam_count() == 5)
	var start := surface.geode_half_center()
	await _surface_touch(surface, start, true)
	await _surface_drag(surface, start, start + Vector2(65.0, 0.0))
	await _surface_touch(surface, start + Vector2(65.0, 0.0), false)
	assert(surface.geode_pull > 0.0 and surface.geode_pull < 120.0)
	await _capture_pair(world, "partial_open_crystal_contact")
	assert(not surface._completion_emitted)

func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	for source: String in CANDIDATES:
		original_textures[source] = load(source) as Texture2D
		var image := Image.load_from_file(String(CANDIDATES[source]))
		assert(image != null and not image.is_empty())
		candidate_textures[source] = ImageTexture.create_from_image(image)
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
	var stars := main.opera_stars
	var save_before := JSON.stringify(main.save_data)
	for width: int in [1280, 1600]:
		width_now = width
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		await _wait(4)
		for career: String in ["teacher", "geologist"]:
			var config: Dictionary = {}
			for act: Dictionary in OperaHouse.ACTS:
				if String(act.get("costume", "")) == career:
					config = act.duplicate(true)
			assert(not config.is_empty())
			config["reward_policy"] = "dev_playtest"
			var names: Array[String] = ["PATTERN", "COUNT", "ADD", "MATCH"] \
				if career == "teacher" else ["RIVER", "FOSSIL", "PAN", "GEODE"]
			for phase_name: String in names:
				phase_now = phase_name
				var competition := OperaCompetition.new()
				competition.configure(career)
				var world := OperaCareerWorld2D.new()
				main.add_child(world)
				world.setup(main, config.duplicate(true), competition, Callable(), [], {}, {})
				var chosen := -1
				for index: int in range(world.phases.size()):
					if String((world.phases[index] as Dictionary).get("name", "")) == phase_name:
						chosen = index
						break
				assert(chosen >= 0)
				world.phase_index = chosen
				world._arm_phase()
				await _wait(20)
				await _capture_pair(world, "invitation")
				var hot := world._active_hotspot()
				assert(hot != null and hot.visible)
				var at: Vector2 = hot.touch_button.get_global_transform_with_canvas() * (hot.touch_button.size * 0.5)
				_touch(at, true)
				await _wait(1)
				_touch(at, false)
				for tick: int in range(300):
					if world.task_open:
						break
					await _wait(1)
				assert(world.task_open)
				await _wait(12)
				await _capture_pair(world, "opened_task")
				if phase_name == "FOSSIL":
					await _partial_fossil(world)
				if phase_name == "GEODE":
					await _partial_geode(world)
				assert(main.opera_stars == stars and JSON.stringify(main.save_data) == save_before)
				world.queue_free()
				await _wait(4)
				print("VECTOR_MOUNT|", career, "|", width, "|", phase_name, "|CAPTURED")
	assert(records.size() == 76)
	var file := FileAccess.open(OUT + "CAPTURE_RECEIPT.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"status": "76_NATIVE_PHASE_FIXTURE_COMPARISONS_CAPTURED", "views": records,
		"original_rewards_and_save_dictionary_unchanged": true,
		"qualification": "Individually selected phases followed by real viewport approach and partial fossil/geode touch input. Current and temporary candidate textures paired at same state. No completed career, uninterrupted training/story route, cinematic, device, child or owner acceptance."}, "\t"))
	file.close()
	print("VECTOR_MOUNT|76_CAPTURED|NO_AWARD_OR_SAVE_CHANGE|REVIEW_PENDING")
	quit(0)
