extends SceneTree
const Duel := preload("res://scripts/opera_bubble_duel.gd")
const Shop := preload("res://scripts/bubble_duel_inventory.gd")
var main: ReefMain
var venue: OperaHouseVenue2D
var game: Control
var output := OS.get_environment("DUEL_CAPTURE_DIR")
var records: Array[Dictionary] = []


func _initialize() -> void:
	var fixture := OS.get_environment("DUEL_CAPTURE_SAVE_ROOT").replace("\\", "/").simplify_path()
	var data_path := OS.get_user_data_dir().replace("\\", "/").simplify_path()
	if output.is_empty() or fixture.is_empty() or not data_path.begins_with(fixture.trim_suffix("/") + "/"):
		printerr("BUBBLECAPTURE|explicit isolated save directory and output required")
		quit(2)
		return
	call_deferred("_run")


func _run() -> void:
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	Engine.time_scale = 8.0
	await process_frame
	await process_frame
	main._start_menu_ref()._dismiss_menu()
	main.day_one_active = false
	main._skip_intro()
	main.quality = "speedy"
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	for i: int in range(20):
		await process_frame
	main._apply_quality("speedy")
	main._castle_rooms_ref().show_room("opera_hall", false)
	for i: int in range(5):
		await process_frame
	var routes := main._castle_career_routes_ref()
	if not routes.open_opera_venue():
		quit(2)
		return
	venue = routes.opera_venue
	root.mode = Window.MODE_WINDOWED
	var width := int(OS.get_environment("DUEL_CAPTURE_WIDTH"))
	root.size = Vector2i(width if width > 0 else 1280, 720)
	for i: int in range(8):
		await process_frame
	await _capture("01-jobs", "Illustrated shop launcher in Jobs")
	# An explicit review fixture supplies pearls. Every acquisition below still
	# calls the actual purchase button and the shared save transaction.
	Shop.reward(main, 2000)
	_tap(venue.bubble_duel_button)
	game = venue.bubble_duel
	if game == null:
		quit(3)
		return
	game.set_process(false)
	await _capture("02-hub", "Rebuilt hub")
	if width != 1280:
		_card(0)
		await _capture("03-wide-duel", "Supported viewport, complete room and actors")
		_back()
		_card(3)
		await _capture("04-wide-shop", "Supported viewport shop")
	else:
		_card(3)
		await _capture("03-shop-page-1", "Purchase prices, color ownership and first four outfits")
		for item: Dictionary in Shop.ITEMS:
			var page: int = Shop.ITEMS.find(item) / 4
			if game.shop_page != page:
				game._turn_shop_page()
			var button := _gear_card(item["id"])
			if button == null:
				quit(4)
				return
			_tap(button)
			if game.gear != item["id"]:
				quit(5)
				return
			if item["id"] == "rainbow":
				await _capture("04-shop-page-2", "Second four outfits")
			_back()
			_card(0)
			await _capture("outfit-" + item["id"] + "-rest", "Purchased outfit on Roshan at rest")
			_tap(game, game._target(0))
			for i: int in range(20):
				game._process(1.0 / 60.0)
			await _capture("outfit-" + item["id"] + "-swim", "Same purchased outfit during an anchored swim")
			if item["id"] not in ["classic", "tidewing"]:
				_tap(game.power_button)
				for i: int in range(8):
					game._process(1.0 / 60.0)
				await _capture("power-" + item["id"], "Player-activated power during the bout")
			_back()
			_card(3)
		for color_index: int in range(5):
			_card(color_index)
			_back()
			_card(0)
			await _capture("bubble-color-" + str(color_index), "Purchased bubble color against the actual arena")
			_back()
			_card(3)
		_back()
		_card(1)
		await _capture("05-practice", "Practice target and pearl payoff")
		_hit(1)
		await _capture("06-practice-pop", "Pop and earned pearl")
		_back()
		_card(2)
		await _capture("07-current", "Current Ride collectible")
		_hit(1)
		await _capture("08-collected", "Collected pearl disappears before respawn")
		_back()
		_card(0)
		_hit(1)
		await _capture("09-first-contact", "Burst and correct surviving bubble")
		_hit(2)
		await _capture("10-replay", "Earned pearls and replay control")
	var file := FileAccess.open(output.path_join("captures.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(), "quality": main.quality,
		"fixture": "2000 review pearls credited through Shop.reward, followed by real purchase controls",
		"captures": records}, "  "))
	file.close()
	venue.close()
	main.queue_free()
	await process_frame
	print("BUBBLECAPTURE|", records.size(), " captures")
	quit(0)


func _capture(key: String, role: String) -> void:
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var path := output.path_join(key + ".png")
	if image.is_empty() or image.save_png(path) != OK:
		printerr("BUBBLECAPTURE|invalid image ", key)
		quit(6)
		return
	records.append({"file": key + ".png", "role": role, "w": image.get_width(),
		"h": image.get_height(), "sha256": FileAccess.get_sha256(path)})


func _tap(control: Control, at: Vector2 = Vector2(-1, -1)) -> void:
	var point := control.size * 0.5 if at.x < 0 else at
	var screen := root.get_screen_transform() * (control.get_screen_transform() * point)
	for down: bool in [true, false]:
		var event := InputEventScreenTouch.new()
		event.index = 1
		event.pressed = down
		event.position = screen
		root.push_input(event, false)


func _card(index: int) -> void:
	_tap(game.menu.get_child(index) as Control)


func _back() -> void:
	_tap(main.global_navigation_button)


func _gear_card(id: String) -> Control:
	for child: Node in game.menu.get_children():
		if child is Control and child.get_meta("gear_id", "") == id:
			return child as Control
	return null


func _hit(expected: int) -> void:
	for attempt: int in range(5):
		_tap(game, game._target(0))
		for i: int in range(240):
			game._process(1.0 / 60.0)
			if game.score == expected:
				return
		printerr("BUBBLECAPTURE|retry contact")
	printerr("BUBBLECAPTURE|contact failed")
	quit(7)

