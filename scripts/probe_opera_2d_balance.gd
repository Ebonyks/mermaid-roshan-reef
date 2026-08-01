extends SceneTree
## Advisory pacing playtest for the SHIPPING 2D opera career path.
##
## probe_opera_balance.gd measures the legacy 3D engines; this probe drives
## the twelve OperaCareerWorld2D acts with three simulated children and
## reports per-career durations against the rebuild target band (~2 minutes,
## OPERA_2D_REBUILD_2026-08-01.md). Advisory only: it never prints gate
## tokens and is not in the trusted probe lists.

const DT := 0.1
const TIME_CAP := 300.0
## Sim seconds exclude the act-entry narration, curtain-call celebration and
## return transition (~15-20s of real play), and simulated children never
## fumble, explore or re-listen. A 70-150s sim median therefore corresponds
## to the ~2-minute real-play target of OPERA_2D_REBUILD_2026-08-01.md.
const BAND_LO := 70.0
const BAND_HI := 150.0

## Simulated children: listen = seconds spent hearing each phase prompt,
## rt = seconds between discrete actions, err = fraction of clumsy actions,
## drag_px = drag speed, spin = circle speed in radians per second.
const PERSONAS := [
	{"name": "speedy", "listen": 1.2, "rt": 0.7, "err": 0.05, "drag_px": 520.0, "spin": 4.5, "skips_gap": true},
	{"name": "casual", "listen": 2.4, "rt": 1.3, "err": 0.14, "drag_px": 380.0, "spin": 3.6, "skips_gap": false},
	{"name": "dreamy", "listen": 3.2, "rt": 2.0, "err": 0.28, "drag_px": 300.0, "spin": 2.8, "skips_gap": false},
]

var main: ReefMain


func _init() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.game = "opera"
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("type", "show")) == "boss":
			continue
		var career := String(source.get("costume", ""))
		var times: Array[float] = []
		for persona: Dictionary in PERSONAS:
			var outcome := await _play(source, persona)
			times.append(float(outcome.get("time", TIME_CAP)))
			print("BALANCE2D|act=%s|persona=%s|time=%.1f|clumsy=%d" % [
				career, String(persona.get("name", "?")), float(outcome.get("time", TIME_CAP)),
				int(outcome.get("clumsy", 0)),
			])
		times.sort()
		var median := times[times.size() / 2]
		var verdict := "ok"
		if median > BAND_HI:
			verdict = "longer"
		elif median < BAND_LO:
			verdict = "brisk"
		if times[times.size() - 1] >= TIME_CAP:
			verdict = "capped"
		print("BALANCE2D|%s|summary med=%.1f lo=%.1f hi=%.1f verdict=%s" % [
			career, median, times[0], times[times.size() - 1], verdict,
		])
	print("BALANCE2D|done")
	quit()


func _play(source: Dictionary, persona: Dictionary) -> Dictionary:
	var config := source.duplicate(true)
	config["force_2d"] = true
	var act := OperaAct.new()
	get_root().add_child(act)
	act.process_mode = Node.PROCESS_MODE_DISABLED
	act.start(main, config, Callable())
	await process_frame
	var world := act.career_world_2d
	if world == null:
		act.queue_free()
		return {"time": TIME_CAP, "clumsy": 0}
	world.process_mode = Node.PROCESS_MODE_DISABLED

	var time := 0.0
	var clumsy := 0
	var listen_left := float(persona.get("listen", 2.0))
	var action_wait := 0.0
	var err_acc := 0.0
	var stroke_t := 0.0
	var last_phase := -1
	var rt := float(persona.get("rt", 1.3))
	while act.state == "play" and time < TIME_CAP:
		time += DT
		act._process(DT)
		world._process(DT)
		if world.phase_index != last_phase:
			last_phase = world.phase_index
			listen_left = float(persona.get("listen", 2.0))
			action_wait = 0.0
			stroke_t = 0.0
		if world.reveal_t > 0.0:
			continue
		if listen_left > 0.0:
			listen_left -= DT
			continue
		if world.phase_gap > 0.0 and not bool(persona.get("skips_gap", false)):
			continue
		if world.phase_index >= world.phases.size():
			continue
		var phase := world.phases[world.phase_index] as Dictionary
		var mode := String(phase.get("mode", "tap"))
		# children drag in short strokes with pauses, and re-grip long holds
		stroke_t += DT
		var stroke_active := fmod(stroke_t, 0.7 + rt * 0.5) < 0.7
		var hold_active := fmod(stroke_t, 1.3 + 0.35) < 1.3
		match mode:
			"hold":
				if hold_active:
					world._on_gesture("hold", DT, 1.0)
			"swipe":
				if stroke_active:
					world._on_gesture("swipe", float(persona.get("drag_px", 380.0)) * DT / 150.0, 1.0)
			"circle":
				if stroke_active:
					world._on_gesture("circle", float(persona.get("spin", 3.6)) * DT / TAU, 1.0)
			_:
				action_wait -= DT
				if action_wait <= 0.0:
					# timing needs a green-window pass (~1.4s sweep); choice
					# needs a re-scan after the target hops to a new lane
					match mode:
						"timing":
							action_wait = maxf(rt, 1.4)
						"choice":
							action_wait = maxf(rt, 1.1)
						_:
							action_wait = rt
					err_acc += float(persona.get("err", 0.1))
					var miss := err_acc >= 1.0
					if miss:
						err_acc -= 1.0
						clumsy += 1
					match mode:
						"tap":
							world._on_gesture("tap", 1.0, 1.0)
						"choice":
							world._on_gesture("choice", 0.24 if miss else 1.0, 0.0 if miss else 1.0)
						"timing":
							world._on_gesture("timing", 0.32 if miss else 1.0, 0.32 if miss else 1.0)
						"bop":
							world._on_gesture("bop", 0.12 if miss else 1.0, 0.2 if miss else 1.0)
						_:
							world._on_gesture("tap", 1.0, 1.0)
	var done_time := time if act.state != "play" else TIME_CAP
	act.cancel()
	await process_frame
	await process_frame
	return {"time": done_time, "clumsy": clumsy}
