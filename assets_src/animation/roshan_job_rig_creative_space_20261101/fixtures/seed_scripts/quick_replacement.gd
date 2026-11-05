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
	var original: Texture2D = scene.original_body_texture
	var anatomy: Texture2D = scene.garment_textures["anatomy"]
	var original_data: PackedByteArray = original.get_image().get_data()
	var anatomy_image: Image = anatomy.get_image()
	var anatomy_data: PackedByteArray = anatomy_image.get_data()
	var domains: PackedByteArray = scene.garment_textures["ownership"].get_image().get_data()
	var removed: int = 0
	var undeleted: int = 0
	for i: int in range(0, original_data.size(), 4):
		if (domains[i] > 128 or domains[i+1] > 128) and original_data[i+3] > 0:
			removed += 1
			if anatomy_data[i+3] != 0:
				undeleted += 1
	var survey_undeleted: int = 0
	var poisoned_pixels: int = 0
	var poisoned: Image = original.get_image()
	# Independently annotated certain old-clothing regions: both sleeve puffs,
	# original pink shirt, both tail side bands, and distal scale/fin junction.
	var boxes: Array[Rect2i] = [Rect2i(451,346,20,22), Rect2i(619,342,12,25), Rect2i(515,370,64,68), Rect2i(487,510,14,64), Rect2i(642,581,12,64), Rect2i(473,795,40,20)]
	for box: Rect2i in boxes:
		for y: int in range(box.position.y, box.end.y):
			for x: int in range(box.position.x, box.end.x):
				var c: Color = poisoned.get_pixel(x,y)
				if c.a > 0.9 and c.b > c.r * 0.84 and c.b > c.g * 1.035:
					poisoned_pixels += 1
					if anatomy_image.get_pixel(x,y).a > 0.0:
						survey_undeleted += 1
					poisoned.set_pixel(x,y,Color(0.0,1.0,0.0,c.a))
	var poison_texture: ImageTexture = ImageTexture.create_from_image(poisoned)
	var rows: Array = []
	var failures: Array = []
	for theme: String in ["ballet", "magician"]:
		scene.set_parts({"head":theme,"body":theme,"tail":theme})
		var folder: String = out.get_base_dir().path_join("render_"+theme+"_v8")
		var records: Array = []
		for clip: String in ["arm_bend", "blink", "tail_bend"]:
			for time: float in [0.0,1.5]:
				records.append({"clip":clip,"time":time,"frame":int(time*30)})
		for record: Dictionary in records:
			scene.set_pose(String(record.clip), float(record.time))
			scene.original_body_texture = original
			scene.set_parts({"head":theme,"body":theme,"tail":theme})
			var normal: Image = await capture(viewport)
			normal.save_png(out.path_join("%s_%s_%04d.png" % [theme,String(record.clip),int(record.frame)]))
			if String(record.clip) == "arm_bend" and int(record.frame) == 0:
				normal.save_png(out.path_join(theme+"_neutral.png"))
			var frozen: Image = normal.duplicate()
			var reproduction_error: int = changed(normal, frozen)
			scene.original_body_texture = poison_texture
			scene.set_parts({"head":theme,"body":theme,"tail":theme})
			var faulty: Image = await capture(viewport)
			var leak: int = changed(normal, faulty)
			if leak > 0 or reproduction_error > 0:
				failures.append({"theme":theme,"clip":record.clip,"frame":record.frame,"base_leak_pixels":leak,"fresh_capture_mismatch_pixels":reproduction_error})
			rows.append({"theme":theme,"clip":record.clip,"frame":record.frame,"base_leak_pixels":leak,"fresh_capture_mismatch_pixels":reproduction_error})
			scene.original_body_texture = original
			scene.set_parts({"head":theme,"body":theme,"tail":theme})
	# Reinsert actual original outfit pieces into the selected skin. The same
	# exact comparison must fail on each independent contamination, not just pass
	# the normal implementation. These are deliberately faulty images.
	scene.set_parts({"head":"ballet","body":"ballet","tail":"ballet"})
	scene.set_pose("arm_bend",0.0)
	var reference: Image = await capture(viewport)
	var controls: Dictionary = {}
	scene.body.texture = original
	var old_underlay: Image = await capture(viewport)
	var underlay_pixels: int = changed(reference,old_underlay)
	controls["old_outfit_underlay"] = {"detected":underlay_pixels > 0,"changed_pixels":underlay_pixels}
	old_underlay.save_png(out.path_join("negative_old_outfit_underlay.png"))
	scene.set_parts({"head":"ballet","body":"ballet","tail":"ballet"})
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
	var pass_all: bool = failures.is_empty() and removed > 0 and undeleted == 0 and survey_undeleted == 0 and poisoned_pixels > 0
	for name: String in controls:
		pass_all = pass_all and bool(controls[name].detected)
	var report: Dictionary = {"pass":pass_all,"engine":Engine.get_version_info(),"frames":rows.size(),"original_clothing_pixels_removed":removed,"undeleted_domain_pixels":undeleted,"undeleted_independent_survey_pixels":survey_undeleted,"poisoned_original_source_pixels":poisoned_pixels,"old_clothing_poison_regions":boxes.map(func(b: Rect2i) -> Array: return [b.position.x,b.position.y,b.size.x,b.size.y]),"rows":rows,"failures":failures,"negative_controls":controls,"limits":"Anatomy-base old clothing alpha must be zero in complete domains and independent six-region survey; poisoning original full-outfit source must not affect selected costume. Reinserted original outfit underlay and old cloth patches must be detected. QUICK12CASE PRECHECK: frozen-frame reproduction disabled here; full audit_replacement.gd remains mandatory. Numerical checks do not establish artistic, full-speed human, device, child or owner acceptance."}
	var file: FileAccess = FileAccess.open(out.path_join("precheck_audit.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report))
	file.close()
	print("REPLACEMENT_AUDIT ",pass_all," frames=",rows.size()," failures=",failures.size())
	quit(0 if pass_all else 1)
