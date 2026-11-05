extends SceneTree
## Independent old-clothing contamination test on actual Mobile renders.
func _initialize() -> void:
	run.call_deferred()

func capture(viewport: SubViewport) -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	return viewport.get_texture().get_image()

func changed(a: Image, b: Image) -> int:
	var av: PackedByteArray = a.get_data()
	var bv: PackedByteArray = b.get_data()
	if av == bv:
		return 0
	var count: int = 0
	for i: int in range(0, av.size(), 4):
		if av[i] != bv[i] or av[i+1] != bv[i+1] or av[i+2] != bv[i+2] or av[i+3] != bv[i+3]:
			count += 1
	return count

func run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var out: String = args[0]
	DirAccess.make_dir_recursive_absolute(out)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.automatic = false
	var viewport: SubViewport = SubViewport.new()
	viewport.size = Vector2i(1024, 1024)
	viewport.transparent_bg = true
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	scene.actor.reparent(viewport)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var original: Texture2D = scene.body.texture
	var poisoned: Image = original.get_image()
	# Independently annotated certain old-clothing regions: both sleeve puffs,
	# original pink shirt, both tail side bands, and distal scale/fin junction.
	var boxes: Array[Rect2i] = [Rect2i(451,346,20,22), Rect2i(619,342,12,25), Rect2i(515,370,64,68), Rect2i(487,510,14,64), Rect2i(642,581,12,64), Rect2i(473,795,40,20)]
	for box: Rect2i in boxes:
		for y: int in range(box.position.y, box.end.y):
			for x: int in range(box.position.x, box.end.x):
				var c: Color = poisoned.get_pixel(x,y)
				if c.a > 0.9 and c.b > c.r * 0.84 and c.b > c.g * 1.035:
					poisoned.set_pixel(x,y,Color(0.0,1.0,0.0,c.a))
	var poison_texture: ImageTexture = ImageTexture.create_from_image(poisoned)
	var rows: Array = []
	var failures: Array = []
	for theme: String in ["ballet", "magician"]:
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		var folder: String = out.get_base_dir().path_join("render_"+theme+"_v3")
		var records: Array = JSON.parse_string(FileAccess.get_file_as_string(folder.path_join("samples.json")))
		for record: Dictionary in records:
			scene.set_pose(String(record.clip), float(record.time))
			scene.body.texture = original
			var normal: Image = await capture(viewport)
			var frozen: Image = Image.load_from_file(folder.path_join(String(record.clip)).path_join("%04d.png" % int(record.frame)))
			var reproduction_error: int = changed(normal, frozen)
			scene.body.texture = poison_texture
			var faulty: Image = await capture(viewport)
			var leak: int = changed(normal, faulty)
			if leak > 0 or reproduction_error > 0:
				failures.append({"theme":theme,"clip":record.clip,"frame":record.frame,"base_leak_pixels":leak,"fresh_capture_mismatch_pixels":reproduction_error})
			rows.append({"theme":theme,"clip":record.clip,"frame":record.frame,"base_leak_pixels":leak,"fresh_capture_mismatch_pixels":reproduction_error})
			scene.body.texture = original
	# Reinsert actual original outfit pieces into the selected skin. The same
	# exact comparison must fail on each independent contamination, not just pass
	# the normal implementation. These are deliberately faulty images.
	scene.set_parts({"head":"ballet","body":"ballet","tail":"ballet"})
	scene.set_pose("arm_bend",0.0)
	var reference: Image = await capture(viewport)
	var controls: Dictionary = {}
	for name: String in ["old_left_sleeve", "old_pink_bodice", "old_tail_band"]:
		var slot: String = "tail" if name == "old_tail_band" else "body"
		var texture: Texture2D = scene.garment_textures["ballet_"+slot]
		var image: Image = texture.get_image()
		var box: Rect2i = Rect2i(451,346,20,22) if name == "old_left_sleeve" else (Rect2i(515,370,64,68) if name == "old_pink_bodice" else Rect2i(642,581,12,64))
		image.blit_rect(original.get_image(),box,box.position)
		scene.clothing_material.set_shader_parameter(slot+"_paint",ImageTexture.create_from_image(image))
		var bad: Image = await capture(viewport)
		var pixels: int = changed(reference,bad)
		controls[name] = {"detected":pixels > 0,"changed_pixels":pixels}
		bad.save_png(out.path_join("negative_"+name+".png"))
		scene.set_parts({"head":"ballet","body":"ballet","tail":"ballet"})
	var pass_all: bool = failures.is_empty()
	for name: String in controls:
		pass_all = pass_all and bool(controls[name].detected)
	var report: Dictionary = {"pass":pass_all,"engine":Engine.get_version_info(),"frames":rows.size(),"old_clothing_poison_regions":boxes.map(func(b: Rect2i) -> Array: return [b.position.x,b.position.y,b.size.x,b.size.y]),"rows":rows,"failures":failures,"negative_controls":controls,"limits":"Exact annotated old-clothing contamination and frozen-render reproduction. Numerical checks do not establish artistic, full-speed human, device, child or owner acceptance."}
	var file: FileAccess = FileAccess.open(out.path_join("replacement_audit.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report))
	file.close()
	print("REPLACEMENT_AUDIT ",pass_all," frames=",rows.size()," failures=",failures.size())
	quit(0 if pass_all else 1)
