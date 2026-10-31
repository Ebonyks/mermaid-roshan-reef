extends SceneTree
## Advisory pacing playtest for the SHIPPING 2D opera career path.
##
## This probe visits the live OperaCareerWorld2D roster with three simulated
## children and
## reports per-career durations against the rebuild target band (~2 minutes,
## OPERA_2D_REBUILD_2026-08-01.md). Advisory only: it never prints gate
## tokens and is not in the trusted probe lists.

const DT := 0.1
const TIME_CAP := 300.0
## Specialized surfaces need their own child-input policy. Never turn an
## unsupported verb into a generic tap and publish a manufactured duration.
const SUPPORTED_MODES: Array[String] = [
	"lens", "catch", "hold", "swipe", "circle", "tap", "oven", "choice",
	"timing", "bop", "talk", "pourt", "echo", "clue_board", "crown_chest",
	"garden_plant", "teacher_pattern", "teacher_count", "teacher_add", "teacher_match",
]
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
var fixture_save_data: Dictionary = {}


func _init() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	main._save_state = SaveState.new(main,
		"user://opera_balance_probe_%d.json" % OS.get_process_id())
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.game = "opera"
	main.process_mode = Node.PROCESS_MODE_DISABLED
	fixture_save_data = main.save_data.duplicate(true)
	var measured := 0
	var capped := 0
	var unmeasured := 0
	print("BALANCE|ROSTER|acts=%d|personas=%d|cap=%.1f" % [
		OperaHouse.LIVE_ACT_INDICES.size(), PERSONAS.size(), TIME_CAP])
	for live_index: int in OperaHouse.LIVE_ACT_INDICES:
		var source: Dictionary = OperaHouse.ACTS[live_index]
		var career := String(source.get("costume", ""))
		var times: Array[float] = []
		var incomplete := 0
		for persona: Dictionary in PERSONAS:
			var outcome := await _play(source, persona)
			var status := String(outcome.get("status", "NOT_MEASURED"))
			if status == "PASS":
				times.append(float(outcome["time"]))
				measured += 1
			else:
				incomplete += 1
				if status == "CAPPED":
					capped += 1
				else:
					unmeasured += 1
			print("BALANCE|canvas|act=%s|persona=%s|time=%s|elapsed=%.1f|clumsy=%d|status=%s|reason=%s" % [
				career, String(persona.get("name", "?")),
				"%.1f" % float(outcome["time"]) if status == "PASS" else "not_measured",
				float(outcome.get("elapsed", 0.0)), int(outcome.get("clumsy", 0)),
				status, String(outcome.get("reason", "")),
			])
		if times.is_empty():
			print("BALANCE|canvas|%s|summary verdict=not_measured|completed=0|incomplete=%d" % [career, incomplete])
			continue
		times.sort()
		var median := times[times.size() / 2]
		var verdict := "ok"
		if median > BAND_HI:
			verdict = "longer"
		elif median < BAND_LO:
			verdict = "brisk"
		if incomplete > 0:
			verdict = "partial"
		print("BALANCE|canvas|%s|summary med=%.1f lo=%.1f hi=%.1f verdict=%s" % [
			career, median, times[0], times[times.size() - 1], verdict,
		])
	var result := "PASS" if capped == 0 and unmeasured == 0 else (
		"CAPPED" if capped > 0 else "NOT_MEASURED")
	print("BALANCE|RESULT|%s|measured=%d|capped=%d|not_measured=%d|expected=%d" % [
		result, measured, capped, unmeasured,
		OperaHouse.LIVE_ACT_INDICES.size() * PERSONAS.size()])
	quit()


func _play(source: Dictionary, persona: Dictionary) -> Dictionary:
	# Performance/lesson checkpoints written by one persona must not make the
	# next persona resume at the curtain call and report a false zero duration.
	main.save_data = fixture_save_data.duplicate(true)
	main.opera_stars = 0
	var config := source.duplicate(true)
	var act := OperaAct.new()
	get_root().add_child(act)
	act.process_mode = Node.PROCESS_MODE_DISABLED
	act.start(main, config, Callable())
	await process_frame
	var world := act.career_world_2d
	if world == null:
		act.queue_free()
		return {"status": "NOT_MEASURED", "reason": "world_unavailable", "clumsy": 0}
	world.process_mode = Node.PROCESS_MODE_DISABLED

	var time := 0.0
	var clumsy := 0
	var listen_left := float(persona.get("listen", 2.0))
	var action_wait := 0.0
	var err_acc := 0.0
	var stroke_t := 0.0
	var last_phase := -1
	var rt := float(persona.get("rt", 1.3))
	var unsupported := ""
	while act.state == "play" and time < TIME_CAP:
		time += DT
		act._process(DT)
		world._process(DT)
		for hotspot: OperaWorldHotspot2D in world.station_nodes:
			hotspot._process(DT)
		if world.task_open and world.surface != null:
			world.surface._process(DT)
		if world.phase_index != last_phase:
			last_phase = world.phase_index
			listen_left = float(persona.get("listen", 2.0))
			action_wait = 0.0
			stroke_t = 0.0
		if world.reveal_t > 0.0:
			continue
		if world.phase_advance_pending:
			continue
		if listen_left > 0.0:
			listen_left -= DT
			continue
		if world.phase_gap > 0.0 and not bool(persona.get("skips_gap", false)):
			continue
		if not world.task_open:
			if not world.interaction_requested and not world.hotspot_opening:
				world._on_hotspot_pressed(world.armed_station)
			continue
		if world.phase_index >= world.phases.size():
			continue
		var phase := world.phases[world.phase_index] as Dictionary
		var mode := String(phase.get("mode", "tap"))
		if mode not in SUPPORTED_MODES:
			unsupported = "unsupported_mode:%s/%s" % [String(source.get("costume", "")), mode]
			break
		if mode == "talk":
			continue
		if mode == "pourt":
			if not world.surface.pour_hold:
				world.surface._press(world.surface._pour_pitcher_rect().get_center())
			continue
		if mode.begins_with("teacher_"):
			action_wait -= DT
			if action_wait <= 0.0:
				action_wait = rt
				var teacher := world.surface as OperaTeacherSurface
				var answer_at := Vector2.INF
				if teacher.lesson_kind() == "add" and not teacher.joined:
					answer_at = OperaTeacherSurface.JOIN_CENTER
				elif teacher.join_t <= 0.0:
					for index in range(teacher.counted.size()):
						if not teacher.counted[index]:
							answer_at = teacher.counter_position(index)
							break
					if not answer_at.is_finite() and teacher.can_answer():
						answer_at = teacher.choice_rect(teacher.answer_index()).get_center()
				if answer_at.is_finite():
					teacher._press(answer_at)
					teacher._release(answer_at)
			continue
		if mode == "lens":
			# sweep the magnifier toward the next sparkle at a child's drag
			# speed — hunting time is real time
			world.lens_demo = false
			for index in range(world.lens_clues.size()):
				if not world.lens_found[index]:
					var step := float(persona.get("drag_px", 380.0)) * DT
					world.lens_pos = world.lens_pos.move_toward(world.lens_clues[index], step)
					break
			continue
		if mode == "catch" and world.nursery_catch != null:
			# steer the cradle under the lowest falling baby, child-style
			var target := world.nursery_catch.lowest_baby_x()
			world.nursery_catch.steer_to(target if target >= 0.0 else 0.5)
			world.nursery_catch._process(DT)
			continue
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
					action_wait = rt
					# timing needs a green-window pass (~1.4s sweep); choice
					# needs a re-scan after the target hops to a new lane
					match mode:
						"timing":
							action_wait = maxf(rt, 1.4)
						"oven":
							# poll the thermometer often; the grab is gated below
							action_wait = 0.15
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
						"echo":
							if world.surface.echo_listening:
								var verse: Array = OperaGestureSurface.ECHO_VERSES[world.surface.echo_verse]
								var star := int(verse[world.surface.echo_input_i])
								var at := world.surface._echo_star_center(star)
								world.surface._press(at)
								world.surface._release(at)
						"clue_board":
							var home := world.surface._clue_token_rect().get_center()
							var target := world.surface._clue_target_rect(world.surface.clue_index).get_center()
							world.surface._press(home)
							world.surface._drag(target)
							world.surface._release(target)
						"crown_chest":
							var at := world.surface._crown_handle_rect().get_center()
							world.surface._press(at)
							world.surface._release(at)
						"garden_plant":
							var home := world.surface._garden_seed_rect().get_center()
							var target := world.surface._garden_hole_point(world.surface.garden_planted)
							world.surface._press(home)
							world.surface._drag(target)
							world.surface._release(target)
						"tap":
							# free placement: every tap is a placed mark; the
							# persona's "miss" is just a mark near the edge
							var tap_at := world.surface.size * 0.5 if not miss else Vector2(8, 8)
							world.surface._press(tap_at)
							world.surface._release(tap_at)
						"oven":
							# a clumsy persona peeks early; everyone grabs the
							# mitt once the thermometer reaches the gold band
							var mitt := world.surface.size * Vector2(0.42, 0.73)
							if miss and world.surface.oven_t < 0.40:
								world.surface._press(mitt)
								world.surface._release(mitt)
								action_wait = maxf(rt, 0.6)
							elif world.surface.oven_t >= 0.5:
								world.surface._press(mitt)
								world.surface._release(mitt)
								action_wait = maxf(rt, 0.8)
						"choice":
							world._on_gesture("choice", 0.24 if miss else 1.0, 0.0 if miss else 1.0)
						"timing":
							world._on_gesture("timing", 0.32 if miss else 1.0, 0.32 if miss else 1.0)
						"bop":
							# strike a roaming imp (or a far corner on a miss)
							var aim := Vector2(6, 6)
							if not miss:
								for imp: Dictionary in world.combat_imps:
									if not bool(imp.get("popped", false)):
										var imp_node := imp.get("node") as TextureRect
										if imp_node != null:
											aim = imp_node.position + imp_node.size * 0.5
										break
							world.swipe_stroke += 1
							world._combat_strike(aim, aim)
						_:
							world._on_gesture("tap", 1.0, 1.0)
	var completed := time > 0.0 and (act.state == "won" or act.state == "done")
	var status := "PASS" if completed else ("NOT_MEASURED" if unsupported != "" else "CAPPED")
	var reason := "completed" if completed else (unsupported if unsupported != "" else "time_cap")
	if status == "CAPPED" and world.phase_index < world.phases.size():
		reason += ":phase=%d,mode=%s,progress=%.6f,goal=%.6f" % [
			world.phase_index, String(world.phases[world.phase_index].get("mode", "")),
			world.phase_progress, float(world.phases[world.phase_index].get("goal", 0.0))]
	act.cancel()
	await process_frame
	await process_frame
	return {"status": status, "time": time if completed else null,
		"elapsed": time, "clumsy": clumsy, "reason": reason}
