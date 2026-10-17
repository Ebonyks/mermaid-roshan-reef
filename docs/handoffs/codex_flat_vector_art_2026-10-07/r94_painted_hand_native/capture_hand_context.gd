extends "res://export/flat_vector_r94/capture_hand.gd"
const R94Background = preload("res://export/flat_vector_r94/skyway_reuse.gd")
var r94_background: RefCounted
var r94_context_delta: Dictionary = {}

func _r94_context_preserved(value: Dictionary) -> Dictionary:
	var result: Dictionary = value.duplicate(true)
	var backdrop: Dictionary = result["backdrop"] as Dictionary
	backdrop.erase("z")
	for row: Dictionary in result["tiles"]:
		row.erase("position")
		row.erase("scale")
	return result

func _enter_handoff(prefix: String) -> bool:
	if not await super(prefix):
		return false
	var before: Dictionary = _r94_signature()
	r94_background = R94Background.new()
	var bound: bool = bool(r94_background.call("attach", m.fairy_conservatory_handoff, "cover"))
	_check("same existingR70painted background layout attaches to original nodes", bound)
	if not bound:
		return false
	var after: Dictionary = _r94_signature()
	var preserved: bool = _r94_context_preserved(before) == _r94_context_preserved(after)
	r94_context_delta = {"before": before, "after": after, "preserved_outside_declared_background_z_tiles_position_scale": preserved, "source_background_defect": "Original opaque backdrop covers existing painted artwork; knownR70issue retained. This is only a nonruntime style-reference context, no source fix/adoption.", "new_generated_background_pixels": false, "background_texture_pixels_changed": false}
	_check("context preserves exact foreground/state/input/world and texture identities", preserved)
	return preserved

func _r94_apply() -> bool:
	if not super():
		return false
	var p: Sprite2D = m.fairy_conservatory_handoff.get("_pointer") as Sprite2D
	p.scale = Vector2.ONE * (36.0 / 665.0)
	var desired_delta := Vector2(-40.0, 0.0) - Vector2(-42.0, -82.0)
	p.offset = desired_delta / p.scale - (R94_TIP - Vector2(627.0, 627.0))
	return true

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	result["r94_painted_neighbor_context"] = r94_context_delta
	result["r94_hand_visible_fit_width"] = 36.0
	result["r94_context_is_production"] = false
	return result
