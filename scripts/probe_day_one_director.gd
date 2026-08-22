extends SceneTree

const DIRECTOR_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")

var checks_failed: int = 0


func _init() -> void:
	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = DIRECTOR_SCRIPT.new(main) as DayOneDirector
	_check("four-room order", director.room_ids() == ["bathroom", "pool", "stuffie", "art"])
	_check("only bathroom starts unlocked",
		main.day_one_current_room_id == "bathroom"
		and director.unlocked_room_ids() == ["bathroom"])
	_check("jobs globally locked", director.jobs_are_globally_locked()
		and not director.is_job_unlocked("any_job")
		and not director.can_start_opera()
		and not director.is_opera_enabled())
	_check("future room locked", not director.can_enter_room("pool"))
	_check("arrival media hook", director.trigger_arrival_plane_media()
		and not director.trigger_arrival_plane_media()
		and main.day_one_event_seen.has(DayOneDirector.EVENT_ARRIVAL_PLANE_MEDIA)
		and main.day_one_event_history.size() == 1)
	director.drain_events()
	_check("bathroom placeholder completes",
		director.complete_tutorial("bathroom")
		and bool(main.day_one_completed_rooms.get("bathroom", false))
		and director.is_room_completed("bathroom")
		and director.is_dust_bunny_cleaned("bathroom")
		and main.day_one_current_room_id == "pool"
		and director.can_enter_room("bathroom")
		and director.can_enter_room("pool"))
	var bathroom_events: Array[Dictionary] = director.drain_events()
	_check("completion cleanup hook", _has_event(bathroom_events, "dust_bunny_cleanup"))
	_check("wrong activity rejected", not director.complete_activity("pool", "wrong"))
	_check("pool activity completes", director.complete_placeholder("pool", "pool_activity"))
	_check("stuffie activity completes", director.complete_activity("stuffie", "stuffie_activity"))
	_check("art activity completes", director.complete_activity("art", "art_activity"))
	_check("all completed and boss glow", director.boss_door_glow
		and director.current_room_id == ""
		and director.can_enter_room("bathroom")
		and director.can_enter_room("art"))
	_check("boss trigger gated and idempotent",
		director.trigger_giant_dust_bunny_boss()
		and not director.trigger_giant_dust_bunny_boss()
		and director.giant_dust_bunny_boss_triggered)
	_check("discovery emits both hooks", director.discover_dirty_castle()
		and not director.discover_dirty_castle()
		and director.dirty_castle_discovered
		and director.grok_video_2_seen)
	var saved: Dictionary = director.serialize_state()
	var save_keys_ok: bool = true
	for key: Variant in saved.keys():
		save_keys_ok = save_keys_ok and String(key).begins_with("day_one_")
	_check("save keys are additive day-one keys", save_keys_ok)
	var restored_main: ReefMain = ReefMain.new()
	var restored: DayOneDirector = DIRECTOR_SCRIPT.new(restored_main) as DayOneDirector
	restored.restore_state({
		"legacy": "untouched by this module",
		"day_one_completed_rooms": {"ART": "yes", "bathroom": 1, "pool": true,
			"future": true},
		"day_one_grok_video_2_seen": true,
		"day_one_giant_dust_bunny_boss_triggered": true,
	})
	_check("restore normalises ordered rooms",
		restored_main.day_one_completed_rooms == {"bathroom": true, "pool": true}
		and restored_main.day_one_current_room_id == "stuffie"
		and restored_main.day_one_cleaned_rooms == {"bathroom": true, "pool": true}
		and not restored_main.day_one_boss_door_glow
		and not restored_main.day_one_giant_dust_bunny_boss_triggered)
	var all_done: Dictionary = saved.duplicate(true)
	all_done["day_one_completed_rooms"] = ["bathroom", "pool", "stuffie", "art"]
	var final_main: ReefMain = ReefMain.new()
	var final_restore: DayOneDirector = DIRECTOR_SCRIPT.new(final_main) as DayOneDirector
	final_restore.restore_state(all_done)
	_check("restore all rooms derives glow", final_main.day_one_boss_door_glow
		and final_main.day_one_current_room_id == ""
		and final_main.day_one_giant_dust_bunny_boss_triggered)
	var later_main: ReefMain = ReefMain.new()
	var later_day: DayOneDirector = DIRECTOR_SCRIPT.new(later_main) as DayOneDirector
	later_day.restore_state({"day_one_active": false})
	_check("later days release jobs and opera", not later_day.jobs_are_globally_locked()
		and later_day.is_job_unlocked("any_job")
		and later_day.is_opera_enabled()
		and later_day.can_start_opera()
		and bool(later_day.serialize_state().get("day_one_opera_enabled", false)))
	main.free()
	restored_main.free()
	final_main.free()
	later_main.free()
	_print_result()
	quit(1 if checks_failed > 0 else 0)


func _events(director: DayOneDirector) -> Array[Dictionary]:
	return director.event_history()


func _has_event(events: Array[Dictionary], event_name: String) -> bool:
	for record: Dictionary in events:
		if String(record.get("event", "")) == event_name:
			return true
	return false


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE|", label, ": ", ("OK" if ok else "FAIL"))


func _print_result() -> void:
	print("DAY_ONE|RESULT: ", ("PASS" if checks_failed == 0 else "FAIL"),
		" checks_failed=", checks_failed)
