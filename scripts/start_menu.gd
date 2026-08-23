class_name StartMenu
extends RefCounted
# Touch-first launch menu. The existing approved boot splash remains the
# complete background so engine splash -> menu is a seamless visual handoff.

const SPLASH_TEXTURE: Texture2D = preload("res://assets/ui/boot_splash_mermaid_roshan.png")
const BUTTON_FRAME: Texture2D = preload("res://assets/opera/worlds/ui/task_card_frame.png")
const LETTERBOX_COLOR := Color("188ed6")

static var skip_once_after_reset := false

var m: ReefMain
var _continue_button: Button = null
var _options_root: Control = null
var _confirm_root: Control = null
var _music_button: Button = null
var _quality_button: Button = null
var _mic_button: Button = null

func _init(main: ReefMain) -> void:
	m = main

func build() -> void:
	if skip_once_after_reset:
		skip_once_after_reset = false
		_enter_game()
		return
	m.start_menu_active = true
	# Existing gameplay and touch guards already treat the story intro as an
	# input-blocking surface. Reuse that contract while the launch menu is up.
	m.intro_active = true
	m.start_menu_layer = CanvasLayer.new()
	m.start_menu_layer.name = "StartMenu"
	m.start_menu_layer.layer = 20
	m.start_menu_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.start_menu_layer)
	var root := Control.new()
	root.name = "StartMenuRoot"
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	m.start_menu_layer.add_child(root)

	var background := ColorRect.new()
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.color = LETTERBOX_COLOR
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(background)
	var art := TextureRect.new()
	art.name = "StartMenuBackground"
	art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	art.texture = SPLASH_TEXTURE
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(art)
	var wash := ColorRect.new()
	wash.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	wash.color = Color(0.04, 0.05, 0.22, 0.10)
	wash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(wash)

	var stage := StorybookUI.add_stage(root, m.get_viewport().get_visible_rect().size)
	var launch_rect := Rect2(252, 514, 776, 178)
	var launch_panel := StorybookUI.add_panel(
		stage, launch_rect, StorybookUI.PURPLE, Color(0.92, 0.97, 1.0, 0.88), 58)
	launch_panel.name = "StartMenuLaunchPanel"
	launch_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.adorn_panel(stage, launch_rect, "StartMenu")

	_continue_button = _menu_button(
		stage, "StartMenuContinueButton", "▶  CONTINUE", Rect2(290, 548, 340, 118), "primary")
	_continue_button.disabled = not m.has_saved_game
	_continue_button.tooltip_text = "Continue the saved adventure"
	_continue_button.pressed.connect(_continue_game)
	var new_game := _menu_button(
		stage, "StartMenuNewGameButton", "★  NEW GAME", Rect2(650, 548, 340, 118), "gold")
	new_game.tooltip_text = "Start a new adventure"
	new_game.pressed.connect(_request_new_game)

	var options := _menu_button(
		stage, "StartMenuOptionsTab", "⚙  OPTIONS", Rect2(1044, 594, 210, 104), "secondary", 25)
	options.tooltip_text = "Options"
	options.pressed.connect(_toggle_options)
	_build_options(stage)
	_build_new_game_confirmation(stage)
	# Focus is deferred one frame so a launch key/button cannot activate the
	# newly focused choice on the same press that started the game.
	var initial_focus: Button = new_game if not m.has_saved_game else _continue_button
	m.get_tree().process_frame.connect(initial_focus.grab_focus, CONNECT_ONE_SHOT)

func _menu_button(
		parent: Control, node_name: String, text: String, rect: Rect2,
		kind: String, font_size: int = 34) -> Button:
	var button := Button.new()
	button.name = node_name
	button.text = text
	button.position = rect.position
	button.size = rect.size
	button.custom_minimum_size = rect.size
	StorybookUI.style_button(button, kind, font_size, 38)
	_style_mermaid_button(button, kind)
	parent.add_child(button)
	_add_shell_frame(button)
	return button

func _style_mermaid_button(button: Button, kind: String) -> void:
	# The title screen carries more of the splash painting's jewel-box richness:
	# aqua, orchid and pearl fills under the approved shell-and-pearl art.
	var fill := Color(0.62, 0.95, 1.0, 0.98)
	match kind:
		"gold":
			fill = Color(1.0, 0.82, 0.46, 0.99)
		"secondary":
			fill = Color(0.91, 0.83, 1.0, 0.99)
		"primary":
			fill = Color(0.55, 0.97, 0.92, 0.99)
	var normal := StorybookUI.panel_style(StorybookUI.PURPLE_DEEP, fill, 44, 3)
	normal.border_color = Color(0.33, 0.14, 0.58, 1.0)
	normal.shadow_color = Color(0.12, 0.05, 0.36, 0.48)
	normal.shadow_size = 12
	normal.shadow_offset = Vector2(0.0, 7.0)
	var hover: StyleBoxFlat = normal.duplicate()
	hover.bg_color = fill.lightened(0.10)
	hover.border_color = StorybookUI.GOLD
	var pressed: StyleBoxFlat = normal.duplicate()
	pressed.bg_color = fill.darkened(0.12)
	pressed.shadow_size = 3
	pressed.shadow_offset = Vector2(0.0, 2.0)
	var focus: StyleBoxFlat = normal.duplicate()
	focus.border_color = Color(1.0, 0.92, 0.48, 1.0)
	focus.set_border_width_all(7)
	var disabled: StyleBoxFlat = normal.duplicate()
	disabled.bg_color = Color(0.70, 0.72, 0.84, 0.94)
	disabled.border_color = Color(0.44, 0.39, 0.62, 0.90)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", focus)
	button.add_theme_stylebox_override("disabled", disabled)
	button.add_theme_color_override("font_color", StorybookUI.PURPLE_DEEP)
	button.add_theme_color_override("font_hover_color", StorybookUI.PURPLE_DEEP)
	button.add_theme_color_override("font_pressed_color", StorybookUI.PURPLE_DEEP)
	button.add_theme_color_override("font_focus_color", StorybookUI.PURPLE_DEEP)
	button.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.92))
	button.add_theme_constant_override("outline_size", 5)

func _add_shell_frame(button: Button) -> void:
	# Nine-slice the existing Opera shell/pearl frame so its sculpted corners
	# stay crisp on both the wide launch buttons and the smaller Options tab.
	var frame := NinePatchRect.new()
	frame.name = String(button.name) + "ShellPearlFrame"
	frame.texture = BUTTON_FRAME
	frame.draw_center = false
	frame.set_patch_margin(SIDE_LEFT, 210)
	frame.set_patch_margin(SIDE_TOP, 210)
	frame.set_patch_margin(SIDE_RIGHT, 210)
	frame.set_patch_margin(SIDE_BOTTOM, 210)
	# Both axes default to Stretch in Godot 4.7.1, which preserves the corners
	# while expanding the pearl bands between them.
	frame.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	frame.offset_left = -9.0
	frame.offset_top = -9.0
	frame.offset_right = 9.0
	frame.offset_bottom = 9.0
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.add_child(frame)

func _build_options(stage: Control) -> void:
	_options_root = Control.new()
	_options_root.name = "StartMenuOptionsPanel"
	_options_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_options_root.visible = false
	stage.add_child(_options_root)
	var dim := StorybookUI.add_dim(_options_root, Color(0.025, 0.06, 0.16, 0.66))
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	var shell_rect := Rect2(650, 72, 560, 548)
	var shell := StorybookUI.add_panel(
		_options_root, shell_rect, StorybookUI.PURPLE, Color(0.92, 0.97, 1.0, 0.99), 58)
	shell.name = "StartMenuOptionsShell"
	StorybookUI.adorn_panel(_options_root, shell_rect, "StartOptions")
	var title := Label.new()
	title.text = "⚙  OPTIONS"
	title.position = Vector2(720, 112)
	title.size = Vector2(350, 70)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_label(title, 38, StorybookUI.INK, 4)
	_options_root.add_child(title)
	_music_button = _menu_button(
		_options_root, "StartMenuMusicButton", "", Rect2(715, 205, 430, 100), "secondary", 30)
	_music_button.pressed.connect(_toggle_music)
	_quality_button = _menu_button(
		_options_root, "StartMenuQualityButton", "", Rect2(715, 325, 430, 100), "primary", 30)
	_quality_button.pressed.connect(_toggle_quality)
	_mic_button = _menu_button(
		_options_root, "StartMenuMicButton", "", Rect2(715, 445, 430, 100), "gold", 30)
	_mic_button.pressed.connect(_toggle_mic)
	var close := Button.new()
	close.name = "StartMenuOptionsCloseButton"
	StorybookUI.style_back_button(close, "Close options")
	close.position = Vector2(1074, 90)
	close.pressed.connect(_close_options)
	_options_root.add_child(close)
	_sync_option_labels()

func _build_new_game_confirmation(stage: Control) -> void:
	_confirm_root = Control.new()
	_confirm_root.name = "StartMenuNewGameConfirmation"
	_confirm_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_confirm_root.visible = false
	stage.add_child(_confirm_root)
	var dim := StorybookUI.add_dim(_confirm_root, Color(0.025, 0.06, 0.16, 0.76))
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	var shell_rect := Rect2(270, 164, 740, 390)
	var shell := StorybookUI.add_panel(
		_confirm_root, shell_rect, StorybookUI.PURPLE, Color(0.94, 0.97, 1.0, 0.99), 62)
	shell.name = "StartMenuNewGameShell"
	StorybookUI.adorn_panel(_confirm_root, shell_rect, "StartNewGame")
	var title := Label.new()
	title.text = "START A NEW GAME?"
	title.position = Vector2(330, 210)
	title.size = Vector2(620, 64)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(title, 40, StorybookUI.INK, 4)
	_confirm_root.add_child(title)
	var note := Label.new()
	note.text = "Your saved adventure will be kept for a grown-up to restore."
	note.position = Vector2(350, 278)
	note.size = Vector2(580, 70)
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	note.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_label(note, 22, StorybookUI.MUTED, 2)
	_confirm_root.add_child(note)
	var keep := _menu_button(
		_confirm_root, "StartMenuKeepGameButton", "↩  KEEP GAME", Rect2(320, 380, 300, 118), "primary", 30)
	keep.pressed.connect(_cancel_new_game)
	var start := _menu_button(
		_confirm_root, "StartMenuConfirmNewGameButton", "★  START NEW", Rect2(660, 380, 300, 118), "gold", 30)
	start.pressed.connect(_perform_new_game)

func _continue_game() -> void:
	if not m.has_saved_game:
		return
	_enter_game()

func _enter_game() -> void:
	m.start_menu_active = false
	m.intro_active = false
	if m.start_menu_layer != null and is_instance_valid(m.start_menu_layer):
		m.start_menu_layer.queue_free()
	m.start_menu_layer = null
	if m.first_session:
		m._build_intro()
	elif m.chime != null:
		m.chime.pitch_scale = 1.0
		m.chime.play()

func _request_new_game() -> void:
	if not m.has_saved_game:
		_perform_new_game()
		return
	_close_options()
	_confirm_root.visible = true
	var confirm := _confirm_root.get_node_or_null("StartMenuConfirmNewGameButton") as Button
	if confirm != null:
		confirm.grab_focus()

func _cancel_new_game() -> void:
	_confirm_root.visible = false
	if _continue_button != null:
		_continue_button.grab_focus()

func _perform_new_game() -> void:
	if not m._start_new_game():
		return
	skip_once_after_reset = true
	m.get_tree().call_deferred("reload_current_scene")

func _toggle_options() -> void:
	if _options_root.visible:
		_close_options()
		return
	_confirm_root.visible = false
	_options_root.visible = true
	_sync_option_labels()
	_music_button.grab_focus()

func _close_options() -> void:
	if _options_root == null:
		return
	_options_root.visible = false

func _toggle_music() -> void:
	m.music_on = not m.music_on
	if m.music != null:
		m.music.volume_db = -8.0 if m.music_on else -60.0
	_save_options()

func _toggle_quality() -> void:
	m._apply_quality("speedy" if m.quality == "sparkly" else "sparkly")
	_save_options()

func _toggle_mic() -> void:
	m.mic_on = not m.mic_on
	if not m.mic_on:
		m._mic_ref().disarm()
	_save_options()

func _save_options() -> void:
	if m._write_save():
		m.has_saved_game = true
		if _continue_button != null:
			_continue_button.disabled = false
	_sync_option_labels()

func _sync_option_labels() -> void:
	if _music_button != null:
		_music_button.text = "♫  MUSIC ON" if m.music_on else "♫̸  MUSIC OFF"
		_music_button.set_meta("toggle_on", m.music_on)
	if _quality_button != null:
		_quality_button.text = "✦  SPARKLY" if m.quality == "sparkly" else "≋  SPEEDY"
		_quality_button.set_meta("toggle_on", m.quality == "sparkly")
	if _mic_button != null:
		_mic_button.text = "🎤  SAY SPELLS" if m.mic_on else "🎤̸  SPELLS OFF"
		_mic_button.set_meta("toggle_on", m.mic_on)
