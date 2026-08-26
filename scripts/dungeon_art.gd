class_name DungeonArt
extends RefCounted

const STORY_ART := preload("res://scripts/story_art.gd")

const PATHS := {
	"arena": "",
	"door": "",
	"imp": "",
	"boss": "",
	"basket": "",
	"pepper_projectile": "",
	"ice_berry_projectile": "",
	"pedestal": "",
	"lantern": "",
	"statue": "",
	"stone": "",
	"pictograms": "",
}

const EMBER_PATHS := {
	"arena": "",
	"door": "",
	"imp": "",
	"boss": "",
	"basket": "",
	"pepper_projectile": "",
	"ice_berry_projectile": "",
	"pedestal": "",
	"lantern": "",
	"statue": "",
	"stone": "",
	"pictograms": "",
	"clue_plaque": "",
	"direction_beak": "",
	"completion_spark": "",
	"pearl_target": "",
}

const PICTOGRAM_NODES := {
	"diamond": "Diamond",
	"orb": "Orb",
	"triangle": "Triangle",
	"ice": "Ice",
	"flame": "Flame",
	"moon": "Moon",
	"star": "Star",
	"question": "Question",
	"left": "Left",
	"right": "Right",
	"pepper": "Pepper",
}

const FALLBACK_PART_ART := {
	"DungeonArena": "res://assets/props/gen2/rock_largea_Image_0_flat.png",
	"DungeonDoor": "res://assets/props/gen2/fanshell_Image_0_flat.png",
	"ShellDoor": "res://assets/props/gen2/fanshell_Image_0_flat.png",
	"Imp": "res://assets/sprites/dust_bunnies/dust_bunny_idle.png",
	"Head": "res://assets/props/gen2/turtle_Image_0.jpg",
	"Shell": "res://assets/props/gen2/spiralshell_Image_0_flat.png",
	"Basket": "res://assets/props/gen2/sponge_barrel_Image_0_flat.png",
	"Projectile": "res://assets/props/story/flower_coral.png",
	"CrystalPedestal": "res://assets/art35/cards/style3/crystal_facet_crystal_facet.png",
	"Lantern": "res://assets/props/gen2/sponge_tubes_Image_0_flat.png",
	"Glow": "res://assets/art35/cards/mg/star_star.png",
	"Statue": "res://assets/props/gen2/turtle_Image_0.jpg",
	"Stone": "res://assets/props/gen2/rock3_Image_0_flat.png",
	"CluePlaque": "res://assets/props/gen2/rock2_Image_0_flat.png",
	"Beak": "res://assets/art35/cards/mg/carrot_carrot.png",
	"Spark": "res://assets/art35/cards/mg/star_star.png",
	"Pearl": "res://assets/props/gen2/sanddollar_Image_0_flat.png",
	"Diamond": "res://assets/art35/cards/style3/crystal_facet_crystal_facet.png",
	"Orb": "res://assets/props/gen2/sanddollar_Image_0_flat.png",
	"Triangle": "res://assets/art35/cards/mg/k_pine_k_pine.png",
	"Ice": "res://assets/art35/cards/mg/snowman_snowman.png",
	"Flame": "res://assets/art35/cards/mg/sun_sun.png",
	"Moon": "res://assets/props/gen2/smallfanshell_Image_0_flat.png",
	"Star": "res://assets/props/gen2/starfish_decal.png",
	"Question": "res://assets/art35/cards/mg/sprout_sprout.png",
	"Left": "res://assets/props/story/leaf_fern.png",
	"Right": "res://assets/props/story/leaf_broad.png",
	"Pepper": "res://assets/props/story/fruit_apple.png",
}

const FALLBACK_ROLE_SIZE := {
	"arena": 24.0,
	"door": 8.0,
	"imp": 3.2,
	"boss": 7.0,
	"basket": 3.0,
	"pepper_projectile": 1.2,
	"ice_berry_projectile": 1.2,
	"pedestal": 3.5,
	"lantern": 3.0,
	"statue": 5.0,
	"stone": 4.0,
	"pictograms": 2.0,
	"clue_plaque": 5.0,
	"direction_beak": 2.0,
	"completion_spark": 1.4,
	"pearl_target": 2.5,
}

static func spawn(role: String, parent: Node3D, position: Vector3 = Vector3.ZERO, theme: String = "") -> Node3D:
	var role_paths: Dictionary = EMBER_PATHS if theme == "ember" else PATHS
	var path: String = String(role_paths.get(role, ""))
	var scene: PackedScene = null
	if path != "":
		scene = load(path) as PackedScene
	if scene == null:
		if path != "":
			push_error("Dungeon art role could not be loaded: %s (%s)" % [role, path])
		var missing := Node3D.new()
		missing.name = "MissingDungeonArt_%s" % role
		missing.position = position
		parent.add_child(missing)
		# Retired model roles keep distinct, readable cards so the spatial
		# puzzles remain playable while their full Canvas2D conversion proceeds.
		var fallback_parts: Array[String] = []
		match role:
			"arena":
				fallback_parts = ["EmberArena" if theme == "ember" else "DungeonArena"]
			"door":
				fallback_parts = ["DungeonDoor", "ShellDoor"]
			"imp":
				fallback_parts = ["Imp"]
			"boss":
				fallback_parts = ["Head", "Shell"]
			"basket":
				fallback_parts = ["Basket"]
			"pepper_projectile", "ice_berry_projectile":
				fallback_parts = ["Projectile"]
			"pedestal":
				fallback_parts = ["CrystalPedestal"]
			"lantern":
				fallback_parts = ["Lantern", "Glow"]
			"statue":
				fallback_parts = ["Statue"]
			"stone":
				fallback_parts = ["Stone"]
			"pictograms":
				fallback_parts.assign(PICTOGRAM_NODES.values())
			"clue_plaque":
				fallback_parts = ["CluePlaque"]
			"direction_beak":
				fallback_parts = ["Beak"]
			"completion_spark":
				fallback_parts = ["Spark"]
			"pearl_target":
				fallback_parts = ["Pearl"]
		for part_name: String in fallback_parts:
			var art_key: String = "DungeonArena" if part_name == "EmberArena" else part_name
			var art_path: String = String(FALLBACK_PART_ART.get(art_key,
				"res://assets/props/story/flower_lavender.png"))
			var fallback_size: float = float(FALLBACK_ROLE_SIZE.get(role, 2.0))
			var part := STORY_ART.crossed_card(art_path, fallback_size)
			part.name = part_name
			for surface: Node in part.get_children():
				surface.name = "Tint_Fallback"
			missing.add_child(part)
		return missing
	var node: Node3D = scene.instantiate() as Node3D
	node.position = position
	parent.add_child(node)
	return node

static func tint(root: Node, surface: Material, trim: Material) -> void:
	if root is MeshInstance3D:
		var mesh_node := root as MeshInstance3D
		if mesh_node.name.begins_with("Tint_"):
			mesh_node.material_override = surface
		elif mesh_node.name.begins_with("Trim_"):
			mesh_node.material_override = trim
	for child in root.get_children():
		tint(child, surface, trim)

static func apply_material(root: Node, material: Material) -> void:
	if root == null:
		return
	if root is MeshInstance3D:
		(root as MeshInstance3D).material_override = material
	for child in root.get_children():
		apply_material(child, material)

static func find_part(root: Node, part_name: String) -> Node3D:
	var found: Node = root.find_child(part_name, true, false)
	if found == null:
		var suffixed: Array[Node] = root.find_children(part_name + "*", "Node3D", true, false)
		if not suffixed.is_empty():
			found = suffixed[0]
	return found as Node3D

static func add_pictogram(kind: String, parent: Node3D, position: Vector3, scale: float = 1.0,
		keep_kinds: Array[String] = [], theme: String = "") -> Node3D:
	var root := spawn("pictograms", parent, position, theme)
	root.scale = Vector3.ONE * scale
	root.rotation_degrees.x = 90.0
	var active_name: String = String(PICTOGRAM_NODES.get(kind, "Question"))
	var keep_names: Array[String] = [active_name]
	for keep_kind: String in keep_kinds:
		var keep_name: String = String(PICTOGRAM_NODES.get(keep_kind, "Question"))
		if keep_name not in keep_names:
			keep_names.append(keep_name)
	root.set_meta("pictogram_keep", keep_names)
	show_pictogram(root, kind)
	return root

static func show_pictogram(root: Node, kind: String) -> void:
	var active_name: String = String(PICTOGRAM_NODES.get(kind, "Question"))
	var keep_names: Array = root.get_meta("pictogram_keep", [active_name])
	for node_name: String in PICTOGRAM_NODES.values():
		var part: Node = root.find_child(node_name + "*", true, false)
		if part is Node3D:
			if node_name == active_name:
				(part as Node3D).visible = true
			elif node_name in keep_names:
				(part as Node3D).visible = false
			else:
				part.get_parent().remove_child(part)
				part.free()
