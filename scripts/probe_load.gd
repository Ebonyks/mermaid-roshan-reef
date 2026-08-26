extends SceneTree
# verifies a saved session restores trophies/stars on boot,
# and that a crafted fish survives a relaunch (it used to vanish: the save
# loads after the reef builds, so build-time spawning missed it)
func _init() -> void:
	# opera_pantry (added 2026-07-25) must survive a save/load round trip
	var sd: Dictionary = {}
	if FileAccess.file_exists("user://reef_save.json"):
		var f := FileAccess.open("user://reef_save.json", FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if d is Dictionary:
				sd = d
	sd["custom_fish"] = [[0.9, 0.3, 0.3, 1.0, 0.8, 0.2]]   # one crafted fish in the save
	sd["animals"] = {"turtle": true}   # one tank friend already set free
	sd["critters"] = {"coral_clownfish": true}   # one Critter Book discovery
	sd["castle_logo_color"] = "purple"
	sd["castle_logo_symbol"] = "dog"
	# A pre-audit build could persist a friend as "resting" after its care
	# countdown expired. The key must remain readable, but loading it must
	# immediately return the friend with boo-boos/progress intact.
	sd["companion"] = "eagle"
	sd["companion_colors"] = ["f7b77f", "ffd86b", "fff2a0"]
	sd["fish_tokens"] = 2
	sd["care_points"] = 7
	sd["stuffie_wins"] = {"round1": true, "friend_lamma": true}
	sd["companion_resting"] = true
	sd["companion_bruises"] = 2
	# Stable Opera bits are deliberately sparse after boss retirement. Keep all
	# three historical tombstone bits plus Chef, while ignoring the stale linear
	# progress field a previous build may have written.
	sd["opera_stars"] = 0x4211
	sd["opera_progress"] = 16
	sd["opera_done"] = false
	var w := FileAccess.open("user://reef_save.json", FileAccess.WRITE)
	w.store_string(JSON.stringify(sd))
	w.close()
	var ps: PackedScene = load("res://scenes/main.tscn")
	var main := ps.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(12):
		await process_frame
	print("loaded trophies: ", main.trophies, "/5  finale_done: ", main.finale_done)
	var stars := 0
	for f in main.friends:
		if f.has("star"):
			stars += 1
	print("won stars shown: ", stars, "/5")
	var crafted := 0
	for mv in main.aquatic_movers:
		if bool(mv.get("crafted", false)):
			crafted += 1
	if crafted < 1:
		print("FAIL: crafted fish missing after reload (custom_fish in save, none swimming)")
	else:
		print("crafted fish restored: ", crafted)
	# a released tank friend must survive a relaunch (same build-before-load trap)
	var pets := 0
	var visible := 0
	for mv in main.aquatic_movers:
		if String(mv.get("shop_pet", "")) == "turtle":
			pets += 1
			var pet_node = mv.get("node", null)
			if pet_node != null and is_instance_valid(pet_node):
				visible += 1
	if pets < 1:
		print("FAIL: shop animal missing after reload (animals.turtle in save, none swimming)")
	elif visible < pets:
		print("FAIL: reloaded shop turtle missing its display card (%d/%d visible)" % [visible, pets])
	else:
		print("shop animals restored: ", pets, " (all display cards)")
	if not bool(main.critter_collection.get("coral_clownfish", false)):
		print("FAIL: Critter Book discovery missing after reload")
	else:
		print("Critter Book restored: coral_clownfish")
	if main.castle_logo_color != "purple" or main.castle_logo_symbol != "dog":
		print("FAIL: castle logo choice missing after reload")
	else:
		print("castle logo restored: purple puppy")
	var first_companion_ok: bool = _legacy_companion_ok(main, "first launch")
	var first_opera_ok: bool = _opera_mask_ok(main, "first launch")
	var first_write_ok: bool = main._write_save()
	var saved_healed: bool = first_write_ok \
		and not bool(main.save_data.get("companion_resting", true)) \
		and String(main.save_data.get("companion", "")) == "eagle" \
		and (main.save_data.get("companion_colors", []) as Array) \
			== ["f7b77f", "ffd86b", "fff2a0"] \
		and int(main.save_data.get("fish_tokens", -1)) == 2 \
		and int(main.save_data.get("care_points", -1)) == 7 \
		and int(main.save_data.get("companion_bruises", -1)) == 2 \
		and bool((main.save_data.get("stuffie_wins", {}) as Dictionary).get(
			"round1", false)) \
		and bool((main.save_data.get("stuffie_wins", {}) as Dictionary).get(
			"friend_lamma", false)) \
		and int(main.save_data.get("opera_stars", -1)) == 0x4211 \
		and int(main.save_data.get("opera_progress", -1)) == 1
	if saved_healed:
		print("legacy companion save rewrote only the retired resting flag")
	else:
		print("FAIL: healed legacy companion did not persist intact")
	main.queue_free()
	for _frame: int in range(3):
		await process_frame
	var relaunched := ps.instantiate() as ReefMain
	root.add_child(relaunched)
	await process_frame
	await process_frame
	relaunched._skip_intro()
	for _frame: int in range(12):
		await process_frame
	var second_companion_ok: bool = _legacy_companion_ok(
		relaunched, "second launch")
	var second_opera_ok: bool = _opera_mask_ok(relaunched, "second launch")
	quit(0 if first_companion_ok and first_opera_ok and saved_healed \
		and second_companion_ok and second_opera_ok else 1)


func _opera_mask_ok(main: ReefMain, label: String) -> bool:
	var ok: bool = main.opera_stars == 0x4211 \
		and main.opera_progress == 1 and not main.opera_done \
		and OperaHouse.live_star_count(main.opera_stars) == 1 \
		and not OperaHouse.has_all_live_stars(main.opera_stars)
	if ok:
		print("sparse Opera mask restored intact on ", label)
	else:
		print("FAIL: sparse Opera save mismatch on %s stars=%04X progress=%d done=%s" % [
			label, main.opera_stars, main.opera_progress, main.opera_done,
		])
	return ok

func _legacy_companion_ok(main: ReefMain, label: String) -> bool:
	var colors_ok: bool = main.companion_colors \
		== ["f7b77f", "ffd86b", "fff2a0"]
	var wins_ok: bool = bool(main.stuffie_wins.get("round1", false)) \
		and bool(main.stuffie_wins.get("friend_lamma", false))
	var pending_care: bool = main.companion_rest_timer > 0.0 \
		and (main.companion_want != "" \
			or not main.companion_want_queue.is_empty())
	var ok: bool = not main.companion_resting \
		and not bool(main.save_data.get("companion_resting", true)) \
		and main.companion_id == "eagle" and colors_ok \
		and main.fish_tokens == 2 and main.care_points == 7 \
		and main.companion_bruises == 2 \
		and wins_ok and pending_care \
		and main.companion_node != null \
		and is_instance_valid(main.companion_node)
	if ok:
		print("legacy resting companion recovered intact on ", label)
	else:
		print("FAIL: legacy companion recovery mismatch on %s " % label,
			"resting=", main.companion_resting,
			" id=", main.companion_id,
			" colors=", main.companion_colors,
			" tokens=", main.fish_tokens,
			" care=", main.care_points,
			" bruises=", main.companion_bruises,
			" wins=", main.stuffie_wins,
			" pending=", pending_care,
			" follower=", main.companion_node)
	return ok
