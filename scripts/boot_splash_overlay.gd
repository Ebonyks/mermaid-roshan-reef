class_name BootSplashOverlay
extends RefCounted

# The engine boot splash and this first-frame handoff use the same artwork and
# aspect policy. The overlay starts opaque before ReefMain builds the world,
# then fades only after the first rendered frame can replace the engine splash.
const SPLASH_TEXTURE: Texture2D = preload("res://assets/ui/boot_splash_mermaid_roshan.png")
const LETTERBOX_COLOR := Color("188ed6")
const HANDOFF_SECONDS := 0.45

static func show(main: ReefMain) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var layer := CanvasLayer.new()
	layer.name = "BootSplashHandoff"
	layer.layer = 100
	layer.process_mode = Node.PROCESS_MODE_ALWAYS
	main.add_child(layer)
	var root := Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(root)
	var background := ColorRect.new()
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.color = LETTERBOX_COLOR
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(background)
	var art := TextureRect.new()
	art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	art.texture = SPLASH_TEXTURE
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(art)
	var tween := layer.create_tween()
	tween.tween_property(root, "modulate:a", 0.0, HANDOFF_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_callback(layer.queue_free)
