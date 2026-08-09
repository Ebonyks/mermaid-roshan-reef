extends SceneTree
# Regression probe for the double-generated lagoon: the rainbow-road/galaxy
# return re-enters level2 on top of the live one. Enters level2 twice (the
# second time exactly like the kart/galaxy return does) and compares the
# scene-tree node count — a duplicated build roughly doubles it.
# Prints OK/FAIL lines (ci.sh convention).

var main: Node

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _frames(30)
	var n1: int = get_node_count()
	var targets1: int = (main.g.get("lagoon_promenade_targets", []) as Array).size()
	# the galaxy/kart return path: re-enter WITHOUT any manual teardown
	main._enter_level2(true)
	await _frames(30)
	var n2: int = get_node_count()
	var targets2: int = (main.g.get("lagoon_promenade_targets", []) as Array).size()
	print("REENTER|nodes first=%d second=%d targets=%d/%d" % [n1, n2, targets1, targets2])
	# Re-entry is safe when the rebuilt three-screen promenade has the same
	# interaction roster and the scene tree stays within the original
	# anti-duplication tolerance.
	# The picture easels were removed on 2026-07-29. The persistent roster is
	# the Reef route plane, slide, single-seat swing, seesaw, and castle door. The
	# full Day One arrival shrinks to the permanent plane shuttle without
	# changing that five-target interaction contract.
	var ok: bool = targets1 == 5 and targets2 == 5 \
		and n2 <= n1 + int(float(n1) * 0.1)
	print("REENTER|no_duplicate_level: ", ("OK" if ok else "FAIL"))
	quit()
