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
	var failed := false
	for kind in ["snowman", "garden", "trampoline", "slide", "xmas"]:
		main._mg2d_open(kind)
		await process_frame
		var t := 0.0
		var press_cd := 0.0
		while main.mg_kind == kind and t < 60.0:
			t += 1.0/60.0 * Engine.time_scale
			press_cd -= 1.0/60.0 * Engine.time_scale
			# The book-canon snowman ending is a movement chase, not another
			# button tap.  Steer toward the snowman (and then his carrot) so
			# this bot exercises the actual interaction instead of timing out.
			if kind == "snowman" and main.touch_ui != null and String(main.mg.get("phase", "")) in ["chase", "carrot"]:
				var chase_dir := signf(float(main.mg.get("run_x", 640.0)) - float(main.mg.get("chaser_x", 640.0)))
				main.touch_ui.stick_vec = Vector2(chase_dir, 0.0)
			elif main.touch_ui != null:
				main.touch_ui.stick_vec = Vector2.ZERO
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
		if main.mg_kind == "":
			results.append("%s: WON (%.1fs)" % [kind, t])
		else:
			failed = true
			results.append("%s: FAIL (STUCK at %.1fs)" % [kind, t])
		if main.mg_kind != "":
			main._mg2d_close()
		if main.touch_ui != null:
			main.touch_ui.stick_vec = Vector2.ZERO
		await process_frame
	print("=== STAGE 2 MINIGAME STRESS TEST ===")
	for r in results: print("  " + r)
	print("MG2D|done: ", "FAIL" if failed else "OK")
	quit()
