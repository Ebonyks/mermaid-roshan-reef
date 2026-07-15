extends RefCounted

const STORY_ROOT := "res://assets/props/story/"

const PLANT_ART := {
	"plant_bush": "leaf_broad.png",
	"plant_bushLargeTriangle": "leaf_broad.png",
	"grass_leafsLarge": "leaf_spear.png",
	"trop_monstera": "leaf_broad.png",
	"trop_bigleaf": "leaf_spear.png",
	"trop_fern": "leaf_fern.png",
	"flower_purpleA": "flower_lavender.png",
	"flower_redA": "flower_coral.png",
	"flower_yellowB": "flower_coral.png",
	"mushroom_red": "mushroom_red.png",
	"mushroom_tanGroup": "mushroom_tan_cluster.png",
}

const FRUIT_ART := {
	"apple": "fruit_apple.png",
	"banana": "fruit_banana.png",
	"orange": "fruit_orange.png",
	"melon": "fruit_melon.png",
}

const BUG_ART := {
	"beetle": "beetle.png",
	"ladybug": "ladybug.png",
}

static func _card_material(path: String, tint: Color = Color.WHITE) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = load(path)
	mat.albedo_color = tint
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	mat.roughness = 1.0
	mat.metallic = 0.0
	return mat

static func _quad(path: String, height: float, tint: Color = Color.WHITE) -> MeshInstance3D:
	var tex: Texture2D = load(path)
	var aspect := 1.0
	if tex != null and tex.get_height() > 0:
		aspect = float(tex.get_width()) / float(tex.get_height())
	var mesh := QuadMesh.new()
	mesh.size = Vector2(height * aspect, height)
	var card := MeshInstance3D.new()
	card.mesh = mesh
	card.material_override = _card_material(path, tint)
	card.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return card

static func crossed_card(path: String, height: float, tint: Color = Color.WHITE) -> Node3D:
	var root := Node3D.new()
	for i in range(2):
		var card := _quad(path, height, tint)
		card.position.y = height * 0.5
		card.rotation.y = float(i) * PI * 0.5
		root.add_child(card)
	root.set_meta("story_art", true)
	return root

static func ground_card(path: String, longest: float) -> Node3D:
	var tex: Texture2D = load(path)
	var aspect := 1.0
	if tex != null and tex.get_height() > 0:
		aspect = float(tex.get_width()) / float(tex.get_height())
	var height := longest / maxf(aspect, 1.0)
	var card := _quad(path, height)
	var mesh := card.mesh as QuadMesh
	mesh.size = Vector2(longest, height)
	card.rotation.x = -PI * 0.5
	card.position.y = 0.04
	var root := Node3D.new()
	root.add_child(card)
	root.set_meta("story_art", true)
	return root

static func plant(role: String, height: float, tint: Color = Color.WHITE) -> Node3D:
	if role in ["trop_palm1", "trop_palm2"]:
		var palm := Node3D.new()
		var trunk := MeshInstance3D.new()
		var trunk_mesh := CylinderMesh.new()
		trunk_mesh.top_radius = height * 0.045
		trunk_mesh.bottom_radius = height * 0.075
		trunk_mesh.height = height * 0.62
		trunk_mesh.radial_segments = 8
		trunk.mesh = trunk_mesh
		var trunk_mat := StandardMaterial3D.new()
		trunk_mat.albedo_texture = load("res://assets/terrain/up_wood_col.jpg")
		trunk_mat.uv1_triplanar = true
		trunk_mat.uv1_scale = Vector3(0.4, 0.4, 0.4)
		trunk_mat.albedo_color = Color(0.95, 0.72, 0.58)
		trunk_mat.roughness = 1.0
		trunk.material_override = trunk_mat
		trunk.position.y = trunk_mesh.height * 0.5
		palm.add_child(trunk)
		var crown := crossed_card(STORY_ROOT + "leaf_palmfan.png", height * 0.58, tint)
		crown.position.y = height * 0.47
		palm.add_child(crown)
		palm.set_meta("story_art", true)
		return palm
	if not PLANT_ART.has(role):
		return null
	var path: String = STORY_ROOT + String(PLANT_ART[role])
	var card_height := height
	if role.begins_with("flower_"):
		card_height = height * 0.72
	elif role.begins_with("mushroom_"):
		card_height = height * 0.8
	var root := crossed_card(path, card_height, tint)
	if role == "plant_bushLargeTriangle":
		for i in range(2):
			var extra := crossed_card(path, card_height * 0.72, tint)
			extra.position = Vector3((-1.0 if i == 0 else 1.0) * height * 0.24, 0.0, height * 0.08)
			extra.rotation.y = float(i) * 0.7
			root.add_child(extra)
	return root

static func fruit(role: String, height: float) -> Node3D:
	if not FRUIT_ART.has(role):
		return null
	return crossed_card(STORY_ROOT + String(FRUIT_ART[role]), height)

static func bug(role: String, longest: float) -> Node3D:
	if not BUG_ART.has(role):
		return null
	return ground_card(STORY_ROOT + String(BUG_ART[role]), longest)

static func apply_triplanar(root: Node, texture_path: String, uv_scale: float, tint: Color = Color.WHITE) -> void:
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = load(texture_path)
	mat.albedo_color = tint
	mat.uv1_triplanar = true
	mat.uv1_scale = Vector3(uv_scale, uv_scale, uv_scale)
	mat.roughness = 1.0
	mat.metallic = 0.0
	mat.metallic_specular = 0.08
	_apply_material(root, mat)

static func _apply_material(node: Node, mat: Material) -> void:
	if node is MeshInstance3D:
		var mesh_instance := node as MeshInstance3D
		if mesh_instance.mesh != null:
			for surface in range(mesh_instance.mesh.get_surface_count()):
				mesh_instance.set_surface_override_material(surface, mat)
	for child in node.get_children():
		_apply_material(child, mat)
