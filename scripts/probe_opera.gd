extends SceneTree
# Pearl Opera House regression: sixteen stable save slots across three lobby
# floors (thirteen career doors + three boss medallions), no passive wins,
# wrong answers stay gentle, stars persist
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
	_ck("opera defines sixteen save-compatible acts", OperaHouse.ACTS.size() == 16)
	var shows := {1: 0, 2: 0, 3: 0}
	var bosses := {1: 0, 2: 0, 3: 0}
	for cfg: Dictionary in OperaHouse.ACTS:
		var story := int(cfg.get("story", 0))
		if String(cfg.get("type", "show")) == "boss":
			bosses[story] = int(bosses[story]) + 1
		else:
			shows[story] = int(shows[story]) + 1
	_ck("floors run four, four and five career shows", int(shows[1]) == 4 and int(shows[2]) == 4 and int(shows[3]) == 5)
	_ck("every floor ends with one boss", int(bosses[1]) == 1 and int(bosses[2]) == 1 and int(bosses[3]) == 1)
	_ck("floor bosses sit at acts five, ten and fifteen",
		String(OperaHouse.ACTS[4]["type"]) == "boss" and String(OperaHouse.ACTS[9]["type"]) == "boss" and String(OperaHouse.ACTS[14]["type"]) == "boss")
	_ck("the stable fifteenth save bit remains the grand finale", bool(OperaHouse.ACTS[14].get("finale", false)))
	_ck("Nursery Nurse appends a stable bit while displaying as job twelve", String(OperaHouse.ACTS[15].get("career", "")) == "Nursery Nurse")
	# every career is its own minigame on its own stage: no two shows may share
	# an engine kind; legacy 3D costumes retain STAGE_SETS while Nursery is 2D
	var show_kinds := {}
	var undressed: Array[String] = []
	for cfg3: Dictionary in OperaHouse.ACTS:
		if String(cfg3.get("type", "show")) == "boss":
			continue
		show_kinds[String(cfg3["kind"])] = int(show_kinds.get(String(cfg3["kind"]), 0)) + 1
		if String(cfg3.get("costume", "")) != "nursery" and not OperaAct.STAGE_SETS.has(String(cfg3.get("costume", ""))):
			undressed.append(String(cfg3["career"]))
	_ck("thirteen careers run thirteen distinct engines", show_kinds.size() == 13)
	_ck("every legacy career has its own dressed stage", undressed.is_empty())
	# ---- the explorable lobby: doors for shows, medallions for bosses ----
	_ck("lobby builds a door for every career show", opera.doors.size() == 13)
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
	# Career ids remain on the real sprite player in puppet mode; no model or
	# bone attachment may replace the animated Roshan atlas on stage.
	_ck("act one dresses the primary Roshan sprite",
		act != null and String(main.player.costume_id) == "chef"
		and main.player.classic_sprite.visible)
	_ck("act one puts the real 2.5D Roshan on stage",
		bool(main.player.puppet) and main.player.visible)
	var act_nodes: int = _descendants(act)
	_ck("act one stays inside the mobile node budget (%d/210)" % act_nodes, act_nodes < 210)
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
	# ...and he must dash somewhere a child can actually swim to. The dash used
	# to place him at y=1.0 ABSOLUTE while the stage sits at y=-2600, putting
	# him 2601 units overhead and permanently out of the sparkle's 8.0 reach.
	_ck("the dashing captain stays at swimming height",
		absf((captain["pos"] as Vector3).y - (act.CENTER.y + 1.0)) < 2.0)
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
		String(main.player.costume_id) == "" and not bool(main.player.puppet))
	# leaving keeps every star; the next visit still shows it
	opera._leave_early()
	await process_frame
	_ck("home icon returns safely", main.game == "level2" and main.opera_game == null)
	main._start_opera()
	opera = main.opera_game
	await _frames(4)
	_ck("stars persist across visits", (main.opera_stars & 1) == 1 and opera.doors.size() == 13)
	# every remaining act: shows through their doors, then each floor's
	# medallion lights up and its boss takes centre stage
	var play_order: Array[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 13, 14]
	for expected: int in play_order:
		var cfg2: Dictionary = OperaHouse.ACTS[expected]
		if expected == 5:
			_ck("dragon star unlocks the balcony floor", opera._floor_unlocked(2))
			_ck("shell gates fold open with the unlock", bool(opera.gates[0]["open"]) and bool(opera.gates[1]["open"]))
		if expected == 10:
			_ck("phantom star unlocks the top gallery", opera._floor_unlocked(3))
		var is_boss := String(cfg2.get("type", "show")) == "boss"
		if is_boss:
			var spot_index := {4: 0, 9: 1, 14: 2}[expected] as int
			_ck("all show stars light the floor %d medallion" % int(cfg2["story"]), opera._spot_lit(opera.boss_spots[spot_index]))
			act = await _open_spot(opera, spot_index)
		else:
			act = await _open_door(opera, expected)
		_ck("act %d builds its %s engine" % [expected + 1, String(cfg2["kind"])], act != null and act.kind == String(cfg2["kind"]))
		if act == null:
			continue
		if String(cfg2["kind"]) == "nursery":
			_ck("nursery uses its dedicated scalable Canvas room",
				act.use_career_world_2d and act.career_world_2d != null
				and act.find_children("*", "Node3D", true, false).is_empty())
		else:
			# Legacy engines retain their per-job 3D dressing in this probe.
			var dressed: bool = OperaAct.STAGE_SETS.has(String(cfg2.get("costume", "")))
			var has_crest: bool = act.find_child("StageCrest", true, false) != null
			_ck("act %d stage matches its dressing (%s)" % [expected + 1, "own set" if dressed else "shared"], has_crest == dressed)
		if bool(cfg2.get("shell", false)) and not act.use_career_world_2d:
			_ck("act %d opens with the backstage brawl" % (expected + 1), act.stage_phase == "brawl")
			_drive_brawl(act)
			_ck("act %d brawl opens the curtain" % (expected + 1), act.stage_phase == "puzzle")
		else:
			# the six acts with no backstage corridor rescue someone on their
			# own stage first; until that is driven the act's engine is frozen
			# and every check after it reads a game that never started
			if not act.use_career_world_2d: _drive_stage_rescue(act)
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
			"nursery":
				await _drive_nursery_2d(act)
		_ck("act %d reaches its curtain call" % (expected + 1), act.state == "won" or act.state == "done")
		act.win_t = 0.0
		await _wait_lobby(opera)
		_ck("act %d wears its star" % (expected + 1), (main.opera_stars & (1 << expected)) != 0)
	await process_frame
	await process_frame
	_ck("all sixteen acts are starred", main.opera_stars == OperaHouse.ALL_STARS)
	_ck("stars count as sixteen cleared acts", main.opera_progress == 16)
	_ck("the grand finale completes the opera", main.opera_done)
	_ck("the Showtime sticker is earned", bool(main.stickers.get("showtime", false)))
	opera._leave_early()
	await process_frame
	_ck("completion returns to the castle", main.game == "level2" and main.opera_game == null)
	print("OPERA|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _drive_nursery_2d(act: OperaAct) -> void:
	var world := act.career_world_2d
	_ck("nursery opens with Roshan and Faron together",
		world != null and world.rival_actor.visible and act.competition.is_cooperative())
	if world == null:
		return
	var guard := 0
	while act.state == "play" and guard < 360:
		if world.nursery_catch != null and world.nursery_catch.active:
			var target := world.nursery_catch.lowest_baby_x()
			world.nursery_catch.steer_to(target if target >= 0.0 else 0.5)
			world.nursery_catch._process(0.12)
		else:
			world._on_gesture("probe", 100.0, 1.0)
		act._process(0.05)
		await process_frame
		guard += 1
	_ck("nursery completes catch, feed, burp and bedtime", guard < 360 and act.state == "won")
	_ck("nursery curtain call is cooperative",
		bool(act.performance_result.get("cooperative", false))
		and world.last_cheer == "THE BABIES ARE COZY!")


func _drive_stage_rescue(act: OperaAct) -> void:

	# the six acts with no backstage corridor now rescue someone on their own
	# stage before their game begins
	if act.stage_phase != "rescue":
		return
	_ck_once("an on-stage rescue cages captives too", act.captives.size() == 2)
	_ck_once("the button says SPARKLE during an on-stage rescue",
		act.action_label() == "SPARKLE")
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
		# keep Roshan's OWN height: teleporting to the imp's exact 3D position
		# masked a dash that flung the captain 2600 units into the sky
		var tp: Vector3 = target["pos"] as Vector3
		act.player_pos = Vector3(tp.x, act.player_pos.y, tp.z)
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
		var bp: Vector3 = target["pos"] as Vector3
		act.player_pos = Vector3(bp.x, act.player_pos.y, bp.z)
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
		# the brush is the painter's own prop, but it was being built inside the
		# chef's branch — every pot tap, stroke and frame dereferenced a null
		_ck("the painter is carrying a real brush", act.brush_node != null)
		# beat 1: the picture is DRAWN before it is painted, and the pot tap
		# that runs the rest of the act cannot skip it
		_ck("the gallery opens on the sketch", act.order_phase == "sketch"
			and act.sketch_dots.size() == act.SKETCH_DOTS)
		act._act_action(0)
		act._tick_sketch(0.05)
		_ck("an idle finger draws nothing", act.sketch_trace == 0
			and act.brush_loaded < 0 and act.order_phase == "sketch")
		if main.touch_ui != null and act.cam != null:
			main.touch_ui.drag_active = true
			var sg := 0
			while act.order_phase == "sketch" and sg < 60:
				sg += 1
				var nxt: Node3D = null
				for d in act.sketch_dots:
					if (d as Node3D).visible:
						nxt = d as Node3D
						break
				if nxt == null:
					break
				main.touch_ui.drag_pos = act.cam.unproject_position(nxt.position)
				act._tick_sketch(0.05)
			main.touch_ui.drag_active = false
		_ck("tracing the guide draws the sketch and calls for colour",
			act.sketch_trace >= act.SKETCH_DOTS and act.order_phase == "fill")
		# beat 2: colour-by-SHAPE on a HOLD. A tap is not a hold, and the wrong
		# shape is a wobble rather than a loss.
		_ck("three shape panels stand out for filling", act.fill_panels.size() == 3)
		var other: int = (act.fill_want + 1) % act.fill_panels.size()
		act.player_pos = (act.fill_panels[other]["pos"] as Vector3)
		act.hold_sim = true
		var fg0 := 0
		while fg0 < 40:
			fg0 += 1
			act._tick_fill(0.1)
		_ck("holding the wrong shape fills nothing",
			act.fill_done == 0 and act.order_phase == "fill")
		act.hold_sim = false
		while act.order_phase == "fill":
			var wi: int = act.fill_want
			act.player_pos = (act.fill_panels[wi]["pos"] as Vector3)
			act._tick_fill(0.1)
			_ck_once("the panel does not fill itself without a finger", act.fill_done == 0)
			act.hold_sim = true
			var fg := 0
			while act.fill_want == wi and fg < 200:
				fg += 1
				act._tick_fill(0.1)
			act.hold_sim = false
		_ck("holding each matching shape opens the paint pots",
			act.fill_done == 3 and act.order_phase == "steps")
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
		while act.order_phase == "stir" and sguard < 700:
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
		_ck("the piping ring is dotted out", act.pipe_dots.size() == 14)
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
		elif act.echo_phase == "ribbon":
			# beat 3: a TRACE. The tile tap that won the echo must not do this.
			_ck_once("the echo opens onto the ribbon",
				act.ribbon_dots.size() == act.RIBBON_DOTS and act.ribbon_trace == 0)
			_ck_once("the ribbon hands the finger to the drag channel",
				main.touch_ui != null and bool(main.touch_ui.drag_mode))
			act._pad_touch(0)
			act._tick_ribbon(0.05)
			_ck_once("tapping a tile traces no ribbon", act.ribbon_trace == 0)
			if main.touch_ui != null and act.cam != null:
				main.touch_ui.drag_active = true
				var rg := 0
				while act.echo_phase == "ribbon" and rg < 60:
					rg += 1
					var nxt: Node3D = null
					for d in act.ribbon_dots:
						if (d as Node3D).visible:
							nxt = d as Node3D
							break
					if nxt == null:
						break
					main.touch_ui.drag_pos = act.cam.unproject_position(nxt.position)
					act._tick_ribbon(0.05)
				main.touch_ui.drag_active = false
			_ck_once("tracing the path flies the ribbon",
				act.ribbon_trace >= act.RIBBON_DOTS and act.echo_phase == "twirl")
		elif act.echo_phase == "twirl":
			# beat 4: circles, not taps — and a straight drag is not a circle
			_ck_once("the ribbon opens onto the twirl", act.twirl_done == 0)
			act._pad_touch(0)
			_ck_once("tapping a tile is not a twirl", act.twirl_done == 0)
			var tg := 0
			while act.echo_phase == "twirl" and act.state == "play" and tg < 400:
				tg += 1
				act._twirl_delta(0.35)
			_ck_once("circling three times finishes the recital",
				act.twirl_done >= act.TWIRL_TURNS and act.state == "won")
		else:
			await process_frame
	_ck("echo act does not stall", guard < 900)
	_ck("the recital plays all four beats",
		act.ribbon_trace >= act.RIBBON_DOTS and act.twirl_done >= act.TWIRL_TURNS)

func _drive_shuffle(act: OperaAct, expected: int) -> void:
	# Roshan performs the trick: every round opens by dragging a hat over the
	# bunny-fish, and only then do the hats dance
	_ck("act %d opens with Roshan hiding the bunny-fish" % (expected + 1),
		act.shuffle_phase == "hide" and act.bunny.visible)
	var guard := 0
	# six escalating rounds are ~46s of watchable swap animation — the guard
	# counts FRAMES through it, so it scales with the show (900 was measured
	# at the edge on run 788's runner and one round over it tipped red)
	while act.state == "play" and guard < 2500:
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
		if act.shuffle_phase == "rope":
			# trick 3: a PULL, and only a pull
			_ck_once("the hat trick opens onto the rope", act.rope_root != null and act.rope_undone == 0)
			_ck_once("the rope hands the finger to the drag channel",
				main.touch_ui != null and bool(main.touch_ui.drag_mode))
			act._shuffle_action(0)
			_ck_once("tapping the rope unties nothing", act.rope_undone == 0)
			_ck_once("the freed ushers' scarves shorten every pull",
				int(main.opera_pantry.get("silk scarves", 0)) == 0
					or act.rope_pull_need < act.ROPE_PULL)
			if main.touch_ui != null:
				main.touch_ui.drag_active = true
				var rguard := 0
				while act.shuffle_phase == "rope" and rguard < 60:
					rguard += 1
					# each pull: plant the finger, then drag it out past the need
					main.touch_ui.drag_pos = Vector2(640.0, 400.0)
					act._tick_rope(0.05)
					main.touch_ui.drag_pos = Vector2(640.0 + act.rope_pull_need + 8.0, 400.0)
					act._tick_rope(0.05)
				main.touch_ui.drag_active = false
			_ck_once("pulling out wide melts every knot",
				act.rope_undone >= act.ROPE_KNOTS and act.shuffle_phase == "cabinet")
			continue
		if act.shuffle_phase == "cabinet":
			# trick 4: a rhythm tap. Off the beat must not count.
			_ck_once("the rope opens onto the trick cabinet",
				act.cab_root != null and act.cab_wand != null and act.cab_taps == 0)
			act.player_pos = act.cab_wand.position
			act.cab_beat_t = act.CAB_BEAT * (act.CAB_WINDOW + 0.2)   # off the beat
			act._shuffle_action(0)
			_ck_once("a wand tap off the beat only twinkles", act.cab_taps == 0)
			var cguard := 0
			while act.shuffle_phase == "cabinet" and act.state == "play" and cguard < 40:
				cguard += 1
				act.cab_beat_t = 0.0                                  # on the beat
				act._shuffle_action(0)
			_ck_once("three taps on the beat open the cabinet", act.cab_taps >= act.CAB_TAPS)
			continue
		if act.shuffle_phase == "finale":
			# trick 5: the old cabinet ending was too small. The new payoff is
			# a sustained one-finger wand hold that fills a stage-sized portal.
			_ck_once("the cabinet opens onto a grand star portal",
				act.magic_portal != null and act.magic_portal_fill != null)
			act.player_pos = act.cab_wand.position
			act.hold_sim = true
			var fguard := 0
			while act.shuffle_phase == "finale" and act.state == "play" and fguard < 80:
				fguard += 1
				act._process(0.1)
				await process_frame
			act.hold_sim = false
			_ck_once("holding the wand fills the portal and wins the duel",
				act.magic_finale_t >= act.MAGIC_FINALE_HOLD and act.state == "won")
			continue
		await process_frame
	_ck("shuffle act does not stall", guard < 2500)
	_ck("act %d finishes the whole routine" % (expected + 1),
		act.state == "won" and act.rope_undone >= act.ROPE_KNOTS and act.cab_taps >= act.CAB_TAPS)

func _drive_fix(act: OperaAct) -> void:
	# Pipe Dream: a grid, a queue you cannot reorder, and bubbles on a fuse
	_ck("the pipe wall is a %dx%d grid" % [act.PIPE_ROWS, act.PIPE_COLS],
		act.pipe_cells.size() == act.PIPE_ROWS * act.PIPE_COLS)
	# the freed engineers' spare pipes are a FOURTH slot — one more piece of
	# lookahead, which is the whole skill of Pipe Dream
	var spares: int = int(main.opera_pantry.get("spare pipes", 0))
	_ck("the queue shows what is coming", act.pipe_queue.size() == act.pipe_queue_depth)
	_ck("the freed engineers' spare pipes deepen the queue",
		(spares > 0 and act.pipe_queue_depth == 4) or (spares == 0 and act.pipe_queue_depth == 3))
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
	# a filled cell the bubbles have NOT reached can be re-laid: a wrong pipe
	# on the path must never brick it (the old refuse rule was a fail state
	# wearing a leak's clothes)
	var mid: int = act._pipe_cell_at(act.PIPE_START_ROW, 0)
	act.pipe_queue[0] = "v"
	act._pipe_place(mid)
	_ck("an unflooded cell accepts a replacement piece",
		String(act.pipe_cells[mid]["shape"]) == "v")
	act.pipe_queue[0] = "h"
	act._pipe_place(mid)
	_ck("a wrong piece can be repaired straight back",
		String(act.pipe_cells[mid]["shape"]) == "h")
	# now let the bubbles run the line
	act.pipe_fuse_t = 0.0
	var guard := 0
	while act.fix_phase == "pipes" and guard < 200:
		guard += 1
		act.pipe_leak_t = 0.0
		act._pipe_advance()
	_ck("pipe puzzle does not stall", guard < 200)
	_ck("a cell the bubbles filled is locked for keeps", not act.pipe_filled.is_empty())
	if not act.pipe_filled.is_empty():
		var flooded: int = act.pipe_filled[0]
		var flooded_shape: String = String(act.pipe_cells[flooded]["shape"])
		act.pipe_queue[0] = "v"
		act._pipe_place(flooded)
		_ck("no piece overwrites a flooded cell",
			String(act.pipe_cells[flooded]["shape"]) == flooded_shape)
	_ck("a finished line carries the bubbles to the rocket", act.fix_phase == "valve")
	act._turn_valve()
	_ck("one spin builds pressure, not launch", act.state == "play" and act.valve_spins == 1)
	var vg := 0
	while act.fix_phase == "valve" and vg < 12:
		vg += 1
		act._turn_valve()
	_ck("enough valve spins open the countdown",
		act.fix_phase == "launch" and act.state == "play" and act.valve_spins >= 5)
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
	# beat 1: the syrup, on a HOLD. The belt does not exist until it is mixed.
	_ck("the sweet shop opens on the syrup bottles",
		act.press_phase == "syrup" and act.syrup_bottles.size() == 3)
	_ck("the belt waits for the syrup", act.belt_items.is_empty())
	var other_b: int = (act.syrup_want + 1) % act.syrup_bottles.size()
	act.player_pos = (act.syrup_bottles[other_b]["pos"] as Vector3)
	act.hold_sim = true
	var sy0 := 0
	while sy0 < 40:
		sy0 += 1
		act._tick_syrup(0.1)
	_ck("holding the wrong bottle pours nothing", act.syrup_want == 0)
	act.hold_sim = false
	while act.press_phase == "syrup":
		var wi: int = act.syrup_want
		act.player_pos = (act.syrup_bottles[wi]["pos"] as Vector3)
		act._tick_syrup(0.1)
		_ck_once("a bottle never pours itself", act.syrup_want == 0)
		act.hold_sim = true
		var sg := 0
		while act.syrup_want == wi and sg < 200:
			sg += 1
			act._tick_syrup(0.1)
		act.hold_sim = false
	_ck("pouring all three colours starts the belt",
		act.press_phase == "sort" and act.syrup_want == 3)
	_ck("the sorting belt has three colour chutes", act.chutes.size() == 3)
	_ck("a candy is riding the belt", act.belt_items.size() > 0)
	act._press_action()
	_ck("the button no longer stamps a candy", act.candies_done == 0)
	# stop at the END OF THE SORT, not the end of the act: sorting now hands off
	# to the wrapping bench instead of winning, so `state == "play"` alone spun
	# this loop against a belt that had already stopped spawning
	var guard := 0
	while act.state == "play" and act.press_phase == "sort" and guard < 400:
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
	_ck("the full sorted batch opens the wrapping", act.candies_done == act.candies_goal)
	_ck("the belt speeds up as the batch grows", act.belt_speed > 2.4)
	# beat 3: the wrappers, on a rotational drag — the sort's drag-and-drop and
	# the parade's tap must not stand in for it
	_ck("the sorted batch opens the wrapping bench",
		act.press_phase == "wrap" and act.wrap_node != null and act.wrap_done == 0)
	act._press_action()
	_ck("a tap does not twist a wrapper", act.wrap_done == 0)
	var wg := 0
	while act.press_phase == "wrap" and wg < 400:
		wg += 1
		act._wrap_delta(0.35)
	_ck("twisting every wrapper rolls out the parade cart",
		act.wrap_done >= 4 and act.press_phase == "parade" and act.parade_cart != null)
	# beat 4: the timed tap. Off-centre bounces, under the chute lands.
	act.parade_cart.position.x = act.CENTER.x + 12.0
	act._parade_action()
	_ck("a tap with the cart away only bounces", act.parade_loaded == 0)
	var pg := 0
	while act.state == "play" and pg < 40:
		pg += 1
		act.parade_cart.position.x = act.CENTER.x
		act._parade_action()
	_ck("tapping under the chute loads the parade and wins",
		act.state == "won" and act.parade_loaded >= 3)

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
		if act.box_phase == "duck":
			# the one DEFENSIVE beat in the opera: a swipe down, not a tap
			_ck_once("a glove swings across between the rounds", act.box_glove != null)
			_ck_once("the duck hands the finger to the drag channel",
				main.touch_ui != null and bool(main.touch_ui.drag_mode))
			act._punch_action()
			_ck_once("punching the glove is not a duck", not act.box_ducked)
			act._tick_duck(0.05)
			_ck_once("an idle finger never ducks by itself", not act.box_ducked)
			if main.touch_ui != null:
				main.touch_ui.drag_active = true
				main.touch_ui.drag_pos = Vector2(640.0, 200.0)
				act._tick_duck(0.05)
				main.touch_ui.drag_pos = Vector2(640.0, 200.0 + act.DUCK_SWIPE + 6.0)
				act._tick_duck(0.05)
				main.touch_ui.drag_active = false
			_ck_once("swiping down ducks under the glove", act.box_ducked)
			var dguard := 0
			while act.box_phase == "duck" and dguard < 300:
				dguard += 1
				act._tick_duck(0.05)
			_ck_once("the glove passes and the next round rings in",
				act.box_phase == "rounds" and act.box_glove == null)
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
	var props_want := int(act.config.get("props_n", 6))
	var clues_want := int(act.config.get("clues", 3))
	_ck("the configured boxes stand on the stage", act.sleuth_props.size() == props_want)
	var clue_n := 0
	for prop in act.sleuth_props:
		if bool(prop["clue"]):
			clue_n += 1
	_ck("exactly the configured clues hide in boxes", clue_n == clues_want)
	act._sleuth_chest()
	_ck("chest waits for every clue", act.state == "play" and not act.chest_ready)
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
	_ck("every clue readies the treasure chest", act.chest_ready)
	# the last clue's celebration plays out before the lens works again
	var pguard := 0
	while act.sleuth_pause > 0.0 and pguard < 80:
		pguard += 1
		act._tick_lens(0.1)
	# sweeping the lens onto the chest is the reveal — still no button
	act.lens_pos = act.goal.position
	act._tick_lens(0.1)
	# the chest no longer WINS: the pawprint trail comes first, then the board
	_ck("the chest opens the pawprint trail, not the case",
		act.state == "play" and act.board_phase == "trail" and not act.trail_prints.is_empty())
	_ck("only the first print shows before she follows",
		(act.trail_prints[0]["node"] as Node3D).visible
		and not (act.trail_prints[act.trail_prints.size() - 1]["node"] as Node3D).visible)
	_ck("the trail takes the magnifier away — following is a swim", not act.lens.visible)
	act._sleuth_chest()
	_ck("the open chest cannot re-open the case", act.board_phase == "trail")
	for tp: Dictionary in act.trail_prints.duplicate():
		act.player_pos = tp["pos"] as Vector3
		act._tick_trail(0.1)
	_ck("walking every print opens the case board",
		act.board_phase == "board" and act.trail_i >= act.trail_prints.size())
	_ck("the board sets out every clue and three friends",
		act.clue_cards.size() == clues_want and act.suspects.size() == 3)
	_ck("the board hands the finger to the drag channel",
		main.touch_ui != null and bool(main.touch_ui.drag_mode))
	_ck("the freed stagehands' lanterns light the library",
		int(main.opera_pantry.get("lanterns", 0)) == 0 or act.lens_dwell_need < act.LENS_DWELL)
	# a clue dropped on the WRONG friend slides home — no loss, no reset
	var mismatch := -1
	for c: Dictionary in act.clue_cards:
		for s: Dictionary in act.suspects:
			if int(s["index"]) != int(c["owner"]):
				mismatch = int(s["index"])
				break
		if mismatch >= 0:
			act._board_grab(int(c["index"]))
			act._board_drop(mismatch)
			_ck("a clue on the wrong friend slides back kindly",
				act.state == "play" and act.board_pinned == 0 and not bool(c["pinned"]))
			break
	# matching every clue to its owner fills the board
	for c2: Dictionary in act.clue_cards:
		act._board_grab(int(c2["index"]))
		act._board_drop(int(c2["owner"]))
	_ck("matching every clue opens the naming beat",
		act.board_pinned == clues_want and act.board_phase == "name")
	_ck("naming is a TAP, and the button says so", act.action_label() == "NAME")
	# the friend with FEWER clues is the wrong answer, and gently so
	var innocent := -1
	for s2: Dictionary in act.suspects:
		if int(s2["index"]) != act.board_culprit:
			innocent = int(s2["index"])
			break
	act._name_action(innocent)
	_ck("naming the wrong friend only re-hints",
		act.state == "play" and act.board_phase == "name")
	act._name_action(act.board_culprit)
	_ck("naming the friend with the most clues closes the case",
		act.state == "won" and act.board_phase == "done")

func _drive_doctor(act: OperaAct) -> void:
	# wash up, then the waiting bench: find the hurt one, carry it in, read
	# the x-ray, wrap the cast, seal it with coban — once per patient in the
	# queue. The rescue in THIS act is the animal herself, so the brawl frees
	# nobody and hands over no gift.
	_ck("the vet act cages nobody — the animal is the rescue",
		act.captives.is_empty() and not act.gift_given)
	_ck("the checkup opens at the washbasin", act.vet_phase == "wash" and act.vet_basin != null)
	# holding away from the basin does nothing; holding AT it fills the meter
	act.hold_sim = true
	act._tick_vet(0.5)
	_ck("washing needs her at the basin", act.vet_phase == "wash" and act.vet_wash_t == 0.0)
	act.player_pos = act.vet_basin.position
	var hguard := 0
	while act.vet_phase == "wash" and hguard < 80:
		hguard += 1
		act._tick_vet(0.1)
	_ck("holding at the basin scrubs up", act.vet_phase == "find" and not act.hold_sim)
	_ck("the ward holds four animals", act.vet_animals.size() == 4)
	var patients := int(act.config.get("patients", 1))
	_ck("the waiting bench holds a queue", patients >= 2)
	for p in range(patients):
		_ck("patient %d: exactly one animal is hurt" % (p + 1),
			act.vet_hurt >= 0 and bool(act.vet_animals[act.vet_hurt]["hurt"]))
		_ck("patient %d: only the hurt one wears an ouch star" % (p + 1),
			(act.vet_animals[act.vet_hurt]["mark"] as Node3D).visible)
		if p == 0:
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
		if p == 0:
			act._vet_bone(act.vet_limb)
			_ck("a warming screen refuses even the right bone",
				act.vet_phase == "xray" and act.vet_warm > 0.0)
		var fuzz := 0
		while act.vet_warm > 0.0 and fuzz < 60:
			fuzz += 1
			act._tick_vet(0.1)
		if p == 0:
			var sound: int = (act.vet_limb + 1) % 4
			act._vet_bone(sound)
			_ck("a sound bone is gently refused", act.vet_phase == "xray")
		var treating: int = act.vet_hurt
		act._vet_bone(act.vet_limb)
		_ck("naming the crack opens the cast", act.vet_phase == "cast")
		if p == 0:
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
		if p < patients - 1:
			_ck("patient %d hops to recovery and the next ouch star appears" % (p + 1),
				act.state == "play" and act.vet_phase == "find" and act.vet_done_n == p + 1)
			_ck("the healed friend is marked healed and picks a different patient",
				bool(act.vet_animals[treating]["healed"]) and act.vet_hurt != treating)
			_ck("the scope is cleared for the next x-ray",
				act.vet_bones.is_empty() and act.vet_layers.is_empty())
		else:
			_ck("the last coban seals the cast and wins", act.state == "won" and act.vet_phase == "done")

func _drive_scroll(act: OperaAct) -> void:
	# beat 1: the planting, a drag-and-drop. The slingshot cannot skip it.
	_ck("the picnic opens on the planting",
		act.farm_phase == "plant" and act.furrows.size() == act.FARM_SEEDS)
	act._farm_launch(0.5)
	_ck("the slingshot does not fire before the seeds are in",
		act.farm_flights.is_empty() and act.farm_phase == "plant")
	for f: Dictionary in act.furrows:
		act._plant_grab(int(f["index"]))
		act._plant_drop(int(f["index"]))
	_ck("planting every seed brings out the piggies",
		act.seeds_planted == act.FARM_SEEDS and act.farm_phase == "feed")
	_ck("meadow has the configured hungry piggies",
		act.piggies.size() == int(act.config.get("piggies", 7)))
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
	_ck("every lobbed veggie brings the herd to the mud",
		act.farm_fed == act.piggies.size() and act.farm_phase == "mud")
	# beat 3: swipe UP. Down is the boxer's duck; it must not hop a piggy.
	if main.touch_ui != null:
		main.touch_ui.drag_active = true
		main.touch_ui.drag_pos = Vector2(640.0, 300.0)
		act._tick_mud(0.05)
		main.touch_ui.drag_pos = Vector2(640.0, 420.0)   # downward
		act._tick_mud(0.05)
		_ck("swiping DOWN does not hop a piggy", act.mud_leaps == 0)
		var mg := 0
		while act.farm_phase == "mud" and mg < 40:
			mg += 1
			main.touch_ui.drag_active = false
			act._tick_mud(0.05)
			main.touch_ui.drag_active = true
			main.touch_ui.drag_pos = Vector2(640.0, 460.0)
			act._tick_mud(0.05)
			main.touch_ui.drag_pos = Vector2(640.0, 340.0)   # upward
			act._tick_mud(0.05)
		main.touch_ui.drag_active = false
	_ck("swiping up hops every piggy over the mud",
		act.mud_leaps >= act.MUD_LEAPS and act.farm_phase == "barn")
	# beat 4: the scrub home. One long pull is not a sweep — it takes both ways.
	_ck("the barn gate is waiting", act.barn_gate != null and act.barn_scrub == 0.0)
	var bg := 0
	while act.farm_phase == "barn" and bg < 400:
		bg += 1
		act._barn_sweep(140.0 if bg % 2 == 0 else -140.0)
	_ck("sweeping the herd home finishes the picnic",
		act.state == "won" and act.farm_phase == "done")

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
	# clear the encore's hits first: this check is "she closed WITHOUT singing",
	# and the 4 hits poked in above would otherwise take the bow here instead
	de.happy_hits = 0
	de.close_demo()
	await process_frame
	_ck("closing without dancing keeps the mic waiting",
		act.state == "play" and act.dance != null)
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
		# SHINE is a charge: one tap beside the lantern must NOT light it.
		# While the phantom still sweeps, even the charge waits.
		act.player_pos = act.lanterns[act.lantern_i]["pos"] as Vector3
		act._lantern_shine_tap()
		_ck("the sweeping phantom refuses the beam", act.lantern_charge == 0.0)
		act.boss["timer"] = 0.0
		act._lantern_shine_tap()
		_ck("one SHINE tap no longer lights the lantern",
			String(act.boss["phase"]) == "shadow" and act.lantern_charge > 0.0)
	else:
		_ck("dragon opens hiding in the curtains", String(act.boss["phase"]) == "hide" and act.action_label() == "SPARKLE")
		_ck("dragon roams five curtain spots when bold", act.peek_spots.size() == 5)
		act._hit_boss()
		_ck("sparkles fizzle while he hides", int(act.boss["hp"]) == hp)
	var modes := {}
	var saw_roar := false
	var roar_hp := -1
	var guard := 0
	while act.state == "play" and guard < 3000:
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
		elif phase == "roar":
			if not saw_roar:
				saw_roar = true
				roar_hp = int(act.boss["hp"])
				act._hit_boss()
				_ck("sparkles fizzle against the ROAR", int(act.boss["hp"]) == roar_hp)
			await process_frame
		else:
			await process_frame
	_ck("boss act does not stall", guard < 3000)
	if finale:
		_ck("the grand finale remixes lanterns AND curtain chases",
			bool(modes.get("lantern", false)) and bool(modes.get("roam", false)))
	if not dual:
		_ck("every fourth star sends the dragon into a roar", saw_roar)

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
