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
const CATCH_Y := 0.74
const PILLOW_Y := 0.91
const INPUT_MEMORY := 2.0

var active := false
var goal := 5
var caught := 0
var missed := 0
var spawned := 0
var elapsed := 0.0
var spawn_t := 0.0
var input_live_t := 0.0
var catcher_x := 0.5
var fallers: Array[Dictionary] = []
var safe_landings: Array[Dictionary] = []
var settled: Array[int] = []
var textures: Array[Texture2D] = []
var backdrop_texture: Texture2D = null
var cradle_texture: Texture2D = null
var pillows_texture: Texture2D = null


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	backdrop_texture = _load_if_exists("res://assets/opera/worlds/widgets/widget_catch_nursery.png")
	cradle_texture = _load_if_exists("res://assets/opera/worlds/widgets/widget_catch_nursery_cradle.png")
	pillows_texture = _load_if_exists("res://assets/opera/worlds/widgets/widget_catch_nursery_pillows.png")
	for path: String in BABY_PATHS:
		var texture := load(path) as Texture2D
		if texture != null:
			textures.append(texture)
	set_meta("no_fail", true)
	set_meta("live_input_gate_seconds", INPUT_MEMORY)


func _load_if_exists(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func start(next_goal: int) -> void:
	goal = maxi(1, next_goal)
	caught = 0
	missed = 0
	spawned = 0
	elapsed = 0.0
	spawn_t = 0.18
	input_live_t = 0.0
	catcher_x = 0.5
	fallers.clear()
	safe_landings.clear()
	settled.clear()
	active = true
	set_process(true)
	queue_redraw()


func stop() -> void:
	active = false
	set_process(false)
	fallers.clear()
	safe_landings.clear()
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
		if touch.pressed:
			_set_catcher_from_local(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		_set_catcher_from_local((event as InputEventScreenDrag).position)
		accept_event()
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.pressed:
			_set_catcher_from_local(button.position)
		accept_event()
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		_set_catcher_from_local((event as InputEventMouseMotion).position)
		accept_event()


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
	baby_caught.emit(1.0)
	if caught >= goal:
		active = false
		set_process(false)


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
	if not active:
		return
	elapsed += delta
	input_live_t = maxf(0.0, input_live_t - delta)
	spawn_t -= delta
	var max_fallers := 2 if caught >= 2 else 1
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
		if (
			hands_on and float(entry["y"]) >= CATCH_Y
			and absf(float(entry["x"]) - catcher_x) <= catch_width
		):
			fallers.remove_at(index)
			_catch(entry)
			if not active:
				break
		elif float(entry["y"]) >= PILLOW_Y:
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


func _draw_baby(texture_index: int, point: Vector2, extent: float, opacity: float = 1.0) -> void:
	var texture := _baby_texture(texture_index)
	if texture == null:
		draw_circle(point, extent * 0.36, Color(1.0, 0.82, 0.72, opacity))
		return
	var rect := Rect2(point - Vector2.ONE * extent * 0.5, Vector2.ONE * extent)
	draw_texture_rect(texture, rect, false, Color(1.0, 1.0, 1.0, opacity))


func _draw() -> void:
	var panel := Rect2(Vector2.ZERO, size)
	if backdrop_texture != null:
		draw_texture_rect(backdrop_texture, panel, false)
	else:
		draw_rect(panel, Color(0.035, 0.04, 0.11, 0.86), true)
	draw_rect(panel.grow(-4.0), Color(0.66, 0.90, 0.88), false, 5.0)
	# The authored backdrop carries the mobile band; keep the vector mobile as
	# a graceful fallback when the raster set is unavailable.
	if backdrop_texture == null:
		var mobile_y := size.y * 0.12
		draw_line(Vector2(size.x * 0.50, 0), Vector2(size.x * 0.50, mobile_y), Color(0.94, 0.83, 0.55), 4.0)
		for index in range(3):
			var mobile_x := size.x * (0.34 + float(index) * 0.16)
			var bob := sin(elapsed * (1.4 + float(index) * 0.13) + float(index)) * 5.0
			draw_line(Vector2(size.x * 0.50, mobile_y), Vector2(mobile_x, mobile_y + 22.0 + bob), Color(0.78, 0.72, 0.92), 3.0)
			draw_circle(Vector2(mobile_x, mobile_y + 29.0 + bob), 7.0, Color(1.0, 0.88, 0.42))

	# Pillow-safe floor. A miss rests here while Faron gently returns the baby.
	if pillows_texture != null:
		draw_texture_rect(pillows_texture, Rect2(0.0, size.y * 0.78, size.x, size.y * 0.22), false)
	else:
		for index in range(5):
			var pillow_x := size.x * (0.10 + float(index) * 0.20)
			draw_circle(Vector2(pillow_x, size.y * 0.91), size.x * 0.085, Color(0.66, 0.55 + float(index % 2) * 0.08, 0.82, 0.88))
	for landing: Dictionary in safe_landings:
		var fade := clampf(float(landing.get("time", 0.0)) / 0.35, 0.0, 1.0)
		_draw_baby(
			int(landing.get("texture", 0)),
			Vector2(float(landing.get("x", 0.5)) * size.x, size.y * 0.82),
			minf(76.0, size.x * 0.21),
			fade
		)

	# Roshan's broad cradle/arms move directly under the player's finger.
	var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
	var catch_radius := minf(58.0, size.x * 0.15)
	if cradle_texture != null:
		draw_texture_rect(
			cradle_texture,
			Rect2(catch_point - Vector2(catch_radius, catch_radius * 1.55), Vector2(catch_radius * 2.0, catch_radius * 2.0)),
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
			minf(86.0, size.x * 0.23)
		)

	# Every caught baby remains visibly safe in the shared cradle.
	var shown := mini(settled.size(), 5)
	for index in range(shown):
		var spread := float(index) - float(shown - 1) * 0.5
		_draw_baby(
			settled[index],
			Vector2(catch_point.x + spread * 25.0, size.y * 0.89),
			42.0
		)
