extends SceneTree
# Numeric arm-mirror solver: for a set of right-arm raises, sweep the left
# upper-arm angle and report the value whose hand2 global position best
# mirrors hand across the sagittal plane. Same for the forearm bend.
# Dev-only; prints a table, no rendering (run --headless).

var main: Node
var pl: Node

func _hand_pos(skel: Skeleton3D, bname: String) -> Vector3:
	var bi: int = pl.bone_idx.get(bname, -1)
	return (skel.get_bone_global_pose(bi) as Transform3D).origin

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	pl = main.player
	pl.set_process(false)
	pl.set_physics_process(false)
	var skel: Skeleton3D = pl.skel
	print("=== ARM SOLVE ===")
	var can_force: bool = skel.has_method("force_update_all_dirty_bones")
	for amt: float in [0.4, 0.8, 1.1, 1.5, 1.9, 2.3]:
		pl._rot_bone("armU", Vector3.RIGHT, amt)
		pl._rot_bone("armF", Vector3.RIGHT, 0.0)
		pl._rot_bone("armF2", Vector3.RIGHT, 0.0)
		if can_force:
			skel.force_update_all_dirty_bones()
		else:
			await process_frame
		var target: Vector3 = _hand_pos(skel, "hand")
		target.x = -target.x
		var best_a := 0.0
		var best_e := 1e9
		var a := -0.5
		while a < 3.3:
			pl._rot_bone("armU2", Vector3.RIGHT, a)
			if can_force:
				skel.force_update_all_dirty_bones()
			else:
				await process_frame
			var e: float = (_hand_pos(skel, "hand2") - target).length()
			if e < best_e:
				best_e = e
				best_a = a
			a += 0.02
		print("armU %.2f -> armU2 %.2f (err %.3f)  [delta %+.2f]" % [amt, best_a, best_e, best_a - amt])
	# forearm bend mirror at a mid raise, using the solved upper answer above
	pl._rot_bone("armU", Vector3.RIGHT, 1.1)
	pl._rot_bone("armU2", Vector3.RIGHT, 2.1)
	for bend: float in [0.3, 0.55]:
		pl._rot_bone("armF", Vector3.RIGHT, bend)
		if can_force:
			skel.force_update_all_dirty_bones()
		else:
			await process_frame
		var target2: Vector3 = _hand_pos(skel, "hand")
		target2.x = -target2.x
		var best_b := 0.0
		var best_e2 := 1e9
		var b := -1.5
		while b < 1.6:
			pl._rot_bone("armF2", Vector3.RIGHT, b)
			if can_force:
				skel.force_update_all_dirty_bones()
			else:
				await process_frame
			var e2: float = (_hand_pos(skel, "hand2") - target2).length()
			if e2 < best_e2:
				best_e2 = e2
				best_b = b
			b += 0.02
		print("armF %.2f -> armF2 %.2f (err %.3f)" % [bend, best_b, best_e2])
	print("=== DONE ===")
	quit()
