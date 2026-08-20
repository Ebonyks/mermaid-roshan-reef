extends SceneTree
# PASSIVE PROBE (Phase 6) — the negative twin of probe_audit.gd.
# Starts each of the five friend games, then provides NO input at all for
# 60 sim-seconds and asserts the game is NOT won. It also checks the special
# Fairy, Penguin Slide and Shop agency gates. Forgiveness is right; zero-agency
# wins or purchases are not. Prints PASSIVE| lines; any FAIL fails CI.
var main: Node3D
var player: Node3D

func _init() -> void:
	seed(20260709)
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
	print("PASSIVE|boot OK")
	var bad := 0
	# Ambient critters may sparkle and move, but zero input can never add them.
	main.critter_collection = {}
	main.touch_ui.action_down = false
	await _frames(120)
	if main._collection_ref().caught_count() != 0:
		print("PASSIVE|Critter Book: FAIL collected with zero input")
		bad += 1
	else:
		print("PASSIVE|Critter Book: OK not collected")
	for fi in range(5):
		var f: Dictionary = main.friends[fi]
		var fname := String(f["fname"])
		var node: Node3D = f["node"]
		# Proximity advertises in Hybrid but must never launch an activity.
		player.position = node.position + Vector3(3, 0, 0)
		player.vel = Vector3.ZERO
		await _frames(10)
		if main.touch_uses_explicit_interactions():
			if main.game != "":
				print("PASSIVE|", fname, ": FAIL proximity auto-started in Hybrid")
				bad += 1
				main._clear_game()
				await _frames(5)
			else:
				print("PASSIVE|", fname, ": OK proximity only advertises")
		var guard := 0
		while float(f["cool"]) > 0.0 and guard < 3000:
			guard += 1
			await process_frame
		for k in range(10):
			player.position = node.position + Vector3(3, 0, 0)
			player.vel = Vector3.ZERO
			await process_frame
		if main.game == "" and main.touch_uses_explicit_interactions():
			main._activate_touch_interactable("friend:%d" % fi, fi)
			await _frames(10)
		if main.game == "":
			print("PASSIVE|", fname, ": FAIL (game did not start)")
			bad += 1
			continue
		var gname := String(main.game)
		# Park arena activities at their spawn. Opaque Canvas routes must preserve
		# their real friend-route return coordinate untouched.
		if gname not in ["melody", "slide"]:
			player.position = main.ARENA_POS + Vector3(0, 8, 18)
			player.vel = Vector3.ZERO
			main.touch_ui.stick_vec = Vector2.ZERO
			main.touch_ui.action_down = false
		var won_before := bool(f["won"])
		var pearls_before: int = main.pearl_count
		var trophies_before: int = main.trophies
		var stickers_before: Dictionary = main.stickers.duplicate(true)
		var medals_before: Dictionary = main.medals.duplicate(true)
		var save_generation_before: int = main.save_generation
		var save_fingerprint_before: String = _save_fingerprint()
		while main.game != "" and float(main.g.get("t", 0.0)) < 60.0:
			await process_frame
		var still_running: bool = main.game != ""
		var activity_progressed := false
		var melody_passive_contract := true
		var slide_passive_contract := true
		if gname == "melody":
			var melody := main._game_obj("melody", MelodyGame) as MelodyGame
			activity_progressed = melody.progress_count() != 0
			melody_passive_contract = melody.active_layer() != null \
				and melody.surface() != null and melody.note_count() == 7 \
				and melody.active_note_id() >= 0 \
				and int(main.g.get("caught", -1)) == 0 \
				and float(main.g.get("t", 0.0)) >= 60.0
		elif gname == "slide":
			var slide := main._game_obj("race", SlideRaceGame) as SlideRaceGame
			var snapshot: Dictionary = slide.audit_snapshot()
			slide_passive_contract = slide.active_layer() != null \
				and slide.stage_root() != null and slide.fish_count() == 5 \
				and String(main.g.get("mode", "")) == "fish" \
				and not bool(main.g.get("steered", true)) \
				and slide.progress_count() < slide.fish_count() \
				and not bool(snapshot.get("completed", true)) \
				and bool(snapshot.get("no_fail_state", false)) \
				and float(main.g.get("t", 0.0)) >= 60.0
		var save_unchanged: bool = main.save_generation == save_generation_before \
			and _save_fingerprint() == save_fingerprint_before
		if still_running:
			main._clear_game()
			await _frames(5)
		var won_passively: bool = bool(f["won"]) and not won_before
		var progression_changed: bool = main.pearl_count != pearls_before or main.trophies != trophies_before or main.stickers != stickers_before or main.medals != medals_before
		if won_passively or progression_changed or activity_progressed \
				or not still_running or not melody_passive_contract \
				or not slide_passive_contract or not save_unchanged:
			print("PASSIVE|", fname, " [", gname, "]: FAIL zero-input state won=", won_passively,
				" progression=", progression_changed,
				" activity_progress=", activity_progressed,
				" surface=", melody_passive_contract and slide_passive_contract,
				" save=", save_unchanged,
				" still_running=", still_running)
			bad += 1
		else:
			print("PASSIVE|", fname, " [", gname, "]: OK active and unrewarded at 60s")
		await _frames(20)
	var shop_bad: int = await _probe_shop_agency()
	bad += shop_bad
	var slide_bad: int = await _probe_penguin_agency()
	bad += slide_bad
	var fairy_bad: int = await _probe_fairy_agency()
	bad += fairy_bad
	var brawl_bad: int = await _probe_brawl_agency()
	bad += brawl_bad
	bad += _probe_companion_patient_care()
	# Water-FX cards are EVENT effects (fx_water.gd): the swell, sleeping-prop
	# sway and every other ambient channel must never proc one. Zero input
	# across this whole run therefore means zero cards, ever.
	if int(main.fxw_total) != 0:
		print("PASSIVE|Water FX: FAIL ", main.fxw_total, " event card(s) with zero input")
		bad += 1
	else:
		print("PASSIVE|Water FX: OK ambient channels proc nothing")
	print("PASSIVE|result: ", ("ALL OK" if bad == 0 else "%d game(s) FAILED" % bad))
	quit()

func _frames(n: int):
	for i in range(n):
		await process_frame


func _save_fingerprint() -> String:
	var path := "user://reef_save.json"
	return FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"

func _progress_snapshot() -> Dictionary:
	var stickers_now: Dictionary = main.stickers
	var shop_now: Dictionary = main.shop_owned
	var animals_now: Dictionary = main.animals_owned
	var medals_now: Dictionary = main.medals
	return {
		"pearls": int(main.pearl_count),
		"trophies": int(main.trophies),
		"stickers": stickers_now.duplicate(true),
		"shop": shop_now.duplicate(true),
		"animals": animals_now.duplicate(true),
		"medals": medals_now.duplicate(true),
	}

func _progress_unchanged(before: Dictionary) -> bool:
	return int(main.pearl_count) == int(before["pearls"]) \
		and int(main.trophies) == int(before["trophies"]) \
		and main.stickers == before["stickers"] \
		and main.shop_owned == before["shop"] \
		and main.animals_owned == before["animals"] \
		and main.medals == before["medals"]

func _probe_companion_patient_care() -> int:
	# The retired 120-second send-home path was a zero-input failure. Cross that
	# boundary with the real care clock and prove that waiting changes nothing
	# except the non-blocking reminder cadence.
	main.companion_id = "eagle"
	main.companion_colors = ["f7b77f", "ffd86b", "fff2a0"]
	main.companion_resting = false
	var companion: CompanionSystem = main._companion_ref()
	companion.tick(0.0)
	if main.companion_node == null or not is_instance_valid(main.companion_node):
		print("PASSIVE|Stuffie patient care: FAIL follower did not spawn")
		return 1
	main.companion_bruises = 2
	companion.after_battle(false)
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	main.touch_ui.action_just = false
	var follower_before: int = main.companion_node.get_instance_id()
	var companion_before: String = main.companion_id
	var colors_before: Array = main.companion_colors.duplicate(true)
	var bruises_before: int = main.companion_bruises
	var tokens_before: int = main.fish_tokens
	var care_before: int = main.care_points
	var wins_before: Dictionary = main.stuffie_wins.duplicate(true)
	var progress_before: Dictionary = _progress_snapshot()
	for _second: int in range(181):
		companion._tick_care(1.0)
	var follower_present: bool = main.companion_node != null \
		and is_instance_valid(main.companion_node) \
		and main.companion_node.get_instance_id() == follower_before \
		and main.companion_node.visible
	var invitation_present: bool = main.companion_want != "" \
		and main.companion_want_bubble != null \
		and is_instance_valid(main.companion_want_bubble)
	var unchanged: bool = not main.companion_resting \
		and main.game == "" and main.stuffie_game == null \
		and main.companion_id == companion_before \
		and main.companion_colors == colors_before \
		and main.companion_bruises == bruises_before \
		and main.fish_tokens == tokens_before \
		and main.care_points == care_before \
		and main.stuffie_wins == wins_before \
		and main.companion_care_t <= 0.0 \
		and main.companion_rest_timer > 0.0 \
		and main.companion_rest_timer <= CompanionSystem.CARE_REMINDER_GAP \
		and _progress_unchanged(progress_before)
	var ok: bool = follower_present and invitation_present and unchanged
	print("PASSIVE|Stuffie patient care: ",
		"OK present, unchanged, and optional after 181s" if ok else \
		"FAIL follower=%s invitation=%s unchanged=%s resting=%s bruises=%d timer=%.2f" \
		% [follower_present, invitation_present, unchanged,
			main.companion_resting, main.companion_bruises,
			main.companion_rest_timer])
	return 0 if ok else 1

func _probe_brawl_agency() -> int:
	# The brawler ships with an AI partner (Huluu) who fights on her own —
	# the sharpest agency risk in the game. Assert the invariant: Huluu only
	# STUNS; with zero player input no imp ever pops, no wave ever clears.
	if main.game != "":
		main._leave_current_activity()   # the fairy agency test leaves its game open
		await _frames(2)
	main.brawl_cool = 0.0
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	main._start_game(main.brawl_fr)
	var before: Dictionary = _progress_snapshot()
	await _frames(600)
	var enemies_left: int = (main.g.get("enemies", []) as Array).size()
	var idle_ok: bool = main.game == "brawl" and int(main.g.get("seg", 0)) == 0 \
		and int(main.g.get("bops", 0)) == 0 and enemies_left > 0 and _progress_unchanged(before)
	main._leave_current_activity()
	await _frames(2)
	var leave_ok: bool = main.game == ""
	print("PASSIVE|Toy Castle agency: ", ("OK Huluu stuns, only Roshan's tap pops" if idle_ok and leave_ok else "FAIL idle=%s leave=%s" % [idle_ok, leave_ok]))
	return 0 if idle_ok and leave_ok else 1

func _probe_shop_agency() -> int:
	main.beans_t = -1.0
	main.speed_mult = 1.0
	main.pearl_count = 20
	main.shop_owned.erase("_beans_once")
	main.touch_ui.action_down = false
	main.touch_ui.action_just = false
	main._start_game(main.shop_fr)
	var beans_base := Vector3.ZERO
	var beans_price := 0
	var found_beans := false
	var items: Array = main.g.get("items", [])
	for raw_item in items:
		var item: Dictionary = raw_item
		if String(item.get("id", "")) == "beans":
			beans_base = item["base"]
			beans_price = int(item["price"])
			found_beans = true
			break
	if not found_beans:
		print("PASSIVE|Pearl Shop: FAIL beans offer missing")
		main._leave_current_activity()
		await _frames(2)
		return 1
	player.position = beans_base
	player.vel = Vector3.ZERO
	var before: Dictionary = _progress_snapshot()
	for i in range(5):
		player.position = beans_base
		player.vel = Vector3.ZERO
		await process_frame
	var idle_ok: bool = main.game == "shop" and _progress_unchanged(before) and float(main.beans_t) < 0.0
	# Model A/Enter still being held when Keep Swimming closes the pause menu.
	main.g["shop_wait_release"] = true
	main.g["shop_action_down"] = false
	main.joy_has_unmapped = true
	main.joy_ev_btn[int(JOY_BUTTON_A)] = true
	for i in range(3):
		player.position = beans_base
		player.vel = Vector3.ZERO
		await process_frame
	var held_ok: bool = main.game == "shop" and _progress_unchanged(before) and float(main.beans_t) < 0.0
	main.joy_ev_btn[int(JOY_BUTTON_A)] = false
	for i in range(2):
		player.position = beans_base
		player.vel = Vector3.ZERO
		await process_frame
	main.joy_ev_btn[int(JOY_BUTTON_A)] = true
	player.position = beans_base
	player.vel = Vector3.ZERO
	await process_frame
	var fresh_ok: bool = int(main.pearl_count) == int(before["pearls"]) - beans_price and float(main.beans_t) > 0.0
	main.joy_ev_btn.clear()
	main.joy_has_unmapped = false
	var ok: bool = idle_ok and held_ok and fresh_ok
	print("PASSIVE|Pearl Shop agency: ", ("OK idle/held safe; fresh press buys once" if ok else "FAIL idle=%s held=%s fresh=%s" % [idle_ok, held_ok, fresh_ok]))
	if main.game == "shop":
		main._leave_current_activity()
		await _frames(2)
	main.beans_t = -1.0
	main.speed_mult = 1.0
	return 0 if ok else 1

func _probe_penguin_agency() -> int:
	main.beans_t = -1.0
	main.speed_mult = 1.0
	main.slide_cool = 0.0
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	main._start_game(main.slide_fr)
	var before: Dictionary = _progress_snapshot()
	main.g["s"] = float(main.g["total"])
	await _frames(2)
	var passive_ok: bool = main.game == "slide" and not bool(main.g.get("steered", false)) \
		and float(main.g.get("s", 1e20)) < float(main.g.get("total", 0.0)) \
		and _progress_unchanged(before)
	main.slide_cool = 0.0
	main._leave_current_activity()
	await _frames(2)
	# the refreshed full cooldown is 3s now ("again!" polish) via _end_game;
	# the pause-menu leave path still sets 14 — assert "refreshed", not "long"
	var leave_ok: bool = main.game == "" and float(main.slide_cool) > 2.0
	# A normal, deliberately-steered finish must also refresh the portal cooldown.
	main.slide_cool = 0.0
	main._start_game(main.slide_fr)
	main.g["steered"] = true
	main.g["s"] = float(main.g["total"])
	await _frames(2)
	var finish_ok: bool = main.game == "" and float(main.slide_cool) > 2.0   # 3.0 fresh minus two frames of decay
	var ok: bool = passive_ok and leave_ok and finish_ok
	print("PASSIVE|Penguin Slide agency: ", ("OK passive restarts; exits are neutral" if ok else "FAIL passive=%s leave=%s finish=%s" % [passive_ok, leave_ok, finish_ok]))
	return 0 if ok else 1

func _probe_fairy_agency() -> int:
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	main.touch_ui.action_just = false
	main._start_game(main.fairy_fr)
	# Put the real tick at its terminal decision point. With no player verb it
	# must wait here forever without granting the Flower sticker or any reward.
	main.g["phase"] = "boss_bloom"
	main.g["bloom_t"] = 0.0
	main.g["boss_center"] = main.ARENA_POS
	main.g["bud"] = null
	main.g["petals"] = []
	main.g["player_acted"] = false
	main.g["fairy_wait_release"] = false
	var before: Dictionary = _progress_snapshot()
	await _frames(3)
	var passive_ok: bool = main.game == "fairyshoot" and not bool(main.g.get("player_acted", false)) \
		and _progress_unchanged(before)
	# A held resume action is menu input, not the deliberate sparkle verb.
	main.g["fairy_wait_release"] = true
	main.touch_ui.action_down = true
	await _frames(2)
	var held_ok: bool = main.game == "fairyshoot" and not bool(main.g.get("player_acted", false)) \
		and _progress_unchanged(before)
	main.touch_ui.action_down = false
	await process_frame
	var release_ok: bool = not bool(main.g.get("fairy_wait_release", true))
	var ok: bool = passive_ok and held_ok and release_ok
	print("PASSIVE|Fairy agency: ", ("OK terminal bloom waits for a fresh verb" if ok else "FAIL passive=%s held=%s release=%s" % [passive_ok, held_ok, release_ok]))
	return 0 if ok else 1
