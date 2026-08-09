class_name OperaRoshanActor
extends Node
## Lightweight atlas player for Mermaid Roshan's Opera career costumes.
## It owns only the target TextureRect's texture; layout and transforms remain
## under the career world's control.

const ATLAS_PATH := "res://assets/opera/worlds/actors/animation/roshan_%s_sheet_a.png"
const ATLAS_SIZE := Vector2i(1024, 1024)
const CELL_SIZE := Vector2(256.0, 256.0)
const FRAME_COUNT := 4
const ANIMATION_ROWS := {
	"idle": 0,
	"travel": 1,
	"work": 2,
	"cheer": 3,
}
const ANIMATION_FPS := {
	"idle": 4.0,
	"travel": 8.0,
	"work": 7.0,
	"cheer": 6.0,
}

var has_animation: bool = false
var current_animation: String = "stopped"
var current_frame: int = 0

var _target: TextureRect = null
var _fallback: Texture2D = null
var _sheet: Texture2D = null
var _frame_texture: AtlasTexture = null
var _frame_elapsed: float = 0.0
var _playing: bool = false


static func idle_frame(career: String, fallback: Texture2D = null) -> Texture2D:
	# Menus use the accepted atlas's first idle cell even when a card is not
	# highlighted. This keeps every visible costume on the audited full-tail
	# art while one shared animator advances only the highlighted card.
	var career_key: String = career.strip_edges().to_lower()
	if career_key.is_empty() or career_key.contains("/") \
			or career_key.contains("\\") or career_key.contains(".."):
		return fallback
	var sheet_path: String = ATLAS_PATH % career_key
	if not ResourceLoader.exists(sheet_path):
		return fallback
	var sheet := ResourceLoader.load(sheet_path) as Texture2D
	if sheet == null or sheet.get_width() != ATLAS_SIZE.x \
			or sheet.get_height() != ATLAS_SIZE.y:
		return fallback
	var frame := AtlasTexture.new()
	frame.atlas = sheet
	frame.filter_clip = true
	frame.region = Rect2(Vector2.ZERO, CELL_SIZE)
	return frame


func setup(target: TextureRect, career: String, fallback: Texture2D) -> void:
	_restore_fallback()
	_target = target
	_fallback = fallback if fallback != null else (
		target.texture if target != null and is_instance_valid(target) else null)
	_sheet = null
	_frame_texture = null
	has_animation = false
	current_animation = "stopped"
	current_frame = 0
	_frame_elapsed = 0.0
	_playing = false
	set_process(false)
	if not _has_target():
		return

	var career_key: String = career.strip_edges().to_lower()
	if not _valid_career_key(career_key):
		_restore_fallback()
		return
	var sheet_path: String = ATLAS_PATH % career_key
	if ResourceLoader.exists(sheet_path):
		var loaded: Resource = ResourceLoader.load(sheet_path)
		_sheet = loaded as Texture2D
	if _sheet == null \
			or _sheet.get_width() != ATLAS_SIZE.x \
			or _sheet.get_height() != ATLAS_SIZE.y:
		_sheet = null
		_restore_fallback()
		return

	_frame_texture = AtlasTexture.new()
	_frame_texture.atlas = _sheet
	_frame_texture.filter_clip = true
	has_animation = true
	play("idle")


func play(animation: String) -> void:
	var requested: String = animation.strip_edges().to_lower()
	if not ANIMATION_ROWS.has(requested):
		stop()
		return
	current_animation = requested
	current_frame = 0
	_frame_elapsed = 0.0
	if not has_animation or not _has_target() or _frame_texture == null:
		_playing = false
		set_process(false)
		_restore_fallback()
		return
	_playing = true
	_apply_frame()
	set_process(true)


func stop() -> void:
	_playing = false
	current_animation = "stopped"
	current_frame = 0
	_frame_elapsed = 0.0
	set_process(false)
	_restore_fallback()


func animation_state() -> String:
	return current_animation


func _process(delta: float) -> void:
	if not _playing or not has_animation:
		set_process(false)
		return
	if not _has_target():
		_playing = false
		set_process(false)
		return
	var fps: float = float(ANIMATION_FPS.get(current_animation, 0.0))
	if fps <= 0.0:
		stop()
		return
	var frame_seconds: float = 1.0 / fps
	_frame_elapsed += maxf(delta, 0.0)
	var advance: int = int(floor(_frame_elapsed / frame_seconds))
	if advance <= 0:
		return
	_frame_elapsed = fposmod(_frame_elapsed, frame_seconds)
	current_frame = posmod(current_frame + advance, FRAME_COUNT)
	_apply_frame()


func _apply_frame() -> void:
	if not _has_target() or _frame_texture == null:
		return
	var row: int = int(ANIMATION_ROWS.get(current_animation, 0))
	_frame_texture.region = Rect2(
		Vector2(float(current_frame) * CELL_SIZE.x, float(row) * CELL_SIZE.y),
		CELL_SIZE)
	_target.texture = _frame_texture


func _restore_fallback() -> void:
	if _has_target():
		_target.texture = _fallback


func _has_target() -> bool:
	return _target != null and is_instance_valid(_target)


func _valid_career_key(career_key: String) -> bool:
	return not career_key.is_empty() \
		and not career_key.contains("/") \
		and not career_key.contains("\\") \
		and not career_key.contains("..")
