class_name OperaTeacherSurface
extends OperaGestureSurface
## One-finger, concrete early maths. Time never answers a lesson.
const Lessons := preload("res://scripts/teacher_lesson_plan.gd")
const BOARD := Rect2(330, 105, 850, 555)
const HINT_CENTER := Vector2(1115, 150)
const JOIN_CENTER := Vector2(755, 325)
const INK := Color("#392958")
const TOKEN_COLORS := [Color("#71d9dd"), Color("#f3bd73"), Color("#be9ae9"),
	Color("#f293b9"), Color("#8ed5ad")]

signal progress_changed(snapshot: Dictionary)
signal lesson_completed(kind: String, assisted: bool)
signal counter_touched(number: int)
signal guidance_requested(event: String)

var lesson: Dictionary = {}
var counted: Array[bool] = []
var joined := false
var assisted := false
var wrong_attempts := 0
var chosen := -1
var solved := false
var help_visible := false
var touch_owner := -1
var press_at := Vector2.ZERO
var join_t := 0.0
var idle_demo_t := 0.0
var _restored_complete := false
var _numerals: Array[Label] = []

func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	super.configure(next_mode, next_accent, choice, next_context)
	lesson.clear()
	counted.clear()
	joined = false
	assisted = false
	wrong_attempts = 0
	chosen = -1
	solved = false
	help_visible = false
	join_t = 0.0
	idle_demo_t = 0.0
	_restored_complete = false
	cancel_input(false)
	demo_active = true

func set_lesson(value: Dictionary) -> void:
	lesson = value.duplicate(true)
	var total := int(lesson.get("target", 0)) if lesson_kind() in ["count", "add"] else 0
	counted.resize(clampi(total, 0, 10))
	counted.fill(false)
	joined = lesson_kind() != "add"
	_update_numerals()
	queue_redraw()

func lesson_kind() -> String:
	return String(lesson.get("kind", mode.trim_prefix("teacher_")))

func answer_index() -> int:
	return int(lesson.get("answer", -1))

func choice_rect(index: int) -> Rect2:
	var amount := (lesson.get("choices", []) as Array).size()
	var step := 255.0 if amount > 2 else 355.0
	var width := 174.0 if amount == 4 else 210.0
	if amount == 4:
		step = 194.0
	var start := BOARD.get_center().x - (float(amount - 1) * step + width) * 0.5
	return Rect2(start + float(index) * step, 454, width, 170)

func counter_position(index: int) -> Vector2:
	var total := counted.size()
	var columns := mini(5, total)
	var row := index / 5
	var column := index % 5
	var row_count := mini(5, total - row * 5)
	return Vector2(755.0 + (float(column) - float(row_count - 1) * 0.5) * 88.0,
		255.0 + float(row) * 85.0 if total > columns else 290.0)

func can_answer() -> bool:
	return joined and not counted.has(false) and join_t <= 0.0

func progress_snapshot() -> Dictionary:
	return {"version": 1, "kind": lesson_kind(),
		"sequence": int(lesson.get("sequence", 0)), "tier": int(lesson.get("tier", 0)),
		"counted": counted.duplicate(), "joined": joined, "assisted": assisted,
		"wrong_attempts": wrong_attempts, "chosen": chosen if solved else -1}

func restore_progress(snapshot: Dictionary) -> void:
	if snapshot.get("kind", "") != lesson_kind() \
			or not _same_number(snapshot.get("version", null), 1) \
			or not _same_number(snapshot.get("sequence", null), int(lesson.get("sequence", 0))) \
			or not _same_number(snapshot.get("tier", null), int(lesson.get("tier", 0))):
		return
	var saved_counted: Variant = snapshot.get("counted", [])
	if saved_counted is Array:
		for index in range(mini(counted.size(), saved_counted.size())):
			counted[index] = typeof(saved_counted[index]) == TYPE_BOOL and saved_counted[index]
	joined = lesson_kind() != "add" or snapshot.get("joined", false) == true \
		and typeof(snapshot.get("joined", false)) == TYPE_BOOL
	if not joined:
		counted.fill(false)
	var attempts: Variant = snapshot.get("wrong_attempts", 0)
	wrong_attempts = clampi(int(attempts), 0, 99) if _whole_number(attempts) else 0
	assisted = wrong_attempts > 0 or (typeof(snapshot.get("assisted", false)) == TYPE_BOOL \
		and snapshot.get("assisted", false) == true)
	help_visible = assisted
	_restored_complete = can_answer() and _same_number(snapshot.get("chosen", null), answer_index())
	chosen = answer_index() if _restored_complete else -1
	cancel_input(false)
	_update_numerals()
	queue_redraw()

func _whole_number(value: Variant) -> bool:
	return typeof(value) in [TYPE_INT, TYPE_FLOAT] and is_finite(float(value)) \
		and float(value) == floorf(float(value))

func _same_number(value: Variant, expected: int) -> bool:
	return _whole_number(value) and float(value) == float(expected)

func cancel_input(checkpoint := true) -> void:
	touch_owner = -1
	held = false
	if checkpoint:
		progress_changed.emit(progress_snapshot())

func restart_demo() -> void:
	if solved or armed_only:
		return
	assisted = true
	help_visible = true
	demo_active = true
	idle_demo_t = 0.0
	progress_changed.emit(progress_snapshot())
	guidance_requested.emit("teacher_help")
	queue_redraw()

func _press(at: Vector2) -> void:
	if armed_only or solved or completion_accepted:
		return
	held = true
	press_at = at
	pointer_pos = at

func _release(at: Vector2) -> void:
	if not held:
		return
	held = false
	touch_owner = -1
	if armed_only or solved or completion_accepted or at.distance_to(press_at) > 38.0:
		return
	if at.distance_to(HINT_CENTER) <= 40.0:
		restart_demo()
		return
	if lesson_kind() == "add" and not joined:
		if at.distance_to(JOIN_CENTER) <= 65.0:
			joined = true
			join_t = 0.4
			_changed()
		return
	if join_t > 0.0:
		return
	for index in range(counted.size()):
		if not counted[index] and at.distance_to(counter_position(index)) <= 36.0:
			counted[index] = true
			counter_touched.emit(counted.count(true))
			_changed()
			return
	if not can_answer():
		return
	var choices: Array = lesson.get("choices", []) as Array
	for index in range(choices.size()):
		if choice_rect(index).has_point(at):
			chosen = index
			if index == answer_index():
				_complete()
			else:
				wrong_attempts += 1
				assisted = true
				help_visible = true
				guidance_requested.emit("teacher_help")
				feedback_anchor = at
				feedback_t = 0.4
				_changed()
			return

func _changed() -> void:
	input_started = true
	demo_active = false
	progress_changed.emit(progress_snapshot())
	_update_numerals()
	queue_redraw()

func _complete() -> void:
	if solved:
		return
	solved = true
	chosen = answer_index()
	demo_active = false
	lesson_completed.emit(lesson_kind(), assisted)
	gesture.emit(mode, 1.0, 1.0)
	progress_changed.emit(progress_snapshot())
	queue_redraw()

func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed and touch_owner == -1 and not armed_only and not solved:
			touch_owner = touch.index
			_press(touch.position)
		elif not touch.pressed and touch.index == touch_owner:
			if touch.canceled:
				cancel_input()
			else:
				_release(touch.position)
		accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION or button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed and touch_owner == -1 and not armed_only and not solved:
			touch_owner = -2
			_press(button.position)
		elif not button.pressed and touch_owner == -2:
			_release(button.position)
		accept_event()

func _notification(what: int) -> void:
	if what in [NOTIFICATION_PAUSED, NOTIFICATION_APPLICATION_PAUSED,
			NOTIFICATION_APPLICATION_FOCUS_OUT]:
		cancel_input()

func _process(delta: float) -> void:
	if _restored_complete and not armed_only:
		_restored_complete = false
		_complete()
	join_t = maxf(0.0, join_t - delta)
	feedback_t = maxf(0.0, feedback_t - delta)
	idle_demo_t += delta
	if fmod(idle_demo_t, 0.06) < delta:
		queue_redraw()

func _update_numerals() -> void:
	for label: Label in _numerals:
		label.queue_free()
	_numerals.clear()
	if int(lesson.get("tier", 0)) == 0 or lesson_kind() not in ["count", "add"]:
		return
	var choices: Array = lesson.get("choices", []) as Array
	for index in range(choices.size()):
		var label := Label.new()
		label.text = str(int(choices[index]))
		StorybookUI._apply_label_typography(label, StorybookUI.ROLE_NUMERIC)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.position = choice_rect(index).position + Vector2(0, 128)
		label.size = Vector2(210, 40)
		label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(label)
		_numerals.append(label)

func _draw() -> void:
	if lesson.is_empty():
		return
	draw_style_box(StorybookUI.panel_style(Color("#a57ab3"), Color("#f8ead5"), 32, 7), BOARD)
	draw_line(Vector2(375, 420), Vector2(1135, 420), Color("#d8c2d3"), 4, true)
	_draw_hint_button()
	match lesson_kind():
		"pattern":
			_draw_pattern()
		"match":
			_draw_shape(int(lesson.get("target", 0)), Vector2(755, 285), 68.0)
		"count", "add":
			_draw_counting()
	var choices: Array = lesson.get("choices", []) as Array
	for index in range(choices.size()):
		var card := choice_rect(index)
		var fill := Color("#fffaf0") if can_answer() else Color("#dfdcde")
		if solved and index == chosen:
			fill = Color("#b6eadc")
		elif help_visible and can_answer() and index == answer_index():
			fill = Color("#fff0a9")
		draw_style_box(StorybookUI.panel_style(INK, fill, 25, 5), card)
		if lesson_kind() in ["count", "add"]:
			var amount := int(choices[index])
			var pearl_radius := _group_radius(amount, card.size.x - 24.0, 40.0)
			_draw_group(amount, card.get_center() + Vector2(0, -15),
				pearl_radius, Color("#75d3df"))
		else:
			_draw_shape(int(choices[index]), card.get_center(), 49.0)
	if not solved:
		_draw_demo()
	else:
		var at := choice_rect(answer_index()).get_center()
		for index in range(6):
			var angle := float(index) * TAU / 6.0 + idle_demo_t * 0.3
			_draw_shape(3, at + Vector2.from_angle(angle) * 118.0, 10.0)

func _draw_hint_button() -> void:
	draw_circle(HINT_CENTER, 30, Color("#e4d3ee"))
	draw_arc(HINT_CENTER - Vector2(0, 4), 12, PI, TAU + PI * 0.65, 24, INK, 5, true)
	draw_line(HINT_CENTER + Vector2(-7, 13), HINT_CENTER + Vector2(7, 13), INK, 4, true)
	for index in range(3):
		var at := HINT_CENTER + Vector2.from_angle(-PI * 0.8 + float(index) * 0.8) * 23
		draw_circle(at, 3, Color("#b18355"))

func _draw_pattern() -> void:
	var tokens: Array = lesson.get("prompt_tokens", []) as Array
	var step := 91.0
	var start := 755.0 - float(tokens.size()) * step * 0.5
	for index in range(tokens.size()):
		var at := Vector2(start + float(index) * step, 285)
		_draw_shape(int(tokens[index]), at, 32.0)
		if int(idle_demo_t / 0.6) % (tokens.size() + 1) == index and not solved:
			draw_arc(at, 42, 0, TAU, 32, Color("#c29acb"), 4, true)
	var blank := Vector2(start + float(tokens.size()) * step, 285)
	if solved:
		_draw_shape(int(lesson.get("target", 0)), blank, 32)
	else:
		draw_style_box(StorybookUI.panel_style(INK, Color("#e8ddeb"), 16, 3),
			Rect2(blank - Vector2(37, 45), Vector2(74, 90)))
		draw_line(blank - Vector2(16, 0), blank + Vector2(16, 0), Color("#947ca9"), 5)

func _draw_counting() -> void:
	if lesson_kind() == "add" and not joined:
		var operands: Array = lesson.get("operands", [1, 1]) as Array
		draw_style_box(StorybookUI.panel_style(INK, Color("#d8eff0"), 30, 4), Rect2(410, 200, 265, 205))
		draw_style_box(StorybookUI.panel_style(INK, Color("#f5d8e4"), 30, 4), Rect2(835, 200, 265, 205))
		var left_amount := int(operands[0])
		var right_amount := int(operands[1])
		_draw_group(left_amount, Vector2(542, 295),
			_group_radius(left_amount, 241.0, 40.0), Color("#74d5df"))
		_draw_group(right_amount, Vector2(967, 295),
			_group_radius(right_amount, 241.0, 40.0), Color("#efa3c7"))
		draw_circle(JOIN_CENTER, 49, Color("#f0d48c"))
		draw_arc(JOIN_CENTER, 49, 0, TAU, 40, INK, 5, true)
		draw_line(JOIN_CENTER - Vector2(22, 0), JOIN_CENTER + Vector2(22, 0), INK, 8, true)
		draw_line(JOIN_CENTER - Vector2(0, 22), JOIN_CENTER + Vector2(0, 22), INK, 8, true)
		return
	for index in range(counted.size()):
		var at := counter_position(index)
		if join_t > 0.0:
			var operands: Array = lesson.get("operands", [1, 1]) as Array
			var start := Vector2(542 if index < int(operands[0]) else 967, 295)
			at = start.lerp(at, 1.0 - join_t / 0.4)
		var color := Color("#f4cf79") if counted[index] else Color("#78d9df")
		draw_circle(at + Vector2(0, 4), 31, Color("#b99bba"))
		draw_circle(at, 29, INK)
		draw_circle(at, 24, color)
		draw_circle(at - Vector2(8, 8), 7, Color(1, 1, 1, 0.6))
		if counted[index]:
			draw_line(at + Vector2(-10, 0), at + Vector2(-2, 8), INK, 4, true)
			draw_line(at + Vector2(-2, 8), at + Vector2(11, -8), INK, 4, true)

func _group_radius(amount: int, available_width: float,
		max_radius: float) -> float:
	var columns := mini(5, maxi(1, amount))
	# _draw_group spaces centers by 1.55r. Each pearl reaches 0.65r +
	# the 3px outline beyond its center, so this bounds the complete row.
	var width_factor := float(columns - 1) * 1.55 + 1.30
	var width_bound := (available_width - 6.0) / width_factor
	return minf(max_radius, width_bound)


func _draw_group(amount: int, center: Vector2, radius: float, color: Color) -> void:
	var columns := mini(5, amount)
	for index in range(amount):
		var row := index / 5
		var row_count := mini(5, amount - row * 5)
		var x := (float(index % 5) - float(row_count - 1) * 0.5) * radius * 1.55
		var y := (float(row) - (0.5 if amount > columns else 0.0)) * radius * 1.65
		var at := center + Vector2(x, y)
		draw_circle(at, radius * 0.65 + 3, INK)
		draw_circle(at, radius * 0.65, color)
		draw_circle(at - Vector2(radius * 0.2, radius * 0.2), radius * 0.16, Color("#fff7dc"))

func _draw_shape(shape: int, at: Vector2, radius: float) -> void:
	var color: Color = TOKEN_COLORS[posmod(shape, TOKEN_COLORS.size())]
	if shape == 0:
		draw_circle(at, radius, INK)
		draw_circle(at, radius - 6, color)
		return
	if shape == 2:
		draw_style_box(StorybookUI.panel_style(INK, color, 8, 6),
			Rect2(at - Vector2.ONE * radius * 0.8, Vector2.ONE * radius * 1.6))
		return
	var points := PackedVector2Array()
	if shape == 1:
		points = PackedVector2Array([at + Vector2(0,-radius),
			at + Vector2(radius * 0.92, radius * 0.75), at + Vector2(-radius * 0.92, radius * 0.75)])
	elif shape == 3:
		for index in range(10):
			points.append(at + Vector2.from_angle(-PI * 0.5 + float(index) * PI / 5.0)
				* radius * (1.0 if index % 2 == 0 else 0.48))
	else:
		for index in range(36):
			var t := float(index) * TAU / 36.0
			points.append(at + Vector2(16.0 * pow(sin(t), 3),
				-(13.0 * cos(t) - 5.0 * cos(2*t) - 2.0 * cos(3*t) - cos(4*t))) * radius / 18.0)
	draw_colored_polygon(points, color)
	var outline := points.duplicate()
	outline.append(points[0])
	draw_polyline(outline, INK, 6, true)

func _draw_demo() -> void:
	var at := Vector2.ZERO
	if lesson_kind() == "add" and not joined:
		at = JOIN_CENTER
	elif counted.has(false):
		at = counter_position(counted.find(false))
	elif help_visible:
		at = choice_rect(answer_index()).get_center()
	elif lesson_kind() == "pattern":
		return
	else:
		return
	var pulse := 1.0 + sin(idle_demo_t * 4) * 0.12
	draw_arc(at, 41.0 * pulse, 0, TAU, 32, Color("#f2d58e"), 6, true)
	draw_circle(at + Vector2(25, 34), 11, Color("#fff4d5"))
