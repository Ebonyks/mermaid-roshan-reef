extends Control
# Canvas presenter for the developed KartGame. Simulation/state stay on KartGame.
# All positions and draw transforms are 2D; no model, spatial camera or light fallback.
const BASE := Vector2(1280, 720)
const INK := Color(0.16, 0.13, 0.32)
const ART_ROOT := "res://assets/kart/canvas/"
var race: Node
var focus := Vector2.ZERO
var view_scale := 7.8
var speed_zoom := 1.0
var _road: PackedVector2Array = []
var _inner: PackedVector2Array = []
var _podium_age := 0.0
var _edge_l: PackedVector2Array = []
var _edge_r: PackedVector2Array = []
var _textures: Dictionary = {}
var _regions: Dictionary = {}
var _drivers: Dictionary = {}
var _driver_regions: Dictionary = {}
var _panels: Dictionary = {}
var _bursts: Array[Dictionary] = []
var _time := 0.0

func setup(engine: Node) -> void:
	race = engine
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	for vehicle in ["kart", "moto"]:
		for view in ["front", "side", "rear", "top", "quarter"]:
			var key: String = vehicle + "_" + view
			var texture: Texture2D = load(ART_ROOT + key + ".png")
			_textures[key] = texture
			_regions[key] = Rect2(texture.get_image().get_used_rect())
	for i in range(int(race.SAMPLES) + 1):
		var s: float = race._cum[i]
		var width: float = race._width_at(s)
		_edge_l.append(race._frame_at(s, -width)[0])
		_edge_r.append(race._frame_at(s, width)[0])
	var inner_right := PackedVector2Array()
	for i in range(int(race.SAMPLES) + 1):
		var at: float = race._cum[i]
		var width: float = race._width_at(at) - 0.8
		_inner.append(race._frame_at(at, -width)[0])
		inner_right.append(race._frame_at(at, width)[0])
	inner_right.reverse()
	_inner.append_array(inner_right)
	_road.append_array(_edge_l)
	var reverse_edge := _edge_r.duplicate()
	reverse_edge.reverse()
	_road.append_array(reverse_edge)

func follow(delta: float) -> void:
	if race == null or race._pl == null:
		return
	var player: Dictionary = race._pl
	var frame: Array = race._kart_frame(float(player["s"]), float(player["lat"]) * 0.35)
	var spd: float = clampf(float(player["speed"]) / (float(race._vmax) * 1.5), 0.0, 1.0)
	var boost: bool = float(player["boost_t"]) > 0.0
	var target_zoom: float = 1.0 - 0.20 * spd - (0.08 if boost else 0.0)
	speed_zoom = lerpf(speed_zoom, target_zoom, clampf(delta * 5.0, 0.0, 1.0))
	view_scale = 7.8 * speed_zoom
	var want: Vector2 = (frame[0] as Vector2) + (frame[1] as Vector2) * 18.0
	focus = focus.lerp(want, clampf(delta * 4.0, 0.0, 1.0))
	queue_redraw()

func burst(point: Vector2, color: Color) -> void:
	# One bounded draw list, rather than transient particle nodes per reward.
	if _bursts.size() >= 12:
		_bursts.pop_front()
	_bursts.append({"point": point, "color": color, "t": 0.45})

func _process(delta: float) -> void:
	_time += delta
	if race != null and race._state == "podium":
		_podium_age += delta
	for i in range(_bursts.size() - 1, -1, -1):
		_bursts[i]["t"] = float(_bursts[i]["t"]) - delta
		if float(_bursts[i]["t"]) <= 0.0:
			_bursts.remove_at(i)
	queue_redraw()

func _screen(point: Vector2) -> Vector2:
	var shake: float = float(race._shake) * sin(_time * 45.0) * 7.0
	return BASE * 0.5 + (point - focus) * view_scale + Vector2(shake, 0)

func _mapped(points: PackedVector2Array) -> PackedVector2Array:
	var result := PackedVector2Array()
	for p in points:
		result.append(_screen(p))
	return result

func _draw() -> void:
	if race == null:
		return
	var fit: float = minf(size.x / BASE.x, size.y / BASE.y)
	draw_set_transform((size - BASE * fit) * 0.5, 0.0, Vector2.ONE * fit)
	var rainbow: bool = race._theme() == "rainbow"
	draw_rect(Rect2(-BASE, BASE * 3.0), Color(0.69, 0.76, 0.95) if rainbow else Color(0.48, 0.81, 0.88))
	# Sparse, native Canvas environment. The undersized raster circuit is not upscaled.
	for i in range(14):
		var p := _screen(Vector2(sin(float(i) * 2.7) * 180.0, cos(float(i) * 1.8) * 190.0))
		var col := Color(0.83, 0.86, 1.0, 0.65) if rainbow else Color(0.68, 0.93, 0.90, 0.65)
		draw_circle(p, 35.0 + float(i % 3) * 14.0, col)
	if race._state == "select":
		_draw_choices()
		return
	if race._state == "podium" and _podium_age >= 0.65:
		_draw_podium()
		return
	_draw_course(rainbow)
	_draw_track_objects()
	var order: Array = race._karts.duplicate()
	order.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return (a["node"] as Node2D).position.y < (b["node"] as Node2D).position.y)
	for k in order:
		_draw_racer(k)
	_draw_minimap()
	for effect in _bursts:
		var p := _screen(effect["point"])
		var age: float = 1.0 - float(effect["t"]) / 0.45
		var c: Color = effect["color"]
		c.a = 1.0 - age
		for j in range(7):
			var d := Vector2.from_angle(float(j) * TAU / 7.0)
			draw_circle(p + d * age * 44.0, 4.0 * (1.0 - age), c)
	if race._pl != null and float(race._pl["boost_t"]) > 0.0:
		for i in range(6):
			var y: float = 80.0 + float(i) * 90.0
			draw_line(Vector2(12, y), Vector2(50, y + 20), Color(1, 1, 1, 0.6), 4.0, true)
			draw_line(Vector2(1228, y), Vector2(1266, y + 20), Color(1, 1, 1, 0.6), 4.0, true)

func _draw_course(rainbow: bool) -> void:
	draw_colored_polygon(_mapped(_road), INK)
	draw_colored_polygon(_mapped(_inner), Color(0.94, 0.84, 0.96) if rainbow else Color(0.93, 0.91, 0.73))
	for i in range(0, int(race.SAMPLES), 4):
		var a: Vector2 = race._lut[i]
		var b: Vector2 = race._lut[(i + 2) % int(race.SAMPLES)]
		draw_line(_screen(a), _screen(b), Color(1, 1, 1, 0.68), 2.5, true)
	var left := _mapped(_edge_l)
	var edge := _mapped(_edge_r)
	draw_polyline(left, Color(0.85, 0.40, 0.64), 7.0, true)
	draw_polyline(edge, Color(0.65, 0.50, 0.87), 7.0, true)
	# Finish line is perpendicular to the road, with a persistent painted arch motif.
	var fr: Array = race._frame_at(0.0, 0.0)
	var center := _screen(fr[0])
	var sideways: Vector2 = (fr[2] as Vector2).normalized()
	var forward: Vector2 = fr[1]
	for i in range(12):
		for j in range(2):
			var pos: Vector2 = center + sideways * (float(i) - 5.5) * 12.0 + forward * (float(j) - 0.5) * 12.0
			var fit: float = minf(size.x / BASE.x, size.y / BASE.y)
			draw_set_transform((size - BASE * fit) * 0.5 + pos * fit, sideways.angle(), Vector2.ONE * fit)
			draw_rect(Rect2(-6, -6, 12, 12), Color.WHITE if (i + j) % 2 == 0 else INK)
	var fit: float = minf(size.x / BASE.x, size.y / BASE.y)
	draw_set_transform((size - BASE * fit) * 0.5, 0.0, Vector2.ONE * fit)

func _draw_track_objects() -> void:
	for strip in race._strip_data:
		var p := _screen(strip["pos"])
		draw_circle(p, 24, Color(0.23, 0.75, 0.86, 0.75))
		_glyph(p, "➜", 36, Color(0.92, 1, 1))
	for ramp in race._ramp_data:
		var p := _screen(ramp["pos"])
		var triangle := PackedVector2Array([p + Vector2(-32, 14), p + Vector2(0, -25), p + Vector2(32, 14)])
		draw_colored_polygon(triangle, Color(1, 0.78, 0.28))
		draw_polyline(PackedVector2Array([triangle[0], triangle[1], triangle[2]]), INK, 4.0, true)
		_glyph(p + Vector2(0, -42), "↑", 26, Color.WHITE)
	for pickup in race._pickups_live:
		var node: Node2D = pickup["node"]
		if not node.visible:
			continue
		var p := _screen(node.position) + Vector2(0, sin(_time * 2.0 + float(pickup["s"])) * 3.0 - 14.0)
		var kind: String = pickup["kind"]
		if kind == "bubble":
			draw_circle(p, 20.0, Color(0.79, 0.98, 1, 0.74))
			draw_arc(p, 20.0, 0, TAU, 20, Color.WHITE, 3.0, true)
			draw_circle(p + Vector2(-6, -7), 5, Color.WHITE)
		elif kind == "shell":
			_glyph(p, "◉", 42, Color(1, 0.72, 0.77))
		else:
			var col := Color.from_hsv(fposmod(_time * 0.5, 1.0), 0.65, 1.0) if kind == "rainbow" else Color(1, 0.88, 0.3)
			_glyph(p, "★", 46, col)
	for pearl in race._pearls_live:
		if bool(pearl["got"]):
			continue
		var p := _screen((pearl["node"] as Node2D).position) + Vector2(0, -10)
		draw_circle(p, 11, Color(0.72, 0.57, 0.86))
		draw_circle(p + Vector2(-1, -2), 8, Color(1, 0.89, 0.97))
		draw_circle(p + Vector2(-3, -5), 3, Color.WHITE)
	for hazard in race._hazards_live:
		_draw_hazard(hazard)
	if race.has_meta("gate_pos") and not bool(race._rev):
		var p := _screen(race.get_meta("gate_pos"))
		draw_arc(p, 31, 0, TAU, 32, Color(0.21, 0.65, 0.58), 9, true)
		_glyph(p, "➜", 30, Color.WHITE)

func _draw_hazard(h: Dictionary) -> void:
	var node: Node2D = h["node"]
	if not node.visible:
		return
	var fit: float = minf(size.x / BASE.x, size.y / BASE.y)
	draw_set_transform((size - BASE * fit) * 0.5 + _screen(node.position) * fit, 0.0, node.scale * fit)
	var p := Vector2.ZERO
	var kind: String = h["kind"]
	match kind:
		"geyser":
			draw_circle(p, 24, Color(0.55, 0.45, 0.53))
			if bool(h.get("erupting", false)):
				for i in range(5):
					draw_circle(p + Vector2(sin(float(i) * 2.2) * 12, -14 - float(i) * 12), 8, Color(0.75, 0.96, 1))
		"kelp":
			for i in range(4):
				var x: float = float(i - 2) * 20.0
				draw_line(p + Vector2(x, 16), p + Vector2(x + sin(_time + float(i)) * 9, -32), Color(0.26, 0.45, 0.41), 13, true)
		"cloud":
			for i in range(3):
				draw_circle(p + Vector2(float(i - 1) * 17, -9), 20, Color(0.59, 0.53, 0.72))
			_glyph(p + Vector2(0, -34), "z", 24, Color.WHITE)
		"whirl":
			for i in range(4):
				draw_arc(p, 10.0 + float(i) * 7.0, _time + float(i), _time + float(i) + PI * 1.6, 24, Color(0.32, 0.37, 0.55), 5, true)
		"jelly":
			draw_circle(p, 26, Color(0.71, 0.36, 0.63))
			draw_arc(p, 20, PI, TAU, 20, Color(0.95, 0.66, 0.83), 5, true)
		_:
			var poly := PackedVector2Array()
			for i in range(12):
				poly.append(p + Vector2.from_angle(float(i) * TAU / 12.0 + node.rotation) * (28.0 if i % 2 == 0 else 17.0))
			draw_colored_polygon(poly, Color(0.38, 0.27, 0.46))
			if kind == "crab":
				draw_circle(p + Vector2(-9, -7), 5, Color.WHITE)
				draw_circle(p + Vector2(9, -7), 5, Color.WHITE)

	draw_set_transform((size - BASE * fit) * 0.5, 0.0, Vector2.ONE * fit)

func _draw_racer(k: Dictionary) -> void:
	var node: Node2D = k["node"]
	var p := _screen(node.position)
	var player: bool = bool(k["is_player"])
	var lift: float = float(k.get("lift", 0.0)) * view_scale
	var width: float = float(race._veh(k)["size"]) * view_scale * 1.75
	# Contact shadow stays on the road through the ramp arc.
	var fit: float = minf(size.x / BASE.x, size.y / BASE.y)
	draw_set_transform((size - BASE * fit) * 0.5 + p * fit, 0.0, Vector2(fit, fit * 0.4))
	draw_circle(Vector2.ZERO, width * 0.32, Color(0.16, 0.14, 0.32, 0.20))
	draw_set_transform((size - BASE * fit) * 0.5, 0.0, Vector2.ONE * fit)
	p.y -= lift
	if player:
		draw_arc(p + Vector2(0, 6), width * 0.52, 0, TAU, 32, Color(1, 0.96, 0.67), 4, true)
	var rear_view: bool = Vector2.from_angle(node.rotation).y < -0.84
	if not rear_view:
		_draw_driver(node, p, width)
	_draw_vehicle(String(k["veh"]), p + Vector2(0, 12), width, node.rotation, node.get_meta("paint", {}))
	if rear_view:
		_draw_driver(node, p + Vector2(0, -width * 0.30), width, true)
	if player:
		_glyph(p + Vector2(0, -width * 0.55), "▼", 22, Color(1, 0.92, 0.34))
	if bool(k.get("drift", false)):
		var tier: int = int(k.get("spray_tier", 0))
		var col: Color = race.DRIFT_COLS[tier]
		for i in range(5):
			var forward := Vector2.from_angle(node.rotation)
			draw_circle(p - forward * (width * 0.25 + float(i) * 8) + forward.orthogonal() * sin(_time * 20 + float(i)) * 9, 3.5, col)

func _draw_driver(node: Node2D, p: Vector2, width: float, head_only: bool = false) -> void:
	var path: String = node.get_meta("sprite_path", "")
	if path.is_empty():
		return
	if not _drivers.has(path):
		_drivers[path] = load(path) if ResourceLoader.exists(path) else null
		var loaded: Texture2D = _drivers[path]
		if loaded != null:
			_driver_regions[path] = Rect2(loaded.get_image().get_used_rect())
	var tex: Texture2D = _drivers[path]
	if tex == null:
		return
	# Crop the occupied upper body with its source ratio; the vehicle occludes
	# the tail. Do not stretch a tall portrait into the square padded car canvas.
	var occupied: Rect2 = _driver_regions[path]
	var upper := Rect2(occupied.position, Vector2(occupied.size.x, occupied.size.y * (0.30 if head_only else 0.55)))
	var driver_width: float = width * 0.56
	var driver_height: float = driver_width * upper.size.y / maxf(1.0, upper.size.x)
	draw_texture_rect_region(tex, Rect2(p + Vector2(-driver_width * 0.5, -driver_height * 0.86), Vector2(driver_width, driver_height)), upper)

func _draw_vehicle(vehicle: String, p: Vector2, width: float, angle: float, paint: Dictionary) -> void:
	if vehicle == "truck":
		# Explicit development art gap: flat toy silhouette, never the retired model.
		var fill := Color(0.40, 0.77, 0.78)
		draw_style_box(_panel(fill), Rect2(p - Vector2(width * 0.35, width * 0.25), Vector2(width * 0.7, width * 0.45)))
		for x in [-1.0, 1.0]:
			draw_circle(p + Vector2(x * width * 0.38, width * 0.15), width * 0.20, INK)
			draw_circle(p + Vector2(x * width * 0.38, width * 0.15), width * 0.08, Color(0.88, 0.77, 0.47))
	else:
		var dir := Vector2.from_angle(angle)
		var view := "side"
		if absf(dir.y) > 0.84:
			view = "front" if dir.y > 0 else "rear"
		elif absf(dir.y) > 0.38:
			view = "quarter"
		var key: String = vehicle + "_" + view
		var tex: Texture2D = _textures[key]
		var source: Rect2 = _regions[key]
		var height: float = width * source.size.y / maxf(1.0, source.size.x)
		var flip: float = -1.0 if dir.x > 0.0 and view in ["side", "quarter"] else 1.0
		var fit: float = minf(size.x / BASE.x, size.y / BASE.y)
		draw_set_transform((size - BASE * fit) * 0.5 + p * fit, 0.0, Vector2(fit * flip, fit))
		draw_texture_rect_region(tex, Rect2(-width * 0.5, -height * 0.65, width, height), source)
		draw_set_transform((size - BASE * fit) * 0.5, 0.0, Vector2.ONE * fit)
	var color_value: Variant = paint.get("col")
	if color_value != null or bool(paint.get("rainbow", false)):
		var trim: Color = Color.from_hsv(fposmod(_time * 0.25, 1.0), 0.75, 1.0) if bool(paint.get("rainbow", false)) else Color(color_value)
		draw_arc(p + Vector2(0, width * 0.15), width * 0.28, 0.15, PI - 0.15, 18, trim, 5, true)

func _panel(fill: Color) -> StyleBoxFlat:
	var key := fill.to_rgba32()
	if _panels.has(key):
		return _panels[key]
	var box := StyleBoxFlat.new()
	box.bg_color = fill
	box.border_color = INK
	box.set_border_width_all(4)
	box.set_corner_radius_all(25)
	_panels[key] = box
	return box

func _draw_choices() -> void:
	var keys: Array = race._vehicle_keys()
	for i in range(keys.size()):
		var chosen: bool = i == int(race._sel_idx)
		var center := Vector2(325 + float(i) * 302, 390)
		var width: float = 260.0 if chosen else 215.0
		draw_style_box(_panel(Color(0.97, 0.89, 0.95) if chosen else Color(0.78, 0.87, 0.92)), Rect2(center - Vector2(143, 126), Vector2(286, 260)))
		var paint: Dictionary = race.PAINTS[int(race._paint_idx)] if race._sel_phase == "paint" and chosen else {}
		_draw_vehicle(String(keys[i]), center + Vector2(0, -10), width * 0.85, PI, paint)
		draw_style_box(_panel(Color(0.76, 0.93, 0.94) if chosen else Color(0.91, 0.90, 0.98)), Rect2(center + Vector2(-137, 180), Vector2(278, 124)))
		_glyph(center + Vector2(0, 244), String(race._vehicles_table()[keys[i]]["label"]), 25, INK)
		if chosen:
			_glyph(center + Vector2(0, -155), "▼", 38, Color(1, 0.86, 0.27))

func _draw_podium() -> void:
	# Roshan's completed crossing remains visible before the result/podium settle.
	var order: Array = race._karts.duplicate()
	order.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a["s"]) > float(b["s"]))
	for i in range(mini(3, order.size())):
		var k: Dictionary = order[i]
		var p := Vector2([640.0, 360.0, 920.0][i], [465.0, 505.0, 525.0][i])
		var color: Color = [Color(1, 0.83, 0.35), Color(0.83, 0.85, 0.95), Color(0.81, 0.61, 0.51)][i]
		draw_style_box(_panel(color), Rect2(p + Vector2(-105, 35), Vector2(210, 180 - float(i) * 25)))
		_draw_driver(k["node"], p, 175)
		_draw_vehicle(String(k["veh"]), p + Vector2(0, 22), 195, PI, (k["node"] as Node2D).get_meta("paint", {}))
		_glyph(p + Vector2(0, 117), str(i + 1), 52, INK)
	# A non-first finish still keeps Roshan in the celebration.
	if race._pl != null and order.find(race._pl) >= 3:
		var p := Vector2(1130, 470)
		_draw_driver(race._pl["node"], p, 140)
		_draw_vehicle(String(race._pl["veh"]), p, 170, PI, (race._pl["node"] as Node2D).get_meta("paint", {}))

func _draw_minimap() -> void:
	var points := PackedVector2Array()
	for p in race._lut:
		points.append(Vector2(1138, 118) + p * 0.48)
	draw_polyline(points, Color(0.2, 0.16, 0.34, 0.50), 9, true)
	for k in race._karts:
		var player: bool = bool(k["is_player"])
		var p: Vector2 = race._pos_at(race._eff(float(k["s"])))
		draw_circle(Vector2(1138, 118) + p * 0.48, 6 if player else 3.5, Color(1, 0.92, 0.35) if player else Color(0.86, 0.41, 0.69))

func _glyph(center: Vector2, value: String, font_size: int, color: Color) -> void:
	var font := ThemeDB.fallback_font
	var width := font.get_string_size(value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	draw_string(font, center + Vector2(-width * 0.5, float(font_size) * 0.32), value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)