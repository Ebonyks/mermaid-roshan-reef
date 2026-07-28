class_name LivingWorldCanvas
extends Control

# One bounded, input-transparent CanvasItem supplies the living-world accents for
# every stage. ReefMain drives it; this node owns no timers, tweens, particles,
# audio, physics, or gameplay state.

var stage_spec: Dictionary = {}
var motion_time := 0.0
var event_progress := -1.0


func configure(spec: Dictionary) -> void:
	stage_spec = spec
	motion_time = 0.0
	event_progress = -1.0
	visible = not spec.is_empty()
	queue_redraw()


func set_motion(next_time: float, next_event_progress: float) -> void:
	motion_time = next_time
	event_progress = next_event_progress
	queue_redraw()


func clear_event() -> void:
	event_progress = -1.0
	queue_redraw()


func _draw() -> void:
	if stage_spec.is_empty():
		return
	var viewport_size: Vector2 = get_viewport_rect().size
	if viewport_size.x < 2.0 or viewport_size.y < 2.0:
		viewport_size = Vector2(1280.0, 720.0)
	var palette: Array = stage_spec.get("palette", [
		Color(0.62, 0.93, 1.0),
		Color(0.92, 0.72, 1.0),
		Color(1.0, 0.93, 0.62),
	])
	var animations: Array = stage_spec.get("animations", [])
	if animations.size() < 2:
		return
	var slow_sway: float = sin(motion_time * 0.58)
	var slow_drift: float = sin(motion_time * 0.34 + 1.7)
	var left_origin := Vector2(
		48.0 + slow_drift * 8.0,
		viewport_size.y * 0.48 + slow_sway * 7.0
	)
	var right_origin := Vector2(
		viewport_size.x - 50.0 + slow_sway * 7.0,
		viewport_size.y * 0.58 + slow_drift * 8.0
	)
	_draw_at(
		String(animations[0].get("motif", "sparkle")),
		left_origin,
		slow_sway * 0.08,
		0.82 + 0.035 * slow_drift,
		_soft_color(Color(palette[0]), 0.30)
	)
	_draw_at(
		String(animations[1].get("motif", "bubble")),
		right_origin,
		slow_drift * 0.07,
		0.68 + 0.04 * slow_sway,
		_soft_color(Color(palette[1]), 0.25)
	)
	if event_progress >= 0.0:
		_draw_idle_event(viewport_size, palette)


func _draw_idle_event(viewport_size: Vector2, palette: Array) -> void:
	var p: float = clampf(event_progress, 0.0, 1.0)
	var envelope: float = sin(p * PI)
	var idle: Dictionary = stage_spec.get("idle_event", {})
	var motion: String = String(idle.get("motion", "peek"))
	var origin := Vector2(viewport_size.x * 0.5, viewport_size.y - 46.0)
	var rotation := 0.0
	var scale := 0.92
	match motion:
		"rise":
			origin = Vector2(viewport_size.x * 0.84, viewport_size.y + 32.0 - envelope * 112.0)
			rotation = sin(p * TAU) * 0.08
		"cross":
			origin = Vector2(-55.0 + (viewport_size.x + 110.0) * p, viewport_size.y * 0.84)
			rotation = sin(p * PI) * 0.12
		"orbit":
			origin = Vector2(
				viewport_size.x * 0.12 + cos(p * TAU) * 44.0,
				viewport_size.y * 0.62 + sin(p * TAU) * 25.0
			)
			rotation = p * TAU
		"bounce":
			origin = Vector2(viewport_size.x * 0.16, viewport_size.y - 38.0 - absf(sin(p * PI * 2.0)) * 74.0)
			rotation = sin(p * TAU) * 0.1
		"burst":
			origin = Vector2(viewport_size.x * 0.88, viewport_size.y * 0.48)
			scale = 0.55 + envelope * 0.75
		_:
			origin = Vector2(viewport_size.x - 25.0 - envelope * 74.0, viewport_size.y * 0.76)
			rotation = -0.1 + envelope * 0.16
	var color := _soft_color(Color(palette[2]), envelope * 0.62)
	_draw_at(String(idle.get("motif", "sparkle")), origin, rotation, scale, color)


func _draw_at(motif: String, origin: Vector2, rotation: float, scale: float, color: Color) -> void:
	draw_set_transform(origin, rotation, Vector2.ONE * scale)
	_draw_motif(motif, color)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_motif(motif: String, color: Color) -> void:
	var outline := _soft_color(color.darkened(0.48), minf(0.72, color.a + 0.18))
	var glow := _soft_color(color.lightened(0.28), color.a * 0.72)
	match motif:
		"bubble":
			draw_circle(Vector2(-8.0, 6.0), 17.0, _soft_color(color, color.a * 0.34))
			draw_arc(Vector2(-8.0, 6.0), 17.0, 0.0, TAU, 24, outline, 2.2, true)
			draw_circle(Vector2(13.0, -15.0), 8.0, _soft_color(color, color.a * 0.25))
			draw_arc(Vector2(13.0, -15.0), 8.0, 0.0, TAU, 16, outline, 1.6, true)
			draw_circle(Vector2(-14.0, -1.0), 3.0, glow)
		"frond":
			var stem := PackedVector2Array([Vector2(0.0, 25.0), Vector2(-2.0, 6.0), Vector2(2.0, -24.0)])
			draw_polyline(stem, outline, 4.0, true)
			for i in range(5):
				var y: float = 15.0 - float(i) * 8.0
				var side: float = -1.0 if i % 2 == 0 else 1.0
				var leaf := PackedVector2Array([
					Vector2(0.0, y + 3.0),
					Vector2(side * (13.0 + float(i)), y - 7.0),
					Vector2(side * 8.0, y + 5.0),
				])
				draw_colored_polygon(leaf, color)
				draw_polyline(PackedVector2Array([leaf[0], leaf[1], leaf[2], leaf[0]]), outline, 1.5, true)
		"leaf":
			var leaf_points := PackedVector2Array([
				Vector2(-22.0, 2.0), Vector2(-7.0, -16.0), Vector2(21.0, -9.0),
				Vector2(13.0, 13.0), Vector2(-8.0, 17.0),
			])
			draw_colored_polygon(leaf_points, color)
			draw_polyline(PackedVector2Array([
				leaf_points[0], leaf_points[1], leaf_points[2], leaf_points[3],
				leaf_points[4], leaf_points[0],
			]), outline, 2.0, true)
			draw_line(Vector2(-16.0, 4.0), Vector2(15.0, -5.0), outline, 1.5, true)
		"flower":
			for i in range(5):
				var angle: float = float(i) * TAU / 5.0 - PI * 0.5
				draw_circle(Vector2(cos(angle), sin(angle)) * 12.0, 9.0, color)
			draw_circle(Vector2.ZERO, 7.0, glow)
			draw_arc(Vector2.ZERO, 7.0, 0.0, TAU, 16, outline, 1.6, true)
		"fish":
			var fish_body := PackedVector2Array([
				Vector2(-18.0, 0.0), Vector2(-7.0, -12.0), Vector2(13.0, -8.0),
				Vector2(22.0, 0.0), Vector2(13.0, 8.0), Vector2(-7.0, 12.0),
			])
			draw_colored_polygon(fish_body, color)
			draw_polyline(PackedVector2Array([
				fish_body[0], fish_body[1], fish_body[2], fish_body[3],
				fish_body[4], fish_body[5], fish_body[0],
			]), outline, 2.0, true)
			var tail := PackedVector2Array([Vector2(-17.0, 0.0), Vector2(-31.0, -11.0), Vector2(-29.0, 12.0)])
			draw_colored_polygon(tail, color)
			draw_circle(Vector2(14.0, -2.0), 2.0, outline)
		"butterfly":
			draw_circle(Vector2.ZERO, 4.0, outline)
			draw_circle(Vector2(-11.0, -7.0), 10.0, color)
			draw_circle(Vector2(11.0, -7.0), 10.0, color)
			draw_circle(Vector2(-9.0, 8.0), 7.0, glow)
			draw_circle(Vector2(9.0, 8.0), 7.0, glow)
			draw_line(Vector2(-1.0, -3.0), Vector2(-7.0, -17.0), outline, 1.4, true)
			draw_line(Vector2(1.0, -3.0), Vector2(7.0, -17.0), outline, 1.4, true)
		"cloud":
			draw_circle(Vector2(-15.0, 2.0), 12.0, color)
			draw_circle(Vector2(0.0, -7.0), 16.0, color)
			draw_circle(Vector2(17.0, 1.0), 11.0, color)
			draw_rect(Rect2(-23.0, 0.0, 48.0, 13.0), color, true)
			draw_arc(Vector2(0.0, 3.0), 25.0, 0.15, PI - 0.15, 20, outline, 1.8, true)
		"ripple", "wave":
			for i in range(3):
				var radius: float = 10.0 + float(i) * 9.0
				draw_arc(Vector2.ZERO, radius, 0.05, PI - 0.05, 18, _soft_color(color, color.a * (1.0 - float(i) * 0.2)), 2.2, true)
		"snow":
			for i in range(3):
				var angle: float = float(i) * PI / 3.0
				var ray := Vector2(cos(angle), sin(angle)) * 22.0
				draw_line(-ray, ray, color, 2.2, true)
			draw_circle(Vector2.ZERO, 4.0, glow)
		"lantern":
			draw_rect(Rect2(-13.0, -17.0, 26.0, 31.0), _soft_color(color, color.a * 0.72), true)
			draw_rect(Rect2(-13.0, -17.0, 26.0, 31.0), outline, false, 2.2)
			draw_arc(Vector2(0.0, -16.0), 10.0, PI, TAU, 12, outline, 2.0, true)
			draw_circle(Vector2.ZERO, 6.0, glow)
		"ember":
			var flame := PackedVector2Array([
				Vector2(0.0, -24.0), Vector2(14.0, -3.0), Vector2(9.0, 17.0),
				Vector2(0.0, 23.0), Vector2(-12.0, 14.0), Vector2(-15.0, -3.0),
			])
			draw_colored_polygon(flame, color)
			draw_polyline(PackedVector2Array([
				flame[0], flame[1], flame[2], flame[3], flame[4], flame[5], flame[0],
			]), outline, 2.0, true)
			draw_colored_polygon(PackedVector2Array([
				Vector2(1.0, -7.0), Vector2(7.0, 5.0), Vector2(0.0, 15.0), Vector2(-6.0, 5.0),
			]), glow)
		"note":
			draw_circle(Vector2(-8.0, 14.0), 8.0, color)
			draw_line(Vector2(-1.0, 12.0), Vector2(-1.0, -21.0), outline, 3.0, true)
			draw_line(Vector2(-1.0, -21.0), Vector2(17.0, -15.0), outline, 3.0, true)
			draw_circle(Vector2(13.0, 18.0), 7.0, glow)
			draw_line(Vector2(19.0, 16.0), Vector2(19.0, -14.0), outline, 3.0, true)
		"curtain", "ribbon", "flag":
			var cloth := PackedVector2Array([
				Vector2(-22.0, -21.0), Vector2(22.0, -17.0), Vector2(17.0, 18.0),
				Vector2(4.0, 12.0), Vector2(-8.0, 21.0), Vector2(-21.0, 14.0),
			])
			draw_colored_polygon(cloth, color)
			draw_polyline(PackedVector2Array([
				cloth[0], cloth[1], cloth[2], cloth[3], cloth[4], cloth[5], cloth[0],
			]), outline, 2.0, true)
			draw_line(Vector2(-12.0, -18.0), Vector2(-14.0, 14.0), glow, 2.0, true)
			draw_line(Vector2(3.0, -18.0), Vector2(1.0, 13.0), glow, 2.0, true)
		"heart":
			var heart := PackedVector2Array([
				Vector2(0.0, 23.0), Vector2(-22.0, 1.0), Vector2(-18.0, -14.0),
				Vector2(-7.0, -20.0), Vector2(0.0, -10.0), Vector2(7.0, -20.0),
				Vector2(18.0, -14.0), Vector2(22.0, 1.0),
			])
			draw_colored_polygon(heart, color)
			draw_polyline(PackedVector2Array([
				heart[0], heart[1], heart[2], heart[3], heart[4], heart[5],
				heart[6], heart[7], heart[0],
			]), outline, 2.0, true)
		"steam":
			for i in range(3):
				var x: float = -14.0 + float(i) * 14.0
				var curl := PackedVector2Array([
					Vector2(x, 20.0), Vector2(x - 5.0, 9.0), Vector2(x + 5.0, -2.0),
					Vector2(x - 3.0, -15.0), Vector2(x + 2.0, -25.0),
				])
				draw_polyline(curl, color, 3.0, true)
		"shell":
			draw_arc(Vector2.ZERO, 23.0, PI, TAU, 24, color, 10.0, true)
			for i in range(5):
				var angle: float = PI + float(i) * PI / 4.0
				draw_line(Vector2(0.0, 8.0), Vector2(cos(angle), sin(angle)) * 22.0, outline, 1.5, true)
			draw_line(Vector2(-23.0, 2.0), Vector2(23.0, 2.0), outline, 2.0, true)
		"candy":
			draw_circle(Vector2.ZERO, 13.0, color)
			draw_arc(Vector2.ZERO, 13.0, 0.0, TAU, 20, outline, 2.0, true)
			draw_colored_polygon(PackedVector2Array([
				Vector2(-12.0, 0.0), Vector2(-29.0, -10.0), Vector2(-27.0, 11.0),
			]), glow)
			draw_colored_polygon(PackedVector2Array([
				Vector2(12.0, 0.0), Vector2(29.0, -10.0), Vector2(27.0, 11.0),
			]), glow)
		"rocket":
			var body := PackedVector2Array([
				Vector2(0.0, -26.0), Vector2(12.0, -7.0), Vector2(9.0, 16.0),
				Vector2(0.0, 23.0), Vector2(-9.0, 16.0), Vector2(-12.0, -7.0),
			])
			draw_colored_polygon(body, color)
			draw_polyline(PackedVector2Array([
				body[0], body[1], body[2], body[3], body[4], body[5], body[0],
			]), outline, 2.0, true)
			draw_circle(Vector2(0.0, -4.0), 5.0, glow)
			draw_colored_polygon(PackedVector2Array([
				Vector2(-6.0, 20.0), Vector2(0.0, 34.0), Vector2(6.0, 20.0),
			]), glow)
		"book":
			draw_colored_polygon(PackedVector2Array([
				Vector2(-25.0, -17.0), Vector2(-2.0, -12.0), Vector2(-2.0, 20.0), Vector2(-25.0, 14.0),
			]), color)
			draw_colored_polygon(PackedVector2Array([
				Vector2(2.0, -12.0), Vector2(25.0, -17.0), Vector2(25.0, 14.0), Vector2(2.0, 20.0),
			]), glow)
			draw_line(Vector2.ZERO + Vector2(0.0, -13.0), Vector2(0.0, 20.0), outline, 2.0, true)
			draw_polyline(PackedVector2Array([
				Vector2(-25.0, -17.0), Vector2(-2.0, -12.0), Vector2(0.0, -13.0),
				Vector2(2.0, -12.0), Vector2(25.0, -17.0),
			]), outline, 2.0, true)
		"crown":
			var crown := PackedVector2Array([
				Vector2(-23.0, 16.0), Vector2(-19.0, -15.0), Vector2(-7.0, 0.0),
				Vector2(0.0, -21.0), Vector2(8.0, 0.0), Vector2(20.0, -15.0), Vector2(23.0, 16.0),
			])
			draw_colored_polygon(crown, color)
			draw_polyline(PackedVector2Array([
				crown[0], crown[1], crown[2], crown[3], crown[4], crown[5], crown[6], crown[0],
			]), outline, 2.0, true)
			draw_circle(Vector2(0.0, 8.0), 4.0, glow)
		"moon":
			draw_circle(Vector2.ZERO, 23.0, color)
			draw_circle(Vector2(-8.0, -6.0), 3.5, glow)
			draw_circle(Vector2(8.0, 7.0), 2.5, _soft_color(glow, glow.a * 0.7))
			draw_arc(Vector2.ZERO, 23.0, 0.0, TAU, 28, outline, 2.0, true)
		"crystal":
			var crystal := PackedVector2Array([
				Vector2(0.0, -27.0), Vector2(18.0, -7.0), Vector2(11.0, 22.0),
				Vector2(-11.0, 22.0), Vector2(-18.0, -7.0),
			])
			draw_colored_polygon(crystal, color)
			draw_polyline(PackedVector2Array([
				crystal[0], crystal[1], crystal[2], crystal[3], crystal[4], crystal[0],
			]), outline, 2.0, true)
			draw_line(Vector2(0.0, -25.0), Vector2(0.0, 20.0), glow, 2.0, true)
		"mushroom":
			draw_arc(Vector2(0.0, -5.0), 22.0, PI, TAU, 24, color, 11.0, true)
			draw_line(Vector2(-7.0, -4.0), Vector2(-5.0, 22.0), outline, 4.0, true)
			draw_line(Vector2(7.0, -4.0), Vector2(5.0, 22.0), outline, 4.0, true)
			draw_circle(Vector2(-8.0, -13.0), 3.0, glow)
			draw_circle(Vector2(9.0, -10.0), 3.0, glow)
		"paw":
			draw_circle(Vector2(0.0, 10.0), 12.0, color)
			draw_circle(Vector2(-15.0, -7.0), 6.0, color)
			draw_circle(Vector2(-5.0, -16.0), 6.0, color)
			draw_circle(Vector2(7.0, -16.0), 6.0, color)
			draw_circle(Vector2(17.0, -6.0), 6.0, color)
		"gear":
			draw_arc(Vector2.ZERO, 19.0, 0.0, TAU, 24, color, 8.0, true)
			draw_circle(Vector2.ZERO, 6.0, outline)
			for i in range(8):
				var angle: float = float(i) * TAU / 8.0
				var start := Vector2(cos(angle), sin(angle)) * 21.0
				var finish := Vector2(cos(angle), sin(angle)) * 29.0
				draw_line(start, finish, outline, 5.0, true)
		"paint":
			draw_circle(Vector2.ZERO, 21.0, color)
			draw_arc(Vector2(10.0, 13.0), 8.0, 0.0, TAU, 16, outline, 2.0, true)
			for p in [Vector2(-10.0, -7.0), Vector2(2.0, -13.0), Vector2(12.0, -4.0)]:
				draw_circle(p, 3.0, glow)
			draw_arc(Vector2.ZERO, 21.0, 0.0, TAU, 28, outline, 2.0, true)
		_:
			_draw_sparkle(color, outline, glow)


func _draw_sparkle(color: Color, outline: Color, glow: Color) -> void:
	var star := PackedVector2Array([
		Vector2(0.0, -27.0), Vector2(6.0, -7.0), Vector2(24.0, 0.0),
		Vector2(6.0, 7.0), Vector2(0.0, 27.0), Vector2(-6.0, 7.0),
		Vector2(-24.0, 0.0), Vector2(-6.0, -7.0),
	])
	draw_colored_polygon(star, color)
	draw_polyline(PackedVector2Array([
		star[0], star[1], star[2], star[3], star[4], star[5], star[6], star[7], star[0],
	]), outline, 2.0, true)
	draw_circle(Vector2.ZERO, 4.0, glow)


func _soft_color(color: Color, alpha: float) -> Color:
	var result := color
	result.a = clampf(alpha, 0.0, 1.0)
	return result
