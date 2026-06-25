extends SceneTree
var main: Node3D
var player: Node3D
func _init() -> void:
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
	var results := []
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
		player.position = node.position + Vector3(3, 0, 0)
		player.vel = Vector3.ZERO
		for k in range(10):
			player.position = node.position + Vector3(3, 0, 0)
			await process_frame
		if main.game == "":
			results.append(fname + ": GAME DID NOT START")
			continue
		var gname: String = main.game
		if player.position.distance_to(main.ARENA_POS) > 120.0:
			results.append(fname + ": NO CUTAWAY")
		var ok := await _drive_game(gname, f)
		results.append(fname + " [" + gname + "]: " + ("WON" if ok else "FAILED/TIMEOUT"))
		main._clear_game()
		await _frames(5)
	# --- treasure cavern dive at the sunken wreck ---
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
		results.append("Secret Cave [treasure]: " + ("WON +pearls" if ok3 and main.pearl_count >= p0 + 3 else "FAILED"))
	else:
		results.append("Secret Cave [treasure]: DID NOT START")
	# --- pearl shop purchase ---
	main.pearl_count = 12
	main._shop_buy("tiara")
	var shop_ok: bool = bool(main.cosmetics.get("tiara", false)) and main.pearl_count == 8 and main.cosmetic_nodes.has("tiara")
	results.append("Pearl Shop [tiara]: " + ("OK (12 -> 8 pearls, crown on)" if shop_ok else "FAIL"))
	main.shop_cool = 0.0
	var w2 := 0
	while main.game == "" and w2 < 900:
		w2 += 1
		player.position = main.manta.position
		player.vel = Vector3.ZERO
		await process_frame
	if main.game == "shop":
		var bought_before: bool = bool(main.cosmetics.get("tail", false))
		var fc2 := 0
		while main.game == "shop" and fc2 < 60 * 60:
			fc2 += 1
			var target: Node3D = null
			for it in main.g.get("items", []):
				if String(it["id"]) == "tail" and (it["node"] as Node3D).visible:
					target = it["node"]
					break
			if target == null:
				# leave by swimming out the front of the room (boundary exit)
				player.position = main.ARENA_POS + Vector3(0, 4, 40)
				player.vel = Vector3.ZERO
				await process_frame
				continue
			player.position = player.position.lerp(target.position, 0.12)
			player.vel = Vector3.ZERO
			await process_frame
		var cabin_ok: bool = main.game == "" and bool(main.cosmetics.get("tail", false)) and not bought_before
		results.append("Shop cabin [walk-in]: " + ("OK (bought tail, left by door)" if cabin_ok else "FAIL"))
	else:
		results.append("Shop cabin [walk-in]: DID NOT OPEN")
	# --- beans: consumable speed boost ---
	main.pearl_count = 5
	main._shop_buy("beans")
	var beans_on: bool = main.speed_mult == 2.0 and main.beans_t > 0.0 and main.cur_track == "banjo" and main.pearl_count == 3
	main.beans_t = 0.01
	for i5 in range(20):
		await process_frame
	var beans_off: bool = main.speed_mult == 1.0 and main.cur_track != "banjo"
	results.append("Can of Beans: " + ("OK (2x zoom + banjo, then wore off)" if beans_on and beans_off else "FAIL on=%s off=%s" % [beans_on, beans_off]))
	# --- pearl respawn on stage complete ---
	var p1: Node3D = main.pearls[0]
	player.position = p1.position
	player.vel = Vector3.ZERO
	for i6 in range(10):
		await process_frame
	var collected: bool = main.pearls.size() == 9
	main._respawn_pearls()
	var respawned: bool = main.pearls.size() == 10
	results.append("Pearl respawn: " + ("OK (9 -> 10)" if collected and respawned else "FAIL c=%s r=%s" % [collected, respawned]))
	# --- LEVEL 2: portal unlock -> sky courtyard -> castle interior ---
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	var pf := 0
	while main.portal_node == null and pf < 300:
		pf += 1
		main._check_level2_unlock(player.position, 0.1)
		await process_frame
	var portal_ok: bool = main.portal_node != null
	# rise the portal then dive in
	var rf := 0
	while main.game == "" and rf < 600:
		rf += 1
		# first leave the radius to arm, then dive in
		if not main.portal_armed:
			player.position = main.portal_node.position + Vector3(20, 6, 20)
		else:
			player.position = main.portal_node.position
		player.vel = Vector3.ZERO
		main._check_level2_unlock(player.position, 0.1)
		await process_frame
	var court_ok: bool = main.game == "level2"
	# collect the 3 dream stars, then enter the door
	var cf := 0
	while main.game == "level2" and String(main.g.get("phase","court")) == "court" and cf < 60 * 90:
		cf += 1
		var tgt: Node3D = null
		for sd in main.l2_stars:
			if not bool(sd["got"]):
				tgt = sd["node"]
				break
		if tgt == null:
			tgt = main.l2_door
		player.position = player.position.lerp(tgt.position, 0.16)
		player.vel = Vector3.ZERO
		await process_frame
	var hall_ok: bool = main.game == "level2" and String(main.g.get("phase","")) == "hall"
	# reach the crown star in the hall
	var hf := 0
	while main.game == "level2" and hf < 60 * 60:
		hf += 1
		var cr: Node3D = main.l2_stars[0]["node"]
		player.position = player.position.lerp(cr.position, 0.16)
		player.vel = Vector3.ZERO
		await process_frame
	var finish_ok: bool = main.game == "" and bool(main.save_data.get("level2", false))
	results.append("Level 2 portal: " + ("OK" if portal_ok else "FAIL"))
	results.append("Level 2 courtyard: " + ("OK (warped in)" if court_ok else "FAIL"))
	results.append("Level 2 castle hall: " + ("OK (door -> interior)" if hall_ok else "FAIL"))
	results.append("Level 2 finish: " + ("OK (crown + saved)" if finish_ok else "FAIL"))
	print("=== MINIGAME BOT RESULTS ===")
	for r in results:
		print(r)
	print("trophies: ", main.trophies, "/5")
	for i2 in range(60):
		await process_frame
	var save_ok: bool = FileAccess.file_exists("user://reef_save.json")
	print("save file: ", "OK" if save_ok else "MISSING")
	print("finale: ", "OK" if main.finale_done else "DID NOT TRIGGER")
	var f3 := FileAccess.open("user://reef_save.json", FileAccess.READ)
	if f3 != null:
		var d3: Variant = JSON.parse_string(f3.get_as_text())
		if d3 is Dictionary:
			var wn: Dictionary = (d3 as Dictionary).get("won", {})
			var cnt := 0
			for k in wn:
				if bool(wn[k]):
					cnt += 1
			print("persisted wins: ", cnt, "/5")
	quit()
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
			var dolls: Array = g.get("dolls", [])
			if dolls.size() > 0 and main.dolls_catcher != null:
				var lowest: ColorRect = dolls[0]
				for d in dolls:
					if (d as ColorRect).position.y > lowest.position.y:
						lowest = d
				main.dolls_catcher.position.x = lerpf(main.dolls_catcher.position.x, lowest.position.x - 40.0, 0.3)
		elif gname == "seek":
			if g.has("bushes") and g.has("which"):
				var bush: Node3D = (g["bushes"] as Array)[int(g["which"])]
				player.position = player.position.lerp(bush.position, 0.15)
				player.vel = Vector3.ZERO
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
	return main.game == "" and bool(f["won"])
