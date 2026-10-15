extends SceneTree
## R48 current Grand Puff encounter audit from a declared private saved checkpoint.
var m: ReefMain
var out_dir := ""
var mode := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var action_events: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")


func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _wait_frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _set_aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var test: Image = get_root().get_texture().get_image()
		if test != null and test.get_size() == target:
			return true
	return false

func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}

func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false

func _retire_main() -> void:
	m.set_process(false)
	m.queue_free()
	await _wait_frames(10)
	m = null


func _new_main(profile: String) -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	m._save_state = SaveState.new(m, profile)
	get_root().add_child(m)
	await _wait_frames(3)
	m._apply_quality("speedy")
	if m.start_menu_active:
		m._start_menu_ref()._dismiss_menu()
	if m.intro_active:
		m._skip_intro()
	if not await _wait_presentation():
		errors.append("startup did not settle")
		return false
	return true

func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row: Dictionary = {"path": str(node.get_path()), "class": node.get_class(), "z_index": item.z_index, "modulate": str(item.modulate)}
		var control := node as Control
		if control != null:
			row["global_rect"] = str(control.get_global_rect())
		var sprite := node as Sprite2D
		var texture: Texture2D = sprite.texture if sprite != null else null
		var tr := node as TextureRect
		if tr != null:
			texture = tr.texture
		if texture != null:
			row["texture"] = texture.resource_path
			row["texture_size"] = str(texture.get_size())
			if texture is AtlasTexture:
				var atlas := texture as AtlasTexture
				row["atlas_source"] = atlas.atlas.resource_path if atlas.atlas != null else ""
				row["atlas_region"] = str(atlas.region)
		var label := node as Label
		if label != null:
			row["text"] = label.text
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _snapshot() -> Dictionary:
	var result: Dictionary = {"game": m.game, "room": m.castle_room_id, "director": m._day_one_ref().serialize_state(), "pearl_count": m.pearl_count, "paused": paused, "story_clip_open": m._day_one_story_clip != null and is_instance_valid(m._day_one_story_clip)}
	var boss: DustBossGame = null
	if m.game == "dustboss":
		boss = m._game_obj("dustboss", DustBossGame) as DustBossGame
	var values: Dictionary = {}
	for key: String in ["db_state", "db_st", "db_hits", "db_damage_taken", "db_opening_misses", "db_taps_this_round", "db_avoids", "db_done", "db_story_transformation"]:
		if m.g.has(key):
			values[key] = m.g[key]
	result["boss_values"] = values
	if m.game == "dustboss" and boss != null:
		result["geometry"] = boss.danger_geometry()
		result["player_floor"] = str(boss.stage.player_local())
		result["navigation"] = {"destination": str(boss.navigation.destination), "travelling": boss.navigation.travelling}
		var k := boss.kit()
		if k != null:
			result["kit"] = {"class": k.get_class(), "vulnerable": k.vulnerable, "accepted_taps": k.accepted_taps, "rounds": k.damage_rounds_completed, "animation": str(k.sprite.animation), "frame": k.sprite.frame, "visual_class": k.sprite.get_class()}
		var lesson := m.g.get("db_lesson") as DustBossLesson2D
		if lesson != null:
			result["lesson"] = {"mode": lesson.mode, "from": str(lesson.from), "target": str(lesson.target), "boss_anchor": str(lesson.boss_anchor), "counter_open": lesson.counter_open}
	return result

func _capture(id: String, role: String) -> void:
	if states.size() >= 90:
		errors.append("bounded native capture cap reached")
		return
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != get_root().size or image.save_png(path) != OK:
		errors.append("native capture failed " + id)
		return
	var rows: Array[Dictionary] = []
	_nodes(m, rows)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path), "width": image.get_width(), "height": image.get_height(), "role": role, "snapshot": _snapshot(), "nodes": rows, "presentation": _presentation(), "last_event": action_events.back() if not action_events.is_empty() else {}})
	print("PUFF48|CAPTURE|" + mode + "|" + id)

func _pointer(pressed: bool, point: Vector2) -> void:
	var motion := InputEventMouseMotion.new()
	motion.position = point
	motion.global_position = point
	get_root().push_input(motion, true)
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = pressed
	ev.position = point
	ev.global_position = point
	get_root().push_input(ev, true)
	action_events.append({"type": "InputEventMouseButton", "pressed": pressed, "point": str(point), "frame": Engine.get_process_frames(), "room": m.castle_room_id})
	await process_frame

func _tap(point: Vector2, purpose: String) -> void:
	action_events.append({"type": "BOT_ORACLE_TARGET", "purpose": purpose, "point": str(point), "frame": Engine.get_process_frames()})
	await _pointer(true, point)
	await _pointer(false, point)

func _enter_portal() -> bool:
	for attempt: int in range(15):
		var button := m.find_child("HallDoor___royal_hall", true, false) as Button
		if button == null or not button.is_visible_in_tree():
			errors.append("event-only Royal Hall portal unavailable")
			return false
		var point: Vector2 = button.get_global_transform_with_canvas() * (button.size * 0.5)
		if point.x > 35.0 and point.x < float(get_root().size.x) - 35.0:
			await _tap(point, "actual event-only Royal Hall portal")
			var began: int = Time.get_ticks_msec()
			while Time.get_ticks_msec() - began < 30000:
				await process_frame
				if m.game == "dustboss":
					return true
			errors.append("actual portal did not start boss before deadline")
			return false
		var endpoint := Vector2(float(get_root().size.x) - 20.0, 600.0)
		await _pointer(true, endpoint)
		await _wait_frames(22)
		await _pointer(false, endpoint)
		await _wait_frames(3)
	errors.append("Royal Hall portal never became onscreen")
	return false

func _play() -> void:
	var boss := m._game_obj("dustboss", DustBossGame) as DustBossGame
	var seen: Dictionary = {}
	var began: int = Time.get_ticks_msec()
	var last_nav_frame: int = -100
	while m.game == "dustboss" and errors.is_empty() and Time.get_ticks_msec() - began < 300000:
		await process_frame
		var state: String = String(m.g.get("db_state", ""))
		var rounds: int = int(m.g.get("db_hits", 0))
		var geometry: Dictionary = boss.danger_geometry()
		var step: int = int(geometry.get("step", 0))
		var key := "r%d_s%d_%s" % [rounds, step, state]
		if state == "splash":
			var splash := m.g.get("db_splash") as BossSplash2D
			if splash != null:
				var beat := "identity" if splash._elapsed < 1.42 else "weakness"
				if splash._elapsed >= 1.02 and not seen.has("splash_" + beat):
					seen["splash_" + beat] = true
					await _capture("splash_" + beat, "ENCOUNTER_CONTEXT")
			continue
		if state == "showing":
			if not seen.has(key):
				seen[key] = true
				await _capture(key, "ENCOUNTER_CONTEXT")
				await _wait_frames(18)
				var lesson := m.g.get("db_lesson") as DustBossLesson2D
				await _tap(lesson.target, "source lesson movement target; real navigation")
		elif state in ["tell", "strike"]:
			var progress: float = boss.patterns.elapsed / maxf(boss.patterns.tell_time, 0.01)
			var beat: String = "late" if progress >= 0.78 else "early"
			var image_id := key + "_" + beat
			if (progress >= 0.18 or state == "strike") and not seen.has(image_id):
				seen[image_id] = true
				await _capture(image_id, "ENCOUNTER_CONTEXT")
			if boss.patterns.contains(boss.stage.player_local()) and Engine.get_process_frames() - last_nav_frame >= 16:
				var safe: Vector2 = geometry.get("safe_point", boss.stage.player_local()) as Vector2
				var point: Vector2 = boss.stage.project_floor_point(safe)
				await _tap(point, "read-only source safe-point oracle; actual floor travel")
				last_nav_frame = Engine.get_process_frames()
		elif state == "vuln":
			var k := boss.kit()
			if k != null and k.vulnerable:
				var tap_id := key + "_tap" + str(k.accepted_taps)
				if not seen.has(tap_id):
					seen[tap_id] = true
					await _capture(tap_id + "_before", "ENCOUNTER_CONTEXT")
				var lesson := m.g.get("db_lesson") as DustBossLesson2D
				var point: Vector2 = lesson.boss_anchor + Vector2(0.0, 28.0)
				action_events.append({"type": "SOURCE_HIT_AREA_OBSERVATION", "hit": boss._screen_hit(point), "point": str(point), "rounds": rounds})
				await _tap(point, "actual vulnerable boss pointer hit")
				await _capture(tap_id + "_after_" + str(action_events.size()), "ENCOUNTER_CONTEXT")
				await _wait_frames(5)
		elif state == "struck":
			if not seen.has(key):
				seen[key] = true
				await _capture(key, "ENCOUNTER_CONTEXT")
			var lesson := m.g.get("db_lesson") as DustBossLesson2D
			if lesson != null and lesson.mode == "dash" and not seen.has("dash_input"):
				seen["dash_input"] = true
				await _capture("dash_lesson", "ENCOUNTER_CONTEXT")
				await _tap(lesson.target, "first actual dash tap")
				await _tap(lesson.target, "second actual dash tap")
		elif state == "friends":
			if not seen.has(key):
				seen[key] = true
				await _capture(key, "ENCOUNTER_CONTEXT")
		elif not seen.has(key) and not state.is_empty():
			seen[key] = true
			await _capture(key, "ENCOUNTER_CONTEXT")
	if m.game == "dustboss":
		errors.append("source-controlled encounter did not finish before deadline")
	await _wait_frames(12)
	await _capture("encounter_boundary", "BOUNDARY_DIAGNOSTIC")

func _seed() -> Dictionary:
	var seen: Dictionary = {}
	for clip: String in DayOneStoryClips.clip_ids():
		seen[clip] = true
	var rooms: Array[String] = ["bathroom", "pool", "stuffie", "art"]
	return {"schema_version": 1, "won": {}, "found": {}, "plays": 3, "pearls": 23, "pearls_ever": 23, "music": false, "mic": false, "quality": "speedy", "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": [], "day_one_active": true, "day_one_current_room": "", "day_one_completed_rooms": rooms, "day_one_cleaned_rooms": rooms, "day_one_arrival_plane_media_seen": true, "day_one_dirty_castle_discovered": true, "day_one_grok_video_2_seen": true, "day_one_story_clips_seen": seen, "companion": "eagle", "stuffie_wins": {"rescued_eagle": true}, "dustboss_pending_rounds": 0, "dustboss_pending_damage": 0, "dustboss_pending_misses": 0, "dustboss_pending_attacks": 0}

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		quit(1)
		return
	mode = "grand_puff"
	var width: int = int(OS.get_environment("R48_WIDTH"))
	out_dir = OS.get_environment("R48_OUT")
	if width not in [1280, 1600] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	normal_before = _normal_hashes()
	if not await _set_aspect(Vector2i(width, 720)):
		quit(1)
		return
	var profile := out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	var seed := _seed()
	var file := FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "	", true) + "\n")
	file.close()
	if not await _new_main(profile):
		await _retire_main()
		quit(1)
		return
	m._enter_level2_now(true, false, false)
	await _wait_frames(35)
	m._enter_castle_interior_now(false)
	await _wait_frames(40)
	await _capture("hall_checkpoint", "ENTRY_DIAGNOSTIC")
	if await _enter_portal():
		await _capture("boss_entry", "ENCOUNTER_CONTEXT")
		await _play()
	m._write_save()
	var ending := _snapshot()
	var normal_after := _normal_hashes()
	var report: Dictionary = {"engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "quality": String(m.save_data.get("quality", "")), "source_revision": OS.get_environment("R48_REV"), "seed": seed, "ending": ending, "states": states, "events": action_events, "errors": errors, "normal_before": normal_before, "normal_after": normal_after, "scope": "Actual production portal and pointer controls after private synthetic all-rooms-clean/seen-clips checkpoint; bot uses source oracle; no natural-earned journey/QA11/device/child/owner or true Canvas acceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "	", true) + "\n")
	output.close()
	await _retire_main()
	quit(0 if errors.is_empty() and normal_before == normal_after else 1)
