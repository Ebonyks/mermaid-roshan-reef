extends OperaGeologySurface
## R16 nonruntime whole-hand candidate; R15 seam treatment retained as context,unaccepted.
const CUE_PATH := "res://assets/mg/star.png"
var cue_texture: Texture2D = load(CUE_PATH) as Texture2D

func _draw_geode() -> void:
	var center := GEODE_RECT.get_center()
	var seam_x := center.x
	var opened := geode_pull > 0.0
	if opened:
		_draw_ellipse(center + Vector2(geode_pull * 0.5, 0.0),
			Vector2(36.0 + geode_pull * 0.32, 122.0), Color("#291f48"),
			Color("#392958"), 8.0)
		if crystals_texture != null:
			draw_texture_rect(crystals_texture,
				Rect2(center + Vector2(geode_pull * 0.5 - 78.0, -84.0),
					Vector2(156.0, 168.0)), false)
		else:
			_draw_crystal_gallery(center + Vector2(geode_pull * 0.5, 18.0))
	var left_half := _geode_half_points(seam_x, center.y, -1.0, 0.0)
	var right_half := _geode_half_points(seam_x + geode_pull, center.y, 1.0, 0.0)
	draw_colored_polygon(left_half, Color("#65506e"))
	draw_colored_polygon(right_half, Color("#755c7d"))
	var left_outline := left_half.duplicate()
	left_outline.append(left_half[0])
	draw_polyline(left_outline, Color("#392958"), 12.0, true)
	var right_outline := right_half.duplicate()
	right_outline.append(right_half[0])
	draw_polyline(right_outline, Color("#392958"), 12.0, true)
	if not opened:
		draw_line(Vector2(seam_x, center.y - 130.0),
			Vector2(seam_x, center.y + 130.0), Color("#392958"), 9.0, true)
	if not opened:
		assert(cue_texture != null, "R15 source must load; no circle/halo artwork fallback")
		for index in range(GEODE_SEAM_SPOTS.size()):
			var spot: Vector2 = GEODE_SEAM_SPOTS[index]
			var alpha: float = 0.32 if geode_seams[index] else 1.0
			draw_texture_rect(cue_texture, Rect2(spot - Vector2(32, 32), Vector2(64, 64)),
				false, Color(1, 1, 1, alpha))

func marker_spot(index: int) -> Vector2:
	return GEODE_SEAM_SPOTS[index]

const HAND_PATH := "res://assets_src/flat_vector_pointer_20261013/pointer_1024.png"
const HAND_SIDE := 74.0
const HAND_TIP_UV := Vector2(0.44580078125, 0.90625)
var painted_hand: Texture2D = ImageTexture.create_from_image(Image.load_from_file(HAND_PATH))

func hand_contract() -> Dictionary:
	var pose: Dictionary = _demo_finger_pose()
	var at: Vector2 = pose.get("at", size * 0.5)
	var pressing: bool = bool(pose.get("pressing", false))
	var origin: Vector2 = at - HAND_TIP_UV * HAND_SIDE
	if not pressing:
		origin.y -= 8.0
	var tip: Vector2 = origin + HAND_TIP_UV * HAND_SIDE
	return {"demo_active": demo_active, "demo_t": demo_t,
		"at": [at.x, at.y], "pressing": pressing,
		"rect": [origin.x, origin.y, HAND_SIDE, HAND_SIDE],
		"visible_fingertip": [tip.x, tip.y], "source": HAND_PATH}

func _draw_demo_finger() -> void:
	if mode != "geology_geode":
		super._draw_demo_finger()
		return
	assert(painted_hand != null, "R16 hand source must load; no flat marker fallback")
	var contract: Dictionary = hand_contract()
	var rect: Array = contract["rect"]
	draw_texture_rect(painted_hand,
		Rect2(float(rect[0]), float(rect[1]), HAND_SIDE, HAND_SIDE), false)
