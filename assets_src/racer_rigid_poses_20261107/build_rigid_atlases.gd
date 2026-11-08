extends "res://assets_src/racer_pose_keys_20261107/build_pose_atlases.gd"
## Reuse one neutral drawing for every motion. The rider leans around the seat
## with a rigid 2D transform, then the original foreground closes the cockpit.
const DEST_V3 := "res://assets/racer/rider_poses_v3/"
const ROSTER := ["roshan", "sparkle", "huluu", "bunny", "kitty", "baby_doll",
	"dolly", "sleepy", "imp", "rumi", "daddy", "mama_baby"]
const TURN_ANGLE := [7.5, 7.5, 8.0, 7.0, 6.0, 6.0, 6.5, 5.5, 7.0, 8.0, 7.5, 5.5]
const BOOST_DROP := [7.0, 6.0, 7.0, 5.0, 5.0, 6.0, 6.0, 5.0, 6.0, 7.0, 6.0, 5.0]
const ROSHAN_SIZE := 230
const ROSHAN_AXLES := [Vector2(335, 546.5), Vector2(310.5, 621), Vector2(330.25, 594.5)]
# Roshan's existing whole drawings include her tail, sleeves and vehicle.
# The upper range includes the helmet and crown of the hair. The short
# shoulder band beneath it returns to the original cockpit drawing.
const ROSHAN_BANDS := [Vector2(94, 110), Vector2(65, 82), Vector2(82, 103)]

func _initialize() -> void:
	var riders := _source_riders()
	var neutral_sheets: Array[Image] = []
	var bodies: Array[Image] = []
	for ride: String in VEHICLES:
		neutral_sheets.append(Image.load_from_file(V1 + ride + ".png"))
		bodies.append(_chassis(ride))
	for i in range(ROSTER.size()):
		var atlas := Image.create(SHEET, SHEET, false, Image.FORMAT_RGBA8)
		for v in range(VEHICLES.size()):
			var ride: String = VEHICLES[v]
			var neutral := _roshan_card(ride, v) if i == 0 else _neutral_card(neutral_sheets[v], i - 1)
			var spec: Array = RIDES[ride]
			for phase in range(TURN.size()):
				var card := neutral.duplicate() as Image
				if phase != 0:
					var angle := deg_to_rad(TURN[phase] * TURN_ANGLE[i] * RIDE_LEAN[v])
					var drop := roundf(TUCK[phase] * BOOST_DROP[i])
					if i == 0:
						var bands: Vector2 = Vector2(BASELINE, BASELINE) + (ROSHAN_BANDS[v] - Vector2(BASELINE, BASELINE)) * float(ROSHAN_SIZE) / CELL
						card = _roshan_key(neutral, bands, angle, drop)
					else:
						card = _seated_key(bodies[v], neutral, riders[i - 1], RIDERS[i - 1], spec, angle, drop)
				var bounds := card.get_used_rect()
				if bounds.position.x < 6 or bounds.position.y < 0 or bounds.end.x > CELL - 6 						or bounds.end.y != neutral.get_used_rect().end.y:
					push_error("%s %s phase %d exceeds registered card bounds: %s" % [ROSTER[i], ride, phase, bounds])
					quit(2)
					return
				card.resize(PACK, PACK, Image.INTERPOLATE_LANCZOS)
				var index := v * TURN.size() + phase
				atlas.blit_rect(card, Rect2i(Vector2i.ZERO, card.get_size()), Vector2i(index % 5, index / 5) * PACK)
		if atlas.save_png(DEST_V3 + ROSTER[i] + ".png") != OK:
			quit(1)
			return
		print("RIGID_KEYS|", ROSTER[i], "|", VEHICLES.size() * TURN.size())
	quit(0)

func _neutral_card(sheet: Image, index: int) -> Image:
	return sheet.get_region(Rect2i(Vector2i(index % 4, index / 4) * CELL, Vector2i(CELL, CELL)))

func _roshan_card(ride: String, index: int) -> Image:
	var source := Image.load_from_file("res://assets/kart/chase/%s_straight.png" % ride)
	source.convert(Image.FORMAT_RGBA8)
	var anchor: Vector2 = ROSHAN_AXLES[index] * float(ROSHAN_SIZE) / source.get_width()
	source.resize(ROSHAN_SIZE, ROSHAN_SIZE, Image.INTERPOLATE_LANCZOS)
	var offset := Vector2i((Vector2(CELL * 0.5, BASELINE) - anchor).round())
	var card := Image.create(CELL, CELL, false, Image.FORMAT_RGBA8)
	card.blit_rect(source, Rect2i(Vector2i.ZERO, source.get_size()), offset)
	return card

func _seated_key(body: Image, neutral: Image, source: Image, rider_spec: Array, ride_spec: Array,
		angle: float, drop: float) -> Image:
	var grip := int(ride_spec[1]) - int(rider_spec[3])
	var height := mini(int(rider_spec[0]), floori(float(grip - 14) / float(rider_spec[1])))
	var width := roundi(float(source.get_width() * height) / source.get_height())
	var contact := Vector2(roundf(width * float(rider_spec[2])), roundf(height * float(rider_spec[1])))
	var pivot := Vector2(CELL * 0.5, grip)
	var rider := source.duplicate() as Image
	rider.resize(width, height, Image.INTERPOLATE_LANCZOS)
	rider.premultiply_alpha()
	var area := Rect2i(Vector2i(pivot - contact) - Vector2i(14, 13), Vector2i(width + 28, height + 30))
	area = area.intersection(Rect2i(0, 0, CELL, CELL))
	var moved := Image.create(area.size.x, area.size.y, false, Image.FORMAT_RGBA8)
	var inverse := Transform2D(-angle, Vector2.ZERO)
	for y in range(area.size.y):
		for x in range(area.size.x):
			var at := Vector2(area.position + Vector2i(x, y)) - pivot - Vector2(0, drop)
			# The same rotation and translation apply to every head, ear,
			# hat and torso pixel. No side scaling, shear or row remapping.
			var sample_at := inverse * at + contact
			moved.set_pixel(x, y, _paint_sample(rider, sample_at.x, sample_at.y))
	var result := body.duplicate() as Image
	result.blend_rect(moved, Rect2i(Vector2i.ZERO, moved.get_size()), area.position)
	_copy_cockpit(result, neutral, ride_spec[2])
	return result

func _copy_cockpit(card: Image, neutral: Image, edge: Array) -> void:
	var segment := 0
	for x in range(CELL):
		while x > int(edge[segment + 1][0]):
			segment += 1
		var a: Array = edge[segment]
		var b: Array = edge[segment + 1]
		var y := roundi(lerpf(float(a[1]), float(b[1]), inverse_lerp(float(a[0]), float(b[0]), float(x))))
		card.blit_rect(neutral, Rect2i(x, y, 1, CELL - y), Vector2i(x, y))

func _roshan_key(neutral: Image, bands: Vector2, angle: float, drop: float) -> Image:
	var result := neutral.duplicate() as Image
	var source := neutral.duplicate() as Image
	source.premultiply_alpha()
	var pivot := Vector2(CELL * 0.5, bands.y)
	var inverse := Transform2D(-angle, Vector2.ZERO)
	for y in range(int(bands.y)):
		for x in range(32, 224):
			var pixel := Vector2(x, y)
			var moved := inverse * (pixel - pivot - Vector2(0, drop)) + pivot
			var weight := 1.0 - smoothstep(bands.x, bands.y, moved.y)
			# The helmet and upper hair use the rigid coordinates exactly.
			# The flex begins at the lower hair and shoulder junction.
			var at := pixel.lerp(moved, weight)
			result.set_pixel(x, y, _paint_sample(source, at.x, at.y))
	return result
