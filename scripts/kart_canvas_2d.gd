extends Control
# Chase view is a planar projection into Canvas; KartGame owns all simulation.
const Worlds := preload("res://scripts/kart_course_worlds.gd")
const BASE := Vector2(1280, 720)
const INK := Color("#51416f")
const STEERING_RECT := Rect2(230, 584, 740, 112)
const TURBO_CENTER := Vector2(1120, 635)
const TURBO_RADIUS := 62.0
const ART_ROOT := "res://assets/kart/chase/"
var race: Node
var focus := Vector2.ZERO
var view_scale := 7.8
var speed_zoom := 1.0
var _forward := Vector2.RIGHT
var _height := 0.0
var _ground_height := 0.0
var _focal := 700.0
var _textures: Dictionary = {}
var _props: Dictionary = {}
var _anchors: Dictionary = {}
var _drivers: Dictionary = {}
var _driver_regions: Dictionary = {}
var _panels: Dictionary = {}
var _backgrounds: Dictionary = {}
var _bursts: Array[Dictionary] = []
var _time := 0.0
var _podium_age := 0.0
var _pose := "straight"
var _pose_age := 1.0
var touch_owner := -1
var turbo_owner := -1
var _mouse_held := false
var _knob := Vector2(600, 640)
var current_sector := 0
var _prior_sector := -1
var _feedback := ""
var _feedback_age := 0.0

func setup(engine: Node) -> void:
	race = engine
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_anchors = (JSON.parse_string(FileAccess.get_file_as_string(ART_ROOT + "anchors.json")) as Dictionary)["sprites"]
	for key in _anchors:
		_textures[key] = load("res://" + String((_anchors[key] as Dictionary)["path"]))
	for path in ["res://assets/flats/castle/dream_house/movie_screen_frame.png",
		"res://assets/flats/castle/dream_house/cloud_settee.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png"]:
		_props[path.get_file()] = load(path)
	_load_background(0)
	queue_redraw()

func _load_background(index: int) -> void:
	if _backgrounds.has(index):
		return
	var cards: Array[Texture2D] = []
	for path in Worlds.backdrop_paths(Worlds.SECTORS[index]):
		cards.append(load(path))
	_backgrounds[index] = cards
	# At most two sets: the visible room and the room inside its next doorway.
	while _backgrounds.size() > 2:
		var obsolete: int = int(_backgrounds.keys()[0])
		if obsolete == current_sector:
			obsolete = int(_backgrounds.keys()[1])
		_backgrounds.erase(obsolete)

func follow(delta: float) -> void:
	if race == null or race._pl == null:
		return
	var player: Dictionary = race._pl
	var frame: Array = race._kart_frame(float(player["s"]), float(player["lat"]) * 0.35)
	var tangent: Vector2 = (frame[1] as Vector2).normalized()
	if player.has("spur_start"):
		var kart_node: Node2D = player["node"]
		frame[0] = kart_node.position
		tangent = ((player["spur_to"] as Vector2) - (player["spur_from"] as Vector2)).normalized()
	var blend := clampf(delta * 8.0, 0.0, 1.0)
	_forward = Vector2.from_angle(lerp_angle(_forward.angle(), tangent.angle(), blend))
	focus = (frame[0] as Vector2) - _forward * 23.0
	_ground_height = float(frame[4])
	_height = _ground_height + 8.0
	var spd: float = clampf(float(player["speed"]) / (float(race._vmax) * 1.5), 0.0, 1.0)
	var boost: bool = float(player["boost_t"]) > 0.0
	speed_zoom = lerpf(speed_zoom, 1.0 - 0.20 * spd - (0.08 if boost else 0.0), clampf(delta * 5.0, 0.0, 1.0))
	view_scale = 7.8 * speed_zoom
	_focal = 700.0 * speed_zoom
	current_sector = Worlds.index_at(float(race._eff(float(player["s"]))) / float(race._len))
	if current_sector != _prior_sector:
		_load_background(current_sector)
		_prior_sector = current_sector
		var place: String = String(Worlds.SECTORS[current_sector]["place"])
		if race._main != null and race._main.has_method("_say") and not bool(race._rev):
			var cues := {"movie_lounge":"castle_movie_enter", "family_gallery":"castle_gallery_enter",
				"mermaid_pool":"castle_pool_enter"}
			if cues.has(place) and race._state == "race":
				race._main._say("roshan", cues[place], 1.4)
	_pose_age += delta
	var steer: float = float(race._steer_input())
	var want := "left" if steer < -0.25 else ("right" if steer > 0.25 else ("boost" if boost else "straight"))
	if _pose_age >= 0.16 and want != _pose:
		_pose = want
		_pose_age = 0.0
	queue_redraw()

func project(point: Vector2, height: float) -> Array:
	var rel := point - focus
	var depth := rel.dot(_forward)
	var side := rel.dot(Vector2(-_forward.y, _forward.x))
	var dy := height - _height
	var z: float = depth * 0.995 - dy * 0.10
	var scale: float = _focal / maxf(z, 0.5)
	var p := Vector2(640.0 + side * scale, 340.0 - (dy * 0.995 + depth * 0.10) * scale)
	return [p, scale, z]

func burst(point: Vector2, color: Color) -> void:
	if _bursts.size() >= 12:
		_bursts.pop_front()
	_bursts.append({"point":point, "color":color, "t":0.45})

func feedback(event: String) -> void:
	_feedback = event
	_feedback_age = 0.85

func clear_touch() -> void:
	touch_owner = -1
	turbo_owner = -1
	_mouse_held = false
	if race != null:
		race._canvas_steer = 0.0
		race._canvas_fire = false
		race._canvas_held = false

func _notification(what: int) -> void:
	if what in [NOTIFICATION_PAUSED, NOTIFICATION_APPLICATION_PAUSED, NOTIFICATION_APPLICATION_FOCUS_OUT]:
		clear_touch()

func _logical(point: Vector2) -> Vector2:
	var fit := minf(size.x / BASE.x, size.y / BASE.y)
	return (point - (size - BASE * fit) * 0.5) / maxf(0.001, fit)

func _press(index: int, point: Vector2) -> void:
	if point.distance_to(TURBO_CENTER) <= TURBO_RADIUS and turbo_owner == -1:
		turbo_owner = index
		race._canvas_fire = true
	elif STEERING_RECT.grow(12).has_point(point) and touch_owner == -1:
		touch_owner = index
		_drag(point)

func _drag(point: Vector2) -> void:
	_knob = Vector2(clampf(point.x, STEERING_RECT.position.x + 42, STEERING_RECT.end.x - 42), 640)
	race._canvas_steer = clampf((point.x - STEERING_RECT.get_center().x) / 230.0, -1.0, 1.0)
	race._canvas_held = true
	race._touch_t = 3.0

func _release(index: int) -> void:
	if index == touch_owner:
		touch_owner = -1
		race._canvas_steer = 0.0
		race._canvas_held = false
	if index == turbo_owner:
		turbo_owner = -1

func _gui_input(event: InputEvent) -> void:
	if race == null or race._state not in ["countdown", "race"]:
		return
	# Touch-generated mouse events precede the real touch in Godot. Owning both
	# would replace a stable finger index with the mouse sentinel.
	if event is InputEventMouse and event.device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_press(touch.index, _logical(touch.position))
		else:
			_release(touch.index)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == touch_owner:
			_drag(_logical(drag.position))
			accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_LEFT:
			if button.pressed:
				_press(-2, _logical(button.position))
				_mouse_held = true
			else:
				_release(-2)
				_mouse_held = false
			accept_event()
	elif event is InputEventMouseMotion and _mouse_held and touch_owner == -2:
		_drag(_logical((event as InputEventMouseMotion).position))
		accept_event()

func _process(delta: float) -> void:
	_time += delta
	_feedback_age = maxf(0.0, _feedback_age - delta)
	if race != null and race._state == "podium":
		_podium_age += delta
	for i in range(_bursts.size() - 1, -1, -1):
		_bursts[i]["t"] = float(_bursts[i]["t"]) - delta
		if float(_bursts[i]["t"]) <= 0:
			_bursts.remove_at(i)
	queue_redraw()

func _draw() -> void:
	if race == null:
		return
	var fit := minf(size.x / BASE.x, size.y / BASE.y)
	draw_set_transform((size - BASE * fit) * 0.5, 0, Vector2.ONE * fit)
	draw_rect(Rect2(-BASE, BASE * 3), Color("#b9b1d3"))
	_draw_background(current_sector, Rect2(0, 0, 1280, 720))
	_draw_furnishings()
	if race._state == "select":
		_draw_choices()
		return
	if race._state == "podium" and _podium_age >= 0.65:
		_draw_podium()
		return
	if race._pl == null:
		return
	_draw_course()
	_draw_objects()
	var order: Array = race._karts.duplicate()
	order.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return float(project((a["node"] as Node2D).position, float((a["node"] as Node2D).get_meta("height", 0.0)))[2]) > float(project((b["node"] as Node2D).position, float((b["node"] as Node2D).get_meta("height", 0.0)))[2]))
	for k in order:
		_draw_racer(k)
	for effect in _bursts:
		var p := project(effect["point"], _ground_height)
		if _visible(p):
			var age: float = 1.0 - float(effect["t"]) / 0.45
			var col: Color = effect["color"]
			col.a = 1.0 - age
			for j in range(7):
				draw_circle((p[0] as Vector2) + Vector2.from_angle(float(j) * TAU / 7.0) * age * 24, 2.5 * (1 - age), col)
	_draw_controls()
	_draw_status()

func _draw_background(index: int, rect: Rect2) -> void:
	_load_background(index)
	var cards: Array = _backgrounds[index]
	var columns: int = int(Worlds.SECTORS[index]["columns"])
	var first: Texture2D = cards[0]
	var native_size := Vector2(first.get_width() * columns, first.get_height() * 2)
	# Cover by cropping the complete source window, including portrait doorway
	# previews. No room, panorama tile or approved contour is stretched.
	var scale: float = maxf(rect.size.x / native_size.x, rect.size.y / native_size.y)
	var total: Vector2 = native_size * scale
	var origin: Vector2 = rect.position - (total - rect.size) * 0.5
	for row in range(2):
		for col in range(columns):
			var card: Texture2D = cards[row * columns + col]
			var target := Rect2(origin + Vector2(float(col) * total.x / float(columns), float(row) * total.y * 0.5), Vector2(total.x / float(columns), total.y * 0.5))
			var clipped := target.intersection(rect)
			if clipped.get_area() > 0:
				var pixels := Vector2(card.get_width(), card.get_height())
				draw_texture_rect_region(card, clipped, Rect2((clipped.position - target.position) / target.size * pixels, clipped.size / target.size * pixels))

func _quad(a: Array, b: Array, c: Array, d: Array, color: Color) -> void:
	if minf(minf(float(a[2]), float(b[2])), minf(float(c[2]), float(d[2]))) < 3.0:
		return
	# Two triangles remain valid where a banked strip foreshortens to a sliver.
	for triangle in [PackedVector2Array([a[0], b[0], c[0]]), PackedVector2Array([a[0], c[0], d[0]])]:
		if absf((triangle[1] - triangle[0]).cross(triangle[2] - triangle[0])) > 0.05:
			draw_colored_polygon(triangle, color)

func _road_point(s: float, lateral: float, raised: float = 0.0) -> Array:
	var frame: Array = race._kart_frame(s, lateral)
	return project(frame[0], float(frame[4]) + raised)

func _course_point(s: float, lateral: float, raised: float = 0.0) -> Array:
	# Stationary course objects use source coordinates, even on a reverse lap.
	var frame: Array = race._frame_at(s, lateral)
	return project(frame[0], float(frame[4]) + raised)

func _draw_course() -> void:
	var at: float = float(race._pl["s"])
	# Bounded far-to-near strips preserve bank, height, width and contact geometry.
	for i in range(92, -1, -1):
		var s: float = at - 18.0 + float(i) * 2.8
		if not _same_place(race._eff(s)):
			continue
		var width: float = race._width_at(race._eff(s))
		var sector: Dictionary = Worlds.sector_at(float(race._eff(s)) / float(race._len))
		var a := _road_point(s, -width)
		var b := _road_point(s, width)
		var c := _road_point(s + 2.9, width)
		var d := _road_point(s + 2.9, -width)
		_quad(a, b, c, d, sector["edge"])
		_quad(_road_point(s, -width + 0.7, 0.015), _road_point(s, width - 0.7, 0.015), _road_point(s + 2.9, width - 0.7, 0.015), _road_point(s + 2.9, -width + 0.7, 0.015), sector["road"])
		if i % 4 == 0:
			_quad(_road_point(s, -0.12, 0.03), _road_point(s, 0.12, 0.03), _road_point(s + 1.1, 0.12, 0.03), _road_point(s + 1.1, -0.12, 0.03), Color("#fff3df"))
		if i % 6 == 0 and float(a[2]) > 5:
			draw_line(a[0], b[0], Color(0.50, 0.39, 0.48, 0.12), 1.4, true)
			# Bridge balustrades mark a physical crossing, not a floating road.
			if String(sector["place"]) in ["castle_bridge", "mermaid_pool"]:
				for edge in [-width, width]:
					var floor := _road_point(s, edge)
					var rail := _road_point(s, edge, 2.0)
					var rail_next := _road_point(s + 16.8, edge, 2.0)
					if float(floor[2]) > 5:
						draw_line(floor[0], rail[0], Color("#c1a278"), maxf(2, float(floor[1]) * 0.12), true)
						draw_circle(rail[0], maxf(2, float(rail[1]) * 0.15), Color("#edd49f"))
						if float(rail_next[2]) > 5:
							draw_line(rail[0], rail_next[0], Color("#c1a278"), maxf(2, float(rail[1]) * 0.10), true)
		var u: float = fposmod(s, float(race._len))
		if u < 3.0:
			for tile in range(12):
				var l: float = lerpf(-width, width, float(tile) / 12.0)
				var r: float = lerpf(-width, width, float(tile + 1) / 12.0)
				_quad(_road_point(s, l, 0.05), _road_point(s, r, 0.05), _road_point(s + 1.5, r, 0.05), _road_point(s + 1.5, l, 0.05), INK if tile % 2 == 0 else Color("#fff3df"))
	_draw_doorway(at)
	if String(Worlds.SECTORS[current_sector]["place"]) == "sky_lagoon" and race.has_meta("gate_pos"):
		var from: Vector2 = race.get_meta("gate_pos")
		var to: Vector2 = race._frame_at(race._shortcut_to_u() * float(race._len), race._rhalf() * 0.78)[0]
		var direction := (to - from).normalized()
		var side := Vector2(-direction.y, direction.x) * 7.0
		# Cull short pieces independently; the lane remains visible after its
		# entrance moves behind the camera during the crossing.
		for i in range(15, -1, -1):
			var a: Vector2 = from.lerp(to, float(i) / 16.0)
			var b: Vector2 = from.lerp(to, float(i + 1) / 16.0)
			_quad(project(a - side, 0.06), project(a + side, 0.06), project(b + side, 0.06), project(b - side, 0.06), Color("#c7d9bd"))
		var entry := project(from, 0.12)
		if _visible(entry) and not bool(race._rev):
			_arrow(entry[0], minf(35, float(entry[1])), Color("#6b9f94"))

func _draw_doorway(at: float) -> void:
	var sector: Dictionary = Worlds.SECTORS[current_sector]
	var next_index: int = (current_sector + (-1 if bool(race._rev) else 1) + Worlds.SECTORS.size()) % Worlds.SECTORS.size()
	var next_place: String = String(Worlds.SECTORS[next_index]["place"])
	# Outdoor windows join one continuous path. Only actual rooms have doorways.
	if next_place == String(sector["place"]) or String(sector["place"]) == "sky_lagoon" or (String(sector["place"]) == "castle_bridge" and next_place == "sky_lagoon"):
		return
	var boundary: float = float(sector["until"]) * float(race._len)
	if bool(race._rev):
		boundary = float(race._len) - (0.0 if current_sector == 0 else float(Worlds.SECTORS[current_sector - 1]["until"]) * float(race._len))
	var distance: float = fposmod(boundary - fposmod(at, float(race._len)), float(race._len))
	if distance > 130.0 or distance < 2.0:
		return
	var foot := _road_point(at + distance, 0)
	var scale: float = float(foot[1])
	if float(foot[2]) < 5:
		return
	var center: Vector2 = foot[0]
	var width: float = race._width_at(race._eff(at + distance)) * scale * 2
	var height: float = 15.0 * scale
	# The route opens a literal passage at the end of this room's driving aisle.
	# Preview is bounded to the opening; no fullscreen transition or teleport.
	var opening := Rect2(center - Vector2(width * 0.5, height), Vector2(width, height))
	if String(sector["place"]) == "castle_bridge":
		var castle: Texture2D = _props["sky_lagoon_castle_four_tower_v4.png"]
		var factor: float = width / 199.0
		var origin := center - Vector2(510, 773) * factor
		draw_texture_rect_region(castle, Rect2(origin, Vector2(1022, 820) * factor), Rect2(0, 0, 1022, 820))
		# Same front door footprint as the shipping Castle card; open for the rally.
		_draw_background(next_index, Rect2(origin + Vector2(410, 557) * factor, Vector2(199, 216) * factor))
		return
	draw_style_box(_panel(Color("#51416f")), opening.grow(7 * scale / 20.0))
	_load_background(next_index)
	_draw_background(next_index, opening)
	draw_line(opening.position, opening.position + Vector2(0, height), Color("#ebc999"), maxf(3, scale * 0.6), true)
	draw_line(opening.position + Vector2(width, 0), opening.end, Color("#ebc999"), maxf(3, scale * 0.6), true)
	draw_arc(center - Vector2(0, height * 0.76), width * 0.5, PI, TAU, 20, Color("#ebc999"), maxf(3, scale * 0.65), true)

func _visible(p: Array) -> bool:
	return float(p[2]) > 5.0 and float(p[2]) < 210.0 and Rect2(-180, -180, 1640, 950).has_point(p[0])

func _draw_objects() -> void:
	for strip in race._strip_data:
		# Physics-only records can omit artwork coordinates, including during
		# controller/lifecycle checks. They still charge through KartGame.
		if not strip.has_all(["s", "lat", "hw", "len"]):
			continue
		var s: float = float(strip["s"])
		if not _same_place(s):
			continue
		var half: float = float(strip["hw"])
		_quad(_course_point(s, float(strip["lat"]) - half, 0.08), _course_point(s, float(strip["lat"]) + half, 0.08), _course_point(s + float(strip["len"]), float(strip["lat"]) + half, 0.08), _course_point(s + float(strip["len"]), float(strip["lat"]) - half, 0.08), Color("#7ccdd0"))
		var p := _course_point(s + float(strip["len"]) * 0.5, float(strip["lat"]), 0.12)
		if _visible(p):
			_arrow(p[0], minf(45, float(p[1]) * 1.3), Color("#fff3df"))
	for ramp in race._ramp_data:
		if not _same_place(float(ramp["s"])):
			continue
		var p := project(ramp["pos"], float(ramp["height"]))
		if _visible(p):
			var center: Vector2 = p[0]
			var radius: float = minf(65, float(p[1]) * 2)
			draw_colored_polygon(PackedVector2Array([center + Vector2(-radius, 0), center + Vector2(0, -radius * 0.5), center + Vector2(radius, 0), center + Vector2(radius, radius * 0.25), center + Vector2(-radius, radius * 0.25)]), Color("#e5b16f"))
			_arrow(center, radius * 0.5, Color("#fff3df"))
	for item in race._pickups_live:
		if not _same_place(float(item["s"])):
			continue
		var node: Node2D = item["node"]
		if not node.visible:
			continue
		var p := project(node.position, float(node.get_meta("height", 0.0)))
		if _visible(p):
			var radius: float = clampf(float(p[1]) * 0.75, 5, 30)
			var kind: String = String(item["kind"])
			if kind == "bubble":
				draw_circle(p[0], radius, Color("#a5e5e2"))
				draw_arc(p[0], radius, 0, TAU, 20, Color("#fff9ef"), 2, true)
				draw_circle((p[0] as Vector2) + Vector2(-radius * 0.3, -radius * 0.3), radius * 0.25, Color.WHITE)
			elif kind == "shell":
				draw_arc(p[0], radius, PI, TAU, 16, Color("#edacb5"), radius, true)
			else:
				_star(p[0], radius, Color("#f4d885") if kind == "star" else Color("#c2a3de"))
	for pearl in race._pearls_live:
		if bool(pearl["got"]):
			continue
		var node: Node2D = pearl["node"]
		if not _same_place(float(node.get_meta("course_s", 0.0))):
			continue
		var p := project(node.position, float(node.get_meta("height", 0.0)))
		if _visible(p):
			var radius: float = clampf(float(p[1]) * 0.40, 3.5, 17)
			draw_circle(p[0], radius, Color("#b69ccc"))
			draw_circle((p[0] as Vector2) + Vector2(-1, -1), radius * 0.78, Color("#ffe6ee"))
	for hazard in race._hazards_live:
		if not _same_place(float(hazard["s"])):
			continue
		var node: Node2D = hazard["node"]
		var p := project(node.position, float(node.get_meta("height", 0.0)))
		if node.visible and _visible(p):
			var radius: float = clampf(float(p[1]) * 1.2, 5, 44)
			var center: Vector2 = p[0]
			var kind: String = String(hazard["kind"])
			if kind == "geyser":
				draw_circle(center, radius, Color("#988296"))
				if bool(hazard.get("erupting", false)):
					draw_line(center, center - Vector2(0, radius * 3), Color("#94d6df"), radius, true)
			elif kind == "kelp":
				for j in range(3):
					draw_line(center + Vector2(float(j - 1) * radius * 0.4, 0), center + Vector2(float(j - 1) * radius * 0.4 + sin(_time + j) * 6, -radius), Color("#618c88"), radius * 0.22, true)
			elif kind == "whirl":
				for j in range(3):
					draw_arc(center, radius * (0.35 + float(j) * 0.3), _time + j, _time + j + PI * 1.5, 16, INK, 3, true)
			else:
				draw_circle(center, radius, Color("#9e7da7"))
				draw_circle(center + Vector2(-radius * 0.3, -radius * 0.4), radius * 0.16, Color.WHITE)
				draw_circle(center + Vector2(radius * 0.3, -radius * 0.4), radius * 0.16, Color.WHITE)

func _draw_card(key: String, foot: Vector2, width: float) -> void:
	var tex: Texture2D = _textures[key]
	var data: Dictionary = _anchors[key]
	var anchor: Array = data["anchor"]
	var factor: float = width / maxf(1.0, float(data["vehicle_width"]))
	draw_texture_rect(tex, Rect2(foot - Vector2(float(anchor[0]), float(anchor[1])) * factor, Vector2(tex.get_width(), tex.get_height()) * factor), false)

func _draw_racer(k: Dictionary) -> void:
	if not _same_place(race._eff(float(k["s"]))):
		return
	var node: Node2D = k["node"]
	var ground_height: float = float(node.get_meta("height", 0.0)) - float(k.get("lift", 0.0)) - 1.2
	var ground := project(node.position, ground_height)
	var p := project(node.position, float(node.get_meta("height", 0.0)) - 1.2)
	if not _visible(p):
		return
	var center: Vector2 = p[0]
	var width: float = clampf(float(race._veh(k)["size"]) * float(p[1]) * 1.18, 12, 330)
	# Shadow stays on ground; authored tires/driver rise together through the jump.
	var fit := minf(size.x / BASE.x, size.y / BASE.y)
	draw_set_transform((size - BASE * fit) * 0.5 + (ground[0] as Vector2) * fit, 0, Vector2(fit, fit * 0.24))
	draw_circle(Vector2.ZERO, width * 0.40, Color(0.20, 0.14, 0.31, 0.20))
	draw_set_transform((size - BASE * fit) * 0.5, 0, Vector2.ONE * fit)
	var vehicle: String = String(k["veh"])
	if bool(k["is_player"]):
		_draw_card(vehicle + "_" + _pose, center, width)
	else:
		# Place the portrait's lower edge behind the authored seat back. Each
		# vehicle has a different seat height; the card occludes the lower body.
		var seat: float = {"kart": 0.50, "moto": 0.93, "truck": 0.52}.get(vehicle, 0.50)
		_draw_driver(node, center - Vector2(0, width * seat), width * 0.48)
		_draw_card("empty_" + vehicle, center, width)
	var paint: Dictionary = node.get_meta("paint", {})
	var trim: Variant = paint.get("col")
	if trim != null or bool(paint.get("rainbow", false)):
		var col: Color = Color.from_hsv(fposmod(_time * 0.15, 1), 0.45, 0.95) if bool(paint.get("rainbow", false)) else Color(trim)
		# Physical rear-bumper stripe; never recolor the character or whole drawing.
		draw_line(center + Vector2(-width * 0.22, -width * 0.11), center + Vector2(width * 0.22, -width * 0.11), col, maxf(2.0, width * 0.035), true)
	if bool(k.get("drift", false)):
		var col: Color = race.DRIFT_COLS[int(k.get("spray_tier", 0))]
		for j in range(4):
			draw_circle(center + Vector2(width * 0.44 * (-1 if j % 2 == 0 else 1), 4 + j * 3), 2.5, col)

func _draw_driver(node: Node2D, foot: Vector2, width: float) -> void:
	var path: String = node.get_meta("sprite_path", "")
	if not _drivers.has(path):
		var tex: Texture2D = load(path) if ResourceLoader.exists(path) else null
		_drivers[path] = tex
		if tex != null:
			_driver_regions[path] = Rect2(tex.get_image().get_used_rect())
	var texture: Texture2D = _drivers[path]
	if texture == null:
		return
	var occupied: Rect2 = _driver_regions[path]
	var head := Rect2(occupied.position, Vector2(occupied.size.x, occupied.size.y * 0.43))
	var h: float = width * head.size.y / maxf(1.0, head.size.x)
	draw_texture_rect_region(texture, Rect2(foot - Vector2(width * 0.5, h), Vector2(width, h)), head)

func _draw_controls() -> void:
	draw_style_box(_panel(Color("#f6e7d5")), STEERING_RECT)
	var middle := STEERING_RECT.get_center()
	draw_line(middle - Vector2(250, 0), middle + Vector2(250, 0), Color("#b8a0c7"), 6, true)
	_arrow(middle - Vector2(300, 0), 20, INK, -PI * 0.5)
	_arrow(middle + Vector2(300, 0), 20, INK, PI * 0.5)
	var knob := _knob if touch_owner != -1 else middle
	draw_circle(knob, 32, Color("#a7d6d4"))
	draw_arc(knob, 32, 0, TAU, 24, INK, 3, true)
	draw_arc(knob, 18, 0, TAU, 24, INK, 4, true)
	draw_line(knob + Vector2(-17, 0), knob + Vector2(17, 0), INK, 3, true)
	draw_line(knob, knob + Vector2(0, 18), INK, 3, true)
	var meter: float = float(race._pl["meter"])
	var boost: bool = float(race._pl["boost_t"]) > 0
	draw_circle(TURBO_CENTER, TURBO_RADIUS, Color("#f6e7d5"))
	draw_arc(TURBO_CENTER, TURBO_RADIUS, 0, TAU, 36, INK, 4, true)
	draw_arc(TURBO_CENTER, TURBO_RADIUS - 8, -PI * 0.5, -PI * 0.5 + TAU * maxf(0.01, meter), 36, Color("#e7b864") if meter >= 0.5 else Color("#83c6c8"), 8, true)
	_arrow(TURBO_CENTER + Vector2(0, 6), 31, Color("#e7b864") if boost or meter >= 0.5 else INK)
	# Demonstration is confined to the actual control surface and pays no progress.
	if race._race_t < 6 and not bool(race._player_acted):
		draw_circle(middle + Vector2(sin(_time * 2) * 70, 0), 14, Color("#edacb5"))

func _draw_status() -> void:
	draw_style_box(_panel(Color("#f6e7d5")), Rect2(158, 20, 238, 92))
	var lap: int = clampi(int(float(race._pl["s"]) / float(race._len)), 0, int(race._laps()) - 1)
	for i in range(int(race._laps())):
		var p := Vector2(197 + i * 62, 58)
		draw_line(p - Vector2(16, 20), p + Vector2(-16, 20), INK, 4, true)
		for x in range(3):
			for y in range(2):
				draw_rect(Rect2(p + Vector2(-14 + x * 9, -19 + y * 10), Vector2(9, 10)), INK if (x + y) % 2 == 0 else Color.WHITE)
		if i <= lap:
			draw_circle(p + Vector2(0, 29), 5, Color("#83c6c8"))
	_glyph(Vector2(350, 65), str(race._placement()), 32, INK)
	draw_style_box(_panel(Color("#f6e7d5")), Rect2(1058, 20, 195, 78))
	draw_circle(Vector2(1100, 60), 15, Color("#d8bada"))
	draw_circle(Vector2(1096, 55), 7, Color("#fff6ed"))
	_glyph(Vector2(1175, 61), str(race._pearls_got), 30, INK)
	if race._state == "countdown":
		var count: int = clampi(ceili(float(race._clock)), 1, 3)
		for i in range(3):
			draw_circle(Vector2(565 + i * 75, 180), 23, Color("#edacb5") if i < count else Color("#83c6c8"))
	if _feedback_age > 0:
		_star(Vector2(443, 65), 21, Color("#e7b864"))

func _same_place(s: float) -> bool:
	var index: int = Worlds.index_at(s / float(race._len))
	if index == current_sector:
		return true
	# The lap wraps inside one Movie Lounge. Its start/finish must stay visible
	# across that seam, while separate Hall visits remain separate windows.
	var count: int = Worlds.SECTORS.size()
	var adjacent: bool = (index + 1) % count == current_sector or (current_sector + 1) % count == index
	return adjacent and String(Worlds.SECTORS[index]["place"]) == String(Worlds.SECTORS[current_sector]["place"])

func _draw_furnishings() -> void:
	var place: String = String(Worlds.SECTORS[current_sector]["place"])
	if place == "movie_lounge":
		_draw_prop("movie_screen_frame.png", Rect2(440, 45, 400, 180))
		_draw_prop("cloud_settee.png", Rect2(12, 375, 275, 150))
		_draw_prop("cloud_settee.png", Rect2(993, 375, 275, 150))

func _draw_prop(key: String, region: Rect2) -> void:
	var texture: Texture2D = _props[key]
	var native_size := Vector2(texture.get_width(), texture.get_height())
	var fitted: Vector2 = native_size * minf(region.size.x / native_size.x, region.size.y / native_size.y)
	draw_texture_rect(texture, Rect2(region.get_center() - fitted * 0.5, fitted), false)

func _panel(fill: Color) -> StyleBoxFlat:
	var key := fill.to_rgba32()
	if _panels.has(key):
		return _panels[key]
	var box := StyleBoxFlat.new()
	box.bg_color = fill
	box.border_color = INK
	box.set_border_width_all(3)
	box.set_corner_radius_all(25)
	_panels[key] = box
	return box

func _draw_choices() -> void:
	var keys: Array = race._vehicle_keys()
	for i in range(keys.size()):
		var selected: bool = i == int(race._sel_idx)
		var center := Vector2(325 + i * 302, 490)
		draw_style_box(_panel(Color("#f6e7d5") if selected else Color("#d7d1e6")), Rect2(Vector2(center.x - 139, 264), Vector2(278, 286)))
		var key: String = String(keys[i]) + "_left"
		var data: Dictionary = _anchors[key]
		var bounds: Array = data["bounds"]
		# A tall motorcycle still fits its visible, native Button target. Road
		# scaling uses vehicle width; picture choices fit the whole driver too.
		var fit: float = minf((230.0 if selected else 215.0) / (float(bounds[2]) - float(bounds[0])), (222.0 if selected else 205.0) / (float(bounds[3]) - float(bounds[1])))
		_draw_card(key, center, float(data["vehicle_width"]) * fit)
		if selected and race._sel_phase == "paint":
			var paint: Dictionary = race.PAINTS[int(race._paint_idx)]
			if paint.get("col") != null or bool(paint.get("rainbow", false)):
				var trim: Color = Color.from_hsv(fposmod(_time * 0.15, 1), 0.45, 0.95) if bool(paint.get("rainbow", false)) else Color(paint["col"])
				draw_line(center + Vector2(-46, -24), center + Vector2(46, -24), trim, 7, true)
		if selected:
			_star(center + Vector2(0, -257), 25, Color("#e7b864"))

func _draw_podium() -> void:
	var order: Array = race._karts.duplicate()
	order.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a["s"]) > float(b["s"]))
	for i in range(mini(3, order.size())):
		var k: Dictionary = order[i]
		var p := Vector2([640, 350, 930][i], [455, 495, 515][i])
		draw_style_box(_panel([Color("#e7c889"), Color("#c6c0d9"), Color("#d9b49b")][i]), Rect2(p + Vector2(-110, 25), Vector2(220, 160 - i * 20)))
		if bool(k["is_player"]):
			_draw_card(String(k["veh"]) + "_left", p, 240)
		else:
			_draw_driver(k["node"], p - Vector2(0, 90), 110)
			_draw_card("empty_" + String(k["veh"]), p, 240)
		_glyph(p + Vector2(0, 88), str(i + 1), 42, INK)
	if race._pl != null and order.find(race._pl) >= 3:
		_draw_card(String(race._pl["veh"]) + "_left", Vector2(1135, 490), 190)

func _arrow(p: Vector2, radius: float, color: Color, angle: float = 0.0) -> void:
	var shape := PackedVector2Array()
	for v in [Vector2(-0.7, 0), Vector2(0, -0.8), Vector2(0.7, 0), Vector2(0.3, 0), Vector2(0.3, 0.8), Vector2(-0.3, 0.8), Vector2(-0.3, 0)]:
		shape.append(p + (v as Vector2).rotated(angle) * radius)
	draw_colored_polygon(shape, color)

func _star(p: Vector2, radius: float, color: Color) -> void:
	var shape := PackedVector2Array()
	for i in range(10):
		shape.append(p + Vector2.from_angle(-PI * 0.5 + i * TAU / 10) * radius * (1 if i % 2 == 0 else 0.48))
	draw_colored_polygon(shape, color)

func _glyph(center: Vector2, value: String, font_size: int, color: Color) -> void:
	var font := ThemeDB.fallback_font
	var width := font.get_string_size(value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	draw_string(font, center + Vector2(-width * 0.5, font_size * 0.32), value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)
