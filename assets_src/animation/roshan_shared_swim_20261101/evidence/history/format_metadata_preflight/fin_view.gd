extends RefCounted
## Common authored-view interpolation. Never created or changed by an outfit.

var material: ShaderMaterial
var data_textures: Array[Texture2D] = []


func build(fields: Dictionary, anatomy_nodes: Dictionary, prefix: String) -> ShaderMaterial:
	material = ShaderMaterial.new()
	var shader: Shader = Shader.new()
	shader.code = FileAccess.get_file_as_string("res://fin_view.gdshader")
	material.shader = shader
	for pose: String in ["broad", "edge", "cup"]:
		material.set_shader_parameter(pose + "_image", anatomy_nodes["fin_" + pose]["payload"]["texture"])
		for kind: String in ["distance", "nearest_uv"]:
			var reference: Dictionary = fields["buffers"]["fin_" + pose][kind]
			var local_path: String = "res://" + str(reference["path"]).trim_prefix(prefix)
			assert(FileAccess.get_sha256(local_path) == reference["sha256"])
			var buffer: PackedByteArray = FileAccess.get_file_as_bytes(local_path)
			var channels: int = 1 if kind == "distance" else 2
			assert(buffer.size() == 512 * 512 * channels * 4)
			var image: Image = Image.create_from_data(512, 512, false, Image.FORMAT_RF if channels == 1 else Image.FORMAT_RGF, buffer)
			var texture: ImageTexture = ImageTexture.create_from_image(image)
			data_textures.append(texture)
			material.set_shader_parameter(pose + ("_distance" if channels == 1 else "_nearest"), texture)
	return material


func set_view(turn_degrees: float, cup: float) -> void:
	material.set_shader_parameter("turn_weight", clampf(turn_degrees / 75.0, 0.0, 1.0))
	material.set_shader_parameter("cup_weight", clampf(cup, 0.0, 1.0))


func snapshot() -> Dictionary:
	var ids: Array = []
	for texture: Texture2D in data_textures:
		ids.append(texture.get_instance_id())
	return {"material": material.get_instance_id(), "field_textures": ids,
		"turn_weight": material.get_shader_parameter("turn_weight"),
		"cup_weight": material.get_shader_parameter("cup_weight")}
