extends RefCounted
# Nonproduction region reuse only; no source bitmap files, state, input targets or clock writes.
const PAINTED_PATH := "res://assets/characters/roshan_25d/roshan_gesture_b.png"
const PAINTED_REGION := Rect2(527.0, 819.0, 28.0, 35.0)
const PAINTED_TIP := Vector2(1.0, 6.5)
const SOURCE_WAYPOINT_BASE_DELTA := Vector2(-42.0, -82.0)
const TARGET_TIP_DELTA := Vector2(-40.0, 0.0)
var _pointer_ref: WeakRef
var before: Dictionary = {}
var after: Dictionary = {}

func _draw_state(pointer: Sprite2D) -> Dictionary:
	var r: Rect2 = pointer.get_rect()
	return {"id": pointer.get_instance_id(), "texture_path": pointer.texture.resource_path, "texture_size": [pointer.texture.get_width(), pointer.texture.get_height()], "scale": [pointer.scale.x, pointer.scale.y], "offset": [pointer.offset.x, pointer.offset.y], "rotation": pointer.rotation, "region_enabled": pointer.region_enabled, "region_rect": [pointer.region_rect.position.x, pointer.region_rect.position.y, pointer.region_rect.size.x, pointer.region_rect.size.y], "draw_rect": [r.position.x, r.position.y, r.size.x, r.size.y], "position": [pointer.position.x, pointer.position.y], "z_index": pointer.z_index, "visible": pointer.visible}

func apply(source: RefCounted) -> bool:
	var pointer: Sprite2D = source.get("_pointer") as Sprite2D
	if pointer == null or pointer.texture == null or pointer.texture.get_size() != Vector2(512.0, 512.0) or not pointer.centered or pointer.flip_h or pointer.flip_v:
		return false
	if pointer.scale != Vector2.ONE * 0.12:
		return false
	_pointer_ref = weakref(pointer)
	before = _draw_state(pointer)
	var tip: Vector2 = Vector2(217.0, 447.0)
	var size: Vector2 = Vector2(512.0, 512.0)
	if OS.get_environment("R72_HAND") == "painted":
		var texture: Texture2D = load(PAINTED_PATH) as Texture2D
		if texture == null or texture.get_size() != Vector2(1024.0, 1024.0):
			return false
		pointer.texture = texture
		pointer.region_enabled = true
		pointer.region_rect = PAINTED_REGION
		pointer.region_filter_clip_enabled = true
		pointer.rotation = -PI * 0.5
		pointer.scale = Vector2.ONE * (49.0 / 27.0)
		tip = PAINTED_TIP
		size = PAINTED_REGION.size
	var desired_delta: Vector2 = TARGET_TIP_DELTA - SOURCE_WAYPOINT_BASE_DELTA
	pointer.offset = desired_delta.rotated(-pointer.rotation) / pointer.scale - (tip - size * 0.5)
	after = _draw_state(pointer)
	return true

func audit_snapshot() -> Dictionary:
	var pointer: Sprite2D = _pointer_ref.get_ref() as Sprite2D if _pointer_ref != null else null
	return {"pointer_alive": pointer != null, "variant": OS.get_environment("R72_HAND"), "before": before, "after": after, "new_nodes": 0, "new_generated_assets": 0, "source_pixels_modified": false, "source_progress_written": false, "frame_processors_added": 0, "source_region_role": "Existing runtime atlas point/reach frame14 literal region, no pixel editing or generation. New pointer use not accepted."}
