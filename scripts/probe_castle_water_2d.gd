extends SceneTree

# End-to-end trial gate for the first two true-Canvas wet rooms.

const EXPECTED_POOL_FIXTURES: Array[String] = [
	"flower_float", "seahorse_fountain", "star_float", "waterfall",
]

var main: ReefMain
var failed := 0


func _check(label: String, condition: bool, detail: String = "") -> void:
	if not condition:
		failed += 1
	print("CASTLE_WATER_2D|", label, ": ", "OK" if condition else "FAIL",
		" " + detail if detail != "" else "")


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _tick_frames(rooms: CastleRooms25D, count: int) -> void:
	for _index in range(count):
		rooms.tick(1.0 / 60.0)
		await process_frame


func _capture(label: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var output_dir := OS.get_environment("CASTLE_WATER_SHOT_OUT")
	if output_dir == "":
		return
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute(output_dir)
	var output_path := output_dir.path_join(label + ".png")
	var save_error := root.get_viewport().get_texture().get_image() \
		.save_png(output_path)
	print("CASTLE_WATER_2D|capture=", output_path, " error=", save_error)


func _fixture_ids(rooms: CastleRooms25D) -> Array[String]:
	var ids: Array[String] = []
	for item_id_value: Variant in rooms.wet_rooms.fixture_sprites.keys():
		ids.append(String(item_id_value))
	ids.sort()
	return ids


func _canvas_descendants_only(node: Node) -> bool:
	for child: Node in node.get_children():
		if not (child is CanvasItem or child is CanvasLayer \
				or child is AudioStreamPlayer or child.get_class() == "Node"):
			return false
		if not _canvas_descendants_only(child):
			return false
	return true


func _run() -> void:
	var main_scene := load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	main.set_process(false)
	await process_frame
	main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(16)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("mermaid_pool", false)
	await _tick_frames(rooms, 4)

	var wet_root := rooms.wet_rooms.root
	_check("pool owns one Canvas root", wet_root != null
		and wet_root is Node2D
		and String(wet_root.get_meta("water_trial_room", ""))
			== "mermaid_pool")
	_check("wet root contains only Canvas presentation", wet_root != null
		and _canvas_descendants_only(wet_root))
	_check("pool exact source-owned fixture roster",
		_fixture_ids(rooms) == EXPECTED_POOL_FIXTURES,
		"runtime=%s" % [_fixture_ids(rooms)])
	var pool_stats: Dictionary = rooms.wet_rooms.stats()
	_check("pool four manifest water layers",
		int(pool_stats.get("fixture_count", 0)) == 4
		and int(pool_stats.get("water_layers", 0)) == 4
		and bool(pool_stats.get("canvas_only", false)))
	_check("pool uses complete healed tile route",
		int(main.g.get("castle_wet_room_background_tiles", 0)) == 8)
	_check("pool allocates no Jolt fixture bodies",
		main.castle_room_fixture_physics.is_empty()
		and main.castle_room_fixture_rigs.is_empty())

	var water_timelines_ok := true
	for item_id: String in EXPECTED_POOL_FIXTURES:
		var water: CastleWaterFixture2D = rooms.wet_rooms.fixture_water.get(
			item_id) as CastleWaterFixture2D
		water_timelines_ok = water_timelines_ok and water != null
		if water == null:
			continue
		rooms.wet_rooms.apply_fixture_frame(item_id, 3, 9, 3)
		water_timelines_ok = water_timelines_ok \
			and int(water.stats().get("active_layers", 0)) == 1
		rooms.wet_rooms.apply_fixture_frame(item_id, 0, 9, 0)
		water_timelines_ok = water_timelines_ok \
			and int(water.stats().get("active_layers", -1)) == 0
	_check("authored pool water appears only on declared frames",
		water_timelines_ok)

	var fountain := rooms.wet_rooms.fixture_sprite("seahorse_fountain")
	rooms._activate_room_item("seahorse_fountain")
	var interaction_started := fountain != null \
		and bool(fountain.get_meta("busy", false))
	var interaction_deadline := Time.get_ticks_msec() + 3000
	while fountain != null and bool(fountain.get_meta("busy", false)) \
			and Time.get_ticks_msec() < interaction_deadline:
		rooms.tick(1.0 / 60.0)
		await process_frame
	var visited: Array = fountain.get_meta(
		"animation_frames_visited", []) as Array if fountain != null else []
	_check("fountain plays exact authored action and resets",
		interaction_started and fountain != null
		and Time.get_ticks_msec() < interaction_deadline
		and visited == [0, 1, 2, 3, 4, 5, 6, 7, 0]
		and fountain.frame == 0
		and not bool(fountain.get_meta("busy", true)),
		"visited=%s frame=%d busy=%s" % [
			visited, fountain.frame if fountain != null else -1,
			bool(fountain.get_meta("busy", true)) if fountain != null else true])

	rooms.wet_rooms.move_player(Vector2(640.0, 550.0))
	await _tick_frames(rooms, 70)
	await _capture("pool_shallow_wade")
	_check("pool shore resolves to tail-supported wade",
		String(rooms.wet_rooms.stats().get("medium_state", ""))
			== "SHALLOW_WADE"
		and rooms.wet_rooms.actor_front_water.visible
		and rooms.wet_rooms.actor_shadow.visible)
	rooms.wet_rooms.move_player(Vector2(640.0, 420.0))
	await _tick_frames(rooms, 80)
	await _capture("pool_surface_swim")
	var surface_state := String(
		rooms.wet_rooms.stats().get("medium_state", ""))
	var actor_height := 256.0 * rooms.wet_rooms.actor.scale.y
	var actor_top := rooms.wet_rooms.actor.position.y - actor_height * 0.5
	var waterline_y := rooms.wet_rooms.actor_waterline.points[0].y \
		if rooms.wet_rooms.actor_waterline.points.size() > 0 else -INF
	_check("deep pool resolves to readable surface swim",
		surface_state == "SURFACE_SWIM"
		and rooms.wet_rooms.actor_front_water.visible
		and not rooms.wet_rooms.actor_shadow.visible
		and waterline_y > actor_top + actor_height * 0.32,
		"state=%s waterline=%.2f face_gate=%.2f" % [
			surface_state, waterline_y, actor_top + actor_height * 0.32])

	rooms.wet_rooms.move_player(Vector2(640.0, 650.0))
	await _tick_frames(rooms, 90)
	_check("pool exit returns to dry without a stuck mask",
		String(rooms.wet_rooms.stats().get("medium_state", "")) == "DRY"
		and not rooms.wet_rooms.actor_front_water.visible
		and rooms.wet_rooms.actor_shadow.visible)
	var event_total := int((rooms.wet_rooms.stats().get(
		"fx", {}) as Dictionary).get("emitted_total", 0))
	await _tick_frames(rooms, 120)
	_check("passive pool creates no new contact events",
		int((rooms.wet_rooms.stats().get(
			"fx", {}) as Dictionary).get("emitted_total", -1)) == event_total)

	var first_root_id := wet_root.get_instance_id()
	rooms.show_room("bubble_bath", false)
	await _tick_frames(rooms, 4)
	await _capture("bubble_bath_dry")
	rooms.show_room("mermaid_pool", false)
	await _tick_frames(rooms, 4)
	var root_count := 0
	for child: Node in main.castle_room_stage.get_children():
		if child.name.begins_with("CastleWetRoom2D_"):
			root_count += 1
	_check("room switch and re-entry replace rather than duplicate the host",
		rooms.wet_rooms.root.get_instance_id() != first_root_id
		and root_count == 1, "root_count=%d" % root_count)

	print("CASTLE_WATER_2D|RESULT=", "FAIL" if failed > 0 else "OK",
		" failures=", failed)
	quit(1 if failed > 0 else 0)


func _init() -> void:
	call_deferred("_run")
