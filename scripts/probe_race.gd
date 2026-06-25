extends SceneTree
func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"): main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	var fr: Dictionary = {}
	for f in main.friends:
		if String(f["game"]) == "race": fr = f
	main._start_game(fr)
	await process_frame
	var t := 0.0; var last := 0; var log := []; var wob := 0.0
	while main.game == "race" and t < 200.0:
		t += 1.0/60.0*Engine.time_scale; wob += 1.0/60.0*Engine.time_scale
		var checks: Array = main.g.get("checks", [])
		var done := 0; var nxt = null
		for c in checks:
			if c["hit"]: done += 1
			elif nxt == null: nxt = c
		if done != last: log.append("  checkpoint %d at t=%.1fs" % [done, t]); last = done
		if String(main.g.get("phase","")) != "slide" and nxt != null:
			var tgt: Vector3 = (nxt["node"] as Node3D).position
			var dir: Vector3 = (tgt - player.position)
			if dir.length() > 0.5: dir = dir.normalized()
			var wb := Vector3(sin(wob*1.4)*0.6, 0, cos(wob*1.0)*0.6)  # wandering 4yo
			player.vel = (dir + wb).normalized() * 13.0
		await process_frame
	print("=== HARPER PLAY-PLACE CHILD-PACED TEST ===")
	for l in log: print(l)
	print("  RESULT: %s at t=%.1fs" % [("WON" if fr.get("won") else "STUCK"), t])
	quit()
