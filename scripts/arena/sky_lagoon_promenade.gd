class_name SkyLagoonPromenade
extends RefCounted
# The Sky Lagoon's three-page 2.5D promenade. The painted PNW flats and
# transparent Codex sprites do the visual work; the real Roshan rig walks in
# one shallow band in front of them. All mutable state remains on ReefMain.

const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")
const HALF_W := 72.0
const HALF_D := 2.6
const BACKDROP_TILE_SIZE := Vector2(24.0, 24.0)
const BACKDROP_COLUMNS := 6
const BACKDROP_ROWS := 2
const BACKDROP_Z := -18.0
const CONTACT_SHADOW_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png"
const SMOKE_WISP_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png"
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
const NIGHT_WORLD_TINT := Color(0.72, 0.78, 0.96, 1.0)
const NIGHT_BACKDROP_TINT := Color(0.48, 0.56, 0.82, 1.0)
const PLANE_DEPARTURE_S := 7.0
const SLIDE_H := 11.4
const SWING_H := 11.8
const SEESAW_H := 4.5
const SLIDE_ANIM_SCALE := SLIDE_H / 19.1
const SWING_ANIM_SCALE := SWING_H / 18.4
const SEESAW_ANIM_SCALE := SEESAW_H / 11.35
const PLAY_ROSHAN_H := 8.34
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
		return
	_tick_hold_travel(delta)
	var old_x: float = m.player.position.x
	var walk_result: Dictionary = stage.walk_tick(delta)
	_sync_target_mural_anchors()
	_sync_roshan_card(
		m.player.position.x - old_x, bool(walk_result.get("moved", false)))
	_tick_ambient_life(delta)
	_tick_doorstep()
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	var focus_t: float = float(m.g.get("lagoon_promenade_focus_t", 0.0)) + delta
	m.g["lagoon_promenade_focus_t"] = focus_t
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var glow: Sprite3D = target.get("highlight") as Sprite3D
		if glow == null or not is_instance_valid(glow):
			continue
		var selected: bool = String(target.get("id", "")) == focus_id
		glow.visible = selected
		if selected:
			if String(target.get("id", "")) == "castle_gate":
				# The door itself breathes brighter in place. Scaling the full
				# castle made a loose gold ghost around every tower and window.
				glow.scale = Vector3.ONE
				glow.modulate.a = 0.58 + sin(focus_t * 5.2) * 0.12
			else:
				var pulse: float = 1.08 + sin(focus_t * 5.2) * 0.035
				glow.scale = Vector3.ONE * pulse

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
	if not _target_at(press).is_empty():
		return
	_set_walk_goal(press)

func handle_touch(screen_pos: Vector2) -> bool:
	if not (m.g.get("lagoon_play_anim", {}) as Dictionary).is_empty():
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
	var swing := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png",
		Vector3(3.0, 6.80, PLAY_Z), SWING_H)
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
	var glow: Sprite3D
	glow = Sprite3D.new()
	if not highlight_path.is_empty():
		glow.texture = load(highlight_path)
		glow.pixel_size = highlight_pixel_size
		glow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
		glow.shaded = false
		glow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		glow.modulate = Color(1.0, 0.82, 0.25, 0.72)
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
		glow.modulate = Color(1.0, 0.82, 0.25, 0.72)
		glow.position = source.position + Vector3(0, 0, -0.05)
		var root_node: Node3D = stage.root()
		root_node.add_child(glow)
	glow.scale = Vector3.ONE * highlight_scale
	glow.visible = false
	var targets: Array = m.g.get("lagoon_promenade_targets", [])
	targets.append({
		"id": id,
		"node": node,
		"kind": kind,
		"payload": payload,
		"radius_px": radius_px,
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
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var item: Dictionary = value as Dictionary
		var glow: Sprite3D = item.get("highlight") as Sprite3D
		if glow != null and is_instance_valid(glow):
			glow.visible = String(item.get("id", "")) == target_id
	var node: Node3D = target.get("node") as Node3D
	if node != null and is_instance_valid(node):
		m._sparkle_burst(node.global_position, Color(1.0, 0.84, 0.30))

func _clear_focus() -> void:
	m.g["lagoon_promenade_focus"] = ""
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var glow: Sprite3D = target.get("highlight") as Sprite3D
		if glow != null and is_instance_valid(glow):
			glow.visible = false

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
	# Three readable pumps. The hands stay near the two painted ropes while
	# the authored frames supply the lean, tail follow-through and seated pose.
	# The purpose-built chair is centered (unlike the old two-seat prop), and a
	# restrained horizontal pose scale brings the authored fist centers onto
	# its two inward ropes without making Roshan too tall for the frame.
	var phase: float = t * TAU / 1.72
	var arc: float = sin(phase)
	var frame_index := 0
	if arc > 0.34:
		frame_index = 1
	elif arc < -0.34:
		frame_index = 2
	elif cos(phase) < 0.0:
		frame_index = 3
	_set_play_frame(frame_index)
	card.scale = Vector3(1.38, 1.0, 1.0)
	card.position = Vector3(
		swing.position.x + arc * 0.08 * SWING_ANIM_SCALE,
		swing.position.y + (-3.60 + (1.0 - cos(phase)) * 0.12) * SWING_ANIM_SCALE,
		PLAY_Z + 0.12)
	card.rotation.z = -arc * 0.055

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
	# Almost three complete low-high-low rocks. Roshan sits on the left shell
	# seat and follows its circular arc while her hands stay on its gold hoop.
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
	var seat_offset := (Vector2(-6.05, 1.42) * SEESAW_ANIM_SCALE).rotated(rock)
	card.position = Vector3(
		seesaw.position.x + seat_offset.x,
		seesaw.position.y + seat_offset.y + 0.95 * SEESAW_ANIM_SCALE,
		PLAY_Z + 0.12)
	card.rotation.z = rock

func _finish_playground_animation() -> void:
	var play: Dictionary = m.g.get("lagoon_play_anim", {})
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	var equipment: Node3D = play.get("equipment") as Node3D
	if equipment != null and is_instance_valid(equipment):
		equipment.rotation.z = float(play.get("equipment_rotation", 0.0))
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
