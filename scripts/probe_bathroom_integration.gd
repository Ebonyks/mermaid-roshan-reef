extends SceneTree
# Focused live-world audit for the Bubble Bath room. The room is a layered
# Sprite2D Canvas stage: four retained source-owned fixtures plus any audited native
# V4 fixtures are separate world cards with projected touch targets, semantic
# atlas animations, and sounds. No modeled bathroom or V3 prop pack may return.

const V4_MANIFEST_PATH := \
	"res://assets/flats/castle/interactions_v4/castle_interactions_v4.json"
const RETAINED_PROP_EXPECTATIONS := {
	"bathtub": {
		"semantic_action": "turn_taps_and_fill_bubbles",
		"sound": "res://assets/audio/castle/bubble_water.ogg",
		"runtime_sound": "castle/bubble_water.ogg",
		"pack": "v2_base",
	},
	"sink": {
		"semantic_action": "turn_faucet_and_run_water",
		"sound": "res://assets/audio/castle/faucet_water.ogg",
		"runtime_sound": "castle/faucet_water.ogg",
		"pack": "v2_base",
	},
	"toilet": {
		"semantic_action": "flap_seat_and_flush",
		"sound": "res://assets/audio/castle/toilet_flush.ogg",
		"runtime_sound": "castle/toilet_flush.ogg",
		"pack": "v2_base",
	},
	"rubber_duck": {
		"semantic_action": "squeak_dive_and_pop_up",
		"sound": "res://assets/audio/castle/duck_squeak.ogg",
		"runtime_sound": "castle/duck_squeak.ogg",
		"pack": "v2_base",
	},
}

var main: ReefMain
var checks_failed := 0
var v4_manifest_contract_ok := true
var v4_manifest_contract_detail := ""


func _expected_props() -> Dictionary:
	var expectations: Dictionary = RETAINED_PROP_EXPECTATIONS.duplicate(true)
	if not FileAccess.file_exists(V4_MANIFEST_PATH):
		return expectations
	var parsed_value: Variant = JSON.parse_string(
		FileAccess.get_file_as_string(V4_MANIFEST_PATH))
	if not parsed_value is Dictionary:
		v4_manifest_contract_ok = false
		v4_manifest_contract_detail = "V4 manifest is not a Dictionary"
		return expectations
	var parsed: Dictionary = parsed_value as Dictionary
	if not parsed.has("assets"):
		return expectations
	var assets_value: Variant = parsed.get("assets", [])
	if not assets_value is Array:
		v4_manifest_contract_ok = false
		v4_manifest_contract_detail = "V4 assets is not an Array"
		return expectations
	var background_routes: Dictionary = parsed.get(
		"runtime_background_tiles", {}) as Dictionary
	var v4_ids: Dictionary = {}
	for asset_value: Variant in assets_value as Array:
		if not asset_value is Dictionary:
			v4_manifest_contract_ok = false
			v4_manifest_contract_detail = "V4 assets contains a non-Dictionary"
			continue
		var asset: Dictionary = asset_value as Dictionary
		var pack: String = String(asset.get("pack", ""))
		if pack == "v3_addition":
			v4_manifest_contract_ok = false
			v4_manifest_contract_detail = "V4 registry contains pack:v3_addition"
			continue
		if pack != "v4_native" \
				or String(asset.get("room", "")) != "bubble_bath":
			continue
		var instances: Array = asset.get("instances", []) as Array
		var ownership: Dictionary = asset.get(
			"source_ownership", {}) as Dictionary
		var behavior: Dictionary = asset.get(
			"animation_behavior", {}) as Dictionary
		var semantic_action: String = String(asset.get("semantic_action", ""))
		var valid: bool = instances.size() == 1 \
			and bool(ownership.get("passed", false)) \
			and bool(ownership.get("verified", false)) \
			and bool(ownership.get("background_healed", false)) \
			and bool(ownership.get("duplicate_pixels_removed", false)) \
			and (ownership.get("source_rect", []) as Array).size() == 4 \
			and String(behavior.get("mode", "")) \
				== "authored_object_states" \
			and String(behavior.get("action", "")) == semantic_action \
			and not bool(behavior.get("generic_transform_fallback", true)) \
			and semantic_action != "" \
			and String(asset.get("render_mode", "")) \
				== "generated_full_object_states" \
			and not bool(asset.get("primary_animation_is_overlay", true))
		if not valid:
			v4_manifest_contract_ok = false
			v4_manifest_contract_detail = \
				"Bubble Bath V4 entry lacks audited ownership/action"
			continue
		var prop_id: String = String(instances[0])
		if prop_id == "" or v4_ids.has(prop_id):
			v4_manifest_contract_ok = false
			v4_manifest_contract_detail = "duplicate or empty Bubble Bath V4 id"
			continue
		v4_ids[prop_id] = true
		var authored_count := int(asset.get("authored_frame_count", 0))
		var timeline: Array = asset.get("timeline_sequence", []) as Array
		if authored_count == 0:
			var pending_ok: bool = String(asset.get("delivery_status", "")) \
				== "ownership_ready_authored_states_pending" \
				and int(asset.get("timeline_frame_count", -1)) == 0 \
				and timeline.is_empty() and asset.get("sheet") == null
			if not pending_ok:
				v4_manifest_contract_ok = false
				v4_manifest_contract_detail = \
					"Bubble Bath V4 pending entry has partial runtime delivery"
			continue
		var sound_path: String = String(asset.get("sound", ""))
		var grid: Array = asset.get("grid", []) as Array
		var runtime_ready: bool = authored_count >= 4 and authored_count <= 12 \
			and timeline.size() >= 4 and timeline.size() <= 12 \
			and int(asset.get("timeline_frame_count", -1)) == timeline.size() \
			and grid.size() == 2 \
			and int(grid[0]) * int(grid[1]) >= authored_count \
			and sound_path != "" and asset.get("sheet") != null \
			and background_routes.has("bubble_bath")
		if not runtime_ready:
			v4_manifest_contract_ok = false
			v4_manifest_contract_detail = \
				"Bubble Bath V4 runtime entry is incomplete"
			continue
		var resource_sound := sound_path
		if not resource_sound.begins_with("res://"):
			resource_sound = "res://" + resource_sound \
				if resource_sound.begins_with("assets/audio/") \
				else "res://assets/audio/" + resource_sound
		if not ResourceLoader.exists(resource_sound):
			v4_manifest_contract_ok = false
			v4_manifest_contract_detail = "Bubble Bath V4 audio is missing"
			continue
		expectations[prop_id] = {
			"semantic_action": semantic_action,
			"sound": resource_sound,
			"runtime_sound": resource_sound.trim_prefix(
				"res://assets/audio/"),
			"pack": "v4_native",
		}
	return expectations

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("BATHROOM_WORLD|", label, ": ", ("OK" if ok else "FAIL"),
		(" " + detail if detail != "" else ""))

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _room_click(rooms: CastleRooms25D, position: Vector2) -> void:
	var press := InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_LEFT
	press.position = position
	press.pressed = true
	rooms._on_room_input(press)
	await process_frame
	var release := InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_LEFT
	release.position = position
	release.pressed = false
	rooms._on_room_input(release)
	await process_frame

func _room_drag(rooms: CastleRooms25D, start: Vector2,
		finish: Vector2) -> void:
	var press := InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_LEFT
	press.position = start
	press.pressed = true
	rooms._on_room_input(press)
	await process_frame
	var motion := InputEventMouseMotion.new()
	motion.position = finish
	motion.relative = finish - start
	motion.button_mask = MOUSE_BUTTON_MASK_LEFT
	rooms._on_room_input(motion)
	await process_frame
	var release := InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_LEFT
	release.position = finish
	release.pressed = false
	rooms._on_room_input(release)
	await process_frame

func _touch(rooms: CastleRooms25D, index: int, position: Vector2,
		pressed: bool, canceled: bool = false) -> void:
	var touch := InputEventScreenTouch.new()
	touch.index = index
	touch.position = position
	touch.pressed = pressed
	touch.canceled = canceled
	rooms._on_room_input(touch)

func _touch_drag(rooms: CastleRooms25D, index: int, start: Vector2,
		finish: Vector2) -> void:
	_touch(rooms, index, start, true)
	await process_frame
	var drag := InputEventScreenDrag.new()
	drag.index = index
	drag.position = finish
	drag.relative = finish - start
	rooms._on_room_input(drag)
	await process_frame

func _stage_screen_position(stage_position: Vector2) -> Vector2:
	return main.castle_room_stage.get_global_transform_with_canvas() \
		* stage_position

func _navigation_point_is_clear(snapshot: Dictionary,
		point: Vector2) -> bool:
	var stage_bounds: Rect2 = snapshot.get("stage_bounds", Rect2()) as Rect2
	if not stage_bounds.has_point(point):
		return false
	for blocker_value: Variant in snapshot.get("body_footprints", []) as Array:
		var blocker: Dictionary = blocker_value as Dictionary
		var body_rect: Rect2 = blocker.get("rect", Rect2()) as Rect2
		if body_rect.has_point(point):
			return false
	return true

func _check_authored_navigation_geometry(rooms: CastleRooms25D,
		room_id: String) -> void:
	var snapshot: Dictionary = rooms.navigation_snapshot()
	var lanes: Array = snapshot.get("lanes", []) as Array
	var backgrounds: Array = snapshot.get("backgrounds", []) as Array
	var export_seam_ok := not backgrounds.is_empty()
	for background_value: Variant in backgrounds:
		var background: Dictionary = background_value as Dictionary
		export_seam_ok = export_seam_ok \
			and String(background.get("texture_path", "")) != "" \
			and background.get("source_art_rect") is Rect2 \
			and background.get("render_art_rect") is Rect2
	var geometry_ok := bool(snapshot.get("authored_lanes", false)) \
		and String(snapshot.get("room_id", "")) == room_id \
		and lanes.size() >= 4
	for lane_value: Variant in lanes:
		var lane: PackedVector2Array = lane_value as PackedVector2Array
		for index: int in range(1, lane.size()):
			for sample_index: int in range(41):
				var point := lane[index - 1].lerp(
					lane[index], float(sample_index) / 40.0)
				geometry_ok = geometry_ok \
					and _navigation_point_is_clear(snapshot, point)
	var contacts_ok := true
	for item_value: Variant in snapshot.get("items", []) as Array:
		var item: Dictionary = item_value as Dictionary
		var route_contact: Vector2 = item.get(
			"route_contact", Vector2.INF) as Vector2
		contacts_ok = contacts_ok and route_contact.is_finite() \
			and rooms._room_navigation.contains_point(route_contact, 0.1) \
			and _navigation_point_is_clear(snapshot, route_contact)
	_ck("%s authored lanes stay in stage and clear fixture bodies" % room_id,
		geometry_ok)
	_ck("%s item approaches resolve onto authored lanes" % room_id,
		contacts_ok)
	_ck("%s navigation snapshot carries atlas source geometry" % room_id,
		export_seam_ok and snapshot.get("stage_bounds") is Rect2 \
		and snapshot.get("body_footprints") is Array)

func _exercise_bathtub_approach(rooms: CastleRooms25D) -> void:
	var record: Dictionary = main.castle_room_item_sprites.get(
		"bathtub", {}) as Dictionary
	var sprite: Sprite2D = record.get("sprite") as Sprite2D
	var hotspot: Button = record.get("hotspot") as Button
	var target: Vector2 = record.get("route_contact", Vector2.INF) as Vector2
	rooms._position_player_at_foot(Vector2(640.0, 650.0), false)
	main.castle_room_prop_sfx.stop()
	main.castle_room_prop_sfx.stream = null
	hotspot.pressed.emit()
	await _frames(2)
	_ck("live bathtub hotspot starts an approach",
		bool(main.castle_room_player_sprite.get_meta("walking", false)))
	_ck("bathtub action waits while Roshan approaches",
		not bool(sprite.get_meta("busy", false))
		and main.castle_room_prop_sfx.stream == null)
	var samples_clear := true
	var no_early_action := true
	var deadline_ms := Time.get_ticks_msec() + 5000
	while bool(main.castle_room_player_sprite.get_meta("walking", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame
		var foot: Vector2 = main.castle_room_player_sprite.get_meta(
			"current_stage_foot", Vector2.INF) as Vector2
		samples_clear = samples_clear \
			and rooms._room_navigation.contains_point(foot, 0.1) \
			and _navigation_point_is_clear(rooms.navigation_snapshot(), foot)
		if bool(main.castle_room_player_sprite.get_meta("walking", false)):
			no_early_action = no_early_action \
				and not bool(sprite.get_meta("busy", false))
	_ck("every bathtub interpolation sample stays on clear authored floor",
		samples_clear and Time.get_ticks_msec() < deadline_ms)
	var arrived_foot: Vector2 = main.castle_room_player_sprite.get_meta(
		"current_stage_foot", Vector2.INF) as Vector2
	_ck("bathtub action begins only at its approach socket",
		no_early_action and arrived_foot.distance_to(target) <= 1.0 \
		and bool(sprite.get_meta("busy", false)))
	deadline_ms = Time.get_ticks_msec() + 4000
	while bool(sprite.get_meta("busy", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame

	# A second real floor tap must cancel both the route and its queued action.
	rooms._position_player_at_foot(Vector2(640.0, 650.0), false)
	main.castle_room_prop_sfx.stop()
	main.castle_room_prop_sfx.stream = null
	hotspot.pressed.emit()
	await _frames(2)
	await _room_click(rooms, _stage_screen_position(Vector2(1000.0, 650.0)))
	deadline_ms = Time.get_ticks_msec() + 5000
	while bool(main.castle_room_player_sprite.get_meta("walking", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame
	await _frames(2)
	_ck("a new real floor tap cancels the queued bathtub action",
		Time.get_ticks_msec() < deadline_ms \
		and not bool(sprite.get_meta("busy", false)) \
		and main.castle_room_prop_sfx.stream == null)


func _exercise_drag_release_to_bathtub(rooms: CastleRooms25D) -> void:
	var record: Dictionary = main.castle_room_item_sprites.get(
		"bathtub", {}) as Dictionary
	var sprite: Sprite2D = record.get("sprite") as Sprite2D
	var hotspot: Button = record.get("hotspot") as Button
	var target: Vector2 = record.get("route_contact", Vector2.INF) as Vector2
	rooms._position_player_at_foot(Vector2(1000.0, 650.0), false)
	main.castle_room_prop_sfx.stop()
	main.castle_room_prop_sfx.stream = null
	var start := _stage_screen_position(Vector2(1000.0, 650.0))
	var finish := _stage_screen_position(
		hotspot.position + hotspot.size * 0.5)
	await _touch_drag(rooms, 11, start, finish)
	_touch(rooms, 11, finish, false)
	await _frames(2)
	_ck("touch drag release over bathtub requests its shared approach",
		rooms._owned_touch_index == -1 \
		and rooms._pending_item_action == "bathtub" \
		and bool(main.castle_room_player_sprite.get_meta("walking", false)))
	var samples_clear := true
	var no_early_action := true
	var deadline_ms := Time.get_ticks_msec() + 5000
	while bool(main.castle_room_player_sprite.get_meta("walking", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame
		var foot: Vector2 = main.castle_room_player_sprite.get_meta(
			"current_stage_foot", Vector2.INF) as Vector2
		samples_clear = samples_clear \
			and rooms._room_navigation.contains_point(foot, 0.1) \
			and _navigation_point_is_clear(rooms.navigation_snapshot(), foot)
		if bool(main.castle_room_player_sprite.get_meta("walking", false)):
			no_early_action = no_early_action \
				and not bool(sprite.get_meta("busy", false))
	var arrived: Vector2 = main.castle_room_player_sprite.get_meta(
		"current_stage_foot", Vector2.INF) as Vector2
	_ck("dragged bathtub action waits for clear path arrival",
		Time.get_ticks_msec() < deadline_ms and samples_clear \
		and no_early_action and arrived.distance_to(target) <= 1.0 \
		and bool(sprite.get_meta("busy", false)))
	deadline_ms = Time.get_ticks_msec() + 4000
	while bool(sprite.get_meta("busy", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame


func _exercise_drag_to_room_door(rooms: CastleRooms25D) -> void:
	rooms.show_room("family_gallery", false)
	await _frames(2)
	var door_record: Dictionary = main.castle_room_item_sprites.get(
		"gallery_dining_door", {}) as Dictionary
	var hotspot: Button = door_record.get("hotspot") as Button
	var start := _stage_screen_position(Vector2(1080.0, 680.0))
	var finish := _stage_screen_position(
		hotspot.position + hotspot.size * 0.5)
	await _room_drag(rooms, start, finish)
	_ck("drag release over an in-room physical door waits for arrival",
		main.castle_room_id == "family_gallery" \
		and rooms._pending_item_action == "gallery_dining_door" \
		and bool(main.castle_room_player_sprite.get_meta("walking", false)))
	var samples_on_lane := true
	var no_early_transition := true
	var deadline_ms := Time.get_ticks_msec() + 7000
	while main.castle_room_id == "family_gallery" \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame
		if main.castle_room_id == "family_gallery":
			var foot: Vector2 = main.castle_room_player_sprite.get_meta(
				"current_stage_foot", Vector2.INF) as Vector2
			samples_on_lane = samples_on_lane \
				and rooms._room_navigation.contains_point(foot, 0.1)
			if bool(main.castle_room_player_sprite.get_meta("walking", false)):
				no_early_transition = no_early_transition \
					and main.castle_room_id == "family_gallery"
	_ck("dragged in-room door follows its lane before changing rooms",
		Time.get_ticks_msec() < deadline_ms and samples_on_lane \
		and no_early_transition and main.castle_room_id == "dining_room")

func _exercise_drag_to_hall_door(rooms: CastleRooms25D) -> void:
	main.set("day_one_active", false)
	rooms.show_room("main_hall", false)
	await _frames(2)
	var door: Button = main.castle_room_buttons.get("library") as Button
	var start := _stage_screen_position(Vector2(1100.0, 680.0))
	var finish := door.get_global_rect().get_center()
	_touch(rooms, 6, finish, true)
	await _frames(3)
	_ck("press held over a hall door cannot arm or enter it",
		rooms._owned_touch_index == 6 \
		and rooms._pending_portal_id == "" \
		and rooms._room_transition_tween == null \
		and main.castle_room_id == "main_hall")
	_touch(rooms, 6, finish, false, true)
	await process_frame
	await _touch_drag(rooms, 7, start, finish)
	_touch(rooms, 8, finish, false)
	await process_frame
	_ck("a foreign touch release cannot steal the owned castle drag",
		rooms._owned_touch_index == 7
		and main.castle_room_id == "main_hall")
	_touch(rooms, 7, finish, false, true)
	await _frames(4)
	_ck("a canceled touch drag clears movement and door intent",
		rooms._owned_touch_index == -1
		and not bool(main.castle_room_player_sprite.get_meta("walking", false))
		and rooms._pending_portal_id == ""
		and main.castle_room_id == "main_hall")
	await _room_drag(rooms, start, finish)
	_ck("drag release on a physical door waits for arrival",
		main.castle_room_id == "main_hall"
		and bool(main.castle_room_player_sprite.get_meta("walking", false)))
	var samples_on_lane := true
	var deadline_ms := Time.get_ticks_msec() + 8000
	while main.castle_room_id == "main_hall" \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame
		if main.castle_room_id == "main_hall":
			var foot: Vector2 = main.castle_room_player_sprite.get_meta(
				"current_stage_foot", Vector2.INF) as Vector2
			samples_on_lane = samples_on_lane \
				and rooms._room_navigation.contains_point(foot, 0.1)
	_ck("dragged door route samples stay on the hall network",
		samples_on_lane)
	_ck("drag release enters the door after Roshan arrives",
		Time.get_ticks_msec() < deadline_ms \
		and main.castle_room_id == "library")

func _shot(capture_name: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	await _frames(3)
	await RenderingServer.frame_post_draw
	var output_dir := OS.get_environment("DAY_ONE_BATH_CAPTURE_OUT")
	if output_dir == "":
		output_dir = ProjectSettings.globalize_path(
			"res://audit/review/day_one_bath_swimmer_2026-08-24_v2")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var output_path := output_dir.path_join(capture_name + ".png")
	var save_error: Error = root.get_viewport().get_texture().get_image() \
		.save_png(output_path)
	print("BATHROOM_WORLD|shot saved: ", output_path,
		" error=", save_error)

func _run() -> void:
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	# The focused probe drives the room controller and tweens directly. Disable
	# unrelated ambient systems so companion-den state cannot pollute this
	# castle-only gate with deferred errors during the long interaction waits.
	await process_frame
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await process_frame
	main._day_one_ref().restore_state({
		"day_one_active": true,
		"day_one_completed_rooms": [],
	})
	main.g.erase("day_one_bathtub_filled")
	main.set_process(false)
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(16)

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("bubble_bath", false)
	await _frames(3)
	var empty_bath_bunny: Dictionary = rooms.day_one_bathtub_swimmer_snapshot()
	_ck("empty Day One bathtub has no swimmer or fill water",
		not bool(empty_bath_bunny.get("filled", true))
		and not bool(empty_bath_bunny.get("fill_water_visible", true))
		and not bool(empty_bath_bunny.get("visible", true)))
	await _shot("00_bubble_bath_empty")
	_ck("sprite stage open", rooms.is_open())
	_ck("direct canvas has no camera",
		main.castle_room_stage.find_children("*", "Camera2D", true, false).is_empty()
		and main.castle_room_stage.find_children("*", "Camera3D", true, false).is_empty())
	_ck("retired modeled bathroom absent",
		not main.g.has("toilet")
		and main.game_nodes.is_empty()
		and main.arena_solids.is_empty()
		and main.arena_zones.is_empty())
	var false_second_tub_left: Node = main.castle_room_front_layer.get_node_or_null(
		"room_bubble_bath_front_left")
	var false_second_tub_right: Node = main.castle_room_front_layer.get_node_or_null(
		"room_bubble_bath_front_right")
	var real_bathtub: Dictionary = main.castle_room_item_sprites.get(
		"bathtub", {}) as Dictionary
	_ck("one child-readable bathtub silhouette",
		false_second_tub_left == null
		and false_second_tub_right == null
		and real_bathtub.get("sprite") is Sprite2D,
		"false_foreground_left=%s false_foreground_right=%s real_bathtub=%s" % [
			false_second_tub_left != null, false_second_tub_right != null,
			real_bathtub.has("sprite")])
	var prop_expectations := _expected_props()
	_ck("audited V4 bathroom registry", v4_manifest_contract_ok,
		v4_manifest_contract_detail)
	var runtime_ids: Dictionary = {}
	var no_v3_props := true
	for runtime_id_value: Variant in main.castle_room_item_sprites.keys():
		var runtime_id: String = String(runtime_id_value)
		runtime_ids[runtime_id] = true
		var runtime_record: Dictionary = main.castle_room_item_sprites.get(
			runtime_id, {}) as Dictionary
		var runtime_data: Dictionary = runtime_record.get(
			"data", {}) as Dictionary
		var runtime_visual: Dictionary = runtime_data.get(
			"v2_visual", {}) as Dictionary
		var runtime_sprite: Sprite2D = runtime_record.get("sprite") as Sprite2D
		no_v3_props = no_v3_props \
			and String(runtime_visual.get("pack", "")) != "v3_addition" \
			and (runtime_sprite == null \
				or not bool(runtime_sprite.get_meta(
					"castle_component_rig_v3", false)))
	var exact_prop_set: bool = runtime_ids.size() == prop_expectations.size()
	for expected_id_value: Variant in prop_expectations.keys():
		exact_prop_set = exact_prop_set \
			and runtime_ids.has(String(expected_id_value))
	_ck("source-owned bath touch props",
		exact_prop_set
		and main.castle_room_item_hotspot_layer.get_child_count() \
			== prop_expectations.size(),
		"expected=%d runtime=%d hotspots=%d" % [
			prop_expectations.size(), runtime_ids.size(),
			main.castle_room_item_hotspot_layer.get_child_count()])
	_ck("zero V3 additions or duplicate props", no_v3_props and exact_prop_set)
	var expects_native_background := prop_expectations.values().any(
		func(expected_value: Variant) -> bool:
			var expected: Dictionary = expected_value as Dictionary
			return String(expected.get("pack", "")) == "v4_native")
	var native_background_ready := \
		main.castle_room_detail_tiles.all(
			func(tile: Sprite2D) -> bool:
				return bool(tile.get_meta(
					"native_source_ownership_background", false)) \
					and tile.texture != null \
					and tile.texture.resource_path.contains(
						"interactions_v4/background_tiles/"))
	_ck("native bath props own pixels over complete full-frame clean tiles",
		native_background_ready == expects_native_background,
		"expected_native=%s runtime_native=%s" % [
			expects_native_background, native_background_ready])

	var props_ok := true
	var depth_ok := true
	var interaction_ok := true
	var fixed_pivots_ok := true
	var temporal_smoothing_seen := false
	var exact_audio_ok := true
	var busy_guards_ok := true
	var toilet_cavity_water_ok := true
	var toilet_cavity_detail := ""
	var bathtub_water_ok := true
	var bathtub_water_detail := ""
	for prop_id: String in prop_expectations:
		var record: Dictionary = main.castle_room_item_sprites.get(prop_id, {})
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		var hotspot: Button = record.get("hotspot") as Button
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		var expected: Dictionary = prop_expectations[prop_id] as Dictionary
		var fixture_rig: Dictionary = record.get(
			"fixture_rig", {}) as Dictionary
		var fixture_visual: Dictionary = fixture_rig.get(
			"visual", {}) as Dictionary
		var physics_mode: String = String(fixture_rig.get(
			"physics_mode", "none"))
		var body: Node2D = fixture_rig.get("body") as Node2D
		var expected_sheet_path: String = "res://" + String(
			fixture_visual.get("sheet", ""))
		var frame_count: int = int(sprite.get_meta(
			"animation_frame_count", 0)) if sprite != null else 0
		var expected_pack: String = String(expected.get("pack", ""))
		if prop_id == "toilet":
			var water_specs: Array = fixture_visual.get("water_layers", []) as Array
			toilet_cavity_water_ok = water_specs.size() == 1
			if water_specs.size() == 1:
				var water_spec: Dictionary = water_specs[0] as Dictionary
				var center_values: Array = water_spec.get("center", []) as Array
				var radius_values: Array = water_spec.get("radius", []) as Array
				var cavity_values: Array = water_spec.get(
					"cavity_bounds_normalized", []) as Array
				var active_frames: Array = water_spec.get("active_frames", []) as Array
				var active_frames_ok: bool = active_frames.size() == 3 \
					and int(active_frames[0]) == 2 \
					and int(active_frames[1]) == 3 \
					and int(active_frames[2]) == 4
				toilet_cavity_water_ok = toilet_cavity_water_ok \
					and String(water_spec.get("role", "")) == "vortex" \
					and String(water_spec.get("contact_role", "")) \
						== "inside_bowl_cavity" \
					and center_values.size() == 2 and radius_values.size() == 2 \
					and cavity_values.size() == 4 \
					and active_frames_ok \
					and float(center_values[1]) >= 0.58 \
					and float(center_values[1]) <= 0.65 \
					and float(radius_values[0]) <= 0.13 \
					and float(radius_values[1]) <= 0.03 \
					and float(water_spec.get("z_offset", 1.0)) <= 0.004
				var runtime_water: Array = fixture_rig.get("water", []) as Array
				toilet_cavity_water_ok = toilet_cavity_water_ok \
					and runtime_water.size() == 1
				if runtime_water.size() == 1:
					var water_record: Dictionary = runtime_water[0] as Dictionary
					var water_node: Sprite2D = water_record.get("node") as Sprite2D
					var bounds: Rect2 = water_record.get(
						"bounds_normalized", Rect2()) as Rect2
					var cavity := Rect2(
						Vector2(float(cavity_values[0]), float(cavity_values[1])),
						Vector2(float(cavity_values[2]), float(cavity_values[3])))
					toilet_cavity_water_ok = toilet_cavity_water_ok \
						and water_node != null and cavity.encloses(bounds) \
						and water_node.z_index == sprite.z_index
					toilet_cavity_detail = \
						"spec=%s bounds=%s cavity=%s water_z=%s sprite_z=%s" % [
							water_spec, bounds, cavity,
							water_node.z_index if water_node != null else INF,
							sprite.z_index if sprite != null else INF]
		if prop_id == "bathtub":
			var bathtub_water: Array = fixture_rig.get("water", []) as Array
			var bathtub_roles := PackedStringArray()
			var bathtub_fill_alpha := 1.0
			for water_value: Variant in bathtub_water:
				var water_record: Dictionary = water_value as Dictionary
				bathtub_roles.append(String(water_record.get("role", "")))
				if String(water_record.get("role", "")) == "fill":
					var water_material: ShaderMaterial = water_record.get(
						"material") as ShaderMaterial
					if water_material != null:
						bathtub_fill_alpha = float(water_material.get_shader_parameter(
							"alpha_base"))
			bathtub_water_ok = bathtub_water.size() == 1 \
				and bathtub_roles.has("fill") \
				and not bathtub_roles.has("stream") \
				and bathtub_fill_alpha <= 0.24
			bathtub_water_detail = "roles=%s alpha=%.3f" % [
				bathtub_roles, bathtub_fill_alpha]
		var native_v4_ok: bool = expected_pack != "v4_native" \
			or (sprite != null \
				and bool(sprite.get_meta("source_owned_native", false)) \
				and bool(sprite.get_meta(
					"source_ownership_verified", false)) \
				and bool(sprite.get_meta(
					"native_authored_object_states", false)) \
				and not bool(sprite.get_meta(
					"generic_transform_fallback", true)))
		props_ok = props_ok and sprite != null \
			and not bool(sprite.get_meta("shaded", false)) \
			and hotspot != null and hotspot.size.x >= 112.0 \
			and hotspot.size.y >= 112.0 \
			and frame_count >= 4 and frame_count <= 12 \
			and sprite.hframes * sprite.vframes >= frame_count \
			and sprite.texture != null \
			and expected_sheet_path != "res://" \
			and sprite.texture.resource_path == expected_sheet_path \
			and String(fixture_visual.get("pack", "")) == expected_pack \
			and native_v4_ok \
			and bool(sprite.get_meta(
				"generated_full_object_states", false)) \
			and not bool(sprite.get_meta(
				"primary_animation_is_overlay", true)) \
			and String(sprite.get_meta("semantic_action", "")) \
				== String(expected["semantic_action"]) \
			and String(item_data.get("sound", "")) \
				== String(expected["runtime_sound"])
		depth_ok = depth_ok and sprite != null \
			and sprite.z_index > main.castle_room_background.z_index \
			and sprite.z_index < int(round(CastleRooms25D.FOREGROUND_Z * 100.0))
		if sprite != null:
			var start_position: Vector2 = sprite.position
			var start_scale: Vector2 = sprite.scale
			var start_rotation: float = sprite.rotation
			main.castle_room_prop_sfx.stop()
			main.castle_room_prop_sfx.stream = null
			rooms._activate_room_item(prop_id)
			var busy_started: bool = bool(sprite.get_meta("busy", false))
			var effects_after_first: int = \
				main.castle_room_item_effect_layer.get_child_count()
			rooms._activate_room_item(prop_id)
			busy_guards_ok = busy_guards_ok \
				and main.castle_room_item_effect_layer.get_child_count() \
					== effects_after_first
			var wait_frames := 0
			var deadline_ms: int = Time.get_ticks_msec() + 3000
			while bool(sprite.get_meta("busy", false)) \
					and Time.get_ticks_msec() < deadline_ms:
				await process_frame
				wait_frames += 1
				if physics_mode == "none":
					fixed_pivots_ok = fixed_pivots_ok \
						and sprite.position.is_equal_approx(start_position) \
						and sprite.scale.is_equal_approx(start_scale) \
						and is_equal_approx(sprite.rotation, start_rotation)
				else:
					var spring: Dictionary = fixture_rig.get(
						"spring", {}) as Dictionary
					var max_displacement_canvas: float = float(
						fixture_rig.get("max_displacement_canvas", 0.0))
					var max_angle: float = float(
						fixture_rig.get("max_angle_radians", 0.0))
					fixed_pivots_ok = fixed_pivots_ok \
						and body == null and not spring.is_empty() \
						and max_displacement_canvas > 0.0 \
						and sprite.position.distance_to(start_position) \
							<= max_displacement_canvas + 0.001 \
						and absf(sprite.rotation - start_rotation) \
							<= max_angle + 0.001 \
						and sprite.scale.is_equal_approx(start_scale)
			var expected_frames: Array[int] = []
			for frame_value: Variant in item_data.get(
					"timeline_sequence", []) as Array:
				expected_frames.append(int(frame_value))
			var expected_steps: Array[int] = []
			for timeline_step: int in range(expected_frames.size()):
				expected_steps.append(timeline_step)
			var visited: Array = sprite.get_meta(
				"animation_frames_visited", []) as Array
			var visited_steps: Array = sprite.get_meta(
				"animation_timeline_steps_visited", []) as Array
			interaction_ok = interaction_ok and busy_started \
				and Time.get_ticks_msec() < deadline_ms \
				and expected_frames.size() >= 4 \
				and expected_frames.size() <= 12 \
				and visited == expected_frames \
				and visited_steps == expected_steps \
				and sprite.frame == int(item_data.get("rest_frame", 0)) \
				and not bool(sprite.get_meta("busy", true))
			if sprite.material == null:
				var smoother: Variant = sprite.get_node_or_null(
					"TemporalSpriteTransition")
				temporal_smoothing_seen = temporal_smoothing_seen \
					or (smoother != null \
						and smoother.smoothness_multiplier() == 3 \
						and smoother.rendered_transition_samples() > 0 \
						and not smoother.is_transition_active() \
						and int(sprite.get_meta(
							"sprite_transition_draws", 0)) == 1)
			if physics_mode != "none":
				var spring: Dictionary = fixture_rig.get(
					"spring", {}) as Dictionary
				var settle_deadline_ms: int = Time.get_ticks_msec() + 5000
				while String(spring.get("phase", "idle")) != "idle" \
						and Time.get_ticks_msec() < settle_deadline_ms:
					await physics_frame
				var max_displacement_canvas: float = float(
					fixture_rig.get("max_displacement_canvas", 0.0))
				fixed_pivots_ok = fixed_pivots_ok \
					and body == null \
					and not spring.is_empty() \
					and String(spring.get("phase", "")) == "idle" \
					and Time.get_ticks_msec() < settle_deadline_ms \
					and max_displacement_canvas > 0.0 \
					and float(fixture_rig.get(
						"peak_angle_radians", 0.0)) > 0.001 \
					and float(fixture_rig.get(
						"peak_displacement", 0.0)) > 0.001 \
					and float(fixture_rig.get(
						"peak_displacement", 0.0)) \
						<= max_displacement_canvas + 0.001 \
					and sprite.position.distance_to(start_position) <= 0.02 \
					and sprite.scale.is_equal_approx(start_scale) \
					and absf(sprite.rotation - start_rotation) <= 0.02
			exact_audio_ok = exact_audio_ok \
				and main.castle_room_prop_sfx.stream != null \
				and main.castle_room_prop_sfx.stream.resource_path \
					== String(expected["sound"])
	_ck("unshaded Sprite2D fixtures", props_ok)
	_ck("fixtures occupy real depth", depth_ok)
	_ck("semantic atlas sequences follow audited timelines and reset",
		interaction_ok)
	_ck("Canvas fixtures add 3x temporal samples and sleep at one idle draw",
		temporal_smoothing_seen)
	_ck("semantic fixture actions stay bounded and restore roots",
		fixed_pivots_ok)
	_ck("fixture actions play exact castle audio", exact_audio_ok)
	_ck("fixture animations reject repeat taps while busy", busy_guards_ok)
	_ck("toilet vortex stays inside the animated bowl cavity",
		toilet_cavity_water_ok, toilet_cavity_detail)
	_ck("bathtub water is a soft contained basin layer",
		bathtub_water_ok, bathtub_water_detail)
	var bath_bunny: Dictionary = rooms.day_one_bathtub_swimmer_snapshot()
	var bath_swimmer: Dictionary = bath_bunny.get("swimmer", {}) as Dictionary
	_ck("filled Day One bathtub reuses the true-swimming bunny",
		bool(bath_bunny.get("filled", false))
		and bool(bath_bunny.get("fill_water_visible", false))
		and bool(bath_bunny.get("visible", false))
		and bool(bath_bunny.get("behind_tub_lip", false))
		and bool(bath_swimmer.get("true_2d", false))
		and bool(bath_swimmer.get("inside_bounds", false))
		and bool(bath_swimmer.get("fully_contained", false))
		and String(bath_swimmer.get("asset", "")).ends_with(
			"dust_bunny_swimming.png")
		and float(bath_swimmer.get("display_width", 0.0)) <= 72.1)
	_ck("no bathtub-like foreground occluders",
		main.castle_room_front_layer.get_child_count() == 0)
	_ck("free-roaming controls disabled",
		not main.touch_ui.world_controls_enabled
		and not main.player.visible
		and main.touch_interactables.is_empty())
	_check_authored_navigation_geometry(rooms, "bubble_bath")
	await _exercise_bathtub_approach(rooms)
	await _exercise_drag_release_to_bathtub(rooms)

	await _shot("01_bubble_bath_filled_swimmer")
	main.set("day_one_active", false)
	rooms.show_room("library", false)
	await _frames(2)
	_check_authored_navigation_geometry(rooms, "library")
	rooms.show_room("playroom", false)
	await _frames(2)
	_check_authored_navigation_geometry(rooms, "playroom")
	await _exercise_drag_to_room_door(rooms)
	await _exercise_drag_to_hall_door(rooms)
	# Let Canvas shader instances and fixture nodes leave the rendering server
	# before SceneTree shutdown. Immediate quit can otherwise produce a dummy-
	# renderer null-material diagnostic after every assertion has passed.
	rooms.close()
	await _frames(2)
	main.queue_free()
	main = null
	await _frames(4)
	print("BATHROOM_WORLD|RESULT: ", checks_failed,
		(" FAIL" if checks_failed > 0 else " OK"))
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
