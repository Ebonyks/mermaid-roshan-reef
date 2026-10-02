class_name OperaNurserySurface
extends OperaGestureSurface
## Connected washing presentation only. CareerWorld owns hold progress,
## completion, route, score and saves. Other Nursery phases keep shared input/drawing.

const WASH_ROOT := "res://assets/opera/worlds/nursery/wash_connected_v1_20261002/"
const WASH_STATES: Array[String] = ["ready", "wet", "rub_palm", "rub_back", "rinse", "clean"]
const WASH_FILES: Array[String] = ["ready", "wet", "rub_palm02", "rub_back", "rinse", "clean"]
var wash_textures: Array[Texture2D] = []
var wash_state := "ready"


func _is_wash() -> bool:
	return mode == "hold" and visual_context in ["nursery_wash", "basin_nursery"]


func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	super.configure(next_mode, next_accent, choice, next_context)
	wash_state = "ready"
	if not _is_wash():
		return
	# The historical nursery prefix selected an empty generic widget family.
	# This specialist binds the same hold to the connected painted action.
	widget_template = ""
	if wash_textures.is_empty():
		for filename: String in WASH_FILES:
			wash_textures.append(load(WASH_ROOT + filename + ".png") as Texture2D)
	queue_redraw()


func _wash_state_index() -> int:
	if completion_accepted:
		return 5
	if widget_fill <= 0.0 or armed_only:
		return 0
	if widget_fill < 0.18:
		return 1
	if widget_fill < 0.42:
		return 2
	if widget_fill < 0.68:
		return 3
	return 4


func _demo_finger_pose() -> Dictionary:
	if not _is_wash():
		return super._demo_finger_pose()
	return {"at": size * Vector2(0.74, 0.55), "pressing": fmod(demo_t, 2.8) < 1.8}


func _draw() -> void:
	if not _is_wash():
		super._draw()
		return
	var index := _wash_state_index()
	wash_state = WASH_STATES[index]
	last_contextual_draw_route = "nursery_connected_wash:" + wash_state
	last_specialist_subject_route = "nursery_connected_wash"
	last_widget_ground_route = "painted_connected_nursery"
	if wash_textures.size() != WASH_STATES.size() or wash_textures[index] == null:
		push_error("Nursery wash: missing reviewed whole-canvas action painting")
		return
	draw_texture_rect(wash_textures[index], Rect2(Vector2.ZERO, size), false)
	if demo_active and not completion_accepted:
		_draw_demo_finger()
