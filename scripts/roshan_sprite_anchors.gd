class_name RoshanSpriteAnchors
extends RefCounted
# Anatomical pivots measured from the approved 256x256 atlas cells. The
# generated swim sheets move Roshan's torso through the cell as well as moving
# her limbs; compensating that authored cell drift keeps her body attached to
# the gameplay position without changing a pixel of the approved source art.

const DIRECTIONAL := [
	Vector2(152.1, 115.2), Vector2(140.5, 117.4),
	Vector2(110.2, 115.2), Vector2(130.5, 119.7),
	Vector2(142.7, 117.6), Vector2(134.4, 116.6),
	Vector2(107.4, 109.8), Vector2(84.4, 110.0),
]
const SWIM_FRONT := [
	Vector2(136.5, 118.1), Vector2(119.4, 120.9),
	Vector2(110.0, 121.8), Vector2(102.9, 121.0),
	Vector2(141.2, 101.7), Vector2(122.5, 100.4),
	Vector2(113.2, 101.8), Vector2(102.9, 102.4),
	Vector2(146.8, 84.2), Vector2(135.6, 89.4),
	Vector2(123.7, 91.7), Vector2(106.1, 91.2),
	Vector2(137.0, 66.0), Vector2(120.1, 69.9),
	Vector2(111.0, 71.1), Vector2(101.8, 71.0),
]
const SWIM_BACK := [
	Vector2(125.9, 107.2), Vector2(120.1, 110.2),
	Vector2(123.0, 107.6), Vector2(109.7, 109.6),
	Vector2(141.2, 93.9), Vector2(130.0, 93.5),
	Vector2(122.2, 96.2), Vector2(124.0, 96.8),
	Vector2(136.0, 86.5), Vector2(124.4, 84.9),
	Vector2(127.3, 89.4), Vector2(111.0, 87.5),
	Vector2(126.0, 71.0), Vector2(117.1, 75.1),
	Vector2(117.8, 75.0), Vector2(109.4, 74.8),
]

static func anchor(sheet: String, frame_index: int) -> Vector2:
	var anchors: Array
	match sheet:
		"directional":
			anchors = DIRECTIONAL
		"swim_front":
			anchors = SWIM_FRONT
		"swim_back":
			anchors = SWIM_BACK
		_:
			return Vector2.ZERO
	return anchors[clampi(frame_index, 0, anchors.size() - 1)] as Vector2

static func has_sheet(sheet: String) -> bool:
	return sheet == "directional" or sheet == "swim_front" \
		or sheet == "swim_back"

static func correction(sheet: String, frame_index: int,
		target_anchor: Vector2, flipped: bool) -> Vector2:
	if not has_sheet(sheet):
		return Vector2.ZERO
	var frame_anchor: Vector2 = anchor(sheet, frame_index)
	# Texture pixels run down the page, while Sprite3D.offset.y moves upward in
	# world space. Horizontal compensation follows image coordinates; vertical
	# compensation therefore uses the opposite sign.
	var result := Vector2(
		target_anchor.x - frame_anchor.x,
		frame_anchor.y - target_anchor.y)
	if flipped:
		result.x = -result.x
	return result
