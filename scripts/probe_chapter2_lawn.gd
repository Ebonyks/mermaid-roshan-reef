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
	_check_scale_and_contacts()
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
	var initial_position := (scene.art["Roshan"] as Control).position
	scene.tick(4.0)
	_check("rocket tap requests bounded travel without remote progress",
		not host.chapter2_candle_lit and host.chapter2_lawn_beat == 0
		and (scene.art["Roshan"] as Control).position.distance_to(initial_position) <= 5.0)
	var canceled_touch := InputEventScreenTouch.new()
	canceled_touch.canceled = true
	canceled_touch.index = 1
	scene._gui_input(canceled_touch)
	_check("another finger cannot cancel the requested ignition",
		String(scene._state()["mode"]) == "ignition_walk")
	canceled_touch.index = 0
	scene._gui_input(canceled_touch)
	_tick(4.0)
	_check("canceled source touch cannot complete ignition later",
		not host.chapter2_candle_lit and String(scene._state()["mode"]) == "story")
	_tap(ChapterTwoLawnFinale2D.ROCKET_RECT.get_center())
	_reload()
	_tick(4.0)
	_check("teardown and reload discard unfinished ignition", not host.chapter2_candle_lit)
	_tap(ChapterTwoLawnFinale2D.ROCKET_RECT.get_center())
	_tick(0.4)
	await _capture("04-ignition-approach")
	scene.set_input_context(&"focus", true)
	scene.set_input_context(&"focus", false)
	_tick(4.0)
	_check("interrupted approach cannot finish after resume",
		not host.chapter2_candle_lit and String(scene._state()["mode"]) == "story")
	_tap(ChapterTwoLawnFinale2D.ROCKET_RECT.get_center())
	var approach_limit := 0
	while String(scene._state()["mode"]) == "ignition_walk" and approach_limit < 300:
		scene.tick(1.0 / 60.0)
		approach_limit += 1
	_check("Roshan reaches the actual rocket before its action",
		approach_limit < 300 and not host.chapter2_candle_lit
		and (scene.art["Roshan"] as Control).position.distance_to(ChapterTwoLawnFinale2D.IGNITION_REACH_POSITION) < 0.1)
	_tick(0.9)
	_check("authored hand reach contacts the ignition before progress",
		bool(scene.get_meta("ignition_hand_contact", false)) and not host.chapter2_candle_lit)
	await _capture("05-ignition-contact")
	scene.set_input_context(&"application", true)
	scene.set_input_context(&"application", false)
	_tick(4.0)
	_check("interrupted contact cannot light the candle later", not host.chapter2_candle_lit)
	_tap(ChapterTwoLawnFinale2D.ROCKET_RECT.get_center())
	_tick(5.0)
	_check("fresh complete travel and ignition light the candle once",
		host.chapter2_candle_lit and host.chapter2_lawn_beat == 1
		and String(scene._state()["mode"]) == "story")
	_reload()
	_check("lighting checkpoint survives disk reload", host.chapter2_candle_lit and host.chapter2_lawn_beat == 1)
	await _capture("09-lit")
	for beat: int in range(3):
		_tick(3.0)
		_tap(ChapterTwoLawnFinale2D.CONTINUE_RECT.get_center())
		if host.chapter2_lawn_beat in [2, 3]:
			await _capture("10-arrival" if host.chapter2_lawn_beat == 2 else "11-demand")
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
	await _capture("12-friends-safe")
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
	await _capture("13-departure")
	_tick(2.0)
	_tap(ChapterTwoLawnFinale2D.CONTINUE_RECT.get_center())
	_reload()
	_check("reassurance completes story without losing party rewards", host.chapter2_lawn_beat == 8 and host.chapter2_story_complete and host.chapter2_party_piece_mask == ChapterTwoPartyPlan.ALL_PARTY_MASK)
	_check("royals leave together", not (scene.art["King"] as Control).visible and not (scene.art["Prince"] as Control).visible)
	await _capture("14-hope")
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

func _visible_bounds(id: String) -> Rect2:
	var actor := scene.art[id] as TextureRect
	var texture_size := actor.texture.get_size()
	var factor := minf(actor.size.x / texture_size.x, actor.size.y / texture_size.y)
	var padding := (actor.size - texture_size * factor) * 0.5
	var pixels := actor.texture.get_image()
	if pixels.is_compressed():
		pixels.decompress()
	# Ignore near-transparent block-compression noise when measuring identity.
	var low := Vector2(pixels.get_width(), pixels.get_height())
	var high := Vector2.ZERO
	for y: int in range(pixels.get_height()):
		for x: int in range(pixels.get_width()):
			if pixels.get_pixel(x, y).a > 0.125:
				low = low.min(Vector2(x, y))
				high = high.max(Vector2(x + 1, y + 1))
	var used := Rect2(low, high - low)
	return Rect2(actor.position + padding + used.position * factor, used.size * factor)

func _check_scale_and_contacts() -> void:
	var king := _visible_bounds("King")
	var prince := _visible_bounds("Prince")
	var roshan := _visible_bounds("Roshan")
	print("LAWN_SCALE|king=", king, " prince=", prince, " roshan=", roshan)
	_check("visible Prince height preserves approved four-fifths King ratio",
		absf(prince.size.y / king.size.y - 0.8) < 0.003)
	_check("King reads larger without dwarfing Roshan",
		king.size.y / roshan.size.y > 1.30 and king.size.y / roshan.size.y < 1.36)
	_check("story cast shares a ground plane despite different texture padding",
		absf(king.end.y - prince.end.y) < 2.0 and absf(king.end.y - roshan.end.y) < 2.0)
	var rocket := scene.art["Rocket"] as TextureRect
	var button := rocket.position + (rocket.size - Vector2.ONE * 140.0) * 0.5 + Vector2(256, 168) * (140.0 / 512.0)
	_check("ignition targets the source-art brass button above the porthole",
		button.distance_to(ChapterTwoLawnFinale2D.IGNITION_POINT) < 0.1)
	_check("authored final fingertip lands on the brass button",
		(ChapterTwoLawnFinale2D.IGNITION_REACH_POSITION + Vector2(16, 77)).distance_to(button) < 1.0)
	_check("warning origin agrees with the King's grounded position",
		scene._screen(ChapterTwoLawnFinale2D.BOSS_POINT).distance_to(Vector2(king.get_center().x, king.end.y)) < 2.0)
	_check("lit and stolen candle use identical display size",
		(scene.art["Candle"] as Control).size == (scene.art["CarriedCandle"] as Control).size)
