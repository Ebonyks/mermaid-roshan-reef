extends SceneTree
# Drives the Go-Kart Cove race like a small child: full throttle, steering
# corrected toward the lane tangent with sloppy gain, until the 2 laps finish.
func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"): main._skip_intro()
	await process_frame
	main._start_game(main.gokart_fr)
	await process_frame
	print("game started: ", main.game == "gokart")
	var t := 0.0
	var best_lap := 0.0
	while main.game == "gokart" and t < 260.0:
		t += 1.0 / 60.0 * Engine.time_scale
		# a 4yo's driving: hold the stick up, let the lane assist steer
		main.touch_ui.stick_vec = Vector2(0.0, -1.0)
		best_lap = maxf(best_lap, float(main.g.get("lap_ang", 0.0)) / TAU)
		await process_frame
	main.touch_ui.stick_vec = Vector2.ZERO
	print("=== GO-KART PROBE ===")
	print("  laps reached: %.2f   finished: %s   t=%.1fs" % [best_lap, str(main.game != "gokart"), t])
	print("  RESULT: %s" % ("WON" if best_lap >= 1.99 and main.game == "" else "STUCK"))
	quit()
