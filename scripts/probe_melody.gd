extends SceneTree
# Dedicated win probe for Gabby's melody orb-catch game (split out of
# probe_audit.gd so an early audit death cannot silently drop coverage).
# Mirrors the audit driving: lerp toward the first uncaught orb each frame —
# the lerp supplies the approach velocity the Phase 6 hold ring requires, so
# a stationary player can never fluke a catch. Win = all 7 colors caught.
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
	var fr: Dictionary = {}
	for f in main.friends:
		if String(f["game"]) == "melody":
			fr = f
	if fr.is_empty():
		print("FAIL: no melody friend found in main.friends")
		quit()
		return
	print("MELODY|boot OK friend=", fr["fname"])
	main._start_game(fr)
	await process_frame
	var fcount := 0
	var last_caught := -1
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	while main.game == "melody" and fcount < 60 * 90:
		fcount += 1
		var g: Dictionary = main.g
		var caught: int = int(g.get("caught", 0))
		if caught != last_caught or fcount % 900 == 0:
			print("MELODY|f=", fcount, " caught=", caught, "/7")
			last_caught = caught
		var orbs: Array = g.get("orbs", [])
		for ob in orbs:
			if not bool(ob["caught"]):
				player.position = player.position.lerp((ob["node"] as Node3D).position, 0.14)
				player.vel = Vector3.ZERO
				break
		await process_frame
	print("END game=", main.game, " won=", fr.get("won"), " frames=", fcount)
	if not bool(fr.get("won", false)):
		print("FAIL: melody did not reach a win (frames=", fcount, ")")
	quit()
