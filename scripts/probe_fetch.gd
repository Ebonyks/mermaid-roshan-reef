extends SceneTree
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
		if String(f["game"]) == "fetch":
			fr = f
	main._start_game(fr)
	await process_frame
	var fcount := 0
	var last_phase := ""
	while main.game == "fetch" and fcount < 60 * 40:
		fcount += 1
		var g: Dictionary = main.g
		var ph := String(g.get("phase", "?"))
		if ph != last_phase:
			print("f=%d phase=%s round=%s miss=%s ballx=%.1f" % [fcount, ph, str(g.get("round")), str(g.get("miss")), (g["ball"] as Node3D).position.x - main.ARENA_POS.x])
			last_phase = ph
		if ph == "aim":
			var ad: Vector3 = g.get("aim_dir", Vector3.ZERO)
			main.touch_ui.action_down = ad != Vector3.ZERO and ad.x < 0.1 and fcount % 12 < 6
		else:
			main.touch_ui.action_down = false
		await process_frame
	print("END game=", main.game, " won=", fr.get("won"), " frames=", fcount)
	quit()
