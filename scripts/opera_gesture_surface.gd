class_name OperaGestureSurface
extends Control
## One-finger input surface shared by all twelve 2D Opera career worlds.
##
## The surrounding world chooses a gesture mode; this node turns mouse and
## touchscreen input into normalized progress without owning career state.
## Incorrect timing/choices report lower quality but still make a little
## progress, so there is no dead end for a non-reader.

signal gesture(kind: String, amount: float, quality: float)

var mode := "tap"
var accent := Color(1.0, 0.62, 0.8)
var target_choice := 1
var choice_count := 3
var timing_position := 0.0
var timing_zone := Vector2(0.38, 0.68)
var held := false
var pointer_pos := Vector2.ZERO
var previous_pos := Vector2.ZERO
var previous_angle := 0.0
var have_angle := false


func configure(next_mode: String, next_accent: Color, choice: int = 1) -> void:
	mode = next_mode
	accent = next_accent
	target_choice = choice
	held = false
	have_angle = false
	queue_redraw()


func set_timing_position(value: float) -> void:
	timing_position = clampf(value, 0.0, 1.0)
	if mode == "timing":
		queue_redraw()


func _press(at: Vector2) -> void:
	held = true
	pointer_pos = at
	previous_pos = at
	previous_angle = (at - size * 0.5).angle()
	have_angle = true
	match mode:
		"tap":
			gesture.emit("tap", 1.0, 1.0)
		"choice":
			var lane := clampi(int(at.x / maxf(1.0, size.x) * float(choice_count)), 0, choice_count - 1)
			gesture.emit("choice", 1.0 if lane == target_choice else 0.24, 1.0 if lane == target_choice else 0.0)
		"timing":
			var quality := 1.0 if timing_position >= timing_zone.x and timing_position <= timing_zone.y else 0.32
			gesture.emit("timing", quality, quality)
	queue_redraw()


func _drag(at: Vector2) -> void:
	pointer_pos = at
	var distance := at.distance_to(previous_pos)
	if mode == "swipe" and distance > 0.0:
		gesture.emit("swipe", distance / 150.0, 1.0)
	elif mode == "circle":
		var center := size * 0.5
		var radius := at.distance_to(center)
		if radius > minf(size.x, size.y) * 0.13:
			var angle := (at - center).angle()
			if have_angle:
				var change := absf(wrapf(angle - previous_angle, -PI, PI))
				gesture.emit("circle", change / TAU, 1.0)
			previous_angle = angle
			have_angle = true
	previous_pos = at
	queue_redraw()


func _release(at: Vector2) -> void:
	held = false
	pointer_pos = at
	have_angle = false
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_press(touch.position)
		else:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_drag(drag.position)
		accept_event()
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.pressed:
			_press(button.position)
		else:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and held:
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _draw() -> void:
	var panel := Rect2(Vector2.ZERO, size)
	draw_rect(panel, Color(0.035, 0.04, 0.11, 0.78), true)
	draw_rect(panel.grow(-4.0), accent.lightened(0.14), false, 5.0)
	var center := size * 0.5
	match mode:
		"tap":
			draw_circle(center, minf(size.x, size.y) * 0.23, Color(accent, 0.25))
			draw_arc(center, minf(size.x, size.y) * 0.23, 0.0, TAU, 48, accent, 9.0)
			draw_circle(center, 18.0, Color.WHITE)
		"hold":
			draw_circle(center, minf(size.x, size.y) * 0.25, Color(accent, 0.24))
			draw_arc(center, minf(size.x, size.y) * 0.25, 0.0, TAU, 48, accent, 10.0)
			draw_circle(center, 24.0 if held else 16.0, Color.WHITE)
		"swipe":
			var left := Vector2(size.x * 0.22, center.y)
			var right := Vector2(size.x * 0.78, center.y)
			draw_line(left, right, accent, 16.0, true)
			draw_colored_polygon(PackedVector2Array([
				right + Vector2(0, -34), right + Vector2(58, 0), right + Vector2(0, 34),
			]), accent)
			draw_circle(left, 22.0, Color.WHITE)
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			draw_arc(center, radius, -2.7, 2.2, 48, accent, 16.0)
			var tip := center + Vector2.from_angle(2.2) * radius
			draw_colored_polygon(PackedVector2Array([
				tip, tip + Vector2(-10, -36), tip + Vector2(30, -14),
			]), accent)
		"choice":
			for index in range(choice_count):
				var point := Vector2(size.x * (float(index) + 0.5) / float(choice_count), center.y)
				var colour := Color(1.0, 0.86, 0.32) if index == target_choice else Color(0.34, 0.42, 0.62)
				draw_circle(point, 54.0, Color(colour, 0.34))
				draw_arc(point, 54.0, 0.0, TAU, 36, colour, 9.0)
				if index == target_choice:
					draw_circle(point, 15.0, Color.WHITE)
		"timing":
			var bar := Rect2(size.x * 0.12, center.y - 23.0, size.x * 0.76, 46.0)
			draw_rect(bar, Color(0.2, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 28.0), Vector2(marker_x, bar.end.y + 28.0), Color.WHITE, 12.0)
