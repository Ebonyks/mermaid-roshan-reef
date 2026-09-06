class_name OperaWorldBackdrop2D
extends Control
## Scalable, code-native scenery for the Opera career worlds.
##
## The accepted 1024x576 scene keys remain composition references: they do not
## meet the project's 2048px-per-playable-screen raster rule. These lightweight
## vector sets preserve each job's landmarks without stretching a concept key.

const PALETTES := {
	"chef": [Color("#4a234f"), Color("#f2a5a0"), Color("#ffd66e")],
	"detective": [Color("#182452"), Color("#546aa8"), Color("#f8d469")],
	"ballerina": [Color("#334f7a"), Color("#d28ed0"), Color("#8fe7df")],
	"candymaker": [Color("#7d355f"), Color("#f397ad"), Color("#72d8cc")],
	"doctor": [Color("#245a6c"), Color("#9de0d8"), Color("#f2faf2")],
	"farmer": [Color("#559bc2"), Color("#75a85b"), Color("#f4ce67")],
	"boxer": [Color("#171936"), Color("#b43e52"), Color("#efc85d")],
	"magician": [Color("#251747"), Color("#714a9a"), Color("#f3ca5f")],
	"painter": [Color("#a84e5b"), Color("#f3a45d"), Color("#ffe599")],
	"astronaut": [Color("#111d48"), Color("#315d9b"), Color("#72d9e8")],
	"racer": [Color("#18234a"), Color("#4b5190"), Color("#ef5a59")],
	"nursery": [Color("#202452"), Color("#88c9bd"), Color("#f4c7a7")],
	"popstar": [Color("#34164d"), Color("#9c3c8c"), Color("#62d9e8")],
	"geologist": [Color("#172b4d"), Color("#725b8f"), Color("#72e0d3")],
}
const SKY_LAGOON_ROOT := "res://assets/flats/sky_lagoon/main/"

var career_id := "chef"
var scene_variant := ""
var elapsed := 0.0
var redraw_t := 0.0
## When true the career set is framed by the proscenium: arch, curtain swags,
## footlights and a warmer wash — the finale-on-stage look. Follows the
## stage/backstage kit grammar from assets_src/concepts/opera_house_flat/.
var stage_mode := false
## The racing surface uses the native painting coordinates, without the
## promotion tool's padded blur. This is framing, not a native-resolution pass.
var racer_driving := false
## The accepted codex career-world painting (owner decision 2026-08-01:
## the 1024x576 scene keys ARE the career backdrops — same 16:9 aspect as
## the 1280x720 viewport). The vector set below remains the fallback.
var painting: Texture2D = null
var world_tiles: Array[Texture2D] = []
var stage_tiles: Array[Texture2D] = []
var room_variant_tiles: Array[Texture2D] = []
var sky_lagoon_tiles: Array[Texture2D] = []


func setup(id: String, variant: String = "") -> void:
	career_id = id
	scene_variant = variant
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_meta("chapter2_scene_variant", scene_variant)
	set_meta("chapter2_scene_specific_2d", not scene_variant.is_empty())
	if career_id == "teacher":
		painting = null
		world_tiles.clear()
		stage_tiles.clear()
		room_variant_tiles.clear()
		for row in range(2):
			for column in range(4):
				var tile := "res://assets/flats/castle/interactions_v4/background_tiles/room_library_background_r%d_c%d.png" % [row, column]
				room_variant_tiles.append(load(tile) as Texture2D)
		queue_redraw()
		return
	if scene_variant == "stuffie_room":
		painting = null
		world_tiles.clear()
		stage_tiles.clear()
		room_variant_tiles = _load_stuffie_room_tiles()
		sky_lagoon_tiles.clear()
		queue_redraw()
		return
	if scene_variant == "sky_lagoon_farmer":
		painting = null
		world_tiles.clear()
		stage_tiles.clear()
		room_variant_tiles.clear()
		sky_lagoon_tiles = _load_sky_lagoon_tiles()
		queue_redraw()
		return
	var path := "res://assets/opera/worlds/backdrops/world_%s.png" % id
	painting = load(path) as Texture2D if ResourceLoader.exists(path) else null
	world_tiles = _load_tile_set("world")
	stage_tiles = _load_tile_set("stage")
	room_variant_tiles.clear()
	sky_lagoon_tiles.clear()
	queue_redraw()


func _load_sky_lagoon_tiles() -> Array[Texture2D]:
	var textures: Array[Texture2D] = []
	# The center meadow is a single contiguous 2x2 crop of the approved 6x2
	# Sky Lagoon panorama. Keeping the source tiles intact preserves their
	# authored seams and avoids inventing a separate Farmer background.
	for row in range(2):
		for column in range(2, 4):
			var path := SKY_LAGOON_ROOT \
				+ "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png" % [row, column]
			if not ResourceLoader.exists(path):
				return []
			var texture := load(path) as Texture2D
			if texture == null:
				return []
			textures.append(texture)
	return textures


func _load_stuffie_room_tiles() -> Array[Texture2D]:
	var textures: Array[Texture2D] = []
	for row in range(2):
		for column in range(4):
			var path := "res://assets/flats/castle/rooms/background_tiles/" \
				+ "room_playroom_background_r%d_c%d.png" % [row, column]
			if not ResourceLoader.exists(path):
				return []
			var texture := load(path) as Texture2D
			if texture == null:
				return []
			textures.append(texture)
	return textures


func _draw_stuffie_room_tiles() -> void:
	var destination_size := Vector2(size.x / 4.0, size.y / 2.0)
	for row in range(2):
		for column in range(4):
			var destination := Rect2(
				Vector2(float(column) * destination_size.x,
					float(row) * destination_size.y),
				destination_size)
			draw_texture_rect(room_variant_tiles[row * 4 + column],
				destination, false)


func _draw_sky_lagoon_farmer() -> void:
	if sky_lagoon_tiles.size() != 4:
		return
	var half := size * 0.5
	for row in range(2):
		for column in range(2):
			# Use the same central 576px vertical crop as the accepted flat-world
			# renderer, keeping sky, flowering meadow, path, and foreground in a
			# readable 16:9 frame on the fixed 1280x720 canvas.
			var source := Rect2(0.0, 224.0, 1024.0, 576.0)
			var destination := Rect2(
				Vector2(float(column) * half.x, float(row) * half.y), half)
			draw_texture_rect_region(sky_lagoon_tiles[row * 2 + column],
				destination, source)
	# A soft harvest basket makes the task's destination legible without
	# replacing the approved world art or turning the scene into a card.
	draw_circle(Vector2(1040.0, 620.0), 48.0, Color("#b87855"))
	draw_arc(Vector2(1040.0, 618.0), 48.0, PI, TAU, 24, Color("#f0c274"), 8.0)


func _load_tile_set(kind: String) -> Array[Texture2D]:
	var textures: Array[Texture2D] = []
	for row in range(2):
		for column in range(2):
			var path: String
			if career_id == "ballerina" and kind == "stage":
				path = "res://assets/opera/worlds/stage/finale_stage_c%dr%d.png" % [column, row]
			else:
				path = "res://assets/opera/worlds/backdrops/%s_%s_c%dr%d.png" % [
					kind, career_id, column, row,
				]
			if not ResourceLoader.exists(path):
				return []
			var texture := load(path) as Texture2D
			if texture == null:
				return []
			textures.append(texture)
	return textures


func _draw_tile_set(textures: Array[Texture2D]) -> void:
	# The authored 16:9 playfield occupies y=448..1600 of the 2048-square
	# master. Draw the central 576px from each POT row into a screen quadrant.
	var half := size * 0.5
	for row in range(2):
		for column in range(2):
			var source_y := 448.0 if row == 0 else 0.0
			var source := Rect2(0.0, source_y, 1024.0, 576.0)
			var destination := Rect2(Vector2(float(column) * half.x, float(row) * half.y), half)
			draw_texture_rect_region(textures[row * 2 + column], destination, source)


func _draw_racer_circuit() -> void:
	# Reconstruct only the unchanged native painting from the padded POT tiles.
	# Coordinates come from the promotion manifest's 1672x941 source master.
	var native_rect := Rect2(188, 553, 1672, 941)
	for row in range(2):
		for column in range(2):
			var tile_origin := Vector2(column * 1024, row * 1024)
			var overlap := native_rect.intersection(Rect2(tile_origin, Vector2(1024, 1024)))
			var source := Rect2(overlap.position - tile_origin, overlap.size)
			var destination := Rect2((overlap.position - native_rect.position) / native_rect.size * size,
				overlap.size / native_rect.size * size)
			draw_texture_rect_region(world_tiles[row * 2 + column], destination, source)


func set_stage(on_stage: bool) -> void:
	if stage_mode == on_stage:
		return
	stage_mode = on_stage
	queue_redraw()


func _process(delta: float) -> void:
	elapsed += delta
	redraw_t += delta
	if redraw_t >= 0.08:
		redraw_t = 0.0
		queue_redraw()


func _draw() -> void:
	if career_id == "teacher" and room_variant_tiles.size() == 8:
		_draw_stuffie_room_tiles()
		return
	if racer_driving and career_id == "racer" and world_tiles.size() == 4:
		_draw_racer_circuit()
		return
	if scene_variant == "stuffie_room" and room_variant_tiles.size() == 8:
		_draw_stuffie_room_tiles()
		if stage_mode:
			_draw_spotlights(Color("#f2d66c"))
		return
	if scene_variant == "sky_lagoon_farmer":
		_draw_sky_lagoon_farmer()
		return
	var palette: Array = PALETTES.get(career_id, PALETTES["chef"])
	var sky := Color(palette[0])
	var mid := Color(palette[1])
	var accent := Color(palette[2])
	var active_tiles: Array[Texture2D] = stage_tiles if stage_mode and stage_tiles.size() == 4 else world_tiles
	if active_tiles.size() == 4:
		_draw_tile_set(active_tiles)
		_draw_spotlights(accent)
		return
	if painting != null:
		draw_texture_rect(painting, Rect2(Vector2.ZERO, size), false)
		# spotlights are stage lighting — over a painted district they fight
		# the art's own light sources
		if stage_mode:
			_draw_spotlights(accent)
		if stage_mode:
			_draw_stage_frame(accent)
		return
	draw_rect(Rect2(Vector2.ZERO, size), sky)
	draw_rect(Rect2(0, size.y * 0.42, size.x, size.y * 0.58), mid.darkened(0.44))
	draw_polygon(
		PackedVector2Array([
			Vector2(0, size.y * 0.44),
			Vector2(size.x * 0.5, size.y * 0.30),
			Vector2(size.x, size.y * 0.44),
		]),
		PackedColorArray([mid.darkened(0.20)])
	)
	_draw_spotlights(accent)
	match career_id:
		"chef":
			_draw_chef(mid, accent)
		"detective":
			_draw_detective(mid, accent)
		"ballerina":
			_draw_ballerina(mid, accent)
		"candymaker":
			_draw_candy(mid, accent)
		"doctor":
			_draw_doctor(mid, accent)
		"farmer":
			_draw_farmer(mid, accent)
		"boxer":
			_draw_boxer(mid, accent)
		"magician":
			_draw_magician(mid, accent)
		"painter":
			_draw_painter(mid, accent)
		"astronaut":
			_draw_astronaut(mid, accent)
		"racer":
			_draw_racer(mid, accent)
		"nursery":
			_draw_nursery(mid, accent)
		"popstar":
			_draw_popstar(mid, accent)
		"geologist":
			_draw_geologist(mid, accent)
	if stage_mode:
		# curtains and columns occlude the set — theatrically correct layering
		_draw_stage_frame(accent)


func _draw_stage_frame(accent: Color) -> void:
	var plum := Color("#58375f")
	var brass := Color("#c88b3c")
	# side proscenium columns with brass trim
	for x in [0.0, size.x - 84.0]:
		draw_rect(Rect2(x, 0, 84, size.y), plum.darkened(0.25), true)
		draw_rect(Rect2(x + (66.0 if x == 0.0 else 4.0), 0, 14, size.y), brass, true)
	# top valance with a scalloped hem of curtain swags
	draw_rect(Rect2(0, 0, size.x, 96), plum, true)
	for index in range(9):
		var cx := 64.0 + float(index) * 144.0
		draw_circle(Vector2(cx, 96), 46, plum.darkened(0.12))
	draw_line(Vector2(0, 8), Vector2(size.x, 8), brass, 6.0)
	# deep side curtains sweeping in from the corners
	draw_polygon(
		PackedVector2Array([Vector2(84, 0), Vector2(240, 0), Vector2(120, size.y * 0.62), Vector2(84, size.y * 0.62)]),
		PackedColorArray([plum.lightened(0.08)])
	)
	draw_polygon(
		PackedVector2Array([Vector2(size.x - 240, 0), Vector2(size.x - 84, 0), Vector2(size.x - 84, size.y * 0.62), Vector2(size.x - 120, size.y * 0.62)]),
		PackedColorArray([plum.lightened(0.08)])
	)
	# footlight apron row with a warm glow — the audience side of the stage
	var glow := 0.28 + (sin(elapsed * 3.1) + 1.0) * 0.05
	for index in range(8):
		var fx := 150.0 + float(index) * 140.0
		draw_circle(Vector2(fx, size.y - 132.0), 30, Color(accent, glow * 0.5))
		draw_circle(Vector2(fx, size.y - 132.0), 12, Color("#ffe0a6"))
	draw_line(Vector2(84, size.y - 108.0), Vector2(size.x - 84, size.y - 108.0), brass, 8.0)


func _draw_spotlights(accent: Color) -> void:
	var pulse := 0.08 + (sin(elapsed * 2.2) + 1.0) * 0.025
	if stage_mode:
		pulse += 0.05
	draw_polygon(
		PackedVector2Array([Vector2(90, 0), Vector2(310, 0), Vector2(520, 620), Vector2(250, 620)]),
		PackedColorArray([Color(accent, pulse)])
	)
	draw_polygon(
		PackedVector2Array([Vector2(970, 0), Vector2(1190, 0), Vector2(1030, 620), Vector2(760, 620)]),
		PackedColorArray([Color(accent, pulse)])
	)


func _draw_chef(mid: Color, accent: Color) -> void:
	for x in [80.0, 1010.0]:
		draw_rect(Rect2(x, 240, 190, 250), mid.darkened(0.38), true)
		draw_rect(Rect2(x + 20, 275, 150, 118), Color("#55314e"), true)
		for i in range(3):
			draw_circle(Vector2(x + 48 + i * 47, 438), 13, accent)
	draw_rect(Rect2(260, 470, 760, 95), Color("#8e5365"), true)
	for i in range(5):
		draw_circle(Vector2(405 + i * 115, 452), 22, Color.from_hsv(0.02 + i * 0.12, 0.48, 1.0))
	draw_rect(Rect2(575, 350, 130, 120), Color("#fff0d5"), true)
	draw_circle(Vector2(640, 346), 72, Color("#ffb5bd"))


func _draw_detective(mid: Color, accent: Color) -> void:
	for x in [55.0, 1005.0]:
		draw_rect(Rect2(x, 190, 220, 360), mid.darkened(0.46), true)
		for row in range(4):
			draw_line(Vector2(x + 18, 245 + row * 74), Vector2(x + 202, 245 + row * 74), accent.darkened(0.2), 7)
			for col in range(5):
				draw_rect(Rect2(x + 24 + col * 35, 208 + row * 74, 24, 32), Color("#8a5f79"), true)
	draw_circle(Vector2(640, 185), 94, Color("#f7e39a"))
	for i in range(7):
		var p := Vector2(365 + i * 88, 520 + sin(float(i)) * 32)
		draw_circle(p, 12, accent)
		draw_circle(p, 4, Color.WHITE)


func _draw_ballerina(mid: Color, accent: Color) -> void:
	for x in [210.0, 640.0, 1070.0]:
		draw_arc(Vector2(x, 390), 170, PI, TAU, 28, accent, 14)
	# recital floor of alternating shell/pearl tiles
	for i in range(9):
		var tile_col := mid.lightened(0.22) if i % 2 == 0 else Color("#f6e7c8")
		draw_rect(Rect2(115 + i * 118, 560, 106, 34), tile_col, true)
	for i in range(8):
		var p1 := Vector2(120 + i * 145, 555)
		var p2 := Vector2(200 + i * 145, 470)
		draw_line(p1, p2, Color("#f7c3e1"), 7)
	# slowly turning mirror ball with sparkle points
	var ball := Vector2(640, 175)
	draw_circle(ball, 44, mid.lightened(0.3))
	for i in range(6):
		var spark := ball + Vector2.from_angle(elapsed * 0.9 + float(i) * TAU / 6.0) * 62.0
		draw_circle(spark, 5, Color.WHITE)
	var ribbon := PackedVector2Array()
	for i in range(25):
		ribbon.append(Vector2(120 + i * 44, 330 + sin(float(i) * 0.7 + elapsed) * 55))
	draw_polyline(ribbon, Color("#78ece1"), 10)


func _draw_candy(mid: Color, accent: Color) -> void:
	for x in [120.0, 910.0]:
		draw_circle(Vector2(x + 110, 380), 112, mid.lightened(0.16))
		draw_rect(Rect2(x + 58, 220, 104, 100), accent.darkened(0.15), true)
	draw_rect(Rect2(210, 505, 860, 70), Color("#513557"), true)
	for i in range(10):
		var c := Color.from_hsv(float(i) / 10.0, 0.48, 1.0)
		draw_circle(Vector2(250 + i * 86, 500), 25, c)
		draw_line(Vector2(222 + i * 86, 500), Vector2(278 + i * 86, 500), Color.WHITE, 4)


func _draw_doctor(mid: Color, accent: Color) -> void:
	for x in [100.0, 940.0]:
		draw_rect(Rect2(x, 270, 240, 250), Color("#dff7ef"), true)
		draw_rect(Rect2(x + 26, 302, 188, 120), mid.darkened(0.34), true)
		draw_line(Vector2(x + 120, 325), Vector2(x + 120, 398), accent, 13)
		draw_line(Vector2(x + 82, 361), Vector2(x + 158, 361), accent, 13)
	draw_rect(Rect2(475, 195, 330, 220), Color("#1c3551"), true)
	draw_line(Vector2(560, 250), Vector2(715, 360), Color("#baf5f3"), 10)
	draw_circle(Vector2(560, 250), 24, Color("#baf5f3"))
	# gentle heartbeat ripple across the x-ray screen
	var beat := PackedVector2Array()
	for i in range(12):
		var bump := 26.0 if i == 5 else (-20.0 if i == 6 else 0.0)
		beat.append(Vector2(505 + i * 25, 390 + bump + sin(elapsed * 2.0) * 3.0))
	draw_polyline(beat, Color("#8ef2c8"), 6)
	# waiting bench with plushy patients
	draw_rect(Rect2(430, 545, 420, 26), mid.darkened(0.1), true)
	for i in range(3):
		draw_circle(Vector2(505 + i * 135, 528), 26, Color.from_hsv(0.02 + float(i) * 0.1, 0.5, 1.0))


func _draw_farmer(mid: Color, accent: Color) -> void:
	draw_circle(Vector2(200, 150), 66, Color("#ffe294"))
	draw_polygon(PackedVector2Array([Vector2(0, 380), Vector2(260, 250), Vector2(520, 390)]), PackedColorArray([Color("#70a865")]))
	draw_polygon(PackedVector2Array([Vector2(440, 390), Vector2(850, 220), Vector2(1280, 390)]), PackedColorArray([Color("#5c985d")]))
	draw_rect(Rect2(835, 270, 260, 260), Color("#b34f58"), true)
	draw_polygon(PackedVector2Array([Vector2(800, 285), Vector2(965, 170), Vector2(1130, 285)]), PackedColorArray([Color("#5b3151")]))
	draw_rect(Rect2(925, 390, 80, 140), Color("#f0ca82"), true)
	# picket fence along the meadow edge
	for i in range(10):
		draw_rect(Rect2(90 + i * 72, 428, 14, 44), mid.lightened(0.34), true)
	draw_line(Vector2(84, 444), Vector2(760, 444), mid.lightened(0.2), 8)
	for row in range(4):
		draw_line(Vector2(95, 470 + row * 48), Vector2(760, 470 + row * 48), accent.darkened(0.25), 12)


func _draw_boxer(mid: Color, accent: Color) -> void:
	# festive pennant line above the ring
	for i in range(9):
		var px := 190.0 + float(i) * 112.0
		draw_colored_polygon(PackedVector2Array([
			Vector2(px, 150), Vector2(px + 44, 150), Vector2(px + 22, 196),
		]), mid.lightened(0.18) if i % 2 == 0 else accent)
	draw_line(Vector2(180, 150), Vector2(1100, 150), Color("#efe3c8"), 5)
	draw_polygon(
		PackedVector2Array([Vector2(190, 520), Vector2(1090, 520), Vector2(940, 245), Vector2(340, 245)]),
		PackedColorArray([Color("#e3b7b0")])
	)
	for y in [305.0, 370.0, 435.0]:
		draw_line(Vector2(245, y), Vector2(1035, y), Color("#ef5964"), 13)
	for x in [240.0, 1040.0]:
		draw_rect(Rect2(x - 18, 235, 36, 330), Color("#33264d"), true)
		draw_circle(Vector2(x, 235), 30, accent)
	draw_circle(Vector2(640, 540), 62, Color("#28355b"))
	draw_circle(Vector2(640, 540), 47, accent)


func _draw_magician(mid: Color, accent: Color) -> void:
	for x in [80.0, 1020.0]:
		draw_rect(Rect2(x, 125, 180, 450), mid.darkened(0.38), true)
		for y in range(170, 560, 72):
			draw_circle(Vector2(x + 90, y), 17, accent)
	var pulse := 90.0 + (sin(elapsed * 2.4) + 1.0) * 18.0
	draw_arc(Vector2(640, 335), pulse, 0, TAU, 48, accent, 15)
	draw_arc(Vector2(640, 335), pulse - 32, 0, TAU, 48, Color("#8ce7df"), 9)
	for x in [360.0, 820.0]:
		draw_polygon(PackedVector2Array([Vector2(x, 500), Vector2(x + 160, 500), Vector2(x + 80, 420)]), PackedColorArray([Color("#2a183f")]))


func _draw_painter(mid: Color, accent: Color) -> void:
	draw_circle(Vector2(640, 220), 145, Color("#ffde81"))
	# rolling paint cart stacked with pots
	draw_rect(Rect2(70, 470, 150, 90), mid.darkened(0.2), true)
	for i in range(3):
		draw_circle(Vector2(102 + i * 44, 462), 18, Color.from_hsv(0.86 - float(i) * 0.28, 0.5, 0.95))
	draw_circle(Vector2(100, 572), 16, Color("#51334e"))
	draw_circle(Vector2(190, 572), 16, Color("#51334e"))
	for x in [220.0, 510.0, 800.0]:
		draw_rect(Rect2(x, 250, 250, 220), Color("#fff3d9"), true)
		draw_rect(Rect2(x + 15, 265, 220, 190), Color.from_hsv(0.02 + x / 1800.0, 0.42, 1.0), true)
		draw_line(Vector2(x + 125, 470), Vector2(x + 65, 570), Color("#51334e"), 12)
		draw_line(Vector2(x + 125, 470), Vector2(x + 185, 570), Color("#51334e"), 12)
	for i in range(12):
		draw_circle(Vector2(90 + i * 102, 590), 18 + float(i % 3) * 5, Color.from_hsv(float(i) / 12.0, 0.65, 1.0))


func _draw_astronaut(mid: Color, accent: Color) -> void:
	for x in [70.0, 980.0]:
		draw_rect(Rect2(x, 210, 230, 330), mid.darkened(0.42), true)
		for row in range(4):
			for col in range(3):
				draw_circle(Vector2(x + 55 + col * 62, 270 + row * 64), 14, accent if (row + col) % 2 == 0 else Color("#ef7d8f"))
	draw_line(Vector2(290, 500), Vector2(990, 500), accent, 18)
	draw_line(Vector2(420, 500), Vector2(420, 300), accent, 18)
	draw_line(Vector2(860, 500), Vector2(860, 300), accent, 18)
	draw_polygon(PackedVector2Array([Vector2(590, 420), Vector2(690, 420), Vector2(640, 180)]), PackedColorArray([Color("#eef6f2")]))
	draw_circle(Vector2(640, 285), 35, Color("#72d9e8"))


func _draw_racer(mid: Color, accent: Color) -> void:
	# grandstand band behind the circuit
	draw_rect(Rect2(250, 195, 780, 74), mid.lightened(0.1), true)
	for i in range(12):
		draw_circle(Vector2(290 + i * 64, 232), 14, Color.from_hsv(float(i) / 12.0, 0.4, 0.98))
	draw_polygon(
		PackedVector2Array([Vector2(0, 540), Vector2(320, 315), Vector2(960, 315), Vector2(1280, 540), Vector2(1280, 650), Vector2(930, 410), Vector2(350, 410), Vector2(0, 650)]),
		PackedColorArray([Color("#303655")])
	)
	for i in range(10):
		var x := 90.0 + i * 125.0
		draw_rect(Rect2(x, 505 - absf(5.0 - i) * 15.0, 62, 14), accent if i % 2 == 0 else Color.WHITE, true)
	for x in [110.0, 1050.0]:
		for row in range(4):
			for col in range(3):
				draw_rect(Rect2(x + col * 32, 230 + row * 32, 28, 28), Color.WHITE if (row + col) % 2 == 0 else Color("#24233f"), true)


func _draw_nursery(mid: Color, accent: Color) -> void:
	# A moonlit infant-care room, not a clinic: rounded cradles, bottle
	# warmers, pillows and a gently moving mobile keep it visually separate
	# from the Stuffie Surgeon X-ray/cast set.
	draw_circle(Vector2(640, 205), 116, Color("#fff0b8"))
	draw_circle(Vector2(687, 168), 112, Color("#202452"))
	for x in [90.0, 1010.0]:
		draw_rect(Rect2(x, 245, 180, 252), mid.darkened(0.34), true)
		for row in range(3):
			draw_line(Vector2(x + 18, 308 + row * 62), Vector2(x + 162, 308 + row * 62), Color("#f7e5d5"), 7.0)
			for col in range(3):
				var bottle_x: float = float(x) + 43.0 + float(col) * 47.0
				draw_rect(Rect2(bottle_x, 269 + row * 62, 22, 34), Color("#eaf8f1"), true)
				draw_circle(Vector2(bottle_x + 11, 267 + row * 62), 7, accent)
	for index in range(5):
		var crib_x := 255.0 + float(index) * 193.0
		var crib_y := 490.0 + sin(elapsed * 1.2 + float(index) * 0.7) * 3.0
		draw_rect(Rect2(crib_x - 74, crib_y - 48, 148, 78), Color("#f4d4c2"), true)
		draw_arc(Vector2(crib_x, crib_y - 45), 75, PI, TAU, 28, Color("#fff0df"), 10.0)
		for rail in range(4):
			var rail_x := crib_x - 50.0 + float(rail) * 34.0
			draw_line(Vector2(rail_x, crib_y - 38), Vector2(rail_x, crib_y + 20), Color("#774f72"), 5.0)
		draw_arc(Vector2(crib_x - 40, crib_y + 31), 24, 0, PI, 16, accent.darkened(0.18), 6.0)
		draw_arc(Vector2(crib_x + 40, crib_y + 31), 24, 0, PI, 16, accent.darkened(0.18), 6.0)
	var mobile_center := Vector2(640, 270)
	for index in range(5):
		var angle := elapsed * 0.22 + float(index) * TAU / 5.0
		var star := mobile_center + Vector2(cos(angle) * 155.0, sin(angle) * 34.0)
		draw_line(mobile_center, star, Color(0.80, 0.72, 0.92, 0.60), 3.0)
		draw_circle(star, 12.0, accent if index % 2 == 0 else Color("#9be2d7"))


func _draw_popstar(mid: Color, accent: Color) -> void:
	draw_rect(Rect2(170, 335, 940, 235), mid.darkened(0.38), true)
	for x in [115.0, 1015.0]:
		draw_rect(Rect2(x, 280, 150, 250), Color("#211935"), true)
		for row in range(3):
			draw_circle(Vector2(x + 75, 335 + row * 70), 30, accent.darkened(float(row) * 0.12))
	for i in range(7):
		var x := 300.0 + i * 112.0
		var h := 55.0 + (sin(elapsed * 3.0 + float(i)) + 1.0) * 38.0
		draw_rect(Rect2(x, 520 - h, 42, h), Color.from_hsv(float(i) / 7.0, 0.55, 1.0), true)
	draw_circle(Vector2(640, 250), 72, Color(accent, 0.42))


func _draw_geologist(mid: Color, accent: Color) -> void:
	# A readable crystal-cave laboratory: layered walls, a fossil table,
	# specimen trays and one glowing destination cluster. All geometry stays
	# broad and sparse enough for the Mobile renderer and a four-year-old.
	for band in range(5):
		var y := 150.0 + float(band) * 74.0
		var color := mid.lightened(0.18 - float(band) * 0.055)
		draw_polyline(PackedVector2Array([
			Vector2(0, y + 24), Vector2(220, y - 12),
			Vector2(470, y + 18), Vector2(760, y - 18),
			Vector2(1040, y + 12), Vector2(1280, y - 10),
		]), color, 34.0)
	if bool(get_meta("geology_work_open", false)):
		return
	# Fossil inspection slab.
	draw_rect(Rect2(250, 430, 250, 94), Color("#d8bb8b"), true)
	draw_arc(Vector2(376, 476), 32, -0.3, TAU * 1.65, 38,
		Color("#875f72"), 11.0)
	# Three big specimen trays match the specialist sorting surface.
	for index in range(3):
		var tray_x := 550.0 + float(index) * 145.0
		draw_rect(Rect2(tray_x, 452, 110, 74), Color("#2f274e"), true)
		draw_rect(Rect2(tray_x, 452, 110, 74), accent.lightened(float(index) * 0.08), false, 7.0)
	# Finale crystal cluster.
	var base := Vector2(1080, 520)
	for crystal in range(5):
		var x := base.x + (float(crystal) - 2.0) * 34.0
		var height := 80.0 + float((crystal * 31) % 55)
		var crystal_color := Color.from_hsv(0.46 + float(crystal) * 0.055, 0.42, 1.0)
		draw_colored_polygon(PackedVector2Array([
			Vector2(x - 20, base.y), Vector2(x - 14, base.y - height * 0.72),
			Vector2(x, base.y - height), Vector2(x + 15, base.y - height * 0.70),
			Vector2(x + 20, base.y),
		]), crystal_color)
	var pulse := 58.0 + (sin(elapsed * 2.1) + 1.0) * 10.0
	draw_arc(Vector2(1080, 420), pulse, 0.0, TAU, 36, Color(accent, 0.55), 8.0)
