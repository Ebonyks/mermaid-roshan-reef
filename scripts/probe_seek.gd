extends SceneTree
# Dedicated win probe for Evie and Lamb-a's hide and seek game (split out of
# probe_audit.gd so an early audit death cannot silently drop coverage).
# Mirrors the audit driving: lerp toward the wiggly bush g["bushes"][g["which"]]
# — a find needs real movement from the seek anchor plus proximity inside the
# growing help radius. Win = Lamb-a' found 4 times.
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
		if String(f["game"]) == "seek":
			fr = f
	if fr.is_empty():
		print("FAIL: no seek friend found in main.friends")
		quit()
		return
	print("SEEK|boot OK friend=", fr["fname"])
	main._start_game(fr)
	await process_frame
	var fcount := 0
	var last_found := -1
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	while main.game == "seek" and fcount < 60 * 90:
		fcount += 1
		var g: Dictionary = main.g
		var found: int = int(g.get("found", 0))
		if found != last_found or fcount % 900 == 0:
			print("SEEK|f=", fcount, " found=", found, "/4 which=", g.get("which"))
			last_found = found
		if g.has("bushes") and g.has("which"):
			var bush: Node3D = (g["bushes"] as Array)[int(g["which"])]
			player.position = player.position.lerp(bush.position, 0.15)
			player.vel = Vector3.ZERO
		await process_frame
	print("END game=", main.game, " won=", fr.get("won"), " frames=", fcount)
	if not bool(fr.get("won", false)):
		print("FAIL: seek did not reach a win (frames=", fcount, ")")
	quit()
