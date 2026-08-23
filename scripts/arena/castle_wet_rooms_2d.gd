class_name CastleWetRooms2D
extends RefCounted

# Conditional true-Canvas presentation for the Mermaid Pool and Bubble Bath.
# The parent Castle controller remains the state owner and supplies normalized
# snapshots from its legacy room registry while those other rooms migrate.

const ART_TO_STAGE := 1.25
const PLAYER_HEIGHT := 270.0
const PLAYER_BASE_SIZE := Vector2(256.0, 256.0)
const WET_ROOM_IDS: Array[String] = ["mermaid_pool", "bubble_bath"]
const WATER_FIXTURE := preload("res://scripts/water/castle_water_fixture_2d.gd")
const WATER_FX := preload("res://scripts/water/water_fx_2d.gd")
const WATER_MEDIUM := preload("res://scripts/water/water_medium_state_2d.gd")
const ROSHAN_FRAMES := preload("res://scripts/roshan_sprite_frames.gd")
const DIRECTIONAL: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_directional.png")
const SWIM_FRONT: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_swim_front.png")
const SHADOW: Texture2D = preload(
	"res://assets/flats/castle/rooms/room_actor_shadow.png")

var m: ReefMain
var root: Node2D = null
var room_id := ""
var fixture_sprites: Dictionary = {}
var fixture_water: Dictionary = {}
var actor: Sprite2D = null
var actor_submerged: Sprite2D = null
var actor_shadow: Sprite2D = null
var actor_front_water: Polygon2D = null
var actor_waterline: Line2D = null
var fx: WaterFx2D = null
var medium: RefCounted = null
var walk_rect := Rect2()
var _actor_foot := Vector2(640.0, 640.0)
var _actor_target := Vector2(640.0, 640.0)
var _actor_velocity := Vector2.ZERO
var _actor_frame_time := 0.0
var _actor_frame := 0
var _actor_source_rect := Rect2()
var _medium_state := "DRY"
var _movement_tween: Tween = null


func _init(main: ReefMain) -> void:
	m = main


func is_active() -> bool:
	return root != null and is_instance_valid(root)


func supports(candidate_room_id: String) -> bool:
	return candidate_room_id in WET_ROOM_IDS


func open(stage: Control, candidate_room_id: String,
		background_specs: Array[Dictionary], fixture_specs: Array[Dictionary],
		foreground_specs: Array[Dictionary], layout: Dictionary,
		player_texture: Texture2D) -> bool:
	close()
	if stage == null or not supports(candidate_room_id):
		return false
	room_id = candidate_room_id
	walk_rect = layout.get(
		"walk", Rect2(170.0, 405.0, 940.0, 265.0)) as Rect2
	root = Node2D.new()
	root.name = "CastleWetRoom2D_%s" % room_id
	root.z_index = 10
	root.set_meta("water_trial_room", room_id)
	root.set_meta("final_medium", "canvas_2d")
	root.set_meta("water_contract", "DL-WTR")
	stage.add_child(root)
	_build_background(background_specs)
	_build_fixtures(fixture_specs)
	_build_actor(player_texture)
	_build_foreground(foreground_specs)
	fx = WATER_FX.new() as WaterFx2D
	fx.name = "WaterEvents2D"
	fx.z_index = 36
	root.add_child(fx)
	medium = WATER_MEDIUM.new() as RefCounted
	center_player(false)
	m.g["castle_wet_room_2d"] = room_id
	m.g["castle_wet_room_2d_stats"] = stats()
	return true


func close() -> void:
	if _movement_tween != null and _movement_tween.is_valid():
		_movement_tween.kill()
	_movement_tween = null
	if fx != null and is_instance_valid(fx):
		fx.clear_events()
	if root != null and is_instance_valid(root):
		root.queue_free()
	root = null
	actor = null
	actor_submerged = null
	actor_shadow = null
	actor_front_water = null
	actor_waterline = null
	fx = null
	medium = null
	fixture_sprites.clear()
	fixture_water.clear()
	room_id = ""
	m.g.erase("castle_wet_room_2d")
	m.g.erase("castle_wet_room_2d_stats")


func fixture_sprite(item_id: String) -> Sprite2D:
	return fixture_sprites.get(item_id) as Sprite2D


func apply_fixture_frame(item_id: String, timeline_step: int,
		timeline_count: int, atlas_frame: int) -> bool:
	var sprite: Sprite2D = fixture_sprites.get(item_id) as Sprite2D
	if sprite == null or not is_instance_valid(sprite):
		return false
	sprite.frame = clampi(atlas_frame, 0,
		maxi(1, sprite.hframes * sprite.vframes) - 1)
	var water: CastleWaterFixture2D = fixture_water.get(
		item_id) as CastleWaterFixture2D
	if water != null and is_instance_valid(water):
		water.apply_timeline(timeline_step, timeline_count, atlas_frame)
	return true


func move_player(stage_position: Vector2) -> void:
	if actor == null:
		return
	var target := Vector2(
		clampf(stage_position.x, walk_rect.position.x, walk_rect.end.x),
		clampf(stage_position.y, walk_rect.position.y, walk_rect.end.y))
	var distance := _actor_foot.distance_to(target)
	if distance < 1.0:
		return
	if _movement_tween != null and _movement_tween.is_valid():
		_movement_tween.kill()
	_actor_target = target
	actor.flip_h = target.x < _actor_foot.x
	var duration := clampf(distance / 520.0, 0.12, 0.85)
	var start := _actor_foot
	_movement_tween = root.create_tween()
	_movement_tween.tween_method(_set_actor_foot, start, target, duration) \
		.set_trans(Tween.TRANS_SINE)
	_movement_tween.tween_callback(_finish_move)


func center_player(tweened: bool = false) -> void:
	var foot := Vector2(walk_rect.get_center().x, walk_rect.end.y - 20.0)
	if tweened:
		move_player(foot)
	else:
		_actor_target = foot
		_set_actor_foot(foot)
		_finish_move()


func tick(delta: float) -> void:
	if not is_active():
		return
	if fx != null:
		fx.tick(delta)
	_actor_frame_time += maxf(0.0, delta)
	var moving := _actor_velocity.length() > 0.5
	if moving and _medium_state == "SURFACE_SWIM":
		var next_frame := int(floor(_actor_frame_time * 8.0)) % 16
		if next_frame != _actor_frame:
			_actor_frame = next_frame
			_apply_actor_sheet()
	elif moving and _medium_state == "SHALLOW_WADE":
		var next_wade_frame := int(floor(_actor_frame_time * 4.0)) % 2
		if next_wade_frame != _actor_frame:
			_actor_frame = next_wade_frame
			_apply_actor_sheet()
	_update_medium(delta)
	m.g["castle_wet_room_2d_stats"] = stats()


func stats() -> Dictionary:
	var water_layer_count := 0
	var active_water_count := 0
	for value: Variant in fixture_water.values():
		var water: CastleWaterFixture2D = value as CastleWaterFixture2D
		if water == null or not is_instance_valid(water):
			continue
		var water_stats: Dictionary = water.stats()
		water_layer_count += int(water_stats.get("layer_count", 0))
		active_water_count += int(water_stats.get("active_layers", 0))
	return {
		"room": room_id,
		"canvas_only": true,
		"fixture_count": fixture_sprites.size(),
		"water_layers": water_layer_count,
		"active_water_layers": active_water_count,
		"medium_state": _medium_state,
		"fx": fx.stats() if fx != null else {},
	}


func _build_background(specs: Array[Dictionary]) -> void:
	var layer := Node2D.new()
	layer.name = "Background"
	layer.z_index = 0
	root.add_child(layer)
	for spec: Dictionary in specs:
		var texture: Texture2D = spec.get("texture") as Texture2D
		var art_rect: Rect2 = spec.get("art_rect", Rect2()) as Rect2
		if texture == null or not art_rect.has_area():
			continue
		var sprite := Sprite2D.new()
		sprite.name = String(spec.get("name", "WetRoomTile"))
		sprite.texture = texture
		sprite.centered = false
		sprite.position = art_rect.position * ART_TO_STAGE
		sprite.scale = art_rect.size * ART_TO_STAGE / texture.get_size()
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		sprite.set_meta("source_asset_role", String(spec.get(
			"source_asset_role", "source_owned_healed_background_tile")))
		sprite.set_meta("native_source_ownership_background",
			bool(spec.get("native", false)))
		layer.add_child(sprite)


func _build_fixtures(specs: Array[Dictionary]) -> void:
	var layer := Node2D.new()
	layer.name = "Fixtures"
	layer.z_index = 12
	root.add_child(layer)
	for spec: Dictionary in specs:
		var item_id := String(spec.get("id", ""))
		var texture: Texture2D = spec.get("texture") as Texture2D
		if item_id == "" or texture == null:
			continue
		var sprite := Sprite2D.new()
		sprite.name = "CanvasFixture_%s" % item_id
		sprite.texture = texture
		sprite.hframes = maxi(1, int(spec.get("hframes", 1)))
		sprite.vframes = maxi(1, int(spec.get("vframes", 1)))
		sprite.frame = clampi(int(spec.get("frame", 0)), 0,
			sprite.hframes * sprite.vframes - 1)
		sprite.position = spec.get("position", Vector2.ZERO) as Vector2
		sprite.scale = spec.get("scale", Vector2.ONE) as Vector2
		sprite.flip_h = bool(spec.get("flip_h", false))
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		sprite.set_meta("source_object_id", room_id + ":" + item_id)
		sprite.set_meta("canvas_water_trial_fixture", true)
		sprite.set_meta("fixed_pivot_animation", true)
		layer.add_child(sprite)
		fixture_sprites[item_id] = sprite
		var water_specs: Array = spec.get("water_layers", []) as Array
		if not water_specs.is_empty():
			var water := WATER_FIXTURE.new() as CastleWaterFixture2D
			water.name = "FixtureWater2D_%s" % item_id
			water.z_index = 1
			sprite.add_child(water)
			water.configure(sprite, water_specs)
			fixture_water[item_id] = water


func _build_actor(player_texture: Texture2D) -> void:
	actor_shadow = Sprite2D.new()
	actor_shadow.name = "RoshanContactShadow2D"
	actor_shadow.texture = SHADOW
	actor_shadow.modulate = Color(0.24, 0.25, 0.48, 0.48)
	actor_shadow.scale = Vector2(210.0, 38.0) / SHADOW.get_size()
	actor_shadow.z_index = 20
	root.add_child(actor_shadow)
	actor = Sprite2D.new()
	actor.name = "RoshanCanvasWaterActor"
	actor.texture = player_texture if player_texture != null else DIRECTIONAL
	actor.centered = true
	actor.z_index = 30
	actor.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	actor.set_meta("water_medium_state", "DRY")
	actor.set_meta("canvas_water_actor", true)
	root.add_child(actor)
	actor_submerged = Sprite2D.new()
	actor_submerged.name = "RoshanSubmergedCanvasSlice"
	actor_submerged.centered = true
	actor_submerged.z_index = 29
	actor_submerged.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	actor_submerged.modulate = Color(0.56, 0.90, 1.0, 0.48)
	actor_submerged.visible = false
	actor_submerged.set_meta("actor_local_water_tint", true)
	root.add_child(actor_submerged)
	actor_front_water = Polygon2D.new()
	actor_front_water.name = "ActorLocalFrontWater"
	actor_front_water.color = Color("#b8f4ff73")
	actor_front_water.z_index = 31
	actor_front_water.visible = false
	root.add_child(actor_front_water)
	actor_waterline = Line2D.new()
	actor_waterline.name = "ActorLocalWaterline"
	actor_waterline.default_color = Color("#effeff")
	actor_waterline.width = 3.0
	actor_waterline.z_index = 32
	actor_waterline.visible = false
	root.add_child(actor_waterline)


func _build_foreground(specs: Array[Dictionary]) -> void:
	var layer := Node2D.new()
	layer.name = "Foreground"
	layer.z_index = 40
	root.add_child(layer)
	for spec: Dictionary in specs:
		var texture: Texture2D = spec.get("texture") as Texture2D
		if texture == null:
			continue
		var sprite := Sprite2D.new()
		sprite.name = String(spec.get("name", "WetRoomForeground"))
		sprite.texture = texture
		sprite.centered = false
		sprite.position = (spec.get("position", Vector2.ZERO) as Vector2) \
			* ART_TO_STAGE
		sprite.scale = Vector2.ONE * ART_TO_STAGE
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		sprite.set_meta("source_asset_role", "foreground_region")
		layer.add_child(sprite)


func _set_actor_foot(foot: Vector2) -> void:
	var prior := _actor_foot
	_actor_foot = foot
	_actor_velocity = _actor_foot - prior
	var depth := inverse_lerp(walk_rect.position.y, walk_rect.end.y, foot.y)
	var depth_scale := lerpf(0.72, 1.05, depth)
	var actor_scale := PLAYER_HEIGHT / PLAYER_BASE_SIZE.y * depth_scale
	actor.scale = Vector2.ONE * actor_scale
	actor.position = Vector2(foot.x, foot.y - PLAYER_HEIGHT * depth_scale * 0.5)
	actor_shadow.position = Vector2(foot.x, foot.y - 7.0)
	actor_shadow.scale = Vector2(210.0, 38.0) / SHADOW.get_size() * depth_scale
	_update_actor_front_water()


func _finish_move() -> void:
	_actor_velocity = Vector2.ZERO
	_actor_foot = _actor_target if _actor_target != Vector2.ZERO else _actor_foot
	_apply_actor_sheet()


func _update_medium(delta: float) -> void:
	var previous := _medium_state
	if room_id != "mermaid_pool" or medium == null:
		_medium_state = "DRY"
	else:
		var actor_height := PLAYER_BASE_SIZE.y * actor.scale.y
		var column_depth := maxf(0.0, 600.0 - _actor_foot.y)
		var supported := column_depth < actor_height * 0.68
		var sample := {
			"body_height": actor_height,
			"water_column_depth": column_depth,
			"support_acquired": supported,
			"contact_inside": column_depth > 0.0,
			"face_depth": -actor_height * 0.24,
			"normal_velocity_hps": 0.0,
			"intent": WATER_MEDIUM.Intent.DEEP_TARGET \
				if _actor_target.y <= 500.0 else WATER_MEDIUM.Intent.NONE,
			"dive_contact_complete": false,
			"emerge_contact_complete": false,
		}
		var state_value := int(medium.advance(delta, sample))
		_medium_state = String(WATER_MEDIUM.state_name(state_value))
	if _medium_state != previous:
		actor.set_meta("water_medium_state", _medium_state)
		_actor_frame = 0
		_actor_frame_time = 0.0
		_apply_actor_sheet()
		if fx != null:
			if previous == "DRY" or _medium_state == "DRY":
				fx.emit_event("small", _actor_foot - Vector2(0.0, 8.0),
					"roshan_boundary")
			elif _medium_state == "SURFACE_SWIM":
				fx.emit_event("ripple", _actor_foot - Vector2(0.0, 20.0),
					"roshan_surface")
	_update_actor_front_water()


func _apply_actor_sheet() -> void:
	if actor == null or actor_submerged == null:
		return
	actor.offset = Vector2.ZERO
	actor_submerged.offset = Vector2.ZERO
	if m.skin_id != "classic":
		actor.texture = load(m.skin_sprite_path()) as Texture2D
		actor.region_enabled = false
		actor_submerged.visible = false
		_actor_source_rect = Rect2()
		return
	var swimming := _medium_state == "SURFACE_SWIM" \
		or _medium_state == "SUBMERGED"
	actor.texture = SWIM_FRONT if swimming else DIRECTIONAL
	actor_submerged.texture = actor.texture
	var sheet := "swim_front" if swimming else "directional"
	var frame_count := 16 if swimming else 8
	var safe_frame := posmod(_actor_frame, frame_count)
	_actor_source_rect = ROSHAN_FRAMES.region(sheet, safe_frame, 4)
	actor.region_enabled = true
	actor.region_rect = _actor_source_rect
	actor_submerged.region_enabled = true
	actor_submerged.region_rect = _actor_source_rect


func _update_actor_front_water() -> void:
	if actor_front_water == null or actor_waterline == null:
		return
	var visible := room_id == "mermaid_pool" and _medium_state in [
		"SHALLOW_WADE", "SURFACE_SWIM"]
	actor_front_water.visible = visible
	actor_waterline.visible = visible
	actor_submerged.visible = false
	actor_shadow.visible = not visible or _medium_state == "SHALLOW_WADE"
	if not visible:
		actor.offset = Vector2.ZERO
		if _actor_source_rect.has_area():
			actor.region_rect = _actor_source_rect
		return
	var actor_height := PLAYER_BASE_SIZE.y * actor.scale.y
	var column_ratio := clampf(
		maxf(0.0, 600.0 - _actor_foot.y) / maxf(1.0, actor_height), 0.0, 1.0)
	var cover_ratio := 0.55 if _medium_state == "SURFACE_SWIM" \
		else lerpf(0.10, 0.52, clampf(column_ratio / 0.68, 0.0, 1.0))
	var waterline_y := _actor_foot.y - actor_height * cover_ratio
	var half_width := actor_height * 0.34
	# Split Roshan at the waterline rather than covering her with a flat patch.
	# The lower slice remains readable through a soft aqua tint while the upper
	# slice stays crisp; this makes the same line read as wading or swimming.
	if m.skin_id == "classic" and _actor_source_rect.has_area():
		var actor_top := actor.position.y - actor_height * 0.5
		var visible_world_height := clampf(
			waterline_y - actor_top, 20.0, actor_height - 2.0)
		var visible_source_height := clampf(
			visible_world_height / maxf(0.001, actor.scale.y),
			2.0, _actor_source_rect.size.y - 2.0)
		var submerged_source_height := \
			_actor_source_rect.size.y - visible_source_height
		actor.region_rect = Rect2(
			_actor_source_rect.position,
			Vector2(_actor_source_rect.size.x, visible_source_height))
		actor.offset = Vector2(
			0.0, -submerged_source_height * 0.5)
		actor_submerged.texture = actor.texture
		actor_submerged.region_enabled = true
		actor_submerged.region_rect = Rect2(
			_actor_source_rect.position \
				+ Vector2(0.0, visible_source_height),
			Vector2(_actor_source_rect.size.x, submerged_source_height))
		actor_submerged.offset = Vector2(0.0, visible_source_height * 0.5)
		actor_submerged.position = actor.position
		actor_submerged.scale = actor.scale
		actor_submerged.flip_h = actor.flip_h
		actor_submerged.visible = true
	# A slim uneven ribbon supplies contact and foam without creating a visible
	# rectangle over the painted pool. Its bottom edge stays within twelve pixels
	# of the surface, so the authored background remains the water body.
	actor_front_water.polygon = PackedVector2Array([
		Vector2(_actor_foot.x - half_width, waterline_y),
		Vector2(_actor_foot.x - half_width * 0.48, waterline_y - 2.0),
		Vector2(_actor_foot.x, waterline_y + 1.0),
		Vector2(_actor_foot.x + half_width * 0.52, waterline_y - 2.0),
		Vector2(_actor_foot.x + half_width, waterline_y),
		Vector2(_actor_foot.x + half_width * 0.88, waterline_y + 10.0),
		Vector2(_actor_foot.x, waterline_y + 8.0),
		Vector2(_actor_foot.x - half_width * 0.88, waterline_y + 11.0),
	])
	actor_waterline.points = PackedVector2Array([
		Vector2(_actor_foot.x - half_width, waterline_y),
		Vector2(_actor_foot.x, waterline_y - 2.0),
		Vector2(_actor_foot.x + half_width, waterline_y),
	])
