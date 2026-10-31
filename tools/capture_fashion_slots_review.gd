extends SceneTree
## Actual Mobile GUI fixture, synthetic unlock setup; no natural route/device/owner claim.
const OUT := "res://assets_src/fashion_designer/slots_v1/review/"
var m: ReefMain
var events: Array[Dictionary] = []
func _initialize() -> void:
	call_deferred("_run")
func _tap(name: String) -> void:
	var node: Control = m.wardrobe_layer.find_child(name,true,false) as Control
	if node == null:
		push_error("Missing capture target "+name)
		quit(1)
		return
	events.append({"target":name,"point":str(node.get_global_transform_with_canvas()*(node.size*0.5)),"input":"Viewport.push_input press/release through GUI"})
	await FashionSkinEngineTestCase._tap(m,node)
func _pick(id: String, slot: String) -> void:
	await _tap("FashionSlot_"+slot)
	for index: int in range(5):
		if m.wardrobe_layer.find_child("FashionOutfit_"+id,true,false) != null:
			await _tap("FashionOutfit_"+id)
			return
		await _tap("FashionNextPage")
	push_error("Missing garment "+id)
	quit(1)
func _shot(id: String) -> void:
	await create_timer(0.45).timeout
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+id+".png")
func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1280,720)
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(3.0).timeout
	m._start_menu_ref()._dismiss_menu()
	m._skip_intro()
	m.day_one_active = false
	for item: Dictionary in FashionParts.CATALOG.data["items"]:
		FashionDesigner.grant(m,String(item["id"]))
	for person: String in FashionParts.PEOPLE:
		FashionDesigner.grant(m,FashionDesigner.PARTY_DRESS if person == "roshan" else person+"_party_v1")
		FashionDesigner.grant(m,person+"_garden_v1")
	var wardrobe := FashionWardrobe.new(m)
	wardrobe.open()
	await process_frame
	await _shot("roshan-body-default-1280x720")
	for person: String in FashionParts.PEOPLE:
		await _tap("FashionCharacter_"+person)
		await _pick("head_strawberry_v1","head")
		await _pick("body_strawberry_v1","body")
		await _pick("tail_strawberry_v1","tail")
		await _shot(person+"-strawberry-tail-1280x720")
		await _pick("head_chef_v1","head")
		await _pick("body_painter_v1","body")
		await _pick("tail_star_v1","tail")
		await _shot(person+"-mixed-tail-1280x720")
		await _tap("FashionSlot_head")
		await _shot(person+"-mixed-head-1280x720")
	m.chapter2_story_complete = true
	m.fashion_disguise_progress = {}
	wardrobe.open()
	await _tap("FashionDisguisePlay")
	await _shot("practice-body-1280x720")
	await _tap("FashionOutfit_roshan_garden_v1")
	await _shot("practice-tail-1280x720")
	await _tap("FashionOutfit_tail_strawberry_v1")
	await _shot("practice-head-1280x720")
	await _tap("FashionOutfit_finish_bow")
	await _shot("practice-complete-1280x720")
	root.size = Vector2i(1920,900)
	await process_frame
	wardrobe.open()
	await _tap("FashionCharacter_rumi")
	await _shot("rumi-wide-1920x900")
	var cache: Array[Dictionary] = []
	for key: String in m.fashion_composed_textures:
		var entry: Dictionary = m.fashion_composed_textures[key] as Dictionary
		cache.append({"family":key,"bytes":entry["bytes"],"compose_usec":entry["compose_usec"]})
	var file: FileAccess = FileAccess.open(OUT+"input_fixture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"schema":1,"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"fixture":"Synthetic unlocks; real GUI selection. No natural route/physical device/owner acceptance.","events":events,"cache":cache,"save_profile":OS.get_user_data_dir()},"\t")+"\n")
	print("FASHION_SLOTS_REVIEW|ALL OK|real Mobile desktop GUI fixture")
	quit()
