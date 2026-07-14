extends SceneTree
# Prints the waterline profile along each lagoon river (rim, floor, water). Dev-only.

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
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
	for i in range(10):
		await process_frame
	var lag = main._lagoon_ref()
	for ri in range(main.LAGOON_RIVERS.size()):
		var rv: Array = main.LAGOON_RIVERS[ri]
		print("--- river %d: %s ---" % [ri, str(rv)])
		for i in range(rv.size() - 1):
			var a2: Vector2 = rv[i]
			var b2: Vector2 = rv[i + 1]
			for si in range(8):
				var p2: Vector2 = a2.lerp(b2, float(si) / 8.0)
				var fl: float = lag._lagoon_local(p2.x, p2.y)
				var dp: float = lag._lagoon_river_dip(p2.x, p2.y)
				var wy: float = maxf(fl + 0.8, (fl + dp) - 1.5)
				print("  (%.0f,%.0f) floor=%.1f rim=%.1f water=%.1f" % [p2.x, p2.y, fl, fl + dp, wy])
	quit()
