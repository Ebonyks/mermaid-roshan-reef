extends RefCounted
## Called by the trusted Opera2D suite and the focused Tree Book probe.
var failures := 0
func check(label: String, ok: bool) -> void:
	print("TREE_BOOK|%s: %s" % [label, "OK" if ok else "FAIL"])
	if not ok:
		failures += 1

func touch(level: OperaTreeBookTest, id: int, down: bool, point: Vector2,
		canceled: bool = false) -> void:
	var event := InputEventScreenTouch.new()
	event.index = id
	event.pressed = down
	event.position = point
	event.canceled = canceled
	level._gui_input(event)

func tap(level: OperaTreeBookTest, point: Vector2) -> void:
	touch(level, 1, true, point)
	touch(level, 1, false, point)

func run(host: Node, main: ReefMain = null) -> bool:
	var level := OperaTreeBookTest.new()
	host.add_child(level)
	level.set_process(false)
	for cue: String in OperaTreeBookTest.CUES + ["try_tree", "try_spots"]:
		var path := "res://assets/audio/arborist_tree_book/roshan_arborist_tree_book_" + cue + ".ogg"
		check("exact cue available " + cue, ResourceLoader.exists(path))
	for step: int in range(3):
		check("four distinct choices at step %d" % step,
			OperaTreeBookTest.ORDERS[step].size() == 4
			and OperaTreeBookTest.ORDERS[step].count(OperaTreeBookTest.ANSWERS[step]) == 1)
		level.advance(5.1)
		check("5-second glow, no passive win %d" % step, level.help_level == 1 and level.stage == step)
		level.advance(5.1)
		check("10-second hand, no passive win %d" % step, level.help_level == 2 and level.stage == step)
		var correct := level.choice_rect(level.answer_slot()).get_center()
		touch(level, 1, true, correct)
		touch(level, 2, true, correct)
		touch(level, 2, false, correct)
		check("second finger cannot answer %d" % step, level.stage == step)
		touch(level, 1, false, correct, true)
		check("canceled touch cannot answer %d" % step, level.stage == step)
		var wrong := level.choice_rect((level.answer_slot()+1)%4).get_center()
		tap(level, wrong)
		check("wrong answer preserves earned work %d" % step, level.stage == step and level.wrong_time > 0)
		touch(level, 1, true, correct)
		level._notification(Control.NOTIFICATION_APPLICATION_FOCUS_OUT)
		level._notification(Control.NOTIFICATION_APPLICATION_FOCUS_IN)
		touch(level, 1, false, correct)
		check("focus loss drops old touch %d" % step, level.stage == step)
		tap(level, correct)
		check("intentional answer advances exactly once %d" % step, level.stage == step+1)
		var saved: Variant = JSON.parse_string(JSON.stringify(level.progress_snapshot()))
		level.restore_progress(saved)
		check("JSON round trip retains step %d" % step, level.stage == step+1)
	level.advance(2.0)
	check("carry arrives without healing", level.stage == 4 and level.treatment == 0.0)
	level.advance(60.0)
	check("treatment also requires input", level.stage == 4 and level.treatment == 0.0)
	touch(level,1,true,OperaTreeBookTest.LEAF_RECT.get_center())
	for tick: int in range(4):
		level.advance(0.1)
	var partial := level.treatment
	level._notification(Control.NOTIFICATION_PAUSED)
	level.advance(1.0)
	level._notification(Control.NOTIFICATION_APPLICATION_FOCUS_OUT)
	level._notification(Control.NOTIFICATION_UNPAUSED)
	check("nested focus loss remains suspended", level.suspended)
	level._notification(Control.NOTIFICATION_APPLICATION_FOCUS_IN)
	level.advance(1.0)
	check("pause cancels held spray", level.stage == 4 and is_equal_approx(partial, level.treatment))
	var resume := level.progress_snapshot()
	level.restore_progress(resume)
	check("partial medicine survives resume", is_equal_approx(level.treatment,partial))
	touch(level,1,true,OperaTreeBookTest.LEAF_RECT.get_center())
	for tick: int in range(12):
		level.advance(0.1)
	check("deliberate medicine heals same patient", level.stage == 5 and level.treatment == 1.0)
	var completed := level.progress_snapshot()
	level.restore_progress(completed)
	check("completed sticker survives resume",level.stage == 5)
	tap(level,OperaTreeBookTest.REPLAY_RECT.get_center())
	check("replay starts a fresh optional practice",level.stage == 0)
	for bad: Variant in [null, [], {"version":1,"patient":"orange_spots","stage":2.5},
			{"version":1,"patient":"wrong","stage":5},{"version":1,"patient":"orange_spots","stage":99}]:
		level.restore_progress(bad)
		check("malformed checkpoint defaults safely",level.stage == 0)
	level.shutdown()
	level.advance(60)
	check("closed activity has no pending action",level.stage == 0 and level.pointer_id == -99)
	level.queue_free()
	await host.get_tree().process_frame
	if main != null:
		var stars := main.opera_stars
		var previous: Variant = main.save_data.get(OperaTreeBookTest.SAVE_KEY)
		main._castle_rooms_ref().open("opera_hall")
		main._castle_rooms_ref().show_room("opera_hall", false)
		var routes: CastleCareerRoutes = main._castle_career_routes_ref()
		routes.sync()
		routes.open_opera_venue()
		var venue: OperaHouseVenue2D = routes.opera_venue
		venue.open(stars)
		venue.practice_book.pressed.emit()
		check("painted Opera House book opens level", venue.tree_book_test != null and not venue.accepting_input
			and main.touch_control_blocks.has("tree_book_practice"))
		var practice: OperaTreeBookTest = venue.tree_book_test
		host.get_tree().root.size = Vector2i(1280,720)
		host.get_tree().root.content_scale_size = Vector2i(1280,720)
		await host.get_tree().process_frame
		var screen_point := practice.get_global_transform_with_canvas() * practice.choice_rect(practice.answer_slot()).get_center()
		for down: bool in [true,false]:
			var physical := InputEventScreenTouch.new()
			physical.index = 4
			physical.pressed = down
			physical.position = screen_point
			host.get_viewport().push_input(physical, true)
			await host.get_tree().process_frame
		check("real viewport touch reaches book without world controls",practice.stage == 1)

		venue._close_tree_book()
		check("exit restores foyer and preserves stars",venue.tree_book_test == null and venue.accepting_input and main.opera_stars == stars
			and not main.touch_control_blocks.has("tree_book_practice"))
		var on_disk: Variant = JSON.parse_string(FileAccess.get_file_as_string(main.SAVE_PATH))
		check("exit writes checkpoint to the actual save file", on_disk is Dictionary
			and on_disk.get(OperaTreeBookTest.SAVE_KEY, {}).get("stage") == 1)
		venue.practice_book.pressed.emit()
		check("reentry uses saved step",venue.tree_book_test.stage == 1)
		venue.close()
		check("venue close tears down child activity",venue.tree_book_test == null and not venue.visible)
		routes.open_opera_venue()
		venue.open_tree_book()
		routes.clear()
		check("room route teardown releases practice input and navigation",
			not main.touch_control_blocks.has("tree_book_practice")
			and main._navigation_ref().top_id() != "arborist_tree_book_test")
		main._castle_rooms_ref().close()
		await host.get_tree().process_frame
		if previous == null:
			main.save_data.erase(OperaTreeBookTest.SAVE_KEY)
		else:
			main.save_data[OperaTreeBookTest.SAVE_KEY] = previous
	return failures == 0
