extends SceneTree
## Day One semantic voice contract probe.
##
## The Parler filler manifest is the current authority. This probe exercises the
## real AudioDirector resolver (including its speaker-prefix ownership), checks
## that every live Day One objective has an exact non-generic stream, and proves
## that a generic cheer cannot interrupt an objective line.

const AUDIO_DIRECTOR := preload("res://scripts/audio_director.gd")

const REQUIRED_CUES: Array[String] = [
	"castle_home_day_one", "castle_door_resting", "day_one_jobs_resting",
	"day_one_rescue_bunnies", "day_one_finish_current",
	"day_one_room_clean", "day_one_new_door", "day_one_all_rooms_clean",
	"day_one_pool_ready", "bathroom_supplies_found", "bathroom_cleanup_start",
	"bathroom_basket_hint", "bathroom_sink_scrub", "bathroom_tub_drain",
	"bathroom_tub_brush", "bathroom_cleanup_done", "pool_surface_clean",
	"pool_waterfall_clean", "pool_seahorse_clean",
	"castle_playroom_rescue_start", "art_studio_hint",
	"art_studio_material_hint", "art_studio_scrub_hint", "dustboss_show",
	"dustboss_tell_opening", "dustboss_tell_shielded", "dustboss_again_miss",
	"dustboss_again_closer", "dustboss_again_mercy", "dustboss_dizzy_first",
	"dustboss_dizzy_round", "dustboss_angry", "dustboss_win",
	"day_two_begins",
]

var failures := 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var main := ReefMain.new()
	get_root().add_child(main)
	main.day_one_active = true
	for _index: int in range(2):
		var player := AudioStreamPlayer.new()
		main.add_child(player)
		main.voice_pool.append(player)
	var director := AUDIO_DIRECTOR.new(main)
	for suffix: String in REQUIRED_CUES:
		var path: String = director._voice_path("roshan", suffix, false)
		_check("exact filler path for %s" % suffix,
			path == "res://assets/audio/voices/filler_v1/roshan_%s.ogg" % suffix
			and not path.ends_with("voice_yay.mp3"))
		_check("required event is classified: %s" % suffix,
			director._is_required_day_one_event(suffix))
	_check("prefixed event still resolves one speaker prefix",
		director._voice_path("roshan", "roshan_bathroom_basket_hint", false)
			== "res://assets/audio/voices/filler_v1/roshan_bathroom_basket_hint.ogg")
	_check("generic talk remains distinct from required objective paths",
		director._voice_path("roshan", "talk", false)
			== "res://assets/audio/voices/filler_v1/roshan_talk.ogg")

	# A required line starts first; the generic success/talk paths must not
	# replace it in the same frame. The second exact objective is queued instead.
	director._say("roshan", "bathroom_basket_hint")
	var first: AudioStreamPlayer = main.voice_pool[0] as AudioStreamPlayer
	var first_stream: AudioStream = first.stream
	director._say("roshan", "talk")
	_check("generic talk cannot truncate required objective",
		first.stream == first_stream and director._active_required_key
		== "roshan_bathroom_basket_hint")
	director._say("roshan", "bathroom_sink_scrub")
	_check("second Roshan objective is queued, not overlapped",
		director._required_voice_queue.size() == 1)
	_check("required path never resolves retired fallback",
		not director._voice_path("roshan", "bathroom_basket_hint", false)
			.ends_with("voice_yay.mp3"))

	print("DAY_ONE_VOICE|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	main.queue_free()
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_VOICE|", label, ": ", "OK" if ok else "FAIL")
