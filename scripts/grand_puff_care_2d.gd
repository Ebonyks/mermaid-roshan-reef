class_name GrandPuffCare2D
extends Sprite2D

## New care acting lives on Canvas. The retained encounter kit supplies timing
## and compatibility signals; its spatial card is hidden for this consumer.
const ATLAS := preload("res://assets/sprites/dust_bunnies/boss/grand_puff_cold_keys_v1.png")
const CELL := 512.0
const ROOT := Vector2(256.0, 470.0)
const FOREHEAD := Vector2(256.0, 282.0)
const ANIMATIONS: Dictionary = {
	&"idle": {"fps": 1.0, "loop": true, "keys": [0, 0, 1, 0]},
	&"care_breath": {"fps": 1.0, "loop": true, "keys": [1]},
	&"care_sneeze": {"fps": 6.0, "keys": [1, 2, 0, 0]},
	&"care_sneeze_final": {"fps": 8.0, "keys": [1, 2, 0, 0]},
	&"jump": {"fps": 6.0, "keys": [1, 2, 0, 0]},
	&"laugh_vulnerable": {"fps": 5.0, "keys": [0, 3, 3, 3]},
	&"flinch_1": {"fps": 12.0, "keys": [0, 3]},
	&"flinch_2": {"fps": 12.0, "keys": [3, 3]},
	&"flinch_3": {"fps": 10.0, "keys": [3, 3]},
	&"care_relief": {"fps": 2.5, "keys": [3, 3]},
	# Compatibility animation names never select the former hostile artwork.
	&"angry": {"fps": 2.5, "keys": [3, 3]},
	&"angry_jump_final": {"fps": 6.0, "keys": [1, 2, 0, 0]},
	&"implode": {"fps": 2.5, "keys": [3, 3, 3, 3]},
}

var _animation: StringName = &""
var _frame: int = -1


func _ready() -> void:
	name = "GrandPuffCareCanvas"
	centered = false
	offset = -ROOT
	z_index = 2
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS


static func make_frames() -> SpriteFrames:
	var result := SpriteFrames.new()
	result.remove_animation(&"default")
	var keys: Array[Texture2D] = []
	for index: int in range(4):
		var key := AtlasTexture.new()
		key.atlas = ATLAS
		key.region = Rect2(float(index % 2) * CELL, float(index / 2) * CELL,
			CELL, CELL)
		key.filter_clip = true
		keys.append(key)
	for animation: StringName in ANIMATIONS:
		var spec: Dictionary = ANIMATIONS[animation]
		result.add_animation(animation)
		result.set_animation_speed(animation, float(spec["fps"]))
		result.set_animation_loop(animation, bool(spec.get("loop", false)))
		for index: int in spec["keys"]:
			result.add_frame(animation, keys[index])
	return result


func present(frames: SpriteFrames, animation: StringName, frame: int,
		foot: Vector2, projected_edge: float) -> void:
	position = foot
	scale = Vector2.ONE * maxf(1.0, projected_edge) / CELL
	if _animation == animation and _frame == frame:
		return
	_animation = animation
	_frame = frame
	if frames != null and frames.has_animation(animation):
		texture = frames.get_frame_texture(animation,
			clampi(frame, 0, frames.get_frame_count(animation) - 1))


func forehead_anchor() -> Vector2:
	return position + (FOREHEAD - ROOT) * scale
