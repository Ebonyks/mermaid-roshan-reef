extends Node2D
## Shell lanterns belong to the same crossing as the deck and its approach.

const Terrain := preload("res://scripts/arena/enchanted_forest_terrain.gd")
const Art := preload("res://scripts/arena/enchanted_forest_card_samples.gd")
const WOOD := preload("res://assets/terrain/up_wood_col.jpg")
const SHELL := preload("res://assets/flats/castle/main_hall_2screen/castle_shell_sconce_touchable.png")
const SWITCHES: Array[Vector2] = [Terrain.BRIDGE + Vector2(-166, -60), Terrain.BRIDGE + Vector2(-157, 81)]
const TAP_RADIUS := 61.0
const EAST_COVE_WAYMARK := Terrain.BRIDGE + Vector2(105, -95)
const WEST_COVE_WAYMARK := Terrain.STOPS[4] + Vector2(116, -113)
const WAYMARK_RADIUS := 50.0
const SHELL_FACE := Rect2(204, 72, 608, 668)
const UNLIT := Color(0.61, 0.66, 0.72)

var mask := 0
var opening := 0.0
var _celebration := 0.0
var _shells: Array[Sprite2D] = []
var _near_rail := Node2D.new()


func _ready() -> void:
	name = "ShellBridge"
	z_index = -1
	_near_rail.name = "NearBridgeRail"
	_near_rail.z_index = 2
	_near_rail.draw.connect(_draw_near_rail)
	add_child(_near_rail)
	for target: Vector2 in SWITCHES:
		var shell := Sprite2D.new()
		shell.texture = Art.prop_sample(SHELL)
		shell.position = target
		shell.scale = Vector2.ONE * 102.0 / shell.texture.get_height()
		shell.modulate = UNLIT
		shell.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		shell.z_index = 6
		add_child(shell)
		_shells.append(shell)


func sync(bits: int, progress: float) -> void:
	if mask == bits and is_equal_approx(opening, progress):
		return
	mask = bits
	opening = progress
	for index: int in range(_shells.size()):
		_shells[index].modulate = Color.WHITE if mask & (1 << index) else UNLIT
	_near_rail.queue_redraw()
	queue_redraw()


func celebrate() -> void:
	_celebration = 1.10
	queue_redraw()


func tick(delta: float) -> void:
	if _celebration > 0.0:
		_celebration = maxf(0.0, _celebration - delta)
		queue_redraw()


func switch_at(point: Vector2) -> int:
	for index: int in range(SWITCHES.size()):
		if point.distance_to(SWITCHES[index]) < TAP_RADIUS:
			return index
	return -1


func cove_waymark_at(point: Vector2) -> bool:
	return point.distance_to(WEST_COVE_WAYMARK) <= WAYMARK_RADIUS \
		or (opening >= 1.0 and point.distance_to(EAST_COVE_WAYMARK) <= WAYMARK_RADIUS)


func _draw() -> void:
	var mid: Vector2 = Terrain.BRIDGE
	var left: float = mid.x - 118.0
	var right: float = mid.x + 118.0
	var deck_y: float = mid.y - 45.0
	_support(Rect2(left - 22.0, deck_y - 10.0, 66.0, 109.0))
	_support(Rect2(right - 44.0, deck_y - 10.0, 66.0, 109.0))
	var length: float = lerpf(36.0, 118.0, opening)
	_planks(Rect2(left, deck_y, length, 89.0))
	_planks(Rect2(right - length, deck_y, length, 89.0))
	if opening < 0.97:
		var post := Vector2(left + 19.0, deck_y)
		draw_line(post, post + Vector2(0, 92), Color("#806146"), 6.0, true)
		draw_circle(post + Vector2(0, 7), 7.5, Color("#d6ab66"), true)
		draw_circle(post + Vector2(0, 83), 7.5, Color("#d6ab66"), true)
	for index: int in range(SWITCHES.size()):
		var anchor: Vector2 = SWITCHES[index]
		var active: bool = bool(mask & (1 << index))
		draw_circle(anchor + Vector2(4, 50), 31.0, Color("#4f62515d"), true)
		_support(Rect2(anchor + Vector2(-23, 26), Vector2(46, 27)))
		draw_arc(anchor, 44.0, 0.0, TAU, 42,
			Color("#ffd679ef") if active else Color("#c7d7ccaa"), 3.0, true)


	_draw_cove_waymark(WEST_COVE_WAYMARK)
	if opening >= 1.0:
		_draw_cove_waymark(EAST_COVE_WAYMARK)
	if _celebration > 0.0:
		var at: Vector2 = Terrain.BRIDGE + Vector2(0, -5)
		var t: float = 1.0 - _celebration / 1.10
		for index: int in range(7):
			var radius: float = (30.0 + index * 5.0) * (0.62 + t)
			var point: Vector2 = at + Vector2.from_angle(index * TAU / 7.0 + t * 0.40) * radius
			point.y -= 27.0 * t
			var glow := Color(1.0, 0.93, 0.64, sin(PI * t) * 0.89)
			draw_line(point - Vector2(0, 6), point + Vector2(0, 6), glow, 2.6, true)
			draw_line(point - Vector2(5, 0), point + Vector2(5, 0), glow, 2.6, true)


func _draw_cove_waymark(at: Vector2) -> void:
	var plate := PackedVector2Array([Vector2(-41, 0), Vector2(-22, -19),
		Vector2(31, -19), Vector2(35, 15), Vector2(-22, 17)])
	for index: int in range(plate.size()):
		plate[index] += at
	draw_line(at + Vector2(12, 4), at + Vector2(12, 46), Color("#5b4d4b"), 10, true)
	draw_colored_polygon(plate, Color("#906a53"))
	plate.append(plate[0])
	draw_polyline(plate, Color("#5b4d4b"), 2.5, true)
	draw_texture_rect_region(SHELL, Rect2(at + Vector2(-10, -15), Vector2(25, 28)),
		SHELL_FACE, Color.WHITE)


func _planks(rect: Rect2) -> void:
	draw_rect(Rect2(rect.position + Vector2(0, 8), rect.size), Color("#5b4d4b"))
	var count: int = maxi(2, roundi(rect.size.x / 16.0))
	var width: float = rect.size.x / count
	for index: int in range(count):
		var at: Vector2 = rect.position + Vector2(index * width, 0)
		var wood: Color = Color("#c69870").lerp(Color("#e1b983"), 0.5 + 0.42 * sin(index * 2.5))
		var strip := Rect2(at, Vector2(width - 1.2, rect.size.y))
		draw_rect(strip, wood)
		var texture_region := Rect2(104 + (index % 4) * 61, 135, 56, 490)
		draw_texture_rect_region(WOOD, strip, texture_region, Color(1.0, 0.94, 0.85, 0.35))
		draw_line(at + Vector2(2, 4), at + Vector2(2, 83), Color("#f3d4a054"), 2.0, true)
	draw_line(rect.position, Vector2(rect.end.x, rect.position.y), Color("#edd4a0"), 3.0, true)
	draw_line(Vector2(rect.position.x, rect.end.y), rect.end, Color("#937055"), 4.0, true)
	if rect.size.x > 85.0:
		_draw_rope(self, rect.position.x, rect.size.x, rect.position.y + 4.0)


func _draw_near_rail() -> void:
	var length: float = lerpf(36.0, 118.0, opening)
	if length > 85.0:
		var mid: Vector2 = Terrain.BRIDGE
		_draw_rope(_near_rail, mid.x - 118.0, length, mid.y + 40.0)
		_draw_rope(_near_rail, mid.x + 118.0 - length, length, mid.y + 40.0)


func _draw_rope(layer: Node2D, x: float, width: float, y: float) -> void:
	var rope := PackedVector2Array()
	for step: int in range(9):
		var t: float = float(step) / 8.0
		rope.append(Vector2(lerpf(x + 9.0, x + width - 9.0, t), y - 8.0 - sin(t * PI) * 4.0))
	layer.draw_polyline(rope, Color("#755a49"), 4.0, true)
	layer.draw_polyline(rope, Color("#d6b781"), 2.0, true)


func _support(rect: Rect2) -> void:
	var stone := StyleBoxFlat.new()
	stone.bg_color = Color("#968977")
	stone.border_color = Color("#6c6c5c")
	stone.set_border_width_all(2)
	stone.set_corner_radius_all(11)
	draw_style_box(stone, rect)




