extends SceneTree
var m: ReefMain
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("R133_OUT")
var lane := OS.get_environment("R133_LANE")
var width := int(OS.get_environment("R133_WIDTH"))
var height := int(OS.get_environment("R133_HEIGHT"))
var driver_only := OS.get_environment("R133_DRIVER_ONLY") == "1"
var failed := 0
var finger_down := false
var angle := 0.0
const DT := 1.0 / 30.0
var ground_paths: PackedStringArray = PackedStringArray([
	"res://assets/mg/snowfield_painted_00.png",
	"res://assets/mg/snowfield_painted_01.png",
	"res://assets/mg/snowfield_painted_10.png",
	"res://assets/mg/snowfield_painted_11.png",
])
func ground_report(label: String) -> Dictionary:
	var p: Panel = m.mg2d_stage.get_node_or_null("SnowfieldGeometry") as Panel
	check(label+" ground original invisible Panel",p!=null and p.size==Vector2(1400,1400) and p.position==Vector2(-60,280) and p.pivot_offset==Vector2.ZERO and p.mouse_filter==Control.MOUSE_FILTER_STOP)
	if p==null:
		return {}
	check(label+" no visible stylebox ground/gloss",p.get_theme_stylebox("panel") is StyleBoxEmpty and p.get_child_count()==4)
	var details: Array[Dictionary] = []
	var resources: Dictionary = {}
	var decoded := 0
	for i in range(4):
		var card: TextureRect = p.get_node_or_null("SnowfieldCard%d"%i) as TextureRect
		check(label+" actual ground card "+str(i),card!=null)
		if card==null:
			continue
		check(label+" ground card geometry "+str(i),card.position==Vector2(float(i%2)*700.0,float(i>>1)*500.0-60.0) and card.size==Vector2(700,500) and card.mouse_filter==Control.MOUSE_FILTER_IGNORE)
		var tex: Texture2D = card.texture
		check(label+" actual native crop texture "+str(i),tex!=null and tex.resource_path==ground_paths[i] and tex.get_size()==Vector2(1024,1024))
		if tex==null:
			continue
		var im: Image = tex.get_image()
		check(label+" mip budget "+str(i),im!=null and im.has_mipmaps() and im.get_data_size()<=5592500)
		if im!=null:
			decoded+=im.get_data_size()
		resources[tex.get_instance_id()]=true
		details.append({"index":i,"path":tex.resource_path,"rect":str(card.get_global_rect()),"local_position":str(card.position),"size":str(card.size),"image_sha256":FileAccess.get_sha256(tex.resource_path),"visible":card.is_visible_in_tree()})
	check(label+" one field four resources decoded budget",resources.size()==4 and decoded<=22400000)
	return {"root_rect":str(p.get_global_rect()),"source_functional_rect":str(Rect2(p.position,p.size)),"cards":details,"unique_resources":resources.size(),"decoded_mips_bytes":decoded,"master_native_size":Vector2i(2048,2048),"source_resampling":false}
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label":label,"pass":ok})
	if not ok:
		failed += 1
		print("R133|FAIL|",label)
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
	var before_focus: bool = get_root().has_focus()
	get_root().grab_focus()
	await wait_frames(4)
	check("owned capture window focused for real touch",get_root().has_focus())
	print("R133|TAP_FOCUS|before=",before_focus,"|after=",get_root().has_focus(),"|point=",point,"|mouse_emulation=",Input.emulate_mouse_from_touch)
	pointer(point,true)
	await wait_frames(4)
	pointer(point,false)
	await wait_frames(4)
	var hovered: Control = get_root().gui_get_hovered_control()
	print("R133|TAP_HOVER|",str(hovered.get_path()) if hovered!=null else "none","|face=",m.mg.get("face"))
func shot(label: String) -> void:
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
	var ground: Dictionary = ground_report(label)
	frames.append({"path":path,"sha256":FileAccess.get_sha256(path),"width":width,"height":height,"label":label,"t":m.mg.get("t"),"phase":m.mg.get("phase"),"balls":m.mg.get("balls"),"bites":m.mg.get("bites",0),"rotation_progress":m.mg.get("rot_acc"),"required_rotation":m.mg.get("rot_need"),"body":body,"ground":ground,"rolling":roll_data,"face":m.mg.get("face"),"stage_scale":str(m.mg2d_stage.scale),"stage_position":str(m.mg2d_stage.position),"configured_original_controller_tick":true,"natural_route":false})
func run() -> void:
	seed(20261103)
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(width,height)
	DirAccess.make_dir_recursive_absolute(out)
	var packed := load("res://scenes/main.tscn") as PackedScene
	m = packed.instantiate() as ReefMain
	m._save_state = SaveState.new(m,"user://r133_isolated_save.json")
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
	if String(m.mg.get("phase",""))!="chase":
		await finish()
		return
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
	var result := {"status":"PASS"if failed==0 else"FAIL","lane":lane,"checks":checks,"captures":frames,"configured_original_controller_tick":true,"manual_main_process_suspended":true,"pointer_driver":"Original trusted-probe virtual-stick vectors immediately before actual controller tick; real single-index0 screen face taps. Configured clock/state drive, no natural-route/physical-touch claim","formal_QA11":null,"device":null,"child":null,"owner":null,"natural_route":false,"source_pin_sha256":OS.get_environment("R133_PIN_SHA256")}
	var f := FileAccess.open(out.path_join("RESULT.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify(result,"\t"))
	f.close()
	print("R133|END|",lane,"|checks=",checks.size(),"|bad=",failed,"|frames=",frames.size())
	quit(0 if failed==0 else 1)
