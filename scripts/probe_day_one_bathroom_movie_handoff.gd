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
	_check("absent movie uses the approved future path hook",
		HANDOFF.normalise_movie_path("") == HANDOFF.DEFAULT_MOVIE_PATH
		and HANDOFF.is_movie_candidate_path(HANDOFF.DEFAULT_MOVIE_PATH)
		and not ResourceLoader.exists(HANDOFF.DEFAULT_MOVIE_PATH))
	_check("present hook accepts a future full-frame stream path",
		HANDOFF.normalise_movie_path("res://future/bathroom_finale.ogv")
		== "res://future/bathroom_finale.ogv"
		and HANDOFF.is_movie_candidate_path("res://future/bathroom_finale.ogv"))

	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = main._day_one_ref()
	director.complete_tutorial("bathroom")
	var fallback: DayOneBathroomMovieHandoff = HANDOFF.new() \
		as DayOneBathroomMovieHandoff
	fallback.setup(main)
	var first: Dictionary = fallback.start_after_completion()
	var second: Dictionary = fallback.start_after_completion()
	_check("absent movie gracefully falls back to clean scene",
		String(first.get("status", "")) == "fallback"
		and int(first.get("playback_count", -1)) == 0
		and int(first.get("fallback_count", -1)) == 1)
	_check("completion and handoff are exactly once across Continue",
		String(second.get("status", "")) == "already_done"
		and int(second.get("playback_count", -1)) == 0
		and bool(main.save_data.get(HANDOFF.HANDOFF_SAVE_KEY, false)))

	var interrupted_main: ReefMain = ReefMain.new()
	var interrupted_director: DayOneDirector = interrupted_main._day_one_ref()
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
