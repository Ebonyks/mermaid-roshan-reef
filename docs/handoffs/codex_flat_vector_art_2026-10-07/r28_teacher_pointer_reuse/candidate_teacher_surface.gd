extends OperaTeacherSurface
## R28 nonruntime whole existing hand; source lesson/touch/save policies inherited.
const TRIAL_SOURCE := "res://assets_src/flat_vector_pointer_20261013/pointer_1024.png"
const TIP_UV := Vector2(0.44580078125, 0.90625)
const TARGET_SIDE := 80.0
const ANSWER_SIDE := 72.0
var trial_enabled: bool = false
var trial_texture: Texture2D
var last_guide_draw: Dictionary = {}

func _trial_texture() -> Texture2D:
	if trial_texture == null:
		var source := Image.load_from_file(TRIAL_SOURCE)
		if source == null or source.is_empty():
			return null
		trial_texture = ImageTexture.create_from_image(source)
	return trial_texture

func pointer_contract() -> Dictionary:
	return {"trial_enabled":trial_enabled,"source":TRIAL_SOURCE,"source_sha256":FileAccess.get_sha256(TRIAL_SOURCE),"prototype_sha256":FileAccess.get_sha256("res://.godot/r28_teacher_pointer_surface.gd"),"last_callback":last_guide_draw.duplicate(true),"whole_source_transform":"RigidPIrotation + uniform80px join/counter or72px answer,alpha0.96;no crop/recolor/mirror/deformation/parts","callback_limit":"Last actual draw-helper snapshot,not QA11/GPU projection;may be stale between redraws","missing_source_scope":"Original helper fallback exists only in isolated trial;missingpackage not physicallytested/retired;production unchanged"}

func _draw_demo() -> void:
	if not trial_enabled:
		last_guide_draw = {"route":"original_flat","callback_time_usec":Time.get_ticks_usec()}
		super._draw_demo()
		return
	var texture := _trial_texture()
	if texture == null:
		last_guide_draw = {"route":"original_flat_missing_reference","callback_time_usec":Time.get_ticks_usec()}
		super._draw_demo()
		return
	var center := Vector2.ZERO
	var at := Vector2.ZERO
	var role := "NONE"
	var eligible := false
	var side := TARGET_SIDE
	if lesson_kind() == "add" and not joined:
		center = JOIN_CENTER
		at = center + Vector2(0,28)
		role = "JOIN_BUTTON"
		eligible = at.distance_to(JOIN_CENTER) <= 65.0
	elif counted.has(false):
		if join_t > 0.0:
			last_guide_draw = {"route":"hidden_until_counter_actionable","join_t":join_t,"declared_whole_texture_commands":0,"callback_time_usec":Time.get_ticks_usec()}
			return
		center = counter_position(counted.find(false))
		at = center + Vector2(0,20)
		role = "NEXT_UNTOUCHED_COUNTER"
		eligible = at.distance_to(center) <= 36.0
	elif help_visible and can_answer():
		var card := choice_rect(answer_index())
		center = card.get_center()
		at = center + Vector2(0,55)
		role = "CORRECT_ANSWER_CARD"
		side = ANSWER_SIDE
		eligible = card.has_point(at)
	if role == "NONE" or not eligible:
		last_guide_draw = {"route":"hidden_no_eligible_guide","declared_whole_texture_commands":0,"callback_time_usec":Time.get_ticks_usec()}
		return
	var rect := Rect2(-TIP_UV*side,Vector2.ONE*side)
	var local_tip := rect.position+TIP_UV*rect.size
	var tip := at+local_tip.rotated(PI)
	last_guide_draw = {"route":"whole_painted_source","target_role":role,"center":[center.x,center.y],"target":[at.x,at.y],"tip":[tip.x,tip.y],"tip_error":tip.distance_to(at),"eligible_target":eligible,"join_t":join_t,"side":side,"rotation_radians":PI,"texture_rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"declared_whole_texture_commands":1,"callback_time_usec":Time.get_ticks_usec()}
	draw_set_transform(at,PI)
	draw_texture_rect(texture,rect,false,Color(1.0,1.0,1.0,0.96))
	draw_set_transform(Vector2.ZERO)
