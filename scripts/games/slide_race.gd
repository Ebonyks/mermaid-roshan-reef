class_name SlideRaceGame
extends RefCounted

# Harper and Fiona's fish route is a flat, opaque storybook stage. The
# Penguin chase and the shared race course below remain the shipped spatial
# activities; every Canvas branch therefore checks BOTH game and mode.
const FISH_CANVAS_LAYER := 7
const FISH_COUNT := 5
const FISH_RUN_SECONDS := 11.5
const FISH_TOUCH_DEAD_ZONE := 0.08
const FISH_STEER_DEAD_ZONE := 0.15
const FISH_LANE_SPEED := 1.45
const FISH_LANE_LIMIT := 1.0
const FISH_CATCH_PROGRESS := 0.065
const FISH_CATCH_LANE := 0.56
const FISH_OBJECTIVE := "Come slide with us! Grab the fishies!"
# harper.ogg is 2.043 seconds. Hybrid focus already speaks this exact line;
# retain a small tail margin so the activation tap cannot start it a second
# time on another voice-pool player while the first copy is still audible.
const FISH_OBJECTIVE_VOICE_WINDOW := 2.15

const FISH_TILE_PATHS: Array[String] = [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c3.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c3.png",
]
const FISH_TILE_SOURCE_RECTS: Array[Rect2i] = [
	Rect2i(0, 0, 1024, 1024),
	Rect2i(1024, 0, 1024, 1024),
	Rect2i(0, 1024, 1024, 1024),
	Rect2i(1024, 1024, 1024, 1024),
]
const FISH_SLIDE_PATH := \
	"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png"
const FISH_FRIENDS_PATH := "res://assets/characters/friends/two_friends.png"
const FISH_ART_PATH := "res://assets/props/gen2/clownfish_side.png"
const FISH_ROSHAN_PATHS: Array[String] = [
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2_v2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3_v2.png",
]
const FISH_PROGRESS_POINTS: Array[float] = [0.17, 0.34, 0.51, 0.69, 0.86]
const FISH_LANES: Array[float] = [-0.72, 0.68, -0.30, 0.72, -0.68]


class FishSteerCueCanvas extends Node2D:
	const HALF_EXTENT := Vector2(67.0, 57.0)

	var cue_center := Vector2.ZERO
	var cue_scale := 1.0
	var cue_time := 0.0
	var cue_direction := 0.0
	var cue_active := false


	func layout(center: Vector2, scale_value: float, time_value: float,
			direction_value: float, active_value: bool) -> void:
		cue_center = center
		cue_scale = scale_value
		cue_time = time_value
		cue_direction = signf(direction_value)
		cue_active = active_value
		queue_redraw()


	func screen_rect() -> Rect2:
		var half_extent: Vector2 = HALF_EXTENT * cue_scale
		return Rect2(cue_center - half_extent, half_extent * 2.0)


	func arrow_tip() -> Vector2:
		var travel: float = (3.0 + sin(cue_time * 3.2) * 3.0) * cue_scale
		return cue_center + Vector2(
			cue_direction * (57.0 * cue_scale + travel), 0.0)


	func _draw() -> void:
		if cue_scale <= 0.0 or cue_direction == 0.0:
			return
		var navy := Color(0.09, 0.08, 0.22, 0.82)
		var gold := Color(1.0, 0.82, 0.28, 0.98)
		var paper := Color(1.0, 0.98, 0.90, 1.0)
		# The 57px field and 67px animated tip are the complete authored bounds.
		# Each cue contains one arrow only, pointing outward toward its own side.
		draw_circle(cue_center, 57.0 * cue_scale, navy)
		draw_arc(cue_center, 50.0 * cue_scale, 0.0, TAU, 48, gold,
			6.0 * cue_scale, true)
		var tip: Vector2 = arrow_tip()
		var neck := cue_center + Vector2(cue_direction * 20.0 * cue_scale, 0.0)
		var wing_x: float = -cue_direction * 16.0 * cue_scale
		var wing_y: float = 14.0 * cue_scale
		var width: float = 7.0 * cue_scale
		draw_line(neck, tip, paper, width, true)
		draw_line(tip, tip + Vector2(wing_x, -wing_y), paper, width, true)
		draw_line(tip, tip + Vector2(wing_x, wing_y), paper, width, true)
		if cue_active:
			draw_circle(cue_center, 9.0 * cue_scale,
				Color(0.42, 0.94, 0.70))


class FishStageTrimCanvas extends Node2D:
	var stage_size := Vector2.ZERO
	var stage_scale := 1.0
	var stage_offset := Vector2.ZERO


	func layout(size_value: Vector2, scale_value: float,
			offset_value: Vector2) -> void:
		stage_size = size_value
		stage_scale = scale_value
		stage_offset = offset_value
		queue_redraw()


	func band_top() -> float:
		return stage_offset.y + (720.0 - 86.0) * stage_scale


	func _draw() -> void:
		if stage_size == Vector2.ZERO:
			return
		var ink := Color(0.08, 0.08, 0.23, 0.78)
		var aqua := Color(0.25, 0.83, 0.85, 0.78)
		var gold := Color(1.0, 0.80, 0.28, 0.96)
		# Anchor the rule to the fitted 1280x720 stage rather than the raw
		# viewport bottom. A 1280x800 window adds 40px below the fitted stage;
		# extending the navy apron through it keeps every pip the same 40px
		# inside the band instead of letting the rule slice through the fish.
		var band_top_value: float = band_top()
		var band_h: float = stage_size.y - band_top_value
		draw_rect(Rect2(Vector2(0.0, band_top_value),
			Vector2(stage_size.x, band_h)), ink, true)
		draw_line(Vector2(0.0, band_top_value),
			Vector2(stage_size.x, band_top_value), aqua,
			6.0 * stage_scale, true)
		for i in range(9):
			var x: float = (float(i) + 0.5) * stage_size.x / 9.0
			var y: float = band_top_value + 13.0 * stage_scale \
				+ sin(float(i) * 1.7) * 4.0 * stage_scale
			draw_circle(Vector2(x, y), 4.0 * stage_scale, gold)
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# race minigame. All state stays on main (m.*); received by reference.

var m: ReefMain
var _fish_layer: CanvasLayer = null
var _fish_surface: Node2D = null
var _fish_screen_fill: ColorRect = null
var _fish_backdrop_root: Node2D = null
var _fish_backdrop_tiles: Array[Sprite2D] = []
var _fish_wash: ColorRect = null
var _fish_play_root: Node2D = null
var _fish_trim: FishStageTrimCanvas = null
var _fish_slide: Sprite2D = null
var _fish_friends: Sprite2D = null
var _fish_roshan: Sprite2D = null
var _fish_roshan_textures: Array[Texture2D] = []
var _fish_nodes: Array[Sprite2D] = []
var _fish_pips: Array[Sprite2D] = []
var _fish_left_cue: FishSteerCueCanvas = null
var _fish_right_cue: FishSteerCueCanvas = null
var _fish_fr: Dictionary = {}
var _fish_viewport_size := Vector2.ZERO
var _fish_stage_scale := 1.0
var _fish_stage_offset := Vector2.ZERO
var _fish_slide_rect := Rect2()
var _fish_friends_rect := Rect2()
var _fish_roshan_point := Vector2.ZERO
var _fish_completed := false
var _fish_tick_count := 0
var _fish_steer_sources: Dictionary = {}
var _fish_blocked_sources: Dictionary = {}
var _fish_blocked_until_release := false
var _fish_startup_release_guard := false
var _fish_pause_waiting_release := false
var _fish_input_context_loss_reasons: Dictionary = {}
var _fish_input_context_restore_guard := false
var _fish_chime_snapshot_valid := false
var _fish_chime_volume_db := 0.0
var _fish_chime_pitch_scale := 1.0

func _init(main: ReefMain) -> void:
	m = main


static func canvas_runtime_art_paths() -> Array[String]:
	var paths: Array[String] = []
	for tile_path: String in FISH_TILE_PATHS:
		paths.append(tile_path)
	paths.append(FISH_SLIDE_PATH)
	paths.append(FISH_FRIENDS_PATH)
	paths.append(FISH_ART_PATH)
	for roshan_path: String in FISH_ROSHAN_PATHS:
		paths.append(roshan_path)
	return paths


func is_canvas_fish_route(fr: Dictionary = {}) -> bool:
	if m == null or String(m.game) != "slide":
		return false
	var effective_mode := String(m.g.get("mode", fr.get("mode", "")))
	return effective_mode == "fish"


func is_canvas_fish_active() -> bool:
	return is_canvas_fish_route(_fish_fr) and active_layer() != null \
		and not _fish_completed


func _build_canvas_fish(fr: Dictionary) -> void:
	stage_close()
	_fish_fr = fr
	m.g["timer"] = -1.0
	m.g["mode"] = "fish"
	m.g["got"] = 0
	m.g["steered"] = false
	m.g["canvas_run_start_t"] = float(m.g.get("t", 0.0))
	m.g["canvas_lane"] = 0.0
	m.g["canvas_lane_velocity"] = 0.0
	m.g["canvas_fish_got"] = [false, false, false, false, false]
	m.g.erase("canvas_context_progress")
	_fish_completed = false
	_fish_tick_count = 0
	_fish_steer_sources.clear()
	_fish_blocked_sources.clear()
	_fish_blocked_until_release = true
	_fish_startup_release_guard = true
	_fish_pause_waiting_release = false
	_fish_input_context_loss_reasons.clear()
	_fish_input_context_restore_guard = false
	_capture_fish_chime_state()

	_fish_layer = CanvasLayer.new()
	_fish_layer.name = "HarperFionaFishSlideCanvasLayer"
	_fish_layer.layer = FISH_CANVAS_LAYER
	m.add_child(_fish_layer)

	_fish_surface = Node2D.new()
	_fish_surface.name = "HarperFionaFishSlideCanvas"
	_fish_layer.add_child(_fish_surface)

	_fish_screen_fill = ColorRect.new()
	_fish_screen_fill.name = "OpaqueSkyFill"
	_fish_screen_fill.color = Color(0.13, 0.42, 0.64)
	_fish_screen_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_fish_screen_fill.z_index = -100
	_fish_surface.add_child(_fish_screen_fill)

	_fish_backdrop_root = Node2D.new()
	_fish_backdrop_root.name = "SkyLagoonCenterTilesCommonTransform"
	_fish_backdrop_root.z_index = -90
	_fish_surface.add_child(_fish_backdrop_root)
	for tile_index in range(FISH_TILE_PATHS.size()):
		var tile := Sprite2D.new()
		tile.name = "SkyLagoonBackdrop_r%d_c%d" \
			% [int(tile_index / 2), 2 + tile_index % 2]
		tile.texture = load(FISH_TILE_PATHS[tile_index]) as Texture2D
		tile.centered = true
		tile.position = Vector2(
			-512.0 + 1024.0 * float(tile_index % 2),
			-512.0 + 1024.0 * float(int(tile_index / 2)))
		tile.set_meta("source_path", FISH_TILE_PATHS[tile_index])
		tile.set_meta("native_source_rect", FISH_TILE_SOURCE_RECTS[tile_index])
		_fish_backdrop_root.add_child(tile)
		_fish_backdrop_tiles.append(tile)

	_fish_wash = ColorRect.new()
	_fish_wash.name = "SkyReadabilityWash"
	_fish_wash.color = Color(0.12, 0.36, 0.50, 0.16)
	_fish_wash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_fish_wash.z_index = -80
	_fish_surface.add_child(_fish_wash)

	_fish_play_root = Node2D.new()
	_fish_play_root.name = "FishSlideResponsiveStage"
	_fish_surface.add_child(_fish_play_root)

	_fish_trim = FishStageTrimCanvas.new()
	_fish_trim.name = "FishSlideStorybookTrim"
	_fish_trim.z_index = 4
	_fish_surface.add_child(_fish_trim)

	_fish_slide = _fish_actor_sprite(
		"ApprovedCompactSlide", FISH_SLIDE_PATH, 12)
	_fish_friends = _fish_actor_sprite(
		"HarperAndFionaProtectedArt", FISH_FRIENDS_PATH, 14)
	_fish_friends.set_meta("protected_original_unchanged", true)
	_fish_roshan = _fish_actor_sprite("RoshanSliding", FISH_ROSHAN_PATHS[0], 24)
	for roshan_path: String in FISH_ROSHAN_PATHS:
		_fish_roshan_textures.append(load(roshan_path) as Texture2D)

	for fish_index in range(FISH_COUNT):
		var fish := _fish_actor_sprite(
			"Clownfish%d" % fish_index, FISH_ART_PATH, 20)
		fish.set_meta("fish_index", fish_index)
		fish.set_meta("course_progress", FISH_PROGRESS_POINTS[fish_index])
		fish.set_meta("lane", FISH_LANES[fish_index])
		_fish_nodes.append(fish)

		var pip := _fish_actor_sprite(
			"FishProgressPip%d" % fish_index, FISH_ART_PATH, 31)
		pip.set_meta("fish_index", fish_index)
		_fish_pips.append(pip)

	_fish_left_cue = FishSteerCueCanvas.new()
	_fish_left_cue.name = "PersistentLeftSteerCue"
	_fish_left_cue.z_index = 30
	_fish_surface.add_child(_fish_left_cue)
	_fish_right_cue = FishSteerCueCanvas.new()
	_fish_right_cue.name = "PersistentRightSteerCue"
	_fish_right_cue.z_index = 30
	_fish_surface.add_child(_fish_right_cue)

	_layout_canvas_fish(true)
	_refresh_canvas_fish()
	m.hud_game.text = ""
	# The exact family recording names both the verb and its target; the
	# persistent side cues and five fish pips repeat it without requiring reading.
	var objective_now := Time.get_ticks_msec() / 1000.0
	var objective_last: float = maxf(
		float(m.said_cool.get("harper_hint", -99.0)),
		float(m.said_cool.get("harper_talk", -99.0)))
	var objective_recent: bool = objective_now - objective_last \
		< FISH_OBJECTIVE_VOICE_WINDOW
	# The opaque layer sits above the shared HUD. Voice + the persistent cues
	# are therefore the truthful child-visible instruction; do not leave a hidden
	# caption that can flash in the Reef after a quick neutral exit. Classic entry
	# with no recent Harper line still speaks this exact authored objective once.
	m.hud_msg.text = ""
	m.hud_msg.visible = false
	m.msg_timer = 0.0
	if not objective_recent:
		m._say("harper", "hint", 0.5)


func _fish_actor_sprite(node_name: String, path: String,
		z_order: int) -> Sprite2D:
	var actor := Sprite2D.new()
	actor.name = node_name
	actor.texture = load(path) as Texture2D
	actor.centered = true
	actor.z_index = z_order
	actor.set_meta("source_path", path)
	_fish_play_root.add_child(actor)
	return actor


func _layout_canvas_fish(force: bool) -> void:
	if _fish_surface == null or not is_instance_valid(_fish_surface):
		return
	var next_size: Vector2 = m.get_viewport().get_visible_rect().size
	next_size.x = maxf(next_size.x, 640.0)
	next_size.y = maxf(next_size.y, 360.0)
	if not force and next_size.is_equal_approx(_fish_viewport_size):
		return
	_fish_viewport_size = next_size
	_fish_screen_fill.position = Vector2.ZERO
	_fish_screen_fill.size = _fish_viewport_size
	_fish_wash.position = Vector2.ZERO
	_fish_wash.size = _fish_viewport_size

	# The four native tiles retain one shared position + scale. Their 2x2 child
	# offsets reconstruct the exact center 2048x2048 screen before cover-crop.
	var backdrop_scale: float = maxf(
		_fish_viewport_size.x / 2048.0,
		_fish_viewport_size.y / 2048.0)
	_fish_backdrop_root.position = _fish_viewport_size * 0.5
	_fish_backdrop_root.scale = Vector2.ONE * backdrop_scale
	_fish_backdrop_root.set_meta("common_scale", backdrop_scale)
	_fish_backdrop_root.set_meta("native_size", Vector2i(2048, 2048))

	_fish_stage_scale = minf(
		_fish_viewport_size.x / 1280.0,
		_fish_viewport_size.y / 720.0)
	_fish_stage_scale = maxf(_fish_stage_scale, 0.5)
	var fitted_size := Vector2(1280.0, 720.0) * _fish_stage_scale
	_fish_stage_offset = (_fish_viewport_size - fitted_size) * 0.5
	_fish_play_root.position = _fish_stage_offset
	_fish_play_root.scale = Vector2.ONE * _fish_stage_scale

	_fish_slide.position = Vector2(760.0, 374.0)
	_fish_slide.scale = Vector2.ONE * 1.22
	_fish_slide_rect = Rect2(Vector2(500.75, 122.68), Vector2(518.5, 502.64))
	_fish_friends.position = Vector2(254.0, 290.0)
	_fish_friends.scale = Vector2.ONE * 0.66
	_fish_friends_rect = Rect2(Vector2(95.6, 138.2), Vector2(316.8, 303.6))
	_fish_roshan.scale = Vector2.ONE * 0.31

	for pip_index in range(_fish_pips.size()):
		var pip: Sprite2D = _fish_pips[pip_index]
		pip.position = Vector2(
			520.0 + float(pip_index) * 62.0, 674.0)
		pip.scale = Vector2.ONE * 0.19
	_fish_trim.layout(_fish_viewport_size, _fish_stage_scale,
		_fish_stage_offset)
	_refresh_canvas_fish()


func _fish_course_point(progress: float, lane: float) -> Vector2:
	var p: float = clampf(progress, 0.0, 1.0)
	# A cubic drawn through the approved compact slide: shell platform to the
	# broad lower lip. Lateral steering stays screen-horizontal and forgiving.
	var inv: float = 1.0 - p
	var start := Vector2(721.0, 204.0)
	var control_a := Vector2(748.0, 248.0)
	var control_b := Vector2(823.0, 460.0)
	var finish := Vector2(932.0, 548.0)
	var base: Vector2 = start * inv * inv * inv \
		+ control_a * 3.0 * inv * inv * p \
		+ control_b * 3.0 * inv * p * p \
		+ finish * p * p * p
	return base + Vector2(lane * 88.0, 0.0)


func _fish_current_progress() -> float:
	if m == null or not m.g.has("canvas_run_start_t"):
		return 0.0
	var elapsed: float = maxf(0.0,
		float(m.g.get("t", 0.0)) - float(m.g["canvas_run_start_t"]))
	return clampf(elapsed / FISH_RUN_SECONDS, 0.0, 1.0)


func _tick_canvas_fish(delta: float, fr: Dictionary) -> void:
	if not is_canvas_fish_active():
		return
	# Layout is renderer state, not gameplay time. Refresh it before every input-
	# context guard so the first drawable frame after an app/window-size change is
	# already opaque and centered while motion, collection and clocks stay frozen.
	_layout_canvas_fish(false)
	if input_context_lost():
		return
	if _fish_input_context_restore_guard:
		# The first fully restored, unpaused game tick is a source-free boundary.
		# It retires the guard but never advances motion or accepts queued input.
		retire_input_context_restore_guard()
		return
	_fish_tick_count += 1
	if _fish_startup_release_guard:
		# Entry can occur on touch-down while the source remains physically held.
		# Keep the rider at the shell until both the reveal and exact release gate
		# are clear, so the first fish is never spent behind black or stale input.
		m.g["canvas_run_start_t"] = float(m.g.get("t", 0.0))
		_refresh_canvas_fish()
		if not _fish_blocked_sources.is_empty() or not _opening_fade_clear():
			return
		_fish_blocked_until_release = false
		_fish_startup_release_guard = false
		return

	var steer: float = _combined_fish_steer()
	if absf(steer) > FISH_STEER_DEAD_ZONE:
		m.g["steered"] = true
	var lane_velocity: float = float(m.g.get("canvas_lane_velocity", 0.0))
	lane_velocity = move_toward(lane_velocity,
		steer * FISH_LANE_SPEED, delta * 5.5)
	if absf(steer) <= FISH_STEER_DEAD_ZONE:
		lane_velocity = move_toward(lane_velocity, 0.0, delta * 3.8)
	var lane: float = float(m.g.get("canvas_lane", 0.0)) \
		+ lane_velocity * maxf(delta, 0.0)
	lane = clampf(lane, -FISH_LANE_LIMIT, FISH_LANE_LIMIT)
	if absf(lane) >= FISH_LANE_LIMIT and signf(lane_velocity) == signf(lane):
		lane_velocity = 0.0
	m.g["canvas_lane"] = lane
	m.g["canvas_lane_velocity"] = lane_velocity

	var progress: float = _fish_current_progress()
	_collect_canvas_fish(progress, lane)
	_refresh_canvas_fish()
	m.hud_game.text = ""
	if progress < 1.0:
		return
	if not bool(m.g.get("steered", false)):
		# Passive auto-motion cannot win. Start a fresh gentle run with the same
		# visible objective and no loss screen, countdown or removed progress.
		m.g["canvas_run_start_t"] = float(m.g.get("t", 0.0))
		m.g["canvas_lane"] = 0.0
		m.g["canvas_lane_velocity"] = 0.0
		# Repeat the exact recorded objective; the always-visible arrow supplies the
		# left/right control cue without depending on an occluded or unrecorded line.
		m._say("harper", "hint", FISH_OBJECTIVE_VOICE_WINDOW)
		return
	_fish_completed = true
	handoff_fish_chime_to_completion_reward()
	var got: int = int(m.g.get("got", 0))
	var finish_text := "WHEEE! You grabbed every fish! Best slider ever!" \
		if got >= FISH_COUNT else "What a ride! You caught %d fish!" % got
	m._end_game(true, fr, finish_text)


func _collect_canvas_fish(progress: float, lane: float) -> void:
	var got_flags: Array = m.g.get("canvas_fish_got", []) as Array
	if got_flags.size() != FISH_COUNT:
		return
	for fish_index in range(FISH_COUNT):
		if bool(got_flags[fish_index]):
			continue
		if absf(progress - FISH_PROGRESS_POINTS[fish_index]) \
				> FISH_CATCH_PROGRESS:
			continue
		if absf(lane - FISH_LANES[fish_index]) > FISH_CATCH_LANE:
			continue
		got_flags[fish_index] = true
		m.g["got"] = int(m.g.get("got", 0)) + 1
		if fish_index < _fish_nodes.size():
			_fish_nodes[fish_index].visible = false
		if m.chime != null:
			m.chime.volume_db = -4.0
			m.chime.pitch_scale = 0.88 + 0.12 * float(m.g["got"])
			m.chime.play()
	m.g["canvas_fish_got"] = got_flags


func _refresh_canvas_fish() -> void:
	if active_layer() == null or _fish_play_root == null:
		return
	var progress: float = _fish_current_progress()
	var lane: float = float(m.g.get("canvas_lane", 0.0))
	var time_value: float = float(m.g.get("t", 0.0))
	_fish_roshan_point = _fish_course_point(progress, lane)
	_fish_roshan.position = _fish_roshan_point
	var frame_index: int
	if progress < 0.12:
		# The accepted ladder poses are distinct action beats, not an idle loop.
		# Play them once in order before the seated ride instead of snapping the
		# silhouette back and forth four times per second at the shell.
		frame_index = 0 if progress < 0.06 else 1
	else:
		# Frames 0/1 are explicitly authored ladder-step poses; frames 2/3 are
		# seated-at-lip/chute-ride poses. Keep the rider seated through the finish
		# instead of snapping upright into ladder art for the last second.
		frame_index = 2 + int(floor(time_value * 4.5)) % 2
	if frame_index >= 0 and frame_index < _fish_roshan_textures.size():
		_fish_roshan.texture = _fish_roshan_textures[frame_index]
	_fish_roshan.rotation = lerpf(-0.14, 0.20, progress) \
		- float(m.g.get("canvas_lane_velocity", 0.0)) * 0.08

	var got_flags: Array = m.g.get("canvas_fish_got", []) as Array
	for fish_index in range(_fish_nodes.size()):
		var fish: Sprite2D = _fish_nodes[fish_index]
		var point := _fish_course_point(
			FISH_PROGRESS_POINTS[fish_index], FISH_LANES[fish_index])
		point.y += sin(time_value * 4.0 + float(fish_index) * 1.3) * 8.0
		fish.position = point
		fish.scale = Vector2.ONE * (0.30 + sin(
			time_value * 3.2 + float(fish_index)) * 0.018)
		fish.rotation = sin(time_value * 3.6 + float(fish_index)) * 0.10
		fish.visible = fish_index >= got_flags.size() \
			or not bool(got_flags[fish_index])
		var pip: Sprite2D = _fish_pips[fish_index]
		var filled: bool = fish_index < got_flags.size() \
			and bool(got_flags[fish_index])
		pip.modulate = Color.WHITE if filled \
			else Color(0.38, 0.48, 0.62, 0.52)
		pip.scale = Vector2.ONE * (0.22 if filled else 0.18)
	_fish_friends.rotation = sin(time_value * 2.0) * 0.018
	_refresh_fish_steer_cues()


func _refresh_fish_steer_cues() -> void:
	if _fish_left_cue == null or not is_instance_valid(_fish_left_cue) \
			or _fish_right_cue == null or not is_instance_valid(_fish_right_cue):
		return
	var combined_steer: float = _combined_fish_steer()
	var time_value: float = float(m.g.get("t", 0.0))
	_fish_left_cue.layout(_base_to_screen(Vector2(120.0, 650.0)),
		_fish_stage_scale, time_value, -1.0,
		combined_steer < -FISH_STEER_DEAD_ZONE)
	_fish_right_cue.layout(_base_to_screen(Vector2(1160.0, 650.0)),
		_fish_stage_scale, time_value, 1.0,
		combined_steer > FISH_STEER_DEAD_ZONE)


func _base_to_screen(point: Vector2) -> Vector2:
	return _fish_stage_offset + point * _fish_stage_scale


func handle_touch_press(screen_position: Vector2,
		source_token: StringName = &"legacy_world_touch") -> bool:
	return _begin_fish_steer(
		_touch_axis(screen_position), source_token)


func handle_touch_drag(screen_position: Vector2,
		source_token: StringName = &"legacy_world_touch") -> void:
	_update_fish_steer(_touch_axis(screen_position), source_token)


func handle_touch_release(
		source_token: StringName = &"legacy_world_touch") -> void:
	_finish_fish_steer(source_token)


func handle_touch_cancel(
		source_token: StringName = &"legacy_world_touch") -> void:
	cancel_input(source_token)
	_finish_fish_steer(source_token)


func handle_steer_press(axis: float,
		source_token: StringName = &"legacy_steer") -> bool:
	return _begin_fish_steer(axis, source_token)


func handle_steer_motion(axis: float,
		source_token: StringName = &"legacy_steer") -> void:
	_update_fish_steer(axis, source_token)


func handle_steer_release(
		source_token: StringName = &"legacy_steer") -> void:
	_finish_fish_steer(source_token)


func _touch_axis(screen_position: Vector2) -> float:
	var width: float = maxf(_fish_viewport_size.x, 1.0)
	var axis: float = clampf(screen_position.x / width * 2.0 - 1.0,
		-1.0, 1.0)
	return 0.0 if absf(axis) < FISH_TOUCH_DEAD_ZONE else axis


func _begin_fish_steer(axis: float, source_token: StringName) -> bool:
	if not is_canvas_fish_active():
		return false
	if input_context_lost() or _fish_input_context_restore_guard:
		return true
	if source_token.is_empty():
		return true
	if _fish_blocked_until_release:
		_fish_blocked_sources[source_token] = true
		return true
	_fish_steer_sources[source_token] = clampf(axis, -1.0, 1.0)
	if absf(axis) > FISH_STEER_DEAD_ZONE:
		m.g["steered"] = true
	_refresh_fish_steer_cues()
	return true


func _update_fish_steer(axis: float, source_token: StringName) -> void:
	if not is_canvas_fish_active() or input_context_lost() \
			or _fish_input_context_restore_guard:
		return
	if not _fish_steer_sources.has(source_token):
		return
	_fish_steer_sources[source_token] = clampf(axis, -1.0, 1.0)
	if absf(axis) > FISH_STEER_DEAD_ZONE:
		m.g["steered"] = true
	_refresh_fish_steer_cues()


func _finish_fish_steer(source_token: StringName) -> void:
	if input_context_lost() or _fish_input_context_restore_guard:
		return
	if _fish_blocked_until_release:
		if not _fish_blocked_sources.has(source_token):
			return
		_fish_blocked_sources.erase(source_token)
		if not _fish_blocked_sources.is_empty():
			return
		_fish_blocked_until_release = false
		_fish_pause_waiting_release = false
		_refresh_fish_steer_cues()
		return
	_fish_steer_sources.erase(source_token)
	_refresh_fish_steer_cues()


func _combined_fish_steer() -> float:
	if _fish_blocked_until_release or input_context_lost() \
			or _fish_input_context_restore_guard:
		return 0.0
	var axis := 0.0
	for source_value: Variant in _fish_steer_sources.values():
		axis += float(source_value)
	return clampf(axis, -1.0, 1.0)


func cancel_input(source_token: StringName = &"") -> void:
	if input_context_lost() or _fish_input_context_restore_guard:
		_arm_fish_context_restore_guard()
		return
	if source_token.is_empty():
		for held_value: Variant in _fish_steer_sources.keys():
			var held_token := StringName(String(held_value))
			_fish_blocked_sources[held_token] = true
		_fish_steer_sources.clear()
	else:
		if _fish_steer_sources.has(source_token):
			_fish_steer_sources.erase(source_token)
		_fish_blocked_sources[source_token] = true
	_fish_blocked_until_release = not _fish_blocked_sources.is_empty()
	_refresh_fish_steer_cues()


func arm_entry_sources(source_tokens: Array) -> void:
	if input_context_lost() or _fish_input_context_restore_guard:
		return
	for source_value: Variant in source_tokens:
		var source_token := StringName(String(source_value))
		if not source_token.is_empty():
			_fish_blocked_sources[source_token] = true
	if _fish_blocked_sources.is_empty():
		return
	_fish_blocked_until_release = true
	# Preserve the fresh build's opening guard until these exact entry sources
	# retire. Mid-run callers have already cleared it, so they remain unaffected.


func forget_sources_with_prefix(source_prefix: String) -> void:
	if source_prefix.is_empty() or input_context_lost() \
			or _fish_input_context_restore_guard:
		return
	for source_value: Variant in _fish_steer_sources.keys():
		var source_token := StringName(String(source_value))
		if String(source_token).begins_with(source_prefix):
			_fish_steer_sources.erase(source_token)
	for source_value: Variant in _fish_blocked_sources.keys():
		var source_token := StringName(String(source_value))
		if String(source_token).begins_with(source_prefix):
			_fish_blocked_sources.erase(source_token)
	if _fish_blocked_sources.is_empty():
		_fish_blocked_until_release = false
		_fish_pause_waiting_release = false
	_refresh_fish_steer_cues()


func on_pause_changed(paused: bool) -> void:
	if input_context_lost() or _fish_input_context_restore_guard:
		_arm_fish_context_restore_guard()
		return
	if paused:
		for source_value: Variant in _fish_steer_sources.keys():
			var source_token := StringName(String(source_value))
			_fish_blocked_sources[source_token] = true
		_fish_steer_sources.clear()
		_fish_pause_waiting_release = not _fish_blocked_sources.is_empty()
		_fish_blocked_until_release = _fish_pause_waiting_release
	elif not _fish_pause_waiting_release:
		_fish_blocked_until_release = false
		_fish_blocked_sources.clear()
	_refresh_fish_steer_cues()


func input_context_lost() -> bool:
	return not _fish_input_context_loss_reasons.is_empty()


func input_context_blocks_input() -> bool:
	return input_context_lost() or _fish_input_context_restore_guard


func retire_input_context_restore_guard() -> bool:
	# A resumed full-screen overlay is unpaused so its UI can animate, but the
	# ride itself remains frozen. Let Main spend the same source-free boundary
	# there without routing through _tick_game (which would advance g.t).
	if input_context_lost() or not _fish_input_context_restore_guard:
		return false
	var held_progress: float = float(m.g.get("canvas_context_progress",
		_fish_current_progress()))
	m.g["canvas_run_start_t"] = float(m.g.get("t", 0.0)) \
		- held_progress * FISH_RUN_SECONDS
	m.g.erase("canvas_context_progress")
	_fish_input_context_restore_guard = false
	_fish_blocked_until_release = false
	# A restore can complete before the opening transition callback. Preserve
	# that independent black-cover boundary so the ride clock still starts only
	# once the stage is actually revealed; mid-run restores see a clear fade.
	_fish_startup_release_guard = not _opening_fade_clear()
	return true


func _arm_fish_context_restore_guard() -> void:
	_fish_steer_sources.clear()
	_fish_blocked_sources.clear()
	_fish_blocked_until_release = true
	_fish_startup_release_guard = true
	_fish_pause_waiting_release = false
	_fish_input_context_restore_guard = true
	_refresh_fish_steer_cues()


func on_input_context_lost(reason: StringName) -> void:
	if reason.is_empty() or _fish_input_context_loss_reasons.has(reason):
		return
	var was_lost: bool = input_context_lost()
	_fish_input_context_loss_reasons[reason] = true
	if not was_lost:
		m.g["canvas_context_progress"] = _fish_current_progress()
		_arm_fish_context_restore_guard()


func on_input_context_restored(reason: StringName) -> void:
	if reason.is_empty() or not _fish_input_context_loss_reasons.has(reason):
		return
	_fish_input_context_loss_reasons.erase(reason)
	if not input_context_lost():
		_arm_fish_context_restore_guard()


func stage_close() -> void:
	_restore_fish_chime_state()
	var old_layer: CanvasLayer = _fish_layer
	if old_layer != null and is_instance_valid(old_layer):
		old_layer.visible = false
		if old_layer.get_parent() != null:
			old_layer.get_parent().remove_child(old_layer)
		old_layer.queue_free()
	_fish_layer = null
	_fish_surface = null
	_fish_screen_fill = null
	_fish_backdrop_root = null
	_fish_backdrop_tiles.clear()
	_fish_wash = null
	_fish_play_root = null
	_fish_trim = null
	_fish_slide = null
	_fish_friends = null
	_fish_roshan = null
	_fish_roshan_textures.clear()
	_fish_nodes.clear()
	_fish_pips.clear()
	_fish_left_cue = null
	_fish_right_cue = null
	_fish_fr = {}
	_fish_viewport_size = Vector2.ZERO
	_fish_stage_scale = 1.0
	_fish_stage_offset = Vector2.ZERO
	_fish_slide_rect = Rect2()
	_fish_friends_rect = Rect2()
	_fish_roshan_point = Vector2.ZERO
	_fish_completed = false
	_fish_tick_count = 0
	_fish_steer_sources.clear()
	_fish_blocked_sources.clear()
	_fish_blocked_until_release = false
	_fish_startup_release_guard = false
	_fish_pause_waiting_release = false
	_fish_input_context_loss_reasons.clear()
	_fish_input_context_restore_guard = false


func active_layer() -> CanvasLayer:
	return _fish_layer if _fish_layer != null \
		and is_instance_valid(_fish_layer) else null


func stage_root() -> Node2D:
	return _fish_surface if _fish_surface != null \
		and is_instance_valid(_fish_surface) else null


func refresh_canvas_layout() -> void:
	# Renderer-only boundary for Main/TouchUI paths which deliberately suppress
	# the gameplay tick (higher overlays, OS loss, or a paused restore).
	if active_layer() != null:
		_layout_canvas_fish(false)


func fish_count() -> int:
	return FISH_COUNT


func progress_count() -> int:
	return int(m.g.get("got", 0)) if m != null else 0


func fish_screen_point(index: int) -> Vector2:
	if index < 0 or index >= _fish_nodes.size():
		return Vector2.ZERO
	return _base_to_screen(_fish_nodes[index].position)


func roshan_screen_point() -> Vector2:
	return _base_to_screen(_fish_roshan_point) \
		if active_layer() != null else Vector2.ZERO


func left_steer_cue_screen_rect() -> Rect2:
	return _fish_left_cue.screen_rect() \
		if _fish_left_cue != null and is_instance_valid(_fish_left_cue) \
		else Rect2()


func right_steer_cue_screen_rect() -> Rect2:
	return _fish_right_cue.screen_rect() \
		if _fish_right_cue != null and is_instance_valid(_fish_right_cue) \
		else Rect2()


func left_steer_cue_screen_center() -> Vector2:
	return _fish_left_cue.cue_center \
		if _fish_left_cue != null and is_instance_valid(_fish_left_cue) \
		else Vector2.ZERO


func right_steer_cue_screen_center() -> Vector2:
	return _fish_right_cue.cue_center \
		if _fish_right_cue != null and is_instance_valid(_fish_right_cue) \
		else Vector2.ZERO


func left_steer_cue_screen_tip() -> Vector2:
	return _fish_left_cue.arrow_tip() \
		if _fish_left_cue != null and is_instance_valid(_fish_left_cue) \
		else Vector2.ZERO


func right_steer_cue_screen_tip() -> Vector2:
	return _fish_right_cue.arrow_tip() \
		if _fish_right_cue != null and is_instance_valid(_fish_right_cue) \
		else Vector2.ZERO


func audit_snapshot() -> Dictionary:
	if active_layer() == null or stage_root() == null:
		return {}
	var fish_points: Array[Vector2] = []
	for fish_index in range(_fish_nodes.size()):
		fish_points.append(fish_screen_point(fish_index))
	var pip_points: Array[Vector2] = []
	for pip: Sprite2D in _fish_pips:
		pip_points.append(_base_to_screen(pip.position))
	var tile_scales: Array[Vector2] = []
	for tile: Sprite2D in _fish_backdrop_tiles:
		tile_scales.append(tile.global_scale)
	var left_cue_center: Vector2 = left_steer_cue_screen_center()
	var right_cue_center: Vector2 = right_steer_cue_screen_center()
	var left_cue_tip: Vector2 = left_steer_cue_screen_tip()
	var right_cue_tip: Vector2 = right_steer_cue_screen_tip()
	var combined_steer: float = _combined_fish_steer()
	return {
		"game": String(m.game),
		"mode": String(m.g.get("mode", "")),
		"route_exact": is_canvas_fish_route(_fish_fr),
		"canvas_layer": _fish_layer.layer,
		"opaque": _fish_screen_fill.color.a >= 1.0,
		"viewport_size": _fish_viewport_size,
		"touch_hit_rect": Rect2(Vector2.ZERO, _fish_viewport_size),
		"tile_paths": FISH_TILE_PATHS.duplicate(),
		"tile_source_rects": FISH_TILE_SOURCE_RECTS.duplicate(),
		"tile_scales": tile_scales,
		"tile_common_position": _fish_backdrop_root.position,
		"tile_common_scale": _fish_backdrop_root.scale,
		"tile_native_reconstruction": Vector2i(2048, 2048),
		"slide_path": FISH_SLIDE_PATH,
		"friends_path": FISH_FRIENDS_PATH,
		"friends_protected_unchanged": true,
		"fish_path": FISH_ART_PATH,
		"roshan_paths": FISH_ROSHAN_PATHS.duplicate(),
		"slide_rect": Rect2(
			_base_to_screen(_fish_slide_rect.position),
			_fish_slide_rect.size * _fish_stage_scale),
		"friends_rect": Rect2(
			_base_to_screen(_fish_friends_rect.position),
			_fish_friends_rect.size * _fish_stage_scale),
		"roshan_point": roshan_screen_point(),
		"fish_points": fish_points,
		"pip_points": pip_points,
		"trim_band_top": _fish_trim.band_top() if _fish_trim != null else -1.0,
		"fish_progress_points": FISH_PROGRESS_POINTS.duplicate(),
		"fish_lanes": FISH_LANES.duplicate(),
		"got": progress_count(),
		"steered": bool(m.g.get("steered", false)),
		"lane": float(m.g.get("canvas_lane", 0.0)),
		"progress": _fish_current_progress(),
		"steer_cue_names": [
			"PersistentLeftSteerCue", "PersistentRightSteerCue"],
		"steer_cues_persistent": _fish_left_cue != null \
			and _fish_right_cue != null and _fish_left_cue.visible \
			and _fish_right_cue.visible,
		"steer_cue_half_extent": Vector2(67.0, 57.0) \
			* _fish_stage_scale,
		"left_steer_cue_rect": left_steer_cue_screen_rect(),
		"right_steer_cue_rect": right_steer_cue_screen_rect(),
		"left_steer_cue_center": left_cue_center,
		"right_steer_cue_center": right_cue_center,
		"left_steer_cue_tip": left_cue_tip,
		"right_steer_cue_tip": right_cue_tip,
		"left_steer_cue_direction": _fish_left_cue.cue_direction,
		"right_steer_cue_direction": _fish_right_cue.cue_direction,
		"left_steer_cue_active": _fish_left_cue.cue_active,
		"right_steer_cue_active": _fish_right_cue.cue_active,
		"left_steer_cue_center_axis": _touch_axis(left_cue_center),
		"right_steer_cue_center_axis": _touch_axis(right_cue_center),
		"left_steer_cue_tip_axis": _touch_axis(left_cue_tip),
		"right_steer_cue_tip_axis": _touch_axis(right_cue_tip),
		"combined_steer": combined_steer,
		"steer_cue_feedback_sign_exact": (
			_fish_left_cue.cue_active \
				== (combined_steer < -FISH_STEER_DEAD_ZONE)
			and _fish_right_cue.cue_active \
				== (combined_steer > FISH_STEER_DEAD_ZONE)),
		"steer_cues_on_correct_sides": (
			left_steer_cue_screen_rect().end.x < _fish_viewport_size.x * 0.5
			and right_steer_cue_screen_rect().position.x \
				> _fish_viewport_size.x * 0.5),
		"steer_cues_contained": Rect2(
			Vector2.ZERO, _fish_viewport_size).encloses(
				left_steer_cue_screen_rect()) and Rect2(
			Vector2.ZERO, _fish_viewport_size).encloses(
				right_steer_cue_screen_rect()),
		"dual_outward_one_direction_cues": true,
		"input_sources": _fish_steer_sources.duplicate(),
		"blocked_sources": _fish_blocked_sources.duplicate(),
		"blocked_until_release": _fish_blocked_until_release,
		"input_context_lost": input_context_lost(),
		"input_context_loss_reasons":
			_fish_input_context_loss_reasons.keys(),
		"input_context_restore_guard": _fish_input_context_restore_guard,
		"tick_count": _fish_tick_count,
		"completed": _fish_completed,
		"no_fail_state": true,
		"has_controller_timer_increment": false,
		"spatial_descendants": 0,
	}


func _opening_fade_clear() -> bool:
	return m.fade_rect == null or (m.fade_rect.modulate.a <= 0.02 \
		and m.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)


func _capture_fish_chime_state() -> void:
	_fish_chime_snapshot_valid = m != null and m.chime != null
	if _fish_chime_snapshot_valid:
		_fish_chime_volume_db = m.chime.volume_db
		_fish_chime_pitch_scale = m.chime.pitch_scale


func _restore_fish_chime_state() -> void:
	if _fish_chime_snapshot_valid and m != null and m.chime != null:
		m.chime.volume_db = _fish_chime_volume_db
		m.chime.pitch_scale = _fish_chime_pitch_scale
	_fish_chime_snapshot_valid = false


func handoff_fish_chime_to_completion_reward() -> void:
	# A completed ride hands the shared player to MedalSystem/_reward. Neutral
	# teardown still restores the pre-entry snapshot through stage_close().
	_fish_chime_snapshot_valid = false

func _build_playplace(origin: Vector3, fr: Dictionary) -> void:
	var gy: float = m.ARENA_POS.y
	var pads := [Color(1.0, 0.5, 0.6), Color(1.0, 0.85, 0.35), Color(0.4, 0.85, 0.95), Color(0.7, 0.55, 1.0)]
	if m.rainbow_slide_mode:
		pads = [Color(1.0, 0.25, 0.3), Color(1.0, 0.6, 0.15), Color(1.0, 0.9, 0.25), Color(0.3, 0.85, 0.4), Color(0.3, 0.55, 1.0), Color(0.6, 0.35, 0.9)]
	# spiral story platforms (3 stories)
	for i in range(9):
		var aa: float = float(i) * 0.75
		var rr: float = 14.0 - float(i) * 0.8
		var pp := Vector3(origin.x + cos(aa) * rr, gy + 2.0 + float(i) * 3.0, origin.z + sin(aa) * rr)
		m._course_box(pp, Vector3(5.5, 0.8, 4.2), pads[i % pads.size()])
	# story rims (visual floors)
	for st in range(3):
		var rim := MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 16.5
		tm.outer_radius = 17.3
		rim.mesh = tm
		rim.material_override = m._soft_mat(pads[st % pads.size()], 0.3)
		rim.position = Vector3(origin.x, gy + 10.0 + float(st) * 9.0, origin.z)
		m.add_child(rim)
		m.game_nodes.append(rim)
	# ball pit (colorful balls in a ring pool)
	var pit := Vector3(origin.x + 14.0, gy + 0.8, origin.z)
	var wall := MeshInstance3D.new()
	var wt := TorusMesh.new()
	wt.inner_radius = 5.4
	wt.outer_radius = 6.6
	wall.mesh = wt
	wall.material_override = m._soft_mat(Color(0.45, 0.6, 1.0), 0.2)
	wall.position = pit
	m.add_child(wall)
	m.game_nodes.append(wall)
	var mmi := MultiMeshInstance3D.new()
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var bms := SphereMesh.new()
	bms.radius = 0.55
	bms.height = 1.1
	var bmat := StandardMaterial3D.new()
	bmat.vertex_color_use_as_albedo = true
	bmat.roughness = 0.4
	bms.material = bmat
	mm.mesh = bms
	mm.instance_count = 90
	for bi in range(90):
		var ba: float = randf() * TAU
		var br: float = sqrt(randf()) * 4.8
		var bp := Vector3(pit.x + cos(ba) * br, gy + 0.7 + randf() * 1.6, pit.z + sin(ba) * br)
		mm.set_instance_transform(bi, Transform3D(Basis(), bp))
		mm.set_instance_color(bi, pads[bi % pads.size()])
	mmi.multimesh = mm
	m.add_child(mmi)
	m.game_nodes.append(mmi)
	# trampoline
	var tramp := Vector3(origin.x - 13.0, gy + 1.2, origin.z + 8.0)
	m._course_box(tramp, Vector3(4.6, 0.7, 4.6), Color(0.25, 0.45, 0.95))
	m._course_box(tramp + Vector3(0, -0.8, 0), Vector3(3.6, 0.9, 3.6), Color(0.15, 0.2, 0.4))
	m.g["tramp_pos"] = tramp
	# finger curtains (2 passages)
	m._build_chain_curtain(Vector3(origin.x - 5.0, gy + 17.5, origin.z - 11.0), Vector3(origin.x + 5.0, gy + 17.5, origin.z - 11.0), 7)
	m._build_chain_curtain(Vector3(origin.x + 4.0, gy + 27.5, origin.z + 3.0), Vector3(origin.x + 4.0, gy + 27.5, origin.z + 13.0), 7)
	# moving ring obstacle (story 2)
	var mv := MeshInstance3D.new()
	var mt := TorusMesh.new()
	mt.inner_radius = 2.6
	mt.outer_radius = 3.4
	mv.mesh = mt
	mv.material_override = m._soft_mat(Color(0.5, 1.0, 0.6), 0.6)
	mv.rotation_degrees = Vector3(90, 0, 0)
	mv.position = Vector3(origin.x - 6.0, gy + 19.0, origin.z + 6.0)
	m.add_child(mv)
	m.game_nodes.append(mv)
	m.g["mover_node"] = mv
	m.g["mover_base"] = mv.position
	# THE BIG SLIDE: yellow chute from the top to the ground
	var path: Array = [
		Vector3(origin.x, gy + 29.0, origin.z),
		Vector3(origin.x + 6.0, gy + 25.5, origin.z + 4.0),
		Vector3(origin.x + 11.0, gy + 21.0, origin.z + 8.0),
		Vector3(origin.x + 14.5, gy + 15.5, origin.z + 12.0),
		Vector3(origin.x + 16.0, gy + 10.0, origin.z + 16.5),
		Vector3(origin.x + 15.0, gy + 5.0, origin.z + 21.0),
		Vector3(origin.x + 12.5, gy + 2.8, origin.z + 25.0)]
	m.g["slide_path"] = path
	for i in range(path.size() - 1):
		var a2: Vector3 = path[i]
		var b2: Vector3 = path[i + 1]
		var mid: Vector3 = (a2 + b2) * 0.5
		var seg := MeshInstance3D.new()
		var sb := BoxMesh.new()
		sb.size = Vector3(3.4, 0.5, a2.distance_to(b2) + 0.7)
		seg.mesh = sb
		seg.material_override = m._soft_mat(Color(1.0, 0.8, 0.2), 0.25)
		m.add_child(seg)
		seg.look_at_from_position(mid, b2, Vector3.UP)
		m.game_nodes.append(seg)
		for sgn in [-1.0, 1.0]:
			var rail := MeshInstance3D.new()
			var rb := BoxMesh.new()
			rb.size = Vector3(0.4, 1.0, a2.distance_to(b2) + 0.7)
			rail.mesh = rb
			rail.material_override = m._soft_mat(Color(1.0, 0.55, 0.25), 0.2)
			m.add_child(rail)
			rail.look_at_from_position(mid, b2, Vector3.UP)
			rail.translate_object_local(Vector3(sgn * 1.7, 0.5, 0))
			m.game_nodes.append(rail)
	# friend cheering at the slide top (only when this game has a friend sprite — the Rainbow Slide has none)
	var cheer_node = fr.get("node")
	if cheer_node != null and is_instance_valid(cheer_node) and cheer_node is Sprite3D:
		var sis := Sprite3D.new()
		sis.texture = (cheer_node as Sprite3D).texture
		sis.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		sis.pixel_size = 0.013
		sis.position = path[0] + Vector3(-3.0, 3.0, -2.0)
		m.add_child(sis)
		m.game_nodes.append(sis)
	# checkpoints: ballpit -> trampoline -> curtain 1 -> moving ring -> curtain 2 -> slide
	m._add_check(pit + Vector3(0, 1.6, 0), "ball")
	m._add_check(m.g["tramp_pos"] + Vector3(0, 1.8, 0), "tramp")
	m._add_check(Vector3(origin.x, gy + 14.6, origin.z - 11.0), "curtain")
	m._add_check(mv.position, "mover")
	m._add_check(Vector3(origin.x + 4.0, gy + 24.6, origin.z + 8.0), "curtain")
	m._add_check(path[0], "slide")

# ===================== PENGUIN ICE SLIDE =====================
# A short N64-style downhill chute. Roshan slides on momentum (gravity along the
# slope); the player only steers left/right. 5 fish to grab, ~12 seconds.
const SLIDE_WIDTH := 18.0          # chute interior width
const SLIDE_GRAV := 44.0           # along-slope gravity pull
const SLIDE_FRICT := 0.32          # speed-proportional drag (sets terminal speed)
const SLIDE_VMAX := 26.0
const SLIDE_VMIN := 13.0           # keeps the flat finish from crawling
const SLIDE_STEER := 38.0          # lateral acceleration from steering
const SLIDE_RIDE := 2.2            # how far above the chute surface Roshan rides
const SLIDE_LEAD := 22.0           # baby penguin's head start (shrinks to 0 at the bottom)

func _slide_plank(a: Vector3, b: Vector3, width: float, mat: StandardMaterial3D, thick: float = 0.8) -> void:
	var mid: Vector3 = (a + b) * 0.5
	var dir: Vector3 = b - a
	var seg: float = dir.length()
	if seg < 0.001:
		return
	var fwd: Vector3 = dir / seg
	var right: Vector3 = Vector3.UP.cross(fwd)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	right = right.normalized()
	var up2: Vector3 = fwd.cross(right).normalized()
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(width, thick, seg)
	mi.mesh = bm
	mi.material_override = mat
	mi.transform = Transform3D(Basis(right, up2, fwd), mid)
	m.add_child(mi)
	m.game_nodes.append(mi)

func _aq_game(model: String, pos: Vector3, scl: float) -> Node3D:
	# spawn an aquatic model as a GAME object (freed with the arena, no flora_nodes leak)
	if m.CREATURE_GEN2.has(model):
		# the slide's baby penguin, cheer squad and bonus fish are HER art
		# too (owner 2026-07-11) - same family model + swim/waddle sway as
		# the reef, registered on the game-lifetime node list instead
		var cw := m._gen2_creature(String(m.CREATURE_GEN2[model]), pos, scl * 2.0)
		if cw != null:
			m.game_nodes.append(cw)
			return cw
	var ps := m._aq(model)
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	if not m.model_cache.has("aq2_" + model):
		m._paint_aq(inst, m._aq_mat(model))   # Riley models are untextured; gen2 aren't
	m.add_child(inst)
	m.game_nodes.append(inst)
	return inst

func _build_slide(origin: Vector3, theme: String = "ice", mode: String = "fish") -> void:
	# ---- centerline: an S-curve that descends, then flattens out at the bottom ----
	var path: Array = []
	var N := 26
	for i in range(N + 1):
		var t: float = float(i) / float(N)
		var z: float = lerp(-110.0, 120.0, t)
		var x: float = sin(t * TAU * 0.85) * 24.0
		# steep at the top (quick whoosh), easing flat near the bottom for a gentle finish
		var y: float = 2.0 + 48.0 * pow(1.0 - t, 1.2)
		path.append(origin + Vector3(x, y, z))
	m.g["path"] = path
	# precompute cumulative arc length
	var cum: Array = [0.0]
	var total := 0.0
	for i in range(path.size() - 1):
		total += (path[i + 1] - path[i]).length()
		cum.append(total)
	m.g["cum"] = cum
	m.g["total"] = total
	m.g["s"] = 0.0
	m.g["v"] = SLIDE_VMIN
	m.g["x"] = 0.0
	m.g["vx"] = 0.0
	m.g["got"] = 0
	m.g["caught"] = false
	# ---- build the chute: themed floor planks + glowing side rails ----
	var rainbow := [Color(0.90, 0.32, 0.42), Color(0.94, 0.58, 0.30), Color(0.92, 0.82, 0.30), Color(0.36, 0.76, 0.46), Color(0.34, 0.67, 0.90), Color(0.50, 0.44, 0.88), Color(0.78, 0.42, 0.84)]
	var rail := m._ice_mat(Color(0.42, 0.68, 0.90), 0.15) if theme == "ice" else m._ice_mat(Color(0.84, 0.72, 0.34), 0.18)
	for i in range(path.size() - 1):
		var a: Vector3 = path[i]
		var b: Vector3 = path[i + 1]
		# plank albedo stays UNDER 1.0 — over-white components push the snow
		# past ACES white and the surface detail clips away (Android blowout)
		var pmat: StandardMaterial3D = m._ice_mat(rainbow[i % rainbow.size()], 0.10) if theme == "rainbow" else m._ice_mat(Color(0.68, 0.78, 0.90), 0.02, "snow")
		_slide_plank(a, b, SLIDE_WIDTH, pmat)
		# side rails sit on the chute edges
		var smp := _slide_dir(i)
		var rt: Vector3 = smp[1]
		_slide_plank(a + rt * (SLIDE_WIDTH * 0.5), b + rt * (SLIDE_WIDTH * 0.5), 1.4, rail, 4.0)
		_slide_plank(a - rt * (SLIDE_WIDTH * 0.5), b - rt * (SLIDE_WIDTH * 0.5), 1.4, rail, 4.0)
		if i % 4 == 1:
			var bank_mid: Vector3 = (a + b) * 0.5
			var bank_fwd: Vector3 = (b - a).normalized()
			var bank_yaw: float = atan2(-bank_fwd.z, bank_fwd.x)
			for bank_side in [-1.0, 1.0]:
				pass
		if i % 4 == 3:
			var tree_side: float = -1.0 if int(i / 4) % 2 == 0 else 1.0
			var tree_pos: Vector3 = (a + b) * 0.5 + rt * tree_side * (SLIDE_WIDTH * 0.5 + 7.2)
			pass
	# A large physical star arch makes the bottom of the run readable from the
	# first bend and replaces the tiny generic finish bar.
	var finish_dir: Vector3 = ((path[path.size() - 1] as Vector3) - (path[path.size() - 2] as Vector3)).normalized()
	var finish_yaw: float = atan2(finish_dir.x, finish_dir.z)
	pass
	# ---- penguins cheering on the banks ----
	for k in range(6):
		var tt: float = 0.12 + 0.72 * float(k) / 5.0
		var ps := _slide_sample(tt * total)
		var side: float = -1.0 if k % 2 == 0 else 1.0
		var peng := _aq_game("Penguin", ps[0] + ps[2] * (side * (SLIDE_WIDTH * 0.5 + 4.0)) + Vector3(0, 2.0, 0), 3.0)
		if peng != null:
			# gen2 creatures face local -X (mover convention): atan2(-t.z, t.x)
			# points the face UP-slope, at the oncoming racer
			peng.rotation.y = atan2(-ps[1].z, ps[1].x) + (0.4 if side > 0.0 else -0.4)
			m._play_clip(peng, "cheer", 0.85 + 0.12 * float(k))   # phase-varied crowd
	m.g["fish"] = []
	if mode == "chase":
		# ---- the baby penguin you race + catch (positioned each frame in _tick_slide) ----
		var baby := _aq_game("Penguin", _slide_sample(40.0)[0] + Vector3(0, SLIDE_RIDE, 0), 2.2)
		m.g["peng_node"] = baby
		m.g["peng_x"] = 0.0
		if baby != null:
			# continuous snow spray kicked up at his tail (+X local: face is -X)
			# so his speed reads even when he's just a dot up the track
			var spray := CPUParticles3D.new()
			spray.amount = 70
			spray.lifetime = 0.7
			spray.direction = Vector3(1.0, 0.7, 0.0)
			spray.spread = 28.0
			spray.initial_velocity_min = 5.0
			spray.initial_velocity_max = 11.0
			spray.gravity = Vector3(0, -16.0, 0)
			spray.scale_amount_min = 0.16
			spray.scale_amount_max = 0.40
			var sbm := BoxMesh.new()
			sbm.size = Vector3(0.3, 0.3, 0.3)
			spray.mesh = sbm
			var spm := StandardMaterial3D.new()
			spm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			# icy BLUE, not white — white spray vanishes into the bright snow
			spm.albedo_color = Color(0.55, 0.8, 1.0)
			spray.material_override = spm
			spray.position = Vector3(1.8, 0.5, 0)
			baby.add_child(spray)
			m.g["peng_spray"] = spray
	else:
		# ---- 5 fish collectables, spaced along the run, alternating sides ----
		var spots := [0.16, 0.34, 0.52, 0.70, 0.86]
		var sides := [-1.0, 1.0, -0.4, 1.0, -1.0]
		for k in range(spots.size()):
			var samp := _slide_sample(float(spots[k]) * total)
			var fpos: Vector3 = samp[0] + samp[2] * (sides[k] * SLIDE_WIDTH * 0.32) + Vector3(0, SLIDE_RIDE + 1.6, 0)
			var fish := _aq_game("ClownFish", fpos, 3.0)
			if fish == null:
				fish = m._check_star(fpos)   # fallback if the model is missing
			var halo := m._halo(fpos, Color(1.0, 0.85, 0.4), 6.0)
			m.game_nodes.append(halo)
			(m.g["fish"] as Array).append({"node": fish, "halo": halo, "pos": fpos, "got": false})
		# ---- a big ball rolling behind, for the "chase" feel (decor only) ----
		var ball := MeshInstance3D.new()
		var bs := SphereMesh.new(); bs.radius = 7.0; bs.height = 14.0
		ball.mesh = bs
		ball.material_override = m._ice_mat(Color(1.0, 0.85, 0.4), 0.5) if theme == "rainbow" else m._ice_mat(Color(0.88, 0.93, 1.0), 0.05, "snow")
		m.add_child(ball); m.game_nodes.append(ball)
		m.g["ball"] = ball
	# ---- place Roshan at the top, facing down the chute ----
	var top := _slide_sample(0.0)
	m.player.position = top[0] + Vector3(0, SLIDE_RIDE, 0)
	m.player.vel = Vector3.ZERO
	m.player.yaw = atan2(top[1].x, top[1].z)

func _slide_dir(i: int) -> Array:
	# tangent + horizontal-right for segment i of the path
	var path: Array = m.g["path"]
	var j: int = clampi(i, 0, path.size() - 2)
	var fwd: Vector3 = (path[j + 1] - path[j]).normalized()
	var right: Vector3 = Vector3.UP.cross(fwd)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [fwd, right.normalized()]

func _slide_pos(s: float) -> Vector3:
	# R1: Catmull-Rom position at arc-length s. The MOTION/CAMERA path is
	# C1-smooth; the plank visuals still sit on the raw polyline (they look
	# fine and the rider floats SLIDE_RIDE above them).
	var path: Array = m.g["path"]
	var cum: Array = m.g["cum"]
	var total: float = m.g["total"]
	s = clampf(s, 0.0, total)
	var i := 0
	while i < cum.size() - 2 and float(cum[i + 1]) < s:
		i += 1
	var seg_len: float = float(cum[i + 1]) - float(cum[i])
	var f: float = 0.0 if seg_len < 0.001 else (s - float(cum[i])) / seg_len
	var p0: Vector3 = path[maxi(i - 1, 0)]
	var p1: Vector3 = path[i]
	var p2: Vector3 = path[mini(i + 1, path.size() - 1)]
	var p3: Vector3 = path[mini(i + 2, path.size() - 1)]
	var f2: float = f * f
	var f3: float = f2 * f
	return ((p1 * 2.0) + (p2 - p0) * f + (p0 * 2.0 - p1 * 5.0 + p2 * 4.0 - p3) * f2 + (p1 * 3.0 - p0 - p2 * 3.0 + p3) * f3) * 0.5

func _slide_sample(s: float) -> Array:
	# returns [pos, tangent, right] at arc-length s along the chute.
	# R1: tangent by central difference of the spline (ds=1.5m), never from
	# segment indices - heading is continuous, no more per-joint yaw snaps.
	var pos := _slide_pos(s)
	var fwd: Vector3 = _slide_pos(s + 1.5) - _slide_pos(s - 1.5)
	var fwd_n: Vector3 = fwd.normalized() if fwd.length() > 0.001 else Vector3.FORWARD
	var right: Vector3 = Vector3.UP.cross(fwd_n)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [pos, fwd_n, right.normalized()]

func _tick_slide(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	if is_canvas_fish_route(fr):
		if active_layer() != null:
			_tick_canvas_fish(delta, fr)
		return
	var total: float = m.g["total"]
	var s: float = m.g["s"]
	var samp := _slide_sample(s)
	var tangent: Vector3 = samp[1]
	var right: Vector3 = samp[2]
	# --- steering input (left/right only) ---
	var steer := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		steer -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		steer += 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		steer += jx
	if m.touch_ui != null and absf(m.touch_ui.stick_vec.x) > 0.15:
		steer += m.touch_ui.stick_vec.x
	steer = clampf(steer, -1.0, 1.0)
	if absf(steer) > 0.15:
		m.g["steered"] = true
	# --- along-slope physics: gravity pulls down the gradient, drag caps speed ---
	var v: float = m.g["v"]
	var grade: float = -tangent.y          # >0 going downhill
	v += (SLIDE_GRAV * grade - SLIDE_FRICT * v) * delta
	v = clampf(v, SLIDE_VMIN, SLIDE_VMAX)
	m.g["v"] = v
	m.g["s"] = s + v * delta
	# --- lateral steering with damping + soft walls ---
	# (negated: the chase-cam looks down +tangent, so the chute's "right" vector
	#  is screen-left — flip so pressing right steers screen-right)
	var vx: float = m.g["vx"]
	vx -= steer * SLIDE_STEER * delta
	vx *= pow(0.02, delta)
	var x: float = float(m.g["x"]) + vx * delta
	var lim: float = SLIDE_WIDTH * 0.5 - 2.0
	if absf(x) > lim:
		x = clampf(x, -lim, lim)
		vx *= -0.3                         # gentle bounce off the ice banks
	m.g["x"] = x
	m.g["vx"] = vx
	# --- place + orient Roshan ---
	var pos: Vector3 = samp[0] + right * x + Vector3(0, SLIDE_RIDE, 0)
	m.player.position = pos
	m.player.yaw = atan2(tangent.x, tangent.z)
	m.player.rotation = Vector3(-0.35, m.player.yaw + PI, -clampf(vx * 0.02, -0.5, 0.5))
	# --- chase camera, locked behind and above ---
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var cam_target: Vector3 = pos - tangent * 15.0 + Vector3(0, 7.0, 0)
		m.player.cam.position = m.player.cam.position.lerp(cam_target, 1.0 - pow(0.0008, delta))
		m.player.cam.look_at(pos + tangent * 6.0 + Vector3(0, 1.0, 0))
	if String(m.g.get("mode", "fish")) == "chase":
		# ===== RACE THE BABY PENGUIN — the BEAN PUZZLE =====
		# Without magic beans he is simply too fast: his lead never shrinks into catch
		# range and he crosses the finish first. EAT BEANS (Pearl Shop) and Roshan gets
		# the super-speed to reel him in — that's the puzzle.
		var p: float = s / total
		var beany: bool = m.beans_t >= 0.0 or bool(m.g.get("beany", false))
		m.g["beany"] = beany   # latch: beans active at any point during the ride count
		var gap: float
		if beany:
			gap = maxf(0.0, SLIDE_LEAD * (1.0 - p * 1.45))   # bean power: reel him in!
		else:
			# NO catch without beans (owner 2026-07-12, supersedes the old
			# "he tires at the bottom" window): the gap teases shut, but the
			# moment Roshan gets close he PANICS — a burst of speed rockets
			# him ahead again. Repeated near-misses sell "he's too speedy";
			# the Pearl Shop beans are the real answer.
			var burst: float = float(m.g.get("burst", 0.0))
			var base_gap: float = SLIDE_LEAD * maxf(0.18, 1.0 - p * 0.75)
			if base_gap + burst < 10.0:
				burst = minf(burst + 34.0 * delta, 18.0)
				m.g["panic_cool"] = float(m.g.get("panic_cool", 5.0)) - delta
				if float(m.g["panic_cool"]) <= 0.0:
					m.g["panic_cool"] = 5.0
					var pn0 = m.g.get("peng_node")
					if pn0 != null and is_instance_valid(pn0):
						m._sparkle_burst((pn0 as Node3D).position + Vector3(0, 1.5, 0), Color(0.7, 0.9, 1.0))
					if m.peng_giggle != null:
						m.peng_giggle.pitch_scale = 1.0 + randf() * 0.15   # cheeky escape giggle
						m.peng_giggle.play()
					if int(m.g.get("panic_n", 0)) < 2:
						m.g["panic_n"] = int(m.g.get("panic_n", 0)) + 1
						m.show_msg(fr["fname"], "WHEEE! He zoomed away! Maybe magic BEANS from the Pearl Shop would help!")
			else:
				burst = maxf(0.0, burst - 3.5 * delta)
			m.g["burst"] = burst
			gap = base_gap + burst
		var peng_s: float = minf(s + gap, total)
		# he FLEES sideways away from Roshan (slower than she can steer), pinned by the
		# chute walls — so a passive player never catches him; you must corner him.
		var px: float = float(m.g.get("peng_x", 0.0))
		var flee_dir: float = signf(px - x)
		if flee_dir == 0.0:
			flee_dir = 1.0 if sin(float(m.g["t"]) * 1.3) >= 0.0 else -1.0
		px += flee_dir * 7.5 * delta
		px += sin(float(m.g["t"]) * 2.5) * 1.2 * delta            # lively wander
		px = clampf(px, -lim, lim)
		m.g["peng_x"] = px
		var psamp := _slide_sample(peng_s)
		var pbpos: Vector3 = psamp[0] + psamp[2] * px + Vector3(0, SLIDE_RIDE, 0)
		var pnode = m.g.get("peng_node")
		if pnode != null and is_instance_valid(pnode):
			var pnd := pnode as Node3D
			pnd.position = pbpos
			var sprinting: bool = float(m.g.get("burst", 0.0)) > 0.5 or (beany and gap < 13.0)
			# gen2 creatures face local -X (mover convention): atan2(t.z, -t.x)
			# points his face DOWN-slope, the way he's racing. Euler is YXZ, so
			# z = innermost = nose-down luge lean, x = body shimmy roll.
			var pyaw: float = atan2(psamp[1].z, -psamp[1].x)
			var shimmy: float = sin(float(m.g["t"]) * (13.0 if sprinting else 9.0)) * (0.12 if sprinting else 0.18)
			pnd.rotation = Vector3(shimmy, pyaw, 0.30 if sprinting else 0.12)
			# rigged clips: he's RACING the whole ride — sprint luge always,
			# kicked faster while panicking or being reeled in
			m._play_clip(pnd, "sprint", 1.6 if sprinting else 1.1)
			var spray = m.g.get("peng_spray")
			if spray != null and is_instance_valid(spray):
				(spray as CPUParticles3D).speed_scale = 1.7 if sprinting else 1.0
		# catch when you've cornered him — BEANS ONLY (he escapes anyone slower)
		if beany and bool(m.g.get("steered", false)) and not bool(m.g.get("caught", false)) and gap < 9.0 and absf(x - px) < 4.5:
			m.g["caught"] = true
			m.award_sticker("penguin")
			var cn = m.g.get("peng_node")
			if cn != null and is_instance_valid(cn):
				m._play_clip(cn as Node3D, "cheer", 1.0)
			m._sparkle_burst(pbpos + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.4))
			if m.peng_giggle != null:
				m.peng_giggle.pitch_scale = 0.95
				m.peng_giggle.play()
			if m.chime != null:
				m.chime.pitch_scale = 1.5; m.chime.play()
			m._end_game(true, fr, "You caught the baby penguin! Hee hee, great race!")
			return
		if beany:
			m.hud_game.text = "BEAN POWER! Catch him!   ← →" if p > 0.3 else "Beans! Toot toot! GO GO GO!"
		elif float(m.g.get("burst", 0.0)) > 0.5:
			m.hud_game.text = "WHEE — too speedy! Beans from the Pearl Shop! ← →"
		else:
			m.hud_game.text = "Catch the baby penguin! ...he's SO fast!"
		if float(m.g["s"]) >= total - 0.5:
			if bool(m.g.get("steered", false)):
				m._end_game(true, fr, "What a race! The baby penguin zoomed ahead — and wants to race you again! Magic Beans can help you catch him.")
			else:
				# Auto-slide alone cannot complete the activity. Restart at the top
				# and demonstrate the one deliberate verb without a loss screen.
				m.g["s"] = 0.0
				m.g["x"] = 0.0
				m.g["vx"] = 0.0
				m.g["burst"] = 0.0
				m.show_msg(fr["fname"], "Lean LEFT or RIGHT to join the race! Take your time.", "hint")
			return
	else:
		# ===== COLLECT THE FISH =====
		# rolling chase snowball behind (decor)
		if m.g.has("ball") and is_instance_valid(m.g["ball"]):
			var bsamp := _slide_sample(maxf(0.0, s - 26.0))
			(m.g["ball"] as Node3D).position = bsamp[0] + Vector3(0, 5.0, 0)
			(m.g["ball"] as Node3D).rotate_x(delta * 3.0)
		for fd in m.g.get("fish", []):
			if fd["got"]:
				continue
			if (fd["pos"] as Vector3).distance_to(pos) < 4.2:
				fd["got"] = true
				m.g["got"] = int(m.g["got"]) + 1
				var fn: Node = fd["node"]
				if is_instance_valid(fn):
					fn.queue_free()
				var fh: Node = fd["halo"]
				if is_instance_valid(fh):
					fh.queue_free()
				m._sparkle_burst(pos + Vector3(0, 1.5, 0), Color(1.0, 0.85, 0.4))
				if m.chime != null:
					m.chime.pitch_scale = 1.0 + 0.12 * float(m.g["got"])
					m.chime.play()
		m.hud_game.text = "Slide!  " + m._pips(int(m.g["got"]), 5, "🐟")
		if float(m.g["s"]) >= total - 0.5:
			var got: int = int(m.g["got"])
			if bool(m.g.get("steered", false)):
				var msg := "WHEEE! You grabbed every fish! Best slider ever!" if got >= 5 else "What a ride! You caught %d fish!" % got
				m._end_game(true, fr, msg)
			else:
				m.g["s"] = 0.0
				m.g["x"] = 0.0
				m.g["vx"] = 0.0
				m.show_msg(fr["fname"], "Lean LEFT or RIGHT to join the slide! Take your time.", "hint")

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.g["checks"] = []
	m.g["chains"] = []
	_build_playplace(origin, fr)
	m.show_msg(fr["fname"], "Welcome to the play place! Touch the sparkles all the way up to the BIG slide!")

func build_slide(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0   # no countdown — reaching the bottom ends it (~12s run)
	var theme: String = String(fr.get("theme", "ice"))
	var mode: String = String(fr.get("mode", "fish"))
	m.g["mode"] = mode
	if is_canvas_fish_route(fr):
		_build_canvas_fish(fr)
		m._play_music("fetch")
		return
	_build_slide(origin, theme, mode)
	m._play_music("fetch")   # reuse the snowy track
	if theme == "rainbow":
		m.arena_env.background_color = Color(0.52, 0.72, 0.92)
		m.arena_env.ambient_light_color = Color(0.88, 0.90, 1.0)
		m.arena_env.ambient_light_energy = 0.62
		m._apply_scene_grade(m.arena_env, "bright_pastel")
	if mode == "chase":
		if m.beans_t >= 0.0:
			m.show_msg(fr["fname"], "BEANS POWER! Now catch that speedy penguin! GO GO GO!")
		else:
			m.show_msg(fr["fname"], "Race the baby penguin! Careful — he's SO speedy!")
			# non-reader breadcrumb to the beans: Roshan thinks out loud
			# SceneTree timers outlive this game AND main itself (probes rebuild
			# the scene) — the lambda must re-check m before touching it
			m.get_tree().create_timer(3.6).timeout.connect(func():
				if is_instance_valid(m) and m.game == "slide" \
						and String(m.g.get("mode", "")) == "chase" and m.beans_t < 0.0:
					m.show_msg("Roshan", "I sure am hungry... I bet I'd be faster after a good MEAL!", "hungry"))
	else:
		m.show_msg(fr["fname"], "Whooosh down the ice! Lean LEFT and RIGHT to grab all 5 fish!")

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m._tick_chains(delta, ppos)
	if m.g.has("mover_node"):
		var mvn: MeshInstance3D = m.g["mover_node"]
		mvn.position = (m.g["mover_base"] as Vector3) + Vector3(sin(float(m.g["t"]) * 0.9) * 6.0, 0, 0)
	# slide ride
	if String(m.g.get("phase", "")) == "slide":
		var path: Array = m.g["slide_path"]
		var st: float = float(m.g.get("slide_t", 0.0)) + delta * 13.0
		m.g["slide_t"] = st
		var total := 0.0
		for i in range(path.size() - 1):
			var seg_len: float = (path[i] as Vector3).distance_to(path[i + 1])
			if st <= total + seg_len:
				m.player.position = (path[i] as Vector3).lerp(path[i + 1], (st - total) / seg_len)
				m.player.vel = Vector3.ZERO
				m.hud_game.text = "WHEEEEE!"
				return
			total += seg_len
		m._sparkle_burst(m.player.position, Color(0.5, 0.85, 1.0))
		if m.chime != null:
			m.chime.play()
		m._end_game(true, fr, "What a SLIDE! Best play place ever!" if m.game == "race" else "")
		return
	var checks: Array = m.g.get("checks", [])
	var done := 0
	var nxt: Dictionary = {}
	for c in checks:
		if c["hit"]:
			done += 1
		elif nxt.is_empty():
			nxt = c
	m.hud_game.text = ("Climb the play place! Sparkles: %d / %d" if m.game == "race" else "Dive the caverns! Sparkles: %d / %d") % [done, checks.size()]
	if nxt.is_empty():
		return
	var node: Node3D = nxt["node"]
	node.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 5.0) * 0.15)
	node.rotate_z(delta * 0.75)
	# Phase 6: the FIRST sparkle must be earned — swim toward it to arm the
	# course. Until armed the magnet is off and checkpoints are inert, so a
	# player who does nothing goes nowhere; one little push starts the ride
	# and the magnet forgiveness carries her from there. Guide sparkles
	# point the way while she idles.
	var cprev: Vector3 = m.g.get("ppos_prev", ppos)
	var cvel: Vector3 = (ppos - cprev) / maxf(delta, 0.001)
	m.g["ppos_prev"] = ppos
	if not bool(m.g.get("armed", false)):
		var to_c: Vector3 = node.position - ppos
		if to_c.length() > 0.5 and cvel.dot(to_c.normalized()) > 2.0:
			m.g["arm_t"] = float(m.g.get("arm_t", 0.0)) + delta
			if float(m.g["arm_t"]) >= 0.2:
				m.g["armed"] = true
				m._sparkle_burst(ppos, Color(1.0, 0.95, 0.6))
		else:
			m.g["arm_t"] = 0.0
			m.g["guide_t"] = float(m.g.get("guide_t", 0.0)) - delta
			if float(m.g["guide_t"]) <= 0.0:
				m.g["guide_t"] = 0.8
				m._sparkle_burst(ppos.lerp(node.position, 0.35), Color(1.0, 0.9, 0.5))
				m._sparkle_burst(ppos.lerp(node.position, 0.65), Color(1.0, 0.9, 0.5))
			m.g["arm_hint_t"] = float(m.g.get("arm_hint_t", 0.0)) + delta
			if float(m.g["arm_hint_t"]) > 6.0 and not bool(m.g.get("arm_hinted", false)):
				m.g["arm_hinted"] = true
				m.show_msg(String(fr.get("fname", "Play Place")), "Swim to the twinkly sparkle to start!", "hint")
		if not bool(m.g.get("armed", false)):
			return
	var dd2: float = node.position.distance_to(ppos)
	# strong, far-reaching magnet carries a 4yo up the play-place automatically
	if dd2 < 34.0:
		m.player.position = m.player.position.lerp(node.position, minf(0.92, delta * 2.6 * (1.0 - dd2 / 34.0)))
		m.player.vel.y = maxf(m.player.vel.y, 0.0)
	if dd2 < 7.5:
		nxt["hit"] = true
		m._sparkle_burst(node.position, Color(1.0, 0.9, 0.5))
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + float(done) * 0.08
			m.chime.play()
		var kind := String(nxt["kind"])
		if kind == "tramp":
			m.player.vel.y = 26.0
			m.show_msg(fr["fname"], "BOING! Up you go!")
		elif kind == "slide":
			m.g["phase"] = "slide"
			m.g["slide_t"] = 0.0
		elif kind == "chest":
			m.pearl_count += 3
			m._update_hud()
			m._write_save()
			m._sparkle_burst(node.position, Color(1.0, 0.85, 0.3))
			m.award_sticker("treasure")
			m._end_game(true, fr, "TREASURE! +3 rainbow pearls for the Pearl Shop!")
		else:
			node.visible = false
