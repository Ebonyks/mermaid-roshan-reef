class_name CastleDoorCue
extends Control
## Input-transparent Canvas cue for one existing painted castle door.

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const BONUS_PERIOD_SECONDS := 4.4
const PLOT_PERIOD_SECONDS := 3.2
const PLOT_SHIMMER_PERIOD_SECONDS := 4.6
const BONUS_OUTER_COLOR := Color(0.96, 0.34, 0.39)
const BONUS_GLOW_COLOR := Color(0.98, 0.26, 0.34)
const PLOT_GLOW_COLOR := Color(1.00, 0.72, 0.16)
const FRAME_GLOW_SHADER := preload(
	"res://shaders/castle_door_frame_glow.gdshader")
const FRAME_TEXTURES := {
	"small": preload(
		"res://assets/flats/castle/door_cues/door_frame_small_exact.png"),
	"opera": preload(
		"res://assets/flats/castle/door_cues/door_frame_opera_exact.png"),
	"royal": preload(
		"res://assets/flats/castle/door_cues/door_frame_royal_exact.png"),
}
const FRAME_FAMILY_INDEX := {
	"small": 0.0,
	"opera": 1.0,
	"royal": 2.0,
}

var door_state: String = DoorLanguage.OPEN
var motion_time := 0.0
var feedback_time := 0.0
var frame_family := ""
var frame_texture: Texture2D = null
var frame_material: ShaderMaterial = null


func _init() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = false
	_sync_visibility()


func configure_physical_frame(next_family: String) -> void:
	frame_family = next_family if FRAME_TEXTURES.has(next_family) else ""
	frame_texture = FRAME_TEXTURES.get(frame_family) as Texture2D
	if frame_texture != null:
		frame_material = ShaderMaterial.new()
		frame_material.shader = FRAME_GLOW_SHADER
	_sync_material()
	queue_redraw()


func set_door_state(next_state: String) -> void:
	var normalized: String = DoorLanguage.normalize(next_state)
	set_meta("castle_door_state", normalized)
	if door_state == normalized:
		return
	door_state = normalized
	_sync_visibility()
	queue_redraw()


func pulse_blocked_feedback() -> void:
	feedback_time = 0.72
	queue_redraw()


func pulse_plot_feedback() -> void:
	# Feedback can emphasize the real story destination, never promote a
	# blocked door or replace the authoritative state after a timer expires.
	if door_state != DoorLanguage.PLOT:
		return
	feedback_time = 0.72
	queue_redraw()


func _sync_visibility() -> void:
	visible = door_state != DoorLanguage.OPEN
	set_process(visible)
	_sync_material()


func _sync_material() -> void:
	var uses_frame: bool = frame_material != null \
		and door_state != DoorLanguage.OPEN
	material = frame_material if uses_frame else null
	if not uses_frame:
		return
	frame_material.set_shader_parameter("motion_time", motion_time)
	frame_material.set_shader_parameter("feedback_strength", feedback_time / 0.72)
	frame_material.set_shader_parameter("shimmer_period", PLOT_SHIMMER_PERIOD_SECONDS)
	frame_material.set_shader_parameter("frame_family",
		float(FRAME_FAMILY_INDEX.get(frame_family, 0.0)))
	var cue_mode := 0.0
	if door_state == DoorLanguage.PLOT:
		cue_mode = 1.0
	elif door_state == DoorLanguage.BLOCKED:
		cue_mode = 2.0
	frame_material.set_shader_parameter("cue_mode", cue_mode)
	frame_material.set_shader_parameter("cue_alpha",
		0.62 if door_state == DoorLanguage.PLOT else 0.36)


func _process(delta: float) -> void:
	motion_time += maxf(0.0, delta)
	feedback_time = maxf(0.0, feedback_time - maxf(0.0, delta))
	_sync_material()
	queue_redraw()


func _draw() -> void:
	if size.x < 2.0 or size.y < 2.0:
		return
	match door_state:
		DoorLanguage.BLOCKED:
			_draw_blocked()
		DoorLanguage.BONUS:
			_draw_bonus_glow()
		DoorLanguage.PLOT:
			_draw_plot_glow()


func _draw_blocked() -> void:
	if frame_texture != null:
		_draw_frame_glow()
		return
	var flutter: float = feedback_time / 0.72
	draw_rect(Rect2(Vector2.ZERO, size),
		Color(0.07, 0.05, 0.15, 0.16 + flutter * 0.10), true)
	for index: int in range(5):
		var phase: float = motion_time * (0.34 + float(index) * 0.025) \
			+ float(index) * 1.37
		var center := Vector2(
			fposmod(size.x * (0.12 + float(index) * 0.22)
				+ sin(phase) * size.x * 0.10, size.x),
			size.y * (0.22 + float(index % 3) * 0.27)
				+ cos(phase * 0.71) * size.y * 0.06)
		var radius: float = maxf(18.0, minf(size.x, size.y) *
			(0.18 + float(index % 2) * 0.05))
		draw_set_transform(center, sin(phase * 0.55) * 0.08,
			Vector2(1.75, 0.52 + flutter * 0.08))
		draw_circle(Vector2.ZERO, radius,
			Color(0.52, 0.52, 0.72, 0.22 + flutter * 0.10))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_bonus_glow() -> void:
	if frame_texture != null:
		_draw_frame_glow()
		return
	_draw_doorway_glow(BONUS_GLOW_COLOR,
		_motion_wave(BONUS_PERIOD_SECONDS), 0.18)


func _draw_plot_glow() -> void:
	if frame_texture != null:
		_draw_frame_glow()
		return
	_draw_doorway_glow(PLOT_GLOW_COLOR,
		_motion_wave(PLOT_PERIOD_SECONDS), 0.24)


func _draw_frame_glow() -> void:
	# The texture is an exact crop of the approved painted doorway. The shader
	# derives emission from those same pixels, so the luminous core cannot drift
	# away from the crest, arch, posts, or Royal Hall columns during camera motion.
	draw_texture_rect(frame_texture, Rect2(Vector2.ZERO, size), false,
		Color.WHITE)


func _draw_doorway_glow(color: Color, pulse: float,
		peak_alpha: float) -> void:
	var center := Vector2(size.x * 0.5, size.y * 0.58)
	# Leave generous transparent margins on every side. The previous ellipse
	# reached the Control bounds and clip_contents exposed those bounds as a
	# false rectangular door frame.
	var radius_x: float = maxf(1.0, size.x * 0.38)
	var top_budget: float = maxf(1.0, center.y - size.y * 0.10)
	var bottom_budget: float = maxf(1.0,
		size.y - center.y - size.y * 0.08)
	var radius_y: float = maxf(1.0, minf(size.y * 0.34,
		minf(top_budget, bottom_budget)))
	var glow_scale := Vector2(radius_x / radius_y, 1.0)
	for layer: int in range(9):
		var radius_fraction: float = 1.0 - float(layer) * 0.09
		var tint := color
		tint.a = peak_alpha * (0.11 + float(layer) * 0.025) \
			* (0.62 + pulse * 0.38)
		draw_set_transform(center, 0.0, glow_scale)
		draw_circle(Vector2.ZERO, radius_y * radius_fraction, tint,
			true, -1.0, true)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _motion_wave(period_seconds: float) -> float:
	return 0.5 + 0.5 * sin(motion_time * TAU / period_seconds)
