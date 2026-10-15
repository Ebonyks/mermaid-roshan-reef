extends "res://docs/handoffs/codex_flat_vector_art_2026-10-07/r42_companion_preview_fit/companion_preview_fit.gd"
const WholeMewsha = preload("res://docs/handoffs/codex_flat_vector_art_2026-10-07/r43_mewsha_whole_trial/whole_mewsha.gd")
func _init(main: ReefMain) -> void:
	super(main)

func _add_creature_preview(parent: Control, d: Dictionary, box_pos: Vector2, box_size: Vector2, body: Color, accent: Color) -> void:
	if String(d.get("id","")) != "mewsha":
		super._add_creature_preview(parent,d,box_pos,box_size,body,accent)
		return
	parent.clip_contents = true
	var third: Color = d["third"] as Color
	if not parent is Button:
		if m.companion_layer != null and m.companion_pick_id == "mewsha" and m.companion_pick_colors.size()==3:
			third = Color.html(String(m.companion_pick_colors[2]))
		elif m.companion_id == "mewsha":
			third = colors()[2]
	var palette: Array[Color] = [body,accent,third]
	WholeMewsha.make(parent,box_pos,box_size,palette)
