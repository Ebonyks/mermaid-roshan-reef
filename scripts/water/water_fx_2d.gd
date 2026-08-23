class_name WaterFx2D
extends Node2D

# Shared, deterministic Canvas playback for the approved water event atlases.
# Events describe real contacts only; ambient water never calls emit_event().

const MAX_ACTIVE := 6
const MAX_LARGE := 2
const EMITTER_COOLDOWN_SECONDS := 0.5
const FRAME_COUNT := 8

const EVENT_SPECS := {
	"small": {
		"texture": preload("res://assets/sprites/fx_water/fx_water_splash_small_atlas.png"),
		"grid": Vector2i(4, 2), "frame_seconds": 0.08, "large": false,
	},
	"medium": {
		"texture": preload("res://assets/sprites/fx_water/fx_water_splash_medium_atlas.png"),
		"grid": Vector2i(3, 3), "frame_seconds": 0.10, "large": true,
	},
	"breach": {
		"texture": preload("res://assets/sprites/fx_water/fx_water_splash_breach_atlas.png"),
		"grid": Vector2i(3, 3), "frame_seconds": 0.11, "large": true,
	},
	"ripple": {
		"texture": preload("res://assets/sprites/fx_water/fx_water_ripple_ring_atlas.png"),
		"grid": Vector2i(4, 2), "frame_seconds": 0.12, "large": false,
	},
	"bubble": {
		"texture": preload("res://assets/sprites/fx_water/fx_water_bubble_burst_atlas.png"),
		"grid": Vector2i(4, 2), "frame_seconds": 0.10, "large": false,
	},
}

var _active: Array[Dictionary] = []
var _emitter_last_time: Dictionary = {}
var _emitted_total := 0


func emit_event(kind: String, stage_position: Vector2,
		emitter_id: String = "player", scale_factor: float = 1.0) -> bool:
	var spec: Dictionary = EVENT_SPECS.get(kind, {}) as Dictionary
	if spec.is_empty():
		return false
	var now := float(Time.get_ticks_msec()) * 0.001
	var last_time := float(_emitter_last_time.get(emitter_id, -1000.0))
	if now - last_time < EMITTER_COOLDOWN_SECONDS:
		return false
	var large := bool(spec.get("large", false))
	if large and _large_count() >= MAX_LARGE:
		return false
	_evict_if_needed()
	var sprite := Sprite2D.new()
	sprite.name = "WaterEvent_%s" % kind
	sprite.texture = spec["texture"] as Texture2D
	var grid: Vector2i = spec["grid"] as Vector2i
	sprite.hframes = grid.x
	sprite.vframes = grid.y
	sprite.frame = 0
	sprite.position = stage_position
	sprite.scale = Vector2.ONE * clampf(scale_factor, 0.35, 1.8)
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	sprite.set_meta("water_event_kind", kind)
	sprite.set_meta("water_event_emitter", emitter_id)
	sprite.set_meta("water_event_logic_authority", false)
	add_child(sprite)
	_active.append({
		"sprite": sprite,
		"kind": kind,
		"elapsed": 0.0,
		"frame_seconds": float(spec["frame_seconds"]),
		"large": large,
	})
	_emitter_last_time[emitter_id] = now
	_emitted_total += 1
	return true


func tick(delta: float) -> void:
	var survivors: Array[Dictionary] = []
	for record_value: Variant in _active:
		var record: Dictionary = record_value as Dictionary
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		if sprite == null or not is_instance_valid(sprite):
			continue
		var elapsed := float(record.get("elapsed", 0.0)) + maxf(0.0, delta)
		var frame_seconds := maxf(0.01, float(record.get("frame_seconds", 0.10)))
		var frame_index := int(floor(elapsed / frame_seconds))
		if frame_index >= FRAME_COUNT:
			sprite.queue_free()
			continue
		sprite.frame = frame_index
		record["elapsed"] = elapsed
		survivors.append(record)
	_active = survivors


func clear_events() -> void:
	for record_value: Variant in _active:
		var record: Dictionary = record_value as Dictionary
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		if sprite != null and is_instance_valid(sprite):
			sprite.queue_free()
	_active.clear()
	_emitter_last_time.clear()


func stats() -> Dictionary:
	return {
		"active": _active.size(),
		"large": _large_count(),
		"emitted_total": _emitted_total,
		"cap": MAX_ACTIVE,
		"canvas_only": true,
	}


func _large_count() -> int:
	var count := 0
	for record_value: Variant in _active:
		var record: Dictionary = record_value as Dictionary
		if bool(record.get("large", false)):
			count += 1
	return count


func _evict_if_needed() -> void:
	if _active.size() < MAX_ACTIVE:
		return
	var index_to_remove := 0
	for index in range(_active.size()):
		var record: Dictionary = _active[index] as Dictionary
		if not bool(record.get("large", false)):
			index_to_remove = index
			break
	var removed: Dictionary = _active[index_to_remove] as Dictionary
	var sprite: Sprite2D = removed.get("sprite") as Sprite2D
	if sprite != null and is_instance_valid(sprite):
		sprite.queue_free()
	_active.remove_at(index_to_remove)
