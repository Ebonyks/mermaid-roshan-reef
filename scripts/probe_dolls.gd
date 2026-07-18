extends SceneTree
# Dedicated win probe for Faron's sleepy-dolls catch game (split out of
# probe_audit.gd so an early audit death cannot silently drop coverage).
# Phase 8: the game is a 2.5D nursery on the SideScrollStage engine — the
# catcher is the real 3D player on a left/right line, babies are Node3Ds
# falling toward stage-local y=0. Mirrors the audit driving: steer through
# the touch stick like a real hand — teleporting the node no longer scores;
# catches require live input inside the last 2s (Phase 6 verb). Win = 3
# dolls caught.
func _init() -> void:
	Engine.time_scale = 6.0
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var fr: Dictionary = {}
	for f in main.friends:
		if String(f["game"]) == "dolls":
			fr = f
	if fr.is_empty():
		print("FAIL: no dolls friend found in main.friends")
		quit()
		return
	print("DOLLS|boot OK friend=", fr["fname"])
	main._start_game(fr)
	await process_frame
	var fcount := 0
	var last_caught := -1
	while main.game == "dolls" and fcount < 60 * 90:
		fcount += 1
		var g: Dictionary = main.g
		var caught: int = int(g.get("caught", 0))
		if caught != last_caught or fcount % 900 == 0:
			print("DOLLS|f=", fcount, " caught=", caught, "/3 missed=", g.get("missed"))
			last_caught = caught
		var dolls: Array = g.get("dolls", [])
		if dolls.size() > 0:
			var lowest: Node3D = dolls[0]
			for d in dolls:
				if is_instance_valid(d) and (d as Node3D).global_position.y < lowest.global_position.y:
					lowest = d
			var want_x: float = lowest.global_position.x
			main.touch_ui.stick_vec = Vector2(clampf((want_x - main.player.global_position.x) / 3.6, -1.0, 1.0), 0.0)
		else:
			main.touch_ui.stick_vec = Vector2(0.3, 0.0)   # keep the hand 'live' between spawns
		await process_frame
	main.touch_ui.stick_vec = Vector2.ZERO   # release the virtual hand
	print("END game=", main.game, " won=", fr.get("won"), " frames=", fcount)
	if not bool(fr.get("won", false)):
		print("FAIL: dolls did not reach a win (frames=", fcount, ")")
	quit()
