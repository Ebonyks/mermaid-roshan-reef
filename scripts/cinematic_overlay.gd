class_name CinematicOverlay
extends RefCounted
# One full-screen player for authored OGV story beats. Missing development
# footage uses a neutral black fallback rather than stretching an invalid plate.

var m: ReefMain
var layer: CanvasLayer = null
var video: VideoStreamPlayer = null
var finished_callback: Callable
var overlay_id := "Story"

func _init(main: ReefMain) -> void:
	m = main

func is_active() -> bool:
	return layer != null and is_instance_valid(layer)

func play(video_path: String, fallback_art: String, on_finished: Callable,
		control_prefix: String = "Story") -> void:
	clear()
	finished_callback = on_finished
	overlay_id = control_prefix
	m.intro_active = true
	m._set_world_controls_enabled(false, "story_cinematic")
	layer = CanvasLayer.new()
	layer.name = control_prefix + "CinematicLayer"
	layer.layer = 25
	layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(layer)
	m.intro_layer = layer
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.add_child(root)
	var black := ColorRect.new()
	black.set_anchors_preset(Control.PRESET_FULL_RECT)
	black.color = Color(0.025, 0.035, 0.11)
	black.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(black)

	var loaded_video := false
	if ResourceLoader.exists(video_path):
		var stream: VideoStream = load(video_path) as VideoStream
		if stream != null:
			video = VideoStreamPlayer.new()
			video.name = control_prefix + "VideoPlayer"
			video.set_anchors_preset(Control.PRESET_FULL_RECT)
			video.expand = true
			video.stream = stream
			video.finished.connect(finish)
			video.mouse_filter = Control.MOUSE_FILTER_IGNORE
			root.add_child(video)
			video.play()
			loaded_video = true
	if not loaded_video:
		var poster := TextureRect.new()
		poster.name = control_prefix + "FallbackPoster"
		poster.set_anchors_preset(Control.PRESET_FULL_RECT)
		poster.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		poster.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		poster.mouse_filter = Control.MOUSE_FILTER_IGNORE
		if ResourceLoader.exists(fallback_art):
			poster.texture = load(fallback_art) as Texture2D
		root.add_child(poster)

	# Tap anywhere is the one-finger skip. The two visible controls make replay
	# and continue discoverable without requiring the child to read.
	var tap := Button.new()
	tap.name = control_prefix + "TapAnywhere"
	tap.set_anchors_preset(Control.PRESET_FULL_RECT)
	tap.flat = true
	tap.focus_mode = Control.FOCUS_NONE
	var empty := StyleBoxEmpty.new()
	tap.add_theme_stylebox_override("normal", empty)
	tap.add_theme_stylebox_override("hover", empty)
	tap.add_theme_stylebox_override("pressed", empty)
	tap.pressed.connect(finish)
	root.add_child(tap)
	var stage := StorybookUI.add_stage(root, m.get_viewport().get_visible_rect().size)
	var replay_button := Button.new()
	replay_button.name = control_prefix + "ReplayButton"
	StorybookUI.style_icon_button(replay_button, "@", "selected",
		Vector2(132, 132), "Play the movie again")
	replay_button.position = Vector2(28, 560)
	replay_button.pressed.connect(replay)
	stage.add_child(replay_button)
	var continue_button := Button.new()
	continue_button.name = control_prefix + "ContinueButton"
	StorybookUI.style_icon_button(continue_button, ">>", "gold",
		Vector2(164, 164), "Continue")
	continue_button.position = Vector2(1080, 526)
	continue_button.pressed.connect(finish)
	stage.add_child(continue_button)
	var hold_skip := Button.new()
	hold_skip.name = control_prefix + "HoldToSkipButton"
	StorybookUI.style_icon_button(hold_skip, ">", "secondary",
		Vector2(112, 112), "Hold to skip")
	hold_skip.position = Vector2(28, 24)
	hold_skip.set_meta("hold_seconds", 1.2)
	stage.add_child(hold_skip)
	var skip_timer := Timer.new()
	skip_timer.one_shot = true
	skip_timer.wait_time = 1.2
	skip_timer.timeout.connect(finish)
	stage.add_child(skip_timer)
	hold_skip.button_down.connect(skip_timer.start)
	hold_skip.button_up.connect(skip_timer.stop)
	layer.set_meta("cinematic_video_path", video_path)
	layer.set_meta("cinematic_fallback_art", fallback_art)
	layer.set_meta("cinematic_fallback", not loaded_video)

func replay() -> void:
	if video != null and is_instance_valid(video):
		video.stream_position = 0.0
		video.play()
	elif m.chime != null:
		m.chime.pitch_scale = 1.0
		m.chime.play()

func finish() -> void:
	if not is_active():
		return
	var callback: Callable = finished_callback
	clear()
	if callback.is_valid():
		callback.call()

func clear() -> void:
	if video != null and is_instance_valid(video):
		video.stop()
	video = null
	if layer != null and is_instance_valid(layer):
		layer.queue_free()
	if m.intro_layer == layer:
		m.intro_layer = null
	layer = null
	m.intro_active = false
	m._set_world_controls_enabled(true, "story_cinematic")
