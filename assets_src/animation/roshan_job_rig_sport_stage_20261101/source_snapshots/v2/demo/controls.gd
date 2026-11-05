extends SceneTree

func _initialize() -> void:
	run.call_deferred()

func snap(view: SubViewport) -> Image:
	await process_frame
	RenderingServer.force_draw(false)
	await process_frame
	return view.get_texture().get_image()

func changed(a: Image,b: Image) -> int:
	var av: PackedByteArray = a.get_data()
	var bv: PackedByteArray = b.get_data()
	var count: int = 0
	for i: int in range(0,av.size(),4):
		if av[i]!=bv[i] or av[i+1]!=bv[i+1] or av[i+2]!=bv[i+2] or av[i+3]!=bv[i+3]:
			count += 1
	return count

func run() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(out)
	var scene: Node2D = load("res://study.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.run_action = false
	var view: SubViewport = SubViewport.new()
	view.size = Vector2i(1024,1024)
	view.transparent_bg = true
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	scene.actor.reparent(view)
	scene.actor.position = Vector2.ZERO
	scene.actor.scale = Vector2.ONE
	var rows: Array = []
	for clip: String in ["boxer","racer","popstar"]:
		scene.set_parts({"head":clip,"body":clip,"tail":clip})
		scene.action = clip
		scene.control = "none"
		scene.pose_action(clip,3.2)
		var normal: Image = await snap(view)
		normal.save_png(out.path_join(clip+"_none.png"))
		rows.append({"clip":clip,"control":"none","record":scene.record(),"image":clip+"_none.png","changed_pixels":0})
		for control: String in ["grip_slip","fixture_drift","missing_arm","original_underlay","identity_scale","frozen_view"]:
			scene.control = control
			scene.pose_action(clip,3.2)
			var pic: Image = await snap(view)
			var name: String = clip+"_"+control+".png"
			pic.save_png(out.path_join(name))
			rows.append({"clip":clip,"control":control,"record":scene.record(),"image":name,"changed_pixels":changed(normal,pic)})
		scene.control = "none"
	# Preserve the independent original-clothing survey and source poison.
	var original: Texture2D = scene.original_body_texture
	var image: Image = original.get_image()
	var anatomy: Image = scene.garment_textures["anatomy"].get_image()
	var poisoned: Image = original.get_image()
	var boxes: Array[Rect2i] = [Rect2i(451,346,20,22),Rect2i(619,342,12,25),Rect2i(515,370,64,68),Rect2i(487,510,14,64),Rect2i(642,581,12,64),Rect2i(473,795,40,20)]
	var surveyed: int = 0
	var undeleted: int = 0
	for box: Rect2i in boxes:
		for y: int in range(box.position.y,box.end.y):
			for x: int in range(box.position.x,box.end.x):
				var c: Color = image.get_pixel(x,y)
				if c.a>0.9 and c.b>c.r*0.84 and c.b>c.g*1.035:
					surveyed += 1
					if anatomy.get_pixel(x,y).a>0.0:
						undeleted += 1
					poisoned.set_pixel(x,y,Color(0,1,0,c.a))
	var poison_texture: ImageTexture = ImageTexture.create_from_image(poisoned)
	var poison_rows: Array = []
	for theme: String in ["boxer","racer","popstar"]:
		for clip: String in ["arm_bend","blink","tail_bend"]:
			for t: float in [0.0,1.1,2.1]:
				scene.original_body_texture = original
				scene.set_parts({"head":theme,"body":theme,"tail":theme})
				scene.action = clip
				scene.pose_action(clip,t)
				var a: Image = await snap(view)
				scene.original_body_texture = poison_texture
				scene.set_parts({"head":theme,"body":theme,"tail":theme})
				scene.pose_action(clip,t)
				var b: Image = await snap(view)
				poison_rows.append({"theme":theme,"clip":clip,"time":t,"source_leak_pixels":changed(a,b)})
	scene.original_body_texture = original
	var file: FileAccess = FileAccess.open(out.path_join("controls.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"rows":rows,"source_poison_rows":poison_rows,"surveyed_old_clothing_pixels":surveyed,"undeleted_old_clothing_pixels":undeleted},"  "))
	print("CONTROLS_CAPTURE_COMPLETE ",rows.size()," controls; source poison=",poison_rows.size())
	quit(0)
