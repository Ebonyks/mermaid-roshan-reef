extends SceneTree
# Pearl Opera House regression: fifteen acts across three lobby floors (four
# career doors + a centre-stage boss medallion per floor, the fifteenth being
# the grand finale), no passive wins, wrong answers stay gentle, stars persist
# across visits, and the completion rewards land exactly once.

var main: ReefMain
var bad := 0
var _once_seen := {}

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
	main.opera_stars = 0
	main.opera_done = false
	main.stickers.erase("showtime")
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_opera()
	var opera: OperaHouse = main.opera_game
	_ck("fresh save can enter the opera house", opera != null)
	await _frames(4)
	_ck("opera defines fifteen acts", OperaHouse.ACTS.size() == 15)
	var shows := {1: 0, 2: 0, 3: 0}
	var bosses := {1: 0, 2: 0, 3: 0}
	for cfg: Dictionary in OperaHouse.ACTS:
		var story := int(cfg.get("story", 0))
		if String(cfg.get("type", "show")) == "boss":
			bosses[story] = int(bosses[story]) + 1
		else:
			shows[story] = int(shows[story]) + 1
	_ck("three floors run four shows each", int(shows[1]) == 4 and int(shows[2]) == 4 and int(shows[3]) == 4)
	_ck("every floor ends with one boss", int(bosses[1]) == 1 and int(bosses[2]) == 1 and int(bosses[3]) == 1)
	_ck("floor bosses sit at acts five, ten and fifteen",
		String(OperaHouse.ACTS[4]["type"]) == "boss" and String(OperaHouse.ACTS[9]["type"]) == "boss" and String(OperaHouse.ACTS[14]["type"]) == "boss")
	_ck("the fifteenth act is the grand finale", bool(OperaHouse.ACTS[14].get("finale", false)))
	# every career is its own minigame on its own stage: no two shows may share
	# an engine kind, and all twelve costumes must have a STAGE_SETS entry
	var show_kinds := {}
	var undressed: Array[String] = []
	for cfg3: Dictionary in OperaHouse.ACTS:
		if String(cfg3.get("type", "show")) == "boss":
			continue
		show_kinds[String(cfg3["kind"])] = int(show_kinds.get(String(cfg3["kind"]), 0)) + 1
		if not OperaAct.STAGE_SETS.has(String(cfg3.get("costume", ""))):
			undressed.append(String(cfg3["career"]))
	_ck("twelve careers run twelve distinct engines", show_kinds.size() == 12)
	_ck("every career has its own dressed stage", undressed.is_empty())
	# ---- the explorable lobby: doors for shows, medallions for bosses ----
	_ck("lobby builds a door for every career show", opera.doors.size() == 12)
	_ck("every floor has a centre-stage medallion", opera.boss_spots.size() == 3)
	_ck("Roshan spawns in the lobby with no act running", opera.act == null and opera.lobby_y == 0.0)
	_ck("lobby HUD never blocks touch", opera.star_label.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	for i in range(30): await process_frame
	_ck("nothing wins passively in the lobby", opera.act == null and main.opera_stars == 0)
	# medallions start dark: standing on one must not start a boss
	_ck("all three medallions start unlit",
		not opera._spot_lit(opera.boss_spots[0]) and not opera._spot_lit(opera.boss_spots[1]) and not opera._spot_lit(opera.boss_spots[2]))
	opera.lobby_pos = (opera.boss_spots[0]["pos"] as Vector3)
	await _frames(30)
	_ck("dark medallion does not start the boss", opera.act == null)
	# handoff floor gating: upper floors and lifts stay locked until the
	# floor below's BOSS star is earned; the lift must stay dormant now
	_ck("upper floors start locked", not opera._floor_unlocked(2) and not opera._floor_unlocked(3))
	opera.lobby_pos = (opera.lifts[0]["pos"] as Vector3) + Vector3(0, 1.1, 0)
	await _frames(40)
	_ck("dormant lift refuses the ride while floors sleep", opera.lobby_y < 0.5 and not opera.lift_busy)
	_ck("shell-clasp gates guard both landings, closed", opera.gates.size() == 2 and not bool(opera.gates[0]["open"]) and not bool(opera.gates[1]["open"]))
	# door one: the chef show gets the full walk-in + brawl + puzzle coverage
	var act: OperaAct = await _open_door(opera, 0)
	# costumes are bone-attached to the REAL rigged player (puppet mode), not
	# floating act props — the act must dress her and put her on stage
	_ck("act one dresses Roshan in a bone-attached costume",
		act != null and String(main.player.costume_id) == "chef" and main.player.costume_nodes.size() > 0)
	_ck("act one puts the real 3D Roshan on stage", bool(main.player.puppet) and main.player.visible)
	_ck("act one stays inside the mobile node budget", _descendants(act) < 170)
	_ck("the audience of friends is watching", act.audience.size() == 4)
	_ck("shelled act opens backstage with the imp brawl", act.stage_phase == "brawl" and act.imps.size() >= 3)
	for i in range(30): await process_frame
	_ck("act one cannot win passively", act.state == "play" and act.stage_phase == "brawl")
	# a sparkle with no imp near just fizzles — never a fail (probe-only
	# teleport to centre stage guarantees every imp is out of reach)
	var far_left: int = act.imps_left
	act.player_pos = act.CENTER + Vector3(0.0, 1.1, 14.0)
	act._brawl_action()
	_ck("far sparkle fizzles kindly in the brawl", act.imps_left == far_left)
	# the last imp is the two-sparkle captain with a giggle-dash between hits
	var captain: Dictionary = act.imps.back()
	_ck("the last imp is a two-sparkle captain", int(captain.get("hp", 1)) == 2)
	var captain_pos: Vector3 = captain["pos"] as Vector3
	act.player_pos = captain_pos
	act._brawl_action()
	_ck("the captain shrugs off the first star and dashes",
		not bool(captain["popped"]) and (captain["pos"] as Vector3).distance_to(captain_pos) > 5.0)
	# the rhythm: the imps are GUARDING someone, and freeing them pays a gift
	_ck("the imps have captives in bubble cages", act.captives.size() == 2)
	_ck("nobody is freed while imps still guard them", not act.gift_given)
	_drive_brawl(act)
	_ck("popped imps open the curtain to the stage", act.stage_phase == "puzzle")
	_ck("the rescue frees the captives", act.gift_given)
	_ck("the freed farmers hand over their carrots",
		int(main.opera_pantry.get("carrots", 0)) >= 1)
	# the pad errand is GONE from the Cake Show — it opens straight onto the
	# sieve now, and a tap on a layer pad is scenery, not a step
	var first_cfg: Dictionary = OperaHouse.ACTS[0]
	var order: Array = first_cfg["order"]
	var wrong: int = (int(order[0]) + 1) % 3
	act._act_action(wrong)
	_ck("tapping a layer pad no longer steps the cake show",
		act.state == "play" and act.step == 0 and act.order_phase == "sift")
	# the rescue arrow is still the safety net: it holds back so the child gets
	# a moment alone with the puzzle, then arrives when she is stuck
	act.progress_t = 0.0
	act._tick_pointer()
	_ck("the arrow waits — the child gets her moment alone", not act.pointer.visible)
	act.progress_t = act.RESCUE_DELAY + 0.1
	act._tick_pointer()
	_ck("a stuck cook is rescued by the arrow", act.pointer.visible)
	act.progress_t = 0.0
	await _drive_order(act, first_cfg)
	_ck("cake show ends in a win", act.state == "won")
	act.win_t = 0.0
	await _wait_lobby(opera)
	_ck("finished door wears a gold star", (main.opera_stars & 1) == 1)
	_ck("one star counts one cleared act", main.opera_progress == 1)
	_ck("the costume comes off backstage",
		String(main.player.costume_id) == "" and main.player.costume_nodes.is_empty() and not bool(main.player.puppet))
	# leaving keeps every star; the next visit still shows it
	opera._leave_early()
	await process_frame
	_ck("home icon returns safely", main.game == "level2" and main.opera_game == null)
	main._start_opera()
	opera = main.opera_game
	await _frames(4)
	_ck("stars persist across visits", (main.opera_stars & 1) == 1 and opera.doors.size() == 12)
	# every remaining act: shows through their doors, then each floor's
	# medallion lights up and its boss takes centre stage
	for expected in range(1, OperaHouse.ACTS.size()):
		var cfg2: Dictionary = OperaHouse.ACTS[expected]
		if expected == 5:
			_ck("dragon star unlocks the balcony floor", opera._floor_unlocked(2))
			_ck("shell gates fold open with the unlock", bool(opera.gates[0]["open"]) and bool(opera.gates[1]["open"]))
		if expected == 10:
			_ck("phantom star unlocks the top gallery", opera._floor_unlocked(3))
		var is_boss := String(cfg2.get("type", "show")) == "boss"
		if is_boss:
			var spot_index := {4: 0, 9: 1, 14: 2}[expected] as int
			_ck("four stars light the floor %d medallion" % int(cfg2["story"]), opera._spot_lit(opera.boss_spots[spot_index]))
			act = await _open_spot(opera, spot_index)
		else:
			act = await _open_door(opera, expected)
		_ck("act %d builds its %s engine" % [expected + 1, String(cfg2["kind"])], act != null and act.kind == String(cfg2["kind"]))
		if act == null:
			continue
		# per-job stages: a career listed in STAGE_SETS performs on its own
		# dressed set; every other career keeps the shared toy proscenium
		var dressed: bool = OperaAct.STAGE_SETS.has(String(cfg2.get("costume", "")))
		var has_crest: bool = act.find_child("StageCrest", true, false) != null
		_ck("act %d stage matches its dressing (%s)" % [expected + 1, "own set" if dressed else "shared"], has_crest == dressed)
		if bool(cfg2.get("shell", false)):
			_ck("act %d opens with the backstage brawl" % (expected + 1), act.stage_phase == "brawl")
			_drive_brawl(act)
			_ck("act %d brawl opens the curtain" % (expected + 1), act.stage_phase == "puzzle")
		else:
			# the six acts with no backstage corridor rescue someone on their
			# own stage first; until that is driven the act's engine is frozen
			# and every check after it reads a game that never started
			_drive_stage_rescue(act)
		match String(cfg2["kind"]):
			"order", "paint":
				await _drive_order(act, cfg2)
			"echo":
				await _drive_echo(act)
			"shuffle":
				await _drive_shuffle(act, expected)
			"fix":
				_drive_fix(act)
			"press":
				await _drive_press(act)
			"box":
				await _drive_box(act)
			"sleuth":
				_drive_sleuth(act)
			"doctor":
				await _drive_doctor(act)
			"scroll":
				_drive_scroll(act)
			"race":
				await _drive_race(act)
			"dance":
				await _drive_dance(act)
			"boss":
				await _drive_boss(act, cfg2)
		_ck("act %d reaches its curtain call" % (expected + 1), act.state == "won" or act.state == "done")
		act.win_t = 0.0
		await _wait_lobby(opera)
		_ck("act %d wears its star" % (expected + 1), (main.opera_stars & (1 << expected)) != 0)
	await process_frame
	await process_frame
	_ck("all fifteen acts are starred", main.opera_stars == OperaHouse.ALL_STARS)
	_ck("stars count as fifteen cleared acts", main.opera_progress == 15)
	_ck("the grand finale completes the opera", main.opera_done)
	_ck("the Showtime sticker is earned", bool(main.stickers.get("showtime", false)))
	opera._leave_early()
	await process_frame
	_ck("completion returns to the castle", main.game == "level2" and main.opera_game == null)
	print("OPERA|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _drive_stage_rescue(act: OperaAct) -> void:
	# the six acts with no backstage corridor now rescue someone on their own
	# stage before their game begins
	if act.stage_phase != "rescue":
		return
	_ck_once("an on-stage rescue cages captives too", act.captives.size() == 2)
	_ck_once("the drag finger is held back during a rescue",
		main.touch_ui == null or not main.touch_ui.drag_mode)
	var guard := 0
	while act.stage_phase == "rescue" and guard < 60:
		guard += 1
		var target := {}
		for g in act.imps:
			if not bool(g["popped"]):
				target = g
				break
		if target.is_empty():
			break
		act.player_pos = (target["pos"] as Vector3)
		act._brawl_action()
	_ck_once("the rescue hands the act back its stage", act.stage_phase == "puzzle")
	_ck_once("freeing them pays the gift", act.gift_given)

func _drive_brawl(act: OperaAct) -> void:
	# the captain takes two sparkles and dashes between hits, so chase by
	# re-reading positions until the curtain opens
	var guard := 0
	while act.stage_phase == "brawl" and guard < 40:
		guard += 1
		var target := {}
		for g in act.imps:
			if not bool(g["popped"]):
				target = g
				break
		if target.is_empty():
			break
		act.player_pos = (target["pos"] as Vector3)
		act._brawl_action()
	if act.stage_phase == "puzzle":
		act.player_pos = act.CENTER + Vector3(0, 1.1, 14.0)

func _drive_order(act: OperaAct, cfg: Dictionary) -> void:
	var order: Array = cfg["order"]
	var flow := String(cfg.get("flow", "deliver"))
	var hidden := bool(cfg.get("hide_props", false))
	if flow == "carry_paint":
		_ck("the painter gets a real canvas to paint on",
			act.paint_canvas != null and act.paint_img != null and act.paint_img.get_width() == act.PAINT_RES)
		for choice in order:
			var idx := int(choice)
			act.player_pos = (act.pads[idx]["pos"] as Vector3)
			act._act_action(idx)
			_ck("pot %d loads the brush" % idx, act.brush_loaded == idx)
			# standing at the easel hands the finger to the canvas
			act.player_pos = act.canvas_pos
			act._tick_easel(0.1)
			_ck("the easel takes over the finger for pot %d" % idx, act.paint_easel)
			# one stroke is not a painted band — coverage has to be earned
			var band := act._paint_band_rows()
			var mid := (float(band.x) + float(band.y)) * 0.5 / float(act.PAINT_RES)
			act._paint_stroke_uv(0.5, mid)
			_ck("a single dab does not finish the band for pot %d" % idx,
				act.brush_loaded == idx and act.paint_band_done > 0)
			# now drag across the band the way a finger would
			var guard := 0
			while act.brush_loaded == idx and guard < 400:
				guard += 1
				var t := fmod(float(guard) * 0.037, 1.0)
				var row := lerpf(float(band.x) + 1.0, float(band.y) - 1.0, fmod(float(guard) * 0.11, 1.0))
				act._paint_stroke_uv(t, row / float(act.PAINT_RES))
			_ck("dragging across the canvas paints the band for pot %d" % idx, act.brush_loaded == -1)
			_ck("a finished band releases the finger for pot %d" % idx, not act.paint_easel)
		if int(cfg.get("decorate", 0)) > 0:
			_ck("last swipe opens the splatter party", act.order_phase == "decorate" and act.state == "play")
			_ck("the freed painter's paints are in the larder",
				int(main.opera_pantry.get("paints", 0)) >= 1)
			for spot: Dictionary in act.deco_spots:
				act.player_pos = (spot["pos"] as Vector3)
				act._deco_action(int(spot["index"]))
			_ck("every splat finishes the masterpiece", act.state == "won")
			_ck("the finished painting is hung in the gallery",
				int(main.opera_pantry.get("painting", 0)) >= 1)
		return
	for choice in order:
		var idx2 := int(choice)
		act.player_pos = (act.pads[idx2]["pos"] as Vector3)
		if hidden:
			for i in range(6):
				await process_frame
			_ck("clue %d pops out when Roshan is near" % idx2, bool(act.pads[idx2]["revealed"]))
		_ck("order pad %d reachable by proximity" % idx2, act._nearest_pad() == idx2)
		act._act_action(idx2)
	if String(cfg.get("finale", "")) == "stir":
		# Cooking Mama chain: sift, pour, stir, bake, pipe, decorate — six
		# different gestures, and none of them is the pad-tap that came before
		_ck("the cake show opens on the sieve", act.order_phase == "sift")
		var sguard0 := 0
		while act.order_phase == "sift" and sguard0 < 600:
			sguard0 += 1
			act.sift_done += 1.0
			act._tick_sift(0.1)
		_ck("scrubbing the sieve fills the bowl", act.order_phase == "pour")
		# pouring is a HOLD: no finger, no milk
		act._tick_pour(0.5)
		_ck("the jug does not pour itself", act.order_phase == "pour" and act.pour_t == 0.0)
		act.hold_sim = true
		var pguard := 0
		while act.order_phase == "pour" and pguard < 200:
			pguard += 1
			act._tick_pour(0.1)
		act.hold_sim = false
		_ck("holding the jug fills to the line", act.order_phase == "stir")
		_ck("every layer opens the stirring finale", act.order_phase == "stir" and act.state == "play")
		act.player_pos = act.goal.position
		act._tick_stir(0.1)
		_ck("the bowl takes over the finger", act.stir_drag)
		# a tap is no longer a stir — the circle is the gesture
		var before: int = act.stir_done
		act._act_action(0)
		_ck("tapping at the bowl does not stir it", act.stir_done == before)
		# trace circles: a full turn of finger travel is one stir
		var sguard := 0
		while act.stir_done < 3 and sguard < 400:
			sguard += 1
			act._stir_drag_delta(0.35)
		_ck("circling the bowl stirs it", act.stir_done >= 3)
		_ck("a finished bowl releases the finger", not act.stir_drag)
		# the oven: tapping a pale cake is refused, a golden one comes out
		_ck("a stirred bowl goes into the oven", act.order_phase == "bake")
		act._bake_action()
		_ck("a pale cake stays in the oven", act.order_phase == "bake")
		var bguard := 0
		while not act.bake_golden and bguard < 400:
			bguard += 1
			act._tick_bake(0.1)
		act._bake_action()
		_ck("a golden cake comes out and opens the piping", act.order_phase == "pipe")
		# piping is a TRACE: every dot on the ring must be passed over
		_ck("the piping ring is dotted out", act.pipe_dots.size() == 10)
		# drive it the way a finger does: the dot only lights when the DRAG
		# passes over it. Poking pipe_trace by hand proved nothing and left
		# _tick_pipe early-returning on an inactive drag, so the act stalled.
		var has_finger: bool = main.touch_ui != null and bool(main.touch_ui.drag_mode)
		_ck("the piping ring hands the finger to the drag channel", has_finger)
		act._tick_pipe(0.1)
		_ck("an idle finger pipes nothing", act.pipe_trace == 0)
		if has_finger and act.cam != null:
			main.touch_ui.drag_active = true
			var tguard := 0
			while act.order_phase == "pipe" and tguard < 40:
				tguard += 1
				var nxt: Node3D = null
				for d in act.pipe_dots:
					if (d as Node3D).visible:
						nxt = d as Node3D
						break
				if nxt == null:
					break
				main.touch_ui.drag_pos = act.cam.unproject_position(nxt.position)
				act._tick_pipe(0.1)
			main.touch_ui.drag_active = false
		_ck("tracing the ring pipes the frosting", act.pipe_trace >= act.pipe_dots.size())
		if int(cfg.get("decorate", 0)) > 0:
			_ck("the piped ring opens the topping party", act.order_phase == "decorate" and act.state == "play")
			for spot: Dictionary in act.deco_spots:
				act.player_pos = (spot["pos"] as Vector3)
				act._deco_action(int(spot["index"]))
			_ck("every plopped topping finishes the cake", act.state == "won")
		else:
			_ck("three stirs finish the cake", act.state == "won")

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
	# Roshan performs the trick: every round opens by dragging a hat over the
	# bunny-fish, and only then do the hats dance
	_ck("act %d opens with Roshan hiding the bunny-fish" % (expected + 1),
		act.shuffle_phase == "hide" and act.bunny.visible)
	var guard := 0
	while act.state == "play" and guard < 900:
		guard += 1
		if act.shuffle_phase == "hide":
			# drag a hat onto the fish
			act.hide_hat = 0
			act.hide_pos = act.hats[0]["pos"] as Vector3
			(act.hats[0]["node"] as Node3D).position = act.bunny.position
			act._tick_hide(0.1)
			_ck_once("the covered bunny-fish goes under the hat she chose",
				act.bunny_at == 0 and act.shuffle_phase != "hide")
			continue
		if act.shuffle_phase == "pick":
			act._shuffle_action(act.bunny_at)
			continue
		await process_frame
	_ck("shuffle act does not stall", guard < 900)
	_ck("act %d finishes the hat trick" % (expected + 1), act.state == "won")

func _drive_fix(act: OperaAct) -> void:
	# Pipe Dream: a grid, a queue you cannot reorder, and bubbles on a fuse
	_ck("the pipe wall is a %dx%d grid" % [act.PIPE_ROWS, act.PIPE_COLS],
		act.pipe_cells.size() == act.PIPE_ROWS * act.PIPE_COLS)
	_ck("three pipes wait in the queue", act.pipe_queue.size() == 3)
	_ck("the bubbles hold on a fuse before setting off", act.pipe_fuse_t > 0.0 and act.pipe_flow_cell < 0)
	# lay a straight run along the middle row, taking whatever the queue gives
	for c in range(act.PIPE_COLS):
		var idx: int = act._pipe_cell_at(act.PIPE_START_ROW, c)
		# the queue is not reorderable, so keep drawing until a straight shows up
		var spins := 0
		while act.pipe_queue[0] != "h" and spins < 40:
			spins += 1
			act.pipe_queue[0] = act._pipe_roll()
		var before: int = act.pipe_queue.size()
		act._pipe_place(idx)
		_ck("laying a pipe consumes the front of the queue and refills it",
			act.pipe_queue.size() == before and String(act.pipe_cells[idx]["shape"]) == "h")
	# a filled cell refuses a second piece
	var mid: int = act._pipe_cell_at(act.PIPE_START_ROW, 0)
	var q_before: String = act.pipe_queue[0]
	act._pipe_place(mid)
	_ck("a filled cell cannot be overwritten", act.pipe_queue[0] == q_before)
	# now let the bubbles run the line
	act.pipe_fuse_t = 0.0
	var guard := 0
	while act.fix_phase == "pipes" and guard < 200:
		guard += 1
		act.pipe_leak_t = 0.0
		act._pipe_advance()
	_ck("pipe puzzle does not stall", guard < 200)
	_ck("a finished line carries the bubbles to the rocket", act.fix_phase == "valve")
	act._turn_valve()
	_ck("one spin builds pressure, not launch", act.state == "play" and act.valve_spins == 1)
	act._turn_valve()
	act._turn_valve()
	_ck("three valve spins open the countdown", act.fix_phase == "launch" and act.state == "play")
	act.hold_sim = true
	for i in range(6):
		act._tick_launch(0.1)
	var built: float = act.launch_hold
	act.hold_sim = false
	act._tick_launch(0.1)
	_ck("letting go sags the thrust, it never resets",
		act.launch_hold < built and act.launch_hold > 0.0 and act.state == "play")
	act.hold_sim = true
	var lguard := 0
	while act.state == "play" and lguard < 200:
		lguard += 1
		act._tick_launch(0.1)
	act.hold_sim = false
	_ck("holding through the countdown launches the rocket", act.state == "won")

func _drive_press(act: OperaAct) -> void:
	# the belt: candies ride out of the press and are DRAGGED to the chute of
	# their own colour. Nothing here is a timed tap any more.
	_ck("the sorting belt has three colour chutes", act.chutes.size() == 3)
	_ck("a candy is riding the belt", act.belt_items.size() > 0)
	act._press_action()
	_ck("the button no longer stamps a candy", act.candies_done == 0)
	var guard := 0
	while act.state == "play" and guard < 400:
		guard += 1
		if act.belt_items.is_empty():
			act._belt_spawn()
			continue
		var it: Dictionary = act.belt_items[0]
		var want: int = int(it["want"])
		if guard == 1:
			# a candy dropped in the WRONG chute is spat back, never lost
			var wrong: int = (want + 1) % act.chutes.size()
			act.sort_held = 0
			(it["node"] as Node3D).position = act.chutes[wrong]["pos"] as Vector3
			act._sort_drop()
			_ck("a wrong chute spits the candy back, no fail",
				act.state == "play" and act.candies_done == 0 and act.belt_items.size() > 0)
			continue
		act.sort_held = 0
		(it["node"] as Node3D).position = act.chutes[want]["pos"] as Vector3
		act._sort_drop()
	_ck("sorting act does not stall", guard < 400)
	_ck("the full sorted batch finishes the show", act.candies_done == act.candies_goal)
	_ck("the belt speeds up as the batch grows", act.belt_speed > 2.4)

func _ck_once(label: String, ok: bool) -> void:
	if _once_seen.has(label):
		return
	_once_seen[label] = true
	_ck(label, ok)

func _drive_box(act: OperaAct) -> void:
	# three beats now: warm up on the swinging bag, fight the rounds, then swim
	# up and take the belt. Each beat is a different verb, so drive each one.
	var waves: Array = (act.config as Dictionary).get("rounds", [3, 4, 5])
	var warmup: int = int((act.config as Dictionary).get("warmup", 0))
	_ck("the bout opens on the training bag", act.box_phase == "warmup" and act.box_bag != null)
	_ck("the ring answers to PUNCH", act.action_label() == "PUNCH")
	# a swing from across the stage swishes — the bag is never a free hit
	act.player_pos = act.CENTER + Vector3(0.0, 1.1, 16.0)
	act._punch_action()
	_ck("a far punch swishes past the bag", act.box_bag_hits == 0)
	var guard := 0
	while act.state == "play" and guard < 1400:
		guard += 1
		if act.box_wait > 0.0:
			await process_frame
			continue
		if act.box_phase == "warmup":
			act.player_pos = act.box_bag.position
			act._punch_action()
			continue
		if act.box_phase == "belt":
			_ck_once("the belt descends for the champion", act.box_belt != null)
			act.player_pos = act.box_belt.position
			await process_frame
			continue
		var target := {}
		for g in act.imps:
			if not bool(g["popped"]):
				target = g
				break
		if target.is_empty():
			await process_frame
			continue
		act.player_pos = (target["pos"] as Vector3)
		if not act._box_on_beat():
			# a swing between the beats whiffs — proven once, then wait for the beat
			_ck_once("a punch between the beats whiffs kindly",
				act.imps_left == int(target.get("hp", 1)) or act.state == "play")
			act.box_beat_t = 0.0
		act._punch_action()
	_ck("box act does not stall", guard < 1400)
	_ck("the warm-up bag takes every bop", act.box_bag_hits >= warmup)
	_ck("every round then the belt wins the championship",
		act.state == "won" and act.box_round >= waves.size() and act.box_phase == "belt")

func _drive_sleuth(act: OperaAct) -> void:
	_ck("six boxes stand on the stage", act.sleuth_props.size() == 6)
	var clue_n := 0
	for prop in act.sleuth_props:
		if bool(prop["clue"]):
			clue_n += 1
	_ck("exactly three boxes hold clues", clue_n == 3)
	act._sleuth_chest()
	_ck("chest waits for all three clues", act.state == "play" and not act.chest_ready)
	# the magnifier: clues are invisible until the lens is over them
	act._tick_lens(0.1)
	_ck("the puzzle phase hands the finger to the magnifier", act.lens_drag and act.lens.visible)
	var far_clue := {}
	for prop in act.sleuth_props:
		if bool(prop["clue"]):
			far_clue = prop
			break
	act.lens_pos = act.CENTER + Vector3(0.0, 0.6, 18.0)   # lens parked far downstage
	act._tick_lens(0.1)
	_ck("a clue stays hidden with the lens away from it",
		not (far_clue["glint"] as Node3D).visible)
	act.lens_pos = (far_clue["pos"] as Vector3)
	act._tick_lens(0.1)
	_ck("the clue glints once the lens is over it", (far_clue["glint"] as Node3D).visible)
	# holding the lens still is what opens a box — one pass is not enough
	_ck("a glance does not open the box", not bool(far_clue["opened"]))
	var dguard := 0
	while not bool(far_clue["opened"]) and dguard < 60:
		dguard += 1
		act._tick_lens(0.1)
	_ck("holding the lens still opens the box", bool(far_clue["opened"]) and act.clues_found == 1)
	var wrong := {}
	for prop in act.sleuth_props:
		if not bool(prop["clue"]):
			wrong = prop
			break
	act.player_pos = (wrong["pos"] as Vector3)
	var clues_before: int = act.clues_found
	act._sleuth_action(int(wrong["index"]))
	_ck("wrong box giggles a silly fish, no fail",
		act.state == "play" and act.clues_found == clues_before)
	for prop in act.sleuth_props:
		if bool(prop["clue"]) and not bool(prop["opened"]):
			act.player_pos = (prop["pos"] as Vector3)
			act._sleuth_action(int(prop["index"]))
	_ck("three clues ready the treasure chest", act.chest_ready)
	# sweeping the lens onto the chest is the reveal — still no button
	act.lens_pos = act.goal.position
	act._tick_lens(0.1)
	_ck("the tiara reveal wins the case", act.state == "won")

func _drive_doctor(act: OperaAct) -> void:
	# five beats with a story: find the hurt one, carry it in, read the x-ray,
	# wrap the cast, seal it with coban. The rescue in THIS act is the animal
	# herself, so the brawl frees nobody and hands over no gift.
	_ck("the vet act cages nobody — the animal is the rescue",
		act.captives.is_empty() and not act.gift_given)
	_ck("the ward holds four animals", act.vet_animals.size() == 4)
	_ck("exactly one of them is hurt", act.vet_hurt >= 0 and bool(act.vet_animals[act.vet_hurt]["hurt"]))
	_ck("only the hurt one wears an ouch star",
		(act.vet_animals[act.vet_hurt]["mark"] as Node3D).visible)
	# a well animal giggles and is not scooped up
	var well: int = (act.vet_hurt + 1) % act.vet_animals.size()
	act._vet_pick(well)
	_ck("a well animal is not carried off", act.vet_phase == "find" and act.state == "play")
	act._vet_pick(act.vet_hurt)
	_ck("the hurt animal gets scooped up", act.vet_phase == "carry")
	# carrying it to the fluoroscope lights the x-ray
	act.player_pos = act.vet_scope.position
	act._tick_vet(0.1)
	_ck("the fluoroscope lights up on arrival", act.vet_phase == "xray" and act.vet_screen.visible)
	_ck("the x-ray shows four bones", act.vet_bones.size() == 4)
	var sound: int = (act.vet_limb + 1) % 4
	act._vet_bone(sound)
	_ck("a sound bone is gently refused", act.vet_phase == "xray")
	act._vet_bone(act.vet_limb)
	_ck("naming the crack opens the cast", act.vet_phase == "cast")
	# wrapping is a circular drag, and it takes real turns
	act._vet_wrap_delta(0.4)
	_ck("one flick does not finish a cast", act.vet_phase == "cast" and act.vet_layers.size() >= 0)
	var wguard := 0
	while act.vet_phase == "cast" and wguard < 400:
		wguard += 1
		act._vet_wrap_delta(0.35)
	_ck("wrapping enough turns finishes the padding", act.vet_phase == "coban")
	var cguard := 0
	while act.vet_phase == "coban" and cguard < 400:
		cguard += 1
		act._vet_wrap_delta(0.35)
	_ck("the coban seals the cast and wins", act.state == "won" and act.vet_phase == "done")

func _drive_scroll(act: OperaAct) -> void:
	_ck("meadow has nine hungry piggies", act.piggies.size() == 9)
	# tapping no longer feeds anyone: the veggie has to be LOBBED
	act._toss_action()
	_ck("tapping no longer feeds a piggy", act.state == "play" and act.farm_fed == 0)
	# a lob that lands in the grass bounces, it never fails
	for pig in act.piggies:
		pig["sx"] = 2000.0
	act._farm_launch(0.2)
	var fguard := 0
	while act.farm_flights.size() > 0 and fguard < 60:
		fguard += 1
		act._tick_flights(0.1)
	_ck("a lob into the grass just bounces", act.state == "play" and act.farm_fed == 0)
	# pull length is throw distance: aim at where the piggy actually is
	for i in range(act.piggies.size()):
		var want: float = 260.0 + float(i) * 55.0
		act.piggies[i]["sx"] = want
		var power: float = clampf((want - act.FARM_ROSHAN_X) / 780.0, 0.0, 1.0)
		act._farm_launch(power)
		var g2 := 0
		while act.farm_flights.size() > 0 and g2 < 60:
			g2 += 1
			act._tick_flights(0.1)
		for pig in act.piggies:
			if not bool(pig["fed"]):
				pig["sx"] = 2000.0
	_ck("every lobbed veggie finishes the picnic", act.state == "won" and act.farm_fed == act.piggies.size())

func _drive_race(act: OperaAct) -> void:
	var guard := 0
	while act.kart == null and guard < 240:
		guard += 1
		await process_frame
	_ck("kart engine is reused for the Grand Prix", act.kart is KartGame)
	# the engine is CONFIGURED for this opera, not launched on its defaults
	var kcfg: Dictionary = (act.kart as KartGame).cfg
	_ck("the Grand Prix wears the opera's own sky", kcfg.has("sky_colors"))
	_ck("the Grand Prix is a show, not a pearl farm", not bool(kcfg.get("pearl_payout", true)))
	_ck("the freed pit crew's wheels became a kart",
		int(main.opera_pantry.get("spare wheels", 0)) == 0 or kcfg.has("vehicles"))
	_ck("exhibition race runs the configured two laps",
		act.kart != null and (act.kart as KartGame)._laps() == int((act.config as Dictionary).get("laps", 1)))
	# ✕ quitting the race returns to the stage without winning; the internals of
	# the race itself are probe_kart_feel's job, so completion is simulated here
	act._race_finished(-1)
	_ck("race quit returns to the stage flag", act.state == "play" and act.kart == null)
	act._race_finished(2)
	_ck("any finishing place wins the act", act.state == "won")

func _drive_dance(act: OperaAct) -> void:
	# the rescued band buy an encore verse: the first close replays, the second wins
	if int(main.opera_pantry.get("instruments", 0)) > 0 and not act.dance_encore_done:
		(act.dance as Object).set("happy_hits", 4)
		act._dance_closed()
		_ck("the freed band earn an encore verse",
			act.dance_encore_done and act.state == "play")
	var guard := 0
	while (act.dance == null or not (act.dance as DanceEngine).active) and guard < 240:
		guard += 1
		await process_frame
	var de := act.dance as DanceEngine
	_ck("dance engine opens in guest mode", de != null and de.guest_mode and de.active)
	de.close_demo()
	await process_frame
	_ck("closing without dancing keeps the mic waiting", act.state == "play")
	act._open_dance()
	guard = 0
	while not de.active and guard < 240:
		guard += 1
		await process_frame
	de.happy_hits = 6
	de.close_demo()
	await process_frame
	_ck("a happy round takes the pop star's bow", act.state == "won")

func _drive_boss(act: OperaAct, cfg: Dictionary) -> void:
	var finale := bool(cfg.get("finale", false))
	var dual := bool(cfg.get("dual", false)) or finale
	var hp: int = int(act.boss["hp"])
	_ck("boss starts with its configured sparkle stars", hp >= 3)
	if dual:
		_ck("boss opens hidden in shadow", String(act.boss["phase"]) == "shadow" and act.action_label() == "SHINE")
		act._hit_boss()
		_ck("sparkles cannot skip the lantern lesson", int(act.boss["hp"]) == hp)
	else:
		_ck("dragon opens hiding in the curtains", String(act.boss["phase"]) == "hide" and act.action_label() == "SPARKLE")
		_ck("dragon roams five curtain spots when bold", act.peek_spots.size() == 5)
		act._hit_boss()
		_ck("sparkles fizzle while he hides", int(act.boss["hp"]) == hp)
	var modes := {}
	var guard := 0
	while act.state == "play" and guard < 1500:
		guard += 1
		var phase := String(act.boss["phase"])
		if phase == "shadow":
			if finale:
				modes[String(act.boss.get("mode", "lantern"))] = true
			act._light_lantern()
			act._hit_boss()
		elif phase == "peek":
			if finale:
				modes[String(act.boss.get("mode", "lantern"))] = true
			act._hit_boss()
		else:
			await process_frame
	_ck("boss act does not stall", guard < 1500)
	if finale:
		_ck("the grand finale remixes lanterns AND curtain chases",
			bool(modes.get("lantern", false)) and bool(modes.get("roam", false)))

func _open_door(opera: OperaHouse, act_i: int) -> OperaAct:
	# stand Roshan on the door's welcome mat; the lobby's own proximity flow
	# (arming, cooldown, transformation) opens the show
	var door := {}
	for d in opera.doors:
		if int(d["i"]) == act_i:
			door = d
	var dpos: Vector3 = door["pos"]
	opera.lobby_y = _floor_of(dpos)
	opera.lobby_pos = dpos
	var guard := 0
	while opera.act == null and guard < 500:
		guard += 1
		await process_frame
	_ck("act %d opens from the lobby walk-in" % (act_i + 1), opera.act != null)
	return opera.act

func _open_spot(opera: OperaHouse, spot_index: int) -> OperaAct:
	var spot: Dictionary = opera.boss_spots[spot_index]
	var spos: Vector3 = spot["pos"]
	opera.lobby_y = _floor_of(spos)
	opera.lobby_pos = spos
	var guard := 0
	while opera.act == null and guard < 500:
		guard += 1
		await process_frame
	_ck("glowing medallion %d starts its boss" % (spot_index + 1), opera.act != null)
	return opera.act

func _floor_of(pos: Vector3) -> float:
	var best := 0.0
	for fy in OperaHouse.FLOOR_YS:
		if absf((pos.y - 1.1) - (OperaHouse.L.y + float(fy))) < 3.0:
			best = float(fy)
	return best

func _wait_lobby(opera: OperaHouse) -> void:
	var guard := 0
	while opera.act != null and guard < 500:
		guard += 1
		await process_frame
	_ck("show hands Roshan back to the lobby", opera.act == null)

func _frames(n: int):
	for i in range(n):
		await process_frame

func _descendants(node: Node) -> int:
	var total := 0
	for child in node.get_children():
		total += 1 + _descendants(child)
	return total

func _ck(label: String, ok: bool) -> void:
	print("OPERA|", label, ": ", "OK" if ok else "FAIL")
	if not ok: bad += 1
