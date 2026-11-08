extends "res://assets_src/imagegen/reef_kart_riders_20261107/build_rider_atlases.gd"
## Build whole Canvas cards from the registered, painted rider sources.
## The upper silhouette changes while hands, hips and chassis stay registered.
const DEST_V2 := "res://assets/racer/rider_poses_v2/"
const V1 := "res://assets/racer/riders_v1/"
const PACK := 200
const SHEET := 1000
const DRIVERS := ["sparkle", "huluu", "bunny", "kitty", "baby_doll", "dolly",
	"sleepy", "imp", "rumi", "daddy", "mama_baby"]
const VEHICLES := ["kart", "moto", "truck"]
const TURN := [0.0, -0.50, -1.0, 0.50, 1.0, 0.0, 0.0]
const TUCK := [0.0, 0.0, 0.0, 0.0, 0.0, 0.52, 1.0]
# Crown/shoulder excursion and tuck by anatomy, in the 256px source cell.
const STYLE := [
	Vector2(15.0, 0.29), Vector2(17.0, 0.32), Vector2(14.0, 0.29),
	Vector2(13.0, 0.28), Vector2(14.0, 0.30), Vector2(16.0, 0.30),
	Vector2(13.0, 0.27), Vector2(17.0, 0.33), Vector2(19.0, 0.31),
	Vector2(15.0, 0.32), Vector2(13.0, 0.28),
]
const RIDE_LEAN := [1.0, 1.13, 0.92]

func _initialize() -> void:
	var riders := _source_riders()
	var bodies: Array[Image] = []
	var neutral_sheets: Array[Image] = []
	for ride: String in VEHICLES:
		neutral_sheets.append(Image.load_from_file(V1 + ride + ".png"))
		bodies.append(_chassis(ride))
	for i in range(DRIVERS.size()):
		var atlas := Image.create(SHEET, SHEET, false, Image.FORMAT_RGBA8)
		for v in range(VEHICLES.size()):
			var ride: String = VEHICLES[v]
			var body := bodies[v]
			var setup: Array = RIDES[ride]
			var neutral := neutral_sheets[v].get_region(Rect2i(Vector2i(i % 4, i / 4) * CELL, Vector2i(CELL, CELL)))
			var grip := int(setup[1]) - int(RIDERS[i][3])
			for phase in range(TURN.size()):
				var card := neutral.duplicate() as Image
				if phase != 0:
					var key := i
					if i == 0 and phase == 2:
						key = 11
					elif i == 0 and phase == 4:
						key = 12
					card = _authored_key(body, neutral, riders[key], RIDERS[key],
						grip, Vector2(TURN[phase] * STYLE[i].x * RIDE_LEAN[v], TUCK[phase] * STYLE[i].y))
				var bounds := card.get_used_rect()
				if bounds.position.x < 12 or bounds.position.y < 10 or bounds.end.x > CELL - 12 or bounds.end.y != BASELINE:
					push_error("%s %s phase %d exceeds registered card bounds: %s" % [DRIVERS[i], ride, phase, bounds])
					quit(2)
					return
				card.resize(PACK, PACK, Image.INTERPOLATE_LANCZOS)
				var index := v * TURN.size() + phase
				atlas.blit_rect(card, Rect2i(Vector2i.ZERO, card.get_size()), Vector2i(index % 5, index / 5) * PACK)
		if atlas.save_png(DEST_V2 + DRIVERS[i] + ".png") != OK:
			quit(1)
			return
		print("CAST_KEYS|", DRIVERS[i], "|", VEHICLES.size() * TURN.size())
	quit(0)

func _source_riders() -> Array[Image]:
	var eagle := Image.load_from_file(SOURCE + "eagle_native.png")
	var toys := Image.load_from_file(SOURCE + "toy_native.png")
	var family := Image.load_from_file(SOURCE + "family_native.png")
	var keys: Array[Image] = [
		_cell(eagle, 0, 0, 3, 1),
		_trim(family.get_region(Rect2i(0, 0, 654, 567))),
	]
	for i in range(6):
		keys.append(_cell(toys, i % 3, i / 3, 3, 2))
	keys.append(_trim(family.get_region(Rect2i(654, 0, 655, 590))))
	keys.append(_trim(family.get_region(Rect2i(0, 567, 654, 635))))
	keys.append(_trim(family.get_region(Rect2i(654, 590, 655, 612))))
	keys.append(_cell(eagle, 1, 0, 3, 1))
	keys.append(_cell(eagle, 2, 0, 3, 1))
	return keys

func _chassis(ride: String) -> Image:
	var source := _trim(Image.load_from_file("res://assets/kart/chase/empty_%s.png" % ride))
	var width := int(RIDES[ride][0])
	var height := roundi(float(source.get_height() * width) / source.get_width())
	source.resize(width, height, Image.INTERPOLATE_LANCZOS)
	var body := Image.create(CELL, CELL, false, Image.FORMAT_RGBA8)
	body.blit_rect(source, Rect2i(Vector2i.ZERO, source.get_size()),
		Vector2i((CELL - width) / 2, BASELINE - height))
	return body

func _authored_key(body: Image, neutral: Image, source: Image, spec: Array,
		grip: int, action: Vector2) -> Image:
	var height := mini(int(spec[0]), floori(float(grip - 14) / float(spec[1])))
	var width := roundi(float(source.get_width() * height) / source.get_height())
	var contact := Vector2i(roundi(width * float(spec[2])), roundi(height * float(spec[1])))
	var origin := Vector2i(CELL / 2, grip) - contact
	var rider := source.duplicate() as Image
	rider.resize(width, height, Image.INTERPOLATE_LANCZOS)
	rider.premultiply_alpha()
	var region := Rect2i(origin.x - 24, 8, width + 48, grip - 12)
	var upper := Image.create(region.size.x, region.size.y, false, Image.FORMAT_RGBA8)
	for row in range(region.size.y):
		var y := region.position.y + row
		var rise := smoothstep(5.0, maxf(14.0, float(contact.y) * 0.53), float(grip - y))
		var lean := action.x * rise * 0.90
		var tuck := action.y * rise
		for column in range(region.size.x):
			var x := region.position.x + column - CELL / 2
			# Torso bends and shoulders roll around the fixed grip row.
			# Unequal near/far compression preserves the sense of turning.
			var side := signf(float(x) - lean)
			var turn := signf(action.x)
			var width_ratio := 1.0 - tuck * 0.23 + side * turn * rise * 0.055
			var sx := (float(x) - lean) / width_ratio + contact.x
			var sy := float(y - origin.y) - tuck * float(contact.y) * 0.78
			sy += (sx - contact.x) * lean * 0.009
			var pixel := _paint_sample(rider, sx, sy)
			upper.set_pixel(column, row, pixel)
	var result := body.duplicate() as Image
	result.blend_rect(upper, Rect2i(Vector2i.ZERO, upper.get_size()), region.position)
	# Copy the whole fixed contact band from the neutral sprite. This also
	# preserves the exact forearms, grip, seatback and shell paint.
	var held := Rect2i(0, grip - 4, CELL, CELL - grip + 4)
	result.blit_rect(neutral, held, held.position)
	return result

func _paint_sample(image: Image, x: float, y: float) -> Color:
	var left := floori(x)
	var top := floori(y)
	if left < 0 or top < 0 or left >= image.get_width() - 1 or top >= image.get_height() - 1:
		return Color.TRANSPARENT
	var a := image.get_pixel(left, top).lerp(image.get_pixel(left + 1, top), x - left)
	var b := image.get_pixel(left, top + 1).lerp(image.get_pixel(left + 1, top + 1), x - left)
	var pixel := a.lerp(b, y - top)
	if pixel.a < 0.004:
		return Color.TRANSPARENT
	return Color(pixel.r / pixel.a, pixel.g / pixel.a, pixel.b / pixel.a, pixel.a)
