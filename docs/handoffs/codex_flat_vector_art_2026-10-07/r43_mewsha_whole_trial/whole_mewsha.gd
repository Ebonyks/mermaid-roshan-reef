extends RefCounted
## Ignored R43: one complete source image; analytic invisible palette regions only.
const SOURCE := "res://assets_src/flat_vector_r43_mewsha_whole_20261015/mewsha_1024.png"
const SHADER := "res://docs/handoffs/codex_flat_vector_art_2026-10-07/r43_mewsha_whole_trial/mewsha_palette.gdshader"
const VISIBLE := Rect2(168,0,708,1024)
static var source_texture: Texture2D = null

static func make(parent: Control, box_pos: Vector2, box_size: Vector2, colors: Array[Color]) -> TextureRect:
	if source_texture == null:
		var image := Image.load_from_file(SOURCE)
		assert(image != null and image.get_size() == Vector2i(1024,1024))
		source_texture = ImageTexture.create_from_image(image)
	var visual := TextureRect.new()
	visual.name = "R43WholeMewsha"
	visual.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	visual.stretch_mode = TextureRect.STRETCH_SCALE
	visual.texture = source_texture
	var fit: float = minf(box_size.x/VISIBLE.size.x,box_size.y/VISIBLE.size.y)
	visual.position = box_pos+(box_size-VISIBLE.size*fit)*0.5-VISIBLE.position*fit
	visual.size = Vector2(1024,1024)*fit
	visual.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var material := ShaderMaterial.new()
	material.shader = load(SHADER) as Shader
	visual.material = material
	visual.set_meta("source_asset_path",SOURCE)
	visual.set_meta("r43_whole_unit",true)
	visual.set_meta("r43_box",Rect2(box_pos,box_size))
	visual.set_meta("r43_visible_bbox",VISIBLE)
	visual.set_meta("r43_meaningful_visible_rect",Rect2(visual.position+VISIBLE.position*fit,VISIBLE.size*fit))
	apply_colors(visual,colors)
	parent.add_child(visual)
	return visual

static func apply_colors(visual: TextureRect, colors: Array[Color]) -> void:
	assert(colors.size()==3)
	var material := visual.material as ShaderMaterial
	var tokens: Array[String] = []
	for i: int in range(3):
		material.set_shader_parameter(["body_choice","horn_choice","heart_choice"][i],colors[i])
		tokens.append(colors[i].to_html(false))
	visual.set_meta("r43_palette_tokens",tokens)
