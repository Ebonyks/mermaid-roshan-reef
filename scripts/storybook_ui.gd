class_name StorybookUI
extends RefCounted
# Shared touch-first visual grammar for every child-facing menu and overlay.
# These helpers build Godot-native Controls only: no generated prototype is
# shipped as a flat runtime texture. Gameplay state remains with each owner.

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const INK := Color(0.20, 0.18, 0.48, 1.0)
const INK_SOFT := Color(0.34, 0.30, 0.66, 0.92)
const PAPER := Color(0.94, 0.98, 1.0, 0.98)
const PAPER_COOL := Color(0.78, 0.95, 0.96, 0.98)
const LAVENDER := Color(0.78, 0.76, 0.98, 0.98)
const MINT := Color(0.52, 0.94, 0.78, 0.98)
const CORAL := Color(1.0, 0.50, 0.48, 0.98)
const GOLD := Color(1.0, 0.78, 0.30, 0.98)
const MUTED := Color(0.38, 0.42, 0.58, 0.92)
const DIM := Color(0.025, 0.06, 0.16, 0.76)
const MIN_TOUCH := Vector2(110.0, 110.0)

static func add_stage(parent: Control, viewport_size: Vector2) -> Control:
	var stage := Control.new()
	stage.name = "StorybookStage"
	stage.custom_minimum_size = CANVAS_SIZE
	stage.size = CANVAS_SIZE
	var scale_value: float = minf(viewport_size.x / CANVAS_SIZE.x, viewport_size.y / CANVAS_SIZE.y)
	stage.scale = Vector2.ONE * scale_value
	stage.position = (viewport_size - CANVAS_SIZE * scale_value) * 0.5
	parent.add_child(stage)
	return stage

static func panel_style(accent: Color = INK_SOFT, fill: Color = PAPER, radius: int = 34, border_width: int = 5) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = accent
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(radius)
	style.shadow_color = Color(0.08, 0.06, 0.22, 0.28)
	style.shadow_size = 12
	style.shadow_offset = Vector2(0.0, 7.0)
	style.content_margin_left = 18.0
	style.content_margin_right = 18.0
	style.content_margin_top = 12.0
	style.content_margin_bottom = 12.0
	return style

static func add_panel(parent: Control, rect: Rect2, accent: Color = INK_SOFT, fill: Color = PAPER, radius: int = 34) -> Panel:
	var panel := Panel.new()
	panel.position = rect.position
	panel.size = rect.size
	panel.add_theme_stylebox_override("panel", panel_style(accent, fill, radius))
	parent.add_child(panel)
	return panel

static func _button_fill(kind: String) -> Color:
	match kind:
		"primary":
			return MINT
		"action":
			return CORAL
		"gold":
			return GOLD
		"selected":
			return PAPER_COOL
		"locked":
			return Color(0.74, 0.76, 0.84, 0.96)
		"danger":
			return Color(0.82, 0.84, 0.92, 0.96)
		_:
			return Color(0.91, 0.93, 1.0, 0.98)

static func style_button(button: Button, kind: String = "secondary", font_size: int = 30, radius: int = 28) -> void:
	var fill: Color = _button_fill(kind)
	var normal := panel_style(INK_SOFT, fill, radius, 4)
	normal.shadow_size = 7
	normal.shadow_offset = Vector2(0.0, 4.0)
	var hover: StyleBoxFlat = normal.duplicate()
	hover.bg_color = fill.lightened(0.08)
	hover.border_color = GOLD if kind != "gold" else INK
	var pressed: StyleBoxFlat = normal.duplicate()
	pressed.bg_color = fill.darkened(0.10)
	pressed.shadow_size = 2
	pressed.shadow_offset = Vector2(0.0, 1.0)
	pressed.expand_margin_top = -2.0
	pressed.expand_margin_bottom = -2.0
	var focus: StyleBoxFlat = normal.duplicate()
	focus.border_color = GOLD
	focus.set_border_width_all(7)
	var disabled: StyleBoxFlat = normal.duplicate()
	disabled.bg_color = MUTED
	disabled.border_color = Color(0.62, 0.64, 0.76, 0.9)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", focus)
	button.add_theme_stylebox_override("disabled", disabled)
	button.add_theme_font_size_override("font_size", font_size)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", INK)
	button.add_theme_color_override("font_pressed_color", INK)
	button.add_theme_color_override("font_focus_color", INK)
	button.add_theme_color_override("font_disabled_color", Color(0.82, 0.84, 0.9))
	button.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.7))
	button.add_theme_constant_override("outline_size", 3)
	button.set_meta("storybook_kind", kind)
	button.set_meta("touch_target", true)

static func style_icon_button(button: Button, icon: String, kind: String = "secondary", size: Vector2 = MIN_TOUCH, parent_hint: String = "") -> void:
	button.text = icon
	button.custom_minimum_size = size
	button.size = size
	button.tooltip_text = parent_hint
	style_button(button, kind, maxi(34, int(minf(size.x, size.y) * 0.34)), int(minf(size.x, size.y) * 0.46))
	button.set_meta("picture_first", true)
	button.set_meta("parent_hint", parent_hint)

static func style_back_button(button: Button, parent_hint: String = "Back") -> void:
	style_icon_button(button, "↩", "secondary", Vector2(112.0, 112.0), parent_hint)
	button.set_meta("neutral_exit", true)

static func style_label(label: Label, font_size: int = 30, color: Color = INK, outline_size: int = 4) -> void:
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.75))
	label.add_theme_constant_override("outline_size", outline_size)

static func set_selected(button: Button, selected: bool, locked: bool = false) -> void:
	style_button(button, "locked" if locked else ("selected" if selected else "secondary"), int(button.get_theme_font_size("font_size")), 28)
	button.set_meta("selected", selected)
	button.set_meta("locked", locked)

static func add_dim(parent: Control, color: Color = DIM) -> ColorRect:
	var dim := ColorRect.new()
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.color = color
	parent.add_child(dim)
	return dim
