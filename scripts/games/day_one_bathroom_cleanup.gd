class_name DayOneBathroomCleanup
extends Control
## Three-part, one-finger cleanup for Day One's Bubble Bathroom.
##
## ReefMain owns the persistent step. This node owns only the temporary
## Canvas2D presentation, one active touch target, visual pointer, and cleanup
## feedback layered over the approved castle room art.

signal cleanup_step_completed(step: int, cleanup_id: String)
signal finale_started
signal cleanup_completed

const ASSET_ROOT := "res://assets/castle/dirty_cleanup_2d/"
const CLEANUP_STEPS: Array[Dictionary] = [
	{
		"id": "cloudy_mirror",
		"texture": ASSET_ROOT + "targets/target_cloudy_mirror.png",
		"center": Vector2(642.0, 154.0),
		"max_size": Vector2(238.0, 196.0),
		"hit_size": Vector2(292.0, 232.0),
	},
	{
		"id": "bath_soap_ring",
		"texture": ASSET_ROOT + "targets/target_bath_soap_ring.png",
		"center": Vector2(310.0, 349.0),
		"max_size": Vector2(300.0, 174.0),
		"hit_size": Vector2(360.0, 224.0),
	},
	{
		"id": "floor_scuff",
		"texture": ASSET_ROOT + "targets/target_floor_scuff.png",
		"center": Vector2(684.0, 554.0),
		"max_size": Vector2(330.0, 166.0),
		"hit_size": Vector2(398.0, 196.0),
	},
]
const TOOL_TEXTURE := ASSET_ROOT + "tools/tool_star_sponge.png"
const POINTER_RING_TEXTURE := ASSET_ROOT + "effects/fx_clean_ring.png"
const BUBBLE_TEXTURE := ASSET_ROOT + "effects/fx_soap_bubbles.png"
const WIPE_TEXTURE := ASSET_ROOT + "effects/fx_wipe_swoosh.png"
const DINGY_WASH := Color(0.18, 0.15, 0.24, 0.18)

var m: ReefMain
var _step: int = 0
var _busy: bool = false
var _finale_started: bool = false
var _completion_emitted: bool = false
var _announcements_enabled: bool = true
var _pulse_time: float = 0.0
var _target_sprites: Array[Sprite2D] = []
var _target_buttons: Array[Button] = []
var _light_wash: ColorRect = null
var _pointer: Label = null
var _focus_ring: Sprite2D = null
var _focus_ring_base_scale: Vector2 = Vector2.ONE
var _tool: Sprite2D = null
var _tool_base_scale: Vector2 = Vector2.ONE
var _hotspot_layer: Control = null
var _hotspot_layer_was_visible: bool = false


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	name = "DayOneBathroomCleanup"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 22
	_suspend_room_hotspots()
	_build_light_wash()
	_build_targets()
	_build_guidance()
	_step = clampi(m.day_one_bathroom_cleanup_step, 0, CLEANUP_STEPS.size())
	_apply_restored_progress()
	set_process(true)
	if _step >= CLEANUP_STEPS.size():
		call_deferred("_begin_finale")
	else:
		call_deferred("_announce_current_step")


func teardown() -> void:
	set_process(false)
	if _hotspot_layer != null and is_instance_valid(_hotspot_layer):
		_hotspot_layer.visible = _hotspot_layer_was_visible
	_hotspot_layer = null
	if is_inside_tree():
		queue_free()
	else:
		free()


func audit_snapshot() -> Dictionary:
	var active_targets: int = 0
	var minimum_touch_side: float = INF
	for button: Button in _target_buttons:
		if not button.disabled:
			active_targets += 1
		minimum_touch_side = minf(minimum_touch_side,
			minf(button.size.x, button.size.y))
	return {
		"cleanup_step_count": CLEANUP_STEPS.size(),
		"current_step": _step,
		"sprite_count": _target_sprites.size(),
		"button_count": _target_buttons.size(),
		"active_target_count": active_targets,
		"minimum_touch_side": minimum_touch_side,
		"voice_guidance_configured": true,
		"announcements_enabled": _announcements_enabled,
		"has_visual_pointer": _pointer != null and _focus_ring != null
			and _tool != null,
		"dingy_lighting": _light_wash != null,
		"finale_started": _finale_started,
		"completion_emitted": _completion_emitted,
		"canvas_only": true,
	}


func probe_advance_current_step() -> bool:
	if _busy or _step >= CLEANUP_STEPS.size():
		return false
	_busy = true
	_finish_cleanup_step(_step)
	return true


func probe_finish_finale() -> bool:
	if not _finale_started or _completion_emitted:
		return false
	_finish_finale()
	return true


func _process(delta: float) -> void:
	_pulse_time += maxf(delta, 0.0)
	if _focus_ring != null and is_instance_valid(_focus_ring) \
			and _focus_ring.visible:
		var ring_pulse: float = 1.0 + sin(_pulse_time * 4.4) * 0.08
		_focus_ring.scale = _focus_ring_base_scale * ring_pulse
		_focus_ring.modulate.a = 0.72 + sin(_pulse_time * 4.4) * 0.16
	if _tool != null and is_instance_valid(_tool) and _tool.visible:
		_tool.rotation = sin(_pulse_time * 3.1) * 0.08
		_tool.scale = _tool_base_scale * (
			1.0 + sin(_pulse_time * 3.8) * 0.035)
	if _pointer != null and is_instance_valid(_pointer) and _pointer.visible:
		_pointer.rotation = sin(_pulse_time * 2.8) * 0.05


func _suspend_room_hotspots() -> void:
	_hotspot_layer = m.castle_room_item_hotspot_layer
	if _hotspot_layer == null or not is_instance_valid(_hotspot_layer):
		_hotspot_layer = null
		return
	_hotspot_layer_was_visible = _hotspot_layer.visible
	_hotspot_layer.visible = false


func _build_light_wash() -> void:
	_light_wash = ColorRect.new()
	_light_wash.name = "DingyBathroomLighting"
	_light_wash.position = Vector2.ZERO
	_light_wash.size = StorybookUI.CANVAS_SIZE
	_light_wash.color = DINGY_WASH
	_light_wash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_light_wash.z_index = 0
	_light_wash.set_meta("day_one_bathroom_dingy_lighting", true)
	add_child(_light_wash)


func _build_targets() -> void:
	for index: int in range(CLEANUP_STEPS.size()):
		var step_data: Dictionary = CLEANUP_STEPS[index]
		var texture: Texture2D = load(String(step_data["texture"])) as Texture2D
		if texture == null:
			push_error("Missing Day One bathroom texture: %s" % step_data["texture"])
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
		_target_sprites.append(sprite)

		var button := Button.new()
		button.name = "Clean_%s" % String(step_data["id"])
		var hit_size: Vector2 = step_data["hit_size"] as Vector2
		button.position = (step_data["center"] as Vector2) - hit_size * 0.5
		button.size = hit_size
		button.flat = true
		button.focus_mode = Control.FOCUS_NONE
		button.mouse_filter = Control.MOUSE_FILTER_STOP
		button.tooltip_text = "Clean this spot"
		button.z_index = 20 + index
		button.set_meta("cleanup_step", index)
		button.pressed.connect(_on_cleanup_pressed.bind(index))
		add_child(button)
		_target_buttons.append(button)


func _build_guidance() -> void:
	var ring_texture: Texture2D = load(POINTER_RING_TEXTURE) as Texture2D
	if ring_texture != null:
		_focus_ring = Sprite2D.new()
		_focus_ring.name = "CleanTargetRing"
		_focus_ring.texture = ring_texture
		_focus_ring.z_index = 30
		_focus_ring.modulate = Color(1.0, 0.93, 0.48, 0.82)
		add_child(_focus_ring)

	var tool_texture: Texture2D = load(TOOL_TEXTURE) as Texture2D
	if tool_texture != null:
		_tool = Sprite2D.new()
		_tool.name = "StarSpongePointer"
		_tool.texture = tool_texture
		_tool.z_index = 32
		add_child(_tool)

	_pointer = Label.new()
	_pointer.name = "CleanHerePointer"
	_pointer.text = "👇"
	_pointer.size = Vector2(96.0, 96.0)
	_pointer.pivot_offset = _pointer.size * 0.5
	_pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pointer.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pointer.z_index = 34
	StorybookUI.style_label(_pointer, 62, Color(1.0, 0.87, 0.32), 6)
	add_child(_pointer)


func _apply_restored_progress() -> void:
	for index: int in range(_target_sprites.size()):
		_target_sprites[index].visible = index >= _step
	_update_dingy_lighting()
	_refresh_current_target()


func _refresh_current_target() -> void:
	for index: int in range(_target_buttons.size()):
		var available: bool = not _busy and index == _step \
			and _target_sprites[index].visible
		_target_buttons[index].disabled = not available
		_target_buttons[index].mouse_filter = Control.MOUSE_FILTER_STOP \
			if available else Control.MOUSE_FILTER_IGNORE
	var target_visible: bool = not _busy and _step < CLEANUP_STEPS.size()
	if _pointer != null:
		_pointer.visible = target_visible
	if _focus_ring != null:
		_focus_ring.visible = target_visible
	if _tool != null:
		_tool.visible = target_visible
	if not target_visible:
		return
	var step_data: Dictionary = CLEANUP_STEPS[_step]
	var target_center: Vector2 = step_data["center"] as Vector2
	var hit_size: Vector2 = step_data["hit_size"] as Vector2
	_pointer.position = target_center + Vector2(
		hit_size.x * 0.28, -hit_size.y * 0.56) - _pointer.size * 0.5
	if _focus_ring != null and _focus_ring.texture != null:
		_focus_ring.position = target_center
		var ring_source: Vector2 = _focus_ring.texture.get_size()
		var ring_scale: float = minf(
			(hit_size.x + 20.0) / maxf(ring_source.x, 1.0),
			(hit_size.y + 20.0) / maxf(ring_source.y, 1.0))
		_focus_ring_base_scale = Vector2.ONE * ring_scale
		_focus_ring.scale = _focus_ring_base_scale
	if _tool != null and _tool.texture != null:
		_tool.position = target_center + Vector2(
			hit_size.x * 0.35, hit_size.y * 0.30)
		var tool_size: Vector2 = _tool.texture.get_size()
		var tool_scale: float = 88.0 / maxf(
			maxf(tool_size.x, tool_size.y), 1.0)
		_tool_base_scale = Vector2.ONE * tool_scale
		_tool.scale = _tool_base_scale


func _on_cleanup_pressed(index: int) -> void:
	if _busy or index != _step or index >= _target_sprites.size():
		return
	_busy = true
	_refresh_current_target()
	m._ui_tap()
	var sprite: Sprite2D = _target_sprites[index]
	_spawn_cleanup_effect(sprite.position)
	var clean_tween: Tween = sprite.create_tween()
	clean_tween.tween_property(sprite, "rotation", -0.07, 0.08)
	clean_tween.tween_property(sprite, "rotation", 0.07, 0.08)
	clean_tween.tween_property(sprite, "rotation", 0.0, 0.08)
	clean_tween.parallel().tween_property(
		sprite, "scale", sprite.scale * 1.10, 0.24)
	clean_tween.tween_property(sprite, "modulate:a", 0.0, 0.24)
	clean_tween.tween_callback(_finish_cleanup_step.bind(index))


func _finish_cleanup_step(index: int) -> void:
	if index != _step or index >= _target_sprites.size():
		_busy = false
		_refresh_current_target()
		return
	var sprite: Sprite2D = _target_sprites[index]
	sprite.visible = false
	sprite.modulate.a = 1.0
	_step += 1
	m.day_one_bathroom_cleanup_step = _step
	cleanup_step_completed.emit(_step, String(CLEANUP_STEPS[index]["id"]))
	_update_dingy_lighting()
	_busy = false
	if _step >= CLEANUP_STEPS.size():
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
		"cloudy_mirror":
			m.show_msg("Roshan",
				"The mirror is cloudy. Tap the glowing sponge!", "talk")
		"bath_soap_ring":
			m.show_msg("Roshan",
				"Great wiping! Tap the bubbly ring around the tub!", "talk")
		"floor_scuff":
			m.show_msg("Roshan",
				"One last purple scuff. Tap it and make the floor sparkle!", "talk")


func _spawn_cleanup_effect(center: Vector2) -> void:
	_spawn_effect_sprite(BUBBLE_TEXTURE, center, Vector2(0.34, 0.34),
		Vector2(0.58, 0.58), 0.52)
	_spawn_effect_sprite(WIPE_TEXTURE, center, Vector2(0.28, 0.28),
		Vector2(0.42, 0.42), 0.38)


func _spawn_effect_sprite(texture_path: String, center: Vector2,
		start_scale: Vector2, end_scale: Vector2, duration: float) -> void:
	var texture: Texture2D = load(texture_path) as Texture2D
	if texture == null:
		return
	var effect := Sprite2D.new()
	effect.texture = texture
	effect.position = center
	effect.scale = start_scale
	effect.z_index = 40
	add_child(effect)
	var effect_tween: Tween = effect.create_tween().set_parallel(true)
	effect_tween.tween_property(effect, "scale", end_scale, duration)
	effect_tween.tween_property(effect, "modulate:a", 0.0, duration)
	effect_tween.chain().tween_callback(effect.queue_free)


func _begin_finale() -> void:
	if _finale_started:
		return
	_finale_started = true
	_busy = true
	_refresh_current_target()
	finale_started.emit()
	_spawn_effect_sprite(BUBBLE_TEXTURE, Vector2(640.0, 380.0),
		Vector2(0.50, 0.50), Vector2(1.28, 1.28), 0.72)
	if _light_wash != null:
		var light_tween: Tween = _light_wash.create_tween()
		light_tween.tween_property(
			_light_wash, "color", Color(0.86, 0.98, 1.0, 0.0), 0.65)
		light_tween.tween_callback(_finish_finale)
	else:
		call_deferred("_finish_finale")


func _finish_finale() -> void:
	if _completion_emitted:
		return
	_completion_emitted = true
	_busy = false
	if _announcements_enabled and m != null:
		m.show_msg("Roshan",
			"The bathroom sparkles! The Mermaid Pool door is glowing next!", "win")
	cleanup_completed.emit()
