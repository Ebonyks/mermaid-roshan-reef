extends SceneTree
## Renders every animation frame of res://rig_wave.tscn by seeking the AnimationPlayer, then saves
## the viewport. Needs a display (e.g. xvfb-run) and a rendering driver.
## godot --path run1_godot --rendering-method gl_compatibility -s res://tools/render_frames.gd -- <out_dir>


func _initialize() -> void:
	_run()


func _run() -> void:
	var args := OS.get_cmdline_user_args()
	var out_dir: String = args[0] if args.size() > 0 else ProjectSettings.globalize_path("res://").path_join("../run1/frames")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: Node = load("res://rig_wave.tscn").instantiate()
	root.add_child(scene)
	var ap: AnimationPlayer = scene.get_node("AnimationPlayer")
	# Manual callback mode: the player never advances on its own, so frame i shows exactly key i.
	ap.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	ap.play("wave")
	var fore: Node2D = scene.get_node("Skeleton/Root/Torso/UpperArm/Fore")
	var anim := ap.get_animation("wave")
	var track := anim.find_track(NodePath("Skeleton/Root/Torso/UpperArm/Fore:rotation"), Animation.TYPE_VALUE)
	var count := int(round(anim.length * 24.0))
	var worst := 0.0
	for i in range(count):
		ap.seek(i / 24.0, true)
		await process_frame
		await RenderingServer.frame_post_draw
		worst = max(worst, absf(fore.rotation - float(anim.track_get_key_value(track, i))))
		root.get_texture().get_image().save_png(out_dir.path_join("%04d.png" % i))
	print("RENDER_OK frames=%d max_key_error_rad=%.6f dir=%s" % [count, worst, out_dir])
	quit(0)
