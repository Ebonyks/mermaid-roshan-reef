extends SceneTree
# Child-paced stress test of the four 2D picture games. The former slide card
# now delegates to the 3D race and is exercised by probe_audit instead.
func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	# No-input remains neutral even after the assist delay. A held virtual-stick
	# direction then activates the accessible roll fallback without auto-winning.
	main._mg2d_open("snowman")
	for _second in range(9):
		main.touch_ui.stick_vec = Vector2.ZERO
		main._tick_mg2d(1.0)
		await process_frame
	var passive_ok: bool = is_zero_approx(float(main.mg.get("rot_acc", -1.0))) and not bool(main.mg.get("motor_assist", false))
	main.touch_ui.stick_vec = Vector2.RIGHT
	for _second in range(9):
		main._tick_mg2d(1.0)
		await process_frame
	var assist_ok: bool = bool(main.mg.get("motor_assist", false)) and float(main.mg.get("rot_acc", 0.0)) > 0.0
	main.touch_ui.stick_vec = Vector2.ZERO
	var results := []
	var failed := not passive_ok or not assist_ok
	results.append("snow assist: %s" % ("OK" if passive_ok and assist_ok else "FAIL"))
	for kind in ["snowman", "garden", "trampoline", "xmas"]:
		if kind != "snowman":
			main._mg2d_open(kind)
			await process_frame
		var t := 0.0
		var press_cd := 0.0
		while main.mg_kind == kind and t < 60.0:
			t += 1.0/60.0 * Engine.time_scale
			press_cd -= 1.0/60.0 * Engine.time_scale
			# Perform each of the snowman's real touch verbs: circle the virtual
			# stick to roll all three balls, then chase the snowman and finally
			# eat his carrot nose (the book-canon ending).
			if kind == "snowman" and main.touch_ui != null:
				var snow_phase: String = String(main.mg.get("phase", ""))
				if snow_phase == "roll":
					var spin_ang: float = float(main.mg.get("t", 0.0)) * 2.4
					main.touch_ui.stick_vec = Vector2(cos(spin_ang), sin(spin_ang))
				elif snow_phase in ["chase", "carrot"]:
					var chase_dir: float = signf(float(main.mg.get("run_x", 640.0)) - float(main.mg.get("chaser_x", 640.0)))
					main.touch_ui.stick_vec = Vector2(chase_dir, 0.0)
				else:
					main.touch_ui.stick_vec = Vector2.ZERO
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
