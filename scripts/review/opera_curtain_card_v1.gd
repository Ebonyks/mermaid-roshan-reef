extends Node2D
## Two original-pixel fabric panels. The original gold arch stays on the wall.

const FABRIC_SHADER := preload("res://shaders/opera_translation_curtain.gdshader")

var opening := 0.0
var left: Sprite2D
var right: Sprite2D
var half_width := 0.0
var materials: Array[ShaderMaterial] = []

func setup(source: Image, rect: Rect2i, world_rect: Rect2) -> void:
	position = world_rect.position
	var clip := Control.new()
	clip.size = world_rect.size
	clip.clip_contents = true
	clip.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(clip)
	var native_scale: Vector2 = world_rect.size/Vector2(rect.size)
	var split: int = rect.size.x/2
	half_width = float(split)*native_scale.x
	for side: int in range(2):
		var crop := Rect2i(rect.position+Vector2i(split*side,0),
			Vector2i(split if side==0 else rect.size.x-split,rect.size.y))
		var panel := Sprite2D.new()
		panel.texture = ImageTexture.create_from_image(source.get_region(crop))
		panel.centered = false
		panel.scale = native_scale
		panel.position.x = half_width*float(side)
		var material := ShaderMaterial.new()
		material.shader = FABRIC_SHADER
		# Native fabric density changes with the restored art; keep authored
		# world-space excursion, phase and fixed-top span unchanged.
		material.set_shader_parameter("pixel_to_legacy",native_scale/Vector2(2560.0/1672.0,1440.0/941.0))
		panel.material = material
		materials.append(material)
		clip.add_child(panel)
		if side==0:
			left = panel
		else:
			right = panel

func pose(phase: float) -> void:
	for material: ShaderMaterial in materials:
		material.set_shader_parameter("phase",phase*1.0)
	left.position.x = -half_width*opening
	right.position.x = half_width+half_width*opening
