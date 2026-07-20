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
	_ck("no sparkle-fish before a stuffie is chosen", main.companion_tokens.is_empty())

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
	_ck("sparkle-fish tokens spawned", main.companion_tokens.size() == CompanionSystem.TOKEN_TOTAL)
	_ck("den built near the shipwreck", main.companion_den != null and is_instance_valid(main.companion_den))
	# collect a token analytically: park Roshan on one
	var tokens_before: int = main.fish_tokens
	var row: Dictionary = main.companion_tokens[0]
	if row["node"] != null:
		main.player.position = (row["node"] as Node3D).position
		main.player.vel = Vector3.ZERO
		await _settle(6)
	_ck("sparkle fish levels the companion", main.fish_tokens >= tokens_before + 1)
	_ck("token slot enters respawn countdown", main.companion_tokens[0]["node"] == null and float(main.companion_tokens[0]["timer"]) > 0.0)

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
		and int(doc.get("fish_tokens", -1)) == main.fish_tokens
		and bool((doc.get("stuffie_wins", {}) as Dictionary).get("round1", false)))
	# roundtrip through a fresh SaveState reader
	var reread := SaveState.new(main)
	var loaded: Variant = reread._recover_save_if_needed()
	_ck("save roundtrips through recovery reader", loaded is Dictionary
		and String((loaded as Dictionary).get("companion", "")) == "mewsha")
