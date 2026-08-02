class_name DustBunnySprite
extends Node3D
# Mobile-safe animated dust-bunny enemy: three six-frame 2D atlases on one
# unshaded camera-facing card. The art remains a sprite at every stage.

signal hop_finished
signal defeat_finished

const FRAME_SIZE := Vector2i(256, 256)
const FRAME_COUNT := 6
const COLUMNS := 3
const DISPLAY_HEIGHT := 3.6
const SHEET_ROOT := "res://assets/sprites/dust_bunnies/"
const ANIMATION_SPECS: Dictionary = {
	&"idle": {
		"path": SHEET_ROOT + "dust_bunny_idle.png",
		"fps": 5.0,
		"loop": true,
	},
	&"hop": {
		"path": SHEET_ROOT + "dust_bunny_hop.png",
		"fps": 9.0,
		"loop": false,
	},
	&"defeat": {
		"path": SHEET_ROOT + "dust_bunny_defeat.png",
		"fps": 8.0,
		"loop": false,
	},
}

var sprite: AnimatedSprite3D = null
var action_locked: bool = false
var defeated: bool = false


func _ready() -> void:
	name = "DustBunnyEnemy"
	add_to_group(&"enemy")
	add_to_group(&"dust_bunny_enemy")
	sprite = AnimatedSprite3D.new()
	sprite.name = "AnimatedDustBunny"
	sprite.sprite_frames = _make_frames()
	sprite.position.y = DISPLAY_HEIGHT * 0.5
	sprite.pixel_size = DISPLAY_HEIGHT / float(FRAME_SIZE.y)
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	sprite.shaded = false
	sprite.double_sided = true
	sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	sprite.visibility_range_end = 90.0
	sprite.visibility_range_end_margin = 8.0
	sprite.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
	sprite.animation_finished.connect(_on_animation_finished)
	add_child(sprite)
	sprite.play(&"idle")


func _make_frames() -> SpriteFrames:
	var frames: SpriteFrames = SpriteFrames.new()
	if frames.has_animation(&"default"):
		frames.remove_animation(&"default")
	for animation: StringName in ANIMATION_SPECS:
		var spec: Dictionary = ANIMATION_SPECS[animation]
		var path: String = String(spec["path"])
		var texture: Texture2D = load(path) as Texture2D
		frames.add_animation(animation)
		frames.set_animation_speed(animation, float(spec["fps"]))
		frames.set_animation_loop(animation, bool(spec["loop"]))
		if texture == null:
			push_error("Dust-bunny sprite sheet could not be loaded: %s" % path)
			continue
		if texture.get_width() != FRAME_SIZE.x * COLUMNS \
				or texture.get_height() != FRAME_SIZE.y * 2:
			push_error("Dust-bunny sprite sheet has the wrong grid size: %s" % path)
			continue
		for frame_index in range(FRAME_COUNT):
			var column_index: int = frame_index % COLUMNS
			var row_index: int = frame_index / COLUMNS
			var atlas: AtlasTexture = AtlasTexture.new()
			atlas.atlas = texture
			atlas.region = Rect2(
				Vector2(
					float(column_index * FRAME_SIZE.x),
					float(row_index * FRAME_SIZE.y)
				),
				Vector2(FRAME_SIZE)
			)
			frames.add_frame(animation, atlas)
	return frames


func play_idle() -> void:
	if sprite == null or action_locked or defeated:
		return
	if sprite.animation != &"idle" or not sprite.is_playing():
		sprite.speed_scale = 1.0
		sprite.play(&"idle")


func play_hop(direction_x: float = 1.0, custom_speed: float = 1.0) -> float:
	if sprite == null or defeated:
		return 0.0
	set_facing_x(direction_x)
	action_locked = true
	sprite.speed_scale = custom_speed
	sprite.stop()
	sprite.play(&"hop")
	return animation_duration(&"hop") / maxf(custom_speed, 0.01)


func play_defeat(direction_x: float = 1.0) -> float:
	if sprite == null or defeated:
		return 0.0
	set_facing_x(direction_x)
	defeated = true
	action_locked = true
	sprite.visible = true
	sprite.speed_scale = 1.0
	sprite.stop()
	sprite.play(&"defeat")
	return animation_duration(&"defeat")


func animation_duration(animation: StringName) -> float:
	if sprite == null or not sprite.sprite_frames.has_animation(animation):
		return 0.0
	var fps: float = sprite.sprite_frames.get_animation_speed(animation)
	if fps <= 0.0:
		return 0.0
	return float(sprite.sprite_frames.get_frame_count(animation)) / fps


func set_facing_x(direction_x: float) -> void:
	if sprite != null and absf(direction_x) > 0.02:
		sprite.flip_h = direction_x < 0.0


func _on_animation_finished() -> void:
	match sprite.animation:
		&"hop":
			action_locked = false
			sprite.speed_scale = 1.0
			sprite.play(&"idle")
			hop_finished.emit()
		&"defeat":
			sprite.stop()
			sprite.visible = false
			defeat_finished.emit()
