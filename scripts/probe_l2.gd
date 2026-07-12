extends SceneTree
# Child-paced playtest of Level 2: wandering swim, ~0.6 reaction, no perfect aim.
func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"): main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	# force unlock + enter level 2
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends: f["found"]=true; f["won"]=true
	main.trophies = 5
	main._enter_level2()
	await process_frame
	var t := 0.0
	var got_log := []
	var last_got := 0
	var entered := false
	var wob := 0.0
	# done = the Crown Star win is recorded (crown celebrates IN PLACE since
	# f5d7689 — the game stays in level2 by design, no ocean eject)
	while main.game == "level2" and not bool(main.g.get("crown_won", false)) and t < 240.0:
		t += 1.0/60.0 * Engine.time_scale
		if main.mg_kind != "":
			main._mg2d_close()
			main.mg_cool = 15.0
			await process_frame
			continue
		if int(t) % 30 == 0 and int(t*6)%180==0:
			print("  dbg t=%.0f phase=%s game=%s" % [t, str(main.g.get("phase","?")), main.game])
		wob += 1.0/60.0 * Engine.time_scale
		var phase = String(main.g.get("phase","court"))
		if phase == "court":
			var got := 0
			var tgt: Node3D = null
			for sd in main.l2_stars:
				if bool(sd["got"]): got += 1
				elif tgt == null: tgt = sd["node"]
			if main.l2_open: tgt = main.l2_door
			if got != last_got:
				got_log.append("  star %d at t=%.1fs" % [got, t]); last_got = got
			if tgt != null:
				# wandering 4yo: drift toward target with sine wobble, slow speed
				var dir: Vector3 = (tgt.position - player.position)
				dir.y = 0
				if dir.length() > 0.5: dir = dir.normalized()
				var wb := Vector3(sin(wob*1.3)*0.5, 0, cos(wob*0.9)*0.5)
				player.vel = (dir + wb).normalized() * 14.0
		else:
			if not entered:
				got_log.append("  entered castle at t=%.1fs" % t); entered = true
			var cr: Node3D = main.l2_stars[0]["node"]
			var dir2: Vector3 = (cr.position - player.position)
			if dir2.length() > 0.5: dir2 = dir2.normalized()
			player.vel = dir2 * 14.0
		await process_frame
	print("=== LEVEL 2 CHILD-PACED STRESS TEST ===")
	for l in got_log: print(l)
	var won: bool = main.game == "" or bool(main.g.get("crown_won", false))
	print("  RESULT: %s in %.1fs sim-time" % [("COMPLETED" if won else "STUCK"), t])
	quit()
