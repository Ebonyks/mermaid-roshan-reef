extends RefCounted
## Three-device engineering: saved consequences belong to the surface/world.

const GEAR_PATH := "res://assets/opera/worlds/widgets/astronaut_gear_v1.png"
const VALVE_PATH := "res://assets/opera/worlds/widgets/widget_crank_astronaut_mover.png"
const RADII := [48.0, 66.0, 40.0]
const TARGETS := [0.35, 0.60, 0.80]
const START_VALUES := [0.12, 0.88, 0.12]
const BAND := 0.11
var s: OperaAstronautSurface
var fitted: Array[bool] = [false, false, false]
var tuned: Array[bool] = [false, false, false]
var values: Array[float] = [0.12, 0.88, 0.12]
var selected := -1
var pending := -1
var pending_contact_index := -1
var drag_at := Vector2.ZERO
var drag_offset := Vector2.ZERO
var press_at := Vector2.ZERO
var travel := 0.0
var preview := 0.0
var gear_texture: Texture2D
var valve_texture: Texture2D
var animation_t := 0.0
var rack_style: StyleBoxFlat


func _init(owner: OperaAstronautSurface) -> void:
	s = owner
	gear_texture = s._load_widget_texture(GEAR_PATH)
	valve_texture = s._load_widget_texture(VALVE_PATH)
	rack_style = StyleBoxFlat.new()
	rack_style.bg_color = Color(0.12, 0.22, 0.29, 0.85)
	rack_style.border_color = Color("#819eaa")
	rack_style.set_border_width_all(4)
	rack_style.set_corner_radius_all(22)


func reset() -> void:
	fitted = [false, false, false]
	tuned = [false, false, false]
	values = [0.12, 0.88, 0.12]
	cancel()
	animation_t = 0.0


func cancel() -> void:
	selected = -1
	pending = -1
	travel = 0.0


func socket(index: int) -> Vector2:
	var first := Vector2(s.size.x * 0.27, s.size.y * 0.35)
	return first + [Vector2.ZERO, Vector2(98, 30), Vector2(186, 0)][index]


func home(index: int) -> Vector2:
	return Vector2(s.size.x * (0.20 + float(index) * 0.30), s.size.y * 0.80)


func valve(index: int) -> Vector2:
	return Vector2(s.size.x * (0.20 + float(index) * 0.30), s.size.y * 0.73)


func work_point(index: int) -> Vector2:
	return socket(index) if s.mode == "gears" else valve(index)


func press(at: Vector2) -> void:
	if s.completion_accepted or pending >= 0 or s.armed_only:
		return
	press_at = at
	travel = 0.0
	for index in range(3):
		var point := home(index) if s.mode == "gears" else valve(index)
		var done := fitted[index] if s.mode == "gears" else tuned[index]
		var reach := float(RADII[index]) + 24.0 if s.mode == "gears" else 72.0
		if not done and at.distance_to(point) <= reach:
			selected = index
			drag_offset = point - at
			drag_at = point
			preview = values[index]
			s.feedback_anchor = point
			s.queue_redraw()
			return
	s.note_result(false)


func drag(at: Vector2) -> void:
	if selected < 0:
		return
	travel = maxf(travel, at.distance_to(press_at))
	if s.mode == "gears":
		drag_at = at + drag_offset
	else:
		# One continuous finger adjusts a physical valve. No idle clock pays.
		preview = clampf(values[selected] + (press_at.y - at.y) / 180.0, 0.0, 1.0)
	s.queue_redraw()


func release(at: Vector2) -> void:
	if selected < 0 or s.completion_accepted:
		return
	drag(at)
	var index := selected
	selected = -1
	if s.mode == "gears":
		if travel < 12.0 or drag_at.distance_to(socket(index)) > float(RADII[index]) + 24.0:
			s.note_result(false)
			s.demo_active = true
			return
	elif travel < 12.0:
		s.note_result(false)
		return
	pending = index
	s.request_device_work(index)


func commit(index: int) -> bool:
	if pending != index or index < 0 or index >= 3:
		return false
	pending = -1
	var gained := false
	if s.mode == "gears":
		if fitted[index]:
			return false
		fitted[index] = true
		gained = true
	else:
		if tuned[index]:
			return false
		values[index] = preview
		if absf(values[index] - float(TARGETS[index])) <= BAND:
			tuned[index] = true
			gained = true
	s.note_result(gained)
	if gained:
		pending_contact_index = index
		s.device_commit_active = true
		s.gesture.emit(s.mode, 1.0, 1.0)
		s.device_commit_active = false
		pending_contact_index = -1
	else:
		s.demo_active = true
	s.progress_changed.emit()
	s.queue_redraw()
	return true


func snapshot() -> Dictionary:
	return {"fitted": fitted.duplicate(), "tuned": tuned.duplicate(), "values": values.duplicate()}


func restore(data: Dictionary, progress: float) -> bool:
	var raw_fitted: Variant = data.get("fitted", null)
	var raw_tuned: Variant = data.get("tuned", null)
	var raw_values: Variant = data.get("values", null)
	if not raw_fitted is Array or not raw_tuned is Array or not raw_values is Array \
			or raw_fitted.size() != 3 or raw_tuned.size() != 3 or raw_values.size() != 3:
		return false
	var count := 0
	for index in range(3):
		if not raw_fitted[index] is bool or not raw_tuned[index] is bool \
				or not s._valid_saved_number(raw_values[index]) \
				or float(raw_values[index]) < 0.0 or float(raw_values[index]) > 1.0:
			return false
		if s.mode == "pressure" and bool(raw_tuned[index]) \
				and absf(float(raw_values[index]) - float(TARGETS[index])) > BAND:
			return false
		count += 1 if bool(raw_fitted[index] if s.mode == "gears" else raw_tuned[index]) else 0
	if not is_equal_approx(float(count), progress):
		return false
	for index in range(3):
		fitted[index] = bool(raw_fitted[index])
		tuned[index] = bool(raw_tuned[index])
		values[index] = float(raw_values[index])
	cancel()
	return true


func tick(delta: float) -> void:
	animation_t += delta
	# Only installed gears move. This display clock never changes progress.
	if fitted.has(true) or s.demo_active:
		s.queue_redraw()


func _gear(at: Vector2, index: int, rotation: float, tint: Color = Color.WHITE) -> void:
	if gear_texture == null:
		return
	var side := float(RADII[index]) * 2.0 / 0.90
	s.draw_set_transform(at, rotation)
	s.draw_texture_rect(gear_texture, Rect2(Vector2.ONE * -side * 0.5, Vector2.ONE * side), false, tint)
	s.draw_set_transform(Vector2.ZERO)


func draw() -> void:
	if s.mode == "gears":
		_draw_gears()
	else:
		_draw_pressure()
	if s.demo_active and selected < 0 and pending < 0 and not s.completion_accepted:
		_draw_hint()


func _draw_gears() -> void:
	s.draw_style_box(rack_style, Rect2(socket(0) - Vector2(90, 94), Vector2(430, 218)))
	var connected := true
	for index in range(3):
		var point := socket(index)
		# A dim copy is the actual size/shape socket; no reading-dependent legend.
		_gear(point, index, 0.0, Color(0.34, 0.44, 0.51, 0.40))
		s.draw_circle(point, 9.0, Color("#e4d8b7"))
		connected = connected and fitted[index]
		if fitted[index]:
			var direction := -1.0 if index == 1 else 1.0
			_gear(point, index, animation_t * direction * 32.0 / float(RADII[index]) if connected else 0.0)
			s.draw_circle(point, 7.0, Color("#84d5a6"))
		elif selected == index or pending == index:
			_gear(drag_at if selected == index else point, index, 0.0)
		else:
			_gear(home(index), index, 0.0)
	var output := socket(2) + Vector2(102, 0)
	s.draw_line(socket(2) + Vector2(40, 0), output, Color("#77878d"), 8.0, true)
	s.draw_circle(output, 27.0, Color("#84d5a6") if fitted.all(func(value: bool) -> bool: return value) else Color("#556878"))
	if fitted.all(func(value: bool) -> bool: return value):
		s.draw_arc(output, 36.0, animation_t, animation_t + PI * 1.5, 24, Color("#f5d581"), 5.0, true)


func _draw_pressure() -> void:
	s.draw_style_box(rack_style, Rect2(Vector2(46, s.size.y * 0.30 - 86), Vector2(s.size.x - 92, 180)))
	for index in range(3):
		var knob := valve(index)
		var gauge := Vector2(knob.x, s.size.y * 0.30)
		var value := preview if selected == index or pending == index else values[index]
		s.draw_circle(gauge, 70.0, Color("#344454"))
		s.draw_circle(gauge, 63.0, Color("#e4dfc9"))
		s.draw_arc(gauge, 51.0, PI * 0.85, TAU + PI * 0.15, 40, Color("#8d9da1"), 8.0, true)
		var low := lerpf(PI * 0.85, TAU + PI * 0.15, float(TARGETS[index]) - BAND)
		var high := lerpf(PI * 0.85, TAU + PI * 0.15, float(TARGETS[index]) + BAND)
		s.draw_arc(gauge, 51.0, low, high, 16, Color("#66b98f"), 15.0, true)
		var angle := lerpf(PI * 0.85, TAU + PI * 0.15, value)
		s.draw_line(gauge, gauge + Vector2.from_angle(angle) * 48.0, Color("#b77b46"), 7.0, true)
		s.draw_circle(gauge, 9.0, Color("#344454"))
		s.draw_line(gauge + Vector2(0, 68), knob - Vector2(0, 50), Color("#7a949e"), 12.0, true)
		if valve_texture != null:
			s.draw_set_transform(knob, (value - 0.5) * PI)
			s.draw_texture_rect(valve_texture, Rect2(-54, -54, 108, 108), false)
			s.draw_set_transform(Vector2.ZERO)
		if tuned[index]:
			s.draw_arc(knob, 63.0, 0.0, TAU, 32, Color("#88d4a6"), 5.0, true)
		else:
			# Up/down arrows physically connect the one-finger gesture to the valve.
			for direction in [-1.0, 1.0]:
				var tip := knob + Vector2(77, direction * 32)
				s.draw_line(knob + Vector2(77, 0), tip, Color("#ecd69a"), 4.0, true)
				s.draw_line(tip, tip + Vector2(-8, -direction * 10), Color("#ecd69a"), 4.0, true)
				s.draw_line(tip, tip + Vector2(8, -direction * 10), Color("#ecd69a"), 4.0, true)


func _draw_hint() -> void:
	var index := -1
	for candidate in range(3):
		if not (fitted[candidate] if s.mode == "gears" else tuned[candidate]):
			index = candidate
			break
	if index < 0:
		return
	var start := home(index) if s.mode == "gears" else valve(index)
	var finish := socket(index) if s.mode == "gears" else start + Vector2(0, (values[index] - float(TARGETS[index])) * 180.0)
	var finger := start.lerp(finish, smoothstep(0.0, 1.0, fmod(animation_t, 2.4) / 2.4))
	s.draw_line(start, finish, Color(1, 0.89, 0.59, 0.45), 5.0, true)
	s.draw_circle(finger, 15.0, Color(1, 0.93, 0.76, 0.82))
	s.draw_arc(finish, 22.0, 0.0, TAU, 24, Color(1, 0.84, 0.44, 0.80), 3.0, true)
