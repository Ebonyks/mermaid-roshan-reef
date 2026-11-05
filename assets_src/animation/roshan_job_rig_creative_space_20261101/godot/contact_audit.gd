extends SceneTree

var viewport: SubViewport
var scene: Node2D

func _initialize() -> void:
	run.call_deferred()

func picture() -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	return viewport.get_texture().get_image()

func texture_alpha_at(sprite: Sprite2D, world: Vector2) -> float:
	var p: Vector2 = sprite.to_local(world)
	if sprite.centered:
		p += sprite.texture.get_size() * 0.5
	var image: Image = sprite.texture.get_image()
	if not Rect2(Vector2.ZERO,Vector2(image.get_size())).has_point(p):
		return 0.0
	return image.get_pixel(int(p.x),int(p.y)).a

func save_json(path: String, value: Variant) -> void:
	var file: FileAccess = FileAccess.open(path,FileAccess.WRITE)
	file.store_string(JSON.stringify(value))

func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	viewport = SubViewport.new()
	viewport.size = Vector2i(1024,1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	scene = load("res://study.tscn").instantiate()
	root.add_child(scene)
	scene.automatic = false
	scene.actor.reparent(viewport)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var rows: Array = []
	var controls: Dictionary = {}
	var failures: Array = []
	for theme: String in ["painter","astronaut"]:
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		var clip: String = "paint_banner" if theme == "painter" else "turn_valve"
		var folder: String = out.path_join(theme).path_join(clip)
		DirAccess.make_dir_recursive_absolute(folder)
		var samples: Array = []
		for index: int in range(151):
			var t: float = index / 30.0
			scene.set_pose(clip,t)
			var row: Dictionary = scene.state_record()
			row.merge({"theme":theme,"clip":clip,"time":t,"frame":index})
			if scene.contact_active:
				var error: float
				var alpha: float
				if theme == "painter":
					var grasp: Vector2 = scene.held_brush.to_global(Vector2(128.0,123.2))
					error = grasp.distance_to(scene.grip.global_position)
					var tip: Vector2 = scene.held_brush.to_global(Vector2(36.8,30.4))
					alpha = texture_alpha_at(scene.painting,tip)
				else:
					error = float(scene.contact_error)
					alpha = texture_alpha_at(scene.valve,scene.grip.global_position)
				rows.append({"theme":theme,"frame":index,"time":t,"binding_error_px":error,"target_alpha":alpha})
				if error > 3.0 or alpha <= 0.75:
					failures.append(rows[-1])
			# Isolate the actor from declared fixed fixtures for the unchanged one-figure seam floor.
			scene.object_root.visible = false
			var isolated: Image = await picture()
			isolated.save_png(folder.path_join("%04d.png" % index))
			scene.object_root.visible = true
			samples.append(row)
		var file: FileAccess = FileAccess.open(out.path_join(theme).path_join("samples.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify(samples))
		print("CONTACT_CAPTURE ",theme)
	# Retain exact image evidence for the faulted bindings.
	scene.set_parts({"head":"painter","body":"painter","tail":"painter"})
	scene.set_pose("paint_banner",1.5)
	var normal: Image = await picture()
	scene.held_brush.position += Vector2(25.0,0.0)
	var slip: Image = await picture()
	var grip_error: float = scene.held_brush.to_global(Vector2(128,123.2)).distance_to(scene.grip.global_position)
	controls["grip_slip"] = grip_error > 3.0 and normal.get_data() != slip.get_data()
	slip.save_png(out.path_join("negative_grip_slip.png"))
	scene.held_brush.position -= Vector2(25.0,0.0)
	scene.set_parts({"head":"astronaut","body":"astronaut","tail":"astronaut"})
	scene.set_pose("turn_valve",1.5)
	normal = await picture()
	scene.valve.position += Vector2(25,0)
	var moved: Image = await picture()
	var actual_palm: Vector2 = scene.actor.to_local(scene.grip.global_position)
	controls["fixture_contact_slip"] = absf(actual_palm.distance_to(scene.valve.position)-32.0)>3.0 and moved.get_data()!=normal.get_data()
	moved.save_png(out.path_join("negative_fixture_slip.png"))
	scene.valve.position -= Vector2(25,0)
	var before: String = JSON.stringify(scene.state_record())
	controls["unavailable_view_rejected_without_pop"] = not scene.bind_view("quarter_right") and not scene.bind_view("profile_right") and scene.bind_view("front") and before == JSON.stringify(scene.state_record())
	# Three independent original-clothing reinsertions must alter an actual render.
	scene.set_parts({"head":"painter","body":"painter","tail":"painter"})
	scene.set_pose("arm_bend",0.0)
	normal = await picture()
	for name: String in ["old_sleeve","old_bodice","old_tail"]:
		var slot: String = "tail" if name=="old_tail" else "body"
		var patch: Image = scene.garment_textures["painter_"+slot].get_image()
		var box: Rect2i = Rect2i(451,346,20,22) if name=="old_sleeve" else (Rect2i(515,370,64,68) if name=="old_bodice" else Rect2i(642,581,12,64))
		patch.blit_rect(scene.original_body_texture.get_image(),box,box.position)
		scene.clothing_material.set_shader_parameter(slot+"_paint",ImageTexture.create_from_image(patch))
		var faulty: Image = await picture()
		controls[name+"_reinsertion"] = faulty.get_data()!=normal.get_data()
		faulty.save_png(out.path_join("negative_"+name+".png"))
		scene.set_parts({"head":"painter","body":"painter","tail":"painter"})
	var passed: bool = failures.is_empty()
	for value: bool in controls.values():
		passed = passed and value
	save_json(out.path_join("contact_audit.json"),{"pass":passed,"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"rows":rows,"failures":failures,"negative_controls":controls,"tolerances":{"binding_px":3.0,"contact_alpha":0.75},"limits":"Front-view source prototype. Alpha/contact coordinates cannot accept artistic grasp, palm pressure, natural motion, unsupported views, device or child/owner review."})
	print("CONTACT_AUDIT ",passed," contact_frames=",rows.size()," failures=",failures.size())
	quit(0 if passed else 1)
