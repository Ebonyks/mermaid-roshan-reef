extends SceneTree
## Desktop Mobile render fixture; no natural chapter-route or owner acceptance claim.
const OUT := "res://assets_src/fashion_designer/skin_engine_v2/review/"
var m: ReefMain
var events: Array[Dictionary] = []
func _initialize() -> void:
	call_deferred("_run")
func _tap(name: String) -> void:
	var card: Control = m.wardrobe_layer.find_child(name,true,false) as Control
	if card == null:
		push_error("Missing review target: "+name)
		quit(1)
		return
	var point: Vector2 = card.get_global_transform_with_canvas() * (card.size*0.5)
	events.append({"target":name,"point":str(point),"input":"Viewport.push_input mouse press/release, real GUI route"})
	await FashionSkinEngineTestCase._tap(m,card)
func _shot(id: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+id+".png")
	print("FASHION_SKIN_REVIEW|CAPTURE|",id)
func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1280,720)
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(3.0).timeout
	m._start_menu_ref()._dismiss_menu()
	m._skip_intro()
	m.day_one_active = false
	await process_frame
	# Explicit review fixture unlocks, never natural progression evidence.
	for person: String in ["roshan","rumi","daddy_mermaid"]:
		FashionDesigner.grant(m,FashionDesigner.PARTY_DRESS if person == "roshan" else person+"_party_v1")
		FashionDesigner.grant(m,person+"_garden_v1")
	var wardrobe := FashionWardrobe.new(m)
	wardrobe.open()
	await process_frame
	for person: String in ["roshan","rumi","daddy_mermaid"]:
		await _tap("FashionCharacter_"+person)
		await _tap("FashionOutfit_"+(FashionDesigner.PARTY_DRESS if person == "roshan" else person+"_party_v1"))
		await _shot(person+"-party-1280x720")
		await _tap("FashionNextPage")
		await _tap("FashionOutfit_"+person+"_garden_v1")
		await _shot(person+"-garden-1280x720")
	root.size = Vector2i(1920,900)
	await process_frame
	wardrobe.open()
	await _tap("FashionCharacter_daddy_mermaid")
	await _shot("daddy-wide-1920x900")
	var record: FileAccess = FileAccess.open(OUT+"input_fixture.json",FileAccess.WRITE)
	record.store_string(JSON.stringify({"schema":1,"renderer":RenderingServer.get_current_rendering_method(),"engine":Engine.get_version_info(),"user_data_dir":OS.get_user_data_dir(),"fixture":"Explicit setup and unlocks; all clothing and character actions use GUI input; no natural route/completion/reload proof","events":events,"acceptance":"Device/child/owner PENDING"},"	")+"\n")
	print("FASHION_SKIN_REVIEW|ALL OK|desktop fixture only")
	quit()
