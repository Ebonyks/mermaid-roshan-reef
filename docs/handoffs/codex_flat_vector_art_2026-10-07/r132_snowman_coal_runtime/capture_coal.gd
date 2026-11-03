extends SceneTree
var m: ReefMain
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("R132_OUT")
var lane := OS.get_environment("R132_LANE")
var width := int(OS.get_environment("R132_WIDTH"))
var height := int(OS.get_environment("R132_HEIGHT"))
var driver_only := OS.get_environment("R132_DRIVER_ONLY") == "1"
var failed := 0
var finger_down := false
var angle := 0.0
var coal_snapshot: Dictionary = {}
const DT := 1.0 / 30.0
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label":label,"pass":ok})
	if not ok:
		failed += 1
		print("R132|FAIL|",label)
func wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame
func pointer(point: Vector2, pressed: bool) -> void:
	var screen: Vector2 = m.mg2d_stage.get_global_transform_with_canvas() * point
	if Input.emulate_mouse_from_touch:
		if pressed and finger_down:
			var drag := InputEventScreenDrag.new()
			drag.index = 0
			drag.position = screen
			Input.parse_input_event(drag)
		else:
			var touch := InputEventScreenTouch.new()
			touch.index = 0
			touch.position = screen
			touch.pressed = pressed
			Input.parse_input_event(touch)
	else:
		var move := InputEventMouseMotion.new()
		move.position = screen
		move.global_position = screen
		move.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
		Input.parse_input_event(move)
		if pressed != finger_down:
			var button := InputEventMouseButton.new()
			button.button_index = MOUSE_BUTTON_LEFT
			button.position = screen
			button.global_position = screen
			button.pressed = pressed
			Input.parse_input_event(button)
	finger_down = pressed
	Input.flush_buffered_events()
func tick(point: Vector2, pressed: bool) -> void:
	pointer(point,false)
	var desired := Vector2.ZERO
	if pressed and String(m.mg.get("phase",""))=="roll":
		var offset: Vector2 = point-m.SNOW_ROLL_C
		if offset.length()>30.0 and offset.length()<460.0:
			desired = offset.normalized()
	elif pressed and String(m.mg.get("phase","")) in ["chase","carrot"]:
		desired = Vector2(signf(point.x-float(m.mg["chaser_x"])),0)
	if m.touch_ui!=null:
		m.touch_ui.stick_vec = desired
	m._tick_mg2d(DT)
	await wait_frames(2)
func neutral(n: int) -> void:
	for i in range(n):
		await tick(Vector2(420,500),false)
func spin_step() -> void:
	angle += 0.18
	await tick(m.SNOW_ROLL_C + Vector2(cos(angle),sin(angle))*190.0,true)
func tap(point: Vector2) -> void:
	pointer(point,true)
	await wait_frames(2)
	pointer(point,false)
	await wait_frames(2)
func check_coal(label: String) -> void:
	var ids: Dictionary = {}
	var visible_choices := 0
	var eyes := 0
	var details: Array[Dictionary] = []
	for value in m.mg.get("btns",[]):
		var button := value as Button
		if button==null or button.get_child_count()==0:
			continue
		var icon := button.get_child(0) as TextureRect
		if icon==null or icon.texture==null:
			continue
		check(label+" no old coal choice fallback",icon.texture.resource_path!="res://assets/mg/coal.png")
		if icon.texture.resource_path!="res://assets/mg/snowman_coal_painted.png":
			continue
		ids[icon.texture.get_instance_id()] = true
		var expected_center: bool = (button.position+button.size*0.5).distance_to(Vector2(220,600))<0.002 or (button.position+button.size*0.5).distance_to(Vector2(500,600))<0.002
		check(label+" original coal touch geometry/paint only",expected_center and button.size==StorybookUI.MIN_TOUCH and button.custom_minimum_size==StorybookUI.MIN_TOUCH and icon.mouse_filter==Control.MOUSE_FILTER_IGNORE and icon.stretch_mode==TextureRect.STRETCH_KEEP_ASPECT_CENTERED)
		if button.is_visible_in_tree():
			visible_choices += 1
		details.append({"kind":"choice","visible":button.is_visible_in_tree(),"button_rect":str(Rect2(button.position,button.size)),"source":icon.texture.resource_path})
		var image: Image = icon.texture.get_image()
		check(label+" actual256RGBA mips within350k",image.get_size()==Vector2i(256,256)and image.get_format()==Image.FORMAT_RGBA8 and image.has_mipmaps()and image.get_data_size()<=350000 and image.detect_alpha()==Image.ALPHA_BLEND)
	for value in m.mg.get("face_bits",[]):
		if not is_instance_valid(value):
			continue
		var eye := value as TextureRect
		if eye==null or eye.texture==null:
			continue
		check(label+" no old coal eye fallback",eye.texture.resource_path!="res://assets/mg/coal.png")
		if eye.texture.resource_path=="res://assets/mg/snowman_coal_painted.png":
			eyes += 1
			ids[eye.texture.get_instance_id()] = true
			check(label+" original42square eye",eye.size.distance_to(Vector2(42,42))<0.002)
			details.append({"kind":"eye","rect":str(Rect2(eye.position,eye.size)),"rotation":eye.rotation,"source":eye.texture.resource_path})
	check(label+" shared texture max2visible tokens",ids.size()<=1 and visible_choices+eyes<=2)
	var phase: String = String(m.mg.get("phase",""))
	if phase=="face":
		check(label+" two coal choices become two eyes",visible_choices+eyes==2)
	elif phase=="chase":
		check(label+" both placed coal eyes follow chase",eyes==2 and visible_choices==0)
	elif phase in["carrot","done","roll"]:
		check(label+" no early or leftover coal",eyes==0 and visible_choices==0)
	coal_snapshot={"visible_choices":visible_choices,"eyes":eyes,"unique_resource_ids":ids.size(),"details":details}
func shot(label: String) -> void:
	check_coal(label)
	check(label+" live configured Snowman",m.mg_kind=="snowman"and m.mg2d_stage!=null and not m.start_menu_active)
	check(label+" manual original clock advances",float(m.mg.get("t",-1))>=0.0 and not m.is_processing())
	if driver_only:
		return
	await RenderingServer.frame_post_draw
	var im: Image = get_root().get_texture().get_image()
	var path: String = out.path_join(label+".png")
	check(label+" native PNG",im.save_png(path)==OK and im.get_size()==Vector2i(width,height))
	var body: Array[Dictionary] = []
	for b in m.mg.get("body",[]):
		if is_instance_valid(b):
			body.append({"rect":str(Rect2(b.position,b.size)),"scale":str(b.scale),"rotation":b.rotation,"instance_id":b.get_instance_id(),"children":b.get_child_count()})
	var roll: Panel = m.mg.get("roll_ball") as Panel
	var roll_data: Dictionary = {}
	if roll!=null and is_instance_valid(roll):
		roll_data={"rect":str(Rect2(roll.position,roll.size)),"instance_id":roll.get_instance_id(),"children":roll.get_child_count()}
	frames.append({"path":path,"sha256":FileAccess.get_sha256(path),"width":width,"height":height,"label":label,"t":m.mg.get("t"),"phase":m.mg.get("phase"),"balls":m.mg.get("balls"),"bites":m.mg.get("bites",0),"rotation_progress":m.mg.get("rot_acc"),"required_rotation":m.mg.get("rot_need"),"body":body,"rolling":roll_data,"coal":coal_snapshot.duplicate(true),"face":m.mg.get("face"),"stage_scale":str(m.mg2d_stage.scale),"stage_position":str(m.mg2d_stage.position),"configured_original_controller_tick":true,"natural_route":false})
func run() -> void:
	seed(20261103)
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(width,height)
	DirAccess.make_dir_recursive_absolute(out)
	var packed := load("res://scenes/main.tscn") as PackedScene
	m = packed.instantiate() as ReefMain
	m._save_state = SaveState.new(m,"user://r132_isolated_save.json")
	get_root().add_child(m)
	await wait_frames(20)
	check("actual display title",m.start_menu_active and m.start_menu_layer!=null)
	if m.start_menu_layer == null:
		await finish()
		return
	var button := m.start_menu_layer.find_child("StartMenuContinueButton",true,false) as Button
	check("real Continue",button!=null)
	if button==null:
		await finish()
		return
	var saved: Dictionary = m.save_data.duplicate(true)
	saved["day_one_active"] = false
	saved["day_one_completed_rooms"] = ["bathroom","pool","stuffie","art"]
	m._day_one_ref().restore_state(saved)
	m.save_data.merge(m._day_one_ref().serialize_state(),true)
	m.has_saved_game = true
	button.disabled = false
	button.pressed.emit()
	await wait_frames(20)
	m._set_touch_mode(m.TOUCH_MODE_HYBRID,false)
	m._apply_quality("speedy")
	m.set_process(false)
	m._mg2d_open("snowman")
	await wait_frames(5)
	check("Mobile",RenderingServer.get_current_rendering_method()=="mobile")
	check("exact viewport",get_root().get_visible_rect().size==Vector2(width,height))
	check("original small26 Panel",m.mg["roll_ball"] is Panel and (m.mg["roll_ball"] as Panel).size==Vector2(52,52))
	check("original source radius124",float(m.mg["final_r"])==124.0)
	await shot("01_small")
	for i in range(15):
		await tick(Vector2(1200,250),true)
	await neutral(15)
	check("wrong far pointer and passive stay zero",int(m.mg["balls"])==0 and float(m.mg["rot_acc"])==0.0 and not bool(m.mg["motor_assist"]))
	await shot("02_wrong_passive")
	for ball_index in range(3):
		var final_r: float = 124.0-float(ball_index)*26.0
		var before_t: float = float(m.mg["t"])
		var n := 0
		while int(m.mg["balls"])==ball_index and float(m.mg["rot_acc"])<float(m.mg["rot_need"])*0.52 and n<200:
			await spin_step()
			n += 1
		check("real pointer original clock/growth "+str(ball_index),float(m.mg["t"])>before_t and float(m.mg["rot_acc"])>2.0 and int(m.mg["balls"])==ball_index)
		check("logical radius actually grew "+str(ball_index),(m.mg["roll_ball"] as Panel).size.x>52.0 and (m.mg["roll_ball"] as Panel).size.x<final_r*2.0)
		check("configured original virtual-stick growth",m.touch_ui!=null and float(m.mg["rot_acc"])>2.0)
		await shot(["03_growing_lower","05_growing_middle","07_growing_head"][ball_index])
		if driver_only:
			await finish()
			return
		while int(m.mg["balls"])==ball_index and n<400:
			await spin_step()
			n += 1
		pointer(Vector2(420,500),false)
		check("original circle goal settled "+str(ball_index),int(m.mg["balls"])==ball_index+1 and (m.mg["body"] as Array).size()==ball_index+1)
		await create_timer(0.65).timeout
		var body: Array = m.mg["body"]
		var settled := body[ball_index] as Panel
		check("original Panel geometry/stack center "+str(ball_index),settled.size.distance_to(Vector2(final_r*2,final_r*2))<0.002 and settled.position.distance_to(Vector2(980,560-float(ball_index)*175)-Vector2(final_r,final_r))<0.1)
		await shot(["04_lower_settled","06_two_settled","08_three_stack_face"][ball_index])
	check("actual new coalPNG hash",FileAccess.get_sha256("res://assets/mg/snowman_coal_painted.png")=="279dffbe48bf8e42c195bd118b50e6fc71ae1e9179c2f182ed81572853448612")
	check("face only after3 actual circles",String(m.mg["phase"])=="face" and (m.mg["btns"] as Array).size()==3)
	var buttons: Array = m.mg["btns"]
	for i in range(3):
		var face_button := buttons[i] as Button
		check("original touch target "+str(i),face_button.size.x>=StorybookUI.MIN_TOUCH.x and face_button.size.y>=StorybookUI.MIN_TOUCH.y)
		await tap(face_button.position+face_button.size*0.5)
		check("real finger placed face "+str(i),int(m.mg["face"])==i+1 and not face_button.visible)
		if i==1:
			await shot("09_partial_face")
	check("all3 placements trigger original chase",String(m.mg["phase"])=="chase" and int(m.mg["bites"])==0)
	await shot("10_chase_full")
	for bite_index in range(3):
		var retiring: Panel = (m.mg["body"] as Array)[0] as Panel
		var weak: WeakRef = weakref(retiring)
		var n := 0
		while int(m.mg["bites"])==bite_index and n<300:
			await tick(Vector2(float(m.mg["run_x"])+70.0,470.0),true)
			n += 1
		pointer(Vector2(420,500),false)
		check("actual original catch/bite "+str(bite_index),int(m.mg["bites"])==bite_index+1 and (m.mg["body"] as Array).size()==2-bite_index)
		await wait_frames(1)
		check("original bite squash live "+str(bite_index),is_instance_valid(retiring) and retiring.scale.y<1.0)
		await shot(["11_lower_bite_squash","13_middle_bite_squash","15_head_bite_squash"][bite_index])
		await create_timer(0.65).timeout
		check("retiring ball actually freed "+str(bite_index),weak.get_ref()==null)
		await shot(["12_remaining_two","14_remaining_head","16_carrot_only"][bite_index])
	check("carrot endpoint no body",String(m.mg["phase"])=="carrot" and (m.mg["body"] as Array).is_empty())
	var n := 0
	while String(m.mg.get("phase",""))=="carrot" and n<120:
		await tick(Vector2(float(m.mg["run_x"]),470.0),true)
		n += 1
	pointer(Vector2(420,500),false)
	check("original carrot reward/win",String(m.mg.get("phase",""))=="done" and bool(m.mg.get("won",false)))
	await shot("17_original_win")
	var old: WeakRef = weakref(m.mg2d_root)
	m._mg2d_close()
	await wait_frames(3)
	check("close frees whole selected stage",old.get_ref()==null and m.mg2d_stage==null and m.mg_kind=="")
	m._mg2d_open("snowman")
	await wait_frames(3)
	check("fresh reentry original small resets",int(m.mg["balls"])==0 and int(m.mg["face"])==0 and String(m.mg["phase"])=="roll" and (m.mg["roll_ball"] as Panel).size==Vector2(52,52))
	await shot("18_fresh_reentry")
	m._mg2d_close()
	await wait_frames(3)
	await finish()
func finish() -> void:
	if m!=null and is_instance_valid(m):
		m.process_mode = Node.PROCESS_MODE_DISABLED
		m.get_parent().remove_child(m)
		m.free()
	await process_frame
	var result := {"status":"PASS"if failed==0 else"FAIL","lane":lane,"checks":checks,"captures":frames,"configured_original_controller_tick":true,"manual_main_process_suspended":true,"pointer_driver":"Original trusted-probe virtual-stick vectors immediately before actual controller tick; real single-index0 screen face taps. Configured clock/state drive, no natural-route/physical-touch claim","formal_QA11":null,"device":null,"child":null,"owner":null,"natural_route":false,"source_pin_sha256":OS.get_environment("R132_PIN_SHA256")}
	var f := FileAccess.open(out.path_join("RESULT.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify(result,"\t"))
	f.close()
	print("R132|END|",lane,"|checks=",checks.size(),"|bad=",failed,"|frames=",frames.size())
	quit(0 if failed==0 else 1)
