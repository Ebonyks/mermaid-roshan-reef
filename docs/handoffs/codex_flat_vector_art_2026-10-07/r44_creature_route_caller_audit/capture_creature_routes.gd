extends SceneTree
## R44 current authored-route vs forced legacy API source audit; private synthetic saves only.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var active_id := ""
var initial_seed: Dictionary = {}

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result


func _wait_frames(count: int) -> void:
	for i: int in range(count):
		await process_frame


func _set_aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var test: Image = get_root().get_texture().get_image()
		if test != null and test.get_size() == target:
			return true
	return false


func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}


func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false


func _retire_main() -> void:
	m.set_process(false)
	m.queue_free()
	await _wait_frames(10)
	m = null


func _overlay() -> Control:
	if m.companion_stage != null:
		return m.companion_stage
	return m.companion_care_stage

func _tap(name: String) -> bool:
	for attempt: int in range(90):
		var stage: Control=_overlay()
		var button: Button=stage.find_child(name,true,false) as Button if stage != null else null
		if button==null or not is_instance_valid(button) or button.is_queued_for_deletion() or not button.is_visible_in_tree() or button.disabled:
			await process_frame
			continue
		var where: Vector2=button.get_global_rect().get_center()
		var move:=InputEventMouseMotion.new()
		move.position=where
		move.global_position=where
		get_root().push_input(move,true)
		await _wait_frames(2)
		if not is_instance_valid(button) or button.is_queued_for_deletion() or get_root().gui_get_hovered_control()!=button:
			continue
		for pressed: bool in [true,false]:
			var event:=InputEventMouseButton.new()
			event.button_index=MOUSE_BUTTON_LEFT
			event.pressed=pressed
			event.position=where
			event.global_position=where
			get_root().push_input(event,true)
			await process_frame
		await _wait_frames(4)
		return true
	errors.append("actual pointer readiness/transition failed "+name)
	return false

func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var item:=node as CanvasItem
	if item!=null and item.is_visible_in_tree():
		var row: Dictionary={"path":str(node.get_path()),"class":node.get_class(),"z_index":item.z_index,"modulate":str(item.modulate)}
		var control:=node as Control
		if control!=null:
			row["global_rect"]=str(control.get_global_rect())
		var tr:=node as TextureRect
		if tr!=null and tr.texture!=null:
			row["texture"]=tr.texture.resource_path
			row["texture_size"]=str(tr.texture.get_size())
			row["scale"]=str(tr.scale)
			row["stretch_mode"]=tr.stretch_mode
		var sprite:=node as Sprite2D
		if sprite!=null and sprite.texture!=null:
			row["texture"]=sprite.texture.resource_path
			row["source_asset_path"]=str(sprite.get_meta("source_asset_path",""))
		var button:=node as Button
		if button!=null:
			row["disabled"]=button.disabled
			row["text"]=button.text
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child,rows)

func _actor_rows(root: Node, result: Array[Dictionary]) -> void:
	if root==null or not is_instance_valid(root):
		return
	var row: Dictionary={"class":root.get_class(),"name":String(root.name),"path":str(root.get_path()) if root.is_inside_tree() else "<detached>"}
	var spatial:=root as Node3D
	if spatial!=null:
		row["visible_flag"]=spatial.visible
		row["visible_in_tree_flag"]=spatial.is_visible_in_tree()
		row["position"]=str(spatial.position)
		row["global_position"]=str(spatial.global_position) if spatial.is_inside_tree() else "<detached>"
		row["scale"]=str(spatial.scale)
	var sprite:=root as Sprite3D
	if sprite!=null:
		row["texture"]=sprite.texture.resource_path if sprite.texture!=null else ""
		row["texture_size"]=str(sprite.texture.get_size()) if sprite.texture!=null else ""
		row["tint"]=str(sprite.modulate)
		row["pixel_size"]=sprite.pixel_size
		row["billboard"]=sprite.billboard
		row["render_priority"]=sprite.render_priority
		var material: Material=sprite.material_override
		if material!=null:
			row["material_class"]=material.get_class()
			var shader_material:=material as ShaderMaterial
			if shader_material!=null and shader_material.shader!=null:
				row["shader_code_sha256"]=shader_material.shader.code.sha256_text()
				var parameters: Dictionary={}
				for uniform: Dictionary in shader_material.shader.get_shader_uniform_list():
					var key:=String(uniform.get("name",""))
					var value: Variant=shader_material.get_shader_parameter(key)
					parameters[key]=str(value)
				row["shader_parameters"]=parameters
	var mesh:=root as MeshInstance3D
	if mesh!=null:
		row["mesh_class"]=mesh.mesh.get_class() if mesh.mesh!=null else ""
	var camera:=root as Camera3D
	if camera!=null:
		row["current"]=camera.current
		row["fov"]=camera.fov
	result.append(row)
	for child: Node in root.get_children():
		_actor_rows(child,result)

func _camera() -> Dictionary:
	var camera: Camera3D=get_root().get_camera_3d()
	return {"present":camera!=null,"path":str(camera.get_path()) if camera!=null else "","current":camera.current if camera!=null else false,"global_position":str(camera.global_position) if camera!=null else ""}

func _layers() -> Array[Dictionary]:
	var result: Array[Dictionary]=[]
	for node: Node in m.find_children("*","CanvasLayer",true,false):
		var layer:=node as CanvasLayer
		result.append({"path":str(layer.get_path()),"layer":layer.layer,"visible":layer.visible})
	return result

func _actor_state(root: Node) -> Dictionary:
	if root==null or not is_instance_valid(root):
		return {"present":false,"nodes":[]}
	var rows: Array[Dictionary]=[]
	_actor_rows(root,rows)
	return {"present":true,"nodes":rows}

func _capture(id: String, context: String, detail: String="") -> void:
	await RenderingServer.frame_post_draw
	var image: Image=get_root().get_texture().get_image()
	if image==null or image.get_size()!=get_root().size:
		errors.append("framebuffer mismatch "+id)
		return
	var path:=out_dir.path_join(id+".png")
	if image.save_png(path)!=OK:
		errors.append("PNGwrite "+id)
		return
	var comp: CompanionSystem=m._companion_ref()
	var nodes: Array[Dictionary]=[]
	for layer: CanvasLayer in [m.companion_layer,m.companion_care_layer,m.castle_room_layer]:
		if layer!=null:
			_nodes(layer,nodes)
	states.append({"id":id,"context_class":context,"detail":detail,"image":{"file":id+".png","bytes":FileAccess.get_file_as_bytes(path).size(),"sha256":FileAccess.get_sha256(path),"dimensions":[image.get_width(),image.get_height()]},"game":m.game,"phase":m.g.get("phase",""),"authored_world_session":m._authored_world_session,"source_calls":comp.get("audit_calls").duplicate(true),"source_events":comp.get("audit_events").duplicate(true),"follow_context_predicate":comp._follow_ctx(),"camera3D":_camera(),"Canvas_layers":_layers(),"follower":_actor_state(m.companion_node),"Studio":_actor_state(m.companion_room),"battle":_actor_state(m.stuffie_game),"Canvas_nodes":nodes,"companion_id":m.companion_id,"companion_colors":m.companion_colors.duplicate(),"care_points":m.care_points,"stuffie_wins":m.stuffie_wins.duplicate(),"normal_save_hashes":_normal_hashes(),"presentation":_presentation(),"actual_child_data":false,"art_context_credit":false,"scope":"Source/dispatch/camera/constructed-resource diagnostic;no normalroute/uniqueartwork/visibility/QA11/device/child/owner/acceptedremoval credit."})
	print("CREATURE44|CAPTURE|"+id)

func _factory_diagnostics() -> Array[Dictionary]:
	var result: Array[Dictionary]=[]
	for kind: String in ["fish","cat","bird"]:
		for third: Color in [Color.BLACK,Color.WHITE]:
			var actor: Node3D=m._make_creature_node(kind,Color(0.95,0.70,0.85),Color(0.60,0.40,0.90),false,false,third)
			if actor==null:
				errors.append("factory null "+kind)
				continue
			m.add_child(actor)
			await _wait_frames(3)
			var row: Dictionary={"kind":kind,"body_input":"f2b3d9","accent_input":"9966e6","third_input":third.to_html(false),"forced_API_only":true,"actor":_actor_state(actor)}
			result.append(row)
			actor.free()
			await _wait_frames(2)
	return result

func _seed() -> Dictionary:
	return {"schema_version":1,"won":{},"found":{},"plays":0,"pearls":23,"pearls_ever":23,"music":false,"mic":false,"quality":"speedy","companion":active_id,"companion_colors":[],"care_points":8,"stuffie_wins":{"rescued_eagle":true,"friend_lamma":true},"crafts":{},"stickers":{},"custom_fish":[[0.9,0.3,0.3,1.0,0.8,0.2],[0.2,0.7,0.8,0.9,0.3,0.4,1,0]],"custom_friends":[["cat",0.95,0.7,0.85,0.6,0.4,0.9],["bird",1.0,0.85,0.3,0.3,0.8,0.9,0,1],["cat",0.95,0.7,0.85,0.6,0.4,0.9,1,0,0.97,0.96,0.93]]}

func _new_main(profile: String) -> bool:
	var scene:=load("res://scenes/main.tscn") as PackedScene
	m=scene.instantiate() as ReefMain
	m._save_state=SaveState.new(m,profile)
	m._companion_system=load("res://docs/handoffs/codex_flat_vector_art_2026-10-07/r44_creature_route_caller_audit/observe_companion.gd").new(m)
	get_root().add_child(m)
	await _wait_frames(3)
	m._apply_quality("speedy")
	m.day_one_active=false
	if m.start_menu_active:
		m._start_menu_ref()._dismiss_menu()
	if m.intro_active:
		m._skip_intro()
	if not await _wait_presentation():
		errors.append("startup presentation did not settle")
		return false
	return true

func _run() -> void:
	var engine:=Engine.get_version_info()
	if int(engine.get("major",0))!=4 or int(engine.get("minor",0))!=7 or int(engine.get("patch",0))!=2 or String(engine.get("status",""))!="stable" or String(engine.get("build",""))!="official" or RenderingServer.get_current_rendering_method()!="mobile" or DisplayServer.get_name()=="headless":
		print("CREATURE44|FAIL|engine/renderer/display")
		quit(1)
		return
	active_id=OS.get_environment("R44_ID")
	var width: int=int(OS.get_environment("R44_WIDTH"))
	var base_out:=OS.get_environment("R44_OUT")
	if active_id not in ["mewsha","eagle","lamma"] or width not in [1280,1600] or base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("CREATURE44|FAIL|exact new job output/id/aspect required")
		quit(1)
		return
	normal_before=_normal_hashes()
	out_dir=base_out
	DirAccess.make_dir_recursive_absolute(out_dir)
	if not await _set_aspect(Vector2i(width,720)):
		quit(1)
		return
	var profile:=out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	initial_seed=_seed()
	var seed_file:=FileAccess.open(profile,FileAccess.WRITE)
	seed_file.store_string(JSON.stringify(initial_seed,"\t",true)+"\n")
	seed_file.close()
	if not await _new_main(profile):
		await _retire_main()
		quit(1)
		return
	var comp: CompanionSystem=m._companion_ref()
	comp.set("audit_phase","normal_source_owner_entry")
	m.level2_done_once=true
	m._enter_level2_now(true,false,false)
	await _wait_frames(70)
	await _capture("promenade_idle","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Existing entryowner;normal Canvasdispatch,notnaturalplaycompletion")
	comp.open_care_menu()
	await _wait_frames(6)
	await _capture("promenade_care","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Existing guardedcaremenu;source-renderer unchanged")
	comp.close_care_menu()
	await _wait_frames(6)
	m._enter_castle_interior_now(false)
	await _wait_frames(70)
	await _capture("Castle_idle","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Observe normalhall dispatch;do notforceStudio orfollower")
	m._castle_rooms_ref()._exit_to_courtyard()
	await _wait_frames(45)
	await _capture("Castle_exit_to_promenade","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Actual productionexit callback")
	comp.set("audit_phase","forced_sparring_API")
	m._start_stuffie_battle()
	await _wait_frames(12)
	await _capture("forced_battle_start","FORCED_PRIVATE_API_ONLY","No named productionentrycurrentlyboundbyscan;do nothideCanvas oraddcamera toforcevisibility")
	await _wait_frames(35)
	await _capture("forced_battle_wait","FORCED_PRIVATE_API_ONLY","Passivefewframes;notbattleaction/route/acceptance")
	if m.stuffie_game==null:
		errors.append("existing battleAPI failed toconstruct")
	else:
		m.stuffie_game.cancel()
	await _wait_frames(35)
	await _capture("forced_battle_cancel","FORCED_PRIVATE_API_ONLY","Actual retainedengine cancellationcallback;no victoryfabrication")
	comp.set("audit_phase","authored_reentry_after_diagnostic")
	m._enter_level2_now(true,false,false)
	await _wait_frames(16)
	m._enter_castle_interior_now(false)
	await _wait_frames(20)
	await _capture("Castle_reentry","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Sourceowner reentry afterexistingAPIcancel")
	comp.set("audit_phase","forced_Studio_constructor")
	comp._build_room()
	await _wait_frames(6)
	await _capture("forced_Studio_build","FORCED_PRIVATE_API_ONLY","Direct existingconstructor,notlegitimate entry;keepopaqueCanvas/cameraownership unchanged")
	if m.companion_room!=null and is_instance_valid(m.companion_room):
		m.game_nodes.erase(m.companion_room)
		m.companion_room.free()
	m.companion_room=null
	m.companion_room_rows=[]
	await _wait_frames(6)
	await _capture("forced_Studio_cleanup","FORCED_PRIVATE_API_ONLY","Freeonly owneddiagnosticroom exactly;othereditor untouched")
	var factories: Array[Dictionary]=[]
	if active_id=="mewsha" and width==1280:
		comp.set("audit_phase","forced_Main_factory_pairs")
		factories=await _factory_diagnostics()
		await _capture("forced_Main_factory_cleanup","FORCED_PRIVATE_API_ONLY","Six originalfactoryinvocations fish/cat/bird,thirdblack/white;no fixtureart/camera")
	comp.set("audit_phase","source_exit_route")
	m._exit_level2_now("reef")
	await _wait_frames(35)
	await _capture("retained_exit_requests_reef","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Record actual target-ignored authoredCanvas return;notlegacyreefcoverage")
	m._write_save()
	var before_reload: Dictionary={"companion_id":m.companion_id,"companion_colors":m.companion_colors.duplicate(),"care_points":m.care_points,"stuffie_wins":m.stuffie_wins.duplicate()}
	await _retire_main()
	if await _new_main(profile):
		if m.companion_id!=String(before_reload["companion_id"]) or m.companion_colors!=before_reload["companion_colors"] or m.care_points!=int(before_reload["care_points"]):
			errors.append("privatecheckpointreload changedcompanionstate")
		m.level2_done_once=true
		m._enter_level2_now(true,false,false)
		await _wait_frames(30)
		await _capture("private_reload_promenade","CURRENT_AUTHORED_ROUTE_CHECKPOINT","Fresh originalMain/SaveState;notnormalchildsave orroutecompletion")
		await _retire_main()
	if _normal_hashes()!=normal_before:
		errors.append("normalusersave changed")
	var report: Dictionary={"schema":"reef.creature_route_caller_audit/1","source_revision":OS.get_environment("R44_REV"),"engine":engine,"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[width,720],"identity":active_id,"states":states,"factory_diagnostics":factories,"synthetic_seed":initial_seed,"normal_before":normal_before,"normal_after":_normal_hashes(),"errors":errors,"actual_child_data":false,"art_context_credits":0,"scope_limits":"Current source-route/checkpoint andforced API dispatch diagnostics only. Do not inferactorpixelvisibility/all-gameunreachability/normalroutecoverage/human/device/QA11/artacceptance fromnodes/counters/source absence. Originalproduction/art unchanged;newgeneration0. Existinglegacy3D builders invokedonlyforisolatedsource audit,noproductiondebt added."}
	var file:=FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t",true)+"\n")
	file.close()
	print("CREATURE44|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
