class_name OperaRoutePresentation
extends RefCounted
## Shared presentation handoff for room launches and temporary job playtests.

static func suspend(m: ReefMain) -> void:
	if m.hud_layer != null:
		m.opera_hud_was_visible = m.hud_layer.visible
		m.opera_hud_previous_layer = m.hud_layer.layer
		m.opera_hud_game_was_visible = m.hud_game != null and m.hud_game.visible
		m.opera_obj_was_visible = m.obj_card != null and m.obj_card.visible
		m.hud_layer.layer = 12
		m.hud_layer.visible = true
		if m.hud_game != null:
			m.hud_game.visible = false
		if m.obj_card != null:
			m.obj_card.visible = false
	if m.hud_msg != null:
		m.hud_msg.text = ""
		m.hud_msg.visible = false
	m.opera_player_was_visible = m.player != null and m.player.visible
	if m.player != null:
		m.player.visible = false
	m._sync_pause_surface_layer()
