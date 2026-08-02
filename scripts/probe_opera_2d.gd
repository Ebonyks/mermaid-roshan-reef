extends SceneTree
## Runtime contract for the twelve Canvas-based Pearl Opera career worlds.
##
## This intentionally forces the 2D path under headless Godot. The older
## probe_opera.gd continues to regression-test the detailed legacy mechanics,
## while this probe proves the shipping door path uses supplied paintings,
## 2D actors, one-finger phases, competition progress and clean teardown.

var main: ReefMain
var bad := 0


func _init() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.game = "opera"

	OS.set_environment("OPERA_FORCE_2D_LOBBY", "1")
	main.opera_stars = 0
	var lobby_touch_before := main.touch_ui.visible if main.touch_ui != null else false
	var house := OperaHouse.new()
	get_root().add_child(house)
	house.start(main, 0, Callable())
	await process_frame
	_check("shipping Opera entry uses the Canvas lobby", house.use_lobby_2d and house.lobby_2d != null)
	if house.lobby_2d != null:
		var lobby := house.lobby_2d
		_check("2D lobby has no 3D navigation children", house.find_children("*", "Node3D", true, false).is_empty())
		_check("2D lobby exposes three direct floor tabs", lobby.floor_tabs.size() == 3)
		_check("2D lobby shows four large job cards on floor one",
			lobby.card_buttons.size() == 5 and _visible_card_count(lobby.card_buttons) == 4)
		var roshan_only := true
		for card: Button in lobby.card_buttons:
			roshan_only = roshan_only and card.get_node_or_null("RoshanActor") != null
			roshan_only = roshan_only and card.get_node_or_null("RivalActor") == null
		_check("job cards show Roshan only, never imp matchup cards", roshan_only)
		_check("floor finale is gated by the four job stars", bool(lobby.boss_button.get_meta("locked", false)))
		lobby.refresh((1 << 4) | (1 << 9), 2)
		_check("Grand Gallery expands to five direct job cards", _visible_card_count(lobby.card_buttons) == 5)
		_check("Nursery Nurse is displayed as job twelve before Pop Star",
			int(lobby.card_buttons[3].get_meta("act_index", -1)) == 15
			and int(lobby.card_buttons[4].get_meta("act_index", -1)) == 13)
		_check("five Grand Gallery jobs gate the finale", bool(lobby.boss_button.get_meta("locked", false)))
		lobby.refresh(0, 0)
	house._leave_early()
	await process_frame
	OS.set_environment("OPERA_FORCE_2D_LOBBY", "0")
	if main.touch_ui != null:
		_check("2D lobby restores the touch layer on exit", main.touch_ui.visible == lobby_touch_before)
	var show_count := 0
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("type", "show")) == "boss":
			continue
		show_count += 1
		var config := source.duplicate(true)
		config["force_2d"] = true
		var touch_before := main.touch_ui.visible if main.touch_ui != null else false
		var act := OperaAct.new()
		get_root().add_child(act)
		act.start(main, config, Callable())
		await process_frame
		var career := String(config.get("costume", ""))
		_check("%s enters Canvas career world" % career,
			act.use_career_world_2d and act.career_world_2d != null)
		if act.career_world_2d == null:
			act.queue_free()
			continue
		var world := act.career_world_2d
		_check("%s uses no 3D children in career play" % career,
			act.find_children("*", "Node3D", true, false).is_empty())
		_check("%s builds a scalable code-native career world" % career,
			world.get_node_or_null("OperaCareerWorld2D/CareerWorldBackdrop") is OperaWorldBackdrop2D)
		_check("%s loads Mermaid Roshan's outfit actor" % career,
			world.player_actor != null and world.player_actor.texture != null)
		_check("%s loads its dressed rival or care partner" % career,
			world.rival_actor != null and world.rival_actor.texture != null)
		var cooperative := act.competition != null and act.competition.is_cooperative()
		if cooperative:
			_check("%s keeps its care partner beside Roshan from the first beat" % career,
				world.rival_actor.visible)
		else:
			_check("%s keeps the rival hidden during earlier minigames" % career,
				not world.rival_actor.visible and not world.in_competition_finale())
		_check("%s pauses competition scoring before the finale" % career,
			not act.competition.active)
		_check("%s has a multi-phase job game" % career, world.phases.size() >= 4)
		_check("%s starts without passive progress" % career,
			is_equal_approx(world.progress(), 0.0))
		var modes: Array[String] = []
		for phase_dict: Dictionary in world.phases:
			modes.append(String(phase_dict.get("mode", "")))
		_check("%s opens with a friendly imp scuffle" % career,
			modes.size() > 0 and modes[0] == "bop")
		var captain_scuffle := -1
		for mode_i in range(1, modes.size()):
			if modes[mode_i] == "bop":
				captain_scuffle = mode_i
		_check("%s stages a bigger scuffle before the stage door" % career,
			captain_scuffle > 0 and captain_scuffle < world._finale_start()
			and float((world.phases[captain_scuffle] as Dictionary).get("goal", 0.0))
			> float((world.phases[0] as Dictionary).get("goal", 0.0)))
		var scuffle_free_finale := true
		for mode_i in range(world._finale_start(), modes.size()):
			scuffle_free_finale = scuffle_free_finale and modes[mode_i] != "bop"
		_check("%s keeps the stage finale for the job contest" % career, scuffle_free_finale)
		var backdrop := world.get_node_or_null("OperaCareerWorld2D/CareerWorldBackdrop") as OperaWorldBackdrop2D
		_check("%s starts in its job world, off the proscenium" % career,
			backdrop != null and not backdrop.stage_mode)
		if career != "nursery":
			_check("%s paints the supplied codex career world" % career,
				backdrop != null and backdrop.painting != null)
		var captain_stage_seen := false
		if career == "detective":
			var original_phase_count := world.phases.size()
			while world.phase_index < world._finale_start():
				if world.phase_index == world.steal_index and backdrop != null:
					captain_stage_seen = captain_stage_seen or backdrop.stage_mode
				world._on_gesture("probe", 100.0, 1.0)
				act._process(0.05)
			_check("detective imp enters only for the final shared mystery",
				world.rival_actor.visible and world.in_competition_finale() and act.competition.active)
			act.competition.round_elapsed = float(act.competition.spec.get("par_time", 40.0)) * 1.2
			act._process(0.1)
			_check("2D detective rival can solve at the 40-second clock",
				world.reveal_t > 0.0 and not world.active)
			world.reveal_t = 0.01
			world._process(0.02)
			_check("2D detective shows the answer then restarts the same guided case",
				world.guided and world.active and world.phase_index == world._finale_start()
				and world.phases.size() == original_phase_count
				and act.competition.retries == 1)

		var saw_finale_imp := world.rival_actor.visible and world.in_competition_finale()
		var rival_hid_through_scuffles := true
		var guard := 0
		while act.state == "play" and guard < 60:
			rival_hid_through_scuffles = rival_hid_through_scuffles \
				and (world.in_competition_finale() or not world.rival_actor.visible)
			if world.phase_index == world.steal_index and backdrop != null:
				captain_stage_seen = captain_stage_seen or backdrop.stage_mode
			world._on_gesture("probe", 100.0, 1.0)
			act._process(0.05)
			await process_frame
			guard += 1
			saw_finale_imp = saw_finale_imp or (world.rival_actor.visible and world.in_competition_finale())
		_check("%s brings in the dressed imp for the final level" % career, saw_finale_imp)
		_check("%s keeps the rival away from both imp scuffles" % career, rival_hid_through_scuffles)
		_check("%s brawls the captain at the stage door" % career, captain_stage_seen)
		_check("%s finishes on the proscenium stage" % career,
			backdrop != null and backdrop.stage_mode)
		_check("%s can complete through one-finger phases" % career,
			act.state == "won" and is_equal_approx(act.competition.player_progress, 1.0))
		_check("%s awards a graded crowd reaction" % career,
			not act.performance_result.is_empty()
			and int(act.performance_result.get("tier", 0)) >= 1
			and int(act.performance_result.get("tier", 0)) <= 3)
		act.cancel()
		await process_frame
		if main.touch_ui != null:
			_check("%s restores the touch layer on exit" % career,
				main.touch_ui.visible == touch_before)

	_check("all thirteen career jobs were exercised", show_count == 13)
	if bad == 0:
		print("OPERA2D|result: ALL OK")
		quit()
	else:
		print("OPERA2D|result: %d FAIL" % bad)
		quit(1)


func _visible_card_count(cards: Array) -> int:
	var count := 0
	for card: Button in cards:
		if card.visible:
			count += 1
	return count


func _check(label: String, condition: bool) -> void:
	if condition:
		print("OPERA2D|OK|", label)
	else:
		bad += 1
		print("OPERA2D|FAIL|", label)
