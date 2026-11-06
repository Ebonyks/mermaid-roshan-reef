class_name BubbleDuelTwoPlayer
extends RefCounted
## Input adapter only. A new press supplies one flap; holding never supplies thrust.
const PADS: Array[Rect2] = [Rect2(18, 488, 184, 184), Rect2(1078, 488, 184, 184)]
const LEFT_KEYS: Array[int] = [KEY_A, KEY_LEFT]
const RIGHT_KEYS: Array[int] = [KEY_D, KEY_RIGHT]
const UP_KEYS: Array[int] = [KEY_W, KEY_UP]
const POWER_KEYS: Array[int] = [KEY_S, KEY_DOWN]
var host: BubbleDuelOverlay


func _init(owner_overlay: BubbleDuelOverlay) -> void:
	host = owner_overlay


func input(event: InputEvent) -> bool:
	var count: int = 2 if host.local_two_player else 1
	if event is InputEventKey:
		var code: int = int(event.physical_keycode if event.physical_keycode != 0 else event.keycode)
		for player: int in range(count):
			if code not in [LEFT_KEYS[player], RIGHT_KEYS[player], UP_KEYS[player], POWER_KEYS[player]]:
				continue
			if event.echo: return true
			host.duo_keys[code] = event.pressed
			var axis: float = float(bool(host.duo_keys.get(RIGHT_KEYS[player], false))) - float(bool(host.duo_keys.get(LEFT_KEYS[player], false)))
			host.world.set_direction(player, axis)
			if code == UP_KEYS[player] and event.pressed:
				host.resume_play()
				host.world.queue_kick(player, axis)
			if code == POWER_KEYS[player]:
				host.world.queue_power(player, event.pressed, event.pressed)
			return true
		return false
	var id: int = -100
	var pressed: bool = false
	var released: bool = false
	var point := Vector2.ZERO
	var dragging: bool = false
	if event is InputEventScreenTouch:
		id = event.index
		point = event.position
		pressed = event.pressed
		released = not event.pressed
	elif event is InputEventScreenDrag:
		id = event.index
		point = event.position
		dragging = true
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		point = event.position
		pressed = event.pressed
		released = not event.pressed
	elif event is InputEventMouseMotion:
		point = event.position
		dragging = true
	else:
		return false
	if pressed and not host.duo_touch_owners.has(id):
		for player: int in range(count):
			if PADS[player].has_point(point) and player not in host.duo_touch_owners.values():
				host.duo_touch_owners[id] = player
				host.resume_play()
				host.world.queue_kick(player, _axis(player, point))
				return true
	if host.duo_touch_owners.has(id):
		var player: int = int(host.duo_touch_owners[id])
		if released:
			if event is InputEventScreenTouch and event.canceled: clear_player(player)
			host.duo_touch_owners.erase(id)
			host.world.set_direction(player, 0.0)
		elif dragging:
			host.world.set_direction(player, _axis(player, point))
		return true
	return false


func _axis(player: int, point: Vector2) -> float:
	var delta: float = point.x - PADS[player].get_center().x
	return 0.0 if absf(delta) < 24.0 else signf(delta)


func activate(player: int) -> bool:
	return host.world.queue_power(player, true, true)


func clear_player(player: int) -> void:
	var fighter: BubbleDuelFighter = host.world.human(player)
	if fighter != null: fighter.clear_controls()


func flush() -> void:
	host.duo_touch_owners.clear()
	host.duo_keys.clear()
	host.world.clear_controls()
