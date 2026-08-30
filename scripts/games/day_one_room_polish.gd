class_name DayOneRoomPolish
extends Control
## One new, saved, picture-first cleaning beat shared by the four Day One
## rooms. Each room supplies a purpose-built, versioned dirt target; one tap
## sends the approved cleaner across it, wipes it away, and hands control to
## that room's established activity.

signal completed(room_id: String, task_id: String)

const POINTER_TEXTURE := preload("res://assets/castle/training/ghost_hand.png")
const TOOL_TEXTURE := preload(
	"res://assets/castle/dirty_cleanup_2d/tools/tool_magic_cleaner_v1.png")
const WIPE_TEXTURE := preload(
	"res://assets/castle/dirty_cleanup_2d/effects/fx_wipe_swoosh.png")
const RING_TEXTURE := preload(
	"res://assets/castle/dirty_cleanup_2d/effects/fx_clean_ring.png")
const BUBBLE_TEXTURE := preload(
	"res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png")

const TASKS: Dictionary = {
	"bathroom": {
		"id": "soap_splatter",
		"texture": "res://assets/castle/day_one_polish_v2/bathroom_soap_splatter.png",
		"center": Vector2(650.0, 390.0),
		"target_longest": 220.0,
		"hit_size": Vector2(250.0, 210.0),
		"tool_start": Vector2(920.0, 410.0),
		"tint": Color.WHITE,
		"cue": "Tap the silly soap splat. One magic wipe!",
	},
	"pool": {
		"id": "algae_tangle",
		"texture": "res://assets/castle/day_one_polish_v2/pool_algae_tangle.png",
		"center": Vector2(650.0, 558.0),
		"target_longest": 230.0,
		"hit_size": Vector2(270.0, 170.0),
		"tool_start": Vector2(930.0, 445.0),
		"tint": Color.WHITE,
		"cue": "Tap the algae tangle. One magic scoop!",
	},
	"stuffie": {
		"id": "loose_stuffing",
		"texture": "res://assets/castle/day_one_polish_v2/stuffie_loose_stuffing.png",
		"center": Vector2(650.0, 565.0),
		"target_longest": 235.0,
		"hit_size": Vector2(290.0, 175.0),
		"tool_start": Vector2(970.0, 430.0),
		"tint": Color.WHITE,
		"cue": "Tap the loose stuffing, then we can help Baby Eagle!",
	},
	"art": {
		"id": "rainbow_paint_spill",
		"texture": "res://assets/castle/day_one_polish_v2/art_rainbow_spill.png",
		"center": Vector2(820.0, 555.0),
		"target_longest": 230.0,
		"hit_size": Vector2(270.0, 175.0),
		"tool_start": Vector2(1040.0, 410.0),
		"tint": Color.WHITE,
		"cue": "Tap the rainbow paint spill. One magic wipe!",
	},
}

var m: ReefMain
var room_id: String = ""
var task_id: String = ""
var _target: Sprite2D = null
var _tool: Sprite2D = null
var _pointer: Sprite2D = null
var _wipe: Sprite2D = null
var _ring: Sprite2D = null
var _bubbles: Sprite2D = null
var _button: Button = null
var _suppressed_guides: Array[CanvasItem] = []
var _elapsed := 0.0
var _busy := false


func setup(main: ReefMain, logical_room_id: String,
		announcements_enabled: bool = true) -> bool:
	m = main
	room_id = logical_room_id
	if not TASKS.has(room_id):
		return false
	var task: Dictionary = TASKS[room_id] as Dictionary
	task_id = String(task["id"])
	name = "DayOneRoomPolish_%s" % room_id
	position = Vector2.ZERO
	size = Vector2(1280.0, 720.0)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 72
	_build_visuals(task)
	_suppress_competing_guides()
	set_process(true)
	if announcements_enabled:
		call_deferred("_announce_task")
	return true


func teardown() -> void:
	set_process(false)
	_restore_competing_guides()
	if is_inside_tree():
		queue_free()
	else:
		free()


func audit_snapshot() -> Dictionary:
	return {
		"room_id": room_id,
		"task_id": task_id,
		"active": not _busy,
		"busy": _busy,
		"target_visible": _target != null and _target.visible,
		"pointer_visible": _pointer != null and _pointer.visible,
		"target_hit_size": _button.size if _button != null else Vector2.ZERO,
		"one_finger": true,
		"no_fail": true,
		"canvas_only": true,
	}


func probe_complete() -> bool:
	if _busy or _button == null:
		return false
	_on_target_pressed()
	return true


func _announce_task() -> void:
	if m == null or _busy or not TASKS.has(room_id):
		return
	var task: Dictionary = TASKS[room_id] as Dictionary
	m.show_msg("Roshan", String(task["cue"]), "talk")
	m._say("roshan", "talk", 0.55)


func _process(delta: float) -> void:
	_elapsed += maxf(delta, 0.0)
	# Some established room activities mount one frame after the room stage.
	# Keep the pre-clean beat's single-instruction ownership if a sibling guide
	# appears after setup, without disturbing non-guide actors or props.
	_suppress_new_competing_guides()
	if _pointer != null and _pointer.visible and _target != null:
		_pointer.position = _target.position + Vector2(0.0,
			-118.0 + sin(_elapsed * 4.0) * 9.0)
		_pointer.rotation = sin(_elapsed * 2.7) * 0.045
	if _target != null and not _busy:
		var pulse: float = 1.0 + sin(_elapsed * 3.4) * 0.035
		_target.scale = (_target.get_meta("rest_scale") as Vector2) * pulse


func _build_visuals(task: Dictionary) -> void:
	var texture: Texture2D = load(String(task["texture"])) as Texture2D
	_target = _make_card("PolishTarget", texture,
		task["center"] as Vector2, float(task["target_longest"]),
		task["tint"] as Color, 2)
	_target.set_meta("rest_scale", _target.scale)
	_tool = _make_card("MagicCleaner", TOOL_TEXTURE,
		task["tool_start"] as Vector2, 108.0, Color.WHITE, 7)
	_tool.visible = false
	_wipe = _make_card("WipeSwoosh", WIPE_TEXTURE,
		task["center"] as Vector2, 220.0, Color.WHITE, 6)
	_wipe.visible = false
	_ring = _make_card("CleanRing", RING_TEXTURE,
		task["center"] as Vector2, 210.0, Color.WHITE, 5)
	_ring.visible = false
	_bubbles = _make_card("SoapBubbles", BUBBLE_TEXTURE,
		task["center"] as Vector2, 190.0, Color.WHITE, 5)
	_bubbles.visible = false
	_pointer = _make_card("TargetPointer", POINTER_TEXTURE,
		(task["center"] as Vector2) + Vector2(0.0, -118.0),
		128.0, Color.WHITE, 10)
	_button = Button.new()
	_button.name = "PolishTargetButton"
	_button.position = (task["center"] as Vector2) \
		- (task["hit_size"] as Vector2) * 0.5
	_button.size = task["hit_size"] as Vector2
	_button.flat = true
	_button.focus_mode = Control.FOCUS_NONE
	_button.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
	_button.mouse_filter = Control.MOUSE_FILTER_STOP
	_button.z_index = 20
	_button.pressed.connect(_on_target_pressed)
	add_child(_button)


func _make_card(card_name: String, texture: Texture2D, center: Vector2,
		longest: float, tint: Color, card_z: int) -> Sprite2D:
	var card := Sprite2D.new()
	card.name = card_name
	card.texture = texture
	card.position = center
	card.modulate = tint
	card.z_index = card_z
	if texture != null:
		var source_longest: float = maxf(
			texture.get_width(), texture.get_height())
		card.scale = Vector2.ONE * longest / maxf(source_longest, 1.0)
	add_child(card)
	return card


func _suppress_competing_guides() -> void:
	# The established room activities may already have mounted their own hand,
	# arrow, or doorway pointer. The saved pre-clean beat owns the only visual
	# instruction until it completes; preserve and restore those guide nodes so
	# the underlying activity resumes unchanged afterward.
	_suppressed_guides.clear()
	_suppress_new_competing_guides()


func _suppress_new_competing_guides() -> void:
	# Bathroom's established activity lives on a sibling overlay rather than
	# under the room stage, so search the owning main scene while still skipping
	# this polish subtree.
	var search_root: Node = m if m != null else get_parent()
	if search_root == null:
		return
	_suppress_guides_below(search_root)


func _suppress_guides_below(node: Node) -> void:
	for child: Node in node.get_children():
		if child == self:
			continue
		if child is CanvasItem:
			var item := child as CanvasItem
			var lower_name: String = item.name.to_lower()
			var is_guide: bool = "pointer" in lower_name \
				or "ghosthand" in lower_name or "ghost_hand" in lower_name \
				or "arrowguide" in lower_name or "arrow_guide" in lower_name
			if is_guide and item.visible:
				_suppressed_guides.append(item)
				item.visible = false
		_suppress_guides_below(child)


func _restore_competing_guides() -> void:
	for item: CanvasItem in _suppressed_guides:
		if is_instance_valid(item):
			item.visible = true
	_suppressed_guides.clear()


func _on_target_pressed() -> void:
	if _busy or m == null:
		return
	_busy = true
	_button.disabled = true
	_pointer.visible = false
	m._ui_tap()
	# Save the single new beat before its animation. A quit during the wipe can
	# only resume farther forward, never restore dirt the child already cleaned.
	if not m.day_one_complete_room_polish(room_id):
		_busy = false
		_button.disabled = false
		_pointer.visible = true
		return
	var task: Dictionary = TASKS[room_id] as Dictionary
	_tool.visible = true
	_tool.position = task["tool_start"] as Vector2
	var target_center: Vector2 = task["center"] as Vector2
	var wipe := create_tween()
	wipe.tween_property(_tool, "position", target_center,
		0.30).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	wipe.tween_callback(_begin_wipe_effect)
	wipe.tween_interval(0.34)
	wipe.tween_callback(_finish_wipe_effect)
	wipe.tween_interval(0.28)
	wipe.tween_callback(_complete_animation)


func _begin_wipe_effect() -> void:
	_wipe.visible = true
	_wipe.modulate.a = 1.0
	_wipe.scale *= 0.68
	_ring.visible = true
	_ring.modulate.a = 0.82
	_ring.scale *= 0.48
	_bubbles.visible = true
	_bubbles.modulate.a = 0.92
	var fx := create_tween().set_parallel(true)
	fx.tween_property(_target, "modulate:a", 0.0, 0.48)
	fx.tween_property(_target, "rotation", 0.16, 0.20)
	fx.tween_property(_wipe, "scale", _wipe.scale * 1.55, 0.42)
	fx.tween_property(_wipe, "modulate:a", 0.0, 0.42)
	fx.tween_property(_ring, "scale", _ring.scale * 2.25, 0.48)
	fx.tween_property(_ring, "modulate:a", 0.0, 0.48)
	fx.tween_property(_bubbles, "position:y", _bubbles.position.y - 42.0,
		0.52)
	fx.tween_property(_bubbles, "modulate:a", 0.0, 0.52)


func _finish_wipe_effect() -> void:
	var task: Dictionary = TASKS[room_id] as Dictionary
	var retreat: Vector2 = task["tool_start"] as Vector2
	var tool_tween := create_tween().set_parallel(true)
	tool_tween.tween_property(_tool, "position", retreat, 0.26)
	tool_tween.tween_property(_tool, "modulate:a", 0.0, 0.26)


func _complete_animation() -> void:
	m.show_msg("Roshan", "Sparkly! Now the next job is ready!", "win")
	m._say("roshan", "win", 0.45)
	completed.emit(room_id, task_id)
	teardown()
