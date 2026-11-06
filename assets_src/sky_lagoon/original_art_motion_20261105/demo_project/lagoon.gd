extends Node2D

const MASTER_SIZE := Vector2(6144.0, 2048.0)
const FRAME_COUNT := 60
const FPS := 30.0
var targets: Array = []
var patch_nodes: Array[Sprite2D] = []
var base_nodes: Array[Sprite2D] = []
var clock_s: float = 0.0
var animated: bool = true
var paused: bool = false
var closeup: bool = false
var scene_root: Node2D
var board_root: Node2D
var board_nodes: Array[Sprite2D] = []
var status: Label

func _ready() -> void:
	targets = JSON.parse_string(FileAccess.get_file_as_string("res://targets.json"))
	scene_root = Node2D.new()
	add_child(scene_root)
	for row in range(2):
		for col in range(6):
			var card := Sprite2D.new()
			card.centered = false
			card.texture = load("res://background/%d_%d.png" % [row, col])
			card.position = Vector2(col * 1024, row * 1024)
			scene_root.add_child(card)
			base_nodes.append(card)
	board_root = Node2D.new()
	add_child(board_root)
	var shader: Shader = load("res://breeze.gdshader")
	for i in range(targets.size()):
		var item: Dictionary = targets[i]
		var card := Sprite2D.new()
		card.centered = false
		card.texture = load("res://patches/%s.png" % item["id"])
		card.position = Vector2(float(item["xy"][0]), float(item["xy"][1]))
		var material := ShaderMaterial.new()
		material.shader = shader
		material.set_shader_parameter("motion_field", load("res://patches/%s_field.png" % item["id"]))
		card.material = material
		scene_root.add_child(card)
		patch_nodes.append(card)
		var board := Sprite2D.new()
		board.centered = false
		board.texture = card.texture
		board.material = material
		board.position = Vector2(i * 528, 0)
		board_root.add_child(board)
		board_nodes.append(board)
	var hud := CanvasLayer.new()
	add_child(hud)
	status = Label.new()
	status.position = Vector2(18, 14)
	hud.add_child(status)
	get_viewport().size_changed.connect(_layout)
	_layout()
	_apply_frame(0)
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if "--verify" in args:
		_verify()

func _layout() -> void:
	var size: Vector2 = get_viewport_rect().size
	var factor: float = minf(size.x / MASTER_SIZE.x, (size.y - 80.0) / MASTER_SIZE.y)
	scene_root.scale = Vector2.ONE * factor
	scene_root.position = (size - MASTER_SIZE * factor) * 0.5 + Vector2(0, 16)
	var board_size := Vector2(1568, 512)
	var board_scale: float = minf(size.x / board_size.x, (size.y - 90.0) / board_size.y)
	board_root.scale = Vector2.ONE * board_scale
	board_root.position = (size - board_size * board_scale) * 0.5 + Vector2(0, 16)
	scene_root.visible = not closeup
	board_root.visible = closeup

func _process(delta: float) -> void:
	if not paused:
		clock_s += delta
	var index: int = int(floor(clock_s * FPS)) % FRAME_COUNT
	_apply_frame(index)
	status.text = "Original Sky Lagoon painting   |   %s   |   Space: pause   A: original/breeze   C: flower close-up" % ("gentle breeze" if animated else "original still")

func _apply_frame(index: int) -> void:
	var phase: float = float(index) * TAU / float(FRAME_COUNT)
	for i in range(targets.size()):
		var item: Dictionary = targets[i]
		var displacement: float = float(item["amplitude"]) * (sin(phase) + 0.16 * sin(phase * 2.0)) / 1.16 if animated else 0.0
		var material: ShaderMaterial = patch_nodes[i].material
		material.set_shader_parameter("displacement_px", displacement)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_SPACE:
			paused = not paused
		elif event.keycode == KEY_A:
			animated = not animated
		elif event.keycode == KEY_C:
			closeup = not closeup
			_layout()
		elif event.keycode == KEY_ESCAPE:
			get_tree().quit()

func _verify() -> void:
	set_process(false)
	status.visible = false
	var errors: Array[String] = []
	var method: String = RenderingServer.get_current_rendering_method()
	if method != "mobile":
		errors.append("Wrong renderer: " + method)
	for i in range(targets.size()):
		var item: Dictionary = targets[i]
		var texture_image: Image = patch_nodes[i].texture.get_image()
		var source_image := Image.load_from_file("res://patches/%s.png" % item["id"])
		texture_image.convert(Image.FORMAT_RGBA8)
		source_image.convert(Image.FORMAT_RGBA8)
		if texture_image.get_data() != source_image.get_data():
			errors.append("Imported source RGBA differs: " + str(item["id"]))
		var field_texture: Texture2D = load("res://patches/%s_field.png" % item["id"])
		var field_import: Image = field_texture.get_image()
		var field_source := Image.load_from_file("res://patches/%s_field.png" % item["id"])
		field_import.convert(Image.FORMAT_RGBA8)
		field_source.convert(Image.FORMAT_RGBA8)
		if field_import.get_data() != field_source.get_data():
			errors.append("Imported motion field differs: " + str(item["id"]))
	var folder: String = ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(folder + "/capture_frames")
	# Independent pristine-tile rendering control: restore original source pixels
	# into each native tile, with no patch nodes or displacement shader.
	var originals: Array[Texture2D] = []
	for n in range(base_nodes.size()):
		var card: Sprite2D = base_nodes[n]
		originals.append(card.texture)
		var pristine: Image = card.texture.get_image()
		pristine.convert(Image.FORMAT_RGBA8)
		var tile_rect := Rect2i(Vector2i(card.position), Vector2i(1024, 1024))
		for j in range(targets.size()):
			var patch_rect := Rect2i(Vector2i(patch_nodes[j].position), Vector2i(512, 512))
			var overlap: Rect2i = tile_rect.intersection(patch_rect)
			if overlap.has_area():
				var source_patch: Image = patch_nodes[j].texture.get_image()
				source_patch.convert(Image.FORMAT_RGBA8)
				pristine.blit_rect(source_patch, Rect2i(overlap.position - patch_rect.position, overlap.size), overlap.position - tile_rect.position)
		card.texture = ImageTexture.create_from_image(pristine)
	for card in patch_nodes:
		card.visible = false
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(folder + "/mobile-pristine-control.png")
	for n in range(base_nodes.size()):
		base_nodes[n].texture = originals[n]
	for card in patch_nodes:
		card.visible = true
	var scene_position: Vector2 = scene_root.position
	for index in range(FRAME_COUNT):
		_apply_frame(index)
		await RenderingServer.frame_post_draw
		var image: Image = get_viewport().get_texture().get_image()
		image.save_png(folder + "/capture_frames/%03d.png" % index)
		if index in [0, 15, 45]:
			image.save_png(folder + "/mobile-%02d.png" % index)
		if scene_root.position != scene_position:
			errors.append("Camera/stage moved")
	var input_hashes: Dictionary = {}
	for file_path in ["res://lagoon.gd", "res://breeze.gdshader", "res://targets.json", "res://project.godot", "res://lagoon.tscn"]:
		input_hashes[file_path] = FileAccess.get_sha256(file_path)
	for row in range(2):
		for col in range(6):
			var file_path: String = "res://background/%d_%d.png" % [row, col]
			input_hashes[file_path] = FileAccess.get_sha256(file_path)
	for item in targets:
		for suffix in ["", "_field"]:
			var file_path: String = "res://patches/%s%s.png" % [item["id"], suffix]
			input_hashes[file_path] = FileAccess.get_sha256(file_path)
	var receipt := {"input_hashes": input_hashes, "engine": Engine.get_version_info(), "renderer": method, "frames": FRAME_COUNT, "animation_fps": FPS, "duration_s": 2.0, "fixed_stage": true, "source_imports_exact": errors.is_empty(), "errors": errors, "device": "PENDING; desktop GPU is not target-device performance evidence"}
	var file := FileAccess.open(folder + "/mobile-verification.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	print("ORIGINAL_ART_MOBILE|", "PASS" if errors.is_empty() else "FAIL", "|", JSON.stringify(receipt))
	get_tree().quit(0 if errors.is_empty() else 1)

