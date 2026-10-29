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
const DRAWS_CARD_BACKING := false

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
var retired_backdrop_path := ""
var cradle_texture: Texture2D = null
var pillows_texture: Texture2D = null
var painted_art: NurseryPaintedArt = null


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	# Keep the path as audit evidence, but never paint the framed legacy card.
	retired_backdrop_path = "res://assets/opera/worlds/widgets/widget_catch_nursery.png"
	backdrop_texture = null
	cradle_texture = _load_if_exists("res://assets/opera/worlds/nursery_quality_20261019/cradle.png")
	pillows_texture = _load_if_exists("res://assets/opera/worlds/nursery_quality_20261019/pillows.png")
	painted_art = NurseryPaintedArt.new()
	painted_art.bind(self)
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
	# One complete painted mobile, not code rods/dots or a separate card.
	if painted_art != null:
		var mobile_side := minf(size.x * 0.28, size.y * 0.44)
		painted_art.picture("mobile", Rect2(
			Vector2(size.x * 0.5 - mobile_side * 0.5, 0), Vector2.ONE * mobile_side))
	if pillows_texture != null:
		var ratio := float(pillows_texture.get_height()) / float(pillows_texture.get_width())
		var height := size.x * ratio
		draw_texture_rect(pillows_texture,
			Rect2(0, size.y * PILLOW_Y - height * 0.5, size.x, height), false)
	for landing: Dictionary in safe_landings:
		var extent := minf(76.0, size.x * 0.21)
		var fade := clampf(float(landing.get("time", 0.0)) / 0.35, 0.0, 1.0)
		_draw_baby(int(landing.get("texture", 0)),
			Vector2(float(landing.get("x", 0.5)) * size.x,
				size.y * PILLOW_Y - extent * 0.47), extent, fade)
	var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
	var catch_radius := minf(58.0, size.x * 0.15)
	if cradle_texture != null:
		draw_texture_rect(cradle_texture,
			Rect2(catch_point - Vector2(catch_radius, catch_radius * 1.55),
				Vector2.ONE * catch_radius * 2.0), false)
	if input_live_t <= 0.0 and painted_art != null:
		painted_art.draw_guide(catch_point + Vector2(0, size.y * 0.08), false)
	for entry: Dictionary in fallers:
		var extent := minf(86.0, size.x * 0.23)
		# The completed-care hold shows any already-spawned extra baby safe on
		# a pillow, with no sixth catch/reward or airborne frozen recipient.
		var center_y := size.y * PILLOW_Y - extent * 0.47 if not active and caught >= goal 			else float(entry.get("y", 0.0)) * size.y - extent * 0.315
		_draw_baby(int(entry.get("texture", 0)),
			Vector2(float(entry.get("x", 0.5)) * size.x, center_y), extent)
	var shown := mini(settled.size(), 5)
	for index in range(shown):
		var spread := float(index) - float(shown - 1) * 0.5
		_draw_baby(settled[index], catch_point + Vector2(spread * 20.0, -42.0 * 0.43), 42.0)
