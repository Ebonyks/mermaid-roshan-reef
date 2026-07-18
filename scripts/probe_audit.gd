extends SceneTree
# AUDIT BOT — corrected version of probe_games.gd (fixes stale cosmetics/tiara/tail
# and ColorRect casts). Prints incrementally so timeouts never lose results.
var main: Node3D
var player: Node3D

func _init() -> void:
	var seed_str := OS.get_environment("AUDIT_SEED")
	if seed_str != "":
		seed(int(seed_str))
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	player = main.player
	print("AUDIT|boot OK, seed=", seed_str)
	var patrol_x := 140.0
	var patrol_z := -115.0
	var patrol_y: float = main._aquatic_patrol_height(patrol_x, patrol_z, -100.0, 4.0)
	var aquatic_continuity: bool = (patrol_y >= main.seabed_y(patrol_x, patrol_z) + 3.99
		and patrol_y <= main.WATER_TOP - 3.0
		and is_equal_approx(main._aquatic_patrol_height(0.0, 0.0, 20.0), 20.0))
	print("AUDIT|Aquatic patrol terrain clearance: ", "OK" if aquatic_continuity else "FAIL")
	var lamb_continuity: bool = (not main._game_obj("seek", SeekGame)._lamb_meadow_placement_allowed(Vector2(0.0, 9.0), "tree_fat")
		and main._game_obj("seek", SeekGame)._lamb_meadow_placement_allowed(Vector2(25.0, 25.0), "tree_fat")
		and not main._game_obj("seek", SeekGame)._lamb_meadow_placement_allowed(Vector2(25.0, 25.0), "tree_palm"))
	print("AUDIT|Lamb meadow hide zones and climate: ", "OK" if lamb_continuity else "FAIL")
	print("AUDIT|Penguin floe at water surface: ",
		"OK" if absf(main.slide_portal_pos.y - (main.WATER_TOP + 0.5)) < 0.01 else "FAIL")
	var t_start := Time.get_ticks_msec()
	# --- Critter Book: approach + one real touch-action edge catches exactly one ---
	main.critter_collection = {}
	var collection: CollectionSystem = main._collection_ref()
	var first_critter: Dictionary = main.collection_nodes[0]
	var critter_node: Node3D = first_critter["node"]
	var critter_def: Dictionary = first_critter["def"]
	player.position = critter_node.position
	player.vel = Vector3.ZERO
	main.touch_ui.action_down = false
	await process_frame
	main.touch_ui.action_down = true
	await process_frame
	main.touch_ui.action_down = false
	var critter_ok: bool = collection.caught_count() == 1 and bool(main.critter_collection.get(String(critter_def["id"]), false))
	print("AUDIT|Critter Book: ", ("OK" if critter_ok else "FAIL"))
	for fi in range(5):
		var f: Dictionary = main.friends[fi]
		var fname: String = f["fname"]
		var node: Node3D = f["node"]
		player.position = node.position + Vector3(3, 0, 0)
		player.vel = Vector3.ZERO
		await _frames(10)
		var guard := 0
		while float(f["cool"]) > 0.0 and guard < 3000:
			guard += 1
			await process_frame
		for k in range(10):
			player.position = node.position + Vector3(3, 0, 0)
			player.vel = Vector3.ZERO
			await process_frame
		if main.game == "":
			print("AUDIT|", fname, ": GAME DID NOT START")
			continue
		var gname: String = main.game
		var cutaway_ok: bool = player.position.distance_to(main.ARENA_POS) <= 120.0
		if gname == "melody":
			var stage: Node = main.get_node_or_null("GabbyTheater3D")
			var stage_ok: bool = stage != null
			if stage_ok:
				var required := ["BackWall", "StageDeck", "RainbowArc0", "ProsceniumBulbs", "Runway", "TheaterSeats", "GabbyPerformer"]
				for child_name in required:
					if stage.get_node_or_null(String(child_name)) == null:
						stage_ok = false
						break
			print("AUDIT|Gabby 3D theater: ", ("OK" if stage_ok else "FAIL"))
		var f0 := Time.get_ticks_msec()
		var ok := await _drive_game(gname, f)
		var secs := float(Time.get_ticks_msec() - f0) / 1000.0
		print("AUDIT|", fname, " [", gname, "]: ", ("WON" if ok else "FAILED/TIMEOUT"),
			" cutaway=", cutaway_ok, " wall_s=%.1f" % secs)
		main._clear_game()
		await _frames(5)
	# --- treasure cavern ---
	main.treasure_cool = 0.0
	player.position = main.wreck_pos + Vector3(0, 4, 2)
	player.vel = Vector3.ZERO
	var waited := 0
	while main.game == "" and waited < 900:
		waited += 1
		player.position = main.wreck_pos + Vector3(0, 4, 2)
		player.vel = Vector3.ZERO
		await process_frame
	if main.game == "treasure":
		var p0: int = main.pearl_count
		var ok3 := await _drive_game("treasure", main.treasure_fr)
		print("AUDIT|Secret Cave [treasure]: ", ("WON +pearls" if ok3 and main.pearl_count >= p0 + 3 else "FAILED"))
	else:
		print("AUDIT|Secret Cave [treasure]: DID NOT START")
	# --- beans consumable (current shop API) ---
	main.pearl_count = 5
	main._shop_buy("beans")
	# beans banjo is a SOUND EFFECT now (dedicated beans_sfx player, works with
	# music off — explicit behaviour change requested earlier), so assert that
	# instead of the old cur_track swap
	var beans_on: bool = main.speed_mult == 2.0 and main.beans_t > 0.0 and main.beans_sfx != null and main.beans_sfx.playing and main.pearl_count == 3
	main.beans_t = 0.01
	for i5 in range(30):
		await process_frame
	var beans_off: bool = main.speed_mult == 1.0 and (main.beans_sfx == null or not main.beans_sfx.playing)
	print("AUDIT|Can of Beans: ", ("OK" if beans_on and beans_off else "FAIL on=%s off=%s" % [beans_on, beans_off]))
	# --- tank idle rigs (the turtle skeleton must actually flap) ---
	main._start_game(main.shop_fr)
	await _frames(10)
	var tanks: Array = main.g.get("tanks", [])
	var turtle_rig: Dictionary = {}
	for tk in tanks:
		if String(tk["id"]) == "turtle":
			turtle_rig = tk.get("rig", {})
	var rig_skel: Skeleton3D = turtle_rig.get("skel", null)
	var flap0 := Quaternion.IDENTITY
	if rig_skel != null:
		flap0 = rig_skel.get_bone_pose_rotation(3)
	await _frames(30)
	var flapped := false
	if rig_skel != null and is_instance_valid(rig_skel):
		flapped = rig_skel.get_bone_pose_rotation(3).angle_to(flap0) > 0.02
	var rig_line: String = "FAIL tanks=%d skel=%s flapped=%s" % [tanks.size(), rig_skel != null, flapped]
	if tanks.size() == 4 and rig_skel != null and rig_skel.get_bone_count() == 7 and flapped:
		rig_line = "OK bones=%d flapped=true" % rig_skel.get_bone_count()
	print("AUDIT|Tank idle rig: ", rig_line)
	main._clear_game()
	await _frames(5)
	# --- animal tanks (the pearl sink: buy the turtle free, it joins the reef) ---
	main.pearl_count = 30
	var movers0: int = main.aquatic_movers.size()
	main._tank_buy("turtle")
	var pets := 0
	var pets_rigged := 0
	for mv0 in main.aquatic_movers:
		if String(mv0.get("shop_pet", "")) == "turtle":
			pets += 1
			if mv0.has("rig"):
				pets_rigged += 1
	var tank_ok: bool = main.pearl_count == 5 and bool(main.animals_owned.get("turtle", false)) \
		and main.aquatic_movers.size() > movers0 and pets >= 1 and pets_rigged == pets
	main._tank_buy("turtle")   # already free: must not charge or double-spawn
	var tank_once: bool = main.pearl_count == 5 and main.aquatic_movers.size() == movers0 + pets
	main.pearl_count = 3
	main._tank_buy("dolphin")  # too few pearls: must not sell
	var tank_poor: bool = main.pearl_count == 3 and not bool(main.animals_owned.get("dolphin", false))
	var tank_line: String = "OK swimming=%d rigged=%d" % [pets, pets_rigged]
	if not (tank_ok and tank_once and tank_poor):
		tank_line = "FAIL buy=%s once=%s poor=%s pets=%d rigged=%d" % [tank_ok, tank_once, tank_poor, pets, pets_rigged]
	print("AUDIT|Animal tanks: ", tank_line)
	# --- pearl respawn ---
	var p1: Node3D = main.pearls[0]
	player.position = p1.position
	player.vel = Vector3.ZERO
	for i6 in range(10):
		await process_frame
	var collected: bool = main.pearls.size() == 9
	main._respawn_pearls()
	print("AUDIT|Pearl respawn: ", ("OK" if collected and main.pearls.size() == 10 else "FAIL"))
	# --- level 2 ---
	main.portal_unlocked = false
	main.pearl_count = main.PEARL_TOTAL - 1
	main.pearls_ever = main.PEARL_TOTAL - 1
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._check_level2_unlock(player.position, 0.1)
	print("AUDIT|Level 2 nine-pearl lock: ", ("OK" if not main.portal_unlocked and main.portal_node == null else "FAIL"))
	main.pearl_count = main.PEARL_TOTAL
	var pf := 0
	while main.portal_node == null and pf < 300:
		pf += 1
		main._check_level2_unlock(player.position, 0.1)
		await process_frame
	print("AUDIT|Level 2 portal: ", ("OK" if main.portal_node != null else "FAIL"))
	main.pearl_count = 0
	main._check_level2_unlock(player.position, 0.1)
	print("AUDIT|Level 2 portal stays unlocked after spending: ", ("OK" if main.portal_unlocked and main.portal_node != null else "FAIL"))
	if main.portal_node != null:
		var rf := 0
		while main.game == "" and rf < 600:
			rf += 1
			if not main.portal_armed:
				player.position = main.portal_node.position + Vector3(20, 6, 20)
			else:
				player.position = main.portal_node.position
			player.vel = Vector3.ZERO
			main._check_level2_unlock(player.position, 0.1)
			await process_frame
		print("AUDIT|Level 2 courtyard: ", ("OK" if main.game == "level2" else "FAIL"))
		# --- Phase 1 gate: star progress must survive a slide round-trip ---
		var sp_f := 0
		while _stars_got() < 2 and sp_f < 60 * 120 and main.game == "level2":
			sp_f += 1
			var tgt2: Node3D = null
			for sd2 in main.l2_stars:
				if not bool(sd2["got"]):
					tgt2 = sd2["node"]
					break
			if tgt2 != null:
				player.position = player.position.lerp(tgt2.position, 0.16)
				player.vel = Vector3.ZERO
			await process_frame
		main._l2_start_slide()
		await _frames(10)
		var slide_ok := await _drive_game(main.game, {"won": true})
		var back_f := 0
		while main.game != "level2" and back_f < 600:
			back_f += 1
			await process_frame
		print("AUDIT|L2 star persistence: ", ("OK" if _stars_got() == 2 else "FAIL"),
			" stars=", _stars_got(), " slide_won=", slide_ok)
		var cf := 0
		var interceptions := 0
		while cf < 60 * 240:
			cf += 1
			if main.game == "level2" and String(main.g.get("phase","court")) == "court":
				var tgt: Node3D = null
				for sd in main.l2_stars:
					if not bool(sd["got"]):
						tgt = sd["node"]
						break
				if tgt == null and main.l2_door != null:
					tgt = main.l2_door
				if tgt != null:
					player.position = player.position.lerp(tgt.position, 0.16)
					player.vel = Vector3.ZERO
			elif main.game == "level2" and String(main.g.get("phase","")) == "hall":
				break
			elif main.mg_kind != "":
				interceptions += 1
				main._mg2d_close()
				await _frames(10)
			elif main.game == "race" or main.game == "fairy":
				interceptions += 1
				var gname2: String = main.game
				await _drive_game(gname2, {"won": true})
				await _frames(30)
			elif main.game == "":
				await _frames(5)
			await process_frame
		print("AUDIT|Level 2 court interceptions: ", interceptions)
		var hall_ok: bool = main.game == "level2" and String(main.g.get("phase","")) == "hall"
		print("AUDIT|Level 2 castle hall: ", ("OK" if hall_ok else "FAIL"),
			" game=", main.game, " phase=", String(main.g.get("phase","?")),
			" mg_kind=", main.mg_kind, " stars_got=", _stars_got(), " l2_open=", main.l2_open)
		var hf := 0
		# the Crown Star celebrates IN PLACE now (owner 2026-07-12: winning
		# must not eject Roshan from her own castle) — drive to the crown,
		# then assert the WIN STATE (crown_won + saved level2 flag), not the
		# old return-to-ocean that the redesign explicitly removed
		while main.game == "level2" and not bool(main.g.get("crown_won", false)) and hf < 60 * 60:
			hf += 1
			var cr: Node3D = main.l2_stars[0]["node"]
			player.position = player.position.lerp(cr.position, 0.16)
			player.vel = Vector3.ZERO
			await process_frame
		print("AUDIT|Level 2 finish: ", ("OK" if bool(main.g.get("crown_won", false)) and bool(main.save_data.get("level2", false)) else "FAIL"))
	for i2 in range(60):
		await process_frame
	print("AUDIT|save file: ", ("OK" if FileAccess.file_exists("user://reef_save.json") else "MISSING"))
	print("AUDIT|finale: ", ("OK" if main.finale_done else "DID NOT TRIGGER"))
	var f3 := FileAccess.open("user://reef_save.json", FileAccess.READ)
	if f3 != null:
		var d3: Variant = JSON.parse_string(f3.get_as_text())
		if d3 is Dictionary:
			var wn: Dictionary = (d3 as Dictionary).get("won", {})
			var cnt := 0
			for k in wn:
				if bool(wn[k]):
					cnt += 1
			print("AUDIT|persisted wins: ", cnt, "/5")
	print("AUDIT|total wall time: %.1fs" % (float(Time.get_ticks_msec() - t_start) / 1000.0))
	quit()

func _stars_got() -> int:
	var got := 0
	for sd in main.l2_stars:
		if bool(sd["got"]):
			got += 1
	return got

func _frames(n: int):
	for i in range(n):
		await process_frame

func _drive_game(gname: String, f: Dictionary) -> bool:
	var deadline := 60.0 * 90.0
	var fcount := 0
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	while main.game != "" and fcount < deadline:
		fcount += 1
		var g: Dictionary = main.g
		if gname == "fetch":
			if g.has("phase") and String(g["phase"]) == "aim":
				var ad: Vector3 = g.get("aim_dir", Vector3.ZERO)
				main.touch_ui.action_down = ad != Vector3.ZERO and ad.x < 0.1 and fcount % 12 < 6
			else:
				main.touch_ui.action_down = false
		elif gname == "dolls":
			# Phase 6: perform the VERB — steer the catcher through the touch
			# stick like a real hand (teleporting the node no longer scores;
			# catches require live input inside the last 2s). Phase 8: the
			# catcher is the real 3D player on the side-scroll stage, babies
			# are Node3Ds falling toward stage-local y=0 — chase the LOWEST.
			var dolls: Array = g.get("dolls", [])
			if dolls.size() > 0:
				var lowest: Node3D = dolls[0]
				for d in dolls:
					if is_instance_valid(d) and (d as Node3D).global_position.y < lowest.global_position.y:
						lowest = d
				var want_x: float = lowest.global_position.x
				main.touch_ui.stick_vec = Vector2(clampf((want_x - main.player.global_position.x) / 3.6, -1.0, 1.0), 0.0)
			else:
				main.touch_ui.stick_vec = Vector2(0.3, 0.0)   # keep the hand 'live' between spawns
		elif gname == "seek":
			if g.has("bushes") and g.has("which"):
				var bush: Node3D = (g["bushes"] as Array)[int(g["which"])]
				player.position = player.position.lerp(bush.position, 0.15)
				player.vel = Vector3.ZERO
		elif gname == "slide":
			# Exercise the deliberate lean that the downhill ride requires.
			var weave: float = 0.65 if int(fcount / 45) % 2 == 0 else -0.65
			main.touch_ui.stick_vec = Vector2(weave, 0.0)
		elif gname == "race" or gname == "treasure":
			if String(g.get("phase", "")) != "slide":
				var checks: Array = g.get("checks", [])
				for c in checks:
					if not c["hit"]:
						player.position = player.position.lerp((c["node"] as Node3D).position, 0.10)
						player.vel = Vector3.ZERO
						break
		elif gname == "melody":
			var orbs: Array = g.get("orbs", [])
			for ob in orbs:
				if not bool(ob["caught"]):
					player.position = player.position.lerp((ob["node"] as Node3D).position, 0.14)
					player.vel = Vector3.ZERO
					break
		await process_frame
	main.touch_ui.stick_vec = Vector2.ZERO   # release the virtual hand
	return main.game == "" and bool(f["won"])
