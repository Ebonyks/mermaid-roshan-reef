extends SceneTree
## Contract probe for the two optional Day One bathroom movie seams.

const HANDOFF := preload("res://scripts/day_one_bathroom_movie_handoff.gd")

var checks_failed: int = 0


func _init() -> void:
	var handoff_source: String = FileAccess.get_file_as_string(
		"res://scripts/day_one_bathroom_movie_handoff.gd")
	var main_source: String = FileAccess.get_file_as_string(
		"res://scripts/main.gd")
	var completion_start: int = main_source.find(
		"func day_one_complete_bathroom_scene()")
	var completion_source: String = main_source.substr(completion_start) \
		if completion_start >= 0 else ""
	var save_order: int = completion_source.find("_write_save()")
	var handoff_order: int = completion_source.find(
		"_start_day_one_bathroom_movie_handoff()")
	_check("cleanup movie seam follows committed bathroom completion",
		save_order >= 0 and handoff_order > save_order
		and completion_source.contains("director.is_room_completed(\"bathroom\")"))
	_check("entry movie blocks before the basket rescue is constructed",
		main_source.find("_day_one_bathroom_entry_movie_blocks_cleanup()") >= 0
		and main_source.find("_day_one_bathroom_entry_movie_blocks_cleanup()")
			< main_source.find("DayOneBathroomCleanupLogic.new()"))
	_check("both movies are optional full-frame Canvas2D overlays",
		handoff_source.contains("VideoStreamPlayer.new()")
		and handoff_source.contains("Control.PRESET_FULL_RECT")
		and handoff_source.contains("modal_input_blocker")
		and handoff_source.contains("player_active"))
	_check("two stable future OGV paths and save keys exist",
		HANDOFF.DEFAULT_ENTRY_MOVIE_PATH.ends_with(
			"day_one_bathroom_entry.ogv")
		and HANDOFF.DEFAULT_CLEANUP_MOVIE_PATH.ends_with(
			"day_one_bathroom_cleaned.ogv")
		and HANDOFF.ENTRY_SAVE_KEY != HANDOFF.CLEANUP_SAVE_KEY
		and not ResourceLoader.exists(HANDOFF.DEFAULT_ENTRY_MOVIE_PATH)
		and not ResourceLoader.exists(HANDOFF.DEFAULT_CLEANUP_MOVIE_PATH))
	var marker_position: int = handoff_source.find(
		"m.save_data[save_key] = true")
	var marker_save_position: int = handoff_source.find(
		"_flush_save()", marker_position)
	var play_position: int = handoff_source.find("_play(stream)")
	_check("a present movie commits its phase marker before playback",
		marker_position >= 0 and marker_save_position > marker_position
		and play_position > marker_save_position)
	_check("paths normalize independently and reject non-OGV media",
		HANDOFF.normalise_movie_path("", HANDOFF.PHASE_ENTRY)
			== HANDOFF.DEFAULT_ENTRY_MOVIE_PATH
		and HANDOFF.normalise_movie_path("", HANDOFF.PHASE_CLEANUP)
			== HANDOFF.DEFAULT_CLEANUP_MOVIE_PATH
		and HANDOFF.is_movie_candidate_path("res://future/bathroom.ogv")
		and not HANDOFF.is_movie_candidate_path(
			"res://future/bathroom.mp4"))

	var entry_main: ReefMain = ReefMain.new()
	var entry: DayOneBathroomMovieHandoff = HANDOFF.new() \
		as DayOneBathroomMovieHandoff
	entry.setup(entry_main, HANDOFF.PHASE_ENTRY)
	var entry_first: Dictionary = entry.start_before_cleanup()
	var entry_second: Dictionary = entry.start_before_cleanup()
	_check("absent entry movie fails open exactly once in memory",
		String(entry_first.get("status", "")) == "fallback"
		and String(entry_second.get("status", "")) == "already_done"
		and int(entry_first.get("playback_count", -1)) == 0
		and not bool(entry_main.save_data.get(HANDOFF.ENTRY_SAVE_KEY, false))
		and bool(entry.audit_snapshot().get(
			"seamless_dirty_scene_cut", false)))
	entry_main.save_data[HANDOFF.ENTRY_SAVE_KEY] = true
	var restored_entry: DayOneBathroomMovieHandoff = HANDOFF.new() \
		as DayOneBathroomMovieHandoff
	restored_entry.setup(entry_main, HANDOFF.PHASE_ENTRY)
	_check("saved entry marker prevents replay across Continue",
		String(restored_entry.start_before_cleanup().get("status", ""))
			== "already_done")

	var cleanup_main: ReefMain = ReefMain.new()
	var director: DayOneDirector = cleanup_main._day_one_ref()
	director.bathroom_supply_hunt_step = 2
	director.bathroom_tools_authorized = true
	director.bathroom_cleanup_step = 2
	director.complete_tutorial("bathroom")
	var cleanup: DayOneBathroomMovieHandoff = HANDOFF.new() \
		as DayOneBathroomMovieHandoff
	cleanup.setup(cleanup_main, HANDOFF.PHASE_CLEANUP)
	var cleanup_first: Dictionary = cleanup.start_after_completion()
	var cleanup_second: Dictionary = cleanup.start_after_completion()
	_check("absent cleanup movie falls through to the clean room",
		String(cleanup_first.get("status", "")) == "fallback"
		and String(cleanup_second.get("status", "")) == "already_done"
		and int(cleanup_first.get("playback_count", -1)) == 0
		and not bool(cleanup_main.save_data.get(
			HANDOFF.CLEANUP_SAVE_KEY, false))
		and bool(cleanup.audit_snapshot().get(
			"seamless_clean_scene_cut", false)))
	_check("pool picture waits while either movie or its save is active",
		main_source.contains("_day_one_bathroom_movie_handoff_pending")
		and main_source.contains("_day_one_bathroom_movie_is_playing()")
		and main_source.contains("not save_dirty and not save_pending"))
	_check("generic room action is not restored by cleanup completion",
		not main_source.contains("castle_room_action_button.visible = true"))

	entry.free()
	restored_entry.free()
	cleanup.free()
	entry_main.free()
	cleanup_main.free()
	print("DAY_ONE_BATHROOM_MOVIE_HANDOFF|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_BATHROOM_MOVIE_HANDOFF|", label, ": ",
		"OK" if ok else "FAIL")
