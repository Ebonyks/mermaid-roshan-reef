class_name FashionSkinEngineTestCase
extends RefCounted
## Focused fixture; UI actions enter through Input, never pressed.emit/_pick.
static func _mouse(main: ReefMain, point: Vector2, down: bool) -> void:
	var motion := InputEventMouseMotion.new()
	motion.position = point
	motion.global_position = point
	main.get_viewport().push_input(motion,true)
	var event := InputEventMouseButton.new()
	event.position = point
	event.global_position = point
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = down
	main.get_viewport().push_input(event,true)
	Input.flush_buffered_events()
	await main.get_tree().process_frame
	await main.get_tree().process_frame

static func _tap(main: ReefMain, control: Control) -> void:
	var point: Vector2 = control.get_global_transform_with_canvas() * (control.size * 0.5)
	await _mouse(main,point,true)
	await _mouse(main,point,false)

static func _touch(main: ReefMain, point: Vector2, index: int, down: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.position = point
	event.index = index
	event.pressed = down
	main.get_viewport().push_input(event,true)
	await main.get_tree().process_frame

static func run(main: ReefMain, check: Callable) -> void:
	var old_skin: String = main.skin_id
	var old_outfits: Dictionary = main.character_outfits.duplicate(true)
	var old_parts: Dictionary = main.character_clothing_parts.duplicate(true)
	var old_dressing: Dictionary = main.fashion_dressing_progress.duplicate(true)
	main._start_menu_ref()._dismiss_menu() # Explicit focused-fixture setup.
	await main.get_tree().process_frame
	main.character_outfits = {}
	main.character_clothing_parts = {}
	main.fashion_dressing_progress = {"future_person":{"future":9}}
	main.skin_id = "classic"
	var source: Texture2D = load("res://assets/characters/roshan_25d/roshan_directional.png") as Texture2D
	var atlas := AtlasTexture.new()
	atlas.atlas = source
	atlas.region = Rect2(256,0,256,256)
	atlas.margin = Rect2(3,4,5,6)
	atlas.filter_clip = true
	var frames := SpriteFrames.new()
	frames.set_animation_speed("default",7.5)
	frames.set_animation_loop("default",false)
	frames.add_frame("default",atlas,0.75)
	frames.add_frame("default",atlas,1.25)
	var actor := AnimatedSprite2D.new()
	actor.sprite_frames = FashionSkinEngine.animation_frames(main,frames)
	actor.position = Vector2(73,126)
	actor.scale = Vector2(0.67,0.67)
	main.add_child(actor)
	var states: Array[Dictionary] = [{"paused":false,"speed":1.3,"custom":-0.75},{"paused":true,"speed":0.8,"custom":2.0},{"paused":false,"speed":0.0,"custom":0.6}]
	for state: Dictionary in states:
		actor.speed_scale = float(state["speed"])
		actor.play("default",float(state["custom"]))
		if bool(state["paused"]): actor.pause()
		actor.set_frame_and_progress(1,0.37)
		var playing: bool = actor.is_playing()
		var speed: float = actor.get_playing_speed()
		var transform: Transform2D = actor.transform
		FashionDesigner.equip(main,"roshan","roshan_ribbon_v1",true)
		var changed: AtlasTexture = actor.sprite_frames.get_frame_texture("default",1) as AtlasTexture
		check.call(actor.frame == 1 and is_equal_approx(actor.frame_progress,0.37) and actor.is_playing() == playing and is_equal_approx(actor.get_playing_speed(),speed) and actor.transform == transform,
			"Skin swap preserves active/paused/zero-speed animation state " + str(state))
		check.call(changed.region == atlas.region and changed.margin == atlas.margin and changed.filter_clip == atlas.filter_clip and actor.sprite_frames.get_animation_speed("default") == 7.5 and not actor.sprite_frames.get_animation_loop("default") and actor.sprite_frames.get_frame_duration("default",0) == 0.75 and actor.sprite_frames.get_frame_duration("default",1) == 1.25,
			"Skin swap preserves atlas sampling and authored timing")
		check.call(atlas.atlas == source and frames.get_frame_texture("default",0) == atlas,
			"Skin swap leaves the shared original resource untouched")
		FashionDesigner.equip(main,"roshan","roshan_original",true)
	actor.queue_free()
	main.character_outfits = {}
	main.character_clothing_parts = {}
	var wardrobe := FashionWardrobe.new(main)
	wardrobe.open()
	await main.get_tree().process_frame
	var initial: Dictionary = main.character_outfits.duplicate(true)
	await main.get_tree().process_frame
	check.call(main.character_outfits == initial,"Opening dress-up never equips passively")
	for person: String in ["roshan","rumi","daddy_mermaid"]:
		var selector: Button = main.wardrobe_layer.find_child("FashionCharacter_"+person,true,false) as Button
		await _tap(main,selector)
		var card: Button = main.wardrobe_layer.find_child("FashionOutfit_"+person+"_ribbon_v1",true,false) as Button
		if card == null:
			check.call(false,"Missing character card after real input: "+person)
			main._wardrobe_ref()._close_wardrobe()
			return
		await _tap(main,card)
		check.call(FashionDesigner.selected(main,person) == person+"_ribbon_v1" and bool((main.fashion_dressing_progress.get(person,{}) as Dictionary).get("dressed",false)),
			"Real pointer tap dresses and remembers " + person)
		var original: Button = main.wardrobe_layer.find_child("FashionOutfit_"+person+"_original",true,false) as Button
		await _tap(main,original)
		card = main.wardrobe_layer.find_child("FashionOutfit_"+person+"_ribbon_v1",true,false) as Button
		var start: Vector2 = card.get_global_transform_with_canvas() * (card.size*0.5)
		await _mouse(main,start,true)
		var stage: Control = main.wd["stage"] as Control
		var fit: Rect2 = main.wd["fashion_fit_rect"] as Rect2
		var end: Vector2 = stage.get_global_transform_with_canvas() * fit.get_center()
		await _mouse(main,end,false)
		check.call(FashionDesigner.selected(main,person) == person+"_ribbon_v1",
			"Real pointer garment placement dresses " + person)
		original = main.wardrobe_layer.find_child("FashionOutfit_"+person+"_original",true,false) as Button
		await _tap(main,original)
		card = main.wardrobe_layer.find_child("FashionOutfit_"+person+"_ribbon_v1",true,false) as Button
		start = card.get_global_transform_with_canvas() * (card.size*0.5)
		await _mouse(main,start,true)
		await _mouse(main,stage.get_global_transform_with_canvas() * Vector2(540,110),false)
		check.call(FashionDesigner.selected(main,person) == person+"_original",
			"Outside drop is neutral for " + person)
	# Focus loss owns cancellation; a later release cannot dress a character.
	var focus_card: Button = main.wardrobe_layer.find_child("FashionOutfit_daddy_mermaid_ribbon_v1",true,false) as Button
	var point: Vector2 = focus_card.get_global_transform_with_canvas() * (focus_card.size*0.5)
	await _mouse(main,point,true)
	var input: FashionDressingInput = main.wd["dressing_input"] as FashionDressingInput
	input.notification(Node.NOTIFICATION_WM_WINDOW_FOCUS_OUT)
	await _mouse(main,point,false)
	check.call(FashionDesigner.selected(main,"daddy_mermaid") == "daddy_mermaid_original" and (main.wd.get("fashion_drag",{}) as Dictionary).is_empty(),
		"Focus cancellation consumes stale release and removes ghost")
	await _touch(main,point,0,true)
	await _touch(main,point,1,true)
	await _touch(main,point,1,false)
	check.call(FashionDesigner.selected(main,"daddy_mermaid") == "daddy_mermaid_original" and int((main.wd.get("fashion_drag",{}) as Dictionary).get("pointer",-99)) == 0,
		"Extra finger cannot steal or complete a garment gesture")
	var touch_stage: Control = main.wd["stage"] as Control
	var touch_fit: Rect2 = main.wd["fashion_fit_rect"] as Rect2
	var touch_end: Vector2 = touch_stage.get_global_transform_with_canvas() * touch_fit.get_center()
	var touch_drag := InputEventScreenDrag.new()
	touch_drag.index = 0
	touch_drag.position = touch_end
	main.get_viewport().push_input(touch_drag,true)
	await _touch(main,touch_end,0,false)
	check.call(FashionDesigner.selected(main,"daddy_mermaid") == "daddy_mermaid_ribbon_v1",
		"Owning finger can finish after unrelated finger release")
	await _tap(main,main.wardrobe_layer.find_child("FashionOutfit_daddy_mermaid_original",true,false) as Button)
	focus_card = main.wardrobe_layer.find_child("FashionOutfit_daddy_mermaid_ribbon_v1",true,false) as Button
	point = focus_card.get_global_transform_with_canvas() * (focus_card.size*0.5)
	await _mouse(main,point,true)
	main._wardrobe_ref()._close_wardrobe()
	await _mouse(main,point,false)
	check.call(FashionDesigner.selected(main,"daddy_mermaid") == "daddy_mermaid_original",
		"Close during gesture cannot equip after leaving")
	main.character_outfits["future_person"] = "future_outfit"
	main.fashion_dressing_progress["rumi"] = {"dressed":true,"outfit_id":"rumi_original","future_field":17}
	check.call(main._write_save(),"Engine dressing memory uses transactional save")
	var saved: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ReefMain.SAVE_PATH)) as Dictionary
	main.character_outfits = {}
	main.character_clothing_parts = {}
	main.fashion_dressing_progress = {}
	FashionDesigner.restore(main,saved)
	check.call(main.character_outfits.get("future_person") == "future_outfit" and (main.fashion_dressing_progress["rumi"] as Dictionary).get("future_field") == 17 and (main.fashion_dressing_progress["future_person"] as Dictionary).get("future") == 9,
		"Disk save/reload retains dressing journal and future fields")
	main.skin_id = old_skin
	main.character_outfits = old_outfits
	main.character_clothing_parts = old_parts
	main.fashion_dressing_progress = old_dressing
	FashionSkinEngine.refresh(main)
	main._write_save()

	await FashionPartsTestCase.run(main,check)
