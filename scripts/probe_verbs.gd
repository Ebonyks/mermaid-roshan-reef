extends SceneTree
# R2-C verb layer probe: every verb in player.VERB_LIB must visibly move its
# signature bone while playing and hand the skeleton back to the procedural
# swim when done. Catches broken keys, bad bone names, and verbs that stick.
func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(20):
		await process_frame
	var pl: Node = main.player
	if pl == null or pl.skel == null:
		print("FAIL: no player/skeleton for verb probe")
		quit()
		return
	if pl.play_verb("nonsense"):
		print("FAIL: play_verb accepted an unknown verb")
	for vname in pl.VERB_LIB:
		var spec: Dictionary = pl.VERB_LIB[vname]
		var sig: Array = spec["sig"]
		var bi: int = pl.bone_idx.get(sig[0], -1)
		if bi < 0:
			print("FAIL: verb ", vname, " signature bone missing: ", sig[0])
			continue
		var rest_q: Quaternion = (pl.rest[sig[0]] as Transform3D).basis.get_rotation_quaternion()
		if not pl.play_verb(vname):
			print("FAIL: play_verb rejected ", vname)
			continue
		var t0: int = Time.get_ticks_msec()
		var maxdev := 0.0
		var deadline: int = t0 + int((float(spec["len"]) + 2.5) * 1000.0)
		while String(pl.verb) == vname and Time.get_ticks_msec() < deadline:
			var rel: Quaternion = rest_q.inverse() * pl.skel.get_bone_pose_rotation(bi)
			var ang: float = rel.get_angle()
			if ang > PI:
				ang = TAU - ang
			maxdev = maxf(maxdev, ang)
			await process_frame
		if String(pl.verb) == vname:
			print("FAIL: verb ", vname, " never finished (stuck)")
		elif maxdev < float(sig[1]):
			print("FAIL: verb ", vname, " barely moved ", sig[0],
				" (", "%.2f" % maxdev, " < ", sig[1], " rad)")
		else:
			print("verb ", vname, ": ok (", sig[0], " peaked %.2f rad)" % maxdev)
		for i in range(30):
			await process_frame
	print("verb probe complete")
	quit()
