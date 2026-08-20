class_name MelodyGame
extends RefCounted
## Daddy Mermaid's seven-note rainbow theater on one opaque Canvas surface.
## Shared progress and ranking state remain on ReefMain; this controller owns
## only the activity's presentation, deliberate input, and synchronous cleanup.

const NOTE_COUNT := 7
const CANVAS_LAYER := 7
const NOTE_CYCLE_SECONDS := 4.2
const NOTE_VISIBLE_SIZE := 84.0
const NOTE_HIT_SIZE := 120.0
const POINTER_SIZE := 64.0

const NAVY := Color(0.075, 0.065, 0.16)
const INK := Color(0.12, 0.10, 0.24)
const INK_SOFT := Color(0.20, 0.16, 0.38)
const AQUA := Color(0.25, 0.78, 0.82)
const MINT := Color(0.39, 0.91, 0.63)
const LAVENDER := Color(0.68, 0.52, 0.88)
const PINK := Color(0.96, 0.43, 0.70)
const GOLD := Color(1.0, 0.78, 0.30)
const PAPER := Color(1.0, 0.97, 0.89)
const NOTE_COLORS := [
	Color(1.0, 0.24, 0.28),
	Color(1.0, 0.54, 0.18),
	Color(1.0, 0.86, 0.24),
	Color(0.30, 0.84, 0.42),
	Color(0.24, 0.68, 0.96),
	Color(0.39, 0.38, 0.88),
	Color(0.72, 0.40, 0.90),
]

const TILE_PATHS: Array[String] = [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c3.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c3.png",
]
const TILE_SOURCE_RECTS: Array[Rect2i] = [
	Rect2i(0, 0, 1024, 1024),
	Rect2i(1024, 0, 1024, 1024),
	Rect2i(0, 1024, 1024, 1024),
	Rect2i(1024, 1024, 1024, 1024),
]
const DADDY_PATH := "res://assets/characters/stickers/daddy.png"
const ROSHAN_PATH := "res://assets/opera/worlds/actors/roshan_popstar.png"
const OBJECTIVE := "Tap each rainbow note in the green!"
const OBJECTIVE_VOICE := "op_popstar_rhythm"


class ProsceniumCanvas extends Control:
	const NAVY := MelodyGame.NAVY
	const INK := MelodyGame.INK
	const INK_SOFT := MelodyGame.INK_SOFT
	const LAVENDER := MelodyGame.LAVENDER
	const PINK := MelodyGame.PINK
	const PAPER := MelodyGame.PAPER
	const GOLD := MelodyGame.GOLD
	const NOTE_COUNT := MelodyGame.NOTE_COUNT
	const NOTE_COLORS := MelodyGame.NOTE_COLORS

	var left_curtain: Polygon2D = null
	var right_curtain: Polygon2D = null
	var crown_header: Polygon2D = null
	var stage_apron: Polygon2D = null
	var coverage_ratio := 0.0


	func setup() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 10
		left_curtain = _polygon("LeftCurtainGeometry", PINK.darkened(0.17))
		right_curtain = _polygon("RightCurtainGeometry", LAVENDER.darkened(0.20))
		crown_header = _polygon("CrownHeaderGeometry", INK)
		stage_apron = _polygon("StageApronGeometry", INK_SOFT)


	func layout(rect: Rect2, viewport_size: Vector2) -> void:
		position = rect.position
		size = rect.size
		var side_width: float = clampf(size.x * 0.15, 176.0, 230.0)
		var header_height: float = clampf(size.y * 0.17, 104.0, 120.0)
		var apron_height: float = clampf(size.y * 0.145, 92.0, 106.0)
		var lower_y: float = size.y - apron_height
		left_curtain.polygon = PackedVector2Array([
			Vector2(0.0, header_height * 0.62),
			Vector2(side_width * 0.72, header_height * 0.78),
			Vector2(side_width, lower_y * 0.48),
			Vector2(side_width * 0.82, lower_y),
			Vector2(0.0, size.y),
		])
		right_curtain.polygon = PackedVector2Array([
			Vector2(size.x, header_height * 0.62),
			Vector2(size.x - side_width * 0.72, header_height * 0.78),
			Vector2(size.x - side_width, lower_y * 0.48),
			Vector2(size.x - side_width * 0.82, lower_y),
			Vector2(size.x, size.y),
		])
		crown_header.polygon = PackedVector2Array([
			Vector2.ZERO,
			Vector2(size.x, 0.0),
			Vector2(size.x, header_height * 0.78),
			Vector2(size.x * 0.80, header_height),
			Vector2(size.x * 0.68, header_height * 0.63),
			Vector2(size.x * 0.50, header_height),
			Vector2(size.x * 0.32, header_height * 0.63),
			Vector2(size.x * 0.20, header_height),
			Vector2(0.0, header_height * 0.78),
		])
		stage_apron.polygon = PackedVector2Array([
			Vector2(0.0, lower_y),
			Vector2(size.x, lower_y),
			Vector2(size.x, size.y),
			Vector2.ZERO + Vector2(0.0, size.y),
		])
		var covered_area: float = size.x * (header_height + apron_height) \
			+ side_width * 2.0 * (size.y - header_height - apron_height)
		coverage_ratio = covered_area / maxf(viewport_size.x * viewport_size.y, 1.0)
		queue_redraw()


	func _draw() -> void:
		if size.x <= 0.0 or size.y <= 0.0:
			return
		var side_width: float = clampf(size.x * 0.15, 176.0, 230.0)
		var header_height: float = clampf(size.y * 0.17, 104.0, 120.0)
		var apron_height: float = clampf(size.y * 0.145, 92.0, 106.0)
		# Navy and pearl outlines keep the authored meadow visibly inside a
		# theatrical object rather than reading as the activity itself.
		draw_line(Vector2(side_width, header_height * 0.88),
			Vector2(side_width * 0.82, size.y - apron_height), NAVY, 18.0, true)
		draw_line(Vector2(size.x - side_width, header_height * 0.88),
			Vector2(size.x - side_width * 0.82, size.y - apron_height), NAVY, 18.0, true)
		for fold_index in range(4):
			var fold_offset: float = 28.0 + float(fold_index) * 31.0
			draw_line(Vector2(fold_offset, header_height),
				Vector2(fold_offset * 0.78, size.y - apron_height),
				Color(1.0, 0.72, 0.88, 0.38), 9.0, true)
			draw_line(Vector2(size.x - fold_offset, header_height),
				Vector2(size.x - fold_offset * 0.78, size.y - apron_height),
				Color(0.84, 0.75, 1.0, 0.38), 9.0, true)
		# A seven-band crown rainbow is the visual identity of Daddy's theater.
		var crown_center := Vector2(size.x * 0.5, header_height * 0.96)
		for color_index in range(NOTE_COUNT):
			var radius: float = 150.0 - float(color_index) * 10.0
			draw_arc(crown_center, radius, PI + 0.20, TAU - 0.20, 40,
				NOTE_COLORS[color_index], 8.0, true)
		# Foot-level rainbow rails turn the lower frame into a runway.
		for color_index in range(NOTE_COUNT):
			var rail_y: float = size.y - apron_height + 14.0 + float(color_index) * 9.0
			draw_line(Vector2(side_width * 0.72, rail_y),
				Vector2(size.x - side_width * 0.72, rail_y),
				NOTE_COLORS[color_index], 6.0, true)
		# Warm bulbs make the proscenium instantly legible even at arm's length.
		var bulb_count: int = maxi(12, int(size.x / 66.0))
		for bulb_index in range(bulb_count):
			var bulb_x: float = 24.0 + float(bulb_index) \
				* (size.x - 48.0) / float(maxi(bulb_count - 1, 1))
			draw_circle(Vector2(bulb_x, 22.0), 7.5, PAPER, true, -1.0, true)
			draw_circle(Vector2(bulb_x, size.y - 19.0), 7.0,
				GOLD.lightened(0.28), true, -1.0, true)


	func _polygon(node_name: String, color: Color) -> Polygon2D:
		var polygon := Polygon2D.new()
		polygon.name = node_name
		polygon.color = color
		polygon.z_index = -1
		add_child(polygon)
		return polygon


class FootlightsCanvas extends Control:
	const NAVY := MelodyGame.NAVY
	const NOTE_COUNT := MelodyGame.NOTE_COUNT
	const NOTE_COLORS := MelodyGame.NOTE_COLORS
	var rail_geometry: Line2D = null

	func setup() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 16
		rail_geometry = Line2D.new()
		rail_geometry.name = "FootlightRailGeometry"
		rail_geometry.default_color = NAVY
		rail_geometry.width = 36.0
		rail_geometry.antialiased = true
		rail_geometry.z_index = -1
		add_child(rail_geometry)


	func layout(rect: Rect2) -> void:
		position = rect.position
		size = rect.size
		rail_geometry.points = PackedVector2Array([
			Vector2(18.0, size.y * 0.5),
			Vector2(maxf(18.0, size.x - 18.0), size.y * 0.5),
		])
		queue_redraw()


	func _draw() -> void:
		if size.x <= 0.0:
			return
		var count := 13
		for index in range(count):
			var center := Vector2((float(index) + 0.5) * size.x / float(count),
				size.y * 0.5)
			var color: Color = NOTE_COLORS[index % NOTE_COUNT]
			draw_circle(center, 15.0, NAVY, true, -1.0, true)
			draw_circle(center, 10.5, color.lightened(0.24), true, -1.0, true)
			draw_circle(center - Vector2(3.0, 3.0), 3.0, Color.WHITE,
				true, -1.0, true)


class StageStarCanvas extends Control:
	const NAVY := MelodyGame.NAVY
	const GOLD := MelodyGame.GOLD
	var star_geometry: Polygon2D = null

	func setup() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 18
		star_geometry = Polygon2D.new()
		star_geometry.name = "StageStarGeometry"
		star_geometry.color = GOLD
		star_geometry.z_index = -1
		add_child(star_geometry)


	func layout(center: Vector2, diameter: float) -> void:
		size = Vector2.ONE * diameter
		position = center - size * 0.5
		star_geometry.polygon = _star_points(size * 0.5,
			minf(size.x, size.y) * 0.39, minf(size.x, size.y) * 0.18)
		queue_redraw()


	func _draw() -> void:
		var center := size * 0.5
		var outer: PackedVector2Array = _star_points(center,
			minf(size.x, size.y) * 0.48, minf(size.x, size.y) * 0.22)
		draw_colored_polygon(outer, NAVY)
		var inner: PackedVector2Array = _star_points(center,
			minf(size.x, size.y) * 0.39, minf(size.x, size.y) * 0.18)
		draw_colored_polygon(inner, GOLD)
		draw_circle(center - size * 0.08, size.x * 0.055, Color.WHITE,
			true, -1.0, true)


	func _star_points(center: Vector2, outer_radius: float,
			inner_radius: float) -> PackedVector2Array:
		var points := PackedVector2Array()
		for index in range(10):
			var radius: float = outer_radius if index % 2 == 0 else inner_radius
			var angle: float = -PI * 0.5 + float(index) * PI / 5.0
			points.append(center + Vector2(cos(angle), sin(angle)) * radius)
		return points


class TimingZoneCanvas extends Control:
	const NAVY := MelodyGame.NAVY
	const MINT := MelodyGame.MINT
	const PAPER := MelodyGame.PAPER

	var pulse := 0.0
	var green_geometry: Polygon2D = null


	func setup() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 28
		green_geometry = Polygon2D.new()
		green_geometry.name = "GreenWindowGeometry"
		green_geometry.color = Color(0.16, 0.78, 0.38, 0.92)
		green_geometry.z_index = -1
		add_child(green_geometry)


	func layout(rect: Rect2) -> void:
		position = rect.position
		size = rect.size
		var bevel: float = minf(size.x, size.y) * 0.20
		green_geometry.polygon = PackedVector2Array([
			Vector2(bevel, 0.0), Vector2(size.x - bevel, 0.0),
			Vector2(size.x, bevel), Vector2(size.x, size.y - bevel),
			Vector2(size.x - bevel, size.y), Vector2(bevel, size.y),
			Vector2(0.0, size.y - bevel), Vector2(0.0, bevel),
		])
		queue_redraw()


	func advance(elapsed: float) -> void:
		pulse = elapsed
		queue_redraw()


	func _draw() -> void:
		var center := size * 0.5
		var radius: float = minf(size.x, size.y) * 0.43
		var breathe: float = 3.0 + sin(pulse * 5.0) * 3.0
		draw_circle(center, radius + 18.0 + breathe,
			Color(MINT.r, MINT.g, MINT.b, 0.24), true, -1.0, true)
		draw_circle(center, radius + 9.0, NAVY, true, -1.0, true)
		draw_circle(center, radius, Color(0.16, 0.78, 0.38, 0.92),
			true, -1.0, true)
		draw_arc(center, radius - 10.0, 0.0, TAU, 48, PAPER, 7.0, true)
		# A simple play triangle is readable without words and distinguishes the
		# green timing window from scenery.
		var triangle := PackedVector2Array([
			center + Vector2(-18.0, -26.0),
			center + Vector2(31.0, 0.0),
			center + Vector2(-18.0, 26.0),
		])
		draw_colored_polygon(triangle, Color.WHITE)


class PointerCanvas extends Control:
	const GOLD := MelodyGame.GOLD
	const PAPER := MelodyGame.PAPER
	const POINTER_SIZE := MelodyGame.POINTER_SIZE

	var target := Vector2.ZERO
	var zone_center := Vector2.ZERO
	var pulse := 0.0
	var target_id := -1
	var target_geometry: Polygon2D = null
	var arrow_geometry: Polygon2D = null
	var line_geometry: Line2D = null
	var inner_ring_geometry: Line2D = null
	var outer_ring_geometry: Line2D = null


	func setup() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 32
		target_geometry = Polygon2D.new()
		target_geometry.name = "PointerTargetGeometry"
		target_geometry.color = Color(GOLD.r, GOLD.g, GOLD.b, 0.18)
		target_geometry.z_index = -1
		add_child(target_geometry)
		arrow_geometry = Polygon2D.new()
		arrow_geometry.name = "PointerArrowGeometry"
		arrow_geometry.color = GOLD
		add_child(arrow_geometry)
		line_geometry = Line2D.new()
		line_geometry.name = "PointerLineGeometry"
		line_geometry.default_color = Color(1.0, 0.94, 0.54, 0.94)
		line_geometry.width = 9.0
		line_geometry.antialiased = true
		add_child(line_geometry)
		inner_ring_geometry = Line2D.new()
		inner_ring_geometry.name = "PointerInnerRingGeometry"
		inner_ring_geometry.default_color = PAPER
		inner_ring_geometry.width = 8.0
		inner_ring_geometry.antialiased = true
		add_child(inner_ring_geometry)
		outer_ring_geometry = Line2D.new()
		outer_ring_geometry.name = "PointerOuterRingGeometry"
		outer_ring_geometry.default_color = Color(GOLD.r, GOLD.g, GOLD.b, 0.82)
		outer_ring_geometry.width = 5.0
		outer_ring_geometry.antialiased = true
		add_child(outer_ring_geometry)


	func layout(viewport_size: Vector2) -> void:
		position = Vector2.ZERO
		size = viewport_size


	func point_at(next_target: Vector2, next_zone_center: Vector2,
			next_target_id: int, elapsed: float) -> void:
		target = next_target
		zone_center = next_zone_center
		target_id = next_target_id
		pulse = elapsed
		target_geometry.visible = target_id >= 0
		arrow_geometry.visible = target_id >= 0
		line_geometry.visible = target_id >= 0
		inner_ring_geometry.visible = target_id >= 0
		outer_ring_geometry.visible = target_id >= 0
		if target_geometry.visible:
			var radius: float = POINTER_SIZE * 0.5
			target_geometry.polygon = PackedVector2Array([
				target + Vector2(0.0, -radius),
				target + Vector2(radius, 0.0),
				target + Vector2(0.0, radius),
				target + Vector2(-radius, 0.0),
			])
			var direction: Vector2 = target - zone_center
			if direction.length_squared() <= 0.001:
				direction = Vector2.RIGHT
			else:
				direction = direction.normalized()
			var normal := Vector2(-direction.y, direction.x)
			arrow_geometry.polygon = PackedVector2Array([
				target,
				target - direction * 46.0 + normal * 17.0,
				target - direction * 46.0 - normal * 17.0,
			])
			var line_start: Vector2 = zone_center + direction * 82.0
			var line_end: Vector2 = target - direction * 38.0
			if line_start.distance_to(line_end) > 14.0:
				line_geometry.points = PackedVector2Array([line_start, line_end])
			else:
				line_geometry.points = PackedVector2Array()
			var ring_radius: float = 34.0 + sin(pulse * 6.0) * 5.0
			inner_ring_geometry.points = _ring_points(target, ring_radius)
			outer_ring_geometry.points = _ring_points(target, ring_radius + 8.0)


	func _ring_points(center: Vector2, radius: float) -> PackedVector2Array:
		var points := PackedVector2Array()
		for index in range(33):
			var angle: float = TAU * float(index) / 32.0
			points.append(center + Vector2(cos(angle), sin(angle)) * radius)
		return points


class RainbowNoteCanvas extends Control:
	const NAVY := MelodyGame.NAVY
	const PAPER := MelodyGame.PAPER
	const NOTE_VISIBLE_SIZE := MelodyGame.NOTE_VISIBLE_SIZE

	var note_color := Color.WHITE
	var note_id := -1
	var color_geometry: Polygon2D = null


	func setup(next_id: int, color: Color) -> void:
		note_id = next_id
		note_color = color
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 35
		size = Vector2.ONE * NOTE_VISIBLE_SIZE
		color_geometry = Polygon2D.new()
		color_geometry.name = "NoteColorGeometry"
		color_geometry.color = note_color
		color_geometry.z_index = -1
		var points := PackedVector2Array()
		for point_index in range(24):
			var angle: float = float(point_index) * TAU / 24.0
			points.append(size * 0.5 + Vector2(cos(angle), sin(angle)) * 41.0)
		color_geometry.polygon = points
		add_child(color_geometry)
		queue_redraw()


	func place(center: Vector2, pulse: float) -> void:
		position = center - size * 0.5
		rotation = sin(pulse * 3.1 + float(note_id)) * 0.035
		pivot_offset = size * 0.5
		queue_redraw()


	func _draw() -> void:
		var center := size * 0.5
		draw_circle(center, 41.0, Color(NAVY.r, NAVY.g, NAVY.b, 0.94),
			true, -1.0, true)
		draw_circle(center, 35.0, note_color, true, -1.0, true)
		draw_circle(center - Vector2(8.0, 9.0), 7.0,
			Color(1.0, 1.0, 1.0, 0.78), true, -1.0, true)
		# One large eighth note, built from broad shapes for preschool legibility.
		draw_circle(Vector2(35.0, 55.0), 11.5, PAPER, true, -1.0, true)
		draw_line(Vector2(44.0, 54.0), Vector2(44.0, 22.0), PAPER, 9.0, true)
		var flag := PackedVector2Array([
			Vector2(44.0, 19.0), Vector2(66.0, 25.0),
			Vector2(59.0, 38.0), Vector2(44.0, 32.0),
		])
		draw_colored_polygon(flag, PAPER)


class ProgressPipCanvas extends Control:
	const NAVY := MelodyGame.NAVY
	const PAPER := MelodyGame.PAPER

	var pip_color := Color.WHITE
	var filled := false
	var current := false
	var pip_geometry: Polygon2D = null


	func setup(color: Color) -> void:
		pip_color = color
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		z_index = 40
		size = Vector2.ONE * 48.0
		pip_geometry = Polygon2D.new()
		pip_geometry.name = "ProgressPipGeometry"
		pip_geometry.z_index = -1
		var points := PackedVector2Array()
		for point_index in range(20):
			var angle: float = float(point_index) * TAU / 20.0
			points.append(size * 0.5 + Vector2(cos(angle), sin(angle)) * 19.0)
		pip_geometry.polygon = points
		add_child(pip_geometry)


	func set_state(next_filled: bool, next_current: bool) -> void:
		filled = next_filled
		current = next_current
		pip_geometry.color = pip_color if filled or current \
			else Color(pip_color.r, pip_color.g, pip_color.b, 0.32)
		queue_redraw()


	func _draw() -> void:
		var center := size * 0.5
		if current:
			draw_circle(center, 23.0, Color(1.0, 1.0, 1.0, 0.92),
				true, -1.0, true)
		draw_circle(center, 19.0, NAVY, true, -1.0, true)
		draw_circle(center, 14.5,
			pip_color if filled else Color(pip_color.r, pip_color.g, pip_color.b, 0.32),
			true, -1.0, true)
		if filled:
			draw_line(center + Vector2(-7.0, 0.0), center + Vector2(-1.0, 7.0),
				PAPER, 4.5, true)
			draw_line(center + Vector2(-1.0, 7.0), center + Vector2(9.0, -8.0),
				PAPER, 4.5, true)


var m: ReefMain
var _layer: CanvasLayer = null
var _surface: Node2D = null
var _screen_fill: ColorRect = null
var _scenic_backcloth: ColorRect = null
var _backdrop_tiles: Array[Sprite2D] = []
var _proscenium: ProsceniumCanvas = null
var _footlights: FootlightsCanvas = null
var _stage_star: StageStarCanvas = null
var _daddy: Sprite2D = null
var _roshan: Sprite2D = null
var _timing_zone: TimingZoneCanvas = null
var _pointer: PointerCanvas = null
var _notes: Array[RainbowNoteCanvas] = []
var _progress_pips: Array[ProgressPipCanvas] = []
var _fr: Dictionary = {}

var _viewport_size := Vector2.ZERO
var _proscenium_rect := Rect2()
var _daddy_rect := Rect2()
var _roshan_rect := Rect2()
var _zone_rect := Rect2()
var _track_start := Vector2.ZERO
var _track_end := Vector2.ZERO
var _note_point := Vector2.ZERO
var _note_cycle_t := 0.0
var _active_note := -1
var _progress := 0
var _elapsed := 0.0
var _tick_count := 0
var _completed := false

var _input_down := false
var _input_kind := ""
var _input_source: StringName = &""
var _blocked_sources: Dictionary = {}
var _press_position := Vector2.ZERO
var _current_position := Vector2.ZERO
var _touch_armed := false
var _blocked_until_release := true
var _startup_release_guard := true
var _cancelled_had_input := false
var _pause_waiting_release := false
var _input_context_loss_reasons: Dictionary = {}
var _input_context_restore_guard := false

var _chime_snapshot_valid := false
var _chime_volume_db := 0.0
var _chime_pitch_scale := 1.0


func _init(main: ReefMain) -> void:
	m = main


static func runtime_art_paths() -> Array[String]:
	var paths: Array[String] = []
	for tile_path: String in TILE_PATHS:
		paths.append(tile_path)
	paths.append(DADDY_PATH)
	paths.append(ROSHAN_PATH)
	return paths


func build(fr: Dictionary, _origin: Variant) -> void:
	stage_close()
	_fr = fr
	m.g["timer"] = -1.0
	m.g["caught"] = 0
	_progress = 0
	_active_note = 0
	_note_cycle_t = 0.0
	_elapsed = 0.0
	_tick_count = 0
	_completed = false
	_reset_press_state()
	_blocked_until_release = true
	_blocked_sources.clear()
	_startup_release_guard = true
	_cancelled_had_input = false
	_pause_waiting_release = false
	_input_context_loss_reasons.clear()
	_input_context_restore_guard = false
	_capture_chime_state()

	_layer = CanvasLayer.new()
	_layer.name = "MelodyCanvasLayer"
	_layer.layer = CANVAS_LAYER
	m.add_child(_layer)

	_surface = Node2D.new()
	_surface.name = "RainbowTheaterCanvas"
	_layer.add_child(_surface)

	_screen_fill = ColorRect.new()
	_screen_fill.name = "OpaqueTheaterFill"
	_screen_fill.color = NAVY
	_screen_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_screen_fill.z_index = -100
	_surface.add_child(_screen_fill)

	_scenic_backcloth = ColorRect.new()
	_scenic_backcloth.name = "ScenicBackcloth"
	_scenic_backcloth.color = Color(0.18, 0.36, 0.46)
	_scenic_backcloth.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_scenic_backcloth.clip_contents = true
	_scenic_backcloth.z_index = -90
	_surface.add_child(_scenic_backcloth)
	_build_backdrop_tiles()

	_proscenium = ProsceniumCanvas.new()
	_proscenium.name = "OperaProscenium"
	_surface.add_child(_proscenium)
	_proscenium.setup()

	_footlights = FootlightsCanvas.new()
	_footlights.name = "StageFootlights"
	_surface.add_child(_footlights)
	_footlights.setup()

	_stage_star = StageStarCanvas.new()
	_stage_star.name = "StageStar"
	_surface.add_child(_stage_star)
	_stage_star.setup()

	_daddy = _actor_sprite("DaddyGuide", DADDY_PATH, 24)
	_roshan = _actor_sprite("PopstarRoshan", ROSHAN_PATH, 25)

	_timing_zone = TimingZoneCanvas.new()
	_timing_zone.name = "TimingZone"
	_surface.add_child(_timing_zone)
	_timing_zone.setup()

	_pointer = PointerCanvas.new()
	_pointer.name = "VisualPointer"
	_surface.add_child(_pointer)
	_pointer.setup()

	for note_id in range(NOTE_COUNT):
		var note := RainbowNoteCanvas.new()
		note.name = "RainbowNote%d" % note_id
		_surface.add_child(note)
		note.setup(note_id, NOTE_COLORS[note_id])
		note.visible = note_id == _active_note
		_notes.append(note)

		var pip := ProgressPipCanvas.new()
		pip.name = "ProgressPip%d" % note_id
		_surface.add_child(pip)
		pip.setup(NOTE_COLORS[note_id])
		_progress_pips.append(pip)

	_layout_stage(true)
	_refresh_stage_state()
	# The exact recorded line carries the complete target and verb for a
	# non-reader. Its persistent green window and moving pointer repeat it.
	m.show_msg("Roshan", OBJECTIVE, OBJECTIVE_VOICE)


func _tick_melody(delta: float, _fr_value: Dictionary,
		_ppos: Variant) -> void:
	if _layer == null or not is_instance_valid(_layer) or _completed:
		return
	# Main normally suppresses the whole gameplay tick while an OS input context
	# is absent. Keep the controller independently fail-closed for direct callers.
	if input_context_lost():
		return
	_tick_count += 1
	_elapsed += maxf(delta, 0.0)
	_layout_stage(false)
	if _blocked_until_release and not _input_down \
			and _blocked_sources.is_empty() \
			and not _cancelled_had_input and not _pause_waiting_release \
			and _opening_fade_clear():
		# A startup guard or cancellation with no known held source expires with
		# the reveal. A source that really was held keeps its latch until release.
		# This also makes a gated quick press+release self-healing if an older
		# router reports both halves only as neutral cancellation.
		_blocked_until_release = false
		_startup_release_guard = false
		_input_context_restore_guard = false
	_note_cycle_t = fposmod(_note_cycle_t + maxf(delta, 0.0),
		NOTE_CYCLE_SECONDS)
	_update_note_point()
	_refresh_stage_state()
	m.hud_game.text = ""


func handle_touch_press(screen_position: Vector2,
		source_token: StringName = &"legacy_world_touch") -> bool:
	return _begin_press("touch", source_token, screen_position, true)


func handle_touch_drag(screen_position: Vector2,
		source_token: StringName = &"legacy_world_touch") -> void:
	if input_context_lost() or _input_context_restore_guard:
		return
	if not _input_down or _input_kind != "touch" or _input_source != source_token:
		return
	_current_position = screen_position
	if screen_position.distance_to(_press_position) > 48.0 \
			or not active_note_hit_rect().has_point(screen_position) \
			or not _note_is_in_green():
		_touch_armed = false


func handle_touch_release(
		source_token: StringName = &"legacy_world_touch") -> void:
	_finish_press("touch", source_token)


func handle_action_press(
		source_token: StringName = &"legacy_action") -> bool:
	return _begin_press("action", source_token, _note_point, false)


func handle_action_release(
		source_token: StringName = &"legacy_action") -> void:
	_finish_press("action", source_token)


func cancel_input(source_token: StringName = &"") -> void:
	if input_context_lost() or _input_context_restore_guard:
		# TouchUI may defensively cancel again as notifications propagate through
		# the tree. Context loss owns the stronger source-free contract.
		_arm_input_context_restore_guard()
		return
	if _input_down and not _input_source.is_empty():
		_block_source(_input_source, _input_kind)
	if not source_token.is_empty():
		_block_source(source_token, _source_kind(source_token))
	_cancelled_had_input = _cancelled_had_input \
		or not _blocked_sources.is_empty()
	_reset_press_state()
	_blocked_until_release = true
	_startup_release_guard = false


func input_context_lost() -> bool:
	return not _input_context_loss_reasons.is_empty()


func input_context_blocks_input() -> bool:
	# Main queries this narrow seam during the restored-but-not-yet-ticked
	# boundary. That source-free guard is gameplay authority, not probe metadata.
	return input_context_lost() or _input_context_restore_guard


func _arm_input_context_restore_guard() -> void:
	_blocked_sources.clear()
	_reset_press_state()
	_blocked_until_release = true
	_startup_release_guard = true
	_cancelled_had_input = false
	_pause_waiting_release = false
	_input_context_restore_guard = true


func on_input_context_lost(reason: StringName) -> void:
	if reason.is_empty() or _input_context_loss_reasons.has(reason):
		return
	var was_lost: bool = input_context_lost()
	_input_context_loss_reasons[reason] = true
	if was_lost:
		return
	# Focus/background loss is not an ordinary Pause sheet: Android may never
	# deliver the terminal event for the finger, key, or pad which was down when
	# the app lost its input context. Forget every now-unreleasable exact owner,
	# then retain one source-free guard through every nested loss reason.
	_arm_input_context_restore_guard()


func on_input_context_restored(reason: StringName) -> void:
	if reason.is_empty() or not _input_context_loss_reasons.has(reason):
		return
	_input_context_loss_reasons.erase(reason)
	if input_context_lost():
		return
	# Clear again on the fully-lost -> active boundary. Delayed platform events
	# cannot become owners, and the first active unpaused tick alone retires this
	# source-free guard.
	_arm_input_context_restore_guard()


func handle_touch_cancel(
		source_token: StringName = &"legacy_world_touch") -> void:
	# A platform-cancelled terminal event belongs to one concrete finger/mouse.
	# Disarm only that exact owner before using the normal exact-token release
	# path. A cancelled sibling therefore cannot score, disarm, or release the
	# deliberate source that is still physically held.
	if _input_down and _input_kind == "touch" and _input_source == source_token:
		_touch_armed = false
	_finish_press("touch", source_token)


func arm_entry_sources(source_tokens: Array) -> void:
	# Main observes physical presses before the fade starts. Seed every source
	# that is still down so a different finger, key, or controller cannot clear
	# the reveal latch on its behalf.
	if input_context_lost() or _input_context_restore_guard:
		return
	for source_value: Variant in source_tokens:
		var source_token := StringName(String(source_value))
		if not source_token.is_empty():
			_block_source(source_token, _source_kind(source_token))
	if _blocked_sources.is_empty():
		return
	_blocked_until_release = true
	_startup_release_guard = false
	_cancelled_had_input = true


func forget_sources_with_prefix(source_prefix: String) -> void:
	# Device disconnects have no release event. Neutralize only that device's
	# sources; another finger/key/pad must retain its independent ownership.
	if source_prefix.is_empty() or input_context_lost() \
			or _input_context_restore_guard:
		return
	var forgot_source := false
	if _input_down and String(_input_source).begins_with(source_prefix):
		_block_source(_input_source, _input_kind)
		_reset_press_state()
		forgot_source = true
	for source_value: Variant in _blocked_sources.keys():
		var source_token := StringName(String(source_value))
		if String(source_token).begins_with(source_prefix):
			_blocked_sources.erase(source_token)
			forgot_source = true
	if not forgot_source:
		return
	if _blocked_sources.is_empty():
		_blocked_until_release = false
		_startup_release_guard = false
		_cancelled_had_input = false
		_pause_waiting_release = false
	else:
		_blocked_until_release = true
		_cancelled_had_input = true


func on_pause_changed(paused: bool) -> void:
	if input_context_lost() or _input_context_restore_guard:
		_arm_input_context_restore_guard()
		return
	if paused:
		if _input_down and not _input_source.is_empty():
			_block_source(_input_source, _input_kind)
		var held_source: bool = not _blocked_sources.is_empty() \
			or _cancelled_had_input
		_reset_press_state()
		_pause_waiting_release = held_source
		_blocked_until_release = held_source
		_startup_release_guard = false
		_cancelled_had_input = held_source
	elif not _pause_waiting_release:
		_blocked_until_release = false
		_blocked_sources.clear()
		_cancelled_had_input = false


func stage_close() -> void:
	_restore_chime_state()
	var old_layer: CanvasLayer = _layer
	if old_layer != null and is_instance_valid(old_layer):
		old_layer.visible = false
		if old_layer.get_parent() != null:
			old_layer.get_parent().remove_child(old_layer)
		old_layer.queue_free()
	_layer = null
	_surface = null
	_screen_fill = null
	_scenic_backcloth = null
	_backdrop_tiles.clear()
	_proscenium = null
	_footlights = null
	_stage_star = null
	_daddy = null
	_roshan = null
	_timing_zone = null
	_pointer = null
	_notes.clear()
	_progress_pips.clear()
	_fr = {}
	_viewport_size = Vector2.ZERO
	_proscenium_rect = Rect2()
	_daddy_rect = Rect2()
	_roshan_rect = Rect2()
	_zone_rect = Rect2()
	_track_start = Vector2.ZERO
	_track_end = Vector2.ZERO
	_note_point = Vector2.ZERO
	_active_note = -1
	_progress = 0
	_completed = false
	_reset_press_state()
	_blocked_until_release = false
	_blocked_sources.clear()
	_startup_release_guard = false
	_cancelled_had_input = false
	_pause_waiting_release = false
	_input_context_loss_reasons.clear()
	_input_context_restore_guard = false


func active_layer() -> CanvasLayer:
	return _layer if _layer != null and is_instance_valid(_layer) else null


func surface() -> Node2D:
	return _surface if _surface != null and is_instance_valid(_surface) else null


func stage_root() -> Node2D:
	return surface()


func active_note_id() -> int:
	return _active_note if active_layer() != null and not _completed else -1


func active_note_screen_point() -> Vector2:
	return _note_point if active_note_id() >= 0 else Vector2.ZERO


func active_note_hit_rect() -> Rect2:
	if active_note_id() < 0:
		return Rect2()
	return Rect2(_note_point - Vector2.ONE * NOTE_HIT_SIZE * 0.5,
		Vector2.ONE * NOTE_HIT_SIZE)


func timing_zone_screen_rect() -> Rect2:
	return _zone_rect if active_layer() != null else Rect2()


func progress_count() -> int:
	return _progress


func note_count() -> int:
	return NOTE_COUNT


func audit_snapshot() -> Dictionary:
	if active_layer() == null or surface() == null:
		return {}
	var pointer_rect := Rect2(_note_point - Vector2.ONE * POINTER_SIZE * 0.5,
		Vector2.ONE * POINTER_SIZE)
	return {
		"tile_paths": TILE_PATHS.duplicate(),
		"tile_source_rects": TILE_SOURCE_RECTS.duplicate(),
		"proscenium_rect": _proscenium_rect,
		"proscenium_coverage": _proscenium.coverage_ratio,
		"proscenium_geometry_nodes": [
			"LeftCurtainGeometry", "RightCurtainGeometry",
			"CrownHeaderGeometry", "StageApronGeometry",
		],
		"footlights_visible": _footlights != null and _footlights.visible,
		"stage_star_visible": _stage_star != null and _stage_star.visible,
		"daddy_path": DADDY_PATH,
		"roshan_path": ROSHAN_PATH,
		"daddy_rect": _daddy_rect,
		"roshan_rect": _roshan_rect,
		"active_note_visible_rect": Rect2(
			_note_point - Vector2.ONE * NOTE_VISIBLE_SIZE * 0.5,
			Vector2.ONE * NOTE_VISIBLE_SIZE),
		"active_note_hit_rect": active_note_hit_rect(),
		"timing_zone_rect": _zone_rect,
		"pointer_rect": pointer_rect,
		"pointer_target_id": active_note_id(),
		"note_colors": NOTE_COLORS.duplicate(),
		"active_note_color": NOTE_COLORS[_active_note] \
			if _active_note >= 0 and _active_note < NOTE_COUNT else Color.BLACK,
		"spatial_descendants": 0,
		"no_fail_state": true,
		"has_timer": false,
		"completed": _completed,
		"input_down": _input_down,
		"input_source": _input_source,
		"touch_armed": _touch_armed,
		"blocked_until_release": _blocked_until_release,
		"blocked_sources": _blocked_sources.duplicate(),
		"input_context_lost": input_context_lost(),
		"input_context_loss_reasons": _input_context_loss_reasons.keys(),
		"input_context_restore_guard": _input_context_restore_guard,
		"tick_count": _tick_count,
		"elapsed": _elapsed,
		"viewport_size": _viewport_size,
	}


func _build_backdrop_tiles() -> void:
	for tile_index in range(TILE_PATHS.size()):
		var tile := Sprite2D.new()
		tile.name = "SkyLagoonBackdrop_r%d_c%d" \
			% [int(tile_index / 2), 2 + tile_index % 2]
		tile.texture = load(TILE_PATHS[tile_index]) as Texture2D
		tile.centered = true
		tile.z_index = 1
		tile.set_meta("source_path", TILE_PATHS[tile_index])
		tile.set_meta("native_source_rect", TILE_SOURCE_RECTS[tile_index])
		_scenic_backcloth.add_child(tile)
		_backdrop_tiles.append(tile)


func _actor_sprite(node_name: String, path: String, z_order: int) -> Sprite2D:
	var actor := Sprite2D.new()
	actor.name = node_name
	actor.texture = load(path) as Texture2D
	actor.centered = true
	actor.z_index = z_order
	actor.set_meta("source_path", path)
	_surface.add_child(actor)
	return actor


func _layout_stage(force: bool) -> void:
	if _surface == null or not is_instance_valid(_surface):
		return
	var next_size: Vector2 = m.get_viewport().get_visible_rect().size
	next_size.x = maxf(next_size.x, 640.0)
	next_size.y = maxf(next_size.y, 360.0)
	if not force and next_size.is_equal_approx(_viewport_size):
		return
	_viewport_size = next_size
	_screen_fill.position = Vector2.ZERO
	_screen_fill.size = _viewport_size

	var margin_x: float = maxf(18.0, _viewport_size.x * 0.01875)
	var margin_y: float = maxf(12.0, _viewport_size.y * 0.025)
	_proscenium_rect = Rect2(Vector2(margin_x, margin_y),
		_viewport_size - Vector2(margin_x * 2.0, margin_y * 2.0))
	_proscenium.layout(_proscenium_rect, _viewport_size)

	var side_width: float = clampf(_proscenium_rect.size.x * 0.15, 176.0, 230.0)
	var scenic_rect := Rect2(
		Vector2(_proscenium_rect.position.x + side_width * 0.94,
			_viewport_size.y * 0.145),
		Vector2(_proscenium_rect.size.x - side_width * 1.88,
			_viewport_size.y * 0.66))
	_scenic_backcloth.position = scenic_rect.position
	_scenic_backcloth.size = scenic_rect.size
	_layout_backdrop_tiles()

	var actor_scale: float = clampf(_viewport_size.y / 720.0, 0.78, 1.15)
	var stage_floor_y: float = minf(_viewport_size.y * 0.72, 530.0)
	var daddy_size := Vector2(172.0, 235.0) * actor_scale
	_daddy_rect = Rect2(
		Vector2(_viewport_size.x - _proscenium_rect.position.x
			- 32.0 * actor_scale - daddy_size.x,
			stage_floor_y - daddy_size.y), daddy_size)
	_place_actor(_daddy, _daddy_rect)
	var roshan_size := Vector2.ONE * 180.0 * actor_scale
	_roshan_rect = Rect2(
		Vector2(_viewport_size.x * 0.29 - roshan_size.x * 0.5,
			stage_floor_y - roshan_size.y), roshan_size)
	_place_actor(_roshan, _roshan_rect)

	var zone_size: float = clampf(_viewport_size.y * 0.25, 160.0, 190.0)
	var zone_center := Vector2(_viewport_size.x * 0.705,
		_viewport_size.y * 0.515)
	_zone_rect = Rect2(zone_center - Vector2.ONE * zone_size * 0.5,
		Vector2.ONE * zone_size)
	_timing_zone.layout(_zone_rect)

	_track_start = Vector2(maxf(_roshan_rect.end.x + 54.0,
		_viewport_size.x * 0.39), zone_center.y)
	_track_end = Vector2(minf(_daddy_rect.position.x - 60.0,
		_viewport_size.x * 0.91), zone_center.y)
	if _track_end.x - _track_start.x < 420.0:
		_track_start.x = maxf(90.0, _track_end.x - 420.0)
	_footlights.layout(Rect2(
		Vector2(_proscenium_rect.position.x + side_width * 0.60,
			stage_floor_y + 6.0),
		Vector2(_proscenium_rect.size.x - side_width * 1.20,
			48.0 * actor_scale)))
	_stage_star.layout(Vector2(_viewport_size.x * 0.30,
		_proscenium_rect.position.y + 67.0 * actor_scale),
		104.0 * actor_scale)
	_pointer.layout(_viewport_size)

	var pip_gap: float = 58.0 * actor_scale
	var pip_start_x: float = _viewport_size.x * 0.5 \
		- pip_gap * float(NOTE_COUNT - 1) * 0.5
	for pip_index in range(_progress_pips.size()):
		var pip: ProgressPipCanvas = _progress_pips[pip_index]
		pip.scale = Vector2.ONE * actor_scale
		pip.position = Vector2(pip_start_x + float(pip_index) * pip_gap,
			_proscenium_rect.position.y + 10.0 * actor_scale)
	_update_note_point()


func _layout_backdrop_tiles() -> void:
	# Reconstruct the complete native square with one whole-canvas transform,
	# then let the real scenic-window clip perform the centered crop. No tile is
	# independently stretched, shifted, or repaired, so every source seam keeps
	# exactly the same scale on both phone aspects.
	var square_side: float = maxf(_scenic_backcloth.size.x,
		_scenic_backcloth.size.y)
	var tile_side := square_side * 0.5
	var square_origin := (_scenic_backcloth.size - Vector2.ONE * square_side) * 0.5
	for tile_index in range(_backdrop_tiles.size()):
		var row: int = tile_index / 2
		var column: int = tile_index % 2
		var tile: Sprite2D = _backdrop_tiles[tile_index]
		tile.scale = Vector2.ONE * (tile_side / 1024.0)
		tile.position = square_origin + Vector2(
			(float(column) + 0.5) * tile_side,
			(float(row) + 0.5) * tile_side)


func _place_actor(actor: Sprite2D, rect: Rect2) -> void:
	if actor == null or actor.texture == null:
		return
	actor.position = rect.get_center()
	actor.scale = rect.size / Vector2(actor.texture.get_size())


func _update_note_point() -> void:
	if _active_note < 0:
		_note_point = Vector2.ZERO
		return
	var travel: float = _note_cycle_t / NOTE_CYCLE_SECONDS
	_note_point = _track_start.lerp(_track_end, travel)
	_note_point.y += sin(travel * TAU * 2.0 + float(_active_note) * 0.7) * 18.0


func _refresh_stage_state() -> void:
	if _surface == null or not is_instance_valid(_surface):
		return
	for note_index in range(_notes.size()):
		var note: RainbowNoteCanvas = _notes[note_index]
		note.visible = note_index == _active_note and not _completed
		if note.visible:
			note.place(_note_point, _elapsed)
	for pip_index in range(_progress_pips.size()):
		_progress_pips[pip_index].set_state(
			pip_index < _progress, pip_index == _active_note)
	_timing_zone.advance(_elapsed)
	_pointer.point_at(_note_point, _zone_rect.get_center(),
		_active_note if not _completed else -1, _elapsed)


func _begin_press(kind: String, source_token: StringName,
		screen_position: Vector2, position_required: bool) -> bool:
	if active_note_id() < 0:
		return false
	if input_context_lost() or _input_context_restore_guard:
		return true
	if source_token.is_empty():
		return true
	if _blocked_until_release:
		_block_source(source_token, kind)
		_cancelled_had_input = not _blocked_sources.is_empty()
		return true
	if _input_down:
		return true
	_input_down = true
	_input_kind = kind
	_input_source = source_token
	_press_position = screen_position
	_current_position = screen_position
	_touch_armed = _note_is_in_green() and (
		not position_required or active_note_hit_rect().has_point(screen_position))
	return true


func _finish_press(kind: String, source_token: StringName) -> void:
	if input_context_lost() or _input_context_restore_guard:
		return
	if _blocked_until_release:
		if not _blocked_sources.is_empty():
			if not _blocked_sources.has(source_token) \
					or String(_blocked_sources[source_token]) != kind:
				return
			_blocked_sources.erase(source_token)
			if not _blocked_sources.is_empty():
				return
		elif source_token.is_empty():
			return
		_blocked_until_release = false
		_startup_release_guard = false
		_cancelled_had_input = false
		_pause_waiting_release = false
		_reset_press_state()
		return
	if not _input_down or _input_kind != kind or _input_source != source_token:
		return
	var should_score: bool = _touch_armed and _note_is_in_green()
	if kind == "touch":
		should_score = should_score \
			and active_note_hit_rect().has_point(_current_position)
	_reset_press_state()
	_cancelled_had_input = false
	_pause_waiting_release = false
	if should_score:
		_score_current_note()


func _block_source(source_token: StringName, kind: String) -> void:
	if source_token.is_empty() or kind.is_empty():
		return
	_blocked_sources[source_token] = kind


func _source_kind(source_token: StringName) -> String:
	var token := String(source_token)
	if token.begins_with("touch:") or token.begins_with("mouse:") \
			or source_token == &"legacy_world_touch":
		return "touch"
	if token.begins_with("key:") or token.begins_with("pad:") \
			or source_token == &"legacy_action":
		return "action"
	return ""


func _score_current_note() -> void:
	if _completed or _active_note < 0:
		return
	_progress += 1
	m.g["caught"] = _progress
	if m.chime != null:
		m.chime.volume_db = -4.0
		m.chime.pitch_scale = 0.86 + float(_progress) * 0.09
		m.chime.play()
	if _progress >= NOTE_COUNT:
		_completed = true
		_active_note = -1
		_refresh_stage_state()
		m._end_game(true, _fr,
			"You played the whole rainbow! Daddy Mermaid cheers for you!")
		return
	_active_note = _progress
	_note_cycle_t = 0.0
	_update_note_point()
	_refresh_stage_state()


func _note_is_in_green() -> bool:
	return active_note_id() >= 0 and _zone_rect.has_point(_note_point)


func _opening_fade_clear() -> bool:
	return m.fade_rect == null or m.fade_rect.modulate.a <= 0.02


func _reset_press_state() -> void:
	_input_down = false
	_input_kind = ""
	_input_source = &""
	_press_position = Vector2.ZERO
	_current_position = Vector2.ZERO
	_touch_armed = false


func _capture_chime_state() -> void:
	_chime_snapshot_valid = m != null and m.chime != null
	if _chime_snapshot_valid:
		_chime_volume_db = m.chime.volume_db
		_chime_pitch_scale = m.chime.pitch_scale


func _restore_chime_state() -> void:
	if _chime_snapshot_valid and m != null and m.chime != null:
		m.chime.volume_db = _chime_volume_db
		m.chime.pitch_scale = _chime_pitch_scale
	_chime_snapshot_valid = false
