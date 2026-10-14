extends OperaBalletSurface
## R24 nonruntime whole R16 hand reuse. Source unaccepted;input/demo behavior inherited.
const TRIAL_SOURCE := "res://assets_src/flat_vector_pointer_20261013/pointer_1024.png"
const TIP_UV := Vector2(0.44580078125,0.90625)
const HAND_ROTATION := 2.443460952792061
var trial_enabled: bool = false
var trial_texture: Texture2D
var last_guide_draw: Dictionary = {}

func _trial_texture() -> Texture2D:
	if trial_texture == null:
		var image := Image.load_from_file(TRIAL_SOURCE)
		if image == null or image.is_empty():
			return null
		trial_texture = ImageTexture.create_from_image(image)
	return trial_texture

func pointer_contract() -> Dictionary:
	return {"trial_enabled":trial_enabled,"source":TRIAL_SOURCE,"source_sha256":FileAccess.get_sha256(TRIAL_SOURCE),"prototype_sha256":FileAccess.get_sha256("res://.godot/r24_ballet_pointer_surface.gd"),"last_callback":last_guide_draw.duplicate(true),"whole_source_transform":"Rigid140degree rotation+uniform98idle/88pressed square;no crop,recolor,pixel edit,parts/UV deformation","callback_limit":"Last helper callback record,not QA11 projection or GPU measurement;may be stale when caller guard hides guide","missing_source_scope":"Original helper fallback exists in isolated trial only;missing package not tested or retired;production unchanged"}

func _draw_ghost_finger(at: Vector2, pressing: bool) -> void:
	if not trial_enabled:
		last_guide_draw = {"route":"original_flat","target":[at.x,at.y],"pressing":pressing}
		super._draw_ghost_finger(at,pressing)
		return
	var texture := _trial_texture()
	if texture == null:
		last_guide_draw = {"route":"original_flat_missing_reference","target":[at.x,at.y],"pressing":pressing}
		super._draw_ghost_finger(at,pressing)
		return
	var side: float = 88.0 if pressing else 98.0
	var rect := Rect2(-TIP_UV*side,Vector2.ONE*side)
	var local_tip := rect.position+TIP_UV*rect.size
	var tip := at+local_tip.rotated(HAND_ROTATION)
	last_guide_draw = {"route":"whole_painted_source","target":[at.x,at.y],"tip":[tip.x,tip.y],"tip_error":tip.distance_to(at),"pressing":pressing,"side":side,"rotation_radians":HAND_ROTATION,"texture_rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"declared_whole_texture_commands":1,"callback_time_usec":Time.get_ticks_usec()}
	draw_set_transform(at,HAND_ROTATION)
	draw_texture_rect(texture,rect,false,Color(1.0,1.0,1.0,0.96))
	draw_set_transform(Vector2.ZERO)
