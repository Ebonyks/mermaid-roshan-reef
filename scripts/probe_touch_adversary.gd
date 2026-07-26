extends SceneTree
# Twenty-five fresh-boot adversarial touch playthroughs. Each run attacks a
# different finger sequence and route slice, then prints its own feedback.
# The run is clear only when it finds no ownership leak, proximity hijack,
# missing zone verb, unreachable steering intent or rollback failure.

const RUN_COUNT := 25

var total_issues := 0

func _init() -> void:
	Engine.time_scale = 8.0
	for run_index in range(RUN_COUNT):
		await _playthrough(run_index)
	if total_issues == 0:
		print("TOUCH_ADVERSARY|ALL 25 PLAYTHROUGHS CLEAR")
	else:
		print("TOUCH_ADVERSARY|FAIL %d issue(s) across 25 playthroughs" % total_issues)
	quit()

func _playthrough(run_index: int) -> void:
	seed(2026072500 + run_index)
	var issues: Array[String] = []
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: Node3D = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(4)
	main._set_touch_mode("hybrid", false)
	main._populate_touch_interactables()

	var touch: CanvasLayer = main.touch_ui
	if touch == null or not touch.wants_touch():
		issues.append("touch router unavailable")
	else:
		var movement: Rect2 = touch.movement_zone()
		var action: Rect2 = touch.action_zone()
		if movement.intersects(action):
			issues.append("thumb zones overlap")
		# Validate against the rendered rest ring, not a fixed 1280x720
		# coordinate: script-mode headless viewports can use desktop dimensions.
		if not movement.encloses(touch.rest_zone().grow(18.0)):
			issues.append("normal left-thumb jitter escapes movement bay")

	# Adversarial child behavior: parking on a friend for several frames must
	# advertise without kidnapping the run into a minigame.
	var friend_index: int = run_index % mini(5, main.friends.size())
	var friend: Dictionary = main.friends[friend_index]
	var friend_node: Node3D = friend["node"]
	main.player.position = friend_node.position + Vector3(randf_range(2.0, 4.0), 0.0, randf_range(-1.0, 1.0))
	main.player.vel = Vector3.ZERO
	await _frames(12)
	if main.game != "":
		issues.append("proximity auto-started friend activity")

	# Screen-space target selection must tolerate a wandering fingertip.
	var camera: Camera3D = main.get_viewport().get_camera_3d()
	if camera == null:
		issues.append("camera missing")
	else:
		main._populate_touch_interactables()
		var projected: Vector2 = camera.unproject_position(friend_node.global_position)
		var finger_offset := Vector2(randf_range(-42.0, 42.0), randf_range(-42.0, 42.0))
		var picked: Dictionary = main._interaction_ref()._pick(projected + finger_offset)
		if String(picked.get("id", "")) != "friend:%d" % friend_index:
			issues.append("child-scale target miss")

	# Assisted travel must point toward the requested route and must cancel on
	# manual authority. Different quadrants cover every heading.
	var angle: float = TAU * float(run_index) / float(RUN_COUNT)
	var target: Vector3 = main.player.position + Vector3(sin(angle), 0.0, cos(angle)) * (24.0 + float(run_index % 4) * 9.0)
	main._tap_move_ref().start(target)
	var desired: Vector3 = main.touch_auto_direction()
	var expected: Vector3 = target - main.player.position
	expected.y = 0.0
	expected = expected.normalized()
	if desired.length() < 0.9 or desired.dot(expected) < 0.94:
		issues.append("assisted steering points away from tap")
	main._on_touch_manual_move()
	if main.touch_auto_active:
		issues.append("manual input failed to cancel assist")

	# Rotate through the long/occluded zones. The check is semantic: every
	# navigation-critical destination must be registered with a large,
	# non-reading-dependent verb and a discover range beyond its activation.
	match run_index % 4:
		0:
			_check_registry(main, ["reef:shop", "reef:treasure", "reef:slide", "reef:brawl", "reef:kart"], issues)
			var reef_actions: Array[String] = ["reef:shop", "reef:treasure", "reef:slide", "reef:brawl"]
			main._activate_touch_interactable(reef_actions[run_index % reef_actions.size()])
			await _frames(4)
			if main.game == "":
				issues.append("explicit reef action did not start")
			else:
				main._clear_game()
				await _frames(3)
		1:
			main.level2_done_once = true
			main._enter_level2_now(true, false, false)
			await _frames(12)
			main._populate_touch_interactables()
			_check_registry(main, ["court:castle", "court:north", "court:opera", "court:kart_a", "court:kart_b"], issues)
			if int(run_index / 4) % 2 == 0:
				var opera_gate: Dictionary = main.g.get("opera_gate", {})
				var opera_gate_pos: Vector3 = opera_gate.get("pos", Vector3.ZERO)
				main._activate_touch_interactable("court:opera")
				await _frames(4)
				if main.game != "opera" or main.opera_game == null:
					issues.append("explicit courtyard Opera target did not open")
				else:
					main.opera_game._leave_early()
					await _frames(4)
					if main.game != "level2" or String(main.g.get("phase", "")) != "court":
						issues.append("Opera exit did not restore courtyard")
					elif opera_gate_pos.distance_to(main.player.position) >= 9.0:
						issues.append("Opera exit did not return beside touch target")
			else:
				main._activate_touch_interactable("court:north")
				await _frames(10)
				if main.game != "north":
					issues.append("explicit courtyard route did not enter northern world")
		2:
			main.level2_done_once = true
			main._enter_level2_now(true, false, false)
			await _frames(8)
			main.level2_done_once = false
			main._enter_castle_interior_now(false)
			await _frames(12)
			main._populate_touch_interactables()
			_check_registry(main, ["hall:bed", "hall:exit", "hall:craft", "hall:wardrobe", "hall:crown"], issues)
			main._activate_touch_interactable("hall:crown")
			await _frames(3)
			if not bool(main.g.get("crown_won", false)):
				issues.append("explicit Crown Star did not award")
			main._activate_touch_interactable("hall:exit")
			await _frames(10)
			if main.game != "level2" or String(main.g.get("phase", "")) != "court":
				issues.append("explicit castle exit did not return to courtyard")
		3:
			main._enter_northern_kingdom()
			await _frames(12)
			main._populate_touch_interactables()
			_check_registry(main, ["north:return"], issues)
			main._activate_touch_interactable("north:return")
			await _frames(10)
			if main.game != "level2" or String(main.g.get("phase", "")) != "court":
				issues.append("explicit northern return did not reach courtyard")

	# Every run crosses the rollback boundary. No Hybrid assist/focus may
	# survive, and restoring Hybrid must remain possible without a reload.
	main._set_touch_mode("classic", false)
	if main.touch_uses_explicit_interactions() or main.touch_auto_active or not main.touch_focus_id.is_empty():
		issues.append("Classic rollback retained Hybrid state")
	main._set_touch_mode("hybrid", false)
	if not main.touch_uses_explicit_interactions():
		issues.append("Hybrid could not be restored")

	if issues.is_empty():
		print("TOUCH_ADVERSARY|RUN %02d|CLEAR — no touch difficulty" % (run_index + 1))
	else:
		total_issues += issues.size()
		print("TOUCH_ADVERSARY|RUN %02d|FAIL — %s" % [run_index + 1, "; ".join(issues)])
	main.queue_free()
	await _frames(3)

func _check_registry(main: Node3D, required: Array[String], issues: Array[String]) -> void:
	var by_id: Dictionary = {}
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		by_id[String(item.get("id", ""))] = item
	for required_id: String in required:
		if not by_id.has(required_id):
			issues.append("missing %s" % required_id)
			continue
		var item: Dictionary = by_id[required_id]
		if String(item.get("verb", "")).is_empty():
			issues.append("%s has no pictorial action verb" % required_id)
		if float(item.get("activation_radius", 0.0)) < 5.0:
			issues.append("%s target is too precise" % required_id)
		if float(item.get("discover_radius", 0.0)) <= float(item.get("activation_radius", 0.0)):
			issues.append("%s glows too late" % required_id)

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame
