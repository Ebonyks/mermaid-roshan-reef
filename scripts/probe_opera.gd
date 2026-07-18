extends SceneTree
# Pearl Opera House regression: ten costume acts across two floors (four
# shows + a boss showdown per floor), no passive wins, wrong answers stay
# gentle, checkpoint resume, and the completion rewards land exactly once.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260718)
	Engine.time_scale = 8.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	# A brand-new save must be able to enter: the opera teaches its own shows.
	main.opera_progress = 0
	main.opera_done = false
	main.stickers.erase("showtime")
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_opera()
	var opera: OperaHouse = main.opera_game
	_ck("fresh save can enter the opera house", opera != null)
	await _wait_for_act(opera, 0)
	_ck("opera defines ten acts", OperaHouse.ACTS.size() == 10)
	var floor1_shows := 0
	var floor2_shows := 0
	var floor1_boss := 0
	var floor2_boss := 0
	for cfg: Dictionary in OperaHouse.ACTS:
		var story := int(cfg.get("story", 0))
		if String(cfg.get("type", "show")) == "boss":
			if story == 1: floor1_boss += 1
			else: floor2_boss += 1
		else:
			if story == 1: floor1_shows += 1
			else: floor2_shows += 1
	_ck("each floor runs four shows", floor1_shows == 4 and floor2_shows == 4)
	_ck("each floor ends with one boss", floor1_boss == 1 and floor2_boss == 1)
	_ck("floor one closes with a boss act", String(OperaHouse.ACTS[4]["type"]) == "boss")
	_ck("floor two closes with a boss act", String(OperaHouse.ACTS[9]["type"]) == "boss")
	_ck("progress HUD never blocks touch", opera.progress_label.mouse_filter == Control.MOUSE_FILTER_IGNORE and opera.act_label.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	var act: OperaAct = opera.act
	_ck("act one dresses Roshan in a costume", act.costume_root != null and act.costume_root.get_child_count() > 0)
	_ck("act one stays inside the mobile node budget", _descendants(act) < 130)
	_ck("the audience of friends is watching", act.audience.size() == 4)
	for i in range(30): await process_frame
	_ck("act one cannot win passively", opera.act_index == 0 and act.state == "play")
	# a wrong tap wobbles and re-hints, it never fails or advances
	var first_cfg: Dictionary = OperaHouse.ACTS[0]
	var order: Array = first_cfg["order"]
	var wrong: int = (int(order[0]) + 1) % 3
	act._act_action(wrong)
	_ck("wrong cake layer is gentle (no fail, no step)", act.state == "play" and act.step == 0)
	_drive_order(act, order)
	_ck("finishing the recipe wins act one", act.state == "won")
	act.win_t = 0.0
	await _wait_for_act(opera, 1)
	_ck("act one clear saves a checkpoint", main.opera_progress == 1)
	opera._leave_early()
	await process_frame
	_ck("home icon returns safely", main.game == "level2" and main.opera_game == null)
	main._start_opera()
	opera = main.opera_game
	await _wait_for_act(opera, 1)
	_ck("next visit resumes at act two", opera.act_index == 1 and opera.act != null)
	for expected in range(1, OperaHouse.ACTS.size()):
		await _wait_for_act(opera, expected)
		var cfg2: Dictionary = OperaHouse.ACTS[expected]
		act = opera.act
		_ck("act %d builds its %s engine" % [expected + 1, String(cfg2["kind"])], act != null and act.kind == String(cfg2["kind"]))
		match String(cfg2["kind"]):
			"order":
				_drive_order(act, cfg2["order"])
			"echo":
				await _drive_echo(act)
			"shuffle":
				await _drive_shuffle(act, expected)
			"fix":
				_drive_fix(act)
			"press":
				await _drive_press(act)
			"boss":
				await _drive_boss(act, bool(cfg2.get("dual", false)))
		_ck("act %d reaches its curtain call" % (expected + 1), act.state == "won" or act.state == "done")
		act.win_t = 0.0
		if expected < OperaHouse.ACTS.size() - 1:
			await _wait_for_act(opera, expected + 1)
	await process_frame
	await process_frame
	_ck("all ten checkpoints persist", main.opera_progress == 10)
	_ck("final act completes the opera", main.opera_done)
	_ck("the Showtime sticker is earned", bool(main.stickers.get("showtime", false)))
	opera._finish(true)
	await process_frame
	_ck("completion returns to the castle", main.game == "level2" and main.opera_game == null)
	print("OPERA|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _drive_order(act: OperaAct, order: Array) -> void:
	for choice in order:
		var idx := int(choice)
		act.player_pos = (act.pads[idx]["pos"] as Vector3)
		_ck("order pad %d reachable by proximity" % idx, act._nearest_pad() == idx)
		act._act_action(idx)

func _drive_echo(act: OperaAct) -> void:
	var guard := 0
	var wrong_tested := false
	while act.state == "play" and guard < 900:
		guard += 1
		if act.echo_phase == "repeat":
			var want: int = act.echo_seq[act.echo_pos]
			if not wrong_tested and act.echo_seq.size() > 1:
				wrong_tested = true
				var miss: int = (want + 1) % act.pads.size()
				act._pad_touch(miss)
				_ck("wrong dance step only replays the tune", act.state == "play" and act.echo_phase == "show")
				continue
			act._pad_touch(want)
		else:
			await process_frame
	_ck("echo act does not stall", guard < 900)

func _drive_shuffle(act: OperaAct, expected: int) -> void:
	var guard := 0
	var wrong_tested := false
	while act.state == "play" and guard < 900:
		guard += 1
		if act.shuffle_phase == "pick":
			if not wrong_tested:
				wrong_tested = true
				var empty_hat: int = (act.bunny_at + 1) % 3
				var round_before: int = act.shuffle_round
				act.player_pos = (act.hats[empty_hat]["pos"] as Vector3)
				act._act_action(act._nearest_pad())
				_ck("act %d empty hat is a mercy peek, not a fail" % (expected + 1), act.state == "play" and act.shuffle_round == round_before)
				continue
			act.player_pos = (act.hats[act.bunny_at]["pos"] as Vector3)
			_ck("bunny hat reachable by proximity", act._nearest_pad() == act.bunny_at)
			act._act_action(act.bunny_at)
		else:
			await process_frame
	_ck("shuffle act does not stall", guard < 900)

func _drive_fix(act: OperaAct) -> void:
	_ck("pipe puzzle has three gaps and three pieces", act.slots.size() == 3 and act.pieces.size() == 3)
	# a wrong shape bounces home kindly — no fail, no lost progress
	var need0: int = int(act.slots[0]["need"])
	var wrong_piece: int = (need0 + 1) % 3
	act._pick_piece(wrong_piece)
	_ck("any piece can be picked up", act.carried == wrong_piece)
	act._place_piece()
	_ck("wrong pipe shape bounces home gently", act.carried == -1 and act.fix_step == 0 and not bool(act.pieces[wrong_piece]["placed"]))
	for s in range(3):
		var need: int = int(act.slots[act.fix_step]["need"])
		act.player_pos = act.pieces[need]["pos"] as Vector3
		_ck("pipe piece %d reachable by proximity" % need, act._nearest_piece() == need)
		act._pick_piece(need)
		act._place_piece()
	_ck("three placed pipes reveal the valve", act.fix_phase == "valve")
	act._turn_valve()
	_ck("spinning the valve launches the rocket", act.state == "won")

func _drive_press(act: OperaAct) -> void:
	# a mistimed press only squishes a giggle — the candy always survives
	act.press_x = 0.96
	act._press_action()
	_ck("mistimed press is gentle (no fail, no candy)", act.state == "play" and act.candies_done == 0)
	var guard := 0
	while act.state == "play" and guard < 900:
		guard += 1
		if act.press_busy <= 0.0 and act.candy_node != null:
			act.press_x = 0.0
			act._press_action()
		else:
			await process_frame
	_ck("press act does not stall", guard < 900)
	_ck("three smiley candies finish the show", act.candies_done == 3)

func _drive_boss(act: OperaAct, dual: bool) -> void:
	var hp: int = int(act.boss["hp"])
	_ck("boss starts with three sparkle stars", hp == 3)
	if dual:
		_ck("phantom opens hidden in shadow", String(act.boss["phase"]) == "shadow" and act.action_label() == "SHINE")
		act._hit_boss()
		_ck("sparkles cannot skip the lantern lesson", int(act.boss["hp"]) == hp)
		for cycle in range(hp):
			_ck("cycle %d asks for the lantern first" % (cycle + 1), String(act.boss["phase"]) == "shadow")
			act._light_lantern()
			_ck("cycle %d lit lantern reveals the phantom" % (cycle + 1), String(act.boss["phase"]) == "peek" and act.action_label() == "SPARKLE")
			act._hit_boss()
	else:
		_ck("dragon opens hiding in the curtains", String(act.boss["phase"]) == "hide" and act.action_label() == "SPARKLE")
		act._hit_boss()
		_ck("sparkles fizzle while he hides", int(act.boss["hp"]) == hp)
		var guard := 0
		while act.state == "play" and guard < 900:
			guard += 1
			if String(act.boss["phase"]) == "peek":
				act._hit_boss()
			else:
				await process_frame
		_ck("dragon act does not stall", guard < 900)

func _wait_for_act(opera: OperaHouse, expected: int) -> void:
	var guard := 0
	while opera != null and (opera.act_index != expected or opera.act == null) and guard < 400:
		guard += 1
		await process_frame

func _descendants(node: Node) -> int:
	var total := 0
	for child in node.get_children():
		total += 1 + _descendants(child)
	return total

func _ck(label: String, ok: bool) -> void:
	print("OPERA|", label, ": ", "OK" if ok else "FAIL")
	if not ok: bad += 1
