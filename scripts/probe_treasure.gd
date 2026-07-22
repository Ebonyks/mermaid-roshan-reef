extends SceneTree
# Dedicated win probe for the Secret Cave treasure game (split out of
# probe_audit.gd so an early audit death cannot silently drop coverage).
# Mirrors the audit driving: enter via wreck proximity, then chase the first
# unhit checkpoint star until the chest check awards +3 pearls and ends the
# game. treasure_fr["won"] starts true, so the pearl delta is the real gate.
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
	var player: Node3D = main.player
	print("TREASURE|boot OK wreck=", main.wreck_pos)
	main.treasure_cool = 0.0
	player.position = main.wreck_pos + Vector3(0, 4, 2)
	player.vel = Vector3.ZERO
	var waited := 0
	while main.game == "" and waited < 900:
		waited += 1
		player.position = main.wreck_pos + Vector3(0, 4, 2)
		player.vel = Vector3.ZERO
		await process_frame
	if main.game != "treasure":
		print("FAIL: treasure did not start (game=", main.game, " waited=", waited, ")")
		quit()
		return
	print("TREASURE|started after ", waited, " frames")
	var p0: int = main.pearl_count
	var fcount := 0
	var last_done := -1
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	while main.game != "" and fcount < 60 * 90:
		fcount += 1
		var g: Dictionary = main.g
		if String(g.get("phase", "")) != "slide":
			var checks: Array = g.get("checks", [])
			var done := 0
			for c in checks:
				if c["hit"]:
					done += 1
			if done != last_done or fcount % 900 == 0:
				print("TREASURE|f=", fcount, " sparkles=", done, "/", checks.size())
				last_done = done
			for c in checks:
				if not c["hit"]:
					player.position = player.position.lerp((c["node"] as Node3D).position, 0.10)
					player.vel = Vector3.ZERO
					break
		await process_frame
	print("END game=", main.game, " pearls=", main.pearl_count, " (start=", p0, ") frames=", fcount)
	if main.game != "" or main.pearl_count < p0 + 3:
		print("FAIL: treasure did not reach a win (frames=", fcount, ")")
	quit()
