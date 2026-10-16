extends RefCounted
# Existing local pixels only. No source state, input box, texture or clock writes.
const SOURCE_TEXTURE_SIZE := Vector2(512.0, 512.0)
const SOURCE_TIP := Vector2(217.0, 447.0)
const SOURCE_WAYPOINT_BASE_DELTA := Vector2(-42.0, -82.0)
var _pointer_ref: WeakRef
var original_offset := Vector2.ZERO
var registered_offset := Vector2.ZERO

func apply(source: RefCounted) -> bool:
	var pointer: Sprite2D = source.get("_pointer") as Sprite2D
	if pointer == null or pointer.texture == null or pointer.texture.get_size() != SOURCE_TEXTURE_SIZE or not pointer.centered or pointer.flip_h or pointer.flip_v:
		return false
	if pointer.scale != Vector2.ONE * 0.12:
		return false
	_pointer_ref = weakref(pointer)
	original_offset = pointer.offset
	registered_offset = -SOURCE_WAYPOINT_BASE_DELTA / pointer.scale - (SOURCE_TIP - SOURCE_TEXTURE_SIZE * 0.5)
	pointer.offset = registered_offset
	return true

func audit_snapshot() -> Dictionary:
	var pointer: Sprite2D = _pointer_ref.get_ref() as Sprite2D if _pointer_ref != null else null
	return {"pointer_alive": pointer != null, "original_offset": [original_offset.x, original_offset.y], "registered_offset": [registered_offset.x, registered_offset.y], "new_nodes": 0, "new_textures": 0, "frame_processors_added": 0, "pixels_changed": false, "source_progress_written": false}
