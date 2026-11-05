class_name BubbleDuelTwoPlayer
extends RefCounted
## Simultaneous local match. Temporary state stays on the owning overlay.
const PADS: Array[Rect2] = [Rect2(164, 600, 254, 110), Rect2(862, 600, 254, 110)]
const LEFT_KEYS: Array[int] = [KEY_A, KEY_LEFT]
const RIGHT_KEYS: Array[int] = [KEY_D, KEY_RIGHT]
const UP_KEYS: Array[int] = [KEY_W, KEY_UP]
const POWER_KEYS: Array[int] = [KEY_S, KEY_DOWN]
var host: BubbleDuelOverlay


func _init(owner_overlay: BubbleDuelOverlay) -> void:
	host = owner_overlay


func start() -> void:
	host.fighters.clear()
	host.duo_touch_owners.clear()
	host.duo_keys.clear()
	host.duo_pops.clear()
	for player: int in range(2):
		host.fighters.append({"profile": host.Shop.profile(host.main, player),
			"position": Vector2(350 if player == 0 else 930, 480), "velocity": Vector2.ZERO,
			"axis": Vector2.ZERO, "facing": 1.0 if player == 0 else -1.0,
			"bubbles": [0, 1], "armed": false, "held": false, "glow": 100.0,
			"power_time": 0.0, "recover": 0.0, "hold_time": 0.0, "held_by": -1,
			"slow_time": 0.0, "slow_by": -1, "pull_time": 0.0, "pull_by": -1,
			"pull": Vector2.ZERO, "shots": []})


func input(event: InputEvent) -> bool:
	if event is InputEventKey:
		var code := int(event.physical_keycode if event.physical_keycode != 0 else event.keycode)
		if code not in LEFT_KEYS + RIGHT_KEYS + UP_KEYS + POWER_KEYS:
			return false
		if event.echo:
			return true
		host.duo_keys[code] = event.pressed
		for player: int in range(2):
			if code == POWER_KEYS[player] and event.pressed:
				activate(player)
		return true
	if event is InputEventScreenTouch:
		if event.pressed:
			for player: int in range(2):
				if PADS[player].has_point(event.position) and player not in host.duo_touch_owners.values():
					host.duo_touch_owners[event.index] = player
					_steer(player, event.position)
					return true
		elif host.duo_touch_owners.has(event.index):
			var player := int(host.duo_touch_owners[event.index])
			host.duo_touch_owners.erase(event.index)
			if event.canceled:
				clear_player(player)
			else:
				host.fighters[player]["held"] = false
				host.fighters[player]["axis"] = Vector2.ZERO
			return true
	elif event is InputEventScreenDrag and host.duo_touch_owners.has(event.index):
		_steer(int(host.duo_touch_owners[event.index]), event.position)
		return true
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			for player: int in range(2):
				if PADS[player].has_point(event.position) and player not in host.duo_touch_owners.values():
					host.duo_touch_owners[-100] = player
					_steer(player, event.position)
					return true
		elif host.duo_touch_owners.has(-100):
			var player := int(host.duo_touch_owners[-100])
			host.duo_touch_owners.erase(-100)
			host.fighters[player]["held"] = false
			host.fighters[player]["axis"] = Vector2.ZERO
			return true
	elif event is InputEventMouseMotion and host.duo_touch_owners.has(-100):
		_steer(int(host.duo_touch_owners[-100]), event.position)
		return true
	return false


func _steer(player: int, at: Vector2) -> void:
	var fighter: Dictionary = host.fighters[player]
	var axis := Vector2(clampf((at.x - PADS[player].get_center().x) / 105.0, -1.0, 1.0), -1.0)
	fighter["axis"] = axis
	fighter["held"] = true
	fighter["armed"] = true
	if absf(axis.x) > 0.1:
		fighter["facing"] = signf(axis.x)


func clear_player(player: int) -> void:
	if host.fighters.size() != 2:
		return
	var fighter: Dictionary = host.fighters[player]
	fighter["held"] = false
	fighter["armed"] = false
	fighter["axis"] = Vector2.ZERO
	fighter["velocity"] = Vector2.ZERO
	fighter["power_time"] = 0.0
	(fighter["shots"] as Array).clear()
	for other: Dictionary in host.fighters:
		for effect: String in ["hold", "slow", "pull"]:
			var owner_key := "held_by" if effect == "hold" else effect + "_by"
			if int(other[owner_key]) == player:
				other[effect + "_time"] = 0.0
				other[owner_key] = -1


func flush() -> void:
	host.duo_touch_owners.clear()
	host.duo_keys.clear()
	for player: int in range(host.fighters.size()):
		clear_player(player)


func bubble_at(player: int, side: int) -> Vector2:
	return (host.fighters[player]["position"] as Vector2) + Vector2(-32 if side == 1 else 32, -98)


func activate(player: int) -> bool:
	if host.mode != host.Mode.VERSUS or host.fighters.size() != 2:
		return false
	var fighter: Dictionary = host.fighters[player]
	var profile: Dictionary = fighter["profile"]
	var gear := String(profile["gear"])
	var definition := host.Shop.item(gear)
	if gear in ["classic", "tidewing"] or (fighter["bubbles"] as Array).is_empty() \
			or float(fighter["recover"]) > 0.0 or float(fighter["glow"]) < float(definition["use"]) \
			or (gear == "rainbow" and not (fighter["shots"] as Array).is_empty()):
		return false
	fighter["glow"] = float(fighter["glow"]) - float(definition["use"])
	fighter["armed"] = true
	fighter["power_time"] = 1.0
	var other: Dictionary = host.fighters[1 - player]
	match gear:
		"moonpearl":
			fighter["power_time"] = 1.5
		"swiftconch":
			fighter["power_time"] = 0.45
		"rainbow":
			var point := host.appearance.tool_tip(profile, fighter["position"], float(fighter["facing"]), bool(fighter["held"]), host.active_time)
			(fighter["shots"] as Array).append({"position": point, "life": 2.5})
		"kelp":
			other["pull"] = ((fighter["position"] as Vector2) - (other["position"] as Vector2)).normalized() * 160.0
			other["pull_time"] = 0.7
			other["pull_by"] = player
		"lullaby":
			other["glow"] = 0.0
			other["slow_time"] = 2.0
			other["slow_by"] = player
		"squid":
			other["hold_time"] = 1.33
			other["held_by"] = player
			other["velocity"] = Vector2.ZERO
	host.main._audio_ref().pop(1)
	host._refresh_power()
	return true


func tick(delta: float) -> void:
	if host.fighters.size() != 2:
		return
	var previous: Array[Vector2] = [host.fighters[0]["position"], host.fighters[1]["position"]]
	for player: int in range(2):
		_integrate(player, delta)
	var hits: Array[Dictionary] = []
	for player: int in range(2):
		var fighter: Dictionary = host.fighters[player]
		var other := 1 - player
		var point: Vector2 = fighter["position"]
		if bool(fighter["armed"]) and not bool(fighter["held"]) and point.y > previous[player].y \
				and not (fighter["bubbles"] as Array).is_empty() and float(fighter["recover"]) <= 0.0:
			var contact := host.appearance.contact(fighter["profile"], false, host.active_time)
			contact.x *= float(fighter["facing"])
			for side: int in host.fighters[other]["bubbles"]:
				var from := previous[player] + contact - (previous[other] + Vector2(-32 if side == 1 else 32, -98))
				var to := point + contact - bubble_at(other, side)
				if float(host.fighters[other]["recover"]) <= 0.0 and from.y < 0.0 and to.y > from.y \
						and Geometry2D.get_closest_point_to_segment(Vector2.ZERO, from, to).length_squared() <= 33.0 * 33.0:
					hits.append({"target": other, "side": side, "source": player})
					break
		_projectiles(player, delta, previous, hits)
	# Resolve both sweeps together: a simultaneous hit cannot favour player one.
	for hit: Dictionary in hits:
		var target := int(hit["target"])
		var bubbles: Array = host.fighters[target]["bubbles"]
		var side := int(hit["side"])
		if side in bubbles:
			bubbles.erase(side)
			host.duo_pops.append({"position": bubble_at(target, side), "time": 0.32})
			host.main._audio_ref().pop(1)
			var source: Dictionary = host.fighters[int(hit["source"])]
			var velocity: Vector2 = source["velocity"]
			velocity.y = -150.0
			source["velocity"] = velocity
	var gone0 := (host.fighters[0]["bubbles"] as Array).is_empty()
	var gone1 := (host.fighters[1]["bubbles"] as Array).is_empty()
	if gone0 or gone1:
		host._complete_two_player(-1 if gone0 and gone1 else (1 if gone0 else 0))


func _integrate(player: int, delta: float) -> void:
	var fighter: Dictionary = host.fighters[player]
	var axis: Vector2 = fighter["axis"]
	var keyboard := Vector2(float(bool(host.duo_keys.get(RIGHT_KEYS[player], false))) - float(bool(host.duo_keys.get(LEFT_KEYS[player], false))), -float(bool(host.duo_keys.get(UP_KEYS[player], false))))
	if keyboard != Vector2.ZERO:
		axis = keyboard
		fighter["held"] = keyboard.y < 0.0
		fighter["armed"] = true
	elif player not in host.duo_touch_owners.values():
		fighter["held"] = false
		axis = Vector2.ZERO
	if absf(axis.x) > 0.1:
		fighter["facing"] = signf(axis.x)
	for timer: String in ["recover", "hold_time", "slow_time", "pull_time", "power_time"]:
		fighter[timer] = maxf(0.0, float(fighter[timer]) - delta)
	if float(fighter["recover"]) > 0.0:
		return
	if not bool(fighter["armed"]) and float(fighter["pull_time"]) <= 0.0:
		return
	fighter["glow"] = minf(100.0, float(fighter["glow"]) + 22.0 * delta)
	if float(fighter["hold_time"]) > 0.0:
		return
	var floor_y := maxf(490.0, 588.0 - host.appearance.bounds(fighter["profile"], false, host.active_time).end.y)
	var velocity: Vector2 = fighter["velocity"]
	var gear := String((fighter["profile"] as Dictionary)["gear"])
	var pace := 0.35 if float(fighter["slow_time"]) > 0.0 else 1.0
	velocity.x = axis.x * 550.0 * pace
	if gear == "swiftconch" and float(fighter["power_time"]) > 0.0:
		velocity.x = float(fighter["facing"]) * 1000.0
	if bool(fighter["held"]):
		velocity.y = -330.0 * pace
	else:
		var gravity := 560.0
		if gear == "moonpearl" and float(fighter["power_time"]) > 0.0 and float(fighter["glow"]) > 0.0:
			gravity = 0.0
			velocity.y = move_toward(velocity.y, 0.0, 1100.0 * delta)
			fighter["glow"] = maxf(0.0, float(fighter["glow"]) - 60.0 * delta)
		if gear == "tidewing" and velocity.y > 170.0 and float(fighter["power_time"]) <= 0.0 and (fighter["position"] as Vector2).y > floor_y - 45.0:
			velocity.y = -90.0
			fighter["power_time"] = 0.7
		velocity.y = minf(365.0, velocity.y + gravity * delta)
	var position: Vector2 = fighter["position"]
	position += velocity * delta
	if float(fighter["pull_time"]) > 0.0:
		position += (fighter["pull"] as Vector2) * delta
	position.x = clampf(position.x, 225.0, 1055.0)
	if position.y < 270.0:
		position.y = 270.0
		velocity.y = 0.0
	if position.y > floor_y:
		position = Vector2(clampf(position.x, 225, 1055), 480)
		velocity = Vector2.ZERO
		fighter["recover"] = 0.6
		fighter["held"] = false
		fighter["armed"] = false
	fighter["position"] = position
	fighter["velocity"] = velocity


func _projectiles(player: int, delta: float, previous: Array[Vector2], hits: Array[Dictionary]) -> void:
	var fighter: Dictionary = host.fighters[player]
	var shots: Array = fighter["shots"]
	var other := 1 - player
	var bubbles: Array = host.fighters[other]["bubbles"]
	for index: int in range(shots.size() - 1, -1, -1):
		var shot: Dictionary = shots[index]
		shot["life"] = float(shot["life"]) - delta
		if bubbles.is_empty() or float(shot["life"]) <= 0.0:
			shots.remove_at(index)
			continue
		var side := int(bubbles[0])
		var from: Vector2 = shot["position"]
		var goal := bubble_at(other, side)
		var next := from.move_toward(goal, 540.0 * delta)
		var old_goal := previous[other] + Vector2(-32 if side == 1 else 32, -98)
		shot["position"] = next
		if float(host.fighters[other]["recover"]) <= 0.0 and Geometry2D.get_closest_point_to_segment(Vector2.ZERO, from - old_goal, next - goal).length_squared() <= 33.0 * 33.0:
			shots.remove_at(index)
			hits.append({"target": other, "side": side, "source": player})
