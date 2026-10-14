extends SceneTree
## R41 source-only current companion consumer contexts; private synthetic saves only.
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

func _capture(id: String, input_info: Dictionary={}) -> void:
	await RenderingServer.frame_post_draw
	var image: Image=get_root().get_texture().get_image()
	if image==null or image.get_size()!=get_root().size:
		errors.append("framebuffer mismatch "+id)
		return
	var filename:=id+".png"
	var path:=out_dir.path_join(filename)
	if image.save_png(path)!=OK:
		errors.append("PNG write failed "+id)
		return
	var nodes: Array[Dictionary]=[]
	for layer: CanvasLayer in [m.companion_layer,m.companion_care_layer,m.castle_room_layer]:
		if layer!=null:
			_nodes(layer,nodes)
	var card: Dictionary={}
	if m.castle_companion_card!=null and is_instance_valid(m.castle_companion_card):
		var c: Control=m.castle_companion_card
		card={"visible":c.is_visible_in_tree(),"position":str(c.position),"scale":str(c.scale),"z_index":c.z_index,"identity":c.get_meta("companion_id",""),"color_tokens":c.get_meta("companion_colors",[]),"source_asset_paths":c.get_meta("source_asset_paths",[]),"source_object_id":c.get_meta("source_object_id",""),"child_count":c.get_child_count()}
	var file:=FileAccess.open(path,FileAccess.READ)
	states.append({"id":id,"image":{"file":filename,"bytes":file.get_length(),"sha256":FileAccess.get_sha256(path),"dimensions":[image.get_width(),image.get_height()]},"input":input_info,"nodes":nodes,"companion_id":m.companion_id,"companion_colors":m.companion_colors.duplicate(),"pick_id":m.companion_pick_id,"pick_slot":m.companion_pick_slot,"pick_colors":m.companion_pick_colors.duplicate(),"care_points":m.care_points,"stuffie_wins":m.stuffie_wins.duplicate(),"custom_fish":m.custom_fish.duplicate(true),"custom_friends":m.custom_friends.duplicate(true),"game":m.game,"game_phase":m.g.get("phase",""),"castle_room_id":m.castle_room_id,"castle_card":card,"picker_open":m.companion_layer!=null,"care_open":m.companion_care_layer!=null,"presentation":_presentation(),"ticks_msec":Time.get_ticks_msec(),"actual_child_data":false})
	file.close()
	print("COMPANION41|CAPTURE|"+id)

func _seed() -> Dictionary:
	return {"schema_version":1,"won":{},"found":{},"plays":0,"pearls":23,"pearls_ever":23,"music":false,"mic":false,"quality":"speedy","companion":active_id,"companion_colors":[],"care_points":8,"stuffie_wins":{"rescued_eagle":true,"friend_lamma":true},"crafts":{},"stickers":{},"custom_fish":[[0.9,0.3,0.3,1.0,0.8,0.2],[0.2,0.7,0.8,0.9,0.3,0.4,1,0]],"custom_friends":[["cat",0.95,0.7,0.85,0.6,0.4,0.9],["bird",1.0,0.85,0.3,0.3,0.8,0.9,0,1],["cat",0.95,0.7,0.85,0.6,0.4,0.9,1,0,0.97,0.96,0.93]]}

func _new_main(profile: String) -> bool:
	var scene:=load("res://scenes/main.tscn") as PackedScene
	m=scene.instantiate() as ReefMain
	m._save_state=SaveState.new(m,profile)
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
		print("COMPANION41|FAIL|engine/renderer/display")
		quit(1)
		return
	active_id=OS.get_environment("R41_ID")
	var width: int=int(OS.get_environment("R41_WIDTH"))
	var base_out:=OS.get_environment("R41_OUT")
	if active_id not in ["mewsha","eagle","lamma"] or width not in [1280,1600] or base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("COMPANION41|FAIL|exact new job output/id/aspect required")
		quit(1)
		return
	normal_before=_normal_hashes()
	out_dir=base_out
	DirAccess.make_dir_recursive_absolute(out_dir)
	if not await _set_aspect(Vector2i(width,720)):
		print("COMPANION41|FAIL|aspect readiness")
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
	comp.open_picker(false,active_id,"studio")
	await _wait_frames(6)
	await _capture("picker_default",{"entry":"guarded production open_picker studio;private synthetic seed,not natural route"})
	if m.companion_pick_id!=active_id:
		errors.append("identity preselect mismatch")
	if active_id=="mewsha":
		for slot: int in range(3):
			await _tap("StuffiePart_%d" % slot)
			for color_index: int in range(CompanionSystem.PALETTE.size()):
				await _tap("StuffieSwatch_%d" % color_index)
				if m.companion_pick_slot!=slot or m.companion_pick_colors[slot]!=CompanionSystem.PALETTE[color_index].to_html(false):
					errors.append("palette pointer state mismatch slot"+str(slot)+" color"+str(color_index))
				await _capture("slot%d_color%d" % [slot,color_index],{"method":"actual raw pointer press/release afternamed visiblehover readiness","slot":slot,"palette_index":color_index})
	else:
		if m.companion_stage.find_child("StuffiePart_0",true,false)!=null or m.companion_stage.find_child("StuffieSwatch_0",true,false)!=null:
			errors.append("nonpaintable identity guard exposed palette")
		await _capture("nonpaintable_identity_guard")
	var expected_colors: Array=m.companion_pick_colors.duplicate()
	await _tap("StuffieConfirmButton")
	await _wait_frames(20)
	if m.companion_layer!=null or m.companion_id!=active_id or m.companion_colors!=expected_colors:
		errors.append("confirm identity/colors/teardown mismatch")
	var adopted_colors: Array=m.companion_colors.duplicate()
	await _capture("confirmed_teardown",{"art_context_credit":false,"reason":"Only persistence/lifetime evidence"})
	comp.open_care_menu()
	await _wait_frames(6)
	if m.companion_care_layer==null:
		errors.append("care entry guarded in current game/phase "+m.game+"/"+String(m.g.get("phase","")))
	await _capture("care_saved_colors",{"entry":"actual productionguarded care entry;no manual guard bypass"})
	comp.close_care_menu()
	await _wait_frames(5)
	m.level2_done_once=true
	m._enter_level2_now(true,false,false)
	await _wait_frames(8)
	m._enter_castle_interior_now(false)
	await _wait_frames(10)
	if m.castle_companion_card==null or not m.castle_companion_card.is_visible_in_tree():
		errors.append("current Castle Canvas companioncard absent")
	await _capture("castle_card_saved_colors",{"entry":"production _enter_level2_now then _enter_castle_interior_now;syntheticcheckpoint,notnaturalroute"})
	await _wait_frames(20)
	await _capture("castle_card_idle_later",{"continuous_motion_review":false,"method":"sameprocess laternativeviewport"})
	m._write_save()
	await _retire_main()
	if await _new_main(profile):
		if m.companion_id!=active_id or m.companion_colors!=adopted_colors:
			errors.append("private savedcompanion identity/colors lost on freshMain reload")
		m._companion_ref().open_picker(false,active_id,"studio")
		await _wait_frames(6)
		await _capture("reloaded_picker_saved_colors",{"entry":"fresh production Main/SaveState reload fromactual emittedprivate save"})
		if m.companion_pick_colors!=adopted_colors:
			errors.append("picker reentry resets savedcolors")
		m._companion_ref().close_picker()
		await _wait_frames(5)
		await _capture("reentry_cancel_teardown",{"art_context_credit":false,"reason":"Only lifetime evidence"})
		await _retire_main()
	if _normal_hashes()!=normal_before:
		errors.append("normal user save hash changed")
	var manifest: Dictionary={"schema":"reef.companion_context/1","source_revision":OS.get_environment("R41_REV"),"engine":engine,"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[width,720],"identity":active_id,"states":states,"synthetic_seed":initial_seed,"normal_before":normal_before,"normal_after":_normal_hashes(),"adopted_colors":adopted_colors,"actual_child_data":false,"errors":errors,"scope_limits":"Guarded direct syntheticcurrent GUI/private save plusactuallevel2/Castleentry calls;notnaturalplay/phone touch/completecontinuousmotion/device/child/owner/QA11 orfullcallerclosure. Originalproduction/sourcepixels unchanged;no candidateadoption/newart."}
	var file:=FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()
	print("COMPANION41|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
