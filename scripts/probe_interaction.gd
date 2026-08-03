extends SceneTree
# Interaction-language integration: proximity advertises, first tap selects,
# assisted movement approaches, and only a second explicit verb activates.

const Affordance := preload("res://scripts/interaction_affordance.gd")

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
	for touch_target_value: Variant in main.touch_interactables:
		var touch_target: Dictionary = touch_target_value as Dictionary
		var target_id: String = String(touch_target.get("id", ""))
		var expected_affordance: String = Affordance.INTERACTION
		if target_id.begins_with("friend:"):
			var friend_index: int = int(touch_target.get("payload", -1))
			if friend_index >= 0 and friend_index < main.friends.size():
				var target_friend: Dictionary = main.friends[friend_index] as Dictionary
				if not bool(target_friend.get("won", false)):
					expected_affordance = Affordance.PLOT
		elif target_id == "reef:lagoon" and not main.level2_done_once:
			expected_affordance = Affordance.PLOT
		elif target_id == "reef:return" and main._all_friends_won():
			expected_affordance = Affordance.PLOT
		var actual_affordance: String = String(touch_target.get(
			"affordance_kind", ""))
		if actual_affordance != expected_affordance:
			_bad("world affordance category wrong for %s" % target_id)
			break
	if Affordance.RED_IDLE.a <= Affordance.BLUE_IDLE.a \
			or Affordance.emission_energy(Affordance.PLOT, false) \
				<= Affordance.emission_energy(Affordance.INTERACTION, false) \
			or Affordance.pulse_amount(Affordance.PLOT, false) \
				<= Affordance.pulse_amount(Affordance.INTERACTION, false):
		_bad("red plot beacon is not the most obvious affordance")

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
	var promenade_targets: Array = main.g.get("lagoon_promenade_targets", [])
	var promenade_ids: Dictionary = {}
	for target_value in promenade_targets:
		var promenade_target: Dictionary = target_value as Dictionary
		var promenade_id: String = String(promenade_target.get("id", ""))
		promenade_ids[promenade_id] = true
		var expected_affordance: String = Affordance.PLOT \
			if promenade_id == "castle_gate" else Affordance.ANIMATION
		var highlight: Sprite3D = promenade_target.get("highlight") as Sprite3D
		if String(promenade_target.get(
				"affordance_kind", "")) != expected_affordance:
			_bad("promenade affordance category wrong for %s" % promenade_id)
		elif highlight == null or not highlight.visible:
			_bad("promenade idle affordance hidden for %s" % promenade_id)
	for expected: String in ["slide", "swing", "seesaw", "castle_gate"]:
		if not promenade_ids.has(expected):
			_bad("promenade interaction missing %s" % expected)
	for removed_frame: String in ["runway_frame", "playground_frame", "castle_frame"]:
		if promenade_ids.has(removed_frame):
			_bad("removed lawn picture still interactive: %s" % removed_frame)
	if promenade_targets.size() < 4 or promenade_targets.size() > 5:
		_bad("promenade roster must be four permanent toys/landmarks plus optional Day One plane")

	# Exercise the first-visit Crown Star target, not the already-won keepsake.
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
		"family_gallery", "opera_hall", "kitchen", "library", "playroom",
		"craft_room", "mermaid_pool", "bubble_bath"]:
		if not main.castle_room_buttons.has(room_id):
			_bad("castle physical doorway missing %s" % room_id)
	if main.castle_room_world_root == null \
			or main.castle_room_camera == null \
			or main.castle_room_camera.projection != Camera3D.PROJECTION_PERSPECTIVE:
		_bad("castle did not build its perspective Sprite3D stage")
	if main.touch_ui.world_controls_enabled or main.player.visible:
		_bad("free-roaming 3D controls remained active inside castle stage")
	if main.touch_discovery_ring == null or main.touch_focus_ring == null:
		_bad("shared glow/focus visuals were not built")
	if main.castle_room_stage.get_node_or_null("ElevatorButton") != null \
			or main.castle_room_back_button == null:
		_bad("redundant room selector remained or contextual Back was missing")
	for dream_room_id: String in [
		"family_gallery", "dining_room", "royal_bedroom",
		"sleepover_bedroom", "movie_lounge"]:
		if rooms._room(dream_room_id).is_empty():
			_bad("dream-house room missing %s" % dream_room_id)
	if main.castle_room_link_layer == null:
		_bad("dream-house room-link layer was not built")
	elif main.castle_room_link_layer.get_child_count() != 0:
		_bad("floating dream-house route buttons remained")

	rooms.show_room("family_gallery", false)
	await _frames(2)
	if main.castle_room_detail_tiles.size() != 4 \
			or main.castle_room_action_button.visible:
		_bad("Dream House Wing did not build as a native physical gallery")
	var castle_affordance: Sprite3D = main.g.get(
		"castle_room_affordance") as Sprite3D
	if castle_affordance == null:
		_bad("castle shared affordance card missing")
	var dream_routes: Array[Dictionary] = [
		{"item": "gallery_dining_door", "child": "dining_room"},
		{"item": "gallery_royal_bedroom_door", "child": "royal_bedroom"},
		{"item": "gallery_sleepover_door", "child": "sleepover_bedroom"},
		{"item": "gallery_movie_door", "child": "movie_lounge"},
	]
	for route: Dictionary in dream_routes:
		var item_id: String = String(route["item"])
		var child_id: String = String(route["child"])
		var route_record: Dictionary = main.castle_room_item_sprites.get(
			item_id, {}) as Dictionary
		var door_sprite: Sprite3D = route_record.get("sprite") as Sprite3D
		var door_hotspot: Button = route_record.get("hotspot") as Button
		if door_sprite == null \
				or String(route_record.get(
					"affordance_kind", "")) != Affordance.INTERACTION \
				or String(door_sprite.get_meta(
					"room_destination", "")) != child_id \
				or not bool(door_sprite.get_meta(
					"castle_physical_door", false)) \
				or door_hotspot == null \
				or String(door_hotspot.get_meta(
					"room_destination", "")) != child_id \
				or not bool(door_hotspot.get_meta("physical_door", false)):
			_bad("physical dream-house doorway missing %s -> %s" % [
				item_id, child_id])
			continue
		door_hotspot.pressed.emit()
		var entered_room: bool = await _wait_for_castle_room(child_id)
		if not entered_room:
			_bad("dream-house doorway did not enter %s" % child_id)
			rooms.show_room("family_gallery", false)
			await _frames(2)
			continue
		main.castle_room_back_button.pressed.emit()
		await _frames(2)
		if main.castle_room_id != "family_gallery":
			_bad("dream-house Back did not return %s to gallery" % child_id)

	main.castle_room_back_button.pressed.emit()
	await _frames(2)
	if main.castle_room_id != "main_hall":
		_bad("Dream House Wing Back did not return to Main Hall")

	rooms.show_room("dining_room", false)
	await _frames(2)
	if main.castle_room_detail_tiles.size() != 4 \
			or not main.castle_room_item_sprites.has("dining_table") \
			or not main.castle_room_item_sprites.has("provisions_hutch"):
		_bad("family dining room did not build native tiles and meal furniture")
	var hutch_record: Dictionary = main.castle_room_item_sprites.get(
		"provisions_hutch", {}) as Dictionary
	if String(hutch_record.get("affordance_kind", "")) != Affordance.ANIMATION \
			or castle_affordance == null \
			or String(castle_affordance.get_meta(
				"affordance_kind", "")) != Affordance.ANIMATION:
		_bad("local castle prop missing gold animation affordance")
	rooms._activate_room_item("provisions_hutch")
	await process_frame
	var all_six_plates_visible := int(
		main.g.get("castle_dining_plates", 0)) == 6
	for plate_index in range(6):
		var plate_record: Dictionary = main.castle_room_item_sprites.get(
			"meal_plate_%d" % plate_index, {}) as Dictionary
		var plate_sprite: Sprite3D = plate_record.get("sprite") as Sprite3D
		all_six_plates_visible = all_six_plates_visible \
			and plate_sprite != null and plate_sprite.visible
	if not all_six_plates_visible:
		_bad("serving dinner did not set six visible places")
	rooms._activate_room_item("dining_table")
	await process_frame
	if int(main.g.get("castle_dining_plates", 0)) != 5:
		_bad("eating at the family table did not consume one place")

	rooms.show_room("royal_bedroom", false)
	await _frames(2)
	for bedroom_item: String in [
		"canopy_bed", "shell_wardrobe",
		"bedside_table", "reading_cushion"]:
		if not main.castle_room_item_sprites.has(bedroom_item):
			_bad("royal bedroom missing role-play prop %s" % bedroom_item)
	var was_night: bool = main.is_night
	var bed_record: Dictionary = main.castle_room_item_sprites.get(
		"canopy_bed", {}) as Dictionary
	var bed_sprite: Sprite3D = bed_record.get("sprite") as Sprite3D
	rooms._activate_room_item("canopy_bed")
	await process_frame
	var sleep_overlay: ColorRect = main.castle_room_stage.get_node_or_null(
		"DreamHouseSleepFade") as ColorRect
	var sleep_marks: Label = main.castle_room_stage.get_node_or_null(
		"DreamHouseSleepMarks") as Label
	if not bool(main.g.get("castle_roleplay_sleeping", false)) \
			or sleep_overlay == null or sleep_marks == null:
		_bad("touching a royal bed did not start the cosy sleep sequence")
	else:
		rooms._flip_roleplay_sleep_time()
		rooms._finish_roleplay_sleep(
			sleep_overlay, sleep_marks, bed_sprite)
		await process_frame
		if main.is_night == was_night \
				or bool(main.g.get("castle_roleplay_sleeping", false)):
			_bad("dream-house sleep did not wake and toggle time")

	rooms.show_room("sleepover_bedroom", false)
	await _frames(2)
	for dream_bed_id: String in [
		"dream_bed_0", "dream_bed_1", "dream_bed_2"]:
		var dream_bed_record: Dictionary = main.castle_room_item_sprites.get(
			dream_bed_id, {}) as Dictionary
		var dream_bed_sprite: Sprite3D = dream_bed_record.get(
			"sprite") as Sprite3D
		if dream_bed_sprite == null \
				or String(dream_bed_sprite.get_meta(
					"roleplay_action", "")) != "sleep":
			_bad("sleepover room missing working bed %s" % dream_bed_id)

	rooms.show_room("movie_lounge", false)
	await _frames(2)
	var picture_record: Dictionary = main.castle_room_item_sprites.get(
		"movie_picture", {}) as Dictionary
	var picture_sprite: Sprite3D = picture_record.get("sprite") as Sprite3D
	var movie_before: int = int(main.g.get("castle_movie_index", 0))
	rooms._activate_room_item("movie_screen")
	await process_frame
	var expected_movie: int = posmod(
		movie_before + 1, CastleRooms25D.MOVIE_IMAGES.size())
	if picture_sprite == null \
			or int(main.g.get("castle_movie_index", -1)) != expected_movie \
			or picture_sprite.texture.resource_path \
				!= CastleRooms25D.MOVIE_IMAGES[expected_movie] \
			or not bool(picture_sprite.get_meta(
				"protected_original_displayed_directly", false)):
		_bad("movie screen did not cycle direct protected home-movie art")
	for lounge_item: String in [
		"cloud_settee_left", "cloud_settee_right", "cloud_pouf"]:
		var lounge_record: Dictionary = main.castle_room_item_sprites.get(
			lounge_item, {}) as Dictionary
		var lounge_sprite: Sprite3D = lounge_record.get("sprite") as Sprite3D
		if lounge_sprite == null \
				or String(lounge_sprite.get_meta(
					"roleplay_action", "")) != "relax":
			_bad("movie lounge missing relaxing seat %s" % lounge_item)

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
	main.castle_room_back_button.pressed.emit()
	await _frames(2)
	if main.castle_room_id != "main_hall":
		_bad("room Back did not return to the Main Hall")
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

func _wait_for_castle_room(expected_room: String,
		timeout_ms: int = 1500) -> bool:
	var deadline: int = Time.get_ticks_msec() + timeout_ms
	while main.castle_room_id != expected_room \
			and Time.get_ticks_msec() < deadline:
		await process_frame
	return main.castle_room_id == expected_room

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
