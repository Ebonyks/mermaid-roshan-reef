extends "res://scripts/companion.gd"
## R42 ignored fit-only trial: original complete drawing, requested box, unchanged identity.
func _init(main: ReefMain) -> void:
	super(main)

func _add_creature_preview(parent: Control, d: Dictionary, box_pos: Vector2, box_size: Vector2, body: Color, accent: Color) -> void:
	if not d.has("sprite"):
		super._add_creature_preview(parent, d, box_pos, box_size, body, accent)
		return
	parent.clip_contents = true
	var direct := TextureRect.new()
	direct.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	direct.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	direct.texture = load(FashionOutfitRenderer.path(m, String(d["sprite"])))
	direct.position = box_pos
	direct.size = box_size
	direct.mouse_filter = Control.MOUSE_FILTER_IGNORE
	direct.set_meta("r42_expected_box", Rect2(box_pos, box_size))
	parent.add_child(direct)
