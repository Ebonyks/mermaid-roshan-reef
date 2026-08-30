class_name DayOneBathroomCleanup
extends Control
## Day One's first bathroom beat: a reading-free basket-to-cleaning handoff.
##
## The rescue owns the temporary Canvas2D presentation. Both child-readable
## tools are already visible in one front-right basket; the only hunt action is
## a generous tap on that basket, after which the cleaning owner demonstrates
## the sponge and brush journeys before accepting gestures.

const DAY_ONE_BATHROOM_CLEANING := preload(
	"res://scripts/games/day_one_bathroom_cleaning.gd")
const DAY_ONE_DUST_BUNNY_SWIMMER := preload(
	"res://scripts/games/day_one_dust_bunny_swimmer.gd")
const DIRTY_ROOM_TEXTURE: Texture2D = preload(
	"res://assets/flats/castle/rooms/room_bubble_bath_dirty_day_one.png")
const DIRTY_ROOM_DRAINED_TEXTURE: Texture2D = preload(
	"res://assets/flats/castle/rooms/room_bubble_bath_dirty_drained_day_one.png")

signal supply_found(index: int, supply_id: String)
signal supply_hunt_completed
signal cleanup_step_completed(step: int, cleanup_id: String)
signal finale_started
signal cleanup_completed

const SPARKLE_TEXTURE := "res://assets/opera/worlds/props/fx_stolen_sparkle.png"
const POINTER_TEXTURE := "res://assets/castle/training/ghost_hand.png"
const SPONGE_TEXTURE := "res://assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png"
const BRUSH_TEXTURE := "res://assets/castle/day_one_art_studio/magic_cleaning_brush.png"
const BASKET_TOOL_SCALE := 0.07
# Reuse the approved Day One cleanup basket as the single, diegetic collection
# point. It is deliberately placed on the front-right floor, clear of the
# lower-right action control, so a child can see where each found tool goes
# without a second card or floating box.
const BASKET_TEXTURE := "res://assets/castle/day_one_pool/activities/cleanup_basket.png"
const BASKET_POSITION := Vector2(940.0, 575.0)
const BASKET_SCALE := 0.105
const BASKET_BUTTON_SIZE := Vector2(220.0, 220.0)
const BASKET_POINTER_OFFSET := Vector2(0.0, -132.0)
# The approved Roshan staging footprint occupies the center-right lesson area;
# this narrow pointer corridor keeps the hand above the basket and out of her
# face, hair, tail, and the sink/tub fixtures.
const ROSHAN_SAFE_RECT := Rect2(700.0, 320.0, 185.0, 320.0)
const POINTER_BOUNDS := Vector2(56.0, 88.0)
const BASKET_CONTENT_OFFSETS: Array[Vector2] = [Vector2(-34.0, -26.0),
	Vector2(36.0, -24.0)]
const SINK_GRIME_TEXTURE := "res://assets/castle/dirty_cleanup_2d/targets/target_sink_grime_v1.png"
const TUB_GRIME_TEXTURE := "res://assets/castle/dirty_cleanup_2d/targets/target_tub_grime_v1.png"
const SINK_GRIME_POSITION := Vector2(642.0, 280.0)
const TUB_GRIME_POSITION := Vector2(270.0, 292.0)
# These are localized fixture marks, not full fixture cards. The approved
# source cards are 1024px square and are intentionally mounted small enough to
# sit inside the painted basin/rim on a 1280x720 phone canvas.
const SINK_GRIME_SCALE := 0.095
const TUB_GRIME_SCALE := 0.10
const SUPPLY_DEFINITIONS: Array[Dictionary] = [
	{
		"id": "sponge",
	},
	{
		"id": "brush",
	},
]
const MAX_SUPPLIES := 2
const DRAG_TARGET_SIZE := Vector2(184.0, 184.0)
const MIN_DRAG_DISTANCE := 36.0
const WORLD_CONTROL_BLOCK_REASON := "day_one_bathroom_cleanup"

var m: ReefMain
var _supply_step: int = 0
var _found: Array[bool] = [false, false]
var _supply_nodes: Array[Node2D] = []
var _sparkle_nodes: Array[Sprite2D] = []
var _basket: Sprite2D = null
var _basket_base_scale: Vector2 = Vector2.ONE
var _basket_button: Button = null
var _sink_grime: Sprite2D = null
var _tub_grime: Sprite2D = null
var _dirty_room_plate: Sprite2D = null
var _drained_room_plate: Sprite2D = null
var _bath_bunny: DayOneDustBunnySwimmer = null
var _clean_room_revealed := false
var _room_background: Sprite2D = null
var _room_background_was_visible := false
var _room_tiles: Array[Sprite2D] = []
var _room_tile_visibility: Array[bool] = []
var _room_visual_layers: Array[CanvasItem] = []
var _room_visual_layer_visibility: Array[bool] = []
var _pointer: Sprite2D = null
var _dragging: bool = false
var _drag_last: Vector2 = Vector2.ZERO
var _drag_distance: float = 0.0
var _busy: bool = false
var _hunt_completed: bool = false
var _handoff_ready: bool = false
var _cleaning_stage: DayOneBathroomCleaning = null
var _announcements_enabled: bool = true
var _pulse_time: float = 0.0
var _hotspot_layer: Control = null
var _hotspot_layer_was_visible: bool = false
var _door_hotspot_layer: Control = null
var _door_hotspot_layer_was_visible: bool = false
var _room_link_layer: Control = null
var _room_link_layer_was_visible: bool = false
var _hud_layer: CanvasLayer = null
var _hud_layer_was_visible: bool = false
var _action_button: Button = null
var _action_button_was_visible: bool = false
var _world_controls_suppressed: bool = false


class SupplyIcon extends Sprite2D:
	var supply_kind: String = "sponge"

	func configure(kind: String) -> void:
		supply_kind = kind
		texture = load(SPONGE_TEXTURE if kind == "sponge" else BRUSH_TEXTURE) \
			as Texture2D


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	name = "DayOneBathroomCleanup"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 22
	_suspend_standard_surfaces()
	_suspend_room_hotspots()
	_suspend_clean_room_visuals()
	_build_dirty_room_plate()
	_build_bath_bunny()
	_build_dirty_overlays()
	_build_basket()
	_build_supply_icons()
	_build_guidance()
	_supply_step = clampi(m.day_one_bathroom_supply_hunt_step, 0, MAX_SUPPLIES)
	_apply_restored_progress()
	set_process(true)
	if _supply_step >= MAX_SUPPLIES:
		_complete_supply_hunt()
	else:
		call_deferred("_announce_current_supply")


func teardown() -> void:
	set_process(false)
	_restore_clean_room_visuals()
	_clear_bath_bunny()
	_clear_dirty_room_plate(false)
	if _cleaning_stage != null and is_instance_valid(_cleaning_stage):
		_cleaning_stage.teardown()
	_cleaning_stage = null
	if _hotspot_layer != null and is_instance_valid(_hotspot_layer):
		_hotspot_layer.visible = _hotspot_layer_was_visible
		_hotspot_layer = null
	if _door_hotspot_layer != null and is_instance_valid(_door_hotspot_layer):
		_door_hotspot_layer.visible = _door_hotspot_layer_was_visible
		_door_hotspot_layer = null
	if _room_link_layer != null and is_instance_valid(_room_link_layer):
		_room_link_layer.visible = _room_link_layer_was_visible
		_room_link_layer = null
	if _hud_layer != null and is_instance_valid(_hud_layer):
		_hud_layer.visible = _hud_layer_was_visible
		_hud_layer = null
	if _action_button != null and is_instance_valid(_action_button):
		_action_button.visible = _action_button_was_visible
		_action_button = null
	if _world_controls_suppressed and m != null \
			and m.has_method("_set_world_controls_enabled"):
		# Removing our named block preserves any unrelated block that was already
		# active, while restoring TouchUI when rescue was the only owner.
		m._set_world_controls_enabled(true, WORLD_CONTROL_BLOCK_REASON)
		_world_controls_suppressed = false
	if is_inside_tree():
		queue_free()
	else:
		free()


func audit_snapshot() -> Dictionary:
	var found_count: int = 0
	for found: bool in _found:
		if found:
			found_count += 1
	return {
		"supply_count": MAX_SUPPLIES,
		"found_count": found_count,
		"current_supply_step": _supply_step,
		"active_target_count": 1 if not _hunt_completed else 0,
		"minimum_touch_side": DRAG_TARGET_SIZE.x,
		"drag_target_size": DRAG_TARGET_SIZE,
		"minimum_drag_distance": MIN_DRAG_DISTANCE,
		"guidance_discloses_target": true,
		"magnifier_following_drag": false,
		"voice_guidance_configured": true,
		"announcements_enabled": _announcements_enabled,
		"has_visual_pointer": _pointer != null and _pointer.visible,
		"interaction_mode": "tap_basket_then_clean",
		"basket_tap_required": not _hunt_completed,
		"auto_started_dirty_room": _dirty_overlays_visible(),
		"dirty_room_plate_visible": _dirty_room_plate != null
			and is_instance_valid(_dirty_room_plate)
			and _dirty_room_plate.visible,
		"clean_room_revealed": _clean_room_revealed,
		"tub_drained": m != null and m.day_one_bathroom_tub_drained,
		"bath_bunny": _bath_bunny.audit_snapshot()
			if _bath_bunny != null and is_instance_valid(_bath_bunny) else {},
		"basket_visible": _basket != null and _basket.visible,
		"basket_pulsing": _basket != null and _basket.get_meta(
			"pulsing", false),
		"basket_position": _basket.position if _basket != null else Vector2.ZERO,
		"basket_collects_supplies": _basket != null and _basket.get_meta(
			"collects_supplies", false),
		"found_tools_visible_in_basket": _found_tools_visible_in_basket(),
		"normal_hud_suppressed": _hud_layer == null or not _hud_layer.visible,
		"room_hotspots_suppressed": _hotspots_suppressed(),
		"room_links_suppressed": _room_link_layer == null
			or not _room_link_layer.visible,
		"room_action_suppressed": _action_button == null
			or not _action_button.visible,
		"world_controls_suppressed": _world_controls_suppressed,
		"basket_clear_of_action_zone": _basket_button == null
			or _basket_button.position.x + _basket_button.size.x <= 1066.0,
		"pointer_position": _pointer.position if _pointer != null else Vector2.ZERO,
		"pointer_aimed_at_basket": _pointer != null
			and _pointer.position.distance_to(BASKET_POSITION) <= 150.0,
		"pointer_clear_of_roshan": _pointer != null
			and not _pointer_bounds().intersects(ROSHAN_SAFE_RECT),
		"localized_fixture_grime": SINK_GRIME_SCALE <= 0.12
			and TUB_GRIME_SCALE <= 0.12,
		"floating_sink_box_suppressed": true,
		"dirty_overlays_visible": _dirty_overlays_visible(),
		"sink_grime_visible": _sink_grime != null and _sink_grime.visible,
		"tub_grime_visible": _tub_grime != null and _tub_grime.visible,
		"cabinet_target_count": 0,
		"cabinet_search_active": false,
		"basket_item_ids": _basket_item_ids(),
		"basket_tap_prompt_voice": not _hunt_completed,
		"basket_tap_prompt_visual": _pointer != null and _pointer.visible,
		"basket_tap_count": int(get_meta("basket_tap_count", 0)),
		"basket_tap_voice_sent": bool(get_meta("basket_tap_voice_sent", false)),
		"basket_tap_pointer_visible": _pointer != null and _pointer.visible,
		"sponge_travel_complete": _cleaning_stage != null
			and bool(_cleaning_stage.audit_snapshot().get(
				"sponge_travel_complete", false)),
		"sink_circle_demo_visible": _cleaning_stage != null
			and bool(_cleaning_stage.audit_snapshot().get(
				"circle_demo_visible", false)),
		"brush_travel_complete": _cleaning_stage != null
			and bool(_cleaning_stage.audit_snapshot().get(
				"brush_travel_complete", false)),
		"whole_room_sparkle": _cleaning_stage != null
			and bool(_cleaning_stage.audit_snapshot().get(
				"whole_room_sparkle", false)),
		"supply_hunt_completed": _hunt_completed,
		"handoff_ready": _handoff_ready,
		"canvas_only": _all_canvas_children(self),
	}


func is_supply_hunt_complete() -> bool:
	return _hunt_completed


func is_handoff_ready() -> bool:
	return _handoff_ready


## Stable seam for the later sink/tub gesture owner. This method intentionally
## does not complete the room; it only acknowledges that both supplies exist.
func begin_cleaning_handoff() -> bool:
	if not _hunt_completed:
		return false
	_handoff_ready = true
	if _cleaning_stage == null or not is_instance_valid(_cleaning_stage):
		_cleaning_stage = DAY_ONE_BATHROOM_CLEANING.new() \
			as DayOneBathroomCleaning
		_cleaning_stage.cleanup_step_completed.connect(
			_on_cleaning_step_completed)
		_cleaning_stage.tub_drain_visual_started.connect(
			_on_tub_drain_visual_started)
		_cleaning_stage.finale_started.connect(_on_cleaning_finale_started)
		_cleaning_stage.cleanup_completed.connect(_on_cleaning_completed)
		add_child(_cleaning_stage)
		_cleaning_stage.setup(m, _announcements_enabled)
		_cleaning_stage.set_supply_basket(BASKET_POSITION)
		_cleaning_stage.set_dirty_overlays(_sink_grime, _tub_grime)
		_cleaning_stage.set_bunny_swimmer(_bath_bunny)
	return true


func cleaning_audit_snapshot() -> Dictionary:
	if _cleaning_stage == null or not is_instance_valid(_cleaning_stage):
		return {"active": false, "handoff_ready": _handoff_ready}
	var snapshot: Dictionary = _cleaning_stage.audit_snapshot()
	snapshot["active"] = true
	snapshot["handoff_ready"] = _handoff_ready
	return snapshot


func probe_cleaning_sink_circle(points: Array[Vector2]) -> bool:
	return _cleaning_stage != null and is_instance_valid(_cleaning_stage) \
		and _cleaning_stage.probe_sink_circle(points)


func probe_cleaning_tub_strokes(points: Array[Vector2]) -> bool:
	return _cleaning_stage != null and is_instance_valid(_cleaning_stage) \
		and _cleaning_stage.probe_tub_strokes(points)


func probe_tap_tub() -> bool:
	return _cleaning_stage != null and is_instance_valid(_cleaning_stage) \
		and _cleaning_stage.probe_tap_tub()


func probe_begin_drag(at: Vector2) -> bool:
	# Kept as a compatibility seam for old callers. The playable rescue has no
	# magnifier or drag surface; one finger always taps the basket instead.
	return false


func probe_drag_to(at: Vector2) -> bool:
	return false


func probe_end_drag() -> void:
	_dragging = false


func probe_reveal_supply(index: int) -> bool:
	return probe_tap_basket()


func probe_tap_basket() -> bool:
	if _hunt_completed or _busy:
		return false
	_on_basket_tapped()
	return _hunt_completed


func _process(delta: float) -> void:
	_pulse_time += maxf(delta, 0.0)
	if _basket != null and is_instance_valid(_basket) and _basket.visible:
		var pulse: float = 1.0 + sin(_pulse_time * 3.6) * 0.045
		_basket.scale = _basket_base_scale * pulse
	if _pointer != null and is_instance_valid(_pointer) and _pointer.visible:
		_pointer.rotation = sin(_pulse_time * 2.6) * 0.04


func _suspend_room_hotspots() -> void:
	_hotspot_layer = m.castle_room_item_hotspot_layer
	if _hotspot_layer != null and is_instance_valid(_hotspot_layer):
		_hotspot_layer_was_visible = _hotspot_layer.visible
		_hotspot_layer.visible = false
	else:
		_hotspot_layer = null
	_door_hotspot_layer = m.castle_room_door_hotspot_layer
	if _door_hotspot_layer != null and is_instance_valid(_door_hotspot_layer):
		_door_hotspot_layer_was_visible = _door_hotspot_layer.visible
		_door_hotspot_layer.visible = false
	_room_link_layer = m.castle_room_link_layer
	if _room_link_layer != null and is_instance_valid(_room_link_layer):
		_room_link_layer_was_visible = _room_link_layer.visible
		_room_link_layer.visible = false


func _suspend_clean_room_visuals() -> void:
	_room_background = m.castle_room_background
	if _room_background != null and is_instance_valid(_room_background):
		_room_background_was_visible = _room_background.visible
		_room_background.visible = false
	else:
		_room_background = null
	_room_tiles.clear()
	_room_tile_visibility.clear()
	for tile: Sprite2D in m.castle_room_detail_tiles:
		if tile != null and is_instance_valid(tile):
			_room_tiles.append(tile)
			_room_tile_visibility.append(tile.visible)
			tile.visible = false
	_room_visual_layers = [
		m.castle_room_item_visual_layer,
		m.castle_room_mid_layer,
		m.castle_room_front_layer,
		m.castle_room_item_effect_layer,
	]
	_room_visual_layer_visibility.clear()
	for layer: CanvasItem in _room_visual_layers:
		var was_visible: bool = layer != null and is_instance_valid(layer) \
			and layer.visible
		_room_visual_layer_visibility.append(was_visible)
		if layer != null and is_instance_valid(layer):
			layer.visible = false


func _restore_clean_room_visuals() -> void:
	if _clean_room_revealed:
		return
	_clean_room_revealed = true
	if _room_background != null and is_instance_valid(_room_background):
		_room_background.visible = _room_background_was_visible
	for index: int in range(_room_tiles.size()):
		var tile: Sprite2D = _room_tiles[index]
		if tile != null and is_instance_valid(tile):
			tile.visible = _room_tile_visibility[index]
	for index: int in range(_room_visual_layers.size()):
		var layer: CanvasItem = _room_visual_layers[index]
		if layer != null and is_instance_valid(layer):
			layer.visible = _room_visual_layer_visibility[index]


func _build_dirty_room_plate() -> void:
	_dirty_room_plate = Sprite2D.new()
	_dirty_room_plate.name = "DayOneDirtyBathroomPlate"
	_dirty_room_plate.texture = DIRTY_ROOM_DRAINED_TEXTURE \
		if m.day_one_bathroom_tub_drained else DIRTY_ROOM_TEXTURE
	_dirty_room_plate.position = StorybookUI.CANVAS_SIZE * 0.5
	_dirty_room_plate.scale = Vector2.ONE * 1.25
	# The castle world root sits below Control chrome. Mount the plate there at
	# the painter seam between fixed fixtures (z 55) and Roshan (z >= 125), so
	# the clean fixtures are covered but Roshan and her shadow stay visible.
	_dirty_room_plate.z_index = 100
	_dirty_room_plate.set_meta(
		"source_asset_role", "day_one_dirty_bathroom_full_plate")
	_dirty_room_plate.set_meta("true_2d", true)
	_dirty_room_plate.set_meta("contains_tub_swimmer", false)
	_dirty_room_plate.set_meta("separate_animated_bunny", true)
	_dirty_room_plate.set_meta("tub_drained", m.day_one_bathroom_tub_drained)
	if m.castle_room_world_root != null:
		m.castle_room_world_root.add_child(_dirty_room_plate)
	else:
		_dirty_room_plate.z_index = 1
		add_child(_dirty_room_plate)


func _build_bath_bunny() -> void:
	if m.day_one_bathroom_tub_drained:
		return
	_bath_bunny = DAY_ONE_DUST_BUNNY_SWIMMER.new() \
		as DayOneDustBunnySwimmer
	var owner: Node = m.castle_room_world_root \
		if m.castle_room_world_root != null else self
	owner.add_child(_bath_bunny)
	_bath_bunny.set_meta("day_one_dirty_bathtub_swimmer", true)
	if not _bath_bunny.setup(Rect2(210.0, 238.0, 210.0, 100.0),
			Vector2(300.0, 286.0), 92.0, Vector2(13.0, 3.0), 110,
			Vector2(78.0, 16.0), Color(0.72, 0.78, 0.48, 0.26), 0.70):
		_bath_bunny.queue_free()
		_bath_bunny = null


func _clear_bath_bunny() -> void:
	if _bath_bunny != null and is_instance_valid(_bath_bunny):
		_bath_bunny.queue_free()
	_bath_bunny = null


func _on_tub_drain_visual_started() -> void:
	if _bath_bunny != null and is_instance_valid(_bath_bunny):
		_bath_bunny.fade_out(0.28)
	_reveal_drained_room_plate()


func _reveal_drained_room_plate() -> void:
	if _dirty_room_plate == null or not is_instance_valid(_dirty_room_plate) \
			or bool(_dirty_room_plate.get_meta("tub_drained", false)):
		return
	var filled_plate: Sprite2D = _dirty_room_plate
	var drained_plate := Sprite2D.new()
	drained_plate.name = "DayOneDrainedDirtyBathroomPlate"
	drained_plate.texture = DIRTY_ROOM_DRAINED_TEXTURE
	drained_plate.position = filled_plate.position
	drained_plate.scale = filled_plate.scale
	drained_plate.z_index = filled_plate.z_index + 1
	drained_plate.modulate.a = 0.0
	drained_plate.set_meta("source_asset_role",
		"day_one_dirty_bathroom_drained_plate")
	drained_plate.set_meta("true_2d", true)
	drained_plate.set_meta("tub_drained", true)
	filled_plate.get_parent().add_child(drained_plate)
	_drained_room_plate = drained_plate
	var drain: Tween = drained_plate.create_tween()
	drain.tween_property(drained_plate, "modulate:a", 1.0, 0.34) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	drain.tween_callback(_finish_drained_room_reveal.bind(
		filled_plate, drained_plate))


func _finish_drained_room_reveal(filled_plate: Sprite2D,
		drained_plate: Sprite2D) -> void:
	if filled_plate != null and is_instance_valid(filled_plate):
		filled_plate.queue_free()
	_dirty_room_plate = drained_plate
	_drained_room_plate = null


func reveal_clean_room() -> void:
	# The dirty plate is a complete alternate room image. Hide it before the
	# clean fixture layers return so the bathtub/sink/toilet are never drawn
	# twice during the reveal. The pearl ring and fixture sparkles provide the
	# visible transition without full-frame transparent overdraw.
	_clear_dirty_room_plate(false)
	_restore_clean_room_visuals()


func _clear_dirty_room_plate(animated: bool) -> void:
	if _drained_room_plate != null and is_instance_valid(_drained_room_plate) \
			and _drained_room_plate != _dirty_room_plate:
		_drained_room_plate.queue_free()
	_drained_room_plate = null
	if _dirty_room_plate == null or not is_instance_valid(_dirty_room_plate):
		_dirty_room_plate = null
		return
	var plate: Sprite2D = _dirty_room_plate
	_dirty_room_plate = null
	if animated and plate.is_inside_tree():
		var reveal: Tween = plate.create_tween()
		reveal.tween_property(plate, "modulate:a", 0.0, 0.34) \
			.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		reveal.tween_callback(plate.queue_free)
	else:
		plate.visible = false
		plate.queue_free()


func day_one_bathroom_plate_snapshot() -> Dictionary:
	var visible: bool = _dirty_room_plate != null \
		and is_instance_valid(_dirty_room_plate) \
		and _dirty_room_plate.visible
	var texture_size := Vector2i.ZERO
	if visible and _dirty_room_plate.texture != null:
		texture_size = Vector2i(_dirty_room_plate.texture.get_width(),
			_dirty_room_plate.texture.get_height())
	return {
		"dirty_plate_visible": visible,
		"true_2d": visible and _dirty_room_plate is Sprite2D,
		"contains_tub_swimmer": visible and bool(
			_dirty_room_plate.get_meta("contains_tub_swimmer", false)),
		"separate_animated_bunny": visible and bool(
			_dirty_room_plate.get_meta("separate_animated_bunny", false)),
		"bunny_depth_occluded": _bath_bunny != null \
			and is_instance_valid(_bath_bunny) \
			and bool(_bath_bunny.audit_snapshot().get(
				"submerged_lower_body", false)),
		"tub_drained": visible and bool(
			_dirty_room_plate.get_meta("tub_drained", false)),
		"clean_fixture_pixels_occluded": visible
			and _dirty_room_plate.z_index == 100,
		"clean_fixture_layer_visible":
			m.castle_room_item_visual_layer != null
			and m.castle_room_item_visual_layer.visible,
		"texture_size": texture_size,
	}


func _suspend_standard_surfaces() -> void:
	# The room rescue owns the whole child-facing presentation. Keep voice/audio
	# alive, but remove status trays, ordinary objective cards, and captions from
	# this layer so the basket is the only hunt invitation.
	_hud_layer = m.hud_layer
	if _hud_layer != null and is_instance_valid(_hud_layer):
		_hud_layer_was_visible = _hud_layer.visible
		_hud_layer.visible = false
	_action_button = m.castle_room_action_button
	if _action_button != null and is_instance_valid(_action_button):
		_action_button_was_visible = _action_button.visible
		_action_button.visible = false
	if m.has_method("_set_world_controls_enabled"):
		m._set_world_controls_enabled(false, WORLD_CONTROL_BLOCK_REASON)
		_world_controls_suppressed = true


func _build_basket() -> void:
	_basket = Sprite2D.new()
	_basket.name = "FrontRightCleanupBasket"
	_basket.texture = load(BASKET_TEXTURE) as Texture2D
	_basket.position = BASKET_POSITION
	_basket.scale = Vector2.ONE * BASKET_SCALE
	_basket_base_scale = _basket.scale
	_basket.z_index = 27
	_basket.set_meta("pulsing", true)
	_basket.set_meta("collects_supplies", true)
	_basket.set_meta("front_right_collection_point", true)
	add_child(_basket)


func _build_dirty_overlays() -> void:
	_sink_grime = _make_dirty_overlay("BathroomSinkGrime", SINK_GRIME_TEXTURE,
		SINK_GRIME_POSITION, SINK_GRIME_SCALE)
	_tub_grime = _make_dirty_overlay("BathroomTubGrime", TUB_GRIME_TEXTURE,
		TUB_GRIME_POSITION, TUB_GRIME_SCALE)


func _make_dirty_overlay(node_name: String, texture_path: String, at: Vector2,
		scale_factor: float) -> Sprite2D:
	var overlay := Sprite2D.new()
	overlay.name = node_name
	overlay.texture = load(texture_path) as Texture2D
	overlay.position = at
	overlay.scale = Vector2.ONE * scale_factor
	overlay.modulate = Color(1.0, 1.0, 1.0, 0.86)
	overlay.z_index = 24
	overlay.set_meta("bathroom_dirty_overlay", true)
	overlay.set_meta("floating_sink_box", false)
	add_child(overlay)
	return overlay


func _build_supply_icons() -> void:
	for index: int in range(MAX_SUPPLIES):
		var icon := SupplyIcon.new()
		icon.name = "BasketTool_%s" % String(SUPPLY_DEFINITIONS[index]["id"])
		icon.configure(String(SUPPLY_DEFINITIONS[index]["id"]))
		icon.position = _basket_content_position(index)
		icon.z_index = 29
		icon.visible = true
		icon.set_meta("collection_role", "basket_tool")
		icon.set_meta("visible_in_basket", false)
		add_child(icon)
		_supply_nodes.append(icon)
		_found[index] = false


func _build_guidance() -> void:
	_pointer = Sprite2D.new()
	_pointer.name = "BasketPointer"
	_pointer.texture = load(POINTER_TEXTURE) as Texture2D
	_pointer.scale = Vector2.ONE * 0.18
	_pointer.z_index = 34
	add_child(_pointer)
	_basket_button = Button.new()
	_basket_button.name = "TapCleanupBasket"
	_basket_button.flat = true
	_basket_button.focus_mode = Control.FOCUS_NONE
	_basket_button.position = BASKET_POSITION - BASKET_BUTTON_SIZE * 0.5
	_basket_button.size = BASKET_BUTTON_SIZE
	_basket_button.modulate = Color(1.0, 1.0, 1.0, 0.0)
	_basket_button.z_index = 35
	_basket_button.set_meta("one_finger_tap", true)
	_basket_button.set_meta("physical_object", true)
	_basket_button.pressed.connect(_on_basket_tapped)
	add_child(_basket_button)


func _apply_restored_progress() -> void:
	for index: int in range(MAX_SUPPLIES):
		# The new rescue starts with both child-readable tools already sitting in
		# the one basket; tapping it is the only hunt action.
		_found[index] = true
		_place_supply_in_basket(index)
	_refresh_guidance()


func _refresh_guidance() -> void:
	var visible: bool = not _hunt_completed
	if _pointer != null:
		_pointer.visible = visible
	if _basket_button != null:
		_basket_button.visible = visible
	if not visible:
		return
	_pointer.position = BASKET_POSITION + BASKET_POINTER_OFFSET


func _reveal_supply(index: int) -> void:
	# Obsolete cabinet/magnifier route: the basket is the only playable target.
	# Keep the method name so older save/probe callers fail closed safely.
	return


func _finish_supply_reveal(index: int) -> void:
	_place_supply_in_basket(index)
	_busy = false
	if _supply_step >= MAX_SUPPLIES:
		_complete_supply_hunt()
	else:
		_refresh_guidance()
		_announce_current_supply()


func _complete_supply_hunt() -> void:
	if _hunt_completed:
		return
	_hunt_completed = true
	_handoff_ready = true
	_busy = false
	_dragging = false
	_refresh_guidance()
	supply_hunt_completed.emit()
	if _announcements_enabled and m != null:
		m.show_msg("Roshan", "We found both cleaning supplies!", "win")
		m._say("roshan", "win", 0.6)
	begin_cleaning_handoff()


func _on_basket_tapped() -> void:
	if _hunt_completed or _busy:
		return
	_busy = true
	set_meta("basket_tap_count", int(get_meta("basket_tap_count", 0)) + 1)
	set_meta("basket_tap_voice_sent", _announcements_enabled and m != null)
	if _announcements_enabled and m != null:
		m._ui_tap()
		m.show_msg("Roshan", "Let’s clean together!", "talk")
		m._say("roshan", "talk", 0.4)
	for index: int in range(MAX_SUPPLIES):
		_found[index] = true
		_place_supply_in_basket(index)
		supply_found.emit(index, String(SUPPLY_DEFINITIONS[index]["id"]))
	_supply_step = MAX_SUPPLIES
	if m != null:
		m.day_one_record_bathroom_supply_step(_supply_step)
	_complete_supply_hunt()


func _announce_current_supply() -> void:
	if not _announcements_enabled or m == null or _hunt_completed:
		return
	m.show_msg("Roshan", "Tap the cleaning basket.", "talk")
	m._say("roshan", "talk", 0.8)


func _spawn_sparkle(center: Vector2) -> void:
	var texture: Texture2D = load(SPARKLE_TEXTURE) as Texture2D
	if texture == null:
		return
	var sparkle := Sprite2D.new()
	sparkle.name = "SupplySparkle"
	sparkle.texture = texture
	sparkle.position = center
	sparkle.scale = Vector2.ONE * 0.42
	sparkle.z_index = 40
	add_child(sparkle)
	_sparkle_nodes.append(sparkle)
	var tween: Tween = sparkle.create_tween().set_parallel(true)
	tween.tween_property(sparkle, "scale", Vector2.ONE * 0.82, 0.42)
	tween.tween_property(sparkle, "rotation", 0.35, 0.42)
	tween.tween_property(sparkle, "modulate:a", 0.0, 0.42)
	tween.chain().tween_callback(sparkle.queue_free)


func _all_canvas_children(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem or not _all_canvas_children(child):
			return false
	return true


func _basket_content_position(index: int) -> Vector2:
	return BASKET_POSITION + BASKET_CONTENT_OFFSETS[clampi(index, 0,
		BASKET_CONTENT_OFFSETS.size() - 1)]


func _basket_item_ids() -> Array[String]:
	var ids: Array[String] = []
	for definition: Dictionary in SUPPLY_DEFINITIONS:
		ids.append(String(definition["id"]))
	return ids


func _pointer_bounds() -> Rect2:
	if _pointer == null:
		return Rect2()
	return Rect2(_pointer.position - POINTER_BOUNDS * 0.5, POINTER_BOUNDS)


func _place_supply_in_basket(index: int) -> void:
	if index < 0 or index >= _supply_nodes.size():
		return
	var supply: Node2D = _supply_nodes[index]
	supply.visible = true
	supply.position = _basket_content_position(index)
	supply.scale = Vector2.ONE * BASKET_TOOL_SCALE
	supply.rotation = -0.08 if index == 0 else 0.08
	supply.modulate.a = 1.0
	supply.set_meta("visible_in_basket", true)


func _found_tools_visible_in_basket() -> bool:
	for index: int in range(_found.size()):
		if _found[index] and (not _supply_nodes[index].visible
				or not bool(_supply_nodes[index].get_meta(
					"visible_in_basket", false))):
			return false
	return true


func _hotspots_suppressed() -> bool:
	return (_hotspot_layer == null or not _hotspot_layer.visible) \
		and (_door_hotspot_layer == null or not _door_hotspot_layer.visible) \
		and (_room_link_layer == null or not _room_link_layer.visible)


func _dirty_overlays_visible() -> bool:
	return _sink_grime != null and _sink_grime.visible \
		and _tub_grime != null and _tub_grime.visible


func _on_cleaning_step_completed(step: int, cleanup_id: String) -> void:
	cleanup_step_completed.emit(step, cleanup_id)


func _on_cleaning_finale_started() -> void:
	finale_started.emit()


func _on_cleaning_completed() -> void:
	cleanup_completed.emit()
