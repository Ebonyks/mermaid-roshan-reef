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

	print("VOICE|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit(1 if bad > 0 else 0)

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
