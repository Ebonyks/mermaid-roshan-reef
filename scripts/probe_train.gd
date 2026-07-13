extends SceneTree
# Courtyard-train probe (Sky Lagoon): the train must circle the castle for a
# full lap without EVER tripping its clip-guard (i.e. no situation where a
# car would intersect terrain or any pre-existing solid), stop at its
# station, carry Roshan glued to a seat while she rides, hide itself the
# moment the game leaves the courtyard phase, and never auto-board the
# zero-input headless player. Prints TRAIN|... OK/FAIL lines (CI greps FAIL).
func _init() -> void:
	Engine.time_scale = 4.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	await process_frame
	var tr: Dictionary = main.g.get("train", {})
	print("TRAIN|built: ", ("OK" if not tr.is_empty() else "FAIL (no g[train])"))
	if tr.is_empty():
		quit()
		return
	var cars: Array = tr["cars"]
	print("TRAIN|consist of 5 (engine+tender+coach+gondola+caboose): ",
		("OK" if cars.size() == 5 else "FAIL (%d)" % cars.size()))
	var seat_kinds: Array = []
	var cabin: Dictionary = {}
	for toy in (main.g.get("toys", []) as Array):
		var kind: String = String((toy as Dictionary)["kind"])
		if kind.begins_with("train"):
			seat_kinds.append(kind)
			if kind == "train_cabin":
				cabin = toy
	print("TRAIN|3 ride seats (1 cabin + 2 open-top): ",
		("OK" if seat_kinds.size() == 3 and not cabin.is_empty() else "FAIL (%s)" % str(seat_kinds)))
	# ---- full-lap clip sweep: crank the speed, drive a whole lap, and the
	# ---- guard must never need to hide the train (corridor really is clear)
	tr["spd_max"] = 55.0
	var lap: float = TAU * 78.0
	var travelled := 0.0
	var last_s: float = float(tr["s"])
	var clipped := false
	var dwelt: int = int(tr["dwells"])
	var t := 0.0
	while travelled < lap + 10.0 and t < 120.0:
		t += 1.0 / 60.0 * Engine.time_scale
		var s_now: float = float(tr["s"])
		travelled += fposmod(s_now - last_s, lap)
		last_s = s_now
		if bool(tr["hidden"]):
			clipped = true
		await process_frame
	print("TRAIN|full lap with zero clip-guard hides: ",
		("OK" if (not clipped and travelled >= lap) else "FAIL (hidden=%s travelled=%.0f)" % [str(clipped), travelled]))
	print("TRAIN|station dwell on the lap: ",
		("OK" if int(tr["dwells"]) > dwelt else "FAIL"))
	# every car must sit ON the ring (railhead between grade and viaduct top)
	var y_ok := true
	var o: Vector3 = tr["o"]
	for car in cars:
		var ly: float = ((car as Dictionary)["node"] as Node3D).global_position.y - o.y
		if ly < -1.0 or ly > 12.0:
			y_ok = false
	print("TRAIN|cars ride the railhead (grade..viaduct band): ", ("OK" if y_ok else "FAIL"))
	# ---- zero-input safety: headless never auto-boards a seat ----
	tr["spd_max"] = 8.0
	player.position = cabin["anchor"]
	for k in range(40):
		await process_frame
	print("TRAIN|headless never auto-boards (passive-safe): ",
		("OK" if (main.toy_play as Dictionary).is_empty() else "FAIL"))
	# ---- ride: board the cabin seat the way the trigger does, then she must
	# ---- stay glued to the moving seat and be CARRIED by the train. Wait for
	# ---- a clear running stretch first, so the station dwell can't park the
	# ---- train mid-measurement.
	var wait_t := 0.0
	while wait_t < 60.0:
		wait_t += 1.0 / 60.0 * Engine.time_scale
		var d_st: float = fposmod(1.6 * 78.0 - float(tr["s"]), lap)
		if String(tr["state"]) == "run" and d_st > 60.0:
			break
		await process_frame
	main.toy_play = {"kind": cabin["kind"], "toy": cabin, "t": 0.0, "dur": 6.0, "ph": 0.0,
		"from": player.position, "yaw0": float(player.yaw)}
	var start_p: Vector3 = ((cabin["node"] as Node3D).to_global(cabin["seat"] as Vector3))
	var glued := true
	var rt := 0.0
	while rt < 3.0:
		rt += 1.0 / 60.0 * Engine.time_scale
		await process_frame
		if rt > 0.8:
			var seat_p: Vector3 = (cabin["node"] as Node3D).to_global(cabin["seat"] as Vector3)
			if player.position.distance_to(seat_p) > 4.0:
				glued = false
	var end_p: Vector3 = ((cabin["node"] as Node3D).to_global(cabin["seat"] as Vector3))
	var carried: float = Vector2(end_p.x - start_p.x, end_p.z - start_p.z).length()
	print("TRAIN|riding stays glued to the cabin seat: ", ("OK" if glued else "FAIL"))
	print("TRAIN|the train carries her (moved %.1f): " % carried, ("OK" if carried > 6.0 else "FAIL"))
	main.toy_play = {}
	player.rotation.x = 0.0
	await process_frame
	# ---- entering the castle must make the train disappear entirely ----
	# (the hall build frees every courtyard node and clears the moving
	# solids; the phase gate in _tick_train is the belt-and-braces hide)
	main._enter_castle_interior()
	for k in range(20):
		await process_frame
	var eng: Node3D = (cars[0] as Dictionary)["node"]
	var gone: bool = bool(tr["hidden"]) and (not is_instance_valid(eng) or not eng.visible)
	print("TRAIN|disappears on castle entry (hall phase): ", ("OK" if gone else "FAIL"))
	# ---- and a fresh train is rebuilt when she steps back out ----
	main._enter_level2(true)
	for k in range(30):
		await process_frame
	var tr2: Dictionary = main.g.get("train", {})
	var back: bool = not tr2.is_empty() and not bool(tr2["hidden"]) \
		and is_instance_valid(((tr2["cars"] as Array)[0] as Dictionary)["node"])
	print("TRAIN|rebuilt back in the courtyard: ", ("OK" if back else "FAIL"))
	print("=== TRAIN PROBE DONE ===")
	quit()
