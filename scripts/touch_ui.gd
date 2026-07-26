extends CanvasLayer
# Touch controls (Android/tablet):
#   HYBRID (default): lower-left movement + a real lower-right action button;
#   taps on unclaimed world space are emitted for select/approach/move.
#   CLASSIC (rollback): the shipped drag-anywhere stick, tap action and
#   second-finger camera path is retained below.
# Implemented through _unhandled_input so overlays and minigame Controls always
# receive first claim. A touch has one owner for its lifetime; ownership never
# changes mid-gesture.

signal world_touched(pos: Vector2)
signal manual_move_started
signal manual_move_ended

enum TouchOwner {
	NONE,
	UI,
	STICK,
	ACTION,
	WORLD_INTERACT,
	WORLD_MOVE,
}

var stick_vec := Vector2.ZERO
var action_down := false
var action_just := false
var control_mode := "hybrid"
var touch_owners: Dictionary = {}
var world_controls_enabled := true

var _root: Control
var _base: Panel
var _knob: Panel
var _btn: Button
var _act_button: Button = null
var _touch_idx := -1
var _jump_fingers := {}
var _pend := {}
var _world_pend := {}
var _look_idx := -1
var _look_dx := 0.0
var _look_dy := 0.0
var _origin := Vector2.ZERO
var _moved := false
var _manual_emitted := false
var _press_ms := 0
var _pulse := 0.0
var _act_vis: Panel = null
var _act_lbl: Label = null
var _act_t := 0.0
var _action_edge_frames := 0

const R := 78.0
const TAP_SLOP := 22.0
const TAP_MS := 300
const JUMP_HOLD_MS := 140
const ACTION_PICTOGRAMS := {
	"JUMP": "↑",
	"PLAY": "▶",
	"SHOP": "◆",
	"OPEN": "◇",
	"SLIDE": "↘",
	"RACE": "⚑",
	"ENTER": "✦",
	"SHOW": "♬",
	"GET": "★",
	"SLEEP": "☾",
	"DRESS": "♛",
	"MAKE": "✂",
	"RING": "♫",
	"TOUCH": "✧",
	"HUG": "♥",
	"EXIT": "↩",
	"CATCH!": "✋",
	"THROW": "➶",
	"BUY": "◆",
	"SWIM": "➜",
}

func _ready() -> void:
	layer = 9
	process_mode = Node.PROCESS_MODE_ALWAYS
	_root = Control.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_root)
	_base = _circle(Color(0.45, 0.85, 0.95, 0.45), 90.0)
	var bsb: StyleBoxFlat = _base.get_theme_stylebox("panel") as StyleBoxFlat
	bsb.border_color = Color(0.55, 1.0, 0.85, 0.95)
	bsb.set_border_width_all(5)
	_knob = _circle(Color(1, 1, 1, 0.55), 46.0)
	_base.visible = false
	_knob.visible = false
	_root.add_child(_base)
	_root.add_child(_knob)
	call_deferred("_rest_stick")
	_btn = Button.new()
	_btn.visible = false
	_root.add_child(_btn)
	# A 176 px real hit target surrounds the 156 px visible action bubble.
	# Classic mode disables this Control and keeps the original all-screen tap.
	if wants_touch():
		_act_button = Button.new()
		_act_button.flat = true
		_act_button.focus_mode = Control.FOCUS_NONE
		_act_button.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
		_act_button.offset_left = -204.0
		_act_button.offset_top = -224.0
		_act_button.offset_right = -28.0
		_act_button.offset_bottom = -48.0
		var empty := StyleBoxEmpty.new()
		for style_name: String in ["normal", "hover", "pressed", "focus"]:
			_act_button.add_theme_stylebox_override(style_name, empty)
		_act_button.button_down.connect(_on_action_button_down)
		_act_button.button_up.connect(_on_action_button_up)
		_root.add_child(_act_button)
		_act_vis = _circle(Color(1.0, 0.75, 0.88, 0.42), 78.0)
		_act_vis.position = Vector2(10.0, 10.0)
		_act_button.add_child(_act_vis)
		_act_lbl = Label.new()
		_act_lbl.text = _action_display("JUMP")
		_act_lbl.add_theme_font_size_override("font_size", 30)
		_act_lbl.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
		_act_lbl.add_theme_color_override("font_outline_color", Color(0.2, 0.15, 0.35, 0.9))
		_act_lbl.add_theme_constant_override("outline_size", 8)
		_act_lbl.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_act_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_act_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		_act_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_act_vis.add_child(_act_lbl)
	set_mode(control_mode)

func _process(delta: float) -> void:
	if _pulse > 0.0:
		_pulse -= delta
		if _pulse <= 0.0 and _jump_fingers.is_empty() and not (_act_button != null and _act_button.button_pressed):
			action_down = false
	# This classification is intentionally Classic-only. Hybrid gives the
	# right-side action button and the world tap separate ownership.
	if control_mode == "classic" and not _pend.is_empty():
		var now := Time.get_ticks_msec()
		for idx: Variant in _pend.keys():
			if now - int(_pend[idx]["ms"]) >= JUMP_HOLD_MS:
				_jump_fingers[idx] = true
				action_down = true
				_arm_action_edge()
				_flash(_pend[idx]["pos"])
				_pend.erase(idx)
	if _act_vis != null:
		_act_t += delta
		var pulse_s: float = 1.0 + sin(_act_t * 2.2) * 0.045
		_act_vis.pivot_offset = _act_vis.size * 0.5
		_act_vis.scale = Vector2(pulse_s, pulse_s) * (0.88 if action_down else 1.0)
	if action_just:
		if _action_edge_frames > 0:
			_action_edge_frames -= 1
		else:
			action_just = false

func _circle(col: Color, rad: float) -> Panel:
	var panel := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(rad))
	panel.add_theme_stylebox_override("panel", sb)
	panel.size = Vector2(rad * 2.0, rad * 2.0)
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return panel

func _jump_pulse() -> void:
	action_down = true
	_arm_action_edge()
	_pulse = 0.18

func _arm_action_edge() -> void:
	# action_just is an input edge, not a remembered wish. Two child-process
	# frames let the parent consume it regardless of scene-tree process order,
	# then it expires so an old press cannot launch a newly focused activity.
	action_just = true
	_action_edge_frames = 2

func _flash(pos: Vector2) -> void:
	var flash := _circle(Color(1.0, 0.95, 0.5, 0.5), 55.0)
	flash.position = pos - flash.size * 0.5
	_root.add_child(flash)
	var tw := flash.create_tween()
	tw.tween_property(flash, "modulate:a", 0.0, 0.35)
	tw.tween_callback(flash.queue_free)

func _press(pos: Vector2, idx: int) -> void:
	_touch_idx = idx
	_origin = pos
	_moved = false
	_manual_emitted = false
	_press_ms = Time.get_ticks_msec()
	_base.position = _origin - _base.size * 0.5
	_knob.position = _origin - _knob.size * 0.5
	_base.modulate.a = 1.0
	_knob.modulate.a = 1.0
	_base.visible = true
	_knob.visible = true
	stick_vec = Vector2.ZERO

func _drag(pos: Vector2) -> void:
	var off: Vector2 = pos - _origin
	if not _moved and off.length() > TAP_SLOP:
		_moved = true
	if off.length() > R:
		off = off.normalized() * R
	if _moved and off.length() > 0.0:
		var mag := clampf((off.length() - TAP_SLOP) / (R - TAP_SLOP), 0.0, 1.0)
		stick_vec = off.normalized() * mag
	else:
		stick_vec = Vector2.ZERO
	_knob.position = _origin + off - _knob.size * 0.5
	if control_mode == "hybrid" and not _manual_emitted and stick_vec.length() > 0.05:
		_manual_emitted = true
		manual_move_started.emit()

func _release_stick() -> void:
	if control_mode == "classic" and not _moved and (Time.get_ticks_msec() - _press_ms) <= TAP_MS:
		_jump_pulse()
		_flash(_origin)
	if _manual_emitted:
		manual_move_ended.emit()
	_touch_idx = -1
	_manual_emitted = false
	stick_vec = Vector2.ZERO
	_rest_stick()

func _rest_stick() -> void:
	if _base == null or _knob == null:
		return
	if not wants_touch() or not world_controls_enabled:
		_base.visible = false
		_knob.visible = false
		return
	var vs: Vector2 = _root.size
	if vs == Vector2.ZERO:
		vs = get_viewport().get_visible_rect().size
	var center := Vector2(170.0, vs.y - 170.0)
	_base.position = center - _base.size * 0.5
	_knob.position = center - _knob.size * 0.5
	_base.modulate.a = 0.55
	_knob.modulate.a = 0.55
	_base.visible = true
	_knob.visible = true

func rest_zone() -> Rect2:
	var vs: Vector2 = _root.size
	if vs == Vector2.ZERO:
		vs = get_viewport().get_visible_rect().size
	return Rect2(Vector2(60.0, vs.y - 280.0), Vector2(220.0, 220.0))

func movement_zone() -> Rect2:
	# The whole lower-left thumb bay accepts the stick, while the resting ring
	# teaches the preferred landing spot. It ends well before the action button.
	var vs: Vector2 = _root.size
	if vs == Vector2.ZERO:
		vs = get_viewport().get_visible_rect().size
	return Rect2(0.0, vs.y * 0.52, maxf(390.0, vs.x * 0.34), vs.y * 0.48)

func action_zone() -> Rect2:
	if _act_button != null:
		return _act_button.get_global_rect()
	var vs: Vector2 = _root.size
	if vs == Vector2.ZERO:
		vs = get_viewport().get_visible_rect().size
	return Rect2(vs - Vector2(214.0, 234.0), Vector2(214.0, 234.0))

func _clear_touch_state() -> void:
	_touch_idx = -1
	_look_idx = -1
	_jump_fingers.clear()
	_pend.clear()
	_world_pend.clear()
	touch_owners.clear()
	stick_vec = Vector2.ZERO
	action_down = false
	action_just = false
	_action_edge_frames = 0
	_look_dx = 0.0
	_look_dy = 0.0
	_moved = false
	_manual_emitted = false
	_pulse = 0.0
	_rest_stick()

func set_mode(next_mode: String) -> void:
	control_mode = "classic" if next_mode == "classic" else "hybrid"
	_clear_touch_state()
	if _act_button != null:
		_act_button.mouse_filter = Control.MOUSE_FILTER_STOP if control_mode == "hybrid" and world_controls_enabled else Control.MOUSE_FILTER_IGNORE
		_act_button.visible = control_mode == "hybrid" and world_controls_enabled

func set_world_controls_enabled(enabled: bool) -> void:
	if world_controls_enabled == enabled:
		if not enabled:
			_clear_touch_state()
		return
	world_controls_enabled = enabled
	_clear_touch_state()
	if _act_button != null:
		_act_button.visible = enabled and control_mode == "hybrid"
		_act_button.mouse_filter = Control.MOUSE_FILTER_STOP if enabled and control_mode == "hybrid" else Control.MOUSE_FILTER_IGNORE

func cancel_all_touches() -> void:
	_clear_touch_state()

func clear_action_edge() -> void:
	action_just = false
	_action_edge_frames = 0

func _on_action_button_down() -> void:
	if control_mode != "hybrid" or not world_controls_enabled:
		return
	action_down = true
	_arm_action_edge()
	_pulse = 0.0
	_flash(action_zone().get_center())

func _on_action_button_up() -> void:
	if control_mode == "hybrid":
		action_down = false

func consume_action() -> void:
	action_down = false
	clear_action_edge()
	_pulse = 0.0

func _request_pause() -> void:
	var main: Node = get_parent()
	if main != null and main.has_method("toggle_pause"):
		main.toggle_pause()

func _flush_parent_save() -> void:
	var main: Node = get_parent()
	if main != null and main.has_method("_write_save"):
		main.call("_write_save")

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		_clear_touch_state()
	elif what == NOTIFICATION_APPLICATION_PAUSED:
		_clear_touch_state()
		_flush_parent_save()
	elif what == NOTIFICATION_WM_GO_BACK_REQUEST:
		_clear_touch_state()
		_request_pause()
	elif what == NOTIFICATION_WM_CLOSE_REQUEST:
		_clear_touch_state()
		_flush_parent_save()

func _unhandled_input(ev: InputEvent) -> void:
	if not wants_touch() or not world_controls_enabled:
		return
	if control_mode == "hybrid":
		_hybrid_unhandled_input(ev)
	else:
		_classic_unhandled_input(ev)

func _hybrid_unhandled_input(ev: InputEvent) -> void:
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		if touch.pressed:
			if _touch_idx == -1 and movement_zone().has_point(touch.position):
				touch_owners[touch.index] = TouchOwner.STICK
				_press(touch.position, touch.index)
			else:
				touch_owners[touch.index] = TouchOwner.WORLD_INTERACT
				_world_pend[touch.index] = {"pos": touch.position, "moved": false}
		else:
			var owner: int = int(touch_owners.get(touch.index, TouchOwner.NONE))
			if owner == TouchOwner.STICK and touch.index == _touch_idx:
				_release_stick()
			elif (owner == TouchOwner.WORLD_INTERACT or owner == TouchOwner.WORLD_MOVE) and _world_pend.has(touch.index):
				var world_data: Dictionary = _world_pend[touch.index]
				if owner == TouchOwner.WORLD_INTERACT and not bool(world_data.get("moved", false)):
					world_touched.emit(touch.position)
					_flash(touch.position)
				_world_pend.erase(touch.index)
			touch_owners.erase(touch.index)
	elif ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		var owner: int = int(touch_owners.get(drag.index, TouchOwner.NONE))
		if owner == TouchOwner.STICK and drag.index == _touch_idx:
			_drag(drag.position)
		elif owner == TouchOwner.WORLD_INTERACT and _world_pend.has(drag.index):
			var world_data: Dictionary = _world_pend[drag.index]
			if (drag.position - (world_data["pos"] as Vector2)).length() > TAP_SLOP:
				world_data["moved"] = true
				touch_owners[drag.index] = TouchOwner.WORLD_MOVE
	elif ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device == InputEvent.DEVICE_ID_EMULATION or mouse_button.button_index != MOUSE_BUTTON_LEFT:
			return
		if mouse_button.pressed:
			if _touch_idx == -1 and movement_zone().has_point(mouse_button.position):
				touch_owners[99] = TouchOwner.STICK
				_press(mouse_button.position, 99)
			else:
				touch_owners[99] = TouchOwner.WORLD_INTERACT
				_world_pend[99] = {"pos": mouse_button.position, "moved": false}
		else:
			var owner: int = int(touch_owners.get(99, TouchOwner.NONE))
			if owner == TouchOwner.STICK and _touch_idx == 99:
				_release_stick()
			elif (owner == TouchOwner.WORLD_INTERACT or owner == TouchOwner.WORLD_MOVE) and _world_pend.has(99):
				var world_data: Dictionary = _world_pend[99]
				if owner == TouchOwner.WORLD_INTERACT and not bool(world_data.get("moved", false)):
					world_touched.emit(mouse_button.position)
					_flash(mouse_button.position)
				_world_pend.erase(99)
			touch_owners.erase(99)
	elif ev is InputEventMouseMotion and touch_owners.get(99, TouchOwner.NONE) == TouchOwner.STICK:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device != InputEvent.DEVICE_ID_EMULATION:
			_drag(mouse_motion.position)
	elif ev is InputEventMouseMotion and touch_owners.get(99, TouchOwner.NONE) == TouchOwner.WORLD_INTERACT:
		var world_motion := ev as InputEventMouseMotion
		if world_motion.device != InputEvent.DEVICE_ID_EMULATION and _world_pend.has(99):
			var world_data: Dictionary = _world_pend[99]
			if (world_motion.position - (world_data["pos"] as Vector2)).length() > TAP_SLOP:
				world_data["moved"] = true
				touch_owners[99] = TouchOwner.WORLD_MOVE

# Reversible shipped input path. Keep behavioral edits to this method out of the
# hybrid experiment so selecting Classic is a genuine runtime rollback.
func _classic_unhandled_input(ev: InputEvent) -> void:
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		if touch.pressed:
			if _touch_idx == -1:
				_press(touch.position, touch.index)
			elif touch.index != _touch_idx:
				_pend[touch.index] = {"pos": touch.position, "ms": Time.get_ticks_msec()}
		else:
			if touch.index == _touch_idx:
				_release_stick()
			elif _pend.has(touch.index):
				_pend.erase(touch.index)
				_jump_pulse()
				_flash(touch.position)
			elif touch.index == _look_idx:
				_look_idx = -1
			elif _jump_fingers.has(touch.index):
				_jump_fingers.erase(touch.index)
				if _jump_fingers.is_empty() and _pulse <= 0.0:
					action_down = false
	elif ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		if drag.index == _touch_idx:
			_drag(drag.position)
		elif _pend.has(drag.index):
			if (drag.position - (_pend[drag.index]["pos"] as Vector2)).length() > TAP_SLOP:
				_pend.erase(drag.index)
				if _look_idx == -1:
					_look_idx = drag.index
				else:
					_jump_fingers[drag.index] = true
					action_down = true
					_arm_action_edge()
		elif drag.index == _look_idx:
			_look_dx += drag.relative.x
			_look_dy += drag.relative.y
	elif ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device == InputEvent.DEVICE_ID_EMULATION:
			return
		if mouse_button.button_index == MOUSE_BUTTON_LEFT:
			if mouse_button.pressed and _touch_idx == -1:
				_press(mouse_button.position, 99)
			elif not mouse_button.pressed and _touch_idx == 99:
				_release_stick()
	elif ev is InputEventMouseMotion and _touch_idx == 99:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag(mouse_motion.position)

func set_action_label(text: String) -> void:
	var display_text: String = _action_display(text)
	if _btn != null and _btn.text != display_text:
		_btn.text = display_text
	if _act_lbl != null and _act_lbl.text != display_text:
		_act_lbl.text = display_text

func _action_display(text: String) -> String:
	var pictogram: String = String(ACTION_PICTOGRAMS.get(text, "✦"))
	return "%s\n%s" % [pictogram, text]

func consume_action_just() -> bool:
	var just_pressed := action_just
	clear_action_edge()
	return just_pressed

func look_active() -> bool:
	return control_mode == "classic" and _look_idx != -1

func consume_look() -> Vector2:
	var look := Vector2(clampf(_look_dx, -120.0, 120.0), clampf(_look_dy, -120.0, 120.0))
	_look_dx = 0.0
	_look_dy = 0.0
	return look

func _input(ev: InputEvent) -> void:
	var toggle := false
	if ev is InputEventKey and (ev as InputEventKey).pressed and not (ev as InputEventKey).echo:
		if (ev as InputEventKey).physical_keycode == KEY_ESCAPE:
			toggle = true
	elif ev is InputEventJoypadButton and (ev as InputEventJoypadButton).pressed:
		if (ev as InputEventJoypadButton).button_index == JOY_BUTTON_START:
			toggle = true
	if toggle:
		_request_pause()

static func wants_touch() -> bool:
	return DisplayServer.is_touchscreen_available() or OS.has_feature("mobile") or "--touch" in OS.get_cmdline_user_args()
