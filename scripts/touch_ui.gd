extends CanvasLayer
# Touch controls: virtual stick (left half) + big context action button (right).
# Auto-shown on touch devices; desktop can force with --touch or the pause menu.

var stick_vec := Vector2.ZERO
var action_down := false
var action_just := false

var _root: Control
var _zone: Control
var _base: Panel
var _knob: Panel
var _btn: Button
var _touch_idx := -1
var _origin := Vector2.ZERO
const R := 95.0

func _ready() -> void:
	layer = 9
	process_mode = Node.PROCESS_MODE_ALWAYS
	_root = Control.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_root)
	# stick zone = left 45% of screen
	_zone = Control.new()
	_zone.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_zone.anchor_right = 0.45
	_zone.mouse_filter = Control.MOUSE_FILTER_STOP
	_zone.gui_input.connect(_zone_input)
	_root.add_child(_zone)
	_base = _circle(Color(1, 1, 1, 0.12), 105.0)
	_knob = _circle(Color(1, 1, 1, 0.30), 46.0)
	_base.visible = false
	_knob.visible = false
	_root.add_child(_base)
	_root.add_child(_knob)
	# action button bottom-right
	_btn = Button.new()
	_btn.text = "JUMP"
	_btn.add_theme_font_size_override("font_size", 30)
	_btn.custom_minimum_size = Vector2(150, 150)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(1.0, 0.78, 0.30, 0.82)
	sb.set_corner_radius_all(75)
	_btn.add_theme_stylebox_override("normal", sb)
	var sb2: StyleBoxFlat = sb.duplicate()
	sb2.bg_color = Color(1.0, 0.9, 0.55, 0.95)
	_btn.add_theme_stylebox_override("pressed", sb2)
	_btn.add_theme_stylebox_override("hover", sb)
	_btn.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	_btn.position = Vector2(-190, -200)
	_btn.button_down.connect(func():
		action_down = true
		action_just = true)
	_btn.button_up.connect(func(): action_down = false)
	_root.add_child(_btn)
	if not wants_touch():
		_zone.visible = false
		_btn.visible = false

func _circle(col: Color, rad: float) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(rad))
	p.add_theme_stylebox_override("panel", sb)
	p.size = Vector2(rad * 2.0, rad * 2.0)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return p

func _zone_input(ev: InputEvent) -> void:
	if ev is InputEventScreenTouch:
		var t := ev as InputEventScreenTouch
		if t.pressed and _touch_idx == -1:
			_touch_idx = t.index
			_origin = t.position
			_base.position = _origin - _base.size * 0.5
			_knob.position = _origin - _knob.size * 0.5
			_base.visible = true
			_knob.visible = true
			stick_vec = Vector2.ZERO
		elif not t.pressed and t.index == _touch_idx:
			_release()
	elif ev is InputEventScreenDrag:
		var d := ev as InputEventScreenDrag
		if d.index == _touch_idx:
			var off: Vector2 = d.position - _origin
			if off.length() > R:
				off = off.normalized() * R
			stick_vec = off / R
			_knob.position = _origin + off - _knob.size * 0.5
	elif ev is InputEventMouseButton:
		var mb := ev as InputEventMouseButton
		if mb.button_index == MOUSE_BUTTON_LEFT:
			if mb.pressed and _touch_idx == -1:
				_touch_idx = 99
				_origin = mb.position
				_base.position = _origin - _base.size * 0.5
				_knob.position = _origin - _knob.size * 0.5
				_base.visible = true
				_knob.visible = true
				stick_vec = Vector2.ZERO
			elif not mb.pressed and _touch_idx == 99:
				_release()
	elif ev is InputEventMouseMotion and _touch_idx == 99:
		var mm := ev as InputEventMouseMotion
		var off2: Vector2 = mm.position - _origin
		if off2.length() > R:
			off2 = off2.normalized() * R
		stick_vec = off2 / R
		_knob.position = _origin + off2 - _knob.size * 0.5

func _release() -> void:
	_touch_idx = -1
	stick_vec = Vector2.ZERO
	_base.visible = false
	_knob.visible = false

func set_action_label(t: String) -> void:
	if _btn.text != t:
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
