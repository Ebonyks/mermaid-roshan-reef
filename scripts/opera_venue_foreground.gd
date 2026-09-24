class_name OperaVenueForeground
extends Control
## Source-owned scene pieces. Replace a body with its piece-removed state
## before moving that exact piece; never layer an unrelated icon over it. The semantic signals/sockets are the animation-bible
## integration boundary; current poses reuse approved Roshan atlas rows only.

signal animation_requested(action: StringName, phase: StringName, context: Dictionary)
signal interaction_finished(object_id: StringName)

const ROOT := "res://assets/flats/castle/opera_house_four_floors/physical/"
const MAX_PARTICLES := 6
const OBJECTS := {
	"flowers": {"art": "flower_stand", "rect": Rect2(0.00000, 402.46546, 127.08134, 179.04357),
		"hit": Rect2(0, 416, 145, 140), "approach": Vector2(172, 529),
		"source": Vector2(72, 512), "action": "flower"},
	"snacks": {"art": "snack_stand", "rect": Rect2(0.00000, 531.77471, 163.06220, 186.69501),
		"hit": Rect2(0, 565, 161, 155), "approach": Vector2(174, 695),
		"source": Vector2(110, 627), "action": "cupcake"},
	"left_couch": {"art": "left_couch", "rect": Rect2(159.23445, 526.41870, 228.89952, 128.54410),
		"hit": Rect2(168, 542, 207, 111), "approach": Vector2(395, 631),
		"seat": Vector2(272, 592), "action": "sit"},
	"planter": {"art": "planter", "rect": Rect2(565.74163, 534.83528, 145.45455, 142.31668),
		"hit": Rect2(574, 535, 150, 141), "approach": Vector2(552, 648),
		"seat": Vector2(640, 649), "action": "sit"},
	"right_couch": {"art": "right_couch", "rect": Rect2(891.10048, 528.71413, 224.30622, 126.24867),
		"hit": Rect2(919, 542, 204, 116), "approach": Vector2(882, 629),
		"seat": Vector2(1020, 592), "action": "sit"},
	"lemonade": {"art": "drinks_cart", "rect": Rect2(1133.01435, 419.29862, 146.98565, 199.70244),
		"hit": Rect2(1130, 470, 150, 154), "approach": Vector2(1137, 644),
		"source": Vector2(1192, 524), "action": "lemonade"},
}
const CLIPS := {
	"reach": {"sheet": "gesture_b", "row": 3},
	"collect": {"sheet": "gesture_c", "row": 0},
	"carry": {"sheet": "gesture_d", "row": 1},
	"sit": {"sheet": "play_b", "row": 2},
}

class Effects:
	extends Node2D
	var owner_layer: OperaVenueForeground
	func _draw() -> void:
		owner_layer.paint_effects(self)

var venue: OperaHouseVenue2D
var hit_targets: Dictionary = {}
var art_nodes: Dictionary = {}
var textures: Dictionary = {}
var pose_sheets: Dictionary = {}
var effects: Effects
var actor_offset := Vector2.ZERO
var active_object := ""
var action := ""
var phase := ""
var clock := 0.0
var seated := false
var held_texture: Texture2D
var held_point := Vector2.ZERO
var held_size := Vector2.ZERO
var liquid_start := Vector2.ZERO
var liquid_end := Vector2.ZERO
var particles: Array[Dictionary] = []
var default_actor_texture: Texture2D
var pose_frame := AtlasTexture.new()
var event_serial := 0
var parts: Dictionary = {}
var bodies: Dictionary = {}
var body_states: Dictionary = {}
var held_card: TextureRect
var jug_card: TextureRect
var cake_eaten := false
var liquid_fraction := 0.0
var current_piece := ""


func setup(host: OperaHouseVenue2D) -> void:
	venue = host
	name = "OperaInteractiveForeground"
	size = OperaHouseVenue2D.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 3
	set_meta("background_ownership", "removed_from_clean_plate")
	default_actor_texture = venue.actor.texture
	parts = JSON.parse_string(FileAccess.get_file_as_string(ROOT + "parts.json")) as Dictionary
	for key: String in ["flower", "flower_core", "cup", "pitcher", "cupcake", "cupcake_bite_1", "cupcake_bite_2"]:
		textures[key] = load(ROOT + key + ".png") as Texture2D
	for i in range(MAX_PARTICLES):
		textures["petal_%d" % i] = load(ROOT + "flower_petal_%d.png" % i) as Texture2D
	for key: String in CLIPS:
		var clip: Dictionary = CLIPS[key]
		pose_sheets[key] = load("res://assets/characters/roshan_25d/roshan_%s.png" % String(clip["sheet"])) as Texture2D
	for id: String in OBJECTS:
		var spec: Dictionary = OBJECTS[id]
		var rect: Rect2 = spec["rect"]
		var texture := load(ROOT + String(spec["art"]) + "_0.png") as Texture2D
		var back := _art(texture, rect, id + "Back")
		art_nodes[id] = back
		body_states[id] = 0
		var variants: Array[Texture2D] = [texture]
		for state in range(1, 4 if id == "lemonade" else (2 if id in ["flowers", "snacks"] else 1)):
			variants.append(load(ROOT + String(spec["art"]) + "_%d.png" % state) as Texture2D)
		bodies[id] = variants
		if String(spec["action"]) == "sit" and texture != null:
			# Split the same image into disjoint back/front regions so the cushion
			# and seat edge can occlude Roshan without drawing its pixels twice.
			var cut := int(float(texture.get_height()) * 0.57)
			var upper := AtlasTexture.new()
			upper.atlas = texture
			upper.region = Rect2(0, 0, texture.get_width(), cut)
			back.texture = upper
			back.size.y = rect.size.y * float(cut) / float(texture.get_height())
			var lower := AtlasTexture.new()
			lower.atlas = texture
			lower.region = Rect2(0, cut, texture.get_width(), texture.get_height() - cut)
			var front := _art(lower, Rect2(rect.position + Vector2(0, back.size.y),
				Vector2(rect.size.x, rect.size.y - back.size.y)), id + "Front")
			front.z_index = 8
		var button := Button.new()
		button.name = id + "Interaction"
		var hit: Rect2 = spec["hit"]
		button.position = hit.position
		button.size = hit.size
		button.text = ""
		button.z_index = 20
		button.tooltip_text = id.replace("_", " ")
		button.set_meta("interaction_id", id)
		button.set_meta("touch_target", true)
		for state: String in ["normal", "hover", "pressed", "disabled", "focus"]:
			button.add_theme_stylebox_override(state, StyleBoxEmpty.new())
		button.pressed.connect(venue.request_foreground.bind(id))
		add_child(button)
		hit_targets[id] = button
	effects = Effects.new()
	effects.owner_layer = self
	effects.z_index = 15
	add_child(effects)
	held_card = _art(null, Rect2(), "ActualHeldScenePiece")
	held_card.z_index = 15
	held_card.visible = false
	jug_card = _art(textures["pitcher"] as Texture2D, _part_rect("pitcher"), "ActualCartPitcher")
	jug_card.z_index = 14
	jug_card.visible = false
	effects.z_index = 16
	set_process(false)


func _art(texture: Texture2D, rect: Rect2, node_name: String) -> TextureRect:
	var card := TextureRect.new()
	card.name = node_name
	card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	card.texture = texture
	card.position = rect.position
	card.size = rect.size
	card.stretch_mode = TextureRect.STRETCH_SCALE
	card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.set_meta("source_role", "foreground_only")
	add_child(card)
	return card


func reset_scene() -> void:
	cancel(true)
	cake_eaten = false
	_body("snacks", 0)


func begin(id: String) -> void:
	if not OBJECTS.has(id) or not venue.accepting_input or venue.floor_index != 0:
		return
	if id == "snacks" and cake_eaten:
		return
	cancel()
	active_object = id
	var spec: Dictionary = OBJECTS[id]
	action = String(spec["action"])
	current_piece = {"flower": "flower", "cupcake": "cupcake", "lemonade": "cup"}.get(action, "")
	# The approved carry frame faces LEFT in the atlas. Mirror it only when
	# the physical target is to Roshan's right, including the lemonade cart.
	var target: Vector2 = spec.get("seat", venue.foot) if current_piece.is_empty() else _part_rect(current_piece).get_center()
	venue.actor.flip_h = target.x > venue.foot.x
	clock = 0.0
	event_serial += 1
	venue.guide_pointer.visible = false
	venue.m._say("roshan", "castle_cosy_seat" if action == "sit" else "talk", 5.0)
	_set_phase("sit" if action == "sit" else "reach")


func cancel(immediate: bool = false) -> void:
	if not active_object.is_empty():
		animation_requested.emit(StringName(action), &"cancel", socket_context())
	_body("flowers", 0)
	_body("lemonade", 0)
	_body("snacks", 1 if cake_eaten else 0)
	active_object = ""
	action = ""
	current_piece = ""
	phase = ""
	clock = 0.0
	seated = false
	held_texture = null
	particles.clear()
	liquid_start = Vector2.ZERO
	liquid_end = Vector2.ZERO
	liquid_fraction = 0.0
	if held_card != null:
		held_card.visible = false
		jug_card.visible = false
	if immediate:
		actor_offset = Vector2.ZERO
	venue.actor.texture = default_actor_texture
	venue.actor.flip_h = false
	venue.actor.remove_meta("opera_interaction_pose")
	venue.actor.remove_meta("animation_bible_action")
	if effects != null:
		effects.queue_redraw()


func _body(id: String, state: int) -> void:
	if not bodies.has(id) or int(body_states[id]) == state:
		return
	body_states[id] = state
	(art_nodes[id] as TextureRect).texture = (bodies[id] as Array)[state] as Texture2D


func _part_rect(key: String) -> Rect2:
	var values: Array = (parts[key] as Dictionary)["source_rect"]
	return Rect2(float(values[0]), float(values[1]), float(values[2]), float(values[3]))


func _hand_fraction() -> Vector2:
	return Vector2(0.74 if venue.actor.flip_h else 0.26, 0.36)


func _mouth_fraction() -> Vector2:
	return Vector2(0.54 if venue.actor.flip_h else 0.46, 0.30)


func _contact_offset() -> Vector2:
	return _part_rect(current_piece).get_center() - (venue.foot
		- Vector2(OperaHouseVenue2D.ACTOR_SIZE.x * 0.5, OperaHouseVenue2D.ACTOR_SIZE.y)
		+ OperaHouseVenue2D.ACTOR_SIZE * _hand_fraction())


func tick(delta: float) -> void:
	if active_object.is_empty():
		actor_offset = actor_offset.move_toward(Vector2.ZERO, delta * 350.0)
		effects.queue_redraw()
		return
	clock += delta
	liquid_start = Vector2.ZERO
	liquid_end = Vector2.ZERO
	if action == "sit":
		var seat: Vector2 = (OBJECTS[active_object] as Dictionary)["seat"]
		actor_offset = (seat - venue.foot) * _smooth(clock / 0.65)
		_pose("sit")
		if clock >= 0.65:
			seated = true
			_set_phase("seated")
	elif clock < 0.7:
		# Mermaid swims into contact; the object never flies across the room.
		actor_offset = _contact_offset() * _smooth(clock / 0.7)
		# Keep the same authored palm socket through contact and pickup.
		_pose("carry")
	else:
		match action:
			"flower": _flower_tick()
			"cupcake": _cake_tick()
			"lemonade": _drink_tick()
	effects.queue_redraw()


func _flower_tick() -> void:
	_body("flowers", 1)
	_pose("carry")
	if clock < 1.4:
		_set_phase("pick")
		actor_offset = _contact_offset() * (1.0 - _smooth((clock - 0.7) / 0.7))
		_hold("flower", _actor_socket(_hand_fraction()))
	elif clock < 3.8:
		if phase != "hold":
			particles.clear()
			for i in range(MAX_PARTICLES):
				var angle := float(i) * TAU / float(MAX_PARTICLES)
				particles.append({"piece": i, "velocity": Vector2(cos(angle) * (45.0 + i * 8.0), -55.0 - i * 9.0)})
		_set_phase("hold")
		_hold("flower_core", _actor_socket(_hand_fraction()))
	elif clock < 4.5:
		particles.clear()
		_set_phase("return")
		actor_offset = _contact_offset() * _smooth((clock - 3.8) / 0.7)
		_hold("flower", _actor_socket(_hand_fraction()))
	else:
		_body("flowers", 0)
		_finish()


func _cake_tick() -> void:
	_body("snacks", 1)
	_pose("carry")
	if clock < 1.4:
		_set_phase("pick_cupcake")
		actor_offset = _contact_offset() * (1.0 - _smooth((clock - 0.7) / 0.7))
		_hold("cupcake", _actor_socket(_hand_fraction()))
	elif clock < 2.1:
		_set_phase("lift_cupcake")
		_hold("cupcake", _actor_socket(_hand_fraction()).lerp(_actor_socket(_mouth_fraction()), _smooth((clock - 1.4) / 0.7)))
	elif clock < 3.4:
		_set_phase("bite")
		_hold("cupcake_bite_1" if clock < 2.75 else "cupcake_bite_2", _actor_socket(_mouth_fraction()))
	else:
		cake_eaten = true
		_finish()


func _drink_tick() -> void:
	_body("lemonade", 1)
	_pose("carry")
	if clock < 1.3:
		_set_phase("pick_cup")
		actor_offset = _contact_offset() + Vector2(-5, 6) * _smooth((clock - 0.7) / 0.6)
		_hold("cup", _actor_socket(_hand_fraction()))
	elif clock < 2.7:
		_set_phase("fill")
		_body("lemonade", 3)
		_hold("cup", _actor_socket(_hand_fraction()))
		var rect := _part_rect("pitcher")
		jug_card.visible = true
		jug_card.position = rect.position
		jug_card.size = rect.size
		jug_card.pivot_offset = rect.size * Vector2(0.42, 0.9)
		jug_card.rotation = -0.3 * sin(clampf((clock - 1.3) / 1.4, 0.0, 1.0) * PI)
		liquid_fraction = clampf((clock - 1.45) / 1.1, 0.0, 1.0)
		if clock > 1.5 and clock < 2.5:
			liquid_start = jug_card.position + jug_card.pivot_offset + (rect.size * Vector2(0.14, 0.1) - jug_card.pivot_offset).rotated(jug_card.rotation)
			liquid_end = held_point - Vector2(0, held_size.y * 0.24)
	elif clock < 3.4:
		_set_phase("lift_cup")
		jug_card.visible = false
		actor_offset = (_contact_offset() + Vector2(-5, 6)) * (1.0 - _smooth((clock - 2.7) / 0.7))
		_hold("cup", _actor_socket(_hand_fraction()))
	elif clock < 4.7:
		_set_phase("drink")
		_hold("cup", _actor_socket(_hand_fraction()).lerp(_actor_socket(_mouth_fraction()), _smooth((clock - 3.4) / 0.5)))
		liquid_fraction = 1.0 - _smooth((clock - 3.9) / 0.7)
	elif clock < 5.4:
		_set_phase("return_cup")
		actor_offset = _contact_offset() * _smooth((clock - 4.7) / 0.7)
		_hold("cup", _actor_socket(_hand_fraction()))
	else:
		_body("lemonade", 0)
		_finish()


func _set_phase(next: String) -> void:
	if phase == next:
		return
	phase = next
	venue.actor.set_meta("animation_bible_action", action + "." + phase)
	animation_requested.emit(StringName(action), StringName(phase), socket_context())


func socket_context() -> Dictionary:
	var spec: Dictionary = OBJECTS.get(active_object, {})
	return {"object_id": active_object, "serial": event_serial,
		"approach": spec.get("approach", venue.foot),
		"prop_origin": _part_rect(current_piece).get_center() if not current_piece.is_empty() else venue.foot,
		"seat": spec.get("seat", venue.foot), "hand": _actor_socket(_hand_fraction()),
		"mouth": _actor_socket(_mouth_fraction()), "facing": "right" if venue.actor.flip_h else "left", "space": "opera_canvas_1280x720",
		"bible_binding": "pending_authored_interaction_clips", "physical_piece": current_piece}


func _actor_socket(normalized: Vector2) -> Vector2:
	return venue.foot - Vector2(OperaHouseVenue2D.ACTOR_SIZE.x * 0.5, OperaHouseVenue2D.ACTOR_SIZE.y) \
		+ actor_offset + OperaHouseVenue2D.ACTOR_SIZE * normalized


func _pose(key: String) -> void:
	var clip: Dictionary = CLIPS[key]
	pose_frame.atlas = pose_sheets[key] as Texture2D
	# Stable contact frame until the authored animation bible supplies sockets
	# per frame; cycling unrelated frames made props visibly slide off hands.
	pose_frame.region = Rect2(256, int(clip["row"]) * 256, 256, 256)
	pose_frame.filter_clip = true
	venue.actor.texture = pose_frame
	venue.actor.set_meta("opera_interaction_pose", key)


func _hold(key: String, point: Vector2) -> void:
	held_texture = textures[key] as Texture2D
	held_point = point
	held_size = _part_rect(current_piece).size
	held_card.texture = held_texture
	held_card.position = point - held_size * 0.5
	held_card.size = held_size
	held_card.visible = true


func _finish() -> void:
	var completed := active_object
	_set_phase("release")
	active_object = ""
	action = ""
	current_piece = ""
	held_texture = null
	held_card.visible = false
	jug_card.visible = false
	particles.clear()
	venue.actor.texture = default_actor_texture
	venue.actor.flip_h = false
	venue.actor.remove_meta("opera_interaction_pose")
	venue.actor.remove_meta("animation_bible_action")
	interaction_finished.emit(StringName(completed))


func paint_effects(canvas: Node2D) -> void:
	if liquid_end != Vector2.ZERO:
		canvas.draw_line(liquid_start, liquid_end, Color(0.86, 0.56, 0.16, 0.8), 1.4, true)
	if action == "lemonade" and held_card.visible and liquid_fraction > 0.0:
		# Liquid is confined to this same cup's opening, never a second cup icon.
		var rim := held_point - Vector2(0, held_size.y * 0.22)
		canvas.draw_line(rim - Vector2(held_size.x * 0.23, 0), rim + Vector2(held_size.x * 0.23, 0), Color(0.86, 0.56, 0.16, liquid_fraction), 1.6, true)
	if action == "flower" and phase == "hold":
		var age := clock - 1.4
		var rejoin := 1.0 - _smooth((age - 1.3) / 1.1)
		for particle: Dictionary in particles:
			var velocity: Vector2 = particle["velocity"]
			var offset := (velocity * age + Vector2(0, 42) * age * age) * rejoin
			var texture := textures["petal_%d" % int(particle["piece"])] as Texture2D
			canvas.draw_texture_rect(texture, Rect2(held_point + offset - held_size * 0.5, held_size), false)


func _smooth(value: float) -> float:
	return smoothstep(0.0, 1.0, clampf(value, 0.0, 1.0))
