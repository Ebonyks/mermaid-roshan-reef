extends "res://scripts/probe_l2_living_cards.gd"
func _frames(count: int) -> void:
	await super._frames(count)
	if main != null and main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
		await process_frame
		await process_frame

var perf_rows: Array[Dictionary] = []
func collect_textures(node: Node, textures: Dictionary) -> void:
	if node is Sprite2D:
		var sprite: Sprite2D = node as Sprite2D
		if sprite.texture != null:
			var texture: Texture2D = sprite.texture
			textures[texture.get_instance_id()] = {"path": texture.resource_path, "width": texture.get_width(), "height": texture.get_height(), "uncompressed_rgba_bytes": texture.get_width() * texture.get_height() * 4}
	for child: Node in node.get_children():
		collect_textures(child, textures)
func sample_view(label: String) -> void:
	for k: int in range(20):
		await process_frame
	var times: Array[float] = []
	var calls: Array[float] = []
	var last: int = Time.get_ticks_usec()
	for k: int in range(120):
		await process_frame
		await RenderingServer.frame_post_draw
		var now: int = Time.get_ticks_usec()
		times.append(float(now-last)/1000.0)
		last = now
		calls.append(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	times.sort()
	calls.sort()
	var textures: Dictionary = {}
	collect_textures(promenade.canvas_root(), textures)
	var bytes: int = 0
	for value: Variant in textures.values():
		bytes += int((value as Dictionary)["uncompressed_rgba_bytes"])
	perf_rows.append({"view": label, "samples": times.size(), "wall_frame_ms_median": times[60], "wall_frame_ms_p95": times[113], "draw_calls_median": calls[60], "global_texture_bytes": Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED), "bound_unique_textures": textures.size(), "bound_texture_uncompressed_rgba_bytes": bytes, "textures": textures.values()})
	var file := FileAccess.open(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join("PERFORMANCE.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"status": "DESKTOP_DIAGNOSTIC_NOT_DEVICE_ACCEPTANCE", "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "preview": OS.get_cmdline_user_args().has("--sky-lagoon-whole-scene-preview"), "limits": "Offscreen desktop window timing includes CPU, GPU synchronization and OS scheduling. Raw bound texture estimate excludes mipmaps, compression, cached rollback resources and non-Sprite2D consumers. Global texture memory is engine-wide, not attributable only to this stage.", "views": perf_rows}, "\t"))
	file.close()
func _capture(name: String) -> void:
	await super._capture(name)
	if name in ["canvas_screen_1_day", "canvas_screen_2_day", "canvas_screen_3_day"]:
		await sample_view(name)
	if name == "canvas_screen_3_night":
		var route: float = promenade.master_route_x()
		for page: int in range(3):
			promenade.set_master_route_x(float(page)*2048.0+1024.0)
			promenade._apply_view_transform(true)
			await sample_view("screen_%d_night" % (page+1))
		promenade.set_master_route_x(route)
		promenade._apply_view_transform(true)


func _prime_idle_event(director: LivingWorldDirector) -> void:
	# GPU mode deliberately cannot use the headless-only force helper.
	# Advance the ordinary idle clock in bounded steps without mutating state.
	var spec: Dictionary = main.living_specs[main.living_stage_id]
	var idle: Dictionary = spec["idle_event"]
	var steps: int = ceili(float(idle["delay"]) / 0.1) + 2
	for _step: int in range(steps):
		director.tick(0.1)
		if main.living_event_time >= 0.0:
			break
