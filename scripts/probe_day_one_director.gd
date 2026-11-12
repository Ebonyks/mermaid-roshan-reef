extends SceneTree

const DIRECTOR_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")

var checks_failed: int = 0


func _init() -> void:
	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = DIRECTOR_SCRIPT.new(main) as DayOneDirector
	_check("four-room order", director.room_ids() == ["art", "bathroom", "pool", "stuffie"])
	_check("only Craft Room starts unlocked",
		main.day_one_current_room_id == "art"
		and director.unlocked_room_ids() == ["art"])
	_check("jobs globally locked", director.jobs_are_globally_locked()
		and not director.is_job_unlocked("any_job")
		and not director.can_start_opera()
		and not director.is_opera_enabled())
	_check("future rooms locked", not director.can_enter_room("bathroom")
		and not director.can_enter_room("pool"))
	_check("arrival media hook", director.trigger_arrival_plane_media()
		and not director.trigger_arrival_plane_media()
		and main.day_one_event_seen.has(DayOneDirector.EVENT_ARRIVAL_PLANE_MEDIA)
		and main.day_one_event_history.size() == 1)
	director.drain_events()
	_check("Art cannot complete or award brush early",
		not director.complete_art_studio()
		and not director.claim_art_brush()
		and not director.record_art_cleanup("grime", "right_counter"))
	for material_id: String in ["brushes", "pink_paint", "blue_paint", "paint_cups"]:
		director.record_art_cleanup("material", material_id)
	_check("left scrub unlocks desk and enables brush claim",
		director.record_art_cleanup("grime", "left_counter")
		and director.art_desk_unlocked
		and director.claim_art_brush()
		and director.art_brush_earned)
	_check("Craft Room completes after brush award without optional color work",
		director.complete_art_studio()
		and director.is_room_completed("art")
		and main.day_one_current_room_id == "bathroom")
	_check("bathroom cannot complete before basket and both scrubs",
		not director.complete_tutorial("bathroom")
		and not director.can_enter_room("pool"))
	director.bathroom_supply_hunt_step = 2
	director.bathroom_tools_authorized = true
	director.bathroom_cleanup_step = 2
	director.bathroom_toilet_cleaned = true
	_check("bathroom rescue completion unlocks pool",
		director.complete_tutorial("bathroom")
		and bool(main.day_one_completed_rooms.get("bathroom", false))
		and director.is_room_completed("bathroom")
		and director.is_dust_bunny_cleaned("bathroom")
		and director.bathroom_cleanup_step == 3
		and main.day_one_current_room_id == "pool"
		and director.can_enter_room("bathroom")
		and director.can_enter_room("pool"))
	var bathroom_events: Array[Dictionary] = director.drain_events()
	_check("Art and bathroom each emit their cleanup hook",
		_has_cleanup_for(bathroom_events, "art")
		and _has_cleanup_for(bathroom_events, "bathroom"))
	_check("wrong activity rejected", not director.complete_activity("pool", "wrong"))
	_check("pool activity completes", director.complete_placeholder("pool", "pool_activity"))
	_check("pool completion derives full cleanup state",
		director.pool_cleanup_step == 4
		and director.pool_skimmer_mask == 0x3F
		and director.pool_waterfall_mask == 0x07
		and director.pool_seahorse_tugs == 8
		and director.pool_rumi_met)
	_check("stuffie activity completes", director.complete_activity("stuffie", "stuffie_activity"))
	# Every room's cleanup is its own story beat (and story clip). A name-only
	# dedupe once let only the first room cleaned in a session reach the hook.
	var later_events: Array[Dictionary] = director.drain_events()
	_check("pool and Stuffie each emit their own cleanup hook in the same session",
		_has_cleanup_for(later_events, "pool")
		and _has_cleanup_for(later_events, "stuffie"))
	var cleanup_sequence: Array[String] = _cleanup_rooms(bathroom_events)
	cleanup_sequence.append_array(_cleanup_rooms(later_events))
	_check("all four cleanup hooks preserve Craft-first route order",
		cleanup_sequence == ["art", "bathroom", "pool", "stuffie"])
	_check("a repeated room completion never re-emits its cleanup hook",
		not director.complete_activity("stuffie", "stuffie_activity")
		and not _has_cleanup_for(director.drain_events(), "stuffie"))
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
	_check("save keys are additive day-one keys", save_keys_ok
		and int(saved.get("day_one_route_version", 0)) == DayOneDirector.ROUTE_VERSION
		and bool(saved.get("day_one_art_brush_earned", false)))
	var restored_main: ReefMain = ReefMain.new()
	var restored: DayOneDirector = DIRECTOR_SCRIPT.new(restored_main) as DayOneDirector
	restored.restore_state({
		"legacy": "untouched by this module",
		"day_one_completed_rooms": {"ART": "yes", "bathroom": 1, "pool": true,
			"future": true},
		"day_one_grok_video_2_seen": true,
		"day_one_giant_dust_bunny_boss_triggered": true,
	})
	_check("legacy restore preserves old prefix and detours to unfinished Art",
		restored_main.day_one_completed_rooms == {"bathroom": true, "pool": true}
		and restored_main.day_one_current_room_id == "art"
		and restored_main.day_one_cleaned_rooms == {"bathroom": true, "pool": true}
		and restored_main.day_one_bathroom_cleanup_step == 3
		and restored_main.day_one_bathroom_tools_authorized
		and restored_main.day_one_pool_cleanup_step == 4
		and restored_main.day_one_pool_skimmer_mask == 0x3F
		and restored_main.day_one_pool_waterfall_mask == 0x07
		and restored_main.day_one_pool_seahorse_tugs == 8
		and restored_main.day_one_pool_rumi_met
		and not restored_main.day_one_boss_door_glow
		and not restored_main.day_one_giant_dust_bunny_boss_triggered)
	var v2_main: ReefMain = ReefMain.new()
	var v2_restore: DayOneDirector = DIRECTOR_SCRIPT.new(v2_main) as DayOneDirector
	v2_restore.restore_state({
		"day_one_route_version": DayOneDirector.ROUTE_VERSION,
		"day_one_completed_rooms": ["art"],
	})
	_check("v2 Art completion resumes in bathroom and owns the earned brush",
		v2_main.day_one_completed_rooms == {"art": true}
		and v2_main.day_one_current_room_id == "bathroom"
		and v2_main.day_one_art_brush_earned)
	var impossible_main: ReefMain = ReefMain.new()
	var impossible_restore: DayOneDirector = DIRECTOR_SCRIPT.new(impossible_main) as DayOneDirector
	impossible_restore.restore_state({
		"day_one_route_version": DayOneDirector.ROUTE_VERSION,
		"day_one_completed_rooms": ["pool"],
	})
	_check("normalization rejects impossible pool-only completion",
		impossible_main.day_one_completed_rooms.is_empty()
		and impossible_main.day_one_current_room_id == "art")
	var all_done: Dictionary = saved.duplicate(true)
	all_done.erase("day_one_route_version")
	all_done["day_one_completed_rooms"] = ["bathroom", "pool", "stuffie", "art"]
	var final_main: ReefMain = ReefMain.new()
	var final_restore: DayOneDirector = DIRECTOR_SCRIPT.new(final_main) as DayOneDirector
	final_restore.restore_state(all_done)
	_check("restore all rooms derives glow", final_main.day_one_boss_door_glow
		and final_main.day_one_current_room_id == ""
		and not final_main.day_one_giant_dust_bunny_boss_triggered
		and final_main.day_one_active)
	var terminal_save: Dictionary = all_done.duplicate(true)
	terminal_save["day_one_active"] = false
	terminal_save["day_one_giant_dust_bunny_boss_triggered"] = true
	terminal_save["day_one_giant_dust_bunny_boss_defeated"] = true
	var terminal_main: ReefMain = ReefMain.new()
	var terminal_restore: DayOneDirector = DIRECTOR_SCRIPT.new(terminal_main) as DayOneDirector
	terminal_restore.restore_state(terminal_save)
	_check("only a terminal save retains the boss latch",
		terminal_main.day_one_giant_dust_bunny_boss_triggered
		and terminal_main.day_one_giant_dust_bunny_boss_defeated
		and not terminal_main.day_one_active)
	var partial_main: ReefMain = ReefMain.new()
	var partial_restore: DayOneDirector = DIRECTOR_SCRIPT.new(partial_main) as DayOneDirector
	partial_restore.restore_state({
		"day_one_active": true,
		"day_one_completed_rooms": ["bathroom"],
		"day_one_pool_cleanup_step": 2,
		"day_one_pool_skimmer_mask": 0x15,
		"day_one_pool_waterfall_mask": 0x03,
		"day_one_pool_seahorse_tugs": 5,
	})
	_check("partial pool progress restores exactly and monotonically",
		partial_main.day_one_current_room_id == "art"
		and partial_main.day_one_pool_cleanup_step == 2
		and partial_main.day_one_pool_skimmer_mask == 0x15
		and partial_main.day_one_pool_waterfall_mask == 0x03
		and partial_main.day_one_pool_waterfall_progress == [1.0, 1.0, 0.0]
		and partial_main.day_one_pool_seahorse_tugs == 5
		and not partial_main.day_one_pool_rumi_met)
	var fractional_save: Dictionary = partial_restore.serialize_state()
	fractional_save["day_one_pool_cleanup_step"] = 1
	fractional_save["day_one_pool_waterfall_mask"] = 1
	fractional_save["day_one_pool_waterfall_progress"] = [0.1, 0.54, "invalid"]
	partial_restore.restore_state(fractional_save)
	_check("fractional waterfall progress round-trips without awarding a lane",
		partial_main.day_one_pool_waterfall_mask == 1
		and partial_restore.serialize_state()["day_one_pool_waterfall_progress"] == [1.0, 0.54, 0.0])
	var later_main: ReefMain = ReefMain.new()
	var later_day: DayOneDirector = DIRECTOR_SCRIPT.new(later_main) as DayOneDirector
	later_day.restore_state({"day_one_active": false})
	_check("later days release jobs and opera", not later_day.jobs_are_globally_locked()
		and later_day.is_job_unlocked("any_job")
		and later_day.is_opera_enabled()
		and later_day.can_start_opera()
		and not later_day.complete_tutorial("bathroom")
		and bool(later_day.serialize_state().get("day_one_opera_enabled", false)))
	main.free()
	restored_main.free()
	final_main.free()
	partial_main.free()
	later_main.free()
	v2_main.free()
	impossible_main.free()
	terminal_main.free()
	_print_result()
	quit(1 if checks_failed > 0 else 0)


func _events(director: DayOneDirector) -> Array[Dictionary]:
	return director.event_history()


func _has_event(events: Array[Dictionary], event_name: String) -> bool:
	for record: Dictionary in events:
		if String(record.get("event", "")) == event_name:
			return true
	return false


func _has_cleanup_for(events: Array[Dictionary], room_id: String) -> bool:
	for record: Dictionary in events:
		if String(record.get("event", "")) == DayOneDirector.EVENT_DUST_BUNNY_CLEANUP \
				and String((record.get("payload", {}) as Dictionary).get("room_id", "")) == room_id:
			return true
	return false


func _cleanup_rooms(events: Array[Dictionary]) -> Array[String]:
	var room_ids: Array[String] = []
	for record: Dictionary in events:
		if String(record.get("event", "")) != DayOneDirector.EVENT_DUST_BUNNY_CLEANUP:
			continue
		room_ids.append(String((record.get("payload", {}) as Dictionary).get(
			"room_id", "")))
	return room_ids


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE|", label, ": ", ("OK" if ok else "FAIL"))


func _print_result() -> void:
	print("DAY_ONE|RESULT: ", ("PASS" if checks_failed == 0 else "FAIL"),
		" checks_failed=", checks_failed)
