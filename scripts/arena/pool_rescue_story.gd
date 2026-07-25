class_name PoolRescueStory
extends RefCounted
# Tap-anywhere storybook chapters for the Royal Natatorium rescue. Runtime
# controls and queue state stay on ReefMain.g; this helper owns only logic.

const STORYBOARD_PATH := "res://assets/castle/pool_2d/whale_rescue_storyboard.png"
const PANEL_COUNT := 9
const PANEL_VOICES: Array[Dictionary] = [
	{"speaker": "roshan", "event": "whale"},
	{"speaker": "roshan", "event": "talk"},
	{"speaker": "roshan", "event": "talk"},
	{"speaker": "roshan", "event": "pearl"},
	{"speaker": "roshan", "event": "talk"},
	{"speaker": "roshan", "event": "pearl2"},
	{"speaker": "roshan", "event": "pearl3"},
	{"speaker": "roshan", "event": "whale"},
	{"speaker": "roshan", "event": "win"},
]

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func is_active() -> bool:
	return bool(m.g.get("pool_story_active", false))

func start_panels(panel_indices: Array[int]) -> void:
	if panel_indices.is_empty():
		return
	# The launch story owns intro_active while it is on screen. A pool chapter
	# never replaces it; the player can meet the whale after that book closes.
	if m.intro_active and not is_active():
		return
	if is_active():
		var active_queue: Array = m.g.get("pool_story_queue", [])
		for panel_index: int in panel_indices:
			if panel_index >= 0 and panel_index < PANEL_COUNT:
				active_queue.append(panel_index)
		return
	var queue: Array[int] = []
	for panel_index: int in panel_indices:
		if panel_index >= 0 and panel_index < PANEL_COUNT:
			queue.append(panel_index)
	if queue.is_empty():
		return
	m.g["pool_story_queue"] = queue
	m.g["pool_story_queue_pos"] = 0
	m.g["pool_story_active"] = true
	m.intro_active = true

	var layer := CanvasLayer.new()
	layer.layer = 24
	layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(layer)
	m.g["pool_story_layer"] = layer

	var backdrop := ColorRect.new()
	backdrop.set_anchors_preset(Control.PRESET_FULL_RECT)
	backdrop.color = Color(0.035, 0.07, 0.15, 0.97)
	backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(backdrop)

	var frame := Panel.new()
	frame.position = Vector2(304.0, 14.0)
	frame.size = Vector2(672.0, 672.0)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var frame_style := StyleBoxFlat.new()
	frame_style.bg_color = Color(0.90, 0.96, 1.0)
	frame_style.border_color = Color(1.0, 0.80, 0.36)
	frame_style.set_border_width_all(7)
	frame_style.set_corner_radius_all(24)
	frame.add_theme_stylebox_override("panel", frame_style)
	layer.add_child(frame)

	var art := TextureRect.new()
	art.position = Vector2(10.0, 10.0)
	art.size = Vector2(652.0, 652.0)
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.add_child(art)
	m.g["pool_story_art"] = art

	var dots := Label.new()
	dots.position = Vector2(500.0, 684.0)
	dots.size = Vector2(280.0, 32.0)
	dots.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	dots.add_theme_font_size_override("font_size", 22)
	dots.add_theme_color_override("font_color", Color(1.0, 0.86, 0.48))
	dots.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(dots)
	m.g["pool_story_dots"] = dots

	var next_hint := Label.new()
	next_hint.text = "▶"
	next_hint.position = Vector2(1182.0, 630.0)
	next_hint.size = Vector2(72.0, 72.0)
	next_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	next_hint.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	next_hint.add_theme_font_size_override("font_size", 48)
	next_hint.add_theme_color_override("font_color", Color(1.0, 0.85, 0.38))
	next_hint.add_theme_color_override("font_outline_color", Color(0.12, 0.08, 0.28))
	next_hint.add_theme_constant_override("outline_size", 8)
	next_hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(next_hint)

	# One finger anywhere advances. The button is last so it receives input over
	# every decorative control without requiring a small reading-dependent target.
	var tap := Button.new()
	tap.set_anchors_preset(Control.PRESET_FULL_RECT)
	tap.flat = true
	tap.focus_mode = Control.FOCUS_NONE
	var clear := StyleBoxEmpty.new()
	tap.add_theme_stylebox_override("normal", clear)
	tap.add_theme_stylebox_override("hover", clear)
	tap.add_theme_stylebox_override("pressed", clear)
	tap.pressed.connect(advance)
	layer.add_child(tap)
	_show_current()

func advance() -> void:
	if not is_active():
		return
	var queue: Array = m.g.get("pool_story_queue", [])
	var queue_pos: int = int(m.g.get("pool_story_queue_pos", 0)) + 1
	if queue_pos >= queue.size():
		close()
		return
	m.g["pool_story_queue_pos"] = queue_pos
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + float(queue_pos % 3) * 0.08
		m.chime.play()
	_show_current()

func close() -> void:
	if not is_active():
		return
	m.g["pool_story_active"] = false
	m.g["castle_pool_action_prev"] = true
	var layer_value: Variant = m.g.get("pool_story_layer")
	if layer_value is CanvasLayer and is_instance_valid(layer_value):
		(layer_value as CanvasLayer).queue_free()
	m.g.erase("pool_story_layer")
	m.g.erase("pool_story_art")
	m.g.erase("pool_story_dots")
	m.g.erase("pool_story_queue")
	m.g.erase("pool_story_queue_pos")
	m.intro_active = false

func _show_current() -> void:
	var queue: Array = m.g.get("pool_story_queue", [])
	var queue_pos: int = int(m.g.get("pool_story_queue_pos", 0))
	if queue_pos < 0 or queue_pos >= queue.size():
		close()
		return
	var panel_index: int = int(queue[queue_pos])
	var art_value: Variant = m.g.get("pool_story_art")
	if not (art_value is TextureRect) or not is_instance_valid(art_value):
		close()
		return
	var atlas := load(STORYBOARD_PATH) as Texture2D
	if atlas == null:
		close()
		return
	@warning_ignore("integer_division")
	var cell_width: int = atlas.get_width() / 3
	@warning_ignore("integer_division")
	var cell_height: int = atlas.get_height() / 3
	@warning_ignore("integer_division")
	var cell_row: int = panel_index / 3
	var atlas_texture := AtlasTexture.new()
	atlas_texture.atlas = atlas
	atlas_texture.region = Rect2(
		float((panel_index % 3) * cell_width),
		float(cell_row * cell_height),
		float(cell_width),
		float(cell_height),
	)
	atlas_texture.filter_clip = true
	(art_value as TextureRect).texture = atlas_texture
	m.g["pool_story_last_panel"] = panel_index
	m.g["pool_story_seen_mask"] = (
		int(m.g.get("pool_story_seen_mask", 0)) | (1 << panel_index))

	var dots_value: Variant = m.g.get("pool_story_dots")
	if dots_value is Label and is_instance_valid(dots_value):
		var dot_text := ""
		for i in range(queue.size()):
			dot_text += "●" if i == queue_pos else "○"
		(dots_value as Label).text = dot_text
	var voice: Dictionary = PANEL_VOICES[panel_index]
	m._say(String(voice["speaker"]), String(voice["event"]), 0.0)
