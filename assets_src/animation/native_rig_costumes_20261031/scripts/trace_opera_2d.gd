extends "res://scripts/probe_opera_2d.gd"
## Diagnostic only: original assertions, driver and rectangles remain unchanged.

func _finale_partner_present(world: OperaCareerWorld2D, career: String) -> bool:
	var present: bool = super._finale_partner_present(world, career)
	if career == "geologist":
		var player_rect: Rect2 = super._actor_visual_rect(world.player_actor)
		var rival_rect: Rect2 = super._actor_visual_rect(world.rival_actor)
		var canvas: Rect2 = Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
		print("GEO_DIAGNOSTIC|", JSON.stringify({
			"phase":world.phase_index,
			"task_open":world.task_open,
			"finale":world.in_competition_finale(),
			"player_visible":world.player_actor.visible,
			"rival_visible":world.rival_actor.visible,
			"player_rect":[player_rect.position.x,player_rect.position.y,player_rect.size.x,player_rect.size.y],
			"rival_rect":[rival_rect.position.x,rival_rect.position.y,rival_rect.size.x,rival_rect.size.y],
			"player_inside":super._rect_inside(player_rect,canvas),
			"rival_inside":super._rect_inside(rival_rect,canvas),
			"overlap":player_rect.intersects(rival_rect)
		}))
	return present
