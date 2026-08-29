extends SceneTree
## Focused launch-policy probe. It keeps Continue and New Game on opposite
## sides of the Day 1 boundary without booting the heavyweight world or
## touching the real child save.

var failures: int = 0


func _init() -> void:
	var main := ReefMain.new()
	main._prepare_start_menu_launch(false)
	_check("completed or legacy Continue stays beyond Day 1",
		not main.day_one_is_active())
	_check("Continue bypasses the legacy intro", not main.first_session)
	main._prepare_start_menu_launch(true)
	_check("partial Day 1 Continue preserves Day 1", main.day_one_is_active())
	_check("New Game bypasses the legacy intro", not main.first_session)
	_probe_wiring()
	main.free()
	print("START_MENU_ROUTING|RESULT: ",
		"PASS" if failures == 0 else "FAIL",
		" failures=", failures)
	quit(1 if failures > 0 else 0)


func _probe_wiring() -> void:
	var main_source: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	var menu_source: String = FileAccess.get_file_as_string("res://scripts/start_menu.gd")
	_check("startup waits for the menu or probe driver",
		not main_source.contains(
			"START_AT_CASTLE_GATE and DisplayServer.get_name()"))
	_check("Continue preserves the loaded Day 1 route",
		menu_source.contains(
			"m._launch_from_start_menu(m.day_one_is_active())"))
	_check("New Game calls the Day 1 route after reload",
		menu_source.contains("m._launch_from_start_menu(true)"))
	_check("New Game reload marker survives the scene reset",
		menu_source.contains("DAY_ONE_AFTER_RESET_META")
		and menu_source.contains("reload_current_scene"))
	_check("menu cannot invoke the retired legacy intro",
		not menu_source.contains("_build_intro"))


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("START_MENU_ROUTING|", label, ": ", "OK" if ok else "FAIL")
