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
		var row := {"path": str(node.get_path()), "class": node.get_class(), "script": node.get_script().resource_path if node.get_script() != null else "", "z_index": item.z_index, "modulate": str(item.modulate)}
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
		s["save_sha256"] = FileAccess.get_sha256(profile) if FileAccess.file_exists(profile) else "absent"
		s["presentation"] = {"menu": m.start_menu_active, "intro": m.intro_active, "boot_splash": m.get_node_or_null("BootSplashHandoff") != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0}
	if is_instance_valid(world):
		var surface := world.surface
		s["world"] = {"career_id": world.career_id, "active": world.active, "task_open": world.task_open, "phase_index": world.phase_index, "phase_progress": world.phase_progress, "phase_advance_pending": world.phase_advance_pending, "phase_complete_t": world.phase_complete_t, "elapsed": world.elapsed, "reveal_t": world.reveal_t, "phase": world.phases[world.phase_index] if world.phase_index < world.phases.size() else {}, "station_for_phase": world.station_for_phase}
		if surface != null:
			s["surface"] = {"rect": str(surface.get_global_rect()), "size": str(surface.size), "visual_context": surface.visual_context, "widget_template": surface.widget_template, "held": surface.held, "target_placed": surface.target_placed.duplicate(), "long_push_journey": surface.long_push_journey, "long_push_engaged": surface.long_push_engaged, "last_contextual_draw_route": surface.last_contextual_draw_route, "last_target_subject_route": surface.last_target_subject_route, "widget_mover": _tex(surface.widget_mover), "widget_stamp": _tex(surface.widget_stamp), "widget_overlay": _tex(surface.widget_overlay)}
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
		if is_instance_valid(world) and m.living_layer != null:
			_nodes(m.living_layer, nodes)
		elif m.castle_room_layer != null:
			_nodes(m.castle_room_layer, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path), "size": [image.get_width(), image.get_height()], "role": role, "snapshot": _snapshot(), "selected_canvas_nodes": nodes, "node_inventory_scope": "Selected visible Canvas subtree only; not native/whole-tree/medium closure", "ticks_msec": Time.get_ticks_msec()})
	print("FARMER51|CAPTURE|", id)

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

func _exercise() -> void:
	if not await _boot() or not await _enter_farmer("first") or not await _open_phase(0, "gather"):
		return
	var freeplay_before := [m.opera_stars, m.opera_progress, m.pearl_count]
	await _frames(30)
	await _capture("gather_passive")
	for i: int in range(5):
		if not is_instance_valid(world) or world.phase_index != 0:
			errors.append("gather advanced before five original pickup taps")
			return
		var target: TextureButton = null
		for b: TextureButton in world.chapter2_strawberry_pickups:
			if not b.disabled and b.is_visible_in_tree():
				target = b
				break
		if target == null:
			errors.append("remaining strawberry pickup unavailable")
			return
		await _tap(target, target.size * 0.5, "gather_%d" % i)
	if not await _open_phase(1, "fill_first"):
		return
	await _capture("fill_before_private_reload")
	# Original lifecycle save/release; no snapshot mask or completion is injected.
	await _retire()
	if not await _boot() or not await _enter_farmer("reload") or not await _open_phase(1, "fill_reload"):
		return
	await _capture("fill_after_private_reload")
	var surface := world.surface
	var before := world.phase_progress
	await _tap(surface, Vector2(8, 8), "fill_off_target")
	if world.phase_progress != before:
		errors.append("off-target input changed fill progress")
	await _frames(30)
	await _capture("fill_passive")
	for i: int in range(5):
		if not is_instance_valid(world) or world.phase_index != 1:
			errors.append("fill advanced before five target taps")
			return
		var next := maxi(0, surface._target_next_unplaced())
		var point := surface._target_anchor_point(next)
		await _tap(surface, point, "fill_%d" % i)
		if i == 1:
			m._pause_ref().toggle_pause()
			await _frames(3)
			await _capture("fill_pause", "EXCLUDED_PAUSE_DIAGNOSTIC")
			m._pause_ref().toggle_pause()
			await _frames(4)
			await _capture("fill_resumed")
		await _frames(3)
	await _capture("fill_full_settle")
	if not await _open_phase(2, "delivery"):
		return
	surface = world.surface
	await _frames(30)
	await _capture("delivery_passive")
	if world.phase_progress != 0.0 or surface.long_push_journey != 0.0:
		errors.append("passive delivery banked progress")
	var start := surface._long_push_start()
	var finish := surface._long_push_end()
	_touch(surface, start, true)
	await _frames(1)
	await _capture("delivery_pressed")
	for i: int in range(1, 33):
		_drag(surface, start.lerp(finish, float(i) / 64.0))
		await process_frame
		if i in [8, 16, 32]:
			await _capture("delivery_drag_%d" % i)
	_touch(surface, start.lerp(finish, 0.5), false)
	await _frames(3)
	await _capture("delivery_partial_released")
	start = surface._long_push_position(surface.long_push_journey)
	_touch(surface, start, true)
	await _frames(1)
	for i: int in range(1, 65):
		_drag(surface, start.lerp(finish, float(i) / 64.0))
		await process_frame
		if i in [16, 32, 48, 63]:
			await _capture("delivery_finish_drag_%d" % i)
	_touch(surface, finish, false)
	await _frames(2)
	await _capture("delivery_endpoint_released")
	if not await _wait(func() -> bool: return m.opera_game == null, 18.0):
		errors.append("delivery did not return through original completion")
	await _capture("farmer_result_return", "EXCLUDED_RETURN_DIAGNOSTIC")
	if [m.opera_stars, m.opera_progress, m.pearl_count] != freeplay_before:
		errors.append("story play changed freeplay reward counters")
	await _retire()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless" or Engine.time_scale != 1.0:
		quit(1)
		return
	out_dir = OS.get_environment("R51_OUT")
	var width := int(OS.get_environment("R51_WIDTH"))
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
		await _exercise()
	await _retire()
	if _normal_hashes() != normal_before:
		errors.append("normal eight save suffixes changed")
	var report := {"schema": "reef.farmer_context/1", "source_revision": OS.get_environment("R51_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "actual_child_data": false, "normal_route_proved": false, "scope": "Original Main/scene/controls from a declared private post-boss checkpoint and startup room API seam. Real viewport inputs, no phase/progress/clock/target/geometry/visual mutation. Source-readable target geometry is a bot oracle, not child/device/QA11 or artwork acceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("FARMER51|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
