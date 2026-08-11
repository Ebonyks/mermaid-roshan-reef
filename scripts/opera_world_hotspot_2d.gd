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
const STAGE_SIZE := Vector2(1280.0, 720.0)

var station_index := -1
var station_id := ""
var source_path := ""
var motion := "breathe"
var presentation := "overlay"
var object_texture: Texture2D = null
var object_size := Vector2(124.0, 124.0)
var visual_offset := Vector2.ZERO
var hit_size := MIN_TOUCH
var object_center := DEFAULT_ENVELOPE * 0.5
var authored_stage_pos := STAGE_SIZE * 0.5
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
		authored_hit_size: Vector2 = MIN_TOUCH,
		presentation_kind := "overlay",
		display_offset := Vector2.ZERO) -> void:
	station_index = index
	station_id = id
	source_path = texture_path
	motion = animation_kind if not animation_kind.is_empty() else "breathe"
	presentation = _valid_presentation(presentation_kind)
	object_size = visual_size
	visual_offset = display_offset
	authored_stage_pos = stage_object_pos
	hit_size = Vector2(
		maxf(MIN_TOUCH.x, authored_hit_size.x),
		maxf(MIN_TOUCH.y, authored_hit_size.y))
	var envelope := Vector2(
		maxf(DEFAULT_ENVELOPE.x, hit_size.x + 72.0),
		maxf(DEFAULT_ENVELOPE.y, hit_size.y + 72.0))
	size = envelope
	object_center = envelope * 0.5
	_reframe_to_stage()
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = false
	object_texture = load(texture_path) as Texture2D \
		if not texture_path.is_empty() and ResourceLoader.exists(texture_path) else null
	_build_touch_button()
	set_meta("station_index", station_index)
	set_meta("station_id", station_id)
	set_meta("source_path", source_path)
	set_meta("motion", motion)
	set_meta("presentation", presentation)
	set_meta("visual_offset", visual_offset)
	set_meta("affordance_kind", Affordance.INTERACTION)
	set_meta("object_pos", stage_object_pos)
	set_meta("visual_pos", position + object_center)
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
		visual_size: Vector2, presentation_kind := "overlay",
		display_offset := Vector2.ZERO) -> void:
	source_path = texture_path
	motion = animation_kind if not animation_kind.is_empty() else "breathe"
	presentation = _valid_presentation(presentation_kind)
	object_size = visual_size
	visual_offset = display_offset
	object_texture = load(texture_path) as Texture2D \
		if not texture_path.is_empty() and ResourceLoader.exists(texture_path) else null
	_reframe_to_stage()
	set_meta("source_path", source_path)
	set_meta("motion", motion)
	set_meta("presentation", presentation)
	set_meta("visual_offset", visual_offset)
	set_meta("visual_pos", position + object_center)
	queue_redraw()


func _reframe_to_stage() -> void:
	# Edge landmarks remain the authored target, but their invitation cutout and
	# complete opening halo shift just far enough inward to stay fully visible.
	var glow_margin := maxf(
		maxf(hit_size.x, hit_size.y) * 0.5 + 4.0,
		_glow_extent())
	var intended_center := authored_stage_pos + visual_offset
	var safe_center := Vector2(
		clampf(intended_center.x, glow_margin, STAGE_SIZE.x - glow_margin),
		clampf(intended_center.y, glow_margin, STAGE_SIZE.y - glow_margin))
	position = safe_center - object_center


func _halo_basis() -> float:
	# Area-based sizing keeps a wide ribbon or lane from acquiring an enormous
	# circular glow while leaving square props as prominent as before.
	return maxf(88.0, sqrt(maxf(object_size.x * object_size.y, 1.0)))


func _glow_extent() -> float:
	return maxf(maxf(object_size.x, object_size.y) * 0.56,
		_halo_basis() * 1.28)


func set_armed(value: bool) -> void:
	armed = value
	visible = value
	if value:
		elapsed = 0.0
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
	var pulse_speed := Affordance.pulse_speed(Affordance.INTERACTION, focus_amount > 0.5)
	var wave := sin(elapsed * pulse_speed)
	var halo_color := Affordance.color(Affordance.INTERACTION, focus_amount > 0.5)
	halo_color.a *= lerpf(0.76, 1.0, wave * 0.5 + 0.5)
	var halo_radius := _halo_basis() * 0.62
	var halo_pulse := 1.0 + wave * Affordance.pulse_amount(
		Affordance.INTERACTION, focus_amount > 0.5)
	if opening:
		halo_pulse += sin(opening_amount * PI) * 0.28
	if presentation == "painted":
		_draw_painted_landmark(wave, opening_amount)
	_draw_halo(halo_radius * halo_pulse, halo_color, opening_amount)
	if presentation != "painted":
		_draw_object(wave, opening_amount)
	_draw_sparkles(halo_radius, opening_amount)


func _valid_presentation(value: String) -> String:
	if value in ["overlay", "effect", "painted"]:
		return value
	return "overlay"


func _draw_painted_landmark(wave: float, opening_amount: float) -> void:
	# Some approved room paintings already contain the exact work object. In
	# that case another cutout would create a duplicate subject. Animate a local
	# theatre-light focus over the painted landmark instead: the landmark stays
	# diegetic while its invitation remains unmistakably alive.
	var half_size := object_size * 0.5
	var radius := maxf(32.0, minf(half_size.x, half_size.y))
	var aspect := Vector2(
		maxf(1.0, half_size.x / radius),
		maxf(1.0, half_size.y / radius))
	var shimmer := 1.0 + wave * 0.035 + sin(opening_amount * PI) * 0.12
	var cue_rotation := elapsed * 0.08
	var cue_offset := Vector2.ZERO
	match motion:
		"spin":
			cue_rotation = elapsed * (0.54 if not opening else 1.9)
		"rock":
			cue_rotation = wave * (0.045 if not opening else 0.09)
		"tilt", "pour":
			cue_rotation = -0.08 + wave * 0.035 - opening_amount * 0.10
		"bounce":
			cue_offset.y -= absf(sin(elapsed * 2.7)) * 6.0
		"shake":
			cue_offset.x += sin(elapsed * 8.0) * 3.0
		"slide":
			cue_offset.x += wave * 6.0
		"pulse":
			shimmer += wave * 0.045
	draw_set_transform(object_center + cue_offset, cue_rotation,
		aspect * shimmer)
	draw_circle(Vector2.ZERO, radius * 0.88,
		Color(0.18, 0.86, 0.96, 0.08 + opening_amount * 0.08))
	draw_arc(Vector2.ZERO, radius * 0.82,
		-PI * 0.72 + elapsed * 0.32,
		PI * 0.46 + elapsed * 0.32, 30,
		Color(0.74, 0.98, 1.0, 0.72), 3.0)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_halo(radius: float, colour: Color, opening_amount: float) -> void:
	var soft := Color(colour, colour.a * 0.18)
	draw_circle(object_center, radius * 1.16, soft)
	draw_arc(object_center, radius, 0.0, TAU, 48,
		Color(colour, colour.a * 0.86), 5.0)
	draw_arc(object_center, radius * 0.78, -PI * 0.65 + elapsed * 0.22,
		PI * 0.72 + elapsed * 0.22, 30,
		Color(Affordance.sparkle_color(Affordance.INTERACTION), 0.52), 3.0)
	if opening_amount > 0.0:
		draw_arc(object_center, radius * lerpf(0.62, 1.48, opening_amount),
			0.0, TAU, 48, Color(1.0, 0.94, 0.70, 1.0 - opening_amount), 7.0)


func _draw_object(wave: float, opening_amount: float) -> void:
	var object_transform: Dictionary = _object_transform(wave, opening_amount)
	var object_scale: Vector2 = object_transform.get("scale", Vector2.ONE) as Vector2
	var object_offset: Vector2 = object_transform.get("offset", Vector2.ZERO) as Vector2
	var object_rotation := float(object_transform.get("rotation", 0.0))
	var draw_size := object_size * object_scale
	# A soft object-local contact shadow stops bottles, tools, food and babies
	# from reading as pasted stickers in the open room. It stays horizontal even
	# while the prop itself rocks, pours or spins.
	var shadow_width := maxf(24.0, minf(draw_size.x * 0.36, 66.0))
	draw_set_transform(object_center
		+ Vector2(object_offset.x, object_size.y * 0.43),
		0.0, Vector2(1.0, 0.30))
	draw_circle(Vector2.ZERO, shadow_width,
		Color(0.05, 0.08, 0.22, 0.22 + opening_amount * 0.08))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
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
	match motion if presentation != "effect" else "pulse":
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
	var sparkle := Affordance.sparkle_color(Affordance.INTERACTION)
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


func stage_object_rect() -> Rect2:
	# Painted landmarks draw no duplicate prop, and low-alpha local effects are
	# allowed to wash over Roshan (bubbles are the clearest example). Only a
	# solid overlay cutout participates in physical visual-overlap QA.
	if presentation != "overlay":
		return Rect2()
	# The maximum 1.16 opening scale is included so QA can reject actual
	# actor/prop collisions before they become visible in a room capture.
	var visual_size := _maximum_visual_size()
	return Rect2(position + object_center - visual_size * 0.5, visual_size)


func _maximum_visual_size() -> Vector2:
	var scaled := object_size * 1.16
	var maximum_angle := 0.0
	if presentation == "overlay":
		match motion:
			"spin":
				maximum_angle = PI * 0.25
			"rock":
				maximum_angle = 0.18
			"tilt", "pour":
				maximum_angle = 0.30
	var cosine := absf(cos(maximum_angle))
	var sine := absf(sin(maximum_angle))
	var result := Vector2(
		scaled.x * cosine + scaled.y * sine,
		scaled.x * sine + scaled.y * cosine)
	match motion:
		"bounce":
			result.y += 32.0
		"shake":
			result.x += 14.0
		"slide":
			result.x += 24.0
	return result


func stage_glow_rect() -> Rect2:
	var radius := _glow_extent()
	return Rect2(position + object_center - Vector2.ONE * radius,
		Vector2.ONE * radius * 2.0)


func animation_state() -> Dictionary:
	return {
		"station_index": station_index,
		"station_id": station_id,
		"source_path": source_path,
		"motion": motion,
		"presentation": presentation,
		"visual_offset": visual_offset,
		"armed": armed,
		"focused": focused,
		"opening": opening,
		"opening_t": opening_t,
		"activation_count": activation_count,
		"authored_object_pos": authored_stage_pos,
		"visual_object_pos": position + object_center,
		"hit_rect": stage_hit_rect(),
		"object_rect": stage_object_rect(),
		"glow_rect": stage_glow_rect(),
	}
