extends SceneTree
## Advisory pacing playtest for the SHIPPING 2D opera career path.
##
## This probe drives all fifteen OperaCareerWorld2D acts with three simulated
## children, walking to and opening every object before a real gesture.
## reports per-career durations against the rebuild target band (~2 minutes,
## OPERA_2D_REBUILD_2026-08-01.md). Advisory only: it never prints gate
## tokens and is not in the trusted probe lists.

const Child := preload("res://scripts/probe_opera_child_driver.gd")
const DT := 1.0 / 30.0
const TIME_CAP := 300.0
## Sim seconds exclude the act-entry narration, curtain-call celebration and
## return transition (~15-20s of real play), and simulated children never
## fumble, explore or re-listen. A 70-150s sim median therefore corresponds
## to the ~2-minute real-play target of OPERA_2D_REBUILD_2026-08-01.md.
const BAND_LO := 70.0
const BAND_HI := 150.0

## Simulated children: listen = seconds spent hearing each phase prompt,
## rt = seconds between discrete actions. Continuous gestures follow the
## pictured path at one shared speed; these are pacing scenarios, not a model
## of mistakes, exploration or child comprehension. Geology is a fast input
## traversal and its result is diagnostic only.
const PERSONAS := [
	{"name": "speedy", "listen": 1.2, "rt": 0.7},
	{"name": "casual", "listen": 2.4, "rt": 1.3},
	{"name": "dreamy", "listen": 3.2, "rt": 2.0},
]

var main: ReefMain


func _init() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.game = "opera"
	for live_index: int in OperaHouse.LIVE_ACT_INDICES:
		var source: Dictionary = OperaHouse.ACTS[live_index]
		var career := String(source.get("costume", ""))
		var times: Array[float] = []
		for persona: Dictionary in PERSONAS:
			var outcome := await _play(source, persona)
			times.append(float(outcome.get("time", TIME_CAP)))
			print("BALANCE|canvas|act=%s|persona=%s|time=%.1f|clumsy=%d" % [
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
		print("BALANCE|canvas|%s|summary med=%.1f lo=%.1f hi=%.1f verdict=%s" % [
			career, median, times[0], times[times.size() - 1], verdict,
		])
	print("BALANCE|canvas|done")
	quit()


func _play(source: Dictionary, persona: Dictionary) -> Dictionary:
	main.save_data["opera_phase_checkpoints"] = {}
	main.save_data["opera_performance_checkpoints"] = {}
	main.save_data["opera_geology_checkpoint"] = {}
	main.save_data["teacher_lesson_checkpoint"] = {}
	var config := source.duplicate(true)
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
	var child := Child.new()
	var listen_left := 0.0
	var last_phase := -1
	while act.state == "play" and time < TIME_CAP:
		time += DT
		if world.phase_index != last_phase:
			last_phase = world.phase_index
			listen_left = float(persona.get("listen", 2.0))
		if listen_left > 0.0:
			listen_left -= DT
		else:
			child.step(world, DT, float(persona.get("rt", 1.2)))
		world.surface._process(DT)
		world._process(DT)
		for hotspot: OperaWorldHotspot2D in world.station_nodes:
			hotspot._process(DT)
		act._process(DT)
	if act.state == "play":
		var phase := String(world.phases[world.phase_index]["name"]) if world.phase_index < world.phases.size() else "curtain"
		print("BALANCE|canvas|capped_phase=%s/%s|progress=%.3f" % [world.career_id, phase, world.phase_progress])
	var done_time := time if act.state != "play" else TIME_CAP
	act.cancel()
	await process_frame
	await process_frame
	return {"time": done_time, "clumsy": clumsy}
