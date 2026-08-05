extends SceneTree
# Twenty-five fresh-instance adversarial touch scenarios. Each run combines
# routed touch input, physical assisted movement and a different route slice,
# then prints its own feedback. This is broad automated stress coverage, not a
# substitute for twenty-five complete human/child sessions on the tablet.

const RUN_COUNT := 25

var total_issues := 0

func _init() -> void:
	Engine.time_scale = 8.0
	for run_index in range(RUN_COUNT):
		await _playthrough(run_index)
	if total_issues == 0:
		print("TOUCH_ADVERSARY|ALL 25 SCENARIO RUNS CLEAR")
		quit()
	else:
		print("TOUCH_ADVERSARY|FAIL %d issue(s) across 25 scenario runs" % total_issues)
		quit(1)

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
		touch.set_action_label("PLAY")
		if touch._act_lbl == null or not "\n" in String(touch._act_lbl.text):
			issues.append("action bubble lacks pictogram-plus-word cue")

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
		var touch_point: Vector2 = projected + finger_offset
		var picked: Dictionary = main._interaction_ref()._pick(touch_point)
		if String(picked.get("id", "")) != "friend:%d" % friend_index:
			issues.append("child-scale target miss")
		elif touch != null:
			if touch.movement_zone().has_point(touch_point) or touch.action_zone().has_point(touch_point):
				issues.append("friend target is hidden under a thumb control")
			else:
				_touch_tap(touch, run_index + 20, touch_point)
				await process_frame
				if main.touch_focus_id != "friend:%d" % friend_index:
					issues.append("routed first tap did not focus friend")
				if main.game != "":
					issues.append("routed first tap launched without confirmation")
				main._interaction_ref().clear_focus()

	# Assisted travel must physically move the existing player controller
	# toward the request. Different quadrants cover every heading.
	var angle: float = TAU * float(run_index) / float(RUN_COUNT)
	var target: Vector3 = main.player.position + Vector3(sin(angle), 0.0, cos(angle)) * 18.0
	var travel_start: Vector3 = main.player.position
	main._tap_move_ref().start(target)
	var routed_target: Vector3 = main.touch_auto_target
	var distance_before: float = _horizontal_distance(travel_start, routed_target)
	var desired: Vector3 = main.touch_auto_direction()
	var expected: Vector3 = routed_target - main.player.position
	expected.y = 0.0
	expected = expected.normalized()
	if desired.length() < 0.9 or desired.dot(expected) < 0.94:
		issues.append("assisted steering points away from tap")
	# Keep the physics portion at device-real delta. Eight-times time scale is
	# useful for world setup, but it can manufacture steering overshoot.
	Engine.time_scale = 1.0
	var early_position: Vector3 = travel_start
	for travel_frame in range(180):
		await process_frame
		if travel_frame == 99:
			early_position = main.player.position
		if not main.touch_auto_active:
			if travel_frame < 100:
				early_position = main.player.position
			break
	Engine.time_scale = 8.0
	var distance_after: float = _horizontal_distance(main.player.position, routed_target)
	var travel_distance: float = _horizontal_distance(travel_start, main.player.position)
	var early_distance: float = _horizontal_distance(travel_start, early_position)
	if early_distance < 1.5:
		issues.append("assisted steering lacked prompt physical response (moved %.1f by 1.7 s)" % early_distance)
	elif distance_after > distance_before - 4.0:
		issues.append("physical travel did not reduce route distance (moved %.1f, %.1f→%.1f)" % [travel_distance, distance_before, distance_after])
	main._tap_move_ref().start(main.player.position + Vector3(cos(angle), 0.0, -sin(angle)) * 22.0)
	main._on_touch_manual_move()
	if main.touch_auto_active:
		issues.append("manual input failed to cancel assist")
	# An immovable player must use the two side-step recoveries and then stop,
	# never swim forever against an obstacle.
	main._tap_move_ref().start(main.player.position + Vector3(32.0, 0.0, 0.0))
	for recovery_step in range(3):
		main._tap_move_ref().tick(1.2)
	if main.touch_auto_active:
		issues.append("blocked assisted route never relinquished control")

	# Rotate through the long/occluded zones. The check is semantic: every
	# navigation-critical destination must be registered with a large,
	# non-reading-dependent verb and a discover range beyond its activation.
	match run_index % 4:
		0:
			_check_registry(main, _reef_required(main), issues)
			var reef_actions: Array[String] = ["reef:slide", "reef:brawl"]
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
			var promenade_targets: Array = main.g.get("lagoon_promenade_targets", [])
			var promenade_ids: Dictionary = {}
			for target_value in promenade_targets:
				var promenade_target: Dictionary = target_value as Dictionary
				promenade_ids[String(promenade_target.get("id", ""))] = true
			var roster_ok: bool = promenade_targets.size() >= 4 \
				and promenade_targets.size() <= 5
			for required_id: String in ["slide", "swing", "seesaw", "castle_gate"]:
				roster_ok = roster_ok and promenade_ids.has(required_id)
			if String(main.g.get("phase", "")) != "promenade" or not roster_ok:
				issues.append("three-screen promenade interaction roster missing")
			else:
				var focus_target: Dictionary = {}
				var focus_id: String = "plane" if promenade_ids.has("plane") else "swing"
				for target_value in promenade_targets:
					var promenade_target: Dictionary = target_value as Dictionary
					if String(promenade_target.get("id", "")) == focus_id:
						focus_target = promenade_target
						break
				main._lagoon_promenade_ref()._focus(focus_target)
				if String(main.g.get("lagoon_promenade_focus", "")) != focus_id:
					issues.append("promenade first press did not focus")
				main._lagoon_promenade_ref()._activate(focus_target)
				await _frames(4)
				if main.game != "level2":
					issues.append("%s interaction left the promenade" % focus_id)
		2:
			main.level2_done_once = true
			main._enter_level2_now(true, false, false)
			await _frames(8)
			main.level2_done_once = false
			# This scenario audits the Crown route only; companion re-offer behavior
			# has dedicated coverage in probe_throne.
			main.companion_id = "birdie"
			main._enter_castle_interior_now(false)
			await _frames(12)
			main._populate_touch_interactables()
			var rooms: CastleRooms25D = main._castle_rooms_ref()
			if not rooms.is_open():
				issues.append("castle Sprite3D stage did not open")
			if not main.touch_interactables.is_empty():
				issues.append("retired 3D hall targets were registered")
			if main.castle_room_buttons.size() != 8 \
					or not main.castle_room_buttons.has("family_gallery") \
					or not main.castle_room_buttons.has("opera_hall") \
					or main.castle_room_stage.get_node_or_null(
						"ElevatorButton") == null \
					or main.castle_room_menu_buttons.size() != 12 \
					or not main.castle_room_menu_buttons.has("dining_room") \
					or not main.castle_room_menu_buttons.has("movie_lounge"):
				issues.append("castle room routes were missing or redundant")
			if main.castle_room_world_root == null \
					or main.castle_room_camera == null \
					or main.castle_room_camera.projection \
						!= Camera3D.PROJECTION_PERSPECTIVE:
				issues.append("castle lacks perspective Sprite3D stage")
			var elevator_button: Button = main.castle_room_stage.get_node_or_null(
				"ElevatorButton") as Button
			if elevator_button != null and main.castle_room_player_sprite != null:
				var elevator_foot_before: Vector2 = \
					main.castle_room_player_sprite.get_meta(
						"stage_foot", Vector2.ZERO) as Vector2
				elevator_button.pressed.emit()
				var blocked_tap := InputEventScreenTouch.new()
				blocked_tap.position = Vector2(640.0, 640.0)
				blocked_tap.pressed = true
				rooms._on_room_input(blocked_tap)
				await _frames(2)
				var elevator_foot_after: Vector2 = \
					main.castle_room_player_sprite.get_meta(
						"stage_foot", Vector2.ZERO) as Vector2
				if not main.castle_room_menu_open \
						or not elevator_foot_after.is_equal_approx(
							elevator_foot_before):
					issues.append("open castle elevator leaked taps into world travel")
				rooms._set_elevator_menu_open(false, false)
			rooms.show_room("main_hall", false)
			rooms.activate_current_room()
			var royal_hall_deadline_ms: int = Time.get_ticks_msec() + 3000
			while not bool(main.g.get("crown_won", false)) \
					and Time.get_ticks_msec() < royal_hall_deadline_ms:
				await process_frame
			if not bool(main.g.get("crown_won", false)):
				issues.append("eligible Royal Hall Crown event did not award")
			rooms._exit_to_courtyard()
			await _frames(10)
			if main.game != "level2" or String(main.g.get("phase", "")) != "promenade":
				issues.append("explicit castle exit did not return to promenade")
		3:
			main._enter_northern_kingdom()
			await _frames(12)
			main._populate_touch_interactables()
			_check_registry(main, ["north:return"], issues)
			main._activate_touch_interactable("north:return")
			await _frames(10)
			if main.game != "level2" or String(main.g.get("phase", "")) != "promenade":
				issues.append("explicit northern return did not reach promenade")

	# Every run crosses the rollback boundary. No Hybrid assist/focus may
	# survive, and restoring Hybrid must remain possible without a reload.
	main._set_touch_mode("classic", false)
	if main.touch_uses_explicit_interactions() or main.touch_auto_active or not main.touch_focus_id.is_empty():
		issues.append("Classic rollback retained Hybrid state")
	main._set_touch_mode("hybrid", false)
	if not main.touch_uses_explicit_interactions():
		issues.append("Hybrid could not be restored")

	if issues.is_empty():
		print("TOUCH_ADVERSARY|RUN %02d|CLEAR — no automated touch concern" % (run_index + 1))
	else:
		total_issues += issues.size()
		print("TOUCH_ADVERSARY|RUN %02d|FAIL — %s" % [run_index + 1, "; ".join(issues)])
	main.queue_free()
	await _frames(3)

func _touch_tap(touch: CanvasLayer, index: int, pos: Vector2) -> void:
	var down := InputEventScreenTouch.new()
	down.index = index
	down.position = pos
	down.pressed = true
	touch._unhandled_input(down)
	var up := InputEventScreenTouch.new()
	up.index = index
	up.position = pos
	up.pressed = false
	touch._unhandled_input(up)

func _reef_required(main: Node3D) -> Array[String]:
	var required: Array[String] = ["reef:slide", "reef:brawl", "reef:kart"]
	for friend_index in range(main.friends.size()):
		required.append("friend:%d" % friend_index)
	if main.portal_node != null and is_instance_valid(main.portal_node):
		required.append("reef:lagoon")
	if main.ocean_routes_enabled:
		required.append("reef:return")
	return required

func _court_required(main: Node3D) -> Array[String]:
	var required: Array[String] = ["court:north", "court:ember", "court:kart_a", "court:kart_b", "court:back_entry", "court:castle"]
	var gates: Array = main.g.get("ocean_kingdom_gates", [])
	for gate_index in range(gates.size()):
		required.append("court:ocean:%d" % gate_index)
	if main.galaxy_unlocked:
		required.append("court:galaxy")
	if main.l2_open:
		for picture_index in range(main.wall_pics.size()):
			required.append("court:picture:%d" % picture_index)
	for star_index in range(main.l2_stars.size()):
		if not bool((main.l2_stars[star_index] as Dictionary).get("got", false)):
			required.append("court:star:%d" % star_index)
	return required

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

func _has_registry_prefix(main: Node3D, prefix: String) -> bool:
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if String(item.get("id", "")).begins_with(prefix):
			return true
	return false

func _has_registry_id(main: Node3D, target_id: String) -> bool:
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if String(item.get("id", "")) == target_id:
			return true
	return false

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame

func _horizontal_distance(a: Vector3, b: Vector3) -> float:
	return Vector2(a.x - b.x, a.z - b.z).length()
