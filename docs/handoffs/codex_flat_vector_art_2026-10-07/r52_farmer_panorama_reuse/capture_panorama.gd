extends SceneTree
## R51 source-exact Farmer context: original scene/viewport inputs/private profile.
var m: ReefMain
var world: OperaCareerWorld2D
var out_dir := ""
var profile := ""
var states: Array[Dictionary] = []
var events: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var seed: Dictionary = {}
var boot_count := 0
var trial_backdrop: OperaWorldBackdrop2D
var visual_mode := "original"
var comparison_checks: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var p := base + suffix
		result[suffix] = FileAccess.get_sha256(p) if FileAccess.file_exists(p) else "absent"
	return result

func _frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _wait(predicate: Callable, seconds: float = 12.0) -> bool:
	var deadline := Time.get_ticks_msec() + int(seconds * 1000.0)
	while Time.get_ticks_msec() < deadline:
		if bool(predicate.call()):
			return true
		await process_frame
	return bool(predicate.call())

func _aspect(size: Vector2i) -> bool:
	root.mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		root.size = size
		DisplayServer.window_set_size(size)
		await process_frame
		var frame: Image = root.get_texture().get_image()
		if frame != null and frame.get_size() == size:
			return true
	return false

func _tex(t: Texture2D) -> Dictionary:
	if t == null:
		return {}
	var row := {"class": t.get_class(), "path": t.resource_path, "size": str(t.get_size())}
	if t is AtlasTexture:
		var atlas := t as AtlasTexture
		row["atlas_path"] = atlas.atlas.resource_path if atlas.atlas != null else ""
		row["region"] = str(atlas.region)
	return row

func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row := {"path": str(node.get_path()), "class": node.get_class(), "script": node.get_script().resource_path if node.get_script() != null else "", "z_index": item.z_index, "modulate": str(item.modulate), "self_modulate": str(item.self_modulate)}
		var c := node as Control
		if c != null:
			row["global_rect"] = str(c.get_global_rect())
			row["mouse_filter"] = c.mouse_filter
		var sprite := node as Sprite2D
		if sprite != null:
			row["texture"] = _tex(sprite.texture)
		var rect := node as TextureRect
		if rect != null:
			row["texture"] = _tex(rect.texture)
		var button := node as TextureButton
		if button != null:
			row["texture"] = _tex(button.texture_normal)
			row["disabled"] = button.disabled
		var color := node as ColorRect
		if color != null:
			row["color"] = str(color.color)
		var poly := node as Polygon2D
		if poly != null:
			row["polygon"] = str(poly.polygon)
			row["color"] = str(poly.color)
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _disk_story() -> Dictionary:
	if not FileAccess.file_exists(profile):
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(profile))
	var result: Dictionary = {}
	if parsed is Dictionary:
		for key: String in ["save_generation", "chapter2_strawberry_mask", "chapter2_job_phase_masks", "chapter2_party_piece_mask", "chapter2_farmer_strawberries_ready", "chapter2_skill_mask"]:
			result[key] = parsed.get(key)
	return result

func _snapshot() -> Dictionary:
	var s := {"normal_route_proved": false, "private_checkpoint": true, "time_scale": Engine.time_scale, "paused": paused}
	if is_instance_valid(m):
		s["game"] = m.game
		s["quality"] = m.quality
		s["castle_room"] = m.castle_room_id
		s["living_stage"] = m.living_stage_id
		s["freeplay"] = [m.opera_stars, m.opera_progress, m.pearl_count]
		s["story"] = m._chapter_two_ref().serialize_state()
		s["save_path"] = m._save_state.save_path
		s["private_disk_story"] = _disk_story()
		s["save_sha256"] = FileAccess.get_sha256(profile) if FileAccess.file_exists(profile) else "absent"
		s["presentation"] = {"menu": m.start_menu_active, "intro": m.intro_active, "boot_splash": m.get_node_or_null("BootSplashHandoff") != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0}
	if is_instance_valid(world):
		var surface := world.surface
		s["world"] = {"career_id": world.career_id, "active": world.active, "task_open": world.task_open, "phase_index": world.phase_index, "phase_progress": world.phase_progress, "phase_advance_pending": world.phase_advance_pending, "phase_complete_t": world.phase_complete_t, "elapsed": world.elapsed, "reveal_t": world.reveal_t, "phase": world.phases[world.phase_index] if world.phase_index < world.phases.size() else {}, "station_for_phase": world.station_for_phase}
		if surface != null:
			s["surface"] = {"rect": str(surface.get_global_rect()), "size": str(surface.size), "visual_context": surface.visual_context, "widget_template": surface.widget_template, "held": surface.held, "target_placed": surface.target_placed.duplicate(), "long_push_journey": surface.long_push_journey, "long_push_engaged": surface.long_push_engaged, "last_contextual_draw_route": surface.last_contextual_draw_route, "last_target_subject_route": surface.last_target_subject_route, "widget_mover": _tex(surface.widget_mover), "widget_stamp": _tex(surface.widget_stamp), "widget_overlay": _tex(surface.widget_overlay)}
	if is_instance_valid(world):
		s["visual_trial"] = {"mode": visual_mode, "production_source_changed": false,
			"world_root_rect": str(world.root.get_global_rect()), "world_root_scale": str(world.root.scale),
			"original_backdrop_visible": world.backdrop_node.visible,
			"candidate_visible": trial_backdrop.visible if is_instance_valid(trial_backdrop) else false,
			"candidate_mapping": trial_backdrop.get("mapping_rows") if is_instance_valid(trial_backdrop) else [],
			"player_rect": str(world.player_actor.get_global_rect()), "player_texture": _tex(world.player_actor.texture),
			"rival_texture": _tex(world.rival_actor.texture),
			"surface_rect": str(world.surface.get_global_rect()) if world.surface != null else ""}
	return s

func _capture(id: String, role := "CURRENT_PRIVATE_CHECKPOINT_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("framebuffer capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	if is_instance_valid(m):
		if is_instance_valid(world) and world.root != null:
			_nodes(world.root, nodes)
		elif m.castle_room_layer != null:
			_nodes(m.castle_room_layer, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path), "size": [image.get_width(), image.get_height()], "role": role, "snapshot": _snapshot(), "selected_canvas_nodes": nodes, "node_inventory_scope": "Selected actual Farmer root subtree; not whole-game/native/medium closure", "ticks_msec": Time.get_ticks_msec()})
	print("FARMER52|CAPTURE|", id)

func _point(c: Control, at: Vector2) -> Vector2:
	return c.get_global_transform_with_canvas() * at

func _touch(c: Control, at: Vector2, pressed: bool) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 71
	e.position = _point(c, at)
	e.pressed = pressed
	events.append({"type": "touch", "pressed": pressed, "point": str(e.position), "local": str(at), "target": str(c.get_path()), "ticks_msec": Time.get_ticks_msec()})
	c.get_viewport().push_input(e, true)

func _drag(c: Control, at: Vector2) -> void:
	var e := InputEventScreenDrag.new()
	e.index = 71
	e.position = _point(c, at)
	events.append({"type": "drag", "point": str(e.position), "local": str(at), "target": str(c.get_path()), "ticks_msec": Time.get_ticks_msec()})
	c.get_viewport().push_input(e, true)

func _tap(c: Control, at: Vector2, id := "") -> void:
	_touch(c, at, true)
	await _frames(1)
	if not id.is_empty():
		await _capture(id + "_pressed")
	_touch(c, at, false)
	await _frames(2)
	if not id.is_empty():
		await _capture(id + "_released")

func _boot() -> bool:
	var packed := load("res://scenes/main.tscn") as PackedScene
	m = packed.instantiate() as ReefMain
	m._save_state = SaveState.new(m, profile)
	root.add_child(m)
	current_scene = m
	boot_count += 1
	await _frames(3)
	m._apply_quality("speedy")
	if not await _wait(func() -> bool: return m.get_node_or_null("BootSplashHandoff") == null, 15.0):
		errors.append("boot splash did not release")
		return false
	var button := m.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button if m.start_menu_layer != null else null
	if button != null and button.is_visible_in_tree() and not button.disabled:
		await _tap(button, button.size * 0.5)
	else:
		errors.append("actual Continue button unavailable")
		return false
	if m.intro_active:
		m._skip_intro()
	if not await _wait(func() -> bool: return not m.start_menu_active and not m.intro_active and m.fade_rect.modulate.a <= 0.02, 15.0):
		errors.append("startup presentation did not settle")
		return false
	if m._save_state.save_path != profile:
		errors.append("private save dependency did not remain bound")
		return false
	# The unchanged current probe uses this declared startup routing seam.
	# No phase,progress,target,clock or geometry is written by this fixture.
	m.game = "level2"
	m.g["t"] = 0.0
	m._enter_castle_interior_now(false)
	await _frames(3)
	m._castle_rooms_ref().show_room("dining_room", false)
	await _frames(3)
	return true

func _enter_farmer(prefix: String) -> bool:
	var routes := m._castle_career_routes_ref()
	routes.sync()
	await _frames(2)
	var button := routes.button_for_act(ChapterTwoDirector.ACT_FARMER)
	if button == null or button.disabled or not button.is_visible_in_tree():
		errors.append("original Farmer DiningRoom picture unavailable")
		return false
	await _capture(prefix + "_dining_room", "EXCLUDED_ROOM_ENTRY_DIAGNOSTIC")
	await _tap(button, button.size * 0.5)
	if not await _wait(func() -> bool: return m.opera_game != null and m.living_stage_id == "opera.act.06" and m.fade_rect.modulate.a <= 0.02, 18.0):
		errors.append("original Farmer picture route did not open")
		return false
	var house := m.opera_game as OperaHouse
	world = house.act.career_world_2d
	if world == null or world.career_id != "farmer" or not world.using_chapter_two_phases:
		errors.append("wrong Farmer world/phase source")
		return false
	await _frames(4)
	await _capture(prefix + "_world")
	return true

func _open_phase(index: int, prefix: String) -> bool:
	if not await _wait(func() -> bool: return is_instance_valid(world) and world.phase_index == index and not world.phase_advance_pending, 15.0):
		errors.append("expected phase did not arm " + str(index))
		return false
	if not world.task_open:
		var station := int(world.station_for_phase.get(index, -1))
		if station < 0 or station >= world.station_nodes.size():
			errors.append("phase station binding missing")
			return false
		var hotspot := world.station_nodes[station] as OperaWorldHotspot2D
		await _capture(prefix + "_invitation")
		await _tap(hotspot.touch_button, hotspot.touch_button.size * 0.5)
	if not await _wait(func() -> bool: return is_instance_valid(world) and world.phase_index == index and world.task_open and world.reveal_t <= 0.0, 15.0):
		errors.append("original approach did not open task " + str(index))
		return false
	await _capture(prefix + "_early")
	await _frames(30)
	await _capture(prefix + "_ready")
	return true

func _retire() -> void:
	if is_instance_valid(m):
		m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
		if current_scene == m:
			current_scene = null
		m.queue_free()
		await _frames(12)
	m = null
	world = null

func _install_trial() -> void:
	var script := load("res://export/flat_vector_r52/candidate_backdrop.gd") as GDScript
	trial_backdrop = script.new() as OperaWorldBackdrop2D
	trial_backdrop.name = "R52VisualOnlyBackdrop"
	world.root.add_child(trial_backdrop)
	world.root.move_child(trial_backdrop, world.backdrop_node.get_index() + 1)
	trial_backdrop.position = world.backdrop_node.position
	trial_backdrop.size = world.backdrop_node.size
	trial_backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	trial_backdrop.setup(world.career_id, world.backdrop_node.scene_variant)
	trial_backdrop.visible = false

func _set_mode(mode: String) -> void:
	visual_mode = mode
	var original := mode in ["original", "original_restore"]
	world.backdrop_node.visible = original
	trial_backdrop.visible = not original
	trial_backdrop.set("trial_mode", mode)
	trial_backdrop.queue_redraw()

func _compare(prefix: String) -> void:
	var story := m._chapter_two_ref().serialize_state()
	var phase := world.phase_index
	var progress := world.phase_progress
	var root_rect := world.root.get_global_rect()
	var surface_rect := world.surface.get_global_rect() if world.surface != null else Rect2()
	for mode: String in ["original", "centered", "preserve_lower", "original_restore"]:
		_set_mode(mode)
		await _frames(2)
		await _capture(prefix + "_" + mode,
			"CURRENT_SOURCE_CONTROL_CONTEXT" if mode in ["original", "original_restore"] else "NONRUNTIME_VISUAL_REUSE_CANDIDATE")
		var same := world.phase_index == phase and world.phase_progress == progress \
			and m._chapter_two_ref().serialize_state() == story \
			and world.root.get_global_rect() == root_rect \
			and (world.surface == null or world.surface.get_global_rect() == surface_rect)
		comparison_checks.append({"state": prefix, "mode": mode, "story_phase_progress_geometry_unchanged": same})
		if not same:
			errors.append("visual-only comparison changed source-owned state/geometry " + prefix + mode)
	_set_mode("preserve_lower")

func _components() -> void:
	for mode: String in ["original", "centered", "preserve_lower"]:
		var viewport := SubViewport.new()
		viewport.size = Vector2i(1280, 720)
		viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(viewport)
		var backdrop: OperaWorldBackdrop2D
		if mode == "original":
			backdrop = OperaWorldBackdrop2D.new()
		else:
			var script := load("res://export/flat_vector_r52/candidate_backdrop.gd") as GDScript
			backdrop = script.new() as OperaWorldBackdrop2D
			backdrop.set("trial_mode", mode)
		viewport.add_child(backdrop)
		backdrop.size = Vector2(1280, 720)
		backdrop.setup("farmer", "sky_lagoon_farmer")
		await _frames(3)
		await RenderingServer.frame_post_draw
		var image := viewport.get_texture().get_image()
		var id := "component_" + mode
		var path := out_dir.path_join(id + ".png")
		if image == null or image.save_png(path) != OK:
			errors.append("component capture failed " + mode)
		else:
			states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path),
				"size": [image.get_width(), image.get_height()], "role": "EXCLUDED_COMPONENT_DIAGNOSTIC",
				"snapshot": {"visual_mode": mode, "live_game_state": false}, "selected_canvas_nodes": []})
		viewport.queue_free()
		await _frames(2)

func _exercise() -> void:
	if not await _boot() or not await _enter_farmer("first"):
		return
	_install_trial()
	var freeplay_before := [m.opera_stars, m.opera_progress, m.pearl_count]
	if not await _open_phase(0, "gather"):
		return
	await _compare("gather_ready")
	for i: int in range(5):
		var target: TextureButton = null
		for button: TextureButton in world.chapter2_strawberry_pickups:
			if not button.disabled and button.is_visible_in_tree():
				target = button
				break
		if target == null:
			errors.append("original pickup unavailable")
			return
		await _tap(target, target.size * 0.5)
		if i in [0, 4]:
			await _capture("gather_candidate_%d" % i, "NONRUNTIME_VISUAL_REUSE_CANDIDATE")
	if not await _open_phase(1, "fill"):
		return
	await _compare("fill_ready")
	var surface := world.surface
	for i: int in range(5):
		await _tap(surface, surface._target_anchor_point(maxi(0, surface._target_next_unplaced())))
		if i in [0, 1, 4]:
			await _capture("fill_candidate_%d" % i, "NONRUNTIME_VISUAL_REUSE_CANDIDATE")
		if i == 1:
			await _compare("fill_partial_two")
	if not await _open_phase(2, "delivery"):
		return
	await _compare("delivery_ready")
	surface = world.surface
	var start := surface._long_push_start()
	var finish := surface._long_push_end()
	_touch(surface, start, true)
	await _frames(1)
	for i: int in range(1, 33):
		_drag(surface, start.lerp(finish, float(i) / 64.0))
		await process_frame
	_touch(surface, start.lerp(finish, 0.5), false)
	await _frames(3)
	await _compare("delivery_half_released")
	start = surface._long_push_position(surface.long_push_journey)
	_touch(surface, start, true)
	await _frames(1)
	for i: int in range(1, 65):
		_drag(surface, start.lerp(finish, float(i) / 64.0))
		await process_frame
	_touch(surface, finish, false)
	await _frames(2)
	await _capture("delivery_candidate_endpoint", "NONRUNTIME_VISUAL_REUSE_CANDIDATE")
	_set_mode("original_restore")
	await _frames(2)
	await _capture("delivery_original_restore_endpoint", "CURRENT_SOURCE_CONTROL_CONTEXT")
	if not await _wait(func() -> bool: return m.opera_game == null, 18.0):
		errors.append("original delivery callback did not return")
	await _capture("farmer_result_return", "EXCLUDED_RETURN_DIAGNOSTIC")
	if [m.opera_stars, m.opera_progress, m.pearl_count] != freeplay_before:
		errors.append("story play changed freeplay counters")
	await _retire()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless" or Engine.time_scale != 1.0:
		quit(1)
		return
	out_dir = OS.get_environment("R52_OUT")
	var width := int(OS.get_environment("R52_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false, "day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER, "day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true, "chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449, "chapter2_job_phase_masks": [0, 0, 0, 0, 0, 0, 0, 0], "music": false, "mic": false, "quality": "speedy", "pearls": 23, "pearls_ever": 23, "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": []}
	var file := FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	if not await _aspect(Vector2i(width, 720)):
		errors.append("native viewport size did not settle")
	else:
		if width == 1280:
			await _components()
		await _exercise()
	await _retire()
	if _normal_hashes() != normal_before:
		errors.append("normal eight save suffixes changed")
	var report := {"schema": "reef.farmer_panorama_reuse/1", "source_revision": OS.get_environment("R52_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count, "mode": "VISUAL_ONLY_PANORAMA_REUSE_NO_PRODUCTION_ADOPTION", "comparison_checks": comparison_checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "actual_child_data": false, "normal_route_proved": false, "scope": "Original Main/scene/viewport controls with declared synthetic postboss/startup room seams. Explicit temporary visual-only ignored backdrop subclass changes source sampling forcomparison;originalrestore retained. No gameplay phase/progress/clock/target/hit/geometry orproduction source writes. Bot geometry oracle;notadoption,QA11/device/child/owner/artacceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("FARMER52|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
