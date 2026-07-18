extends SceneTree
# E2 probe: the push-block grotto. Verifies a real swim-push moves a block
# one grid cell, solves the rest through the same slide path the pushes use,
# and asserts the win fires exactly once (pads lit, +5 pearls, done latch).
func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(30):
		await process_frame
	var g: GrottoPuzzle = main._grotto_ref()
	if g == null or g.blocks.size() != 2 or g.pads.size() != 2:
		print("FAIL: grotto missing pieces")
		quit()
		return
	if g.done:
		print("FAIL: grotto started already-won (probe_passive hazard)")
	var pl: Node3D = main.player
	# 1. physical push: park her against block 0's west face, swimming east
	var b0: Dictionary = g.blocks[0]
	var start_cell: Vector2i = b0["cell"]
	for i in range(90):
		var bp: Vector3 = (b0["node"] as Node3D).position
		pl.position = bp + Vector3(-3.2, 0.0, 0.0)
		pl.vel = Vector3(8.0, 0.0, 0.0)
		await process_frame
		if Vector2i(b0["cell"]) != start_cell:
			break
	if Vector2i(b0["cell"]) == start_cell:
		print("FAIL: sustained swim-push never slid the block")
	else:
		print("grotto: swim-push slid block to ", b0["cell"])
	pl.vel = Vector3.ZERO
	pl.position = Vector3(g.CENTER.x, g.floor_y + 26.0, g.CENTER.z)
	# 2. solve via the same slide path pushes use
	var pearls0: int = int(main.pearl_count)
	var moves := 0
	while not g.done and moves < 12:
		moves += 1
		var moving := false
		for b in g.blocks:
			if float(b["move_t"]) >= 0.0:
				moving = true
		if moving:
			for i in range(30):
				await process_frame
			continue
		var advanced := false
		for bi in range(g.blocks.size()):
			var b: Dictionary = g.blocks[bi]
			var target: Vector2i = g.PADS[bi]
			var c: Vector2i = b["cell"]
			if c == target:
				continue
			var stepc := Vector2i(signi(target.x - c.x), 0)
			if stepc.x == 0:
				stepc = Vector2i(0, signi(target.y - c.y))
			if g._try_slide(b, stepc):
				advanced = true
				break
			# blocked (other block in the way): route around via the free row
			var alt := Vector2i(0, signi(target.y - c.y)) if stepc.x != 0 else Vector2i(signi(target.x - c.x), 0)
			if alt != Vector2i(0, 0) and g._try_slide(b, alt):
				advanced = true
				break
		for i in range(30):
			await process_frame
		if not advanced and not g.done:
			continue
	if not g.done:
		print("FAIL: grotto never reported done after ", moves, " solve moves")
	elif int(main.pearl_count) - pearls0 < 5:
		print("FAIL: grotto win paid ", int(main.pearl_count) - pearls0, " pearls (wanted 5)")
	else:
		print("grotto: solved, +", int(main.pearl_count) - pearls0, " pearls")
	# 3. the win must latch: nudge a block off and back, no double reward
	var pearls1: int = int(main.pearl_count)
	var bb: Dictionary = g.blocks[0]
	g._try_slide(bb, Vector2i(0, -1))
	for i in range(40):
		await process_frame
	g._try_slide(bb, Vector2i(0, 1))
	for i in range(40):
		await process_frame
	if int(main.pearl_count) != pearls1:
		print("FAIL: grotto re-rewarded after the win latch")
	else:
		print("grotto probe complete")
	quit()
