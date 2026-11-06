class_name BubbleDuelView
extends Control
## A clipped true-2D playfield. Menus and two finger pads remain on the parent.
const ZOOM: float = 2.1
const TOP := Vector2(0, 72)
const MAGNIFY: float = 0.58
var host: BubbleDuelOverlay
var blend: float = 0.0


func _draw() -> void:
	if host == null or host.world == null: return
	var world: BubbleDuelArena = host.world
	draw_rect(Rect2(0, 0, 840, 720), Color(0.04, 0.22, 0.31, 0.11))
	draw_line(Vector2(0, 114), Vector2(840, 114), Color(0.7, 0.95, 1, 0.17), 2)
	for fighter: BubbleDuelFighter in world.fighters:
		if fighter.lost: continue
		var root: Vector2 = fighter.position
		if absf(root.x - fighter.previous.x) < 100.0 and absf(root.y - fighter.previous.y) < 100.0:
			root = fighter.previous.lerp(root, blend)
		var offset: Vector2 = root - fighter.position
		var at: Vector2 = TOP + root * ZOOM
		var color: Color = host.COLORS[clampi(int(fighter.profile.get("color", 0)), 0, 4)]
		for side: int in world.SIDES:
			if not world._side_exists(fighter, side): continue
			var point: Vector2 = TOP + (world.bubble_position(fighter, side) + offset) * ZOOM
			var radius: float = world.bubble_radius(fighter) * ZOOM
			draw_line(point + Vector2(0, radius * 0.8), at + Vector2(0, -8), Color(0.25, 0.42, 0.38), 2, true)
			draw_texture_rect(host.bubble, Rect2(point - Vector2.ONE * radius, Vector2.ONE * radius * 2), false, color)
		var draw_at: Vector2 = at + Vector2(fighter.draw_offset.x * fighter.facing, fighter.draw_offset.y) * ZOOM
		host.appearance.draw_actor(self, fighter.profile, draw_at, fighter.facing,
			fighter.moving_pose, fighter.draw_clock, MAGNIFY)
		if fighter.invincible > 0:
			draw_arc(at, 26, 0, TAU, 28, Color(0.85, 1.0, 1.0, 0.65), 2, true)
		if fighter.held > 0:
			draw_texture_rect(host._icon(6), Rect2(at - Vector2(22, 22), Vector2(44, 44)), false, Color(1, 1, 1, 0.75))
		var badge: Vector2 = at + Vector2(36 if fighter.facing > 0 else -36, -8)
		draw_circle(badge, 9, Color(0.20, 0.65, 0.86) if fighter.team == 0 else Color(0.91, 0.46, 0.64))
		for dot: int in range(1 + maxi(0, fighter.human)):
			draw_circle(badge + Vector2(float(dot) * 7.0 - (3.5 if fighter.human == 1 else 0.0), 0), 2, Color.WHITE)
	for shot: Dictionary in world.shots:
		if int(shot["life"]) <= 0: continue
		var at: Vector2 = TOP + (shot["position"] as Vector2) * ZOOM
		draw_texture_rect(host.PEARL, Rect2(at - Vector2(10, 10), Vector2(20, 20)), false)
	for index: int in range(host.bonus_items.size()):
		var item: Dictionary = host.bonus_items[index]
		if not bool(item["active"]): continue
		var at: Vector2 = TOP + (item["position"] as Vector2) * ZOOM
		var art: Texture2D = host.PEARL if item["kind"] == "pearl" else host._icon(6)
		draw_texture_rect(art, Rect2(at - Vector2(20, 20), Vector2(40, 40)), false)
	for effect: Dictionary in host.duo_pops:
		var progress: float = (0.32 - float(effect["time"])) / 0.32
		var at: Vector2 = TOP + (effect["position"] as Vector2) * ZOOM
		draw_texture_rect_region(host.POP, Rect2(at - Vector2(40, 40), Vector2(80, 80)),
			host._cell(mini(7, int(progress * 8)), 4))
