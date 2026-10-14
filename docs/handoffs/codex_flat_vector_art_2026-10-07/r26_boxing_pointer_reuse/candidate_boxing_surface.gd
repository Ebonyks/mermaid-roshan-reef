extends OperaBoxingSurface
## R26 nonruntime existing whole R16 hand reuse; original input/demo state inherited.
const TRIAL_SOURCE := "res://assets_src/flat_vector_pointer_20261013/pointer_1024.png"
const TIP_UV := Vector2(0.44580078125, 0.90625)
const HAND_SIDE := 82.0
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
	return {"trial_enabled":trial_enabled,"source":TRIAL_SOURCE,"source_sha256":FileAccess.get_sha256(TRIAL_SOURCE),"prototype_sha256":FileAccess.get_sha256("res://.godot/r26_boxing_pointer_surface.gd"),"last_callback":last_guide_draw.duplicate(true),"whole_source_transform":"Rigid glove-to-mitt ray rotation + uniform82px square,alpha0.96;no crop/recolor/deformation/parts","callback_limit":"Last draw-helper snapshot,not QA11/GPU measurement;may be stale when hidden or between redraws","missing_source_scope":"Original helper fallback exists only in isolated trial;missing package not physically tested/retired;production unchanged"}

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
	# Original demonstration geometry and mode/hand timing copied unchanged.
	var cycle := fmod(demo_t, 2.4) / 2.4
	var hand := int(floor(fmod(demo_t, 4.8) / 2.4))
	var start := glove_rest_position(hand)
	var target := active_target_position()
	if mode == "boxing_guide":
		target = guide_target_position(hand)
	elif mode == "boxing_guard":
		hand = _guard_side
		start = glove_rest_position(hand)
		target = guard_target_position(hand)
	elif mode == "boxing_belt":
		target = active_target_position()
	var travel := clampf(cycle / 0.72, 0.0, 1.0)
	travel = travel * travel * (3.0 - 2.0 * travel)
	var at := start.lerp(target, travel)
	var rotation := (target-start).angle()-PI*0.5
	var rect := Rect2(-TIP_UV*HAND_SIDE, Vector2.ONE*HAND_SIDE)
	var local_tip := rect.position+TIP_UV*rect.size
	var tip := at+local_tip.rotated(rotation)
	last_guide_draw = {"route":"whole_painted_source","demo_t":demo_t,"hand":hand,"start":[start.x,start.y],"goal":[target.x,target.y],"travel":travel,"target":[at.x,at.y],"tip":[tip.x,tip.y],"tip_error":tip.distance_to(at),"side":HAND_SIDE,"rotation_radians":rotation,"texture_rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"declared_whole_texture_commands":1,"callback_time_usec":Time.get_ticks_usec()}
	draw_set_transform(at, rotation)
	draw_texture_rect(texture, rect, false, Color(1.0,1.0,1.0,0.96))
	draw_set_transform(Vector2.ZERO)
