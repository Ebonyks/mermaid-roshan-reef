class_name DungeonArt
extends RefCounted
# Theme-local 2D art factory shared by combat and puzzle rooms.

const ROOT := "res://assets/minigames/dungeon/crystal/"
const EMBER_ROOT := "res://assets/minigames/dungeon/ember/"
const SHARED_ROOT := "res://assets/minigames/dungeon/shared/"

const PATHS := {
	"arena": ROOT + "arena.png",
	"door": ROOT + "door.svg",
	"imp": ROOT + "imp.png",
	"basket": ROOT + "basket.svg",
	"pepper_projectile": SHARED_ROOT + "pepper.svg",
	"ice_berry_projectile": SHARED_ROOT + "ice_berry.svg",
	"pedestal": ROOT + "pedestal.svg",
	"lantern": ROOT + "lantern.svg",
	"statue": ROOT + "statue.svg",
	"stone": ROOT + "pedestal.svg",
	"completion_spark": SHARED_ROOT + "spark.svg",
	"enemy_projectile": SHARED_ROOT + "enemy_orb.svg",
	"direction_beak": SHARED_ROOT + "direction_beak.svg",
	"pearl_target": SHARED_ROOT + "pearl_target.svg",
}

const EMBER_PATHS := {
	"arena": EMBER_ROOT + "arena.png",
	"door": EMBER_ROOT + "door.svg",
	"imp": EMBER_ROOT + "imp.png",
	"basket": EMBER_ROOT + "basket.svg",
	"pepper_projectile": SHARED_ROOT + "pepper.svg",
	"ice_berry_projectile": SHARED_ROOT + "ice_berry.svg",
	"pedestal": EMBER_ROOT + "pedestal.svg",
	"lantern": EMBER_ROOT + "lantern.svg",
	"statue": EMBER_ROOT + "statue.svg",
	"stone": EMBER_ROOT + "pedestal.svg",
	"clue_plaque": EMBER_ROOT + "pedestal.svg",
	"direction_beak": SHARED_ROOT + "direction_beak.svg",
	"completion_spark": SHARED_ROOT + "spark.svg",
	"pearl_target": SHARED_ROOT + "pearl_target.svg",
	"enemy_projectile": SHARED_ROOT + "enemy_orb.svg",
}

const ROLE_HEIGHT := {
	"door": 10.0,
	"imp": 5.4,
	"basket": 3.4,
	"pepper_projectile": 1.5,
	"ice_berry_projectile": 1.7,
	"pedestal": 4.2,
	"lantern": 5.6,
	"statue": 8.0,
	"stone": 4.0,
	"clue_plaque": 4.2,
	"direction_beak": 2.8,
	"completion_spark": 2.0,
	"pearl_target": 3.4,
	"enemy_projectile": 1.5,
}

const PICTOGRAM_INDEX := {
	"diamond": 0,
	"orb": 1,
	"triangle": 2,
	"ice": 3,
	"flame": 4,
	"moon": 5,
	"star": 6,
	"question": 7,
	"left": 8,
	"right": 9,
	"pepper": 10,
}
const PICTOGRAM_NAMES := {
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

static func _add_sprite(
		parent: Node3D,
		path: String,
		height: float,
		node_name: String = "Sprite",
		local_position: Vector3 = Vector3.ZERO) -> Sprite3D:
	var sprite := Sprite3D.new()
	sprite.name = node_name
	var texture: Texture2D = load(path)
	sprite.texture = texture
	sprite.pixel_size = height / maxf(1.0, float(texture.get_height()))
	sprite.position = local_position
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	parent.add_child(sprite)
	return sprite

static func _spawn_arena(path: String, parent: Node3D, position: Vector3) -> Node3D:
	var root := Node3D.new()
	root.name = "DungeonArena"
	root.position = position
	parent.add_child(root)
	var floor := _add_sprite(root, path, 58.0, "ArenaSprite")
	floor.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	floor.rotation.x = -PI * 0.5
	floor.position.y = 0.04
	floor.transparent = false
	return root

static func _spawn_boss(parent: Node3D, position: Vector3, theme: String) -> Node3D:
	var root := Node3D.new()
	root.name = "DragonTurtle2D"
	root.position = position
	parent.add_child(root)
	var prefix := EMBER_ROOT if theme == "ember" else ROOT
	var shell := Node3D.new()
	shell.name = "Shell"
	root.add_child(shell)
	_add_sprite(shell, prefix + "boss_shell.png", 10.5, "ShellSprite")
	var head := Node3D.new()
	head.name = "Head"
	head.position = Vector3(0.0, 0.25, 2.8)
	root.add_child(head)
	var head_sprite := _add_sprite(head, prefix + "boss_head.png", 7.2, "HeadSprite")
	head_sprite.render_priority = 1
	return root

static func spawn(
		role: String,
		parent: Node3D,
		position: Vector3 = Vector3.ZERO,
		theme: String = "") -> Node3D:
	var role_paths: Dictionary = EMBER_PATHS if theme == "ember" else PATHS
	if role == "arena":
		return _spawn_arena(String(role_paths["arena"]), parent, position)
	if role == "boss":
		return _spawn_boss(parent, position, theme)
	var path := String(role_paths.get(role, ""))
	if path == "" or not ResourceLoader.exists(path):
		push_error("Dungeon 2D art role could not be loaded: %s (%s)" % [role, path])
		var missing := Node3D.new()
		missing.name = "MissingDungeonArt_%s" % role
		missing.position = position
		parent.add_child(missing)
		return missing
	var root := Node3D.new()
	var role_names := {
		"door": "DungeonDoor",
		"imp": "MischiefImp",
		"pedestal": "CrystalPedestal",
		"lantern": "PepperLantern",
		"statue": "TurtleStatue",
		"stone": "SteppingStone",
	}
	root.name = String(role_names.get(role, "DungeonSprite_%s" % role))
	root.position = position
	parent.add_child(root)
	_add_sprite(root, path, float(ROLE_HEIGHT.get(role, 4.0)), "Body")
	if role == "lantern":
		var glow := Node3D.new()
		glow.name = "Glow"
		glow.position = Vector3(0.0, 2.4, 0.0)
		root.add_child(glow)
		var spark := _add_sprite(glow, SHARED_ROOT + "spark.svg", 1.5, "GlowSprite")
		spark.modulate = Color(1.0, 0.9, 0.45)
	return root

static func tint(_root: Node, _surface: Material, _trim: Material) -> void:
	# Authored sprite palettes are already theme-correct and stay untinted.
	pass

static func apply_material(root: Node, material: Material) -> void:
	if root == null:
		return
	if root is Sprite3D and material is StandardMaterial3D:
		(root as Sprite3D).modulate = (material as StandardMaterial3D).albedo_color
	for child in root.get_children():
		apply_material(child, material)

static func find_part(root: Node, part_name: String) -> Node3D:
	if root == null:
		return null
	var found: Node = root.find_child(part_name, true, false)
	return found as Node3D

static func add_pictogram(
		kind: String,
		parent: Node3D,
		position: Vector3,
		scale: float = 1.0,
		keep_kinds: Array[String] = [],
		_theme: String = "") -> Node3D:
	var root := Node3D.new()
	root.name = "Pictogram_%s" % kind
	root.position = position
	root.scale = Vector3.ONE * scale
	parent.add_child(root)
	var sprite := Sprite3D.new()
	sprite.name = "PictogramSprite"
	sprite.texture = load(SHARED_ROOT + "symbols.svg")
	sprite.region_enabled = true
	sprite.pixel_size = 4.4 / 192.0
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	root.add_child(sprite)
	var marker_kinds: Array[String] = [kind]
	for keep_kind: String in keep_kinds:
		if keep_kind not in marker_kinds:
			marker_kinds.append(keep_kind)
	for marker_kind: String in marker_kinds:
		var marker := Node3D.new()
		marker.name = String(PICTOGRAM_NAMES[marker_kind])
		marker.visible = false
		root.add_child(marker)
	root.set_meta("pictogram_keep", keep_kinds)
	show_pictogram(root, kind)
	return root

static func show_pictogram(root: Node, kind: String) -> void:
	if root == null:
		return
	var sprite: Sprite3D = root.find_child("PictogramSprite", true, false) as Sprite3D
	if sprite == null:
		return
	var index: int = int(PICTOGRAM_INDEX.get(kind, PICTOGRAM_INDEX["question"]))
	var column := index % 4
	var row := index / 4
	sprite.region_rect = Rect2(float(column * 192), float(row * 192), 192.0, 192.0)
	sprite.visible = true
	for marker_kind: String in PICTOGRAM_NAMES:
		var marker: Node3D = root.find_child(
			String(PICTOGRAM_NAMES[marker_kind]), false, false) as Node3D
		if marker != null:
			marker.visible = marker_kind == kind
