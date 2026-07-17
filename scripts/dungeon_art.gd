class_name DungeonArt
extends RefCounted

const ROOT := "res://assets/dungeon/"
const PATHS := {
	"arena": ROOT + "dungeon_arena.glb",
	"door": ROOT + "dungeon_door.glb",
	"imp": ROOT + "mischief_imp.glb",
	"boss": ROOT + "dragon_turtle.glb",
	"basket": ROOT + "pepper_basket.glb",
	"pepper_projectile": ROOT + "pepper_projectile.glb",
	"ice_berry_projectile": ROOT + "ice_berry_projectile.glb",
	"pedestal": ROOT + "crystal_pedestal.glb",
	"lantern": ROOT + "pepper_lantern.glb",
	"statue": ROOT + "turtle_statue.glb",
	"stone": ROOT + "stepping_stone.glb",
	"pictograms": ROOT + "dungeon_pictograms.glb",
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

static func spawn(role: String, parent: Node3D, position: Vector3 = Vector3.ZERO) -> Node3D:
	var path: String = String(PATHS.get(role, ""))
	var scene: PackedScene = load(path) as PackedScene
	if scene == null:
		push_error("Dungeon art role could not be loaded: %s (%s)" % [role, path])
		var missing := Node3D.new()
		missing.name = "MissingDungeonArt_%s" % role
		missing.position = position
		parent.add_child(missing)
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
	if root is MeshInstance3D:
		(root as MeshInstance3D).material_override = material
	for child in root.get_children():
		apply_material(child, material)

static func find_part(root: Node, part_name: String) -> Node3D:
	var found: Node = root.find_child(part_name, true, false)
	return found as Node3D

static func add_pictogram(kind: String, parent: Node3D, position: Vector3, scale: float = 1.0, keep_kinds: Array[String] = []) -> Node3D:
	var root := spawn("pictograms", parent, position)
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
		var part: Node = root.find_child(node_name, true, false)
		if part is Node3D:
			if node_name == active_name:
				(part as Node3D).visible = true
			elif node_name in keep_names:
				(part as Node3D).visible = false
			else:
				part.get_parent().remove_child(part)
				part.free()
