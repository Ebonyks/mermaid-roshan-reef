class_name OperaNurseryCare
extends RefCounted
## Connected-body presentation only. The catch surface owns all progress/input.
## Keys are semantic receiving/lowering states, not a repeating atlas loop.
const DATA := "res://assets/opera/worlds/nursery/refinement_v2/care_keys.json"
const EXTENT := 250.0
const BABY_EXTENT := 72.0
const TRANSFER_TIME := 1.42
const FLOOR_Y := 0.80
const RETURN_SPEED := 320.0

var textures: Array[Texture2D] = []
var hips: Array[Vector2] = []
var palms: Array[Vector2] = []
var bounds: Array[Rect2] = []
var hip := Vector2.ZERO
var key := 1
var ready := false

func setup() -> bool:
	if not FileAccess.file_exists(DATA):
		return false
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(DATA))
	if not data is Dictionary or not (data as Dictionary).get("poses", []) is Array:
		return false
	var rows: Array = (data as Dictionary)["poses"]
	if rows.size() != 8:
		return false
	for row: Dictionary in rows:
		var path := "res://" + String(row["path"])
		if not ResourceLoader.exists(path):
			return false
		var texture: Texture2D = load(path) as Texture2D
		if texture == null or texture.get_size() != Vector2(512, 512):
			return false
		textures.append(texture)
		var pivot: Array = row["hip_xy"]
		var palm: Array = row["palm_xy"]
		var alpha: Array = row["alpha_bounds"]
		hips.append(Vector2(float(pivot[0]), float(pivot[1])) / 512.0)
		palms.append(Vector2(float(palm[0]), float(palm[1])) / 512.0)
		bounds.append(Rect2(Vector2(float(alpha[0]), float(alpha[1])) / 512.0,
			Vector2(float(alpha[2]) - float(alpha[0]), float(alpha[3]) - float(alpha[1])) / 512.0))
	ready = true
	return true

func reset(hand: Vector2) -> void:
	key = 1
	hip = hand - (palms[key] - hips[key]) * EXTENT

func hand_point() -> Vector2:
	return hip + (palms[key] - hips[key]) * EXTENT

func seek_hand(hand: Vector2, delta: float) -> void:
	key = 1
	var target: Vector2 = hand - (palms[key] - hips[key]) * EXTENT
	hip = hip.move_toward(target, RETURN_SPEED * delta)

func transfer_pose(transfer: Dictionary, target_hand: Vector2) -> void:
	var age: float = float(transfer["time"])
	if age < 0.16:
		key = 1
	elif age < 0.32:
		key = 2
	elif age < 0.78:
		key = 3
	elif age < 0.95:
		key = 4
	elif age < 1.08:
		key = 5
	elif age < 1.23:
		key = 6
	else:
		key = 7
	var from := Vector2(float(transfer["hip_x"]), float(transfer["hip_y"]))
	var target: Vector2 = target_hand - (palms[7] - hips[7]) * EXTENT
	var fraction := clampf((age - 0.32) / 0.46, 0.0, 1.0)
	# Whole-body movement is the actual local carry route. The baby is drawn
	# at the authored palms throughout; it never travels separately from her.
	hip = from.lerp(target, fraction)

func visible_rect() -> Rect2:
	var origin: Vector2 = hip - hips[key] * EXTENT
	return Rect2(origin + bounds[key].position * EXTENT, bounds[key].size * EXTENT)

func draw_body(canvas: Control) -> void:
	canvas.draw_texture_rect(textures[key], Rect2(hip - hips[key] * EXTENT,
		Vector2.ONE * EXTENT), false)
