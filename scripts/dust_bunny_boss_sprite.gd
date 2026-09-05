class_name DustBunnyBossSprite
extends Node3D
# Four-frame 2D boss animations displayed on one unshaded Sprite3D card.
# Gameplay owns arena movement; this class owns the visual three-by-three hit cycle.

signal action_finished(animation: StringName)
signal vulnerability_changed(is_open: bool)
signal tap_progress_changed(accepted_taps: int, required_taps: int)
signal damage_cycle_completed
signal boss_health_changed(rounds_remaining: int, total_rounds: int)
signal final_round_started(speed_multiplier: float)
signal implosion_finished

const FRAME_SIZE := Vector2i(512, 512)
const FRAME_COUNT := 4
const COLUMNS := 2
const DISPLAY_HEIGHT := 7.2
const REQUIRED_TAPS := 3
const TOTAL_DAMAGE_ROUNDS := 3
const VULNERABILITY_WINDOW := 0.75
const FINAL_ROUND_VULNERABILITY_WINDOW := 0.65
const FINAL_ROUND_SPEED_SCALE := 1.25
const SHEET_ROOT := "res://assets/sprites/dust_bunnies/boss/"
const TAP_SFX_PATHS: Array[String] = [
	"res://assets/audio/ui_tap.ogg",
	"res://assets/audio/hop_boing.ogg",
	"res://assets/audio/chime.ogg",
]
const TAP_SFX_PITCHES: Array[float] = [0.86, 1.04, 1.18]
const TAP_SFX_VOLUMES: Array[float] = [-5.0, -9.0, -6.0]
const ANIMATION_SPECS: Dictionary = {
	&"idle": {
		"path": SHEET_ROOT + "dust_bunny_boss_jump.png",
		"fps": 1.0,
		"loop": true,
		"frames": [0],
	},
	&"jump": {
		"path": SHEET_ROOT + "dust_bunny_boss_jump.png",
		"fps": 6.0,
		"loop": false,
		"frames": [0, 1, 2, 3],
	},
	&"laugh_vulnerable": {
		"path": SHEET_ROOT + "dust_bunny_boss_laugh_vulnerable.png",
		"fps": 5.0,
		"loop": false,
		"frames": [0, 1, 2, 3],
	},
	&"flinch_1": {
		"path": SHEET_ROOT + "dust_bunny_boss_flinch.png",
		"fps": 12.0,
		"loop": false,
		"frames": [0, 1],
	},
	&"flinch_2": {
		"path": SHEET_ROOT + "dust_bunny_boss_flinch.png",
		"fps": 12.0,
		"loop": false,
		"frames": [1, 2],
	},
	&"flinch_3": {
		"path": SHEET_ROOT + "dust_bunny_boss_flinch.png",
		"fps": 10.0,
		"loop": false,
		"frames": [2, 3],
	},
	&"angry": {
		"path": SHEET_ROOT + "dust_bunny_boss_angry.png",
		"fps": 7.0,
		"loop": false,
		"frames": [0, 1, 2, 3],
	},
	&"angry_jump_final": {
		"path": SHEET_ROOT + "dust_bunny_boss_angry.png",
		"paths": [
			SHEET_ROOT + "dust_bunny_boss_angry.png",
			SHEET_ROOT + "dust_bunny_boss_angry.png",
			SHEET_ROOT + "dust_bunny_boss_jump.png",
			SHEET_ROOT + "dust_bunny_boss_jump.png",
		],
		"fps": 8.0,
		"loop": false,
		"frames": [2, 3, 1, 3],
	},
	&"implode": {
		"path": SHEET_ROOT + "dust_bunny_boss_implode.png",
		"fps": 6.0,
		"loop": false,
		"frames": [0, 1, 2, 3],
	},
}

var sprite: AnimatedSprite3D = null
var tap_sfx_player: AudioStreamPlayer3D = null
var action_locked: bool = false
var vulnerable: bool = false
var defeated: bool = false
var accepted_taps: int = 0
var vulnerability_time_left: float = 0.0
var last_tap_sfx_path: String = ""
var damage_rounds_completed: int = 0
var boss_health_rounds_remaining: int = TOTAL_DAMAGE_ROUNDS
var final_round_active: bool = false
var combat_speed_scale: float = 1.0


func _ready() -> void:
	name = "DustBunnyBoss"
	add_to_group(&"enemy")
	add_to_group(&"boss_enemy")
	add_to_group(&"dust_bunny_boss")
	sprite = AnimatedSprite3D.new()
	sprite.name = "AnimatedDustBunnyBoss"
	sprite.sprite_frames = make_sprite_frames()
	sprite.position.y = DISPLAY_HEIGHT * 0.5
	sprite.pixel_size = DISPLAY_HEIGHT / float(FRAME_SIZE.y)
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	sprite.shaded = false
	sprite.double_sided = true
	sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	sprite.visibility_range_end = 110.0
	sprite.visibility_range_end_margin = 10.0
	sprite.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
	sprite.frame_changed.connect(_on_frame_changed)
	sprite.animation_finished.connect(_on_animation_finished)
	add_child(sprite)
	tap_sfx_player = AudioStreamPlayer3D.new()
	tap_sfx_player.name = "BossTapSfx"
	tap_sfx_player.bus = &"SFX"
	tap_sfx_player.unit_size = 8.0
	tap_sfx_player.max_distance = 65.0
	tap_sfx_player.max_polyphony = 3
	add_child(tap_sfx_player)
	sprite.play(&"idle")


static func make_sprite_frames() -> SpriteFrames:
	var frames: SpriteFrames = SpriteFrames.new()
	if frames.has_animation(&"default"):
		frames.remove_animation(&"default")
	for animation: StringName in ANIMATION_SPECS:
		var spec: Dictionary = ANIMATION_SPECS[animation]
		var default_path: String = String(spec["path"])
		var source_paths: Array = spec.get("paths", []) as Array
		frames.add_animation(animation)
		frames.set_animation_speed(animation, float(spec["fps"]))
		frames.set_animation_loop(animation, bool(spec["loop"]))
		var source_frames: Array = spec["frames"] as Array
		for sequence_index: int in source_frames.size():
			var source_frame: Variant = source_frames[sequence_index]
			var frame_index: int = int(source_frame)
			var path: String = default_path
			if sequence_index < source_paths.size():
				path = String(source_paths[sequence_index])
			var texture: Texture2D = load(path) as Texture2D
			if texture == null:
				push_error("Dust-bunny boss sheet could not be loaded: %s" % path)
				continue
			if texture.get_width() != FRAME_SIZE.x * COLUMNS \
					or texture.get_height() != FRAME_SIZE.y * 2:
				push_error("Dust-bunny boss sheet has the wrong grid size: %s" % path)
				continue
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


func play_jump(direction_x: float = 1.0) -> float:
	_reset_tap_progress()
	set_facing_x(direction_x)
	var jump_animation: StringName = (
		&"angry_jump_final" if final_round_active else &"jump"
	)
	return _play_action(jump_animation)


func play_vulnerable_laugh() -> float:
	_reset_tap_progress()
	return _play_action(&"laugh_vulnerable")


func register_vulnerable_tap() -> bool:
	if sprite == null or defeated or not vulnerable or vulnerability_time_left <= 0.0:
		return false
	accepted_taps += 1
	tap_progress_changed.emit(accepted_taps, REQUIRED_TAPS)
	_play_tap_sfx(accepted_taps)
	var flinch_animation: StringName = StringName("flinch_%d" % accepted_taps)
	action_locked = true
	sprite.speed_scale = combat_speed_scale
	sprite.stop()
	sprite.play(flinch_animation)
	if accepted_taps >= REQUIRED_TAPS:
		_set_vulnerable(false)
		_complete_damage_round()
	return true


func _process(delta: float) -> void:
	if not vulnerable:
		return
	vulnerability_time_left = maxf(0.0, vulnerability_time_left - delta)
	if vulnerability_time_left <= 0.0:
		_expire_tap_window()


func _play_tap_sfx(tap_number: int) -> void:
	var tap_index: int = clampi(tap_number - 1, 0, TAP_SFX_PATHS.size() - 1)
	last_tap_sfx_path = TAP_SFX_PATHS[tap_index]
	var stream: AudioStream = load(last_tap_sfx_path) as AudioStream
	if tap_sfx_player == null or stream == null:
		return
	tap_sfx_player.stream = stream
	tap_sfx_player.pitch_scale = TAP_SFX_PITCHES[tap_index]
	tap_sfx_player.volume_db = TAP_SFX_VOLUMES[tap_index]
	tap_sfx_player.play()


func _expire_tap_window() -> void:
	if not vulnerable:
		return
	_set_vulnerable(false)
	# An expired tell is encouragement to watch the next hop, never an angry
	# punishment beat. The boss keeps moving playfully and the round remains
	# available through the normal mercy pacing.
	play_jump()


func play_angry() -> float:
	_reset_tap_progress()
	var angry_animation: StringName = (
		&"angry_jump_final" if final_round_active else &"angry"
	)
	return _play_action(angry_animation)


func play_implode() -> float:
	if sprite == null or defeated:
		return 0.0
	_reset_tap_progress()
	defeated = true
	sprite.visible = true
	return _play_action(&"implode", true)


func _play_action(animation: StringName, allow_defeated: bool = false) -> float:
	if sprite == null or (defeated and not allow_defeated):
		return 0.0
	_set_vulnerable(false)
	action_locked = true
	sprite.speed_scale = 1.0 if animation == &"implode" else combat_speed_scale
	sprite.stop()
	sprite.play(animation)
	return animation_duration(animation)


func animation_duration(animation: StringName) -> float:
	if sprite == null or not sprite.sprite_frames.has_animation(animation):
		return 0.0
	var fps: float = sprite.sprite_frames.get_animation_speed(animation)
	if fps <= 0.0:
		return 0.0
	var playback_scale: float = 1.0 if animation == &"implode" else combat_speed_scale
	return float(sprite.sprite_frames.get_frame_count(animation)) / (
		fps * playback_scale
	)


func set_facing_x(direction_x: float) -> void:
	if sprite != null and absf(direction_x) > 0.02:
		sprite.flip_h = direction_x < 0.0


func close_vulnerability() -> void:
	_set_vulnerable(false)
	_reset_tap_progress()


func _set_vulnerable(is_open: bool) -> void:
	if vulnerable == is_open:
		return
	vulnerable = is_open
	vulnerability_time_left = current_vulnerability_window() if vulnerable else 0.0
	vulnerability_changed.emit(vulnerable)


func current_vulnerability_window() -> float:
	return (
		FINAL_ROUND_VULNERABILITY_WINDOW
		if final_round_active
		else VULNERABILITY_WINDOW
	)


func _complete_damage_round() -> void:
	damage_rounds_completed = mini(
		damage_rounds_completed + 1,
		TOTAL_DAMAGE_ROUNDS
	)
	boss_health_rounds_remaining = TOTAL_DAMAGE_ROUNDS - damage_rounds_completed
	boss_health_changed.emit(
		boss_health_rounds_remaining,
		TOTAL_DAMAGE_ROUNDS
	)
	damage_cycle_completed.emit()
	if damage_rounds_completed == TOTAL_DAMAGE_ROUNDS - 1:
		final_round_active = true
		combat_speed_scale = FINAL_ROUND_SPEED_SCALE
		final_round_started.emit(combat_speed_scale)


func _reset_tap_progress() -> void:
	accepted_taps = 0
	tap_progress_changed.emit(accepted_taps, REQUIRED_TAPS)


func _on_frame_changed() -> void:
	if sprite.animation == &"laugh_vulnerable" and sprite.frame >= 1:
		_set_vulnerable(true)


func _on_animation_finished() -> void:
	var finished_animation: StringName = sprite.animation
	match finished_animation:
		&"laugh_vulnerable":
			if vulnerable:
				sprite.pause()
				sprite.frame = FRAME_COUNT - 1
		&"flinch_1", &"flinch_2":
			action_finished.emit(finished_animation)
			if vulnerable and vulnerability_time_left > 0.0:
				sprite.animation = &"laugh_vulnerable"
				sprite.frame = FRAME_COUNT - 1
				sprite.pause()
			else:
				play_angry()
		&"flinch_3":
			action_finished.emit(finished_animation)
			if boss_health_rounds_remaining <= 0:
				play_implode()
			else:
				play_angry()
		&"implode":
			_set_vulnerable(false)
			sprite.stop()
			sprite.visible = false
			implosion_finished.emit()
			action_finished.emit(finished_animation)
		_:
			action_locked = false
			sprite.speed_scale = 1.0
			sprite.play(&"idle")
			action_finished.emit(finished_animation)
