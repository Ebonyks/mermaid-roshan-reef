extends Node2D
## Optional Lily Pond puzzle. Both channels remain usable after the discovery.

const SHELL := preload("res://assets/flats/castle/main_hall_2screen/castle_shell_sconce_touchable.png")
const SHELL_FACE := Rect2(204, 72, 608, 668)
const START := Vector2(0, 29)
const DOCKS: Array[Vector2] = [Vector2(-101, -11), Vector2(102, -9)]
const VALVES: Array[Vector2] = [Vector2(-88, -65), Vector2(89, -65)]
const CHARM := Vector2(128, -33)
const CARGO_OFFSET := Vector2(6, -12)
const DEPOSIT_TIME := 0.26
const INK := Color("#504455")
const WOOD := Color("#99705d")
const TRIM := Color("#eac591")
const WATER := Color("#b2ede2")
const GOLD := Color("#fff0b3")

signal discovery

static var _shell_alpha: BitMap

var found := false
var arrived := false
var destination := -1
var selected := -1
var boat := START
var _origin := START
var _elapsed := 0.0
var _clock := 0.0
var _idle := 0.0
var _near := false
var _moving := false
var _deposit_progress := -1.0
var _pulse := 0.0
var _pulse_valve := -1

# Review tuning is injected only by the dedicated replay. Shipping defaults are the final round.
var hit_radius := 35.0
var trip_time := 0.84
var hint_time := 3.0
var show_channels := true
var mark_docks := true
var preview_current := true
var redirect := true
var dry_controls := true
var mark_reward := true
var acknowledge := true
var replay_reward := true


func _ready() -> void:
	if _shell_alpha == null:
		var pixels: Image = SHELL.get_image()
		if pixels == null or (pixels.is_compressed() and pixels.decompress() != OK):
			push_error("Reed Cove could not read the shell touch silhouette")
			return
		var face: Image = pixels.get_region(Rect2i(SHELL_FACE))
		_shell_alpha = BitMap.new()
		_shell_alpha.create_from_image_alpha(face, 0.1)


func target(point: Vector2) -> int:
	var local: Vector2 = to_local(point)
	var closest: float = hit_radius
	var choice := -1
	for index: int in range(VALVES.size()):
		var distance: float = local.distance_to(valve(index))
		if distance <= closest:
			closest = distance
			choice = index
	if arrived and not found and local.distance_to(CHARM) < closest:
		return 2
	return choice


func hits_painted_control(point: Vector2, index: int) -> bool:
	var local: Vector2 = to_local(point)
	if index < 2:
		var knob: Vector2 = valve(index)
		return local.distance_to(knob) <= 19.0 or local.distance_to(knob + Vector2(0, 5)) <= 20.0
	# The raised shell is drawn in front. Preserve direct contact on its
	# painted contour before considering wildlife in the larger touch margin.
	var shell: Rect2 = _charm_rect(CHARM, 34.0)
	if _shell_alpha == null or not mark_reward or not shell.has_point(local):
		return false
	var source := Vector2i((local - shell.position) / shell.size * SHELL_FACE.size)
	return _shell_alpha.get_bitv(source)


func valve(index: int) -> Vector2:
	return VALVES[index] if dry_controls else VALVES[index] + Vector2(0, 27)


func interaction_point(index: int) -> Vector2:
	return to_global(CHARM if index == 2 else valve(index))


func interaction_stand(index: int) -> Vector2:
	if index == 2:
		return to_global(Vector2(150, -64))
	return to_global(VALVES[index] + Vector2(0, -32))


func select_target(index: int) -> void:
	if selected != index:
		selected = index
		_idle = 0.0
		queue_redraw()


func interact(index: int) -> void:
	select_target(-1)
	if index == 2:
		if arrived and not found:
			found = true
			discovery.emit()
		return
	if _moving and (not redirect or destination == index):
		return
	if not _moving and boat.distance_to(DOCKS[index]) < 1.0:
		_idle = 0.0
		_pulse = 0.28
		_pulse_valve = index
		queue_redraw()
		return
	_begin(index)


func _begin(index: int) -> void:
	destination = index
	_origin = boat
	_elapsed = 0.0
	_idle = 0.0
	_moving = true
	queue_redraw()


func tick(delta: float, player: Vector2) -> void:
	_clock += delta
	_pulse = maxf(0.0, _pulse - delta)
	_near = player.distance_to(global_position) < 395.0
	if _near and not _moving and selected < 0:
		_idle += delta
	if _deposit_progress >= 0.0 and not arrived:
		_deposit_progress = minf(1.0, _deposit_progress + delta / DEPOSIT_TIME)
		arrived = _deposit_progress >= 1.0
	if _moving:
		_elapsed = minf(trip_time, _elapsed + delta)
		var progress: float = _elapsed / trip_time
		boat = journey_point(smoothstep(0.0, 1.0, progress))
		if progress >= 1.0:
			_moving = false
			if destination == 1 and not arrived and not found and _deposit_progress < 0.0:
				_deposit_progress = 0.0
	if _near:
		queue_redraw()


func journey_point(t: float) -> Vector2:
	var end: Vector2 = START if destination < 0 else DOCKS[destination]
	var bend: Vector2 = _origin.lerp(end, 0.5) + Vector2(0, 31)
	return _origin.lerp(bend, t).lerp(bend.lerp(end, t), t)

 
func _draw() -> void:
	for index: int in range(VALVES.size()):
		var socket: Vector2 = valve(index)
		var dock: Vector2 = DOCKS[index]
		var water_line := PackedVector2Array([START + Vector2(0, 8),
			START.lerp(dock, 0.5) + Vector2(0, 14), dock])
		if show_channels:
			draw_polyline(water_line, Color("#427f8259"), 6.0, true)
			draw_polyline(water_line, Color("#9bcac080"), 2.0, true)
		if preview_current and _near and _moving and destination == index:
			var progress: float = smoothstep(0.0, 1.0, _elapsed / trip_time)
			for offset: float in [0.11, 0.24, 0.37]:
				var t: float = progress + offset
				if t >= 1.0:
					break
				var ripple: Vector2 = journey_point(t)
				var heading: Vector2 = (journey_point(t + 0.01) - ripple).normalized()
				var back: Vector2 = ripple - 8.0 * heading
				var spread: Vector2 = heading.orthogonal() * 4.0
				draw_polyline(PackedVector2Array([back - spread, ripple, back + spread]),
					WATER, 2.5, true)
		_draw_dock(dock, index)
		draw_line(socket + Vector2(0, 14), dock + Vector2(0, -9), INK, 6.0, true)
		draw_line(socket + Vector2(0, 14), dock + Vector2(0, -9), WOOD, 3.0, true)
		_draw_valve(socket, index)
	_draw_boat()
	if selected >= 0:
		var at: Vector2 = CHARM if selected == 2 else valve(selected)
		draw_arc(at, 25.0, 0, TAU, 32, GOLD, 3, true)
	if mark_reward:
		_draw_charm(CHARM, 34.0, TRIM)
		_draw_charm(CHARM + Vector2(0, 1), 29.0, INK)
		if not found:
			_draw_charm(cargo_position(), 29.0, Color.WHITE)
		elif replay_reward:
			_draw_charm(CHARM, 29.0, Color("#d7a85f"))
	if idle_hint_visible():
		if arrived:
			_draw_hint(CHARM)
		elif destination == 0:
			_draw_hint(valve(1))
		else:
			_draw_hint(valve(0))
			_draw_hint(valve(1))


func idle_hint_visible() -> bool:
	return _near and not _moving and selected < 0 and _idle >= hint_time and not found


func _draw_hint(at: Vector2) -> void:
	draw_arc(at, 26 + sin(_clock * 3.6) * 2, 0, TAU, 32, GOLD, 2, true)


func _draw_dock(at: Vector2, index: int) -> void:
	for plank: int in range(3):
		var pos: Vector2 = at + Vector2(-21, -19 + plank * 10)
		draw_rect(Rect2(pos, Vector2(42, 12)), INK)
		draw_rect(Rect2(pos + Vector2(2, 2), Vector2(38, 8)), WOOD)
		draw_line(pos + Vector2(4, 3), pos + Vector2(37, 3), TRIM, 1, true)
	if mark_docks and index == 1:
		draw_line(CHARM + Vector2(0, 12), at + Vector2(14, -8), INK, 6, true)


func _draw_valve(at: Vector2, index: int) -> void:
	var pressed: bool = acknowledge and _moving and destination == index
	draw_circle(at + Vector2(0, 5), 20, INK, true, -1.0, true)
	draw_circle(at, 19, Color("#815776"), true, -1.0, true)
	draw_arc(at, 16, 0, TAU, 28, TRIM if not pressed else GOLD, 3, true)
	if _pulse_valve == index and _pulse > 0.0:
		draw_arc(at, lerpf(29.0, 22.0, _pulse / 0.28), 0, TAU, 30, GOLD, 2, true)
	var side: float = -1.0 if index == 0 else 1.0
	draw_polyline(PackedVector2Array([at + Vector2(-6 * side, -7),
		at + Vector2(6 * side, 0), at + Vector2(-6 * side, 7)]), GOLD, 3, true)


func _draw_boat() -> void:
	var at: Vector2 = boat + Vector2(0, sin(_clock * 4) * 1.7)
	draw_arc(at + Vector2(0, 3), 22, 0.08, 2.98, 18, WATER, 2, true)
	var hull := PackedVector2Array([at + Vector2(-21, -4), at + Vector2(-8, -10),
		at + Vector2(20, -7), at + Vector2(12, 3), at + Vector2(-8, 6)])
	draw_colored_polygon(hull, Color("#63854b"))
	hull.append(hull[0])
	draw_polyline(hull, INK, 2.5, true)
	draw_colored_polygon(PackedVector2Array([at + Vector2(-4, -8),
		at + Vector2(-4, -30), at + Vector2(12, -10)]), GOLD)


func cargo_position() -> Vector2:
	if _deposit_progress < 0.0:
		return boat + CARGO_OFFSET + Vector2(0, sin(_clock * 4) * 1.7)
	var t: float = _deposit_progress
	return (DOCKS[1] + CARGO_OFFSET).lerp(CHARM, t) - Vector2(0, sin(PI * t) * 12)


func _charm_rect(at: Vector2, height: float) -> Rect2:
	var size: Vector2 = Vector2(SHELL_FACE.size.x / SHELL_FACE.size.y, 1.0) * height
	return Rect2(at - size * 0.5, size)


func _draw_charm(at: Vector2, height: float, tint: Color) -> void:
	draw_texture_rect_region(SHELL, _charm_rect(at, height), SHELL_FACE, tint)
