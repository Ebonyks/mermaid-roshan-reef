extends SceneTree
## Contract probe for the optional Day One bathroom end-movie seam.

const HANDOFF := preload("res://scripts/day_one_bathroom_movie_handoff.gd")

var checks_failed: int = 0


class SaveWriter:
	var attempts: int = 0
	var fail_first: bool = true

	func write() -> bool:
		attempts += 1
		return not fail_first or attempts > 1


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
	_check("movie seam is wired after bathroom completion save",
		save_order >= 0 and handoff_order > save_order
		and completion_source.contains("director.is_room_completed(\"bathroom\")"))
	_check("future movie is an optional full-frame Canvas2D overlay",
		handoff_source.contains("VideoStreamPlayer.new()")
		and handoff_source.contains("Control.PRESET_FULL_RECT")
		and handoff_source.contains("player_active"))
	_check("movie path is an additive contract, not a delivered asset",
		handoff_source.contains("DEFAULT_MOVIE_PATH")
		and handoff_source.contains("ResourceLoader.exists(movie_path)")
		and not ResourceLoader.exists(HANDOFF.DEFAULT_MOVIE_PATH))
	var marker_position: int = handoff_source.find(
		"HANDOFF_SAVE_KEY] = true")
	var marker_save_position: int = handoff_source.find(
		"_flush_save()", marker_position)
	var play_position: int = handoff_source.find("_play(stream)")
	_check("handoff marker is committed before playback",
		marker_position >= 0 and marker_save_position > marker_position
		and play_position > marker_save_position)
	_check("absent movie uses the approved future path hook",
		HANDOFF.normalise_movie_path("") == HANDOFF.DEFAULT_MOVIE_PATH
		and HANDOFF.is_movie_candidate_path(HANDOFF.DEFAULT_MOVIE_PATH)
		and not ResourceLoader.exists(HANDOFF.DEFAULT_MOVIE_PATH))
	_check("present hook accepts a future full-frame stream path",
		HANDOFF.normalise_movie_path("res://future/bathroom_finale.ogv")
		== "res://future/bathroom_finale.ogv"
		and HANDOFF.is_movie_candidate_path("res://future/bathroom_finale.ogv")
		and not HANDOFF.is_movie_candidate_path(
			"res://future/bathroom_finale.mp4"))

	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = main._day_one_ref()
	director.bathroom_supply_hunt_step = 2
	director.bathroom_tools_authorized = true
	director.bathroom_cleanup_step = 2
	director.complete_tutorial("bathroom")
	var fallback: DayOneBathroomMovieHandoff = HANDOFF.new() \
		as DayOneBathroomMovieHandoff
	fallback.setup(main)
	var first: Dictionary = fallback.start_after_completion()
	var second: Dictionary = fallback.start_after_completion()
	_check("absent movie gracefully falls back to clean scene",
		String(first.get("status", "")) == "fallback"
		and int(first.get("playback_count", -1)) == 0
		and int(first.get("fallback_count", -1)) == 1
		and bool(fallback.audit_snapshot().get(
			"seamless_clean_scene_cut", false)))
	_check("completion and handoff are exactly once across Continue",
		String(second.get("status", "")) == "already_done"
		and int(second.get("playback_count", -1)) == 0
		and bool(main.save_data.get(HANDOFF.HANDOFF_SAVE_KEY, false)))

	var interrupted_main: ReefMain = ReefMain.new()
	var interrupted_director: DayOneDirector = interrupted_main._day_one_ref()
	interrupted_director.bathroom_supply_hunt_step = 2
	interrupted_director.bathroom_tools_authorized = true
	interrupted_director.bathroom_cleanup_step = 2
	interrupted_director.complete_tutorial("bathroom")
	var writer := SaveWriter.new()
	var interrupted: DayOneBathroomMovieHandoff = HANDOFF.new() \
		as DayOneBathroomMovieHandoff
	interrupted.setup(interrupted_main)
	interrupted.set_save_writer(Callable(writer, "write"))
	var pending: Dictionary = interrupted.start_after_completion()
	_check("interrupted marker save never starts playback",
		String(pending.get("status", "")) == "save_pending"
		and int(pending.get("playback_count", -1)) == 0
		and not bool(interrupted_main.save_data.get(HANDOFF.HANDOFF_SAVE_KEY, false)))
	var recovered: Dictionary = interrupted.start_after_completion()
	_check("handoff retries safely after save recovery",
		String(recovered.get("status", "")) == "fallback"
		and writer.attempts == 2
		and bool(interrupted_main.save_data.get(HANDOFF.HANDOFF_SAVE_KEY, false)))

	fallback.free()
	interrupted.free()
	main.free()
	interrupted_main.free()
	print("DAY_ONE_BATHROOM_MOVIE_HANDOFF|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_BATHROOM_MOVIE_HANDOFF|", label, ": ",
		"OK" if ok else "FAIL")
