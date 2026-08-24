class_name SkyLagoonPromenade
extends RefCounted
# True-Canvas Sky Lagoon promenade. The complete 6144x2048 painting is the
# canonical coordinate system for rendering, movement, touch and save/return.
# All mutable gameplay state stays on ReefMain.g; this satellite owns logic and
# temporary Canvas nodes only.

const Affordance := preload("res://scripts/interaction_affordance.gd")
const ANCHORS := preload("res://scripts/roshan_sprite_anchors.gd")
const FRAMES := preload("res://scripts/roshan_sprite_frames.gd")

const MASTER_SIZE := Vector2(6144.0, 2048.0)
const BACKDROP_COLUMNS := 6
const BACKDROP_ROWS := 2
const BACKDROP_TILE_PX := Vector2(1024.0, 1024.0)
const STAGE_LAYER := -1
const VIEW_HEIGHT_MARGIN := 0.0
const CAMERA_FOLLOW := 7.5
const WALK_SPEED_MASTER := 790.0
const ARRIVE_RADIUS_MASTER := 28.0
const EDGE_MARGIN_PX := 112.0
const PLAYER_HEIGHT_PX := 382.0
const PLAY_ROSHAN_HEIGHT_PX := 315.0
const ANIMAL_TOUCH_RADIUS_PX := 114.0
const ANIMAL_PAGE_SPAWN_S := 0.70
const ANIMAL_RESPAWN_S := 5.5
const ANIMAL_STARTLE_ALERT_S := 0.24
const ANIMAL_STARTLE_SQUASH_S := 0.18
const ANIMAL_STARTLE_HOP_S := 0.24
const ANIMAL_ATLAS_COLUMNS := 2
const ANIMAL_ATLAS_ROWS := 2
const FIREFLY_COUNT := 18
const PLANE_DEPARTURE_S := 7.0
const PLAY_SETTLE_S := 0.34
const PLAY_SETTLE_HOP := 18.0
const CASTLE_DOOR_MASTER_X := 5312.0
const CASTLE_CARD_TEXTURE_SIZE := Vector2(1022.0, 1024.0)
const CASTLE_DOOR_FOCUS_BOUNDS := Rect2(Vector2(410.0, 557.0), Vector2(199.0, 228.0))
const CASTLE_CARD_HEIGHT_MASTER := 1060.0
const CASTLE_CARD_BOTTOM_MASTER_Y := 1120.0
const DOORSTEP_RADIUS_MASTER := 62.0
const DOORSTEP_REARM_MASTER := 330.0
const LOCKED_MURAL_PARALLAX := 1.0
const REAR_PARALLAX := 0.82
const FOREGROUND_PARALLAX := 1.06

const CONTACT_SHADOW_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png"
const FIREFLY_TEX := "res://assets/fairy/sprites/bug_firefly.png"
const SMOKE_WISP_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png"
const SWING_FRAME_TEX := "res://assets/props/story/play_swing_frame.png"
const SWING_SEAT_TEX := "res://assets/props/story/play_swing_seat.png"
const SWING_GRIP_LENGTH_MASTER := 361.0
const SWING_SEAT_ANCHORS := [
	Vector2(264.5, 204.5),
	Vector2(168.0, 205.0),
	Vector2(322.5, 186.0),
	Vector2(222.0, 190.0),
]
const SEESAW_SEAT_ANCHORS := [
	Vector2(300.0, 420.0),
	Vector2(225.0, 400.0),
	Vector2(270.0, 340.0),
	Vector2(220.0, 360.0),
]
const SEESAW_RIGHT_SEAT_SOCKET_MASTER := Vector2(226.13, -9.42)
const SLIDE_RIDE_START_MASTER := Vector2(-62.0, -325.0)
const SLIDE_RIDE_CONTROL_MASTER := Vector2(54.0, -217.0)
const SLIDE_RIDE_FINISH_MASTER := Vector2(250.0, 92.0)
const ROSHAN_DIRECTIONAL := preload("res://assets/characters/roshan_25d/roshan_directional.png")
const ROSHAN_SWIM_FRONT := preload("res://assets/characters/roshan_25d/roshan_swim_front.png")

# Master-pixel route sampled from the approved v5 painting. It remains a real
# continuous path: every screen point resolves onto it and both stick/tap use
# this same geometry.
const ROUTE_MASTER: Array[Vector2] = [
	Vector2(170.0, 1610.0),
	Vector2(610.0, 1644.0),
	Vector2(1380.0, 1668.0),
	Vector2(2230.0, 1652.0),
	Vector2(3072.0, 1644.0),
	Vector2(3920.0, 1652.0),
	Vector2(4520.0, 1668.0),
	Vector2(4905.0, 1610.0),
	Vector2(CASTLE_DOOR_MASTER_X, 1584.0),
]

# One pooled actor represents the page's ecological roster. Paths are master
# pixels, clear of the route/equipment and intentionally larger than the old
# too-small frog/otter presentation.
const ANIMAL_DEFS: Array[Dictionary] = [
	{
		"id": "otter", "page": 0, "habitat": "arrival_shore",
		"idle": "res://assets/sprites/sky_lagoon/animals/otter_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/otter_startle_atlas.png",
		"path": [Vector2(180, 1240), Vector2(330, 1225), Vector2(470, 1242)],
		"height": 420.0, "speed": 56.0, "exit_speed": 620.0,
		"frame_s": 0.26, "dwell_s": 1.4, "bob": 3.0,
		"requires_plane_departed": true,
		"day_tint": Color(0.92, 1.0, 1.0), "night_tint": Color(0.67, 0.79, 1.0),
	},
	{
		"id": "frog", "page": 0, "habitat": "arrival_shore",
		"idle": "res://assets/sprites/sky_lagoon/animals/frog_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/frog_startle_atlas.png",
		"path": [Vector2(145, 1280), Vector2(285, 1260), Vector2(425, 1278)],
		"height": 322.0, "speed": 72.0, "exit_speed": 580.0,
		"frame_s": 0.30, "dwell_s": 1.7, "bob": 8.0,
		"requires_plane_departed": true,
		"day_tint": Color(0.96, 1.0, 1.0), "night_tint": Color(0.69, 0.86, 0.98),
	},
	{
		"id": "hare", "page": 1, "habitat": "west_meadow_edge",
		"idle": "res://assets/sprites/sky_lagoon/animals/hare_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/hare_startle_atlas.png",
		"path": [Vector2(2055, 1125), Vector2(2125, 1105), Vector2(2195, 1128)],
		"height": 245.0, "speed": 68.0, "exit_speed": 660.0,
		"frame_s": 0.28, "dwell_s": 1.6, "bob": 6.0,
		"day_tint": Color.WHITE, "night_tint": Color(0.68, 0.77, 0.99),
	},
	{
		"id": "squirrel", "page": 1, "habitat": "west_meadow_edge",
		"idle": "res://assets/sprites/sky_lagoon/animals/squirrel_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/squirrel_startle_atlas.png",
		"path": [Vector2(2065, 1015), Vector2(2140, 995), Vector2(2210, 1020)],
		"height": 290.0, "speed": 82.0, "exit_speed": 690.0,
		"frame_s": 0.22, "dwell_s": 1.25, "bob": 4.0,
		"day_tint": Color(0.9, 0.98, 1.0), "night_tint": Color(0.60, 0.74, 0.96),
	},
	{
		"id": "raccoon", "page": 2, "habitat": "castle_shrub_edge",
		"idle": "res://assets/sprites/sky_lagoon/animals/raccoon_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/raccoon_startle_atlas.png",
		"path": [Vector2(4360, 1160), Vector2(4510, 1145), Vector2(4660, 1170)],
		"height": 290.0, "speed": 60.0, "exit_speed": 640.0,
		"frame_s": 0.29, "dwell_s": 1.8, "bob": 3.0,
		"day_tint": Color.WHITE, "night_tint": Color(0.76, 0.84, 1.0),
	},
]

const PLAY_FRAME_PATHS := {
	"swing": [
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2_v2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3_v2.png",
	],
	"slide": [
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2_v2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3_v2.png",
	],
	"seesaw": [
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_3.png",
	],
}
const PLAY_DURATIONS := {"swing": 5.6, "slide": 5.4, "seesaw": 5.8}

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func root() -> CanvasLayer:
	return m.g.get("lagoon_canvas_layer") as CanvasLayer

func canvas_root() -> Control:
	return m.g.get("lagoon_canvas_root") as Control

func camera_2d() -> Camera2D:
	return m.g.get("lagoon_camera_2d") as Camera2D

func master_route_x() -> float:
	return float(m.g.get("lagoon_master_x", ROUTE_MASTER[0].x))

func build(from_castle: bool, from_north: bool, at_ocean_gate_hub: bool) -> void:
	teardown()
	m.g["phase"] = "promenade"
	m.g["ocean_gate_hub"] = at_ocean_gate_hub
	m.g["lagoon_promenade_targets"] = []
	m.g["lagoon_promenade_focus"] = ""
	m.g["lagoon_promenade_focus_t"] = 0.0
	m.g["lagoon_walk_goal_master"] = null
	m.g["lagoon_play_anim"] = {}
	m.g["lagoon_reef_guidance_pending"] = false
	m.g["lagoon_castle_armed"] = not (from_castle or from_north)
	m.lagoon_floor = false
	m.northern_floor = false

	var layer := CanvasLayer.new()
	layer.name = "SkyLagoonCanvasLayer"
	layer.layer = int(m.SKY_LAGOON_STAGE_CANVAS_LAYER) if "SKY_LAGOON_STAGE_CANVAS_LAYER" in m else STAGE_LAYER
	# CanvasLayer is normally screen-fixed. This stage is a world canvas, so it
	# explicitly follows the current Camera2D; render and hit geometry then share
	# the same transform instead of maintaining a second hand-built projection.
	layer.follow_viewport_enabled = true
	layer.follow_viewport_scale = 1.0
	layer.set_meta("canvas_stage", true)
	layer.set_meta("canonical_master_size", MASTER_SIZE)
	layer.set_meta("no_spatial_descendants", true)
	m.add_child(layer)
	m.g["lagoon_canvas_layer"] = layer

	var viewport := Control.new()
	viewport.name = "SkyLagoonViewport"
	viewport.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	viewport.mouse_filter = Control.MOUSE_FILTER_IGNORE
	# The parent CanvasLayer follows Camera2D. A screen-sized clipping Control is
	# itself camera-transformed and clips the world to a top-left quadrant; the
	# opaque master already covers the entire camera frame, so no clip is needed.
	viewport.clip_contents = false
	viewport.set_meta("canonical_space", "sky_lagoon_master_6144x2048")
	layer.add_child(viewport)
	m.g["lagoon_canvas_root"] = viewport

	var content := Node2D.new()
	content.name = "SkyLagoonMasterSpace"
	content.set_meta("master_size", MASTER_SIZE)
	viewport.add_child(content)
	m.g["lagoon_master_space"] = content

	for holder_spec: Dictionary in [
		{"key": "lagoon_base_layer", "name": "SkyLagoonBase", "z": -500, "parallax": LOCKED_MURAL_PARALLAX},
		{"key": "lagoon_rear_layer", "name": "SkyLagoonRear", "z": -400, "parallax": REAR_PARALLAX},
		{"key": "lagoon_landmark_layer", "name": "SkyLagoonLandmarks", "z": -300, "parallax": LOCKED_MURAL_PARALLAX},
		{"key": "lagoon_interactive_layer", "name": "SkyLagoonInteractive", "z": 0, "parallax": LOCKED_MURAL_PARALLAX},
		{"key": "lagoon_actor_layer", "name": "SkyLagoonActors", "z": 100, "parallax": LOCKED_MURAL_PARALLAX},
		{"key": "lagoon_foreground_layer", "name": "SkyLagoonForeground", "z": 300, "parallax": FOREGROUND_PARALLAX},
	]:
		var holder := Node2D.new()
		holder.name = String(holder_spec["name"])
		holder.z_index = int(holder_spec["z"])
		holder.set_meta("canvas_layer_role", String(holder_spec["name"]))
		holder.set_meta("parallax_factor", float(holder_spec["parallax"]))
		content.add_child(holder)
		m.g[String(holder_spec["key"])] = holder

	var camera := Camera2D.new()
	camera.name = "SkyLagoonCamera2D"
	camera.enabled = true
	camera.position = Vector2(MASTER_SIZE.x * 0.5, MASTER_SIZE.y * 0.5)
	content.add_child(camera)
	m.g["lagoon_camera_2d"] = camera

	_build_backdrop()
	_build_ambient_life()
	_build_night_fireflies()
	_build_runway_screen()
	_build_playground_screen()
	_build_castle_screen()
	_build_roshan_card()
	_build_animals()
	var spawn_x: float = 4520.0 if from_castle or from_north else 610.0
	set_master_route_x(spawn_x)
	_apply_view_transform(true)
	if from_castle:
		m.show_msg("Roshan", "Back outside! Tap a playground toy or the castle door once to light it up, then tap it again to play.")
	elif m.first_session and at_ocean_gate_hub:
		m.g["lagoon_reef_guidance_pending"] = true
	else:
		_show_reef_route_guidance()

func teardown() -> void:
	var layer: CanvasLayer = root()
	if layer != null and is_instance_valid(layer):
		if layer.get_parent() != null:
			layer.get_parent().remove_child(layer)
		layer.free()
	for key: String in [
		"lagoon_canvas_layer", "lagoon_canvas_root", "lagoon_master_space",
		"lagoon_camera_2d", "lagoon_base_layer", "lagoon_rear_layer",
		"lagoon_landmark_layer", "lagoon_interactive_layer", "lagoon_actor_layer",
		"lagoon_foreground_layer", "lagoon_roshan_card", "lagoon_animal_actor",
		"lagoon_plane_card", "lagoon_reef_route_card", "lagoon_castle_card",
		"lagoon_castle_door_focus", "lagoon_night_fireflies",
		"lagoon_ambient_cards", "lagoon_animals", "lagoon_animal_cycles",
		"lagoon_promenade_targets", "lagoon_promenade_focus",
		"lagoon_promenade_focus_t", "lagoon_walk_goal_master",
		"lagoon_play_anim", "lagoon_reef_guidance_pending", "lagoon_castle_armed",
		"lagoon_master_x", "lagoon_master_y", "lagoon_route_t",
		"lagoon_camera_x", "lagoon_plane_t", "lagoon_hop_t",
		"lagoon_roshan_anim_t", "lagoon_roshan_frame", "lagoon_ambient_t",
		"lagoon_press_t", "lagoon_press_position",
	]:
		m.g.erase(key)

func tick(delta: float) -> void:
	if m.mg_kind != "" or root() == null:
		return
	if bool(m.g.get("lagoon_reef_guidance_pending", false)) and not m.intro_active:
		m.g["lagoon_reef_guidance_pending"] = false
		_show_reef_route_guidance()
	if not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		m.g["lagoon_walk_goal_master"] = null
		_tick_playground_animation(delta)
	else:
		_tick_movement(delta)
		_handle_action()
		_tick_doorstep()
	_tick_plane_arrival(delta)
	_tick_ambient_life(delta)
	_tick_animals(delta)
	_tick_roshan_animation(delta)
	var focus_t: float = float(m.g.get("lagoon_promenade_focus_t", 0.0)) + delta
	m.g["lagoon_promenade_focus_t"] = focus_t
	_tick_target_affordances(String(m.g.get("lagoon_promenade_focus", "")), focus_t)
	_apply_view_transform()

func handle_touch(screen_pos: Vector2) -> bool:
	if not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		return true
	var animal: Dictionary = _animal_at(screen_pos)
	if not animal.is_empty():
		_startle_animal(animal)
		return true
	var target: Dictionary = _target_at(screen_pos)
	if target.is_empty():
		_clear_focus()
		_set_walk_goal(screen_pos)
		return true
	m.g["lagoon_walk_goal_master"] = null
	var target_id: String = String(target.get("id", ""))
	if String(target.get("kind", "")) == "reef" \
			or String(m.g.get("lagoon_promenade_focus", "")) == target_id:
		_activate(target)
		_clear_focus()
	else:
		_focus(target)
	return true

func handle_drag(_from: Vector2, to: Vector2) -> bool:
	if root() == null or not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		return false
	cancel_navigation()
	_set_walk_goal(to)
	return true

func cancel_navigation() -> void:
	# One cancellation seam owns every child-visible route promise. Manual stick
	# or keyboard movement, pause/focus loss and overlay transitions all use it so
	# no off-screen PLAY/ENTER focus or old autowalk can resume later.
	m.g["lagoon_walk_goal_master"] = null
	m.g["lagoon_press_t"] = 0.0
	m.g.erase("lagoon_press_position")
	_clear_focus()

func action_label() -> String:
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) != focus_id:
			continue
		match String(target.get("kind", "")):
			"castle": return "ENTER"
			"reef": return "FLY"
			_: return "PLAY"
	return "JUMP"

func set_master_route_x(master_x: float) -> void:
	var point: Vector2 = _route_point_for_x(clampf(master_x, ROUTE_MASTER[0].x, ROUTE_MASTER[-1].x))
	m.g["lagoon_master_x"] = point.x
	m.g["lagoon_master_y"] = point.y
	m.g["lagoon_route_t"] = _route_fraction(point.x)
	m.g["lagoon_camera_x"] = _camera_clamp_x(point.x)
	m.g["lagoon_walk_goal_master"] = null
	_sync_roshan_card(0.0, false)
	_apply_view_transform(true)

func screen_from_master(point: Vector2, parallax_factor: float = 1.0) -> Vector2:
	var viewport_size: Vector2 = _viewport_size()
	var scale_factor: float = _master_scale(viewport_size)
	var camera_x: float = float(m.g.get("lagoon_camera_x", point.x))
	var half_master: float = viewport_size.x / scale_factor * 0.5
	var left: float = camera_x - half_master
	return Vector2((point.x - left * parallax_factor) * scale_factor,
		point.y * scale_factor)

func master_from_screen(point: Vector2) -> Vector2:
	var viewport_size: Vector2 = _viewport_size()
	var scale_factor: float = _master_scale(viewport_size)
	var camera_x: float = float(m.g.get("lagoon_camera_x", MASTER_SIZE.x * 0.5))
	var left: float = camera_x - viewport_size.x / scale_factor * 0.5
	return Vector2(left + point.x / scale_factor, point.y / scale_factor)

func _build_backdrop() -> void:
	var holder: Node2D = m.g.get("lagoon_base_layer") as Node2D
	for row: int in range(BACKDROP_ROWS):
		for column: int in range(BACKDROP_COLUMNS):
			var path: String = "res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png" % [row, column]
			var tile := _make_sprite(path, Vector2(column, row) * BACKDROP_TILE_PX + BACKDROP_TILE_PX * 0.5, BACKDROP_TILE_PX.y, false, holder)
			tile.name = "SkyLagoonBackdrop_r%d_c%d" % [row, column]
			tile.set_meta("canvas_layer_role", "base_panorama")
			tile.set_meta("source_owned", true)
			if m.is_night:
				tile.modulate = Color(0.48, 0.56, 0.82)

func _build_ambient_life() -> void:
	m.g["lagoon_ambient_t"] = 0.0
	m.g["lagoon_ambient_cards"] = []
	# These approved transparent assets form a genuinely independent broad rear
	# layer. They move at REAR_PARALLAX while the 12-tile panorama remains one
	# base layer, satisfying the layered-scene contract without duplicate pixels.
	var tree := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png",
		Vector2(4180, 1185), 465.0, true, m.g.get("lagoon_rear_layer") as Node2D)
	tree.name = "SkyLagoonRearTree"
	tree.set_meta("ambient_kind", "tree")
	tree.set_meta("canvas_layer_role", "rear_ambient")
	tree.set_meta("source_owned", true)
	_mark_living_card(tree, "sway", "quiet", 465.0)
	var cloud := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png",
		Vector2(2680, 430), 235.0, false, m.g.get("lagoon_rear_layer") as Node2D)
	cloud.name = "SkyLagoonRearCloud"
	cloud.set_meta("ambient_kind", "cloud")
	cloud.set_meta("canvas_layer_role", "rear_ambient")
	cloud.set_meta("source_owned", true)
	_mark_living_card(cloud, "drift", "quiet", 235.0)
	m.g["lagoon_ambient_cards"] = [tree, cloud]
	for index: int in range(3):
		var smoke := _make_sprite(SMOKE_WISP_TEX,
			Vector2(4700.0 + float(index) * 150.0, 755.0 + float(index) * 68.0),
			135.0, false, m.g.get("lagoon_landmark_layer") as Node2D)
		smoke.name = "SkyLagoonSmoke_%d" % index
		smoke.set_meta("ambient_kind", "smoke")
		smoke.set_meta("canvas_layer_role", "landmark_ambient")
		smoke.set_meta("phase", float(index) * 2.0)
		_mark_living_card(smoke, "rise_fade", "quiet", 135.0)
		(m.g["lagoon_ambient_cards"] as Array).append(smoke)
	# A distinct approved slender tree occupies a clean-plate foreground socket;
	# it never duplicates the rear tree's source pixels or a baked object.
	var foreground_tree := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_slender_v1.png",
		Vector2(5750, 1510), 350.0, true,
		m.g.get("lagoon_foreground_layer") as Node2D)
	foreground_tree.name = "SkyLagoonForegroundTree"
	foreground_tree.set_meta("ambient_kind", "foreground_tree")
	foreground_tree.set_meta("canvas_layer_role", "sparse_foreground")
	_mark_living_card(foreground_tree, "sway", "quiet", 350.0)
	(m.g["lagoon_ambient_cards"] as Array).append(foreground_tree)
	if m.is_night:
		for value: Variant in m.g["lagoon_ambient_cards"] as Array:
			var ambient: Sprite2D = value as Sprite2D
			ambient.modulate *= Color(0.72, 0.78, 0.96, 1.0)
			ambient.set_meta("night_tinted", true)

func _mark_living_card(card: Sprite2D, motion_class: String,
		intensity_class: String, display_height: float) -> void:
	card.set_meta("living_card", true)
	card.set_meta("motion_class", motion_class)
	card.set_meta("intensity_class", intensity_class)
	card.set_meta("source_owned", true)
	card.set_meta("ambient_base", card.position)
	card.set_meta("target_master_height", display_height)
	card.set_meta("content_height_fraction",
		0.992188 if String(card.get_meta("ambient_kind", "")) == "smoke" else 1.0)
	card.set_meta("source_aspect",
		float(card.texture.get_width()) / maxf(1.0, float(card.texture.get_height()))
		if card.texture != null else 0.0)

func _build_night_fireflies() -> void:
	if not m.is_night:
		return
	var holder: Node2D = m.g.get("lagoon_foreground_layer") as Node2D
	var fireflies: Array[Sprite2D] = []
	var texture: Texture2D = load(FIREFLY_TEX) as Texture2D
	for index: int in range(FIREFLY_COUNT):
		var fly := Sprite2D.new()
		fly.name = "SkyLagoonFirefly_%02d" % index
		fly.texture = texture
		fly.position = Vector2(260.0 + fmod(float(index * 337), 5550.0), 760.0 + fmod(float(index * 173), 650.0))
		fly.scale = Vector2.ONE * (0.030 + float(index % 4) * 0.006)
		fly.modulate = Color(1.0, 0.88, 0.35, 0.75)
		fly.set_meta("ambient_kind", "fireflies")
		fly.set_meta("lighting_medium", "canvas_sprite2d")
		fly.set_meta("night_only", true)
		fly.set_meta("night_tinted", true)
		fly.set_meta("canvas_layer_role", "sparse_foreground")
		holder.add_child(fly)
		fireflies.append(fly)
	m.g["lagoon_night_fireflies"] = fireflies

func _build_runway_screen() -> void:
	if bool(m.save_data.get("lagoon_plane_departed", false)):
		_build_reef_route_marker()
		return
	var plane := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
		Vector2(600, 1420), 445.0, true, m.g.get("lagoon_landmark_layer") as Node2D)
	plane.name = "SkyLagoonArrivalPlane"
	m.g["lagoon_plane_card"] = plane
	m.g["lagoon_plane_t"] = 0.0
	_register_target("reef_route", plane, "reef", "reef", 132.0, 1.10)

func _build_reef_route_marker() -> void:
	var plane := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
		Vector2(310, 1040), 270.0, true, m.g.get("lagoon_landmark_layer") as Node2D)
	plane.name = "SkyLagoonReefPlane"
	m.g["lagoon_reef_route_card"] = plane
	_register_target("reef_route", plane, "reef", "reef", 132.0, 1.12)

func _build_playground_screen() -> void:
	var holder: Node2D = m.g.get("lagoon_interactive_layer") as Node2D
	var slide := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
		Vector2(2655, 1315), 620.0, true, holder)
	slide.name = "SkyLagoonSlide"
	var swing := _build_promenade_swing(Vector2(3200, 1268))
	var seesaw := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png",
		Vector2(3760, 1510), 265.0, true, holder)
	seesaw.name = "SkyLagoonSeesaw"
	_register_target("slide", slide, "playground", "slide", 118.0, 1.10)
	_register_target("swing", swing, "playground", "swing", 122.0, 1.10)
	_register_target("seesaw", seesaw, "playground", "seesaw", 112.0, 1.12)

func _build_promenade_swing(position_master: Vector2) -> Sprite2D:
	var frame := _make_sprite(SWING_FRAME_TEX, position_master, 610.0, true,
		m.g.get("lagoon_interactive_layer") as Node2D)
	frame.name = "SkyLagoonPromenadeSwingFrame"
	var pivot := Node2D.new()
	pivot.name = "SwingSeatPivot"
	pivot.position = Vector2(0.0, -258.0)
	frame.add_child(pivot)
	var seat := _make_sprite(SWING_SEAT_TEX, Vector2(0, 250), 540.0, false, pivot)
	seat.name = "SwingSeatAndRopes"
	frame.set_meta("swing_seat_pivot", pivot)
	frame.set_meta("swing_seat_sprite", seat)
	return frame

func _build_castle_screen() -> void:
	var castle := _make_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png",
		Vector2(5260, CASTLE_CARD_BOTTOM_MASTER_Y), CASTLE_CARD_HEIGHT_MASTER,
		true, m.g.get("lagoon_landmark_layer") as Node2D)
	castle.name = "SkyLagoonCastleFourTower"
	castle.set_meta("exterior_dressing_contract", "authored_sprite2d_only")
	castle.set_meta("lighting_medium", "authored_rgba_canvas_sprite")
	m.g["lagoon_castle_card"] = castle
	var door_anchor := Node2D.new()
	door_anchor.name = "SkyLagoonCastleDoorFocus"
	# Derive the focus socket from the accepted door-pixel bounds in the actual
	# scaled castle card. This cannot drift when the facade scale changes.
	var door_center_pixels: Vector2 = CASTLE_DOOR_FOCUS_BOUNDS.position \
		+ CASTLE_DOOR_FOCUS_BOUNDS.size * 0.5
	door_anchor.position = castle.position \
		+ (door_center_pixels - CASTLE_CARD_TEXTURE_SIZE * 0.5) * castle.scale
	door_anchor.set_meta("source_owned", true)
	(m.g.get("lagoon_interactive_layer") as Node2D).add_child(door_anchor)
	m.g["lagoon_castle_door_focus"] = door_anchor
	_register_target("castle_gate", door_anchor, "castle", "", 128.0, 1.0,
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png", 266.0)

func _build_roshan_card() -> void:
	var card := Sprite2D.new()
	card.name = "SkyLagoonRoshan"
	card.texture = ROSHAN_DIRECTIONAL
	card.region_enabled = true
	card.region_rect = FRAMES.region("directional", 2, 4)
	card.centered = true
	card.scale = Vector2.ONE * (PLAYER_HEIGHT_PX / 256.0)
	card.set_meta("walking", false)
	card.set_meta("canvas_layer_role", "actor")
	card.set_meta("source_owned", true)
	(m.g.get("lagoon_actor_layer") as Node2D).add_child(card)
	m.g["lagoon_roshan_card"] = card
	m.g["lagoon_roshan_anim_t"] = 0.0
	m.g["lagoon_roshan_frame"] = 2
	_add_contact_shadow(card, Vector2(175, 48))
	if m.player != null:
		m.player.visible = false

func _build_animals() -> void:
	m.g["lagoon_animals"] = ANIMAL_DEFS.duplicate(true)
	m.g["lagoon_animal_cycles"] = {0: 0, 1: 0, 2: 0}
	var card := Sprite2D.new()
	card.name = "SkyLagoonAnimalPool"
	card.centered = true
	card.visible = false
	card.set_meta("living_card", true)
	card.set_meta("ambient_kind", "animal")
	card.set_meta("canvas_layer_role", "interactive_animal")
	card.set_meta("touch_footprint_px", ANIMAL_TOUCH_RADIUS_PX * 2.0)
	card.set_meta("source_owned", true)
	card.set_meta("animal_lighting_profile", "canvas_day_night_tint")
	(m.g.get("lagoon_interactive_layer") as Node2D).add_child(card)
	_add_contact_shadow(card, Vector2(145, 38))
	m.g["lagoon_animal_actor"] = {
		"node": card, "definition": {}, "page": -1, "state": "hidden",
		"state_t": 0.0, "spawn_t": ANIMAL_PAGE_SPAWN_S,
		"route_position": Vector2.ZERO, "path_index": 1,
		"path_direction": 1, "exit_direction": -1.0,
	}

func _make_sprite(path: String, position_master: Vector2, height_master: float,
		bottom_aligned: bool, parent: Node) -> Sprite2D:
	var texture: Texture2D = load(path) as Texture2D
	var sprite := Sprite2D.new()
	sprite.texture = texture
	sprite.position = position_master
	if texture != null:
		var scale_factor: float = height_master / maxf(1.0, float(texture.get_height()))
		sprite.scale = Vector2.ONE * scale_factor
		if bottom_aligned:
			sprite.position.y -= height_master * 0.5
	sprite.set_meta("source_path", path)
	sprite.set_meta("source_owned", true)
	parent.add_child(sprite)
	return sprite

func _add_contact_shadow(sprite: Sprite2D, size_master: Vector2) -> Sprite2D:
	var shadow := Sprite2D.new()
	shadow.name = "%sContactShadow" % sprite.name
	shadow.texture = load(CONTACT_SHADOW_TEX) as Texture2D
	shadow.modulate = Color(0.20, 0.28, 0.42, 0.30)
	if shadow.texture != null:
		shadow.scale = size_master / shadow.texture.get_size()
	shadow.z_index = sprite.z_index - 1
	shadow.set_meta("canvas_layer_role", "contact_shadow")
	shadow.set_meta("contact_shadow", true)
	shadow.set_meta("source_owned", true)
	sprite.get_parent().add_child(shadow)
	sprite.set_meta("contact_shadow", shadow)
	_sync_contact_shadow(sprite)
	return shadow

func _sync_contact_shadow(sprite: Sprite2D) -> void:
	var shadow: Sprite2D = sprite.get_meta("contact_shadow") as Sprite2D \
		if sprite != null and sprite.has_meta("contact_shadow") else null
	if shadow == null or not is_instance_valid(shadow):
		return
	shadow.position = Vector2(sprite.position.x, sprite.position.y + _sprite_draw_height(sprite) * 0.5)
	shadow.visible = sprite.visible

func _register_target(id: String, node: Node2D, kind: String, payload: String,
		radius_px: float, highlight_scale: float, highlight_path: String = "",
		highlight_height: float = 0.0) -> void:
	var affordance_kind: String = Affordance.PLOT if kind == "castle" \
		else Affordance.INTERACTION if kind == "reef" else Affordance.ANIMATION
	var glow := Sprite2D.new()
	glow.name = "SkyLagoonFocus_%s" % id
	if kind == "playground" or kind == "reef":
		# A neutral procedural ring plus arrow names the object without cloning
		# any of its pixels. At the full-height phone scale the selected composite
		# remains over 64 px and its tip lands on the source card's top edge.
		glow.texture = _affordance_diamond_texture()
		glow.scale = Vector2.ONE * highlight_scale
		var pointer_tip := Vector2(0.0, 128.0)
		_add_affordance_pointer(glow, pointer_tip)
		var visible_top_y: float = _sprite_alpha_top_master(node as Sprite2D) \
			if node is Sprite2D else node.position.y
		glow.position = Vector2(node.position.x,
			visible_top_y - pointer_tip.y * highlight_scale)
		glow.set_meta("focus_cue_role", "procedural_ring_pointer")
		glow.set_meta("pointer_tip_local", pointer_tip)
		glow.set_meta("focus_cue_nominal_master_size", Vector2(192.0, 256.0))
	elif not highlight_path.is_empty():
		glow.texture = load(highlight_path) as Texture2D
		if glow.texture != null and highlight_height > 0.0:
			glow.scale = Vector2.ONE * (highlight_height / glow.texture.get_height())
	elif node is Sprite2D:
		var source := node as Sprite2D
		glow.texture = source.texture
		glow.scale = source.scale
	if kind != "playground" and kind != "reef":
		glow.position = node.position
	var idle_tint: Color = Affordance.color(affordance_kind, false)
	# A complete duplicate object is never the affordance. Idle animation targets
	# use a nearly invisible shimmer; selection raises the same pixels briefly.
	idle_tint.a = minf(idle_tint.a,
		0.055 if kind == "playground" or kind == "reef" else 0.10)
	glow.modulate = idle_tint
	glow.visible = true
	glow.z_index = node.z_index + 4
	glow.set_meta("canvas_layer_role", "interaction_affordance")
	glow.set_meta("interaction_id", id)
	glow.set_meta("affordance_base_scale", glow.scale)
	(m.g.get("lagoon_interactive_layer") as Node2D).add_child(glow)
	node.set_meta("interaction_id", id)
	node.set_meta("touch_footprint_px", radius_px * 2.0)
	node.set_meta("canvas_layer_role", "interactive")
	var targets: Array = m.g.get("lagoon_promenade_targets", []) as Array
	targets.append({
		"id": id, "node": node, "kind": kind, "payload": payload,
		"radius_px": radius_px, "affordance_kind": affordance_kind,
		"highlight": glow, "highlight_scale": highlight_scale,
	})
	m.g["lagoon_promenade_targets"] = targets

func _affordance_diamond_texture() -> GradientTexture2D:
	var gradient := Gradient.new()
	gradient.colors = PackedColorArray([
		Color(1.0, 1.0, 1.0, 0.0),
		Color(1.0, 1.0, 1.0, 0.98),
		Color(1.0, 1.0, 1.0, 0.0),
	])
	gradient.offsets = PackedFloat32Array([0.0, 0.50, 1.0])
	var texture := GradientTexture2D.new()
	texture.gradient = gradient
	texture.width = 192
	texture.height = 192
	texture.fill = GradientTexture2D.FILL_RADIAL
	texture.fill_from = Vector2(0.5, 0.5)
	texture.fill_to = Vector2(1.0, 0.5)
	return texture

func _add_affordance_pointer(glow: Sprite2D, tip: Vector2) -> void:
	var outline := Polygon2D.new()
	outline.name = "PointerOutline"
	outline.polygon = PackedVector2Array([
		Vector2(-32.0, 70.0), Vector2(32.0, 70.0),
		Vector2(18.0, 101.0), tip, Vector2(-18.0, 101.0),
	])
	outline.color = Color(0.10, 0.16, 0.34, 0.96)
	outline.set_meta("canvas_layer_role", "interaction_affordance_pointer_outline")
	glow.add_child(outline)
	var arrow := Polygon2D.new()
	arrow.name = "PointerFill"
	arrow.polygon = PackedVector2Array([
		Vector2(-22.0, 75.0), Vector2(22.0, 75.0),
		Vector2(11.0, 99.0), Vector2(0.0, 119.0), Vector2(-11.0, 99.0),
	])
	arrow.color = Color.WHITE
	arrow.set_meta("canvas_layer_role", "interaction_affordance_pointer_fill")
	glow.add_child(arrow)

func _target_at(screen_pos: Vector2) -> Dictionary:
	var best: Dictionary = {}
	var best_distance: float = INF
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		var node: Node2D = target.get("node") as Node2D
		if node == null or not is_instance_valid(node):
			continue
		var distance: float = screen_from_master(node.position).distance_to(screen_pos)
		if distance <= float(target.get("radius_px", 110.0)) and distance < best_distance:
			best = target
			best_distance = distance
	return best

func _focus(target: Dictionary) -> void:
	m.g["lagoon_promenade_focus"] = String(target.get("id", ""))
	m.g["lagoon_promenade_focus_t"] = 0.0
	_tick_target_affordances(String(target.get("id", "")), 0.0)

func _clear_focus() -> void:
	m.g["lagoon_promenade_focus"] = ""
	_tick_target_affordances("", float(m.g.get("lagoon_promenade_focus_t", 0.0)))

func _tick_target_affordances(focus_id: String, focus_t: float) -> void:
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		var glow: Sprite2D = target.get("highlight") as Sprite2D
		if glow == null or not is_instance_valid(glow):
			continue
		var selected: bool = String(target.get("id", "")) == focus_id
		glow.visible = true
		var kind: String = String(target.get("affordance_kind", Affordance.INTERACTION))
		var wave: float = sin(focus_t * Affordance.pulse_speed(kind, selected))
		var tint: Color = Affordance.color(kind, selected)
		if selected:
			tint.a = lerpf(0.82, 1.0, wave * 0.5 + 0.5)
		else:
			tint.a = minf(tint.a, 0.055)
		glow.modulate = tint
		var pulse: float = 1.0 + wave * Affordance.pulse_amount(kind, selected)
		var base_scale: float = float(target.get("highlight_scale", 1.0))
		if String(glow.get_meta("focus_cue_role", "")) \
				== "procedural_ring_pointer":
			glow.scale = Vector2.ONE * base_scale * pulse
		elif String(target.get("id", "")) != "castle_gate":
			var node: Node2D = target.get("node") as Node2D
			if node is Sprite2D:
				glow.scale = (node as Sprite2D).scale * base_scale * pulse

func _activate(target: Dictionary) -> void:
	match String(target.get("kind", "")):
		"reef":
			m._exit_level2()
		"playground":
			_start_playground_animation(String(target.get("payload", "")), target.get("node") as Node2D)
		"castle":
			m._enter_castle_interior()

func _handle_action() -> bool:
	if m.touch_ui == null or not m.touch_ui.consume_action_just():
		return false
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == focus_id:
			_activate(target)
			_clear_focus()
			return true
	# No failure state: an unfocused action is a small happy hop.
	m.g["lagoon_hop_t"] = 0.32
	return true

func _set_walk_goal(screen_pos: Vector2) -> void:
	# Any new travel promise supersedes a selected verb. Keeping PLAY/ENTER armed
	# while walking toward unrelated open ground leaves a stale off-screen action.
	_clear_focus()
	var master: Vector2 = master_from_screen(screen_pos)
	m.g["lagoon_walk_goal_master"] = _closest_route_point(master)

func _tick_hold_travel(delta: float) -> void:
	# Tap selection still resolves on release. A deliberate hold on open world
	# space follows the finger after 0.20 s, while the router-owned movement,
	# action and pause zones can never leak into travel.
	# Classic's first finger is always the stick owner—even when stationary—so
	# its emulated mouse must never also become an invisible walk command.
	if m.touch_ui == null or String(m.touch_ui.control_mode) != "hybrid":
		m.g["lagoon_press_t"] = 0.0
		m.g.erase("lagoon_press_position")
		return
	if not Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		m.g["lagoon_press_t"] = 0.0
		m.g.erase("lagoon_press_position")
		return
	var viewport: Viewport = m.get_viewport()
	var press: Vector2 = viewport.get_mouse_position()
	if m.touch_ui != null and m.touch_ui.reserved_zone_hit(press):
		m.g["lagoon_press_t"] = 0.0
		return
	if not _animal_at(press).is_empty() or not _target_at(press).is_empty():
		m.g["lagoon_press_t"] = 0.0
		return
	var held: float = float(m.g.get("lagoon_press_t", 0.0)) + delta
	m.g["lagoon_press_t"] = held
	m.g["lagoon_press_position"] = press
	if held >= 0.20:
		_set_walk_goal(press)

func _set_spawn(master_x: float) -> void:
	set_master_route_x(master_x)

func _walk_x(master_x: float) -> float:
	# Compatibility helper: in true Canvas the painting and route share one x.
	return master_x

func _walk_y(master_y: float) -> float:
	return master_y

func _refresh_route() -> void:
	# The route is authored directly in immutable master pixels; no projection.
	pass

func _sync_target_mural_anchors() -> void:
	# All target nodes already live in the same canonical master space.
	pass

func _tick_movement(delta: float) -> void:
	_tick_hold_travel(delta)
	var direction: float = 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		direction -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		direction += 1.0
	if m.touch_ui != null:
		var stick: Vector2 = m.touch_ui.stick_vec as Vector2
		if absf(stick.x) > 0.10:
			direction = stick.x
	var old_x: float = master_route_x()
	var next_x: float = old_x
	var goal_value: Variant = m.g.get("lagoon_walk_goal_master")
	if absf(direction) > 0.05:
		cancel_navigation()
		next_x += direction * WALK_SPEED_MASTER * delta
	elif goal_value is Vector2:
		var goal: Vector2 = goal_value as Vector2
		next_x = move_toward(next_x, goal.x, WALK_SPEED_MASTER * delta)
		if absf(next_x - goal.x) <= ARRIVE_RADIUS_MASTER:
			next_x = goal.x
			m.g["lagoon_walk_goal_master"] = null
	next_x = clampf(next_x, ROUTE_MASTER[0].x, ROUTE_MASTER[-1].x)
	var point: Vector2 = _route_point_for_x(next_x)
	m.g["lagoon_master_x"] = point.x
	m.g["lagoon_master_y"] = point.y
	m.g["lagoon_route_t"] = _route_fraction(point.x)
	var camera_target: float = _camera_clamp_x(point.x)
	m.g["lagoon_camera_x"] = camera_target if delta <= 0.0 else lerpf(
		float(m.g.get("lagoon_camera_x", camera_target)), camera_target,
		1.0 - exp(-CAMERA_FOLLOW * delta))
	_sync_roshan_card(next_x - old_x, absf(next_x - old_x) > 0.1)

func _sync_roshan_card(delta_x: float = 0.0, moving: bool = false) -> void:
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if card == null or not is_instance_valid(card):
		return
	card.position = Vector2(float(m.g.get("lagoon_master_x", ROUTE_MASTER[0].x)),
		float(m.g.get("lagoon_master_y", ROUTE_MASTER[0].y)) - PLAYER_HEIGHT_PX * 0.47)
	card.set_meta("walking", moving)
	if moving:
		card.flip_h = delta_x < 0.0
	_sync_contact_shadow(card)

func _tick_roshan_animation(delta: float) -> void:
	if not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		return
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if card == null or not is_instance_valid(card):
		return
	var moving: bool = bool(card.get_meta("walking", false))
	var timer: float = float(m.g.get("lagoon_roshan_anim_t", 0.0)) + delta
	m.g["lagoon_roshan_anim_t"] = timer
	var frame_index: int
	if moving:
		frame_index = int(floor(timer * 9.0)) % 16
		card.texture = ROSHAN_SWIM_FRONT
		card.region_rect = FRAMES.region("swim_front", frame_index, 4)
		card.offset = ANCHORS.correction("swim_front", frame_index,
			ANCHORS.anchor("directional", 2), card.flip_h) \
			+ FRAMES.offset_correction("swim_front", frame_index, card.flip_h)
	else:
		frame_index = 2
		card.texture = ROSHAN_DIRECTIONAL
		card.region_rect = FRAMES.region("directional", frame_index, 4)
		card.offset = Vector2(0.0, sin(timer * 1.65) * 1.8)
	m.g["lagoon_roshan_frame"] = frame_index
	var hop_t: float = maxf(0.0, float(m.g.get("lagoon_hop_t", 0.0)) - delta)
	m.g["lagoon_hop_t"] = hop_t
	card.position.y -= sin((hop_t / 0.32) * PI) * 26.0 if hop_t > 0.0 else 0.0

func _apply_view_transform(snap: bool = false) -> void:
	var content: Node2D = m.g.get("lagoon_master_space") as Node2D
	if content == null or not is_instance_valid(content):
		return
	var viewport_size: Vector2 = _viewport_size()
	var scale_factor: float = _master_scale(viewport_size)
	var camera_x: float = _camera_clamp_x(float(m.g.get("lagoon_camera_x", MASTER_SIZE.x * 0.5)))
	m.g["lagoon_camera_x"] = camera_x
	var left: float = camera_x - viewport_size.x / scale_factor * 0.5
	# Camera2D is the sole view transform. Content remains in literal master
	# pixels, which keeps rendering and the public coordinate helpers identical.
	content.scale = Vector2.ONE
	content.position = Vector2.ZERO
	var camera: Camera2D = camera_2d()
	if camera != null:
		camera.position = Vector2(camera_x, MASTER_SIZE.y * 0.5)
		camera.zoom = Vector2.ONE * scale_factor
	var rear: Node2D = m.g.get("lagoon_rear_layer") as Node2D
	if rear != null:
		rear.position.x = left * (1.0 - REAR_PARALLAX)
		rear.set_meta("observable_parallax_offset", rear.position.x)
	var foreground: Node2D = m.g.get("lagoon_foreground_layer") as Node2D
	if foreground != null:
		foreground.position.x = left * (1.0 - FOREGROUND_PARALLAX)
		foreground.set_meta("observable_parallax_offset", foreground.position.x)
	if snap:
		content.set_meta("transform_snapped", true)

func _viewport_size() -> Vector2:
	var size: Vector2 = m.get_viewport().get_visible_rect().size
	return size if size.x > 0.0 and size.y > 0.0 else Vector2(1280, 720)

func _master_scale(viewport_size: Vector2) -> float:
	return (viewport_size.y - VIEW_HEIGHT_MARGIN * 2.0) / MASTER_SIZE.y

func _camera_clamp_x(value: float) -> float:
	var viewport_size: Vector2 = _viewport_size()
	var half_master: float = viewport_size.x / _master_scale(viewport_size) * 0.5
	return clampf(value, half_master, MASTER_SIZE.x - half_master)

func _route_point_for_x(value: float) -> Vector2:
	for index: int in range(ROUTE_MASTER.size() - 1):
		var start: Vector2 = ROUTE_MASTER[index]
		var finish: Vector2 = ROUTE_MASTER[index + 1]
		if value <= finish.x:
			var amount: float = inverse_lerp(start.x, finish.x, value)
			return start.lerp(finish, amount)
	return ROUTE_MASTER[-1]

func _route_fraction(value: float) -> float:
	return inverse_lerp(ROUTE_MASTER[0].x, ROUTE_MASTER[-1].x, value)

func _closest_route_point(point: Vector2) -> Vector2:
	var best: Vector2 = ROUTE_MASTER[0]
	var best_distance: float = INF
	for index: int in range(ROUTE_MASTER.size() - 1):
		var start: Vector2 = ROUTE_MASTER[index]
		var finish: Vector2 = ROUTE_MASTER[index + 1]
		var segment: Vector2 = finish - start
		var amount: float = clampf((point - start).dot(segment) / maxf(segment.length_squared(), 0.001), 0.0, 1.0)
		var candidate: Vector2 = start + segment * amount
		var distance: float = candidate.distance_squared_to(point)
		if distance < best_distance:
			best = candidate
			best_distance = distance
	return best

func _tick_doorstep() -> void:
	var x: float = master_route_x()
	if x < CASTLE_DOOR_MASTER_X - DOORSTEP_REARM_MASTER:
		m.g["lagoon_castle_armed"] = true
		return
	if bool(m.g.get("lagoon_castle_armed", false)) \
			and x >= CASTLE_DOOR_MASTER_X - DOORSTEP_RADIUS_MASTER:
		m.g["lagoon_castle_armed"] = false
		m.g["lagoon_walk_goal_master"] = null
		_clear_focus()
		m._enter_castle_interior()

func _tick_plane_arrival(delta: float) -> void:
	var plane: Sprite2D = m.g.get("lagoon_plane_card") as Sprite2D
	if plane == null or not is_instance_valid(plane):
		return
	var timer: float = float(m.g.get("lagoon_plane_t", 0.0)) + delta
	m.g["lagoon_plane_t"] = timer
	plane.position.y += sin(timer * 2.2) * 0.12
	if timer < PLANE_DEPARTURE_S:
		return
	_finish_plane_arrival()

func _finish_plane_arrival() -> void:
	var plane: Sprite2D = m.g.get("lagoon_plane_card") as Sprite2D
	if plane != null and is_instance_valid(plane):
		var target_index: int = _target_index("reef_route")
		if target_index >= 0:
			var targets: Array = m.g.get("lagoon_promenade_targets", []) as Array
			var old_target: Dictionary = targets[target_index] as Dictionary
			var highlight: Sprite2D = old_target.get("highlight") as Sprite2D
			if highlight != null and is_instance_valid(highlight):
				if highlight.get_parent() != null:
					highlight.get_parent().remove_child(highlight)
				highlight.free()
			targets.remove_at(target_index)
		if plane.get_parent() != null:
			plane.get_parent().remove_child(plane)
		plane.free()
	m.g["lagoon_plane_card"] = null
	m.save_data["lagoon_plane_departed"] = true
	m._write_save()
	_build_reef_route_marker()

func _target_index(target_id: String) -> int:
	var targets: Array = m.g.get("lagoon_promenade_targets", []) as Array
	for index: int in range(targets.size()):
		if String((targets[index] as Dictionary).get("id", "")) == target_id:
			return index
	return -1

func _show_reef_route_guidance() -> void:
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == "reef_route":
			_focus(target)
			break
	m.show_msg("Roshan", "Tap the pearl plane to visit the Reef!", "intro4")

func _tick_ambient_life(delta: float) -> void:
	var timer: float = fmod(float(m.g.get("lagoon_ambient_t", 0.0)) + delta, 3600.0)
	m.g["lagoon_ambient_t"] = timer
	for value: Variant in m.g.get("lagoon_ambient_cards", []) as Array:
		var card: Sprite2D = value as Sprite2D
		if card == null or not is_instance_valid(card):
			continue
		match String(card.get_meta("ambient_kind", "")):
			"tree":
				card.rotation = sin(timer * 0.72) * 0.010
			"foreground_tree":
				card.rotation = sin(timer * 0.78 + 0.7) * 0.008
			"cloud":
				var base: Vector2 = card.get_meta("ambient_base", card.position) as Vector2
				# Bounded triangle drift starts exactly at the authored socket and
				# never teleports when its quiet 32-second cycle wraps.
				var phase: float = fposmod(timer, 32.0) / 32.0
				card.position.x = base.x + (1.0 - absf(phase * 2.0 - 1.0)) * 520.0
			"smoke":
				var base: Vector2 = card.get_meta("ambient_base", card.position) as Vector2
				var phase: float = fposmod(timer + float(card.get_meta("phase", 0.0)), 6.0) / 6.0
				card.position.y = base.y - phase * 78.0
				card.modulate.a = sin(phase * PI) * 0.62
	for value: Variant in m.g.get("lagoon_night_fireflies", []) as Array:
		var fly: Sprite2D = value as Sprite2D
		if fly != null and is_instance_valid(fly):
			var phase: float = timer * 1.7 + float(fly.get_index()) * 0.83
			fly.modulate.a = 0.25 + (sin(phase) * 0.5 + 0.5) * 0.72

func _animal_page_index() -> int:
	return clampi(int(floor(float(m.g.get("lagoon_camera_x", 0.0)) / 2048.0)), 0, 2)

func _animal_definition(animal_id: String) -> Dictionary:
	for definition: Dictionary in ANIMAL_DEFS:
		if String(definition["id"]) == animal_id:
			return definition
	return {}

func _animal_definitions_for_page(page: int) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for definition: Dictionary in ANIMAL_DEFS:
		if int(definition["page"]) == page:
			result.append(definition)
	return result

func _animal_path_is_safe(definition: Dictionary) -> bool:
	var path: Array = definition.get("path", []) as Array
	if path.size() < 2 or float(definition.get("height", 0.0)) <= 0.0:
		return false
	for value: Variant in path:
		var point: Vector2 = value as Vector2
		if _closest_route_point(point).distance_to(point) < 115.0:
			return false
	return true

func _bind_next_animal(page: int) -> bool:
	var definitions: Array[Dictionary] = _animal_definitions_for_page(page)
	if definitions.is_empty():
		return false
	var cycles: Dictionary = m.g.get("lagoon_animal_cycles", {}) as Dictionary
	return _bind_animal(definitions[int(cycles.get(page, 0)) % definitions.size()])

func _bind_animal_id(animal_id: String) -> bool:
	var definition: Dictionary = _animal_definition(animal_id)
	return false if definition.is_empty() else _bind_animal(definition)

func _bind_animal(definition: Dictionary) -> bool:
	if not _animal_path_is_safe(definition):
		return false
	if bool(definition.get("requires_plane_departed", false)) \
			and not bool(m.save_data.get("lagoon_plane_departed", false)):
		return false
	var actor: Dictionary = m.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite2D = actor.get("node") as Sprite2D
	if node == null or not is_instance_valid(node):
		return false
	var path: Array = definition["path"] as Array
	node.texture = load(String(definition["idle"])) as Texture2D
	node.region_enabled = true
	node.region_rect = Rect2(Vector2.ZERO, Vector2(256, 256))
	node.position = path[0] as Vector2
	node.scale = Vector2.ONE * (float(definition["height"]) / 256.0)
	node.modulate = definition["night_tint"] as Color if m.is_night else definition["day_tint"] as Color
	node.visible = true
	node.set_meta("animal_id", String(definition["id"]))
	actor["definition"] = definition
	actor["page"] = int(definition["page"])
	actor["state"] = "idle"
	actor["state_t"] = 0.0
	actor["route_position"] = node.position
	actor["path_index"] = 1
	_sync_contact_shadow(node)
	return true

func _hide_animal(actor: Dictionary, delay: float, advance_roster: bool) -> void:
	var node: Sprite2D = actor.get("node") as Sprite2D
	if node != null and is_instance_valid(node):
		node.visible = false
	actor["state"] = "hidden"
	actor["spawn_t"] = delay
	if advance_roster:
		var page: int = int(actor.get("page", -1))
		var cycles: Dictionary = m.g.get("lagoon_animal_cycles", {}) as Dictionary
		cycles[page] = int(cycles.get(page, 0)) + 1
	_sync_contact_shadow(node)

func _tick_animals(delta: float) -> void:
	var actor: Dictionary = m.g.get("lagoon_animal_actor", {}) as Dictionary
	if actor.is_empty():
		return
	var page: int = _animal_page_index()
	if int(actor.get("page", -1)) != page:
		_hide_animal(actor, ANIMAL_PAGE_SPAWN_S, false)
		actor["page"] = page
	var state: String = String(actor.get("state", "hidden"))
	if state == "hidden":
		actor["spawn_t"] = float(actor.get("spawn_t", 0.0)) - delta
		if float(actor["spawn_t"]) <= 0.0:
			_bind_next_animal(page)
		return
	if state == "startle":
		_tick_animal_startle(actor, delta)
	else:
		_tick_animal_idle(actor, delta)

func _tick_animal_idle(actor: Dictionary, delta: float) -> void:
	var node: Sprite2D = actor.get("node") as Sprite2D
	var definition: Dictionary = actor.get("definition", {}) as Dictionary
	if node == null or definition.is_empty():
		return
	var path: Array = definition["path"] as Array
	var index: int = int(actor.get("path_index", 1))
	var target: Vector2 = path[index] as Vector2
	var old_x: float = node.position.x
	node.position = node.position.move_toward(target, float(definition["speed"]) * delta)
	if node.position.distance_to(target) < 1.0:
		var direction: int = int(actor.get("path_direction", 1))
		if index >= path.size() - 1 or index <= 0:
			direction *= -1
		actor["path_direction"] = direction
		actor["path_index"] = clampi(index + direction, 0, path.size() - 1)
	node.flip_h = node.position.x < old_x
	var timer: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = timer
	var frame: int = int(floor(timer / float(definition["frame_s"]))) % 4
	node.region_rect = Rect2(Vector2(float(frame % 2), float(frame / 2)) * 256.0, Vector2(256, 256))
	actor["route_position"] = node.position
	_sync_contact_shadow(node)

func _startle_animal(actor: Dictionary) -> void:
	var node: Sprite2D = actor.get("node") as Sprite2D
	var definition: Dictionary = actor.get("definition", {}) as Dictionary
	if node == null or definition.is_empty():
		return
	actor["state"] = "startle"
	actor["state_t"] = 0.0
	node.texture = load(String(definition["startle"])) as Texture2D

func _tick_animal_startle(actor: Dictionary, delta: float) -> void:
	var node: Sprite2D = actor.get("node") as Sprite2D
	var definition: Dictionary = actor.get("definition", {}) as Dictionary
	if node == null or definition.is_empty():
		return
	var timer: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = timer
	var alert_end: float = ANIMAL_STARTLE_ALERT_S
	var squash_end: float = alert_end + ANIMAL_STARTLE_SQUASH_S
	var hop_end: float = squash_end + ANIMAL_STARTLE_HOP_S
	var frame: int = 0 if timer < alert_end else 1 if timer < squash_end else 2 if timer < hop_end else 3
	node.region_rect = Rect2(Vector2(float(frame % 2), float(frame / 2)) * 256.0, Vector2(256, 256))
	if timer >= squash_end:
		node.position.x += float(definition["exit_speed"]) * delta * (-1.0 if node.position.x < float(m.g.get("lagoon_camera_x", 0.0)) else 1.0)
		node.position.y -= sin(clampf((timer - squash_end) / ANIMAL_STARTLE_HOP_S, 0.0, 1.0) * PI) * 3.0
	if timer >= hop_end + 0.45:
		_hide_animal(actor, ANIMAL_RESPAWN_S, true)
	_sync_contact_shadow(node)

func _animal_at(screen_pos: Vector2) -> Dictionary:
	var actor: Dictionary = m.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite2D = actor.get("node") as Sprite2D
	if node == null or not is_instance_valid(node) or not node.visible \
			or String(actor.get("state", "")) == "startle":
		return {}
	return actor if screen_from_master(node.position).distance_to(screen_pos) <= ANIMAL_TOUCH_RADIUS_PX else {}

func _start_playground_animation(kind: String, equipment: Node2D) -> void:
	if not PLAY_FRAME_PATHS.has(kind) or equipment == null \
			or not is_instance_valid(equipment):
		return
	var frames: Array[Texture2D] = []
	for path_value: Variant in PLAY_FRAME_PATHS[kind]:
		frames.append(load(String(path_value)) as Texture2D)
	if frames.size() != 4:
		return
	m.g["lagoon_walk_goal_master"] = null
	m.g["lagoon_play_anim"] = {
		"kind": kind, "phase": "action", "t": 0.0,
		"dur": float(PLAY_DURATIONS[kind]), "equipment": equipment,
		"equipment_rotation": equipment.rotation, "frames": frames,
		"frame_index": -1,
		"equipment_rest_rotation": equipment.rotation,
	}
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if card != null:
		# Playground poses are authored in one facing. Route movement may have
		# left the pooled card mirrored after approaching a toy from the right.
		card.flip_h = false
	_set_play_frame(0)
	# Place the first pose on its authored contact socket immediately. Waiting
	# for the next process tick exposes one frame at Roshan's old route position.
	match kind:
		"swing": _tick_swing_animation(card, equipment, 0.0)
		"slide": _tick_slide_animation(card, equipment, 0.0)
		"seesaw": _tick_seesaw_animation(card, equipment, 0.0)

func _set_play_frame(frame_index: int) -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {}) as Dictionary
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if play.is_empty() or card == null or frame_index < 0 or frame_index >= 4:
		return
	if int(play.get("frame_index", -1)) == frame_index:
		return
	play["frame_index"] = frame_index
	card.texture = (play.get("frames", []) as Array)[frame_index] as Texture2D
	card.region_enabled = false
	card.offset = Vector2.ZERO
	card.scale = Vector2.ONE * (PLAY_ROSHAN_HEIGHT_PX / maxf(1.0, card.texture.get_height()))

func _play_anchor_local(card: Sprite2D, anchor_pixels: Vector2) -> Vector2:
	var texture_size: Vector2 = card.texture.get_size()
	var local: Vector2 = anchor_pixels - texture_size * 0.5 + card.offset
	local *= card.scale
	return local.rotated(card.rotation)

func _play_anchor_master(card: Sprite2D, anchor_pixels: Vector2) -> Vector2:
	var master_space: Node2D = m.g.get("lagoon_master_space") as Node2D
	if master_space == null:
		return card.position + _play_anchor_local(card, anchor_pixels)
	var texture_size: Vector2 = card.texture.get_size()
	var anchor_local: Vector2 = anchor_pixels - texture_size * 0.5 + card.offset
	return master_space.to_local(card.to_global(anchor_local))

func _place_play_anchor(card: Sprite2D, equipment: Node2D,
		anchor_pixels: Vector2, socket_offset: Vector2) -> void:
	var card_parent: Node2D = card.get_parent() as Node2D
	if card_parent == null:
		return
	var socket_parent: Vector2 = card_parent.to_local(equipment.to_global(socket_offset))
	card.position = socket_parent - _play_anchor_local(card, anchor_pixels)

func _tick_playground_animation(delta: float) -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {}) as Dictionary
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if play.is_empty() or card == null:
		return
	if String(play.get("phase", "action")) == "settle":
		_tick_playground_settle(card, play, delta)
		return
	var equipment_value: Variant = play.get("equipment")
	var equipment: Node2D = null
	if is_instance_valid(equipment_value):
		equipment = equipment_value as Node2D
	if equipment == null:
		_finish_playground_animation()
		return
	var timer: float = float(play.get("t", 0.0)) + delta
	play["t"] = timer
	match String(play.get("kind", "")):
		"swing": _tick_swing_animation(card, equipment, timer)
		"slide": _tick_slide_animation(card, equipment, timer)
		"seesaw": _tick_seesaw_animation(card, equipment, timer)
	_sync_contact_shadow(card)
	if timer >= float(play.get("dur", 0.0)):
		_finish_playground_animation()

func _tick_swing_animation(card: Sprite2D, swing: Node2D, timer: float) -> void:
	var phase: float = timer * TAU / 1.72
	var angle: float = sin(phase) * 0.20
	var pivot: Node2D = swing.get_meta("swing_seat_pivot") as Node2D \
		if swing.has_meta("swing_seat_pivot") else null
	if pivot != null:
		pivot.rotation = angle
	var frame: int = 1 if sin(phase) > 0.34 else 2 if sin(phase) < -0.34 else 3 if cos(phase) < 0.0 else 0
	_set_play_frame(frame)
	card.rotation = angle * 0.65
	var grip_socket: Vector2 = (pivot.position if pivot != null else Vector2(0.0, -258.0)) \
		+ Vector2(0.0, SWING_GRIP_LENGTH_MASTER).rotated(angle)
	_place_play_anchor(card, swing, SWING_SEAT_ANCHORS[frame], grip_socket)

func _tick_slide_animation(card: Sprite2D, slide: Node2D, timer: float) -> void:
	if timer < 2.55:
		var progress: float = clampf(timer / 2.55, 0.0, 1.0)
		_set_play_frame(int(floor(progress * 5.0)) % 2)
		card.position = slide.position + Vector2(-135.0 + progress * 65.0,
			95.0 - progress * 435.0 - sin(progress * 5.0 * PI) * 18.0)
		card.rotation = 0.03
	elif timer < 3.15:
		_set_play_frame(2)
		var settle: float = smoothstep(0.0, 1.0, (timer - 2.55) / 0.60)
		card.position = slide.position + Vector2(-70.0, -340.0).lerp(
			SLIDE_RIDE_START_MASTER, settle)
		card.rotation = lerpf(0.03, 0.12, settle)
	else:
		_set_play_frame(3)
		var ride: float = smoothstep(0.0, 1.0, clampf((timer - 3.15) / 2.05, 0.0, 1.0))
		var first: Vector2 = SLIDE_RIDE_START_MASTER.lerp(SLIDE_RIDE_CONTROL_MASTER, ride)
		var second: Vector2 = SLIDE_RIDE_CONTROL_MASTER.lerp(SLIDE_RIDE_FINISH_MASTER, ride)
		card.position = slide.position + first.lerp(second, ride)
		card.rotation = lerpf(0.12, 0.42, ride)

func _tick_seesaw_animation(card: Sprite2D, seesaw: Node2D, timer: float) -> void:
	var phase: float = timer * TAU / 1.92
	var rock: float = sin(phase) * 0.105
	var play: Dictionary = m.g.get("lagoon_play_anim", {}) as Dictionary
	# Always sample from the immutable authored rest angle. Adding each sine
	# sample to the previous frame accumulated nearly a radian during one ride.
	seesaw.rotation = float(play.get("equipment_rest_rotation", 0.0)) + rock
	var frame: int = 2 if sin(phase) > 0.45 else 0 if sin(phase) < -0.45 else 1 if cos(phase) > 0.0 else 3
	_set_play_frame(frame)
	card.rotation = rock
	card.scale = Vector2.ONE * (PLAY_ROSHAN_HEIGHT_PX \
		/ maxf(1.0, float(card.texture.get_height()))) * 1.12
	_place_play_anchor(card, seesaw, SEESAW_SEAT_ANCHORS[frame],
		SEESAW_RIGHT_SEAT_SOCKET_MASTER)
	play["equipment_rotation"] = seesaw.rotation

func _sprite_alpha_bounds_master(sprite: Sprite2D) -> Rect2:
	if sprite == null or sprite.texture == null:
		return Rect2()
	var image: Image = sprite.texture.get_image()
	if image == null or image.is_empty():
		return Rect2()
	if image.is_compressed() and image.decompress() != OK:
		return Rect2()
	var source := Rect2i(Vector2i.ZERO, image.get_size())
	if sprite.region_enabled and sprite.region_rect.size.x > 0.0 \
			and sprite.region_rect.size.y > 0.0:
		source = Rect2i(sprite.region_rect)
	var alpha_min := Vector2i(source.end.x, source.end.y)
	var alpha_max := Vector2i(source.position.x - 1, source.position.y - 1)
	for y: int in range(source.position.y, source.end.y):
		for x: int in range(source.position.x, source.end.x):
			if image.get_pixel(x, y).a < 0.10:
				continue
			alpha_min.x = mini(alpha_min.x, x)
			alpha_min.y = mini(alpha_min.y, y)
			alpha_max.x = maxi(alpha_max.x, x)
			alpha_max.y = maxi(alpha_max.y, y)
	if alpha_max.x < alpha_min.x or alpha_max.y < alpha_min.y:
		return Rect2()
	var local_top_left: Vector2 = sprite.offset
	if sprite.centered:
		local_top_left -= Vector2(source.size) * 0.5
	var local_min := local_top_left + Vector2(alpha_min - source.position)
	var local_max := local_top_left + Vector2(alpha_max - source.position)
	var corners: Array[Vector2] = [
		sprite.transform * local_min,
		sprite.transform * Vector2(local_max.x, local_min.y),
		sprite.transform * local_max,
		sprite.transform * Vector2(local_min.x, local_max.y),
	]
	var bounds := Rect2(corners[0], Vector2.ZERO)
	for corner: Vector2 in corners:
		bounds = bounds.expand(corner)
	return bounds

func _sprite_alpha_top_master(sprite: Sprite2D) -> float:
	var bounds: Rect2 = _sprite_alpha_bounds_master(sprite)
	return bounds.position.y if bounds.get_area() > 0.0 else sprite.position.y \
		- _sprite_draw_height(sprite) * 0.5

func _finish_playground_animation() -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {}) as Dictionary
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if play.is_empty() or card == null or String(play.get("phase", "")) == "settle":
		return
	var equipment_value: Variant = play.get("equipment")
	var equipment: Node2D = null
	if is_instance_valid(equipment_value):
		equipment = equipment_value as Node2D
	if equipment != null:
		equipment.rotation = float(play.get("equipment_rest_rotation", 0.0))
		var pivot: Node2D = equipment.get_meta("swing_seat_pivot") as Node2D \
			if equipment.has_meta("swing_seat_pivot") else null
		if pivot != null:
			pivot.rotation = 0.0
	play["phase"] = "settle"
	play["settle_t"] = 0.0
	play["settle_start_position"] = card.position
	play["settle_start_rotation"] = card.rotation

func _tick_playground_settle(card: Sprite2D, play: Dictionary, delta: float) -> void:
	var timer: float = minf(float(play.get("settle_t", 0.0)) + delta, PLAY_SETTLE_S)
	play["settle_t"] = timer
	var progress: float = timer / PLAY_SETTLE_S
	var target: Vector2 = Vector2(float(m.g.get("lagoon_master_x", 0.0)),
		float(m.g.get("lagoon_master_y", 0.0)) - PLAYER_HEIGHT_PX * 0.47)
	card.position = (play.get("settle_start_position", card.position) as Vector2).lerp(target,
		smoothstep(0.0, 1.0, progress)) - Vector2(0.0, sin(progress * PI) * PLAY_SETTLE_HOP)
	card.rotation = lerp_angle(float(play.get("settle_start_rotation", 0.0)), 0.0, progress)
	if timer < PLAY_SETTLE_S:
		return
	m.g["lagoon_play_anim"] = {}
	card.texture = ROSHAN_DIRECTIONAL
	card.region_enabled = true
	card.region_rect = FRAMES.region("directional", 2, 4)
	card.scale = Vector2.ONE * (PLAYER_HEIGHT_PX / 256.0)
	card.rotation = 0.0
	_sync_roshan_card()

func _celebrate_visible_roshan() -> void:
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	if card == null or not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		return
	card.scale = Vector2(1.07, 0.93) * (PLAYER_HEIGHT_PX / 256.0)
	var tween: Tween = m.create_tween()
	tween.tween_property(card, "scale", Vector2.ONE * (PLAYER_HEIGHT_PX / 256.0), 0.26).set_trans(Tween.TRANS_BACK)

func _stop_visible_roshan_celebration() -> void:
	pass

func _sprite_draw_height(sprite: Sprite2D) -> float:
	if sprite == null or sprite.texture == null:
		return 0.0
	var source_height: float = sprite.region_rect.size.y \
		if sprite.region_enabled and sprite.region_rect.size.y > 0.0 \
		else float(sprite.texture.get_height())
	return source_height * absf(sprite.scale.y)
