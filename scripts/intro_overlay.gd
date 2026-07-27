class_name IntroOverlay
extends RefCounted
# Picture-first, voice-first storybook intro. Protected character art is loaded
# unchanged; all framing and controls are Godot-native.

const INTRO_PANELS := [
	{"title": "Princess Huluu", "art": ["huluu"], "vo": "intro1", "text": "Princess Huluu lives in a kingdom in the sky."},
	{"title": "The Storm", "art": ["huluu"], "vo": "intro2", "text": "A storm swept her down to the sea!"},
	{"title": "Best Friends", "art": ["roshan"], "vo": "intro3", "text": "Roshan says: I will help you, Huluu!"},
	{"title": "Go Home Together", "art": ["roshan", "huluu"], "vo": "intro4", "text": "Find the pearls. Open the sky river. Take Huluu home!"}]

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_intro() -> void:
	m.intro_active = true
	m.intro_idx = 0
	m.intro_layer = CanvasLayer.new()
	m.intro_layer.layer = 20
	m.intro_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.intro_layer)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.intro_layer.add_child(root)
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.04, 0.18, 0.34)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(bg)
	var stage := StorybookUI.add_stage(root, m.get_viewport().get_visible_rect().size)

	# Tap-anywhere remains the easiest single-finger path. The visible next
	# shell below is the affordance; child buttons consume their own presses.
	var tap := Button.new()
	tap.name = "IntroTapAnywhere"
	tap.set_anchors_preset(Control.PRESET_FULL_RECT)
	tap.flat = true
	tap.focus_mode = Control.FOCUS_NONE
	var clear := StyleBoxEmpty.new()
	tap.add_theme_stylebox_override("normal", clear)
	tap.add_theme_stylebox_override("hover", clear)
	tap.add_theme_stylebox_override("pressed", clear)
	tap.pressed.connect(_intro_next)
	stage.add_child(tap)

	var book := StorybookUI.add_panel(stage, Rect2(150, 90, 980, 470), StorybookUI.INK_SOFT, Color(0.86, 0.97, 1.0, 0.98), 74)
	book.name = "IntroStoryBook"
	book.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var current := ColorRect.new()
	current.position = Vector2(626, 125)
	current.size = Vector2(12, 390)
	current.color = Color(0.52, 0.64, 0.86, 0.28)
	current.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(current)

	var pip_row := HBoxContainer.new()
	pip_row.position = Vector2(500, 18)
	pip_row.size = Vector2(280, 64)
	pip_row.add_theme_constant_override("separation", 18)
	stage.add_child(pip_row)
	var pips: Array[Label] = []
	for i in range(INTRO_PANELS.size()):
		var pip := Label.new()
		pip.text = "◉"
		pip.custom_minimum_size = Vector2(52, 52)
		pip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		pip.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		StorybookUI.style_label(pip, 42, StorybookUI.LAVENDER, 3)
		pip_row.add_child(pip)
		pips.append(pip)
	m.intro_layer.set_meta("page_pips", pips)

	m.intro_art = TextureRect.new()
	m.intro_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	m.intro_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	m.intro_art.size = Vector2(390, 410)
	m.intro_art.position = Vector2(445, 118)
	m.intro_art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(m.intro_art)
	m.intro_art2 = TextureRect.new()
	m.intro_art2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	m.intro_art2.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	m.intro_art2.size = Vector2(350, 390)
	m.intro_art2.position = Vector2(660, 132)
	m.intro_art2.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(m.intro_art2)

	var caption := StorybookUI.add_panel(stage, Rect2(350, 590, 580, 96), StorybookUI.LAVENDER, Color(0.94, 0.94, 1.0, 0.94), 30)
	caption.name = "IntroParentCaption"
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_text = Label.new()
	m.intro_text.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	m.intro_text.offset_left = 24
	m.intro_text.offset_right = -24
	m.intro_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	m.intro_text.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	m.intro_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	m.intro_text.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(m.intro_text, 22, StorybookUI.INK, 2)
	caption.add_child(m.intro_text)

	var speaker := Button.new()
	speaker.name = "IntroRepeatVoiceButton"
	StorybookUI.style_icon_button(speaker, "✦ )))", "selected", Vector2(132, 132), "Hear this page again")
	speaker.position = Vector2(36, 552)
	speaker.pressed.connect(_intro_repeat)
	stage.add_child(speaker)
	var next := Button.new()
	next.name = "IntroNextButton"
	StorybookUI.style_icon_button(next, "☞  ❯", "gold", Vector2(164, 164), "Next story picture")
	next.position = Vector2(1080, 526)
	next.pressed.connect(_intro_next)
	stage.add_child(next)

	# Whole-story skip requires a deliberate hold, preventing an edge graze
	# from throwing away the first-session story.
	var skip := Button.new()
	skip.name = "IntroHoldToSkipButton"
	StorybookUI.style_icon_button(skip, "▣", "secondary", Vector2(112, 112), "Hold to skip story")
	skip.position = Vector2(28, 24)
	skip.set_meta("hold_seconds", 1.2)
	stage.add_child(skip)
	var skip_timer := Timer.new()
	skip_timer.name = "IntroSkipHoldTimer"
	skip_timer.one_shot = true
	skip_timer.wait_time = 1.2
	skip_timer.timeout.connect(_skip_intro)
	stage.add_child(skip_timer)
	skip.button_down.connect(skip_timer.start)
	skip.button_up.connect(skip_timer.stop)
	_intro_show()

func _intro_tex(key: String) -> Texture2D:
	if key == "huluu":
		return load("res://assets/characters/friends/huluu.png")
	return load("res://assets/characters/roshan_sprite.png")

func _intro_show() -> void:
	var panel: Dictionary = INTRO_PANELS[m.intro_idx]
	m.intro_text.text = String(panel["title"]) + "  •  " + String(panel["text"])
	m._say("roshan", String(panel.get("vo", "")))
	var pips: Array = m.intro_layer.get_meta("page_pips", [])
	for i in range(pips.size()):
		var pip: Label = pips[i]
		pip.add_theme_color_override("font_color", StorybookUI.GOLD if i == m.intro_idx else StorybookUI.LAVENDER)
		pip.scale = Vector2.ONE * (1.18 if i == m.intro_idx else 1.0)
	var arts: Array = panel["art"]
	m.intro_art.texture = _intro_tex(String(arts[0]))
	if arts.size() > 1:
		m.intro_art.position = Vector2(280, 118)
		m.intro_art2.texture = _intro_tex(String(arts[1]))
		m.intro_art2.visible = true
	else:
		m.intro_art.position = Vector2(445, 118)
		m.intro_art2.visible = false

func _intro_repeat() -> void:
	if m.intro_idx < 0 or m.intro_idx >= INTRO_PANELS.size():
		return
	var panel: Dictionary = INTRO_PANELS[m.intro_idx]
	m._say("roshan", String(panel.get("vo", "")))

func _intro_next() -> void:
	m.intro_idx += 1
	if m.intro_idx >= INTRO_PANELS.size():
		_skip_intro()
		if m.voice != null:
			m.voice.pitch_scale = 1.1
			m.voice.play()
		return
	if m.chime != null:
		m.chime.pitch_scale = 1.0
		m.chime.play()
	_intro_show()

func _skip_intro() -> void:
	m.intro_active = false
	if m.intro_layer != null and is_instance_valid(m.intro_layer):
		m.intro_layer.queue_free()
	m.intro_layer = null
