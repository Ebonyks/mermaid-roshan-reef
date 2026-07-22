extends SceneTree
# Stuffed-friend companion wing probe: the picker applies a choice + colours,
# the follower spawns and tags along in the reef, sparkle-fish tokens level the
# companion, the sparring den battle requires input (passive can never win),
# attacks befriend opponents, the DODGE QTE resolves both ways without a fail
# state, and every new save key round-trips.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260718)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _locked_case()
	await _picker_case()
	await _follower_case()
	await _battle_case()
	await _save_case()
	await _switch_case()
	await _award_case()
	await _lamma_case()
	await _zone_case()
	await _rest_case()
	print("STUFFIE|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("STUFFIE|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _locked_case() -> void:
	# fresh save: no companion, so no follower, no den, no tokens appear
	await _settle(10)
	_ck("fresh save has no companion", main.companion_id == "" and main.companion_node == null)
	_ck("no den before a stuffie is chosen", main.companion_den == null)
	_ck("no want bubble before a stuffie is chosen", main.companion_want == "" and main.companion_want_bubble == null)

func _picker_case() -> void:
	var comp: CompanionSystem = main._companion_ref()
	# owner 2026-07-19: meeting Princess Huluu IS the trigger — her greeting
	# leads straight into "I want you to have a new friend!" and the picker.
	# Drive the satellite directly with hall state (no awaits, so the live
	# main loop never sees the borrowed game/g values).
	main.game = "level2"
	main.g = {"phase": "hall", "huluu_greeted": true}
	comp._tick_gift(3.0)
	_ck("meeting Huluu offers the new friend", main.companion_layer != null
		and bool(main.g.get("companion_offered", false)))
	comp.close_picker()
	main.game = ""
	main.g = {}
	comp.open_picker()
	await process_frame
	_ck("picker overlay builds", main.companion_layer != null and main.companion_stage != null)
	comp._pick_friend("mewsha")
	await process_frame
	comp._pick_color(0, Color(0.45, 0.82, 0.95))
	await process_frame
	comp._confirm_pick()
	await process_frame
	_ck("mewsha chosen with painted body", main.companion_id == "mewsha"
		and main.companion_colors.size() == 3
		and String(main.companion_colors[0]) == Color(0.45, 0.82, 0.95).to_html(false))
	_ck("picker closed after choosing", main.companion_layer == null)
	var def: Dictionary = comp.active_def()
	_ck("roster is data-driven", String(def["kind"]) == "cat" and String(def["attack"]) == "CLAW")

func _follower_case() -> void:
	await _settle(20)
	_ck("follower spawned in the reef", main.companion_node != null and is_instance_valid(main.companion_node))
	var pd: float = main.companion_node.position.distance_to(main.player.position) if main.companion_node != null else INF
	_ck("follower stays near Roshan", pd < 40.0)
	_ck("den built near the shipwreck", main.companion_den != null and is_instance_valid(main.companion_den))
	# The stuffie owns an inset upper-hand launcher, leaving the far corner to
	# Pause, and a complete storybook Tamagotchi sheet behind that one tap.
	var launcher: Button = main.companion_menu_button
	_ck("care launcher appears in the inset upper-right hand area",
		launcher != null and launcher.visible and launcher.position.x >= 900.0
		and launcher.position.x + launcher.size.x <= 1130.0
		and launcher.position.y <= 40.0 and launcher.size.x >= 120.0 and launcher.size.y >= 120.0
		and String(launcher.get_meta("hud_zone", "")) == "upper_right_inset")
	var comp: CompanionSystem = main._companion_ref()
	comp.open_care_menu()
	await process_frame
	var care_back := main.companion_care_stage.find_child("StuffieCareBackButton", true, false) as Control
	var care_actions: Array[Node] = main.companion_care_stage.find_children("StuffieCareAction_*", "Button", true, false)
	var actions_big := care_actions.size() == 5
	for action: Node in care_actions:
		var control := action as Control
		actions_big = actions_big and control != null and control.size.x >= 110.0 and control.size.y >= 110.0
	_ck("Tamagotchi sheet has a neutral back and five large care actions",
		main.companion_care_layer != null and care_back != null
		and care_back.size.x >= 110.0 and care_back.size.y >= 110.0 and actions_big)
	_ck("Tamagotchi sheet shows need, growth, and friend switching",
		main.companion_care_stage.find_child("StuffieCurrentNeed", true, false) != null
		and main.companion_care_stage.find_child("StuffieGrowthPips", true, false) != null
		and main.companion_care_stage.find_child("StuffieSwitchButton", true, false) != null)
	var menu_care_before: int = main.care_points
	comp._choose_menu_care("play")
	_ck("care menu action closes into a real care moment",
		main.companion_care_layer == null and main.companion_care_t > 0.0)
	main.companion_care_t = minf(main.companion_care_t, 0.01)
	await _settle(4)
	_ck("menu care grows the stuffie", main.care_points == menu_care_before + 1)
	# TAMAGOTCHI CARE: force a want, park Roshan beside the stuffie, tend it
	var care_before: int = main.care_points
	comp._begin_want("feed")
	await _settle(3)
	_ck("want bubble appears over the stuffie", main.companion_want == "feed"
		and main.companion_want_bubble != null and is_instance_valid(main.companion_want_bubble))
	# passive: a want alone can never grow the stuffie (no input, no points)
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	await _settle(30)
	_ck("wants wait patiently and never self-fulfil", main.companion_want == "feed"
		and main.care_points == care_before)
	# tend it: stand close + THE button
	main.player.position = (main.companion_node as Node3D).position + Vector3(2.0, 0, 0)
	main.player.vel = Vector3.ZERO
	main.touch_ui.action_down = true
	await _settle(3)
	main.touch_ui.action_down = false
	await _settle(3)
	_ck("care moment starts on tap", main.companion_want == "" or main.companion_care_t > 0.0)
	main.companion_care_t = minf(main.companion_care_t, 0.01)
	await _settle(4)
	_ck("tending a want grows the stuffie", main.care_points == care_before + 1
		and main.companion_want == "")
	# level-up celebration fires exactly on the stage boundary
	main.care_points = CompanionSystem.LEVEL_EVERY - 1
	comp._begin_want("cuddle")
	await _settle(2)
	main.touch_ui.action_down = true
	await _settle(3)
	main.touch_ui.action_down = false
	main.companion_care_t = minf(main.companion_care_t, 0.01)
	await _settle(4)
	_ck("care stages level the companion", main.care_points == CompanionSystem.LEVEL_EVERY
		and comp.stage() == 2 and comp.tier() == 1)

func _battle_case() -> void:
	main._start_stuffie_battle()
	await process_frame
	var battle: StuffieBattle = main.stuffie_game
	_ck("battle starts round 1 with two imps", battle != null and main.game == "stuffie"
		and battle.enemies.size() == 2 and battle.round_tag == "round1")
	_ck("battle creature is the painted mewsha", battle != null and battle.creature != null
		and String(battle.creature_def.get("id", "")) == "mewsha")
	if battle == null:
		return
	# passive: no input → nothing can be won
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	await _settle(30)
	_ck("battle cannot win passively", battle.state == "play" and battle.befriended_count == 0)
	# QTE both ways: a missed window is a harmless bump (state stays play), a
	# pressed window counts a dodge — no fail state anywhere. Telegraphs may
	# already have fired naturally during the passive frames, so count deltas.
	var miss0: int = battle.miss_count
	var dodge0: int = battle.dodge_success_count
	battle._qte_begin(battle.enemies[0])
	_ck("telegraph opens the DODGE window", battle.qte_t > 0.0 and battle.dodge_btn.visible)
	battle.qte_t = 0.0001
	await process_frame
	_ck("missed dodge is a bump, never a fail", battle.state == "play" and battle.miss_count == miss0 + 1)
	battle._qte_begin(battle.enemies[0])
	battle.press_dodge()
	_ck("tapping DODGE in the window succeeds", battle.dodge_success_count == dodge0 + 1 and battle.qte_t <= 0.0)
	# bop both imps dizzy → they get befriended → the round is won
	for enemy: Dictionary in battle.enemies:
		while int(enemy["hp"]) > 0:
			battle._hit_enemy(enemy)
		enemy["timer"] = 0.0
	await _settle(4)
	_ck("bopped imps become friends", battle.befriended_count == 2)
	_ck("all friends wins the round", battle.state == "won")
	battle.win_t = 0.0
	await process_frame
	await process_frame
	_ck("round win saves ladder progress and returns", bool(main.stuffie_wins.get("round1", false))
		and main.game == "" and main.stuffie_game == null)
	_ck("winning pays pearls", main.pearl_count >= 8)

func _save_case() -> void:
	main._write_save()
	var doc: Dictionary = main.save_data
	_ck("save carries companion keys", String(doc.get("companion", "")) == "mewsha"
		and (doc.get("companion_colors", []) as Array).size() == 3
		and int(doc.get("care_points", -1)) == main.care_points
		and bool((doc.get("stuffie_wins", {}) as Dictionary).get("round1", false)))
	# roundtrip through a fresh SaveState reader
	var reread := SaveState.new(main)
	var loaded: Variant = reread._recover_save_if_needed()
	_ck("save roundtrips through recovery reader", loaded is Dictionary
		and String((loaded as Dictionary).get("companion", "")) == "mewsha")

func _switch_case() -> void:
	# owner 2026-07-19: the stuffie is swappable ANY time — the Stuffie Den
	# shelves open the picker preselected on the tapped friend
	var comp: CompanionSystem = main._companion_ref()
	comp.open_picker(false, "eagle")
	_ck("den shelf preselects the tapped stuffie", main.companion_pick_id == "eagle"
		and main.companion_layer != null)
	comp._confirm_pick()
	_ck("companion swaps to Baby Eagle", main.companion_id == "eagle")
	await _settle(15)
	_ck("swapped follower respawns as the bird", main.companion_node != null
		and is_instance_valid(main.companion_node)
		and String(comp.active_def()["kind"]) == "bird")

func _award_case() -> void:
	# THE CAPTURE LOOP (owner 2026-07-20): befriend a boss stuffie → it comes
	# home → it becomes a carryable companion. Lamb-a' is the first.
	var comp: CompanionSystem = main._companion_ref()
	_ck("Lamb-a' starts locked", not comp.unlocked("lamma")
		and comp.unlocked_defs().size() == 2)
	main.stuffie_wins["round2"] = true
	main.stuffie_wins["round3"] = true
	main.stuffie_cool = 0.0
	main._start_stuffie_battle()
	await process_frame
	var battle: StuffieBattle = main.stuffie_game
	_ck("ladder reaches the Lamb-a' capture round", battle != null
		and battle.round_tag == "boss_lamma" and battle.enemies.size() == 1)
	if battle == null:
		return
	var boss: Dictionary = battle.enemies[0]
	while int(boss["hp"]) > 0:
		battle._hit_enemy(boss)
	boss["timer"] = 0.0
	await _settle(4)
	_ck("boss stuffie is befriended, never hurt", battle.state == "won")
	battle.win_t = 0.0
	await process_frame
	await process_frame
	_ck("Lamb-a' comes home to the Den", bool(main.stuffie_wins.get("friend_lamma", false))
		and comp.unlocked("lamma") and comp.unlocked_defs().size() == 3)

func _lamma_case() -> void:
	var comp: CompanionSystem = main._companion_ref()
	comp.open_picker(false, "lamma")
	_ck("captured friend joins the picker", main.companion_pick_id == "lamma"
		and main.companion_layer != null)
	comp._confirm_pick()
	await _settle(15)
	_ck("Lamb-a' can be carried on missions", main.companion_id == "lamma"
		and main.companion_node != null and is_instance_valid(main.companion_node))

func _zone_case() -> void:
	# zone watch: changing worlds always snaps the stuffie back to her side
	# (drive the satellite directly — no awaits, so the live loop never sees
	# the borrowed game value)
	var comp: CompanionSystem = main._companion_ref()
	if main.companion_node == null or not is_instance_valid(main.companion_node):
		_ck("zone case needs a follower", false)
		return
	main.companion_node.position = main.player.position + Vector3(60.0, 0, 0)
	main.game = "north"
	comp.tick(0.016)
	var near: bool = main.companion_node != null and is_instance_valid(main.companion_node) \
		and main.companion_node.position.distance_to(main.player.position) < 12.0
	main.game = ""
	comp.tick(0.016)
	_ck("zone change snaps the stuffie to her side", near)

func _rest_case() -> void:
	# THE GENTLE FAILURE (owner 2026-07-21): battle bumps leave boo-boos; the
	# stuffie asks for its post-battle hug + bath. Tended boo-boos heal;
	# ignored ones send it home to its Den shelf, and Roshan picks a friend
	# again at the castle (the same one included). Nothing else is lost.
	var comp: CompanionSystem = main._companion_ref()
	var care_before: int = main.care_points
	var friend_before: String = main.companion_id
	# --- heal path: get bumped, win anyway, then tend the hug + bath
	main.stuffie_cool = 0.0
	main._start_stuffie_battle()
	await process_frame
	var battle: StuffieBattle = main.stuffie_game
	_ck("care-loop battle starts", battle != null and main.game == "stuffie")
	if battle == null:
		return
	battle._bump_pal(battle.pal_pos + Vector3(0, 0, 3.0))
	_ck("bumps leave boo-boos, never end the battle", battle.bruises == 1
		and battle.state == "play")
	for enemy: Dictionary in battle.enemies:
		while int(enemy["hp"]) > 0 and String(enemy["state"]) == "active":
			battle._hit_enemy(enemy)
		enemy["timer"] = 0.0
	await _settle(4)
	battle.win_t = 0.0
	await process_frame
	await process_frame
	_ck("boo-boos come home asking for hug + bath", main.companion_bruises >= 1
		and main.companion_rest_timer > 0.0
		and (main.companion_want_queue.size() >= 1 or main.companion_want != ""))
	main.player.position = (main.companion_node as Node3D).position + Vector3(2.0, 0, 0)
	main.player.vel = Vector3.ZERO
	for i in range(2):
		for f in range(60):
			if main.companion_want != "":
				break
			await process_frame
		main.touch_ui.action_down = true
		await _settle(3)
		main.touch_ui.action_down = false
		main.companion_care_t = minf(main.companion_care_t, 0.01)
		await _settle(4)
	_ck("hug + bath heal every boo-boo", main.companion_bruises == 0
		and main.companion_rest_timer < 0.0 and not main.companion_resting)
	# --- rest path: hurt again, then let the patience clock run out
	main.stuffie_cool = 0.0
	main._start_stuffie_battle()
	await process_frame
	battle = main.stuffie_game
	if battle == null:
		_ck("rest-path battle starts", false)
		return
	battle._bump_pal(battle.pal_pos + Vector3(0, 0, 3.0))
	battle.cancel()
	await process_frame
	await process_frame
	_ck("leaving early keeps the boo-boo", main.companion_bruises >= 1
		and main.game == "")
	main.companion_rest_timer = 0.01
	await _settle(4)
	_ck("uncared boo-boos send the stuffie home to rest", main.companion_resting
		and (main.companion_node == null or not is_instance_valid(main.companion_node)))
	main._start_stuffie_battle()
	_ck("no battles while resting", main.stuffie_game == null)
	_ck("rest loses no progress", main.care_points >= care_before
		and bool(main.stuffie_wins.get("friend_lamma", false)))
	# picking again at the Den (the same friend included) wakes it up
	comp.open_picker(false, friend_before)
	comp._confirm_pick()
	await _settle(12)
	_ck("re-picking at the Den wakes the stuffie", not main.companion_resting
		and main.companion_id == friend_before
		and main.companion_node != null and is_instance_valid(main.companion_node))
