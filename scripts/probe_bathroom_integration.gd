extends SceneTree
# Focused live-world audit for the Bubble Bath room. The room is a layered
# Sprite3D stage: tub, sink, toilet, and duck are separate world cards with
# projected touch targets, semantic atlas animations, and sounds. No modeled
# bathroom may be rebuilt.

const PROP_EXPECTATIONS := {
	"bathtub": {
		"semantic_action": "turn_taps_and_fill_bubbles",
		"sound": "res://assets/audio/castle/bubble_water.ogg",
	},
	"sink": {
		"semantic_action": "turn_faucet_and_run_water",
		"sound": "res://assets/audio/castle/faucet_water.ogg",
	},
	"toilet": {
		"semantic_action": "flap_seat_and_flush",
		"sound": "res://assets/audio/castle/toilet_flush.ogg",
	},
	"rubber_duck": {
		"semantic_action": "squeak_dive_and_pop_up",
		"sound": "res://assets/audio/castle/duck_squeak.ogg",
	},
}

var main: ReefMain
var checks_failed := 0

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
		"res://audit/castle_sprite3d")
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
	_ck("sprite stage open", rooms.is_open())
	_ck("perspective camera",
		main.castle_room_camera != null
		and main.castle_room_camera.projection
			== Camera3D.PROJECTION_PERSPECTIVE)
	_ck("retired modeled bathroom absent",
		not main.g.has("toilet")
		and main.game_nodes.is_empty()
		and main.arena_solids.is_empty()
		and main.arena_zones.is_empty())
	_ck("four separate touch props",
		main.castle_room_item_sprites.size() == 4
		and main.castle_room_item_hotspot_layer.get_child_count() == 4)

	var props_ok := true
	var depth_ok := true
	var interaction_ok := true
	var fixed_pivots_ok := true
	var exact_audio_ok := true
	var busy_guards_ok := true
	for prop_id: String in PROP_EXPECTATIONS:
		var record: Dictionary = main.castle_room_item_sprites.get(prop_id, {})
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		var hotspot: Button = record.get("hotspot") as Button
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		var expected: Dictionary = PROP_EXPECTATIONS[prop_id] as Dictionary
		var frame_count: int = int(sprite.get_meta(
			"animation_frame_count", 0)) if sprite != null else 0
		props_ok = props_ok and sprite != null and not sprite.shaded \
			and hotspot != null and hotspot.size.x >= 112.0 \
			and hotspot.size.y >= 112.0 \
			and frame_count >= 4 and frame_count <= 12 \
			and sprite.hframes * sprite.vframes >= frame_count \
			and sprite.texture != null \
			and sprite.texture.resource_path.ends_with(
				"bubble_bath_" + prop_id + "_atlas.png") \
			and String(sprite.get_meta("semantic_action", "")) \
				== String(expected["semantic_action"]) \
			and String(item_data.get("sound", "")) \
				== String(expected["sound"]).trim_prefix(
					"res://assets/audio/")
		depth_ok = depth_ok and sprite != null \
			and sprite.position.z > main.castle_room_background.position.z \
			and sprite.position.z < CastleRooms25D.FOREGROUND_Z
		if sprite != null:
			var start_position: Vector3 = sprite.position
			var start_scale: Vector3 = sprite.scale
			var start_rotation: Vector3 = sprite.rotation
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
				fixed_pivots_ok = fixed_pivots_ok \
					and sprite.position.is_equal_approx(start_position) \
					and sprite.scale.is_equal_approx(start_scale) \
					and sprite.rotation.is_equal_approx(start_rotation)
			var expected_frames: Array[int] = []
			for frame_index: int in range(frame_count):
				expected_frames.append(frame_index)
			var visited: Array = sprite.get_meta(
				"animation_frames_visited", []) as Array
			interaction_ok = interaction_ok and busy_started \
				and Time.get_ticks_msec() < deadline_ms \
				and visited == expected_frames \
				and sprite.frame == 0 \
				and not bool(sprite.get_meta("busy", true))
			exact_audio_ok = exact_audio_ok \
				and main.castle_room_prop_sfx.stream != null \
				and main.castle_room_prop_sfx.stream.resource_path \
					== String(expected["sound"])
	_ck("unshaded Sprite3D fixtures", props_ok)
	_ck("fixtures occupy real depth", depth_ok)
	_ck("semantic atlas sequences visit every frame and reset", interaction_ok)
	_ck("semantic fixture actions keep fixed root pivots", fixed_pivots_ok)
	_ck("fixture actions play exact castle audio", exact_audio_ok)
	_ck("fixture animations reject repeat taps while busy", busy_guards_ok)
	_ck("foreground occluders",
		main.castle_room_front_layer.get_child_count() == 2
		and (main.castle_room_front_layer.get_child(0) as Sprite3D).position.z
			> main.castle_room_player_sprite.position.z)
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
