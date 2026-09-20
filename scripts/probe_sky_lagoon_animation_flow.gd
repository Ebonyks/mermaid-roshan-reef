extends SceneTree
var main: ReefMain
var promenade: SkyLagoonPromenade
var failures: int = 0
func check(label: String, okay: bool) -> void:
	print("SKYFLOW|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280, 720)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	for frame: int in range(4):
		await process_frame
	if main.intro_active:
		main._skip_intro()
	main.day_one_active = false
	main._day_one_ref().clear_day_one_routing()
	main.save_data["lagoon_plane_departed"] = true
	main.g["lagoon_art_version"] = "animated_v1"
	main._enter_level2_now(true, false, false)
	main.set_process(false)
	promenade = main._lagoon_promenade_ref()
	check("preview_option_survives_build", String(main.g.get("lagoon_art_version_active", "")) == "animated_v1")
	var speed_ok: bool = true
	for from_x: float in [4800.0, 4850.0, 4950.0, 5100.0]:
		for direction: float in [-1.0, 1.0]:
			var next_x: float = promenade._advance_preview_route(from_x, from_x + 100.0 * direction, 7.9)
			var distance: float = promenade._route_point_for_x(from_x).distance_to(promenade._route_point_for_x(next_x))
			speed_ok = speed_ok and absf(distance - 7.9) < 0.01
	check("sloped_route_constant_speed_both_directions", speed_ok)
	var gate: Dictionary = promenade._target_by_id("castle_gate")
	var node: Node2D = gate["node"] as Node2D
	promenade.set_master_route_x(4520)
	var screen: Vector2 = promenade.screen_from_master(node.position)
	var save_before: String = JSON.stringify(main.save_data)
	promenade.handle_touch(screen)
	check("far_tap_requests_travel", main.g.get("lagoon_walk_goal_master") is Vector2 and String(main.g.get("phase", "")) == "promenade")
	for repeat: int in range(20):
		promenade.handle_touch(screen)
	check("repeat_taps_cannot_enter_remotely", String(main.g.get("phase", "")) == "promenade" and promenade.master_route_x() == 4520)
	promenade.cancel_navigation()
	for step: int in range(100):
		promenade._tick_movement(0.016)
		promenade._tick_doorstep()
	check("cancel_preserves_position_and_save", promenade.master_route_x() == 4520 and JSON.stringify(main.save_data) == save_before)
	promenade.handle_drag(screen - Vector2(100, 0), screen)
	check("door_drag_same_request", main.g.get("lagoon_walk_goal_master") == promenade.ANIMATED_ROUTE_MASTER[-1])
	var crossed: bool = false
	var entry_x: float = -1.0
	var entry_camera: float = -1.0
	for step: int in range(300):
		promenade._tick_movement(0.016)
		crossed = crossed or int(main.g.get("lagoon_bridge_play_count", 0)) > 0
		entry_x = promenade.master_route_x()
		entry_camera = float(main.g.get("lagoon_camera_x", -1.0))
		promenade._tick_doorstep()
		if String(main.g.get("phase", "")) == "hall":
			break
	check("door_arrival_after_bridge_contact", crossed and String(main.g.get("phase", "")) == "hall" and entry_x >= 5250)
	main._castle_rooms_ref()._go_back()
	promenade = main._lagoon_promenade_ref()
	check("exact_castle_return", String(main.g.get("phase", "")) == "promenade" and is_equal_approx(promenade.master_route_x(), entry_x) and is_equal_approx(float(main.g.get("lagoon_camera_x", -2.0)), entry_camera))
	promenade._tick_doorstep()
	check("return_does_not_reenter", String(main.g.get("phase", "")) == "promenade")
	var near_repeat_ok: bool = true
	for cycle: int in range(3):
		promenade.set_master_route_x(5270)
		var near_gate: Dictionary = promenade._target_by_id("castle_gate")
		var near_node: Node2D = near_gate["node"] as Node2D
		promenade.handle_touch(promenade.screen_from_master(near_node.position))
		promenade._tick_doorstep()
		near_repeat_ok = near_repeat_ok and String(main.g.get("phase", "")) == "hall"
		main._castle_rooms_ref()._go_back()
		promenade = main._lagoon_promenade_ref()
		near_repeat_ok = near_repeat_ok and is_equal_approx(promenade.master_route_x(), 5270.0)
		promenade._tick_doorstep()
		near_repeat_ok = near_repeat_ok and String(main.g.get("phase", "")) == "promenade"
	check("near_tap_reentry_and_return_three_cycles", near_repeat_ok)
	promenade.set_master_route_x(4520)
	var water_gate: Dictionary = promenade._target_by_id("castle_gate")
	promenade.handle_touch(promenade.screen_from_master((water_gate["node"] as Node2D).position))
	promenade.handle_touch(promenade.screen_from_master(Vector2(5600, 1400)))
	check("water_tap_cancels_old_door_request", main.g.get("lagoon_walk_goal_master") == null and String(main.g.get("lagoon_promenade_focus", "")) == "" and int(main.g.get("lagoon_water_emit_count", 0)) == 1)
	promenade.set_master_route_x(-1000)
	check("out_of_bounds_clamped", promenade.master_route_x() == promenade.ANIMATED_ROUTE_MASTER[0].x)
	promenade.set_master_route_x(4520)
	promenade.cancel_navigation()
	for step: int in range(1200):
		promenade._tick_movement(0.016)
		promenade._tick_doorstep()
	check("zero_input_does_not_enter", String(main.g.get("phase", "")) == "promenade" and promenade.master_route_x() == 4520)
	print("SKYFLOW|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
