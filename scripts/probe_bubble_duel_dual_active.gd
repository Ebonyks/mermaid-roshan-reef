extends "res://scripts/probe_bubble_duel_cast.gd"
## Test-only two active touch policies. No fighter position/velocity/bubble edits.
var active_stats: Dictionary = {}


func _tour(index: int, seen: Dictionary) -> bool:
	var before := cast_cases.size()
	var result := super._tour(index, seen)
	if cast_cases.size() > before:
		cast_cases.back()["winner"] = active_stats.get("winner", -2)
		cast_cases.back()["dual_active"] = active_stats.duplicate(true)
	var file := FileAccess.open(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT") + ".cast.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks": checked, "failures": bad, "cases": cast_cases, "pairs": pairs.keys(), "fixture": "Two independent asymmetric touch pulse/chase policies; actual pad input only. Initial purchased powers through real buttons. No position/velocity/bubble fixtures inside any full bout. Not human preference or child acceptance."}, "  "))
	file.close()
	return result


func _play(d: BubbleDuelOverlay, _player: int, run: int) -> bool:
	var down: Array[bool] = [false, false]
	var release_until: Array[float] = [0.0, 0.0]
	var owned_frames: Array[int] = [0, 0]
	var presses: Array[int] = [0, 0]
	var travel: Array[float] = [0.0, 0.0]
	var dt := 1.0 / (30.0 if run % 2 else 60.0)
	for player: int in range(2):
		if String((d.fighters[player]["profile"] as Dictionary)["gear"]) not in ["classic", "tidewing"]:
			_tap(d.power_button if player == 0 else d.second_power_button)
	active_stats = {"winner": -2}
	for frame: int in range(4800):
		if d.mode == Duel.Mode.CELEBRATE:
			var gone0 := (d.fighters[0]["bubbles"] as Array).is_empty()
			var gone1 := (d.fighters[1]["bubbles"] as Array).is_empty()
			active_stats = {"winner": -1 if gone0 and gone1 else (1 if gone0 else 0), "frames": frame, "seconds": frame * dt, "dt": dt, "owned_control_frames": owned_frames, "presses": presses, "travel_pixels": travel}
			_check("both active policies owned their real pad", owned_frames[0] > 0 and owned_frames[1] > 0)
			for player: int in range(2):
				if down[player]: _finger(d, 10 + player, d.Duo.PADS[player].get_center(), false)
			return gone0 or gone1
		var time := frame * dt
		var previous: Array[Vector2] = [d.fighters[0]["position"], d.fighters[1]["position"]]
		for player: int in range(2):
			var fighter: Dictionary = d.fighters[player]
			var other := 1 - player
			var bubbles: Array = d.fighters[other]["bubbles"]
			if bubbles.is_empty(): continue
			var position: Vector2 = fighter["position"]
			var target := d.duo.bubble_at(other, int(bubbles[0]))
			var contact := d.appearance.contact(fighter["profile"], false, d.active_time)
			var facing := float(fighter["facing"])
			var goal := target.x - contact.x * facing
			var turn := 0.0
			# Face the fin toward a wall-side target using an actual pad gesture.
			# A chase policy that only pushes into the wall cannot align its fin.
			if goal < 225.0 - 28.0 or goal > 1055.0 + 28.0:
				facing = -facing
				goal = target.x - contact.x * facing
				turn = facing
			var error := clampf(goal, 225.0, 1055.0) - position.x
			var period := 1.75 + float(run % 5) * 0.04 if player == 0 else 2.25 + float(run % 7) * 0.035
			var phase := fposmod(time + float(player) * 0.43, period)
			var thrust := phase < period * 0.56
			if down[player] and ((position.y + contact.y < target.y - 22.0 and absf(error) < 35.0) or (position.y <= 271.0 and phase > 0.38)):
				release_until[player] = time + 0.85
			if time < release_until[player]: thrust = false
			var pad: Rect2 = d.Duo.PADS[player]
			var axis := clampf(error / 65.0, -1.0, 1.0)
			if turn != 0.0: axis = turn * 0.2
			var point := pad.get_center() + Vector2(axis * 105.0, 0)
			if thrust and not down[player]:
				_finger(d, 10 + player, point, true)
				down[player] = true
				presses[player] += 1
			elif thrust:
				_drag(d, 10 + player, point)
			elif down[player]:
				_finger(d, 10 + player, point, false)
				down[player] = false
			if d.duo_touch_owners.get(10 + player, -1) == player: owned_frames[player] += 1
		d._process(dt)
		for player: int in range(2): travel[player] += (d.fighters[player]["position"] as Vector2).distance_to(previous[player])
	for player: int in range(2):
		if down[player]: _finger(d, 10 + player, d.Duo.PADS[player].get_center(), false, true)
	active_stats = {"winner": -2, "frames": 4800, "seconds": 4800 * dt, "owned_control_frames": owned_frames, "presses": presses, "travel_pixels": travel, "classification": "Incomplete policy trial; no pass credit. Inspect trajectories before attributing a game defect."}
	print("BUBBLEACTIVE|incomplete|", run, "|", active_stats, "|", d.fighters)
	return false
