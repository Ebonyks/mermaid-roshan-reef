extends SceneTree
# E1/E3 probe (ZELDA_GAMEPLAY_WORKORDER): scoop a starfish, toss it into a
# singing shell, earn a pearl, and confirm the star settles back to idle so
# the toy can be played again. Also asserts the scoop claims the ACTION press
# away from the jump (main ticks before the player, so the same press must
# not double as a swim-kick).
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
	var carry: CarrySystem = main._carry_ref()
	if carry == null or carry.stars.size() < 2 or carry.shells.size() < 2:
		print("FAIL: carry system missing props (stars=",
			carry.stars.size() if carry != null else -1, " shells=",
			carry.shells.size() if carry != null else -1, ")")
		quit()
		return
	print("carry props: ", carry.stars.size(), " stars, ", carry.shells.size(), " shells")
	var pl: Node3D = main.player
	var star: Dictionary = carry.stars[0]
	var snode: Node3D = star["node"]
	pl.position = snode.position + Vector3(2.0, 1.5, 0.0)
	pl.vel = Vector3.ZERO
	carry._action(pl.position)
	if String(star["state"]) != "held":
		print("FAIL: action near starfish did not scoop it (state=", star["state"], ")")
	if float(pl.jump_cool) < 0.3:
		print("FAIL: scoop did not claim the action press from the jump")
	# swim over to shell 0 (teleport), let the held star catch up to the
	# carry point in front of her, then aim square at the mouth and toss
	var sh: Dictionary = carry.shells[0]
	var mouth: Vector3 = sh["mouth"]
	pl.position = mouth + Vector3(-11.0, 0.5, 0.0)
	pl.yaw = atan2(mouth.x - pl.position.x, mouth.z - pl.position.z)
	var c_end: int = Time.get_ticks_msec() + 900   # wall-clock: the carry lerp is time-based
	while Time.get_ticks_msec() < c_end:
		await process_frame
	pl.yaw = atan2(mouth.x - pl.position.x, mouth.z - pl.position.z)
	pl.vel = Vector3.ZERO
	var pearls0: int = int(main.pearl_count)
	carry._action(pl.position)
	if String(star["state"]) != "fly":
		print("FAIL: second action did not throw the held star (state=", star["state"], ")")
	var hit := false
	var fly_end: int = Time.get_ticks_msec() + 8000
	while Time.get_ticks_msec() < fly_end:
		await process_frame
		if int(main.pearl_count) > pearls0:
			hit = true
			break
	if not hit:
		print("FAIL: thrown star never rang the shell (pearls unchanged)")
	else:
		print("carry: scoop/throw/sing ok (+", int(main.pearl_count) - pearls0, " pearl)")
	var settle_end: int = Time.get_ticks_msec() + 15000
	while Time.get_ticks_msec() < settle_end:
		await process_frame
		if String(star["state"]) == "idle":
			break
	if String(star["state"]) != "idle":
		print("FAIL: star stuck in state '", star["state"], "' after the toss")
	else:
		print("carry probe complete")
	quit()
