extends SceneTree
## Phase-selected disposable fixtures followed by actual viewport approach/input.
## Source candidates only; original runtime files and persisted rewards unchanged.
const OUT := "res://tmp/geode_embedded_mount_v99/native_views/"
const StudySurface := preload("res://audit/job_geode_opening_states_v3_20261001/study_surface.gd")
const CANDIDATES := {
 "res://assets/opera/worlds/hotspots/geologist_fossil.svg": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/fossil/attempt_02/whole_canvas_1024.png",
 "res://assets/opera/worlds/hotspots/geologist_layered_rock.svg": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/layered_rock/attempt_01/whole_canvas_1024.png",
 "res://assets/opera/worlds/props/goal_geologist.svg": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/crystal_reward/attempt_01/whole_canvas_1024.png"
}
const PAINTED_PATHS := {
 "fossil": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/fossil/attempt_02/whole_canvas_1024.png",
 "layered_rock": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/layered_rock/attempt_01/whole_canvas_1024.png",
 "washing_pan": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/washing_pan/attempt_01/whole_canvas_1024.png",
 "closed_geode": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/closed_geode/attempt_01/whole_canvas_1024.png",
 "crystal_reward": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/crystal_reward/attempt_01/whole_canvas_1024.png",
 "open_geode": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/open_geode/attempt_02/whole_canvas_1024.png",
 "work_surface": "res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/work_surface/attempt_04/whole_canvas_1024.png"
}
const SOURCE_BOXES := {
 "fossil": [
  115,
  171,
  917,
  845
 ],
 "layered_rock": [
  120,
  188,
  920,
  862
 ],
 "washing_pan": [
  44,
  233,
  981,
  822
 ],
 "closed_geode": [
  192,
  213,
  837,
  815
 ],
 "crystal_reward": [
  231,
  130,
  800,
  897
 ],
 "open_geode": [
  104,
  214,
  921,
  814
 ],
 "work_surface": [
  68,
  332,
  957,
  701
 ]
}
var main: ReefMain
var records: Array[Dictionary] = []
var width_now := 1280
var phase_now := ""
var original_textures: Dictionary = {}
var candidate_textures: Dictionary = {}
var painted_textures: Dictionary = {}
var study_background: TextureRect
var original_presentations: Dictionary = {}

func _opening_texture(path: String, region: Rect2) -> AtlasTexture:
	var texture := ImageTexture.create_from_image(Image.load_from_file(path))
	var atlas := AtlasTexture.new()
	atlas.atlas = texture
	atlas.region = region
	return atlas

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
		surface.pan_texture = painted_textures["washing_pan"] as Texture2D if use_new else null
		surface.queue_redraw()

func _capture_pair(world: OperaCareerWorld2D, state_name: String) -> void:
	var states: Dictionary = {}
	_freeze(world, states)
	var before := _snapshot(world)
	for lane: String in ["painted_staging"]:
		var use_new := lane != "original"
		_use_candidates(world, use_new)
		var study := world.surface as StudySurface
		study.painted_study = lane == "painted_staging"
		study_background.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
		study_background.position = Vector2.ZERO
		study_background.size = Vector2(1280, 720)
		study_background.visible = study.painted_study
		world.backdrop_node.visible = not study.painted_study
		if study.painted_study:
			study.fossil_texture = painted_textures["fossil"] as Texture2D
			study.rock_texture = painted_textures["layered_rock"] as Texture2D
			study.crystals_texture = painted_textures["crystal_reward"] as Texture2D
			study.geode_texture = painted_textures["closed_geode"] as Texture2D
			study.middle_open_texture = _opening_texture("res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/opening_geode/middle_open/attempt_01/whole_canvas_1024.png", Rect2(99, 70, 845, 569))
			study.early_crack_texture = _opening_texture("res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/opening_geode/early_crack/attempt_01/whole_canvas_1024.png", Rect2(77, 85, 870, 741))
			study.pan_texture = painted_textures["washing_pan"] as Texture2D
			var active := world._active_hotspot()
			var prop_key := "layered_rock"
			if phase_now == "FOSSIL":
				prop_key = "fossil"
			elif phase_now == "PAN":
				prop_key = "washing_pan"
			elif phase_now == "GEODE":
				prop_key = "closed_geode"
			active.object_texture = painted_textures[prop_key] as Texture2D
			active.presentation = "overlay"
			active.queue_redraw()
		study.queue_redraw()
		await _wait(2)
		await RenderingServer.frame_post_draw
		var pixels: Image = root.get_texture().get_image()
		var ident := "%s_%d_%s_%s_%s" % [world.career_id, width_now, phase_now.to_lower(),
			state_name, lane]
		var path := OUT + ident + ".webp"
		assert(pixels.save_webp(path, true) == OK)
		var hot := world._active_hotspot()
		records.append({"id": ident, "path": ident + ".webp", "sha256": FileAccess.get_sha256(path),
			"viewport": [pixels.get_width(), pixels.get_height()], "career": world.career_id,
			"phase": phase_now, "phase_index": world.phase_index, "state": state_name,
			"variant": lane, "task_open": world.task_open,
			"phase_progress": world.phase_progress, "surface_progress": before,
			"hotspot_source": hot.source_path if hot != null else "",
			"hotspot_visible": hot.visible if hot != null else false,
			"hotspot_size": [hot.object_size.x, hot.object_size.y] if hot != null else [],
			"goal_visible": world.prop_rect.visible if world.prop_rect != null else false,
			"geode_pull": study.geode_pull,
			"authored_opening_state": "closed" if study.geode_pull <= 0.0 else "early_crack" if study.geode_pull < 40.0 else "middle_open" if study.geode_pull < 90.0 else "fully_open",
			"fixture": "Phase-selected four-authored-state static opening review using actual inherited seam taps and25/40/55px pull segments with current source, literal raster injection and explicit painted drawing/layout study. Painted staging uses undersize room as REFERENCE_ONLY, not runtime art; no complete career/story/device/child/owner pass."})
	_use_candidates(world, false)
	(world.surface as StudySurface).painted_study = false
	study_background.visible = false
	world.backdrop_node.visible = true
	for raw_hot: Control in world.station_nodes:
		var reset_hot := raw_hot as OperaWorldHotspot2D
		reset_hot.presentation = String(original_presentations[reset_hot])
		reset_hot.queue_redraw()
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
	await _surface_drag(surface, start, start + Vector2(25.0, 0.0))
	await _surface_touch(surface, start + Vector2(25.0, 0.0), false)
	assert(surface.geode_pull > 0.0 and surface.geode_pull < 40.0)
	await _capture_pair(world, "early_crack_rooted_glimpse")
	var midway := surface.geode_half_center()
	await _surface_touch(surface, midway, true)
	await _surface_drag(surface, midway, midway + Vector2(40.0, 0.0))
	await _surface_touch(surface, midway + Vector2(40.0, 0.0), false)
	assert(surface.geode_pull > 0.0 and surface.geode_pull < 120.0)
	await _capture_pair(world, "partial_open_crystal_contact")
	assert(not surface._completion_emitted)
	# Isolate only the completion callbacks for this disposable endpoint review.
	# Production input determines the end state; career award/save cannot run.
	surface.gesture.disconnect(Callable(world, "_on_gesture"))
	surface.progress_changed.disconnect(Callable(world, "_on_geology_progress_changed"))
	var continued := surface.geode_half_center()
	await _surface_touch(surface, continued, true)
	await _surface_drag(surface, continued, continued + Vector2(55.0, 0.0))
	await _surface_touch(surface, continued + Vector2(55.0, 0.0), false)
	assert(surface.geode_pull >= OperaGeologySurface.GEODE_PULL_DISTANCE)
	assert(surface._completion_emitted and world.task_open)
	await _capture_pair(world, "fully_open_embedded_interior")


func _partial_river(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as OperaGeologySurface
	var start := surface.river_path_point(0)
	await _surface_touch(surface, start, true)
	for index: int in range(1, 4):
		var next := surface.river_path_point(index)
		await _surface_drag(surface, start, next)
		start = next
	await _surface_touch(surface, start, false)
	assert(not surface._completion_emitted and not surface._river_connected())
	await _capture_pair(world, "partial_connected_river")

func _partial_pan(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as OperaGeologySurface
	var start := OperaGeologySurface.PAN_RECT.get_center()
	await _surface_touch(surface, start, true)
	for offset: float in [80.0, -80.0, 80.0, -80.0]:
		var next := OperaGeologySurface.PAN_RECT.get_center() + Vector2(offset, 0)
		await _surface_drag(surface, start, next)
		start = next
	await _surface_touch(surface, start, false)
	assert(surface.pan_reversals > 0 and surface.pan_reversals < 9)
	assert(not surface._completion_emitted)
	await _capture_pair(world, "partial_panning_reversals")

func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	for source: String in CANDIDATES:
		original_textures[source] = load(source) as Texture2D
		var image := Image.load_from_file(String(CANDIDATES[source]))
		assert(image != null and not image.is_empty())
		candidate_textures[source] = ImageTexture.create_from_image(image)
	for key: String in PAINTED_PATHS:
		var img := Image.load_from_file(String(PAINTED_PATHS[key]))
		var texture := ImageTexture.create_from_image(img)
		var b := SOURCE_BOXES[key] as Array
		var atlas := AtlasTexture.new()
		atlas.atlas = texture
		atlas.region = Rect2(float(b[0]), float(b[1]), float(b[2]) - float(b[0]), float(b[3]) - float(b[1]))
		painted_textures[key] = atlas
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
		for career: String in ["geologist"]:
			var config: Dictionary = {}
			for act: Dictionary in OperaHouse.ACTS:
				if String(act.get("costume", "")) == career:
					config = act.duplicate(true)
			assert(not config.is_empty())
			config["reward_policy"] = "dev_playtest"
			var names: Array[String] = []
			if career == "teacher":
				names.assign(["PATTERN", "COUNT", "ADD", "MATCH"])
			else:
				names.assign(["GEODE"])
			for phase_name: String in names:
				phase_now = phase_name
				var competition := OperaCompetition.new()
				competition.configure(career)
				var world := OperaCareerWorld2D.new()
				main.add_child(world)
				world.setup(main, config.duplicate(true), competition, Callable(), [], {}, {})
				var old_surface := world.surface
				var study := StudySurface.new()
				study.name = "PaintedGeologyDisposableSurface"
				study.position = old_surface.position
				study.size = old_surface.size
				study.mouse_filter = old_surface.mouse_filter
				study.bop_texture = old_surface.bop_texture
				study.bop_captain_texture = old_surface.bop_captain_texture
				study.gesture.connect(Callable(world, "_on_gesture"))
				study.progress_changed.connect(Callable(world, "_on_geology_progress_changed"))
				var child_index := old_surface.get_index()
				world.action_panel.remove_child(old_surface)
				old_surface.queue_free()
				world.action_panel.add_child(study)
				world.action_panel.move_child(study, child_index)
				world.surface = study
				study.work_texture = painted_textures["work_surface"] as Texture2D
				study.geode_texture = painted_textures["closed_geode"] as Texture2D
				var open_source := ImageTexture.create_from_image(Image.load_from_file(String(PAINTED_PATHS["open_geode"])))
				var left_half := AtlasTexture.new()
				left_half.atlas = open_source
				left_half.region = Rect2(53, 91, 448, 501)
				var right_half := AtlasTexture.new()
				right_half.atlas = open_source
				right_half.region = Rect2(524, 91, 448, 500)
				study.open_left_texture = left_half
				study.open_right_texture = right_half
				study_background = TextureRect.new()
				study_background.name = "UNDERSIZE_REFERENCE_ONLY_ROOM"
				study_background.texture = ImageTexture.create_from_image(Image.load_from_file("res://assets_src/imagegen/geologist_painted_rebuild_v1_20261001/grotto/attempt_01/native.png"))
				study_background.position = Vector2.ZERO
				study_background.size = Vector2(1280, 720)
				study_background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				study_background.stretch_mode = TextureRect.STRETCH_SCALE
				study_background.mouse_filter = Control.MOUSE_FILTER_IGNORE
				study_background.visible = false
				world.root.add_child(study_background)
				world.root.move_child(study_background, world.backdrop_node.get_index())
				original_presentations.clear()
				for raw_hot: Control in world.station_nodes:
					var hot_prop := raw_hot as OperaWorldHotspot2D
					original_presentations[hot_prop] = hot_prop.presentation
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
				if phase_name == "RIVER":
					await _partial_river(world)
				if phase_name == "PAN":
					await _partial_pan(world)
				if phase_name == "FOSSIL":
					await _partial_fossil(world)
				if phase_name == "GEODE":
					await _partial_geode(world)
				assert(main.opera_stars == stars and JSON.stringify(main.save_data) == save_before)
				world.queue_free()
				await _wait(4)
				print("EMBEDDED_GEODE_MOUNT|", career, "|", width, "|", phase_name, "|CAPTURED")
	assert(records.size() == 24)
	var file := FileAccess.open(OUT + "CAPTURE_RECEIPT.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"status": "24_NATIVE_EMBEDDED_GEODE_FIXTURE_COMPARISONS_CAPTURED", "views": records,
		"original_rewards_and_save_dictionary_unchanged": true,
		"qualification": "GEODE phase selected followed by actual viewport approach, five seam taps,65px partial pull and continuation to120px full surface opening. Only endpoint completion callbacks are disconnected in this disposable fixture so no career award/save can run. Three drawing lanes paired at identical inherited progress. No full career/training/story, cinematic, device, child or owner acceptance."}, "\t"))
	file.close()
	print("EMBEDDED_GEODE_MOUNT|24_CAPTURED|NO_AWARD_OR_SAVE_CHANGE|REVIEW_PENDING")
	quit(0)
