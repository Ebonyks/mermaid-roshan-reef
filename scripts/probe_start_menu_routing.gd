extends SceneTree
## Focused launch-policy probe. It keeps Continue and New Game on opposite
## sides of the Day 1 boundary without booting the heavyweight world or
## touching the real child save.

var failures: int = 0
const START_MENU := preload("res://scripts/start_menu.gd")


func _init() -> void:
	var main := ReefMain.new()
	main._prepare_start_menu_launch(false)
	_check("Continue bypasses Day 1", not main.day_one_is_active())
	_check("Continue bypasses the legacy intro", not main.first_session)
	main._prepare_start_menu_launch(true)
	_check("New Game selects Day 1", main.day_one_is_active())
	_check("New Game bypasses the legacy intro", not main.first_session)
	_check("Continue preserves an explicitly active Day One save",
		START_MENU.continue_day_one_mode({"day_one_active": true}))
	_check("legacy Continue remains outside Day One",
		not START_MENU.continue_day_one_mode({"legacy": true}))
	_check("New Game confirmation is delayed and hold-gated",
		menu_source_for_hold().contains("NEW_GAME_ARM_DELAY_SECONDS := 1.5")
		and menu_source_for_hold().contains("NEW_GAME_HOLD_SECONDS := 0.8")
		and menu_source_for_hold().contains("button_down.connect(_begin_new_game_hold")
		and menu_source_for_hold().contains("button_up.connect(_cancel_new_game_hold"))
	_check("confirm sheet focuses the safe KEEP GAME action",
		menu_source_for_hold().contains('get_node_or_null("StartMenuKeepGameButton")')
		and menu_source_for_hold().contains("keep.grab_focus()"))
	_check("saved menu makes Continue gold and New Game secondary",
		menu_source_for_hold().contains('"gold" if m.has_saved_game else "primary"')
		and menu_source_for_hold().contains(
			'"secondary" if m.has_saved_game else "gold"'))
	_check("grown-up restore uses the three-second Options hold",
		menu_source_for_hold().contains("ARCHIVE_RESTORE_HOLD_SECONDS := 3.0")
		and menu_source_for_hold().contains("_restore_new_game_archive()"))
	_probe_day_one_resume_contract(main)
	_probe_wiring()
	main.free()
	print("START_MENU_ROUTING|RESULT: ",
		"PASS" if failures == 0 else "FAIL",
		" failures=", failures)
	quit(1 if failures > 0 else 0)


func _probe_wiring() -> void:
	var main_source: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	var menu_source: String = FileAccess.get_file_as_string("res://scripts/start_menu.gd")
	var lagoon_source: String = FileAccess.get_file_as_string(
		"res://scripts/arena/sky_lagoon_promenade.gd")
	var pause_source: String = FileAccess.get_file_as_string(
		"res://scripts/pause_menu.gd")
	var director_source: String = FileAccess.get_file_as_string(
		"res://scripts/day_one_director.gd")
	_check("startup waits for the menu or probe driver",
		not main_source.contains(
			"START_AT_CASTLE_GATE and DisplayServer.get_name()"))
	_check("Continue derives its mode from the saved Day One flag",
		menu_source.contains("continue_day_one_mode(m.save_data)"))
	_check("New Game calls the Day 1 route after reload",
		menu_source.contains("m._launch_from_start_menu(true)"))
	_check("New Game reload marker survives the scene reset",
		menu_source.contains("DAY_ONE_AFTER_RESET_META")
		and menu_source.contains("reload_current_scene"))
	_check("menu cannot invoke the retired legacy intro",
		not menu_source.contains("_build_intro"))
	_check("fresh Day One focuses the castle approach",
		lagoon_source.contains("var day_one_entry: bool = m.day_one_is_active()")
		and lagoon_source.contains("_focus(castle_target)")
		and lagoon_source.contains("roshan_day1_castle"))
	_check("Day One Reef target is fail-closed",
		lagoon_source.contains("m._day_one_refuse_reef_exit()")
		and lagoon_source.contains("m.day_one_is_active()"))
	_check("Day One castle affordance survives idle cap",
		lagoon_source.contains('String(target.get("id", "")) == "castle_gate"')
		and lagoon_source.contains("maxf(tint.a, 0.45)"))
	_check("castle pointer stays visible and actionable",
		lagoon_source.contains('_activate(target)')
		and director_source_for_castle_pointer().contains("button.visible")
		and director_source_for_castle_pointer().contains("clampf(")
		and director_source_for_castle_pointer().contains('pointer_target", "elevator"')
		and director_source_for_castle_pointer().contains("pointer.visible = is_open()")
		and director_source_for_castle_pointer().contains("pointer.modulate.a = 1.0"))
	_check("attic and level exits route through Day One gate",
		main_source.contains("func _day_one_refuse_reef_exit()")
		and main_source.contains("_day_one_reorient_after_exit_now")
		and main_source.contains("if day_one_is_active():"))
	_check("pause hides the Reef tile during Day One",
		pause_source.contains("and not m.day_one_is_active()"))
	_check("Day Two clears stale Day One routing",
		director_source.contains("func clear_day_one_routing()")
		and main_source.contains("clear_day_one_routing()"))


func _probe_day_one_resume_contract(main: ReefMain) -> void:
	var expected: Dictionary = {
		"bathroom": "bubble_bath",
		"pool": "mermaid_pool",
		"stuffie": "playroom",
		"art": "craft_room",
	}
	for logical_room: String in expected:
		main.day_one_current_room_id = logical_room
		_check("Continue maps valid room %s" % logical_room,
			main.day_one_castle_room_for_current() == String(expected[logical_room]))
	main.day_one_current_room_id = "not_a_day_one_room"
	_check("Continue invalid room fails closed to hall",
		main.day_one_castle_room_for_current() == "main_hall")
	var normalised_valid: Dictionary = DayOneDirector.normalise_save_patch({
		"day_one_current_room": "pool",
		"day_one_completed_rooms": ["bathroom"],
	})
	_check("save normalization preserves authoritative valid room",
		String(normalised_valid.get("day_one_current_room", "")) == "pool")
	var normalised_invalid: Dictionary = DayOneDirector.normalise_save_patch({
		"day_one_current_room": "reef",
		"day_one_completed_rooms": ["bathroom"],
	})
	_check("save normalization falls back invalid room safely",
		String(normalised_invalid.get("day_one_current_room", "")) == "pool")
	var director: DayOneDirector = main._day_one_ref()
	director.current_room_id = "pool"
	director.dirty_castle_discovered = true
	director.clear_day_one_routing()
	_check("Day Two routing clear removes room and discovery latch",
		director.current_room_id == "" and not director.dirty_castle_discovered)


func menu_source_for_hold() -> String:
	return FileAccess.get_file_as_string("res://scripts/start_menu.gd")


func director_source_for_castle_pointer() -> String:
	return FileAccess.get_file_as_string(
		"res://scripts/arena/castle_rooms_25d.gd")


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("START_MENU_ROUTING|", label, ": ", "OK" if ok else "FAIL")
