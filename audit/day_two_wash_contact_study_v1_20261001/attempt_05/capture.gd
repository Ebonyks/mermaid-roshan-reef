extends SceneTree
## Static contact placement study after actual viewport approach; no production edit.
const OUT := "res://tmp/doctor_sink_water_contact_v68/native_views/"
const SOURCES := [
	"res://assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png",
	"res://assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/attempt01_native.png",
]
class ContactCanvas extends Control:
	var character: Texture2D
	var sink: Texture2D
	var sink_extent := 180.0
	var sink_offset := 0.0
	var sink_offset_y := 0.0
	var water_on := false
	var water_spout := Vector2.ZERO
	var soap_contact := Vector2.ZERO
	var basin_centre := Vector2.ZERO
	var hand_source := Vector2(690.0,739.0)
	var character_rect := Rect2(25.0,0.0,200.071326676177,250.0)
	var hand := Vector2.ZERO
	var sink_rect := Rect2()
	func refresh_geometry() -> void:
		hand = character_rect.position + hand_source * (character_rect.size.y/1402.0)
		var scale_factor := sink_extent/256.0
		sink_rect = Rect2(hand + Vector2(sink_offset,sink_offset_y) - Vector2(128.0,105.0)*scale_factor,
			Vector2.ONE*sink_extent)
		water_spout = sink_rect.position + Vector2(128.0,69.0)*scale_factor
		soap_contact = character_rect.position + Vector2(684.0,680.0)*(character_rect.size.y/1402.0)
		basin_centre = sink_rect.position + Vector2(128.0,111.0)*scale_factor
		queue_redraw()
	func _draw() -> void:
		draw_texture_rect(sink,sink_rect,false)
		if water_on:
			draw_line(water_spout,soap_contact,Color("448fa9"),3.5,true)
			draw_line(water_spout,soap_contact,Color("caf9ff"),1.6,true)
		draw_texture_rect(character,character_rect,false)
		if water_on:
			var runoff := PackedVector2Array([soap_contact+Vector2(9.0,6.0),basin_centre+Vector2(8.0,-1.0)])
			draw_polyline(runoff,Color("77c7dc"),2.0,true)
			draw_circle(basin_centre+Vector2(7.0,-1.0),2.0,Color("caf9ff"))
		var atlas: AtlasTexture = sink as AtlasTexture
		var scale_factor := sink_extent/256.0
		var front_region := Rect2(0.0,116.0,256.0,140.0)
		var front_rect := Rect2(sink_rect.position+Vector2(0.0,116.0)*scale_factor,front_region.size*scale_factor)
		draw_texture_rect_region(atlas.atlas,front_rect,front_region)

var main: ReefMain
var records: Array[Dictionary] = []
func _initialize() -> void:
	_run.call_deferred()
func _wait(count: int) -> void:
	for _index: int in range(count):
		await process_frame
func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index=0
	event.pressed=pressed
	event.position=at
	Input.parse_input_event(event)
func _capture(ident: String, data: Dictionary) -> void:
	await RenderingServer.frame_post_draw
	var pixels: Image = root.get_texture().get_image()
	var path := OUT+ident+".webp"
	assert(pixels.save_webp(path,true)==OK)
	data["path"] = ident+".webp"
	data["sha256"] = FileAccess.get_sha256(path)
	data["viewport"] = [pixels.get_width(),pixels.get_height()]
	records.append(data)
func _run() -> void:
	Engine.max_fps=30
	assert(DisplayServer.get_name()!="headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT)==OK)
	main=(load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
	main.day_one_active=false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game="level2"
	main.g["phase"]="hall"
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible=false
	main.player.visible=false
	var stars := main.opera_stars
	var sink_atlas := AtlasTexture.new()
	sink_atlas.atlas=ImageTexture.create_from_image(Image.load_from_file(
		"res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png"))
	sink_atlas.region=Rect2(0.0,0.0,256.0,256.0)
	sink_atlas.filter_clip=true
	for width: int in [1280,1600]:
		root.size=Vector2i(width,720)
		DisplayServer.window_set_size(root.size)
		await _wait(4)
		var config: Dictionary={}
		for act: Dictionary in OperaHouse.ACTS:
			if String(act.get("costume",""))=="doctor":
				config=act.duplicate(true)
		assert(not config.is_empty())
		var competition := OperaCompetition.new()
		competition.configure("doctor")
		var world := OperaCareerWorld2D.new()
		main.add_child(world)
		world.setup(main,config,competition,Callable(),[],{}, {})
		await _wait(38)
		var hotspot := world.station_nodes[world.armed_station] as OperaWorldHotspot2D
		var point: Vector2 = hotspot.touch_button.get_global_transform_with_canvas() * (hotspot.touch_button.size*0.5)
		_touch(point,true)
		await _wait(1)
		_touch(point,false)
		for tick: int in range(240):
			if world.task_open:
				break
			await _wait(1)
		assert(world.task_open)
		await _wait(20)
		await _capture("doctor_%d_original"%width,{"variant":"original_after_actual_approach"})
		world.set_process(false)
		world.player_animator.set_process(false)
		world.player_actor.visible=false
		world.action_panel.visible=false
		for station: Control in world.station_nodes:
			station.visible=false
		var canvas := ContactCanvas.new()
		canvas.position=world.player_actor.position
		canvas.size=Vector2(250.0,250.0)
		canvas.mouse_filter=Control.MOUSE_FILTER_IGNORE
		canvas.sink=sink_atlas
		world.root.add_child(canvas)
		for source_index: int in range(SOURCES.size()):
			canvas.character=ImageTexture.create_from_image(Image.load_from_file(SOURCES[source_index]))
			canvas.character_rect=Rect2(25.0,0.0,300.0*1122.0/1402.0,300.0)
			canvas.sink_extent=140.0
			for shift: float in [0.0,-10.0]:
				canvas.sink_offset_y=shift
				for flow: bool in [false,true]:
					canvas.water_on=flow
					canvas.refresh_geometry()
					await _wait(2)
					var ident := "doctor_%d_source%d_sinky%d_water%d"%[width,source_index,int(shift),int(flow)]
					await _capture(ident,{"variant":"static_outward_sink_water_contact","source":SOURCES[source_index],"source_sha256":FileAccess.get_sha256(SOURCES[source_index]),"sink_source":"res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png","sink_source_sha256":FileAccess.get_sha256("res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png"),"sink_region":[0,0,256,256],"sink_extent":canvas.sink_extent,"sink_offset_y":shift,"front_region":[0,116,256,140],"draw_order":"whole_sink_then_water_behind_whole_character_then_short_runoff_then_same_sink_front","actor_position":[canvas.position.x,canvas.position.y],"character_rect":[canvas.character_rect.position.x,canvas.character_rect.position.y,canvas.character_rect.size.x,canvas.character_rect.size.y],"hand_source_landmark":[canvas.hand_source.x,canvas.hand_source.y],"hand_local":[canvas.hand.x,canvas.hand.y],"sink_rect":[canvas.sink_rect.position.x,canvas.sink_rect.position.y,canvas.sink_rect.size.x,canvas.sink_rect.size.y],"water_on":flow,"water_spout_local":[canvas.water_spout.x,canvas.water_spout.y],"soap_contact_local":[canvas.soap_contact.x,canvas.soap_contact.y],"basin_centre_local":[canvas.basin_centre.x,canvas.basin_centre.y],"water_presentation":"Static test-only sparse 2D line from literal spout to upper hand and short runoff into basin; no causal/timed/action acceptance."})
		assert(main.opera_stars==stars and world.phase_progress==0.0)
		world.queue_free()
		await _wait(4)
	assert(records.size()==18)
	var file := FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"STATIC_WATER_CONTACT_PLACEMENTS_CAPTURED","views":records,"qualification":"Actual viewport approach precedes static test-only composition; task input surface and old actor/hotspot overlay are hidden only in this fixture. No production binding, wash progress, temporal continuity, complete action, device/child/owner or cinematic acceptance."},"\t"))
	file.close()
	print("DOCTOR_SINK_WATER_CONTACT|18_CAPTURED|NO_AWARD|REVIEW_PENDING")
	quit(0)
