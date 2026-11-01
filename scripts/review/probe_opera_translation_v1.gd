extends Node
## Explicit private-review integration probe. Never runs from normal gameplay.
## The successful callback leg is a presentation fixture, not a played win.

const OUTPUT := "C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/opera-four-screen-v1-20261031/assets_src/review/opera_exploration_v1/verification/"
var output_dir: String = OUTPUT
var venue: Node
var rows: Array[Dictionary] = []
var done := false
var phase := "starting"
var results: Dictionary = {}
var samples := 0
var island_clear := true
var floor_safe := true
var lift_samples := 0
var visual_floor_safe := true
var visual_alpha_cache: Dictionary = {}
var visual_image_cache: Dictionary = {}
var max_visual_floor_error := 0.0

func _ready() -> void:
	call_deferred("_run")

func _record(name: String, passed: bool, evidence: Variant = null) -> void:
	rows.append({"check":name,"result":"PASS" if passed else "FAIL","evidence":evidence})
	print("OPERA_TRANSLATION_PROBE|%s|%s" % [name,"PASS" if passed else "FAIL"])

func _wait(condition: Callable) -> bool:
	for index: int in range(1200):
		await get_tree().process_frame
		var point: Vector2 = venue.player_root.position
		island_clear = island_clear and not Rect2(1120,1085,315,255).has_point(point)
		if venue.riding_lift:
			lift_samples += 1
			floor_safe = floor_safe and (absf(point.x-438.0)<0.05 or absf(point.x-2120.0)<0.05) \
				and point.y>=372.0 and point.y<=1035.0
		else:
			floor_safe = floor_safe and venue.floor_navigation.contains_point(point)
		var visual_error: float = _visual_foot_error(venue.actor)
		var smoother: Node = venue.actor.get_node("TemporalSpriteTransition")
		var ghost: Sprite2D = smoother.transition_ghost()
		if ghost.visible:
			visual_error = maxf(visual_error,_visual_foot_error(ghost))
		max_visual_floor_error = maxf(max_visual_floor_error,visual_error)
		visual_floor_safe = visual_floor_safe and visual_error<=0.5
		samples += 1
		if bool(condition.call()):
			return true
	return false

func _visual_foot_error(sprite: Sprite2D) -> float:
	# Derive the GPU's actual sample independently of the placement helper.
	var sample := Rect2(Vector2.ZERO,sprite.texture.get_size())
	if sprite.region_enabled:
		sample = sprite.region_rect
	var cell: Vector2 = sample.size/Vector2(sprite.hframes,sprite.vframes)
	sample = Rect2(sample.position+Vector2(sprite.frame%sprite.hframes,
		floori(float(sprite.frame)/float(sprite.hframes)))*cell,cell)
	var texture_id: int = sprite.texture.get_instance_id()
	var key: String = "%d:%s" % [texture_id,str(sample)]
	if not visual_alpha_cache.has(key):
		if not visual_image_cache.has(texture_id):
			var image: Image = sprite.texture.get_image()
			if image.is_compressed():
				image.decompress()
			visual_image_cache[texture_id] = image
		var image: Image = visual_image_cache[texture_id] as Image
		visual_alpha_cache[key] = image.get_region(Rect2i(sample)).get_used_rect()
	var alpha: Rect2i = visual_alpha_cache[key] as Rect2i
	var local_foot := Vector2(sprite.get_rect().get_center().x,sprite.get_rect().position.y+float(alpha.end.y))
	var foot: Vector2 = venue.world.to_local(sprite.to_global(local_foot))
	return absf(foot.y-venue.player_root.position.y)

func _travel(point: Vector2) -> bool:
	venue.request_destination(point)
	return await _wait(func() -> bool: return venue.route.is_empty() and venue.job==null and not venue.busy)

func _capture(name: String) -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	var image: Image = get_viewport().get_texture().get_image()
	image.save_png(output_dir+name+".png")

func _run() -> void:
	if str(ProjectSettings.get_setting("application/config/custom_user_dir_name",""))!="MermaidReef-OperaRemovalReview-20261017":
		push_error("Refusing Opera review probe outside the isolated profile")
		return
	venue = get_tree().current_scene.find_child("OperaExplorationV1",true,false)
	if venue==null:
		push_error("Opera review is not open")
		return
	if venue.paused:
		venue._set_paused(false)
	var empty_review: Control = load("res://scripts/review/opera_translation_v1.gd").new() as Control
	_record("uninitialized review snapshot is safe",empty_review.review_snapshot().get("ready",true)==false)
	empty_review.free()
	var baseline_mask: int = venue.completed_mask
	var baseline_save_hash: int = venue.m.save_data.hash()
	var baseline_stars: int = venue.m.opera_stars
	var baseline_pearls: int = venue.m.pearl_count
	var initial_launches: int = venue.launches
	phase = "pause and focus"
	venue.cancel_travel()
	venue._set_paused(true)
	var paused_phase: float = venue.ambience.phase
	var paused_position: Vector2 = venue.player_root.position
	for index: int in range(12):
		await get_tree().process_frame
	_record("pause freezes travel and ambient time",venue.ambience.phase==paused_phase and venue.player_root.position==paused_position)
	venue._set_paused(false)
	venue.notification(NOTIFICATION_APPLICATION_FOCUS_OUT)
	var focus_stopped: bool = venue.paused and venue.focus_paused
	venue.notification(NOTIFICATION_APPLICATION_FOCUS_IN)
	_record("focus notification resumes only automatic pause",focus_stopped and not venue.paused and not venue.focus_paused)
	_record("passive no award",venue.completed_mask==baseline_mask and venue.m.opera_stars==baseline_stars)
	phase = "floor lock and bounded recovery"
	_record("lift shafts are excluded from ordinary floor lanes",
		not venue.floor_navigation.contains_point(Vector2(438,500))
		and not venue.floor_navigation.contains_point(Vector2(2120,850))
		and not venue.navigation.contains_point(Vector2(438,500))
		and not venue.floor_navigation.contains_point(Vector2(485,870)))
	venue._preview_pointer(Vector2(438,500)-venue.camera_position)
	_record("wall touch previews a real floor contact",venue.floor_navigation.contains_point(venue.marker.position))
	venue.cancel_travel()
	var safe_position: Vector2 = venue.player_root.position
	var recoveries_before: int = venue.floor_recoveries
	var recoveries_valid := true
	for invalid: Vector2 in [Vector2(-500,-500),Vector2(1280,780),Vector2(4000,4000),Vector2(INF,NAN)]:
		venue.player_root.position = invalid
		venue._process(0.0)
		recoveries_valid = recoveries_valid and venue.player_root.position==safe_position \
			and venue.route.is_empty() and venue.pending_object.is_empty()
	_record("off-floor and non-finite positions recover to the last floor contact",
		recoveries_valid and venue.floor_recoveries==recoveries_before+4)
	venue.request_destination(Vector2(INF,NAN))
	_record("invalid destination cannot create a route",venue.route.is_empty() and venue.player_root.position==safe_position)
	venue.request_destination(Vector2(438,340))
	var riding: bool = await _wait(func() -> bool: return venue.riding_lift and not venue.floor_navigation.contains_point(venue.player_root.position))
	venue.cancel_travel()
	_record("interrupted lift stops at a real landing",riding and not venue.riding_lift and venue.floor_navigation.contains_point(venue.player_root.position) and venue.route.is_empty())
	await _travel(Vector2(1280,1380))
	venue.request_destination(Vector2(2120,340))
	var riding_before_pause: bool = await _wait(func() -> bool: return venue.riding_lift and not venue.floor_navigation.contains_point(venue.player_root.position))
	venue._set_paused(true)
	_record("pausing a lift leaves Roshan at a floor landing",riding_before_pause and not venue.riding_lift and venue.floor_navigation.contains_point(venue.player_root.position) and venue.route.is_empty())
	venue._set_paused(false)
	await _travel(Vector2(1280,1380))
	var rides_before: int = venue.lift_rides
	var upper_floor: bool = await _travel(Vector2(1280,372))
	_record("cross-floor travel uses a controlled lift",upper_floor and venue.lift_rides>rides_before and venue.floor_navigation.contains_point(venue.player_root.position))
	await _capture("floor_locked_upper_gallery")
	await _travel(Vector2(1280,1380))
	phase = "routed native input"
	var motion := InputEventMouseMotion.new()
	motion.position = Vector2(500,500)
	motion.global_position = motion.position
	Input.parse_input_event(motion)
	await get_tree().process_frame
	var press := InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_LEFT
	press.position = motion.position
	press.global_position = motion.position
	press.pressed = true
	Input.parse_input_event(press)
	await get_tree().process_frame
	_record("routed mouse press responds within two frames",venue.marker.visible and venue.pointer_owner==-1)
	var release := InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_LEFT
	release.position = motion.position
	release.global_position = motion.position
	release.pressed = false
	Input.parse_input_event(release)
	await get_tree().process_frame
	_record("routed mouse release commits a destination",not venue.route.is_empty())
	venue.cancel_travel()
	var touch := InputEventScreenTouch.new()
	touch.index = 0
	touch.position = Vector2(500,500)
	touch.pressed = true
	Input.parse_input_event(touch)
	await get_tree().process_frame
	var drag := InputEventScreenDrag.new()
	drag.index = 0
	drag.position = Vector2(800,430)
	drag.relative = Vector2(300,-70)
	Input.parse_input_event(drag)
	await get_tree().process_frame
	var lifted := InputEventScreenTouch.new()
	lifted.index = 0
	lifted.position = drag.position
	lifted.pressed = false
	Input.parse_input_event(lifted)
	await get_tree().process_frame
	_record("routed one-finger drag commits a destination",not venue.route.is_empty() and venue.pointer_owner==-2)
	venue.cancel_travel()
	phase = "four-screen traversal"
	await _travel(Vector2(1280,1380))
	var left_top: bool = await _travel(Vector2(438,340))
	_record("left lift reaches original upper gallery",left_top and venue.player_root.position.distance_to(Vector2(438,372))<1.0)
	await _capture("operative_upper_left")
	# A lift stop is an action target. Choose gallery floor beside it when
	# testing horizontal travel, then tap the lift itself for the ride leg.
	venue.request_destination(Vector2(2030,372))
	for index: int in range(12):
		await get_tree().process_frame
	var frame_a: int = venue.animator.get("_displayed_frame")
	await _capture("authored_swim_a")
	for index: int in range(13):
		await get_tree().process_frame
	var frame_b: int = venue.animator.get("_displayed_frame")
	await _capture("authored_swim_b")
	_record("authored swim advances during travel",frame_a!=frame_b and venue.animator.animation_state()=="swim",[frame_a,frame_b])
	var right_top: bool = await _wait(func() -> bool: return venue.route.is_empty())
	_record("upper gallery connects across screen boundary",right_top and venue.player_root.position.distance_to(Vector2(2030,372))<1.0)
	await _capture("operative_upper_right")
	var right_ground: bool = await _travel(Vector2(2120,1035))
	_record("right lift reaches original foyer",right_ground and venue.player_root.position.distance_to(Vector2(2120,1035))<1.0)
	await _capture("operative_lower_right")
	var left_ground: bool = await _travel(Vector2(800,1035))
	_record("foyer connects across screen boundary",left_ground and venue.player_root.position.distance_to(Vector2(800,1035))<1.0)
	await _capture("operative_lower_left")
	phase = "cancellation"
	venue.request_destination(Vector2(1412,900))
	for index: int in range(5):
		await get_tree().process_frame
	venue.cancel_travel()
	var cancelled_position: Vector2 = venue.player_root.position
	for index: int in range(12):
		await get_tree().process_frame
	_record("cancel stops travel and queued door",venue.player_root.position==cancelled_position and venue.launches==initial_launches and venue.completed_mask==baseline_mask)
	phase = "interactive original props"
	var prior_responses: int = venue.prop_responses
	var counter: bool = await _travel(Vector2(630,940))
	_record("ticket counter responds after approach",counter and venue.prop_responses==prior_responses+1 and venue.ambience.bell_burst>0)
	await _capture("operative_counter_response")
	var tea: bool = await _travel(Vector2(2360,1150))
	_record("refreshment cart responds after approach",tea and venue.prop_responses==prior_responses+2 and venue.ambience.tea_burst>0)
	await _capture("operative_cart_response")
	phase = "activity cancellation and exact return"
	venue.request_destination(Vector2(1412,900))
	var launched: bool = await _wait(func() -> bool: return venue.job!=null)
	_record("physical doorway starts shipping private practice",launched and venue.running_act==2 and venue.job.dev_playtest)
	if launched:
		var source_position: Vector2 = venue.return_position
		var source_camera: Vector2 = venue.return_camera
		venue.job._leave_early()
		await get_tree().process_frame
		_record("cancel returns to exact source position and camera",venue.job==null and venue.player_root.position==source_position and venue.camera_position==source_camera and venue.completed_mask==baseline_mask)
	phase = "successful callback presentation fixture"
	venue.request_destination(Vector2(1412,900))
	var fixture_started: bool = await _wait(func() -> bool: return venue.job!=null)
	if fixture_started:
		var house: OperaHouse = venue.job
		if house.act!=null:
			house.act.cancel()
			house.act = null
		house.act_index = -1
		house._finish(true)
		await get_tree().process_frame
		_record("successful callback marks corresponding physical crest",venue.completed_mask==(baseline_mask|(1<<2)) and venue.badges[2].visible)
		await _capture("completion_callback_fixture")
		var completed_mask: int = venue.completed_mask
		venue._job_finished(true)
		_record("stale callback cannot award again",venue.completed_mask==completed_mask and venue.running_act==-1)
		venue.completed_mask = baseline_mask
		venue._refresh_badges()
	else:
		_record("successful callback fixture could start",false)
	_record("normal progress and practice saves unchanged",venue.m.opera_stars==baseline_stars and venue.m.pearl_count==baseline_pearls and venue.m.save_data.hash()==baseline_save_hash)
	_record("routes avoid central seating footprint",island_clear,{"samples":samples})
	_record("every sampled movement stays on floor or a controlled lift",floor_safe and lift_samples>0,{"samples":samples,"lift_samples":lift_samples})
	_record("approved atlas and blend silhouette stay at the painted floor contact",visual_floor_safe,{"maximum_error_pixels":max_visual_floor_error})
	_record("runtime samples the displayed256pixel cell",venue.actor.region_enabled and venue.actor.region_rect.size==Vector2(256,256) and venue.actor.hframes==1 and venue.actor.vframes==1)
	phase = "restore exploration starting point"
	await _travel(Vector2(1280,1380))
	await _capture("operative_final_foyer")
	var failures := 0
	for row: Dictionary in rows:
		if row["result"]=="FAIL":
			failures += 1
	results = {"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),
		"profile":ProjectSettings.get_setting("application/config/custom_user_dir_name"),
		"scope":"Private runtime integration; successful completion is a declared callback fixture, not an end-to-end played win",
		"checks":rows,"failed":failures,"final":venue.review_snapshot(),"baseline_save_hash":baseline_save_hash,"final_save_hash":venue.m.save_data.hash()}
	var file: FileAccess = FileAccess.open(output_dir+"focused_runtime.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(results,"\t")+"\n")
	done = true
	phase = "finished"
	print("OPERA_TRANSLATION_PROBE|RESULT|%s" % ("ALL OK" if failures==0 else "FAIL"))
