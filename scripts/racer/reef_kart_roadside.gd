extends RefCounted
## Painted roadside architecture on the same Canvas projection as the karts.
## Each entry defines a room vignette, its frontage, depth, deck height and cap.
const PAINT := "res://assets/racer/roadside_v1/fascias.png"
const ROOMS := {
	"playroom": [
		[0, 0.075, -1, 520.0, 242.0, 48.0, Color("#ded3b5"), Color("#f2cfa6")],
		[0, 0.335, -1, 560.0, 258.0, 34.0, Color("#cf9db9"), Color("#e9c3b9")],
		[0, 0.565, -1, 540.0, 274.0, 27.0, Color("#b9a17e"), Color("#e8c79b")],
		[0, 0.850, 1, 520.0, 236.0, 62.0, Color("#ad9fca"), Color("#e8c9a3")],
	],
	"kitchen": [
		[1, 0.105, -1, 640.0, 242.0, 83.0, Color("#e9d3a9"), Color("#f4d8af")],
		[1, 0.350, 1, 620.0, 258.0, 65.0, Color("#d7ac8b"), Color("#efc293")],
		[1, 0.596, -1, 610.0, 244.0, 55.0, Color("#c2d1bd"), Color("#e1d7b9")],
		[1, 0.850, -1, 650.0, 276.0, 92.0, Color("#c1d5cc"), Color("#f0d5aa")],
	],
	"mermaid_pool": [
		[2, 0.070, -1, 520.0, 250.0, 44.0, Color("#ead4b6"), Color("#f2cead")],
		[2, 0.348, -1, 710.0, 300.0, 24.0, Color("#54a8bc"), Color("#f1c9a4")],
		[2, 0.642, -1, 720.0, 330.0, 18.0, Color("#529bb6"), Color("#e6be9e")],
		[2, 0.835, 1, 650.0, 295.0, 24.0, Color("#65afbd"), Color("#f0cca9")],
	],
	"opera_hall": [
		[3, 0.100, -1, 600.0, 250.0, 60.0, Color("#b69aae"), Color("#e6c69e")],
		[3, 0.355, -1, 610.0, 240.0, 54.0, Color("#ae86a9"), Color("#d8b793")],
		[3, 0.605, -1, 720.0, 294.0, 69.0, Color("#bd9d7e"), Color("#e5c298")],
		[3, 0.840, 1, 620.0, 266.0, 48.0, Color("#9296ad"), Color("#d1b79c")],
	],
}

const CROSSTREK_TOY := "res://assets/racer/roadside_v1/crosstrek_2021_paf.png"
const ROOM := "res://assets/flats/castle/rooms/"
const REEF := "res://assets/racer/tracks/pearl_canal/billboards/"
const DETAILS := {
	"playroom": [
		[ROOM + "room_playroom_item_blocks.png", Rect2(12, 21, 90, 71), 103.0],
		[ROOM + "room_playroom_item_stacking_toy.png", Rect2(15, 10, 92, 144), 73.0],
		[ROOM + "room_playroom_item_play_tent.png", Rect2(13, 8, 130, 120), 108.0],
		[ROOM + "room_playroom_item_blocks.png", Rect2(12, 21, 90, 71), 91.0],
	],
	"kitchen": [
		[ROOM + "room_kitchen_item_soup_pot.png", Rect2(0, 14, 273, 204), 125.0],
		[ROOM + "room_kitchen_item_pan_1.png", Rect2(4, 14, 36, 53), 66.0],
		[ROOM + "room_kitchen_item_pan_2.png", Rect2(4, 4, 40, 65), 70.0],
		[ROOM + "room_kitchen_item_pan_3.png", Rect2(4, 6, 41, 62), 72.0],
	],
	"mermaid_pool": [
		[REEF + "pearl_clam.png", Rect2(1, 0, 168, 109), 122.0],
		[REEF + "reef_fan.png", Rect2(1, 1, 265, 278), 119.0],
		[REEF + "reef_blue_shelf.png", Rect2(1, 1, 203, 164), 155.0],
		[REEF + "coral_cluster.png", Rect2(1, 1, 197, 147), 135.0],
	],
	"opera_hall": [
		[ROOM + "room_opera_hall_item_stage_star.png", Rect2(1, 4, 43, 41), 79.0],
		[ROOM + "room_opera_hall_item_footlights.png", Rect2(14, 0, 166, 22), 166.0],
		[ROOM + "room_opera_hall_item_stage_star.png", Rect2(1, 4, 43, 41), 93.0],
		[ROOM + "room_opera_hall_item_footlights.png", Rect2(14, 0, 166, 22), 141.0],
	],
}

var _canvas: CanvasItem
var _atlas: Texture2D
var _water: Texture2D
var _camera: Vector2
var _forward: Vector2
var _right: Vector2
var _focal: float
var _eye: float
var _horizon: float
var _near: float
var _mid_x: float


static func build(track: ReefKartTrack) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	var profiles: Array = ROOMS.get(track.id, [])
	for zone in range(profiles.size()):
		var profile: Array = profiles[zone]
		var side := int(profile[2])
		var station := track.length * float(profile[1])
		var size := Vector2(profile[3], profile[4])
		var deck := _place(track, station, side, size, result)
		if deck.is_empty():
			# Narrow interior sections still get a substantial fixture plinth.
			deck = _place(track, station, side, size * Vector2(0.68, 0.78), result)
		if not deck.is_empty():
			_finish(deck, profile, float(profile[5]), zone, true)
			_stage_fixtures(track, zone, deck)
			result.append(deck)
	# Reserve the large bays first. Minor pieces must fit around them.
	for zone in range(profiles.size()):
		var profile: Array = profiles[zone]
		var side := int(profile[2])
		var station := track.length * float(profile[1])
		# Low, opposing trim connects the foreground to the named room vignette.
		# Its irregular spacing leaves sightlines through the switchbacks.
		var quarter := track.length * 0.25
		for index in range(2):
			var at := station + quarter * (-0.18 if index == 0 else 0.30)
			var width := minf(quarter * (0.23 if index == 0 else 0.30), 390.0)
			var side_size := Vector2(width, 52.0 if index == 0 else 124.0)
			var edge := _place(track, at, -side, side_size, result)
			if edge.is_empty():
				edge = _place(track, at, -side, side_size * Vector2(0.70, 0.75), result)
			if edge.is_empty():
				continue
			var height := 19.0 if index == 0 else 30.0
			if int(profile[0]) == 2:
				height -= 5.0
			_finish(edge, profile, height, zone, false)
			result.append(edge)
			if index == 1:
				_add_detail(track, edge, DETAILS[track.id][zone], "roadside_detail_" + str(zone))
			elif track.id == "playroom" and zone == 3:
				# Die-cast Crosstrek on the low shelf in the toy station sector.
				var width_on_shelf := minf(146.0, (edge["half"] as Vector2).x * 1.65)
				_add_detail(track, edge, [CROSSTREK_TOY, Rect2(9, 37, 495, 207), width_on_shelf], "crosstrek_2021_paf")
	_mount_turn_signs(track, result)
	return result


static func _mount_turn_signs(track: ReefKartTrack, decks: Array[Dictionary]) -> void:
	for signpost: Dictionary in track.landmarks:
		if String(signpost["id"]) != "turn_marker":
			continue
		var origin: Vector2 = signpost["pos"]
		for deck: Dictionary in decks:
			var center: Vector2 = deck["pos"]
			var along: Vector2 = deck["along"]
			var across: Vector2 = deck["across"]
			var half: Vector2 = deck["half"]
			var offset := origin - center
			if absf(offset.dot(along)) <= half.x + 85.0 and absf(offset.dot(across)) <= half.y + 65.0:
				# Nearby furniture becomes the sign's physical mount. Keep the
				# arrow on its original approach side and outside the rail.
				var x := clampf(offset.dot(along), -half.x + 29.0, half.x - 29.0)
				var y := -(half.y - 13.0) * float(deck["side"])
				signpost["pos"] = center + along * x + across * y
				signpost["lift"] = float(deck["height"])
				signpost["supported"] = true
				signpost["w"] = 91.0
				break


static func _add_detail(track: ReefKartTrack, deck: Dictionary, spec: Array, detail_id: String) -> void:
	track.landmarks.append({"id": detail_id, "path": spec[0], "crop": spec[1],
		"pos": deck["pos"], "s": deck["s"], "w": spec[2], "max_h": 98.0,
		"lift": deck["height"], "supported": true})


static func _place(track: ReefKartTrack, station: float, side: int, size: Vector2, placed: Array[Dictionary]) -> Dictionary:
	var half := size * 0.5
	# Clearance is tested against the entire circuit, including adjacent
	# switchbacks. The half-sample margin covers the gaps between samples.
	var margin := ReefKartTrack.RAIL + 22.0 + track.length / float(ReefKartTrack.SAMPLES) * 0.5
	for direction: int in [side, -side]:
		for setback: float in [0.0, 60.0, 125.0, 205.0, 310.0, 460.0]:
			for adjustment: float in [0.0, -72.0, 72.0, -156.0, 156.0]:
				var s := track.wrap_s(station + adjustment)
				var along := track.tangent_at(s)
				var across := Vector2(-along.y, along.x)
				var center := track.point_at(s, (margin + half.y + setback) * direction)
				if _clears_route(track, center, along, across, half, margin) \
						and _clears_decks(center, along, across, half, placed):
					return {"pos": center, "s": s, "along": along, "across": across, "half": half,
						"radius": half.length(), "side": direction}
	return {}


static func _clears_route(track: ReefKartTrack, center: Vector2, along: Vector2,
		across: Vector2, half: Vector2, margin: float) -> bool:
	var reach := pow(half.length() + margin, 2.0)
	for sample: Vector2 in track.center:
		var delta := sample - center
		if delta.length_squared() > reach:
			continue
		var x := maxf(0.0, absf(delta.dot(along)) - half.x)
		var y := maxf(0.0, absf(delta.dot(across)) - half.y)
		if x * x + y * y < margin * margin:
			return false
	return true


static func _clears_decks(center: Vector2, along: Vector2, across: Vector2,
		half: Vector2, placed: Array[Dictionary]) -> bool:
	for other: Dictionary in placed:
		var delta: Vector2 = other["pos"] - center
		var lengthwise: Vector2 = other["along"]
		var crosswise: Vector2 = other["across"]
		var extent: Vector2 = other["half"]
		var separated := false
		for axis: Vector2 in [along, across, lengthwise, crosswise]:
			var own_span := absf(along.dot(axis)) * half.x + absf(across.dot(axis)) * half.y
			var other_span := absf(lengthwise.dot(axis)) * extent.x + absf(crosswise.dot(axis)) * extent.y
			if absf(delta.dot(axis)) > own_span + other_span + 6.0:
				separated = true
				break
		if not separated:
			return false
	return true


static func _finish(deck: Dictionary, profile: Array, height: float, zone: int, main: bool) -> void:
	deck["height"] = height
	deck["zone"] = zone
	deck["main"] = main
	deck["tile"] = int(profile[0])
	var cap: Color = profile[6]
	var trim: Color = profile[7]
	deck["cap"] = cap if main else cap.lerp(trim, 0.6)
	deck["trim"] = trim


static func _stage_fixtures(track: ReefKartTrack, zone: int, deck: Dictionary) -> void:
	var group: Array[Dictionary] = []
	for fixture: Dictionary in track.landmarks:
		if int(fixture.get("zone", -1)) == zone and float(fixture.get("lift", 0.0)) == 0.0:
			group.append(fixture)
	var center: Vector2 = deck["pos"]
	var along: Vector2 = deck["along"]
	var across: Vector2 = deck["across"]
	var half: Vector2 = deck["half"]
	var side := float(deck["side"])
	for index in range(group.size()):
		var fixture := group[index]
		var station := 0.0 if index == 0 else (-0.61 if index == 1 else 0.61)
		fixture["pos"] = center + along * half.x * station + across * half.y * side * (0.12 if index == 0 else -0.20)
		fixture["w"] = minf(float(fixture["w"]), half.x * (0.68 if index == 0 else 0.43))
		fixture["lift"] = float(deck["height"])
		fixture["supported"] = true


func begin(canvas: CanvasItem, camera: Vector2, heading: float, atlas: Texture2D, water: Texture2D,
		focal: float, eye: float, horizon: float, near_plane: float, mid_x: float) -> void:
	_canvas = canvas
	_camera = camera
	_forward = Vector2(sin(heading), -cos(heading))
	_right = Vector2(-_forward.y, _forward.x)
	_atlas = atlas
	_water = water
	_focal = focal
	_eye = eye
	_horizon = horizon
	_near = near_plane
	_mid_x = mid_x


func draw(deck: Dictionary) -> void:
	var center: Vector2 = deck["pos"]
	var along: Vector2 = deck["along"]
	var across: Vector2 = deck["across"]
	var half: Vector2 = deck["half"]
	var height := float(deck["height"])
	var trim: Color = deck["trim"]
	var cap: Color = deck["cap"]
	var tile := int(deck["tile"])
	var bevel := minf(20.0, half.y * 0.38)
	var corners := _beveled(center, along, across, half, bevel)
	_horizontal(_beveled(center + Vector2(9, 9), along, across, half + Vector2(13, 11), bevel + 4.0),
		0.0, Color(0.21, 0.14, 0.30, 0.16))
	for index in range(corners.size()):
		var a := corners[index]
		var b := corners[(index + 1) % corners.size()]
		var middle := (a + b) * 0.5
		if (_camera - middle).dot(middle - center) <= 0.0:
			continue
		if _atlas != null:
			_painted_wall(a, b, height, tile, trim, index % 4 == 0, index % 2 != 0)
		else:
			var corner_tint := cap.lerp(trim, 0.38).darkened(0.17)
			_quad(a, b, height, 0.0, corner_tint, PackedVector2Array(), null)
			_quad(a, b, height, height - 4.0, trim, PackedVector2Array(), null)
	if height >= _eye:
		return
	_horizontal(corners, height, trim)
	var inset := Vector2(9.0, 8.0)
	_horizontal(_beveled(center, along, across, half - inset, bevel * 0.70), height, cap)
	if bool(deck["main"]) and tile == 2 and height <= 24.0:
		# The approved pool painting supplies the inset caustic surface.
		var water_uv := PackedVector2Array([Vector2(0.25, 0.54), Vector2(0.71, 0.54),
			Vector2(0.71, 0.68), Vector2(0.25, 0.68)])
		var water_edge := _corners(center, along, across, half - Vector2(22.0, 17.0))
		_polygon(water_edge, PackedFloat32Array([height, height, height, height]), water_uv,
			Color(0.79, 0.89, 0.93), _water)
	elif bool(deck["main"]):
		var inner := _corners(center, along, across, half - Vector2(30.0, 24.0))
		_horizontal(inner, height, cap.lightened(0.08))


func _corners(center: Vector2, along: Vector2, across: Vector2, half: Vector2) -> PackedVector2Array:
	var a := along * half.x
	var b := across * half.y
	return PackedVector2Array([center - a - b, center + a - b, center + a + b, center - a + b])


func _beveled(center: Vector2, along: Vector2, across: Vector2, half: Vector2, bevel: float) -> PackedVector2Array:
	var a := along * half.x
	var b := across * half.y
	var u := along * bevel
	var v := across * bevel
	return PackedVector2Array([center - a - b + u, center + a - b - u,
		center + a - b + v, center + a + b - v, center + a + b - u, center - a + b + u,
		center - a + b - v, center - a - b + v])


func _horizontal(points: PackedVector2Array, lift: float, color: Color) -> void:
	var height := PackedFloat32Array()
	height.resize(points.size())
	height.fill(lift)
	_polygon(points, height, PackedVector2Array(), color, null)


func _painted_wall(a: Vector2, b: Vector2, height: float, tile: int, trim: Color, long: bool, bevel: bool) -> void:
	var tiles_x := float(tile % 2) * 0.5
	var tiles_y := float(tile >> 1) * 0.5
	var u0 := tiles_x + (0.006 if long else 0.026)
	var u1 := tiles_x + (0.494 if long else (0.048 if bevel else 0.122))
	var v0 := tiles_y + 0.009
	var v1 := tiles_y + 0.491
	var uv := PackedVector2Array([Vector2(u0, v1), Vector2(u1, v1), Vector2(u1, v0), Vector2(u0, v0)])
	var shade := 0.94 if long else (0.83 if bevel else 0.78)
	_quad(a, b, height, 0.0, Color(shade, shade, shade), uv, _atlas)
	_quad(a, b, height, maxf(0.0, height - 3.0), trim.lightened(0.13), PackedVector2Array(), null)


func _quad(a: Vector2, b: Vector2, upper: float, lower: float, color: Color,
		uv: PackedVector2Array, texture: Texture2D) -> void:
	_polygon(PackedVector2Array([a, b, b, a]), PackedFloat32Array([lower, lower, upper, upper]),
		uv, color, texture)


func _polygon(world: PackedVector2Array, lift: PackedFloat32Array, uv: PackedVector2Array,
		color: Color, texture: Texture2D) -> void:
	var out := PackedVector2Array()
	var texcoords := PackedVector2Array()
	var vertex_colors := PackedColorArray()
	var textured := texture != null
	# Clip edges before dividing by depth. A nearby end cannot drag an
	# entire shelf across the viewport as the camera passes it.
	for i in range(world.size()):
		var prev := (i + world.size() - 1) % world.size()
		var depth := (world[i] - _camera).dot(_forward)
		var old_depth := (world[prev] - _camera).dot(_forward)
		if (depth >= _near) != (old_depth >= _near):
			var t := (_near - old_depth) / (depth - old_depth)
			out.append(_screen(world[prev].lerp(world[i], t), lerpf(lift[prev], lift[i], t), _near))
			if textured:
				_pack_texture_vertex(texcoords, vertex_colors, uv[prev].lerp(uv[i], t), _near, color.b)
		if depth >= _near:
			out.append(_screen(world[i], lift[i], depth))
			if textured:
				_pack_texture_vertex(texcoords, vertex_colors, uv[i], depth, color.b)
	if out.size() < 3:
		return
	# Degenerate faces at the silhouette or exact near cut have no area.
	var area := 0.0
	for i in range(out.size()):
		area += out[i].cross(out[(i + 1) % out.size()])
	if absf(area) > 0.25:
		_canvas.draw_polygon(out, vertex_colors if textured else PackedColorArray([color]), texcoords, texture)


func _pack_texture_vertex(uvs: PackedVector2Array, colors: PackedColorArray, uv: Vector2, depth: float, shade: float) -> void:
	var q := _near / depth
	var low := q * 255.0
	uvs.append(Vector2(2.0, 2.0) + uv * q)
	colors.append(Color(floorf(low) / 255.0, fposmod(low, 1.0), shade, 1.0))


func _screen(world: Vector2, lift: float, depth: float) -> Vector2:
	var scale := _focal / depth
	return Vector2(_mid_x + (world - _camera).dot(_right) * scale, _horizon + (_eye - lift) * scale)
