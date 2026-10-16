extends Node2D
## R75 nonproduction original-pixel registration preview; no input, source-state or clock ownership.
var source_book: OperaTreeBookTest
var original_hand: Texture2D
var sprite: Sprite2D
var detached := false

func attach(host: OperaTreeBookTest) -> bool:
	if host == null or host.hand == null or host.get_script().resource_path != "res://scripts/opera_tree_book_test.gd":
		return false
	source_book = host
	original_hand = host.hand
	name = "R75HandRegistrationPreview"
	host.add_child(self)
	sprite = Sprite2D.new()
	sprite.name = "R75OriginalHandPixels"
	sprite.texture = original_hand
	sprite.centered = false
	add_child(sprite)
	# Suppress only this named drawing resource. _fit(null) returns; it has no input or fallback branch.
	host.hand = null
	host.queue_redraw()
	_sync()
	return true

func _process(_delta: float) -> void:
	_sync()

func _sync() -> void:
	if detached or not is_instance_valid(source_book) or not is_instance_valid(sprite):
		return
	var hint := (source_book.stage < 3 and source_book.help_level == 2) or (source_book.stage == 4 and source_book.help_level > 0)
	sprite.visible = hint and source_book.is_visible_in_tree()
	if not hint:
		return
	var box: Rect2
	if source_book.stage < 3:
		var target: Rect2 = source_book.choice_rect(source_book.answer_slot())
		box = Rect2(target.end - Vector2(68, 55 + sin(source_book.elapsed * 3.0) * 9.0), Vector2(80, 80))
		box.position.y -= 36.0
	else:
		box = Rect2(OperaTreeBookTest.LEAF_RECT.position + Vector2(80, 78 + sin(source_book.elapsed * 3.0) * 10.0), Vector2(95, 95))
		box.position.y -= 44.0
	sprite.position = box.position
	sprite.scale = box.size / original_hand.get_size()

func tip_state() -> Dictionary:
	if detached or not is_instance_valid(source_book) or not is_instance_valid(sprite):
		return {}
	_sync()
	var target: Rect2 = source_book.choice_rect(source_book.answer_slot()) if source_book.stage < 3 else OperaTreeBookTest.LEAF_RECT
	var native_tip: Vector2 = sprite.get_global_transform_with_canvas() * Vector2(217, 447)
	var local_tip: Vector2 = source_book.get_global_transform_with_canvas().affine_inverse() * native_tip
	var origin: Vector2 = source_book.get_global_transform_with_canvas() * target.position
	var end: Vector2 = source_book.get_global_transform_with_canvas() * target.end
	return {"stage": source_book.stage, "help": source_book.help_level, "elapsed": source_book.elapsed, "bob_phase_radians": source_book.elapsed * 3.0, "texture": {"path": original_hand.resource_path, "class": original_hand.get_class(), "size": [original_hand.get_width(), original_hand.get_height()]}, "source_alpha64_tip": [217, 447], "draw_box": [sprite.position.x, sprite.position.y, sprite.scale.x * 512.0, sprite.scale.y * 512.0], "local_tip": [local_tip.x, local_tip.y], "native_tip": [native_tip.x, native_tip.y], "target": [target.position.x, target.position.y, target.size.x, target.size.y], "native_target": [origin.x, origin.y, end.x-origin.x, end.y-origin.y], "inside": target.has_point(local_tip), "pointer_visible_by_source_branch": sprite.visible, "sprite_instance": sprite.get_instance_id(), "sprite_transform": str(sprite.get_global_transform_with_canvas()), "registered_upward_offset": 36 if source_book.stage < 3 else 44, "original_hand_suppressed": source_book.hand == null}

func restore() -> bool:
	if detached or not is_instance_valid(source_book):
		return false
	source_book.hand = original_hand
	source_book.queue_redraw()
	detached = true
	sprite.visible = false
	queue_free()
	return true
