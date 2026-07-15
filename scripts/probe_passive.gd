extends SceneTree
# PASSIVE PROBE (Phase 6) — the negative twin of probe_audit.gd.
# Starts each of the five friend games, then provides NO input at all for
# 60 sim-seconds and asserts the game is NOT won. Forgiveness is right;
# zero-agency wins are not. Prints PASSIVE| lines; any FAIL fails CI.
var main: Node3D
var player: Node3D

func _init() -> void:
	seed(20260709)
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	player = main.player
	print("PASSIVE|boot OK")
	var bad := 0
	for fi in range(5):
		var f: Dictionary = main.friends[fi]
		var fname := String(f["fname"])
		var node: Node3D = f["node"]
		# approach only to START the game (starting is a greeting, not a win)
		player.position = node.position + Vector3(3, 0, 0)
		player.vel = Vector3.ZERO
		await _frames(10)
		var guard := 0
		while float(f["cool"]) > 0.0 and guard < 3000:
			guard += 1
			await process_frame
		for k in range(10):
			player.position = node.position + Vector3(3, 0, 0)
			player.vel = Vector3.ZERO
			await process_frame
		if main.game == "":
			print("PASSIVE|", fname, ": FAIL (game did not start)")
			bad += 1
			continue
		var gname := String(main.game)
		# park at the arena spawn, hands off everything, 60 sim-seconds
		player.position = main.ARENA_POS + Vector3(0, 8, 18)
		player.vel = Vector3.ZERO
		main.touch_ui.stick_vec = Vector2.ZERO
		main.touch_ui.action_down = false
		var won_before := bool(f["won"])
		var pearls_before: int = main.pearl_count
		var trophies_before: int = main.trophies
		var stickers_before: Dictionary = main.stickers.duplicate(true)
		while main.game != "" and float(main.g.get("t", 0.0)) < 60.0:
			await process_frame
		var still_running: bool = main.game != ""
		if still_running:
			main._clear_game()
			await _frames(5)
		var won_passively: bool = bool(f["won"]) and not won_before
		var progression_changed: bool = main.pearl_count != pearls_before or main.trophies != trophies_before or main.stickers != stickers_before
		if won_passively or progression_changed or not still_running:
			print("PASSIVE|", fname, " [", gname, "]: FAIL zero-input state won=", won_passively,
				" progression=", progression_changed, " still_running=", still_running)
			bad += 1
		else:
			print("PASSIVE|", fname, " [", gname, "]: OK active and unrewarded at 60s")
		await _frames(20)
	print("PASSIVE|result: ", ("ALL OK" if bad == 0 else "%d game(s) FAILED" % bad))
	quit()

func _frames(n: int):
	for i in range(n):
		await process_frame
