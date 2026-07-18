class_name IntroOverlay
extends RefCounted
# Mechanical extraction of the storybook intro overlay from main.gd. All
# state (intro_layer, intro_idx, intro_active, the art/text controls) stays
# on main (m.*); this class receives main by reference and owns only logic.

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
	# tap-anywhere advance button (full screen, transparent)
	var tap := Button.new()
	tap.set_anchors_preset(Control.PRESET_FULL_RECT)
	tap.flat = true
	tap.focus_mode = Control.FOCUS_NONE
	var clear := StyleBoxEmpty.new()
	tap.add_theme_stylebox_override("normal", clear)
	tap.add_theme_stylebox_override("hover", clear)
	tap.add_theme_stylebox_override("pressed", clear)
	tap.pressed.connect(_intro_next)
	m.intro_layer.add_child(tap)
	# soft underwater backdrop
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.05, 0.13, 0.26)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_layer.add_child(bg)
	var glowtop := ColorRect.new()
	glowtop.set_anchors_preset(Control.PRESET_TOP_WIDE)
	glowtop.custom_minimum_size = Vector2(0, 360)
	glowtop.size = Vector2(1280, 360)
	glowtop.color = Color(0.12, 0.30, 0.45, 0.6)
	glowtop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_layer.add_child(glowtop)
	# two character slots
	m.intro_art = TextureRect.new()
	m.intro_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	m.intro_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	m.intro_art.custom_minimum_size = Vector2(360, 560)
	m.intro_art.size = Vector2(360, 560)
	m.intro_art.position = Vector2(470, 70)
	m.intro_art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_layer.add_child(m.intro_art)
	m.intro_art2 = TextureRect.new()
	m.intro_art2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	m.intro_art2.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	m.intro_art2.custom_minimum_size = Vector2(300, 470)
	m.intro_art2.size = Vector2(300, 470)
	m.intro_art2.position = Vector2(760, 150)
	m.intro_art2.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_layer.add_child(m.intro_art2)
	# narration panel
	var panel := Panel.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.04, 0.08, 0.2, 0.92)
	psb.set_corner_radius_all(8)
	psb.border_color = Color(1.0, 0.8, 0.5)
	psb.set_border_width_all(3)
	panel.add_theme_stylebox_override("panel", psb)
	panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	panel.position = Vector2(90, 540)
	panel.size = Vector2(1100, 150)
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_layer.add_child(panel)
	m.intro_text = Label.new()
	m.intro_text.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	m.intro_text.offset_left = 30
	m.intro_text.offset_right = -30
	m.intro_text.add_theme_font_size_override("font_size", 30)
	m.intro_text.add_theme_color_override("font_outline_color", Color(0.10, 0.08, 0.28, 0.88))
	m.intro_text.add_theme_constant_override("outline_size", 5)
	m.intro_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	m.intro_text.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	m.intro_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	m.intro_text.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(m.intro_text)
	# "tap to continue" hint
	var hint := Label.new()
	hint.text = "tap to continue \u25b6"
	hint.add_theme_font_size_override("font_size", 22)
	hint.add_theme_color_override("font_color", Color(1.0, 0.9, 0.6))
	hint.position = Vector2(980, 700)
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.intro_layer.add_child(hint)
	_intro_show()

func _intro_tex(key: String) -> Texture2D:
	if key == "huluu":
		return load("res://assets/characters/friends/huluu.png")
	return load("res://assets/characters/roshan_sprite.png")

func _intro_show() -> void:
	var p: Dictionary = INTRO_PANELS[m.intro_idx]
	m.intro_text.text = String(p["text"])
	m._say("roshan", String(p.get("vo", "")))
	var arts: Array = p["art"]
	m.intro_art.texture = _intro_tex(String(arts[0]))
	if arts.size() > 1:
		m.intro_art.position = Vector2(330, 70)
		m.intro_art2.texture = _intro_tex(String(arts[1]))
		m.intro_art2.visible = true
	else:
		m.intro_art.position = Vector2(470, 70)
		m.intro_art2.visible = false

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
