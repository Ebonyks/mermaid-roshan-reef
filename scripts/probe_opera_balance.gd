extends SceneTree
# Advisory balance playtest for the Pearl Opera House. Every act (except the
# kart race and the DanceEngine concert, which have their own tuned engines)
# is played TEN times by simulated children — personas with real reaction
# delays, travel speeds, wandering and wrong-tap rates — by pumping
# OperaAct._process() with a fixed timestep. Prints one BALANCE| line per run
# plus a per-act summary with a verdict against the 120-240s fun band
# (owner 2026-07-25: every act is a 2-4 minute performance with its own
# pacing — the old 55-140s band described a show that was over too fast).
# This probe is ADVISORY: it prints metrics and never the gate's fail tokens.

const DT := 0.1
const TIME_CAP := 360.0
const BAND_LO := 120.0
const BAND_HI := 240.0

# Personas are calibrated to a real 4-year-old, not an optimal bot: slow
# reactions, slower swimming, wandering, and GAWK — the pause to stare at
# sparkles/confetti after doing something exciting.
const PERSONAS := [
	{"name": "speedy", "reaction": 0.9, "err": 0.06, "speed": 0.85, "wander": 0.05, "gawk": 0.15},
	{"name": "casual", "reaction": 1.5, "err": 0.15, "speed": 0.7, "wander": 0.15, "gawk": 0.3},
	{"name": "casual", "reaction": 1.4, "err": 0.16, "speed": 0.7, "wander": 0.15, "gawk": 0.3},
	{"name": "wander", "reaction": 1.8, "err": 0.12, "speed": 0.6, "wander": 0.5, "gawk": 0.35},
	{"name": "masher", "reaction": 1.0, "err": 0.32, "speed": 0.75, "wander": 0.1, "gawk": 0.2},
	{"name": "speedy", "reaction": 1.0, "err": 0.08, "speed": 0.85, "wander": 0.05, "gawk": 0.15},
	{"name": "casual", "reaction": 1.6, "err": 0.18, "speed": 0.7, "wander": 0.2, "gawk": 0.3},
	{"name": "wander", "reaction": 2.0, "err": 0.1, "speed": 0.6, "wander": 0.55, "gawk": 0.4},
	{"name": "masher", "reaction": 1.1, "err": 0.3, "speed": 0.75, "wander": 0.1, "gawk": 0.2},
	{"name": "casual", "reaction": 1.5, "err": 0.2, "speed": 0.7, "wander": 0.15, "gawk": 0.3},
]

var main: ReefMain
var done := false
var mistakes := 0
var wait_t := 0.0
var persona: Dictionary = {}
var intent_key := -9999            # sticky wrong/right choice per objective step
var intent_choice := -1
var echo_key := -1                 # sticky echo intent: (round, pos) being danced
var echo_target := -1
var farm_pull_t := 0.0             # seconds spent drawing the sling back
var barn_dir := 1.0                # which way the shooing hand is sweeping
var brawl_taps := 0                # sparkles actually thrown this run
var hold_key := -1                 # which hold target the finger is currently on

func _init() -> void:
	Engine.time_scale = 8.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.game = "opera"   # inert branch of main's tick — acts are driven directly
	print("BALANCE|band=%d-%ds runs=10 dt=%.2f" % [int(BAND_LO), int(BAND_HI), DT])
	for act_i in range(OperaHouse.ACTS.size()):
		var cfg: Dictionary = OperaHouse.ACTS[act_i]
		var kind := String(cfg["kind"])
		if kind == "race" or kind == "dance":
			print("BALANCE|act=%02d %s|skipped (engine has its own tuning: %s)" % [act_i + 1, String(cfg["career"]), kind])
			continue
		var times: Array[float] = []
		var mistake_counts: Array[int] = []
		var incomplete := 0
		for run in range(10):
			seed(9000 + act_i * 100 + run)
			persona = PERSONAS[run]
			var t := await _play_act(cfg.duplicate())
			if t < 0.0:
				incomplete += 1
				print("BALANCE|act=%02d %s|run=%d persona=%s|INCOMPLETE cap=%ds mistakes=%d snap[%s]" % [act_i + 1, String(cfg["career"]), run, String(persona["name"]), int(TIME_CAP), mistakes, last_snapshot])
			else:
				times.append(t)
				mistake_counts.append(mistakes)
				print("BALANCE|act=%02d %s|run=%d persona=%s|time=%.1f mistakes=%d" % [act_i + 1, String(cfg["career"]), run, String(persona["name"]), t, mistakes])
		times.sort()
		if times.is_empty():
			print("BALANCE|act=%02d %s|summary verdict=NEVER-COMPLETED" % [act_i + 1, String(cfg["career"])])
			continue
		var med: float = times[times.size() / 2]
		var verdict := "ok"
		if med < BAND_LO: verdict = "SHORT"
		elif med > BAND_HI: verdict = "LONG"
		var mist_total := 0
		for mc in mistake_counts: mist_total += mc
		print("BALANCE|act=%02d %s|summary med=%.1f min=%.1f max=%.1f mistakes_avg=%.1f incomplete=%d verdict=%s" % [
			act_i + 1, String(cfg["career"]), med, times[0], times[times.size() - 1], float(mist_total) / maxf(1.0, float(mistake_counts.size())), incomplete, verdict])
	print("BALANCE|done")
	quit()

var last_snapshot := ""

func _snapshot(act: OperaAct) -> String:
	if not is_instance_valid(act):
		return "act-freed"
	var base := "state=%s phase=%s" % [act.state, act.stage_phase]
	if act.stage_phase == "brawl" or act.stage_phase == "rescue":
		# the six shelled acts keep stalling here; report enough to stop guessing
		var nearest := -1.0
		var live := 0
		for g in act.imps:
			if bool(g["popped"]):
				continue
			live += 1
			var gap: Vector3 = (g["pos"] as Vector3) - act.player_pos
			gap.y = 0.0
			if nearest < 0.0 or gap.length() < nearest:
				nearest = gap.length()
		# the survivor's HP and how many sparkles we actually threw: a stall with
		# hp still full means the taps are not landing, a stall with hp draining
		# means something is healing it. Guessing between those cost two rounds
		# earlier, so the snapshot answers it directly.
		var hp := -1
		for g2 in act.imps:
			if not bool(g2["popped"]):
				hp = int(g2.get("hp", -1))
				break
		return base + " imps=%d live=%d left=%d hp=%d taps=%d nearest=%.1f pos=(%.1f,%.1f) wait=%.2f" % [
			act.imps.size(), live, act.imps_left, hp, brawl_taps, nearest,
			act.player_pos.x - act.CENTER.x, act.player_pos.z - act.CENTER.z, wait_t]
	match act.kind:
		"echo":
			return base + " echo=%s round=%d pos=%d dwell=%.2f" % [act.echo_phase, act.echo_round, act.echo_pos, act.pad_dwell]
		"boss":
			var bphase := String(act.boss.get("phase", "?"))
			var bdist := ((act.boss["node"] as Node3D).position).distance_to(act.player_pos) if act.boss.has("node") else -1.0
			return base + " boss=%s hp=%d lant=%d dist=%.1f" % [bphase, int(act.boss.get("hp", -1)), act.lantern_i, bdist]
		"order", "paint":
			return base + " order=%s step=%d brush=%d sift=%.1f pour=%.1f bake=%.1f pipe=%d" % [
				act.order_phase, act.step, act.brush_loaded, act.sift_done, act.pour_t, act.bake_t, act.pipe_trace]
		"press":
			return base + " press=%s candies=%d syrup=%d wrap=%d parade=%d" % [
				act.press_phase, act.candies_done, act.syrup_want, act.wrap_done, act.parade_loaded]
		"shuffle":
			return base + " shuffle=%s round=%d knots=%d taps=%d" % [
				act.shuffle_phase, act.shuffle_round, act.rope_undone, act.cab_taps]
		"doctor":
			return base + " vet=%s hurt=%d limb=%d wrap=%.1f" % [act.vet_phase, act.vet_hurt, act.vet_limb, act.vet_wrap]
		"scroll":
			return base + " farm=%s planted=%d fed=%d leaps=%d scrub=%.0f" % [
				act.farm_phase, act.seeds_planted, act.farm_fed, act.mud_leaps, act.barn_scrub]
		"fix":
			return base + " fix=%s flow=%d fuse=%.1f leak=%.1f laid=%d" % [act.fix_phase, act.pipe_flow_cell, act.pipe_fuse_t, act.pipe_leak_t, act.pipe_filled.size()]
	return base

func _play_act(cfg: Dictionary) -> float:
	done = false
	mistakes = 0
	wait_t = 1.0
	intent_key = -9999
	intent_choice = -1
	echo_key = -1
	echo_target = -1
	farm_pull_t = 0.0
	barn_dir = 1.0
	brawl_taps = 0
	hold_key = -1
	last_snapshot = ""
	var act := OperaAct.new()
	act.process_mode = Node.PROCESS_MODE_DISABLED   # only our manual pumps tick it
	get_root().add_child(act)
	act.start(main, cfg, Callable(self, "_act_done"))
	var sim_t := 0.0
	var pumps := 0
	while not done and sim_t < TIME_CAP:
		_drive(act, DT)
		act._process(DT)
		sim_t += DT
		pumps += 1
		if pumps % 100 == 0:
			await process_frame
	var result := sim_t if done else -1.0
	if not done:
		last_snapshot = _snapshot(act)
		act.cancel()
	await process_frame
	await process_frame
	return result

func _act_done() -> void:
	done = true

func _travel(act: OperaAct, target: Vector3, dt: float) -> bool:
	# returns true when the persona has arrived (within tap reach)
	var flat := target - act.player_pos
	flat.y = 0.0
	var arrive := flat.length() < 3.0
	if arrive:
		return true
	var dir := flat.normalized()
	if randf() < float(persona["wander"]) * dt:
		dir = dir.rotated(Vector3.UP, randf_range(-1.2, 1.2))
	act.player_pos += dir * act.MOVE_SPEED * float(persona["speed"]) * dt
	return false

func _ready_to_act(dt: float) -> bool:
	wait_t -= dt
	if wait_t > 0.0:
		return false
	wait_t = float(persona["reaction"]) * randf_range(0.7, 1.4)
	if randf() < float(persona.get("gawk", 0.0)):
		wait_t += randf_range(1.5, 3.0)   # staring at the sparkles
	return true

func _drive(act: OperaAct, dt: float) -> void:
	if act.state != "play":
		return
	if act.stage_phase == "brawl" or act.stage_phase == "rescue":
		var target := Vector3.ZERO
		var found := false
		for g in act.imps:
			if not bool(g["popped"]):
				target = g["pos"] as Vector3
				found = true
				break
		# Imps CHASE Roshan and her bubble shield shoves them off at 2.5, so the
		# gap oscillates and _travel()'s 3.0 arrival almost never latches. Play
		# it the way a child does instead: close the distance, then tap as soon
		# as the imp is inside the sparkle's real 8.0 reach.
		if found:
			var gap := target - act.player_pos
			gap.y = 0.0
			if gap.length() < 7.0:
				if _ready_to_act(dt):
					# close enough that a child would swing: settle onto the imp
					# so the shield bump cannot shove the tap out of reach
					act.player_pos = Vector3(target.x, act.player_pos.y, target.z)
					brawl_taps += 1
					act._brawl_action()
			else:
				_travel(act, target, dt)
		return
	match act.kind:
		"order", "paint":
			_drive_order(act, dt)
		"echo":
			_drive_echo(act, dt)
		"shuffle":
			_drive_shuffle(act, dt)
		"press":
			_drive_press(act, dt)
		"box":
			_drive_box(act, dt)
		"sleuth":
			_drive_sleuth(act, dt)
		"doctor":
			_drive_doctor(act, dt)
		"scroll":
			_drive_scroll(act, dt)
		"fix":
			_drive_fix(act, dt)
		"boss":
			_drive_boss(act, dt)

func _intent(count: int, want: int, key: int) -> int:
	# one sticky decision per objective step: usually right, sometimes a
	# wrong reach (rolled ONCE, not per tick). After the engine's gentle
	# bounce the persona learns and goes for the right thing.
	if key != intent_key:
		intent_key = key
		intent_choice = want
		if count > 1 and randf() < float(persona["err"]):
			mistakes += 1
			intent_choice = (want + 1 + randi() % maxi(1, count - 1)) % count
	return intent_choice

func _intent_learned(want: int) -> void:
	intent_choice = want

func _drive_order(act: OperaAct, dt: float) -> void:
	# the painter's canvas is painted by dragging, so a simulated child at the
	# easel sweeps the brush back and forth rather than tapping once
	if act.paint_easel and act.brush_loaded >= 0:
		if _ready_to_act(dt):
			var band := act._paint_band_rows()
			for i in range(6):
				var t := randf()
				var row := randf_range(float(band.x) + 1.0, float(band.y) - 1.0)
				act._paint_stroke_uv(t, row / float(act.PAINT_RES))
		return
	match act.order_phase:
		"sketch":
			# a trace: one guide dot per ready-tick, at the persona's hand speed
			if not _ready_to_act(dt) or main.touch_ui == null or act.cam == null:
				return
			for d in act.sketch_dots:
				if not (d as Node3D).visible:
					continue
				main.touch_ui.drag_active = true
				main.touch_ui.drag_pos = act.cam.unproject_position((d as Node3D).position)
				act._tick_sketch(dt)
				main.touch_ui.drag_active = false
				return
			return
		"fill":
			# swim to the called shape, then hold on it. The finger LIFTS between
			# panels (hold_key), so every panel costs its own reaction time —
			# leaving hold_sim latched made the whole beat cost one hold.
			if act.fill_want >= act.fill_panels.size():
				return
			if hold_key != act.fill_want:
				hold_key = act.fill_want
				act.hold_sim = false
			var want: Vector3 = act.fill_panels[act.fill_want]["pos"] as Vector3
			if _travel(act, want, dt) and (act.hold_sim or _ready_to_act(dt)):
				act.hold_sim = true
			act._tick_fill(dt)
			return
		"sift":
			# scrubbing travel, at the persona's hand speed
			act.sift_done += dt * lerpf(6.0, 13.0, float(persona["speed"]))
			act._tick_sift(dt)
			return
		"pour":
			if act.hold_sim or _ready_to_act(dt):
				act.hold_sim = true
			act._tick_pour(dt)
			return
		"bake":
			act._tick_bake(dt)
			if act.bake_golden and _ready_to_act(dt):
				act._bake_action()
			return
		"pipe":
			# tracing the ring: one bead per reaction beat
			if _ready_to_act(dt):
				for d in act.pipe_dots:
					var n := d as Node3D
					if n.visible:
						n.visible = false
						act.pipe_trace += 1
						break
				act._tick_pipe(dt)
			return
	if act.order_phase == "stir":
		# stirring is a circular drag: once at the bowl the persona traces
		# circles at roughly its own hand speed rather than tapping three times
		if act.stir_drag:
			act._stir_drag_delta(dt * lerpf(2.2, 4.5, float(persona["speed"])))
			return
		_travel(act, act.goal.position, dt)
		return
	if act.order_phase == "decorate":
		for spot in act.deco_spots:
			if not bool(spot["done"]):
				if _travel(act, spot["pos"] as Vector3, dt) and _ready_to_act(dt):
					act._deco_action(int(spot["index"]))
				return
		return
	if act.order_flow == "carry_paint" and act.brush_loaded >= 0:
		_travel(act, act.canvas_pos, dt)   # engine paints on proximity
		return
	if act.step >= act.order_steps.size():
		return
	var want: int = act.order_steps[act.step]
	var choice := _intent(act.pads.size(), want, 1000 + act.step)
	if _travel(act, act.pads[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
		act._act_action(choice)
		if choice != want:
			_intent_learned(want)

func _drive_echo(act: OperaAct, dt: float) -> void:
	# tiles fire on DWELL now: the persona picks a sticky target per step
	# (sometimes the wrong tile), swims there and simply stands on it
	if act.echo_phase == "ribbon":
		# a trace: the persona sweeps her finger along the arc at her own hand
		# speed, one dot per ready-tick, so a slower child takes longer
		if not _ready_to_act(dt) or main.touch_ui == null or act.cam == null:
			return
		for d in act.ribbon_dots:
			if not (d as Node3D).visible:
				continue
			main.touch_ui.drag_active = true
			main.touch_ui.drag_pos = act.cam.unproject_position((d as Node3D).position)
			act._tick_ribbon(dt)
			main.touch_ui.drag_active = false
			return
		return
	if act.echo_phase == "twirl":
		# circles: a quarter-turn of finger travel per ready-tick
		if _ready_to_act(dt):
			act._twirl_delta(PI * 0.5)
		return
	if act.echo_phase != "repeat" or act.echo_pos >= act.echo_seq.size():
		echo_key = -1
		return
	var key: int = act.echo_round * 100 + act.echo_pos
	if key != echo_key:
		echo_key = key
		var want: int = act.echo_seq[act.echo_pos]
		echo_target = want
		if randf() < float(persona["err"]):
			mistakes += 1
			echo_target = (want + 1 + randi() % maxi(1, act.pads.size() - 1)) % act.pads.size()
	if act.last_pad == echo_target:
		# the tile underfoot just fired — step off the row so it can re-arm
		_travel(act, (act.pads[echo_target]["pos"] as Vector3) + Vector3(0, 0, 6.0), dt)
		return
	_travel(act, act.pads[echo_target]["pos"] as Vector3, dt)

func _drive_shuffle(act: OperaAct, dt: float) -> void:
	if act.shuffle_phase == "hide":
		# the showmanship beat: carry a hat over to the fish and set it down
		if not _ready_to_act(dt):
			return
		act.hide_hat = randi() % act.hats.size()
		act.hide_pos = act.hats[act.hide_hat]["pos"] as Vector3
		(act.hats[act.hide_hat]["node"] as Node3D).position = act.bunny.position
		act._tick_hide(dt)
		return
	if act.shuffle_phase == "rope":
		# the rope waits for a finger forever — unlike the duck it has no clock
		# of its own, so the persona has to actually pull it or the act stalls
		if not _ready_to_act(dt) or main.touch_ui == null:
			return
		main.touch_ui.drag_active = true
		main.touch_ui.drag_pos = Vector2(640.0, 400.0)
		act._tick_rope(dt)
		main.touch_ui.drag_pos = Vector2(640.0 + act.rope_pull_need + 8.0, 400.0)
		act._tick_rope(dt)
		main.touch_ui.drag_active = false
		return
	if act.shuffle_phase == "cabinet":
		# a rhythm beat: she taps when she is ready, and it only counts on the
		# beat, so the persona's reaction time and the beat both cost time
		if act.cab_wand != null and _travel(act, act.cab_wand.position, dt) and _ready_to_act(dt):
			act._shuffle_action(0)
		return
	if act.shuffle_phase != "pick":
		return
	if not _ready_to_act(dt):
		return
	var choice := _intent(act.hats.size(), act.bunny_at, 5000 + act.shuffle_round)
	act._shuffle_action(choice)
	if choice != act.bunny_at:
		_intent_learned(act.bunny_at)

func _drive_press(act: OperaAct, dt: float) -> void:
	if act.press_phase == "syrup":
		# swim to the sparkling bottle, then hold on it. The finger lifts between
		# bottles for the same reason it lifts between the painter's panels.
		if act.syrup_want >= act.syrup_bottles.size():
			return
		if hold_key != act.syrup_want:
			hold_key = act.syrup_want
			act.hold_sim = false
		var bpos: Vector3 = act.syrup_bottles[act.syrup_want]["pos"] as Vector3
		if _travel(act, bpos, dt) and (act.hold_sim or _ready_to_act(dt)):
			act.hold_sim = true
		act._tick_syrup(dt)
		return
	if act.press_phase == "wrap":
		# a rotational drag: a quarter-turn of finger travel per ready-tick
		if _ready_to_act(dt):
			act._wrap_delta(PI * 0.5)
		return
	if act.press_phase == "parade":
		# a timed tap: the persona taps when it is ready, and only a tap with
		# the cart underneath counts, so its reaction time is the real cost
		if _ready_to_act(dt):
			act._parade_action()
		return
	# the persona grabs the front candy, carries it to a chute and drops it,
	# sometimes into the wrong one. The reaction cost is paid at the GRAB;
	# once the finger is down the drag is continuous, like the stir and the
	# fill — the old one-step-per-reaction carry could never outrun the belt
	# for any persona slower than speedy (step 13*speed*dt vs the 1.0 gap
	# between belt and chute radius), which is exactly what run 761 measured.
	if act.belt_items.is_empty():
		return
	if not (act.sort_held >= 0 and act.hold_sim):
		if not _ready_to_act(dt):
			return
		act.sort_held = 0
		act.hold_sim = true
	var it: Dictionary = act.belt_items[0]
	var want: int = int(it["want"])
	var choice := _intent(act.chutes.size(), want, 7000 + act.candies_done)
	var node := it["node"] as Node3D
	var chute: Vector3 = act.chutes[choice]["pos"] as Vector3
	# carry it there at the persona's hand speed instead of teleporting
	var step: float = act.MOVE_SPEED * float(persona["speed"]) * dt
	var to_chute := chute - node.position
	if to_chute.length() > step:
		node.position += to_chute.normalized() * step
		return
	node.position = chute
	act.hold_sim = false
	act._sort_drop()
	if choice != want:
		_intent_learned(want)

func _drive_box(act: OperaAct, dt: float) -> void:
	if act.box_wait > 0.0:
		return
	if act.box_phase == "warmup":
		if act.box_bag != null and _travel(act, act.box_bag.position, dt) and _ready_to_act(dt):
			act._punch_action()
		return
	if act.box_phase == "belt":
		if act.box_belt != null:
			_travel(act, act.box_belt.position, dt)
		return
	if act.box_phase == "duck":
		# the glove crosses on its own clock whether or not she reacts, so this
		# beat costs its DUCK_SWEEP either way — the persona's reaction time
		# only decides whether she gets the whoosh or the giggle
		if not act.box_ducked and _ready_to_act(dt) and main.touch_ui != null:
			main.touch_ui.drag_active = true
			main.touch_ui.drag_pos = Vector2(640.0, 200.0)
			act._tick_duck(0.0)
			main.touch_ui.drag_pos = Vector2(640.0, 200.0 + act.DUCK_SWIPE + 6.0)
			act._tick_duck(0.0)
			main.touch_ui.drag_active = false
		return
	var target := Vector3.ZERO
	var found := false
	for g in act.imps:
		if not bool(g["popped"]):
			target = g["pos"] as Vector3
			found = true
			break
	if found and _travel(act, target, dt) and _ready_to_act(dt):
		if act._box_on_beat():
			act._punch_action()

func _drive_sleuth(act: OperaAct, dt: float) -> void:
	# the detective drags a magnifier rather than swimming and tapping: the
	# persona sweeps the lens toward its target at its own hand speed and has
	# to hold it there, so dwell time is part of the act's real cost
	if act.board_phase == "board":
		# the deduction beat: one card matched per ready-tick, with the persona's
		# usual sticky wrong reach so a mismatch costs a slide-back like a child's
		if not _ready_to_act(dt):
			return
		for c: Dictionary in act.clue_cards:
			if bool(c["pinned"]):
				continue
			var owner: int = int(c["owner"])
			var pick := _intent(act.suspects.size(), owner, 9000 + int(c["index"]))
			act._board_grab(int(c["index"]))
			act._board_drop(pick)
			if pick != owner:
				_intent_learned(owner)
			return
		return
	if act.board_phase == "name":
		if _travel(act, act.suspects[act.board_culprit]["pos"] as Vector3, dt) and _ready_to_act(dt):
			act._name_action(act.board_culprit)
		return
	if act.board_phase == "trail":
		# the pawprint trail is plain swimming: head for the live print and
		# let the act light it on proximity
		if act.trail_i < act.trail_prints.size():
			_travel(act, act.trail_prints[act.trail_i]["pos"] as Vector3, dt)
		return
	if act.lens_drag:
		var want := act.goal.position if act.chest_ready else _nearest_unopened(act)
		var arm := want - act.lens_pos
		arm.y = 0.0
		var reach := act.MOVE_SPEED * float(persona["speed"]) * dt
		if arm.length() <= reach:
			act.lens_pos = Vector3(want.x, act.lens_pos.y, want.z)
		else:
			act.lens_pos += arm.normalized() * reach
		return
	if act.chest_ready:
		if _travel(act, act.goal.position, dt) and _ready_to_act(dt):
			act._sleuth_chest()
		return
	# a curious child peeks nearest-box-first with no answer knowledge
	var target := Vector3.ZERO
	var found := false
	var best_d := 1e9
	for prop in act.sleuth_props:
		if bool(prop["opened"]):
			continue
		var d: float = (prop["pos"] as Vector3).distance_to(act.player_pos)
		if d < best_d:
			best_d = d
			target = prop["pos"] as Vector3
			found = true
	if not found:
		return
	if _travel(act, target, dt) and _ready_to_act(dt):
		for prop in act.sleuth_props:
			if not bool(prop["opened"]) and (prop["pos"] as Vector3).distance_to(act.player_pos) < 4.5:
				act._sleuth_action(int(prop["index"]))
				break

func _nearest_unopened(act: OperaAct) -> Vector3:
	var best := act.lens_pos
	var best_d := 1e9
	for prop in act.sleuth_props:
		if bool(prop["opened"]):
			continue
		var d: float = (prop["pos"] as Vector3).distance_to(act.lens_pos)
		if d < best_d:
			best_d = d
			best = prop["pos"] as Vector3
	return best

func _drive_doctor(act: OperaAct, dt: float) -> void:
	match act.vet_phase:
		"wash":
			# swim to the basin and hold; the act drains the meter if she lets go
			if _travel(act, act.vet_basin.position, dt) and (act.hold_sim or _ready_to_act(dt)):
				act.hold_sim = true
		"find":
			# a child looks around the ward before spotting the ouch star —
			# keyed per patient, so each new ouch star is its own little search
			var want: int = act.vet_hurt
			var choice := _intent(act.vet_animals.size(), want, 9000 + act.vet_done_n * 20)
			if _travel(act, act.vet_animals[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
				act._vet_pick(choice)
				if choice != want:
					_intent_learned(want)
		"carry":
			_travel(act, act.vet_scope.position, dt)
		"xray":
			if not _ready_to_act(dt):
				return
			var bone := _intent(4, act.vet_limb, 9100 + act.vet_done_n * 20)
			act._vet_bone(bone)
			if bone != act.vet_limb:
				_intent_learned(act.vet_limb)
		"cast", "coban":
			act._vet_wrap_delta(dt * lerpf(2.0, 4.2, float(persona["speed"])))

func _drive_scroll(act: OperaAct, dt: float) -> void:
	if act.farm_phase == "plant":
		# a drag-and-drop: one seed carried into its hole per ready-tick
		if not _ready_to_act(dt):
			return
		for f: Dictionary in act.furrows:
			if bool(f["planted"]):
				continue
			act._plant_grab(int(f["index"]))
			act._plant_drop(int(f["index"]))
			return
		return
	if act.farm_phase == "mud":
		if _ready_to_act(dt):
			act._mud_hop()
		return
	if act.farm_phase == "barn":
		# a scrub: one sweep of the hand per ready-tick, direction alternating
		if _ready_to_act(dt):
			barn_dir = -barn_dir
			act._barn_sweep(220.0 * float(persona["speed"]) * barn_dir)
		return
	if act.farm_phase == "done":
		return
	# lobbing: the persona picks the nearest unfed piggy, judges the pull, and
	# lets go — with an aim wobble scaled to how careless it is
	if act.farm_flights.size() > 0:
		return
	var target := -1.0
	var best := 1e9
	for pig in act.piggies:
		if bool(pig["fed"]):
			continue
		var sx: float = float(pig["sx"])
		if sx < act.FARM_ROSHAN_X or sx > 1030.0:
			continue
		if sx < best:
			best = sx
			target = sx
	if target < 0.0:
		farm_pull_t = 0.0
		return
	# drawing the sling back is part of the throw, so charge before releasing
	farm_pull_t += dt
	if farm_pull_t < 0.45 * float(persona["reaction"]):
		return
	if not _ready_to_act(dt):
		return
	farm_pull_t = 0.0
	var power: float = (target - act.FARM_ROSHAN_X) / 780.0
	power += randf_range(-1.0, 1.0) * float(persona["err"]) * 0.5
	act._farm_launch(clampf(power, 0.0, 1.0))

func _drive_fix(act: OperaAct, dt: float) -> void:
	if act.fix_phase == "launch":
		if act.hold_sim or _ready_to_act(dt):
			act.hold_sim = true
		return
	if act.fix_phase == "valve":
		if _travel(act, act.valve.position, dt) and _ready_to_act(dt):
			act._turn_valve()
		return
	# Pipe Dream: lay the front piece where the bubbles are heading, or ahead
	# of them along the middle row. Sometimes into a square that will not help.
	if not _ready_to_act(dt):
		return
	var want := act.pipe_flow_cell
	if want < 0:
		want = act._pipe_cell_at(act.PIPE_START_ROW, 0)
	# bubbles parked at an occupied square means the piece there is WRONG —
	# the act now allows laying the front piece straight over it, so the
	# persona does what a real child does: slap a new pipe on the leak
	var swap: bool = want >= 0 and want == act.pipe_flow_cell \
		and String(act.pipe_cells[want]["shape"]) != ""
	if not swap and (want < 0 or String(act.pipe_cells[want]["shape"]) != ""):
		# the head is already piped; look along the row for the next gap
		for c in range(act.PIPE_COLS):
			var idx: int = act._pipe_cell_at(act.PIPE_START_ROW, c)
			if idx >= 0 and String(act.pipe_cells[idx]["shape"]) == "":
				want = idx
				break
	if want < 0 or (not swap and String(act.pipe_cells[want]["shape"]) != ""):
		return
	# a careless child sometimes lays a corner where a straight was needed
	if randf() > float(persona["err"]):
		var spins := 0
		while act.pipe_queue[0] != "h" and spins < 3:
			spins += 1
			act.pipe_queue[0] = act._pipe_roll()
	else:
		mistakes += 1
	act._pipe_place(want)

func _drive_boss(act: OperaAct, dt: float) -> void:
	var phase := String(act.boss["phase"])
	if phase == "shadow":
		var lant: Dictionary = act.lanterns[act.lantern_i]
		if _travel(act, lant["pos"] as Vector3, dt) and _ready_to_act(dt):
			act._light_lantern()
		return
	if phase == "peek":
		var bpos: Vector3 = (act.boss["node"] as Node3D).position
		var near := bpos.distance_to(act.player_pos) <= 15.0
		if not near:
			_travel(act, bpos, dt)
			return
		if _ready_to_act(dt):
			act._fire_star()
