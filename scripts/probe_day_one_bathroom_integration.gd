extends SceneTree
## Focused persistence and physical-route probe for the first Day One rescue.

const DIRECTOR_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")
const REQUIRED_WIRING: Dictionary = {
	"res://scripts/main.gd": [
		"var day_one_bathroom_cleanup_step: int = 0",
		"var day_one_bathroom_rebuild_replay_pending: bool = false",
		"func day_one_record_bathroom_cleanup_step",
		"func day_one_record_bathroom_supply_step",
		"func day_one_complete_bathroom_scene",
		"start_day_one_bathroom_cleanup()",
	],
	"res://scripts/arena/castle_rooms_25d.gd": [
		"DAY_ONE_BATHROOM_CLEANUP",
		"_sync_day_one_bathroom_cleanup(room_id)",
		"m.day_one_complete_bathroom_scene()",
		"m.day_one_bathroom_rebuild_replay_pending",
	],
	"res://scripts/day_one_director.gd": [
		"day_one_bathroom_cleanup_step",
		"day_one_bathroom_supply_hunt_step",
		"day_one_bathroom_rebuild_replay_pending",
		"complete_bathroom_rebuild_replay",
		"saved_bathroom_step",
	],
}

var checks_failed: int = 0


func _init() -> void:
	var main := ReefMain.new()
	var director: DayOneDirector = DIRECTOR_SCRIPT.new(main) as DayOneDirector
	_check("bathroom rescue is the first playable room",
		director.current_room_id == "bathroom"
		and director.unlocked_room_ids() == ["bathroom"]
		and not director.can_enter_room("pool"))
	main.day_one_bathroom_cleanup_step = 2
	main.day_one_bathroom_supply_hunt_step = 1
	var mid_rescue_save: Dictionary = director.serialize_state()
	_check("mid-rescue step enters the additive Day One save",
		int(mid_rescue_save.get("day_one_bathroom_cleanup_step", -1)) == 2)
	_check("mid-hunt supply progress enters additive Day One save",
		int(mid_rescue_save.get("day_one_bathroom_supply_hunt_step", -1)) == 1)

	var restored_main := ReefMain.new()
	var restored: DayOneDirector = DIRECTOR_SCRIPT.new(restored_main) \
		as DayOneDirector
	restored.restore_state(mid_rescue_save)
	_check("mid-rescue progress restores without unlocking the pool",
		restored_main.day_one_bathroom_cleanup_step == 2
		and restored.current_room_id == "bathroom"
		and not restored.can_enter_room("pool"))
	_check("mid-hunt supply progress restores without loss",
		restored_main.day_one_bathroom_supply_hunt_step == 1)
	_check("partial bathroom completion cannot unlock the pool",
		not restored_main.day_one_complete_bathroom_scene()
		and restored.current_room_id == "bathroom"
		and not restored.can_enter_room("pool"))
	restored_main.day_one_bathroom_supply_hunt_step = 2
	_check("bathroom completion unlocks the pool after both gestures",
		restored.complete_tutorial("bathroom")
		and restored_main.day_one_bathroom_cleanup_step == 3
		and restored.current_room_id == "pool"
		and restored.can_enter_room("bathroom")
		and restored.can_enter_room("pool")
		and not restored.can_enter_room("stuffie"))

	var legacy_patch: Dictionary = DayOneDirector.normalise_save_patch({
		"day_one_active": false,
		"day_one_completed_rooms": ["bathroom"],
	})
	_check("Continue-mode primitive saves queue the rebuilt rescue",
		not bool(legacy_patch.get("day_one_active", true))
		and int(legacy_patch.get("day_one_bathroom_cleanup_step", -1)) == 0
		and int(legacy_patch.get(
			"day_one_bathroom_supply_hunt_step", -1)) == 0
		and bool(legacy_patch.get(
			"day_one_bathroom_rebuild_replay_pending", false))
		and not bool(legacy_patch.get(
			"day_one_bathroom_rebuild_replay_seen", true))
		and String(legacy_patch.get("day_one_current_room", "")) == "pool")
	var legacy_main: ReefMain = ReefMain.new()
	var legacy_director: DayOneDirector = DIRECTOR_SCRIPT.new(legacy_main) \
		as DayOneDirector
	legacy_director.restore_state(legacy_patch)
	var legacy_events_before: int = legacy_director.event_history().size()
	legacy_main.day_one_bathroom_cleanup_step = 2
	legacy_main.day_one_bathroom_supply_hunt_step = 2
	_check("rebuilt replay preserves old progress and pool access",
		legacy_director.complete_bathroom_rebuild_replay()
		and legacy_director.is_room_completed("bathroom")
		and legacy_director.current_room_id == "pool"
		and legacy_director.can_enter_room("pool")
		and not legacy_main.day_one_bathroom_rebuild_replay_pending
		and legacy_main.day_one_bathroom_rebuild_replay_seen
		and legacy_main.day_one_bathroom_cleanup_step == 3
		and legacy_main.day_one_bathroom_supply_hunt_step == 2
		and legacy_director.event_history().size() == legacy_events_before)
	var modern_patch: Dictionary = DayOneDirector.normalise_save_patch(
		legacy_director.serialize_state())
	_check("completed rebuilt rescue does not replay again",
		not bool(modern_patch.get(
			"day_one_bathroom_rebuild_replay_pending", true))
		and bool(modern_patch.get(
			"day_one_bathroom_rebuild_replay_seen", false)))
	var interrupted_patch: Dictionary = DayOneDirector.normalise_save_patch({
		"day_one_bathroom_cleanup_step": 3,
	})
	_check("a saved final wipe cannot skip director completion",
		int(interrupted_patch.get("day_one_bathroom_cleanup_step", -1)) == 3
		and String(interrupted_patch.get("day_one_current_room", "")) == "bathroom"
		and (interrupted_patch.get("day_one_completed_rooms", []) as Array).is_empty())
	_probe_wiring()
	main.free()
	restored_main.free()
	legacy_main.free()
	print("DAY_ONE_BATHROOM_INTEGRATION|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


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
		checks_failed += 1
	print("DAY_ONE_BATHROOM_INTEGRATION|", label, ": ",
		"OK" if ok else "FAIL")
