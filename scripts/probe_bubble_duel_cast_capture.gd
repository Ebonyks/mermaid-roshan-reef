extends "res://scripts/probe_bubble_duel_capture.gd"
const Cast := preload("res://scripts/bubble_duel_cast.gd")


func _run() -> void:
	if not await _setup_scene(): return
	await _capture("01-jobs", "Actual Jobs entry")
	Shop.reward(main, 20000)
	_tap(venue.bubble_duel_button)
	game = venue.bubble_duel
	if game == null:
		quit(3)
		return
	game.set_process(false)
	await _capture("02-hub", "Solo and two-friend entry")
	game._show_setup(false)
	await _capture("03-solo-setup", "Selected playable friend and computer friend")
	game._open_picker(0, "character")
	await _capture("04-six-friends", "The six existing playable characters")
	game._show_setup(true)
	await _capture("05-two-player-setup", "Independent character and loadout selection")
	var width := int(OS.get_environment("DUEL_CAPTURE_WIDTH"))
	if width == 1280 or width == 0:
		for person: String in Cast.PEOPLE:
			for item: Dictionary in Shop.ITEMS:
				for player: int in range(2):
					Shop.choose_character(main, person, player)
					Shop.choose_item(main, item["id"], player)
					Shop.choose_color(main, player, player)
				game._begin_versus()
				var prefix := "pair-" + person + "-" + String(item["id"])
				await _capture(prefix + "-rest", "Matching worn equipment on both real players; left and right facing")
				for player: int in range(2):
					_finger(player, game.Duo.PADS[player].get_center() + Vector2(30 if player == 0 else -30, 0), true)
				for frame: int in range(16): game._process(1.0 / 60.0)
				await _capture(prefix + "-moving", "Authored moving pose with source-bound wearable attachment on each player")
				for player: int in range(2): _finger(player, game.Duo.PADS[player].get_center(), false)
	else:
		Shop.choose_character(main, "roshan", 0)
		Shop.choose_character(main, "daddy_mermaid", 1)
		Shop.choose_item(main, "rainbow", 0)
		Shop.choose_item(main, "swiftconch", 1)
		game._begin_versus()
		await _capture("06-local-game", "Both actors and controls at supported viewport")
	# Real overlapping-player input case at every viewport. No teleported actors.
	for player: int in range(2):
		Shop.choose_character(main, "roshan", player)
		Shop.choose_item(main, "classic", player)
		Shop.choose_color(main, 0, player)
	game._begin_versus()
	for player: int in range(2): _finger(player, game.Duo.PADS[player].get_center() + Vector2(105, 0), true)
	for frame: int in range(82): game._process(1.0 / 60.0)
	var overlap_ready: bool = game.duo_touch_owners.size() == 2
	for player: int in range(2):
		var point: Vector2 = game.fighters[player]["position"]
		overlap_ready = overlap_ready and point.is_equal_approx(Vector2(1055, 270))
	if not overlap_ready:
		printerr("BUBBLECASTCAPTURE|FAIL|both native viewport touches must reach the shared wall/ceiling", game.fighters)
		quit(4)
		return
	await _capture("06-shared-ownership", "Both identical same-facing/same-colour players reach the same wall/ceiling via actual simultaneous touch; opposite-side one/two-dot markers remain visible")
	for player: int in range(2): _finger(player, game.Duo.PADS[player].get_center(), false)
	for player: int in range(2):
		game._show_setup(true)
		game._open_player_shop(player)
		await _capture("shop-player-" + str(player + 1), "Player-specific real shop and worn-equipment previews")
	game._show_setup(true)
	game._open_picker(0, "look")
	await _capture("unlocked-clothes", "Existing unlocked shared wardrobe and purchased sets")
	var file := FileAccess.open(output.path_join("captures.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(), "quality": main.quality,
		"fixture": "20000 isolated review pearls through Shop.reward; real closed purchase/selection methods and real viewport pad input. No production save used.",
		"captures": records, "acceptance": "Diagnostic appearance only; not formal QA11, device, child or owner acceptance."}, "  "))
	file.close()
	venue.close()
	main.queue_free()
	await process_frame
	print("BUBBLECASTCAPTURE|", records.size(), " frames")
	quit(0)


func _finger(index: int, point: Vector2, down: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index
	# Explicit viewport-local injection avoids applying screen stretch twice.
	event.position = game.get_global_transform_with_canvas() * point
	event.pressed = down
	root.push_input(event, true)
