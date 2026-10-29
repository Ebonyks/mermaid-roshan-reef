class_name ChefPaintedArt
extends RefCounted
## Rendering only. The existing gesture surface remains the input/state owner.

const ROOT := "res://assets/opera/worlds/chef_quality_20261019/"
const CAVITY := [Vector2(99, 449), Vector2(141, 359), Vector2(204, 305),
	Vector2(332, 266), Vector2(481, 252), Vector2(648, 270), Vector2(787, 352),
	Vector2(879, 449), Vector2(890, 530), Vector2(804, 623), Vector2(651, 669),
	Vector2(444, 698), Vector2(275, 665), Vector2(160, 609), Vector2(96, 520)]
const CUP_CAVITY := [Vector2(65, 98), Vector2(69, 90), Vector2(80, 84),
	Vector2(98, 80), Vector2(123, 78), Vector2(148, 82), Vector2(165, 89),
	Vector2(175, 99), Vector2(167, 105), Vector2(144, 111), Vector2(119, 113),
	Vector2(92, 109), Vector2(74, 104)]
var surface: Control
var textures: Dictionary = {}


func bind(owner_surface: Control) -> void:
	surface = owner_surface


func art(name: String) -> Texture2D:
	if not textures.has(name):
		textures[name] = load(ROOT + name + ".png") as Texture2D
	return textures[name] as Texture2D


func value(name: String) -> float:
	return float(surface.get(name))


func picture(name: String, destination: Rect2) -> void:
	var texture := art(name)
	if texture != null:
		surface.draw_texture_rect(texture, destination, false)


func masked_picture(name: String, destination: Rect2, polygon: Array,
		reveal: Rect2, native_side: float) -> void:
	var texture := art(name)
	if texture == null:
		return
	var window := PackedVector2Array([reveal.position,
		Vector2(reveal.end.x, reveal.position.y), reveal.end,
		Vector2(reveal.position.x, reveal.end.y)])
	for clipped: PackedVector2Array in Geometry2D.intersect_polygons(
			PackedVector2Array(polygon), window):
		var vertices := PackedVector2Array()
		var uvs := PackedVector2Array()
		for point: Vector2 in clipped:
			vertices.append(destination.position + point / native_side * destination.size)
			uvs.append(point / native_side)
		surface.draw_polygon(vertices, PackedColorArray([Color.WHITE]), uvs, texture)


func draw_meter(heat: float) -> void:
	var destination: Rect2 = surface.call("_oven_meter_rect")
	# Native regions reveal the same registered tube; no whole-object ghosting.
	var bottom := 496.0
	var top := lerpf(bottom, 284.0, heat / 0.45) if heat < 0.45 else (
		lerpf(284.0, 160.0, (heat - 0.45) / 0.35) if heat <= 0.80 else
		lerpf(160.0, 104.0, (heat - 0.80) / 0.20))
	for row: Array in [["thermometer_empty", 0.0, top],
			["thermometer_full", top, 512.0 - top]]:
		var source := Rect2(0, float(row[1]), 128, float(row[2]))
		if source.size.y > 0.0:
			surface.draw_texture_rect_region(art(String(row[0])),
				Rect2(destination.position + Vector2(0, source.position.y / 512.0 * destination.size.y),
					Vector2(destination.size.x, source.size.y / 512.0 * destination.size.y)), source)


func draw_oven() -> void:
	var heat := clampf(value("oven_t"), 0.0, 1.0)
	var state := "oven_cool" if heat < 0.45 else "oven_warm"
	if value("oven_peek") > 0.0 or bool(surface.get("completion_accepted")):
		state = "oven_open"
	var handle: Rect2 = surface.call("_oven_handle_rect")
	var side := minf(surface.size.x * 0.76, surface.size.y * 0.84)
	picture(state, Rect2(handle.get_center()
		- Vector2(0.499919735, 0.746334546) * side, Vector2.ONE * side))
	draw_meter(heat)


func bowl_rect() -> Rect2:
	var mouth: Rect2 = surface.call("_pour_bowl_rect")
	var side := mouth.size.x / 0.78
	return Rect2(Vector2(mouth.get_center().x, mouth.position.y + 16.0)
		- Vector2(0.5, 0.46875) * side, Vector2.ONE * side)


func draw_pour() -> void:
	var destination := bowl_rect()
	picture("bowl_empty", destination)
	var amount := clampf(value("pour_level"), 0.0, 1.0)
	if amount > 0.0:
		var top := lerpf(700.0, 250.0, amount)
		masked_picture("bowl_unstirred", destination, CAVITY,
			Rect2(0, top, 1024, 1024 - top), 1024.0)
	draw_pour_stream()
	draw_pitcher()


func draw_pitcher() -> void:
	var pitcher: Rect2 = surface.call("_pour_pitcher_rect")
	var rotation := float(surface.call("_pour_pitcher_rotation"))
	var full := surface.get("widget_mover") as Texture2D
	surface.draw_set_transform(pitcher.get_center(), rotation)
	var local := Rect2(-pitcher.size * 0.5, pitcher.size)
	if full != null:
		surface.draw_texture_rect(full, local, false)
	# Reveal only the emptied batter cavity; every original exterior pixel stays.
	var amount := clampf(value("pour_level"), 0.0, 1.0)
	if amount > 0.0:
		masked_picture("pitcher_empty", local, CUP_CAVITY,
			Rect2(0, 0, 256, lerpf(78.0, 114.0, amount)), 256.0)
	surface.draw_set_transform(Vector2.ZERO)


func draw_pour_stream() -> void:
	if not bool(surface.call("_pour_stream_active")) or value("pour_level") >= 1.0:
		return
	var spout: Vector2 = surface.call("_pour_spout_point")
	var landing: Vector2 = surface.call("_pour_landing_point")
	var flow := landing - spout
	var scale_factor := 7.0 / 42.0
	var remaining := flow.length()
	var travelled := 0.0
	surface.draw_set_transform(spout, flow.angle() - PI * 0.5, Vector2.ONE * scale_factor)
	while remaining > 0.01:
		var native_length := minf(496.0, remaining / scale_factor)
		surface.draw_texture_rect_region(art("batter_stream"),
			Rect2(-21, travelled / scale_factor, 42, native_length),
			Rect2(11, 8, 42, native_length))
		travelled += native_length * scale_factor
		remaining -= native_length * scale_factor
	surface.draw_set_transform(Vector2.ZERO)
	for index in range(3):
		var fraction := fposmod(value("demo_t") * 1.8 + float(index) / 3.0, 1.0)
		var point := spout.lerp(landing, fraction)
		picture("batter_drop", Rect2(point - Vector2.ONE * 9, Vector2.ONE * 18))
	picture("batter_splash", Rect2(landing - Vector2(17, 22), Vector2.ONE * 34))


func draw_stir() -> void:
	var destination := bowl_rect()
	picture("bowl_stirred" if bool(surface.get("completion_accepted")) else "bowl_unstirred", destination)
	var tool := surface.get("widget_mover") as Texture2D
	if tool == null:
		return
	var action: Rect2 = surface.call("_crank_action_rect")
	var angle := value("crank_rotation")
	var contact := Vector2(destination.get_center().x, destination.position.y + destination.size.y * 0.47)
	var handle := contact + Vector2(cos(angle) * action.size.x * 0.36,
		sin(angle) * action.size.y * 0.30)
	var side := minf(action.size.x, action.size.y) * 0.68
	var tool_angle := (contact - handle).angle() - Vector2(0.70, -0.67).angle()
	surface.draw_set_transform(handle, tool_angle)
	surface.draw_texture_rect(tool, Rect2(-Vector2(0.16, 0.84) * side, Vector2.ONE * side), false)
	surface.draw_set_transform(Vector2.ZERO)


func cake_rect() -> Rect2:
	var side := minf(surface.size.x * 0.76, surface.size.y * 0.92)
	return Rect2(surface.size * Vector2(0.5, 0.53) - Vector2.ONE * side * 0.5,
		Vector2.ONE * side)


func draw_frost() -> void:
	picture("cake_frosted" if bool(surface.get("completion_accepted")) else "cake_unfrosted", cake_rect())
	draw_frost_path()


func draw_frost_path() -> void:
	if bool(surface.get("completion_accepted")):
		return
	var points: PackedVector2Array = surface.call("_trace_path_points", value("trace_journey"))
	var distance_since := 14.0
	for index in range(1, points.size()):
		var previous := points[index - 1]
		var delta := points[index] - previous
		var length := delta.length()
		if length < 0.01:
			continue
		var travelled := maxf(0.0, 14.0 - distance_since)
		while travelled <= length:
			var at := previous + delta / length * travelled
			surface.draw_set_transform(at, delta.angle())
			picture("frosting_segment", Rect2(-10, -10, 20, 20))
			travelled += 14.0
		distance_since = length - (travelled - 14.0)
	surface.draw_set_transform(Vector2.ZERO)
	var progress := value("trace_journey")
	var at: Vector2 = surface.call("_trace_demo_point", progress)
	var following: Vector2 = surface.call("_trace_demo_point", minf(1.0, progress + 0.01))
	var tangent := following - at
	if tangent.length_squared() < 0.01:
		tangent = Vector2.DOWN
	if progress > 0.001:
		var start: Vector2 = surface.call("_trace_demo_point", 0.0)
		var next_start: Vector2 = surface.call("_trace_demo_point", 0.01)
		surface.draw_set_transform(start, (next_start - start).angle())
		picture("frosting_cap_start", Rect2(-10, -10, 20, 20))
		surface.draw_set_transform(at, tangent.angle())
		picture("frosting_cap_end", Rect2(-10, -10, 20, 20))
	surface.draw_set_transform(at, tangent.angle() - Vector2(-1, 1).angle())
	var side := 64.0
	picture("piping_bag", Rect2(-Vector2(0.029601555, 0.935259806) * side, Vector2.ONE * side))
	surface.draw_set_transform(Vector2.ZERO)


func draw_targets() -> void:
	picture("cake_frosted", cake_rect())
	var placed: Array = surface.get("target_placed")
	var animations: Array = surface.get("target_piece_anim")
	for index in range(placed.size()):
		if not bool(placed[index]):
			continue
		var texture := surface.call("_target_piece_texture", index) as Texture2D
		var destination: Rect2 = surface.call("_target_piece_rect", index)
		var settle := clampf(1.0 - float(animations[index]) / 0.42, 0.0, 1.0)
		var factor := 1.0 + 0.12 * pow(sin(settle * PI), 2.0)
		destination = Rect2(destination.get_center() - destination.size * factor * 0.5,
			destination.size * factor)
		if texture != null:
			surface.draw_texture_rect(texture, destination, false)


func draw_hand(at: Vector2) -> void:
	picture("guide_hand", Rect2(at - Vector2(0.436523438, 0.986328125) * 58.0,
		Vector2.ONE * 58.0))
