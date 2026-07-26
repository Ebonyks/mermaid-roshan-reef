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

	# Exercise the first-visit Crown Star target, not the already-won keepsake.
	main.level2_done_once = false
	main._enter_castle_interior_now(false)
	await _frames(24)
	main._populate_touch_interactables()
	var hall_ids := _ids()
	for expected: String in ["hall:bed", "hall:stand", "hall:exit", "hall:craft", "hall:wardrobe", "hall:crown"]:
		if not hall_ids.has(expected):
			_bad("castle registry missing %s" % expected)
	if main.touch_discovery_ring == null or main.touch_focus_ring == null:
		_bad("shared glow/focus visuals were not built")

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

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame

func _bad(message: String) -> void:
	failures += 1
	print("INTERACTION|ISSUE ", message)

func _finish() -> void:
	if failures == 0:
		print("INTERACTION|ALL OK")
	else:
		print("INTERACTION|RESULT %d issue(s)" % failures)
	quit()
