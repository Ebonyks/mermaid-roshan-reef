extends SceneTree
## Diagnostic artwork census. Direct phase selection is declared, never
## authoritative interaction, motion, device or owner acceptance.

const OUT := "res://audit/day2_job_contexts_2026-09-30/"
const ASPECTS: Array[Vector2i] = [Vector2i(1280, 720), Vector2i(1600, 720)]
var main: ReefMain
var states: Array[Dictionary] = []
var cases: Array[Dictionary] = []
var current_case := ""
var current_phase := -1
var aspect := ""
var texture_cache: Dictionary = {}
var launch_checks: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _base_texture(texture: Texture2D) -> Dictionary:
	if texture == null:
		return {}
	var region := Rect2()
	if texture is AtlasTexture:
		region = (texture as AtlasTexture).region
		texture = (texture as AtlasTexture).atlas
	if texture == null:
		return {}
	var path := texture.resource_path
	if path.is_empty():
		return {"path": "GENERATED_TEXTURE", "size": [texture.get_width(), texture.get_height()]}
	if not texture_cache.has(path):
		texture_cache[path] = FileAccess.get_sha256(path)
	return {"path": path.trim_prefix("res://"), "sha256": texture_cache[path],
		"native_size": [texture.get_width(), texture.get_height()],
		"region": [region.position.x, region.position.y, region.size.x, region.size.y]}

func _textures(value: Variant, slot: String, output: Array[Dictionary], depth: int = 0) -> void:
	if depth > 3:
		return
	if value is Texture2D:
		var entry := _base_texture(value as Texture2D)
		entry["slot"] = slot
		output.append(entry)
	elif value is Array:
		for index: int in range((value as Array).size()):
			_textures(value[index], slot + "[%d]" % index, output, depth + 1)
	elif value is Dictionary:
		for key: Variant in value:
			_textures(value[key], slot + "." + str(key), output, depth + 1)

func _census(node: Node, output: Array[Dictionary]) -> void:
	if not node is CanvasItem:
		for child: Node in node.get_children():
			_census(child, output)
		return
	if node is CanvasItem and not (node as CanvasItem).is_visible_in_tree():
		return
	var script_path := ""
	var script: Script = node.get_script() as Script
	if script != null:
		script_path = script.resource_path.trim_prefix("res://")
	var textures: Array[Dictionary] = []
	for prop: Dictionary in node.get_property_list():
		var prop_name := String(prop.get("name", ""))
		if prop_name in ["script", "owner", "m", "main", "competition", "config"]:
			continue
		var type_id := int(prop.get("type", -1))
		if type_id in [TYPE_OBJECT, TYPE_ARRAY, TYPE_DICTIONARY]:
			_textures(node.get(prop_name), prop_name, textures)
	if not textures.is_empty() or not script_path.is_empty() and node is CanvasItem \
			or node is Button or node is Label or node is ProgressBar \
			or node is ColorRect or node is Panel or node is PanelContainer:
		var item := {"node": str(node.get_path()), "class": node.get_class(),
			"script": script_path, "textures": textures,
			"visibility_qualification": "Visible node; stored draw textures may be unused in the current branch"}
		if node is Control:
			var rect := (node as Control).get_global_rect()
			item["rect"] = [rect.position.x, rect.position.y, rect.size.x, rect.size.y]
		if node is CanvasItem:
			item["z_index"] = (node as CanvasItem).z_index
			item["modulate"] = str((node as CanvasItem).modulate)
		if node is Button or node is Label:
			item["text"] = String(node.get("text"))
		if node is ColorRect:
			item["color"] = str((node as ColorRect).color)
		output.append(item)
	for child: Node in node.get_children():
		_census(child, output)

func shot(beat: String, world: OperaCareerWorld2D = null) -> void:
	await frames(3)
	await RenderingServer.frame_post_draw
	var id := "%s--p%02d--%s--%s" % [current_case, current_phase, beat, aspect]
	var path := OUT + "captures/" + id + ".webp"
	var image: Image = root.get_texture().get_image()
	var error: Error = image.save_webp(path, false)
	var items: Array[Dictionary] = []
	_census(root, items)
	var state := {"id": id, "case": current_case, "phase_index": current_phase,
		"beat": beat, "aspect": aspect, "image": "captures/" + id + ".webp",
		"dimensions": [image.get_width(), image.get_height()], "save_error": error,
		"sha256": FileAccess.get_sha256(path), "items": items,
		"entry_method": "diagnostic_direct_state_selection", "acceptance": "DIAGNOSTIC_ONLY"}
	if world != null:
		state["snapshot"] = world.scene_snapshot()
		state["phase"] = world.phases[current_phase] if current_phase >= 0 and current_phase < world.phases.size() else {}
	states.append(state)
	print("JOBART|", id, "|", error, "|items=", items.size())

func _midpoint(world: OperaCareerWorld2D) -> void:
	# Deliberate state fixtures make all drawn variants inspectable. They do not
	# demonstrate that a child input reaches any of these states.
	var phase: Dictionary = world.phases[world.phase_index]
	world.phase_progress = float(phase.get("goal", 1.0)) * 0.5
	world.surface.set_fill(0.5)
	world.phase_fill.value = 50.0
	world.action_panel.queue_redraw()
	var surface: OperaGestureSurface = world.surface
	if surface is OperaTeacherSurface:
		var teacher := surface as OperaTeacherSurface
		for index: int in range(teacher.counted.size() / 2):
			teacher.counted[index] = true
		teacher.help_visible = true
		teacher.joined = true
		teacher.queue_redraw()
	elif surface is OperaGeologySurface:
		var geology := surface as OperaGeologySurface
		for index: int in range(geology.river_wet.size() / 2):
			geology.river_wet[index] = true
		for index: int in range(geology.fossil_cleared.size() / 2):
			geology.fossil_cleared[index] = true
		geology.pan_wash = 0.5
		geology.geode_pull = 65.0
		geology.queue_redraw()

func _case(config: Dictionary, lane: String, act_index: int) -> void:
	main.clear_dialogue()
	if main.hud_msg != null:
		main.hud_msg.visible = false
	var career := String(config.get("costume", ""))
	current_case = lane + "-" + career
	var director := OperaCompetition.new()
	director.configure(career)
	var world := OperaCareerWorld2D.new()
	main.add_child(world)
	world.setup(main, config, director, Callable())
	if world.root == null or world.phases.is_empty():
		push_error("JOBART: setup failed for " + current_case)
		world.set_process(false)
		world.queue_free()
		await frames(1)
		return
	await frames(4)
	world.set_process(false)
	cases.append({"id": current_case, "career": career, "lane": lane,
		"act_index": act_index, "phase_count": world.phases.size(),
		"phases": world.phases.duplicate(true), "aspect": aspect,
		"story_qualification": "Explicit catalog phase fixture; unmodified story setup separately checked" if lane == "day2" else "Production freeplay configuration"})
	for index: int in range(world.phases.size()):
		current_phase = index
		world.phase_index = index
		world.active = true
		world.reveal_t = 0.0
		world.phase_advance_pending = false
		world.phase_gap = 0.0
		world._arm_phase()
		await shot("invitation", world)
		world._open_task()
		await frames(20)
		await shot("open", world)
		_midpoint(world)
		await shot("partial-fixture", world)
		if world.surface is OperaGeologySurface:
			var geology := world.surface as OperaGeologySurface
			if geology.mode == "geology_fossil":
				geology.fossil_stage = 1
				geology.fossil_cleared.fill(true)
				geology.queue_redraw()
				await shot("assembly-fixture", world)
				geology.fossil_stage = 2
				geology.fossil_snapped = [true, true, true]
				geology.queue_redraw()
				await shot("assembled-fixture", world)
			elif geology.mode == "geology_geode":
				geology.geode_seams.fill(true)
				geology.geode_pull = 140.0
				geology.queue_redraw()
				await shot("opened-geode-fixture", world)
	current_phase = world.phases.size() - 1
	world.celebrate({"tier": 1, "quality": 1.0, "won": true})
	await frames(25)
	await shot("reward-fixture", world)
	world.close()
	world.queue_free()
	await frames(3)

func _tree() -> void:
	main.clear_dialogue()
	if main.hud_msg != null:
		main.hud_msg.visible = false
	current_case = "practice-arborist"
	var level := OperaTreeBookTest.new()
	level.setup(main)
	root.add_child(level)
	await frames(3)
	level.set_process(false)
	cases.append({"id": current_case, "career": "arborist", "lane": "practice", "phase_count": 6, "aspect": aspect})
	for step: int in range(6):
		current_phase = step
		level.restore_progress({"version": 1, "patient": "orange_spots", "stage": step})
		await shot("open")
		if step == 4:
			level.treatment = 0.5
			level.queue_redraw()
			await shot("partial-fixture")
	level.queue_free()
	await frames(2)

func _rooms() -> void:
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.open("opera_hall")
	for room_id: String in CastleCareerRoutes.ROOM_ACT_INDICES:
		current_case = "entrance-" + room_id
		current_phase = -1
		rooms.show_room(room_id, false)
		main._castle_career_routes_ref().sync()
		await frames(8)
		await shot("entrance")
		if room_id == "opera_hall":
			main._castle_career_routes_ref().open_opera_venue()
			await frames(8)
			await shot("foyer")
			main._castle_career_routes_ref().close_opera_venue()
	rooms.close()
	await frames(3)

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT + "captures")
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	# Isolate all startup and diagnostic checkpoint writes from the owner's save.
	main._save_state = SaveState.new(main, "res://tmp/day2_job_capture_save.json")
	root.add_child(main)
	await frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.player != null:
		main.player.visible = false
	for size: Vector2i in ASPECTS:
		root.mode = Window.MODE_WINDOWED
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		root.size = size
		DisplayServer.window_set_size(size)
		await frames(5)
		aspect = "%dx%d" % [size.x, size.y]
		await _rooms()
		for index: int in OperaHouse.LIVE_ACT_INDICES:
			await _case((OperaHouse.ACTS[index] as Dictionary).duplicate(true), "career", index)
		for entry: Dictionary in ChapterTwoPartyPlan.LIVE_CAREERS:
			var index := int(entry["act_index"])
			var config := (OperaHouse.ACTS[index] as Dictionary).duplicate(true)
			config["reward_policy"] = "chapter2_story"
			config["run_context"] = {"chapter": "chapter2"}
			config["scene_adapter"] = ChapterTwoCareerSceneAdapter.adapter_config(
				String(config["costume"]))
			if aspect == "1280x720":
				var check_director := OperaCompetition.new()
				check_director.configure(String(config["costume"]))
				var check_world := OperaCareerWorld2D.new()
				main.add_child(check_world)
				check_world.set_process(false)
				check_world.setup(main, config, check_director, Callable())
				launch_checks.append({"act_index": index,
					"career": config["costume"], "production_equivalent_config": config.duplicate(true),
					"root_built": check_world.root != null,
					"phase_count": check_world.phases.size(),
					"qualification": "Direct world seam using the unmodified OperaHouse story configuration, not UI route traversal"})
				check_world.queue_free()
				await frames(1)
			# The unmodified production setup currently rejects its default empty
			# phase_overrides. This explicit catalog fixture exposes the authored
			# art for review; it must not be represented as a working story route.
			config["phase_overrides"] = ChapterTwoCareerSceneAdapter.phase_set(
				String(config["costume"]))["phases"]
			config["scene_adapter"] = ChapterTwoCareerSceneAdapter.adapter_config(
				String(config["costume"]))
			await _case(config, "day2", index)
		await _tree()
	var file := FileAccess.open(OUT + "capture_manifest.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"schema": "reef.job_art_diagnostic.v1",
		"engine": Engine.get_version_info(), "renderer": RenderingServer.get_current_rendering_method(),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_job_contexts.gd"),
		"captured_at_utc": Time.get_datetime_string_from_system(true),
		"cases": cases, "states": states, "launch_checks": launch_checks,
		"acceptance": "DIAGNOSTIC_ONLY",
		"limitations": "Direct phase/open/progress/reward fixtures, hidden global HUD; no one-use authoritative layer proof, real route traversal, played motion, device, child or owner acceptance."}, "\t"))
	file.close()
	main.queue_free()
	await frames(2)
	quit()
