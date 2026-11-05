extends SceneTree

const Duel := preload("res://scripts/opera_bubble_duel.gd")
const Shop := preload("res://scripts/bubble_duel_inventory.gd")
var main: ReefMain
var venue: OperaHouseVenue2D
var bad := 0
var rows: Array[Dictionary] = []
var checked := 0


func _initialize() -> void:
	var fixture := OS.get_environment("BUBBLE_DUEL_STRESS_ROOT").replace("\\", "/").simplify_path()
	var data_path := OS.get_user_data_dir().replace("\\", "/").simplify_path()
	if fixture.is_empty() or not data_path.begins_with(fixture.trim_suffix("/") + "/"):
		printerr("BUBBLESTRESS|isolated test directory required")
		quit(2)
		return
	call_deferred("_run")


func _run() -> void:
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	Engine.time_scale = 8.0
	await process_frame
	await process_frame
	if OS.get_environment("BUBBLE_DUEL_VERIFY_RELOAD") == "1":
		_verify_reload()
		return
	main._start_menu_ref()._dismiss_menu()
	main.day_one_active = false
	main._skip_intro()
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	for i: int in range(12):
		await process_frame
	main._castle_rooms_ref().show_room("opera_hall", false)
	for i: int in range(3):
		await process_frame
	var routes := main._castle_career_routes_ref()
	_check("Opera venue opens", routes.open_opera_venue())
	venue = routes.opera_venue
	if venue == null:
		quit(3)
		return
	var old_story := _story()
	var powers_seen: Dictionary = {}
	var requested := OS.get_environment("BUBBLE_DUEL_CYCLES")
	var iteration_count := 100 if requested.is_empty() else clampi(int(requested), 1, 100)
	for run: int in range(iteration_count):
		var before := bad
		var result := _tour(run, powers_seen)
		_check("tour %d returns to Jobs" % run, result)
		_check("tour %d preserves other progress" % run, _story() == old_story)
		rows.append({"run": run, "passed": bad == before, "pearls": Shop.state(main)["pearls"],
			"owned": Shop.state(main)["owned"], "gear": Shop.equipped(main)})
		await process_frame
	for item: Dictionary in Shop.ITEMS:
		_check("owns " + item["id"], item["id"] in Shop.state(main)["owned"])
	_check("all seven powers exercised", powers_seen.size() == 7)
	var inventory := Shop.state(main)
	var disk: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(main._save_state.save_path))
	_check("saved inventory round trips", disk[Shop.SAVE_KEY] == JSON.parse_string(JSON.stringify(inventory)))
	var original := main._save_state.future_schema_read_only
	main._save_state.future_schema_read_only = true
	var previous := Shop.state(main)
	_check("blocked save rejects purchase", not Shop.choose_item(main, "classic"))
	_check("blocked save rolls back the inventory", Shop.state(main) == previous)
	main._save_state.future_schema_read_only = original
	var file := FileAccess.open(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info().string,
		"cycles": rows, "checks": checked, "failures": bad, "powers_seen": powers_seen}, "  "))
	file.close()
	venue.close()
	main.queue_free()
	await process_frame
	print("BUBBLESTRESS|", rows.size(), " tours|", checked, " checks|", bad, " failures")
	quit(0 if bad == 0 else 1)


func _verify_reload() -> void:
	var previous: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT")))
	var last: Dictionary = previous["cycles"][-1]
	var saved := Shop.state(main)
	_check("fresh process restores pearl balance", int(saved["pearls"]) == int(last["pearls"]))
	_check("fresh process restores equipped outfit", Shop.equipped(main) == String(last["gear"]))
	_check("fresh process restores all purchased outfits", saved["owned"] == last["owned"])
	_check("fresh process restores selected bubble color", Shop.color(main) == 4)
	for index: int in range(5):
		_check("fresh process restores color ownership " + str(index), index in saved["colors"])
	var file := FileAccess.open(OS.get_environment("BUBBLE_DUEL_RELOAD_OUTPUT"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks": checked, "failures": bad, "inventory": saved}, "  "))
	file.close()
	print("BUBBLERELOAD|", checked, " checks|", bad, " failures")
	main.queue_free()
	quit(0 if bad == 0 else 1)


func _check(label: String, condition: bool) -> void:
	checked += 1
	if not condition:
		bad += 1
		print("BUBBLESTRESS|FAIL|", label)


func _story() -> Array:
	return [main.opera_stars, main.opera_progress, main.pearl_count, main.medals.duplicate(true),
		main.chapter2_party_piece_mask, main.chapter2_job_phase_masks.duplicate()]


func _tap(control: Control, at: Vector2 = Vector2(-1, -1)) -> void:
	var point := control.size * 0.5 if at.x < 0 else at
	var screen := root.get_screen_transform() * (control.get_screen_transform() * point)
	for pressed: bool in [true, false]:
		var event := InputEventScreenTouch.new()
		event.index = 1
		event.pressed = pressed
		event.position = screen
		root.push_input(event, false)


func _back() -> void:
	_tap(main.global_navigation_button)


func _card(d: Control, index: int) -> void:
	_tap(d.menu.get_child(index) as Control)


func _gear_card(d: Control, id: String) -> Control:
	for child: Node in d.menu.get_children():
		if child is Control and child.get_meta("gear_id", "") == id:
			return child as Control
	return null


func _hit(d: Control, expected: int, dt: float) -> bool:
	for attempt: int in range(5):
		if d.score == expected:
			return true
		for frame: int in range(60):
			d._process(dt)
			if d.return_cooldown <= 0.0:
				break
		_tap(d, d._target(0))
		for frame: int in range(300):
			var other_target: Vector2 = d._target(1)
			d._process(dt)
			if d.score == expected:
				if d.mode == Duel.Mode.CURRENT:
					_check("collecting a pearl does not teleport its neighbour", absf(d._target(1).y - other_target.y) <= 60.0 * dt + 0.01)
				return true
	return false


func _tour(index: int, seen: Dictionary) -> bool:
	_tap(venue.bubble_duel_button)
	var d: Control = venue.bubble_duel
	if d == null:
		return false
	d.set_process(false)
	_card(d, 3)
	var before := Shop.state(main)
	var selected := index % 5
	_card(d, selected)
	var after := Shop.state(main)
	var expected_cost := 0 if selected in before["colors"] else Shop.COLOR_PRICES[selected]
	if int(before["pearls"]) >= expected_cost:
		_check("color purchase charges once", int(before["pearls"]) - int(after["pearls"]) == expected_cost)
		_card(d, selected)
		_check("owned color is free to equip", Shop.state(main)["pearls"] == after["pearls"])
	var desired := index % Shop.ITEMS.size()
	for slot: int in range(1, Shop.ITEMS.size()):
		if Shop.ITEMS[slot]["id"] not in Shop.state(main)["owned"]:
			desired = slot
			break
	var entry: Dictionary = Shop.ITEMS[desired]
	var required_page := desired / 4
	if d.shop_page != required_page:
		d._turn_shop_page()
	var button := _gear_card(d, entry["id"])
	if button == null:
		return false
	before = Shop.state(main)
	_tap(button)
	after = Shop.state(main)
	if int(before["pearls"]) >= int(entry["price"]) or entry["id"] in before["owned"]:
		_check("owned outfit equipped", Shop.equipped(main) == entry["id"])
		var cost: int = 0 if entry["id"] in before["owned"] else int(entry["price"])
		_check("outfit exact price", int(before["pearls"]) - int(after["pearls"]) == cost)
		_tap(_gear_card(d, entry["id"]))
		_check("repeat outfit purchase idempotent", Shop.state(main)["pearls"] == after["pearls"])
	else:
		_check("unaffordable outfit preserves balance and ownership", before == after)
	_back()
	_card(d, 1)
	var dt := 1.0 / (30.0 if index % 2 else 60.0)
	for frame: int in range(20):
		d._process(dt)
	_check("idle practice cannot score", d.score == 0 and not d.armed)
	_check_solo_controls(d)
	if not _hit(d, 1, dt):
		return false
	_back()
	_card(d, 2)
	_check_solo_controls(d)
	if not _hit(d, 1, dt):
		return false
	_back()
	_card(d, 0)
	_check("Duel presents character and equipment setup", d.mode == Duel.Mode.SETUP)
	for child: Node in d.menu.get_children():
		if child is Button and child.tooltip_text == "Play":
			_tap(child as Control)
			break
	_check("setup Play starts actual Duel", d.mode == Duel.Mode.DUEL)
	var gear: String = d.gear
	var starting_rival: Vector2 = d.rival
	_tap(d, d._target(0))
	d._process(dt)
	_check("Computer friend starts moving without a position jump", d.rival.distance_to(starting_rival) <= 5.0)
	d._begin(Duel.Mode.DUEL)
	var initial_glow: float = d.glow
	if gear != "classic":
		_tap(d.power_button)
		if gear == "tidewing":
			seen[gear] = true
			_check("passive ribbons keep glow", d.glow == initial_glow)
			_tap(d, Vector2(230, 530))
			var lift_seen := false
			for frame: int in range(100):
				d._process(dt)
				if d.velocity_y < -20.0 and d.power_time > 0.0:
					lift_seen = true
			_check("ribbons provide a real lift after swimming", lift_seen)
			d._begin(Duel.Mode.DUEL)
		else:
			_check("power charges its glow cost", d.glow < initial_glow)
			seen[gear] = true
			var rival_before: Vector2 = d.rival
			for frame: int in range(12):
				d._process(dt)
			if gear == "rainbow":
				for frame: int in range(180):
					d._process(dt)
					if d.score == 1:
						break
				_check("wand projectile makes contact without a tail hit", d.score == 1)
			elif gear == "moonpearl":
				_check("moonpearl holds Roshan at her height", absf(d.swimmer.y - d.START.y) < 1.0)
			elif gear == "squid":
				_check("ink holds computer friend", d.rival == rival_before)
			elif gear == "kelp":
				_check("kelp pulls computer friend smoothly", d.rival_offset.length() > 0.0)
			elif gear == "lullaby":
				_check("lullaby drains rival glow", d.rival_glow < 50.0)
			elif gear == "swiftconch":
				_check("conch moves Roshan", d.swimmer != d.START)
	for expected: int in [1, 2]:
		if d.score < expected and not _hit(d, expected, dt):
			return false
	if d.mode != Duel.Mode.CELEBRATE:
		return false
	before = Shop.state(main)
	for frame: int in range(20):
		d._process(dt)
	_check("completed round cannot duplicate reward", Shop.state(main) == before)
	_card(d, 0)
	if d.mode != Duel.Mode.DUEL or d.score != 0:
		return false
	if gear != "classic":
		_tap(d.power_button)
	d._notification(Control.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_check("focus loss clears active powers and input", not d.armed and d.projectiles.is_empty() and d.power_time == 0.0)
	for frame: int in range(90):
		d._process(dt)
	_check("focus loss cannot finish a bout", d.score == 0)
	_back()
	_back()
	if venue.bubble_duel != null:
		return false
	return venue.accepting_input and main._navigation_ref().top_id() == "opera_venue"



func _check_solo_controls(d: Control) -> void:
	if d.gear in ["kelp", "lullaby", "squid"]:
		var initial: float = d.glow
		_check("friend-only power is not offered without a friend", not d.power_button.visible and not d.glow_bar.visible)
		d._activate_power()
		_check("inapplicable power cannot spend glow or start a swim", d.glow == initial and not d.armed)
