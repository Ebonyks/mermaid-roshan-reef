class_name ReefKartRace
extends Node2D
## Reef Grand Prix: an original perspective kart race on the Racer career's
## own in-game world, the Pearl Canal Circuit (see ReefKartTrack).
##
## True 2D throughout: a projected Canvas ground (one ColorRect with a canvas
## shader), a scrolling painted skyline, and depth-sorted billboard sprites, HUD
## and touch controls drawn by Node2D draw callbacks. The node tree is fixed
## after setup. The owning surface clocks every step and supplies steer, brake
## and the item bubble; it stops stepping while the child is not playing, so
## zero input can never move, win or lose anything.
##
## Systems: pearls raise Roshan's top speed and are never lost, the gem buoys
## and the item bubbles under the pearl arches give one of four original items,
## and the imp's kart really races. If he finishes first only the race restarts (DL-INT-14); he
## slows after each win and drives at half pace after two.
##
## INTERIM_PLACEHOLDER drawing (code shapes for pearls, bubbles, buoys, kelp,
## arches, controls and the imp's kart, and the painting's top band as skyline)
## stays only until the Codex art packet in
## docs/handoffs/codex_reef_kart_art_2026-11-03/ lands. Every asset in that
## packet reorganizes existing repository art; none is new content.

signal race_event(kind: String, value: float)

const TrackScript := preload("res://scripts/racer/reef_kart_track.gd")
const FloorShader := preload("res://scripts/racer/reef_kart_floor.gdshader")

const VIEW := Vector2(1280.0, 720.0)
const HORIZON_Y := 268.0
const CAM_BACK := 82.0
const CAM_HEIGHT := 34.0
const FOCAL := 560.0
const NEAR := 10.0
const FAR := 2300.0
const LAPS := 2
const BASE_TOP := 300.0
const PEARL_BONUS := 0.025
const MAX_PEARLS := 10
const ACCEL := 250.0
const BRAKE := 640.0
const TURN_MAX := 2.45
const GRIP_LOSS := 0.18
const LANE_RATE := 120.0
const WRONG_WAY := 1.75
const APRON_TOP := 0.52
const BOOST_TOP := 1.42
const KART_RADIUS := 16.0
const PICK_RADIUS := 30.0
const KART_SPRITE := 31.0
const COUNTDOWN := 1.5
const GO_SHOW := 0.7
const ROULETTE := 1.0
const IMP_BEAT := 1.8
const IMP_PACE := 0.965
const RETRY_PACE := 0.88
const MERCY_PACE := 0.5
const START_ITEM := "zoom"
## A sparkle bubble always outruns any kart, even one fired from a standstill.
const SPARKLE_SPEED := 560.0
const ITEM_KINDS: Array[String] = ["zoom", "sparkle", "kelp", "pearls"]
const ROSHAN_FACE := Rect2(150, 10, 170, 180)
const IMP_FACE := Rect2(130, 15, 240, 225)
const GUIDE_TIP := Vector2(0.42, 0.95)
const TEXTURES := {
	"kart_straight": "res://assets/kart/chase/kart_straight.png",
	"kart_left": "res://assets/kart/chase/kart_left.png",
	"kart_right": "res://assets/kart/chase/kart_right.png",
	"kart_boost": "res://assets/kart/chase/kart_boost.png",
	"kart_empty": "res://assets/kart/chase/empty_kart.png",
	"roshan": "res://assets/opera/worlds/actors/roshan_racer.png",
	"imp": "res://assets/opera/worlds/actors/rival_racer.png",
	"guide_hand": "res://assets/opera/worlds/widgets/widget_pipe_guide_hand.png",
}
## Codex art binds here (docs/handoffs/codex_reef_kart_art_2026-11-03/): each
## role uses its file when present and the INTERIM_PLACEHOLDER shape when not.
const ART_ROOT := "res://assets/racer/"
const OPTIONAL_ART := {
	"pearl": "pickups/pearl.png",
	"item_bubble": "pickups/item_bubble.png",
	"kelp": "pickups/kelp_patch.png",
	"sparkle": "pickups/sparkle.png",
	"dizzy": "pickups/dizzy_stars.png",
	"gem_buoy_teal": "pickups/gem_buoy_teal.png",
	"gem_buoy_lavender": "pickups/gem_buoy_lavender.png",
	"gem_buoy_pink": "pickups/gem_buoy_pink.png",
	"imp_kart_straight": "karts/imp_kart_straight.png",
	"imp_kart_left": "karts/imp_kart_left.png",
	"imp_kart_right": "karts/imp_kart_right.png",
	"icon_zoom": "icons/zoom.png",
	"icon_sparkle": "icons/sparkle.png",
	"icon_kelp": "icons/kelp.png",
	"icon_pearls": "icons/pearls.png",
}
## Interim skyline: the top band of the in-game Racer painting itself (deep
## water, pennants, coral ledges and arch tops: native rows 0-286 of the
## 1672x941 picture inside its 2048 POT tiles),
## repeated with alternate copies mirrored so every join is seamless. One turn
## of the camera scrolls exactly SKY_LOOP pixels, matching the ground.
const PALACE_TILES: Array[String] = ["res://assets/opera/worlds/backdrops/world_racer_c0r0.png",
	"res://assets/opera/worlds/backdrops/world_racer_c1r0.png"]
const PALACE_SOURCES: Array[Rect2] = [Rect2(188, 553, 836, 286), Rect2(0, 553, 836, 286)]
const SKY_BAND := 196.0
const SKY_COPIES := 4
const SKY_LOOP := TAU * FOCAL
## The painted skyline (4096x256) keeps its band in rows 28-256.
const SKYLINE_SOURCE := Rect2(0, 28, 4096, 228)
const SKY_WATER := Color("#2f8fcf")
const BUOY_COLORS := {"teal": Color("#3fc7b4"), "lavender": Color("#c9a8f0"),
	"pink": Color("#f07ab8")}
const INK := Color("#51416f")
## Runtime tint that tells the imp's kart apart; no recoloured art needed.
const IMP_TINT := Color(0.86, 0.78, 1.0)

var track: ReefKartTrack = null
var karts: Array[Dictionary] = []
var _pl: Dictionary = {}
var state := "grid"
var clock := 0.0
var race_time := 0.0
var attempt := 1
var imp_wins := 0
var assist := 0.75
var projectiles: Array[Dictionary] = []
var traps: Array[Dictionary] = []
var rng := RandomNumberGenerator.new()
var cam_pos := Vector2.ZERO
var cam_heading := 0.0
var turbo_count := 0
var flash := 0.0
var go_t := 0.0
var controls: Dictionary = {}
var leader_id := ""

var _sky: Node2D = null
var _floor: ColorRect = null
var _world: Node2D = null
var _hud: Node2D = null
var _controls: Node2D = null
var _floor_material: ShaderMaterial = null
var _tex: Dictionary = {}
var _sky_tex: Array[Texture2D] = []
var _skyline: Texture2D = null
var _landmark_tex: Dictionary = {}
var _drawables: Array = []
var _minimap := PackedVector2Array()
var _minimap_rect := Rect2(1090, 18, 170, 170)
var _count_mark := 3
var _time := 0.0
var _confetti_t := 0.0


func setup(options: Dictionary = {}) -> void:
	set_process(false)
	track = TrackScript.new()
	assist = clampf(float(options.get("assist", 0.75)), 0.0, 1.0)
	rng.seed = int(options.get("seed", 20261103))
	var roster: Array = options.get("racers", [
		{"id": "roshan", "player": true},
		{"id": "imp", "player": false, "skill": IMP_PACE},
	])
	karts.clear()
	for index in range(roster.size()):
		karts.append(_new_kart(roster[index] as Dictionary))
	_pl = karts[0]
	_place_grid()
	_load_textures()
	_build_view()
	_build_minimap()
	_update_camera(1.0, true)
	_refresh_view()


func _new_kart(spec: Dictionary) -> Dictionary:
	return {
		"id": String(spec.get("id", "racer")), "player": bool(spec.get("player", false)),
		"skill": float(spec.get("skill", 1.0)), "base_skill": float(spec.get("skill", 1.0)),
		"pos": Vector2.ZERO, "heading": 0.0, "speed": 0.0, "track_s": 0.0, "race_s": 0.0,
		"lat": 0.0, "lat_goal": 0.0, "lap": 0, "pearls": 0, "item": "", "pending": "",
		"roulette_t": 0.0, "boost_t": 0.0, "spin_t": 0.0, "slow_t": 0.0,
		"bump_t": 0.0, "finished": false, "finish_time": 0.0,
		"flubbed": false, "steer_vis": 0.0, "ai_item_t": 0.0, "spin_vis": 0.0,
		"wrong_way": false,
	}


## Side by side on the line: Roshan on the left, the imp on the right.
func _place_grid() -> void:
	var slots: Array[Vector2] = [Vector2(-70.0, -36.0), Vector2(-70.0, 36.0),
		Vector2(-130.0, -36.0), Vector2(-130.0, 36.0)]
	for index in range(karts.size()):
		var k := karts[index]
		var slot: Vector2 = slots[index % slots.size()] - Vector2(float(index / slots.size()) * 120.0, 0.0)
		k["track_s"] = track.wrap_s(slot.x)
		k["race_s"] = slot.x
		k["lat"] = slot.y
		k["lat_goal"] = slot.y
		k["pos"] = track.point_at(slot.x, slot.y)
		k["heading"] = track.heading_at(slot.x)
		k["speed"] = 0.0
		k["lap"] = 0
		for key: String in ["roulette_t", "boost_t", "spin_t", "slow_t", "bump_t",
				"finish_time", "steer_vis", "ai_item_t", "spin_vis"]:
			k[key] = 0.0
		k["finished"] = false
		k["flubbed"] = false
		k["wrong_way"] = false
		k["pending"] = ""
		k["item"] = START_ITEM if bool(k["player"]) else ""


func _load_textures() -> void:
	_tex.clear()
	for key: String in TEXTURES:
		var path: String = TEXTURES[key]
		if ResourceLoader.exists(path):
			_tex[key] = load(path) as Texture2D
	_sky_tex.clear()
	for path: String in PALACE_TILES:
		if ResourceLoader.exists(path):
			_sky_tex.append(load(path) as Texture2D)
	_skyline = null
	if ResourceLoader.exists(ReefKartTrack.PAINTED_SKYLINE):
		_skyline = load(ReefKartTrack.PAINTED_SKYLINE) as Texture2D
	for key: String in OPTIONAL_ART:
		var path: String = ART_ROOT + String(OPTIONAL_ART[key])
		if ResourceLoader.exists(path):
			_tex[key] = load(path) as Texture2D
	_landmark_tex.clear()
	for landmark: Dictionary in ReefKartTrack.LANDMARKS:
		var id := String(landmark["id"])
		var path := ReefKartTrack.TRACK_ROOT + "billboards/%s.png" % id
		if not _landmark_tex.has(id) and ResourceLoader.exists(path):
			_landmark_tex[id] = load(path) as Texture2D


func _build_view() -> void:
	_sky = Node2D.new()
	_sky.name = "Skyline"
	add_child(_sky)
	_sky.draw.connect(_draw_sky)
	_floor = ColorRect.new()
	_floor.name = "Ground"
	_floor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_floor.position = Vector2(0.0, HORIZON_Y)
	_floor.size = Vector2(VIEW.x, VIEW.y - HORIZON_Y)
	_floor_material = ShaderMaterial.new()
	_floor_material.shader = FloorShader
	var painted := ResourceLoader.exists(ReefKartTrack.PAINTED_FLOOR)
	_floor_material.set_shader_parameter("use_painted", painted)
	if painted:
		_floor_material.set_shader_parameter("painted_floor", load(ReefKartTrack.PAINTED_FLOOR))
	else:
		_floor_material.set_shader_parameter("field", track.floor_field())
	_floor_material.set_shader_parameter("rect_size", _floor.size)
	_floor_material.set_shader_parameter("cam_height", CAM_HEIGHT)
	_floor_material.set_shader_parameter("focal", FOCAL)
	_floor_material.set_shader_parameter("world_size", ReefKartTrack.WORLD_SIZE)
	_floor_material.set_shader_parameter("road_edge", ReefKartTrack.ROAD_HALF / ReefKartTrack.FIELD_FAR)
	_floor_material.set_shader_parameter("rail_edge", ReefKartTrack.RAIL / ReefKartTrack.FIELD_FAR)
	_floor_material.set_shader_parameter("lane_line", 40.0 / ReefKartTrack.FIELD_FAR)
	_floor.material = _floor_material
	add_child(_floor)
	_world = Node2D.new()
	_world.name = "Racers"
	add_child(_world)
	_world.draw.connect(_draw_world)
	_hud = Node2D.new()
	_hud.name = "RaceHud"
	add_child(_hud)
	_hud.draw.connect(_draw_hud)
	_controls = Node2D.new()
	_controls.name = "TouchControls"
	add_child(_controls)
	_controls.draw.connect(_draw_controls)


func _build_minimap() -> void:
	_minimap = PackedVector2Array()
	var scale := _minimap_rect.size.x / ReefKartTrack.WORLD_SIZE
	for index in range(0, ReefKartTrack.SAMPLES, 6):
		_minimap.append(_minimap_rect.position + track.center[index] * scale)
	_minimap.append(_minimap[0])


## First deliberate touch starts the countdown; nothing moves before it.
func begin() -> void:
	if state == "grid":
		state = "countdown"
		clock = COUNTDOWN
		_count_mark = 3


func player_progress() -> float:
	return clampf(float(_pl["race_s"]) / track.length, 0.0, float(LAPS))


func imp() -> Dictionary:
	for k: Dictionary in karts:
		if String(k["id"]) == "imp":
			return k
	return karts[mini(1, karts.size() - 1)]


func order() -> Array[Dictionary]:
	var sorted: Array[Dictionary] = karts.duplicate()
	sorted.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		if bool(a["finished"]) != bool(b["finished"]):
			return bool(a["finished"])
		if bool(a["finished"]):
			return float(a["finish_time"]) < float(b["finish_time"])
		return float(a["race_s"]) > float(b["race_s"]))
	return sorted


## The surface publishes its control geometry and finger state here.
func set_controls(next: Dictionary) -> void:
	controls = next
	if _controls != null:
		_controls.queue_redraw()


## One fixed step. `input` carries steer (-1..1), brake and item_pressed.
func step_race(delta: float, input: Dictionary) -> void:
	_time += delta
	flash = maxf(0.0, flash - delta)
	go_t = maxf(0.0, go_t - delta)
	match state:
		"countdown":
			clock -= delta
			var mark := maxi(0, ceili(clock / 0.5))
			if mark < _count_mark:
				_count_mark = mark
				race_event.emit("countdown", float(3 - mark))
			if clock <= 0.0:
				state = "race"
				go_t = GO_SHOW
				race_event.emit("go", 0.0)
		"race":
			race_time += delta
			_step_racers(delta, input)
		"imp_beat":
			clock -= delta
			for k: Dictionary in karts:
				k["speed"] = move_toward(float(k["speed"]), 0.0, BRAKE * 0.6 * delta)
				_move(k, delta)
			if clock <= 0.0:
				_restart_attempt()
		"finished":
			_confetti_t += delta
			for k: Dictionary in karts:
				k["speed"] = move_toward(float(k["speed"]), 0.0, BRAKE * 0.45 * delta)
				_move(k, delta)
	_tick_pickups(delta)
	_update_camera(delta, false)
	_refresh_view()


func _step_racers(delta: float, input: Dictionary) -> void:
	if bool(input.get("item_pressed", false)) and String(_pl["item"]) != "" \
			and float(_pl["roulette_t"]) <= 0.0:
		_use_item(_pl)
	for k: Dictionary in karts:
		if bool(k["finished"]):
			k["speed"] = move_toward(float(k["speed"]), 0.0, BRAKE * 0.45 * delta)
			_move(k, delta)
			continue
		var steer := 0.0
		var braking := false
		if bool(k["player"]):
			steer = _player_steer(k, clampf(float(input.get("steer", 0.0)), -1.0, 1.0), delta)
			braking = bool(input.get("brake", false))
		else:
			steer = _ai_steer(k)
			_ai_items(k, delta)
		_drive(k, steer, braking, delta)
	_separate_karts()
	_tick_projectiles(delta)
	_tick_traps(delta)
	_check_finish()
	_check_lead()


## Tell the surface when the lead changes hands (value 1 = the imp leads).
func _check_lead() -> void:
	if state != "race":
		return
	var front: Dictionary = karts[0]
	for k: Dictionary in karts:
		if float(k["race_s"]) > float(front["race_s"]) + 8.0:
			front = k
	var id := String(front["id"])
	if leader_id == "":
		leader_id = id
	elif id != leader_id:
		leader_id = id
		race_event.emit("lead", 0.0 if bool(front["player"]) else 1.0)


## Child assist: the stick moves the lane she wants and the kart steers itself
## smoothly into that lane and holds it round bends, so it never fights her.
## Below the default assist (0.75) the raw stick blends back in; assist 0 is
## pure manual steering. Facing the wrong way, the kart turns back toward the
## course on its own.
func _player_steer(k: Dictionary, stick: float, delta: float) -> float:
	var guard := ReefKartTrack.ROAD_HALF * 0.74
	var lat_goal := clampf(float(k["lat_goal"]) + stick * LANE_RATE * delta, -guard, guard)
	k["lat_goal"] = lat_goal
	var error := wrapf(track.heading_at(float(k["track_s"])) - float(k["heading"]), -PI, PI)
	if absf(error) > WRONG_WAY:
		if not bool(k["wrong_way"]):
			k["wrong_way"] = true
			race_event.emit("wrong_way", 0.0)
		return signf(error)
	k["wrong_way"] = false
	var follow := _steer_to(k, lat_goal)
	return clampf(lerpf(stick, follow, clampf(assist / 0.75, 0.0, 1.0)), -1.0, 1.0)


## Lane-holding steering: follow the course heading, add a correction toward
## the wanted lateral offset, and feed the bend's curvature forward so the kart
## neither cuts corners nor runs wide. Returns a steer command in -1..1.
func _steer_to(k: Dictionary, lateral: float) -> float:
	var s := float(k["track_s"])
	var speed := float(k["speed"])
	var pace := maxf(speed, 70.0)
	var preview := s + pace * 0.1
	var cross := lateral - float(k["lat"])
	var wanted := track.heading_at(preview) + atan(cross * 1.8 / pace)
	var grip := clampf(speed / 90.0, 0.2, 1.0) * (1.0 - GRIP_LOSS * 0.8)
	# A lane off the centre line bends tighter (inside) or wider (outside).
	var bend := track.curvature_at(preview)
	var lane_bend := bend / maxf(0.3, 1.0 - bend * float(k["lat"]))
	var feed := speed * lane_bend / (TURN_MAX * grip)
	return clampf(feed + wrapf(wanted - float(k["heading"]), -PI, PI) * 2.6, -1.0, 1.0)


func _ai_steer(k: Dictionary) -> float:
	var target := track.racing_lat(float(k["track_s"]) + 90.0)
	k["lat_goal"] = lerpf(float(k["lat_goal"]), target, 0.04)
	return _steer_to(k, float(k["lat_goal"]))


func _top_speed(k: Dictionary, terrain: int) -> float:
	var top := BASE_TOP * float(k["skill"])
	if bool(k["player"]):
		top *= 1.0 + PEARL_BONUS * float(k["pearls"])
	else:
		# Keep the race close without the child noticing: a pull toward Roshan
		# that never lets him pass a kart holding full speed on the road.
		var gap := float(_pl["race_s"]) - float(k["race_s"])
		top *= 1.0 + clampf(gap / 600.0, -0.15, 0.18)
		top *= 1.0 - minf(0.22, absf(track.curvature_at(float(k["track_s"]) + 60.0)) * 40.0)
	if terrain == ReefKartTrack.Terrain.APRON:
		top *= APRON_TOP
	if float(k["boost_t"]) > 0.0:
		top *= BOOST_TOP
	if float(k["slow_t"]) > 0.0:
		top *= 0.55
	if bool(k["player"]):
		top = minf(top, _corner_speed(k, top))
	return top


## Child assist, like traction control: ease off before a bend the kart
## cannot hold at full speed in her lane, scaled by `assist`. Never raises
## speed; the brake still slows her further.
func _corner_speed(k: Dictionary, top: float) -> float:
	if assist <= 0.0:
		return top
	var s := float(k["track_s"])
	var worst := 0.0
	for ahead: float in [40.0, 120.0, 200.0]:
		var bend := track.curvature_at(s + ahead)
		var lane_bend := bend / maxf(0.3, 1.0 - bend * float(k["lat_goal"]))
		worst = maxf(worst, absf(lane_bend))
	if worst < 0.0005:
		return top
	var holdable := TURN_MAX * (1.0 - GRIP_LOSS) / worst
	return lerpf(top, minf(top, holdable), assist)


func _drive(k: Dictionary, steer: float, braking: bool, delta: float) -> void:
	for key: String in ["boost_t", "spin_t", "slow_t", "bump_t"]:
		k[key] = maxf(0.0, float(k[key]) - delta)
	var terrain := track.terrain_at_lat(float(k["lat"]))
	var top := _top_speed(k, terrain)
	var speed := float(k["speed"])
	var accel := ACCEL * (2.4 if float(k["boost_t"]) > 0.0 else 1.0) \
		* (0.6 if terrain == ReefKartTrack.Terrain.APRON else 1.0)
	if float(k["spin_t"]) > 0.0:
		speed = move_toward(speed, 0.0, BRAKE * 0.5 * delta)
		steer = 0.0
		k["spin_vis"] = float(k["spin_vis"]) + delta * 11.0
	elif braking:
		speed = move_toward(speed, 0.0, BRAKE * delta)
	elif speed < top:
		speed = minf(top, speed + accel * delta * (1.0 - 0.55 * speed / maxf(1.0, top)))
	else:
		speed = move_toward(speed, top, 260.0 * delta)
	if float(k["spin_t"]) <= 0.0:
		k["spin_vis"] = 0.0
	var grip := clampf(speed / 90.0, 0.0, 1.0) \
		* (1.0 - GRIP_LOSS * pow(minf(1.0, speed / maxf(1.0, top)), 2.0))
	var turn := steer * TURN_MAX * grip * (1.25 if braking else 1.0)
	k["heading"] = wrapf(float(k["heading"]) + turn * delta, -PI, PI)
	k["steer_vis"] = lerpf(float(k["steer_vis"]), steer, 1.0 - exp(-10.0 * delta))
	k["speed"] = speed
	_move(k, delta)
	_contact_features(k, delta)


func _move(k: Dictionary, delta: float) -> void:
	var forward := Vector2(sin(float(k["heading"])), -cos(float(k["heading"])))
	var pos: Vector2 = k["pos"] as Vector2 + forward * float(k["speed"]) * delta
	var proj := track.project(pos, float(k["track_s"]))
	var lateral := proj.y
	var limit := ReefKartTrack.RAIL - KART_RADIUS
	if absf(lateral) > limit:
		# Soft rail: stop at the rail, slow down, turn along the course.
		pos = track.point_at(proj.x, signf(lateral) * limit)
		lateral = signf(lateral) * limit
		var along := track.heading_at(proj.x)
		if absf(wrapf(float(k["heading"]) - along, -PI, PI)) > PI * 0.5:
			along = wrapf(along + PI, -PI, PI)
		k["heading"] = lerp_angle(float(k["heading"]), along, 0.5)
		k["speed"] = float(k["speed"]) * 0.55
		if float(k["bump_t"]) <= 0.0:
			k["bump_t"] = 0.35
			if bool(k["player"]):
				race_event.emit("bump", 0.0)
	var ds := wrapf(proj.x - float(k["track_s"]), -track.length * 0.5, track.length * 0.5)
	k["race_s"] = float(k["race_s"]) + ds
	k["track_s"] = proj.x
	k["lat"] = lateral
	k["pos"] = pos
	var lap := maxi(0, floori(float(k["race_s"]) / track.length))
	if lap > int(k["lap"]):
		k["lap"] = lap
		if bool(k["player"]) and lap < LAPS:
			race_event.emit("lap", float(lap))


## Karts nudge apart sideways instead of overlapping; nobody loses speed.
func _separate_karts() -> void:
	for a in range(karts.size()):
		for b in range(a + 1, karts.size()):
			var pa: Vector2 = karts[a]["pos"]
			var pb: Vector2 = karts[b]["pos"]
			var gap := pa.distance_to(pb)
			if gap >= KART_RADIUS * 2.0 or gap < 0.001:
				continue
			var push := (pb - pa) / gap * (KART_RADIUS * 2.0 - gap) * 0.5
			karts[a]["pos"] = pa - push
			karts[b]["pos"] = pb + push


func _contact_features(k: Dictionary, delta: float) -> void:
	var pos: Vector2 = k["pos"]
	if bool(k["player"]):
		# Pearls are Roshan's alone: the imp drives through them untouched.
		for pearl: Dictionary in track.pearls:
			if float(pearl["respawn_t"]) <= 0.0 \
					and pos.distance_to(pearl["pos"] as Vector2) <= PICK_RADIUS:
				pearl["respawn_t"] = 8.0
				if int(k["pearls"]) < MAX_PEARLS:
					k["pearls"] = int(k["pearls"]) + 1
				race_event.emit("pearl", float(k["pearls"]))
	for source: Array in [track.bubbles, track.buoys]:
		for bubble: Dictionary in source:
			if float(bubble["respawn_t"]) <= 0.0 \
					and pos.distance_to(bubble["pos"] as Vector2) <= PICK_RADIUS + 6.0:
				bubble["respawn_t"] = 3.0
				if String(k["item"]) == "" and float(k["roulette_t"]) <= 0.0:
					k["roulette_t"] = ROULETTE
					k["pending"] = _pick_item(k)
					if bool(k["player"]):
						race_event.emit("item_roll", 0.0)
	if float(k["roulette_t"]) > 0.0:
		k["roulette_t"] = maxf(0.0, float(k["roulette_t"]) - delta)
		if float(k["roulette_t"]) <= 0.0:
			k["item"] = k["pending"]
			k["pending"] = ""
			k["ai_item_t"] = 0.0
			if bool(k["player"]):
				race_event.emit("item_ready", float(ITEM_KINDS.find(String(k["item"]))))


## Position-weighted draws keep the race close: whoever is behind is more
## likely to get a boost. The imp only ever receives zoom or kelp.
func _pick_item(k: Dictionary) -> String:
	var behind := float(k["race_s"]) < float(_other_leader(k)["race_s"])
	var roll := rng.randf()
	if not bool(k["player"]):
		return "zoom" if behind or roll < 0.5 else "kelp"
	if behind:
		if roll < 0.5:
			return "zoom"
		if roll < 0.85:
			return "sparkle"
		return "pearls"
	if roll < 0.35:
		return "kelp"
	if roll < 0.7:
		return "pearls"
	return "zoom"


func _other_leader(k: Dictionary) -> Dictionary:
	var best: Dictionary = k
	for other: Dictionary in karts:
		if not is_same(other, k) and float(other["race_s"]) > float(best["race_s"]):
			best = other
	return best


func _use_item(k: Dictionary) -> void:
	var kind := String(k["item"])
	k["item"] = ""
	var forward := Vector2(sin(float(k["heading"])), -cos(float(k["heading"])))
	match kind:
		"zoom":
			k["boost_t"] = maxf(float(k["boost_t"]), 1.4)
			if bool(k["player"]):
				turbo_count += 1
				flash = 0.5
				race_event.emit("turbo", float(turbo_count))
		"sparkle":
			projectiles.append({"owner": k, "s": float(k["track_s"]) + 30.0,
				"lat": float(k["lat"]), "speed": maxf(float(k["speed"]) + 260.0, SPARKLE_SPEED),
				"life": 3.5, "pos": k["pos"] as Vector2 + forward * 30.0})
			if bool(k["player"]):
				race_event.emit("item_used", 1.0)
		"kelp":
			traps.append({"owner": k, "pos": k["pos"] as Vector2 - forward * 48.0,
				"life": 22.0, "armed_t": 0.6})
			if bool(k["player"]):
				race_event.emit("item_used", 2.0)
		"pearls":
			k["pearls"] = mini(MAX_PEARLS, int(k["pearls"]) + 3)
			if bool(k["player"]):
				race_event.emit("pearl", float(k["pearls"]))


## The imp boosts and drops kelp behind him; he never aims at Roshan.
func _ai_items(k: Dictionary, delta: float) -> void:
	if String(k["item"]) == "":
		return
	k["ai_item_t"] = float(k["ai_item_t"]) + delta
	if String(k["item"]) not in ["zoom", "kelp"]:
		k["item"] = "zoom"
	if String(k["item"]) == "zoom" and float(k["ai_item_t"]) >= 0.3:
		_use_item(k)
	elif String(k["item"]) == "kelp" and float(k["ai_item_t"]) >= 1.2:
		_use_item(k)


func _tick_projectiles(delta: float) -> void:
	for index in range(projectiles.size() - 1, -1, -1):
		var p := projectiles[index]
		p["life"] = float(p["life"]) - delta
		p["s"] = float(p["s"]) + float(p["speed"]) * delta
		var target := _next_ahead(p["owner"] as Dictionary, float(p["s"]))
		if not target.is_empty():
			p["lat"] = move_toward(float(p["lat"]), float(target["lat"]), 150.0 * delta)
		p["pos"] = track.point_at(float(p["s"]), float(p["lat"]))
		var hit := false
		for k: Dictionary in karts:
			if is_same(k, p["owner"]):
				continue
			if (k["pos"] as Vector2).distance_to(p["pos"] as Vector2) <= KART_RADIUS + 16.0:
				k["spin_t"] = 1.0
				k["speed"] = float(k["speed"]) * 0.45
				race_event.emit("bonk", 0.0 if bool(k["player"]) else 1.0)
				hit = true
				break
		if hit or float(p["life"]) <= 0.0:
			projectiles.remove_at(index)


func _next_ahead(owner: Dictionary, s: float) -> Dictionary:
	var best: Dictionary = {}
	var best_gap := 1200.0
	for k: Dictionary in karts:
		if is_same(k, owner):
			continue
		var gap := wrapf(float(k["track_s"]) - track.wrap_s(s), 0.0, track.length)
		if gap < best_gap:
			best_gap = gap
			best = k
	return best


func _tick_traps(delta: float) -> void:
	for index in range(traps.size() - 1, -1, -1):
		var t := traps[index]
		t["life"] = float(t["life"]) - delta
		t["armed_t"] = maxf(0.0, float(t["armed_t"]) - delta)
		var used := false
		for k: Dictionary in karts:
			if is_same(k, t["owner"]) and float(t["armed_t"]) > 0.0:
				continue
			if (k["pos"] as Vector2).distance_to(t["pos"] as Vector2) <= KART_RADIUS + 14.0:
				k["slow_t"] = 0.9
				k["speed"] = float(k["speed"]) * 0.6
				used = true
				if bool(k["player"]):
					race_event.emit("slip", 0.0)
				break
		if used or float(t["life"]) <= 0.0:
			traps.remove_at(index)


func _tick_pickups(delta: float) -> void:
	if state != "race":
		return
	for pearl: Dictionary in track.pearls:
		pearl["respawn_t"] = maxf(0.0, float(pearl["respawn_t"]) - delta)
	for source: Array in [track.bubbles, track.buoys]:
		for bubble: Dictionary in source:
			bubble["respawn_t"] = maxf(0.0, float(bubble["respawn_t"]) - delta)


func _check_finish() -> void:
	var goal := track.length * float(LAPS)
	var imp_kart := imp()
	# The imp's one scripted mistake: a spin early in the second lap.
	if not bool(imp_kart["flubbed"]) and float(imp_kart["race_s"]) >= track.length * 1.12:
		imp_kart["flubbed"] = true
		imp_kart["spin_t"] = 1.5
		race_event.emit("imp_flub", 0.0)
	if float(_pl["race_s"]) >= goal and not bool(_pl["finished"]):
		# Ties go to Roshan: she is checked first in the same step.
		_pl["finished"] = true
		_pl["finish_time"] = race_time
		_pl["race_s"] = goal
		state = "finished"
		race_event.emit("finish", 1.0)
		return
	for k: Dictionary in karts:
		if bool(k["player"]) or bool(k["finished"]):
			continue
		if float(k["race_s"]) >= goal:
			k["finished"] = true
			k["finish_time"] = race_time
			if is_same(k, imp_kart):
				imp_wins += 1
				state = "imp_beat"
				clock = IMP_BEAT
				race_event.emit("imp_win", float(imp_wins))
				return


func _restart_attempt() -> void:
	attempt += 1
	projectiles.clear()
	traps.clear()
	for pearl: Dictionary in track.pearls:
		pearl["respawn_t"] = 0.0
	for source: Array in [track.bubbles, track.buoys]:
		for bubble: Dictionary in source:
			bubble["respawn_t"] = 0.0
	# Earned pearls stay with Roshan; only the race itself resets.
	var kept := int(_pl["pearls"])
	_place_grid()
	_pl["pearls"] = kept
	var imp_kart := imp()
	var pace := 1.0
	if imp_wins >= 2:
		pace = MERCY_PACE
	elif imp_wins == 1:
		pace = RETRY_PACE
	imp_kart["skill"] = float(imp_kart["base_skill"]) * pace
	race_time = 0.0
	leader_id = ""
	state = "countdown"
	clock = COUNTDOWN
	_count_mark = 3
	_update_camera(1.0, true)
	race_event.emit("restart", float(attempt))


func _update_camera(delta: float, snap: bool) -> void:
	var target := float(_pl["heading"])
	if snap:
		cam_heading = target
	else:
		cam_heading = lerp_angle(cam_heading, target, 1.0 - exp(-7.5 * delta))
	var forward := Vector2(sin(cam_heading), -cos(cam_heading))
	cam_pos = (_pl["pos"] as Vector2) - forward * CAM_BACK


func _refresh_view() -> void:
	if _floor_material == null:
		return
	var forward := Vector2(sin(cam_heading), -cos(cam_heading))
	_floor_material.set_shader_parameter("cam_pos", cam_pos)
	_floor_material.set_shader_parameter("cam_forward", forward)
	_floor_material.set_shader_parameter("cam_right", Vector2(-forward.y, forward.x))
	_floor_material.set_shader_parameter("time", _time)
	_sky.queue_redraw()
	_world.queue_redraw()
	_hud.queue_redraw()
	_controls.queue_redraw()


func _depth(world: Vector2) -> float:
	return (world - cam_pos).dot(Vector2(sin(cam_heading), -cos(cam_heading)))


## World point to screen; points behind the camera clamp to the near plane.
func screen_of(world: Vector2) -> Vector2:
	return _screen(world, maxf(NEAR, _depth(world)))


func _screen(world: Vector2, depth: float) -> Vector2:
	var forward := Vector2(sin(cam_heading), -cos(cam_heading))
	var lateral := (world - cam_pos).dot(Vector2(-forward.y, forward.x))
	return Vector2(VIEW.x * 0.5 + lateral * FOCAL / depth, HORIZON_Y + CAM_HEIGHT * FOCAL / depth)


func _draw_sky() -> void:
	_sky.draw_rect(Rect2(Vector2.ZERO, Vector2(VIEW.x, HORIZON_Y + 2.0)), SKY_WATER)
	var band_y := HORIZON_Y - SKY_BAND + 2.0
	if _skyline != null:
		# Painted 360-degree band from the Codex packet: one seamless loop.
		var x := -fposmod(cam_heading / TAU * SKY_LOOP, SKY_LOOP)
		while x < VIEW.x:
			_sky.draw_texture_rect_region(_skyline, Rect2(x, band_y, SKY_LOOP, SKY_BAND),
				SKYLINE_SOURCE)
			x += SKY_LOOP
		return
	if _sky_tex.size() != PALACE_TILES.size():
		return
	var total := SKY_LOOP
	var copy := total / float(SKY_COPIES)
	var piece := copy / float(PALACE_TILES.size())
	var offset := fposmod(cam_heading / TAU * total, total)
	var first := int(floor(offset / copy))
	var x := -(offset - float(first) * copy)
	var index := first
	while x < VIEW.x:
		var mirrored := index % 2 == 1
		for part in range(PALACE_TILES.size()):
			var slot := part if not mirrored else PALACE_TILES.size() - 1 - part
			var at := Vector2(x + float(part) * piece, band_y)
			if mirrored:
				_sky.draw_set_transform(at + Vector2(piece, 0.0), 0.0, Vector2(-1.0, 1.0))
				_sky.draw_texture_rect_region(_sky_tex[slot],
					Rect2(Vector2.ZERO, Vector2(piece, SKY_BAND)), PALACE_SOURCES[slot])
				_sky.draw_set_transform(Vector2.ZERO)
			else:
				_sky.draw_texture_rect_region(_sky_tex[slot],
					Rect2(at, Vector2(piece, SKY_BAND)), PALACE_SOURCES[slot])
		x += copy
		index += 1


func _draw_world() -> void:
	_drawables.clear()
	for index in range(track.pearls.size()):
		var pearl := track.pearls[index]
		if float(pearl["respawn_t"]) <= 0.0:
			_queue_drawable(pearl["pos"] as Vector2, "pearl", index)
	for index in range(track.bubbles.size()):
		var bubble := track.bubbles[index]
		if float(bubble["respawn_t"]) <= 0.0:
			_queue_drawable(bubble["pos"] as Vector2, "bubble", index)
	for index in range(track.buoys.size()):
		_queue_drawable(track.buoys[index]["pos"] as Vector2, "buoy", index)
	for index in range(track.landmarks.size()):
		var landmark: Dictionary = track.landmarks[index]
		if bool(landmark.get("spans", false)):
			_queue_drawable(landmark["pos"] as Vector2, "span", index)
		elif _landmark_tex.has(String(landmark["id"])):
			_queue_drawable(landmark["pos"] as Vector2, "landmark", index)
	for index in range(traps.size()):
		_queue_drawable(traps[index]["pos"] as Vector2, "kelp", index)
	for index in range(projectiles.size()):
		_queue_drawable(projectiles[index]["pos"] as Vector2, "sparkle", index)
	for index in range(karts.size()):
		_queue_drawable(karts[index]["pos"] as Vector2, "kart", index)
	_drawables.sort_custom(func(a: Array, b: Array) -> bool: return float(a[0]) > float(b[0]))
	for entry: Array in _drawables:
		var depth := float(entry[0])
		var screen := _screen(entry[3] as Vector2, depth)
		var scale := FOCAL / depth
		match String(entry[1]):
			"pearl":
				_draw_pearl(screen, scale)
			"bubble":
				_draw_bubble(screen, scale)
			"buoy":
				_draw_buoy(track.buoys[int(entry[2])], screen, scale)
			"span":
				_draw_span(track.landmarks[int(entry[2])], scale)
			"kelp":
				_draw_kelp(screen, scale)
			"sparkle":
				_draw_sparkle(screen, scale)
			"landmark":
				_draw_landmark(track.landmarks[int(entry[2])], screen, scale)
			"kart":
				_draw_kart(karts[int(entry[2])], screen, scale)


func _queue_drawable(world: Vector2, kind: String, index: int) -> void:
	var depth := _depth(world)
	if depth < NEAR or depth > FAR:
		return
	_drawables.append([depth, kind, index, world])


## An isolated painted landmark standing upright beside the road.
func _draw_landmark(landmark: Dictionary, screen: Vector2, scale: float) -> void:
	var texture := _landmark_tex.get(String(landmark["id"])) as Texture2D
	if texture == null:
		return
	var size := Vector2(float(landmark["w"]), float(landmark["h"])) * scale
	if size.x < 3.0:
		return
	var bottom := screen.y - float(landmark.get("lift", 0.0)) * scale
	_world.draw_texture_rect(texture,
		Rect2(screen.x - size.x * 0.5, bottom - size.y, size.x, size.y), false)


func _draw_pearl(screen: Vector2, scale: float) -> void:
	var r := maxf(2.0, 7.0 * scale)
	var at := screen - Vector2(0.0, (11.0 + sin(_time * 3.0) * 2.0) * scale)
	_world.draw_circle(screen, r * 0.8, Color(0.18, 0.12, 0.3, 0.18))
	if _draw_art("pearl", at, Vector2(r, r) * 2.3):
		return
	_world.draw_circle(at, r, Color("#fff4e2"))
	_world.draw_circle(at + Vector2(r * 0.15, r * 0.2), r * 0.72, Color("#f4dcef"))
	_world.draw_circle(at - Vector2(r * 0.3, r * 0.35), r * 0.28, Color.WHITE)


func _draw_bubble(screen: Vector2, scale: float) -> void:
	var r := maxf(3.0, 16.0 * scale)
	var at := screen - Vector2(0.0, (24.0 + sin(_time * 2.2) * 3.0) * scale)
	if _draw_art("item_bubble", at, Vector2(r, r) * 2.2):
		return
	_world.draw_circle(at, r, Color(0.85, 0.95, 1.0, 0.42))
	for band in range(3):
		var hue := fposmod(_time * 0.2 + float(band) * 0.33, 1.0)
		_world.draw_arc(at, r * (0.92 - float(band) * 0.1), 0.0, TAU, 32,
			Color.from_hsv(hue, 0.45, 1.0, 0.9), maxf(1.0, r * 0.09), true)
	_draw_star(_world, at, r * 0.42, Color("#fff2a8"))
	_world.draw_circle(at - Vector2(r * 0.42, r * 0.45), r * 0.16, Color.WHITE)


func _draw_star(canvas: CanvasItem, at: Vector2, r: float, color: Color) -> void:
	var points := PackedVector2Array()
	for i in range(10):
		var radius := r if i % 2 == 0 else r * 0.45
		var angle := -PI * 0.5 + TAU * float(i) / 10.0
		points.append(at + Vector2(cos(angle), sin(angle)) * radius)
	canvas.draw_colored_polygon(points, color)


## Centered texture draw for an optional art role; false when it is missing.
func _draw_art(key: String, center: Vector2, size: Vector2) -> bool:
	var texture := _tex.get(key) as Texture2D
	if texture == null:
		return false
	_world.draw_texture_rect(texture, Rect2(center - size * 0.5, size), false)
	return true


## An arch over the lane: the painted card when Codex has isolated it from the
## painting, otherwise an INTERIM_PLACEHOLDER arch in the painting's colours
## (cream shell arch with pearls at the start, pink checkered ribbon, lilac
## pearl arches over the back straight).
func _draw_span(landmark: Dictionary, scale: float) -> void:
	var s := float(landmark["s"])
	var half := float(landmark["w"]) * 0.5
	var left := track.point_at(s, -half)
	var right := track.point_at(s, half)
	var dl := _depth(left)
	var dr := _depth(right)
	if dl < NEAR or dr < NEAR:
		return
	var base_l := _screen(left, dl)
	var base_r := _screen(right, dr)
	var width_px := base_r.x - base_l.x
	if width_px < 4.0:
		return
	var id := String(landmark["id"])
	var art := _landmark_tex.get(id) as Texture2D
	var ground := maxf(base_l.y, base_r.y)
	if art != null:
		var height := width_px * float(landmark["h"]) / float(landmark["w"])
		_world.draw_texture_rect(art, Rect2(base_l.x, ground - height, width_px, height), false)
		return
	var tall := float(landmark["h"]) * 0.78
	var top_l := base_l - Vector2(0.0, tall * FOCAL / dl)
	var top_r := base_r - Vector2(0.0, tall * FOCAL / dr)
	var post := maxf(2.0, 16.0 * scale)
	var stone := Color("#f3e6cf")
	var trim := Color("#c9a8f0")
	if id == "pearl_arch":
		stone = Color("#c9b3ea")
		trim = Color("#f4eefa")
	for pair: Array in [[base_l, top_l], [base_r, top_r]]:
		_world.draw_line(pair[0], pair[1], INK, post + 4.0, true)
		_world.draw_line(pair[0], pair[1], stone, post, true)
	if id == "ribbon_arch":
		# Pink-and-white checkered ribbon strung low across the lane.
		var rib_l := base_l.lerp(top_l, 0.42)
		var rib_r := base_r.lerp(top_r, 0.42)
		var cells := 10
		var thick := maxf(2.0, 14.0 * scale)
		for i in range(cells):
			var a := rib_l.lerp(rib_r, float(i) / float(cells))
			var b := rib_l.lerp(rib_r, float(i + 1) / float(cells))
			_world.draw_line(a, b, Color("#f07ab8") if i % 2 == 0 else Color("#fff4f8"), thick, true)
		return
	var arch := PackedVector2Array()
	for i in range(17):
		var t := float(i) / 16.0
		var p := top_l.lerp(top_r, t)
		p.y -= sin(t * PI) * (top_r.x - top_l.x) * 0.22
		arch.append(p)
	_world.draw_polyline(arch, INK, post + 4.0, true)
	_world.draw_polyline(arch, stone, post, true)
	for i in range(1, 16, 2):
		_world.draw_circle(arch[i], maxf(1.5, post * 0.32), trim)


## A gem buoy on its pearl-ringed float; its orb pops when a kart takes it.
func _draw_buoy(buoy: Dictionary, screen: Vector2, scale: float) -> void:
	var color: Color = BUOY_COLORS.get(String(buoy["color"]), Color.WHITE)
	var key := "gem_buoy_" + String(buoy["color"])
	var ready := float(buoy["respawn_t"]) <= 0.0
	if _tex.has(key):
		# The painted buoy fades while its orb is popped, then returns whole.
		var size := Vector2(56.0, 60.0) * scale
		_world.draw_texture_rect(_tex[key] as Texture2D,
			Rect2(screen - Vector2(size.x * 0.5, size.y - 4.0 * scale), size), false,
			Color(1.0, 1.0, 1.0, 1.0 if ready else 0.35))
		return
	_world.draw_set_transform(screen, 0.0, Vector2(1.0, 0.36))
	_world.draw_circle(Vector2.ZERO, maxf(3.0, 26.0 * scale), INK)
	_world.draw_circle(Vector2.ZERO, maxf(2.0, 23.0 * scale), Color("#c9b3ea"))
	_world.draw_set_transform(Vector2.ZERO)
	var ring := screen - Vector2(0.0, 16.0 * scale)
	_world.draw_arc(ring, maxf(2.0, 13.0 * scale), PI, TAU, 16, Color("#e7c06a"), maxf(1.0, 4.0 * scale), true)
	if not ready:
		return
	var orb := screen - Vector2(0.0, (34.0 + sin(_time * 2.6) * 2.0) * scale)
	var r := maxf(2.0, 12.0 * scale)
	_world.draw_circle(orb, r + maxf(1.0, 2.0 * scale), INK)
	_world.draw_circle(orb, r, color)
	_world.draw_circle(orb - Vector2(r * 0.35, r * 0.35), r * 0.3, Color(1.0, 1.0, 1.0, 0.8))


func _draw_kelp(screen: Vector2, scale: float) -> void:
	if _draw_art("kelp", screen - Vector2(0.0, 6.0 * scale), Vector2(52.0, 22.0) * scale):
		return
	_world.draw_set_transform(screen, 0.0, Vector2(1.0, 0.34))
	_world.draw_circle(Vector2.ZERO, maxf(3.0, 24.0 * scale), Color("#4fa36b"))
	_world.draw_circle(Vector2(6.0 * scale, -4.0 * scale), maxf(2.0, 14.0 * scale), Color("#77c98a"))
	_world.draw_set_transform(Vector2.ZERO)


func _draw_sparkle(screen: Vector2, scale: float) -> void:
	var r := maxf(3.0, 14.0 * scale)
	var at := screen - Vector2(0.0, 18.0 * scale)
	if _draw_art("sparkle", at, Vector2(r, r) * 2.4):
		return
	_world.draw_circle(at, r, Color(1.0, 0.92, 0.6, 0.55))
	_draw_star(_world, at, r * 0.9, Color("#fff8c8"))


func _draw_kart(k: Dictionary, screen: Vector2, scale: float) -> void:
	var size := KART_SPRITE * scale
	_world.draw_set_transform(screen, 0.0, Vector2(1.0, 0.3))
	_world.draw_circle(Vector2.ZERO, size * 0.42, Color(0.15, 0.1, 0.28, 0.24))
	_world.draw_set_transform(Vector2.ZERO)
	var center := screen - Vector2(0.0, size * 0.42)
	var wobble := sin(float(k["spin_vis"])) * 0.45
	_world.draw_set_transform(center, wobble, Vector2.ONE)
	var rect := Rect2(-size * 0.5, -size * 0.44, size, size)
	if bool(k["player"]):
		var key := "kart_straight"
		if float(k["boost_t"]) > 0.0:
			key = "kart_boost"
		elif float(k["steer_vis"]) > 0.35:
			key = "kart_right"
		elif float(k["steer_vis"]) < -0.35:
			key = "kart_left"
		var texture := _tex.get(key) as Texture2D
		if texture != null:
			_world.draw_texture_rect(texture, rect, false)
	elif _tex.has("imp_kart_straight"):
		var imp_key := "imp_kart_straight"
		if float(k["steer_vis"]) > 0.35 and _tex.has("imp_kart_right"):
			imp_key = "imp_kart_right"
		elif float(k["steer_vis"]) < -0.35 and _tex.has("imp_kart_left"):
			imp_key = "imp_kart_left"
		_world.draw_texture_rect(_tex[imp_key] as Texture2D, rect, false, IMP_TINT)
	else:
		var body := _tex.get("kart_empty") as Texture2D
		var face := _tex.get("imp") as Texture2D
		if face != null:
			var head := size * 0.42
			_world.draw_texture_rect_region(face,
				Rect2(-head * 0.5, rect.position.y + size * 0.02, head, head * IMP_FACE.size.y / IMP_FACE.size.x),
				IMP_FACE)
		if body != null:
			_world.draw_texture_rect(body, rect.grow(-size * 0.04), false, IMP_TINT)
	_world.draw_set_transform(Vector2.ZERO)
	if float(k["spin_t"]) > 0.0:
		var dizzy := _tex.get("dizzy") as Texture2D
		var over := center - Vector2(0.0, size * 0.55)
		if dizzy != null:
			_world.draw_texture_rect(dizzy, Rect2(over - Vector2(size * 0.4, size * 0.2),
				Vector2(size * 0.8, size * 0.4)), false)
		else:
			for i in range(3):
				var angle := _time * 6.0 + TAU * float(i) / 3.0
				_draw_star(_world, over + Vector2(cos(angle) * size * 0.32, sin(angle) * size * 0.1),
					size * 0.07, Color("#ffe27a"))
	if bool(k["player"]) and float(k["boost_t"]) > 0.0:
		for i in range(5):
			var y := screen.y - size * (0.1 + float(i) * 0.09)
			var spread := size * (0.55 + float(i) * 0.08)
			_world.draw_line(Vector2(screen.x - spread, y + size * 0.4),
				Vector2(screen.x - spread * 1.35, y + size * 0.6), Color(1, 1, 1, 0.55), 3.0)
			_world.draw_line(Vector2(screen.x + spread, y + size * 0.4),
				Vector2(screen.x + spread * 1.35, y + size * 0.6), Color(1, 1, 1, 0.55), 3.0)


func _draw_hud() -> void:
	for lap in range(LAPS):
		var center := Vector2(190.0 + float(lap) * 88.0, 68.0)
		var done := player_progress() >= float(lap + 1)
		_hud.draw_circle(center, 35.0, INK)
		_hud.draw_circle(center, 29.0, Color("#ffe2a0") if done else Color("#e7ddef"))
		var fraction := clampf(player_progress() - float(lap), 0.0, 1.0)
		if fraction > 0.001:
			_hud.draw_arc(center, 32.0, -PI * 0.5, -PI * 0.5 + TAU * fraction, 48, Color("#71d7d0"), 7.0, true)
		_hud.draw_line(center + Vector2(-10, 12), center + Vector2(-10, -13), Color("#655078"), 4.0, true)
		_hud.draw_colored_polygon(PackedVector2Array([center + Vector2(-8, -12),
			center + Vector2(13, -7), center + Vector2(-8, 0)]),
			Color("#ee91b7") if done else Color("#8ccfd1"))
	for index in range(MAX_PEARLS):
		var at := Vector2(160.0 + float(index) * 22.0, 124.0)
		var got := index < int(_pl["pearls"])
		_hud.draw_circle(at, 9.0, INK)
		_hud.draw_circle(at, 6.5, Color("#fff4e2") if got else Color(0.75, 0.7, 0.82, 0.6))
	_draw_order_faces()
	_draw_minimap()
	if state == "countdown":
		for index in range(3):
			var lit := clock <= COUNTDOWN - float(index) * 0.5
			_hud.draw_circle(Vector2(550.0 + float(index) * 90.0, 200.0), 30.0, INK)
			_hud.draw_circle(Vector2(550.0 + float(index) * 90.0, 200.0), 24.0,
				Color("#ffe5a8") if lit else Color("#9abcc8"))
	if go_t > 0.0:
		var grow := 1.0 + (1.0 - go_t / GO_SHOW) * 0.4
		_hud.draw_circle(Vector2(640.0, 200.0), 48.0 * grow, INK)
		_hud.draw_circle(Vector2(640.0, 200.0), 42.0 * grow, Color("#7ee08f"))
		_hud.draw_colored_polygon(PackedVector2Array([Vector2(622.0, 176.0),
			Vector2(666.0, 200.0), Vector2(622.0, 224.0)]), Color.WHITE)
	if bool(_pl["wrong_way"]):
		_draw_turn_arrow()
	if state == "imp_beat":
		var face := _tex.get("imp") as Texture2D
		if face != null:
			var bounce := absf(sin(_time * 9.0)) * 18.0
			_hud.draw_texture_rect_region(face, Rect2(560.0, 140.0 - bounce, 160.0, 150.0), IMP_FACE)
	if state == "finished":
		for i in range(28):
			var x := fposmod(float(i) * 97.0 + _confetti_t * 60.0, VIEW.x)
			var y := fposmod(float(i) * 53.0 + _confetti_t * 210.0, VIEW.y * 0.7)
			_hud.draw_rect(Rect2(x, y, 10.0, 14.0), Color.from_hsv(fposmod(float(i) * 0.13, 1.0), 0.5, 1.0))
	if flash > 0.0:
		_hud.draw_rect(Rect2(Vector2.ZERO, VIEW), Color(1.0, 1.0, 1.0, flash * 0.18))


## Facing the wrong way: a big bouncing arrow shows which way the course goes.
func _draw_turn_arrow() -> void:
	var error := wrapf(track.heading_at(float(_pl["track_s"])) - float(_pl["heading"]), -PI, PI)
	var side := signf(error)
	var bob := sin(_time * 8.0) * 10.0
	var center := Vector2(640.0 + side * (60.0 + bob), 190.0)
	var points := PackedVector2Array([
		center + Vector2(-60.0 * side, -22.0), center + Vector2(10.0 * side, -22.0),
		center + Vector2(10.0 * side, -50.0), center + Vector2(70.0 * side, 0.0),
		center + Vector2(10.0 * side, 50.0), center + Vector2(10.0 * side, 22.0),
		center + Vector2(-60.0 * side, 22.0)])
	var outline := points.duplicate()
	outline.append(points[0])
	_hud.draw_colored_polygon(points, Color("#ffd36b"))
	_hud.draw_polyline(outline, INK, 6.0, true)


func _draw_order_faces() -> void:
	var sorted := order()
	for index in range(mini(2, sorted.size())):
		var k := sorted[index]
		var at := Vector2(565.0 + float(index) * 150.0, 22.0)
		var texture := _tex.get("roshan" if bool(k["player"]) else "imp") as Texture2D
		var region := ROSHAN_FACE if bool(k["player"]) else IMP_FACE
		var side := 86.0 if index == 0 else 70.0
		_hud.draw_circle(at + Vector2(side, side) * 0.5, side * 0.58, INK)
		_hud.draw_circle(at + Vector2(side, side) * 0.5, side * 0.53,
			Color("#ffe27a") if index == 0 else Color("#e7ddef"))
		if texture != null:
			_hud.draw_texture_rect_region(texture, Rect2(at, Vector2(side, side)), region)


func _draw_minimap() -> void:
	_hud.draw_rect(_minimap_rect.grow(10.0), Color(1.0, 1.0, 1.0, 0.55))
	_hud.draw_polyline(_minimap, INK, 9.0, true)
	_hud.draw_polyline(_minimap, Color("#f4e6f0"), 5.0, true)
	var scale := _minimap_rect.size.x / ReefKartTrack.WORLD_SIZE
	for k: Dictionary in karts:
		var at := _minimap_rect.position + (k["pos"] as Vector2) * scale
		_hud.draw_circle(at, 8.0, INK)
		_hud.draw_circle(at, 6.0, Color("#ff9db6") if bool(k["player"]) else Color("#b48ce8"))


## Green steering stick (left), red brake and the item bubble (right).
func _draw_controls() -> void:
	if controls.is_empty():
		return
	var base: Vector2 = controls.get("stick_base", Vector2(230, 540))
	var knob: Vector2 = controls.get("stick_knob", base)
	var stick_r := float(controls.get("stick_radius", 104.0))
	var stick_held := bool(controls.get("stick_held", false))
	_controls.draw_circle(base, stick_r + 5.0, Color(INK, 0.55))
	_controls.draw_circle(base, stick_r, Color(0.37, 0.81, 0.48, 0.38 if stick_held else 0.28))
	_controls.draw_arc(base, stick_r - 4.0, 0.0, TAU, 48, Color("#2f6b46"), 5.0, true)
	for side: float in [-1.0, 1.0]:
		var tip := base + Vector2(side * (stick_r - 18.0), 0.0)
		_controls.draw_colored_polygon(PackedVector2Array([tip,
			tip + Vector2(-side * 22.0, -16.0), tip + Vector2(-side * 22.0, 16.0)]),
			Color(1.0, 1.0, 1.0, 0.85))
	_controls.draw_circle(knob, 52.0, INK)
	_controls.draw_circle(knob, 47.0, Color("#5fcf7a") if not stick_held else Color("#7ee08f"))
	_controls.draw_circle(knob - Vector2(14.0, 16.0), 13.0, Color(1.0, 1.0, 1.0, 0.5))
	var brake_at: Vector2 = controls.get("brake_center", Vector2(1175, 625))
	var brake_r := float(controls.get("brake_radius", 80.0))
	var brake_held := bool(controls.get("brake_held", false))
	var brake_draw := brake_r * (0.92 if brake_held else 1.0)
	_controls.draw_circle(brake_at, brake_draw + 5.0, INK)
	_controls.draw_circle(brake_at, brake_draw, Color("#c93a52") if brake_held else Color("#ef5a6f"))
	_controls.draw_circle(brake_at - Vector2(brake_draw * 0.3, brake_draw * 0.32),
		brake_draw * 0.22, Color(1.0, 1.0, 1.0, 0.35))
	_controls.draw_rect(Rect2(brake_at - Vector2(brake_draw * 0.42, brake_draw * 0.13),
		Vector2(brake_draw * 0.84, brake_draw * 0.26)), Color.WHITE)
	_draw_item_bubble()
	if bool(controls.get("guide", false)):
		var hand := _tex.get("guide_hand") as Texture2D
		if hand != null:
			var sway := sin(_time * 2.4) * stick_r * 0.45
			var tip := Vector2(base.x + sway, base.y)
			var side := 104.0
			_controls.draw_texture_rect(hand, Rect2(tip - GUIDE_TIP * side, Vector2(side, side)), false)


func _draw_item_bubble() -> void:
	var at: Vector2 = controls.get("bubble_center", Vector2(1010, 505))
	var radius := float(controls.get("bubble_radius", 70.0))
	var held := bool(controls.get("bubble_held", false))
	var item := String(_pl["item"])
	var rolling := float(_pl["roulette_t"]) > 0.0
	var ready := item != "" and not rolling
	var lit := ready or rolling
	var pulse := 1.0 + (sin(_time * 5.0) * 0.05 if ready else 0.0)
	var r := radius * pulse * (0.93 if held else 1.0)
	_controls.draw_circle(at, r + 5.0, Color(INK, 0.85 if lit else 0.4))
	_controls.draw_circle(at, r, Color(0.85, 0.95, 1.0, 0.55 if lit else 0.22))
	for band in range(3):
		var hue := fposmod(_time * 0.25 + float(band) * 0.33, 1.0)
		_controls.draw_arc(at, r * (0.94 - float(band) * 0.07), 0.0, TAU, 40,
			Color.from_hsv(hue, 0.4, 1.0, 0.9 if lit else 0.35), 4.0, true)
	var shown := item
	if rolling:
		shown = ITEM_KINDS[int(floor(_time * 12.0)) % ITEM_KINDS.size()]
	if shown != "":
		_draw_item_icon(shown, at, r * 0.55)
	_controls.draw_circle(at - Vector2(r * 0.42, r * 0.45), r * 0.13, Color(1.0, 1.0, 1.0, 0.8))


func _draw_item_icon(kind: String, at: Vector2, r: float) -> void:
	var icon := _tex.get("icon_" + kind) as Texture2D
	if icon != null:
		_controls.draw_texture_rect(icon, Rect2(at - Vector2(r, r), Vector2(r, r) * 2.0), false)
		return
	match kind:
		"zoom":
			for offset: float in [-0.35, 0.25]:
				var c := at + Vector2(r * offset, 0.0)
				_controls.draw_colored_polygon(PackedVector2Array([c + Vector2(-r * 0.3, -r * 0.6),
					c + Vector2(r * 0.35, 0.0), c + Vector2(-r * 0.3, r * 0.6),
					c + Vector2(-r * 0.05, 0.0)]), Color("#ff9db6"))
		"sparkle":
			_draw_star(_controls, at, r * 0.95, Color("#ffe27a"))
		"kelp":
			_controls.draw_circle(at + Vector2(0.0, r * 0.2), r * 0.62, Color("#4fa36b"))
			_controls.draw_circle(at + Vector2(-r * 0.3, -r * 0.25), r * 0.4, Color("#77c98a"))
		"pearls":
			for offset: Vector2 in [Vector2(-0.45, 0.25), Vector2(0.45, 0.25), Vector2(0.0, -0.4)]:
				_controls.draw_circle(at + offset * r, r * 0.38, INK)
				_controls.draw_circle(at + offset * r, r * 0.32, Color("#fff4e2"))
