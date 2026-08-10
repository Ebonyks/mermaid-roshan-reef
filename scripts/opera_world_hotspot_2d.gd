class_name OperaWorldHotspot2D
extends Control
## One diegetic, non-reading activity invitation inside an Opera career room.
##
## The career world owns story/game state. This node owns only the established
## world-object affordance, a generous invisible touch target, and a short
## object-local handoff animation. It deliberately has no labels, progress, or
## reward logic.

signal pressed(station_index: int)
signal opening_finished(station_index: int)

const Affordance := preload("res://scripts/interaction_affordance.gd")

const MIN_TOUCH := Vector2(112.0, 112.0)
const OPENING_SECONDS := 0.62
const DEFAULT_ENVELOPE := Vector2(212.0, 212.0)

var station_index := -1
var station_id := ""
var source_path := ""
var motion := "breathe"
var object_texture: Texture2D = null
var object_size := Vector2(124.0, 124.0)
var hit_size := MIN_TOUCH
var object_center := DEFAULT_ENVELOPE * 0.5
var elapsed := 0.0
var opening_t := 0.0
var armed := false
var focused := false
var opening := false
var activation_count := 0
var touch_button: Button = null


func setup(index: int, id: String, stage_object_pos: Vector2,
		texture_path: String, animation_kind: String,
		visual_size: Vector2 = Vector2(124.0, 124.0),
		authored_hit_size: Vector2 = MIN_TOUCH) -> void:
	station_index = index
	station_id = id
	source_path = texture_path
	motion = animation_kind if not animation_kind.is_empty() else "breathe"
	object_size = visual_size
	hit_size = Vector2(
		maxf(MIN_TOUCH.x, authored_hit_size.x),
		maxf(MIN_TOUCH.y, authored_hit_size.y))
	var envelope := Vector2(
		maxf(DEFAULT_ENVELOPE.x, hit_size.x + 72.0),
		maxf(DEFAULT_ENVELOPE.y, hit_size.y + 72.0))
	size = envelope
	position = stage_object_pos - envelope * 0.5
	object_center = envelope * 0.5
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = false
	object_texture = load(texture_path) as Texture2D \
		if not texture_path.is_empty() and ResourceLoader.exists(texture_path) else null
	_build_touch_button()
	set_meta("station_index", station_index)
	set_meta("station_id", station_id)
	set_meta("source_path", source_path)
	set_meta("motion", motion)
	set_meta("affordance_kind", Affordance.PLOT)
	set_meta("object_pos", stage_object_pos)
	set_meta("hit_size", hit_size)
	visible = false
	set_process(true)
	queue_redraw()


func _build_touch_button() -> void:
	if touch_button != null:
		touch_button.queue_free()
	touch_button = Button.new()
	touch_button.name = "ObjectTouchTarget"
	touch_button.flat = true
	touch_button.focus_mode = Control.FOCUS_NONE
	touch_button.mouse_filter = Control.MOUSE_FILTER_STOP
	touch_button.position = object_center - hit_size * 0.5
	touch_button.size = hit_size
	touch_button.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
	touch_button.set_meta("station_index", station_index)
	touch_button.set_meta("physical_object", true)
	touch_button.pressed.connect(_emit_pressed)
	add_child(touch_button)


func configure_object(texture_path: String, animation_kind: String,
		visual_size: Vector2) -> void:
	source_path = texture_path
	motion = animation_kind if not animation_kind.is_empty() else "breathe"
	object_size = visual_size
	object_texture = load(texture_path) as Texture2D \
		if not texture_path.is_empty() and ResourceLoader.exists(texture_path) else null
	set_meta("source_path", source_path)
	set_meta("motion", motion)
	queue_redraw()


func set_armed(value: bool) -> void:
	armed = value
	visible = value
	focused = false
	opening = false
	opening_t = 0.0
	if touch_button != null:
		touch_button.disabled = not value
	queue_redraw()


func set_focused(value: bool) -> void:
	if not armed:
		return
	focused = value
	queue_redraw()


func play_opening() -> void:
	if not armed or opening:
		return
	focused = true
	opening = true
	opening_t = 0.0
	activation_count += 1
	if touch_button != null:
		touch_button.disabled = true
	queue_redraw()


func restart_invitation() -> void:
	if not armed or opening:
		return
	elapsed = 0.0
	focused = true
	queue_redraw()


func _emit_pressed() -> void:
	if armed and not opening:
		pressed.emit(station_index)


func _process(delta: float) -> void:
	if not armed:
		return
	elapsed += delta
	if opening:
		opening_t += delta
		if opening_t >= OPENING_SECONDS:
			opening = false
			opening_t = OPENING_SECONDS
			opening_finished.emit(station_index)
	queue_redraw()


func _draw() -> void:
	if not armed:
		return
	var opening_amount := clampf(opening_t / OPENING_SECONDS, 0.0, 1.0)
	var focus_amount := 1.0 if focused or opening else 0.0
	var pulse_speed := Affordance.pulse_speed(Affordance.PLOT, focus_amount > 0.5)
	var wave := sin(elapsed * pulse_speed)
	var halo_color := Affordance.color(Affordance.PLOT, focus_amount > 0.5)
	halo_color.a *= lerpf(0.76, 1.0, wave * 0.5 + 0.5)
	var halo_radius := maxf(object_size.x, object_size.y) * 0.62
	var halo_pulse := 1.0 + wave * Affordance.pulse_amount(
		Affordance.PLOT, focus_amount > 0.5)
	if opening:
		halo_pulse += sin(opening_amount * PI) * 0.28
	_draw_halo(halo_radius * halo_pulse, halo_color, opening_amount)
	_draw_object(wave, opening_amount)
	_draw_sparkles(halo_radius, opening_amount)


func _draw_halo(radius: float, colour: Color, opening_amount: float) -> void:
	var soft := Color(colour, colour.a * 0.18)
	draw_circle(object_center, radius * 1.16, soft)
	draw_arc(object_center, radius, 0.0, TAU, 48,
		Color(colour, colour.a * 0.86), 5.0)
	draw_arc(object_center, radius * 0.78, -PI * 0.65 + elapsed * 0.22,
		PI * 0.72 + elapsed * 0.22, 30,
		Color(Affordance.sparkle_color(Affordance.PLOT), 0.52), 3.0)
	if opening_amount > 0.0:
		draw_arc(object_center, radius * lerpf(0.62, 1.48, opening_amount),
			0.0, TAU, 48, Color(1.0, 0.94, 0.70, 1.0 - opening_amount), 7.0)


func _draw_object(wave: float, opening_amount: float) -> void:
	var object_transform: Dictionary = _object_transform(wave, opening_amount)
	var object_scale: Vector2 = object_transform.get("scale", Vector2.ONE) as Vector2
	var object_offset: Vector2 = object_transform.get("offset", Vector2.ZERO) as Vector2
	var object_rotation := float(object_transform.get("rotation", 0.0))
	var draw_size := object_size * object_scale
	draw_set_transform(object_center + object_offset,
		object_rotation, Vector2.ONE)
	var local_rect := Rect2(-draw_size * 0.5, draw_size)
	if object_texture != null:
		draw_texture_rect(object_texture, local_rect, false,
			Color(1.0, 1.0, 1.0, lerpf(0.94, 1.0, opening_amount)))
	else:
		# Asset-safe fallback: a pearl activity token, never a clipboard/easel.
		draw_circle(Vector2.ZERO, minf(draw_size.x, draw_size.y) * 0.34,
			Color("#fff4cf"))
		draw_arc(Vector2.ZERO, minf(draw_size.x, draw_size.y) * 0.34,
			0.0, TAU, 32, Color("#d89332"), 7.0)
		draw_circle(Vector2(-draw_size.x * 0.08, -draw_size.y * 0.08),
			minf(draw_size.x, draw_size.y) * 0.08, Color.WHITE)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _object_transform(wave: float, opening_amount: float) -> Dictionary:
	var scale_amount := 1.0 + wave * 0.025
	var rotation_amount := 0.0
	var offset := Vector2(0.0, -absf(wave) * 3.0)
	match motion:
		"spin":
			rotation_amount = elapsed * (0.28 if not opening else 2.6)
		"rock":
			rotation_amount = wave * (0.07 if not opening else 0.18)
		"tilt", "pour":
			rotation_amount = -0.08 + wave * 0.055 - opening_amount * 0.22
		"bounce":
			offset.y -= absf(sin(elapsed * 2.7)) * (7.0 + opening_amount * 9.0)
		"shake":
			offset.x += sin(elapsed * (7.0 if not opening else 18.0)) \
				* (2.5 + opening_amount * 4.0)
		"slide":
			offset.x += wave * (5.0 + opening_amount * 7.0)
		"pulse":
			scale_amount += wave * 0.035
		_:
			pass
	if opening:
		scale_amount += sin(opening_amount * PI) * 0.16
	return {
		"scale": Vector2.ONE * scale_amount,
		"rotation": rotation_amount,
		"offset": offset,
	}


func _draw_sparkles(radius: float, opening_amount: float) -> void:
	var sparkle := Affordance.sparkle_color(Affordance.PLOT)
	for index in range(5):
		var phase := elapsed * (0.48 + float(index) * 0.035) \
			+ float(index) * TAU / 5.0
		var orbit := radius * (0.84 + float(index % 2) * 0.16)
		var point := object_center + Vector2.from_angle(phase) * orbit
		var strength := 0.38 + 0.36 * (sin(phase * 2.0) * 0.5 + 0.5)
		strength = clampf(strength + opening_amount * 0.38, 0.0, 1.0)
		var arm := 3.0 + strength * 5.0
		draw_line(point - Vector2(arm, 0.0), point + Vector2(arm, 0.0),
			Color(sparkle, strength), 2.5)
		draw_line(point - Vector2(0.0, arm), point + Vector2(0.0, arm),
			Color(sparkle, strength), 2.5)


func stage_hit_rect() -> Rect2:
	return Rect2(position + object_center - hit_size * 0.5, hit_size)


func stage_glow_rect() -> Rect2:
	var radius := maxf(object_size.x, object_size.y) * 0.76
	return Rect2(position + object_center - Vector2.ONE * radius,
		Vector2.ONE * radius * 2.0)


func animation_state() -> Dictionary:
	return {
		"station_index": station_index,
		"station_id": station_id,
		"source_path": source_path,
		"motion": motion,
		"armed": armed,
		"focused": focused,
		"opening": opening,
		"opening_t": opening_t,
		"activation_count": activation_count,
		"hit_rect": stage_hit_rect(),
		"glow_rect": stage_glow_rect(),
	}
