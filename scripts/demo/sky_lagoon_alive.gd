extends Node2D
# Sky Lagoon "alive painting" demo.
#
# Standalone evaluation scene for making the approved painted flat feel alive
# without redrawing it. Nothing in the main game loads this file; run it with
#     godot --path . res://scenes/demo/sky_lagoon_alive.tscn
# It reads the unchanged v5 panorama tiles, the existing layout floor data and
# approved sprites, writes no save data and awards nothing.
#
# Layers, back to front: shader-driven painting (sway, water, clouds, depth
# warp, tap ripples), chimney smoke, animals and Roshan with contact shadows,
# butterflies, meadow motes, tap effects. Press M to switch all painting
# motion off/on for an A/B comparison.

const Frames := preload("res://scripts/roshan_sprite_frames.gd")
const Anchors := preload("res://scripts/roshan_sprite_anchors.gd")
const PAINTING_SHADER := preload("res://assets/shaders/sky_lagoon_alive_painting.gdshader")

const MASTER_SIZE := Vector2(6144.0, 2048.0)
const TILE_PATH := "res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
const LAYOUT_PATH := "res://scripts/arena/sky_lagoon_layout.json"
# Same land route as the shipping promenade (scripts/arena/sky_lagoon_promenade.gd).
const ROUTE_MASTER: Array[Vector2] = [
	Vector2(170.0, 1610.0),
	Vector2(610.0, 1644.0),
	Vector2(1380.0, 1668.0),
	Vector2(2230.0, 1652.0),
	Vector2(3072.0, 1644.0),
	Vector2(3920.0, 1652.0),
	Vector2(4520.0, 1668.0),
	Vector2(4905.0, 1610.0),
	Vector2(5312.0, 1584.0),
]
const ROSHAN_DIRECTIONAL := preload("res://assets/characters/roshan_25d/roshan_directional.png")
const ROSHAN_SWIM_FRONT := preload("res://assets/characters/roshan_25d/roshan_swim_front.png")
const ROSHAN_GESTURE_A := preload("res://assets/characters/roshan_25d/roshan_gesture_a.png")
const ROSHAN_SCALE := 1.4921875
# Directional frame 2 contact anchor (layout roshan_route) minus its body anchor.
const ROSHAN_BODY_ABOVE_CONTACT := 172.0
const ROSHAN_SPEED := 560.0
const ROSHAN_SWIM_FPS := 7.0
const ROSHAN_TWIRL_FRAMES: Array[int] = [12, 13, 14, 15]
const ROSHAN_TWIRL_FRAME_S := 0.15
const DIR_FRONT := 0
const DIR_FRONT_LEFT := 1
const DIR_LEFT := 2
const DIR_RIGHT := 6
const DIR_FRONT_RIGHT := 7

const CONTACT_SHADOW_TEX := preload("res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png")
const SMOKE_TEX := preload("res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png")
const BUTTERFLY_TEX := preload("res://assets/fairy/sprites/bug_moth.png")
const SPLASH_TEX := preload("res://assets/sprites/fx_water/fx_water_splash_small_atlas.png")
const RING_TEX := preload("res://assets/sprites/fx_water/fx_water_ripple_ring_atlas.png")
const FX_COLUMNS := 4
const FX_FRAMES := 8
const FX_FRAME_S := 0.07

const SFX_WATER := preload("res://assets/audio/castle/bubble_water.ogg")
const SFX_RUSTLE := preload("res://assets/audio/castle/curtain_swish.ogg")
const SFX_CHIME := preload("res://assets/audio/chime.ogg")
const SFX_HOP := preload("res://assets/audio/hop_boing.ogg")
const SFX_TAP := preload("res://assets/audio/ui_tap.ogg")
const AMBIENCE := preload("res://assets/audio/ambience_lagoon.ogg")

const CHIMNEY_MASTER := Vector2(4794.0, 428.0)
const CABINS: Array[Vector2] = [
	Vector2(4790.0, 500.0), Vector2(4590.0, 630.0), Vector2(4782.0, 712.0), Vector2(3864.0, 866.0),
]
const CABIN_TOUCH_RADIUS := 95.0
# Unchanged animal atlases, placed inside layout.json's reviewed floor bounds.
const ANIMALS: Array[Dictionary] = [
	{"id": "otter", "x": 0.75, "height": 420.0, "frame_s": 0.26},
	{"id": "frog", "x": 0.2, "height": 322.0, "frame_s": 0.30},
	{"id": "hare", "x": 0.5, "height": 245.0, "frame_s": 0.28},
	{"id": "raccoon", "x": 0.5, "height": 290.0, "frame_s": 0.29},
]
const ANIMAL_ATLAS := "res://assets/sprites/sky_lagoon/animals/%s_%s_atlas.png"
const ANIMAL_TOUCH_RADIUS := 150.0
const BUTTERFLY_HOMES: Array[Vector2] = [
	Vector2(1250.0, 1780.0), Vector2(3950.0, 1930.0), Vector2(5650.0, 1660.0),
]
const BUTTERFLY_WIDTH := 92.0
const BUTTERFLY_TOUCH_RADIUS := 110.0
const LAKE_JUMP_SPOTS: Array[Vector2] = [
	Vector2(5150.0, 1260.0), Vector2(5600.0, 1180.0), Vector2(5900.0, 1360.0), Vector2(220.0, 1300.0),
]
const MASK_SIZE := Vector2i(1024, 512)
const MAX_RIPPLES := 6
const MAX_SHAKES := 4
const DRAG_THRESHOLD_PX := 28.0
const MANUAL_CAMERA_HOLD_S := 3.0

var clock := 0.0
var motion_on := true
# Separate from motion_on so a measurement can hold the camera still.
var camera_breathing := true
var painting: Polygon2D
var painting_material: ShaderMaterial
var mask_viewport: SubViewport
var camera: Camera2D
var camera_x := 1900.0
var manual_camera_until := -1.0
var ripples: Array[Vector4] = []
var shakes: Array[Vector4] = []
var tile_images: Dictionary = {}

var roshan: Sprite2D
var roshan_shadow: Sprite2D
var roshan_x := 1900.0
var roshan_target_x := 1900.0
var roshan_facing := DIR_FRONT_RIGHT
var roshan_twirl_left := 0.0

var animals: Array[Dictionary] = []
var butterflies: Array[Dictionary] = []
var effects: Array[Dictionary] = []
var smoke_puff: CPUParticles2D
var next_fish_jump := 4.0
var fish_jump_index := 0
var audio_players: Array[AudioStreamPlayer] = []
var audio_cursor := 0

var press_screen := Vector2.ZERO
var press_active := false
var dragging := false
# Probe-readable record of every reaction: {"kind", "master", "time"}.
var reaction_log: Array[Dictionary] = []


func _ready() -> void:
	_build_painting()
	_build_smoke()
	_build_animals()
	_build_roshan()
	_build_butterflies()
	_build_motes()
	_build_audio()
	camera = Camera2D.new()
	camera.name = "DemoCamera"
	add_child(camera)
	camera.make_current()
	_update_camera(0.0)


func _process(delta: float) -> void:
	clock += delta
	_tick_roshan(delta)
	_tick_animals(delta)
	_tick_butterflies(delta)
	_tick_effects(delta)
	_tick_fish(delta)
	_update_camera(delta)
	_push_shader_state(delta)


# --- painting ---------------------------------------------------------------

func _build_painting() -> void:
	painting = Polygon2D.new()
	painting.name = "AlivePainting"
	painting.polygon = PackedVector2Array([
		Vector2.ZERO, Vector2(MASTER_SIZE.x, 0.0), MASTER_SIZE, Vector2(0.0, MASTER_SIZE.y),
	])
	painting.z_index = -10
	painting_material = ShaderMaterial.new()
	painting_material.shader = PAINTING_SHADER
	var tiles: Array[Texture2D] = []
	for row: int in range(2):
		for column: int in range(6):
			tiles.append(load(TILE_PATH % [row, column]) as Texture2D)
	painting_material.set_shader_parameter("tiles", tiles)
	painting_material.set_shader_parameter("master_size", MASTER_SIZE)
	painting.material = painting_material
	# One-time GPU mask pass: the same shader classifies the painting into a
	# small power-of-two render target, which every later frame only samples.
	mask_viewport = SubViewport.new()
	mask_viewport.name = "MotionMaskViewport"
	mask_viewport.size = MASK_SIZE
	mask_viewport.transparent_bg = true
	mask_viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
	var mask_quad := Polygon2D.new()
	mask_quad.polygon = painting.polygon
	mask_quad.scale = Vector2(MASK_SIZE) / MASTER_SIZE
	var mask_material := ShaderMaterial.new()
	mask_material.shader = PAINTING_SHADER
	mask_material.set_shader_parameter("tiles", tiles)
	mask_material.set_shader_parameter("master_size", MASTER_SIZE)
	mask_material.set_shader_parameter("mask_pass", true)
	mask_quad.material = mask_material
	mask_viewport.add_child(mask_quad)
	add_child(mask_viewport)
	painting_material.set_shader_parameter("motion_mask", mask_viewport.get_texture())
	add_child(painting)
	for _i: int in range(MAX_RIPPLES):
		ripples.append(Vector4.ZERO)
	for _i: int in range(MAX_SHAKES):
		shakes.append(Vector4.ZERO)


func _push_shader_state(delta: float) -> void:
	for i: int in range(shakes.size()):
		var s: Vector4 = shakes[i]
		s.w = maxf(0.0, s.w - delta * 1.4)
		shakes[i] = s
	painting_material.set_shader_parameter("now", clock)
	painting_material.set_shader_parameter("motion_amount", 1.0 if motion_on else 0.0)
	var span: float = maxf(1.0, MASTER_SIZE.x - _visible_master_width())
	var left: float = camera_x - _visible_master_width() * 0.5
	painting_material.set_shader_parameter("camera_norm", clampf(left / span, 0.0, 1.0) * 2.0 - 1.0)
	painting_material.set_shader_parameter("ripples", ripples)
	painting_material.set_shader_parameter("shakes", shakes)


func add_ripple(master: Vector2, strength: float) -> void:
	ripples.pop_front()
	ripples.append(Vector4(master.x, master.y, clock, strength))


func add_shake(master: Vector2, radius: float) -> void:
	shakes.pop_front()
	shakes.append(Vector4(master.x, master.y, radius, 1.0))


func set_motion(enabled: bool) -> void:
	motion_on = enabled


# CPU twin of the shader's classify() so a tap reacts to what is painted there.
# A 3x3 vote around the finger keeps small painted details (a highlight on a
# leaf, a dark ripple) from flipping the answer, and forgives imprecise taps.
func material_at(master: Vector2) -> String:
	var votes := {"water": 0, "foliage": 0, "cloud": 0}
	for dy: int in range(-1, 2):
		for dx: int in range(-1, 2):
			var kind: String = _pixel_material(master + Vector2(dx, dy) * 36.0)
			if votes.has(kind):
				votes[kind] = (votes[kind] as int) + 1
	var best := ""
	var best_votes := 2
	for kind: String in ["water", "foliage", "cloud"]:
		if (votes[kind] as int) > best_votes:
			best = kind
			best_votes = votes[kind] as int
	if best != "":
		return best
	return "sky" if master.y < 820.0 else "ground"


func _pixel_material(master: Vector2) -> String:
	var color: Color = _painting_color(master)
	if color.a <= 0.0:
		return ""
	var hue: float = color.h * 360.0
	var in_lakes: bool = (master.x < 700.0 and master.y > 1120.0 and master.y < 1480.0) \
		or (master.x > 4450.0 and master.y > 960.0 and master.y < 1620.0)
	if in_lakes and hue > 176.0 and hue < 202.0 and color.s > 0.62 and color.v > 0.36:
		return "water"
	if hue > 80.0 and hue < 207.0 and color.s > 0.32 and color.v < 0.6 and master.y > 260.0 \
			and (master.y > 880.0 or master.x < 420.0):
		return "foliage"
	var sky_cloud: bool = color.s < 0.2 and color.v > 0.87 and master.y < 780.0 \
		and (master.x < 4400.0 or (master.x > 5050.0 and master.x < 5800.0 and master.y < 360.0))
	var sea_cloud: bool = color.s < 0.38 and color.v > 0.84 and master.x > 480.0 \
		and master.x < 3450.0 and master.y > 900.0 and master.y < 1300.0
	if sky_cloud or sea_cloud:
		return "cloud"
	return ""


func _painting_color(master: Vector2) -> Color:
	var p: Vector2 = master.clamp(Vector2.ZERO, MASTER_SIZE - Vector2.ONE)
	var column: int = int(p.x / 1024.0)
	var row: int = int(p.y / 1024.0)
	var key: int = row * 6 + column
	if not tile_images.has(key):
		var texture: Texture2D = load(TILE_PATH % [row, column]) as Texture2D
		var image: Image = texture.get_image() if texture != null else null
		if image != null and image.is_compressed():
			if image.decompress() != OK:
				image = null
		tile_images[key] = image
	var cached: Image = tile_images[key] as Image
	if cached == null:
		return Color(0, 0, 0, 0)
	return cached.get_pixel(int(p.x) - column * 1024, int(p.y) - row * 1024)


# --- camera -----------------------------------------------------------------

func _zoom_for_viewport() -> float:
	var size: Vector2 = get_viewport_rect().size
	return maxf(size.y / MASTER_SIZE.y, size.x / MASTER_SIZE.x)


func _visible_master_width() -> float:
	return get_viewport_rect().size.x / _zoom_for_viewport()


func _update_camera(delta: float) -> void:
	if clock > manual_camera_until:
		var follow: float = 1.0 - exp(-delta * 2.2)
		camera_x = lerpf(camera_x, roshan_x, follow)
	var half: float = _visible_master_width() * 0.5
	camera_x = clampf(camera_x, half, MASTER_SIZE.x - half)
	# A slow "breathing" drift that never shows past the painting's edge:
	# zoom only ever pushes slightly in, and the offset stays inside that margin.
	var breathe: float = 1.004 + 0.004 * sin(clock * 0.13) if motion_on and camera_breathing else 1.004
	var zoom: float = _zoom_for_viewport() * breathe
	camera.zoom = Vector2(zoom, zoom)
	var margin: Vector2 = get_viewport_rect().size / zoom * (1.0 - 1.0 / breathe) * 0.5
	var drift := Vector2(sin(clock * 0.21), sin(clock * 0.17)) * margin * 0.9 \
		if motion_on and camera_breathing else Vector2.ZERO
	camera.position = Vector2(clampf(camera_x + drift.x, half, MASTER_SIZE.x - half),
		MASTER_SIZE.y * 0.5 + drift.y)


# --- input ------------------------------------------------------------------

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey:
		var key := event as InputEventKey
		if key.pressed and not key.echo and key.keycode == KEY_M:
			motion_on = not motion_on
		return
	if event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed:
			press_active = true
			dragging = false
			press_screen = button.position
		elif press_active:
			press_active = false
			if not dragging:
				tap_screen(button.position)
	elif event is InputEventMouseMotion and press_active:
		var motion := event as InputEventMouseMotion
		if dragging or motion.position.distance_to(press_screen) > DRAG_THRESHOLD_PX:
			dragging = true
			camera_x -= motion.relative.x / camera.zoom.x
			manual_camera_until = clock + MANUAL_CAMERA_HOLD_S


# Holds the camera over one spot (probe measurements, owner screenshots).
func park_camera(master_x: float, seconds: float) -> void:
	camera_x = master_x
	manual_camera_until = clock + seconds


func screen_to_master(screen: Vector2) -> Vector2:
	return get_canvas_transform().affine_inverse() * screen


func tap_screen(screen: Vector2) -> String:
	return tap_master(screen_to_master(screen))


# Every tap gets an answer from the thing that was touched (DL-INT-02); there
# is no wrong place to touch and nothing is collected or scored.
func tap_master(master: Vector2) -> String:
	var kind: String = _tap_target(master)
	match kind:
		"roshan":
			roshan_twirl_left = ROSHAN_TWIRL_FRAMES.size() * ROSHAN_TWIRL_FRAME_S * 2.0
			_play(SFX_CHIME, -4.0)
		"animal":
			pass
		"butterfly":
			_play(SFX_TAP, -6.0)
		"cabin":
			smoke_puff.global_position = CHIMNEY_MASTER
			smoke_puff.restart()
			add_shake(master, 120.0)
			_play(SFX_CHIME, -8.0)
		"water":
			add_ripple(master, 1.0)
			_spawn_fx(SPLASH_TEX, master, 170.0)
			_spawn_fx(RING_TEX, master + Vector2(0.0, 10.0), 260.0)
			_play(SFX_WATER, -4.0)
		"foliage":
			add_shake(master, 260.0)
			add_ripple(master, 0.45)
			_play(SFX_RUSTLE, -6.0)
		"cloud":
			add_ripple(master, 0.8)
			_play(SFX_CHIME, -12.0)
		"sky":
			add_ripple(master, 0.35)
			_play(SFX_TAP, -10.0)
		_:
			roshan_target_x = clampf(master.x, ROUTE_MASTER[0].x, ROUTE_MASTER[ROUTE_MASTER.size() - 1].x)
			add_ripple(_route_point(roshan_target_x), 0.35)
			_play(SFX_TAP, -8.0)
			kind = "ground"
	reaction_log.append({"kind": kind, "master": master, "time": clock})
	return kind


func _tap_target(master: Vector2) -> String:
	var body: Vector2 = _route_point(roshan_x) - Vector2(0.0, ROSHAN_BODY_ABOVE_CONTACT)
	if master.distance_to(body) < 170.0:
		return "roshan"
	for animal: Dictionary in animals:
		var sprite: Sprite2D = animal["sprite"] as Sprite2D
		var centre: Vector2 = (animal["contact"] as Vector2) - Vector2(0.0, (animal["height"] as float) * 0.45)
		if master.distance_to(centre) < ANIMAL_TOUCH_RADIUS and sprite.visible:
			_startle(animal)
			return "animal"
	for butterfly: Dictionary in butterflies:
		var sprite: Sprite2D = butterfly["sprite"] as Sprite2D
		if master.distance_to(sprite.position) < BUTTERFLY_TOUCH_RADIUS:
			butterfly["flee"] = 2.5
			return "butterfly"
	for cabin: Vector2 in CABINS:
		if master.distance_to(cabin) < CABIN_TOUCH_RADIUS:
			return "cabin"
	return material_at(master)


# --- Roshan -----------------------------------------------------------------

func _build_roshan() -> void:
	roshan_shadow = Sprite2D.new()
	roshan_shadow.name = "RoshanShadow"
	roshan_shadow.texture = CONTACT_SHADOW_TEX
	roshan_shadow.modulate = Color(1, 1, 1, 0.55)
	add_child(roshan_shadow)
	roshan = Sprite2D.new()
	roshan.name = "Roshan"
	roshan.centered = false
	roshan.region_enabled = true
	roshan.scale = Vector2(ROSHAN_SCALE, ROSHAN_SCALE)
	add_child(roshan)


func _tick_roshan(delta: float) -> void:
	var sheet := "directional"
	var frame: int = roshan_facing
	var texture: Texture2D = ROSHAN_DIRECTIONAL
	var columns := 4
	var gap: float = roshan_target_x - roshan_x
	if roshan_twirl_left > 0.0:
		roshan_twirl_left -= delta
		var step: int = int(roshan_twirl_left / ROSHAN_TWIRL_FRAME_S) % ROSHAN_TWIRL_FRAMES.size()
		sheet = "gesture_a"
		frame = ROSHAN_TWIRL_FRAMES[ROSHAN_TWIRL_FRAMES.size() - 1 - step]
		texture = ROSHAN_GESTURE_A
	elif absf(gap) > 6.0:
		roshan_x += signf(gap) * minf(absf(gap), ROSHAN_SPEED * delta)
		roshan_facing = DIR_FRONT_RIGHT if gap > 0.0 else DIR_FRONT_LEFT
		sheet = "swim_front"
		frame = int(clock * ROSHAN_SWIM_FPS) % 16
		texture = ROSHAN_SWIM_FRONT
	roshan.texture = texture
	roshan.region_rect = Frames.region(sheet, frame, columns)
	var anchor: Vector2 = Anchors.anchor(sheet, frame) if Anchors.has_sheet(sheet) \
		else Vector2(128.0, 118.0)
	anchor -= Frames.shift(sheet, frame)
	var contact: Vector2 = _route_point(roshan_x)
	var bob: float = sin(clock * 2.1) * 7.0
	var body := contact - Vector2(0.0, ROSHAN_BODY_ABOVE_CONTACT - bob)
	roshan.position = body - anchor * ROSHAN_SCALE
	roshan.z_index = 2
	roshan_shadow.position = contact
	var shadow_scale: float = 1.15 - bob * 0.01
	roshan_shadow.scale = Vector2(shadow_scale * 1.5, shadow_scale)
	roshan_shadow.z_index = 1


func _route_point(x: float) -> Vector2:
	if x <= ROUTE_MASTER[0].x:
		return ROUTE_MASTER[0]
	for i: int in range(1, ROUTE_MASTER.size()):
		var a: Vector2 = ROUTE_MASTER[i - 1]
		var b: Vector2 = ROUTE_MASTER[i]
		if x <= b.x:
			return a.lerp(b, (x - a.x) / maxf(1.0, b.x - a.x))
	return ROUTE_MASTER[ROUTE_MASTER.size() - 1]


func roshan_master_x() -> float:
	return roshan_x


# --- animals ----------------------------------------------------------------

func _build_animals() -> void:
	var text: String = FileAccess.get_file_as_string(LAYOUT_PATH)
	var parsed: Variant = JSON.parse_string(text)
	if not parsed is Dictionary:
		push_warning("sky_lagoon_alive: layout data missing; animals skipped")
		return
	var ground: Dictionary = (parsed as Dictionary).get("animal_ground", {}) as Dictionary
	var species: Dictionary = ground.get("species", {}) as Dictionary
	for def: Dictionary in ANIMALS:
		var id: String = def["id"] as String
		if not species.has(id):
			continue
		var data: Dictionary = species[id] as Dictionary
		var bounds: Array = data["bounds"] as Array
		var contact := Vector2(float(bounds[0]) + float(bounds[2]) * (def["x"] as float),
			float(bounds[1]) + float(bounds[3]) * 0.5)
		var sprite := Sprite2D.new()
		sprite.name = "Animal_%s" % id
		sprite.centered = false
		sprite.region_enabled = true
		var height: float = def["height"] as float
		sprite.scale = Vector2.ONE * (height / 256.0)
		sprite.z_index = 1
		var shadow := Sprite2D.new()
		shadow.texture = CONTACT_SHADOW_TEX
		shadow.modulate = Color(1, 1, 1, 0.45)
		shadow.position = contact
		shadow.scale = Vector2(height / 260.0, height / 520.0)
		add_child(shadow)
		add_child(sprite)
		animals.append({
			"id": id, "sprite": sprite, "contact": contact, "height": height,
			"idle": load(ANIMAL_ATLAS % [id, "idle"]) as Texture2D,
			"startle": load(ANIMAL_ATLAS % [id, "startle"]) as Texture2D,
			"idle_feet": data["idle_feet_y"] as Array,
			"startle_feet": data["startle_feet_y"] as Array,
			"frame_s": def["frame_s"] as float, "startle_left": 0.0,
			"phase": randf() * 3.0,
		})
	_tick_animals(0.0)


func _startle(animal: Dictionary) -> void:
	if (animal["startle_left"] as float) > 0.0:
		return
	animal["startle_left"] = 4.0 * 0.12 * 2.0
	_play(SFX_HOP, -6.0)


func _tick_animals(delta: float) -> void:
	for animal: Dictionary in animals:
		var sprite: Sprite2D = animal["sprite"] as Sprite2D
		var startle_left: float = maxf(0.0, (animal["startle_left"] as float) - delta)
		animal["startle_left"] = startle_left
		var feet: Array
		var frame: int
		var hop := 0.0
		if startle_left > 0.0:
			sprite.texture = animal["startle"] as Texture2D
			feet = animal["startle_feet"] as Array
			var total: float = 4.0 * 0.12 * 2.0
			var t: float = 1.0 - startle_left / total
			frame = mini(3, int(t * 4.0))
			hop = sin(t * PI) * 60.0
		else:
			sprite.texture = animal["idle"] as Texture2D
			feet = animal["idle_feet"] as Array
			frame = int((clock + (animal["phase"] as float)) / (animal["frame_s"] as float)) % 4
		sprite.region_rect = Rect2(Vector2(float(frame % 2), float(frame >> 1)) * 256.0, Vector2(256.0, 256.0))
		var foot := Vector2(128.0, float(feet[frame]))
		sprite.position = (animal["contact"] as Vector2) - foot * sprite.scale - Vector2(0.0, hop)


# --- butterflies, smoke, motes --------------------------------------------------

func _build_butterflies() -> void:
	for i: int in range(BUTTERFLY_HOMES.size()):
		var sprite := Sprite2D.new()
		sprite.name = "Butterfly_%d" % i
		sprite.texture = BUTTERFLY_TEX
		sprite.z_index = 3
		add_child(sprite)
		butterflies.append({"sprite": sprite, "home": BUTTERFLY_HOMES[i],
			"phase": float(i) * 2.1, "flee": 0.0, "lift": 0.0})
	_tick_butterflies(0.0)


func _tick_butterflies(delta: float) -> void:
	var base: float = BUTTERFLY_WIDTH / float(BUTTERFLY_TEX.get_width())
	for butterfly: Dictionary in butterflies:
		var sprite: Sprite2D = butterfly["sprite"] as Sprite2D
		var phase: float = butterfly["phase"] as float
		var flee: float = maxf(0.0, (butterfly["flee"] as float) - delta)
		butterfly["flee"] = flee
		var lift: float = butterfly["lift"] as float
		lift = lerpf(lift, 420.0 if flee > 0.0 else 0.0, 1.0 - exp(-delta * (3.0 if flee > 0.0 else 0.8)))
		butterfly["lift"] = lift
		var t: float = clock * 0.55 + phase
		var home: Vector2 = butterfly["home"] as Vector2
		sprite.position = home + Vector2(sin(t) * 150.0 + sin(t * 2.3) * 40.0,
			-90.0 + sin(t * 1.7) * 45.0 - lift)
		var flap_speed: float = 22.0 if flee > 0.0 else 11.0
		var flap: float = 0.3 + 0.7 * absf(sin(clock * flap_speed + phase))
		sprite.scale = Vector2(base * flap, base)
		sprite.rotation = 0.18 * sin(t * 2.0)


func _build_smoke() -> void:
	var smoke := CPUParticles2D.new()
	smoke.name = "ChimneySmoke"
	smoke.texture = SMOKE_TEX
	smoke.position = CHIMNEY_MASTER
	smoke.amount = 5
	smoke.lifetime = 5.0
	smoke.preprocess = 5.0
	smoke.direction = Vector2(0.15, -1.0)
	smoke.spread = 8.0
	smoke.gravity = Vector2(6.0, 0.0)
	smoke.initial_velocity_min = 22.0
	smoke.initial_velocity_max = 30.0
	smoke.scale_amount_min = 0.35
	smoke.scale_amount_max = 0.5
	smoke.scale_amount_curve = _rising_curve(0.6, 1.4)
	smoke.color_ramp = _fade_ramp(Color(1, 1, 1, 0.75))
	add_child(smoke)
	smoke_puff = smoke.duplicate() as CPUParticles2D
	smoke_puff.name = "ChimneyPuff"
	smoke_puff.one_shot = true
	smoke_puff.emitting = false
	smoke_puff.preprocess = 0.0
	smoke_puff.amount = 6
	smoke_puff.lifetime = 2.4
	smoke_puff.explosiveness = 0.85
	smoke_puff.initial_velocity_min = 60.0
	smoke_puff.initial_velocity_max = 90.0
	smoke_puff.spread = 25.0
	add_child(smoke_puff)


func _build_motes() -> void:
	var motes := CPUParticles2D.new()
	motes.name = "MeadowMotes"
	motes.texture = _soft_dot()
	motes.position = Vector2(2800.0, 1450.0)
	motes.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	motes.emission_rect_extents = Vector2(1500.0, 380.0)
	motes.amount = 24
	motes.lifetime = 8.0
	motes.preprocess = 8.0
	motes.direction = Vector2(0.4, -1.0)
	motes.spread = 35.0
	motes.gravity = Vector2.ZERO
	motes.initial_velocity_min = 12.0
	motes.initial_velocity_max = 26.0
	motes.scale_amount_min = 0.8
	motes.scale_amount_max = 1.5
	motes.color_ramp = _fade_ramp(Color(1.0, 0.96, 0.78, 0.8))
	motes.z_index = 4
	add_child(motes)


func _soft_dot() -> GradientTexture2D:
	var gradient := Gradient.new()
	gradient.set_color(0, Color(1, 1, 1, 1))
	gradient.set_color(1, Color(1, 1, 1, 0))
	var texture := GradientTexture2D.new()
	texture.gradient = gradient
	texture.fill = GradientTexture2D.FILL_RADIAL
	texture.fill_from = Vector2(0.5, 0.5)
	texture.fill_to = Vector2(1.0, 0.5)
	texture.width = 16
	texture.height = 16
	return texture


func _fade_ramp(color: Color) -> Gradient:
	var ramp := Gradient.new()
	ramp.offsets = PackedFloat32Array([0.0, 0.2, 0.75, 1.0])
	var clear := Color(color.r, color.g, color.b, 0.0)
	ramp.colors = PackedColorArray([clear, color, color, clear])
	return ramp


func _rising_curve(start: float, end: float) -> Curve:
	var curve := Curve.new()
	curve.max_value = maxf(start, end)
	curve.add_point(Vector2(0.0, start))
	curve.add_point(Vector2(1.0, end))
	return curve


# --- lake life and one-shot water effects ---------------------------------------

func _tick_fish(_delta: float) -> void:
	if clock < next_fish_jump:
		return
	var spot: Vector2 = LAKE_JUMP_SPOTS[fish_jump_index % LAKE_JUMP_SPOTS.size()]
	fish_jump_index += 1
	next_fish_jump = clock + 6.0 + float(fish_jump_index % 3) * 2.5
	add_ripple(spot, 0.6)
	_spawn_fx(SPLASH_TEX, spot, 120.0)


func _spawn_fx(texture: Texture2D, master: Vector2, width: float) -> void:
	var sprite := Sprite2D.new()
	sprite.texture = texture
	sprite.region_enabled = true
	sprite.offset = Vector2(0.0, -96.0)
	sprite.position = master
	sprite.scale = Vector2.ONE * (width / 256.0)
	sprite.z_index = 2
	add_child(sprite)
	effects.append({"sprite": sprite, "age": 0.0})
	_tick_effects(0.0)


func _tick_effects(delta: float) -> void:
	for i: int in range(effects.size() - 1, -1, -1):
		var effect: Dictionary = effects[i]
		var age: float = (effect["age"] as float) + delta
		effect["age"] = age
		var sprite: Sprite2D = effect["sprite"] as Sprite2D
		var frame: int = int(age / FX_FRAME_S)
		if frame >= FX_FRAMES:
			sprite.queue_free()
			effects.remove_at(i)
			continue
		sprite.region_rect = Rect2(Vector2(float(frame % FX_COLUMNS), floorf(float(frame) / FX_COLUMNS)) * 256.0,
			Vector2(256.0, 256.0))


# --- audio ------------------------------------------------------------------

func _build_audio() -> void:
	for _i: int in range(4):
		var player := AudioStreamPlayer.new()
		add_child(player)
		audio_players.append(player)
	var ambience := AudioStreamPlayer.new()
	ambience.name = "Ambience"
	ambience.stream = AMBIENCE
	ambience.volume_db = -14.0
	add_child(ambience)
	ambience.play()


func _play(stream: AudioStream, volume_db: float) -> void:
	var player: AudioStreamPlayer = audio_players[audio_cursor]
	audio_cursor = (audio_cursor + 1) % audio_players.size()
	player.stream = stream
	player.volume_db = volume_db
	player.play()
