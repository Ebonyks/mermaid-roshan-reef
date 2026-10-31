extends SceneTree

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const DoorCue := preload("res://scripts/castle_door_cue.gd")

var failures := 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var completed: Array[String] = []
	for current_id: String in DoorLanguage.ACT_ONE_DESTINATIONS:
		var states: Dictionary = _act_one_states(current_id, completed, false)
		_check("one highlight while " + current_id + " is current",
			_highlight_count(states) == 1)
		_check(current_id + " is the sole rainbow plot door",
			String(states[current_id]) == DoorLanguage.PLOT
			and _highlight_id(states) == current_id)
		for completed_id: String in completed:
			_check(completed_id + " stays quiet open",
				String(states[completed_id]) == DoorLanguage.OPEN)
		var current_index: int = DoorLanguage.ACT_ONE_DESTINATIONS.find(
			current_id)
		for future_index: int in range(current_index + 1,
				DoorLanguage.ACT_ONE_DESTINATIONS.size()):
			var future_id: String = DoorLanguage.ACT_ONE_DESTINATIONS[
				future_index]
			_check(future_id + " stays fog blocked",
				String(states[future_id]) == DoorLanguage.BLOCKED)
		completed.append(current_id)

	var baby_eagle_states: Dictionary = _act_one_states(
		"playroom", ["bubble_bath", "mermaid_pool"], false)
	_check("Baby Eagle rescue is plot, never bonus",
		String(baby_eagle_states["playroom"]) == DoorLanguage.PLOT)
	_check("unrelated early rooms stay blocked",
		String(baby_eagle_states["kitchen"]) == DoorLanguage.BLOCKED
		and String(baby_eagle_states["library"]) == DoorLanguage.BLOCKED
		and String(baby_eagle_states["opera_hall"])
			== DoorLanguage.BLOCKED)

	var boss_states: Dictionary = _act_one_states("", completed, true)
	_check("boss handoff has one highlight",
		_highlight_count(boss_states) == 1)
	_check("Royal Hall becomes the sole plot door after four rooms",
		_highlight_id(boss_states) == DoorLanguage.ROYAL_HALL_ID
		and String(boss_states[DoorLanguage.ROYAL_HALL_ID])
			== DoorLanguage.PLOT)
	for completed_id: String in completed:
		_check(completed_id + " remains open at boss handoff",
			String(boss_states[completed_id]) == DoorLanguage.OPEN)

	var bonus_states: Dictionary = {}
	for destination_id: String in DoorLanguage.CASTLE_DESTINATIONS:
		bonus_states[destination_id] = DoorLanguage.resolve_act_one(
			destination_id, "mermaid_pool", ["bubble_bath"], false,
			DoorLanguage.BONUS)
	_check("optional arbitration still permits only one red highlight",
		_highlight_count(bonus_states) == 1
		and _highlight_id(bonus_states) == "mermaid_pool"
		and String(bonus_states["mermaid_pool"]) == DoorLanguage.BONUS)
	_check("bonus cue is a slow red pulse",
		DoorCue.BONUS_OUTER_COLOR.r > DoorCue.BONUS_OUTER_COLOR.g
		and DoorCue.BONUS_OUTER_COLOR.r > DoorCue.BONUS_OUTER_COLOR.b
		and DoorCue.BONUS_PERIOD_SECONDS >= 4.0)
	_check("plot cue remains slower and restrained",
		DoorCue.PLOT_PERIOD_SECONDS >= 3.0
		and DoorCue.PLOT_SHIMMER_PERIOD_SECONDS >= 4.0)

	_check("unknown direct routes fail closed",
		DoorLanguage.resolve_act_one("retired_backdoor", "bubble_bath", [],
			false) == DoorLanguage.BLOCKED)
	_check("blocked state cannot travel",
		not DoorLanguage.allows_travel(DoorLanguage.BLOCKED))
	_check("open and highlighted states can travel",
		DoorLanguage.allows_travel(DoorLanguage.OPEN)
		and DoorLanguage.allows_travel(DoorLanguage.BONUS)
		and DoorLanguage.allows_travel(DoorLanguage.PLOT))

	var cue: Control = DoorCue.new() as Control
	root.add_child(cue)
	cue.size = Vector2(180.0, 300.0)
	cue.call("set_door_state", DoorLanguage.PLOT)
	_check("plot cue is visible and input-transparent",
		cue.visible and cue.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	for frame_index in range(6):
		await process_frame
		_check("real plot cue survives process frame %d" % frame_index,
			String(cue.get("door_state")) == DoorLanguage.PLOT and cue.visible)
	cue.call("pulse_plot_feedback")
	cue.call("_process", 1.0)
	_check("story attention pulse never expires the real plot state",
		String(cue.get("door_state")) == DoorLanguage.PLOT and cue.visible)
	_check("unified cue has no legacy keyhole child",
		cue.find_child("*Keyhole*", true, false) == null
		and cue.find_child("*LockIcon*", true, false) == null)
	for family: String in ["small", "opera", "royal"]:
		cue.call("configure_physical_frame", family)
		var frame_texture: Texture2D = cue.get("frame_texture") as Texture2D
		_check(family + " physical frame texture exists", frame_texture != null)
		cue.call("set_door_state", DoorLanguage.PLOT)
		_check(family + " plot uses painted-mask shader", cue.material is ShaderMaterial)
		cue.call("pulse_plot_feedback")
		cue.call("_process", 0.1)
		var frame_material: ShaderMaterial = cue.material as ShaderMaterial
		_check(family + " feedback reaches physical shader",
			float(frame_material.get_shader_parameter("feedback_strength")) > 0.0)
	cue.call("set_door_state", DoorLanguage.BLOCKED)
	cue.call("pulse_blocked_feedback")
	_check("blocked fog cue owns local feedback",
		cue.visible and float(cue.get("feedback_time")) > 0.0)
	for attempt in range(3):
		cue.call("pulse_plot_feedback")
		cue.call("_process", 0.1)
		_check("repeated blocked feedback cannot advertise plot %d" % attempt,
			String(cue.get("door_state")) == DoorLanguage.BLOCKED
			and not DoorLanguage.allows_travel(String(cue.get("door_state"))))
	cue.call("set_door_state", DoorLanguage.PLOT)
	await process_frame
	_check("newly unlocked plot survives earlier blocked feedback",
		String(cue.get("door_state")) == DoorLanguage.PLOT and cue.visible)
	cue.call("pulse_plot_feedback")
	cue.call("set_door_state", DoorLanguage.OPEN)
	cue.call("_process", 1.0)
	_check("ordinary open has no cue", not cue.visible)
	cue.queue_free()
	await _check_hall_frame_geometry()

	var cue_source: String = FileAccess.get_file_as_string("res://scripts/castle_door_cue.gd")
	_check("no synthetic frame tracing returns",
		"_arch_points" not in cue_source and "draw_polyline" not in cue_source)

	if failures == 0:
		print("DOORLANGUAGE|ALL OK")
		quit(0)
	else:
		print("DOORLANGUAGE|FAIL|%d" % failures)
		quit(1)


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _check_hall_frame_geometry() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: Node = scene.instantiate()
	root.add_child(main)
	await _frames(3)
	main.call("_skip_intro")
	if bool(main.get("start_menu_active")):
		var menu: RefCounted = main.call("_start_menu_ref") as RefCounted
		menu.call("_dismiss_menu")
	main.call("_enter_level2_now", true, false, false)
	await _frames(4)
	main.call("_enter_castle_interior_now", false)
	await _frames(4)
	var rooms: RefCounted = main.call("_castle_rooms_ref") as RefCounted
	main.set("day_one_active", false)
	rooms.call("show_room", "main_hall", false)
	await _frames(4)
	main.process_mode = Node.PROCESS_MODE_DISABLED
	var world: Node2D = main.get("castle_room_world_root") as Node2D
	var records: Array = main.get("castle_room_door_hotspots") as Array
	var scratch: Dictionary = main.get("g") as Dictionary
	var layer: Control = scratch.get("castle_room_door_visual_layer") as Control
	_check("physical cues have a separate below-character layer",
		layer != null and layer.z_index == -950)
	_check("all nine painted doors are registered", records.size() == 9)
	var origin_position: Vector2 = world.position
	for record: Dictionary in records:
		var data: Dictionary = record["data"] as Dictionary
		var physical_cue: Control = record["cue"] as Control
		var button: Button = record["button"] as Button
		_check(String(data["id"]) + " uses its painted family below input",
			physical_cue.get_parent() == layer and button.get_parent() != layer
			and String(physical_cue.get("frame_family")) == String(data["frame_family"]))
		world.position = origin_position
		rooms.call("_update_hall_portals")
		var full_size: Vector2 = physical_cue.size
		# Put the door halfway across either viewport edge without moving input
		# or the player. The old intersection/rescale path shrank this silhouette.
		for edge: float in [0.0, 1280.0]:
			world.position.x += edge - physical_cue.position.x - full_size.x * 0.5
			rooms.call("_update_hall_portals")
			_check(String(data["id"]) + " keeps full mask at edge " + str(edge),
				physical_cue.size.is_equal_approx(full_size) and button.visible
				and button.size.x >= 112.0 and button.size.y >= 112.0)
	world.position = origin_position
	rooms.call("show_room", "bubble_bath", false)
	_check("hall mask layer hides in a room", not layer.visible)
	rooms.call("show_room", "main_hall", false)
	_check("hall mask layer returns with the hall", layer.visible)
	rooms.call("close")
	_check("teardown removes transient layer ownership",
		not scratch.has("castle_room_door_visual_layer"))
	main.queue_free()
	await _frames(3)


func _act_one_states(current_id: String, completed: Array[String],
		boss_ready: bool) -> Dictionary:
	var states: Dictionary = {}
	for destination_id: String in DoorLanguage.CASTLE_DESTINATIONS:
		states[destination_id] = DoorLanguage.resolve_act_one(
			destination_id, current_id, completed, boss_ready)
	return states


func _highlight_count(states: Dictionary) -> int:
	var count := 0
	for state_value: Variant in states.values():
		if DoorLanguage.is_highlighted(String(state_value)):
			count += 1
	return count


func _highlight_id(states: Dictionary) -> String:
	for destination_value: Variant in states.keys():
		var destination_id: String = String(destination_value)
		if DoorLanguage.is_highlighted(String(states[destination_id])):
			return destination_id
	return ""


func _check(label: String, passed: bool) -> void:
	if passed:
		print("DOORLANGUAGE|OK|" + label)
	else:
		failures += 1
		print("DOORLANGUAGE|FAIL|" + label)
