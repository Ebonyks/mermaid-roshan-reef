class_name DayOneCastleGrime
extends Node2D
## Day One's temporary code-drawn disrepair marks, split out of
## DayOneCastleDressing so a room whose cleanup authors its own dirty state can
## hide them while the dressing keeps its approved dust-bunny cutouts.
##
## This is measured overdraw debt (MA-VIS-008, gold-star OD3/OD5): an edge
## grime band, drips, a 12% interior wash and two cracks drawn as code shapes
## above the room art and Roshan. It stays only in rooms that have no authored
## dirty state yet; DayOneCastleDressing.AUTHORED_DIRT_ROOMS lists the rooms
## that no longer draw it.

const EXTERIOR_GRIME_COLOR := Color(0.19, 0.16, 0.29, 0.18)
const INTERIOR_DIRT_COLOR := Color(0.22, 0.18, 0.32, 0.12)
const CRACK_COLOR := Color(0.18, 0.14, 0.25, 0.38)
const MAIN_HALL_ID := "main_hall"

var _room_id := MAIN_HALL_ID
var _room_center := Vector2.ZERO
var _room_dirty := false


func show_for(room_id: String, room_center: Vector2, room_dirty: bool) -> void:
	if room_id == _room_id and room_center == _room_center and room_dirty == _room_dirty:
		return
	_room_id = room_id
	_room_center = room_center
	_room_dirty = room_dirty
	queue_redraw()


func _draw() -> void:
	_draw_exterior_grime()
	if _room_id == MAIN_HALL_ID or not _room_dirty:
		return
	_draw_room_dressing()


func _draw_exterior_grime() -> void:
	# A low-alpha edge wash reads as grime without painting over the source art.
	draw_rect(Rect2(0.0, 0.0, 1280.0, 26.0), EXTERIOR_GRIME_COLOR)
	draw_rect(Rect2(0.0, 694.0, 1280.0, 26.0), EXTERIOR_GRIME_COLOR)
	draw_rect(Rect2(0.0, 0.0, 22.0, 720.0), EXTERIOR_GRIME_COLOR)
	draw_rect(Rect2(1258.0, 0.0, 22.0, 720.0), EXTERIOR_GRIME_COLOR)
	for index: int in range(8):
		var x: float = 46.0 + float(index) * 166.0
		var drip_height: float = 8.0 + float(index % 3) * 5.0
		draw_line(Vector2(x, 25.0), Vector2(x + 5.0, 25.0 + drip_height), EXTERIOR_GRIME_COLOR, 3.0)


func _draw_room_dressing() -> void:
	# This rect is the current room viewport, not a stitched hall overview.
	var room_rect := Rect2(Vector2.ZERO, Vector2(1280.0, 720.0))
	draw_rect(room_rect, INTERIOR_DIRT_COLOR)
	# Two short cracks keep the disrepair cue graphic and child-readable.
	var crack_origin := _room_center + Vector2(-76.0, -62.0)
	draw_line(crack_origin, crack_origin + Vector2(17.0, 12.0), CRACK_COLOR, 3.0)
	draw_line(crack_origin + Vector2(17.0, 12.0), crack_origin + Vector2(9.0, 29.0), CRACK_COLOR, 3.0)
	var second_crack := _room_center + Vector2(69.0, 35.0)
	draw_line(second_crack, second_crack + Vector2(-13.0, 9.0), CRACK_COLOR, 3.0)
