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
	if act.stage_phase == "brawl":
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
		return base + " imps=%d live=%d left=%d nearest=%.1f pos=(%.1f,%.1f) wait=%.2f" % [
			act.imps.size(), live, act.imps_left, nearest,
			act.player_pos.x - act.CENTER.x, act.player_pos.z - act.CENTER.z, wait_t]
	match act.kind:
		"echo":
			return base + " echo=%s round=%d pos=%d dwell=%.2f" % [act.echo_phase, act.echo_round, act.echo_pos, act.pad_dwell]
		"boss":
			var bphase := String(act.boss.get("phase", "?"))
			var bdist := ((act.boss["node"] as Node3D).position).distance_to(act.player_pos) if act.boss.has("node") else -1.0
			return base + " boss=%s hp=%d lant=%d dist=%.1f" % [bphase, int(act.boss.get("hp", -1)), act.lantern_i, bdist]
		"order", "paint":
			return base + " order=%s step=%d brush=%d" % [act.order_phase, act.step, act.brush_loaded]
		"press":
			return base + " candies=%d busy=%.2f" % [act.candies_done, act.press_busy]
		"shuffle":
			return base + " shuffle=%s round=%d" % [act.shuffle_phase, act.shuffle_round]
		"doctor":
			return base + " vet=%s hurt=%d limb=%d wrap=%.1f" % [act.vet_phase, act.vet_hurt, act.vet_limb, act.vet_wrap]
		"scroll":
			return base + " fed=%d" % act.farm_fed
		"fix":
			return base + " fix=%s step=%d carried=%d" % [act.fix_phase, act.fix_step, act.carried]
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
	if act.stage_phase == "brawl":
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
	if act.shuffle_phase != "pick":
		return
	if not _ready_to_act(dt):
		return
	var choice := _intent(act.hats.size(), act.bunny_at, 5000 + act.shuffle_round)
	act._shuffle_action(choice)
	if choice != act.bunny_at:
		_intent_learned(act.bunny_at)

func _drive_press(act: OperaAct, dt: float) -> void:
	# the persona grabs the front candy, carries it to a chute and drops it,
	# sometimes into the wrong one
	if act.belt_items.is_empty():
		return
	if not _ready_to_act(dt):
		return
	var it: Dictionary = act.belt_items[0]
	var want: int = int(it["want"])
	var choice := _intent(act.chutes.size(), want, 7000 + act.candies_done)
	var node := it["node"] as Node3D
	var chute: Vector3 = act.chutes[choice]["pos"] as Vector3
	# carry it there at the persona's hand speed instead of teleporting
	act.sort_held = 0
	var step: float = act.MOVE_SPEED * float(persona["speed"]) * dt
	var to_chute := chute - node.position
	if to_chute.length() > step:
		node.position += to_chute.normalized() * step
		return
	node.position = chute
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
		"find":
			# a child looks around the ward before spotting the ouch star
			var want: int = act.vet_hurt
			var choice := _intent(act.vet_animals.size(), want, 9000)
			if _travel(act, act.vet_animals[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
				act._vet_pick(choice)
				if choice != want:
					_intent_learned(want)
		"carry":
			_travel(act, act.vet_scope.position, dt)
		"xray":
			if not _ready_to_act(dt):
				return
			var bone := _intent(4, act.vet_limb, 9100)
			act._vet_bone(bone)
			if bone != act.vet_limb:
				_intent_learned(act.vet_limb)
		"cast", "coban":
			act._vet_wrap_delta(dt * lerpf(2.0, 4.2, float(persona["speed"])))

func _drive_scroll(act: OperaAct, dt: float) -> void:
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
		# the countdown is a HOLD: the persona grabs the lever after its usual
		# reaction beat and then keeps hold of it
		if act.hold_sim or _ready_to_act(dt):
			act.hold_sim = true
		return
	if act.fix_phase == "valve":
		if _travel(act, act.valve.position, dt) and _ready_to_act(dt):
			act._turn_valve()
		return
	if act.fix_step >= act.slots.size():
		return
	if act.carried >= 0:
		if _travel(act, act.slots[act.fix_step]["pos"] as Vector3, dt) and _ready_to_act(dt):
			act._place_piece()
		return
	var want: int = int(act.slots[act.fix_step]["need"])
	var choice := _intent(act.pieces.size(), want, 4000 + act.fix_step)
	if bool(act.pieces[choice]["placed"]):
		choice = want
	if _travel(act, act.pieces[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
		act._pick_piece(choice)
		if choice != want:
			_intent_learned(want)

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
