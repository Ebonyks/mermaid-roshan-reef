class_name SkyLagoonPromenade
extends RefCounted
# The Sky Lagoon's three-page 2.5D promenade. The painted PNW flats and
# transparent Codex sprites do the visual work; the real Roshan rig walks in
# one shallow band in front of them. All mutable state remains on ReefMain.

const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")
const Affordance := preload("res://scripts/interaction_affordance.gd")
const OPAQUE_STORYBOOK_CUTOUT_SHADER := preload(
	"res://assets/shaders/opaque_storybook_cutout.gdshader")
const WATER_ANIMAL_BODY := preload("res://scripts/arena/sky_lagoon_water_body.gd")
const HALF_W := 72.0
const HALF_D := 2.6
const BACKDROP_TILE_SIZE := Vector2(24.0, 24.0)
const BACKDROP_COLUMNS := 6
const BACKDROP_ROWS := 2
const BACKDROP_Z := -18.0
const CONTACT_SHADOW_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png"
const SMOKE_WISP_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png"
const FIREFLY_TEX := "res://assets/fairy/sprites/bug_firefly.png"
const FIREFLY_COUNT := 18
# THE PAINTING IS THE SCREEN. The 6x2 lossless Sprite3D grid reconstructs one
# native 6144x2048, 144x48-world-unit mural. Each 1024px square is a separate
# unshaded depth card, retaining the higher detail generated per square.
# The lens is sized so the frame lands INSIDE it: the camera sits far enough
# back that the frustum is ~45 units tall where it
# crosses the mural (1.6 units of painted margin top and bottom) and pans only
# as far as SideScrollStage.screen_pan_limit allows. Nothing outside the
# painting can enter frame, so no environment sky is ever visible.
#   Mural: y in [-14.5, 33.5] (centre BACKDROP_CENTER_Y), x in [-72, 72].
#   Lens:  horizontal (look_h == cam_h), so the view centre is CAM_H at every
#          depth — Roshan's 7.8-unit card reads ~24% of frame height with her
#          feet at ~79% down, standing on the painted lawn.
const CAM_DIST := 47.0
const CAM_H := 9.5
const CAM_FOV := 38.0
const BACKDROP_CENTER_Y := CAM_H
# the walk band read off the painted lawn: the touch projection maps this
# window of screen height into the shallow depth band
const BAND_Y := -5.0
const BAND_H := 10.0
# a press has to be held this long on open ground before it becomes follow-the-
# finger travel; below it the press still belongs to the tap router
const HOLD_TRAVEL_S := 0.20
# REAL STORYBOOK DEPTH. The clean v5 plate has the extracted props removed,
# so every restored card can occupy an intentional plane without doubling a
# painted copy. Heights and y positions are perspective-compensated for these
# depths, preserving the approved 720p composition while allowing restrained
# parallax and correct player occlusion.
const CLOUD_Z := -16.0       # drifting sky card
const LANDMARK_Z := -11.0    # pearl plane and castle facade
const DRESS_Z := -9.0        # rear PNW foliage
const PLAY_Z := -6.0         # playground standees
const NEAR_Z := -1.5         # near PNW foliage, inside the walk-depth band
const SMOKE_Z := -10.5       # clears the castle cutout's transparent depth card
# Landmarks retain restrained physical parallax. Playground equipment and
# smoke origins are exact mural sockets: they remain Sprite3D cards at real
# depth for occlusion, but compensate the entire camera-depth offset so they
# cannot slide loose from the painted lawn/roof as Roshan crosses the stage.
const DEFAULT_MURAL_SOCKET_LOCK := 0.65
const GROUND_SOCKET_LOCK := 1.0
const CLOUD_DRIFT_MIN_X := -10.0
const CLOUD_DRIFT_MAX_X := 10.0
const WIND_DIRECTION := 1.0
const WIND_GUST_PERIOD_S := 24.0
const WIND_GUST_RISE_AT_S := 16.0
const WIND_GUST_PEAK_AT_S := 18.0
const WIND_GUST_FALL_AT_S := 21.0
# Three cabin roof/flue origins measured on the native 6144x2048 mural at
# master pixels (4798,419), (4591,581), and (4806,669), then
# perspective-compensated from BACKDROP_Z to SMOKE_Z at the approved
# screen-three framing. The middle cabin intentionally keeps the roof
# representation already baked into the approved mural; no chimney sticker is
# added. Each receives one staggered thin-wisp card, preserving the former
# three-card smoke budget while bringing every cabin to life.
const CABIN_SMOKE_ANCHORS := [
	Vector3(41.323918, 22.043570, SMOKE_Z),
	Vector3(37.032151, 18.684796, SMOKE_Z),
	Vector3(41.489784, 16.860276, SMOKE_Z),
]
const SMOKE_CARD_HEIGHT := 2.2
const SMOKE_LIFETIME_S := 6.0
const ANIMAL_ATLAS_COLUMNS := 2
const ANIMAL_ATLAS_ROWS := 2
const ANIMAL_STARTLE_ALERT_S := 0.24
const ANIMAL_STARTLE_SQUASH_S := 0.18
const ANIMAL_STARTLE_HOP_S := 0.24
const ANIMAL_BRUSH_ENTRY_S := 0.48
const ANIMAL_TREE_CLIMB_S := 1.05
const ANIMAL_PAGE_SPAWN_S := 0.70
const ANIMAL_RESPAWN_S := 5.5
const ANIMAL_TOUCH_RADIUS_PX := 114.0
const ANIMAL_ROUTE_CLEARANCE := 1.25
const ANIMAL_SUPPORT_RECTS: Dictionary = {
	"arrival_water": Rect2(-60.2, 2.0, 3.7, 1.4),
	"west_path_shoulder_ground": Rect2(-21.2, -2.4, 4.5, 0.8),
	"castle_path_shoulder_ground": Rect2(27.2, -2.4, 4.3, 0.8),
}
# One pooled animal card is intentional. It keeps the five-species roster in
# the game without adding ten permanently visible transparent cards to the
# Speedy scene. Each camera page owns an ecological roster; tapping an animal
# advances that page to its next species after the animal exits.
const ANIMAL_PAGE_CENTERS := [-48.0, 0.0, 48.0]
const ANIMAL_EXCLUSION_RECTS: Array[Dictionary] = [
	{"id": "screen_1_2_seam", "rect": Rect2(-27.0, -2.0, 6.0, 10.0)},
	{"id": "screen_2_3_seam", "rect": Rect2(21.0, -2.0, 6.0, 10.0)},
	{"id": "slide", "rect": Rect2(-17.0, -1.0, 11.0, 14.0)},
	{"id": "swing", "rect": Rect2(-3.0, -1.0, 12.0, 14.5)},
	{"id": "seesaw", "rect": Rect2(11.0, -1.5, 12.0, 7.0)},
	{"id": "drawbridge_and_door", "rect": Rect2(40.0, -2.0, 18.0, 10.0)},
]
const ANIMAL_DEFS: Array[Dictionary] = [
	{
		"id": "otter",
		"page": 0,
		"habitat": "arrival_shore",
		"support": "water_jolt",
		"support_zone": "arrival_water",
		"idle": "res://assets/sprites/sky_lagoon/animals/otter_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/otter_startle_atlas.png",
		"path": [
			Vector3(-59.8, 2.72, -5.8),
			Vector3(-58.2, 2.72, -5.8),
			Vector3(-56.8, 2.72, -5.8),
		],
		"height": 2.6,
		"speed": 0.52,
		"exit_speed": 12.0,
		"frame_s": 0.26,
		"dwell_s": 1.4,
		"bob": 0.045,
		"locomotion": "waddle",
		"refuge_kind": "brush",
		"refuge_point": Vector3(-60.0, 2.72, -5.8),
		"refuge_fx_point": Vector3(-60.85, 4.85, -5.72),
		"refuge_speed": 3.2,
		"requires_plane_departed": true,
		"water_surface_y": 2.72,
		"water_mass": 1.35,
		"water_wave": 0.075,
		"day_tint": Color(0.92, 1.00, 1.08, 1.0),
		"night_tint": Color(0.70, 0.98, 1.0, 1.0),
		"shadow_day": Color(0.38, 0.58, 0.70, 0.34),
		"shadow_night": Color(0.24, 0.36, 0.58, 0.30),
	},
	{
		"id": "frog",
		"page": 0,
		"habitat": "arrival_shore",
		"support": "water_jolt",
		"support_zone": "arrival_water",
		"idle": "res://assets/sprites/sky_lagoon/animals/frog_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/frog_startle_atlas.png",
		"path": [
			Vector3(-59.6, 2.55, -6.1),
			Vector3(-58.1, 2.55, -6.1),
			Vector3(-56.8, 2.55, -6.1),
		],
		"height": 1.65,
		"speed": 0.72,
		"exit_speed": 10.5,
		"frame_s": 0.30,
		"dwell_s": 1.7,
		"bob": 0.18,
		"locomotion": "hop",
		"refuge_kind": "brush",
		"refuge_point": Vector3(-60.0, 2.55, -6.1),
		"refuge_fx_point": Vector3(-60.85, 4.68, -6.02),
		"refuge_speed": 3.5,
		"requires_plane_departed": true,
		"water_surface_y": 2.55,
		"water_mass": 0.55,
		"water_wave": 0.11,
		"day_tint": Color(0.96, 1.06, 1.02, 1.0),
		"night_tint": Color(0.72, 0.82, 1.0, 1.0),
		"shadow_day": Color(0.34, 0.55, 0.66, 0.30),
		"shadow_night": Color(0.22, 0.34, 0.56, 0.28),
	},
	{
		"id": "hare",
		"page": 1,
		"habitat": "west_path_shoulder",
		"support": "ground",
		"support_zone": "west_path_shoulder_ground",
		"idle": "res://assets/sprites/sky_lagoon/animals/hare_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/hare_startle_atlas.png",
		"path": [
			Vector3(-20.7, -0.55, -4.8),
			Vector3(-18.9, -0.48, -4.8),
			Vector3(-17.2, -0.53, -4.8),
		],
		"height": 3.1,
		"speed": 0.66,
		"exit_speed": 13.5,
		"frame_s": 0.28,
		"dwell_s": 1.6,
		"bob": 0.12,
		"locomotion": "hop",
		"refuge_kind": "brush",
		"refuge_point": Vector3(-16.82, -0.55, -4.8),
		"refuge_fx_point": Vector3(-16.72, -0.05, -4.72),
		"refuge_speed": 6.4,
		"day_tint": Color(0.95, 0.99, 1.03, 1.0),
		"night_tint": Color(0.68, 0.77, 0.99, 1.0),
		"shadow_day": Color(0.29, 0.34, 0.42, 0.36),
		"shadow_night": Color(0.20, 0.25, 0.46, 0.30),
	},
	{
		"id": "squirrel",
		"page": 2,
		"habitat": "castle_fir_edge",
		"support": "ground",
		"support_zone": "castle_path_shoulder_ground",
		"idle": "res://assets/sprites/sky_lagoon/animals/squirrel_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/squirrel_startle_atlas.png",
		"path": [
			Vector3(27.45, -0.68, -7.2),
			Vector3(28.65, -0.60, -7.2),
			Vector3(29.85, -0.65, -7.2),
		],
		"height": 2.9,
		"speed": 0.82,
		"exit_speed": 14.5,
		"frame_s": 0.22,
		"dwell_s": 1.25,
		"bob": 0.055,
		"locomotion": "scamper",
		"refuge_kind": "tree",
		"refuge_point": Vector3(27.25, -0.68, -7.2),
		"refuge_climb_point": Vector3(26.10, 6.10, -7.2),
		"refuge_fx_point": Vector3(26.10, 6.35, -7.12),
		"refuge_speed": 7.2,
		"day_tint": Color(0.84, 0.97, 1.05, 1.0),
		"night_tint": Color(0.66, 0.84, 1.0, 1.0),
		"shadow_day": Color(0.27, 0.34, 0.40, 0.34),
		"shadow_night": Color(0.19, 0.24, 0.44, 0.29),
	},
	{
		"id": "raccoon",
		"page": 2,
		"habitat": "castle_path_shoulder",
		"support": "ground",
		"support_zone": "castle_path_shoulder_ground",
		"idle": "res://assets/sprites/sky_lagoon/animals/raccoon_idle_atlas.png",
		"startle": "res://assets/sprites/sky_lagoon/animals/raccoon_startle_atlas.png",
		"path": [
			Vector3(28.3, -0.60, -7.0),
			Vector3(29.5, -0.52, -7.0),
			Vector3(30.5, -0.58, -7.0),
		],
		"height": 3.0,
		"speed": 0.58,
		"exit_speed": 13.0,
		"frame_s": 0.29,
		"dwell_s": 1.8,
		"bob": 0.035,
		"locomotion": "amble",
		"refuge_kind": "brush",
		"refuge_point": Vector3(31.35, -0.58, -7.0),
		"refuge_fx_point": Vector3(31.28, -0.03, -6.92),
		"refuge_speed": 6.0,
		"day_tint": Color(1.06, 1.08, 1.12, 1.0),
		"night_tint": Color(0.78, 0.86, 1.0, 1.0),
		"shadow_day": Color(0.27, 0.32, 0.40, 0.37),
		"shadow_night": Color(0.19, 0.24, 0.45, 0.31),
	},
]
const NIGHT_WORLD_TINT := Color(0.72, 0.78, 0.96, 1.0)
const NIGHT_BACKDROP_TINT := Color(0.48, 0.56, 0.82, 1.0)
const PLANE_DEPARTURE_S := 7.0
const SLIDE_H := 11.4
const SWING_H := 10.8
const SEESAW_H := 4.5
const SLIDE_ANIM_SCALE := SLIDE_H / 19.1
const SEESAW_ANIM_SCALE := SEESAW_H / 11.35
const PLAY_ROSHAN_H := 8.34
const SWING_FRAME_TEX := "res://assets/props/story/play_swing_frame.png"
const SWING_SEAT_TEX := "res://assets/props/story/play_swing_seat.png"
const SWING_ARM_H := 7.55
const SWING_SEAT_W := 4.6
const SWING_GRIP_ARM := 5.05
const SWING_SEAT_CONTACT_ANCHOR := Vector2(200.0, 360.0)
const SWING_PERIOD_S := 1.72
const SWING_MAX_ANGLE := 0.20
const OPAQUE_CUTOUT_ALPHA_THRESHOLD := 0.24
# The generated play frames do not share a consistent transparent-canvas
# origin. Anchor the visible action point instead of the 512x512 canvas centre,
# or Roshan jumps several world units between poses.
const SWING_HAND_ANCHORS := [
	Vector2(264.5, 204.5),
	Vector2(168.0, 205.0),
	Vector2(322.5, 186.0),
	Vector2(186.0, 184.5),
]
const SEESAW_SEAT_ANCHORS := [
	Vector2(300.0, 420.0),
	Vector2(225.0, 400.0),
	Vector2(270.0, 340.0),
	Vector2(220.0, 360.0),
]
# The seesaw pose faces left, so Roshan belongs on the right shell seat facing
# its inward hoop. Placing this pose on the left seat put her below and outside
# the beam.
const SEESAW_RIGHT_SEAT_SOCKET := Vector2(3.84, 0.16)
const PLAY_FRAME_PATHS := {
	"swing": [
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3.png",
	],
	"slide": [
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3.png",
	],
	"seesaw": [
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_3.png",
	],
}
const PLAY_DURATIONS := {"swing": 5.6, "slide": 5.4, "seesaw": 5.8}

# THE ROUTE THROUGH THE LEVEL (owner request 2026-07-27: "she should have a
# clear routing path through the level as well"). The promenade is a path, not
# an open field: the stone way from the pearl-plane dock, along the shore,
# across the lawn, up the drawbridge, to the castle door. Waypoints are in
# PAINTED coordinates - (mural x, painted ground y) - because that is where
# the way visibly is; _walk_x/_walk_y convert them into the plane Roshan
# actually walks, which is 18 units nearer the lens and therefore does NOT
# share the painting's x scale once the lens pins at a painted edge.
# A touch anywhere still works; it resolves onto this line.
const ROUTE_PAINTED := [
	Vector2(-68.0, -2.6),    # the stepping stones by the pearl plane
	Vector2(-58.0, -3.4),    # the shore path
	Vector2(-40.0, -4.0),    # the path's near edge
	Vector2(-20.0, -3.6),    # onto the lawn
	Vector2(0.0, -3.4),      # the playground lawn
	Vector2(20.0, -3.6),     # the lawn's far side
	Vector2(34.0, -4.0),     # the way to the castle
	Vector2(43.0, -2.6),     # the drawbridge deck
	Vector2(52.5, -2.0),     # the castle doorstep - walking here goes inside
]
const CASTLE_DOOR_X := 52.5      # painted x of the door, shared with the gate card
const DOORSTEP_R := 1.5          # how close counts as arriving at the door
const DOORSTEP_REARM := 8.0      # walk this far back before it can fire again
const CASTLE_CARD_SIZE := Vector2(1022.0, 1024.0)
const CASTLE_DOOR_FOCUS_BOUNDS := Rect2(
	Vector2(410.0, 557.0), Vector2(199.0, 228.0))
# Roshan's card hangs 1.0 above her node and stands 7.8 tall, so her feet are
# 2.9 below the node: the offset that turns a painted ground height into hover.
const FOOT_OFFSET := 2.9

var m: ReefMain
var stage: SideScrollStage

func _init(main: ReefMain) -> void:
	m = main
	stage = SideScrollStage.new(main)

func build(from_castle: bool, from_north: bool, at_ocean_gate_hub: bool) -> void:
	m.g["phase"] = "promenade"
	m.g["ocean_gate_hub"] = at_ocean_gate_hub
	m.g["lagoon_promenade_targets"] = []
	m.g["lagoon_promenade_focus"] = ""
	m.g["lagoon_promenade_focus_t"] = 0.0
	m.g["lagoon_play_anim"] = {}
	m.lagoon_floor = false
	m.northern_floor = false
	m.arena_center = m.LEVEL2_POS
	m.arena_dome = 92.0
	m.arena_ceil = 34.0
	stage.open({
		"origin": m.LEVEL2_POS,
		"half_w": HALF_W,
		"half_d": HALF_D,
		"hover": 3.0,
		"bob_amp": 0.18,
		"steer_speed": 18.5,
		"arrive_r": 0.85,
		"band_y": BAND_Y,
		"band_h": BAND_H,
		"cam_h": CAM_H,
		"cam_dist": CAM_DIST,
		"look_h": CAM_H,
		"cam_fov": CAM_FOV,
		"cam_follow": 1.0,
		# Keep the optical axis perpendicular to the mural while camera
		# position eases. A yawing lens makes different Sprite3D depths skate
		# against their painted sockets and visibly rebounds at the edge clamp.
		"side_on_axis_lock": true,
		# the mural the lens may never pan off
		"screen_half_w": BACKDROP_TILE_SIZE.x * float(BACKDROP_COLUMNS) * 0.5,
		"screen_z": BACKDROP_Z,
		# taps belong to the interaction director below, not to raw travel
		"touch_travel": false,
		# and she may never stroll off the side of the pinned frame
		"keep_on_screen": true,
		"edge_margin": 5.0,
	})
	# Twelve native 1024px squares reconstruct the exact 6144x2048, 3:1
	# master at one depth. They meet without runtime overlap or rescaling.
	for row: int in range(BACKDROP_ROWS):
		for column: int in range(BACKDROP_COLUMNS):
			_add_backdrop(
				"res://assets/flats/sky_lagoon/main/"
				+ "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
				% [row, column],
				-60.0 + float(column) * BACKDROP_TILE_SIZE.x,
				21.5 - float(row) * BACKDROP_TILE_SIZE.y,
				row,
				column)
	_build_ambient_life()
	_build_night_fireflies()
	_build_animals()
	_build_runway_screen()
	_build_playground_screen()
	_build_castle_screen()
	_build_roshan_card()
	_refresh_route()
	# returning from the castle must not re-trigger the doorstep on frame one
	m.g["lagoon_castle_armed"] = not (from_castle or from_north)
	var spawn_at := -60.0                     # painted: beside the pearl plane
	if from_castle or from_north:
		spawn_at = 34.0                       # painted: the way in front of the castle
	_set_spawn(_walk_x(spawn_at))
	_sync_target_mural_anchors()
	if from_castle:
		m.show_msg("Roshan", "Back outside! Tap a playground toy or the castle door once to light it up, then tap it again to play.")
	elif m.g.get("lagoon_plane_card") is Sprite3D:
		m.show_msg("Roshan", "Our pearl plane landed! Tap the plane or a playground toy to explore.", "intro")
	else:
		m.show_msg("Roshan", "The Sky Lagoon is ready! Tap a playground toy once to light it up, then tap it again to play.", "intro")

func tick(delta: float) -> void:
	if m.mg_kind != "":
		return
	_refresh_route()
	if not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		m.g["ss_walk_goal"] = null
		stage.walk_tick(delta)
		_sync_target_mural_anchors()
		_tick_playground_animation(delta)
		_tick_ambient_life(delta)
		_tick_animals(delta)
		return
	_tick_hold_travel(delta)
	if _handle_action():
		return
	var old_x: float = m.player.position.x
	var walk_result: Dictionary = stage.walk_tick(delta)
	_sync_target_mural_anchors()
	_sync_roshan_card(
		m.player.position.x - old_x, bool(walk_result.get("moved", false)))
	_tick_ambient_life(delta)
	_tick_animals(delta)
	_tick_doorstep()
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	var focus_t: float = float(m.g.get("lagoon_promenade_focus_t", 0.0)) + delta
	m.g["lagoon_promenade_focus_t"] = focus_t
	_tick_target_affordances(focus_id, focus_t)

func _tick_target_affordances(focus_id: String, focus_t: float) -> void:
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var glow: Sprite3D = target.get("highlight") as Sprite3D
		if glow == null or not is_instance_valid(glow):
			continue
		var target_id: String = String(target.get("id", ""))
		var selected: bool = target_id == focus_id
		var affordance_kind: String = String(target.get(
			"affordance_kind", Affordance.INTERACTION))
		var phase: float = float(absi(target_id.hash()) % 127) * 0.037
		var wave: float = sin(
			focus_t * Affordance.pulse_speed(affordance_kind, selected) + phase)
		var tint: Color = Affordance.color(affordance_kind, selected)
		var opacity_floor: float = Affordance.opacity_floor(affordance_kind)
		tint.a *= lerpf(opacity_floor, 1.0, wave * 0.5 + 0.5)
		glow.modulate = tint
		if target_id == "castle_gate":
			# The plot door beacons through opacity. Scaling a facade-shaped
			# signal would make a loose ghost around every tower and window.
			glow.scale = Vector3.ONE
		else:
			var base_scale: float = float(target.get("highlight_scale", 1.0))
			var pulse: float = 1.0 + wave * Affordance.pulse_amount(
				affordance_kind, selected)
			glow.scale = Vector3.ONE * base_scale * pulse
		glow.visible = true

func action_label() -> String:
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	if focus_id == "":
		return "JUMP"
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == focus_id:
			return "ENTER" if String(target.get("kind", "")) == "castle" else "PLAY"
	return "JUMP"

func _handle_action() -> bool:
	if m.touch_ui == null or not m.touch_ui.consume_action_just():
		return false
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	if focus_id != "":
		for value in (m.g.get("lagoon_promenade_targets", []) as Array):
			var target: Dictionary = value as Dictionary
			if String(target.get("id", "")) == focus_id:
				_activate(target)
				_clear_focus()
				return true
	# No focused toy owns the action, so the medallion performs the hop it
	# advertises. SideScrollStage consumes this one-frame request below.
	m.g["ss_walk_jump_request"] = true
	return false

func _tick_hold_travel(delta: float) -> void:
	# The touch grammar, kept honest: a TAP belongs to the tap router
	# (handle_touch, which the touch UI fires on release), a HOLD on open
	# ground is travel. The engine's own hold-to-travel is switched off for
	# this stage (cfg touch_travel false) — while it was on, every press was
	# travel, so pressing an interactive prop walked Roshan across the promenade
	# on the way to opening it.
	var vp := m.get_viewport()
	if vp == null:
		return
	if not Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		m.g["lagoon_press_t"] = 0.0
		return
	var held: float = float(m.g.get("lagoon_press_t", 0.0)) + delta
	m.g["lagoon_press_t"] = held
	if held < HOLD_TRAVEL_S:
		return
	var press: Vector2 = vp.get_mouse_position()
	if not _animal_at(press).is_empty() or not _target_at(press).is_empty():
		return
	_set_walk_goal(press)

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
	m.g["ss_walk_goal"] = null
	var target_id: String = String(target.get("id", ""))
	if String(m.g.get("lagoon_promenade_focus", "")) == target_id:
		_activate(target)
		_clear_focus()
	else:
		_focus(target)
	return true

func _build_runway_screen() -> void:
	if bool(m.save_data.get("lagoon_plane_departed", false)):
		m.g["lagoon_plane_card"] = null
		return
	var plane := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
		Vector3(-58.0, 5.341, LANDMARK_Z), 10.732)   # fully inside the painted dock
	m.g["lagoon_plane_card"] = plane
	m.g["lagoon_plane_base"] = plane.position
	_register_target("plane", plane, "plane", "", 118.0, 1.12)
	var targets: Array = m.g.get("lagoon_promenade_targets", [])
	var plane_target: Dictionary = targets.back() as Dictionary
	m.g["lagoon_plane_highlight"] = plane_target.get("highlight")

func _build_playground_screen() -> void:
	# Alpha-silhouette placement, not nominal sprite rectangles: there is
	# visible grass between all three opaque cutouts at their actual scales.
	# The single-seat swing and slide are sized against Roshan's 8.34-unit
	# authored play pose instead of the old compact prop scale.
	var slide := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
		Vector3(-11.5, 6.61, PLAY_Z), SLIDE_H)
	var swing := _build_promenade_swing(Vector3(3.0, 6.30, PLAY_Z))
	var seesaw := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png",
		Vector3(17.0, 1.20, PLAY_Z), SEESAW_H)
	# These are opaque storybook cutouts, not translucent overlays. Alpha
	# scissoring keeps their transparent canvas while forcing the painted
	# equipment into the depth-writing opaque pass (the swing source contains
	# many soft-alpha interior pixels and otherwise looks ghosted).
	slide.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	swing.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	seesaw.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	_register_target("slide", slide, "playground", "slide", 118.0, 1.10,
		GROUND_SOCKET_LOCK)
	_register_target("swing", swing, "playground", "swing", 122.0, 1.10,
		GROUND_SOCKET_LOCK)
	_register_target("seesaw", seesaw, "playground", "seesaw", 112.0, 1.12,
		GROUND_SOCKET_LOCK)

func _opaque_storybook_cutout(sprite: Sprite3D) -> void:
	var material := ShaderMaterial.new()
	material.shader = OPAQUE_STORYBOOK_CUTOUT_SHADER
	material.set_shader_parameter("albedo_texture", sprite.texture)
	material.set_shader_parameter("tint", sprite.modulate)
	material.set_shader_parameter(
		"alpha_threshold", OPAQUE_CUTOUT_ALPHA_THRESHOLD)
	sprite.material_override = material
	sprite.modulate = Color.WHITE
	sprite.transparency = 0.0
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD

func _build_promenade_swing(pos: Vector3) -> Sprite3D:
	# The former swing was one flattened frame/rope/seat card. Roshan could
	# change poses, but no part of the equipment could follow a pendulum arc.
	# Reuse the approved separated playground layers so the ropes and seat own
	# a real top-bar pivot and Roshan can share that exact motion.
	var frame := _add_sprite(SWING_FRAME_TEX, pos, SWING_H)
	frame.name = "SkyLagoonPromenadeSwingFrame"
	_opaque_storybook_cutout(frame)

	var pivot := Node3D.new()
	pivot.name = "SwingSeatPivot"
	pivot.position = Vector3(0.0, SWING_H * 0.5, 0.02)
	frame.add_child(pivot)

	var seat_texture: Texture2D = load(SWING_SEAT_TEX) as Texture2D
	var seat := Sprite3D.new()
	seat.name = "SwingSeatAndRopes"
	seat.texture = seat_texture
	seat.pixel_size = 1.0
	seat.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	seat.shaded = false
	seat.double_sided = true
	seat.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	seat.modulate = NIGHT_WORLD_TINT if m.is_night else Color.WHITE
	var seat_y_scale: float = SWING_ARM_H / 860.0
	var seat_visual_h: float = float(seat_texture.get_height()) * seat_y_scale
	seat.scale = Vector3(
		SWING_SEAT_W / float(seat_texture.get_width()), seat_y_scale, 1.0)
	seat.position = Vector3(0.0, -seat_visual_h * 0.5, 0.03)
	pivot.add_child(seat)
	_opaque_storybook_cutout(seat)

	frame.set_meta("swing_seat_pivot", pivot)
	frame.set_meta("swing_seat_sprite", seat)
	return frame

func _set_promenade_swing_angle(swing: Node3D, angle: float) -> void:
	var pivot: Node3D = swing.get_meta("swing_seat_pivot", null) as Node3D
	if pivot != null and is_instance_valid(pivot):
		pivot.rotation.z = angle

func _swing_grip_socket(swing: Node3D, angle: float) -> Vector2:
	var pivot: Node3D = swing.get_meta("swing_seat_pivot", null) as Node3D
	if pivot == null or not is_instance_valid(pivot):
		return Vector2(0.0, -SWING_GRIP_ARM).rotated(angle)
	return Vector2(pivot.position.x, pivot.position.y) \
		+ Vector2(0.0, -SWING_GRIP_ARM).rotated(angle)

func _build_castle_screen() -> void:
	# The four-tower castle remains one neutral, unshaded depth card. Its world
	# width, waterline and bridge landing are fitted to the approved fallback.
	var castle := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png",
		Vector3(51.572852, 11.022284, LANDMARK_Z), 28.430568, false)
	castle.name = "SkyLagoonCastleFourTower"
	m.g["lagoon_castle_card"] = castle
	_register_mural_socket(castle, GROUND_SOCKET_LOCK)
	var door_center_px: Vector2 = (
		CASTLE_DOOR_FOCUS_BOUNDS.position
		+ CASTLE_DOOR_FOCUS_BOUNDS.size * 0.5)
	var door_position := castle.position + Vector3(
		(door_center_px.x - CASTLE_CARD_SIZE.x * 0.5) * castle.pixel_size,
		(CASTLE_CARD_SIZE.y * 0.5 - door_center_px.y) * castle.pixel_size,
		0.10)
	var door_anchor := Node3D.new()
	door_anchor.name = "SkyLagoonCastleDoorFocus"
	door_anchor.position = door_position
	stage.root().add_child(door_anchor)
	m.g["lagoon_castle_door_focus"] = door_anchor
	_register_target(
		"castle_gate", door_anchor, "castle", "", 128.0, 1.0,
		GROUND_SOCKET_LOCK,
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png",
		castle.pixel_size)

func _build_roshan_card() -> void:
	var card := _add_sprite(
		"res://assets/characters/roshan_25d/roshan_base.png",
		Vector3(0.0, 4.0, 0.2), 7.8)
	card.name = "SkyLagoonRoshan"
	card.set_meta("walking", false)
	var animator: RoshanSpriteLoop = ROSHAN_SPRITE_LOOP.new()
	animator.name = "AlwaysAliveSpriteLoop"
	card.add_child(animator)
	animator.setup_sprite_3d(card, false, card, 2)
	m.g["lagoon_roshan_card"] = card
	m.g["lagoon_roshan_animator"] = animator
	m.g["lagoon_roshan_idle_texture"] = card.texture
	m.g["lagoon_roshan_idle_pixel_size"] = card.pixel_size
	m.player.visible = false

func _sync_roshan_card(delta_x: float = 0.0, moving: bool = false) -> void:
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	var root_node: Node3D = stage.root()
	if card == null or not is_instance_valid(card) or root_node == null:
		return
	var local_player: Vector3 = m.player.position - root_node.position
	card.position = Vector3(local_player.x, local_player.y + 1.0, local_player.z + 0.2)
	_sync_contact_shadow(card)
	var is_moving: bool = moving or absf(delta_x) > 0.01
	card.set_meta("walking", is_moving)
	if is_moving:
		card.flip_h = delta_x < 0.0
	var animator: RoshanSpriteLoop = m.g.get(
		"lagoon_roshan_animator") as RoshanSpriteLoop
	if animator != null and is_instance_valid(animator):
		animator.set_moving(is_moving)

func _build_ambient_life() -> void:
	m.g["lagoon_ambient_t"] = 0.0
	m.g["lagoon_wind_gust"] = 1.0
	m.g["lagoon_wind_distance"] = 0.0
	m.g["lagoon_ambient_cards"] = []
	# This approved PNW cutout restores depth where its baked-in counterpart
	# was removed. The former near tree at x=-27 was deliberately retired:
	# against the complete hedge it read as an asset stamp at the screen-one/
	# screen-two boundary instead of as part of the continuous landscape.
	_add_ambient_card("tree",
		"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png",
		Vector3(26.0, 6.912, DRESS_Z), 8.197, 0.42, 0.010,
		"foliage_far", "quiet", true)
	# One cloud in one clear corridor: enough motion to keep the sky alive,
	# without the overdraw from several translucent cards crossing each other.
	_add_ambient_card("cloud",
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png",
		Vector3(CLOUD_DRIFT_MIN_X, 28.414, CLOUD_Z), 3.104, 0.45, 0.0,
		"cloud", "quiet", false)
	# One thin, airy wisp per cabin. Their phase offsets keep the smoke gentle
	# and preserve the old three-card overdraw cost instead of tripling it. The
	# approved panorama's existing roof/chimney representations remain baked
	# into the mural; no extra chimney sticker is layered over them.
	for index: int in range(CABIN_SMOKE_ANCHORS.size()):
		_add_ambient_card("smoke", SMOKE_WISP_TEX,
			CABIN_SMOKE_ANCHORS[index], SMOKE_CARD_HEIGHT,
			0.0, 0.0, "smoke", "quiet", false, index)

func _build_night_fireflies() -> void:
	# A single low-count particle draw scatters a few readable fireflies across
	# each outdoor page. Reuse the approved Fairy Pond subject instead of adding
	# new art or lights; the lifetime ramp supplies independent-looking blinks
	# once preprocess has distributed the particles through their cycle.
	if not m.is_night:
		return
	var root_node: Node3D = stage.root()
	if root_node == null:
		return
	var fireflies := CPUParticles3D.new()
	fireflies.name = "SkyLagoonNightFireflies"
	fireflies.amount = FIREFLY_COUNT
	fireflies.lifetime = 5.4
	fireflies.preprocess = fireflies.lifetime
	fireflies.randomness = 0.78
	fireflies.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
	fireflies.emission_box_extents = Vector3(HALF_W - 5.0, 4.6, 0.45)
	fireflies.direction = Vector3(0.45, 0.25, 0.0)
	fireflies.spread = 180.0
	fireflies.gravity = Vector3.ZERO
	fireflies.initial_velocity_min = 0.08
	fireflies.initial_velocity_max = 0.34
	fireflies.damping_min = 0.03
	fireflies.damping_max = 0.10
	fireflies.angular_velocity_min = -24.0
	fireflies.angular_velocity_max = 24.0
	fireflies.scale_amount_min = 0.72
	fireflies.scale_amount_max = 1.16

	var blink := Gradient.new()
	blink.offsets = PackedFloat32Array([
		0.0, 0.10, 0.34, 0.50, 0.66, 0.88, 1.0,
	])
	blink.colors = PackedColorArray([
		Color(1.0, 0.88, 0.34, 0.0),
		Color(1.0, 0.94, 0.52, 1.0),
		Color(1.0, 0.82, 0.24, 0.72),
		Color(1.0, 0.88, 0.34, 0.08),
		Color(1.0, 0.96, 0.58, 1.0),
		Color(1.0, 0.84, 0.28, 0.68),
		Color(1.0, 0.88, 0.34, 0.0),
	])
	fireflies.color_ramp = blink

	var quad := QuadMesh.new()
	quad.size = Vector2(0.92, 0.92)
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	material.vertex_color_use_as_albedo = true
	material.albedo_texture = load(FIREFLY_TEX)
	material.emission_enabled = true
	material.emission = Color(1.0, 0.78, 0.18)
	material.emission_energy_multiplier = 1.45
	quad.material = material
	fireflies.mesh = quad
	fireflies.position = Vector3(0.0, 7.0, PLAY_Z + 0.4)
	fireflies.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	fireflies.set_meta("ambient_kind", "fireflies")
	fireflies.set_meta("night_only", true)
	fireflies.set_meta("outdoor_only", true)
	root_node.add_child(fireflies)
	m.g["lagoon_night_fireflies"] = fireflies

func _build_animals() -> void:
	# All five definitions share one visual card. Water fauna ride a constrained
	# RigidBody3D whose buoyancy and wake are integrated by Jolt; land fauna
	# freeze that same body and use audited painted-ground support points.
	m.g["lagoon_animals"] = ANIMAL_DEFS.duplicate(true)
	m.g["lagoon_animal_cycles"] = {0: 0, 1: 0, 2: 0}
	var first_definition: Dictionary = ANIMAL_DEFS[0]
	var first_path: Array = first_definition["path"] as Array
	var root_node: Node3D = stage.root()
	var body: WATER_ANIMAL_BODY = WATER_ANIMAL_BODY.new()
	body.name = "SkyLagoonAnimalJoltBody"
	body.position = first_path[0] as Vector3
	var collision: CollisionShape3D = CollisionShape3D.new()
	var collision_shape: SphereShape3D = SphereShape3D.new()
	collision_shape.radius = 0.48
	collision.shape = collision_shape
	body.add_child(collision)
	root_node.add_child(body)
	var card: Sprite3D = _add_sprite(
		String(first_definition["idle"]), first_path[0] as Vector3,
		float(first_definition["height"]))
	card.name = "SkyLagoonAnimalPool"
	card.hframes = ANIMAL_ATLAS_COLUMNS
	card.vframes = ANIMAL_ATLAS_ROWS
	card.frame = 0
	card.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	card.visible = false
	card.set_meta("living_card", true)
	card.set_meta("ambient_kind", "animal")
	card.set_meta("motion_class", "authored_habitat_path")
	card.set_meta("intensity_class", "quiet")
	card.set_meta("touch_footprint_px", ANIMAL_TOUCH_RADIUS_PX * 2.0)
	_sync_contact_shadow(card)
	card.reparent(body)
	card.position = Vector3.ZERO
	var ripple: Sprite3D = Sprite3D.new()
	ripple.name = "SkyLagoonAnimalWaterline"
	ripple.texture = _animal_waterline_texture()
	ripple.pixel_size = 3.4 / float(ripple.texture.get_width())
	ripple.no_depth_test = false
	ripple.shaded = false
	ripple.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	ripple.render_priority = 2
	ripple.visible = false
	ripple.set_meta("animal_support_effect", "jolt_waterline")
	root_node.add_child(ripple)
	var refuge_fx: Sprite3D = Sprite3D.new()
	refuge_fx.name = "SkyLagoonAnimalRefugeRustle"
	refuge_fx.texture = _animal_brush_texture()
	refuge_fx.pixel_size = 2.15 / float(refuge_fx.texture.get_width())
	refuge_fx.shaded = false
	refuge_fx.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	refuge_fx.render_priority = 3
	refuge_fx.visible = false
	refuge_fx.set_meta("animal_refuge_effect", "brush_rustle")
	root_node.add_child(refuge_fx)

	m.g["lagoon_animal_actor"] = {
		"node": card,
		"body": body,
		"waterline": ripple,
		"refuge_fx": refuge_fx,
		"definition": {},
		"page": -1,
		"state": "hidden",
		"state_t": 0.0,
		"spawn_t": ANIMAL_PAGE_SPAWN_S,
		"route_position": first_path[0] as Vector3,
		"path_index": 1,
		"refuge_entry_position": first_path[0] as Vector3,
		"refuge_contacted": false,
		"refuge_effect_played": false,
		"refuge_completed": false,
		"path_direction": 1,
		"refuge_direction": -1.0,
		"escape_impulse_sent": false,
	}

func _animal_waterline_texture() -> ImageTexture:
	# A tiny generated ring gives the solver-driven card a readable contact
	# line without copying or repainting any pixels from the protected mural.
	var width: int = 128
	var height: int = 48
	var image: Image = Image.create(width, height, false, Image.FORMAT_RGBA8)
	for y: int in range(height):
		for x: int in range(width):
			var px: float = (float(x) / float(width - 1) - 0.5) / 0.48
			var py: float = (float(y) / float(height - 1) - 0.5) / 0.34
			var radius: float = sqrt(px * px + py * py)
			var ring: float = clampf(1.0 - absf(radius - 0.78) / 0.12, 0.0, 1.0)
			var wake: float = clampf(1.0 - absf(radius - 0.50) / 0.08, 0.0, 1.0) * 0.38
			var alpha: float = maxf(ring, wake) * 0.72
			image.set_pixel(x, y, Color(0.70, 0.98, 1.0, alpha))
	return ImageTexture.create_from_image(image)

func _animal_brush_texture() -> ImageTexture:
	# One pooled, code-native leaf cluster supplies the brief rustle at every
	# brush refuge. It adds no permanent transparent-overdraw card or asset.
	var size: int = 96
	var image: Image = Image.create(size, size, false, Image.FORMAT_RGBA8)
	var centers: Array[Vector2] = [
		Vector2(-0.34, 0.04), Vector2(0.0, -0.17), Vector2(0.34, 0.04),
		Vector2(-0.16, 0.30), Vector2(0.19, 0.29),
	]
	var angles: Array[float] = [-0.52, 0.08, 0.54, -0.24, 0.28]
	var fills: Array[Color] = [
		Color(0.39, 0.72, 0.47, 0.94), Color(0.52, 0.82, 0.54, 0.96),
		Color(0.31, 0.64, 0.48, 0.94), Color(0.58, 0.79, 0.44, 0.94),
		Color(0.38, 0.70, 0.56, 0.94),
	]
	var outline := Color(0.16, 0.25, 0.31, 0.96)
	for y: int in range(size):
		for x: int in range(size):
			var point := Vector2(float(x) / float(size - 1) * 2.0 - 1.0,
				float(y) / float(size - 1) * 2.0 - 1.0)
			var pixel := Color(0.0, 0.0, 0.0, 0.0)
			for index: int in range(centers.size()):
				var local: Vector2 = (point - centers[index]).rotated(-angles[index])
				var radius: float = sqrt(pow(local.x / 0.29, 2.0)
					+ pow(local.y / 0.48, 2.0))
				if radius <= 1.0:
					pixel = outline if radius > 0.82 else fills[index]
			image.set_pixel(x, y, pixel)
	return ImageTexture.create_from_image(image)

func _animal_camera_x() -> float:
	var root_node: Node3D = stage.root()
	var cam: Camera3D = m.player.cam
	if root_node == null or cam == null or not cam.is_inside_tree():
		return 0.0
	return root_node.to_local(cam.global_position).x

func _animal_page_index() -> int:
	return clampi(int(floor((_animal_camera_x() + HALF_W) / 48.0)), 0, 2)

func _animal_definition(animal_id: String) -> Dictionary:
	for definition: Dictionary in ANIMAL_DEFS:
		if String(definition["id"]) == animal_id:
			return definition
	return {}

func _animal_definitions_for_page(page: int) -> Array[Dictionary]:
	var definitions: Array[Dictionary] = []
	for definition: Dictionary in ANIMAL_DEFS:
		if int(definition["page"]) == page:
			definitions.append(definition)
	return definitions

func _animal_distance_to_segment(point: Vector2, start: Vector2,
		finish: Vector2) -> float:
	var segment: Vector2 = finish - start
	var length_squared: float = segment.length_squared()
	if length_squared <= 0.00001:
		return point.distance_to(start)
	var amount: float = clampf((point - start).dot(segment) / length_squared, 0.0, 1.0)
	return point.distance_to(start + segment * amount)

func _animal_sample_has_safe_support(point: Vector3, height: float,
		support: String, support_rect: Rect2) -> bool:
	var support_point: Vector2 = (
		Vector2(point.x, point.y)
		if support == "water_jolt"
		else Vector2(point.x, point.y - height * 0.5)
	)
	if not support_rect.has_point(support_point):
		return false
	var route_clearance: float = INF
	for route_index: int in range(ROUTE_PAINTED.size() - 1):
		route_clearance = minf(route_clearance, _animal_distance_to_segment(
			support_point, ROUTE_PAINTED[route_index],
			ROUTE_PAINTED[route_index + 1]))
	if route_clearance < ANIMAL_ROUTE_CLEARANCE:
		return false
	for exclusion: Dictionary in ANIMAL_EXCLUSION_RECTS:
		var rect: Rect2 = exclusion["rect"] as Rect2
		if rect.has_point(support_point):
			return false
	return true

func _animal_path_is_safe(definition: Dictionary) -> bool:
	var path: Array = definition.get("path", []) as Array
	var height: float = float(definition.get("height", 0.0))
	var support: String = String(definition.get("support", ""))
	var support_zone_id: String = String(definition.get("support_zone", ""))
	var support_rect: Rect2 = ANIMAL_SUPPORT_RECTS.get(
		support_zone_id, Rect2()) as Rect2
	var refuge_kind: String = String(definition.get("refuge_kind", ""))
	var refuge_point: Variant = definition.get("refuge_point")
	var refuge_fx_point: Variant = definition.get("refuge_fx_point")
	if (path.size() < 2 or height <= 0.0
			or support not in ["ground", "water_jolt"]
			or not ANIMAL_SUPPORT_RECTS.has(support_zone_id)
			or refuge_kind not in ["brush", "tree"]
			or not refuge_point is Vector3 or not refuge_fx_point is Vector3):
		return false
	for value: Variant in path:
		var point: Vector3 = value as Vector3
		var foot := Vector2(point.x, point.y - height * 0.5)
		var support_point: Vector2 = Vector2(point.x, point.y) \
			if support == "water_jolt" else foot
		if not support_rect.has_point(support_point):
			return false
		var route_clearance: float = INF
		for route_index: int in range(ROUTE_PAINTED.size() - 1):
			route_clearance = minf(route_clearance, _animal_distance_to_segment(
				support_point, ROUTE_PAINTED[route_index], ROUTE_PAINTED[route_index + 1]))
		if route_clearance < ANIMAL_ROUTE_CLEARANCE:
			return false
		for exclusion: Dictionary in ANIMAL_EXCLUSION_RECTS:
			var rect: Rect2 = exclusion["rect"] as Rect2
			if rect.has_point(support_point):
				return false
	var refuge: Vector3 = refuge_point as Vector3
	for value: Variant in path:
		var start: Vector3 = value as Vector3
		for sample_index: int in range(13):
			var amount: float = float(sample_index) / 12.0
			var sample: Vector3 = start.lerp(refuge, amount)
			var sample_support: Vector2
			if support == "water_jolt":
				sample_support = Vector2(sample.x, sample.y)
			else:
				sample_support = Vector2(sample.x, sample.y - height * 0.5)
			if not support_rect.has_point(sample_support):
				return false
	# Activation can happen between authored waypoints. Sample both every idle
	# segment and the possible retreat from each sampled position so diagonal
	# shortcuts cannot cross the player route, scenery, water, or a page seam.
	for path_index: int in range(path.size() - 1):
		var segment_start: Vector3 = path[path_index] as Vector3
		var segment_finish: Vector3 = path[path_index + 1] as Vector3
		for idle_index: int in range(13):
			var idle_amount: float = float(idle_index) / 12.0
			var current: Vector3 = segment_start.lerp(
				segment_finish, idle_amount)
			if not _animal_sample_has_safe_support(
					current, height, support, support_rect):
				return false
			for retreat_index: int in range(13):
				var retreat_amount: float = float(retreat_index) / 12.0
				if not _animal_sample_has_safe_support(
						current.lerp(refuge, retreat_amount),
						height, support, support_rect):
					return false

	var page: int = int(definition.get("page", -1))
	if page < 0 or page >= ANIMAL_PAGE_CENTERS.size():
		return false
	var page_center: float = float(ANIMAL_PAGE_CENTERS[page])
	if absf(refuge.x - page_center) > 23.5:
		return false
	if refuge_kind == "tree" and not definition.get("refuge_climb_point") is Vector3:
		return false
	return true

func _animal_tint(definition: Dictionary) -> Color:
	return definition["night_tint"] as Color if m.is_night \
		else definition["day_tint"] as Color

func _animal_shadow_tint(definition: Dictionary) -> Color:
	return definition["shadow_night"] as Color if m.is_night \
		else definition["shadow_day"] as Color

func _sync_animal_shadow(actor: Dictionary) -> void:
	var node: Sprite3D = actor.get("node") as Sprite3D
	var body: WATER_ANIMAL_BODY = actor.get("body") as WATER_ANIMAL_BODY
	var waterline: Sprite3D = actor.get("waterline") as Sprite3D
	var definition: Dictionary = actor.get("definition", {}) as Dictionary
	if node == null or definition.is_empty() or not node.has_meta("contact_shadow"):
		return
	var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
	if shadow == null or not is_instance_valid(shadow):
		return
	var support: String = String(definition.get("support", "ground"))
	if support == "water_jolt":
		shadow.visible = false
		if waterline != null and is_instance_valid(waterline) and body != null:
			waterline.position = Vector3(body.position.x,
				body.visual_waterline_y(), body.position.z + 0.045)
			waterline.visible = node.visible
			waterline.modulate = Color(1.0, 0.90, 0.84, 0.52) \
				if m.is_night else Color(0.82, 1.0, 1.0, 0.72)
			var wake_scale: float = 1.0 + minf(0.22, absf(body.linear_velocity.x) * 0.12)
			waterline.scale = Vector3(wake_scale, 1.0 / wake_scale, 1.0)
		return
	if waterline != null and is_instance_valid(waterline):
		waterline.visible = false
	var route_position: Vector3 = actor.get("route_position", body.position) as Vector3
	var height: float = float(definition["height"])
	shadow.position = Vector3(
		route_position.x,
		route_position.y - height * 0.5 + maxf(0.08, height * 0.025),
		route_position.z - 0.035)
	shadow.visible = node.visible
	shadow.modulate = _animal_shadow_tint(definition)
	shadow.pixel_size = maxf(1.0, height * 0.58) / maxf(
		1.0, float(shadow.texture.get_width()))
	shadow.scale.y = 0.20 if String(definition["habitat"]) == "arrival_shore" else 0.22

func _hide_animal(actor: Dictionary, delay: float, advance_roster: bool) -> void:
	var node: Sprite3D = actor.get("node") as Sprite3D
	var body: WATER_ANIMAL_BODY = actor.get("body") as WATER_ANIMAL_BODY
	var refuge_fx: Sprite3D = actor.get("refuge_fx") as Sprite3D
	if node != null and is_instance_valid(node):
		node.visible = false
	if body != null and is_instance_valid(body):
		body.disable_water()
	if refuge_fx != null and is_instance_valid(refuge_fx):
		refuge_fx.visible = false
	actor["state"] = "hidden"
	actor["spawn_t"] = delay
	if advance_roster:
		actor["refuge_completed"] = true
	else:
		actor["refuge_contacted"] = false
		actor["refuge_effect_played"] = false
		actor["refuge_completed"] = false
	if advance_roster:
		var page: int = int(actor.get("page", -1))
		var cycles: Dictionary = m.g.get("lagoon_animal_cycles", {}) as Dictionary
		cycles[page] = int(cycles.get(page, 0)) + 1
		m.g["lagoon_animal_cycles"] = cycles
	_sync_animal_shadow(actor)

func _bind_animal(definition: Dictionary) -> bool:
	var actor: Dictionary = m.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite3D = actor.get("node") as Sprite3D
	var body: WATER_ANIMAL_BODY = actor.get("body") as WATER_ANIMAL_BODY
	var refuge_fx: Sprite3D = actor.get("refuge_fx") as Sprite3D
	if node == null or body == null or not is_instance_valid(node) \
			or not is_instance_valid(body) or not _animal_path_is_safe(definition):
		push_error("Sky Lagoon animal path rejected: %s" % String(
			definition.get("id", "unknown")))
		return false
	var idle_texture: Texture2D = load(String(definition["idle"])) as Texture2D
	var startle_texture: Texture2D = load(String(definition["startle"])) as Texture2D
	if idle_texture == null or startle_texture == null:
		push_error("Sky Lagoon animal atlas failed to load: %s" % String(definition["id"]))
		return false
	var path: Array = definition["path"] as Array
	var route_position: Vector3 = path[0] as Vector3
	var height: float = float(definition["height"])
	actor["definition"] = definition
	actor["page"] = int(definition["page"])
	actor["state"] = "idle"
	actor["state_t"] = 0.0
	actor["route_position"] = route_position
	actor["path_index"] = 1
	actor["path_direction"] = 1
	actor["idle_texture"] = idle_texture
	actor["startle_texture"] = startle_texture
	actor["refuge_entry_position"] = route_position
	actor["refuge_contacted"] = false
	actor["refuge_effect_played"] = false
	actor["refuge_completed"] = false
	actor["escape_impulse_sent"] = false
	node.name = "SkyLagoonAnimal_%s" % String(definition["id"])
	node.texture = idle_texture
	node.pixel_size = height / maxf(1.0,
		float(idle_texture.get_height()) / float(ANIMAL_ATLAS_ROWS))
	body.disable_water()
	body.position = route_position
	node.position = Vector3.ZERO
	if String(definition["support"]) == "water_jolt":
		body.configure_water(route_position,
			float(definition["water_surface_y"]), float(definition["speed"]),
			float(definition["water_mass"]), float(definition["water_wave"]))
	node.frame = 0
	node.flip_h = false
	node.scale = Vector3.ONE
	node.visible = true
	node.modulate = _animal_tint(definition)
	if refuge_fx != null and is_instance_valid(refuge_fx):
		refuge_fx.visible = false
		refuge_fx.scale = Vector3.ONE
		refuge_fx.rotation.z = 0.0
	node.set_meta("animal_id", String(definition["id"]))
	node.set_meta("animal_habitat", String(definition["habitat"]))
	node.set_meta("animal_support", String(definition["support"]))
	node.set_meta("animal_support_zone", String(definition["support_zone"]))
	node.set_meta("animal_lighting_profile", "night" if m.is_night else "day")
	body.set_meta("animal_id", String(definition["id"]))
	body.set_meta("animal_support", String(definition["support"]))
	node.set_meta("contact_shadow_height", height)
	m.g["lagoon_animal_actor"] = actor
	_sync_animal_shadow(actor)
	return true

func _bind_animal_id(animal_id: String) -> bool:
	var definition: Dictionary = _animal_definition(animal_id)
	return not definition.is_empty() and _bind_animal(definition)

func _bind_next_animal(page: int) -> bool:
	if page == 0 and m.g.get("lagoon_plane_card") is Sprite3D:
		return false
	var definitions: Array[Dictionary] = _animal_definitions_for_page(page)
	if definitions.is_empty():
		return false
	var cycles: Dictionary = m.g.get("lagoon_animal_cycles", {}) as Dictionary
	var definition: Dictionary = definitions[int(cycles.get(page, 0)) % definitions.size()]
	return _bind_animal(definition)

func _animal_at(screen_pos: Vector2) -> Dictionary:
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return {}
	var actor: Dictionary = m.g.get("lagoon_animal_actor", {}) as Dictionary
	if String(actor.get("state", "")) not in ["idle", "pause"]:
		return {}
	var node: Sprite3D = actor.get("node") as Sprite3D
	if node == null or not is_instance_valid(node) or not node.visible \
			or cam.is_position_behind(node.global_position):
		return {}
	var distance: float = cam.unproject_position(
		node.global_position).distance_to(screen_pos)
	return actor if distance <= ANIMAL_TOUCH_RADIUS_PX else {}

func _startle_animal(animal: Dictionary) -> void:
	if animal.is_empty() or String(animal.get("state", "")) not in ["idle", "pause"]:
		return
	var node: Sprite3D = animal.get("node") as Sprite3D
	var body: WATER_ANIMAL_BODY = animal.get("body") as WATER_ANIMAL_BODY
	var refuge_fx: Sprite3D = animal.get("refuge_fx") as Sprite3D
	if node == null or body == null or not is_instance_valid(node) or not is_instance_valid(body):
		return
	var definition: Dictionary = animal.get("definition", {}) as Dictionary
	var refuge_point: Vector3 = definition["refuge_point"] as Vector3
	var current_position: Vector3 = body.position
	var refuge_direction: float = signf(refuge_point.x - current_position.x)
	if is_zero_approx(refuge_direction):
		refuge_direction = 1.0
	animal["state"] = "startle"
	animal["state_t"] = 0.0
	animal["refuge_direction"] = refuge_direction
	animal["escape_impulse_sent"] = false
	animal["refuge_contacted"] = false
	animal["refuge_effect_played"] = false
	animal["refuge_completed"] = false
	if refuge_fx != null and is_instance_valid(refuge_fx):
		refuge_fx.visible = false
	node.texture = animal.get("startle_texture") as Texture2D
	node.frame = 0
	node.flip_h = refuge_direction < 0.0
	m.g["ss_walk_goal"] = null
	_clear_focus()
	m._sparkle_burst(node.global_position + Vector3(0.0,
		float(definition["height"]) * 0.25, 0.0), Color(1.0, 0.78, 0.42))
	m.player.play_verb("giggle")

func _begin_animal_refuge(actor: Dictionary) -> void:
	var definition: Dictionary = actor["definition"] as Dictionary
	var node: Sprite3D = actor["node"] as Sprite3D
	var body: WATER_ANIMAL_BODY = actor["body"] as WATER_ANIMAL_BODY
	var refuge_fx: Sprite3D = actor.get("refuge_fx") as Sprite3D
	if node == null or body == null or not is_instance_valid(node) or not is_instance_valid(body):
		return
	actor["state"] = "refuge"
	actor["state_t"] = 0.0
	actor["refuge_entry_position"] = body.position
	actor["route_position"] = body.position
	actor["refuge_contacted"] = true
	if String(definition["support"]) == "water_jolt":
		body.disable_water()
	node.position = Vector3.ZERO
	node.scale = Vector3.ONE
	node.modulate = _animal_tint(definition)
	node.set_meta("animal_refuge_kind", String(definition["refuge_kind"]))
	var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
	if shadow != null and is_instance_valid(shadow):
		shadow.visible = false
	var waterline: Sprite3D = actor.get("waterline") as Sprite3D
	if waterline != null and is_instance_valid(waterline):
		waterline.visible = false
	if refuge_fx != null and is_instance_valid(refuge_fx):
		refuge_fx.position = definition["refuge_fx_point"] as Vector3
		refuge_fx.scale = Vector3.ONE
		refuge_fx.rotation.z = 0.0
		refuge_fx.visible = String(definition["refuge_kind"]) == "brush"
		actor["refuge_effect_played"] = refuge_fx.visible

func _tick_animal_refuge(actor: Dictionary, delta: float) -> void:
	var definition: Dictionary = actor["definition"] as Dictionary
	var node: Sprite3D = actor["node"] as Sprite3D
	var body: WATER_ANIMAL_BODY = actor["body"] as WATER_ANIMAL_BODY
	var refuge_fx: Sprite3D = actor.get("refuge_fx") as Sprite3D
	var state_t: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = state_t
	var refuge_kind: String = String(definition["refuge_kind"])
	var duration: float = ANIMAL_TREE_CLIMB_S if refuge_kind == "tree" else ANIMAL_BRUSH_ENTRY_S
	var amount: float = clampf(state_t / duration, 0.0, 1.0)
	var eased: float = amount * amount * (3.0 - 2.0 * amount)
	if refuge_kind == "tree":
		var start: Vector3 = actor["refuge_entry_position"] as Vector3
		var climb: Vector3 = definition["refuge_climb_point"] as Vector3
		var climb_position: Vector3 = start.lerp(climb, eased)
		body.position = climb_position
		actor["route_position"] = climb_position
		node.position = Vector3(absf(sin(state_t * 17.0)) * 0.06, 0.0, 0.0)
		node.frame = 2 + int(floor(state_t / 0.11)) % 2
		node.flip_h = true
		node.scale = Vector3.ONE * lerpf(1.0, 0.82, amount)
		if refuge_fx != null and is_instance_valid(refuge_fx) and amount >= 0.38:
			refuge_fx.visible = true
			actor["refuge_effect_played"] = true
	else:
		body.position = actor["refuge_entry_position"] as Vector3
		node.position = Vector3(0.0, -0.48 * eased, 0.0)
		node.scale = Vector3.ONE.lerp(Vector3(0.52, 0.52, 1.0), eased)
		node.frame = 3 if amount >= 0.42 else 2
		if refuge_fx != null and is_instance_valid(refuge_fx):
			refuge_fx.visible = true
			actor["refuge_effect_played"] = true
	if refuge_fx != null and is_instance_valid(refuge_fx) and refuge_fx.visible:
		refuge_fx.position = definition["refuge_fx_point"] as Vector3
		refuge_fx.rotation.z = sin(state_t * 28.0) * 0.16 * (1.0 - amount)
		var pulse: float = 1.0 + sin(state_t * 22.0) * 0.12
		refuge_fx.scale = Vector3(pulse, 2.0 - pulse, 1.0)
		var rustle_tint := Color(0.65, 0.75, 0.94, 1.0) if m.is_night else Color(0.92, 1.0, 0.86, 1.0)
		rustle_tint.a = sin(amount * PI) * 0.92
		refuge_fx.modulate = rustle_tint
	var animal_tint: Color = _animal_tint(definition)
	animal_tint.a = clampf(1.0 - maxf(0.0, amount - 0.62) / 0.38, 0.0, 1.0)
	node.modulate = animal_tint
	if amount >= 1.0:
		actor["refuge_completed"] = true
		_hide_animal(actor, ANIMAL_RESPAWN_S, true)

func _tick_animal_idle(actor: Dictionary, delta: float) -> void:
	var node: Sprite3D = actor["node"] as Sprite3D
	var definition: Dictionary = actor["definition"] as Dictionary
	if String(definition["support"]) == "water_jolt":
		_tick_animal_water_idle(actor, delta)
		return
	var body: WATER_ANIMAL_BODY = actor["body"] as WATER_ANIMAL_BODY
	var path: Array = definition["path"] as Array
	var state: String = String(actor["state"])
	var state_t: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = state_t
	if state == "pause":
		var pause_t: float = maxf(0.0, float(actor.get("pause_t", 0.0)) - delta)
		actor["pause_t"] = pause_t
		node.frame = 1 if pause_t > float(definition["dwell_s"]) * 0.45 else 3
		body.position = actor["route_position"] as Vector3
		node.position = Vector3.ZERO
		if pause_t <= 0.0:
			var path_index: int = int(actor["path_index"])
			var path_direction: int = int(actor["path_direction"])
			if path_index >= path.size() - 1:
				path_direction = -1
			elif path_index <= 0:
				path_direction = 1
			actor["path_direction"] = path_direction
			actor["path_index"] = path_index + path_direction
			actor["state"] = "idle"
			actor["state_t"] = 0.0
		_sync_animal_shadow(actor)
		return
	var route_position: Vector3 = actor["route_position"] as Vector3
	var target: Vector3 = path[int(actor["path_index"])] as Vector3
	var direction: float = signf(target.x - route_position.x)
	route_position = route_position.move_toward(target, float(definition["speed"]) * delta)
	actor["route_position"] = route_position
	var frame_s: float = float(definition["frame_s"])
	node.frame = 2 if int(floor(state_t / frame_s)) % 2 == 0 else 0
	node.flip_h = direction < 0.0
	var bob: float = float(definition["bob"])
	var locomotion: String = String(definition["locomotion"])
	var bob_amount: float = absf(sin(state_t * (8.5 if locomotion == "hop" else 5.5))) * bob
	body.position = route_position
	node.position = Vector3(0.0, bob_amount, 0.0)
	if route_position.distance_to(target) <= 0.001:
		actor["state"] = "pause"
		actor["pause_t"] = float(definition["dwell_s"])
		node.frame = 1
		body.position = route_position
		node.position = Vector3.ZERO
	_sync_animal_shadow(actor)

func _tick_animal_water_idle(actor: Dictionary, delta: float) -> void:
	var node: Sprite3D = actor["node"] as Sprite3D
	var body: WATER_ANIMAL_BODY = actor["body"] as WATER_ANIMAL_BODY
	var definition: Dictionary = actor["definition"] as Dictionary
	var path: Array = definition["path"] as Array
	var state: String = String(actor["state"])
	var state_t: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = state_t
	actor["route_position"] = body.position
	node.position = Vector3.ZERO
	if state == "pause":
		var pause_t: float = maxf(0.0, float(actor.get("pause_t", 0.0)) - delta)
		actor["pause_t"] = pause_t
		body.set_patrol_target(body.position.x, 0.1)
		node.frame = 1 if pause_t > float(definition["dwell_s"]) * 0.45 else 3
		if pause_t <= 0.0:
			var path_index: int = int(actor["path_index"])
			var path_direction: int = int(actor["path_direction"])
			if path_index >= path.size() - 1:
				path_direction = -1
			elif path_index <= 0:
				path_direction = 1
			actor["path_direction"] = path_direction
			actor["path_index"] = path_index + path_direction
			actor["state"] = "idle"
			actor["state_t"] = 0.0
		_sync_animal_shadow(actor)
		return
	var target: Vector3 = path[int(actor["path_index"])] as Vector3
	body.set_patrol_target(target.x, float(definition["speed"]))
	var direction: float = signf(target.x - body.position.x)
	var frame_s: float = float(definition["frame_s"])
	node.frame = 2 if int(floor(state_t / frame_s)) % 2 == 0 else 0
	node.flip_h = direction < 0.0
	if absf(body.position.x - target.x) <= 0.16 \
			and absf(body.linear_velocity.x) <= 0.32:
		actor["state"] = "pause"
		actor["pause_t"] = float(definition["dwell_s"])
		node.frame = 1
	_sync_animal_shadow(actor)

func _tick_animal_startle(actor: Dictionary, delta: float) -> void:
	var node: Sprite3D = actor["node"] as Sprite3D
	var definition: Dictionary = actor["definition"] as Dictionary
	if String(definition["support"]) == "water_jolt":
		_tick_animal_water_startle(actor, delta)
		return
	var body: WATER_ANIMAL_BODY = actor["body"] as WATER_ANIMAL_BODY
	var state_t: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = state_t
	var route_position: Vector3 = actor["route_position"] as Vector3
	var squash_end: float = ANIMAL_STARTLE_ALERT_S + ANIMAL_STARTLE_SQUASH_S
	var hop_end: float = squash_end + ANIMAL_STARTLE_HOP_S
	if state_t < ANIMAL_STARTLE_ALERT_S:
		node.frame = 0
		body.position = route_position
		node.position = Vector3.ZERO
	elif state_t < squash_end:
		node.frame = 1
		body.position = route_position
		node.position = Vector3.ZERO
	elif state_t < hop_end:
		node.frame = 2
		body.position = route_position
		node.position = Vector3(0.0,
			sin((state_t - squash_end) / ANIMAL_STARTLE_HOP_S * PI) * 0.28, 0.0)
	else:
		var run_t: float = state_t - hop_end
		node.frame = 2 + int(floor(run_t / 0.13)) % 2
		var refuge_point: Vector3 = definition["refuge_point"] as Vector3
		route_position = route_position.move_toward(refuge_point,
			float(definition["refuge_speed"]) * delta)
		actor["route_position"] = route_position
		body.position = route_position
		node.position = Vector3(0.0,
			absf(sin(run_t * 10.0)) * 0.12, 0.0)
		if route_position.distance_to(refuge_point) <= 0.04:
			body.position = refuge_point
			actor["route_position"] = refuge_point
			_begin_animal_refuge(actor)
			return
	_sync_animal_shadow(actor)

func _tick_animal_water_startle(actor: Dictionary, delta: float) -> void:
	var node: Sprite3D = actor["node"] as Sprite3D
	var body: WATER_ANIMAL_BODY = actor["body"] as WATER_ANIMAL_BODY
	var definition: Dictionary = actor["definition"] as Dictionary
	var state_t: float = float(actor.get("state_t", 0.0)) + delta
	actor["state_t"] = state_t
	var squash_end: float = ANIMAL_STARTLE_ALERT_S + ANIMAL_STARTLE_SQUASH_S
	var hop_end: float = squash_end + ANIMAL_STARTLE_HOP_S
	var refuge_point: Vector3 = definition["refuge_point"] as Vector3
	if state_t < ANIMAL_STARTLE_ALERT_S:
		node.frame = 0
		body.set_patrol_target(body.position.x, 0.1)
	elif state_t < squash_end:
		node.frame = 1
		body.set_patrol_target(body.position.x, 0.1)
	else:
		if not bool(actor.get("escape_impulse_sent", false)):
			body.apply_escape_to(refuge_point.x,
				float(definition["refuge_speed"]))
			actor["escape_impulse_sent"] = true
		if state_t < hop_end:
			node.frame = 2
		else:
			var run_t: float = state_t - hop_end
			node.frame = 2 + int(floor(run_t / 0.13)) % 2
			if absf(body.position.x - refuge_point.x) <= 0.16:
				actor["route_position"] = body.position
				_begin_animal_refuge(actor)
				return
	actor["route_position"] = body.position
	node.position = Vector3.ZERO
	_sync_animal_shadow(actor)

func _tick_animals(delta: float) -> void:
	var actor: Dictionary = m.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite3D = actor.get("node") as Sprite3D
	if node == null or not is_instance_valid(node):
		return
	var page: int = _animal_page_index()
	if page != int(actor.get("page", -1)):
		actor["page"] = page
		_hide_animal(actor, ANIMAL_PAGE_SPAWN_S, false)
	if page == 0 and m.g.get("lagoon_plane_card") is Sprite3D:
		if node.visible:
			_hide_animal(actor, ANIMAL_PAGE_SPAWN_S, false)
		actor["spawn_t"] = ANIMAL_PAGE_SPAWN_S
		return
	var state: String = String(actor.get("state", "hidden"))
	if state == "hidden":
		var spawn_t: float = maxf(0.0, float(actor.get("spawn_t", 0.0)) - delta)
		actor["spawn_t"] = spawn_t
		if spawn_t <= 0.0:
			_bind_next_animal(page)
		return
	if state == "startle":
		_tick_animal_startle(actor, delta)
	elif state == "refuge":
		_tick_animal_refuge(actor, delta)
	else:
		_tick_animal_idle(actor, delta)

func _add_ambient_card(kind: String, path: String, pos: Vector3, height: float,
		speed: float, amplitude: float, motion_class: String,
		intensity_class: String, contact_shadow: bool = true,
		cycle_index: int = 0) -> void:
	var card := _add_sprite(path, pos, height, contact_shadow)
	card.name = "SkyLagoonAmbient_%s_%02d" % [kind, cycle_index]
	card.set_meta("ambient_kind", kind)
	card.set_meta("ambient_base", pos)
	card.set_meta("ambient_phase", _phase_token(pos))
	card.set_meta("ambient_speed", speed)
	card.set_meta("ambient_amplitude", amplitude)
	card.set_meta("living_card", true)
	card.set_meta("motion_class", motion_class)
	card.set_meta("intensity_class", intensity_class)
	card.set_meta("source_aspect",
		float(card.texture.get_width()) / maxf(1.0, float(card.texture.get_height())))
	card.set_meta("content_height_fraction", 0.992188 if kind == "smoke" else 1.0)
	card.set_meta("target_world_height", height)
	card.set_meta("touch_footprint_px", 0.0)
	card.set_meta("ambient_cycle_index", cycle_index)
	var socket_lock: float = GROUND_SOCKET_LOCK \
		if kind == "smoke" or kind == "tree" \
		else DEFAULT_MURAL_SOCKET_LOCK
	_register_mural_socket(card, socket_lock)
	if kind == "smoke":
		card.flip_h = cycle_index % 2 == 1
	card.modulate = NIGHT_WORLD_TINT if m.is_night else Color.WHITE
	var cards: Array = m.g.get("lagoon_ambient_cards", [])
	cards.append(card)
	m.g["lagoon_ambient_cards"] = cards

func _phase_token(pos: Vector3) -> float:
	return wrapf(pos.x * 0.73 + pos.z * 1.31, 0.0, TAU)

func _wind_gust_at(ambient_t: float) -> float:
	var cycle_t: float = fposmod(ambient_t, WIND_GUST_PERIOD_S)
	if cycle_t < WIND_GUST_RISE_AT_S:
		return 1.0
	if cycle_t < WIND_GUST_PEAK_AT_S:
		return lerpf(1.0, 1.5, smoothstep(
			WIND_GUST_RISE_AT_S, WIND_GUST_PEAK_AT_S, cycle_t))
	if cycle_t < WIND_GUST_FALL_AT_S:
		return lerpf(1.5, 1.0, smoothstep(
			WIND_GUST_PEAK_AT_S, WIND_GUST_FALL_AT_S, cycle_t))
	return 1.0

func _tick_ambient_life(delta: float) -> void:
	var ambient_t: float = float(m.g.get("lagoon_ambient_t", 0.0)) + delta
	m.g["lagoon_ambient_t"] = ambient_t
	var wind_gust: float = _wind_gust_at(ambient_t)
	m.g["lagoon_wind_gust"] = wind_gust
	var wind_distance: float = float(m.g.get("lagoon_wind_distance", 0.0)) \
		+ delta * wind_gust
	m.g["lagoon_wind_distance"] = wind_distance
	if not m.g.has("lagoon_ambient_cards"):
		return
	var ambient_cards: Array = m.g["lagoon_ambient_cards"] as Array
	for value in ambient_cards:
		var card := value as Sprite3D
		if card == null or not is_instance_valid(card):
			continue
		var base: Vector3 = card.get_meta("ambient_base", card.position) as Vector3
		var phase: float = float(card.get_meta("ambient_phase", 0.0))
		var speed: float = float(card.get_meta("ambient_speed", 0.5))
		var kind: String = String(card.get_meta("ambient_kind", "flower"))
		if kind == "cloud":
			card.position = Vector3(
				wrapf(base.x + wind_distance * speed,
					CLOUD_DRIFT_MIN_X, CLOUD_DRIFT_MAX_X),
				base.y + sin(ambient_t * 0.32 + phase) * 0.18,
				base.z)
			continue
		if kind == "smoke":
			var cycle_index: int = int(card.get_meta("ambient_cycle_index", 0))
			var life: float = fposmod(
				ambient_t + float(cycle_index) * SMOKE_LIFETIME_S / 3.0,
				SMOKE_LIFETIME_S) / SMOKE_LIFETIME_S
			var fade_in: float = smoothstep(0.0, 0.10, life)
			var fade_out: float = 1.0 - smoothstep(0.60, 1.0, life)
			var smoke_scale: float = lerpf(0.50, 0.85, life)
			card.scale = Vector3.ONE * smoke_scale
			var target_height: float = float(card.get_meta(
				"target_world_height", SMOKE_CARD_HEIGHT))
			var smoke_base: Vector3 = _mural_anchored_position(
				base,
				float(card.get_meta("mural_reference_camera_x",
					_mural_reference_camera_x(base.x))),
				float(card.get_meta("mural_socket_lock",
					DEFAULT_MURAL_SOCKET_LOCK)))
			card.set_meta("mural_socket_world_base", smoke_base)
			card.position = smoke_base + Vector3(
				WIND_DIRECTION * life * 0.20 * wind_gust,
				target_height * smoke_scale * 0.5 + life * 0.45,
				0.0)
			var smoke_tint := Color(0.58, 0.60, 0.68, 1.0)
			if m.is_night:
				smoke_tint = smoke_tint.lerp(NIGHT_WORLD_TINT, 0.35)
			smoke_tint.a = fade_in * fade_out * 0.62
			card.modulate = smoke_tint
			continue
		var wave: float = sin(ambient_t * speed + phase)
		var amplitude: float = float(card.get_meta("ambient_amplitude", 0.02))
		card.rotation.z = wave * amplitude * wind_gust
		var grounded_base: Vector3 = _mural_anchored_position(
			base,
			float(card.get_meta("mural_reference_camera_x",
				_mural_reference_camera_x(base.x))),
			float(card.get_meta("mural_socket_lock",
				DEFAULT_MURAL_SOCKET_LOCK)))
		card.set_meta("mural_socket_world_base", grounded_base)
		card.position = grounded_base + Vector3(
			wave * 0.04, absf(wave) * 0.025, 0.0)
		_sync_contact_shadow(card)
	var plane: Sprite3D = m.g.get("lagoon_plane_card") as Sprite3D
	if plane != null and is_instance_valid(plane):
		var plane_base: Vector3 = m.g.get("lagoon_plane_base", plane.position) as Vector3
		var anchored_plane_base: Vector3 = _mural_anchored_position(
			plane_base,
			float(plane.get_meta("mural_reference_camera_x",
				_mural_reference_camera_x(plane_base.x))),
			float(plane.get_meta("mural_socket_lock",
				DEFAULT_MURAL_SOCKET_LOCK)))
		plane.position = anchored_plane_base + Vector3(
			0.0, sin(ambient_t * 1.05) * 0.12, 0.0)
		plane.rotation.z = sin(ambient_t * 0.72) * 0.010
		_sync_contact_shadow(plane)
		var plane_glow: Sprite3D = m.g.get("lagoon_plane_highlight") as Sprite3D
		if plane_glow != null and is_instance_valid(plane_glow):
			plane_glow.position = plane.position + Vector3(0.0, 0.0, -0.05)
			plane_glow.rotation.z = plane.rotation.z
		if ambient_t >= PLANE_DEPARTURE_S:
			_finish_plane_arrival()

func teardown() -> void:
	# Mutable stage state belongs to ReefMain by project architecture, so the
	# persistent promenade helper explicitly releases its transient keys.
	m.g.erase("lagoon_ambient_cards")
	m.g.erase("lagoon_ambient_t")
	m.g.erase("lagoon_wind_gust")
	m.g.erase("lagoon_wind_distance")
	m.g.erase("lagoon_night_fireflies")
	m.g.erase("lagoon_animals")
	m.g.erase("lagoon_animal_actor")
	m.g.erase("lagoon_animal_cycles")

func _finish_plane_arrival() -> void:
	var plane: Sprite3D = m.g.get("lagoon_plane_card") as Sprite3D
	if plane == null or not is_instance_valid(plane):
		return
	var highlight: Sprite3D = m.g.get("lagoon_plane_highlight") as Sprite3D
	if highlight != null and is_instance_valid(highlight):
		highlight.queue_free()
	var plane_shadow: Sprite3D = null
	if plane.has_meta("contact_shadow"):
		plane_shadow = plane.get_meta("contact_shadow") as Sprite3D
	if plane_shadow != null and is_instance_valid(plane_shadow):
		plane_shadow.queue_free()
	plane.queue_free()
	m.g["lagoon_plane_card"] = null
	m.g["lagoon_plane_highlight"] = null
	var retained: Array = []
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) != "plane":
			retained.append(target)
	m.g["lagoon_promenade_targets"] = retained
	m.save_data["lagoon_plane_departed"] = true
	m._write_save()

func _add_backdrop(path: String, x: float, y: float, row: int, column: int) -> void:
	var root_node: Node3D = stage.root()
	if root_node == null:
		return
	# A tile that fails to load must never take the rest of the promenade down
	# with it. This used to read backdrop.texture.get_width() unguarded, so one
	# null texture aborted build() half-way — after _enter_level2_now had
	# already hidden the reef sun and switched the music — and left Roshan
	# standing in the legacy reef underneath, unlit (owner report 2026-07-29).
	# Losing one painted square is a blemish; losing the whole area is the bug.
	var tex: Texture2D = load(path) as Texture2D
	if tex == null:
		push_error("Sky Lagoon mural tile failed to load: %s" % path)
		return
	var backdrop := Sprite3D.new()
	backdrop.name = "SkyLagoonBackdrop_r%d_c%d" % [row, column]
	backdrop.texture = tex
	backdrop.pixel_size = BACKDROP_TILE_SIZE.x / maxf(
		1.0, float(tex.get_width()))
	# NEVER billboard the mural. A billboarded card swings about its OWN centre
	# to face the lens, so the moment the camera was not dead in front of a
	# tile the three cards stopped being coplanar, their painted edges pulled
	# apart, and the environment sky showed through the wedges between them as
	# vertical blue seams. The mural is one flat wall facing +Z (where the
	# side-on camera lives); its tiles then meet exactly, as the resolution
	# audit specifies.
	backdrop.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	# opaque pass + depth write: the wall sorts against the standees in front
	# of it by real depth instead of by transparent-queue distance
	backdrop.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	backdrop.shaded = false
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	backdrop.modulate = NIGHT_BACKDROP_TINT if m.is_night else Color.WHITE
	backdrop.position = Vector3(x, y, BACKDROP_Z)
	root_node.add_child(backdrop)

func _add_sprite(path: String, pos: Vector3, height: float,
		contact_shadow: bool = true) -> Sprite3D:
	var root_node: Node3D = stage.root()
	var sprite := Sprite3D.new()
	sprite.texture = load(path)
	sprite.pixel_size = height / maxf(1.0, float(sprite.texture.get_height()))
	# Standees are cutouts standing IN the diorama, not billboards: they stay
	# parallel to the mural so that panning the side-on lens slides them past
	# the painting instead of swivelling each one out of its painted setting.
	sprite.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	sprite.shaded = false
	sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	sprite.modulate = NIGHT_WORLD_TINT if m.is_night else Color.WHITE
	sprite.position = pos
	root_node.add_child(sprite)
	if contact_shadow:
		var shadow := _add_contact_shadow(pos, maxf(1.2, height * 0.62), height)
		sprite.set_meta("contact_shadow", shadow)
		sprite.set_meta("contact_shadow_height", height)
	return sprite

func _add_contact_shadow(pos: Vector3, width: float, height: float) -> Sprite3D:
	var root_node: Node3D = stage.root()
	var shadow := Sprite3D.new()
	shadow.name = "SkyLagoonContactShadow"
	shadow.set_meta("sky_lagoon_contact_shadow", true)
	shadow.texture = load(CONTACT_SHADOW_TEX)
	shadow.pixel_size = width / maxf(1.0, float(shadow.texture.get_width()))
	shadow.scale.y = 0.22
	shadow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	shadow.shaded = false
	shadow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	shadow.position = Vector3(
		pos.x,
		pos.y - height * 0.5 + maxf(0.08, height * 0.025),
		pos.z - 0.035)
	root_node.add_child(shadow)
	return shadow

func _sync_contact_shadow(sprite: Sprite3D) -> void:
	if not sprite.has_meta("contact_shadow"):
		return
	var shadow: Sprite3D = sprite.get_meta("contact_shadow") as Sprite3D
	if shadow == null or not is_instance_valid(shadow):
		return
	if sprite == m.g.get("lagoon_roshan_card") and not (
			m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
		shadow.visible = false
		return
	var height: float = float(sprite.get_meta("contact_shadow_height", 1.0))
	shadow.position = Vector3(
		sprite.position.x,
		sprite.position.y - height * 0.5 + maxf(0.08, height * 0.025),
		sprite.position.z - 0.035)
	shadow.visible = sprite.visible

func _mural_reference_camera_x(reference_x: float) -> float:
	# The approved review framings are the centres of the three 48-unit pages.
	# Preserve a card exactly in the page where it was placed, then compensate
	# only as the lens travels away from that authored framing.
	return clampf(roundf(reference_x / 48.0) * 48.0, -48.0, 48.0)

func _mural_anchored_x(reference_x: float, card_z: float,
		reference_camera_x: float,
		socket_lock: float = DEFAULT_MURAL_SOCKET_LOCK) -> float:
	# Compatibility seam for older callers and probes. New placement uses the
	# exact 2D projection in _mural_anchored_position so both axes stay locked.
	var reference_position := Vector3(reference_x, CAM_H, card_z)
	return _mural_anchored_position(
		reference_position, reference_camera_x, socket_lock).x

func _mural_reference_position(reference_position: Vector3,
		reference_camera_x: float) -> Vector3:
	# Recover the point on the painted wall that the authored card centre
	# covered in its approved page framing. The source cards were composed at
	# real depth, so their local coordinates already include perspective.
	var backdrop_distance: float = CAM_DIST - BACKDROP_Z
	var card_distance: float = maxf(0.001, CAM_DIST - reference_position.z)
	var depth_scale: float = backdrop_distance / card_distance
	return Vector3(
		reference_camera_x
			+ (reference_position.x - reference_camera_x) * depth_scale,
		CAM_H + (reference_position.y - CAM_H) * depth_scale,
		BACKDROP_Z)

func _mural_anchored_position(reference_position: Vector3,
		reference_camera_x: float,
		socket_lock: float = DEFAULT_MURAL_SOCKET_LOCK) -> Vector3:
	# Project the authored mural socket through the CURRENT camera, then
	# intersect that screen ray with the card's real depth plane. This remains
	# exact while the camera is moving, at both edge clamps, and on any aspect
	# ratio. Blending retains restrained parallax for non-socket landmarks.
	var root_node: Node3D = stage.root()
	var cam: Camera3D = m.player.cam
	if root_node == null or cam == null or not cam.is_inside_tree():
		return reference_position
	var mural_local: Vector3 = _mural_reference_position(
		reference_position, reference_camera_x)
	var mural_global: Vector3 = root_node.to_global(mural_local)
	if cam.is_position_behind(mural_global):
		return reference_position
	var screen_point: Vector2 = cam.unproject_position(mural_global)
	var ray_origin: Vector3 = cam.project_ray_origin(screen_point)
	var ray_direction: Vector3 = cam.project_ray_normal(screen_point)
	if absf(ray_direction.z) <= 0.00001:
		return reference_position
	var target_global_z: float = root_node.to_global(
		Vector3(0.0, 0.0, reference_position.z)).z
	var ray_t: float = (target_global_z - ray_origin.z) / ray_direction.z
	if ray_t <= 0.0:
		return reference_position
	var exact_local: Vector3 = root_node.to_local(
		ray_origin + ray_direction * ray_t)
	exact_local.z = reference_position.z
	return reference_position.lerp(exact_local, clampf(socket_lock, 0.0, 1.0))

func _register_mural_socket(node: Node3D,
		socket_lock: float = DEFAULT_MURAL_SOCKET_LOCK) -> void:
	node.set_meta("mural_reference_x", node.position.x)
	node.set_meta("mural_reference_position", node.position)
	node.set_meta("mural_reference_camera_x",
		_mural_reference_camera_x(node.position.x))
	node.set_meta("mural_socket_lock", socket_lock)
	node.set_meta("mural_backdrop_reference", _mural_reference_position(
		node.position, _mural_reference_camera_x(node.position.x)))

func _sync_mural_socket(node: Node3D) -> void:
	if node == null or not is_instance_valid(node):
		return
	var reference_position: Vector3 = node.get_meta(
		"mural_reference_position", node.position) as Vector3
	var reference_camera_x: float = float(node.get_meta(
		"mural_reference_camera_x",
		_mural_reference_camera_x(reference_position.x)))
	var socket_lock: float = float(node.get_meta(
		"mural_socket_lock", DEFAULT_MURAL_SOCKET_LOCK))
	node.position = _mural_anchored_position(
		reference_position, reference_camera_x, socket_lock)
	node.set_meta("mural_socket_world_base", node.position)
	if node is Sprite3D:
		_sync_contact_shadow(node as Sprite3D)

func _sync_target_mural_anchors() -> void:
	var castle: Node3D = m.g.get("lagoon_castle_card") as Node3D
	if castle != null and is_instance_valid(castle):
		_sync_mural_socket(castle)
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var node: Node3D = target.get("node") as Node3D
		if node == null or not is_instance_valid(node):
			continue
		_sync_mural_socket(node)
		var glow: Sprite3D = target.get("highlight") as Sprite3D
		if glow != null and is_instance_valid(glow):
			glow.position = node.position + Vector3(0.0, 0.0, -0.05)
			glow.rotation.z = node.rotation.z

func _register_target(id: String, node: Node3D, kind: String, payload: String,
		radius_px: float, highlight_scale: float,
		socket_lock: float = DEFAULT_MURAL_SOCKET_LOCK,
		highlight_path: String = "", highlight_pixel_size: float = 0.0) -> void:
	_register_mural_socket(node, socket_lock)
	var affordance_kind: String = Affordance.PLOT \
		if kind == "castle" else Affordance.ANIMATION
	var glow: Sprite3D
	glow = Sprite3D.new()
	if not highlight_path.is_empty():
		glow.texture = load(highlight_path)
		glow.pixel_size = highlight_pixel_size
		glow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
		glow.shaded = false
		glow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		glow.modulate = Affordance.color(affordance_kind, false)
		glow.position = node.position + Vector3(0, 0, -0.05)
		var root_node: Node3D = stage.root()
		root_node.add_child(glow)
	elif node is Sprite3D:
		var source := node as Sprite3D
		glow.texture = source.texture
		glow.pixel_size = source.pixel_size
		glow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
		glow.shaded = false
		glow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		glow.modulate = Affordance.color(affordance_kind, false)
		glow.position = source.position + Vector3(0, 0, -0.05)
		var root_node: Node3D = stage.root()
		root_node.add_child(glow)
	glow.scale = Vector3.ONE * highlight_scale
	glow.visible = true
	var targets: Array = m.g.get("lagoon_promenade_targets", [])
	targets.append({
		"id": id,
		"node": node,
		"kind": kind,
		"payload": payload,
		"radius_px": radius_px,
		"affordance_kind": affordance_kind,
		"highlight": glow,
		"highlight_scale": highlight_scale,
	})
	m.g["lagoon_promenade_targets"] = targets

func _target_at(screen_pos: Vector2) -> Dictionary:
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return {}
	var best: Dictionary = {}
	var best_dist := INF
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var node: Node3D = target.get("node") as Node3D
		if node == null or not is_instance_valid(node):
			continue
		var dist: float = cam.unproject_position(node.global_position).distance_to(screen_pos)
		if dist <= float(target.get("radius_px", 92.0)) and dist < best_dist:
			best = target
			best_dist = dist
	return best

func _focus(target: Dictionary) -> void:
	var target_id: String = String(target.get("id", ""))
	m.g["lagoon_promenade_focus"] = target_id
	m.g["lagoon_promenade_focus_t"] = 0.0
	_tick_target_affordances(target_id, 0.0)
	var node: Node3D = target.get("node") as Node3D
	if node != null and is_instance_valid(node):
		m._sparkle_burst(node.global_position, Affordance.sparkle_color(
			String(target.get("affordance_kind", Affordance.INTERACTION))))

func _clear_focus() -> void:
	m.g["lagoon_promenade_focus"] = ""
	_tick_target_affordances(
		"", float(m.g.get("lagoon_promenade_focus_t", 0.0)))

func _activate(target: Dictionary) -> void:
	var node: Node3D = target.get("node") as Node3D
	match String(target.get("kind", "")):
		"plane":
			_bounce(node, 0.20)
			m._sparkle_burst(node.global_position, Color(0.65, 0.94, 1.0))
			m.show_msg("Roshan", "The pearl plane is ready for another sky adventure!")
		"playground":
			_start_playground_animation(String(target.get("payload", "")), node)
			m._sparkle_burst(node.global_position, Color(1.0, 0.65, 0.88))
		"castle":
			m.player.visible = true
			m._enter_castle_interior()

func _bounce(node: Node3D, tilt: float) -> void:
	if node == null or not is_instance_valid(node):
		return
	var tween: Tween = m.create_tween()
	tween.tween_property(node, "rotation:z", tilt, 0.16).set_trans(Tween.TRANS_BACK)
	tween.tween_property(node, "rotation:z", -tilt * 0.45, 0.18)
	tween.tween_property(node, "rotation:z", 0.0, 0.16)

func _start_playground_animation(kind: String, equipment: Node3D) -> void:
	if not PLAY_FRAME_PATHS.has(kind) or equipment == null or not is_instance_valid(equipment):
		return
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	var root_node: Node3D = stage.root()
	if card == null or not is_instance_valid(card) or root_node == null:
		return
	var frames: Array[Texture2D] = []
	for path_value in PLAY_FRAME_PATHS[kind]:
		var frame: Texture2D = load(String(path_value)) as Texture2D
		if frame != null:
			frames.append(frame)
	if frames.size() != 4:
		return
	m.g["ss_walk_goal"] = null
	var equipment_reference_x: float = float(
		equipment.get_meta("mural_reference_x", equipment.position.x))
	m.player.position.x = root_node.position.x + _walk_x(equipment_reference_x)
	m.g["lagoon_play_anim"] = {
		"kind": kind,
		"t": 0.0,
		"dur": float(PLAY_DURATIONS[kind]),
		"equipment": equipment,
		"equipment_rotation": equipment.rotation.z,
		"frames": frames,
		"frame_index": -1,
	}
	var animator: RoshanSpriteLoop = m.g.get(
		"lagoon_roshan_animator") as RoshanSpriteLoop
	if animator != null and is_instance_valid(animator):
		animator.set_paused(true)
	card.visible = true
	card.flip_h = false
	card.hframes = 1
	card.vframes = 1
	card.frame = 0
	# The authored playground poses are whole PNGs, not atlas cells. Drop any
	# sampling window RoshanSpriteLoop left on the card, or the pose is sliced
	# by a window measured for a different sheet.
	card.region_enabled = false
	card.offset = Vector2.ZERO
	card.position.z = PLAY_Z + 0.12
	card.rotation.z = 0.0
	card.scale = Vector3.ONE
	_set_play_frame(0)
	# Snap to the first authored pose immediately, before the next frame. This
	# keeps Roshan's hands/seat contact aligned after the equipment was resized
	# and avoids one frame at her prior walking position.
	match kind:
		"swing":
			_tick_swing_animation(card, equipment, 0.0)
		"slide":
			_tick_slide_animation(card, equipment, 0.0)
		"seesaw":
			_tick_seesaw_animation(card, equipment, 0.0)

func _set_play_frame(frame_index: int) -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {})
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	if play.is_empty() or card == null or not is_instance_valid(card):
		return
	var frames: Array = play.get("frames", [])
	if frame_index < 0 or frame_index >= frames.size():
		return
	if int(play.get("frame_index", -1)) == frame_index:
		return
	play["frame_index"] = frame_index
	card.texture = frames[frame_index] as Texture2D
	card.pixel_size = PLAY_ROSHAN_H / maxf(1.0, float(card.texture.get_height()))

func _play_anchor_local(card: Sprite3D, anchor_pixels: Vector2) -> Vector2:
	var texture_size: Vector2 = card.texture.get_size()
	var local := Vector2(
		(anchor_pixels.x - texture_size.x * 0.5) * card.pixel_size * card.scale.x,
		(texture_size.y * 0.5 - anchor_pixels.y) * card.pixel_size * card.scale.y)
	return local.rotated(card.rotation.z)

func _place_play_anchor(card: Sprite3D, equipment: Node3D,
		anchor_pixels: Vector2, socket_offset: Vector2) -> void:
	var local_anchor: Vector2 = _play_anchor_local(card, anchor_pixels)
	card.position = Vector3(
		equipment.position.x + socket_offset.x - local_anchor.x,
		equipment.position.y + socket_offset.y - local_anchor.y,
		PLAY_Z + 0.12)

func _tick_playground_animation(delta: float) -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {})
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	var equipment: Node3D = play.get("equipment") as Node3D
	if play.is_empty() or card == null or not is_instance_valid(card):
		return
	if equipment == null or not is_instance_valid(equipment):
		_finish_playground_animation()
		return
	var t: float = float(play.get("t", 0.0)) + delta
	play["t"] = t
	var kind: String = String(play.get("kind", ""))
	match kind:
		"swing":
			_tick_swing_animation(card, equipment, t)
		"slide":
			_tick_slide_animation(card, equipment, t)
		"seesaw":
			_tick_seesaw_animation(card, equipment, t)
	_sync_contact_shadow(card)
	if t >= float(play.get("dur", 0.0)):
		_finish_playground_animation()

func _tick_swing_animation(card: Sprite3D, swing: Node3D, t: float) -> void:
	# Three readable pumps. The separated seat-and-rope layer and Roshan now
	# share one top-bar pivot; the authored frames add the pumping lean without
	# pretending that a static chair is moving.
	var phase: float = t * TAU / SWING_PERIOD_S
	var arc: float = sin(phase)
	var angle: float = arc * SWING_MAX_ANGLE
	var frame_index := 0
	if arc > 0.34:
		frame_index = 1
	elif arc < -0.34:
		frame_index = 2
	elif cos(phase) < 0.0:
		frame_index = 3
	_set_play_frame(frame_index)
	card.scale = Vector3(1.38, 1.0, 1.0)
	card.rotation.z = angle * 0.65
	_set_promenade_swing_angle(swing, angle)
	var hand_socket: Vector2 = _swing_grip_socket(swing, angle)
	_place_play_anchor(
		card, swing, SWING_HAND_ANCHORS[frame_index], hand_socket)

func _tick_slide_animation(card: Sprite3D, slide: Node3D, t: float) -> void:
	if t < 2.55:
		# Five distinct rung landings. Squash and extend alternate instead of
		# gliding up the ladder, so every stair has a little mermaid-tail hop.
		var step_f: float = clampf(t / 2.55, 0.0, 1.0) * 5.0
		var step_i: int = mini(4, floori(step_f))
		var step_phase: float = step_f - floorf(step_f)
		var bounce: float = sin(step_phase * PI) * 0.42
		_set_play_frame(step_i % 2)
		card.position = Vector3(
			slide.position.x + (-6.2 + float(step_i) * 0.42) * SLIDE_ANIM_SCALE,
			slide.position.y + (-3.7 + float(step_i) * 1.52) * SLIDE_ANIM_SCALE + bounce,
			PLAY_Z + 0.12)
		card.rotation.z = -0.03
	elif t < 3.15:
		_set_play_frame(2)
		var settle: float = smoothstep(0.0, 1.0, (t - 2.55) / 0.60)
		card.position = Vector3(
			slide.position.x + lerpf(-4.5, -2.1, settle) * SLIDE_ANIM_SCALE,
			slide.position.y + lerpf(2.5, 3.9, settle) * SLIDE_ANIM_SCALE,
			PLAY_Z + 0.12)
		card.rotation.z = lerpf(-0.03, -0.12, settle)
	else:
		_set_play_frame(3)
		var ride: float = smoothstep(0.0, 1.0, clampf((t - 3.15) / 2.05, 0.0, 1.0))
		# A quadratic chute path: gently over the lip, then faster down and out.
		var start := Vector2(
			slide.position.x - 2.1 * SLIDE_ANIM_SCALE,
			slide.position.y + 3.9 * SLIDE_ANIM_SCALE)
		var control := Vector2(
			slide.position.x + 1.8 * SLIDE_ANIM_SCALE,
			slide.position.y + 2.6 * SLIDE_ANIM_SCALE)
		var finish := Vector2(
			slide.position.x + 7.1 * SLIDE_ANIM_SCALE,
			slide.position.y - 4.2 * SLIDE_ANIM_SCALE)
		var a: Vector2 = start.lerp(control, ride)
		var b: Vector2 = control.lerp(finish, ride)
		var point: Vector2 = a.lerp(b, ride)
		card.position = Vector3(point.x, point.y, PLAY_Z + 0.12)
		card.rotation.z = lerpf(-0.12, -0.42, ride)

func _tick_seesaw_animation(card: Sprite3D, seesaw: Node3D, t: float) -> void:
	# Almost three complete low-high-low rocks. This pose faces left, so Roshan
	# sits on the right shell seat and follows its circular arc while her hands
	# stay on the inward hoop.
	var phase: float = t * TAU / 1.92
	var rock: float = sin(phase) * 0.105
	seesaw.rotation.z = float(
		(m.g.get("lagoon_play_anim", {}) as Dictionary).get(
			"equipment_rotation", 0.0)) + rock
	var frame_index := 0
	if sin(phase) > 0.45:
		frame_index = 2
	elif sin(phase) < -0.45:
		frame_index = 0
	elif cos(phase) > 0.0:
		frame_index = 1
	else:
		frame_index = 3
	_set_play_frame(frame_index)
	card.rotation.z = rock
	var seat_socket: Vector2 = SEESAW_RIGHT_SEAT_SOCKET.rotated(rock)
	_place_play_anchor(
		card, seesaw, SEESAW_SEAT_ANCHORS[frame_index], seat_socket)

func _finish_playground_animation() -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {})
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	var equipment: Node3D = play.get("equipment") as Node3D
	if equipment != null and is_instance_valid(equipment):
		equipment.rotation.z = float(play.get("equipment_rotation", 0.0))
		if String(play.get("kind", "")) == "swing":
			_set_promenade_swing_angle(equipment, 0.0)
	m.g["lagoon_play_anim"] = {}
	var animator: RoshanSpriteLoop = m.g.get(
		"lagoon_roshan_animator") as RoshanSpriteLoop
	if card != null and is_instance_valid(card):
		card.pixel_size = float(m.g.get("lagoon_roshan_idle_pixel_size", card.pixel_size))
		card.rotation.z = 0.0
		card.scale = Vector3.ONE
		card.flip_h = false
		card.set_meta("walking", false)
	if animator != null and is_instance_valid(animator):
		animator.set_paused(false)
	_sync_roshan_card()
	m.player.play_verb("giggle")

func _depth_ratio() -> float:
	# her plane sits at z 0, the painting at BACKDROP_Z: everything painted is
	# this much further from the lens than she is
	return CAM_DIST / (CAM_DIST - BACKDROP_Z)

func _walk_x(mural_x: float) -> float:
	# Where Roshan must STAND so she appears at a painted spot. While the lens
	# is free to centre her the two agree exactly; once it pins at a painted
	# edge they diverge by the depth ratio, which is why the drawbridge sat out
	# of reach of a straight x = painted_x assumption.
	# the lens is created deferred, so a build that runs on the very first
	# frames (the ocean-kingdom hub path) can reach here before it exists
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return mural_x
	var pan: float = stage.screen_pan_limit(m.g.get("ss_cfg", {}), cam)
	if pan < 0.0:
		return mural_x
	var ratio: float = _depth_ratio()
	if mural_x > pan:
		return pan + (mural_x - pan) * ratio
	if mural_x < -pan:
		return -pan + (mural_x + pan) * ratio
	return mural_x

func _walk_y(painted_y: float) -> float:
	# her hover so that her FEET land on a painted ground height
	return CAM_H + (painted_y - CAM_H) * _depth_ratio() + FOOT_OFFSET

func _refresh_route() -> void:
	# the lens pan limit depends on the viewport, so the painted route is
	# reprojected into walk space every tick rather than baked once
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	if cfg.is_empty():
		return
	var route: Array = []
	for value in ROUTE_PAINTED:
		var point: Vector2 = value as Vector2
		route.append(Vector2(_walk_x(point.x), _walk_y(point.y)))
	cfg["route"] = route

func _tick_doorstep() -> void:
	# Walk to the end of the way and you are at the castle door, so the child
	# can simply follow the path in - the two-tap gate stays as the other road.
	# Armed only after she has walked clear of the door, so stepping back out
	# of the castle cannot bounce her straight back inside.
	var root_node: Node3D = stage.root()
	if root_node == null or m.mg_kind != "":
		return
	var door_x: float = _walk_x(CASTLE_DOOR_X)
	var x: float = m.player.position.x - root_node.position.x
	if x < door_x - DOORSTEP_REARM:
		m.g["lagoon_castle_armed"] = true
		return
	if not bool(m.g.get("lagoon_castle_armed", false)):
		return
	if x < door_x - DOORSTEP_R:
		return
	m.g["lagoon_castle_armed"] = false
	m.g["ss_walk_goal"] = null
	_clear_focus()
	m.player.visible = true
	m._enter_castle_interior()

func _set_walk_goal(screen_pos: Vector2) -> void:
	# one projection for the whole engine: the stage owns the band window, so
	# a tap here and a hold in walk_tick land on exactly the same spot
	var goal: Variant = stage.plane_goal(screen_pos)
	if goal is Vector2:
		m.g["ss_walk_goal"] = goal

func _set_spawn(x: float) -> void:
	var root_node: Node3D = stage.root()
	if root_node == null:
		return
	m.player.position = root_node.position + Vector3(
		x, stage.route_y(m.g.get("ss_cfg", {}), x, 3.0), 0.0)
	m.player.vel = Vector3.ZERO
	m.player.rotation.y = PI
	var cam: Camera3D = m.player.cam
	if cam != null and cam.is_inside_tree():
		cam.fov = CAM_FOV
		# spawn straight onto the framing the glide would settle into — the
		# lens starts inside the mural instead of gliding in from off the edge
		var pan: float = stage.screen_pan_limit(m.g.get("ss_cfg", {}), cam)
		var cam_x: float = x if pan < 0.0 else clampf(x, -pan, pan)
		cam.position = root_node.position + Vector3(cam_x, CAM_H, CAM_DIST)
		cam.look_at(root_node.position + Vector3(cam_x, CAM_H, 0.0))
	_sync_roshan_card()
