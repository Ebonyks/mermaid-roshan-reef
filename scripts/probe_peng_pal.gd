extends SceneTree
# PENGUIN PAL PROBE — verifies the caught baby penguin spawns in the reef,
# follows Roshan (sprint when lagging, waddle when close), faces his motion,
# and wears his new beak. Windowed run:
#   Godot_console.exe --path . --resolution 1280x720 -s res://scripts/probe_peng_pal.gd
var main: Node3D
var cam: Camera3D

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	get_root().get_viewport().get_texture().get_image().save_png(
		ProjectSettings.globalize_path("res://tools/out/penguin_probe/") + name)

func _frame_pal(back: float, side: float) -> void:
	if main.peng_pal == null:
		return
	var pp: Node3D = main.peng_pal
	var to_pl: Vector3 = (main.player.position - pp.position)
	to_pl.y = 0.0
	var dir: Vector3 = to_pl.normalized() if to_pl.length() > 0.1 else Vector3.FORWARD
	cam.position = pp.position + dir * back + Vector3(0, 2.5, 0) + dir.cross(Vector3.UP) * side
	cam.look_at(pp.position + Vector3(0, 0.8, 0))

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://tools/out/penguin_probe"))
	cam = Camera3D.new()
	get_root().add_child(cam)
	cam.current = true
	# earn the sticker (as if she caught him on the slide)
	main.stickers["penguin"] = true
	# let him spawn + settle at her side
	for i in range(150):
		await process_frame
	var pp = main.peng_pal
	print("PAL|spawned=", pp != null and is_instance_valid(pp))
	if pp == null:
		quit(); return
	var ap: AnimationPlayer = main._find_anim(pp)
	print("PAL|idle_clip=", "none" if ap == null else ap.current_animation, " d=%.1f" % pp.position.distance_to(main.player.position))
	await _frame_pal(5.0, 2.0)
	await _shot("pal_idle.png")
	# warp Roshan 40m away -> he should SPRINT after her
	main.player.position += Vector3(28.0, 4.0, 24.0)
	for i in range(30):
		await process_frame
	print("PAL|lag_clip=", "none" if ap == null else ap.current_animation, " d=%.1f" % pp.position.distance_to(main.player.position))
	await _frame_pal(7.0, 3.0)
	await _shot("pal_sprint.png")
	# let him catch up and settle
	var t := 0.0
	while t < 12.0:
		await process_frame
		t += 1.0 / 60.0
	var d_end: float = pp.position.distance_to(main.player.position)
	print("PAL|settled_clip=", "none" if ap == null else ap.current_animation, " d=%.1f" % d_end, " visible=", pp.visible)
	await _frame_pal(4.5, 1.5)
	await _shot("pal_close.png")
	print("PAL|done caught_up=", d_end < 9.0)
	quit()
