class_name MinigameStorybookArt
extends RefCounted

# Small runtime bridge for the 3D-to-2D migration. Gameplay may continue to use
# Node3D coordinates and analytic movement, while every visible authored object
# is a Sprite3D card or a CanvasItem.

static func sprite(
		parent: Node3D,
		path: String,
		height: float,
		position: Vector3 = Vector3.ZERO,
		billboard: bool = true,
		node_name: String = "StorybookSprite") -> Sprite3D:
	var card := Sprite3D.new()
	card.name = node_name
	var texture: Texture2D = load(path)
	card.texture = texture
	card.pixel_size = height / maxf(1.0, float(texture.get_height()))
	card.position = position
	card.billboard = BaseMaterial3D.BILLBOARD_ENABLED if billboard else BaseMaterial3D.BILLBOARD_DISABLED
	card.shaded = false
	card.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	card.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	card.set_meta("storybook_2d", true)
	parent.add_child(card)
	return card

static func camera_background(camera: Camera3D, path: String, height: float = 116.0) -> Sprite3D:
	var card := sprite(camera, path, height, Vector3(0, 0, -100.0), false, "StorybookBackground")
	card.centered = true
	card.transparent = false
	card.render_priority = -20
	return card

static func world_backdrop(
		parent: Node3D,
		path: String,
		height: float,
		position: Vector3,
		node_name: String = "StorybookBackdrop") -> Sprite3D:
	var card := sprite(parent, path, height, position, false, node_name)
	card.transparent = false
	card.render_priority = -15
	return card

static func retire_legacy_visuals(root: Node) -> void:
	# Imported/procedural meshes remain only as temporary gameplay-state
	# scaffolding until those scripts are mechanically extracted. Cull layers
	# make them non-rendering without mutating `visible`, which several legacy
	# minigame state machines still use as a logical flag. Sprite3D, Label3D
	# and CanvasItem visuals remain available.
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for child: Node in node.get_children():
			stack.append(child)
		if bool(node.get_meta("storybook_2d", false)):
			continue
		if node is MeshInstance3D:
			(node as MeshInstance3D).layers = 0
		elif node is MultiMeshInstance3D:
			(node as MultiMeshInstance3D).layers = 0
		elif node is Light3D:
			(node as Light3D).light_cull_mask = 0
		elif node is GPUParticles3D:
			(node as GPUParticles3D).layers = 0
		elif node is CPUParticles3D:
			(node as CPUParticles3D).layers = 0
