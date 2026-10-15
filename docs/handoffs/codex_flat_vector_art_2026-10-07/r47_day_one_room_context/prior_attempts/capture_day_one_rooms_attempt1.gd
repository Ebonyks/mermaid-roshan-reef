extends SceneTree
## R47 original Day One scene/current pointer actions from private saved checkpoints.
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
	var studio: DayOneArtStudio = m._day_one_art_studio
	return {"game": m.game, "room": m.castle_room_id, "director": m._day_one_ref().serialize_state(), "companion": m.companion_id, "stuffie_wins": m.stuffie_wins.duplicate(), "art_studio": studio.audit_snapshot() if studio != null and is_instance_valid(studio) else {}, "art_contact_active": studio._contact_action.active if studio != null and is_instance_valid(studio) and studio._contact_action != null else false, "attack_customizer_open": m._attack_customizer != null and is_instance_valid(m._attack_customizer) and m._attack_customizer.is_open, "companion_picker_open": m.companion_layer != null and is_instance_valid(m.companion_layer), "story_clip_open": m._day_one_story_clip != null and is_instance_valid(m._day_one_story_clip), "normal_entry_scope": "Private saved checkpoint to hall; actual pointer door/action events, not full natural journey/QA11 or acceptance"}

func _capture(id: String, role: String) -> void:
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != get_root().size or image.save_png(path) != OK:
		errors.append("native capture failed " + id)
		return
	var rows: Array[Dictionary] = []
	_nodes(m, rows)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path), "width": image.get_width(), "height": image.get_height(), "role": role, "snapshot": _snapshot(), "nodes": rows, "presentation": _presentation(), "last_event": action_events.back() if not action_events.is_empty() else {}})
	print("DAYONE47|CAPTURE|" + mode + "|" + id)

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

func _tap_control(control: Control, label: String) -> bool:
	if control == null or not is_instance_valid(control) or not control.is_visible_in_tree():
		errors.append("unavailable actual control " + label)
		return false
	var point: Vector2 = control.get_global_transform_with_canvas() * (control.size * 0.5)
	if not Rect2(Vector2.ZERO, Vector2(get_root().size)).has_point(point):
		errors.append("offscreen actual control " + label + str(point))
		return false
	await _pointer(true, point)
	await _pointer(false, point)
	return true

func _find_button(name: String) -> Button:
	return m.find_child(name, true, false) as Button

func _door(room: String) -> bool:
	for attempt: int in range(15):
		var button := _find_button("HallDoor_" + room)
		if button == null or not button.is_visible_in_tree():
			errors.append("actual hall door unavailable " + room)
			return false
		var point: Vector2 = button.get_global_transform_with_canvas() * (button.size * 0.5)
		if point.x > 35.0 and point.x < float(get_root().size.x) - 35.0 and point.y > 20.0 and point.y < 700.0:
			if not await _tap_control(button, "HallDoor_" + room):
				return false
			for i: int in range(600):
				await process_frame
				if m.castle_room_id == room:
					await _wait_frames(30)
					return true
			errors.append("actual hall door did not enter " + room)
			return false
		var walk_point := Vector2(float(get_root().size.x) * (0.84 if point.x > 0.0 else 0.16), 650.0)
		await _pointer(true, walk_point)
		await _pointer(false, walk_point)
		await _wait_frames(90)
	errors.append("door not reached in bounded actual walking " + room)
	return false

func _rescue() -> void:
	for id: String in ["eagle_pin_left", "eagle_pin_right"]:
		var record: Dictionary = m.castle_room_item_sprites.get(id, {}) as Dictionary
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		if sprite == null:
			errors.append("rescue pin absent " + id)
			return
		var point: Vector2 = sprite.get_global_transform_with_canvas() * Vector2.ZERO
		await _pointer(true, point)
		await _capture(id + "_pressed", "ROOM_ACTION_CONTEXT")
		await _pointer(false, point)
		await _wait_frames(3)
		await _capture(id + "_release", "ROOM_ACTION_CONTEXT")
		await _wait_frames(18)
		await _capture(id + "_settle", "ROOM_ACTION_CONTEXT")
		if not bool(m.stuffie_wins.get("rescued_" + id, false)):
			errors.append("real pointer failed rescue pin " + id)
			return
	await _wait_frames(60)
	await _capture("rescue_offer", "ROOM_ACTION_CONTEXT")
	if not bool(m.stuffie_wins.get("rescued_eagle", false)):
		errors.append("two real pins did not rescue Eagle")
		return
	var card := _find_button("StuffieCard_eagle")
	if not await _tap_control(card, "StuffieCard_eagle"):
		return
	await _wait_frames(6)
	await _capture("eagle_choice", "OVERLAY_DIAGNOSTIC")
	if not await _tap_control(_find_button("StuffieConfirmButton"), "StuffieConfirmButton"):
		return
	await _wait_frames(55)
	await _capture("adopted_checkpoint", "ROOM_ACTION_CONTEXT")
	if m.companion_layer != null or m.companion_care_layer != null:
		await _tap_control(m.global_navigation_button, "GlobalNavigationButton close companion")
		await _wait_frames(15)
	await _capture("rescue_room_after_offer", "ROOM_ACTION_CONTEXT")

func _art() -> void:
	for kind: String in ["material", "grime"]:
		var ids: Array[String] = DayOneDirector.ART_MATERIAL_IDS if kind == "material" else DayOneDirector.ART_GRIME_IDS
		for id: String in ids:
			var button := _find_button(("Collect_" if kind == "material" else "Scrub_") + id)
			if button == null or not button.is_visible_in_tree():
				errors.append("cleanup target absent " + kind + id)
				return
			var point: Vector2 = button.get_global_transform_with_canvas() * (button.size * 0.5)
			await _pointer(true, point)
			await _capture(kind + "_" + id + "_pressed", "ROOM_ACTION_CONTEXT")
			await _pointer(false, point)
			await _wait_frames(12)
			await _capture(kind + "_" + id + "_contact", "ROOM_ACTION_CONTEXT")
			var finished := false
			for i: int in range(600):
				await process_frame
				var collected: Dictionary = m.day_one_art_collected_materials if kind == "material" else m.day_one_art_cleaned_grime
				if bool(collected.get(id, false)):
					finished = true
					break
			if not finished:
				errors.append("real cleanup pointer did not progress " + kind + id)
				return
			await _capture(kind + "_" + id + "_changed", "ROOM_ACTION_CONTEXT")
			await _wait_frames(20)
	await _capture("desk_unlocked", "ROOM_ACTION_CONTEXT")
	if not await _tap_control(_find_button("OpenPaintDesk"), "OpenPaintDesk"):
		return
	await _wait_frames(12)
	await _capture("desk_customizer", "OVERLAY_DIAGNOSTIC")
	if not await _tap_control(_find_button("AttackCustomizerConfirm"), "AttackCustomizerConfirm"):
		return
	await _wait_frames(60)
	await _capture("art_complete_room", "ROOM_ACTION_CONTEXT")
	if not m._day_one_ref().is_room_completed("art"):
		errors.append("actual desk confirmation did not complete art")

func _seed() -> Dictionary:
	var completed: Array[String] = ["bathroom", "pool"]
	if mode == "art":
		completed.append("stuffie")
	var seen: Dictionary = {}
	for clip: String in DayOneStoryClips.clip_ids():
		seen[clip] = true
	return {"schema_version": 1, "won": {}, "found": {}, "plays": 3, "pearls": 23, "pearls_ever": 23, "music": false, "mic": false, "quality": "speedy", "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": [], "day_one_active": true, "day_one_current_room": "art" if mode == "art" else "stuffie", "day_one_completed_rooms": completed, "day_one_cleaned_rooms": completed, "day_one_arrival_plane_media_seen": true, "day_one_dirty_castle_discovered": true, "day_one_grok_video_2_seen": true, "day_one_story_clips_seen": seen, "companion": "eagle" if mode == "art" else "", "stuffie_wins": {"rescued_eagle": true, "rescued_eagle_pin_left": true, "rescued_eagle_pin_right": true} if mode == "art" else {}}

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		quit(1)
		return
	mode = OS.get_environment("R47_MODE")
	var width: int = int(OS.get_environment("R47_WIDTH"))
	out_dir = OS.get_environment("R47_OUT")
	if mode not in ["rescue", "art"] or width not in [1280, 1600] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	normal_before = _normal_hashes()
	if not await _set_aspect(Vector2i(width, 720)):
		quit(1)
		return
	var seed := _seed()
	var profile := out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	var seed_file := FileAccess.open(profile, FileAccess.WRITE)
	seed_file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	seed_file.close()
	if not await _new_main(profile):
		await _retire_main()
		quit(1)
		return
	var room := "craft_room" if mode == "art" else "playroom"
	m._enter_level2_now(true, false, false)
	await _wait_frames(35)
	m._enter_castle_interior_now(false)
	await _wait_frames(40)
	await _capture("hall_checkpoint", "ENTRY_DIAGNOSTIC")
	var entered: bool = await _door(room)
	if entered:
		await _capture("room_ready", "ROOM_ACTION_CONTEXT")
		await _wait_frames(60)
		await _capture("room_passive", "ROOM_ACTION_CONTEXT")
		m._pause_ref().toggle_pause()
		await _wait_frames(3)
		await _capture("room_pause", "PAUSE_DIAGNOSTIC")
		m._pause_ref().toggle_pause()
		await _wait_frames(8)
		await _capture("room_resumed", "ROOM_ACTION_CONTEXT")
		if mode == "rescue":
			await _rescue()
		else:
			await _art()
	var before_reload := _snapshot()
	m._write_save()
	await _retire_main()
	if errors.is_empty() and await _new_main(profile):
		m._enter_level2_now(true, false, false)
		await _wait_frames(30)
		m._enter_castle_interior_now(false)
		await _wait_frames(30)
		await _capture("reload_hall", "RELOAD_DIAGNOSTIC")
		if await _door(room):
			await _capture("reload_reentry", "ROOM_ACTION_CONTEXT")
		await _retire_main()
	if _normal_hashes() != normal_before:
		errors.append("normal save artifacts changed")
	var report: Dictionary = {"schema": "reef.day_one_room_context/1", "source_revision": OS.get_environment("R47_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "quality": "speedy", "mode": mode, "aspect": [width, 720], "states": states, "seed": seed, "before_reload": before_reload, "events": action_events, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "full_natural_journey_proved": false, "actual_child_data": false, "scope": "Private saved-state checkpoint to hall through production API; actual live door/pointer actions thereafter. No progress/timing/target writes after seed. Sparse states,not full motion/QA11/device/child/owner or art acceptance. All prior-room/seen-clip/companion flags explicitly synthetic."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t", true) + "\n")
	file.close()
	print("DAYONE47|RESULT|" + ("PASS" if errors.is_empty() else "FAIL") + "|" + str(errors))
	quit(0 if errors.is_empty() else 1)
