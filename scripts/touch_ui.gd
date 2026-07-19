extends CanvasLayer
# Touch controls (Android/tablet):
#   * drag anywhere on EMPTY screen -> a virtual stick appears under your finger
#   * quick tap (no drag)           -> jump/action
#   * a SECOND finger: tap or hold  -> jump (held = swim up, as before)
#                      DRAG         -> camera look-around (peek, drifts back)
#     which one is decided after TAP_SLOP px of movement or JUMP_HOLD_MS,
#     whichever comes first — same trick the stick uses to split tap vs steer
# Implemented via _unhandled_input, so every button / 2D minigame / overlay control
# (any canvas layer) gets first claim on its taps — the stick only sees touches
# nothing else wanted. No fixed buttons, no blocking zones.

var stick_vec := Vector2.ZERO
var action_down := false
var action_just := false

var _root: Control
var _base: Panel
var _knob: Panel
var _btn: Button          # legacy action button — kept for set_action_label() compat, never shown
var _touch_idx := -1      # the finger that owns the stick
var _jump_fingers := {}   # extra fingers currently HELD as jump (swim up while held)
var _pend := {}           # extra fingers not yet classified: idx -> {"pos", "ms"}
var _look_idx := -1       # the finger that owns the camera peek
var _look_dx := 0.0       # accumulated camera-drag pixels, consumed by the
var _look_dy := 0.0       # active camera owner (player.gd or galaxy.gd)
var _origin := Vector2.ZERO
var _moved := false
var _press_ms := 0
var _pulse := 0.0         # keeps action_down true briefly after a tap so per-frame readers never miss it
const R := 78.0   # smaller thumb travel for full deflection — livelier steering on tablets
const TAP_SLOP := 22.0    # finger drift allowed for a "tap" (px)
const TAP_MS := 300       # max press time for a tap
const JUMP_HOLD_MS := 140 # still second finger older than this = held jump

func _ready() -> void:
	layer = 9
	process_mode = Node.PROCESS_MODE_ALWAYS
	_root = Control.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_IGNORE   # visuals only — never blocks input
	add_child(_root)
	_base = _circle(Color(1, 1, 1, 0.12), 105.0)
	_knob = _circle(Color(1, 1, 1, 0.30), 46.0)
	_base.visible = false
	_knob.visible = false
	_root.add_child(_base)
	_root.add_child(_knob)
	_btn = Button.new()
	_btn.visible = false
	_root.add_child(_btn)
	# STORYBOOK FORK: a big visible action bubble, bottom-right. Tapping
	# anywhere with a second finger still works — this is the AFFORDANCE a
	# 4yo needs (see the button, know there's a thing to press), with the
	# current action name (JUMP / THROW / FIRE) written on it.
	if wants_touch():
		_act_vis = _circle(Color(1.0, 0.75, 0.88, 0.34), 74.0)
		_act_vis.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
		_act_vis.offset_left = -186.0
		_act_vis.offset_top = -206.0
		_act_vis.offset_right = -38.0
		_act_vis.offset_bottom = -58.0
		_root.add_child(_act_vis)
		_act_lbl = Label.new()
		_act_lbl.text = "JUMP"
		_act_lbl.add_theme_font_size_override("font_size", 34)
		_act_lbl.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
		_act_lbl.add_theme_color_override("font_outline_color", Color(0.2, 0.15, 0.35, 0.9))
		_act_lbl.add_theme_constant_override("outline_size", 8)
		_act_lbl.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_act_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_act_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		_act_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_act_vis.add_child(_act_lbl)

var _act_vis: Panel = null
var _act_lbl: Label = null
var _act_t := 0.0

func _process(delta: float) -> void:
	if _pulse > 0.0:
		_pulse -= delta
		if _pulse <= 0.0 and _jump_fingers.is_empty():
			action_down = false
	# a second finger that sat still past the decision window is a HELD jump —
	# it was only kept pending in case it turned into a camera drag
	if not _pend.is_empty():
		var now := Time.get_ticks_msec()
		for idx in _pend.keys():
			if now - int(_pend[idx]["ms"]) >= JUMP_HOLD_MS:
				_jump_fingers[idx] = true
				action_down = true
				action_just = true
				_flash(_pend[idx]["pos"])
				_pend.erase(idx)
	if _act_vis != null:
		_act_t += delta
		var pulse_s: float = 1.0 + sin(_act_t * 2.2) * 0.045
		_act_vis.pivot_offset = _act_vis.size * 0.5
		_act_vis.scale = Vector2(pulse_s, pulse_s) * (0.88 if action_down else 1.0)

func _circle(col: Color, rad: float) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(rad))
	p.add_theme_stylebox_override("panel", sb)
	p.size = Vector2(rad * 2.0, rad * 2.0)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return p

func _jump_pulse() -> void:
	action_down = true
	action_just = true
	_pulse = 0.18

func _flash(pos: Vector2) -> void:
	# quick fading ring where a jump finger lands — visible confirmation for little hands
	var f := _circle(Color(1.0, 0.95, 0.5, 0.5), 55.0)
	f.position = pos - f.size * 0.5
	_root.add_child(f)
	var tw := f.create_tween()
	tw.tween_property(f, "modulate:a", 0.0, 0.35)
	tw.tween_callback(f.queue_free)

func _press(pos: Vector2, idx: int) -> void:
	_touch_idx = idx
	_origin = pos
	_moved = false
	_press_ms = Time.get_ticks_msec()
	_base.position = _origin - _base.size * 0.5
	_knob.position = _origin - _knob.size * 0.5
	_base.visible = true
	_knob.visible = true
	stick_vec = Vector2.ZERO

func _drag(pos: Vector2) -> void:
	var off: Vector2 = pos - _origin
	if not _moved and off.length() > TAP_SLOP:
		_moved = true
	if off.length() > R:
		off = off.normalized() * R
	stick_vec = off / R if _moved else Vector2.ZERO
	_knob.position = _origin + off - _knob.size * 0.5

func _release_stick() -> void:
	# a short press with no real drag = TAP -> jump/action
	if not _moved and (Time.get_ticks_msec() - _press_ms) <= TAP_MS:
		_jump_pulse()
		_flash(_origin)   # same confirmation ring the second-finger tap gets
	_touch_idx = -1
	stick_vec = Vector2.ZERO
	_base.visible = false
	_knob.visible = false

func _clear_touch_state() -> void:
	_touch_idx = -1
	_look_idx = -1
	_jump_fingers.clear()
	_pend.clear()
	stick_vec = Vector2.ZERO
	action_down = false
	action_just = false
	_look_dx = 0.0
	_look_dy = 0.0
	_moved = false
	_pulse = 0.0
	if _base != null:
		_base.visible = false
	if _knob != null:
		_knob.visible = false

func _request_pause() -> void:
	var m: Node = get_parent()
	if m != null and m.has_method("toggle_pause"):
		m.toggle_pause()

func _flush_parent_save() -> void:
	var m: Node = get_parent()
	if m != null and m.has_method("_write_save"):
		m.call("_write_save")

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
	if not wants_touch():
		return
	if ev is InputEventScreenTouch:
		var t := ev as InputEventScreenTouch
		if t.pressed:
			if _touch_idx == -1:
				_press(t.position, t.index)          # first finger: stick (or tap-to-jump)
			elif t.index != _touch_idx:
				# extra finger: jump OR camera drag — pending until it moves
				# past TAP_SLOP (camera) or JUMP_HOLD_MS elapses (held jump)
				_pend[t.index] = {"pos": t.position, "ms": Time.get_ticks_msec()}
		else:
			if t.index == _touch_idx:
				_release_stick()
			elif _pend.has(t.index):
				# quick second-finger tap, decided on release: jump/action
				_pend.erase(t.index)
				_jump_pulse()
				_flash(t.position)
			elif t.index == _look_idx:
				_look_idx = -1
			elif _jump_fingers.has(t.index):
				_jump_fingers.erase(t.index)
				if _jump_fingers.is_empty() and _pulse <= 0.0:
					action_down = false
	elif ev is InputEventScreenDrag:
		var d := ev as InputEventScreenDrag
		if d.index == _touch_idx:
			_drag(d.position)
		elif _pend.has(d.index):
			if (d.position - (_pend[d.index]["pos"] as Vector2)).length() > TAP_SLOP:
				_pend.erase(d.index)
				if _look_idx == -1:
					_look_idx = d.index   # a real drag: this finger drives the camera
				else:
					# a camera finger is already down — treat a third drag as held jump
					_jump_fingers[d.index] = true
					action_down = true
					action_just = true
		elif d.index == _look_idx:
			_look_dx += d.relative.x
			_look_dy += d.relative.y
	elif ev is InputEventMouseButton:
		var mb := ev as InputEventMouseButton
		if mb.device == InputEvent.DEVICE_ID_EMULATION:
			return   # synthesized from touch — the touch path above already handled it
		if mb.button_index == MOUSE_BUTTON_LEFT:
			if mb.pressed and _touch_idx == -1:
				_press(mb.position, 99)
			elif not mb.pressed and _touch_idx == 99:
				_release_stick()
	elif ev is InputEventMouseMotion and _touch_idx == 99:
		var mm := ev as InputEventMouseMotion
		if mm.device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag(mm.position)

func set_action_label(t: String) -> void:
	if _btn != null and _btn.text != t:
		_btn.text = t
	if _act_lbl != null and _act_lbl.text != t:
		_act_lbl.text = t

func consume_action_just() -> bool:
	var j := action_just
	action_just = false
	return j

func look_active() -> bool:
	return _look_idx != -1

func consume_look() -> Vector2:
	# capped so deltas that piled up while no camera was consuming (minigame
	# handoffs, overlays) nudge the camera instead of snapping it
	var v := Vector2(clampf(_look_dx, -120.0, 120.0), clampf(_look_dy, -120.0, 120.0))
	_look_dx = 0.0
	_look_dy = 0.0
	return v

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
