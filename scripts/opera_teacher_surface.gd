class_name OperaTeacherSurface
extends OperaGestureSurface
## One-finger, concrete early maths. Time never answers a lesson.
const Lessons := preload("res://scripts/teacher_lesson_plan.gd")
const BOARD := Rect2(330, 105, 850, 555)
const HINT_CENTER := Vector2(1115, 150)
const JOIN_CENTER := Vector2(755, 325)
const TEACHER_ART := "res://assets/opera/worlds/teacher/"
const SHAPE_NAMES := ["circle", "triangle", "square", "star", "heart"]
const GUIDE_HAND := "res://assets/opera/worlds/teacher/guide_hand.png"
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
var _teacher_textures: Dictionary = {}

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

func _paint(asset: String, rect: Rect2) -> void:
	var path := GUIDE_HAND if asset == "guide_hand" else TEACHER_ART + asset + ".png"
	if not _teacher_textures.has(path):
		_teacher_textures[path] = load(path) as Texture2D
	var picture: Texture2D = _teacher_textures[path] as Texture2D
	assert(picture != null, "Missing painted Teacher object: " + path)
	var dimensions := picture.get_size()
	var ratio := minf(rect.size.x / dimensions.x, rect.size.y / dimensions.y)
	var fitted := dimensions * ratio
	draw_texture_rect(picture, Rect2(rect.get_center() - fitted * 0.5, fitted), false)

func _draw() -> void:
	if lesson.is_empty():
		return
	# The object is drawn whole, uniformly fitted. Input/lesson coordinates stay fixed.
	_paint("lesson_board", Rect2(300, 56, 910, 654))
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
		var state := "rest"
		if solved and index == chosen or help_visible and can_answer() and index == answer_index():
			state = "right"
		elif index == chosen:
			state = "chosen"
		_paint("answer_card_" + state, card)
		if lesson_kind() in ["count", "add"]:
			var amount := int(choices[index])
			# Whole square cards fit the old rectangular hits. Pearls stay inside their blank face.
			var pearl_radius := _group_radius(amount, minf(card.size.x, card.size.y) - 44.0, 40.0)
			_draw_group(amount, card.get_center() + Vector2(0, -15), pearl_radius)
		else:
			_draw_shape(int(choices[index]), card.get_center(), 49.0)
	if not solved:
		_draw_demo()
	else:
		var at := choice_rect(answer_index()).get_center()
		for index in range(6):
			var angle := float(index) * TAU / 6.0 + idle_demo_t * 0.3
			_draw_shape(3, at + Vector2.from_angle(angle) * 118.0, 10.0, true)

func _draw_hint_button() -> void:
	_paint("shape_slot", Rect2(HINT_CENTER - Vector2(32, 32), Vector2(64, 64)))
	_paint_hand(HINT_CENTER + Vector2(0, 18), 50.0)

func _draw_pattern() -> void:
	var tokens: Array = lesson.get("prompt_tokens", []) as Array
	var step := 91.0
	var start := 755.0 - float(tokens.size()) * step * 0.5
	for index in range(tokens.size()):
		var at := Vector2(start + float(index) * step, 285)
		var lit := int(idle_demo_t / 0.6) % (tokens.size() + 1) == index and not solved
		_draw_shape(int(tokens[index]), at, 32.0, lit)
	var blank := Vector2(start + float(tokens.size()) * step, 285)
	if solved:
		_draw_shape(int(lesson.get("target", 0)), blank, 32, true)
	else:
		_paint("shape_slot", Rect2(blank - Vector2(37, 45), Vector2(74, 90)))

func _draw_counting() -> void:
	if lesson_kind() == "add" and not joined:
		var operands: Array = lesson.get("operands", [1, 1]) as Array
		_paint("tray_aqua", Rect2(410, 200, 265, 205))
		_paint("tray_pink", Rect2(835, 200, 265, 205))
		var left_amount := int(operands[0])
		var right_amount := int(operands[1])
		_draw_group(left_amount, Vector2(542, 295), _group_radius(left_amount, 190.0, 40.0))
		_draw_group(right_amount, Vector2(967, 295), _group_radius(right_amount, 190.0, 40.0))
		_paint("join_shell", Rect2(JOIN_CENTER - Vector2(56, 56), Vector2(112, 112)))
		return
	for index in range(counted.size()):
		var at := counter_position(index)
		if join_t > 0.0:
			var operands: Array = lesson.get("operands", [1, 1]) as Array
			var start := Vector2(542 if index < int(operands[0]) else 967, 295)
			at = start.lerp(at, 1.0 - join_t / 0.4)
		var state := "counted" if counted[index] else "uncounted"
		_paint("pearl_" + state, Rect2(at - Vector2(31, 31), Vector2(62, 62)))

func _group_radius(amount: int, available_width: float,
		max_radius: float) -> float:
	var columns := mini(5, maxi(1, amount))
	# _draw_group spaces centers by 1.55r. Each pearl reaches 0.65r +
	# the 3px outline beyond its center, so this bounds the complete row.
	var width_factor := float(columns - 1) * 1.55 + 1.30
	var width_bound := (available_width - 6.0) / width_factor
	return minf(max_radius, width_bound)


func _draw_group(amount: int, center: Vector2, radius: float) -> void:
	var columns := mini(5, amount)
	for index in range(amount):
		var row := index / 5
		var row_count := mini(5, amount - row * 5)
		var x := (float(index % 5) - float(row_count - 1) * 0.5) * radius * 1.55
		var y := (float(row) - (0.5 if amount > columns else 0.0)) * radius * 1.65
		var at := center + Vector2(x, y)
		var side := radius * 1.3 + 6.0
		_paint("pearl_uncounted", Rect2(at - Vector2.ONE * side * 0.5, Vector2.ONE * side))

func _draw_shape(shape: int, at: Vector2, radius: float, lit := false) -> void:
	var name: String = SHAPE_NAMES[posmod(shape, SHAPE_NAMES.size())]
	var state := "lit" if lit else "rest"
	_paint("shape_" + name + "_" + state,
		Rect2(at - Vector2.ONE * radius, Vector2.ONE * radius * 2.0))

func _draw_demo() -> void:
	var at := Vector2.ZERO
	if lesson_kind() == "add" and not joined:
		at = JOIN_CENTER
	elif counted.has(false):
		at = counter_position(counted.find(false))
	elif help_visible:
		at = choice_rect(answer_index()).get_center()
	else:
		return
	var offset := Vector2(0, sin(idle_demo_t * 4.0) * 3.0)
	# Reuse the authored pointing hand rather than drawing a ring over the object.
	_paint_hand(at + offset, 58.0)

func _paint_hand(tip: Vector2, side: float) -> void:
	var tip_uv := Vector2(0.436523, 0.986328)
	_paint("guide_hand", Rect2(tip - tip_uv * side, Vector2.ONE * side))
