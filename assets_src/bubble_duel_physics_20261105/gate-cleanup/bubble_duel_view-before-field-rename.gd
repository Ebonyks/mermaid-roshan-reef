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
	_draw_power_effects()
	for fighter: BubbleDuelFighter in world.fighters:
		if fighter.lost: continue
		var root: Vector2 = _root(fighter)
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
		if fighter.hover_last:
			draw_arc(at, 30, 0, TAU, 28, Color(0.75, 0.96, 1.0, 0.55), 2, true)
		if fighter.invincible > 0:
			draw_arc(at, 26, 0, TAU, 28, Color(0.85, 1.0, 1.0, 0.65), 2, true)
		if fighter.held > 0:
			draw_texture_rect(host._icon(6), Rect2(at - Vector2(22, 22), Vector2(44, 44)), false, Color(1, 1, 1, 0.75))
		var badge_x: float = (-36.0 if fighter.human == 0 else 36.0) if fighter.human >= 0 else (36.0 if fighter.facing > 0 else -36.0)
		var badge: Vector2 = at + Vector2(badge_x, -8)
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


func _draw_power_effects() -> void:
	for effect: Dictionary in host.power_effects:
		if float(effect["life"]) <= 0.0: continue
		var actor: BubbleDuelFighter = host.world.fighters[int(effect["actor"])]
		var root: Vector2 = _root(actor)
		var start: Vector2 = TOP + (root + Vector2(actor.shot_tip.x * actor.facing, actor.shot_tip.y)) * ZOOM
		var progress: float = 1.0 - float(effect["life"])
		var alpha: float = minf(0.65, float(effect["life"]))
		match String(effect["gear"]):
			"kelp":
				var target: int = int(effect["target"])
				if target < 0: continue
				var end: Vector2 = TOP + _root(host.world.fighters[target]) * ZOOM
				var points := PackedVector2Array()
				for index: int in range(13):
					var weight: float = float(index) / 12
					points.append(start.lerp(end, weight) + Vector2(0, sin(weight * PI) * 18))
				draw_polyline(points, Color(0.42, 0.82, 0.46, alpha), 3, true)
			"lullaby":
				for index: int in range(3):
					var radius: float = 10 + fposmod(progress * 70 + index * 22, 70)
					draw_arc(start, radius, -PI, PI, 24, Color(0.86, 0.77, 1, alpha * 0.6), 2, true)
			"squid":
				var target: int = int(effect["target"])
				if target >= 0:
					var end: Vector2 = TOP + _root(host.world.fighters[target]) * ZOOM
					draw_texture_rect(host._icon(6), Rect2(end - Vector2(28, 28), Vector2(56, 56)), false, Color(1, 1, 1, alpha))
			"swiftconch":
				for index: int in range(3):
					var point: Vector2 = TOP + root * ZOOM - Vector2(actor.facing * (18 + index * 15), 0)
					draw_arc(point, 4 + index * 2, 0, TAU, 12, Color(0.68, 0.96, 1, alpha * 0.5), 2, true)


func _root(fighter: BubbleDuelFighter) -> Vector2:
	if absf(fighter.position.x - fighter.previous.x) < 100 and absf(fighter.position.y - fighter.previous.y) < 100:
		return fighter.previous.lerp(fighter.position, blend)
	return fighter.position
