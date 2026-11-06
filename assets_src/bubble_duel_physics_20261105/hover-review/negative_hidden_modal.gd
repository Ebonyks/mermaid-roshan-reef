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


func _setup_scene() -> bool:
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
		return false
	venue = routes.opera_venue
	root.mode = Window.MODE_WINDOWED
	var width := int(OS.get_environment("DUEL_CAPTURE_WIDTH"))
	root.size = Vector2i(width if width > 0 else 1280, 720)
	for i: int in range(8):
		await process_frame
	await create_timer(0.3).timeout
	return true


func _run() -> void:
	if not await _setup_scene(): return
	var portal: Button = venue.buttons[0]
	var hover_event := InputEventMouseMotion.new()
	hover_event.position = root.get_screen_transform() * (portal.get_screen_transform() * (portal.size * 0.5))
	root.push_input(hover_event, false)
	if root.gui_get_hovered_control() != portal:
		printerr("BUBBLECAPTURE|native portal hover fixture did not bind")
		quit(8)
		return
	await _capture("01-elevator", "Painted left elevator; detached launcher removed")
	Shop.reward(main, 20000)
	_tap(venue.bubble_duel_button)
	for frame: int in range(500):
		if venue.bubble_duel != null: break
		await process_frame
	game = venue.bubble_duel
	if game == null:
		quit(3)
		return
	# Negative fixture: deliberately expose underlying venue hover.
	game.hide()
	root.push_input(hover_event, false)
	var modal_hover: Control = root.gui_get_hovered_control()
	if modal_hover != null and modal_hover != game and not game.is_ancestor_of(modal_hover) \
			and modal_hover != main.global_navigation_button:
		printerr("BUBBLECAPTURE|inactive venue retained hover over arcade")
		quit(9)
		return
	print("BUBBLECAPTURE|native modal hover refreshed")
	game.set_process(false)
	await _capture("02-hub", "Actual elevator arcade hub")
	game._show_setup(true)
	await _capture("03-two-player", "Independent cast, clothing and items; versus or cooperative")
	game._open_picker(0, "character")
	await _capture("04-six-friends", "All six reusable identities")
	var width: int = int(OS.get_environment("DUEL_CAPTURE_WIDTH"))
	if width == 1280 or width == 0:
		for person: String in BubbleDuelCast.PEOPLE:
			for entry: Dictionary in Shop.ITEMS:
				for player: int in range(2):
					Shop.choose_character(main, person, player)
					Shop.choose_item(main, entry["id"], player)
				game._show_setup(true)
				await _capture("wear-" + person + "-" + String(entry["id"]), "Both facing directions; actual worn attachments and large setup previews")
		for index: int in range(4):
			var data: Dictionary = Shop.state(main)
			data["campaign"] = {"stage": index * 4, "checkpoint": {}}
			main.save_data[Shop.SAVE_KEY] = data
			Shop.choose_character(main, "roshan", 0)
			Shop.choose_character(main, "rumi", 1)
			Shop.choose_item(main, ["rainbow", "kelp", "lullaby", "squid"][index], 0)
			Shop.choose_item(main, "swiftconch", 1)
			game._begin_coop()
			var pilots: Array[BubbleDuelTestPolicy] = [BubbleDuelTestPolicy.new(91, 6), BubbleDuelTestPolicy.new(13, 8, false)]
			for tick: int in range(105):
				for player: int in range(2):
					var action: Dictionary = pilots[player].observe(game.world.human(player), game.world, tick)
					if tick == 0 or bool(action["flap"]):
						_tap(game, game.Duo.PADS[player].get_center() + Vector2(float(action["axis"]) * 60, 0))
					if bool(action["power"]): _tap(game.power_button if player == 0 else game.second_power_button)
				game._process(1.0 / 30)
			await _capture("arena-tier-" + str(index + 1), "Natural cooperative play: live opponents, source motion, visible tethers and control separation")
		game._begin(Duel.Mode.CURRENT)
		_tap(game, game.Duo.PADS[0].get_center())
		for tick: int in range(150): game._process(1.0 / 30)
		await _capture("05-current", "Real scrolling pearl and ink-current hazards")
	else:
		game._begin_coop()
		for player: int in range(2): _tap(game, game.Duo.PADS[player].get_center())
		for tick: int in range(40): game._process(1.0 / 30)
		await _capture("05-wide-arena", "Full arena at supported viewport, both independent pads")
	game._show_shop()
	await _capture("06-shop", "Shared owned items, pearl balance, purchase controls")
	game._turn_shop_page()
	await _capture("07-shop-second", "Remaining worn power items")
	if width == 1280 or width == 0: await _fit_key_tour()
	await _overlap_tour()
	var file: FileAccess = FileAccess.open(output.path_join("captures.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info(),
		"renderer": RenderingServer.get_current_rendering_method(), "quality": main.quality,
		"source_hashes": _capture_source_hashes(),
		"captures": records, "limits": "Native full-context candidate review. No physical device/child/owner or formal QA11 acceptance inferred."}, "\t") + "\n")
	file.close()
	await _motion_tour()
	_back()
	_back()
	var return_hover: Control = root.gui_get_hovered_control()
	if venue.bubble_duel != null or not venue.accepting_input or return_hover == game \
			or (return_hover != null and game.is_ancestor_of(return_hover)):
		printerr("BUBBLECAPTURE|native arcade return retained modal input or hover")
		quit(10)
		return
	print("BUBBLECAPTURE|native venue hover restored")
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
	if index == 0 and game.mode == Duel.Mode.SETUP:
		for child: Node in game.menu.get_children():
			if child is Button and child.tooltip_text == "Play":
				_tap(child as Control)
				break


func _back() -> void:
	_tap(main.global_navigation_button)


func _gear_card(id: String) -> Control:
	for child: Node in game.menu.get_children():
		if child is Control and child.get_meta("gear_id", "") == id:
			return child as Control
	return null




func _motion_tour() -> void:
	var folder: String = OS.get_environment("DUEL_MOTION_FRAMES")
	if folder.is_empty(): return
	DirAccess.make_dir_recursive_absolute(folder)
	var people: Array[Array] = [["roshan", "rumi"], ["daddy_mermaid", "baby_eagle"], ["rainbow_dust_bunny", "marlo"], ["roshan", "rumi"]]
	var gear: Array[Array] = [["classic", "classic"], ["swiftconch", "rainbow"], ["kelp", "lullaby"], ["squid", "moonpearl"]]
	var frames: Array[Dictionary] = []
	for scene: int in range(4):
		for player: int in range(2):
			Shop.choose_character(main, people[scene][player], player)
			Shop.choose_item(main, gear[scene][player], player)
		if scene == 3: game._begin_coop()
		else: game._begin_versus()
		var policies: Array[BubbleDuelTestPolicy] = [BubbleDuelTestPolicy.new(57 + scene, 6), BubbleDuelTestPolicy.new(79 + scene, 8, false)]
		for tick: int in range(120):
			for player: int in range(2):
				var fighter: BubbleDuelFighter = game.world.human(player)
				var action: Dictionary = policies[player].observe(fighter, game.world, tick)
				if (tick == 0 or bool(action["flap"])) and not (fighter.gear == "moonpearl" and tick >= 90 and tick < 116):
					_tap(game, game.Duo.PADS[player].get_center() + Vector2(float(action["axis"]) * 60, 0))
				if bool(action["power"]) and fighter.gear != "moonpearl":
					_tap(game.power_button if player == 0 else game.second_power_button)
				if fighter.gear == "moonpearl" and tick in [90, 116]:
					var control: Control = game.power_button if player == 0 else game.second_power_button
					var event := InputEventScreenTouch.new()
					event.index = 301
					event.pressed = tick == 90
					event.position = root.get_screen_transform() * (control.get_screen_transform() * (control.size * 0.5))
					root.push_input(event, false)
			game._process(1.0 / 30)
			await RenderingServer.frame_post_draw
			var picture: Image = root.get_texture().get_image()
			var name: String = "frame-%04d.jpg" % (scene * 120 + tick)
			picture.save_jpg(folder.path_join(name), 0.93)
			frames.append({"file": name, "scene": scene, "tick": tick, "sha256": FileAccess.get_sha256(folder.path_join(name))})
	var file: FileAccess = FileAccess.open(output.path_join("motion-frames.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"fps": 30, "frames": frames,
		"scope": "GAMEPLAY_REVIEW_ONLY; deterministic30Hz input-driven action at source cadence, all6 cast and powered attachments, JPEG review frames only; no cinematic or device acceptance."}, "\t") + "\n")
	file.close()


func _capture_source_hashes() -> Dictionary:
	var result: Dictionary = {}
	for path: String in ["opera_bubble_duel.gd", "bubble_duel_motion.gd", "bubble_duel_fighter.gd", "bubble_duel_arena.gd", "bubble_duel_brain.gd", "bubble_duel_two_player.gd", "bubble_duel_geometry.gd", "bubble_duel_view.gd", "bubble_duel_inventory.gd", "bubble_duel_cast.gd", "opera_house_venue_2d.gd", "probe_bubble_duel_capture.gd"]:
		result[path] = FileAccess.get_sha256("res://scripts/" + path)
	return result


func _overlap_tour() -> void:
	for player: int in range(2):
		Shop.choose_character(main, "roshan", player)
		Shop.choose_item(main, "classic", player)
		Shop.choose_color(main, 0, player)
	game._begin_versus()
	var captured: bool = false
	var turned: bool = false
	for tick: int in range(50):
		if tick in [0, 8]:
			for player: int in range(2):
				_tap(game, game.Duo.PADS[player].get_center() + Vector2(60 if player == 0 else -60, 0))
		if not turned and tick > 8 and absf(BubbleDuelMotion.wrapped_dx(game.world.human(0).position.x - game.world.human(1).position.x)) < 55:
			_tap(game, game.Duo.PADS[1].get_center() + Vector2(60, 0))
			turned = true
		game._process(1.0 / 30)
		var first: BubbleDuelFighter = game.world.human(0)
		var second: BubbleDuelFighter = game.world.human(1)
		if first.facing > 0 and second.facing > 0 and absf(BubbleDuelMotion.wrapped_dx(first.position.x - second.position.x)) < 24 and absf(first.position.y - second.position.y) < 15:
			await _capture("08-identical-overlap", "Identical same-facing and same-colour actors approach through actual flap inputs; fixed opposite-side1/2-dot human markers stay separate")
			captured = true
			break
	if not captured:
		printerr("BUBBLECAPTURE|FAIL|natural identical-player overlap fixture did not occur")
		quit(7)


func _fit_key_tour() -> void:
	var cases: Array[Array] = [["rumi", "kelp"], ["marlo", "rainbow"], ["marlo", "swiftconch"], ["baby_eagle", "squid"], ["rainbow_dust_bunny", "squid"]]
	for spec: Array in cases:
		for player: int in range(2):
			Shop.choose_character(main, String(spec[0]), player)
			Shop.choose_item(main, String(spec[1]), player)
		var keys: int = 4 if String(spec[0]) in ["rumi", "marlo"] else 1
		var fps: float = 6.0 if String(spec[0]) == "rumi" else 5.0
		for key: int in range(keys):
			game._show_setup(true)
			for child: Node in game.menu.find_children("*", "Control", true, false):
				if child.get_script() == load("res://scripts/bubble_duel_preview.gd"):
					child.set_process(false)
					child.set("moving", true)
					child.set("clock", (float(key) + 0.25) / fps)
			await _capture("fit-" + String(spec[0]) + "-" + String(spec[1]) + "-key-" + str(key),
				"Native source-key wardrobe review after socket repair; both directions, frozen authored source pose, not a completed gameplay bout")
