extends SceneTree
# PENGUIN RACE VISUAL PROBE — verifies the chase-mode baby penguin faces
# down-slope, plays the sprint clip, and kicks a snow-spray trail.
# Run windowed (screenshots need a real viewport):
#   Godot_console.exe --path . --resolution 1280x720 -s res://scripts/probe_penguin_face.gd
var main: Node3D
var cam: Camera3D

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var fr := {"fname": "PenguinProbe", "game": "slide", "theme": "ice", "mode": "chase", "won": true, "cool": 0.0}
	main._start_game(fr)
	await process_frame
	cam = Camera3D.new()
	get_root().add_child(cam)
	cam.current = true
	var outdir: String = ProjectSettings.globalize_path("res://tools/out/penguin_probe")
	DirAccess.make_dir_recursive_absolute(outdir)
	# shots: early race / mid race / late (panic bursts live late in the run)
	var stamps := [1.0, 4.0, 8.0, 11.0]
	var t := 0.0
	var shot := 0
	while main.game == "slide" and t < 14.0:
		await process_frame
		t += 1.0 / 60.0
		var pn = main.g.get("peng_node")
		if pn == null or not is_instance_valid(pn):
			continue
		var pnd := pn as Node3D
		# front-quarter view of the penguin, looking back up the slide at him
		var s_p: float = minf(float(main.g["s"]) + 22.0, float(main.g["total"]))
		var samp: Array = main._slide_sample(s_p)
		var tang: Vector3 = samp[1]
		cam.position = pnd.position + tang * 11.0 + Vector3(0, 4.0, 0) + (samp[2] as Vector3) * 5.0
		cam.look_at(pnd.position + Vector3(0, 1.0, 0))
		if shot < stamps.size() and t >= float(stamps[shot]):
			await RenderingServer.frame_post_draw
			var img := get_root().get_viewport().get_texture().get_image()
			img.save_png(outdir + "/shot_%d.png" % shot)
			var ap: AnimationPlayer = main._find_anim(pnd)
			var clip: String = "NO_ANIMPLAYER" if ap == null else ap.current_animation
			print("PROBE|shot=%d t=%.1f clip=%s speed=%.2f yaw=%.2f rot=%s burst=%.1f gap_x=%.1f" %
				[shot, t, clip, (0.0 if ap == null else ap.speed_scale), pnd.rotation.y,
				str(pnd.rotation), float(main.g.get("burst", 0.0)),
				absf(float(main.g.get("peng_x", 0.0)) - float(main.g.get("x", 0.0)))])
			if ap != null:
				print("PROBE|clips=", ap.get_animation_list())
			shot += 1
	print("PROBE|done shots=", shot, " game=", main.game)
	quit()
