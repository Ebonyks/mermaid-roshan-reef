extends SceneTree
## Focused Day One wiring probe. It exercises ReefMain's policy seam without
## running the heavyweight world boot, then verifies every live boundary calls
## that seam so the standalone logic cannot become dead code.

const REQUIRED_WIRING: Dictionary = {
	"res://scripts/main.gd": [
		"DayOneDirector.new(self)",
		"func day_one_try_enter_castle_room",
		"func day_one_activate_castle_room",
		"_day_one_begin_arrival()",
		"_day_one_discover_dirty_castle()",
		"_start_game(dust_boss_fr)",
	],
	"res://scripts/save_state.gd": [
		"m._day_one_ref().restore_state(m.save_data)",
		"m._day_one_ref().serialize_state()",
		"DayOneDirector.normalise_save_patch(raw)",
	],
	"res://scripts/arena/castle_rooms_25d.gd": [
		"m.day_one_try_enter_castle_room(start_room)",
		"m.day_one_try_enter_castle_room(room_id)",
		"m.day_one_activate_castle_room(m.castle_room_id)",
		"m._day_one_attach_castle_dressing()",
		"m._day_one_clear_castle_dressing()",
	],
	"res://scripts/castle_career_routes.gd": [
		"m.day_one_jobs_locked()",
	],
}

var failures: int = 0


func _init() -> void:
	var main := ReefMain.new()
	var director: DayOneDirector = main._day_one_ref()
	_check("director uses ReefMain state owner", director.m == main)
	_check("Day One starts with jobs and opera locked",
		main.day_one_jobs_locked() and not main.day_one_opera_enabled())
	_check("only physical bathroom route starts unlocked",
		main.day_one_can_enter_castle_room("main_hall")
		and main.day_one_can_enter_castle_room("bubble_bath")
		and not main.day_one_can_enter_castle_room("mermaid_pool")
		and not main.day_one_can_enter_castle_room("opera_hall"))
	director.complete_tutorial("bathroom")
	_check("completion advances the physical castle route",
		main.day_one_can_enter_castle_room("bubble_bath")
		and main.day_one_can_enter_castle_room("craft_room")
		and not main.day_one_can_enter_castle_room("mermaid_pool")
		and not main.day_one_can_enter_castle_room("playroom"))
	director.restore_state({"day_one_active": false})
	_check("later-day policy releases rooms, jobs, and opera",
		main.day_one_can_enter_castle_room("opera_hall")
		and not main.day_one_jobs_locked()
		and main.day_one_opera_enabled())
	_probe_save_patch()
	_probe_wiring()
	main.free()
	print("DAY_ONE_INTEGRATION|RESULT: ",
		"PASS" if failures == 0 else "FAIL",
		" failures=", failures)
	quit(1 if failures > 0 else 0)


func _probe_save_patch() -> void:
	var patch: Dictionary = DayOneDirector.normalise_save_patch({
		"legacy_key": "preserved by SaveState's duplicate",
		"day_one_completed_rooms": ["bathroom", "pool", "art"],
	})
	_check("save normalization preserves old-route completion membership",
		patch.get("day_one_completed_rooms", []) == ["bathroom", "art", "pool"]
		and String(patch.get("day_one_current_room", "")) == "stuffie")


func _probe_wiring() -> void:
	for path_value: Variant in REQUIRED_WIRING:
		var path: String = String(path_value)
		var source: String = FileAccess.get_file_as_string(path)
		_check("wiring source is readable: " + path, not source.is_empty())
		for token_value: Variant in REQUIRED_WIRING[path]:
			var token: String = String(token_value)
			_check("wired %s -> %s" % [path.get_file(), token],
				source.contains(token))


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_INTEGRATION|", label, ": ", "OK" if ok else "FAIL")
