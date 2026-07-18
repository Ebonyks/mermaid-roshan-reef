extends SceneTree
# E4 probe: reef currents. Rides the geyser lift from the seabed and asserts
# it carries her to the surface band, checks the field is zero far away, and
# that the geyser actually breathes (off phase exists) so nothing can be
# pinned in the column forever.
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
	var flow: ReefFlow = main._flow_ref()
	if flow == null:
		print("FAIL: no flow system")
		quit()
		return
	if flow.accel_at(Vector3(200.0, 30.0, 200.0)) != Vector3.ZERO:
		print("FAIL: current field is not zero far from every stream")
	var gx: float = float(flow.GEYSER["x"])
	var gz: float = float(flow.GEYSER["z"])
	# wait for the start of an ON phase so the ride gets the full 6 s window
	var waited := 0
	while not (flow.geyser_on() and fmod(Time.get_ticks_msec() / 1000.0, flow.GEYSER_CYCLE) < 1.0):
		waited += 1
		if waited > 900:
			print("FAIL: geyser never entered a fresh ON phase")
			quit()
			return
		await process_frame
	var pl: Node3D = main.player
	pl.position = Vector3(gx, main.seabed_y(gx, gz) + 4.0, gz)
	pl.vel = Vector3.ZERO
	var max_y := -999.0
	for i in range(360):
		await process_frame
		max_y = maxf(max_y, pl.position.y)
	if max_y < 50.0:
		print("FAIL: geyser ride peaked at y=", "%.1f" % max_y, " (wanted the surface band > 50)")
	else:
		print("flow: geyser lifted her to y=", "%.1f" % max_y)
	# the breathing gap: an OFF phase must exist within one cycle
	var saw_off := false
	for i in range(700):
		await process_frame
		if not flow.geyser_on():
			saw_off = true
			break
	if not saw_off:
		print("FAIL: geyser never turned off (bot-trap hazard)")
	else:
		print("flow probe complete")
	quit()
