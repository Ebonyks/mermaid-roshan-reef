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
	"res://scripts/games/dust_boss.gd": [
		"m.day_one_complete_boss_and_begin_day_two()",
		"m._end_game(true, fr",
	],
}

var failures: int = 0
var main: ReefMain


func _init() -> void:
	main = ReefMain.new()
	var director: DayOneDirector = main._day_one_ref()
	_check("director uses ReefMain state owner", director.m == main)
	_check("Day One starts with jobs and opera locked",
		main.day_one_jobs_locked() and not main.day_one_opera_enabled())
	_check("only physical bathroom route starts unlocked",
		main.day_one_can_enter_castle_room("main_hall")
		and main.day_one_can_enter_castle_room("bubble_bath")
		and not main.day_one_can_enter_castle_room("mermaid_pool")
		and not main.day_one_can_enter_castle_room("opera_hall"))
	# Match the live bathroom completion contract: the basket authorizes both
	# tools, then the drain and grime gestures must be complete.
	director.bathroom_tools_authorized = true
	director.bathroom_supply_hunt_step = 2
	director.bathroom_cleanup_step = 2
	director.complete_tutorial("bathroom")
	_check("completion advances the physical castle route",
		main.day_one_can_enter_castle_room("bubble_bath")
		and main.day_one_can_enter_castle_room("mermaid_pool")
		and not main.day_one_can_enter_castle_room("playroom"))
	_check("Day Two cannot bypass the real boss defeat",
		not director.complete_day_one_after_boss())
	_check("remaining physical rooms arm the real boss boundary",
		director.complete_placeholder("pool", "pool_activity")
		and director.complete_activity("stuffie", "stuffie_activity")
		and director.complete_activity("art", "art_activity")
		and director.boss_door_glow)
	# This lightweight policy probe has no rendered arena. The full
	# probe_dust_boss run below owns the physical trigger; mark that already-
	# verified boundary here so emitting the terminal event cannot try to build
	# a 3D arena on an unready ReefMain.
	director.giant_dust_bunny_boss_triggered = true
	_check("the recorded boss defeat starts Chapter 2 before Day Two",
		director.complete_giant_dust_bunny_boss()
		and main.chapter2_active
		and main.chapter2_unlocked_opera_mask
		== ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK
		and director.complete_day_one_after_boss()
		and not director.complete_day_one_after_boss())
	_check("Day Two policy releases rooms, jobs, and opera",
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
	_check("save normalization cannot skip the room order",
		patch.get("day_one_completed_rooms", []) == ["bathroom", "pool"]
		and String(patch.get("day_one_current_room", "")) == "stuffie")
	var legacy_terminal: Dictionary = {
		"day_one_active": false,
		"day_one_completed_rooms": DayOneDirector.ROOM_ORDER.duplicate(),
		"day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER.duplicate(),
		"day_one_giant_dust_bunny_boss_triggered": true,
		"chapter3_fairy_door_revealed": true,
		"chapter3_fairy_door_opened": false,
	}
	var save_state := SaveState.new(main)
	var migrated: Dictionary = save_state._normalise_save(legacy_terminal)
	_check("exact origin Day-Two terminal backfills the boss defeat",
		bool(migrated.get(
			"day_one_giant_dust_bunny_boss_defeated", false))
		and bool(migrated.get("chapter2_active", false))
		and int(migrated.get("chapter2_unlocked_opera_mask", 0))
		== ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK)
	_check("Day-Two migration preserves independent Chapter 3 door state",
		bool(migrated.get("chapter3_fairy_door_revealed", false))
		and not bool(migrated.get("chapter3_fairy_door_opened", true)))
	var unrelated: Dictionary = legacy_terminal.duplicate(true)
	unrelated["day_one_giant_dust_bunny_boss_triggered"] = false
	var untouched: Dictionary = save_state._normalise_save(unrelated)
	_check("inactive or unlocked legacy data alone cannot invent a defeat",
		not bool(untouched.get(
			"day_one_giant_dust_bunny_boss_defeated", true))
		and not bool(untouched.get("chapter2_active", true)))


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
