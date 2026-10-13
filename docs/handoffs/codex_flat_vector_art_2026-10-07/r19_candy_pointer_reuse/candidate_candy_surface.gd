extends OperaGestureSurface
## R19 isolated source-review trial. One whole existing R16 hand; Candy SYRUP only.
const TRIAL_SOURCE := "res://assets_src/flat_vector_pointer_20261013/pointer_1024.png"
const TIP_UV := Vector2(0.44580078125, 0.90625)
var trial_texture: Texture2D

func _trial_texture() -> Texture2D:
	if trial_texture == null:
		var image := Image.load_from_file(TRIAL_SOURCE)
		assert(image != null and not image.is_empty(), "R19 diagnostic candidate missing")
		trial_texture = ImageTexture.create_from_image(image)
	return trial_texture

func hand_contract() -> Dictionary:
	var pose: Dictionary = _demo_finger_pose()
	var at: Vector2 = pose.get("at", size * 0.5)
	var pressing: bool = pose.get("pressing", false)
	var side: float = 58.0 if pressing else 54.0
	var rect := Rect2(at - TIP_UV * side, Vector2.ONE * side)
	var tip := rect.position + TIP_UV * side
	return {"source":TRIAL_SOURCE,"source_sha256":FileAccess.get_sha256(TRIAL_SOURCE),"script_sha256":FileAccess.get_sha256("res://.godot/r19_candy_pointer_surface.gd"),"candidate_loaded":_trial_texture() != null,"candidate_draw_active":demo_active and _is_candymaker_pour(),"pressing":pressing,"side":side,"target":[at.x,at.y],"tip":[tip.x,tip.y],"rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"tip_error":tip.distance_to(at),"whole_texture_draw_count":1,"old_hand_field_required":false}

func _draw_demo_finger() -> void:
	if not _is_candymaker_pour():
		super._draw_demo_finger()
		return
	var pose: Dictionary = _demo_finger_pose()
	var at: Vector2 = pose.get("at", size * 0.5)
	var pressing: bool = pose.get("pressing", false)
	var side: float = 58.0 if pressing else 54.0
	draw_texture_rect(_trial_texture(), Rect2(at - TIP_UV * side, Vector2.ONE * side), false, Color(1.0, 1.0, 1.0, 0.96))
