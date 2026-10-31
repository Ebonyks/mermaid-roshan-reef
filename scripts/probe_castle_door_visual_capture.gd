extends SceneTree
## Mobile-renderer visual evidence for every Castle doorway silhouette and cue.

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const OUTPUT_DIR := "res://tmp/doorframe-evidence/captures"
const TARGETS: Array[Dictionary] = [
	{"id": "opera_hall", "foot": Vector2(1025.0, 620.0),
		"family": "opera"},
	{"id": "mermaid_pool", "foot": Vector2(2415.0, 620.0),
		"family": "small"},
	{"id": "__royal_hall", "foot": Vector2(3045.0, 620.0),
		"family": "royal"},
]
const SAMPLE_TIMES: Array[float] = [0.0, 1.1, 2.2, 3.3]

var failures := 0
var output_path := ""
var capture_main: Node = null


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _check(label: String, passed: bool) -> void:
	if not passed:
		failures += 1
	print("CASTLE_DOOR_VISUAL|%s|%s" % ["OK" if passed else "FAIL", label])


func _capture(name: String) -> void:
	await _frames(2)
	var unobscured: bool = capture_main.get("_day_one_story_clip") == null \
		and not bool(capture_main.get("start_menu_active")) and not paused
	_check("uncovered live hall " + name, unobscured)
	if not unobscured:
		return
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path: String = output_path.path_join(name + ".png")
	var error: Error = image.save_png(path)
	_check("capture %s %s" % [name, image.get_size()],
		not image.is_empty() and error == OK and image.get_size() == Vector2i(1280, 720))


func _cue_for(main: Node, target_id: String) -> Control:
	var records: Array = main.get("castle_room_door_hotspots") as Array
	for value: Variant in records:
		var record: Dictionary = value as Dictionary
		var data: Dictionary = record.get("data", {}) as Dictionary
		if String(data.get("id", "")) == target_id:
			return record.get("cue") as Control
	return null


func _silence_all_cues(main: Node) -> void:
	var records: Array = main.get("castle_room_door_hotspots") as Array
	for value: Variant in records:
		var record: Dictionary = value as Dictionary
		var cue: Control = record.get("cue") as Control
		if cue != null:
			cue.call("set_door_state", DoorLanguage.OPEN)


func _apply_act_one_sequence(main: Node, current_id: String,
		completed: Array[String], boss_ready: bool) -> int:
	var highlighted := 0
	var records: Array = main.get("castle_room_door_hotspots") as Array
	for value: Variant in records:
		var record: Dictionary = value as Dictionary
		var data: Dictionary = record.get("data", {}) as Dictionary
		var portal_id: String = String(data.get("id", ""))
		var state: String = DoorLanguage.resolve_act_one(
			portal_id, current_id, completed, boss_ready)
		var cue: Control = record.get("cue") as Control
		if cue != null:
			cue.call("set_door_state", state)
			cue.call("_sync_material")
			cue.queue_redraw()
		if DoorLanguage.is_highlighted(state):
			highlighted += 1
	return highlighted


func _capture_act_one_sequence(main: Node, rooms: RefCounted) -> void:
	var completed: Array[String] = []
	for beat_index: int in range(DoorLanguage.ACT_ONE_DESTINATIONS.size()):
		var current_id: String = DoorLanguage.ACT_ONE_DESTINATIONS[beat_index]
		var target_foot := Vector2(2415.0, 620.0)
		var records: Array = main.get("castle_room_door_hotspots") as Array
		for value: Variant in records:
			var record: Dictionary = value as Dictionary
			var data: Dictionary = record.get("data", {}) as Dictionary
			if String(data.get("id", "")) == current_id:
				target_foot = data.get("foot", target_foot) as Vector2
				break
		main.process_mode = Node.PROCESS_MODE_INHERIT
		rooms.call("_position_hall_player_at_foot", target_foot, false)
		await create_timer(1.5).timeout
		rooms.call("_update_hall_portals")
		main.process_mode = Node.PROCESS_MODE_DISABLED
		var highlight_count: int = _apply_act_one_sequence(
			main, current_id, completed, false)
		_check("one visual highlight at Act One beat %d" % (beat_index + 1),
			highlight_count == 1)
		_check_target_visible(main, current_id)
		await _capture("sequence_beat_%02d_%s" % [
			beat_index + 1, current_id])
		completed.append(current_id)
	main.process_mode = Node.PROCESS_MODE_INHERIT
	rooms.call("_position_hall_player_at_foot", Vector2(3045.0, 620.0), false)
	await create_timer(1.5).timeout
	rooms.call("_update_hall_portals")
	main.process_mode = Node.PROCESS_MODE_DISABLED
	var boss_highlights: int = _apply_act_one_sequence(
		main, "", completed, true)
	_check("one visual highlight at Royal Hall handoff", boss_highlights == 1)
	_check_target_visible(main, DoorLanguage.ROYAL_HALL_ID)
	await _capture("sequence_beat_05_royal_hall")


func _capture_target(main: Node, rooms: RefCounted,
		target: Dictionary) -> void:
	var target_id: String = String(target["id"])
	main.process_mode = Node.PROCESS_MODE_INHERIT
	rooms.call("_position_hall_player_at_foot",
		target["foot"] as Vector2, false)
	await create_timer(1.5).timeout
	rooms.call("_update_hall_portals")
	await _frames(2)
	main.process_mode = Node.PROCESS_MODE_DISABLED
	_silence_all_cues(main)
	var cue: Control = _cue_for(main, target_id)
	_check("cue exists " + target_id, cue != null)
	if cue == null:
		return
	_check_target_visible(main, target_id)
	_check("frame family " + target_id,
		String(cue.get("frame_family")) == String(target["family"]))
	var stable_size: Vector2 = cue.size
	for state: String in [
		DoorLanguage.BLOCKED, DoorLanguage.BONUS, DoorLanguage.PLOT]:
		for sample_index: int in range(SAMPLE_TIMES.size()):
			cue.call("set_door_state", state)
			cue.set("motion_time", SAMPLE_TIMES[sample_index])
			cue.call("_sync_material")
			cue.queue_redraw()
			await _capture("%s_%s_%02d" % [
				target_id.trim_prefix("__"), state, sample_index])
		cue.call("set_door_state", DoorLanguage.OPEN)
	_check("full cue size remained stable " + target_id,
		cue.size.is_equal_approx(stable_size))


func _check_target_visible(main: Node, target_id: String) -> void:
	var cue: Control = _cue_for(main, target_id)
	var rect: Rect2 = cue.get_global_rect()
	var clipped: Rect2 = rect.intersection(Rect2(0.0, 0.0, 1280.0, 720.0))
	_check("target is on screen " + target_id,
		clipped.get_area() >= rect.get_area() * 0.95)


func _run() -> void:
	output_path = ProjectSettings.globalize_path(OUTPUT_DIR)
	var dir_error: Error = DirAccess.make_dir_recursive_absolute(output_path)
	_check("output directory", dir_error == OK)
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: Node = scene.instantiate()
	capture_main = main
	root.add_child(main)
	await _frames(2)
	if bool(main.get("start_menu_active")):
		var start_menu: RefCounted = main.call("_start_menu_ref") as RefCounted
		if start_menu != null:
			start_menu.call("_dismiss_menu")
	main.call("_launch_from_start_menu", false)
	if bool(main.get("intro_active")):
		main.call("_skip_intro")
	for _skip: int in range(8):
		var clip: Node = main.get("_day_one_story_clip") as Node
		if clip == null:
			break
		clip.call("skip")
		await _frames(2)
	main.set("day_one_active", false)
	main.call("_apply_quality", "speedy")
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(1280, 720)
	_check("Mobile renderer", RenderingServer.get_current_rendering_method() == "mobile")
	await _frames(3)
	main.set("pearl_count", 10)
	for friend_value: Variant in main.get("friends") as Array:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.set("trophies", 5)
	main.set("level2_done_once", true)
	main.call("_enter_level2_now", true, false, false)
	await _frames(12)
	main.call("_enter_castle_interior_now", false)
	await _frames(18)
	var rooms: RefCounted = main.call("_castle_rooms_ref") as RefCounted
	_check("Castle controller", rooms != null)
	if rooms != null:
		rooms.call("show_room", "main_hall", false)
		await _frames(10)
		# Let the real narration caption expire before freezing timed cue fixtures.
		await create_timer(maxf(float(main.get("msg_timer")) + 0.3, 0.3)).timeout
		await _frames(2)
		await _capture("live_hall_before_resolver_fixtures")
		await _capture_act_one_sequence(main, rooms)
		for target: Dictionary in TARGETS:
			await _capture_target(main, rooms, target)
	main.queue_free()
	await _frames(3)
	print("CASTLE_DOOR_VISUAL|DONE|failures=%d|output=%s" % [
		failures, output_path])
	quit(1 if failures > 0 else 0)


func _init() -> void:
	call_deferred("_run")
