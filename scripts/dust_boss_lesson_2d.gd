class_name DustBossLesson2D
extends Control

## Presentation only: gestures, connected sparkle and optional dust play.
## Host ticks own all progression. Effects never hit the boss or move Roshan.
const HAND = preload("res://assets/castle/training/ghost_hand.png")
const DUST = preload("res://assets/opera/worlds/props/fx_dust_puff.png")
var floor_effects: bool = false
var mode: String = ""
var from := Vector2.ZERO
var target := Vector2.ZERO
var tuft := Vector2.ZERO
var tuft_visible: bool = false
var _time: float = 0.0
var _last_mode: String = ""
var _redraw: float = 0.0
var _beam_time: float = 0.0
var _beam_from := Vector2.ZERO
var _beam_to := Vector2.ZERO
var _dust_time: float = 0.0
var _dust_at := Vector2.ZERO

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func counter(origin: Vector2, destination: Vector2) -> void:
	_beam_from = origin - Vector2(0.0, 28.0)
	_beam_to = destination
	_beam_time = 0.55

func land(point: Vector2) -> void:
	_dust_at = point
	_dust_time = 0.65

func _process(delta: float) -> void:
	if mode != _last_mode:
		_last_mode = mode
		_time = 0.0
	_time += delta
	_beam_time = maxf(0.0, _beam_time - delta)
	_dust_time = maxf(0.0, _dust_time - delta)
	_redraw += delta
	if _redraw >= 1.0 / 30.0:
		_redraw = 0.0
		queue_redraw()

func _draw() -> void:
	if floor_effects and tuft_visible:
		var edge: float = 62.0 + 3.0 * sin(_time * 2.0)
		draw_texture_rect(DUST, Rect2(tuft - Vector2(edge, edge) * 0.5, Vector2(edge, edge)), false)
	if floor_effects and _dust_time > 0.0:
		var progress: float = 1.0 - _dust_time / 0.65
		for i: int in range(5):
			var direction := Vector2.from_angle(TAU * float(i) / 5.0)
			var point: Vector2 = _dust_at + direction * progress * Vector2(66.0, 22.0)
			var edge: float = 42.0 + progress * 24.0
			draw_texture_rect(DUST, Rect2(point - Vector2.ONE * edge * 0.5, Vector2.ONE * edge), false, Color(1.0, 1.0, 1.0, (1.0 - progress) * 0.65))
	if floor_effects:
		return
	if _beam_time > 0.0:
		var progress: float = 1.0 - _beam_time / 0.55
		var tip: Vector2 = _beam_from.lerp(_beam_to, minf(1.0, progress * 3.0))
		draw_line(_beam_from, tip, Color(1.0, 0.80, 0.32, 1.0 - progress), 9.0, true)
		draw_line(_beam_from, tip, Color(1.0, 0.98, 0.80, 1.0 - progress), 3.0, true)
		for i: int in range(5):
			var point: Vector2 = _beam_from.lerp(tip, float(i + 1) / 5.0)
			draw_circle(point, 4.0 + sin(progress * PI) * 3.0, Color(1.0, 0.94, 0.54, 1.0 - progress))
	if mode == "":
		return
	var cycle: float = fmod(_time, 2.6)
	# Contact onsets are 260 ms apart, inside the real 360 ms dash window.
	var pressing: bool = cycle < 0.14 or (mode == "dash" and cycle > 0.26 and cycle < 0.40)
	var point: Vector2 = target
	# A moving ghost demonstrates the relation between finger and Roshan.
	# It never defines an accepted destination or draws a 'safe spot' marker.
	if mode == "move":
		point = from.lerp(target, smoothstep(0.0, 1.0, minf(cycle / 1.2, 1.0)))
	var hand_size := Vector2(72.0, 72.0)
	draw_texture_rect(HAND, Rect2(point - hand_size * Vector2(0.435, 0.875) - Vector2(0.0, 0.0 if pressing else 8.0), hand_size), false, Color(1.0, 1.0, 1.0, 0.85))
	if pressing:
		draw_arc(point, 19.0, 0.0, TAU, 24, Color(1.0, 0.94, 0.68, 0.85), 3.0, true)
