extends CanvasLayer
# Touch controls (Android/tablet):
#   HYBRID (default): point-to-interact + a contextual lower-right action button;
#   taps on unclaimed world space are emitted for select/approach/move.
#   CLASSIC (rollback): the shipped drag-anywhere stick, tap action and
#   second-finger camera path is retained below.
# World taps remain in _unhandled_input so overlays receive first claim.
# Persistent movement/action/pause controls are claimed in _input: these are
# visible promises and must not become inert when another Control overlaps.
# A touch has one owner for its lifetime; ownership never changes mid-gesture.

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

# ---- drag channel (owner 2026-07-25) ----
# Some acts are played by DRAGGING a finger across the screen rather than by
# swimming and tapping — painting, scrubbing, tracing, lens-dragging. While
# drag_mode is on, the first finger reports its absolute screen position here
# instead of raising the virtual stick, so the act reads a stroke, not a
# direction. Everything else (second-finger jump, pause) is untouched.
var drag_mode := false
var drag_active := false
var drag_pos := Vector2.ZERO
var drag_started := false          # set for one read on touch-down

var _root: Control
var _base: Panel
var _knob: Panel
var _stick_hint: Panel    # fixed ghost wheel teaching the bottom-left thumb bay
var _btn: Button          # legacy action button — kept for set_action_label() compat, never shown
var _act_button: Button = null
var _touch_idx := -1      # the finger that owns the stick
var _jump_fingers := {}   # extra fingers currently HELD as jump (swim up while held)
var _action_fingers := {}
var _pend := {}           # extra fingers not yet classified: idx -> {"pos", "ms"}
var _world_pend := {}
var _look_idx := -1       # the finger that owns the camera peek
var _look_dx := 0.0       # accumulated camera-drag pixels, consumed by the
var _look_dy := 0.0       # active camera owner (player.gd or galaxy.gd)
var _origin := Vector2.ZERO
var _press_pos := Vector2.ZERO
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
	"BONK!": "✋",
	"WAIT": "◇",
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
	# A fixed ghost wheel teaches the bottom-left ownership before the first
	# drag; the real drag-anywhere stick still appears under the finger.
	_stick_hint = _circle(Color(0.28, 0.42, 0.62, 0.48), 90.0, StorybookUI.MINT, 7)
	_stick_hint.name = "TouchShellPad"
	_stick_hint.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	_stick_hint.offset_left = 26.0
	_stick_hint.offset_top = -206.0
	_stick_hint.offset_right = 206.0
	_stick_hint.offset_bottom = -26.0
	_stick_hint.visible = false
	_root.add_child(_stick_hint)
	var hint_arrows := Label.new()
	hint_arrows.name = "TouchDirectionHints"
	hint_arrows.text = "▲\n◀   ▶\n▼"
	hint_arrows.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hint_arrows.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint_arrows.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	hint_arrows.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(hint_arrows, 27, StorybookUI.PEARL_BLUE, 6)
	_stick_hint.add_child(hint_arrows)
	StorybookUI.add_shell_crest(_stick_hint, Rect2(55, 128, 70, 50), "TouchPadShellCrest")
	_base = _circle(Color(0.28, 0.42, 0.62, 0.58), 105.0, StorybookUI.MINT, 7)
	_knob = _circle(Color(0.64, 1.0, 0.84, 0.86), 46.0, StorybookUI.INK, 4)
	_base.visible = false
	_knob.visible = false
	_root.add_child(_base)
	_root.add_child(_knob)
	call_deferred("_rest_stick")
	_btn = Button.new()
	_btn.visible = false
	_root.add_child(_btn)
	# A 176 px real hit target surrounds the 148 px visible action bubble.
	# Classic mode hides this Control and keeps the original all-screen tap.
	# The rect is only an anchor/affordance: presses are claimed from raw
	# ScreenTouch in _hybrid_unhandled_input, because a Control Button only
	# hears the FIRST finger (mouse-from-touch emulation) — a second finger
	# pressed while the stick is held would otherwise be silently dropped.
	if wants_touch():
		_act_button = Button.new()
		_act_button.flat = true
		_act_button.focus_mode = Control.FOCUS_NONE
		_act_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_act_button.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
		_act_button.offset_left = -204.0
		_act_button.offset_top = -224.0
		_act_button.offset_right = -28.0
		_act_button.offset_bottom = -48.0
		var empty := StyleBoxEmpty.new()
		for style_name: String in ["normal", "hover", "pressed", "focus"]:
			_act_button.add_theme_stylebox_override(style_name, empty)
		_root.add_child(_act_button)
		# Storybook coral bubble: 148 px visible, centred in the 176 px envelope.
		_act_vis = _circle(Color(1.0, 0.50, 0.48, 0.86), 74.0, StorybookUI.INK, 5)
		_act_vis.name = "ActionShellMedallion"
		_act_vis.position = Vector2(14.0, 14.0)
		_act_button.add_child(_act_vis)
		_act_lbl = Label.new()
		_act_lbl.text = _action_display("JUMP")
		_act_lbl.add_theme_font_size_override("font_size", 27)
		_act_lbl.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
		_act_lbl.add_theme_color_override("font_outline_color", Color(0.2, 0.15, 0.35, 0.9))
		_act_lbl.add_theme_constant_override("outline_size", 8)
		_act_lbl.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		_act_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_act_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		_act_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_act_vis.add_child(_act_lbl)
		StorybookUI.add_shell_crest(_act_vis, Rect2(46, 104, 56, 40), "ActionShellCrest")
	set_mode(control_mode)

func _process(delta: float) -> void:
	if _pulse > 0.0:
		_pulse -= delta
		if _pulse <= 0.0 and _jump_fingers.is_empty() and _action_fingers.is_empty():
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

func _circle(col: Color, rad: float, outline: Color = Color.TRANSPARENT, border_width: int = 0) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(rad))
	if border_width > 0:
		sb.border_color = outline
		sb.set_border_width_all(border_width)
	p.add_theme_stylebox_override("panel", sb)
	p.size = Vector2(rad * 2.0, rad * 2.0)
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return p

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
	# THE STICK ORIGIN IS ALWAYS THE FINGER (owner report 2026-08-03: "touching
	# the left side of the screen sometimes moves right, in Sky Lagoon").
	# Hybrid used to anchor the origin to a fixed bottom-left ring instead. That
	# ring is never drawn (see _rest_stick), yet movement_zone() claims the whole
	# lower-left third of the phone — so on a 1600x720 handset roughly three
	# quarters of the thumb bay lay to the RIGHT of the invisible anchor and
	# shoved Roshan right the instant it was touched, with nothing on screen to
	# explain why. A finger-anchored origin makes the drag direction and the
	# travel direction the same thing everywhere in the bay. Classic already
	# worked this way; the two paths now agree.
	_origin = pos
	_press_pos = pos
	if drag_mode:
		# the finger paints instead of steering — no stick, no tap-to-jump
		drag_active = true
		drag_started = true
		drag_pos = pos
		stick_vec = Vector2.ZERO
		return
	_moved = false
	_manual_emitted = false
	_press_ms = Time.get_ticks_msec()
	if _stick_hint != null:
		_stick_hint.visible = false
	_base.position = _origin - _base.size * 0.5
	_knob.position = _origin - _knob.size * 0.5
	_base.modulate.a = 1.0
	_knob.modulate.a = 1.0
	_base.visible = false
	_knob.visible = false
	stick_vec = Vector2.ZERO

func _drag(pos: Vector2) -> void:
	if drag_mode:
		drag_active = true
		drag_pos = pos
		stick_vec = Vector2.ZERO
		return
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
	if drag_mode:
		drag_active = false
		_touch_idx = -1
		stick_vec = Vector2.ZERO
		return
	# a short press with no real drag = TAP -> jump/action
	if control_mode == "classic" and not _moved and (Time.get_ticks_msec() - _press_ms) <= TAP_MS:
		_jump_pulse()
		_flash(_origin)
	elif control_mode == "hybrid" and not _moved:
		# The thumb bay is an accessibility stick, not a hole in the world. A
		# press that never became a drag is still a tap on whatever is painted
		# underneath, so tap-to-travel and tap-to-select keep working in the
		# lower-left corner exactly as they do everywhere else. No TAP_MS gate:
		# a four-year-old's deliberate press is slow, and the world-tap owner
		# elsewhere in this router has no time limit either.
		world_touched.emit(_press_pos)
		_flash(_press_pos)
	if _manual_emitted:
		manual_move_ended.emit()
	_touch_idx = -1
	_manual_emitted = false
	stick_vec = Vector2.ZERO
	_rest_stick()

func _rest_stick() -> void:
	# Point-to-interact keeps the screen clear. Gesture steering remains available
	# to legacy movement activities without drawing a virtual stick.
	if _base != null:
		_base.visible = false
	if _knob != null:
		_knob.visible = false
	if _stick_hint != null:
		_stick_hint.visible = false

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

func pause_zone() -> Rect2:
	var main: Node = get_parent()
	if main != null:
		var pause_button := main.find_child("PauseCornerButton", true, false) as Control
		if pause_button != null and pause_button.visible:
			return pause_button.get_global_rect()
	var vs: Vector2 = _root.size
	if vs == Vector2.ZERO:
		vs = get_viewport().get_visible_rect().size
	return Rect2(Vector2(vs.x - 170.0, 0.0), Vector2(170.0, 170.0))

func reserved_zone_hit(pos: Vector2) -> bool:
	# True when this router already owns a press at this screen point. Stages
	# that read the EMULATED MOUSE directly for hold-to-travel must ask first:
	# that pointer knows nothing about touch ownership, so without this guard a
	# hold on the action medallion (bottom-right) or in the thumb bay commanded
	# travel toward that corner of the screen — Roshan strolled off to the right
	# while the child was simply holding PLAY down.
	if not wants_touch() or not world_controls_enabled:
		return false
	if pause_zone().has_point(pos):
		return true
	if control_mode != "hybrid":
		return false
	return action_zone().has_point(pos) or movement_zone().has_point(pos)

func _clear_touch_state() -> void:
	drag_active = false
	drag_started = false
	_touch_idx = -1
	_look_idx = -1
	_jump_fingers.clear()
	_action_fingers.clear()
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
	_press_pos = Vector2.ZERO
	_pulse = 0.0
	_rest_stick()

func set_mode(next_mode: String) -> void:
	control_mode = "classic" if next_mode == "classic" else "hybrid"
	_clear_touch_state()
	if _act_button != null:
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
	_rest_stick()

func _request_pause() -> void:
	var m: Node = get_parent()
	# Start advances the always-processing story intro via ReefMain. Do not
	# also raise the pause sheet over that same press.
	if m != null and bool(m.get("intro_active")):
		return
	if m != null and m.has_method("toggle_pause"):
		_clear_touch_state()
		m.toggle_pause()

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

func _action_hit(pos: Vector2) -> bool:
	return _act_button != null and _act_button.visible and action_zone().has_point(pos)

func _claim_action(finger_index: int) -> void:
	touch_owners[finger_index] = TouchOwner.ACTION
	_action_fingers[finger_index] = true
	_on_action_button_down()

func _release_action(finger_index: int) -> void:
	_action_fingers.erase(finger_index)
	if _action_fingers.is_empty():
		_on_action_button_up()

func _hybrid_unhandled_input(ev: InputEvent) -> void:
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		if touch.pressed:
			if _action_hit(touch.position):
				_claim_action(touch.index)
			elif _touch_idx == -1 and movement_zone().has_point(touch.position):
				touch_owners[touch.index] = TouchOwner.STICK
				_press(touch.position, touch.index)
			else:
				touch_owners[touch.index] = TouchOwner.WORLD_INTERACT
				_world_pend[touch.index] = {"pos": touch.position, "moved": false}
		else:
			var owner: int = int(touch_owners.get(touch.index, TouchOwner.NONE))
			if owner == TouchOwner.STICK and touch.index == _touch_idx:
				_release_stick()
			elif owner == TouchOwner.ACTION:
				_release_action(touch.index)
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
			if _action_hit(mouse_button.position):
				_claim_action(99)
			elif _touch_idx == -1 and movement_zone().has_point(mouse_button.position):
				touch_owners[99] = TouchOwner.STICK
				_press(mouse_button.position, 99)
			else:
				touch_owners[99] = TouchOwner.WORLD_INTERACT
				_world_pend[99] = {"pos": mouse_button.position, "moved": false}
		else:
			var owner: int = int(touch_owners.get(99, TouchOwner.NONE))
			if owner == TouchOwner.STICK and _touch_idx == 99:
				_release_stick()
			elif owner == TouchOwner.ACTION:
				_release_action(99)
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

func set_drag_mode(on: bool) -> void:
	drag_mode = on
	drag_active = false
	drag_started = false
	stick_vec = Vector2.ZERO
	if on:
		_touch_idx = -1
		_rest_stick()

func consume_drag_started() -> bool:
	var j := drag_started
	drag_started = false
	return j

func look_active() -> bool:
	return control_mode == "classic" and _look_idx != -1

func consume_look() -> Vector2:
	var look := Vector2(clampf(_look_dx, -120.0, 120.0), clampf(_look_dy, -120.0, 120.0))
	_look_dx = 0.0
	_look_dy = 0.0
	return look

func _input(ev: InputEvent) -> void:
	# These fixed controls must win before ordinary GUI routing. Overlay
	# builders disable world_controls_enabled, so their own buttons still keep
	# the whole screen while open.
	if wants_touch() and ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		if touch.pressed and pause_zone().has_point(touch.position):
			_request_pause()
			get_viewport().set_input_as_handled()
			return
		if control_mode == "hybrid" and world_controls_enabled:
			if touch.pressed:
				if _action_hit(touch.position):
					_claim_action(touch.index)
					get_viewport().set_input_as_handled()
					return

			else:
				var owner: int = int(touch_owners.get(touch.index, TouchOwner.NONE))
				if owner == TouchOwner.STICK and touch.index == _touch_idx:
					_release_stick()
					touch_owners.erase(touch.index)
					get_viewport().set_input_as_handled()
					return
				if owner == TouchOwner.ACTION:
					_release_action(touch.index)
					touch_owners.erase(touch.index)
					get_viewport().set_input_as_handled()
					return
	elif wants_touch() and ev is InputEventScreenDrag and control_mode == "hybrid" \
			and world_controls_enabled:
		var drag := ev as InputEventScreenDrag
		if touch_owners.get(drag.index, TouchOwner.NONE) == TouchOwner.STICK \
				and drag.index == _touch_idx:
			_drag(drag.position)
			get_viewport().set_input_as_handled()
			return
	elif wants_touch() and ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device != InputEvent.DEVICE_ID_EMULATION \
				and mouse_button.button_index == MOUSE_BUTTON_LEFT:
			if mouse_button.pressed and pause_zone().has_point(mouse_button.position):
				_request_pause()
				get_viewport().set_input_as_handled()
				return
			if control_mode == "hybrid" and world_controls_enabled:
				if mouse_button.pressed and _action_hit(mouse_button.position):
					_claim_action(99)
					get_viewport().set_input_as_handled()
					return
				if not mouse_button.pressed and touch_owners.get(99, TouchOwner.NONE) == TouchOwner.STICK:
					_release_stick()
					touch_owners.erase(99)
					get_viewport().set_input_as_handled()
					return
				if not mouse_button.pressed and touch_owners.get(99, TouchOwner.NONE) == TouchOwner.ACTION:
					_release_action(99)
					touch_owners.erase(99)
					get_viewport().set_input_as_handled()
					return
	elif wants_touch() and ev is InputEventMouseMotion and control_mode == "hybrid" \
			and world_controls_enabled and touch_owners.get(99, TouchOwner.NONE) == TouchOwner.STICK:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device != InputEvent.DEVICE_ID_EMULATION:
			_drag(mouse_motion.position)
			get_viewport().set_input_as_handled()
			return
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
	# Touch-first game: editor/debug desktop runs take the touch path too, so the
	# mouse drives the same stick/tap code the phone uses. `--no-touch` restores
	# the bare desktop scheme for probes that need it.
	if "--no-touch" in OS.get_cmdline_user_args():
		return false
	return DisplayServer.is_touchscreen_available() or OS.has_feature("mobile") \
		or OS.has_feature("pc") or OS.has_feature("editor") or OS.is_debug_build() \
		or "--touch" in OS.get_cmdline_user_args()
