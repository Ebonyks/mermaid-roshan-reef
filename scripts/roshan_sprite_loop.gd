class_name RoshanSpriteLoop
extends Node
# Lightweight always-on atlas player for cutaway modes that use their own
# Roshan standee instead of the primary Player node. Even at zero velocity the
# loop advances slowly, so a stopped kart, puzzle room, or stage never leaves
# her frozen on one frame.

const SWIM_FRONT: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_swim_front.png")
const SWIM_BACK: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_swim_back.png")
const ATLAS_COLUMNS := 4
const FRAME_COUNT := 16
const CELL_SIZE := Vector2(256.0, 256.0)
const IDLE_FPS := 4.0
const MAX_FPS := 12.0

var _sprite: Sprite3D = null
var _texture_rect: TextureRect = null
var _atlas_texture: AtlasTexture = null
var _motion_node: Node3D = null
var _last_position := Vector3.ZERO
var _has_last_position := false
var _frame_cursor := 0.0
var _displayed_frame := -1

func setup_sprite_3d(sprite: Sprite3D, back_view: bool = false,
	motion_node: Node3D = null) -> void:
	_sprite = sprite
	_motion_node = motion_node if motion_node != null else sprite
	_sprite.texture = SWIM_BACK if back_view else SWIM_FRONT
	_sprite.hframes = ATLAS_COLUMNS
	_sprite.vframes = FRAME_COUNT / ATLAS_COLUMNS
	_apply_frame(0)

func setup_texture_rect(texture_rect: TextureRect,
	back_view: bool = false) -> void:
	_texture_rect = texture_rect
	_atlas_texture = AtlasTexture.new()
	_atlas_texture.atlas = SWIM_BACK if back_view else SWIM_FRONT
	_texture_rect.texture = _atlas_texture
	_apply_frame(0)

func _process(delta: float) -> void:
	if not _has_target():
		queue_free()
		return
	var speed: float = _sample_speed(delta)
	var fps: float = minf(IDLE_FPS + speed * 0.35, MAX_FPS)
	_frame_cursor = fposmod(_frame_cursor + delta * fps, float(FRAME_COUNT))
	_apply_frame(int(floor(_frame_cursor)))

func _has_target() -> bool:
	return (_sprite != null and is_instance_valid(_sprite)) \
		or (_texture_rect != null and is_instance_valid(_texture_rect))

func _sample_speed(delta: float) -> float:
	if _motion_node == null or not is_instance_valid(_motion_node):
		return 0.0
	var current: Vector3 = _motion_node.global_position
	if not _has_last_position:
		_last_position = current
		_has_last_position = true
		return 0.0
	var speed: float = current.distance_to(_last_position) / maxf(delta, 0.001)
	_last_position = current
	return speed

func _apply_frame(frame_index: int) -> void:
	var safe_frame: int = posmod(frame_index, FRAME_COUNT)
	if safe_frame == _displayed_frame:
		return
	_displayed_frame = safe_frame
	if _sprite != null and is_instance_valid(_sprite):
		_sprite.frame = safe_frame
	if _atlas_texture != null:
		var column: int = safe_frame % ATLAS_COLUMNS
		var row: int = safe_frame / ATLAS_COLUMNS
		_atlas_texture.region = Rect2(
			Vector2(float(column), float(row)) * CELL_SIZE, CELL_SIZE)
