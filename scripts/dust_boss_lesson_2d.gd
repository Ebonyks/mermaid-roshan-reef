class_name DustBossLesson2D
extends Control

## Storybook effect choreography. Host input/state owns every actual action.
const DUST := preload("res://assets/opera/worlds/props/fx_dust_puff.png")
const STAR := preload("res://assets/opera/worlds/props/fx_stolen_sparkle.png")
const BUBBLES := preload("res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png")
var floor_effects: bool = false
var mode: String = ""
var from := Vector2.ZERO
var target := Vector2.ZERO
var tuft := Vector2.ZERO
var tuft_visible: bool = false
var boss_anchor := Vector2.ZERO
var counter_open: bool = false
var _time: float = 0.0
var _last_mode: String = ""
var _open_time: float = 0.0
var _redraw: float = 0.0
var _beam_time: float = 0.0
var _beam_from := Vector2.ZERO
var _beam_to := Vector2.ZERO
var _dust_time: float = 0.0
var _dust_at := Vector2.ZERO

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
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
	_open_time = _open_time + delta if counter_open else 0.0
	_beam_time = maxf(0.0, _beam_time - delta)
	_dust_time = maxf(0.0, _dust_time - delta)
	_redraw += delta
	if _redraw >= 1.0 / 30.0:
		_redraw = fmod(_redraw, 1.0 / 30.0)
		queue_redraw()

func _draw() -> void:
	if floor_effects:
		_draw_floor_effects()
		return
	if counter_open:
		# One gold invitation unfolds with the real opening; never a rehearsal.
		var unfold: float = smoothstep(0.0, 0.18, _open_time)
		var edge: float = (53.0 + sin(_open_time * 3.0) * 3.0) * lerpf(0.65, 1.0, unfold)
		_stamp(STAR, boss_anchor, Vector2.ONE * edge, unfold)
		for i: int in range(2):
			var angle: float = _open_time * 1.8 + float(i) * PI
			var point: Vector2 = boss_anchor + Vector2(cos(angle) * 37.0, sin(angle) * 13.0)
			_stamp(STAR, point, Vector2.ONE * 11.0, unfold * 0.7)
	if _beam_time > 0.0:
		_draw_counter()
	if mode == "move":
		_draw_current(fmod(_time, 2.6) / 2.6, 0.65)
	elif mode == "dash":
		var cycle: float = fmod(_time, 2.6)
		# Two painted bubble contacts, 260 ms apart, then a quick flowing wake.
		for onset: float in [0.0, 0.26]:
			var beat: float = (cycle - onset) / 0.18
			if beat >= 0.0 and beat <= 1.0:
				_stamp(BUBBLES, target, Vector2.ONE * lerpf(26.0, 52.0, beat), sin(beat * PI) * 0.9)
		if cycle >= 0.44 and cycle < 1.5:
			_draw_current((cycle - 0.44) / 1.06, 0.8)

func _draw_current(progress: float, alpha: float) -> void:
	var normal: Vector2 = (target - from).normalized().orthogonal()
	for i: int in range(5):
		var fraction: float = progress - float(i) * 0.09
		if fraction < 0.0 or fraction > 1.0:
			continue
		var point: Vector2 = from.lerp(target, fraction) + normal * sin(fraction * PI) * 13.0
		var edge: float = 42.0 - float(i) * 3.0
		_stamp(BUBBLES, point, Vector2.ONE * edge, sin(fraction * PI) * alpha)

func _draw_counter() -> void:
	var elapsed: float = 0.55 - _beam_time
	var arrive: float = clampf(elapsed / 0.16, 0.0, 1.0)
	for i: int in range(7):
		var fraction: float = clampf(arrive - float(i) * 0.08, 0.0, 1.0)
		var point: Vector2 = _beam_from.lerp(_beam_to, fraction) - Vector2(0.0, sin(fraction * PI) * 30.0)
		var edge: float = 24.0 - float(i) * 2.0
		_stamp(STAR, point, Vector2.ONE * edge, _beam_time / 0.55 * (1.0 - float(i) * 0.08))
	if arrive >= 1.0:
		var bloom: float = (elapsed - 0.16) / 0.39
		for i: int in range(5):
			var direction := Vector2.from_angle(TAU * float(i) / 5.0)
			_stamp(STAR, _beam_to + direction * bloom * 42.0, Vector2.ONE * (18.0 - bloom * 8.0), 1.0 - bloom)

func _draw_floor_effects() -> void:
	if tuft_visible:
		var breath: float = sin(_time * 1.8)
		_stamp(DUST, tuft + Vector2(0.0, breath * 2.0), Vector2(64.0 + breath * 2.0, 40.0), 0.95)
	if _dust_time > 0.0:
		var progress: float = 1.0 - _dust_time / 0.65
		for i: int in range(5):
			var direction := Vector2.from_angle(TAU * float(i) / 5.0)
			var point: Vector2 = _dust_at + direction * progress * Vector2(75.0, 25.0)
			point.y -= sin(progress * PI) * (11.0 + float(i % 2) * 7.0)
			var edge: float = 36.0 + sin(progress * PI) * 20.0
			_stamp(DUST, point, Vector2(edge, edge * 0.68), (1.0 - progress) * 0.72)

func _stamp(texture: Texture2D, point: Vector2, dimensions: Vector2, alpha: float) -> void:
	draw_set_transform(point, 0.0, dimensions / texture.get_size())
	draw_texture(texture, -texture.get_size() * 0.5, Color(1.0, 1.0, 1.0, alpha))
	draw_set_transform(Vector2.ZERO)
