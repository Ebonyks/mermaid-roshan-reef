extends SceneTree
## Focused persistence and physical-route probe for the first Day One rescue.

const DIRECTOR_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")
const REQUIRED_WIRING: Dictionary = {
	"res://scripts/main.gd": [
		"var day_one_bathroom_cleanup_step: int = 0",
		"DayOneBathroomCleanupLogic",
		"func day_one_record_bathroom_cleanup_step",
		"func day_one_record_bathroom_supply_step",
		"func day_one_complete_bathroom_scene",
		"func _sync_day_one_bathroom_cleanup",
		"func _clear_day_one_bathroom_cleanup",
		"_start_day_one_bathroom_movie_handoff()",
		"if not day_one_is_active():",
	],
	"res://scripts/day_one_director.gd": [
		"day_one_bathroom_cleanup_step",
		"day_one_bathroom_supply_hunt_step",
		"saved_bathroom_step",
	],
}

var checks_failed: int = 0


func _init() -> void:
	var main := ReefMain.new()
	var director: DayOneDirector = main._day_one_ref()
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
	var restored: DayOneDirector = restored_main._day_one_ref()
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
	restored_main.day_one_bathroom_tools_authorized = true
	var bathroom_completed: bool = restored.complete_tutorial("bathroom")
	_check("bathroom completion unlocks the pool after both gestures",
		bathroom_completed
		and restored_main.day_one_bathroom_cleanup_step == 3
		and restored.current_room_id == "pool"
		and restored.can_enter_room("bathroom")
		and restored.can_enter_room("pool")
		and not restored.can_enter_room("stuffie"))
	_check("completed bathroom rescue is strictly one-shot",
		not restored.complete_tutorial("bathroom")
		and restored.current_room_id == "pool")

	var legacy_patch: Dictionary = DayOneDirector.normalise_save_patch({
		"day_one_active": false,
		"day_one_completed_rooms": ["bathroom"],
	})
	_check("post-Day-One saves never queue the bathroom rescue again",
		not bool(legacy_patch.get("day_one_active", true))
		and int(legacy_patch.get("day_one_bathroom_cleanup_step", -1)) == 3
		and int(legacy_patch.get(
			"day_one_bathroom_supply_hunt_step", -1)) == 2
		and String(legacy_patch.get("day_one_current_room", "")) == "pool")
	var inactive_main: ReefMain = ReefMain.new()
	inactive_main.day_one_active = false
	inactive_main.day_one_bathroom_cleanup_step = 2
	inactive_main.day_one_bathroom_supply_hunt_step = 2
	_check("inactive Day One cannot complete or relaunch the bathroom rescue",
		not inactive_main.day_one_complete_bathroom_scene())
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
	inactive_main.free()
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
	var main_source: String = FileAccess.get_file_as_string(
		"res://scripts/main.gd")
	var completion_start: int = main_source.find(
		"func day_one_complete_bathroom_scene()")
	var completion_source: String = main_source.substr(completion_start) \
		if completion_start >= 0 else ""
	var save_order: int = completion_source.find("_write_save()")
	var movie_order: int = completion_source.find(
		"_start_day_one_bathroom_movie_handoff()")
	_check("bathroom entry automatically builds the dirty rescue",
		main_source.contains("not day_one_castle_room_is_clean(\"bubble_bath\")")
		and main_source.contains("DayOneBathroomCleanupLogic.new()"))
	_check("clean rescue emits whole-room sparkle and pool pointer seam",
		main_source.contains("_day_one_sync_castle_dressing()")
		and main_source.contains("_burst(\"✦\""))
	_check("pool route uses approved picture and pointer without a UI box",
		main_source.contains("sign_mermaid_pool.png")
		and main_source.contains("PoolRouteGhostHand")
		and main_source.contains("StyleBoxEmpty.new()")
		and not main_source.contains(
			"style_icon_button(_day_one_pool_route_button"))
	_check("completion saves before starting the optional movie handoff",
		save_order >= 0 and movie_order > save_order)
	_check("completion and movie handoff are Day One-only and one-shot",
		completion_source.contains("if not day_one_is_active():")
		and completion_source.contains("director.is_room_completed(\"bathroom\")")
		and main_source.contains("_day_one_bathroom_movie_handoff != null"))
	var cleanup_source: String = FileAccess.get_file_as_string(
		"res://scripts/games/day_one_bathroom_cleanup.gd")
	_check("bathroom route owns the basket-to-sink handoff",
		cleanup_source.contains("_build_basket()")
		and cleanup_source.contains("_build_dirty_overlays()")
		and cleanup_source.contains("begin_cleaning_handoff()"))
	var sealed_castle_source: String = FileAccess.get_file_as_string(
		"res://scripts/arena/castle_rooms_25d.gd")
	_check("bathroom rescue does not alter the sealed castle frame owner",
		not sealed_castle_source.contains("DAY_ONE_BATHROOM_CLEANUP")
		and not sealed_castle_source.contains(
			"_sync_day_one_bathroom_cleanup"))


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_BATHROOM_INTEGRATION|", label, ": ",
		"OK" if ok else "FAIL")
