class_name AttackCustomizer
extends Control
## A tiny, touch-first atelier for Roshan's attack profile.
##
## The art is intentionally picture-first: the paint dots, cleaning brush and
## bubbles/splash marks communicate the choices before a child can read. The
## owner (ReefMain) remains the state authority; this controller only mirrors
## and writes the two profile fields through Object.set so it can be introduced
## without breaking older save files during the migration.

signal profile_changed(color: Color, effect: String)
signal closed

const DEFAULT_COLOR := Color(0.2705882353, 0.8588235294, 0.9215686275, 1.0)
const DEFAULT_EFFECT := "bubbles"
const COLORS := [
	DEFAULT_COLOR,
	Color(0.52, 0.95, 0.72, 1.0),
	Color(1.0, 0.78, 0.30, 1.0),
	Color(1.0, 0.48, 0.55, 1.0),
	Color(0.74, 0.58, 1.0, 1.0),
]
const EFFECTS := ["bubbles", "splashes"]

var m: ReefMain = null
var attack_color: Color = DEFAULT_COLOR
var attack_effect: String = DEFAULT_EFFECT
var is_open := false
var _on_confirm: Callable = Callable()

var _dim: ColorRect = null
var _card: Panel = null
var _color_row: HBoxContainer = null
var _effect_row: HBoxContainer = null
var _brush: BrushBadge = null
var _color_buttons: Array[AttackChoice] = []
var _effect_buttons: Array[AttackChoice] = []

class BrushBadge extends Control:
	var attack_color: Color = DEFAULT_COLOR

	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		queue_redraw()

	func _draw() -> void:
		# A simple broad brush silhouette reads at phone size without a texture.
		draw_circle(Vector2(58.0, 68.0), 24.0, Color(0.35, 0.22, 0.66, 0.25))
		draw_line(Vector2(54.0, 62.0), Vector2(112.0, 20.0), Color(0.42, 0.25, 0.68), 17.0, true)
		draw_line(Vector2(52.0, 63.0), Vector2(112.0, 20.0), Color(0.95, 0.79, 0.38), 9.0, true)
		var bristles := PackedVector2Array([
			Vector2(22.0, 76.0), Vector2(66.0, 67.0), Vector2(58.0, 103.0),
			Vector2(15.0, 95.0),
		])
		draw_colored_polygon(bristles, attack_color)
		draw_polyline(bristles, Color(0.22, 0.14, 0.52), 4.0, true)
		draw_circle(Vector2(17.0, 88.0), 6.0, attack_color if is_instance_valid(self) else DEFAULT_COLOR)

class AttackChoice extends Button:
	var choice_color := DEFAULT_COLOR
	var choice_effect := ""
	var selected := false

	func configure(color: Color, effect: String) -> void:
		choice_color = color
		choice_effect = effect
		text = ""
		tooltip_text = ""
		mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		queue_redraw()

	func set_choice_selected(value: bool) -> void:
		selected = value
		queue_redraw()

	func _draw() -> void:
		var center := size * 0.5
		if choice_effect.is_empty():
			draw_circle(center, minf(size.x, size.y) * 0.26, choice_color)
			draw_circle(center, minf(size.x, size.y) * 0.26, Color(0.22, 0.14, 0.52, 0.92), false, 5.0)
		else:
			if choice_effect == "bubbles":
				draw_circle(center + Vector2(-15.0, 8.0), 16.0, choice_color, false, 7.0)
				draw_circle(center + Vector2(15.0, -10.0), 11.0, choice_color, false, 6.0)
				draw_circle(center + Vector2(7.0, 17.0), 7.0, choice_color, false, 5.0)
			else:
				for i in range(8):
					var angle := TAU * float(i) / 8.0
					var end := center + Vector2(cos(angle), sin(angle)) * 29.0
					draw_line(center, end, choice_color, 7.0, true)
				draw_circle(center, 10.0, choice_color)
		if selected:
			draw_arc(center, minf(size.x, size.y) * 0.42, 0.0, TAU, 32, StorybookUI.GOLD, 8.0, true)

func _ready() -> void:
	visible = false
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func attach(owner: ReefMain) -> void:
	m = owner
	_sync_from_main()
	_build()

func configure(owner: ReefMain) -> void:
	attach(owner)

func open(on_confirm: Callable = Callable()) -> void:
	if _card == null:
		_build()
	_sync_from_main()
	_refresh_choices()
	_on_confirm = on_confirm
	visible = true
	is_open = true
	if _card != null:
		_card.scale = Vector2(0.92, 0.92)
		var tw: Tween = _card.create_tween()
		tw.tween_property(_card, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func close() -> void:
	if not is_open:
		return
	is_open = false
	visible = false
	if _on_confirm.is_valid():
		var callback: Callable = _on_confirm
		_on_confirm = Callable()
		callback.call()
	closed.emit()

func toggle() -> void:
	close() if is_open else open()

func set_profile(color: Color, effect: String) -> void:
	attack_color = color
	attack_effect = effect if effect in EFFECTS else DEFAULT_EFFECT
	_write_to_main()
	_refresh_choices()
	profile_changed.emit(attack_color, attack_effect)

func apply_profile(color: Color, effect: String) -> void:
	set_profile(color, effect)

func set_color(color: Color) -> void:
	set_profile(color, attack_effect)

func set_effect(effect: String) -> void:
	set_profile(attack_color, effect)

func current_profile() -> Dictionary:
	return {"attack_color": attack_color, "attack_effect": attack_effect}


func audit_snapshot() -> Dictionary:
	return {
		"color_choices": _color_buttons.size(),
		"effect_choices": _effect_buttons.size(),
		"confirm_button": get_node_or_null("AttackCustomizerCard/AttackCustomizerConfirm") != null,
		"canvas_only": true,
	}

func _build() -> void:
	if _card != null and is_instance_valid(_card):
		return
	if get_parent() == null:
		return
	_dim = ColorRect.new()
	_dim.name = "AttackCustomizerDim"
	_dim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_dim.color = Color(0.025, 0.06, 0.16, 0.72)
	_dim.mouse_filter = Control.MOUSE_FILTER_STOP
	_dim.gui_input.connect(_on_dim_input)
	add_child(_dim)
	_card = StorybookUI.add_panel(self, Rect2(260.0, 82.0, 760.0, 556.0), StorybookUI.PURPLE, StorybookUI.PAPER, 42)
	_card.name = "AttackCustomizerCard"
	_card.mouse_filter = Control.MOUSE_FILTER_STOP
	_card.pivot_offset = _card.size * 0.5
	_brush = BrushBadge.new()
	_brush.name = "CleaningBrush"
	_brush.position = Vector2(32.0, 30.0)
	_brush.size = Vector2(130.0, 124.0)
	_card.add_child(_brush)
	var confirm := Button.new()
	confirm.name = "AttackCustomizerConfirm"
	confirm.text = "✦"
	confirm.tooltip_text = "Use this magic attack"
	confirm.position = Vector2(610.0, 28.0)
	confirm.custom_minimum_size = Vector2(116.0, 116.0)
	confirm.size = Vector2(116.0, 116.0)
	confirm.focus_mode = Control.FOCUS_NONE
	StorybookUI.style_picture_button(confirm, StorybookUI.GOLD,
		StorybookUI.PURPLE, 34)
	confirm.pressed.connect(close)
	_card.add_child(confirm)
	var color_panel := StorybookUI.add_hud_panel(_card, Rect2(34.0, 176.0, 692.0, 142.0), StorybookUI.PEARL_BLUE, StorybookUI.PAPER_COOL, 28)
	color_panel.name = "AttackColorChoices"
	_color_row = HBoxContainer.new()
	_color_row.position = Vector2(45.0, 16.0)
	_color_row.size = Vector2(602.0, 110.0)
	_color_row.add_theme_constant_override("separation", 18)
	color_panel.add_child(_color_row)
	for color: Color in COLORS:
		var choice := AttackChoice.new()
		choice.custom_minimum_size = Vector2(104.0, 104.0)
		choice.size = Vector2(104.0, 104.0)
		choice.configure(color, "")
		StorybookUI.style_picture_button(choice, StorybookUI.PAPER, StorybookUI.PURPLE, 30)
		choice.pressed.connect(_on_color_pressed.bind(color))
		_color_row.add_child(choice)
		_color_buttons.append(choice)
	var effect_panel := StorybookUI.add_hud_panel(_card, Rect2(34.0, 344.0, 692.0, 142.0), StorybookUI.LILAC, StorybookUI.PAPER, 28)
	effect_panel.name = "AttackEffectChoices"
	_effect_row = HBoxContainer.new()
	_effect_row.position = Vector2(142.0, 16.0)
	_effect_row.size = Vector2(408.0, 110.0)
	_effect_row.add_theme_constant_override("separation", 56)
	effect_panel.add_child(_effect_row)
	for effect: String in EFFECTS:
		var choice := AttackChoice.new()
		choice.custom_minimum_size = Vector2(150.0, 110.0)
		choice.size = Vector2(150.0, 110.0)
		choice.configure(attack_color, effect)
		StorybookUI.style_picture_button(choice, StorybookUI.PAPER, StorybookUI.PURPLE, 30)
		choice.pressed.connect(_on_effect_pressed.bind(effect))
		_effect_row.add_child(choice)
		_effect_buttons.append(choice)
	_refresh_choices()

func _sync_from_main() -> void:
	if m == null:
		return
	var stored_color: Variant = m.get("attack_color")
	if stored_color is Color:
		attack_color = stored_color as Color
	var stored_effect: Variant = m.get("attack_effect")
	if stored_effect is String and String(stored_effect) in EFFECTS:
		attack_effect = String(stored_effect)
	_write_to_main()

func _write_to_main() -> void:
	if m == null:
		return
	if m.has_method("set_attack_profile"):
		m.call("set_attack_profile", attack_color, attack_effect)
	else:
		m.set("attack_color", attack_color)
		m.set("attack_effect", attack_effect)

func _on_color_pressed(color: Color) -> void:
	set_color(color)

func _on_effect_pressed(effect: String) -> void:
	set_effect(effect)

func _on_dim_input(event: InputEvent) -> void:
	# The dimmer consumes stray taps so the required picture choice cannot be
	# skipped accidentally. The large glowing star on the brush card confirms.
	if event is InputEventScreenTouch or event is InputEventMouseButton:
		accept_event()

func _refresh_choices() -> void:
	for button: AttackChoice in _color_buttons:
		button.set_choice_selected(button.choice_color.is_equal_approx(attack_color))
	for button: AttackChoice in _effect_buttons:
		button.choice_color = attack_color
		button.set_choice_selected(button.choice_effect == attack_effect)
		button.queue_redraw()
	if _brush != null:
		_brush.attack_color = attack_color
		_brush.queue_redraw()
