class_name DayOnePoolCleanup
extends Control
## Four-part, one-finger cleanup for Day One's Mermaid Pool.
##
## Persistent progress stays on ReefMain. This node owns only the temporary
## Canvas2D presentation, touch targets, and reveal animation for the live room.

signal cleanup_step_completed(step: int, cleanup_id: String)
signal finale_started
signal reveal_completed

const ASSET_ROOT := "res://assets/castle/day_one_pool/"
const CLEANUP_STEPS: Array[Dictionary] = [
	{
		"id": "pool_surface",
		"texture": ASSET_ROOT + "pool_algae_trash.png",
		"center": Vector2(620.0, 385.0),
		"max_size": Vector2(520.0, 235.0),
		"hit_size": Vector2(555.0, 265.0),
	},
	{
		"id": "rainbow_fountain",
		"texture": ASSET_ROOT + "waterfall_growth.png",
		"center": Vector2(372.0, 206.0),
		"max_size": Vector2(230.0, 280.0),
		"hit_size": Vector2(250.0, 300.0),
	},
	{
		"id": "pool_rim",
		"texture": ASSET_ROOT + "pool_rim_grime.png",
		"center": Vector2(880.0, 540.0),
		"max_size": Vector2(385.0, 155.0),
		"hit_size": Vector2(420.0, 185.0),
	},
	{
		"id": "seahorse",
		"texture": ASSET_ROOT + "seahorse_sick.png",
		"center": Vector2(918.0, 244.0),
		"max_size": Vector2(245.0, 345.0),
		"hit_size": Vector2(285.0, 375.0),
	},
]
const RUMI_POOL_ATLAS := \
	"res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png"
const RUMI_POSE_ATLAS := \
	"res://assets/characters/rumi/rumi_eight_pose_runtime.png"
const RUMI_POOL_CELL_SIZE := Vector2(256.0, 256.0)
const RUMI_POSE_CELL_SIZE := Vector2(256.0, 384.0)
const RUMI_SWIM_SCALE := 1.02
const RUMI_UPRIGHT_START_SCALE := 0.83
const RUMI_UPRIGHT_SCALE := 0.96
const DINGY_WASH := Color(0.18, 0.20, 0.11, 0.36)
const CLEAN_SPARKLE_COLORS: Array[Color] = [
	Color(0.48, 0.96, 0.94),
	Color(1.0, 0.83, 0.38),
	Color(0.88, 0.70, 1.0),
	Color(1.0, 0.68, 0.82),
]

var m: ReefMain
var _step: int = 0
var _busy: bool = false
var _finale_started: bool = false
var _announcements_enabled: bool = true
var _pulse_time: float = 0.0
var _step_sprites: Array[Sprite2D] = []
var _step_buttons: Array[Button] = []
var _light_wash: ColorRect = null
var _pointer: Label = null
var _rumi: AnimatedSprite2D = null
var _healthy_seahorse: Sprite2D = null
var _clean_seahorse: Sprite2D = null
var _hidden_fixture_items: Array[Dictionary] = []


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	name = "DayOnePoolCleanup"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 22
	_build_light_wash()
	_capture_healthy_seahorse()
	_build_cleanup_steps()
	_build_pointer()
	_step = clampi(m.day_one_pool_cleanup_step, 0, CLEANUP_STEPS.size())
	_apply_restored_progress()
	set_process(true)
	if _step >= CLEANUP_STEPS.size():
		call_deferred("_begin_finale")
	else:
		call_deferred("_announce_current_step")


func teardown() -> void:
	set_process(false)
	if _healthy_seahorse != null and is_instance_valid(_healthy_seahorse):
		_healthy_seahorse.visible = true
	for record: Dictionary in _hidden_fixture_items:
		var item: CanvasItem = record.get("item") as CanvasItem
		if item != null and is_instance_valid(item):
			item.visible = bool(record.get("was_visible", true))
	_hidden_fixture_items.clear()
	if is_inside_tree():
		queue_free()
	else:
		free()


func audit_snapshot() -> Dictionary:
	return {
		"cleanup_step_count": CLEANUP_STEPS.size(),
		"current_step": _step,
		"seahorse_is_last": String(CLEANUP_STEPS[-1]["id"]) == "seahorse",
		"sprite_count": _step_sprites.size(),
		"button_count": _step_buttons.size(),
		"dingy_lighting": _light_wash != null,
		"finale_started": _finale_started,
		"rumi_present": _rumi != null and is_instance_valid(_rumi),
		"rumi_approved_identity": _rumi != null and is_instance_valid(_rumi)
			and bool(_rumi.get_meta("approved_private_canon", false)),
		"rumi_authored_animation": _rumi != null and is_instance_valid(_rumi)
			and _rumi.sprite_frames != null
			and _rumi.sprite_frames.get_frame_count(&"idle") == 2
			and _rumi.sprite_frames.get_frame_count(&"wave") == 2
			and _rumi.sprite_frames.get_frame_count(&"swim") == 4,
		"rumi_animation": String(_rumi.animation) \
			if _rumi != null and is_instance_valid(_rumi) else "",
		"canvas_only": true,
	}


func probe_advance_current_step() -> bool:
	if _busy or _step >= CLEANUP_STEPS.size():
		return false
	_busy = true
	_finish_cleanup_step(_step)
	return true


func _process(delta: float) -> void:
	_pulse_time += maxf(delta, 0.0)
	if _pointer == null or not is_instance_valid(_pointer) \
			or not _pointer.visible:
		return
	var pulse: float = 1.0 + sin(_pulse_time * 4.2) * 0.10
	_pointer.scale = Vector2.ONE * pulse
	_pointer.rotation = sin(_pulse_time * 2.7) * 0.055


func _build_light_wash() -> void:
	_light_wash = ColorRect.new()
	_light_wash.name = "DingyPoolLighting"
	_light_wash.position = Vector2.ZERO
	_light_wash.size = StorybookUI.CANVAS_SIZE
	_light_wash.color = DINGY_WASH
	_light_wash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_light_wash.z_index = 0
	_light_wash.set_meta("day_one_pool_dingy_lighting", true)
	add_child(_light_wash)


func _capture_healthy_seahorse() -> void:
	var record: Dictionary = m.castle_room_item_sprites.get(
		"seahorse_fountain", {}) as Dictionary
	_healthy_seahorse = record.get("sprite") as Sprite2D
	if _healthy_seahorse != null:
		_healthy_seahorse.visible = false
	var fixture_rig: Dictionary = record.get("fixture_rig", {}) as Dictionary
	for water_value: Variant in fixture_rig.get("water", []):
		var water: Dictionary = water_value as Dictionary
		var water_item: CanvasItem = water.get("node") as CanvasItem
		if water_item == null:
			continue
		_hidden_fixture_items.append({
			"item": water_item,
			"was_visible": water_item.visible,
		})
		water_item.visible = false
	var clean_texture: Texture2D = load(
		"res://assets/flats/castle/rooms/room_mermaid_pool_item_seahorse_fountain.png"
	) as Texture2D
	if clean_texture != null:
		_clean_seahorse = Sprite2D.new()
		_clean_seahorse.name = "HealthySeahorseRest"
		_clean_seahorse.texture = clean_texture
		_clean_seahorse.position = Vector2(915.625, 246.875)
		_clean_seahorse.scale = Vector2.ONE * 1.25
		_clean_seahorse.z_index = 1
		_clean_seahorse.visible = false
		add_child(_clean_seahorse)


func _build_cleanup_steps() -> void:
	for index: int in range(CLEANUP_STEPS.size()):
		var step_data: Dictionary = CLEANUP_STEPS[index]
		var texture: Texture2D = load(String(step_data["texture"])) as Texture2D
		if texture == null:
			push_error("Missing Day One pool cleanup texture: %s" % step_data["texture"])
			continue
		var sprite := Sprite2D.new()
		sprite.name = "Dirty_%s" % String(step_data["id"])
		sprite.texture = texture
		sprite.position = step_data["center"] as Vector2
		var max_size: Vector2 = step_data["max_size"] as Vector2
		var source_size: Vector2 = texture.get_size()
		var fit_scale: float = minf(
			max_size.x / maxf(source_size.x, 1.0),
			max_size.y / maxf(source_size.y, 1.0))
		sprite.scale = Vector2.ONE * fit_scale
		sprite.z_index = 2 + index
		sprite.set_meta("cleanup_id", String(step_data["id"]))
		add_child(sprite)
		_step_sprites.append(sprite)

		var button := Button.new()
		button.name = "Clean_%s" % String(step_data["id"])
		var hit_size: Vector2 = step_data["hit_size"] as Vector2
		button.position = (step_data["center"] as Vector2) - hit_size * 0.5
		button.size = hit_size
		button.flat = true
		button.focus_mode = Control.FOCUS_NONE
		button.mouse_filter = Control.MOUSE_FILTER_STOP
		button.tooltip_text = "Clean this spot"
		button.z_index = 12 + index
		button.set_meta("cleanup_step", index)
		button.pressed.connect(_on_cleanup_pressed.bind(index))
		add_child(button)
		_step_buttons.append(button)


func _build_pointer() -> void:
	_pointer = Label.new()
	_pointer.name = "CleanHerePointer"
	_pointer.text = "👇"
	_pointer.size = Vector2(96.0, 96.0)
	_pointer.pivot_offset = _pointer.size * 0.5
	_pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pointer.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pointer.z_index = 30
	StorybookUI.style_label(_pointer, 64, Color(1.0, 0.88, 0.35), 6)
	add_child(_pointer)


func _apply_restored_progress() -> void:
	for index: int in range(_step_sprites.size()):
		_step_sprites[index].visible = index >= _step
	_update_dingy_lighting()
	_refresh_current_target()
	if _clean_seahorse != null and is_instance_valid(_clean_seahorse):
		_clean_seahorse.visible = _step >= CLEANUP_STEPS.size()


func _refresh_current_target() -> void:
	for index: int in range(_step_buttons.size()):
		var available: bool = not _busy and index == _step \
			and _step_sprites[index].visible
		_step_buttons[index].disabled = not available
		_step_buttons[index].mouse_filter = Control.MOUSE_FILTER_STOP \
			if available else Control.MOUSE_FILTER_IGNORE
	if _pointer == null:
		return
	_pointer.visible = not _busy and _step < CLEANUP_STEPS.size()
	if _pointer.visible:
		var target_center: Vector2 = CLEANUP_STEPS[_step]["center"] as Vector2
		var hit_size: Vector2 = CLEANUP_STEPS[_step]["hit_size"] as Vector2
		_pointer.position = target_center + Vector2(
			hit_size.x * 0.23, -hit_size.y * 0.56) - _pointer.size * 0.5


func _on_cleanup_pressed(index: int) -> void:
	if _busy or index != _step or index >= _step_sprites.size():
		return
	_busy = true
	_refresh_current_target()
	m._ui_tap()
	var sprite: Sprite2D = _step_sprites[index]
	_spawn_clean_sparkles(sprite.position)
	var clean_tween: Tween = sprite.create_tween()
	clean_tween.tween_property(sprite, "rotation", -0.07, 0.08)
	clean_tween.tween_property(sprite, "rotation", 0.07, 0.08)
	clean_tween.tween_property(sprite, "rotation", 0.0, 0.08)
	clean_tween.parallel().tween_property(
		sprite, "scale", sprite.scale * 1.12, 0.24)
	clean_tween.tween_property(sprite, "modulate:a", 0.0, 0.22)
	clean_tween.tween_callback(_finish_cleanup_step.bind(index))


func _finish_cleanup_step(index: int) -> void:
	if index != _step or index >= _step_sprites.size():
		_busy = false
		_refresh_current_target()
		return
	var sprite: Sprite2D = _step_sprites[index]
	sprite.visible = false
	sprite.modulate.a = 1.0
	_step += 1
	m.day_one_pool_cleanup_step = _step
	cleanup_step_completed.emit(
		_step, String(CLEANUP_STEPS[index]["id"]))
	_update_dingy_lighting()
	_busy = false
	if _step >= CLEANUP_STEPS.size():
		if _clean_seahorse != null and is_instance_valid(_clean_seahorse):
			_clean_seahorse.visible = true
		_begin_finale()
	else:
		_refresh_current_target()
		_announce_current_step()


func _update_dingy_lighting() -> void:
	if _light_wash == null:
		return
	var remaining_ratio: float = 1.0 - float(_step) / float(
		maxi(CLEANUP_STEPS.size(), 1))
	_light_wash.color = Color(
		DINGY_WASH.r, DINGY_WASH.g, DINGY_WASH.b,
		DINGY_WASH.a * remaining_ratio)


func _announce_current_step() -> void:
	if not _announcements_enabled or m == null \
			or _step >= CLEANUP_STEPS.size():
		return
	match String(CLEANUP_STEPS[_step]["id"]):
		"pool_surface":
			m.show_msg("Roshan",
				"Oh no! The pool is covered in algae and trash. Tap the glowing mess!",
				"talk")
		"rainbow_fountain":
			m.show_msg("Roshan",
				"The rainbow fountain is clogged too. Tap the hanging seaweed!",
				"talk")
		"pool_rim":
			m.show_msg("Roshan",
				"Almost there! Tap the soggy trash by the pool edge!",
				"talk")
		"seahorse":
			m.show_msg("Roshan",
				"The seahorse looks sick! Tap the seaweed to help it last!",
				"talk")


func _spawn_clean_sparkles(center: Vector2) -> void:
	for index: int in range(8):
		var sparkle := Label.new()
		sparkle.text = "✦"
		sparkle.size = Vector2(42.0, 42.0)
		sparkle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sparkle.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		sparkle.mouse_filter = Control.MOUSE_FILTER_IGNORE
		sparkle.z_index = 40
		var angle: float = TAU * float(index) / 8.0
		var start_offset := Vector2(cos(angle), sin(angle)) * 18.0
		var end_offset := Vector2(cos(angle), sin(angle)) * (70.0 + index * 3.0)
		sparkle.position = center + start_offset - sparkle.size * 0.5
		StorybookUI.style_label(
			sparkle, 32, CLEAN_SPARKLE_COLORS[index % CLEAN_SPARKLE_COLORS.size()], 3)
		add_child(sparkle)
		var sparkle_tween: Tween = sparkle.create_tween().set_parallel(true)
		sparkle_tween.tween_property(
			sparkle, "position", center + end_offset - sparkle.size * 0.5, 0.46)
		sparkle_tween.tween_property(sparkle, "modulate:a", 0.0, 0.46)
		sparkle_tween.chain().tween_callback(sparkle.queue_free)


func _begin_finale() -> void:
	if _finale_started:
		return
	_finale_started = true
	_busy = true
	_refresh_current_target()
	if _pointer != null:
		_pointer.visible = false
	if _light_wash != null:
		var light_tween: Tween = _light_wash.create_tween()
		light_tween.tween_property(
			_light_wash, "color", Color(0.82, 0.96, 1.0, 0.0), 0.85)
	finale_started.emit()
	_spawn_rumi_rise()


func _spawn_rumi_rise() -> void:
	var pool_atlas: Texture2D = load(RUMI_POOL_ATLAS) as Texture2D
	var pose_atlas: Texture2D = load(RUMI_POSE_ATLAS) as Texture2D
	if pool_atlas == null or pose_atlas == null:
		push_error("Missing approved Rumi animation atlases: %s / %s" % [
			RUMI_POOL_ATLAS, RUMI_POSE_ATLAS])
		_finish_rumi_reveal()
		return
	_rumi = AnimatedSprite2D.new()
	_rumi.name = "RumiVioletReveal"
	_rumi.sprite_frames = _build_rumi_sprite_frames(pool_atlas, pose_atlas)
	_rumi.animation_finished.connect(_on_rumi_animation_finished)
	_rumi.position = Vector2(640.0, 610.0)
	_rumi.scale = Vector2.ONE * RUMI_SWIM_SCALE * 0.72
	_rumi.modulate.a = 0.0
	_rumi.z_index = 18
	_rumi.set_meta("approved_private_canon", true)
	_rumi.set_meta("source_working_name", "Violet Tide")
	add_child(_rumi)
	_rumi.play(&"swim")
	_spawn_reveal_ripple()
	var rise_tween: Tween = _rumi.create_tween().set_parallel(true)
	rise_tween.tween_property(
		_rumi, "position", Vector2(650.0, 350.0), 1.15
	).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	rise_tween.tween_property(
		_rumi, "scale", Vector2.ONE * RUMI_SWIM_SCALE, 1.0
	).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	rise_tween.tween_property(_rumi, "modulate:a", 1.0, 0.52)
	rise_tween.chain().tween_callback(_finish_rumi_reveal)


func _build_rumi_sprite_frames(
		pool_atlas: Texture2D, pose_atlas: Texture2D) -> SpriteFrames:
	var frames := SpriteFrames.new()
	frames.remove_animation(&"default")
	frames.add_animation(&"idle")
	frames.set_animation_speed(&"idle", 1.5)
	frames.set_animation_loop(&"idle", true)
	for column: int in range(2):
		frames.add_frame(&"idle", _rumi_atlas_frame(
			pose_atlas, column, 0, RUMI_POSE_CELL_SIZE))
	frames.add_animation(&"wave")
	frames.set_animation_speed(&"wave", 2.0)
	frames.set_animation_loop(&"wave", false)
	for column: int in range(2, 4):
		frames.add_frame(&"wave", _rumi_atlas_frame(
			pose_atlas, column, 0, RUMI_POSE_CELL_SIZE))
	frames.add_animation(&"swim")
	frames.set_animation_speed(&"swim", 5.0)
	frames.set_animation_loop(&"swim", true)
	for column: int in range(4):
		frames.add_frame(&"swim", _rumi_atlas_frame(
			pool_atlas, column, 1, RUMI_POOL_CELL_SIZE))
	return frames


func _rumi_atlas_frame(atlas: Texture2D, column: int, row: int,
		cell_size: Vector2) -> AtlasTexture:
	var frame := AtlasTexture.new()
	frame.atlas = atlas
	frame.region = Rect2(
		Vector2(float(column) * cell_size.x, float(row) * cell_size.y),
		cell_size)
	return frame


func _on_rumi_animation_finished() -> void:
	if _rumi != null and is_instance_valid(_rumi) \
			and _rumi.animation == &"wave":
		_rumi.play(&"idle")


func _spawn_reveal_ripple() -> void:
	var ripple := Label.new()
	ripple.name = "RumiRiseRipple"
	ripple.text = "○"
	ripple.position = Vector2(490.0, 470.0)
	ripple.size = Vector2(300.0, 110.0)
	ripple.pivot_offset = ripple.size * 0.5
	ripple.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ripple.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	ripple.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ripple.z_index = 17
	ripple.scale = Vector2(0.45, 0.20)
	StorybookUI.style_label(ripple, 92, Color(0.54, 0.96, 1.0), 5)
	add_child(ripple)
	var ripple_tween: Tween = ripple.create_tween().set_parallel(true)
	ripple_tween.tween_property(ripple, "scale", Vector2(2.1, 0.56), 1.0)
	ripple_tween.tween_property(ripple, "modulate:a", 0.0, 1.0)
	ripple_tween.chain().tween_callback(ripple.queue_free)


func _finish_rumi_reveal() -> void:
	_busy = false
	if _rumi != null and is_instance_valid(_rumi):
		_rumi.scale = Vector2.ONE * RUMI_UPRIGHT_START_SCALE
		_rumi.play(&"wave")
		var settle_tween: Tween = _rumi.create_tween()
		settle_tween.tween_property(
			_rumi, "scale", Vector2.ONE * RUMI_UPRIGHT_SCALE, 0.35
		).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		var idle_tween: Tween = _rumi.create_tween().set_loops()
		idle_tween.tween_property(
			_rumi, "position:y", _rumi.position.y - 7.0, 1.15
		).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		idle_tween.tween_property(
			_rumi, "position:y", _rumi.position.y + 7.0, 1.15
		).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	if m != null:
		m.show_msg("Rumi",
			"Thank you, Roshan! You saved the pool and our seahorse. I'm Rumi!",
			"intro")
	reveal_completed.emit()
