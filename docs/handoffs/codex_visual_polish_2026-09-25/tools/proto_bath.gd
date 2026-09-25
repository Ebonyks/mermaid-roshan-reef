extends SceneTree
## Prototype: warm, breathing light in the Bubble Bath. Scratch only; injects
## effects into the running game's real bathroom and records before/after.

const DIR := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a128eb5f-c316-4162-83d1-fbdbf9c3f497/scratchpad/aesthetics/proto"
var P: Script
var main: ReefMain


func _capture(folder: String, count: int, fps: float) -> void:
	DirAccess.make_dir_recursive_absolute(DIR + "/" + folder)
	for i in range(count):
		await RenderingServer.frame_post_draw
		var img := get_root().get_texture().get_image()
		img.resize(1280, int(1280.0 * img.get_height() / img.get_width()), Image.INTERPOLATE_BILINEAR)
		img.save_jpg(DIR + "/" + folder + "/f%03d.jpg" % i, 0.92)
		await create_timer(1.0 / fps).timeout
	print("CAPTURED ", folder)


func _init() -> void:
	P = load(DIR + "/proto_common.gd")
	var path := ProjectSettings.globalize_path("user://aes_bath.json")
	P.finished_day_one_save(path)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, path)
	get_root().add_child(main)
	for _i in range(20):
		await process_frame
	main._start_menu_ref()._dismiss_menu()
	main._launch_from_start_menu(false)
	await create_timer(1.0).timeout
	main._enter_castle_interior_now()
	await create_timer(1.0).timeout
	main._castle_rooms_ref().show_room("bubble_bath", false)
	await create_timer(9.0).timeout
	await _capture("bath_before", 36, 12.0)
	var world: Node2D = main.castle_room_world_root
	# 1. Wall lamps breathe with a warm glow (lamp centres measured from the art).
	var lamps := [Vector2(580, 113), Vector2(807, 111), Vector2(118, 142), Vector2(391, 150), Vector2(535, 154)]
	var phase := 0.0
	for lamp: Vector2 in lamps:
		var glow: Sprite2D = P.glow_card(lamp, 70.0, Color(1.0, 0.80, 0.52), 0.34, phase)
		glow.z_index = 2
		world.add_child(glow)
		phase += 1.7
	# 2. Soft light shafts and bubbles in the two ocean windows.
	var rays := Sprite2D.new()
	rays.texture = P.file_texture(DIR + "/mask_bath_windows.png")
	rays.position = Vector2(640, 360)
	rays.z_index = 2
	var rm: ShaderMaterial = P.shader(P.RAYS_SHADER)
	rm.set_shader_parameter("strength", 0.34)
	rays.material = rm
	world.add_child(rays)
	for rect: Rect2 in [Rect2(174, 26, 193, 259), Rect2(990, 32, 143, 242)]:
		var bubbles := CPUParticles2D.new()
		bubbles.texture = P.soft_dot(24, true)
		bubbles.position = rect.get_center() + Vector2(0, rect.size.y * 0.25)
		bubbles.z_index = 3
		bubbles.amount = 9
		bubbles.lifetime = 4.5
		bubbles.preprocess = 4.5
		bubbles.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
		bubbles.emission_rect_extents = Vector2(rect.size.x * 0.35, rect.size.y * 0.2)
		bubbles.direction = Vector2(0, -1)
		bubbles.spread = 10.0
		bubbles.initial_velocity_min = 12.0
		bubbles.initial_velocity_max = 22.0
		bubbles.scale_amount_min = 0.25
		bubbles.scale_amount_max = 0.55
		bubbles.color = Color(0.85, 0.97, 1.0, 0.5)
		world.add_child(bubbles)
	# 3. A gentle light beam from the left window across the floor, with motes.
	var beam := Sprite2D.new()
	beam.texture = P.soft_dot(8, false)
	beam.position = Vector2(420, 420)
	beam.rotation = deg_to_rad(-28.0)
	beam.scale = Vector2(260.0 / 8.0, 620.0 / 8.0)
	beam.z_index = 4
	beam.material = P.shader(P.BEAM_SHADER)
	world.add_child(beam)
	var motes := CPUParticles2D.new()
	motes.texture = P.soft_dot(12, false)
	motes.position = Vector2(430, 420)
	motes.z_index = 5
	motes.amount = 22
	motes.lifetime = 6.0
	motes.preprocess = 6.0
	motes.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	motes.emission_rect_extents = Vector2(160, 220)
	motes.direction = Vector2(1, -0.3)
	motes.spread = 180.0
	motes.gravity = Vector2(0, -2)
	motes.initial_velocity_min = 3.0
	motes.initial_velocity_max = 9.0
	motes.scale_amount_min = 0.15
	motes.scale_amount_max = 0.35
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 0.95, 0.85, 0))
	ramp.set_color(1, Color(1, 0.95, 0.85, 0))
	ramp.add_point(0.5, Color(1, 0.95, 0.85, 0.7))
	motes.color_ramp = ramp
	world.add_child(motes)
	# 4. Storybook vignette.
	var vl := CanvasLayer.new()
	vl.layer = 15
	var vig := ColorRect.new()
	vig.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vig.material = P.shader(P.VIGNETTE_SHADER)
	vl.add_child(vig)
	main.add_child(vl)
	await create_timer(1.5).timeout
	await _capture("bath_after", 48, 12.0)
	P.remove_save(path)
	quit(0)
