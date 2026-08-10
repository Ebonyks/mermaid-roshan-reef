class_name SeekGame
extends RefCounted
## Evie and Lamb-a's four-find game on one bounded, opaque Canvas surface.
## State remains on ReefMain; this satellite owns presentation and behavior.

const GOAL := 4
const REVEAL_SECONDS := 0.95
const CONTROL_REASON := "seek_game"
const FRAME_SIZE := Vector2(256.0, 256.0)

const EVIE_ANIMATION := "res://assets/minigames/seek/evie_animation.png"
const LAMMA_ANIMATION := "res://assets/minigames/seek/lamma_animation.png"
const EVIE_PORTRAIT := "res://assets/minigames/seek/evie_portrait.png"
const ROSHAN_ANIMATION := \
	"res://assets/characters/roshan_25d/roshan_gesture_a.png"
const BACKDROP_ART := [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c3.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c3.png",
]
const COVER_ART := [
	"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_medium_v1.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_slender_v1.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_medium_v1.png",
]
const EVIE_STATES := {
	&"idle": {"frames": [0, 1, 2, 3, 1], "fps": 3.2, "loop": true},
	&"point": {"frames": [0, 4, 4, 2], "fps": 3.0, "loop": true},
	&"cheer": {"frames": [5, 6, 7, 6], "fps": 5.5, "loop": true},
}
const LAMMA_STATES := {
	&"hide": {"frames": [4, 4, 0, 1], "fps": 2.8, "loop": true},
	&"peek": {"frames": [0, 1, 2, 3], "fps": 4.2, "loop": true},
	&"reveal": {"frames": [4, 5, 6, 7], "fps": 7.0, "loop": false},
	&"celebrate": {"frames": [5, 6, 7, 6], "fps": 5.8, "loop": true},
}
const ROSHAN_STATES := {
	&"wave": {"frames": [0, 1, 2, 3, 1], "fps": 4.0, "loop": true},
	&"cheer": {"frames": [4, 5, 6, 7], "fps": 5.2, "loop": true},
	&"clap": {"frames": [8, 9, 10, 11], "fps": 5.6, "loop": true},
}

const RoshanFrameWindows = preload("res://scripts/roshan_sprite_frames.gd")


class SeekAtlasActor extends TextureRect:
	var source_path := ""
	var state_specs: Dictionary = {}
	var animation_state: StringName = &""
	var displayed_frame := -1
	var frame_changes := 0
	var frame_cursor := 0.0
	var animation_finished := false
	var window_sheet := ""
	var atlas_texture: AtlasTexture = null
	var display_rect := Rect2()


	func setup_actor(path: String, specs: Dictionary,
			initial_state: StringName, corrected_sheet: String = "") -> void:
		source_path = path
		state_specs = specs
		window_sheet = corrected_sheet
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		focus_mode = Control.FOCUS_NONE
		expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		var source_texture: Texture2D = load(path) as Texture2D
		atlas_texture = AtlasTexture.new()
		atlas_texture.atlas = source_texture
		atlas_texture.region = Rect2(Vector2.ZERO, SeekGame.FRAME_SIZE)
		texture = atlas_texture
		play_state(initial_state, true)


	func set_display_rect(rect: Rect2) -> void:
		display_rect = rect
		_apply_display_rect()


	func play_state(next_state: StringName, restart: bool = false) -> void:
		if not state_specs.has(next_state):
			return
		if animation_state == next_state and not restart:
			return
		animation_state = next_state
		frame_cursor = 0.0
		animation_finished = false
		displayed_frame = -1
		_apply_sequence_frame()
		set_meta("seek_animation_state", String(animation_state))


	func advance(delta: float) -> void:
		if animation_state == &"" or not state_specs.has(animation_state):
			return
		var spec: Dictionary = state_specs[animation_state]
		var sequence: Array = spec.get("frames", []) as Array
		if sequence.is_empty():
			return
		var fps := float(spec.get("fps", 1.0))
		var loop := bool(spec.get("loop", true))
		frame_cursor += maxf(delta, 0.0) * fps
		if loop:
			frame_cursor = fposmod(frame_cursor, float(sequence.size()))
		else:
			var last_cursor := float(sequence.size() - 1)
			if frame_cursor >= last_cursor:
				frame_cursor = last_cursor
				animation_finished = true
		_apply_sequence_frame()


	func _apply_sequence_frame() -> void:
		if atlas_texture == null or not state_specs.has(animation_state):
			return
		var spec: Dictionary = state_specs[animation_state]
		var sequence: Array = spec.get("frames", []) as Array
		if sequence.is_empty():
			return
		var sequence_index := clampi(int(floor(frame_cursor)), 0,
			sequence.size() - 1)
		var next_frame := int(sequence[sequence_index])
		if displayed_frame != next_frame:
			displayed_frame = next_frame
			frame_changes += 1
			set_meta("seek_displayed_frame", displayed_frame)
		if window_sheet.is_empty():
			var cell := Vector2(float(displayed_frame % 4),
				float(displayed_frame / 4)) * SeekGame.FRAME_SIZE
			atlas_texture.region = Rect2(cell, SeekGame.FRAME_SIZE)
		else:
			atlas_texture.region = RoshanFrameWindows.region(
				window_sheet, displayed_frame, 4)
		_apply_display_rect()


	func _apply_display_rect() -> void:
		position = display_rect.position
		size = display_rect.size
		pivot_offset = size * 0.5
		if not window_sheet.is_empty() and displayed_frame >= 0:
			var correction: Vector2 = RoshanFrameWindows.shift(
				window_sheet, displayed_frame)
			position += Vector2(
				correction.x * size.x / SeekGame.FRAME_SIZE.x,
				correction.y * size.y / SeekGame.FRAME_SIZE.y)


class SeekMeadowSurface extends Control:
	signal bush_pressed(index: int)

	const BUSH_CENTERS := [0.13, 0.375, 0.625, 0.87]
	const WRONG_SECONDS := 0.55
	const BACKDROP_NATIVE_SIZE := Vector2(2048.0, 2048.0)

	var backdrop: Control = null
	var backdrop_tiles: Array[TextureRect] = []
	var bushes: Array[TextureRect] = []
	var bush_hit_rects: Array[Rect2] = []
	var roshan_actor: SeekAtlasActor = null
	var evie_actor: SeekAtlasActor = null
	var lamma_actor: SeekAtlasActor = null
	var which := 0
	var found := 0
	var elapsed := 0.0
	var help_seconds := 0.0
	var assist_strength := 0.0
	var revealing := false
	var reveal_elapsed := 0.0
	var wrong_index := -1
	var wrong_t := 0.0


	func setup() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		focus_mode = Control.FOCUS_NONE
		clip_contents = true
		set_process(false)

		backdrop = Control.new()
		backdrop.name = "SeekBackdropMosaic"
		backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
		backdrop.z_index = -100
		add_child(backdrop)
		for index in range(SeekGame.BACKDROP_ART.size()):
			var tile := TextureRect.new()
			tile.name = "SeekBackdropTile%d" % index
			tile.texture = load(String(SeekGame.BACKDROP_ART[index])) as Texture2D
			tile.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			tile.stretch_mode = TextureRect.STRETCH_SCALE
			tile.mouse_filter = Control.MOUSE_FILTER_IGNORE
			backdrop.add_child(tile)
			backdrop_tiles.append(tile)

		lamma_actor = SeekAtlasActor.new()
		lamma_actor.name = "SeekLammaActor"
		lamma_actor.z_index = 10
		lamma_actor.setup_actor(SeekGame.LAMMA_ANIMATION,
			SeekGame.LAMMA_STATES, &"hide")
		add_child(lamma_actor)

		for index in range(SeekGame.GOAL):
			var cover := TextureRect.new()
			cover.name = "SeekCover%d" % index
			cover.texture = load(String(SeekGame.COVER_ART[index])) as Texture2D
			cover.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			cover.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			cover.mouse_filter = Control.MOUSE_FILTER_IGNORE
			cover.flip_h = index % 2 == 1
			cover.z_index = 20
			add_child(cover)
			bushes.append(cover)

		roshan_actor = SeekAtlasActor.new()
		roshan_actor.name = "SeekRoshanActor"
		roshan_actor.z_index = 30
		roshan_actor.setup_actor(SeekGame.ROSHAN_ANIMATION,
			SeekGame.ROSHAN_STATES, &"wave", "gesture_a")
		add_child(roshan_actor)

		evie_actor = SeekAtlasActor.new()
		evie_actor.name = "SeekEvieActor"
		evie_actor.z_index = 30
		evie_actor.setup_actor(SeekGame.EVIE_ANIMATION,
			SeekGame.EVIE_STATES, &"point")
		add_child(evie_actor)

		set_meta("no_fail", true)
		set_meta("visual_pointer", true)
		set_meta("objective_recording_gap", "evie_tap_wiggly_bush")
		set_meta("approved_backdrop_art", SeekGame.BACKDROP_ART)
		set_meta("approved_cover_art", SeekGame.COVER_ART)
		set_meta("approved_actor_art", [
			SeekGame.ROSHAN_ANIMATION, SeekGame.EVIE_ANIMATION,
			SeekGame.LAMMA_ANIMATION])


	func layout_for(viewport_size: Vector2) -> void:
		position = Vector2.ZERO
		size = viewport_size
		_layout_backdrop(viewport_size)

		bush_hit_rects.clear()
		var hit_width := clampf(viewport_size.x * 0.205, 145.0, 270.0)
		var hit_height := clampf(viewport_size.y * 0.38, 155.0, 285.0)
		var cover_base := viewport_size.y * 0.94
		for index in range(bushes.size()):
			var center_x := viewport_size.x * float(BUSH_CENTERS[index])
			var hit_rect := Rect2(
				Vector2(center_x - hit_width * 0.5, cover_base - hit_height),
				Vector2(hit_width, hit_height))
			bush_hit_rects.append(hit_rect)
			var cover: TextureRect = bushes[index]
			var texture_size: Vector2 = cover.texture.get_size() \
				if cover.texture != null else Vector2(1.0, 1.0)
			var cover_height := hit_height * 0.96
			var cover_width := cover_height * texture_size.x \
				/ maxf(texture_size.y, 1.0)
			cover.position = Vector2(
				center_x - cover_width * 0.5, cover_base - cover_height)
			cover.size = Vector2(cover_width, cover_height)
			cover.pivot_offset = cover.size * 0.5

		var host_size := clampf(minf(
			viewport_size.x / 1280.0, viewport_size.y / 720.0) * 205.0,
			154.0, 218.0)
		roshan_actor.set_display_rect(Rect2(
			Vector2(viewport_size.x * 0.205, viewport_size.y * 0.14),
			Vector2.ONE * host_size))
		evie_actor.set_display_rect(Rect2(
			Vector2(viewport_size.x * 0.67, viewport_size.y * 0.15),
			Vector2.ONE * host_size))
		_update_lamma_pose()
		queue_redraw()


	func begin_hide(next_index: int, progress: int) -> void:
		which = clampi(next_index, 0, SeekGame.GOAL - 1)
		found = clampi(progress, 0, SeekGame.GOAL)
		revealing = false
		reveal_elapsed = 0.0
		help_seconds = 0.0
		assist_strength = 0.0
		wrong_index = -1
		wrong_t = 0.0
		# The authored tree cards have intentionally open, transparent roots.
		# Keep Lamb-a binary-hidden until an authored peek begins so no part of
		# her opaque atlas can leak below a cover or through the stage frame.
		lamma_actor.visible = false
		lamma_actor.modulate = Color.WHITE
		lamma_actor.play_state(&"hide", true)
		roshan_actor.play_state(&"wave")
		evie_actor.play_state(&"point")
		_update_lamma_pose()
		queue_redraw()


	func begin_reveal(progress: int) -> void:
		found = clampi(progress, 0, SeekGame.GOAL)
		revealing = true
		reveal_elapsed = 0.0
		wrong_index = -1
		wrong_t = 0.0
		lamma_actor.visible = true
		lamma_actor.modulate = Color.WHITE
		lamma_actor.play_state(&"reveal", true)
		roshan_actor.play_state(&"clap" if found >= SeekGame.GOAL else &"cheer")
		evie_actor.play_state(&"cheer")
		_update_lamma_pose()
		queue_redraw()


	func set_help_seconds(seconds: float) -> void:
		help_seconds = maxf(seconds, 0.0)


	func play_wrong(index: int) -> void:
		wrong_index = clampi(index, 0, SeekGame.GOAL - 1)
		wrong_t = WRONG_SECONDS
		queue_redraw()


	func advance(delta: float) -> void:
		elapsed += delta
		wrong_t = maxf(0.0, wrong_t - delta)
		if wrong_t <= 0.0:
			wrong_index = -1
		if revealing:
			reveal_elapsed = minf(
				reveal_elapsed + delta, SeekGame.REVEAL_SECONDS)

		_update_lamma_pose()
		roshan_actor.advance(delta)
		evie_actor.advance(delta)
		lamma_actor.advance(delta)

		for index in range(bushes.size()):
			var cover: TextureRect = bushes[index]
			var wobble := 0.0
			var pulse := 1.0
			cover.modulate = Color.WHITE
			if index == which and not revealing:
				wobble = sin(elapsed * 6.4) * (0.038 + assist_strength * 0.018)
				pulse = 1.0 + (sin(elapsed * 4.8) + 1.0) \
					* (0.012 + assist_strength * 0.008)
			elif index == which and revealing:
				var reveal_progress := clampf(
					reveal_elapsed / SeekGame.REVEAL_SECONDS, 0.0, 1.0)
				wobble = sin(reveal_progress * PI) \
					* (0.085 if index % 2 == 0 else -0.085)
				pulse = 1.0 - sin(reveal_progress * PI) * 0.045
			elif index == wrong_index and wrong_t > 0.0:
				var wrong_phase := (WRONG_SECONDS - wrong_t) * 31.0
				wobble = sin(wrong_phase) * 0.14
				pulse = 1.0 + absf(sin(wrong_phase)) * 0.14
				cover.modulate = Color(1.0, 0.92, 0.52)
			cover.rotation = wobble
			cover.scale = Vector2.ONE * pulse
		queue_redraw()


	func reveal_complete() -> bool:
		return revealing and reveal_elapsed >= SeekGame.REVEAL_SECONDS


	func bush_hit_rect(index: int) -> Rect2:
		if index < 0 or index >= bush_hit_rects.size():
			return Rect2()
		return bush_hit_rects[index]


	func backdrop_tile_rect(index: int) -> Rect2:
		if backdrop == null or index < 0 or index >= backdrop_tiles.size():
			return Rect2()
		var tile: TextureRect = backdrop_tiles[index]
		return Rect2(backdrop.position + tile.position, tile.size)


	func focus_rect_at(at_elapsed: float) -> Rect2:
		var target := bush_hit_rect(which)
		if target.size.is_zero_approx():
			return Rect2()
		var radius := minf(78.0, target.size.x * 0.29) \
			+ sin(at_elapsed * 4.4) * 3.0
		var bob := sin(at_elapsed * 3.6) * 4.0
		var center := Vector2(target.get_center().x,
			target.end.y - radius - 9.0 + bob)
		return Rect2(
			Vector2(center.x - radius - 7.0, center.y - 7.0),
			Vector2((radius + 7.0) * 2.0, radius + 14.0))


	func pair_reveal_rect() -> Rect2:
		return _lamma_reveal_rect()


	func _layout_backdrop(viewport_size: Vector2) -> void:
		if backdrop == null:
			return
		var backdrop_scale := viewport_size.x / BACKDROP_NATIVE_SIZE.x
		var tile_size := Vector2(1024.0, 1024.0) * backdrop_scale
		var mosaic_size := BACKDROP_NATIVE_SIZE * backdrop_scale
		backdrop.position = Vector2(0.0,
			(viewport_size.y - mosaic_size.y) * 0.5)
		backdrop.size = mosaic_size
		for index in range(backdrop_tiles.size()):
			var row := index / 2
			var column := index % 2
			var tile: TextureRect = backdrop_tiles[index]
			tile.position = Vector2(float(column), float(row)) * tile_size
			tile.size = tile_size


	func _update_lamma_pose() -> void:
		if lamma_actor == null or bush_hit_rects.is_empty():
			return
		if revealing:
			assist_strength = 0.0
			var progress := clampf(
				reveal_elapsed / SeekGame.REVEAL_SECONDS, 0.0, 1.0)
			var eased := progress * progress * (3.0 - 2.0 * progress)
			lamma_actor.set_display_rect(_lerp_rect(
				_lamma_hidden_rect(), _lamma_reveal_rect(), eased))
			if lamma_actor.animation_finished:
				lamma_actor.play_state(&"celebrate")
			return

		assist_strength = 0.0
		if help_seconds >= 20.0:
			assist_strength = 1.0
		elif help_seconds >= 8.0:
			var peek_phase := fposmod(elapsed, 2.8)
			if peek_phase < 0.75:
				assist_strength = sin(peek_phase / 0.75 * PI)
		lamma_actor.set_display_rect(_lerp_rect(
			_lamma_hidden_rect(), _lamma_peek_rect(), assist_strength))
		lamma_actor.visible = assist_strength > 0.01
		lamma_actor.play_state(&"peek" if assist_strength > 0.01 else &"hide")


	func _lamma_hidden_rect() -> Rect2:
		var target := bush_hit_rect(which)
		var actor_size := _lamma_actor_size()
		return Rect2(Vector2(
			target.get_center().x - actor_size * 0.5,
			target.end.y - actor_size * 0.55), Vector2.ONE * actor_size)


	func _lamma_peek_rect() -> Rect2:
		var target := bush_hit_rect(which)
		var actor_size := _lamma_actor_size()
		return Rect2(Vector2(
			target.get_center().x - actor_size * 0.5,
			target.position.y - actor_size * 0.35), Vector2.ONE * actor_size)


	func _lamma_reveal_rect() -> Rect2:
		var target := bush_hit_rect(which)
		var actor_size := _lamma_actor_size()
		return Rect2(Vector2(
			target.get_center().x - actor_size * 0.5,
			target.position.y - actor_size * 0.70), Vector2.ONE * actor_size)


	func _lamma_actor_size() -> float:
		return clampf(minf(size.x / 1280.0, size.y / 720.0) * 210.0,
			158.0, 224.0)


	func _lerp_rect(from: Rect2, to: Rect2, weight: float) -> Rect2:
		return Rect2(from.position.lerp(to.position, weight),
			from.size.lerp(to.size, weight))


	func _gui_input(event: InputEvent) -> void:
		if revealing:
			return
		var local_position := Vector2.ZERO
		var pressed := false
		if event is InputEventScreenTouch:
			var touch := event as InputEventScreenTouch
			local_position = touch.position
			pressed = touch.pressed
		elif event is InputEventMouseButton:
			var button := event as InputEventMouseButton
			local_position = button.position
			pressed = button.button_index == MOUSE_BUTTON_LEFT and button.pressed
		if not pressed:
			return
		for index in range(bush_hit_rects.size()):
			if bush_hit_rect(index).has_point(local_position):
				bush_pressed.emit(index)
				accept_event()
				return


	func _draw() -> void:
		if size.is_zero_approx():
			return
		# Four large picture pips are the reading-free goal and progress display.
		for index in range(SeekGame.GOAL):
			var pip_x := size.x * 0.5 \
				+ (float(index) - 1.5) * minf(58.0, size.x * 0.052)
			draw_circle(Vector2(pip_x + 2.0, size.y * 0.073 + 3.0), 23.0,
				Color(0.10, 0.08, 0.24, 0.28))
			draw_circle(Vector2(pip_x, size.y * 0.073), 22.0,
				Color(0.12, 0.10, 0.27, 0.96))
			draw_circle(Vector2(pip_x, size.y * 0.073), 15.0,
				Color(1.0, 0.72, 0.45) if index < found
				else Color(0.87, 0.95, 0.88, 0.82))

		# The focus is a pulsing lower U behind the authored cover art.
		if not revealing:
			var focus_rect := focus_rect_at(elapsed)
			if not focus_rect.size.is_zero_approx():
				var radius := focus_rect.size.x * 0.5 - 7.0
				var center := Vector2(focus_rect.get_center().x,
					focus_rect.position.y + 7.0)
				var focus_alpha := 0.74 + (sin(elapsed * 4.4) + 1.0) * 0.09
				draw_arc(center, radius, 0.0, PI, 42,
					Color(0.12, 0.10, 0.27, focus_alpha), 12.0, true)
				draw_arc(center, radius, 0.0, PI, 42,
					Color(1.0, 0.78, 0.30, focus_alpha), 6.0, true)

		# Wrong covers rustle brightly; no pip, timer or progress changes.
		if wrong_index >= 0 and wrong_t > 0.0:
			var wrong_rect := bush_hit_rect(wrong_index)
			var fade := wrong_t / WRONG_SECONDS
			for side in [-1.0, 1.0]:
				var start := Vector2(wrong_rect.get_center().x
					+ side * wrong_rect.size.x * 0.40,
					wrong_rect.position.y + wrong_rect.size.y * 0.20)
				draw_line(start, start + Vector2(side * 28.0, -22.0),
					Color(1.0, 0.91, 0.38, fade), 7.0, true)

		# Navy/purple double frame locks the scene to the established UI language.
		draw_rect(Rect2(Vector2.ZERO, size).grow(-7.0),
			Color(0.12, 0.10, 0.27), false, 14.0)
		draw_rect(Rect2(Vector2.ZERO, size).grow(-18.0),
			Color(0.75, 0.63, 0.93, 0.92), false, 4.0)


var m: ReefMain
var layer: CanvasLayer = null
var surface: SeekMeadowSurface = null
var controls_owned := false


static func runtime_art_paths() -> Array[String]:
	var paths: Array[String] = [
		EVIE_ANIMATION, LAMMA_ANIMATION, EVIE_PORTRAIT, ROSHAN_ANIMATION,
	]
	for path_value: Variant in BACKDROP_ART:
		paths.append(String(path_value))
	for path_value: Variant in COVER_ART:
		var path := String(path_value)
		if not paths.has(path):
			paths.append(path)
	return paths


func _init(main: ReefMain) -> void:
	m = main


func build(fr: Dictionary) -> void:
	stage_close()
	m.g["found"] = 0
	m.g["timer"] = -1.0
	m.g["help_t"] = 0.0
	m.g["slow_find"] = 0.0
	m.g["gig_t"] = 2.2
	m.g["which"] = -1
	m.g["reveal_wait"] = 0.0
	m.g["wrong_taps"] = 0
	m._set_world_controls_enabled(false, CONTROL_REASON)
	controls_owned = true

	layer = CanvasLayer.new()
	layer.name = "SeekMeadowLayer"
	layer.layer = 7
	m.add_child(layer)

	surface = SeekMeadowSurface.new()
	surface.name = "SeekMeadowSurface"
	layer.add_child(surface)
	surface.setup()
	surface.bush_pressed.connect(_on_bush_pressed)
	_layout_surface()

	m.g["seek_layer"] = layer
	m.g["seek_surface"] = surface
	m.g["bushes"] = surface.bushes
	m.g["lamb"] = surface.lamma_actor
	_seek_hide()
	# The available Evie start recording announces hide-and-seek, but does not
	# say the exact tap verb. The persistent wiggle, U-cue, peek and giggle carry
	# that missing semantic without modifying protected family recordings.
	m.show_msg(fr["fname"],
		"Lamb-a' is hiding! Tap the wiggly tree to find her!")


func tick(delta: float, fr: Dictionary) -> void:
	if surface == null or not is_instance_valid(surface) \
			or not surface.is_inside_tree():
		return
	_layout_surface()
	if not surface.revealing:
		m.g["help_t"] = float(m.g.get("help_t", 0.0)) + delta
		surface.set_help_seconds(float(m.g["help_t"]))
		m.g["gig_t"] = float(m.g.get("gig_t", 2.2)) - delta
		if float(m.g["gig_t"]) <= 0.0:
			m.g["gig_t"] = 2.8
			if m.voice != null:
				m.voice.pitch_scale = 1.45 + randf() * 0.15
				m.voice.play()
		var button_index := m._btn_pressed()
		if button_index >= 0:
			_on_bush_pressed(button_index)
	surface.advance(delta)
	if surface.revealing and surface.reveal_complete():
		if int(m.g.get("found", 0)) >= GOAL:
			m._end_game(true, fr,
				"You found Lamb-a' every time! Best seeker ever!")
			return
		_seek_hide()
	m.hud_game.text = ""


func _on_bush_pressed(index: int) -> void:
	if surface == null or not is_instance_valid(surface) or surface.revealing:
		return
	if index != int(m.g.get("which", -1)):
		m.g["wrong_taps"] = int(m.g.get("wrong_taps", 0)) + 1
		surface.play_wrong(index)
		if m.chime != null:
			m.chime.pitch_scale = 0.92
			m.chime.play()
		return
	m.g["slow_find"] = maxf(float(m.g.get("slow_find", 0.0)),
		float(m.g.get("help_t", 0.0)))
	m.g["found"] = int(m.g.get("found", 0)) + 1
	m.g["help_t"] = 0.0
	surface.begin_reveal(int(m.g["found"]))
	if m.voice != null:
		m.voice.pitch_scale = 1.0 + randf() * 0.3
		m.voice.play()


func _seek_hide() -> void:
	if surface == null or not is_instance_valid(surface):
		return
	var previous := int(m.g.get("which", -1))
	var candidates: Array[int] = []
	var portrait_over_left := m.speech_layer != null \
		and is_instance_valid(m.speech_layer) and m.speech_layer.visible \
		and m.speech_t > 0.0
	for index in range(GOAL):
		if index != previous and (index != 0 or not portrait_over_left):
			candidates.append(index)
	# There are always at least two eligible trees, but retain a defensive
	# fallback so a future layout/count change cannot strand the activity.
	if candidates.is_empty():
		for index in range(GOAL):
			if index != previous:
				candidates.append(index)
	var next_index := candidates[randi() % candidates.size()]
	m.g["which"] = next_index
	m.g["help_t"] = 0.0
	m.g["gig_t"] = 2.2
	surface.begin_hide(next_index, int(m.g.get("found", 0)))


func _layout_surface() -> void:
	if surface == null or not is_instance_valid(surface):
		return
	surface.layout_for(m.get_viewport().get_visible_rect().size)


func stage_close() -> void:
	var old_layer: CanvasLayer = layer
	if old_layer != null and is_instance_valid(old_layer):
		if old_layer.get_parent() != null:
			old_layer.get_parent().remove_child(old_layer)
		old_layer.queue_free()
	surface = null
	layer = null
	if m != null and controls_owned:
		m._set_world_controls_enabled(true, CONTROL_REASON)
	controls_owned = false
