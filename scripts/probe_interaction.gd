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
	var promenade_targets: Array = main.g.get("lagoon_promenade_targets", [])
	var promenade_ids: Dictionary = {}
	for target_value in promenade_targets:
		var promenade_target: Dictionary = target_value as Dictionary
		promenade_ids[String(promenade_target.get("id", ""))] = true
	for expected: String in ["slide", "swing", "seesaw", "castle_gate"]:
		if not promenade_ids.has(expected):
			_bad("promenade interaction missing %s" % expected)
	for removed_frame: String in ["runway_frame", "playground_frame", "castle_frame"]:
		if promenade_ids.has(removed_frame):
			_bad("removed lawn picture still interactive: %s" % removed_frame)
	if promenade_targets.size() < 4 or promenade_targets.size() > 5:
		_bad("promenade roster must be four permanent toys/landmarks plus optional Day One plane")

	# Fix regression: with the castle OPEN the door slab is parked ~30 units up
	# in the sky. court:castle must anchor at the doorway at walk height, and a
	# real screen-space tap on the ground-level archway must pick the castle —
	# not the secret back hatch through the walls.
	# Exercise the first-visit Crown Star target, not the already-won keepsake.
	main.level2_done_once = false
	main._enter_castle_interior_now(false)
	await _frames(24)
	main._populate_touch_interactables()
	var hall_ids := _ids()
	for expected: String in ["hall:bed", "hall:stand", "hall:exit", "hall:craft", "hall:wardrobe", "hall:bell_song", "hall:crown"]:
		if not hall_ids.has(expected):
			_bad("castle registry missing %s" % expected)
	if main.touch_discovery_ring == null or main.touch_focus_ring == null:
		_bad("shared glow/focus visuals were not built")

	# Hybrid advertises the music objective at proximity but starts it only
	# through its explicit Music Star target.
	var bellgame: Dictionary = main.g.get("bellgame", {})
	bellgame["state"] = "idle"
	bellgame["cool"] = 0.0
	main.player.position = (main.g.get("song_star", main.player.position) as Vector3) + Vector3(2.0, 0.0, 0.0)
	await _frames(8)
	if String(bellgame.get("state", "")) != "idle":
		_bad("Hybrid proximity auto-started the bell objective")
	main._activate_touch_interactable("hall:bell_song")
	await process_frame
	if String(bellgame.get("state", "")) != "play":
		_bad("explicit Music Star target did not start the bell objective")
	main._populate_touch_interactables()
	if _has_id_prefix("hall:bell:"):
		_bad("bell target remained advertised during song playback")
	# Playback completion must expose the bells in the exact frame that the
	# child is told "Your turn."
	bellgame["i"] = (bellgame.get("seq", []) as Array).size()
	bellgame["t"] = 0.0
	main._tick_bellgame(bellgame, 0.1, main.player.position)
	if String(bellgame.get("state", "")) != "echo" or not _has_id_prefix("hall:bell:"):
		_bad("play-to-echo transition did not expose bell targets immediately")
	# A wrong echo restarts playback and must remove those targets immediately.
	var sequence: Array = bellgame.get("seq", [])
	var wrong_note: int = (int(sequence[0]) + 1) % 7
	main._bellgame_echo(bellgame, wrong_note)
	if String(bellgame.get("state", "")) != "play" or _has_id_prefix("hall:bell:"):
		_bad("echo-to-play transition left stale bell targets")
	# The completed third round returns the free-play bells immediately.
	bellgame["state"] = "echo"
	bellgame["round"] = 3
	bellgame["seq"] = [0]
	bellgame["i"] = 0
	main._bellgame_echo(bellgame, 0)
	if String(bellgame.get("state", "")) != "idle" or not _has_id_prefix("hall:bell:"):
		_bad("bell completion did not restore free-play targets")

	# Modal cutscenes intentionally clear a held movement finger and keep world
	# controls blocked until their visual layer is gone.
	main.touch_ui.touch_owners[71] = 2   # TouchOwner.STICK
	main.touch_ui._press(Vector2(170.0, 550.0), 71)
	main.touch_ui._drag(Vector2(245.0, 520.0))
	main._begin_sleep()
	if main.touch_ui.world_controls_enabled or not main.touch_ui.touch_owners.is_empty() or not (main.touch_ui.stick_vec as Vector2).is_zero_approx():
		_bad("sleep cutscene retained held movement")
	main._populate_touch_interactables()
	if _ids().has("hall:bed"):
		_bad("sleep target remained restartable during cutscene")
	main._end_sleep()
	if not main.touch_ui.world_controls_enabled:
		_bad("world controls did not return after sleep")
	main.touch_ui.touch_owners[72] = 2   # TouchOwner.STICK
	main.touch_ui._press(Vector2(170.0, 550.0), 72)
	main.touch_ui._drag(Vector2(245.0, 520.0))
	main._play_hug_cutscene()
	if main.touch_ui.world_controls_enabled or not main.touch_ui.touch_owners.is_empty():
		_bad("hug cutscene retained held movement")
	main._end_hug_cutscene()
	await process_frame
	if not main.touch_ui.world_controls_enabled:
		_bad("world controls did not return after hug")

	# Pointer-driven 2D games own the whole screen. World controls must vanish
	# so the lower-right action bubble cannot cover a picture target.
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
	if not main.touch_ui.world_controls_enabled:
		_bad("world controls did not return after picture game")

	# Synchronous zone rebuilds clear focus/assist immediately and reject taps
	# until the black reveal finishes.
	main.touch_focus_id = "hall:bed"
	main.touch_auto_active = true
	main._return_to_courtyard()
	main._on_touch_world(main.get_viewport().get_visible_rect().size * 0.5)
	if not main.touch_focus_id.is_empty() or main.touch_auto_active:
		_bad("rapid transition tap retained or created stale navigation")
	if main.fade_rect != null and main.fade_rect.mouse_filter != Control.MOUSE_FILTER_STOP:
		_bad("fade cover did not claim touches during transition")
	await _frames(8)

	# Fix regression: leaving the castle mid-tuck-in (pause -> "Leave") must
	# unwind the sleep cutscene. Its reason-keyed "sleep" input block once
	# leaked and left every touch control dead until an app restart.
	main._enter_castle_interior_now(false)
	await _frames(12)
	main._begin_sleep()
	if main.touch_ui.world_controls_enabled:
		_bad("tuck-in did not take the sleep input block")
	main._exit_level2_now()
	await _frames(4)
	if not main.touch_ui.world_controls_enabled:
		_bad("leaving mid-sleep left touch controls dead (sleep block leak)")
	if float(main.sleep_t) >= 0.0 or main.sleep_layer != null:
		_bad("leaving mid-sleep left cutscene state armed")

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
