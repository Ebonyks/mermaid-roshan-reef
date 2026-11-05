extends Node2D
## Provisional source-view binding. No production rig or gameplay authority.

var actor: Node2D
var skeleton: Skeleton2D
var bones: Dictionary = {}
var rest_world: Dictionary = {}
var rig: Dictionary
var plan: Array
var records: Array = []
var recording: bool = false
var sample_index: int = 0
var play_time: float = 0.0
var preview_items: Array[CanvasItem] = []


func local_stage(node: Node2D) -> Transform2D:
	return actor.global_transform.affine_inverse() * node.global_transform


func _ready() -> void:
	rig = JSON.parse_string(FileAccess.get_file_as_string("res://view_binding.json"))
	plan = JSON.parse_string(FileAccess.get_file_as_string("res://plan.json"))
	var bg: ColorRect = ColorRect.new()
	bg.color = Color("102f43")
	bg.size = Vector2(1280, 720)
	bg.z_index = -10
	add_child(bg)
	preview_items.append(bg)
	var title: Label = Label.new()
	title.text = "Roshan · tail stroke and glide"
	title.position = Vector2(42, 30)
	title.add_theme_font_size_override("font_size", 27)
	add_child(title)
	preview_items.append(title)
	var caption: Label = Label.new()
	caption.text = "Locomotion study · existing swimming artwork"
	caption.position = Vector2(42, 660)
	caption.modulate.a = 0.65
	caption.add_theme_font_size_override("font_size", 18)
	add_child(caption)
	preview_items.append(caption)
	actor = Node2D.new()
	actor.name = "Actor"
	add_child(actor)
	actor.scale = Vector2(2.2, 2.2)
	skeleton = Skeleton2D.new()
	skeleton.name = "Skeleton"
	actor.add_child(skeleton)
	for data in rig.bones:
		var bone: Bone2D = Bone2D.new()
		bone.name = str(data.name)
		bone.set_autocalculate_length_and_angle(false)
		var parent: Node2D = skeleton if data.parent == null else bones[str(data.parent)]
		parent.add_child(bone)
		var head: Vector2 = Vector2(data.head[0], data.head[1])
		var tail: Vector2 = Vector2(data.tail[0], data.tail[1])
		bone.transform = local_stage(parent).affine_inverse() * Transform2D((tail-head).angle(), head)
		bone.set_length(head.distance_to(tail))
		bone.set_bone_angle(0.0)
		bone.rest = bone.transform
		bones[str(data.name)] = bone
		rest_world[str(data.name)] = local_stage(bone)
	var source: Image = Image.load_from_file(ProjectSettings.globalize_path("res://approved_swim_atlas.png"))
	var texture: ImageTexture = ImageTexture.create_from_image(source.get_region(Rect2i(512,512,256,256)))
	for mesh in rig.meshes:
		var polygon: Polygon2D = Polygon2D.new()
		polygon.name = str(mesh.name)
		polygon.texture = texture
		polygon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var points: PackedVector2Array = PackedVector2Array()
		for p in mesh.vertices:
			points.append(Vector2(p[0],p[1]))
		polygon.polygon = points
		polygon.uv = points
		var triangles: Array = []
		for tri in mesh.triangles:
			triangles.append(PackedInt32Array(tri))
		polygon.polygons = triangles
		actor.add_child(polygon)
		polygon.skeleton = polygon.get_path_to(skeleton)
		for bone_name in mesh.weights:
			polygon.add_bone(skeleton.get_path_to(bones[bone_name]),PackedFloat32Array(mesh.weights[bone_name]))
	apply_sample(0)
	recording = "--capture" in OS.get_cmdline_user_args()
	if recording:
		capture.call_deferred()


func apply_sample(index: int) -> void:
	var sample: Dictionary = plan[index]
	for name in bones:
		var bone: Bone2D = bones[name]
		bone.rotation = bone.rest.get_rotation() + float(sample.angles.get(name,0.0))
	# This displacement is integrated from tail/water force, not a position tween.
	actor.position = Vector2(490.0+float(sample.x)*2.2,390.0)-Vector2(119,132)*2.2
	actor.rotation = 0.0


func capture() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://frames"))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://rgba"))
	for i in range(plan.size()):
		apply_sample(i)
		await RenderingServer.frame_post_draw
		var pixels: Image = get_viewport().get_texture().get_image()
		pixels.save_png(ProjectSettings.globalize_path("res://frames/%04d.png" % i))
		for item in preview_items:
			item.visible = false
		get_viewport().transparent_bg = true
		await RenderingServer.frame_post_draw
		pixels = get_viewport().get_texture().get_image()
		pixels.save_png(ProjectSettings.globalize_path("res://rgba/%04d.png" % i))
		get_viewport().transparent_bg = false
		for item in preview_items:
			item.visible = true
		var states: Dictionary = {}
		for name in bones:
			var transform: Transform2D = local_stage(bones[name])
			states[name] = [transform.x.x,transform.x.y,transform.y.x,transform.y.y,transform.origin.x,transform.origin.y]
		records.append({"index":i,"t":float(plan[i].t),"bones":states,"actor_rotation":actor.rotation,"position":[actor.position.x,actor.position.y],"scale":[actor.scale.x,actor.scale.y]})
	var file: FileAccess = FileAccess.open("res://samples.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"\t"))
	file.close()
	var info: Dictionary = {"version":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"adapter":RenderingServer.get_video_adapter_name(),"frames":plan.size(),"size":[1280,720],"fps":30,"scope":"Source-only native Mobile render; no production or human acceptance"}
	file = FileAccess.open("res://environment.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(info,"\t"))
	file.close()
	print("Captured ",plan.size()," tail-driven source frames")
	get_tree().quit()


func _process(delta: float) -> void:
	if recording:
		return
	play_time = fmod(play_time+delta,6.5)
	sample_index = mini(int(play_time*30.0),plan.size()-1)
	apply_sample(sample_index)
