class_name OperaNurseryCatch
extends Control
## One-finger falling-baby phase for Pearl Opera job #12.
##
## This keeps the proven dolls-game grammar (move under a gently falling baby,
## live-input verb gate, pillow-safe misses, escalating mercy) while expanding
## it to five catches, two simultaneous fallers, three authored baby sprites,
## a visible cradle, and Faron's safe-return loop. A miss can lower applause,
## but can never lose a baby or end the job.

signal baby_caught(quality: float)
signal baby_missed()

const BABY_PATHS: Array[String] = [
	"res://assets/opera/worlds/nursery/baby_0.png",
	"res://assets/opera/worlds/nursery/baby_1.png",
	"res://assets/opera/worlds/nursery/baby_2.png",
]
const SPAWN_LANES: Array[float] = [0.17, 0.50, 0.83, 0.32, 0.68, 0.22, 0.77]
const CATCH_Y := 0.64
const PILLOW_Y := 0.84
const INPUT_MEMORY := 2.0
const DRAWS_CARD_BACKING := false
const PALM_UV := Vector2(0.50, 0.675)
const HOLD_SECONDS := 0.22
const TRANSFER_SECONDS := 0.65

var active := false
var goal := 5
var caught := 0
var missed := 0
var spawned := 0
var elapsed := 0.0
var spawn_t := 0.0
var input_live_t := 0.0
var catcher_x := 0.5
var touch_index := -1
var mouse_held := false
var fallers: Array[Dictionary] = []
var safe_landings: Array[Dictionary] = []
var settled: Array[int] = []
var transfers: Array[Dictionary] = []
var textures: Array[Texture2D] = []
var baby_feet: Array[Vector2] = []
var backdrop_texture: Texture2D = null
var retired_backdrop_path := ""
var cradle_texture: Texture2D = null
var pillows_texture: Texture2D = null
var cushion_surface_rows: Array[int] = []
var care: OperaNurseryCare = null


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	# Keep the path as audit evidence, but never paint the framed legacy card.
	retired_backdrop_path = "res://assets/opera/worlds/widgets/widget_catch_nursery.png"
	backdrop_texture = null
	cradle_texture = _load_if_exists("res://assets/opera/worlds/nursery/refinement_v1/cradle.png")
	var pads := AtlasTexture.new()
	pads.atlas = _load_if_exists("res://assets/opera/worlds/nursery/refinement_v1/pillows.png")
	pads.region = Rect2(6, 115, 1014, 117)
	pillows_texture = pads if pads.atlas != null else null
	_measure_cushion_surface()
	var body := OperaNurseryCare.new()
	if body.setup():
		care = body
	for path: String in BABY_PATHS:
		var texture := load(path) as Texture2D
		if texture != null:
			textures.append(texture)
			var used: Rect2i = texture.get_image().get_used_rect()
			baby_feet.append(Vector2(used.position.x + used.size.x * 0.5,
				used.end.y) / texture.get_size())
	set_meta("no_fail", true)
	set_meta("live_input_gate_seconds", INPUT_MEMORY)


func _load_if_exists(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _measure_cushion_surface() -> void:
	cushion_surface_rows.clear()
	if pillows_texture == null:
		return
	var image: Image = pillows_texture.get_image()
	if image == null or image.is_empty():
		return
	# Cache native alpha geometry once, never download texture pixels per draw.
	for column in range(image.get_width()):
		var support_row := 0
		for row in range(image.get_height()):
			if image.get_pixel(column, row).a >= 0.5:
				support_row = row
				break
		cushion_surface_rows.append(support_row)


func start(next_goal: int) -> void:
	goal = maxi(1, next_goal)
	caught = 0
	missed = 0
	spawned = 0
	elapsed = 0.0
	spawn_t = 0.18
	input_live_t = 0.0
	catcher_x = 0.5
	touch_index = -1
	mouse_held = false
	fallers.clear()
	safe_landings.clear()
	settled.clear()
	transfers.clear()
	if care != null:
		care.reset(Vector2(catcher_x * size.x, size.y * CATCH_Y))
	active = true
	set_process(true)
	queue_redraw()


func stop() -> void:
	active = false
	touch_index = -1
	mouse_held = false
	input_live_t = 0.0
	set_process(false)
	fallers.clear()
	safe_landings.clear()
	transfers.clear()
	queue_redraw()


func steer_to(normalized_x: float) -> void:
	catcher_x = clampf(normalized_x, 0.10, 0.90)
	input_live_t = INPUT_MEMORY
	queue_redraw()


func lowest_baby_x() -> float:
	var best_y := -1.0
	var best_x := -1.0
	for entry: Dictionary in fallers:
		var y := float(entry.get("y", 0.0))
		if y > best_y:
			best_y = y
			best_x = float(entry.get("x", 0.5))
	return best_x


func _set_catcher_from_local(at: Vector2) -> void:
	steer_to(at.x / maxf(1.0, size.x))


func _gui_input(event: InputEvent) -> void:
	if not active:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed and touch_index in [-1, touch.index]:
			touch_index = touch.index
			mouse_held = false
			_set_catcher_from_local(touch.position)
		elif not touch.pressed and touch.index == touch_index:
			touch_index = -1
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == touch_index:
			_set_catcher_from_local(drag.position)
		accept_event()
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if touch_index >= 0:
			# Android may also deliver mouse emulation for the owned touch. It
			# must not retarget the hand or keep an unrelated mouse hold alive.
			mouse_held = false
		elif button.pressed:
			mouse_held = true
			_set_catcher_from_local(button.position)
		else:
			mouse_held = false
		accept_event()
	elif event is InputEventMouseMotion and mouse_held and touch_index < 0:
		_set_catcher_from_local((event as InputEventMouseMotion).position)
		accept_event()


func _notification(what: int) -> void:
	if what in [NOTIFICATION_APPLICATION_PAUSED, NOTIFICATION_WM_WINDOW_FOCUS_OUT]:
		touch_index = -1
		mouse_held = false
		input_live_t = 0.0


func _spawn_baby() -> void:
	var lane := float(SPAWN_LANES[spawned % SPAWN_LANES.size()])
	if missed >= 2:
		# The dolls game steers later drops toward Roshan after two misses. Keep
		# that proven mercy contract here, with a small alternating offset so the
		# player still performs the catch instead of receiving passive progress.
		var side := -1.0 if spawned % 2 == 0 else 1.0
		lane = clampf(catcher_x + side * maxf(0.035, 0.11 - float(missed) * 0.012), 0.12, 0.88)
	var speed := maxf(0.115, 0.205 - float(missed) * 0.011)
	fallers.append({
		"base_x": lane,
		"x": lane,
		"y": -0.12,
		"speed": speed,
		"sway": 0.018 + float(spawned % 3) * 0.008,
		"phase": float(spawned) * 1.71,
		"texture": spawned % maxi(1, textures.size()),
	})
	spawned += 1


func _catch(entry: Dictionary) -> void:
	caught += 1
	settled.append(int(entry.get("texture", 0)))
	transfers.append({"slot": settled.size() - 1, "texture": int(entry.get("texture", 0)),
		"time": 0.0, "from_x": catcher_x})
	if care != null:
		transfers[-1]["hip_x"] = care.hip.x
		transfers[-1]["hip_y"] = care.hip.y
	baby_caught.emit(1.0)
	if caught >= goal:
		active = false


func _miss(entry: Dictionary) -> void:
	missed += 1
	safe_landings.append({
		"x": float(entry.get("x", 0.5)),
		"texture": int(entry.get("texture", 0)),
		"time": 1.25,
	})
	baby_missed.emit()
	spawn_t = minf(spawn_t, 0.28)


func _process(delta: float) -> void:
	for index in range(transfers.size() - 1, -1, -1):
		var transfer: Dictionary = transfers[index]
		var age: float = float(transfer["time"]) + delta
		transfer["time"] = age
		if age <= HOLD_SECONDS and care == null:
			transfer["from_x"] = catcher_x
		if care != null:
			care.transfer_pose(transfer, resting_point(int(transfer["slot"])))
		var finish: float = OperaNurseryCare.TRANSFER_TIME if care != null else HOLD_SECONDS + TRANSFER_SECONDS
		if age >= finish:
			transfers.remove_at(index)
		else:
			transfers[index] = transfer
	if not active:
		set_process(not transfers.is_empty())
		queue_redraw()
		return
	if care != null and not transfers.is_empty():
		# Helping one baby must not make another fall faster or require a second
		# finger. Hold the remaining mobile safely until this placement resolves.
		input_live_t = maxf(0.0, input_live_t - delta)
		queue_redraw()
		return
	if care != null:
		var target_x: float = catcher_x
		var nearest_y := -1.0
		for waiting: Dictionary in fallers:
			var y: float = float(waiting.get("y", 0.0))
			var x: float = float(waiting.get("x", 0.5))
			var reach := minf(0.22, 0.145 + float(missed) * 0.013)
			if input_live_t > 0.0 and y >= CATCH_Y - 0.14 and y > nearest_y \
				and absf(x - catcher_x) <= reach:
				# Existing generous intent eligibility becomes an early visible
				# hand approach. The baby keeps its actual falling lane.
				target_x = x
				nearest_y = y
		care.seek_hand(Vector2(target_x * size.x, size.y * CATCH_Y), delta)
	elapsed += delta
	input_live_t = maxf(0.0, input_live_t - delta)
	spawn_t -= delta
	var max_fallers := mini(goal - caught, 2 if caught >= 2 else 1)
	if spawn_t <= 0.0 and caught < goal and fallers.size() < max_fallers:
		_spawn_baby()
		spawn_t = maxf(0.64, 1.02 - float(caught) * 0.055)

	for index in range(fallers.size() - 1, -1, -1):
		var entry: Dictionary = fallers[index]
		entry["y"] = float(entry["y"]) + float(entry["speed"]) * delta
		entry["x"] = clampf(
			float(entry["base_x"]) + sin(elapsed * 2.2 + float(entry["phase"])) * float(entry["sway"]),
			0.08,
			0.92
		)
		fallers[index] = entry
		var catch_width := minf(0.22, 0.145 + float(missed) * 0.013)
		var hands_on := input_live_t > 0.0
		var hand: Vector2 = catch_point()
		var contact_y: float = maxf(_catch_plane(), hand.y / maxf(1.0, size.y)) if care != null else _catch_plane()
		var contact_x: float = hand.x / maxf(1.0, size.x) if care != null else catcher_x
		var support_width: float = 12.0 / maxf(1.0, size.x) if care != null else catch_width
		if (
			hands_on and float(entry["y"]) >= contact_y and float(entry["y"]) < _pillow_plane()
			and absf(float(entry["x"]) - contact_x) <= support_width
		):
			fallers.remove_at(index)
			_catch(entry)
			if not active or care != null:
				break
		elif float(entry["y"]) >= _pillow_plane():
			fallers.remove_at(index)
			_miss(entry)

	for index in range(safe_landings.size() - 1, -1, -1):
		var landing: Dictionary = safe_landings[index]
		landing["time"] = float(landing["time"]) - delta
		if float(landing["time"]) <= 0.0:
			safe_landings.remove_at(index)
		else:
			safe_landings[index] = landing
	queue_redraw()


func _baby_texture(index: int) -> Texture2D:
	if textures.is_empty():
		return null
	return textures[posmod(index, textures.size())]


func _catch_plane() -> float:
	return CATCH_Y


func _pillow_plane() -> float:
	return OperaNurseryCare.FLOOR_Y if care != null else PILLOW_Y


func _baby_anchor(texture_index: int) -> Vector2:
	if not baby_feet.is_empty() and baby_feet.size() == textures.size():
		return baby_feet[posmod(texture_index, baby_feet.size())]
	# Specialized callers may load textures in their own _ready. Never index an
	# absent anchor table; measure the visible foot for an unregistered texture.
	var texture: Texture2D = _baby_texture(texture_index)
	if texture != null:
		var image: Image = texture.get_image()
		if image != null:
			var used: Rect2i = image.get_used_rect()
			return Vector2(used.position.x + used.size.x * 0.5, used.end.y) / texture.get_size()
	return Vector2(0.5, 1.0)


func _draw_baby(texture_index: int, point: Vector2, extent: float, opacity: float = 1.0) -> void:
	var texture := _baby_texture(texture_index)
	if texture == null:
		draw_circle(point, extent * 0.36, Color(1.0, 0.82, 0.72, opacity))
		return
	# point is the visible swaddle foot, not the transparent canvas center.
	var foot: Vector2 = _baby_anchor(texture_index)
	var rect := Rect2(point - foot * extent, Vector2.ONE * extent)
	draw_texture_rect(texture, rect, false, Color(1.0, 1.0, 1.0, opacity))


func resting_point(slot: int) -> Vector2:
	return cushion_point(0.10 + float(slot) * 0.20)


func cushion_point(normalized_x: float) -> Vector2:
	var point := Vector2(size.x * normalized_x, size.y * _pillow_plane())
	if cushion_surface_rows.is_empty():
		return point
	# The atlas canvas contains a small transparent margin above the paint.
	# Measure the receiving surface at this actual x; no art is redrawn and
	# a baby cannot float above the pad just because its canvas begins there.
	var width := cushion_surface_rows.size()
	var column := clampi(int(roundf(normalized_x * float(width))), 0, width - 1)
	point.y += float(cushion_surface_rows[column]) * size.x / float(width)
	return point


func catch_point() -> Vector2:
	return care.hand_point() if care != null else Vector2(catcher_x * size.x, size.y * CATCH_Y)


func _resting_extent() -> float:
	return OperaNurseryCare.BABY_EXTENT if care != null else minf(56.0, size.x * 0.12)


func _draw() -> void:
	# Borderless room-grown mobile. The room remains visible through every gap.
	var mobile_y := size.y * 0.12
	draw_line(Vector2(size.x * 0.50, 0), Vector2(size.x * 0.50, mobile_y), Color(0.94, 0.83, 0.55), 4.0)
	for index in range(3):
		var mobile_x := size.x * (0.34 + float(index) * 0.16)
		var bob := sin(elapsed * (1.4 + float(index) * 0.13) + float(index)) * 5.0
		draw_line(Vector2(size.x * 0.50, mobile_y), Vector2(mobile_x, mobile_y + 22.0 + bob), Color(0.78, 0.72, 0.92), 3.0)
		draw_circle(Vector2(mobile_x, mobile_y + 29.0 + bob), 7.0, Color(1.0, 0.88, 0.42))

	# Pillow-safe floor. A miss rests here while Faron gently returns the baby.
	if pillows_texture != null:
		# Keep the authored cushion aspect. cushion_point measures each receiving
		# painted surface independently of the transparent top canvas edge.
		var pad_height: float = size.x * 117.0 / 1014.0
		draw_texture_rect(pillows_texture,
			Rect2(0.0, size.y * _pillow_plane(), size.x, pad_height), false)
	else:
		for index in range(5):
			var pillow_x := size.x * (0.10 + float(index) * 0.20)
			draw_circle(Vector2(pillow_x, size.y * 0.91), size.x * 0.085, Color(0.66, 0.55 + float(index % 2) * 0.08, 0.82, 0.88))
	for landing: Dictionary in safe_landings:
		var fade := clampf(float(landing.get("time", 0.0)) / 0.35, 0.0, 1.0)
		_draw_baby(
			int(landing.get("texture", 0)),
			cushion_point(float(landing.get("x", 0.5))),
			minf(76.0, size.x * 0.21),
			fade
		)

	# Roshan's broad cradle/arms move directly under the player's finger.
	var catch_point: Vector2 = catch_point()
	var catch_radius := minf(58.0, size.x * 0.15)
	if care != null:
		care.draw_body(self)
	elif cradle_texture != null:
		draw_texture_rect(
			cradle_texture,
			Rect2(catch_point - PALM_UV * catch_radius * 2.0, Vector2.ONE * catch_radius * 2.0),
			false
		)
	else:
		draw_circle(catch_point + Vector2(0, 12), catch_radius, Color(0.35, 0.76, 0.78, 0.34))
		draw_arc(catch_point, catch_radius, 0.10, PI - 0.10, 36, Color(1.0, 0.74, 0.78), 12.0)
		draw_line(catch_point + Vector2(-catch_radius, 2), catch_point + Vector2(-catch_radius * 0.42, -18), Color(1.0, 0.86, 0.72), 11.0, true)
		draw_line(catch_point + Vector2(catch_radius, 2), catch_point + Vector2(catch_radius * 0.42, -18), Color(1.0, 0.86, 0.72), 11.0, true)
	if input_live_t <= 0.0:
		var arrow := catch_point + Vector2(0, -72)
		draw_colored_polygon(PackedVector2Array([
			arrow + Vector2(-18, -22), arrow + Vector2(18, -22), arrow + Vector2(0, 12),
		]), Color(1.0, 0.88, 0.30))

	for entry: Dictionary in fallers:
		_draw_baby(
			int(entry.get("texture", 0)),
			Vector2(float(entry.get("x", 0.5)) * size.x, float(entry.get("y", 0.0)) * size.y),
			OperaNurseryCare.BABY_EXTENT if care != null else minf(86.0, size.x * 0.23)
		)

	# A caught baby stays on the palms before moving into its own fixed pad.
	# Pending transfers are not also drawn in their settled slots.
	var shown := mini(settled.size(), 5)
	for index in range(shown):
		var moving: bool = false
		for transfer: Dictionary in transfers:
			if int(transfer["slot"]) == index:
				moving = true
				break
		if moving:
			continue
		_draw_baby(
			settled[index],
			resting_point(index),
			_resting_extent()
		)
	for transfer: Dictionary in transfers:
		if care != null:
			_draw_baby(int(transfer["texture"]), care.hand_point(), OperaNurseryCare.BABY_EXTENT)
			continue
		var age: float = float(transfer["time"])
		var fraction: float = clampf((age - HOLD_SECONDS) / TRANSFER_SECONDS, 0.0, 1.0)
		var from := Vector2(float(transfer["from_x"]) * size.x, size.y * CATCH_Y)
		var point: Vector2 = from.lerp(resting_point(int(transfer["slot"])), fraction)
		_draw_baby(int(transfer["texture"]), point,
			lerpf(minf(86.0, size.x * 0.23), _resting_extent(), fraction))
