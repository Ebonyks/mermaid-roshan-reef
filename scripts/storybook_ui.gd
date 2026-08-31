class_name StorybookUI
extends RefCounted
# Shared touch-first visual grammar for every child-facing menu and overlay.
# These helpers build Godot-native Controls only: no generated prototype is
# shipped as a flat runtime texture. Gameplay state remains with each owner.

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const INK := Color(0.20, 0.18, 0.48, 1.0)
const INK_SOFT := Color(0.34, 0.30, 0.66, 0.92)
const PURPLE_DEEP := Color(0.22, 0.14, 0.52, 1.0)
const PURPLE := Color(0.43, 0.30, 0.76, 1.0)
const LILAC := Color(0.82, 0.76, 1.0, 0.98)
const PEARL := Color(0.97, 0.95, 1.0, 1.0)
const PEARL_BLUE := Color(0.70, 0.97, 1.0, 1.0)
const PAPER := Color(0.94, 0.98, 1.0, 0.98)
const PAPER_COOL := Color(0.78, 0.95, 0.96, 0.98)
const LAVENDER := Color(0.78, 0.76, 0.98, 0.98)
const MINT := Color(0.52, 0.94, 0.78, 0.98)
const CORAL := Color(1.0, 0.50, 0.48, 0.98)
const GOLD := Color(1.0, 0.78, 0.30, 0.98)
const MUTED := Color(0.38, 0.42, 0.58, 0.92)
const DIM := Color(0.025, 0.06, 0.16, 0.76)
const MIN_TOUCH := Vector2(110.0, 110.0)
const SHELL_ORNAMENT_SCRIPT := preload("res://scripts/shell_ornament.gd")

# Typography roles are explicit, but font identity and fallback evidence are
# still unresolved.  The engine/system default is not a project authority and
# must never be reported as approved or deterministic.
const TYPOGRAPHY_FONT_AUTHORITY: String = "UNRESOLVED"
const TYPOGRAPHY_FALLBACK_AUTHORITY: String = "MISSING"
const ROLE_DISPLAY := &"display"
const ROLE_TITLE := &"title"
const ROLE_CHILD_CONTROL := &"child_control"
const ROLE_BODY := &"body"
const ROLE_ADULT_CAPTION := &"adult_caption"
const ROLE_STATUS := &"status"
const ROLE_NUMERIC := &"numeric_progress"
const ROLE_DECORATIVE_GLYPH := &"decorative_glyph"
const TYPOGRAPHY_ROLES: Dictionary = {
	ROLE_DISPLAY: {"font_size": 56, "font_color": PEARL, "outline_color": INK,
		"outline_size": 6, "focus_color": PEARL, "pressed_color": PEARL,
		"hover_pressed_color": PEARL,
		"disabled_color": MUTED, "wrap_mode": TextServer.AUTOWRAP_OFF,
		"max_lines": 1},
	ROLE_TITLE: {"font_size": 44, "font_color": INK, "outline_color": PEARL,
		"outline_size": 4, "focus_color": INK, "pressed_color": INK,
		"hover_pressed_color": INK,
		"disabled_color": MUTED, "wrap_mode": TextServer.AUTOWRAP_WORD_SMART,
		"max_lines": 2},
	ROLE_CHILD_CONTROL: {"font_size": 30, "font_color": PURPLE_DEEP,
		"outline_color": Color(1.0, 1.0, 1.0, 0.7), "outline_size": 3,
		"focus_color": PURPLE_DEEP, "pressed_color": PURPLE_DEEP,
		"hover_pressed_color": PURPLE_DEEP,
		"disabled_color": Color(0.82, 0.84, 0.9),
		"wrap_mode": TextServer.AUTOWRAP_WORD_SMART, "max_lines": 2},
	ROLE_BODY: {"font_size": 30, "font_color": INK, "outline_color": PEARL,
		"outline_size": 4, "focus_color": INK, "pressed_color": INK,
		"hover_pressed_color": INK,
		"disabled_color": MUTED, "wrap_mode": TextServer.AUTOWRAP_WORD_SMART,
		"max_lines": 3},
	ROLE_ADULT_CAPTION: {"font_size": 22, "font_color": INK_SOFT,
		"outline_color": PEARL, "outline_size": 3, "focus_color": INK_SOFT,
		"pressed_color": INK_SOFT, "hover_pressed_color": INK_SOFT,
		"disabled_color": MUTED,
		"wrap_mode": TextServer.AUTOWRAP_WORD_SMART, "max_lines": 3},
	ROLE_STATUS: {"font_size": 30, "font_color": INK, "outline_color": PEARL,
		"outline_size": 4, "focus_color": INK, "pressed_color": INK,
		"hover_pressed_color": INK,
		"disabled_color": MUTED, "wrap_mode": TextServer.AUTOWRAP_WORD_SMART,
		"max_lines": 2},
	ROLE_NUMERIC: {"font_size": 34, "font_color": PURPLE_DEEP,
		"outline_color": PEARL, "outline_size": 4,
		"focus_color": PURPLE_DEEP, "pressed_color": PURPLE_DEEP,
		"hover_pressed_color": PURPLE_DEEP,
		"disabled_color": MUTED, "wrap_mode": TextServer.AUTOWRAP_OFF,
		"max_lines": 1},
	ROLE_DECORATIVE_GLYPH: {"font_size": 30, "font_color": PURPLE_DEEP,
		"outline_color": PEARL, "outline_size": 3,
		"focus_color": PURPLE_DEEP, "pressed_color": PURPLE_DEEP,
		"hover_pressed_color": PURPLE_DEEP,
		"disabled_color": MUTED, "wrap_mode": TextServer.AUTOWRAP_OFF,
		"max_lines": 1},
}

static func typography_role(role: StringName) -> Dictionary:
	var token: Dictionary = (TYPOGRAPHY_ROLES[role] if TYPOGRAPHY_ROLES.has(role)
		else TYPOGRAPHY_ROLES[ROLE_BODY]).duplicate()
	token["font_authority"] = TYPOGRAPHY_FONT_AUTHORITY
	token["fallback_authority"] = TYPOGRAPHY_FALLBACK_AUTHORITY
	token["line_spacing"] = 0
	return token

static func _apply_typography(control: Control, role: StringName,
		font_size: int = -1) -> void:
	var token: Dictionary = typography_role(role)
	var resolved_size: int = int(token["font_size"]) if font_size < 0 else font_size
	control.add_theme_font_size_override("font_size", resolved_size)
	control.add_theme_color_override("font_color", token["font_color"])
	control.add_theme_color_override("font_outline_color", token["outline_color"])
	control.add_theme_constant_override("outline_size", int(token["outline_size"]))
	control.add_theme_constant_override("line_spacing", int(token["line_spacing"]))
	control.set_meta("typography_role", role)
	control.set_meta("typography_font_authority", TYPOGRAPHY_FONT_AUTHORITY)
	control.set_meta("typography_fallback_authority", TYPOGRAPHY_FALLBACK_AUTHORITY)
	control.set_meta("typography_wrap_mode", int(token["wrap_mode"]))

static func _apply_button_typography(button: Button, role: StringName,
		font_size: int = -1) -> void:
	var token: Dictionary = typography_role(role)
	_apply_typography(button, role, font_size)
	button.add_theme_color_override("font_hover_color", token["focus_color"])
	button.add_theme_color_override("font_focus_color", token["focus_color"])
	button.add_theme_color_override("font_pressed_color", token["pressed_color"])
	button.add_theme_color_override("font_hover_pressed_color", token["hover_pressed_color"])
	button.add_theme_color_override("font_disabled_color", token["disabled_color"])
	button.autowrap_mode = int(token["wrap_mode"])
	# Button has no max_lines_visible property.  Keep max_lines a Label-only
	# contract rather than implying that this metadata limits Button text.
	button.set_meta("typography_max_lines_supported", false)

static func _apply_label_typography(label: Label, role: StringName,
		font_size: int = -1) -> void:
	var token: Dictionary = typography_role(role)
	_apply_typography(label, role, font_size)
	label.autowrap_mode = int(token["wrap_mode"])
	label.max_lines_visible = int(token["max_lines"])
	label.set_meta("typography_max_lines", int(token["max_lines"]))

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
	# Every surface keeps the dark-violet contour from the approved shell
	# prototypes. The caller's accent still tints the contour, but can no
	# longer turn a menu into a generic pale rounded rectangle.
	style.border_color = accent.lerp(PURPLE_DEEP, 0.62)
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(radius)
	style.shadow_color = Color(0.19, 0.10, 0.48, 0.34)
	style.shadow_size = 14
	style.shadow_offset = Vector2(0.0, 8.0)
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

static func add_hud_panel(parent: Node, rect: Rect2, accent: Color = INK_SOFT, fill: Color = PAPER, radius: int = 30) -> Panel:
	var panel := Panel.new()
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_theme_stylebox_override("panel", panel_style(accent, fill, radius, 4))
	panel.set_meta("storybook_surface", true)
	parent.add_child(panel)
	return panel

static func add_shell_crest(parent: Node, rect: Rect2, ornament_name: String = "StorybookShellCrest") -> Control:
	var crest: Control = SHELL_ORNAMENT_SCRIPT.new()
	crest.name = ornament_name
	crest.position = rect.position
	crest.size = rect.size
	crest.set_meta("storybook_shell", true)
	parent.add_child(crest)
	return crest

static func add_pearl(parent: Node, center: Vector2, diameter: float = 18.0, ornament_name: String = "StorybookPearl") -> Panel:
	var dot := Panel.new()
	dot.name = ornament_name
	dot.position = center - Vector2.ONE * diameter * 0.5
	dot.size = Vector2.ONE * diameter
	dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = PEARL_BLUE
	style.border_color = PURPLE_DEEP
	style.set_border_width_all(maxi(2, int(diameter * 0.12)))
	style.set_corner_radius_all(int(diameter * 0.5))
	style.shadow_color = Color(0.24, 0.13, 0.54, 0.28)
	style.shadow_size = 4
	dot.add_theme_stylebox_override("panel", style)
	dot.set_meta("storybook_pearl", true)
	parent.add_child(dot)
	return dot

static func adorn_panel(parent: Node, rect: Rect2, prefix: String = "Storybook") -> void:
	# A restrained crest and four pearls reproduce the shell/pearl hierarchy of
	# the prototype without obscuring content or creating expensive overdraw.
	add_shell_crest(parent, Rect2(
		Vector2(rect.get_center().x - 58.0, rect.position.y - 22.0),
		Vector2(116.0, 82.0)), prefix + "ShellCrest")
	add_pearl(parent, rect.position + Vector2(28.0, 31.0), 18.0, prefix + "PearlTL")
	add_pearl(parent, Vector2(rect.end.x - 28.0, rect.position.y + 31.0), 18.0, prefix + "PearlTR")
	add_pearl(parent, Vector2(rect.position.x + 32.0, rect.end.y - 30.0), 14.0, prefix + "PearlBL")
	add_pearl(parent, rect.end - Vector2(32.0, 30.0), 14.0, prefix + "PearlBR")

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

static func style_button(button: Button, kind: String = "secondary", font_size: int = -1,
		radius: int = 28, role: StringName = ROLE_CHILD_CONTROL) -> void:
	var fill: Color = _button_fill(kind)
	var normal := panel_style(PURPLE, fill, radius, 5)
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
	var hover_pressed: StyleBoxFlat = pressed.duplicate()
	hover_pressed.bg_color = fill.darkened(0.04)
	hover_pressed.border_color = GOLD if kind != "gold" else INK
	var focus: StyleBoxFlat = normal.duplicate()
	focus.border_color = GOLD
	focus.set_border_width_all(8)
	var disabled: StyleBoxFlat = normal.duplicate()
	disabled.bg_color = MUTED
	disabled.border_color = Color(0.62, 0.64, 0.76, 0.9)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("hover_pressed", hover_pressed)
	button.add_theme_stylebox_override("focus", focus)
	button.add_theme_stylebox_override("disabled", disabled)
	_apply_button_typography(button, role, font_size)
	var token: Dictionary = typography_role(role)
	button.add_theme_color_override("font_hover_pressed_color", token["hover_pressed_color"])
	button.set_meta("storybook_kind", kind)
	button.set_meta("touch_target", true)

static func style_picture_button(button: Button, fill: Color = PAPER,
		accent: Color = PURPLE, radius: int = 28,
		role: StringName = ROLE_CHILD_CONTROL, font_size: int = -1) -> void:
	# Art-backed choices still need the same violet contour, physical press,
	# focus ring and shadow as text/icon tiles. Keeping this in the shared
	# system prevents picture games and selectors from falling back to flat,
	# feedback-free hotspots.
	var normal := panel_style(accent, fill, radius, 5)
	normal.shadow_size = 7
	normal.shadow_offset = Vector2(0.0, 4.0)
	var hover: StyleBoxFlat = normal.duplicate()
	hover.bg_color = fill.lightened(0.08)
	hover.border_color = GOLD
	var pressed: StyleBoxFlat = normal.duplicate()
	pressed.bg_color = fill.darkened(0.10)
	pressed.shadow_size = 2
	pressed.shadow_offset = Vector2(0.0, 1.0)
	var hover_pressed: StyleBoxFlat = pressed.duplicate()
	hover_pressed.bg_color = fill.darkened(0.04)
	hover_pressed.border_color = GOLD
	var focus: StyleBoxFlat = normal.duplicate()
	focus.border_color = GOLD
	focus.set_border_width_all(8)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("hover_pressed", hover_pressed)
	button.add_theme_stylebox_override("focus", focus)
	button.add_theme_stylebox_override("disabled", panel_style(
		MUTED, Color(0.74, 0.76, 0.84, 0.96), radius, 5))
	_apply_button_typography(button, role, font_size)
	var token: Dictionary = typography_role(role)
	button.add_theme_color_override("font_hover_pressed_color", token["hover_pressed_color"])
	button.set_meta("storybook_kind", "picture")
	button.set_meta("picture_first", true)
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

static func style_label(label: Label, font_size: int = -1,
		color: Color = Color(-1.0, -1.0, -1.0, -1.0), outline_size: int = -1,
		role: StringName = ROLE_BODY) -> void:
	_apply_label_typography(label, role, font_size)
	var token: Dictionary = typography_role(role)
	# Keep historical color/outline arguments as compatibility overrides while
	# allowing omitted values to use the named role token.
	label.add_theme_color_override("font_color",
			token["font_color"] if color.r < 0.0 else color)
	label.add_theme_constant_override("outline_size",
			int(token["outline_size"]) if outline_size < 0 else outline_size)

static func style_hud_label(label: Label, font_size: int = -1,
		color: Color = Color(-1.0, -1.0, -1.0, -1.0), outline_size: int = -1,
		role: StringName = ROLE_STATUS) -> void:
	style_label(label, font_size, color, outline_size, role)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.set_meta("storybook_hud", true)

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
