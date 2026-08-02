class_name OperaGestureSurface
extends Control
## One-finger input surface shared by all thirteen 2D Opera career worlds.
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
## Friendly imp-scuffle targets for the "bop" combat beats. Each entry:
## {home: Vector2, pos: Vector2, r: float, hp: int, captain: bool, popped: bool}
var bop_targets: Array = []
var bop_texture: Texture2D = null
var bop_captain_texture: Texture2D = null
var last_bop_pos := Vector2.ZERO


## Ghost-finger demo: until the child touches, a glowing dot acts out the
## expected gesture so no phase ever needs reading to understand.
var demo_active := true
var demo_t := 0.0
var _demo_redraw := 0.0
## Choice lanes flash gold briefly, then dim so the pick uses recognition
## memory instead of tap-the-highlight; wrong picks kindly re-flash.
var choice_flash := 1.4
## Directional hint for swipe phases (DUCK draws a downward arrow).
var swipe_dir := Vector2.RIGHT
## Tap phases aim at a moving point that leaves a happy mark per hit.
var tap_point := Vector2.ZERO
var tap_marks: Array = []
## Diegetic scene painted behind the affordance (nursery basin/bottle/cribs).
var visual_context := ""
var nursery_textures: Array[Texture2D] = []


func configure(next_mode: String, next_accent: Color, choice: int = 1, next_context: String = "") -> void:
	mode = next_mode
	accent = next_accent
	target_choice = choice
	visual_context = next_context
	if visual_context.begins_with("nursery") and nursery_textures.is_empty():
		for index in range(3):
			var path := "res://assets/opera/worlds/nursery/baby_%d.png" % index
			var texture := load(path) as Texture2D
			if texture != null:
				nursery_textures.append(texture)
	held = false
	have_angle = false
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.4
	swipe_dir = Vector2.RIGHT
	tap_marks = []
	tap_point = size * 0.5
	if next_mode != "bop":
		bop_targets = []
	queue_redraw()


func note_input() -> void:
	demo_active = false


func restart_demo() -> void:
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.2


func reflash_choice() -> void:
	choice_flash = 1.2
	queue_redraw()


func _process(delta: float) -> void:
	if choice_flash > 0.0 and mode == "choice":
		choice_flash -= delta
		if choice_flash <= 0.0:
			queue_redraw()
	if not demo_active:
		return
	demo_t += delta
	_demo_redraw += delta
	if _demo_redraw >= 0.05:
		_demo_redraw = 0.0
		queue_redraw()


func set_bop_targets(targets: Array) -> void:
	bop_targets = targets
	queue_redraw()


func bop_remaining() -> int:
	var left := 0
	for target: Dictionary in bop_targets:
		if not bool(target.get("popped", false)):
			left += 1
	return left


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
			if at.distance_to(tap_point) <= 92.0:
				tap_marks.append(tap_point)
				_relocate_tap_point()
				gesture.emit("tap", 1.0, 1.0)
			else:
				# near-misses still sparkle and trickle — no dead ends
				gesture.emit("tap", 0.3, 0.4)
		"choice":
			var lane := clampi(int(at.x / maxf(1.0, size.x) * float(choice_count)), 0, choice_count - 1)
			gesture.emit("choice", 1.0 if lane == target_choice else 0.24, 1.0 if lane == target_choice else 0.0)
		"timing":
			var quality := 1.0 if timing_position >= timing_zone.x and timing_position <= timing_zone.y else 0.32
			gesture.emit("timing", quality, quality)
		"bop":
			_bop_press(at)
		"hold":
			# a tap on the hold circle answers with a small warm trickle
			gesture.emit("hold", 0.06, 0.6)
		"swipe", "circle":
			gesture.emit(mode, 0.05, 0.6)
	queue_redraw()


func _relocate_tap_point() -> void:
	var n := tap_marks.size()
	tap_point = Vector2(
		size.x * 0.5 + sin(float(n) * 2.4 + 0.9) * size.x * 0.3,
		size.y * 0.5 + cos(float(n) * 1.7 + 0.4) * size.y * 0.26
	)


func _bop_press(at: Vector2) -> void:
	for target: Dictionary in bop_targets:
		if bool(target.get("popped", false)):
			continue
		var pos: Vector2 = target.get("pos", Vector2.ZERO)
		var reach := float(target.get("r", 44.0)) * 1.45
		if at.distance_to(pos) <= reach:
			target["hp"] = int(target.get("hp", 1)) - 1
			last_bop_pos = pos
			if int(target["hp"]) <= 0:
				target["popped"] = true
			gesture.emit("bop", 1.0, 1.0)
			return
	# a stray tap fizzles kindly and still trickles a little progress
	last_bop_pos = at
	gesture.emit("bop", 0.12, 0.2)


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
		if button.device == InputEvent.DEVICE_ID_EMULATION:
			return  # already handled as the touch event on tablets
		if button.pressed:
			_press(button.position)
		else:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and held:
		if (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _draw() -> void:
	var panel := Rect2(Vector2.ZERO, size)
	# light paper inset window per the StorybookUI language
	draw_rect(panel, Color(0.94, 0.97, 1.0, 0.96), true)
	draw_rect(panel.grow(-3.0), accent.lerp(Color("#382485"), 0.62), false, 4.0)
	var center := size * 0.5
	if visual_context.begins_with("nursery"):
		_draw_nursery_context(center)
		if demo_active:
			_draw_demo_finger()
		return
	match mode:
		"tap":
			for mark: Vector2 in tap_marks:
				draw_circle(mark, 13.0, Color(accent, 0.85))
				draw_circle(mark, 6.0, Color.WHITE)
			draw_circle(tap_point, 64.0, Color(accent, 0.25))
			draw_arc(tap_point, 64.0, 0.0, TAU, 48, accent, 9.0)
			draw_circle(tap_point, 18.0, Color.WHITE)
		"hold":
			draw_circle(center, minf(size.x, size.y) * 0.25, Color(accent, 0.24))
			draw_arc(center, minf(size.x, size.y) * 0.25, 0.0, TAU, 48, accent, 10.0)
			draw_circle(center, 24.0 if held else 16.0, Color.WHITE)
		"swipe":
			var span := minf(size.x, size.y) * 0.42
			var tail := center - swipe_dir * span
			var head := center + swipe_dir * span
			var side := swipe_dir.orthogonal()
			draw_line(tail, head, accent, 16.0, true)
			draw_colored_polygon(PackedVector2Array([
				head + side * 34.0, head + swipe_dir * 58.0, head - side * 34.0,
			]), accent)
			draw_circle(tail, 22.0, Color.WHITE)
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			draw_arc(center, radius, -2.7, 2.2, 48, accent, 16.0)
			var tip := center + Vector2.from_angle(2.2) * radius
			draw_colored_polygon(PackedVector2Array([
				tip, tip + Vector2(-10, -36), tip + Vector2(30, -14),
			]), accent)
		"choice":
			var show_answer := choice_flash > 0.0 or demo_active
			for index in range(choice_count):
				var point := Vector2(size.x * (float(index) + 0.5) / float(choice_count), center.y)
				var is_answer := index == target_choice and show_answer
				var colour := Color(1.0, 0.86, 0.32) if is_answer else Color(0.34, 0.42, 0.62)
				draw_circle(point, 54.0, Color(colour, 0.34))
				draw_arc(point, 54.0, 0.0, TAU, 36, colour, 9.0)
				if is_answer:
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
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					_draw_imp(target)
	if demo_active:
		_draw_demo_finger()


func _draw_nursery_baby(texture_index: int, center: Vector2, extent: float) -> void:
	if nursery_textures.is_empty():
		draw_circle(center, extent * 0.30, Color("#ffd6bf"))
		return
	var texture: Texture2D = nursery_textures[posmod(texture_index, nursery_textures.size())]
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * extent * 0.5, Vector2.ONE * extent), false)


func _draw_nursery_context(center: Vector2) -> void:
	match visual_context:
		"nursery_wash":
			var basin := Rect2(center.x - 92.0, center.y - 12.0, 184.0, 82.0)
			draw_rect(basin, Color("#78cfd0"), true)
			draw_arc(Vector2(center.x, basin.position.y), 92.0, 0.0, PI, 32, Color("#ecfbf4"), 10.0)
			for index in range(7):
				var bubble := center + Vector2(-70.0 + float(index) * 23.0, -48.0 - float(index % 3) * 17.0)
				draw_circle(bubble, 9.0 + float(index % 2) * 4.0, Color(0.82, 0.97, 1.0, 0.62))
			draw_circle(center, 25.0 if held else 17.0, Color.WHITE)
			draw_arc(center, 58.0, 0.0, TAU, 40, accent, 9.0)
		"nursery_feed":
			for index in range(3):
				_draw_nursery_baby(index, Vector2(86.0 + float(index) * 100.0, center.y + 48.0), 88.0)
			var bottle_center := Vector2(center.x, center.y - 58.0)
			draw_rect(Rect2(bottle_center - Vector2(23, 38), Vector2(46, 76)), Color("#edf9ee"), true)
			draw_rect(Rect2(bottle_center - Vector2(17, 31), Vector2(34, 51)), Color("#ffe7ac"), true)
			draw_circle(bottle_center + Vector2(0, -44), 12.0, Color("#f1b1a1"))
			draw_arc(bottle_center, 61.0, 0.0, TAU, 40, accent, 9.0)
			draw_circle(bottle_center, 22.0 if held else 15.0, Color.WHITE)
		"nursery_burp":
			_draw_nursery_baby(1, Vector2(center.x, 70.0), 105.0)
			var hand := Vector2(center.x + 92.0, 78.0)
			draw_circle(hand, 28.0, Color("#ffd8bd"))
			draw_arc(hand, 45.0, -1.2, 1.2, 24, accent, 8.0)
			var bar := Rect2(size.x * 0.12, size.y - 82.0, size.x * 0.76, 42.0)
			draw_rect(bar, Color(0.20, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 22.0), Vector2(marker_x, bar.end.y + 22.0), Color.WHITE, 11.0)
		"nursery_bedtime":
			for index in range(3):
				var crib_center := Vector2(72.0 + float(index) * 114.0, center.y + 20.0)
				draw_rect(Rect2(crib_center - Vector2(48, 30), Vector2(96, 78)), Color("#f1d2c2"), true)
				_draw_nursery_baby(index, crib_center - Vector2(0, 10), 74.0)
				draw_rect(Rect2(crib_center.x - 43.0, crib_center.y + 7.0, 86.0, 37.0), Color(0.52, 0.81, 0.77, 0.94), true)
			for star in [Vector2(55, 44), Vector2(145, 30), Vector2(235, 50)]:
				draw_circle(star, 7.0, Color("#ffe483"))
			var arrow_x := size.x - 24.0
			draw_line(Vector2(arrow_x, 54.0), Vector2(arrow_x, size.y - 42.0), accent, 13.0, true)
			draw_colored_polygon(PackedVector2Array([
				Vector2(arrow_x - 28.0, size.y - 68.0), Vector2(arrow_x + 28.0, size.y - 68.0), Vector2(arrow_x, size.y - 28.0),
			]), accent)

func _draw_demo_finger() -> void:
	var center := size * 0.5
	var cycle := fmod(demo_t, 2.4)
	var pressing := cycle > 1.1
	var at := center
	match mode:
		"swipe":
			at = Vector2(lerpf(size.x * 0.22, size.x * 0.78, cycle / 2.4), center.y)
			pressing = true
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			at = center + Vector2.from_angle(-2.7 + cycle * 2.0) * radius
			pressing = true
		"choice":
			var lane := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), center.y)
			at = center.lerp(lane, clampf(cycle / 1.1, 0.0, 1.0))
		"timing":
			var bar_x := lerpf(size.x * 0.12, size.x * 0.88, timing_position)
			at = Vector2(bar_x, center.y + 58.0)
			pressing = timing_position >= timing_zone.x and timing_position <= timing_zone.y
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					var pos: Vector2 = target.get("pos", Vector2.ZERO)
					at = center.lerp(pos, clampf(cycle / 1.1, 0.0, 1.0))
					break
		"hold":
			pressing = true
	var halo := 30.0 if pressing else 20.0
	draw_circle(at, halo, Color(0.22, 0.14, 0.52, 0.18))
	draw_circle(at, 14.5, Color("#382485"))
	draw_circle(at, 12.0, Color(1.0, 0.98, 0.86, 0.98))
	if pressing:
		var ring := 18.0 + fmod(demo_t * 46.0, 26.0)
		draw_arc(at, ring, 0.0, TAU, 24, Color(1.0, 0.95, 0.6, 0.6), 4.0)


func _draw_imp(target: Dictionary) -> void:
	var pos: Vector2 = target.get("pos", Vector2.ZERO)
	var radius := float(target.get("r", 44.0))
	var captain := bool(target.get("captain", false))
	var texture := bop_captain_texture if captain else bop_texture
	if texture != null:
		var side := radius * 2.4
		draw_texture_rect(texture, Rect2(pos - Vector2(side, side) * 0.5, Vector2(side, side)), false)
		if captain:
			# plain gold band ring marks the captain over the costume sprite
			draw_arc(pos, radius * 1.16, 0.0, TAU, 36, Color("#e0b34c"), 6.0)
			if int(target.get("hp", 1)) > 1:
				draw_arc(pos, radius * 1.3, 0.0, TAU, 36, Color(1.0, 0.9, 0.5, 0.45), 4.0)
		return
	# basic place-in imp until the codex mischief-imp sprite set lands
	var body := Color("#7a4f9a") if not captain else Color("#5f3a85")
	var belly := Color("#b28ccd")
	draw_circle(pos, radius * 1.18, Color(1.0, 0.86, 0.4, 0.16))
	# curled striped horns
	for side_sign in [-1.0, 1.0]:
		var horn := pos + Vector2(side_sign * radius * 0.62, -radius * 0.78)
		draw_arc(horn, radius * 0.34, PI * 0.2, PI * 1.4, 12, Color("#e8d6a8"), 9.0)
		draw_arc(horn, radius * 0.34, PI * 0.5, PI * 1.1, 8, Color("#a8794f"), 9.0)
	# curled tail
	draw_arc(pos + Vector2(radius * 0.95, radius * 0.55), radius * 0.4, -PI * 0.6, PI * 0.7, 10, body.lightened(0.1), 8.0)
	draw_circle(pos, radius, body)
	draw_circle(pos + Vector2(0, radius * 0.3), radius * 0.55, belly)
	# amber eyes and a friendly fanged grin
	for side_sign in [-1.0, 1.0]:
		var eye := pos + Vector2(side_sign * radius * 0.34, -radius * 0.22)
		draw_circle(eye, radius * 0.17, Color("#f4b642"))
		draw_circle(eye, radius * 0.08, Color("#33203f"))
	draw_arc(pos + Vector2(0, radius * 0.1), radius * 0.34, 0.35, PI - 0.35, 12, Color("#33203f"), 5.0)
	for side_sign in [-1.0, 1.0]:
		var fang := pos + Vector2(side_sign * radius * 0.18, radius * 0.36)
		draw_colored_polygon(PackedVector2Array([
			fang + Vector2(-5, 0), fang + Vector2(5, 0), fang + Vector2(0, 10),
		]), Color.WHITE)
	if captain:
		# plain gold waistband marks the captain (no shell or crest motifs)
		draw_line(pos + Vector2(-radius * 0.8, radius * 0.62), pos + Vector2(radius * 0.8, radius * 0.62), Color("#e0b34c"), 8.0)
		if int(target.get("hp", 1)) > 1:
			draw_arc(pos, radius * 1.12, 0.0, TAU, 32, Color("#e0b34c"), 5.0)
