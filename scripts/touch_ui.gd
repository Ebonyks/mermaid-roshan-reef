extends CanvasLayer
# Touch controls (Android/tablet): drag ANYWHERE to summon a virtual stick at your
# finger; a quick TAP (no drag) anywhere = jump/action. No fixed buttons.
# Auto-shown on touch devices; desktop can force with --touch.

var stick_vec := Vector2.ZERO
var action_down := false
var action_just := false

var _root: Control
var _zone: Control
var _base: Panel
var _knob: Panel
var _btn: Button          # legacy action button — kept for API compat, never shown
var _touch_idx := -1
var _origin := Vector2.ZERO
var _moved := false
var _press_ms := 0
var _pulse := 0.0         # keeps action_down true briefly after a tap so a frame is never missed
const R := 95.0
const TAP_SLOP := 22.0    # finger drift allowed for a "tap" (px)
const TAP_MS := 300       # max press time for a tap

func _ready() -> void:
	layer = 9
	process_mode = Node.PROCESS_MODE_ALWAYS
	_root = Control.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_root)
	# the whole screen is the control surface: drag = stick, tap = jump
	_zone = Control.new()
	_zone.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_zone.mouse_filter = Control.MOUSE_FILTER_STOP
	_zone.gui_input.connect(_zone_input)
	_root.add_child(_zone)
	_base = _circle(Color(1, 1, 1, 0.12), 105.0)
	_knob = _circle(Color(1, 1, 1, 0.30), 46.0)
	_base.visible = false
	_knob.visible = false
	_root.add_child(_base)
	_root.add_child(_knob)
	# legacy action button: some code calls set_action_label(); keep the node, never show it
	_btn = Button.new()
	_btn.visible = false
	_root.add_child(_btn)
	if not wants_touch():
		_zone.visible = false

func _process(delta: float) -> void:
	if _pulse > 0.0:
		_pulse -= delta
		if _pulse <= 0.0:
			action_down = false

func _circle(col: Color, rad: float) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(rad))
	p.add_theme_stylebox_override("panel", sb)
	p.size = Vector2(rad * 2.0, rad * 2.0)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return p

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

func _zone_input(ev: InputEvent) -> void:
	if ev is InputEventScreenTouch:
		var t := ev as InputEventScreenTouch
		if t.pressed and _touch_idx == -1:
			_press(t.position, t.index)
		elif not t.pressed and t.index == _touch_idx:
			_release()
	elif ev is InputEventScreenDrag:
		var d := ev as InputEventScreenDrag
		if d.index == _touch_idx:
			_drag(d.position)
	elif ev is InputEventMouseButton:
		var mb := ev as InputEventMouseButton
		if mb.button_index == MOUSE_BUTTON_LEFT:
			if mb.pressed and _touch_idx == -1:
				_press(mb.position, 99)
			elif not mb.pressed and _touch_idx == 99:
				_release()
	elif ev is InputEventMouseMotion and _touch_idx == 99:
		_drag((ev as InputEventMouseMotion).position)

func _release() -> void:
	# a short press with no real drag = TAP -> jump/action
	if not _moved and (Time.get_ticks_msec() - _press_ms) <= TAP_MS:
		action_down = true
		action_just = true
		_pulse = 0.18
	_touch_idx = -1
	stick_vec = Vector2.ZERO
	_base.visible = false
	_knob.visible = false

func set_action_label(t: String) -> void:
	if _btn != null and _btn.text != t:
		_btn.text = t

func consume_action_just() -> bool:
	var j := action_just
	action_just = false
	return j

func _input(ev: InputEvent) -> void:
	var toggle := false
	if ev is InputEventKey and (ev as InputEventKey).pressed and not (ev as InputEventKey).echo:
		if (ev as InputEventKey).physical_keycode == KEY_ESCAPE:
			toggle = true
	elif ev is InputEventJoypadButton and (ev as InputEventJoypadButton).pressed:
		if (ev as InputEventJoypadButton).button_index == JOY_BUTTON_START:
			toggle = true
	if toggle:
		var m: Node = get_parent()
		if m != null and m.has_method("toggle_pause"):
			m.toggle_pause()

static func wants_touch() -> bool:
	return DisplayServer.is_touchscreen_available() or OS.has_feature("mobile") or "--touch" in OS.get_cmdline_user_args()
