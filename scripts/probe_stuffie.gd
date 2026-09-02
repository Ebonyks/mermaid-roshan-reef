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
	main.day_one_active = false
	await _locked_case()
	await _picker_case()
	await _studio_room_case()
	await _follower_case()
	await _menu_case()
	await _battle_case()
	await _save_case()
	await _switch_case()
	await _award_case()
	await _lamma_case()
	await _zone_case()
	await _patient_care_case()
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
	# The picture-first castle introduces stuffies through Baby Eagle's rescue:
	# two real-depth bunny cards clear first, then the focused picker tutorial.
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _settle(8)
	main._enter_castle_interior_now(false)
	await _settle(8)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("playroom", false)
	await _settle(2)
	var eagle_record: Dictionary = main.castle_room_item_sprites.get(
		"baby_eagle_rescue", {}) as Dictionary
	var left_record: Dictionary = main.castle_room_item_sprites.get(
		"eagle_pin_left", {}) as Dictionary
	var right_record: Dictionary = main.castle_room_item_sprites.get(
		"eagle_pin_right", {}) as Dictionary
	var eagle_sprite: Sprite2D = eagle_record.get("sprite") as Sprite2D
	var left_sprite: Sprite2D = left_record.get("sprite") as Sprite2D
	var right_sprite: Sprite2D = right_record.get("sprite") as Sprite2D
	# The V3 additive sticker pack is deliberately retired. The audited room now
	# contains its four established interactions, one source-owned V4 subject,
	# the complete V2 tent, and these three rescue cards. Assert the exact
	# semantic roster so an unrelated addition cannot make a raw count pass.
	var expected_playroom_ids: Array[String] = [
		"stuffie_nook", "stacking_toy", "blocks", "play_tent",
		"shelf_sailboat",
		"baby_eagle_rescue", "eagle_pin_left", "eagle_pin_right",
	]
	var audited_playroom_roster := \
		main.castle_room_item_sprites.size() == expected_playroom_ids.size()
	for expected_id: String in expected_playroom_ids:
		audited_playroom_roster = audited_playroom_roster \
			and main.castle_room_item_sprites.has(expected_id)
	_ck("Playroom starts with Baby Eagle and two pinning dust bunnies",
		audited_playroom_roster
		and main.castle_room_item_hotspot_layer.get_child_count() == 5
		and eagle_sprite != null
		and left_sprite != null
		and right_sprite != null
		and eagle_sprite.get_meta("source_asset_role", "") == "unique_object"
		and left_sprite.get_meta("source_asset_role", "") == "unique_object"
		and right_sprite.get_meta("source_asset_role", "") == "unique_object"
		and float(eagle_sprite.get_meta("depth_z", 0.0))
			< float(left_sprite.get_meta("depth_z", 0.0))
		and float(eagle_sprite.get_meta("depth_z", 0.0))
			< float(right_sprite.get_meta("depth_z", 0.0)))
	_ck("Playroom rescue uses proximity cards instead of flat hotspots",
		left_record.get("hotspot") == null
		and right_record.get("hotspot") == null
		and String(left_sprite.get_meta("dust_bunny_role", ""))
			== "playroom_pin_left"
		and String(right_sprite.get_meta("dust_bunny_role", ""))
			== "playroom_pin_right"
		and main.castle_room_action_button != null
		and not main.castle_room_action_button.visible)
	rooms.activate_current_room()
	await process_frame
	_ck("Stuffie picker stays locked until Baby Eagle is rescued",
		main.companion_layer == null
		and main.castle_room_id == "playroom"
		and main.game_nodes.is_empty())
	rooms.tick(0.016)
	var cleared: Dictionary = main.g.get(
		"castle_dust_bunnies_cleared", {}) as Dictionary
	_ck("Standing at the room spawn does not clear either bunny",
		not bool(cleared.get("eagle_pin_left", false))
		and not bool(cleared.get("eagle_pin_right", false)))
	rooms._position_player_at_foot(
		left_record.get("contact_foot", Vector2.ZERO) as Vector2, false)
	rooms.tick(0.016)
	await _settle(2)
	_ck("One bunny cleared is not enough to finish the rescue",
		bool((main.g.get(
			"castle_dust_bunnies_cleared", {}) as Dictionary).get(
				"eagle_pin_left", false))
		and bool(main.stuffie_wins.get(
			"rescued_eagle_pin_left", false))
		and bool((main.save_data.get(
			"stuffie_wins", {}) as Dictionary).get(
				"rescued_eagle_pin_left", false))
		and not bool(main.stuffie_wins.get("rescued_eagle", false))
		and main.companion_layer == null)
	main.g["castle_dust_bunnies_cleared"] = {}
	rooms.show_room("playroom", false)
	await _settle(2)
	right_record = main.castle_room_item_sprites.get(
		"eagle_pin_right", {}) as Dictionary
	_ck("Saved half-rescue restores without respawning the first bunny",
		not main.castle_room_item_sprites.has("eagle_pin_left")
		and not right_record.is_empty()
		and not bool(main.stuffie_wins.get("rescued_eagle", false)))
	rooms._position_player_at_foot(
		right_record.get("contact_foot", Vector2.ZERO) as Vector2, false)
	rooms.tick(0.016)
	_ck("Roshan contact clears the second pinning bunny",
		bool((main.g.get(
			"castle_dust_bunnies_cleared", {}) as Dictionary).get(
				"eagle_pin_right", false))
		and bool(main.stuffie_wins.get("rescued_eagle", false)))
	await _settle(60)
	_ck("Second bunny frees Baby Eagle and opens the focused tutorial",
		bool(main.stuffie_wins.get("rescued_eagle", false))
		and main.companion_layer != null
		and main.companion_pick_id == "eagle"
		and bool(main.g.get("stuffie_rescue_tutorial", false))
		and int(main.g.get("stuffie_rescue_tutorial_step", -1)) == 0
		and main.companion_stage.get_node_or_null(
			"StuffieRescueTutorialFocus") != null
		and main.companion_stage.get_node_or_null(
			"StuffieRescueTutorialPointer") != null
		and main.companion_stage.find_children(
			"StuffieCard_*", "Button", true, false).size() == 1)
	var picker_back: Button = main.companion_stage.find_child(
		"StuffiePickerBackButton", true, false) as Button
	_ck("rescue picker keeps the familiar escapable back path",
		picker_back != null and picker_back.visible and picker_back.disabled == false)
	comp.close_picker()
	_ck("closing before confirmation leaves a safe castle state",
		main.companion_layer == null and main.companion_id == ""
		and bool(main.g.get("stuffie_rescue_tutorial", false)))
	rooms.show_room("playroom", false)
	await _settle(3)
	_ck("playroom re-entry reopens the unconfirmed adoption",
		main.companion_layer != null and main.companion_pick_id == "eagle"
		and main.companion_id == "")
	comp._pick_color_slot(1)
	await process_frame
	_ck("Tutorial state advances from part to color",
		int(main.g.get("stuffie_rescue_tutorial_step", -1)) == 1)
	_ck("Tutorial keeps the color focus visible",
		main.companion_stage.get_node_or_null(
			"StuffieRescueTutorialFocus") != null)
	comp._pick_color(1, Color(0.45, 0.82, 0.95))
	await process_frame
	_ck("Tutorial focus advances from color to the heart",
		int(main.g.get("stuffie_rescue_tutorial_step", -1)) == 2
		and main.companion_stage.get_node_or_null(
			"StuffieConfirmButton") != null)
	comp._confirm_pick()
	await process_frame
	_ck("Rescued Baby Eagle becomes the first stuffie friend",
		main.companion_id == "eagle"
		and main.companion_layer == null
		and not main.g.has("stuffie_rescue_tutorial"))
	var reward_card: Control = main.castle_companion_card
	var reward_cards: Array[Node] = main.castle_room_item_visual_layer.find_children(
		"CastleCompanionCard", "Control", true, false)
	var reward_instance: int = reward_card.get_instance_id() \
		if reward_card != null and is_instance_valid(reward_card) else -1
	rooms._position_player_at_foot(Vector2(500.0, 560.0), false)
	rooms._position_player_at_foot(Vector2(540.0, 570.0), false)
	var card_is_reused: bool = reward_card != null \
		and is_instance_valid(reward_card) \
		and reward_card.get_instance_id() == reward_instance
	var card_canvas_only: bool = reward_card != null \
		and is_instance_valid(reward_card) \
		and _all_canvas_children(reward_card)
	_ck("confirmed friend has exactly one visible Canvas companion card",
		reward_cards.size() == 1 and reward_card != null
		and is_instance_valid(reward_card) and reward_card.visible
		and String(reward_card.get_meta("companion_id", "")) == "eagle"
		and String(reward_card.get_meta("source_asset_path", ""))
			== "res://assets/book/baby_eagle.png"
		and card_canvas_only)
	_ck("castle companion card repositions without duplication",
		card_is_reused and main.castle_room_item_visual_layer.find_children(
			"CastleCompanionCard", "Control", true, false).size() == 1)
	_ck("confirmed friend identity persists safely",
		String(main.save_data.get("companion", "")) == "eagle"
		and (main.save_data.get("companion_colors", []) as Array).size() == 3)
	rooms._exit_to_courtyard()
	await _settle(6)
	main._exit_level2_now()
	await _settle(4)
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

func _studio_room_case() -> void:
	var comp: CompanionSystem = main._companion_ref()
	comp._build_room()
	var room: Node3D = main.companion_room
	_ck("Stuffie Studio builds six clear display cubbies",
		room != null and main.companion_room_rows.size() == CompanionSystem.ROOM_SLOT_COUNT
		and room.find_child("StuffieSixCubbyDisplay", true, false) is Sprite3D)
	_ck("Studio has separate upgrade table and active-friend chest",
		room.find_child("StuffieUpgradeTable", true, false) is Sprite3D
		and room.find_child("StuffieActiveToyChest", true, false) is Sprite3D
		and room.get_meta("table_anchor") is Node3D
		and room.get_meta("chest_anchor") is Node3D)
	_ck("Studio room is sprite-only with no legacy mesh furniture",
		room.find_children("*", "MeshInstance3D", true, false).is_empty())
	var lamma: Dictionary = comp.def_by_id("lamma")
	var lamma_colors: Array[Color] = [
		lamma["body"] as Color, lamma["accent"] as Color, lamma["third"] as Color]
	var lamma_cutout: Node3D = comp.creature_for(lamma, lamma_colors)
	_ck("Lamb-a uses a 2D cutout instead of the retired GLB",
		lamma.has("sprite") and not lamma.has("model")
		and lamma_cutout != null
		and not lamma_cutout.find_children("*", "Sprite3D", true, false).is_empty()
		and lamma_cutout.find_children("*", "MeshInstance3D", true, false).is_empty())
	if lamma_cutout != null:
		lamma_cutout.free()
	comp.open_picker(false, "eagle", "swap")
	_ck("toy chest opens selection-only mode",
		main.companion_pick_mode == "swap"
		and main.companion_stage.find_children("StuffieCard_*", "Button", true, false).size() == 2
		and main.companion_stage.find_children("StuffieSwatch_*", "Button", true, false).is_empty())
	comp.close_picker()
	var want_before := "feed"
	main.companion_want = want_before
	comp.open_picker(false, main.companion_id, "studio")
	_ck("worktable opens one-friend color studio",
		main.companion_pick_mode == "studio"
		and main.companion_stage.find_children("StuffieCard_*", "Button", true, false).size() == 1
		and not main.companion_stage.find_children("StuffieSwatch_*", "Button", true, false).is_empty())
	comp._pick_color(1, Color(1.0, 0.72, 0.42))
	comp._confirm_pick()
	_ck("repainting preserves the active friend's care request",
		main.companion_id == "mewsha" and main.companion_want == want_before)
	main.companion_want = ""
	if room != null and is_instance_valid(room):
		main.game_nodes.erase(room)
		room.queue_free()
	main.companion_room = null
	main.companion_room_rows = []

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
		launcher != null and launcher.visible and launcher.position.x >= 820.0
		and launcher.position.x + launcher.size.x <= 1000.0
		and launcher.position.y <= 40.0 and launcher.size.x >= 120.0 and launcher.size.y >= 120.0
		and String(launcher.get_meta("hud_zone", "")) == "upper_right_inset")
	var comp: CompanionSystem = main._companion_ref()
	comp._begin_want("play")
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
	_ck("Tamagotchi sheet shows need, growth, and table repainting",
		main.companion_care_stage.find_child("StuffieCurrentNeed", true, false) != null
		and main.companion_care_stage.find_child("StuffieGrowthPips", true, false) != null
		and main.companion_care_stage.find_child("StuffieHeartProgress", true, false) != null
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

func _menu_case() -> void:
	# One inset Storybook launcher owns both asked care and always-welcome affection.
	var comp: CompanionSystem = main._companion_ref()
	var buttons: Array[Node] = main.find_children("StuffieCareMenuButton", "Button", true, false)
	_ck("exactly one Stuffie HUD launcher exists after adoption", buttons.size() == 1
		and main.companion_menu_button != null and is_instance_valid(main.companion_menu_button))
	var pts: int = main.care_points
	comp.open_care_menu()
	_ck("the Storybook care menu opens from that launcher", main.companion_care_layer != null
		and main.companion_care_stage != null)
	comp._choose_menu_care("bath")
	await _settle(2)
	_ck("unasked care is affection with no growth point", main.care_points == pts
		and main.companion_care_layer == null)
	comp._begin_want("feed")
	comp.open_care_menu()
	comp._choose_menu_care("feed")
	_ck("the same menu tends an asked want remotely", main.companion_care_t > 0.0
		and main.companion_node.position.distance_to(main.player.position) < 8.0)
	main.companion_care_t = 0.01
	await _settle(4)
	_ck("asked menu care grows the stuffie", main.care_points == pts + 1
		and main.companion_want == "")

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
	# The Studio toy chest owns active-friend swapping; shelf taps only introduce.
	var comp: CompanionSystem = main._companion_ref()
	comp.open_picker(false, "eagle", "swap")
	_ck("toy chest preselects the tapped stuffie", main.companion_pick_id == "eagle"
		and main.companion_layer != null and main.companion_pick_mode == "swap")
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
	_ck("Lamb-a' comes home to the Studio", bool(main.stuffie_wins.get("friend_lamma", false))
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
	# owner 2026-07-21 ("vanishes after ocean"): follow is hide-list based, so
	# new explorable levels follow by DEFAULT; only camera-owning engines hide
	main.game = "ember"
	var follows_ember: bool = comp._follow_ctx()
	main.game = "treasure"
	var follows_arena: bool = comp._follow_ctx()
	main.game = "kart"
	var hides_kart: bool = not comp._follow_ctx()
	main.game = ""
	_ck("follows into new levels and arena games by default", follows_ember and follows_arena)
	_ck("hides only inside camera-owning engines", hides_kart)

func _patient_care_case() -> void:
	# Battle bumps leave boo-boos and invite a hug + bath. Tending both heals;
	# waiting through any number of reminder cycles never removes the friend,
	# blocks play, or loses progress.
	var comp: CompanionSystem = main._companion_ref()
	var care_before: int = main.care_points
	var friend_before: String = main.companion_id
	var colors_before: Array = main.companion_colors.duplicate(true)
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
		# Exercise the queued care transition without tying the probe to runner
		# frame rate: 60 uncapped CI frames can be shorter than the real 1.2 s
		# follow-up delay, even though the same sequence passes at local cadence.
		main.companion_want_cool = 0.0
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
	# --- patient path: hurt again, then cross the retired timeout repeatedly
	main.stuffie_cool = 0.0
	main._start_stuffie_battle()
	await process_frame
	battle = main.stuffie_game
	if battle == null:
		_ck("patient-care battle starts", false)
		return
	battle._bump_pal(battle.pal_pos + Vector3(0, 0, 3.0))
	battle.cancel()
	await process_frame
	await process_frame
	_ck("leaving early keeps the boo-boo", main.companion_bruises >= 1
		and main.game == "")
	var bruises_before: int = main.companion_bruises
	var tokens_at_wait: int = main.fish_tokens
	var care_at_wait: int = main.care_points
	var follower_before: int = main.companion_node.get_instance_id()
	for reminder in range(4):
		main.companion_rest_timer = 0.01
		await _settle(4)
	_ck("uncared boo-boos wait without removing the friend",
		not main.companion_resting
		and main.companion_node != null and is_instance_valid(main.companion_node)
		and main.companion_node.get_instance_id() == follower_before
		and main.companion_bruises >= bruises_before
		and main.companion_rest_timer > 0.0
		and (main.companion_want_queue.size() >= 1 or main.companion_want != ""))
	# A reminder remains voiced and picture-first without escalating into a
	# threat or destination-dependent objective.
	if main.companion_want == "":
		main.companion_want_cool = 0.0
		comp._tick_care(0.0)
	main.clear_dialogue()
	main.said_cool.clear()
	var voice_before: int = main.voice_i
	main.companion_rest_timer = 0.01
	comp._tick_care(0.02)
	comp._sync_menu_button()
	var reminder_copy: String = main.hud_msg.text.to_lower()
	var reminder_is_kind: bool = reminder_copy == \
		"whenever you're ready, tap me for a hug and bubble bath!" \
		and not reminder_copy.contains("home") \
		and not reminder_copy.contains("last chance") \
		and not reminder_copy.contains("one more minute") \
		and not reminder_copy.contains("hurt too much")
	var reminder_pointer_ok: bool = main.companion_want_bubble != null \
		and is_instance_valid(main.companion_want_bubble)
	var reminder_hud_ok: bool = main.companion_menu_button != null \
		and main.companion_menu_button.visible \
		and main.companion_menu_button.text == "🩹" \
		and String(main.companion_menu_button.get_meta(
			"storybook_kind", "")) == "action"
	var reminder_voice_ok: bool = main.voice_i == voice_before + 1
	if not (reminder_voice_ok and reminder_is_kind \
			and reminder_pointer_ok and reminder_hud_ok):
		print("STUFFIE|patient reminder detail: voice=", reminder_voice_ok,
			" copy=", reminder_copy, " kind=", reminder_is_kind,
			" pointer=", reminder_pointer_ok, " hud=", reminder_hud_ok)
	_ck("patient reminder stays voiced, kind, and picture-first",
		reminder_voice_ok and reminder_is_kind \
		and reminder_pointer_ok and reminder_hud_ok)
	# Keep the retired key in the schema but prove it cannot be written true or
	# resurrect either runtime gate. The following raw screen taps run while the
	# in-memory sentinel is deliberately true.
	main.companion_resting = true
	main._write_save()
	var saved_patient_state: bool = not bool(main.save_data.get(
		"companion_resting", true)) \
		and String(main.save_data.get("companion", "")) == friend_before \
		and (main.save_data.get("companion_colors", []) as Array) == colors_before \
		and int(main.save_data.get("companion_bruises", -1)) == bruises_before \
		and int(main.save_data.get("fish_tokens", -1)) == tokens_at_wait \
		and int(main.save_data.get("care_points", -1)) == care_at_wait \
		and bool((main.save_data.get("stuffie_wins", {}) as Dictionary).get(
			"friend_lamma", false))
	_ck("retired resting flag saves healed without changing progress",
		saved_patient_state and main.companion_resting)
	main._set_touch_mode("hybrid", false)
	main.stuffie_cool = 0.0
	if main.companion_den == null or not is_instance_valid(main.companion_den):
		comp._tick_den(0.0)
	var den = main.companion_den
	if den == null:
		_ck("patient friend keeps a raw-touch den route", false)
		main.companion_resting = false
		return
	var near_den = den.position
	near_den.x += 1.0
	near_den.y += 1.0
	main.player.position = near_den
	main.player.vel *= 0.0
	main.player.snap_cam()
	await _settle(3)
	main._populate_touch_interactables()
	var den_registered: bool = false
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if String(item.get("id", "")) == "reef:den":
			den_registered = true
			break
	var camera = main.player.cam
	var first_tap_focused := false
	if den_registered and camera != null and not camera.is_position_behind(
			den.global_position):
		var den_screen: Vector2 = camera.unproject_position(den.global_position)
		_touch_tap(40, den_screen)
		await process_frame
		first_tap_focused = main.game == "" \
			and main.touch_focus_id == "reef:den" and main.touch_focus_ready
		_touch_tap(41, den_screen)
		await _settle(4)
	_ck("patient friend keeps a raw-touch den route",
		den_registered and first_tap_focused \
		and main.game == "stuffie" and main.stuffie_game != null)
	if main.stuffie_game != null:
		main.stuffie_game.cancel()
		await _settle(2)
	main.companion_resting = false
	main._start_stuffie_battle()
	await process_frame
	_ck("waiting for care never blocks another battle",
		main.stuffie_game != null and main.game == "stuffie")
	if main.stuffie_game != null:
		main.stuffie_game.cancel()
		await _settle(2)
	_ck("patient care loses no progress", main.care_points >= care_before
		and main.companion_id == friend_before
		and bool(main.stuffie_wins.get("friend_lamma", false)))

func _touch_tap(index: int, pos: Vector2) -> void:
	var down := InputEventScreenTouch.new()
	down.index = index
	down.position = pos
	down.pressed = true
	main.touch_ui._unhandled_input(down)
	var up := InputEventScreenTouch.new()
	up.index = index
	up.position = pos
	up.pressed = false
	main.touch_ui._unhandled_input(up)


func _all_canvas_children(node: Node) -> bool:
	if not node is CanvasItem:
		return false
	for child: Node in node.get_children():
		if not _all_canvas_children(child):
			return false
	return true
