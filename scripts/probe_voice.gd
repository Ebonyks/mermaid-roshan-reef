extends SceneTree

var bad := 0

const MELODY_VOICE_PATH := \
	"res://assets/audio/voices/filler_v1/roshan_op_popstar_rhythm.ogg"
const MELODY_VOICE_SHA256 := \
	"e2d819527d370aff926302dbfecd6beb9e6c2165024d7abad131a28d90cac4ed"
const MELODY_OBJECTIVE := "Tap each rainbow note in the green!"
const YAY_PATH := "res://assets/audio/voices/filler_v1/yay.ogg"
const YAY_SHA256 := \
	"464867230434ae2d1473a3712ce2bad5ac07cdbf1b577fa3eb97a693a82f93b9"
const ROSHAN_TALK_PATH := "res://assets/audio/voices/filler_v1/roshan_talk.ogg"
const ROSHAN_TALK_SHA256 := \
	"1b347e1fee454c32b29796b658aa8aeb058a516157b3164cd53cc62f1015c1ee"


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
	# The carry and grotto routes retired with the 3D reef (2026-09-23); the
	# Critter Book is the remaining generic reaction route.
	var generic_route_sources := FileAccess.get_file_as_string(
		"res://scripts/collection_system.gd")
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
	_check("common Roshan reactions use distinct contextual cues",
		generic_route_sources.count('_say("roshan", "talk")') == 0
		and generic_route_sources.contains(
			'_say("roshan", "collection_book_open")'))
	var expected_events := [
		"talk", "whale", "ship", "wreck", "beans", "intro1", "intro4",
		"win", "pearl", "op_popstar_rhythm", "op_racer_tune_up",
		"op_racer_to_the_line", "castle_main_hall_enter",
		"bathroom_cleanup_start", "dungeon_room_enter",
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

	# Roshan's free-swim reef reactions (whale, ghost ship, wreck) retired with
	# the 3D reef on 2026-09-23 and are no longer exercised here. Keep their
	# neutral dialogue setup so the beans cue is not dropped behind a live line.
	main.game = ""
	main.intro_active = false
	main.clear_dialogue()

	# Avoid award_sticker's separate success cheer so this assertion isolates
	# the beans cue itself and proves _beans_go emits exactly one spoken line.
	main.stickers["beans"] = true
	main.said_cool.erase("roshan_beans")
	var before: int = main.voice_i
	main._beans_go()
	_check_exact_cue(main, "beans", before)

	var brawl_audio := CountingAudioDirector.new(main)
	main._audio_dir = brawl_audio
	await _check_melody_message_cue(main, brawl_audio)
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
