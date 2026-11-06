extends SceneTree
## Full real-venue bouts. Policies press actual viewport controls; no combat warps.
const Duel := preload("res://scripts/opera_bubble_duel.gd")
const Shop := preload("res://scripts/bubble_duel_inventory.gd")
var main: ReefMain
var venue: OperaHouseVenue2D
var bad: int = 0
var checked: int = 0
var rows: Array[Dictionary] = []
var powers_seen: Dictionary = {}
var power_cases: Array[Dictionary] = []
var source_snapshot: Dictionary = {}


func _initialize() -> void:
	var fixture: String = OS.get_environment("BUBBLE_DUEL_STRESS_ROOT").replace("\\", "/").simplify_path()
	var actual: String = OS.get_user_data_dir().replace("\\", "/").simplify_path()
	if fixture.is_empty() or not actual.begins_with(fixture.trim_suffix("/") + "/"):
		printerr("BUBBLESTRESS|isolated test directory required")
		quit(2)
		return
	call_deferred("_run")


func _run() -> void:
	source_snapshot = _source_hashes()
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	Engine.time_scale = 8
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
	for frame: int in range(12): await process_frame
	main._castle_rooms_ref().show_room("opera_hall", false)
	for frame: int in range(3): await process_frame
	_check("Opera venue opens", main._castle_career_routes_ref().open_opera_venue())
	venue = main._castle_career_routes_ref().opera_venue
	if venue == null:
		quit(3)
		return
	var story: Array = _story()
	# Explicit isolated economy fixture; all subsequent purchases use real buttons.
	main.save_data[Shop.SAVE_KEY] = {"pearls": 30000, "owned": ["classic"], "colors": [0],
		"future_item": {"keep": true}, "players": {"future": {"keep": 7}},
		"campaign": {"future": "preserved", "stage": 0}}
	main._write_save()
	await _enter()
	var d: BubbleDuelOverlay = venue.bubble_duel
	if d == null:
		quit(4)
		return
	d.set_process(false)
	_inventory(d)
	_controls(d)
	_powers(d)
	_bonus_and_checkpoint(d)
	_back()
	_back()
	var amount: int = clampi(int(OS.get_environment("BUBBLE_DUEL_CYCLES")), 1, 100)
	for index: int in range(amount):
		var prior: int = bad
		await _enter()
		d = venue.bubble_duel
		if d == null:
			_check("elevator reopens", false)
			break
		d.set_process(false)
		_tour(d, index)
		_check("story and family wardrobe untouched", _story() == story)
		_check("unknown nested save values retained", Shop.state(main)["future_item"] == {"keep": true}
			and Shop.state(main)["players"]["future"] == {"keep": 7}
			and Shop.campaign(main)["future"] == "preserved")
		var saved: Dictionary = Shop.state(main)
		rows.back()["passed"] = bad == prior
		rows.back()["pearls"] = saved["pearls"]
		rows.back()["owned"] = saved["owned"]
		rows.back()["gear"] = Shop.equipped(main)
		print("BUBBLESTRESS|ROW|",index,"|complete=",rows.back()["completed"],"|seconds=",rows.back()["seconds"],"|mode=",rows.back()["mode"])
		_report(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT") + ".partial.json", {"cycles": rows, "failures": bad})
		_back()
		_back()
		_check("Back restores venue route and controls", venue.bubble_duel == null and venue.accepting_input
			and main._navigation_ref().top_id() == "opera_venue")
		await process_frame
	_check("candidate source stays unchanged throughout trial", _source_hashes() == source_snapshot)
	var inventory: Dictionary = Shop.state(main)
	var disk: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(main._save_state.save_path))
	_check("all progress matches disk", disk[Shop.SAVE_KEY] == JSON.parse_string(JSON.stringify(inventory)))
	var readonly: bool = main._save_state.future_schema_read_only
	main._save_state.future_schema_read_only = true
	var before: Dictionary = Shop.state(main)
	_check("blocked purchase rejected", not Shop.choose_item(main, "classic"))
	_check("blocked purchase rolls back", Shop.state(main) == before)
	main._save_state.future_schema_read_only = readonly
	_report(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT"), {"engine": Engine.get_version_info(),
		"cycles": rows, "checks": checked, "failures": bad, "powers_seen": powers_seen, "power_cases": power_cases,
		"inventory": inventory, "source_hashes": source_snapshot, "scope": "Actual viewport touch pulses; source-art geometry; natural bouts and explicit timed friendly draws. No mid-bout position, velocity, bubble or stock edits. Bot evidence is not human fun or device acceptance."})
	venue.close()
	main.queue_free()
	await process_frame
	print("BUBBLESTRESS|", rows.size(), " bouts|", checked, " checks|", bad, " failures")
	quit(0 if bad == 0 else 1)


func _enter() -> void:
	_tap(venue.bubble_duel_button)
	_check("elevator tap starts walking before entry", venue.bubble_duel == null)
	for frame: int in range(500):
		if venue.bubble_duel != null: return
		await process_frame
	_check("physical elevator arrival opens arcade", venue.bubble_duel != null)


func _tour(d: BubbleDuelOverlay, index: int) -> void:
	var pair: int = index / 2 if index % 2 == 0 else index
	for player: int in range(2):
		_check("cast selection saves", Shop.choose_character(main, BubbleDuelCast.PEOPLE[(pair / (6 if player else 1)) % 6], player))
		_check("independent purchased power selection", Shop.choose_item(main, Shop.ITEMS[(index + player * 3) % 8]["id"], player))
		_check("independent color selection", Shop.choose_color(main, (index + player) % 5, player))
	var stage_before: int = int(Shop.campaign(main)["stage"])
	var kind: int = index % 4
	var resumed_damage: int = 0
	var checkpoint: Dictionary = Shop.campaign(main).get("checkpoint", {})
	if kind in [1, 2] and int(checkpoint.get("stage", -1)) == stage_before:
		var enemies: Array = checkpoint.get("enemies", [])
		for saved: Dictionary in enemies:
			resumed_damage += maxi(0, 2 - int(saved.get("bubbles", 2)))
	if kind == 0: d._begin_versus()
	elif kind == 1: d._begin(Duel.Mode.DUEL)
	elif kind == 2: d._begin_coop()
	else: d._begin(Duel.Mode.PRACTICE)
	_check("separate selected human loadout", d.world.human(0).profile == Shop.profile(main, 0))
	var players: int = 2 if d.local_two_player else 1
	if players == 2: _check("second player selected loadout", d.world.human(1).profile == Shop.profile(main, 1))
	var policies: Array[BubbleDuelTestPolicy] = []
	var presses: Array[int] = [0, 0]
	for player: int in range(players):
		policies.append(BubbleDuelTestPolicy.new(5101 + index * 83 + player * 73, 6 + (index + player * 2) % 5, player == index % players))
	var ticks: int = 0
	while d.mode != Duel.Mode.CELEBRATE and ticks < 7200:
		for player: int in range(players):
			var fighter: BubbleDuelFighter = d.world.human(player)
			var action: Dictionary = policies[player].observe(fighter, d.world, ticks)
			if ticks == 0 or bool(action["flap"]):
				var point: Vector2 = d.Duo.PADS[player].get_center() + Vector2(float(action["axis"]) * 60, 0)
				_finger(d, 10 + player, point, true)
				_finger(d, 10 + player, point, false)
				presses[player] += 1
			if bool(action["power"]): _tap(d.power_button if player == 0 else d.second_power_button)
		d._process(1.0 / 30.0)
		ticks += 1
		if ticks % 30 == 0:
			for fighter: BubbleDuelFighter in d.world.fighters:
				_check("finite bounded live simulation", fighter.position.is_finite() and fighter.velocity.is_finite()
					and fighter.bubbles in range(3) and fighter.spares >= 0 and fighter.charge >= 0 and fighter.charge <= 100.001)
	if d.mode != Duel.Mode.CELEBRATE:
		for fighter: BubbleDuelFighter in d.world.fighters:
			print("UISTALL|run=",index,"|slot=",fighter.slot,"|",fighter.position,"|",fighter.velocity,"|bubbles=",fighter.bubbles,"|gear=",fighter.gear,"|lost=",fighter.lost)
	_check("complete bout through real controls", d.mode == Duel.Mode.CELEBRATE)
	_check("fresh rounds pop physically; continuations retain proven prior damage", d.world.pops > 0 or resumed_damage > 0)
	_check("every human issues real press impulses", presses[0] > 1 and (players == 1 or presses[1] > 1))
	if kind in [1, 2]:
		_check("timed rest saves progress without inventing a win", int(Shop.campaign(main)["stage"]) == (stage_before if d.world.timed_draw else (stage_before + 1) % 16))
	var earned: Dictionary = Shop.state(main)
	for frame: int in range(30): d._process(1.0 / 30.0)
	_check("celebration cannot repeat payout", Shop.state(main) == earned)
	rows.append({"run": index, "mode": kind, "completed": d.mode == Duel.Mode.CELEBRATE,
		"ticks": ticks, "seconds": float(ticks) / 30, "pops": d.world.pops,
		"winner": d.world.winner, "timed_draw": d.world.timed_draw, "resumed_bubble_damage": resumed_damage,
		"bumps": d.world.bumps, "presses": presses, "enemies": d.world.fighters.size() - players,
		"p1": Shop.profile(main, 0), "p2": Shop.profile(main, 1),
		"campaign": Shop.campaign(main)})


func _inventory(d: BubbleDuelOverlay) -> void:
	d._show_shop()
	for index: int in range(5):
		var before: Dictionary = Shop.state(main)
		_tap(d.menu.get_child(index) as Control)
		var cost: int = 0 if index in before["colors"] else Shop.COLOR_PRICES[index]
		_check("pictured color exact price", int(Shop.state(main)["pearls"]) == int(before["pearls"]) - cost)
	for index: int in range(Shop.ITEMS.size()):
		var id: String = Shop.ITEMS[index]["id"]
		if d.shop_page != index / 4: d._turn_shop_page()
		var before: Dictionary = Shop.state(main)
		var card: Control = _gear_card(d, id)
		_check("pictured item exists", card != null)
		if card == null: continue
		_tap(card)
		var cost: int = 0 if id in before["owned"] else Shop.ITEMS[index]["price"]
		_check("item exact price and ownership", int(Shop.state(main)["pearls"]) == int(before["pearls"]) - cost
			and Shop.equipped(main) == id)
		_tap(_gear_card(d, id))
		_check("repeat owned purchase is free", int(Shop.state(main)["pearls"]) == int(before["pearls"]) - cost)


func _controls(d: BubbleDuelOverlay) -> void:
	Shop.choose_item(main, "classic")
	d._begin_versus()
	var first: Vector2 = d.world.human(0).position
	for frame: int in range(120): d._process(1.0 / 30)
	_check("zero input never starts or rewards", not d.world.started and d.world.human(0).position == first)
	for player: int in range(2):
		_finger(d, 30 + player, d.Duo.PADS[player].get_center() + Vector2(60 if player == 0 else -60, 0), true)
	for frame: int in range(10): d._process(1.0 / 30)
	_check("two real fingers have independent ownership", d.duo_touch_owners.size() == 2)
	_check("holding causes exactly one flap each", d.world.human(0).kick_count == 1 and d.world.human(1).kick_count == 1)
	_check("direction is an impulse, not direct velocity", is_equal_approx(d.world.human(0).velocity.x, 2.25) and is_equal_approx(d.world.human(1).velocity.x, -2.25))
	var momentum: Vector2 = d.world.human(0).velocity
	var point: Vector2 = d.world.human(0).position
	d.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_check("focus clears input, preserves momentum", d.duo_touch_owners.is_empty() and d.world.human(0).velocity == momentum)
	for frame: int in range(30): d._process(1.0 / 30)
	_check("suspended game never advances", d.world.human(0).position == point)
	_tap(d, d.Duo.PADS[0].get_center())
	d._process(1.0 / 30)
	_check("fresh press resumes physical movement", not d.world.paused and d.world.human(0).position != point)
	d._begin_versus()
	_tap(d, d.Duo.PADS[0].get_center() + Vector2(60, 0))
	d._process(1.0 / 30)
	_check("released quick tap retains its queued direction", is_equal_approx(d.world.human(0).velocity.x, 2.25))
	d._begin_versus()
	_finger(d, 80, d.Duo.PADS[0].get_center(), true)
	var cancel := InputEventScreenTouch.new()
	cancel.index = 80
	cancel.canceled = true
	cancel.pressed = false
	cancel.position = root.get_screen_transform() * (d.get_screen_transform() * d.Duo.PADS[0].get_center())
	root.push_input(cancel, false)
	d._process(1.0 / 30)
	_check("canceled press cannot start the match", not d.world.started)


func _powers(d: BubbleDuelOverlay) -> void:
	for player: int in range(2):
		for person: String in BubbleDuelCast.PEOPLE:
			for entry: Dictionary in Shop.ITEMS:
				var id: String = entry["id"]
				if id == "classic": continue
				for slot: int in range(2): Shop.choose_item(main, "classic", slot)
				Shop.choose_character(main, person, player)
				Shop.choose_item(main, id, player)
				d._begin_versus()
				# Explicit isolated activation fixture, never a complete-bout result.
				var actor: BubbleDuelFighter = d.world.human(player)
				var target: BubbleDuelFighter = d.world.human(1 - player)
				actor.charge = 100
				target.charge = 100
				_tap(d, d.Duo.PADS[player].get_center())
				if id == "tidewing":
					for tick: int in range(120): d._process(1.0 / 30)
				else:
					d._refresh_power()
					_tap(d.power_button if player == 0 else d.second_power_button)
					d._process(1.0 / 30)
				var activated: bool = actor.kick_count > 1 if id == "tidewing" else actor.charms_used > 0
				_check("real equipment activation %s/%s/P%d" % [person, id, player + 1], activated)
				if id != "tidewing":
					_check("equipment spends its energy", actor.charge < 100)
				match id:
					"swiftconch": _check("conch is a facing-dependent impulse", actor.velocity.x * actor.facing > 6)
					"moonpearl": _check("short pearl tap reaches the hover path", actor.hover_last)
					"kelp": _check("kelp transfers real wrapped momentum", absf(target.velocity.x) > 1)
					"lullaby": _check("lullaby drains the opponent battery", target.charge < 5)
					"squid": _check("squid holds the intended opponent", target.held >= 39)
					"rainbow":
						var owned_shot: bool = false
						for shot: Dictionary in d.world.shots:
							if int(shot["life"]) > 0 and int(shot["owner"]) == actor.slot: owned_shot = true
						_check("wand shot preserves correct player ownership", owned_shot)
				powers_seen[id] = bool(powers_seen.get(id, true)) and activated
				power_cases.append({"player": player, "character": person, "gear": id, "activated": activated})
	_check("all84 cast/power/player fixture cases run", power_cases.size() == 84)
	_check("all seven power paths exercised for both players", powers_seen.size() == 7 and false not in powers_seen.values())



func _verify_reload() -> void:
	var previous: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT")))
	var saved: Dictionary = Shop.state(main)
	_check("fresh process restores complete inventory and checkpoints", JSON.parse_string(JSON.stringify(saved)) == previous["inventory"])
	_report(OS.get_environment("BUBBLE_DUEL_RELOAD_OUTPUT"), {"checks": checked, "failures": bad, "inventory": saved})
	main.queue_free()
	quit(0 if bad == 0 else 1)


func _story() -> Array:
	return [main.opera_stars, main.opera_progress, main.pearl_count, main.medals.duplicate(true),
		main.chapter2_party_piece_mask, main.chapter2_job_phase_masks.duplicate(),
		main.character_outfits.duplicate(true), main.character_clothing_parts.duplicate(true), main.outfits_unlocked.duplicate(true)]


func _check(label: String, condition: bool) -> void:
	checked += 1
	if not condition:
		bad += 1
		if bad < 80: print("BUBBLESTRESS|FAIL|", label)


func _tap(control: Control, at: Vector2 = Vector2(-1, -1)) -> void:
	var point: Vector2 = control.size * 0.5 if at.x < 0 else at
	for down: bool in [true, false]: _finger(control, 1, point, down)


func _finger(control: Control, id: int, point: Vector2, down: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = id
	event.pressed = down
	event.position = root.get_screen_transform() * (control.get_screen_transform() * point)
	root.push_input(event, false)


func _back() -> void:
	_tap(main.global_navigation_button)


func _gear_card(d: BubbleDuelOverlay, id: String) -> Control:
	for child: Node in d.menu.get_children():
		if child is Control and child.get_meta("gear_id", "") == id: return child as Control
	return null


func _report(path: String, value: Dictionary) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	if file != null:
		file.store_string(JSON.stringify(value, "\t") + "\n")
		file.close()
	else:
		_check("report can be written", false)


func _bonus_and_checkpoint(d: BubbleDuelOverlay) -> void:
	Shop.choose_character(main, "roshan", 0)
	Shop.choose_item(main, "classic", 0)
	d._begin(Duel.Mode.DUEL)
	var pilot := BubbleDuelTestPolicy.new(109, 6, true)
	for tick: int in range(2700):
		if d.score > 0 or d.mode == Duel.Mode.CELEBRATE: break
		var action: Dictionary = pilot.observe(d.world.human(0), d.world, tick)
		if tick == 0 or bool(action["flap"]):
			_tap(d, d.Duo.PADS[0].get_center() + Vector2(float(action["axis"]) * 60, 0))
		d._process(1.0 / 30)
	_check("checkpoint fixture earns a genuine first pop", d.score > 0 and d.mode != Duel.Mode.CELEBRATE)
	var checkpoint: Dictionary = Shop.campaign(main)["checkpoint"].duplicate(true)
	var coins: int = int(Shop.state(main)["pearls"])
	_back()
	d._begin(Duel.Mode.DUEL)
	var index: int = 0
	for fighter: BubbleDuelFighter in d.world.fighters:
		if fighter.human >= 0: continue
		var enemy: Dictionary = checkpoint["enemies"][index]
		_check("return restores exact partial enemy bubble and spare state", fighter.bubbles == int(enemy["bubbles"])
			and fighter.spares == int(enemy["spares"]) and fighter.lost == bool(enemy["lost"]))
		index += 1
	_check("restoring a checkpoint never pays again", int(Shop.state(main)["pearls"]) == coins and not d.world.started)
	d._begin(Duel.Mode.CURRENT)
	var before: int = int(Shop.state(main)["pearls"])
	var taps: int = 0
	var ink_seen: bool = false
	for tick: int in range(2702):
		if d.mode == Duel.Mode.CELEBRATE: break
		var player: BubbleDuelFighter = d.world.human(0)
		var goal := Vector2(150, 150)
		var nearest: float = INF
		for item: Dictionary in d.bonus_items:
			if not bool(item["active"]): continue
			if item["kind"] == "ink":
				ink_seen = true
				continue
			var point: Vector2 = item["position"]
			var distance: float = absf(point.x - player.position.x) + absf(point.y - player.position.y)
			if point.x > 40 and distance < nearest:
				goal = point
				nearest = distance
		var vx: float = clampf((goal.x - player.position.x) * 0.12, -3.5, 3.5)
		var vy: float = clampf((goal.y - player.position.y) * 0.12, -4, 4)
		var axis: float = signf(vx - player.velocity.x) if absf(vx - player.velocity.x) > 0.7 else 0.0
		if tick == 0 or (tick % 6 == 0 and player.velocity.y > vy + 0.5):
			_tap(d, d.Duo.PADS[0].get_center() + Vector2(axis * 60, 0))
			taps += 1
		d._process(1.0 / 30)
	_check("current ride ends through actual queued flaps", d.mode == Duel.Mode.CELEBRATE and taps > 1)
	_check("moving pearls and ink hazards both exist", d.score > 0 and ink_seen)
	_check("collected pearls are banked exactly once and best ride persists",
		int(Shop.state(main)["pearls"]) == before + d.score and int(Shop.state(main)["best_ride"]) >= d.score)


func _source_hashes() -> Dictionary:
	var result: Dictionary = {}
	for path: String in ["opera_bubble_duel.gd", "bubble_duel_motion.gd", "bubble_duel_fighter.gd", "bubble_duel_arena.gd", "bubble_duel_brain.gd", "bubble_duel_two_player.gd", "bubble_duel_geometry.gd", "bubble_duel_view.gd", "bubble_duel_inventory.gd", "bubble_duel_cast.gd", "opera_house_venue_2d.gd", "probe_bubble_duel_stress.gd", "bubble_duel_test_policy.gd"]:
		result[path] = FileAccess.get_sha256("res://scripts/" + path)
	return result
