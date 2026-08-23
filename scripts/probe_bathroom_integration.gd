extends SceneTree
# Focused live-world audit for the Bubble Bath Canvas trial. Retained and
# audited source-owned fixtures share one 2D hierarchy with exact touch targets,
# semantic atlas animation, manifest water geometry, and sound. No modeled
# bathroom, spatial water, Jolt garnish, or V3 prop pack may return.

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

func _shot() -> void:
	if DisplayServer.get_name() == "headless":
		return
	await _frames(3)
	await RenderingServer.frame_post_draw
	var output_dir := ProjectSettings.globalize_path(
		"res://audit/castle_water_2d")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var output_path := output_dir.path_join("bubble_bath.png")
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
	main.set_process(false)
	await process_frame
	main._skip_intro()
	await process_frame
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
	_ck("wet room stage open", rooms.is_open()
		and rooms.wet_rooms != null and rooms.wet_rooms.is_active())
	_ck("full Canvas presentation active",
		rooms.wet_rooms.root is Node2D
		and String(rooms.wet_rooms.root.get_meta("final_medium", ""))
			== "canvas_2d"
		and main.castle_room_world_root != null
		and not main.castle_room_world_root.visible
		and main.castle_room_camera != null
		and not main.castle_room_camera.current)
	_ck("retired modeled bathroom absent",
		not main.g.has("toilet")
		and main.game_nodes.is_empty()
		and main.arena_solids.is_empty()
		and main.arena_zones.is_empty())
	var prop_expectations := _expected_props()
	_ck("audited V4 bathroom registry", v4_manifest_contract_ok,
		v4_manifest_contract_detail)
	var runtime_ids: Dictionary = {}
	var all_canvas_props := true
	for runtime_id_value: Variant in main.castle_room_item_sprites.keys():
		var runtime_id: String = String(runtime_id_value)
		runtime_ids[runtime_id] = true
		var runtime_record: Dictionary = main.castle_room_item_sprites.get(
			runtime_id, {}) as Dictionary
		var runtime_sprite: Sprite2D = runtime_record.get(
			"canvas_sprite") as Sprite2D
		all_canvas_props = all_canvas_props and runtime_sprite != null \
			and bool(runtime_sprite.get_meta(
				"canvas_water_trial_fixture", false))
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
	_ck("zero duplicate props and every visible fixture is Canvas",
		all_canvas_props and exact_prop_set)
	var expects_native_background := prop_expectations.values().any(
		func(expected_value: Variant) -> bool:
			var expected: Dictionary = expected_value as Dictionary
			return String(expected.get("pack", "")) == "v4_native")
	var native_background_ready := \
		main.castle_room_detail_tiles.all(
			func(tile: Sprite3D) -> bool:
				return bool(tile.get_meta(
					"native_source_ownership_background", false)) \
					and tile.texture != null \
					and tile.texture.resource_path.contains(
						"interactions_v4/background_tiles/"))
	_ck("native bath props replace pixels in healed high-resolution tiles",
		native_background_ready == expects_native_background,
		"expected_native=%s runtime_native=%s" % [
			expects_native_background, native_background_ready])

	var props_ok := true
	var interaction_ok := true
	var fixed_pivots_ok := true
	var exact_audio_ok := true
	var busy_guards_ok := true
	var toilet_cavity_water_ok := true
	var toilet_cavity_detail := ""
	for prop_id: String in prop_expectations:
		var record: Dictionary = main.castle_room_item_sprites.get(prop_id, {})
		var sprite: Sprite2D = record.get("canvas_sprite") as Sprite2D
		var hotspot: Button = record.get("hotspot") as Button
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		var expected: Dictionary = prop_expectations[prop_id] as Dictionary
		var fixture_visual: Dictionary = item_data.get(
			"v2_visual", {}) as Dictionary
		var water: CastleWaterFixture2D = rooms.wet_rooms.fixture_water.get(
			prop_id) as CastleWaterFixture2D
		var expected_sheet_path: String = "res://" + String(
			fixture_visual.get("sheet", ""))
		var frame_count: int = int(item_data.get("frames", 0))
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
				var runtime_water: Array[Dictionary] = water.layer_metadata() \
					if water != null else []
				toilet_cavity_water_ok = toilet_cavity_water_ok \
					and runtime_water.size() == 1
				if runtime_water.size() == 1:
					var water_record: Dictionary = runtime_water[0]
					var bounds: Rect2 = water_record.get(
						"bounds_normalized", Rect2()) as Rect2
					var cavity := Rect2(
						Vector2(float(cavity_values[0]), float(cavity_values[1])),
						Vector2(float(cavity_values[2]), float(cavity_values[3])))
					toilet_cavity_water_ok = toilet_cavity_water_ok \
						and cavity.encloses(bounds) \
						and String(water_record.get("role", "")) == "vortex"
					toilet_cavity_detail = \
						"spec=%s bounds=%s cavity=%s" % [
							water_spec, bounds, cavity]
		props_ok = props_ok and sprite != null \
			and hotspot != null and hotspot.size.x >= 110.0 \
			and hotspot.size.y >= 110.0 \
			and frame_count >= 4 and frame_count <= 12 \
			and sprite.hframes * sprite.vframes >= frame_count \
			and sprite.texture != null \
			and expected_sheet_path != "res://" \
			and sprite.texture.resource_path == expected_sheet_path \
			and String(fixture_visual.get("pack", "")) == expected_pack \
			and bool(sprite.get_meta("fixed_pivot_animation", false)) \
			and String(item_data.get("sound", "")) \
				== String(expected["runtime_sound"])
		if sprite != null:
			var start_position: Vector2 = sprite.position
			var start_scale: Vector2 = sprite.scale
			var start_rotation: float = sprite.rotation
			main.castle_room_prop_sfx.stop()
			main.castle_room_prop_sfx.stream = null
			rooms._activate_room_item(prop_id)
			var busy_started: bool = bool(sprite.get_meta("busy", false))
			var visited_after_first: Array = sprite.get_meta(
				"animation_frames_visited", []) as Array
			rooms._activate_room_item(prop_id)
			busy_guards_ok = busy_guards_ok \
				and sprite.get_meta("animation_frames_visited", []) \
					== visited_after_first
			var wait_frames := 0
			var deadline_ms: int = Time.get_ticks_msec() + 3000
			while bool(sprite.get_meta("busy", false)) \
					and Time.get_ticks_msec() < deadline_ms:
				await process_frame
				wait_frames += 1
				fixed_pivots_ok = fixed_pivots_ok \
					and sprite.position.is_equal_approx(start_position) \
					and sprite.scale.is_equal_approx(start_scale) \
					and is_equal_approx(sprite.rotation, start_rotation)
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
			exact_audio_ok = exact_audio_ok \
				and main.castle_room_prop_sfx.stream != null \
				and main.castle_room_prop_sfx.stream.resource_path \
					== String(expected["sound"])
	_ck("source-owned Sprite2D fixtures and production touch", props_ok)
	_ck("semantic atlas sequences follow audited timelines and reset",
		interaction_ok)
	_ck("semantic fixture actions keep fixed Canvas pivots",
		fixed_pivots_ok)
	_ck("fixture actions play exact castle audio", exact_audio_ok)
	_ck("fixture animations reject repeat taps while busy", busy_guards_ok)
	_ck("toilet vortex stays inside the animated bowl cavity",
		toilet_cavity_water_ok, toilet_cavity_detail)
	var foreground: Node2D = rooms.wet_rooms.root.get_node_or_null(
		"Foreground") as Node2D
	_ck("Canvas foreground occluders",
		foreground != null and foreground.get_child_count() == 2
		and foreground.z_index > rooms.wet_rooms.actor.z_index)
	var wet_stats: Dictionary = rooms.wet_rooms.stats()
	_ck("fixture water is Canvas-only with no Jolt allocation",
		bool(wet_stats.get("canvas_only", false))
		and int(wet_stats.get("water_layers", 0)) == 6
		and main.castle_room_fixture_physics.is_empty()
		and main.castle_room_fixture_rigs.is_empty())
	_ck("free-roaming controls disabled",
		not main.touch_ui.world_controls_enabled
		and not main.player.visible
		and main.touch_interactables.is_empty())

	await _shot()
	print("BATHROOM_WORLD|RESULT: ", checks_failed,
		(" FAIL" if checks_failed > 0 else " OK"))
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
