extends SceneTree
# Child-paced stress test of the 5 Stage-2 minigames.
func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	var results := []
	for kind in ["snowman", "garden", "trampoline", "slide", "xmas"]:
		main._mg2d_open(kind)
		await process_frame
		var t := 0.0
		var press_cd := 0.0
		while main.mg_kind == kind and t < 60.0:
			t += 1.0/60.0 * Engine.time_scale
			press_cd -= 1.0/60.0 * Engine.time_scale
			# a 4yo taps roughly twice a second, hitting visible buttons
			if press_cd <= 0.0:
				press_cd = 0.5
				var btns: Array = main.mg.get("btns", [])
				for b in btns:
					if is_instance_valid(b) and b.visible and not b.disabled:
						b.pressed.emit()
						break
			main._tick_mg2d(1.0/60.0 * Engine.time_scale)
			await process_frame
		results.append("%s: %s (%.1fs)" % [kind, ("WON" if main.mg_kind == "" else "STUCK"), t])
		if main.mg_kind != "":
			main._mg2d_close()
		await process_frame
	print("=== STAGE 2 MINIGAME STRESS TEST ===")
	for r in results: print("  " + r)
	quit()
