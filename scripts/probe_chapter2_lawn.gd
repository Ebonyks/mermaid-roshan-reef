extends SceneTree

## Exercises the actual Canvas host through pointer edges and disk checkpoints.
## The full SaveState transactional recovery suite remains the disk owner gate.
class TestMain extends ReefMain:
	func _say(_speaker: String, _event: String = "", _gap: float = 0.0) -> void:
		pass

	func _write_save() -> bool:
		var file := FileAccess.open("user://chapter2_lawn_probe.json", FileAccess.WRITE)
		if file == null:
			return false
		var state := _chapter_two_ref().serialize_state()
		state["day_one_giant_dust_bunny_boss_defeated"] = true
		file.store_string(JSON.stringify(state))
		file.close()
		return true

var host: TestMain
var scene: ChapterTwoLawnFinale2D
var failures := 0

func _initialize() -> void:
	call_deferred("_run")

func _check(label: String, value: bool) -> void:
	print("CHAPTER2_LAWN|%s: %s" % [label, "OK" if value else "FAIL"])
	if not value:
		failures += 1

func _run() -> void:
	host = TestMain.new()
	host._chapter_two_director = ChapterTwoDirector.new(host)
	host.chapter2_active = true
	host.chapter2_party_piece_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
	host.chapter2_lawn_started = true
	host.chapter2_party_event_phase = ChapterTwoDirector.PARTY_EVENT_CANDLE_FOUND
	host.game = "chapter2_lawn"
	scene = ChapterTwoLawnFinale2D.new()
	root.add_child(scene)
	scene.setup(host, Callable())
	_check("birthday staging represents all eight earned castle jobs",
		(scene.get_meta("earned_party_pieces", []) as Array).size() == 8)
	for id: String in ["Cake", "Banner", "StuffieCat", "StuffieBunny", "MusicBox", "Rumi", "PartyMicrophone", "Rocket", "Candle"]:
		_check("earned handoff is physically visible: " + id, (scene.art[id] as Control).visible)
	_check("stuffies reuse the original protected ballet art",
		(scene.art["StuffieCat"] as TextureRect).texture.resource_path == "res://assets/book/doll_cat.png"
		and (scene.art["StuffieBunny"] as TextureRect).texture.resource_path == "res://assets/book/doll_bunny.png")
	_check("birthday lawn contains no playground equipment",
		scene.find_children("*Swing*", "", true, false).is_empty()
		and scene.find_children("*Slide*", "", true, false).is_empty()
		and scene.find_children("*Seesaw*", "", true, false).is_empty())
	await _capture("01-party")
	_tick(30.0)
	_check("idle lawn cannot light candle or start battle", not host.chapter2_party_started)
	_tap(ChapterTwoLawnFinale2D.ROCKET_RECT.get_center())
	_check("rocket fresh press lights the candle", host.chapter2_candle_lit and host.chapter2_lawn_beat == 1)
	_reload()
	_check("lighting checkpoint survives disk reload", host.chapter2_candle_lit and host.chapter2_lawn_beat == 1)
	for beat: int in range(3):
		_tick(3.0)
		_tap(ChapterTwoLawnFinale2D.CONTINUE_RECT.get_center())
	_check("introduction reaches playable battle", host.chapter2_lawn_beat == 4)
	await _capture("02-battle")
	_tick(60.0)
	_check("zero input cannot protect friends or lose progress", host.chapter2_protection_rounds == 0 and not host.chapter2_candle_taken)
	for round_index: int in range(3):
		var limit := 0
		while scene.battle.engine().state != BossEncounter2D.State.OPENING and limit < 2400:
			limit += 1
			var engine := scene.battle.engine()
			if engine.state == BossEncounter2D.State.TELL:
				var safe: Vector2 = engine.patterns.readout().get("safe_point", Vector2.ZERO)
				scene._destination(scene._screen(safe))
			scene.tick(1.0 / 60.0)
		_check("round %d has reachable safe lawn" % round_index, limit < 2400)
		if round_index == 0:
			scene._point_event(Vector2(500.0, 650.0), true, 77)
			scene.set_input_context(&"focus", true)
			scene.set_input_context(&"application", true)
			var elapsed: float = scene._state()["elapsed"]
			_tick(10.0)
			_check("background freezes encounter and clears held pointer",
				is_equal_approx(float(scene._state()["elapsed"]), elapsed)
				and int(scene._state()["pointer_id"]) == -1)
			scene.set_input_context(&"focus", false)
			_tap(ChapterTwoLawnFinale2D.KING_RECT.get_center())
			_check("focus alone cannot restore an application pause",
				host.chapter2_protection_rounds == 0 and scene._input_context_lost())
			scene.set_input_context(&"application", false)
			scene._point_event(ChapterTwoLawnFinale2D.KING_RECT.get_center(), false, 77)
			_check("late release after resume cannot award a counter",
				host.chapter2_protection_rounds == 0 and not scene._input_context_lost())
		_tap(Vector2(500.0, 650.0))
		_check("off-target press cannot award protection", host.chapter2_protection_rounds == round_index)
		_tap(ChapterTwoLawnFinale2D.KING_RECT.get_center())
		_check("fresh visible counter advances exactly one round", host.chapter2_protection_rounds == round_index + 1)
		_reload()
		_check("round checkpoint survives disk reload", host.chapter2_protection_rounds == round_index + 1)
	_check("three rounds preserve candle until story theft", host.chapter2_lawn_beat == 5 and not host.chapter2_candle_taken)
	_tick(2.0)
	_tap(ChapterTwoLawnFinale2D.CONTINUE_RECT.get_center())
	_check("King cheats only after protection success", host.chapter2_candle_taken and host.chapter2_lawn_beat == 6 and not host.chapter2_story_complete)
	_reload()
	_check("theft checkpoint does not skip reassurance", host.chapter2_lawn_beat == 6 and not host.chapter2_story_complete)
	for id: String in ["Cake", "Banner", "StuffieCat", "StuffieBunny", "MusicBox", "Rumi", "PartyMicrophone", "Rocket"]:
		_check("King leaves earned handoff intact: " + id, (scene.art[id] as Control).visible)
	_check("King takes only the local candle", not (scene.art["Candle"] as Control).visible)
	await _capture("03-theft")
	_tick(2.0)
	_tap(ChapterTwoLawnFinale2D.CONTINUE_RECT.get_center())
	_tick(2.0)
	_tap(ChapterTwoLawnFinale2D.CONTINUE_RECT.get_center())
	_reload()
	_check("reassurance completes story without losing party rewards", host.chapter2_lawn_beat == 8 and host.chapter2_story_complete and host.chapter2_party_piece_mask == ChapterTwoPartyPlan.ALL_PARTY_MASK)
	_check("royals leave together", not (scene.art["King"] as Control).visible and not (scene.art["Prince"] as Control).visible)
	scene.teardown()
	scene.free()
	host.free()
	print("CHAPTER2_LAWN|RESULT: %s checks_failed=%d" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(1 if failures > 0 else 0)

func _tick(seconds: float) -> void:
	for frame: int in range(int(seconds * 60.0)):
		scene.tick(1.0 / 60.0)

func _tap(point: Vector2) -> void:
	scene._point_event(point, true, 0)
	scene._point_event(point, false, 0)

func _reload() -> void:
	_check("checkpoint writes to disk", host._write_save())
	var state: Variant = JSON.parse_string(FileAccess.get_file_as_string("user://chapter2_lawn_probe.json"))
	scene.teardown()
	scene.free()
	host._chapter_two_ref().restore_state(state)
	scene = ChapterTwoLawnFinale2D.new()
	root.add_child(scene)
	scene.setup(host, Callable())
	_tick(0.5)

func _capture(label: String) -> void:
	if not "--lawn-capture" in OS.get_cmdline_user_args():
		return
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	var target := "res://.tmp/chapter2/" + label + ".png"
	var result := root.get_texture().get_image().save_png(target)
	_check("render capture " + label, result == OK)
