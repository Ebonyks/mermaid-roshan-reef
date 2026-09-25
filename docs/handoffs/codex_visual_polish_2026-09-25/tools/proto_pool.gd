extends SceneTree
## Prototype: the living Mermaid Pool. Scratch only; injects effects into the
## running game's real pool room and records before/after frames.

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
	var path := ProjectSettings.globalize_path("user://aes_pool.json")
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
	main._castle_rooms_ref().show_room("mermaid_pool", false)
	await create_timer(9.0).timeout
	if main.hud_msg != null:
		main.hud_msg.visible = false
	await _capture("pool_before", 36, 12.0)
	var world: Node2D = main.castle_room_world_root
	# 1. Rippling, caustic-lit pool water, masked to the painted water.
	var water := Sprite2D.new()
	water.name = "ProtoWater"
	water.texture = P.file_texture(DIR + "/mask_pool.png")
	water.position = Vector2(640, 360)
	water.z_index = 1
	var wm: ShaderMaterial = P.shader(P.WATER_SHADER)
	wm.set_shader_parameter("ripple_tex", load("res://assets/terrain/up_water_nrm.jpg"))
	wm.set_shader_parameter("caustics_tex", load("res://assets/terrain/caustics.png"))
	wm.set_shader_parameter("caustic_strength", 0.32)
	water.material = wm
	world.add_child(water)
	# 2. Light rays and rising bubbles in the ocean window.
	var rays := Sprite2D.new()
	rays.name = "ProtoWindowRays"
	rays.texture = P.file_texture(DIR + "/mask_window.png")
	rays.position = Vector2(640, 360)
	rays.z_index = 2
	rays.material = P.shader(P.RAYS_SHADER)
	world.add_child(rays)
	var bubbles := CPUParticles2D.new()
	bubbles.name = "ProtoWindowBubbles"
	bubbles.texture = P.soft_dot(24, true)
	bubbles.position = Vector2(780, 200)
	bubbles.z_index = 3
	bubbles.amount = 14
	bubbles.lifetime = 4.0
	bubbles.preprocess = 4.0
	bubbles.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	bubbles.emission_rect_extents = Vector2(95, 40)
	bubbles.direction = Vector2(0, -1)
	bubbles.spread = 12.0
	bubbles.gravity = Vector2(0, -6)
	bubbles.initial_velocity_min = 14.0
	bubbles.initial_velocity_max = 26.0
	bubbles.scale_amount_min = 0.25
	bubbles.scale_amount_max = 0.6
	bubbles.color = Color(0.85, 0.97, 1.0, 0.55)
	world.add_child(bubbles)
	# 3. Flowing highlights on the painted waterfall and seahorse streams.
	var fall: Sprite2D = P.find_sprite(world, "Animated_waterfall")
	if fall != null:
		var flow := Sprite2D.new()
		flow.texture = load("res://assets/flats/castle/rooms/room_mermaid_pool_item_waterfall.png")
		flow.position = fall.position + Vector2(8, 4)
		flow.scale = Vector2.ONE * 1.25
		flow.z_index = fall.z_index + 1
		var fm: ShaderMaterial = P.shader(P.FLOW_SHADER)
		fm.set_shader_parameter("noise_tex", load("res://assets/terrain/caustics.png"))
		fm.set_shader_parameter("box", Vector4(0.30, 0.04, 0.97, 0.80))
		fm.set_shader_parameter("dir", Vector2(0, -1))
		fm.set_shader_parameter("speed", 0.55)
		fm.set_shader_parameter("strength", 0.42)
		flow.material = fm
		fall.get_parent().add_child(flow)
		var foam := CPUParticles2D.new()
		foam.texture = P.soft_dot(16, false)
		foam.position = fall.position + Vector2(20, 92)
		foam.z_index = fall.z_index + 2
		foam.amount = 18
		foam.lifetime = 0.9
		foam.preprocess = 1.0
		foam.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
		foam.emission_rect_extents = Vector2(58, 6)
		foam.direction = Vector2(0, -1)
		foam.spread = 55.0
		foam.gravity = Vector2(0, 140)
		foam.initial_velocity_min = 25.0
		foam.initial_velocity_max = 55.0
		foam.scale_amount_min = 0.35
		foam.scale_amount_max = 0.8
		foam.color = Color(1, 1, 1, 0.75)
		fall.get_parent().add_child(foam)
		print("PROTO waterfall at ", fall.position)
	var horse: Sprite2D = P.find_sprite(world, "Animated_seahorse_fountain")
	if horse != null:
		var stream := Sprite2D.new()
		stream.texture = load("res://assets/flats/castle/rooms/room_mermaid_pool_item_seahorse_fountain.png")
		stream.position = horse.position + Vector2(-6, 6)
		stream.scale = Vector2.ONE * 1.25
		stream.z_index = horse.z_index + 1
		var sm: ShaderMaterial = P.shader(P.FLOW_SHADER)
		sm.set_shader_parameter("noise_tex", load("res://assets/terrain/caustics.png"))
		sm.set_shader_parameter("box", Vector4(0.02, 0.36, 0.46, 0.96))
		sm.set_shader_parameter("dir", Vector2(0.45, -1.0))
		sm.set_shader_parameter("speed", 0.8)
		sm.set_shader_parameter("strength", 0.38)
		stream.material = sm
		horse.get_parent().add_child(stream)
		var drops := CPUParticles2D.new()
		drops.texture = P.soft_dot(14, false)
		drops.position = horse.position + Vector2(-92, 96)
		drops.z_index = horse.z_index + 2
		drops.amount = 16
		drops.lifetime = 0.7
		drops.preprocess = 1.0
		drops.direction = Vector2(-0.3, -1)
		drops.spread = 40.0
		drops.gravity = Vector2(0, 260)
		drops.initial_velocity_min = 40.0
		drops.initial_velocity_max = 80.0
		drops.scale_amount_min = 0.3
		drops.scale_amount_max = 0.7
		drops.color = Color(0.92, 1.0, 1.0, 0.8)
		horse.get_parent().add_child(drops)
		print("PROTO seahorse at ", horse.position)
	# 4. Slow sun glints on the water.
	var glints := CPUParticles2D.new()
	glints.name = "ProtoGlints"
	glints.texture = P.sparkle_texture(32)
	glints.position = Vector2(640, 450)
	glints.z_index = 4
	glints.amount = 12
	glints.lifetime = 1.1
	glints.preprocess = 1.1
	glints.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	glints.emission_rect_extents = Vector2(520, 120)
	glints.gravity = Vector2.ZERO
	glints.initial_velocity_min = 0.0
	glints.initial_velocity_max = 0.0
	glints.angular_velocity_min = -40.0
	glints.angular_velocity_max = 40.0
	var star_size: float = maxf(1.0, (glints.texture as Texture2D).get_size().x)
	glints.scale_amount_min = 10.0 / star_size
	glints.scale_amount_max = 22.0 / star_size
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0))
	ramp.set_color(1, Color(1, 1, 1, 0))
	ramp.add_point(0.5, Color(1, 1, 1, 0.9))
	glints.color_ramp = ramp
	world.add_child(glints)
	# 5. Storybook vignette: lavender, above the room, below the UI.
	var vl := CanvasLayer.new()
	vl.layer = 15
	var vig := ColorRect.new()
	vig.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vig.material = P.shader(P.VIGNETTE_SHADER)
	vl.add_child(vig)
	main.add_child(vl)
	await create_timer(1.5).timeout
	await _capture("pool_after", 48, 12.0)
	P.remove_save(path)
	quit(0)
