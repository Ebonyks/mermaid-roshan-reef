class_name IntroOverlay
extends RefCounted
# The Day One opener.
#
# OWNER 2026-08-03: the four-panel Princess Huluu storybook intro ("a storm
# swept her down to the sea… find the pearls, open the sky river") is DATED and
# is cut. It set up a premise the game no longer follows. Nothing replaces it
# in the interim: the child now lands straight in the Sky Lagoon, where the
# Day One guide (`day_one_guide.gd`) teaches movement and interaction with the
# playground and the animals instead of with a slideshow.
#
# A movie of Mermaid Roshan and Daddy Mermaid flying to the castle together
# will be added eventually. Drop it at OPENING_VIDEO and it plays on the first
# session with no code change. **While the file is absent there is no overlay
# at all** — no black frame, no poster, no placeholder panel. An opener that
# exists but shows nothing is worse than no opener.
#
# The `_build_intro` / `_intro_next` / `_skip_intro` API is kept because ~40
# probes call `_skip_intro()` defensively at boot. All three are safe no-ops
# when no movie is playing.

const OPENING_VIDEO := "res://assets/cinematics/opening/roshan_daddy_flight.ogv"

var m: ReefMain
var video: VideoStreamPlayer = null

func _init(main: ReefMain) -> void:
	m = main

func _build_intro() -> void:
	m.intro_idx = 0
	if DisplayServer.get_name() == "headless":
		return   # a headless probe has no video decoder and needs no opener
	if not ResourceLoader.exists(OPENING_VIDEO):
		return   # the flight movie has not been delivered yet — go straight in
	var stream: VideoStream = load(OPENING_VIDEO) as VideoStream
	if stream == null:
		return
	m.intro_active = true
	m.intro_layer = CanvasLayer.new()
	m.intro_layer.name = "OpeningFlightLayer"
	m.intro_layer.layer = 25
	m.intro_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.intro_layer)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.intro_layer.add_child(root)
	# Letterbox in the boot splash's own colour so the movie's native aspect is
	# never stretched or cropped to fill the phone.
	var letterbox := ColorRect.new()
	letterbox.set_anchors_preset(Control.PRESET_FULL_RECT)
	letterbox.color = BootSplashOverlay.LETTERBOX_COLOR
	letterbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(letterbox)
	video = VideoStreamPlayer.new()
	video.name = "OpeningFlightVideo"
	video.set_anchors_preset(Control.PRESET_FULL_RECT)
	video.expand = false               # keep the delivered edit's framing
	video.stream = stream
	video.mouse_filter = Control.MOUSE_FILTER_IGNORE
	video.finished.connect(_skip_intro)
	root.add_child(video)
	video.play()
	# One finger, one rule: tap anywhere ends the movie. There is no page
	# furniture to learn, because there are no pages.
	var tap := Button.new()
	tap.name = "IntroTapAnywhere"
	tap.set_anchors_preset(Control.PRESET_FULL_RECT)
	tap.flat = true
	tap.focus_mode = Control.FOCUS_NONE
	var clear := StyleBoxEmpty.new()
	tap.add_theme_stylebox_override("normal", clear)
	tap.add_theme_stylebox_override("hover", clear)
	tap.add_theme_stylebox_override("pressed", clear)
	tap.pressed.connect(_skip_intro)
	root.add_child(tap)

func _intro_repeat() -> void:
	if video != null and is_instance_valid(video):
		video.stream_position = 0.0
		video.play()

func _intro_next() -> void:
	_skip_intro()

func _skip_intro() -> void:
	if video != null and is_instance_valid(video):
		video.stop()
	video = null
	m.intro_active = false
	if m.intro_layer != null and is_instance_valid(m.intro_layer):
		m.intro_layer.queue_free()
	m.intro_layer = null
