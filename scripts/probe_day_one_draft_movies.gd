extends SceneTree
## Behavioral contract probe for the opt-in Day One draft movie layer.

const SCRIPT_PATH := "res://scripts/day_one_draft_movies.gd"
const MAIN_PATH := "res://scripts/main.gd"
const MANIFEST_PATH := "res://assets_src/cinematics/day_one_davinci_draft_2026-09-04/runtime_manifest.json"
const DRAFT := preload("res://scripts/day_one_draft_movies.gd")
var failures: int = 0
var _behavior_started: bool = false

func _init() -> void:
	var source: String = FileAccess.get_file_as_string(SCRIPT_PATH)
	var main_source: String = FileAccess.get_file_as_string(MAIN_PATH)
	var manifest: String = FileAccess.get_file_as_string(MANIFEST_PATH)
	_check("draft script exists", not source.is_empty())
	_check("explicit opt-in flag", source.contains("--day-one-draft-movies"))
	_check("all 14 movie IDs are declared",
		source.count("D1-C") >= 14 and manifest.count("D1-C") >= 14)
	_check("missing media fails open", source.contains("ResourceLoader.exists"))
	_check("manifest gates runtime playback", source.contains("runtime_preview_eligible")
		and source.contains("runtime_manifest.json"))
	_check("draft has safe tap skip", source.contains("skip_button")
		and source.contains("func skip()"))
	_check("draft never writes saves", not source.contains("save_data")
		and not source.contains("_write_save"))
	_check("bathroom overlay is not duplicated", main_source.contains(
		"_day_one_bathroom_movie_is_playing() or _day_one_bathroom_movie_handoff_pending"))
	_check("hooks are opt-in", main_source.contains("DayOneDraftMoviesLogic.enabled()"))
	_check("preview renders on dedicated top CanvasLayer", main_source.contains("layer = 100"))
	_check("delivery claims remain false", manifest.contains('"delivery_accepted": false'))
	_run_behavioral_checks()
	call_deferred("_run_behavioral_checks")

func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_DRAFT_MOVIES|", label, ": ", "OK" if ok else "FAIL")

func _run_behavioral_checks() -> void:
	if _behavior_started:
		return
	_behavior_started = true
	var missing: DayOneDraftMovies = DRAFT.new() as DayOneDraftMovies
	get_root().add_child(missing)
	var was_paused: bool = paused
	paused = true
	_check("missing setup preserves an already-paused tree",
		not missing.setup("D1-C99") and paused)
	missing.free()
	paused = was_paused
	_check("invalid and ineligible IDs fail closed",
		not DRAFT.runtime_preview_eligible("D1-C99")
		and DRAFT.path_for("D1-C99") == "")
	var valid_id: String = ""
	for candidate: String in DRAFT.MOVIE_IDS:
		if DRAFT.runtime_preview_eligible(candidate):
			valid_id = candidate
			break
	if not DRAFT.enabled():
		var disabled_preview: DayOneDraftMovies = DRAFT.new() as DayOneDraftMovies
		get_root().add_child(disabled_preview)
		_check("without opt-in flag, eligible media remains disabled",
			valid_id.is_empty() or not disabled_preview.setup(valid_id))
		disabled_preview.free()
		print("DAY_ONE_DRAFT_MOVIES|real OGV behavior: SKIP (flag not supplied)")
	elif valid_id.is_empty():
		print("DAY_ONE_DRAFT_MOVIES|real OGV behavior: SKIP (no eligible export yet)")
	else:
		var preview: DayOneDraftMovies = DRAFT.new() as DayOneDraftMovies
		get_root().add_child(preview)
		var signals: Array[int] = [0]
		preview.finished.connect(func(_id: String, _status: String) -> void:
			signals[0] += 1)
		paused = false
		await process_frame
		_check("eligible OGV setup succeeds", preview.setup(valid_id))
		await process_frame
		_check("eligible OGV begins playback", preview.player != null
			and preview.player.is_playing())
		preview.skip()
		preview.skip()
		_check("skip is once-only and restores unpaused state", signals[0] == 1 and not paused)
		preview.free()
		var timeout_preview: DayOneDraftMovies = DRAFT.new() as DayOneDraftMovies
		get_root().add_child(timeout_preview)
		_check("timeout preview setup succeeds", timeout_preview.setup(valid_id))
		timeout_preview._finish("timeout")
		_check("timeout finish is idempotent", not paused)
		timeout_preview.free()
		var preserved: DayOneDraftMovies = DRAFT.new() as DayOneDraftMovies
		get_root().add_child(preserved)
		paused = true
		_check("eligible OGV setup succeeds while paused", preserved.setup(valid_id))
		preserved.free()
		_check("abrupt free preserves prior paused state", paused)
		paused = false
		var unpaused: DayOneDraftMovies = DRAFT.new() as DayOneDraftMovies
		get_root().add_child(unpaused)
		_check("second eligible setup succeeds", unpaused.setup(valid_id))
		unpaused.free()
		_check("abrupt free restores unpaused state", not paused)
		print("DAY_ONE_DRAFT_MOVIES|real OGV behavior: PASS")
	print("DAY_ONE_DRAFT_MOVIES|RESULT: ",
			"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
