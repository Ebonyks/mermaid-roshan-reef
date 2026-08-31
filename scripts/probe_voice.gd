extends SceneTree

var bad := 0

const MELODY_VOICE_PATH := \
	"res://assets/audio/voices/filler_v1/roshan_op_popstar_rhythm.ogg"
const MELODY_VOICE_SHA256 := \
	"6f6839b043dc58647324f1d04df6429ccf3bb197b175bfd89317ff1b9e2ead4d"
const MELODY_OBJECTIVE := "Tap each rainbow note in the green!"
const YAY_PATH := "res://assets/audio/voices/filler_v1/yay.ogg"
const YAY_SHA256 := \
	"66be8684f15000fb917f8d93728e6b43e473935eb7de74bc13f32d57d7246759"
const ROSHAN_TALK_PATH := "res://assets/audio/voices/filler_v1/roshan_talk.ogg"
const ROSHAN_TALK_SHA256 := \
	"bd0cf6fa76e5cff31f35fc4717fb6a54b7bc3a7935ed8f3bf535499cfcfa52da"
const SLIDE_TALK_PATH := "res://assets/audio/voices/filler_v1/harper.ogg"
const SLIDE_TALK_SHA256 := \
	"46dda4a090600ce83a9278f7aa99015a62c542a5ca9951860711973b519936e7"
const SLIDE_TALK_SECONDS := 2.4265
const SLIDE_HINT_PATH := "res://assets/audio/voices/filler_v1/harper_hint.ogg"
const SLIDE_HINT_SHA256 := \
	"46dda4a090600ce83a9278f7aa99015a62c542a5ca9951860711973b519936e7"
const SLIDE_HINT_SECONDS := 2.4265
const SLIDE_OBJECTIVE := "Come slide with us! Grab the fishies!"
const SLIDE_TOUCH_INDEX := 81


class CountingAudioDirector:
	extends AudioDirector

	var requests: Array[Dictionary] = []
	var accepted: Array[Dictionary] = []

	func _say(speaker: String, event: String = "", min_gap: float = 0.0) -> void:
		var request := {"speaker": speaker, "event": event, "min_gap": min_gap}
		requests.append(request)
		var voice_before: int = m.voice_i
		super._say(speaker, event, min_gap)
		if m.voice_i == voice_before + 1:
			accepted.append(request)


func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	main._skip_intro()
	await process_frame
	var licenses := FileAccess.get_file_as_string("res://ASSET_LICENSES.md")
	var voice_manifest := FileAccess.get_file_as_string(
		"res://assets/audio/voices/VOICE_MANIFEST.md")
	var voice_generator := FileAccess.get_file_as_string(
		"res://tools/make_voices.py")
	_check("Harper objective filler retains exact generator and ledger provenance",
		licenses.contains("assets/audio/voices/filler_v1/*.ogg")
		and licenses.contains("Parler-TTS Mini v1.1")
		and voice_manifest.contains("filler_v1/FILLER_MANIFEST.json")
		and voice_generator.contains(
			'"harper":     ("harper", "Come slide with us! Grab the fishies!"),'))
	_check("Yay and This is so much fun are exact synthetic filler cues",
		ResourceLoader.exists(YAY_PATH)
		and FileAccess.get_sha256(YAY_PATH) == YAY_SHA256
		and ResourceLoader.exists(ROSHAN_TALK_PATH)
		and FileAccess.get_sha256(ROSHAN_TALK_PATH) == ROSHAN_TALK_SHA256
		and voice_generator.contains('"yay":           ("roshan", "Yay!"),')
		and voice_generator.contains(
			'"roshan_talk":   ("roshan", "This is so much fun!"),'))
	var expected_events := [
		"talk", "whale", "ship", "wreck", "beans", "intro1", "intro4",
		"win", "pearl", "op_popstar_rhythm", "op_racer_tune_up",
		"op_racer_to_the_line",
	]
	var present := 0
	for ln: String in expected_events:
		if ResourceLoader.exists("res://assets/audio/voices/filler_v1/roshan_%s.ogg" % ln):
			present += 1
	_check("expected Roshan clips present", present == expected_events.size(),
		"%d / %d" % [present, expected_events.size()])
	_check("Racer repair owns exact generated objective text",
		voice_generator.contains(
			'"roshan_op_racer_tune_up": ("roshan", "Turn the wrench in big circles. Tighten every wheel before the race!"),')
		and voice_generator.contains(
			'"roshan_op_racer_to_the_line": ("roshan", "Push the kart all the way out to the starting line!"),'))

	# Exercise the real reaction branches. Ship and wreck are currently guarded
	# behind removed runtime art, so deterministic probe-only Node3Ds keep their
	# voice routing covered without restoring either discarded feature.
	var whale := Node3D.new()
	var ship := Node3D.new()
	main.add_child(whale)
	main.add_child(ship)
	main.whale_node = whale
	main.manta = ship
	main.game = ""
	main.finale_t = -1.0
	main.intro_active = false
	main.msg_timer = 5.0
	main.clear_dialogue()

	whale.position = Vector3(10.0, 0.0, 10.0)
	ship.position = Vector3(1000.0, 0.0, 1000.0)
	main.wreck_pos = Vector3(2000.0, 0.0, 2000.0)
	main.roshan_spot_cool = 0.0
	main.said_cool.erase("roshan_whale")
	var before := main.voice_i
	main._tick_roshan_reactions(0.0, whale.position)
	_check_exact_cue(main, "whale", before)
	main.clear_dialogue()

	whale.position = Vector3(1000.0, 0.0, 1000.0)
	ship.position = Vector3(20.0, 0.0, 20.0)
	main.roshan_spot_cool = 0.0
	main.said_cool.erase("roshan_ship")
	before = main.voice_i
	main._tick_roshan_reactions(0.0, ship.position)
	_check_exact_cue(main, "ship", before)
	main.clear_dialogue()

	ship.position = Vector3(1000.0, 0.0, 1000.0)
	main.wreck_pos = Vector3(30.0, 0.0, 30.0)
	main.roshan_spot_cool = 0.0
	main.said_cool.erase("roshan_wreck")
	before = main.voice_i
	main._tick_roshan_reactions(0.0, main.wreck_pos)
	_check_exact_cue(main, "wreck", before)
	main.clear_dialogue()

	# Avoid award_sticker's separate success cheer so this assertion isolates
	# the beans cue itself and proves _beans_go emits exactly one spoken line.
	main.stickers["beans"] = true
	main.said_cool.erase("roshan_beans")
	before = main.voice_i
	main._beans_go()
	_check_exact_cue(main, "beans", before)

	var brawl_audio := CountingAudioDirector.new(main)
	main._audio_dir = brawl_audio
	await _check_melody_message_cue(main, brawl_audio)
	await _check_slide_message_cue(main, brawl_audio)
	await _check_brawl_message_cues(main, brawl_audio)
	_check_dialogue_speech_lifecycle(main)

	print("VOICE|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit(1 if bad > 0 else 0)


func _check_melody_message_cue(main: ReefMain,
		audio: CountingAudioDirector) -> void:
	# Melody's child-facing sentence is a project-owned exact recording. Daddy's
	# numbered sacred archive clips are intentionally not objective substitutes.
	var friend: Dictionary = {}
	var melody_routes := 0
	for candidate_value: Variant in main.friends:
		var candidate: Dictionary = candidate_value as Dictionary
		if String(candidate.get("game", "")) == "melody":
			melody_routes += 1
			if friend.is_empty():
				friend = candidate
	_check("Melody Daddy route exists for exact cue coverage",
		melody_routes == 1 and not friend.is_empty()
		and String(friend.get("fname", "")) == "Daddy Mermaid")
	if friend.is_empty():
		return
	main.clear_dialogue()
	main.said_cool.erase("roshan_op_popstar_rhythm")
	var before: int = main.voice_i
	var requests_before: int = audio.requests.size()
	main._start_game_now(friend)
	_check_named_cue(main, audio, "Melody entry", "roshan",
		"op_popstar_rhythm", before, requests_before)
	_check("Melody exact cue path and immutable bytes are present",
		ResourceLoader.exists(MELODY_VOICE_PATH)
		and FileAccess.get_sha256(MELODY_VOICE_PATH) == MELODY_VOICE_SHA256
		and _stream_path(_last_pool_player(main)) == MELODY_VOICE_PATH)
	_check("Melody entry retains the exact semantic objective copy",
		main.game == "melody" and main.hud_msg.text == MELODY_OBJECTIVE)
	main.clear_dialogue()
	main._clear_game()
	await process_frame
	await process_frame


func _check_slide_message_cue(main: ReefMain,
		audio: CountingAudioDirector) -> void:
	# Harper's discovery, Hybrid focus, and Canvas entry use different semantic
	# moments, but every one resolves to the same exact family recording. Cover
	# the complete real route: discovery -> immediate focus -> immediate entry,
	# a fresh focus -> delayed entry while the clip is still audible, and a
	# fresh Classic proximity entry with no preceding spoken focus.
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(1280, 720)
	await _frames(3)
	var friend: Dictionary = {}
	var friend_index := -1
	var slide_routes := 0
	for index in range(main.friends.size()):
		var candidate: Dictionary = main.friends[index]
		if String(candidate.get("game", "")) == "slide" \
				and String(candidate.get("mode", "")) == "fish":
			slide_routes += 1
			if friend.is_empty():
				friend = candidate
				friend_index = index
	_check("Harper and Fiona own one exact fish-slide friend route",
		slide_routes == 1 and friend_index >= 0
		and String(friend.get("fname", "")) == "Harper and Fiona")
	if friend.is_empty():
		return

	# Discovery speaks harper_talk. An immediate focus asks for harper_hint, but
	# both keys contain the same immutable take and the same-speaker guard lets
	# the discovery sentence finish without a restart. Entry
	# then requests no additional playback: voice plus the persistent steer cues are
	# the instruction, while the opaque stage intentionally remains text-free.
	main.clear_dialogue()
	main._set_touch_mode(main.TOUCH_MODE_HYBRID, false)
	var friend_node: Variant = friend.get("node")
	friend["found"] = false
	friend["cool"] = 0.0
	main.said_cool.erase("harper_talk")
	main.said_cool.erase("harper_hint")
	var requests_before: int = audio.requests.size()
	var accepted_before: int = audio.accepted.size()
	var voice_before: int = main.voice_i
	main.player.position = friend_node.position
	main.player.position.x += 3.0
	main.player.vel *= 0.0
	await _frames(10)
	var discovery_stamp: float = float(main.said_cool.get(
		"harper_talk", -99.0))
	main._populate_touch_interactables()
	var target_id := "friend:%d" % friend_index
	var target_projection: Dictionary = _slide_voice_target_projection(
		main, target_id)
	var screen_point: Vector2 = target_projection.get(
		"point", Vector2(-1.0, -1.0)) as Vector2
	var immediate_before_focus_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	immediate_before_focus_diag["target_projection"] = \
		target_projection.duplicate(true)
	_push_touch(main, screen_point, true, SLIDE_TOUCH_INDEX)
	_push_touch(main, screen_point, false, SLIDE_TOUCH_INDEX)
	await process_frame
	var immediate_focus_exact: bool = \
		bool(target_projection.get("exact", false)) \
		and main.touch_focus_id == target_id \
		and main.touch_focus_ready and main.game == ""
	var focus_stamp: float = float(main.said_cool.get("harper_hint", -99.0))
	var immediate_after_focus_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	immediate_after_focus_diag["target_projection"] = \
		target_projection.duplicate(true)
	main._populate_touch_interactables()
	target_projection = _slide_voice_target_projection(main, target_id)
	screen_point = target_projection.get(
		"point", Vector2(-1.0, -1.0)) as Vector2
	var immediate_entry_target_exact: bool = bool(
		target_projection.get("exact", false))
	_push_touch(main, screen_point, true, SLIDE_TOUCH_INDEX + 1)
	_push_touch(main, screen_point, false, SLIDE_TOUCH_INDEX + 1)
	await process_frame
	var immediate_after_entry_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	immediate_after_entry_diag["target_projection"] = \
		target_projection.duplicate(true)

	var discovery_request: Dictionary = audio.requests[requests_before] \
		if audio.requests.size() > requests_before else {}
	var focus_request: Dictionary = audio.requests[requests_before + 1] \
		if audio.requests.size() > requests_before + 1 else {}
	var accepted_request: Dictionary = audio.accepted[accepted_before] \
		if audio.accepted.size() > accepted_before else {}
	var player := _last_pool_player(main)
	var slide := main._game_obj("race", SlideRaceGame) as SlideRaceGame
	var snapshot: Dictionary = slide.audit_snapshot()
	var immediate_route_exact: bool = \
		immediate_focus_exact and immediate_entry_target_exact \
		and bool(friend.get("found", false)) and main.game == "slide" \
		and String(main.g.get("mode", "")) == "fish" \
		and bool(snapshot.get("route_exact", false))
	var immediate_semantics_exact: bool = \
		audio.requests.size() == requests_before + 2 \
		and String(discovery_request.get("speaker", "")) == "harper" \
		and String(discovery_request.get("event", "")) == "talk" \
		and String(focus_request.get("speaker", "")) == "harper" \
		and String(focus_request.get("event", "")) == "hint" \
		and is_equal_approx(float(discovery_request.get(
			"min_gap", -1.0)), 0.5) \
		and is_equal_approx(float(focus_request.get("min_gap", -1.0)), 0.5) \
		and focus_stamp >= discovery_stamp \
		and focus_stamp - discovery_stamp < SLIDE_TALK_SECONDS
	var immediate_playback_exact: bool = \
		audio.accepted.size() == accepted_before + 1 \
		and String(accepted_request.get("speaker", "")) == "harper" \
		and String(accepted_request.get("event", "")) == "talk" \
		and main.voice_i == voice_before + 1 \
		and _playing_pool_count(main) == 1
	var immediate_stage_exact: bool = \
		player != null and player.stream != null and player.playing \
		and _stream_path(player) == SLIDE_TALK_PATH \
		and ResourceLoader.exists(SLIDE_TALK_PATH) \
		and FileAccess.get_sha256(SLIDE_TALK_PATH) == SLIDE_TALK_SHA256 \
		and ResourceLoader.exists(SLIDE_HINT_PATH) \
		and FileAccess.get_sha256(SLIDE_HINT_PATH) == SLIDE_HINT_SHA256 \
		and absf(player.stream.get_length() - SLIDE_TALK_SECONDS) < 0.02 \
		and SlideRaceGame.FISH_OBJECTIVE_VOICE_WINDOW \
			> player.stream.get_length() \
		and SlideRaceGame.FISH_OBJECTIVE == SLIDE_OBJECTIVE \
		and main.hud_msg.text.is_empty() and not main.hud_msg.visible \
		and is_zero_approx(main.msg_timer) \
		and bool(snapshot.get("steer_cues_persistent", false)) \
		and _slide_voice_cues_live(slide)
	_check("real Harper discovery, immediate focus, and PLAY enter the Canvas",
		immediate_route_exact)
	_check("discovery and focus request their exact semantic Harper keys",
		immediate_semantics_exact)
	_check("discovery finishes without a focus or entry restart",
		immediate_playback_exact)
	_check("discovery route resolves immutable Harper audio and keeps the opaque stage text-free",
		immediate_stage_exact)
	if not (immediate_route_exact and immediate_semantics_exact \
			and immediate_playback_exact and immediate_stage_exact):
		print("VOICE_DIAG|hybrid-immediate|before=%s|focus=%s|entry=%s" % [
			immediate_before_focus_diag, immediate_after_focus_diag,
			immediate_after_entry_diag,
		])
	await _close_slide_voice_fixture(main)

	# With discovery already known, focus is the one speaking edge. Delay the
	# entry by a real 0.85 seconds: longer than the generic 0.5 cooldown but
	# deliberately shorter than the exact objective recording.
	main._set_touch_mode(main.TOUCH_MODE_HYBRID, false)
	friend["found"] = true
	friend["cool"] = 0.0
	main.player.position = friend_node.position
	main.player.position.x += 3.0
	main.player.vel *= 0.0
	await _frames(10)
	main._populate_touch_interactables()
	target_projection = _slide_voice_target_projection(main, target_id)
	screen_point = target_projection.get(
		"point", Vector2(-1.0, -1.0)) as Vector2
	main.said_cool.erase("harper_talk")
	main.said_cool.erase("harper_hint")
	requests_before = audio.requests.size()
	accepted_before = audio.accepted.size()
	voice_before = main.voice_i
	var delayed_before_focus_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	delayed_before_focus_diag["target_projection"] = \
		target_projection.duplicate(true)
	_push_touch(main, screen_point, true, SLIDE_TOUCH_INDEX + 2)
	_push_touch(main, screen_point, false, SLIDE_TOUCH_INDEX + 2)
	await process_frame
	var delayed_focus_exact: bool = \
		bool(target_projection.get("exact", false)) \
		and main.touch_focus_id == target_id \
		and main.touch_focus_ready and main.game == ""
	var delayed_focus_msec: int = Time.get_ticks_msec()
	var delayed_after_focus_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	delayed_after_focus_diag["target_projection"] = \
		target_projection.duplicate(true)
	await _wait_wall_msec(850)
	main._populate_touch_interactables()
	target_projection = _slide_voice_target_projection(main, target_id)
	screen_point = target_projection.get(
		"point", Vector2(-1.0, -1.0)) as Vector2
	var delayed_entry_target_exact: bool = bool(
		target_projection.get("exact", false))
	var delayed_entry_msec: int = Time.get_ticks_msec()
	var delayed_before_entry_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	delayed_before_entry_diag["target_projection"] = \
		target_projection.duplicate(true)
	_push_touch(main, screen_point, true, SLIDE_TOUCH_INDEX + 3)
	_push_touch(main, screen_point, false, SLIDE_TOUCH_INDEX + 3)
	await process_frame
	var delayed_after_entry_diag: Dictionary = _slide_voice_hybrid_diag(
		main, friend, screen_point, audio, requests_before,
		accepted_before, voice_before)
	delayed_after_entry_diag["target_projection"] = \
		target_projection.duplicate(true)
	var delayed_seconds: float = float(
		delayed_entry_msec - delayed_focus_msec) / 1000.0
	player = _last_pool_player(main)
	snapshot = slide.audit_snapshot()
	var delayed_request: Dictionary = audio.requests[requests_before] \
		if audio.requests.size() > requests_before else {}
	var delayed_route_exact: bool = \
		delayed_focus_exact and delayed_entry_target_exact \
		and delayed_seconds >= 0.75 and delayed_seconds <= 1.0 \
		and delayed_seconds < SLIDE_HINT_SECONDS \
		and main.game == "slide" and String(main.g.get("mode", "")) == "fish" \
		and bool(snapshot.get("route_exact", false))
	var delayed_playback_exact: bool = \
		audio.requests.size() == requests_before + 1 \
		and audio.accepted.size() == accepted_before + 1 \
		and main.voice_i == voice_before + 1 \
		and String(delayed_request.get("speaker", "")) == "harper" \
		and String(delayed_request.get("event", "")) == "hint" \
		and _playing_pool_count(main) == 1
	var delayed_stage_exact: bool = \
		player != null and player.playing \
		and _stream_path(player) == SLIDE_HINT_PATH \
		and FileAccess.get_sha256(SLIDE_HINT_PATH) == SLIDE_HINT_SHA256 \
		and SlideRaceGame.FISH_OBJECTIVE == SLIDE_OBJECTIVE \
		and main.hud_msg.text.is_empty() and not main.hud_msg.visible \
		and is_zero_approx(main.msg_timer) \
		and bool(snapshot.get("steer_cues_persistent", false)) \
		and _slide_voice_cues_live(slide)
	_check("delayed real Hybrid focus then PLAY enters the exact Canvas route",
		delayed_route_exact)
	_check("delayed Hybrid entry requests no duplicate playback while Harper is audible",
		delayed_playback_exact)
	_check("delayed route retains exact objective audio, steer cues, and a text-free stage",
		delayed_stage_exact)
	if not (delayed_route_exact and delayed_playback_exact \
			and delayed_stage_exact):
		print(("VOICE_DIAG|hybrid-delayed|before=%s|focus=%s" \
			+ "|before_entry=%s|entry=%s") % [
			delayed_before_focus_diag, delayed_after_focus_diag,
			delayed_before_entry_diag, delayed_after_entry_diag,
		])
	await _close_slide_voice_fixture(main)

	# Classic has no focus cue. With both semantic timestamps freshened away,
	# its real proximity entry must speak the same objective exactly once.
	main._set_touch_mode(main.TOUCH_MODE_CLASSIC, false)
	main.said_cool.erase("harper_talk")
	main.said_cool.erase("harper_hint")
	friend["found"] = true
	friend["cool"] = 0.0
	requests_before = audio.requests.size()
	accepted_before = audio.accepted.size()
	voice_before = main.voice_i
	main.player.position = friend_node.position
	main.player.position.x += 3.0
	main.player.vel *= 0.0
	var classic_guard := 0
	while main.game == "" and classic_guard < 120:
		classic_guard += 1
		await process_frame
	player = _last_pool_player(main)
	snapshot = slide.audit_snapshot()
	var classic_request: Dictionary = audio.requests[requests_before] \
		if audio.requests.size() > requests_before else {}
	_check("fresh Classic proximity enters and speaks one Harper objective",
		main.game == "slide" and String(main.g.get("mode", "")) == "fish"
		and audio.requests.size() == requests_before + 1
		and audio.accepted.size() == accepted_before + 1
		and main.voice_i == voice_before + 1
		and String(classic_request.get("speaker", "")) == "harper"
		and String(classic_request.get("event", "")) == "hint"
		and _playing_pool_count(main) == 1)
	_check("Classic entry retains exact objective audio, steer cues, and a text-free stage",
		player != null and player.playing
		and _stream_path(player) == SLIDE_HINT_PATH
		and FileAccess.get_sha256(SLIDE_HINT_PATH) == SLIDE_HINT_SHA256
		and SlideRaceGame.FISH_OBJECTIVE == SLIDE_OBJECTIVE
		and main.hud_msg.text.is_empty() and not main.hud_msg.visible
		and is_zero_approx(main.msg_timer)
		and bool(snapshot.get("steer_cues_persistent", false))
		and _slide_voice_cues_live(slide))

	# Cross the real controller's passive loop boundary with no steer. The retry
	# must request the same recorded objective directly, remain non-winning, and
	# keep the opaque Canvas free of hidden/unrecorded caption text.
	await _wait_slide_ready(main, slide)
	main.clear_dialogue()
	main.said_cool["harper_hint"] = Time.get_ticks_msec() / 1000.0 \
		- SlideRaceGame.FISH_OBJECTIVE_VOICE_WINDOW - 0.25
	requests_before = audio.requests.size()
	accepted_before = audio.accepted.size()
	voice_before = main.voice_i
	main.g["steered"] = false
	main.g["canvas_run_start_t"] = float(main.g.get("t", 0.0)) \
		- SlideRaceGame.FISH_RUN_SECONDS
	slide._tick_canvas_fish(0.0, friend)
	var retry_request: Dictionary = audio.requests[requests_before] \
		if audio.requests.size() > requests_before else {}
	player = _last_pool_player(main)
	snapshot = slide.audit_snapshot()
	_check("passive loop retries the exact direct Harper objective once without winning",
		audio.requests.size() == requests_before + 1
		and audio.accepted.size() == accepted_before + 1
		and main.voice_i == voice_before + 1
		and String(retry_request.get("speaker", "")) == "harper"
		and String(retry_request.get("event", "")) == "hint"
		and is_equal_approx(float(retry_request.get("min_gap", -1.0)),
			SlideRaceGame.FISH_OBJECTIVE_VOICE_WINDOW)
		and player != null and player.playing
		and _stream_path(player) == SLIDE_HINT_PATH
		and _playing_pool_count(main) == 1
		and main.game == "slide" and not bool(main.g.get("steered", true))
		and not bool(snapshot.get("completed", true))
		and is_zero_approx(float(snapshot.get("progress", -1.0)))
		and main.hud_msg.text.is_empty() and not main.hud_msg.visible
		and is_zero_approx(main.msg_timer)
		and bool(snapshot.get("steer_cues_persistent", false))
		and _slide_voice_cues_live(slide))
	await _close_slide_voice_fixture(main)
	main._set_touch_mode(main.TOUCH_MODE_CLASSIC, false)


func _close_slide_voice_fixture(main: ReefMain) -> void:
	var route_friend: Dictionary = main.g.get("fr", {}) as Dictionary
	if not route_friend.is_empty():
		route_friend["cool"] = 10.0
	main.clear_dialogue()
	main._clear_game()
	var deadline_msec: int = Time.get_ticks_msec() + 1500
	while main.fade_rect != null \
			and main.fade_rect.mouse_filter != Control.MOUSE_FILTER_IGNORE \
			and Time.get_ticks_msec() < deadline_msec:
		await process_frame
	var guard_deadline_msec: int = Time.get_ticks_msec() + 1500
	while bool(main.call("_slide_canvas_return_guard_active")) \
			and Time.get_ticks_msec() < guard_deadline_msec:
		await process_frame
	_check("voice fixture return guard retires before the next forced route",
		not bool(main.call("_slide_canvas_return_guard_active")))


func _slide_voice_target_projection(main: ReefMain,
		target_id: String) -> Dictionary:
	var target: Dictionary = {}
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if String(item.get("id", "")) == target_id:
			target = item
			break
	var out := {
		"target": target,
		"point": Vector2(-1.0, -1.0),
		"behind": true,
		"exact": false,
	}
	if target.is_empty():
		return out
	var camera: Variant = main.active_viewport_camera()
	var target_node: Variant = target.get("node")
	if camera == null or target_node == null \
			or not is_instance_valid(target_node):
		return out
	var target_position: Variant = target_node.get("global_position")
	var behind: bool = camera.is_position_behind(target_position)
	out["behind"] = behind
	if behind:
		return out
	var projected: Vector2 = camera.unproject_position(target_position)
	var visible_rect: Rect2 = main.get_viewport().get_visible_rect()
	var point: Vector2 = projected.clamp(
		visible_rect.position + Vector2.ONE,
		visible_rect.end - Vector2.ONE)
	var screen_radius: float = float(target.get(
		"screen_radius", InteractionDirector.SCREEN_HIT_RADIUS))
	var screen_distance: float = projected.distance_to(point)
	var picked: Dictionary = main._interaction_ref().call(
		"_pick", point) as Dictionary
	out["point"] = point
	out["projected"] = projected
	out["screen_radius"] = screen_radius
	out["screen_distance"] = screen_distance
	out["picked_id"] = String(picked.get("id", ""))
	out["exact"] = \
		String(target.get("id", "")) == target_id \
		and String(target.get("label", "")) == "Harper and Fiona" \
		and String(target.get("verb", "")) == "PLAY" \
		and bool(target.get("enabled", true)) \
		and visible_rect.has_point(point) \
		and screen_distance <= screen_radius \
		and String(picked.get("id", "")) == target_id \
		and main.touch_ui.world_controls_enabled \
		and main.game == ""
	return out


func _slide_voice_hybrid_diag(main: ReefMain, friend: Dictionary,
		screen_point: Vector2, audio: CountingAudioDirector,
		requests_before: int, accepted_before: int,
		voice_before: int) -> Dictionary:
	var fade_alpha := -1.0
	var fade_filter := -1
	if main.fade_rect != null:
		fade_alpha = main.fade_rect.modulate.a
		fade_filter = int(main.fade_rect.mouse_filter)
	var friend_node: Variant = friend.get("node")
	var player_distance := INF
	if friend_node != null and main.player != null:
		player_distance = main.player.position.distance_to(
			friend_node.global_position)
	var targets: Array[Dictionary] = []
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		targets.append({
			"id": String(item.get("id", "")),
			"verb": String(item.get("verb", "")),
			"enabled": bool(item.get("enabled", false)),
		})
	var request_tail: Array[Dictionary] = []
	for request_index in range(requests_before, audio.requests.size()):
		request_tail.append(audio.requests[request_index])
	var accepted_tail: Array[Dictionary] = []
	for accepted_index in range(accepted_before, audio.accepted.size()):
		accepted_tail.append(audio.accepted[accepted_index])
	return {
		"fade_alpha": fade_alpha,
		"fade_filter": fade_filter,
		"return_guard": bool(main.call(
			"_slide_canvas_return_guard_active")),
		"world_controls": main.touch_ui.world_controls_enabled,
		"touch_owners": main.touch_ui.touch_owners.duplicate(),
		"slide_held": main._slide_canvas_held_sources.duplicate(),
		"return_held": main._slide_canvas_return_held_sources.duplicate(),
		"melody_held": main._melody_held_sources.duplicate(),
		"friend_found": bool(friend.get("found", false)),
		"friend_cool": float(friend.get("cool", -1.0)),
		"player_distance": player_distance,
		"screen_point": screen_point,
		"targets": targets,
		"focus_id": main.touch_focus_id,
		"focus_ready": main.touch_focus_ready,
		"game": main.game,
		"mode": String(main.g.get("mode", "")),
		"requests_delta": audio.requests.size() - requests_before,
		"accepted_delta": audio.accepted.size() - accepted_before,
		"voice_delta": main.voice_i - voice_before,
		"request_tail": request_tail,
		"accepted_tail": accepted_tail,
	}


func _slide_voice_cues_live(slide: SlideRaceGame) -> bool:
	var surface: Node2D = slide.stage_root()
	if surface == null:
		return false
	var left := surface.get_node_or_null("PersistentLeftSteerCue") as Node2D
	var right := surface.get_node_or_null("PersistentRightSteerCue") as Node2D
	return left != null and right != null \
		and left.get_parent() == surface and right.get_parent() == surface \
		and left.visible and right.visible \
		and left.z_index == 30 and right.z_index == 30 \
		and is_equal_approx(float(left.get("cue_direction")), -1.0) \
		and is_equal_approx(float(right.get("cue_direction")), 1.0)


func _wait_wall_msec(duration_msec: int) -> void:
	var deadline_msec: int = Time.get_ticks_msec() + duration_msec
	while Time.get_ticks_msec() < deadline_msec:
		await process_frame


func _wait_slide_ready(main: ReefMain, slide: SlideRaceGame) -> void:
	for _index in range(180):
		var snapshot: Dictionary = slide.audit_snapshot()
		var fade_clear: bool = main.fade_rect == null or (
			main.fade_rect.modulate.a <= 0.02
			and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)
		if fade_clear and not bool(snapshot.get("blocked_until_release", true)) \
				and not bool(snapshot.get(
					"input_context_restore_guard", true)):
			return
		await process_frame


func _check_brawl_message_cues(main: ReefMain, audio: CountingAudioDirector) -> void:
	# Every child-visible brawl prompt owns its one intended Huluu cue. These
	# checks exercise the real entry, route, and imp-warning branches so an
	# adjacent _say cannot hide behind the cue cooldown again.
	main.clear_dialogue()
	main.said_cool.erase("huluu_greet")
	var before: int = main.voice_i
	var requests_before: int = audio.requests.size()
	main._start_game_now(main.brawl_fr)
	_check_named_cue(main, audio, "brawl entry", "huluu", "greet", before, requests_before)
	_check("brawl entry caption and state stay intact",
		main.game == "brawl" and int(main.g.get("seg", -1)) == 0
		and main.hud_msg.text == "Mischief imps are in Huluu's toy castle! Tap to POP them — Huluu helps!")

	var brawl: BrawlGame = main._game_obj("brawl", BrawlGame) as BrawlGame
	# Spawn the first real wave, leave one one-hit imp on Roshan's mark, then
	# land the actual clearing tap. The existing progression branch must open
	# the next route while speaking exactly once.
	brawl._tick_brawl(0.0, main.brawl_fr, main.player.position)
	var enemies: Array = main.g.get("enemies", []) as Array
	while enemies.size() > 1:
		brawl._damage_imp(enemies[0] as Dictionary, 99)
	var last_imp: Dictionary = enemies[0] as Dictionary
	var stage_root: Node3D = brawl.stage.root()
	(last_imp["node"] as Node3D).position = Vector3(0.0, 0.4, 0.0)
	last_imp["hp"] = 1
	main.player.position = stage_root.position + Vector3(0.0, 3.0, 0.0)
	main.g["ss_tap_prev"] = false
	main.touch_ui.action_down = false
	main.touch_ui.action_just = true
	main.clear_dialogue()
	main.said_cool.erase("huluu_talk")
	before = main.voice_i
	requests_before = audio.requests.size()
	brawl._tick_brawl(0.0, main.brawl_fr, main.player.position)
	_check_named_cue(main, audio, "brawl route", "huluu", "talk", before, requests_before)
	_check("brawl route caption and progression stay intact",
		int(main.g.get("seg", -1)) == 1
		and main.hud_msg.text == "This way! More imps ahead! ➜")

	# Feed the real warning dispatcher one deterministic telegraph event.
	main.clear_dialogue()
	main.said_cool.erase("huluu_talk")
	main.g["imp_warned"] = false
	var warning_brain := ImpAI.new()
	warning_brain.events.append({"kind": "telegraph", "pos": Vector2.ZERO})
	before = main.voice_i
	requests_before = audio.requests.size()
	brawl._brawl_brain_events(warning_brain, stage_root, Vector2.ZERO)
	_check_named_cue(main, audio, "brawl warning", "huluu", "talk", before, requests_before)
	_check("brawl warning caption and one-shot state stay intact",
		bool(main.g.get("imp_warned", false))
		and main.hud_msg.text == "Look out — that imp is winding up! POP it quick!")

	main.touch_ui.action_down = false
	main.touch_ui.action_just = false
	main.clear_dialogue()
	for active_tween: Tween in main.get_tree().get_processed_tweens():
		active_tween.kill()
	main._clear_game()
	await process_frame
	await process_frame


func _check_dialogue_speech_lifecycle(main: ReefMain) -> void:
	# Clearing dialogue is also the location-teardown contract. A new fallback
	# cue first replaces the exact line, then neither may leak into the next scene.
	main.clear_dialogue()
	main.said_cool.erase("roshan_talk")
	main._say("roshan", "talk")
	main._say("missing_speaker", "missing_event")
	_check("fallback speech replaces prior exact speech", _playing_pool_count(main) == 0)
	_check("fallback speech is active before clear", main.voice != null and main.voice.playing)
	main.clear_dialogue()
	_check("clear stops every pooled voice", _playing_pool_count(main) == 0)
	_check("clear stops fallback voice", main.voice != null and not main.voice.playing)

	# Rapid skips must stop the previous player before starting the next one.
	# Three different exact clips avoid cooldown interaction and let the probe
	# verify both the selected path and the one-cue-at-a-time invariant.
	for cue_key: String in ["roshan_talk", "roshan_intro1", "roshan_intro4"]:
		main.said_cool.erase(cue_key)
	var before: int = main.voice_i
	main.say_sequence([
		{"who": "Roshan", "text": "First", "vo": "talk", "hold": 9.0},
		{"who": "Roshan", "text": "Second", "vo": "intro1", "hold": 9.0},
		{"who": "Roshan", "text": "Third", "vo": "intro4", "hold": 9.0},
	])
	var first: AudioStreamPlayer = _last_pool_player(main)
	_check("sequence starts one cue", main.voice_i == before + 1 and _playing_pool_count(main) == 1)
	_check("sequence starts first exact clip", _stream_path(first) == "res://assets/audio/voices/filler_v1/roshan_talk.ogg")

	_check("first rapid skip is consumed", main.skip_dialogue())
	var second: AudioStreamPlayer = _last_pool_player(main)
	_check("first rapid skip stops prior cue", first != null and not first.playing)
	_check("first rapid skip starts only next cue",
		main.voice_i == before + 2 and _playing_pool_count(main) == 1
		and _stream_path(second) == "res://assets/audio/voices/filler_v1/roshan_intro1.ogg")

	_check("second rapid skip is consumed", main.skip_dialogue())
	var third: AudioStreamPlayer = _last_pool_player(main)
	_check("second rapid skip stops prior cue", second != null and not second.playing)
	_check("second rapid skip starts only next cue",
		main.voice_i == before + 3 and _playing_pool_count(main) == 1
		and _stream_path(third) == "res://assets/audio/voices/filler_v1/roshan_intro4.ogg")

	_check("final rapid skip is consumed", main.skip_dialogue())
	_check("sequence exhaustion stops final cue",
		third != null and not third.playing and _playing_pool_count(main) == 0)
	_check("sequence exhaustion clears dialogue state",
		not main.dialogue_active and main.dialogue_queue.is_empty())

	# The stop-before-advance change must not alter key-based cooldowns.
	main.said_cool.erase("roshan_talk")
	before = main.voice_i
	main._say("roshan", "talk", 10.0)
	main._say("roshan", "talk", 10.0)
	_check("voice cooldown still suppresses duplicate cue", main.voice_i == before + 1)
	main.clear_dialogue()


func _playing_pool_count(main: ReefMain) -> int:
	var count := 0
	for voice_player_value: Variant in main.voice_pool:
		var voice_player: AudioStreamPlayer = voice_player_value as AudioStreamPlayer
		if voice_player != null and voice_player.playing:
			count += 1
	return count


func _last_pool_player(main: ReefMain) -> AudioStreamPlayer:
	if main.voice_i <= 0 or main.voice_pool.is_empty():
		return null
	var index := posmod(main.voice_i - 1, main.voice_pool.size())
	return main.voice_pool[index] as AudioStreamPlayer


func _stream_path(player: AudioStreamPlayer) -> String:
	if player == null or player.stream == null:
		return "missing"
	return player.stream.resource_path


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _push_touch(main: ReefMain, position: Vector2, pressed: bool,
		index: int, device: int = 0) -> void:
	var event := InputEventScreenTouch.new()
	event.device = device
	event.index = index
	event.position = position
	event.pressed = pressed
	main.get_viewport().push_input(event, false)


func _check_named_cue(main: ReefMain, audio: CountingAudioDirector, label: String,
		speaker: String, event: String, before: int, requests_before: int) -> void:
	var actual_path: String = _stream_path(_last_pool_player(main))
	var expected_path := "res://assets/audio/voices/filler_v1/%s_%s.ogg" % [speaker, event]
	var request: Dictionary = audio.requests[-1] if not audio.requests.is_empty() else {}
	_check("%s makes one intended request" % label,
		audio.requests.size() == requests_before + 1
		and String(request.get("speaker", "")) == speaker
		and String(request.get("event", "")) == event
		and is_equal_approx(float(request.get("min_gap", -1.0)), 0.5),
		"requests=%d->%d cue=%s_%s" % [requests_before, audio.requests.size(),
			request.get("speaker", "missing"), request.get("event", "missing")])
	_check("%s plays one cue" % label, main.voice_i == before + 1,
		"voice_i=%d->%d" % [before, main.voice_i])
	_check("%s resolves exact clip" % label, actual_path == expected_path,
		"expected=%s actual=%s" % [expected_path, actual_path])


func _check_exact_cue(main: ReefMain, event: String, before: int) -> void:
	var actual_path := "missing"
	if main.voice_i > 0 and not main.voice_pool.is_empty():
		var index := posmod(main.voice_i - 1, main.voice_pool.size())
		var player := main.voice_pool[index] as AudioStreamPlayer
		if player != null and player.stream != null:
			actual_path = player.stream.resource_path
	var expected_path := "res://assets/audio/voices/filler_v1/roshan_%s.ogg" % event
	_check("%s cue speaks once" % event, main.voice_i == before + 1,
		"voice_i=%d->%d" % [before, main.voice_i])
	_check("%s cue resolves exact clip" % event, actual_path == expected_path,
		"expected=%s actual=%s" % [expected_path, actual_path])

func _check(label: String, ok: bool, detail: String = "") -> void:
	print("VOICE|%s: %s|%s" % [label, "OK" if ok else "FAIL", detail])
	if not ok:
		bad += 1
