extends SceneTree

var bad := 0

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	main._skip_intro()
	await process_frame
	var expected_events := [
		"talk", "whale", "ship", "wreck", "beans", "intro1", "intro4",
		"win", "pearl",
	]
	var present := 0
	for ln: String in expected_events:
		if ResourceLoader.exists("res://assets/audio/voices/roshan_%s.ogg" % ln):
			present += 1
	_check("expected Roshan clips present", present == expected_events.size(),
		"%d / %d" % [present, expected_events.size()])

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

	whale.position = Vector3(10.0, 0.0, 10.0)
	ship.position = Vector3(1000.0, 0.0, 1000.0)
	main.wreck_pos = Vector3(2000.0, 0.0, 2000.0)
	main.roshan_spot_cool = 0.0
	main.said_cool.erase("roshan_whale")
	var before := main.voice_i
	main._tick_roshan_reactions(0.0, whale.position)
	_check_exact_cue(main, "whale", before)

	whale.position = Vector3(1000.0, 0.0, 1000.0)
	ship.position = Vector3(20.0, 0.0, 20.0)
	main.roshan_spot_cool = 0.0
	main.said_cool.erase("roshan_ship")
	before = main.voice_i
	main._tick_roshan_reactions(0.0, ship.position)
	_check_exact_cue(main, "ship", before)

	ship.position = Vector3(1000.0, 0.0, 1000.0)
	main.wreck_pos = Vector3(30.0, 0.0, 30.0)
	main.roshan_spot_cool = 0.0
	main.said_cool.erase("roshan_wreck")
	before = main.voice_i
	main._tick_roshan_reactions(0.0, main.wreck_pos)
	_check_exact_cue(main, "wreck", before)

	# Avoid award_sticker's separate success cheer so this assertion isolates
	# the beans cue itself and proves _beans_go emits exactly one spoken line.
	main.stickers["beans"] = true
	main.said_cool.erase("roshan_beans")
	before = main.voice_i
	main._beans_go()
	_check_exact_cue(main, "beans", before)

	_check_dialogue_speech_lifecycle(main)

	print("VOICE|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit(1 if bad > 0 else 0)


func _check_dialogue_speech_lifecycle(main: ReefMain) -> void:
	# Clearing dialogue is also the location-teardown contract: neither an
	# exact pooled line nor the fallback cheer may leak into the next scene.
	main.clear_dialogue()
	main.said_cool.erase("roshan_talk")
	main._say("roshan", "talk")
	main._say("missing_speaker", "missing_event")
	_check("exact speech is active before clear", _playing_pool_count(main) == 1)
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
	_check("sequence starts first exact clip", _stream_path(first) == "res://assets/audio/voices/roshan_talk.ogg")

	_check("first rapid skip is consumed", main.skip_dialogue())
	var second: AudioStreamPlayer = _last_pool_player(main)
	_check("first rapid skip stops prior cue", first != null and not first.playing)
	_check("first rapid skip starts only next cue",
		main.voice_i == before + 2 and _playing_pool_count(main) == 1
		and _stream_path(second) == "res://assets/audio/voices/roshan_intro1.ogg")

	_check("second rapid skip is consumed", main.skip_dialogue())
	var third: AudioStreamPlayer = _last_pool_player(main)
	_check("second rapid skip stops prior cue", second != null and not second.playing)
	_check("second rapid skip starts only next cue",
		main.voice_i == before + 3 and _playing_pool_count(main) == 1
		and _stream_path(third) == "res://assets/audio/voices/roshan_intro4.ogg")

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


func _check_exact_cue(main: ReefMain, event: String, before: int) -> void:
	var actual_path := "missing"
	if main.voice_i > 0 and not main.voice_pool.is_empty():
		var index := posmod(main.voice_i - 1, main.voice_pool.size())
		var player := main.voice_pool[index] as AudioStreamPlayer
		if player != null and player.stream != null:
			actual_path = player.stream.resource_path
	var expected_path := "res://assets/audio/voices/roshan_%s.ogg" % event
	_check("%s cue speaks once" % event, main.voice_i == before + 1,
		"voice_i=%d->%d" % [before, main.voice_i])
	_check("%s cue resolves exact clip" % event, actual_path == expected_path,
		"expected=%s actual=%s" % [expected_path, actual_path])

func _check(label: String, ok: bool, detail: String = "") -> void:
	print("VOICE|%s: %s|%s" % [label, "OK" if ok else "FAIL", detail])
	if not ok:
		bad += 1
