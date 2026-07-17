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
	var river_depth: float = float(main.g.get("l2_river_min_depth", 0.0))
	print("STREAMS|minimum swim depth %.1f: %s" % [river_depth,
		"OK" if river_depth >= 4.0 else "FAIL"])
	var wayfinder_children: int = main.get_child_count()
	main._wayfind_t = 0.0
	main._tick_wayfinder(0.1, player.position)
	var wayfinder_ok: bool = (main._wayfind_t > 2.0
		and main.get_child_count() >= wayfinder_children + 3)
	print("WAYFINDER|Level 2 sparkle trail: ", "OK" if wayfinder_ok else "FAIL")
	_kart_gateway_regressions(main, player)
	# The Alpine addition must remain one distinct corner, clear of the train,
	# with its attached mountain and near-summit secret cave fully built.
	var alpine_ok: bool = (main.g.has("alpine_village_center")
		and main.g.has("alpine_mountain_center")
		and main.g.has("alpine_cave_entrance")
		and main.g.has("alpine_secret_pos"))
	if alpine_ok:
		var village: Vector3 = main.g["alpine_village_center"]
		var mountain: Vector3 = main.g["alpine_mountain_center"]
		var secret: Vector3 = main.g["alpine_secret_pos"]
		var vl: Vector3 = village - main.LEVEL2_POS
		var ml: Vector3 = mountain - main.LEVEL2_POS
		var sl: Vector3 = secret - main.LEVEL2_POS
		var train_clear: bool = Vector2(vl.x, vl.z + 120.0).length() > 90.0
		var attached: bool = Vector2(vl.x - ml.x, vl.z - ml.z).length() < 80.0
		alpine_ok = vl.x < -60.0 and vl.z < -140.0 and train_clear and attached and sl.y > 45.0
	print("ALPINE|corner + mountain + secret cave: ", "OK" if alpine_ok else "FAIL")
	# All three chalets must expose a clear front-to-centre corridor and place the
	# Blender habitat beyond the doorway, with its cage and animal separable.
	var houses_ok: bool = (main.g.has("alpine_house_entries")
		and main.g.has("alpine_house_bonuses"))
	var entries: Array = main.g.get("alpine_house_entries", [])
	var bonuses: Array = main.g.get("alpine_house_bonuses", [])
	houses_ok = houses_ok and entries.size() == 3 and bonuses.size() == 3
	var expected_kinds: Array[String] = ["fish", "insect", "bird"]
	var expected_cages: Array[String] = ["aquarium", "terrarium", "bird_cage"]
	if houses_ok:
		for house_index in range(3):
			var entry_data: Dictionary = entries[house_index]
			var bonus_data: Dictionary = bonuses[house_index]
			var entry_pos: Vector3 = entry_data["entry"]
			var inside_pos: Vector3 = entry_data["inside"]
			var bonus_pos: Vector3 = bonus_data["pos"]
			var habitat: Node3D = bonus_data["habitat"] as Node3D
			var cage: Node3D = bonus_data["cage"] as Node3D
			var animal: Node3D = bonus_data["node"] as Node3D
			houses_ok = (houses_ok
				and float(entry_data["door_width"]) >= 5.0
				and entry_pos.distance_to(inside_pos) < 7.0
				and bonus_pos.distance_to(inside_pos) < 6.0
				and bonus_pos.z < entry_pos.z
				and String(bonus_data["kind"]) == expected_kinds[house_index]
				and String(bonus_data["cage_kind"]) == expected_cages[house_index]
				and is_instance_valid(habitat)
				and is_instance_valid(cage)
				and is_instance_valid(animal)
				and String(animal.name) == "Collectible"
				and habitat.visible
				and cage.visible)
			for sample_index in range(7):
				var sample_pos: Vector3 = entry_pos.lerp(inside_pos,
					float(sample_index) / 6.0)
				if _arena_point_blocked(main, sample_pos):
					houses_ok = false
	# Exercise one real rescue twice: the first visit pays exactly once and hides
	# the animal/pointer, while its aquarium remains; lingering cannot farm pearls.
	var bonus_once_ok := false
	if bonuses.size() == 3:
		var first_bonus: Dictionary = bonuses[0]
		var first_key: String = first_bonus["key"]
		var first_node: Node3D = first_bonus["node"] as Node3D
		var first_halo: Node3D = first_bonus["halo"] as Node3D
		var first_cage: Node3D = first_bonus["cage"] as Node3D
		var first_habitat: Node3D = first_bonus["habitat"] as Node3D
		main.stickers.erase(first_key)
		first_bonus["claimed"] = false
		first_node.visible = true
		first_halo.visible = true
		var pearls_before: int = main.pearl_count
		main._lagoon_ref()._tick_alpine_house_bonuses(0.016, first_bonus["pos"])
		var pearls_after_first: int = main.pearl_count
		main._lagoon_ref()._tick_alpine_house_bonuses(0.016, first_bonus["pos"])
		bonus_once_ok = (pearls_after_first == pearls_before + 1
			and main.pearl_count == pearls_after_first
			and bool(main.stickers.get(first_key, false))
			and not first_node.visible
			and not first_halo.visible
			and first_cage.visible
			and first_habitat.visible)
	print("ALPINE HOUSES|walk-in + fish/insect/bird cages: ",
		"OK" if houses_ok and bonus_once_ok else "FAIL")
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
	print("  RESULT: %s in %.1fs sim-time" % [("COMPLETED" if won else "FAIL (STUCK)"), t])
	quit()


func _arena_point_blocked(main: Node, point: Vector3) -> bool:
	for value in main.arena_solids:
		var solid: Dictionary = value
		if point.y < float(solid["y0"]) or point.y > float(solid["y1"]):
			continue
		if bool(solid.get("box", false)):
			if (absf(point.x - float(solid["cx"])) <= float(solid["hx"])
				and absf(point.z - float(solid["cz"])) <= float(solid["hz"])):
				return true
		else:
			var dx: float = point.x - float(solid["x"])
			var dz: float = point.z - float(solid["z"])
			var radius: float = float(solid["r"])
			if dx * dx + dz * dz <= radius * radius:
				return true
	return false

func _kart_gateway_regressions(main: Node, player: Node3D) -> void:
	# Exercise the real Sky Lagoon portal logic without launching either large
	# destination. The world is already built for this probe, so this is cheap.
	var was_processing: bool = main.is_processing()
	var old_pos: Vector3 = player.position
	var old_vel: Vector3 = player.vel
	var old_galaxy: bool = bool(main.galaxy_unlocked)
	var old_float_armed: bool = bool(main.kart_float_portals_armed)
	var old_galaxy_armed: bool = bool(main.galaxy_gateway_armed)
	var old_kart_cool: float = float(main.kart_cool)
	var old_bw_cool: float = float(main.bw_cool)
	var old_intro: bool = bool(main.g.get("kart_intro", false))
	var old_t: float = float(main.g.get("t", 0.0))
	main.set_process(false)
	main.g["kart_intro"] = true

	main.kart_float_portals_armed = false
	main.kart_cool = 0.0
	main._tick_level2(0.0, main.kart_legA)
	var float_blocked: bool = main.game == "level2" and main.kart_game == null and not main.kart_float_portals_armed
	main._tick_level2(0.0, main.kart_legA + Vector3(24.0, 0.0, 0.0))
	var float_rearmed: bool = bool(main.kart_float_portals_armed)

	main.galaxy_unlocked = true
	main.galaxy_gateway_armed = false
	main.bw_cool = 0.0
	main.kart_cool = 0.0
	main._tick_level2(0.0, main.bw_portal_pos)
	var galaxy_blocked: bool = main.game == "level2" and main.galaxy_game == null and not main.galaxy_gateway_armed
	main._tick_level2(0.0, main.bw_portal_pos + Vector3(16.0, 0.0, 0.0))
	var galaxy_rearmed: bool = bool(main.galaxy_gateway_armed)

	# main owns the one cooldown decrement; SkyLagoon must not subtract it too.
	main.galaxy_unlocked = false
	main.kart_float_portals_armed = false
	main.galaxy_gateway_armed = false
	main.kart_cool = 6.0
	player.position = main.bw_portal_pos + Vector3(60.0, 60.0, 0.0)
	player.vel = Vector3.ZERO
	main._process(0.1)
	var single_cooldown: bool = is_equal_approx(float(main.kart_cool), 5.9)
	print("KARTGATES|float blocked/rearm=%s/%s galaxy blocked/rearm=%s/%s cooldown=%.1f" % [float_blocked, float_rearmed, galaxy_blocked, galaxy_rearmed, float(main.kart_cool)])
	if not float_blocked or not float_rearmed:
		print("FAIL|Sky Lagoon kart gate did not require leave + re-enter")
	if not galaxy_blocked or not galaxy_rearmed:
		print("FAIL|Butterfly World gate did not require leave + re-enter")
	if not single_cooldown:
		print("FAIL|kart cooldown decremented more than once in one Level 2 frame")

	player.position = old_pos
	player.vel = old_vel
	main.galaxy_unlocked = old_galaxy
	main.kart_float_portals_armed = old_float_armed
	main.galaxy_gateway_armed = old_galaxy_armed
	main.kart_cool = old_kart_cool
	main.bw_cool = old_bw_cool
	main.g["kart_intro"] = old_intro
	main.g["t"] = old_t
	main.set_process(was_processing)
