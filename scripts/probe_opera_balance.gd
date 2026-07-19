extends SceneTree
# Advisory balance playtest for the Pearl Opera House. Every act (except the
# kart race and the DanceEngine concert, which have their own tuned engines)
# is played TEN times by simulated children — personas with real reaction
# delays, travel speeds, wandering and wrong-tap rates — by pumping
# OperaAct._process() with a fixed timestep. Prints one BALANCE| line per run
# plus a per-act summary with a verdict against the 55-140s fun band
# (target: every act is a 1-2 minute performance).
# This probe is ADVISORY: it prints metrics and never the gate's fail tokens.

const DT := 0.1
const TIME_CAP := 240.0
const BAND_LO := 55.0
const BAND_HI := 140.0

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
var wrong_pending := -1            # a queued wrong choice (mistake) to commit first
var echo_key := -1                 # sticky echo intent: (round, pos) being danced
var echo_target := -1

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
	match act.kind:
		"echo":
			return base + " echo=%s round=%d pos=%d dwell=%.2f" % [act.echo_phase, act.echo_round, act.echo_pos, act.pad_dwell]
		"boss":
			var bphase := String(act.boss.get("phase", "?"))
			var bdist := ((act.boss["node"] as Node3D).position).distance_to(act.player_pos) if act.boss.has("node") else -1.0
			return base + " boss=%s hp=%d lant=%d dist=%.1f" % [bphase, int(act.boss.get("hp", -1)), act.lantern_i, bdist]
		"order":
			return base + " order=%s step=%d brush=%d" % [act.order_phase, act.step, act.brush_loaded]
		"press":
			return base + " candies=%d busy=%.2f" % [act.candies_done, act.press_busy]
		"shuffle":
			return base + " shuffle=%s round=%d" % [act.shuffle_phase, act.shuffle_round]
		"doctor":
			return base + " step=%d" % act.doc_step
		"scroll":
			return base + " fed=%d" % act.farm_fed
		"fix":
			return base + " fix=%s step=%d carried=%d" % [act.fix_phase, act.fix_step, act.carried]
	return base

func _play_act(cfg: Dictionary) -> float:
	done = false
	mistakes = 0
	wait_t = 1.0
	wrong_pending = -1
	echo_key = -1
	echo_target = -1
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
		for g in act.gremlins:
			if not bool(g["popped"]):
				target = g["pos"] as Vector3
				found = true
				break
		if found and _travel(act, target, dt) and _ready_to_act(dt):
			act._brawl_action()
		return
	match act.kind:
		"order":
			_drive_order(act, dt)
		"echo":
			_drive_echo(act, dt)
		"shuffle":
			_drive_shuffle(act, dt)
		"press":
			_drive_press(act, dt)
		"doctor":
			_drive_doctor(act, dt)
		"scroll":
			_drive_scroll(act, dt)
		"fix":
			_drive_fix(act, dt)
		"boss":
			_drive_boss(act, dt)

func _maybe_wrong(count: int, want: int) -> int:
	# a persona sometimes reaches for the wrong thing first; the engine's
	# gentle bounce costs time, which is exactly what we want to measure
	if wrong_pending >= 0:
		var w := wrong_pending
		wrong_pending = -1
		return w
	if randf() < float(persona["err"]):
		mistakes += 1
		wrong_pending = want
		return (want + 1 + randi() % maxi(1, count - 1)) % count
	return want

func _drive_order(act: OperaAct, dt: float) -> void:
	if act.order_phase == "stir":
		if _travel(act, act.goal.position, dt) and _ready_to_act(dt):
			act._stir_action()
		return
	if act.order_flow == "carry_paint" and act.brush_loaded >= 0:
		_travel(act, act.canvas_pos, dt)   # engine paints on proximity
		return
	if act.step >= act.order_steps.size():
		return
	var want: int = act.order_steps[act.step]
	var choice := _maybe_wrong(act.pads.size(), want)
	if _travel(act, act.pads[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
		act._act_action(choice)

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
	if act.shuffle_phase != "pick":
		return
	var choice := _maybe_wrong(act.hats.size(), act.bunny_at)
	if _travel(act, act.hats[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
		act._act_action(choice)

func _drive_press(act: OperaAct, dt: float) -> void:
	if act.press_busy > 0.0 or act.candy_node == null:
		return
	if not _ready_to_act(dt):
		return
	if randf() < float(persona["err"]):
		mistakes += 1
		act.press_x = 0.9   # a mistimed jab
		act._press_action()
		return
	if absf(act.press_x) <= act.press_zone * 0.9:
		act._press_action()
	else:
		wait_t = 0.0   # keep watching the slider

func _drive_doctor(act: OperaAct, dt: float) -> void:
	if act.doc_step >= act.doc_targets.size():
		return
	var choice := _maybe_wrong(act.doc_targets.size(), act.doc_step)
	if _travel(act, act.doc_targets[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
		act._doctor_action(choice)

func _drive_scroll(act: OperaAct, dt: float) -> void:
	if act.farm_toss_cool > 0.0:
		return
	var near := false
	for pig in act.piggies:
		if not bool(pig["fed"]) and absf(float(pig["sx"]) - 250.0) < 150.0:
			near = true
			break
	if near and _ready_to_act(dt):
		act._toss_action()

func _drive_fix(act: OperaAct, dt: float) -> void:
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
	var choice := _maybe_wrong(act.pieces.size(), want)
	if bool(act.pieces[choice]["placed"]):
		choice = want
	if _travel(act, act.pieces[choice]["pos"] as Vector3, dt) and _ready_to_act(dt):
		act._pick_piece(choice)

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
