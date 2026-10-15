extends "res://scripts/arena/castle_rooms_25d.gd"
const WholeMewsha = preload("res://docs/handoffs/codex_flat_vector_art_2026-10-07/r43_mewsha_whole_trial/whole_mewsha.gd")
func _init(main: ReefMain) -> void:
	super(main)

func sync_castle_companion_card() -> void:
	super.sync_castle_companion_card()
	if m.companion_id != "mewsha" or m.castle_companion_card == null or not is_instance_valid(m.castle_companion_card):
		return
	var card: Control = m.castle_companion_card
	if card.get_child_count()!=1 or not card.get_child(0).has_meta("r43_whole_unit"):
		for child: Node in card.get_children():
			child.free()
		WholeMewsha.make(card,Vector2.ZERO,CASTLE_COMPANION_CARD_SIZE,m._companion_ref().colors())
	else:
		WholeMewsha.apply_colors(card.get_child(0) as TextureRect,m._companion_ref().colors())
	card.set_meta("source_asset_paths",[WholeMewsha.SOURCE])
	card.set_meta("source_asset_path",WholeMewsha.SOURCE)
	card.set_meta("r43_whole_unit",true)
