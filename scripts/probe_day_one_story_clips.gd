extends SceneTree
## Trusted contract for the Day One story clips (owner decision 2026-09-23,
## DL-CIN-16): manifest integrity, fail-open lookup, real OGV playback, the
## single Back skip route, the story hook map, the transformation-then-epilogue
## queue ahead of the Day Two card, save persistence, and Grand Puff staying
## whole for the transformation clip instead of imploding.

const CLIPS := preload("res://scripts/day_one_story_clips.gd")
const PROVENANCE_PATH := \
	"res://assets_src/cinematics/day_one_story_clips_2026-09-23/CLIP_MANIFEST.json"
const PROBE_SAVE := "user://probe_day_one_story_clips.json"
const SAVE_SUFFIXES := ["", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp",
	".bak.old", ".before_new_game"]
const EXPECTED: Array[String] = [
	"d1_opening", "d1_castle", "d1_bath_arrival", "d1_bath_clean",
	"d1_pool_arrival", "d1_pool_clean", "d1_eagle_free", "d1_art_arrival",
	"d1_art_clean", "d1_rainbow_route", "d1_puff_arrival",
	"d1_puff_transformation", "d1_epilogue",
]
const HOOKS: Array[String] = [
	'_day_one_play_story_clip("d1_opening")',
	'_day_one_play_story_clip("d1_castle")',
	'"bathroom": movie_id = "d1_bath_arrival"',
	'"pool": movie_id = "d1_pool_arrival"',
	'"art": movie_id = "d1_art_arrival"',
	'"bathroom": "d1_bath_clean", "pool": "d1_pool_clean"',
	'"stuffie": "d1_eagle_free", "art": "d1_art_clean"',
	'_day_one_play_story_clip("d1_rainbow_route")',
	'_day_one_play_story_clip("d1_puff_arrival")',
	'_day_one_play_story_clip("d1_puff_transformation")',
	'_day_one_play_story_clip("d1_epilogue")',
]
var failures: int = 0
var _behavior_started: bool = false


func _init() -> void:
	_check("manifest lists the 13 story clips in story order",
		CLIPS.clip_ids() == EXPECTED)
	var all_present: bool = true
	for id: String in EXPECTED:
		if not CLIPS.available(id) or CLIPS.seconds_for(id) <= 0.0:
			all_present = false
	_check("every story clip exists at its manifest path", all_present)
	_check("the opening is the 30-second introduction to the game",
		absf(CLIPS.seconds_for("d1_opening") - 30.54) < 0.1)
	_check("unknown and traversal ids fail open",
		not CLIPS.available("d1_missing") and CLIPS.path_for("../d1_opening") == "")
	_check("headless runs stay deterministic unless a probe opts in",
		not CLIPS.enabled())
	var provenance: String = FileAccess.get_file_as_string(PROVENANCE_PATH)
	_check("every clip is an owner-directed runtime clip, never delivery-accepted",
		provenance.count('"status": "OWNER_DIRECTED_RUNTIME_CLIP"') == EXPECTED.size()
		and not provenance.contains('"status": "DELIVERY_ACCEPTED"'))
	var main_source: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	var hooks_ok: bool = true
	for hook: String in HOOKS:
		if not main_source.contains(hook):
			hooks_ok = false
			print("DAY_ONE_STORY_CLIPS|missing hook: ", hook)
	_check("every story moment is wired to its clip", hooks_ok)
	_check("the global Back control is the one skip route",
		main_source.contains(
			'_navigation_push("day_one_story_clip", preview, Callable(preview, "skip"))')
		and FileAccess.get_file_as_string("res://scripts/day_one_story_clips.gd").contains(
			"mouse_filter = Control.MOUSE_FILTER_STOP"))
	call_deferred("_run_behavioral_checks")


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_STORY_CLIPS|", label, ": ", "OK" if ok else "FAIL")


func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame


func _clean_save() -> void:
	for suffix: String in SAVE_SUFFIXES:
		var path: String = ProjectSettings.globalize_path(PROBE_SAVE + suffix)
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)


func _run_behavioral_checks() -> void:
	if _behavior_started:
		return
	_behavior_started = true
	CLIPS.headless_override = true
	# --- the standalone player ---
	var missing: DayOneStoryClips = CLIPS.new() as DayOneStoryClips
	get_root().add_child(missing)
	paused = true
	_check("a missing clip fails open and leaves a paused tree paused",
		not missing.setup("d1_missing") and paused)
	missing.free()
	paused = false
	var preview: DayOneStoryClips = CLIPS.new() as DayOneStoryClips
	get_root().add_child(preview)
	var signals: Array[int] = [0]
	preview.finished.connect(func(_id: String, _status: String) -> void:
		signals[0] += 1)
	_check("a real clip sets up and pauses the game behind it",
		preview.setup("d1_rainbow_route") and paused)
	await _frames(2)
	_check("the real OGV begins playback", preview.player != null
		and preview.player.is_playing())
	preview.skip()
	preview.skip()
	_check("skip is once-only and restores the unpaused game",
		signals[0] == 1 and not paused)
	await _frames(1)
	# --- the story through ReefMain ---
	_clean_save()
	var main := (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, PROBE_SAVE)
	get_root().add_child(main)
	await _frames(3)
	if main.intro_active:
		main._skip_intro()
	await _frames(3)
	# Emulate the real win boundary: Day One is complete (the opening already
	# seen), then the story hooks fire exactly as the boss victory emits them.
	main._day_one_ref().arrival_plane_media_seen = true
	main._day_one_ref().day_one_active = false
	main._on_day_one_hook_event(DayOneDirector.EVENT_GIANT_DUST_BUNNY_BOSS_DEFEATED, {})
	_check("the boss-defeated hook plays the transformation clip",
		main._day_one_story_clip != null
		and main._day_one_story_clip.movie_id == "d1_puff_transformation" and paused)
	main._on_day_one_hook_event(DayOneDirector.EVENT_DAY_TWO_BEGINS, {})
	_check("the Day Two hook queues the epilogue behind it",
		main._day_one_story_clip_queue == ["d1_epilogue"])
	main._show_day_two_transition()
	_check("the Day Two card waits for the story",
		main._day_one_story_boss_transition_pending)
	main._day_one_story_clip.skip()
	await _frames(3)
	_check("Back hands the story over to the queued epilogue",
		main._day_one_story_clip != null
		and main._day_one_story_clip.movie_id == "d1_epilogue")
	main._day_one_story_clip.skip()
	await _frames(3)
	_check("after the epilogue the Day Two card is shown",
		main._day_one_story_clip == null
		and not main._day_one_story_boss_transition_pending
		and main.day_two_transition_active)
	_check("a story clip never replays on the same save",
		not main._day_one_play_story_clip("d1_puff_transformation"))
	main._write_save()
	var saved: Variant = main.save_data.get("day_one_story_clips_seen", {})
	_check("watched clips persist in the save",
		saved is Dictionary and (saved as Dictionary).has("d1_puff_transformation")
		and (saved as Dictionary).has("d1_epilogue"))
	main.queue_free()
	await _frames(3)
	# --- Grand Puff stays whole for the transformation ---
	var boss: DustBunnyBossSprite = DustBunnyBossSprite.new()
	get_root().add_child(boss)
	await _frames(2)
	var ended: Array[int] = [0]
	boss.implosion_finished.connect(func() -> void:
		ended[0] += 1)
	boss.transform_ending = true
	boss.boss_health_rounds_remaining = 0
	boss.hold_for_transformation()
	_check("Grand Puff stays visible and ends without imploding",
		boss.sprite != null and boss.sprite.visible and boss.defeated
		and ended[0] == 1 and String(boss.sprite.animation) != "implode")
	boss.queue_free()
	await _frames(1)
	CLIPS.headless_override = false
	_clean_save()
	print("DAY_ONE_STORY_CLIPS|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
