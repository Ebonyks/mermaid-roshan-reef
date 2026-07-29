extends SceneTree
# Interaction-language integration: proximity advertises, first tap selects,
# assisted movement approaches, and only a second explicit verb activates.

var main: Node3D
var failures := 0

func _init() -> void:
	Engine.time_scale = 4.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(8)
	main._set_touch_mode("hybrid", false)
	main._populate_touch_interactables()
	if main.touch_interactables.size() < main.friends.size():
		_bad("reef registry omitted core friends")

	var friend: Dictionary = main.friends[0]
	var friend_node: Node3D = friend["node"]
	main.player.position = friend_node.position + Vector3(3.0, 0.0, 0.0)
	main.player.vel = Vector3.ZERO
	await _frames(20)
	if main.game != "":
		_bad("proximity launched a friend activity")

	var camera: Camera3D = main.get_viewport().get_camera_3d()
	if camera == null:
		_bad("camera unavailable for screen-space selection")
	else:
		var tap: Vector2 = camera.unproject_position(friend_node.global_position)
		# An action press made before anything is selected must expire. It may
		# not be remembered and applied to the next focus, even in the same
		# rendered frame.
		main.touch_ui._on_action_button_down()
		main.touch_ui._on_action_button_up()
		main._interaction_ref().on_world_touch(tap)
		await process_frame
		if main.touch_focus_id != "friend:0" or not main.touch_focus_ready:
			_bad("first friend tap did not focus/ready")
		if main.game != "":
			_bad("first friend tap launched instead of acknowledging")
		main._interaction_ref().on_world_touch(tap)
		await _frames(12)
		if main.game == "":
			_bad("second friend tap did not activate")
	if main.game != "":
		main._clear_game()
		await _frames(6)

	# Open-space assisted movement feeds steering and yields to manual input.
	var travel_target: Vector3 = main.player.position + Vector3(25.0, 0.0, 18.0)
	main._tap_move_ref().start(travel_target)
	var direction: Vector3 = main.touch_auto_direction()
	if not bool(main.touch_auto_active) or direction.length() < 0.9:
		_bad("assisted movement produced no steering intent")
	main._on_touch_manual_move()
	if bool(main.touch_auto_active):
		_bad("manual override failed")

	# Fix regression: an ELEVATED target (the penguin floe rides just under the
	# surface) must become ready through assisted travel. Horizontal-only
	# steering once stopped short of the vertically-weighted readiness check
	# and looped "Tap again!" forever.
	if main.slide_portal_pos == Vector3.ZERO:
		_bad("penguin floe position unavailable for the elevated approach")
	else:
		var floe: Vector3 = main.slide_portal_pos
		main.player.position = Vector3(floe.x + 9.0, floe.y - 26.0, floe.z)
		main.player.vel = Vector3.ZERO
		main._populate_touch_interactables()
		main.touch_focus_id = "reef:slide"
		main.touch_focus_ready = false
		main._tap_move_ref().start(floe, "reef:slide", 14.0)
		var previous_scale: float = Engine.time_scale
		Engine.time_scale = 1.0
		var climb_start_y: float = main.player.position.y
		var deadline: int = Time.get_ticks_msec() + 12000
		while Time.get_ticks_msec() < deadline and not main.touch_focus_ready:
			await process_frame
		Engine.time_scale = previous_scale
		if not main.touch_focus_ready:
			_bad("elevated floe never became ready (vertical approach wedge)")
		if main.player.position.y - climb_start_y < 4.0:
			_bad("assisted travel did not climb toward the elevated floe")
		main._tap_move_ref().cancel("probe")
		main._interaction_ref().clear_focus()

	# Build the two navigation-heavy zones and assert that each important verb
	# has a touch target. This catches hidden-floor regressions without relying
	# on a camera-perfect scripted swim.
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(24)
	main._populate_touch_interactables()
	var court_ids := _ids()
	for expected: String in ["court:castle", "court:north", "court:kart_a", "court:kart_b"]:
		if not court_ids.has(expected):
			_bad("courtyard registry missing %s" % expected)
	if court_ids.has("court:opera") or main.g.has("opera_gate"):
		_bad("retired 3D courtyard Opera route was rebuilt")

	# Fix regression: with the castle OPEN the door slab is parked ~30 units up
	# in the sky. court:castle must anchor at the doorway at walk height, and a
	# real screen-space tap on the ground-level archway must pick the castle —
	# not the secret back hatch through the walls.
	var entry: Vector3 = main.g.get("entry", Vector3.ZERO)
	var castle_item: Dictionary = {}
	for item_value: Variant in main.touch_interactables:
		if String((item_value as Dictionary).get("id", "")) == "court:castle":
			castle_item = item_value as Dictionary
	if not castle_item.is_empty() and entry != Vector3.ZERO:
		var anchor: Vector3 = castle_item.get("pos", Vector3.ZERO)
		if castle_item.get("node") != null:
			_bad("court:castle tracks a node (the sliding door slab)")
		var walk_y: float = main.lagoon_walk_h(anchor.x, anchor.z)
		if absf(anchor.y - walk_y) > 6.0:
			_bad("court:castle anchor is %.1f units off walk height" % absf(anchor.y - walk_y))
		main.player.position = entry + Vector3(0.0, 2.0, 55.0)
		main.player.position.y = walk_y + 2.0
		main.player.vel = Vector3.ZERO
		main.player.yaw = PI
		if main.player.has_method("snap_cam"):
			main.player.snap_cam()
		await _frames(6)
		var court_camera: Camera3D = main.get_viewport().get_camera_3d()
		if court_camera != null:
			var doorway := Vector3(entry.x, walk_y + 3.0, entry.z)
			var door_tap: Vector2 = court_camera.unproject_position(doorway)
			main._interaction_ref().on_world_touch(door_tap)
			await process_frame
			if main.touch_focus_id != "court:castle":
				_bad("front-door tap picked '%s' instead of the castle" % main.touch_focus_id)
			main._tap_move_ref().cancel("probe")
			main._interaction_ref().clear_focus()

	# The castle is one picture-first Sprite3D stage, not a second free-roaming
	# 3D world. Room props use UI hit targets projected over their world cards;
	# the retired hall registry must therefore remain empty.
	main.level2_done_once = false
	main._enter_castle_interior_now(false)
	await _frames(24)
	main._populate_touch_interactables()
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	if not rooms.is_open():
		_bad("castle Sprite3D room stage did not open")
	if not _ids().is_empty():
		_bad("retired 3D hall touch targets were populated")
	for retired_key: String in [
		"hall_exit", "bed_pos", "stand_chest", "toilet", "dungeon_gate",
		"craft_easel", "wardrobe", "song_star", "secret_door", "hall_touch",
		"bells", "opera_gate"]:
		if main.g.has(retired_key):
			_bad("retired 3D hall state rebuilt %s" % retired_key)
	for room_id: String in [
		"main_hall", "opera_hall", "kitchen", "library", "playroom",
		"craft_room", "mermaid_pool", "bubble_bath"]:
		if not main.castle_room_buttons.has(room_id):
			_bad("castle elevator missing %s" % room_id)
	if main.castle_room_world_root == null \
			or main.castle_room_camera == null \
			or main.castle_room_camera.projection != Camera3D.PROJECTION_PERSPECTIVE:
		_bad("castle did not build its perspective Sprite3D stage")
	if main.touch_ui.world_controls_enabled or main.player.visible:
		_bad("free-roaming 3D controls remained active inside castle stage")
	if main.touch_discovery_ring == null or main.touch_focus_ring == null:
		_bad("shared glow/focus visuals were not built")
	rooms._toggle_menu()
	if not main.castle_room_menu_open or not main.castle_room_menu_panel.visible:
		_bad("storybook elevator did not expand")
	rooms.show_room("bubble_bath", false)
	await _frames(2)
	for prop_id: String in ["bathtub", "sink", "toilet"]:
		if not main.castle_room_item_sprites.has(prop_id):
			_bad("bubble bath missing separate Sprite3D prop %s" % prop_id)
	var toilet_record: Dictionary = main.castle_room_item_sprites.get("toilet", {})
	var toilet_sprite: Sprite3D = toilet_record.get("sprite") as Sprite3D
	rooms._activate_room_item("toilet")
	await process_frame
	if toilet_sprite == null or not bool(toilet_sprite.get_meta("busy", false)):
		_bad("touching the toilet did not animate its Sprite3D card")
	if main.castle_room_prop_sfx == null or main.castle_room_prop_sfx.stream == null:
		_bad("touching a room prop did not attach relevant sound")
	rooms.show_room("main_hall", false)
	rooms.activate_current_room()
	await process_frame
	if not bool(main.g.get("crown_won", false)):
		_bad("Main Hall action did not award the Crown Star")

	# Pointer-driven activities may temporarily cover the castle, but closing a
	# nested overlay must return to the room stage rather than resurrecting the
	# retired free-roaming controls.
	main._mg2d_open("garden")
	await process_frame
	if main.touch_ui.world_controls_enabled or (main.touch_ui._act_button != null and main.touch_ui._act_button.visible):
		_bad("world action controls occluded a picture game")
	# Nested pause overlays must release only their own block; closing Sticker
	# Book while the picture game remains open cannot resurrect world controls.
	main._open_stickers()
	await process_frame
	main._close_stickers()
	await process_frame
	if main.touch_ui.world_controls_enabled or (main.touch_ui._act_button != null and main.touch_ui._act_button.visible):
		_bad("closing nested overlay re-enabled controls above picture game")
	main._mg2d_close()
	await process_frame
	if main.touch_ui.world_controls_enabled:
		_bad("picture game close enabled 3D controls over castle stage")

	# Leaving the picture stage clears stale assisted navigation and restores the
	# courtyard. The room overlay and its Sprite3D world must be fully released.
	main.touch_focus_id = "retired:hall"
	main.touch_auto_active = true
	rooms._exit_to_courtyard()
	main._on_touch_world(main.get_viewport().get_visible_rect().size * 0.5)
	if not main.touch_focus_id.is_empty() or main.touch_auto_active:
		_bad("rapid transition tap retained or created stale navigation")
	if main.fade_rect != null and main.fade_rect.mouse_filter != Control.MOUSE_FILTER_STOP:
		_bad("fade cover did not claim touches during transition")
	await _frames(8)

	# Leaving Level 2 directly from the castle must also tear down both UI and
	# world-card roots; otherwise the old stage can remain over the reef.
	main._enter_castle_interior_now(false)
	await _frames(12)
	main._exit_level2_now()
	await _frames(4)
	if not main.touch_ui.world_controls_enabled:
		_bad("leaving the castle left touch controls blocked")
	if rooms.is_open() or main.castle_room_world_root != null:
		_bad("leaving Level 2 retained the castle Sprite3D stage")

	# Fix regression (Hybrid contract): the sparring den may advertise by
	# proximity but must start ONLY from its explicit tap target.
	main.companion_id = "eagle"
	main.companion_resting = false
	main.stuffie_cool = 0.0
	await _frames(30)
	if main.companion_den == null or not is_instance_valid(main.companion_den):
		_bad("companion den never built for the contract check")
	else:
		main.player.position = main.companion_den.position + Vector3(1.0, 1.0, 0.0)
		main.player.vel = Vector3.ZERO
		await _frames(20)
		if main.game != "":
			_bad("Hybrid proximity auto-started the sparring battle")
		main._populate_touch_interactables()
		if not _ids().has("reef:den"):
			_bad("sparring den is not an explicit touch target in Hybrid")
		main._activate_touch_interactable("reef:den")
		await _frames(4)
		if main.game != "stuffie":
			_bad("explicit den target did not start the battle")
		if bool(main.touch_auto_active) or not main.touch_focus_id.is_empty():
			_bad("battle start kept stale focus/assisted travel")

	main._set_touch_mode("classic", false)
	if main.touch_uses_explicit_interactions() or main.touch_auto_active:
		_bad("Classic rollback left Hybrid systems active")
	_finish()

func _ids() -> Array[String]:
	var result: Array[String] = []
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		result.append(String(item.get("id", "")))
	return result

func _has_id_prefix(prefix: String) -> bool:
	for interactable_id: String in _ids():
		if interactable_id.begins_with(prefix):
			return true
	return false

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame

func _bad(message: String) -> void:
	failures += 1
	print("INTERACTION|FAIL ", message)

func _finish() -> void:
	if failures == 0:
		print("INTERACTION|ALL OK")
		quit()
	else:
		print("INTERACTION|FAIL %d issue(s)" % failures)
		quit(1)
