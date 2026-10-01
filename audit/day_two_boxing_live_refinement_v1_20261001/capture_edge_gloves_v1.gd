extends SceneTree
## Actual local-handler boundary drags, no production input or geometry override.
const OUT := "res://audit/day_two_boxing_live_refinement_v1_20261001/native_edges_v1/"
var main: ReefMain
var views: Array[Dictionary] = []
func _initialize() -> void:
	_run.call_deferred()
func _frames(n: int) -> void:
	for _i: int in range(n):
		await process_frame
func _run() -> void:
	Engine.max_fps = 60
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	var config: Dictionary = {}
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume", "")) == "boxer":
			config = act.duplicate(true)
	for width: int in [1280,1600]:
		root.size = Vector2i(width,720)
		DisplayServer.window_set_size(root.size)
		await _frames(6)
		var competition: OperaCompetition = OperaCompetition.new()
		competition.configure("boxer")
		var world: OperaCareerWorld2D = OperaCareerWorld2D.new()
		main.add_child(world)
		world.setup(main,config,competition,Callable())
		await _frames(6)
		world.set_process(false)
		var jab: int = -1
		for i: int in range(world.phases.size()):
			if String(world.phases[i].get("mode", "")) == "boxing_jab":
				jab = i
		assert(jab >= 0)
		for hand: int in [0,1]:
			for corner: int in range(4):
				world.phase_index = jab
				world.phase_advance_pending = false
				world.reveal_t = 0.0
				world._arm_phase()
				world._open_task()
				await _frames(6)
				var surface: OperaBoxingSurface = world.surface as OperaBoxingSurface
				var at: Vector2 = Vector2(0.0 if corner % 2 == 0 else surface.size.x,0.0 if corner < 2 else surface.size.y)
				var touch: InputEventScreenTouch = InputEventScreenTouch.new()
				touch.pressed = true
				touch.index = 0
				touch.position = surface.glove_rest_position(hand)
				surface._gui_input(touch)
				assert(int(surface.touch_owners.get(0,-1))==hand)
				var drag: InputEventScreenDrag = InputEventScreenDrag.new()
				drag.index = 0
				drag.position = at
				surface._gui_input(drag)
				await _frames(2)
				await RenderingServer.frame_post_draw
				var texture: Texture2D = surface._left_glove_texture if hand==0 else surface._right_glove_texture
				var image: Image = texture.get_image()
				var used: Rect2i = image.get_used_rect()
				var fraction: float = 164.0 / float(image.get_width())
				var rect: Rect2 = Rect2(Vector2(used.position)*fraction+Vector2(-82.0,-91.0),Vector2(used.size)*fraction)
				var pos: Vector2 = surface.glove_positions[hand]
				var scale_value: float = 0.92+surface._glove_depth(hand)*0.38
				var angle: float = (-0.08 if hand==0 else 0.08)+clampf((surface.pointer_pos.x-pos.x)/maxf(1.0,surface.size.x),-0.08,0.08)
				var bounds: Rect2 = Rect2(pos+rect.position.rotated(angle)*scale_value,Vector2.ZERO)
				for point: Vector2 in [rect.position,rect.position+Vector2(rect.size.x,0.0),rect.position+rect.size,rect.position+Vector2(0.0,rect.size.y)]:
					bounds = bounds.expand(pos+point.rotated(angle)*scale_value)
				var inside: bool = Rect2(Vector2.ZERO,surface.size).encloses(bounds)
				var path: String = "%d_hand%d_corner%d.webp" % [width,hand,corner]
				assert(root.get_texture().get_image().save_webp(OUT+path,true)==OK)
				assert(surface.landed_punches==0 and world.phase_progress==0.0)
				views.append({"path":path,"sha256":FileAccess.get_sha256(OUT+path),"width":width,"hand":hand,"corner":corner,"glove_position":[pos.x,pos.y],"draw_scale":scale_value,"draw_angle":angle,"painted_nonzero_alpha_local_bounds":[bounds.position.x,bounds.position.y,bounds.size.x,bounds.size.y],"inside_action_surface":inside,"hits":surface.landed_punches,"progress":world.phase_progress})
				touch.pressed = false
				touch.position = at
				surface._gui_input(touch)
				assert(surface.touch_owners.is_empty())
		world.close()
		world.queue_free()
		await _frames(4)
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"CURRENT_ACTUAL_LOCAL_HANDLER_16_BOUNDARY_DRAGS","views":views,"qualification":"Boundary geometry and complete native rendered fixtures; no manually placed gloves, progress or texture overrides. A rectangle around nonzero-alpha pixels is conservative, not a per-pixel screen-clip test."},"\t")+"\n")
	file.close()
	main.queue_free()
	await _frames(3)
	print("BOXING_EDGE|16 cases|"+str(views.filter(func(v: Dictionary) -> bool: return bool(v["inside_action_surface"])).size())+" enclosed")
	quit(0)
