extends "res://tools/capture_day2_job_contexts.gd"
## Additional diagnostic output states. Parent capture and its hashes stay intact.

func _run() -> void:
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, "res://tmp/day2_output_capture_save.json")
	root.add_child(main)
	await frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.set_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	for next_size: Vector2i in ASPECTS:
		root.size = next_size
		DisplayServer.window_set_size(next_size)
		aspect = "%dx%d" % [next_size.x, next_size.y]
		await frames(5)
		rooms.open("main_hall")
		main.clear_dialogue()
		if main.hud_msg != null:
			main.hud_msg.visible = false
		current_case = "output-party-table"
		var inspection_layer := CanvasLayer.new()
		inspection_layer.layer = 200
		root.add_child(inspection_layer)
		var table := ChapterTwoPartyTable2D.new()
		inspection_layer.add_child(table)
		table.setup(main)
		for step: int in range(8):
			current_phase = step
			main.chapter2_party_piece_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK if step == 7 else 0
			table.refresh()
			table.giant_cake.apply_milestone_masks(31 if step > 0 else 0,
				(1 << step) - 1)
			table.giant_cake.visible = table.giant_cake.has_visual_progress()
			table.party_candle.set_lit(step == 7)
			await shot("output-fixture")
		table.queue_free()
		inspection_layer.queue_free()
		await frames(3)
		rooms.close()
		current_case = "output-candle-closeup"
		var plate := ColorRect.new()
		plate.color = Color("#dcebe2")
		plate.size = Vector2(next_size)
		root.add_child(plate)
		var candle := ChapterTwoRainbowCandle2D.new()
		root.add_child(candle)
		candle.setup(false)
		candle.position = Vector2(490.0, 250.0)
		candle.scale = Vector2(2.0, 2.0)
		for step: int in range(2):
			current_phase = step
			candle.set_lit(step == 1)
			candle.set_process(false)
			await shot("output-fixture")
		candle.queue_free()
		plate.queue_free()
		await frames(3)
	var file := FileAccess.open(OUT + "output_capture_manifest.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"states": states, "engine": Engine.get_version_info(),
		"renderer": RenderingServer.get_current_rendering_method(),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_job_outputs.gd"),
		"parent_harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_job_contexts.gd"),
		"captured_at_utc": Time.get_datetime_string_from_system(true),
		"acceptance": "DIAGNOSTIC_ONLY",
		"limitations": "Direct persistent output fixtures on a declared inspection CanvasLayer above the room, and enlarged candle inspection; no real route/input/plot/child/owner acceptance."}, "\t"))
	file.close()
	main.queue_free()
	await frames(2)
	quit()
