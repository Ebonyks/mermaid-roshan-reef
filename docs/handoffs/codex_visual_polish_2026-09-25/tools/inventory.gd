extends SceneTree
## Transparency/cut-off audit, capture side (scratch only; never part of the
## project). For one scenario it boots the real game on an isolated save,
## visits castle rooms, saves a full-resolution screenshot per scene and dumps
## every visible textured canvas item with the exact region it samples. Each
## unique sampled region is written out losslessly for the Python analyzer.
##   godot -s inventory.gd -- <scenario>
## scenarios: free, d1_bath, d1_pool, d1_playroom, d1_craft, boss

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a128eb5f-c316-4162-83d1-fbdbf9c3f497/scratchpad/transparency/out"
const CLIPS := ["d1_opening", "d1_castle", "d1_bath_arrival", "d1_bath_clean",
	"d1_pool_arrival", "d1_pool_clean", "d1_eagle_free", "d1_art_arrival",
	"d1_art_clean", "d1_rainbow_route", "d1_puff_arrival",
	"d1_puff_transformation", "d1_epilogue"]
const FREE_ROOMS := ["main_hall", "bubble_bath", "mermaid_pool", "playroom",
	"craft_room", "library", "opera_hall", "kitchen", "dining_room",
	"royal_bedroom", "movie_lounge", "family_gallery", "sleepover_bedroom"]

var main: ReefMain
var scenario := "free"
var regions := {}
var records: Array = []


func _save_doc(path: String, doc: Dictionary) -> void:
	var clips := {}
	for id: String in CLIPS:
		clips[id] = true
	doc["schema_version"] = 1
	doc["save_generation"] = 3
	doc["music"] = false
	doc["day_one_story_clips_seen"] = clips
	doc["day_one_bathroom_entry_movie_handoff_done"] = true
	doc["day_one_bathroom_end_movie_handoff_done"] = true
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify(doc))
	f.close()


func _scenario_doc() -> Dictionary:
	match scenario:
		"free":
			return {"day_one_active": false,
				"day_one_completed_rooms": ["bathroom", "pool", "stuffie", "art"],
				"day_one_giant_dust_bunny_boss_triggered": true,
				"day_one_giant_dust_bunny_boss_defeated": true}
		"d1_bath":
			return {"day_one_active": true, "day_one_completed_rooms": []}
		"d1_pool":
			return {"day_one_active": true, "day_one_completed_rooms": ["bathroom"]}
		"d1_playroom":
			return {"day_one_active": true, "day_one_completed_rooms": ["bathroom", "pool"]}
		"d1_craft":
			return {"day_one_active": true,
				"day_one_completed_rooms": ["bathroom", "pool", "stuffie"],
				"companion_id": "eagle"}
		"boss":
			return {"day_one_active": true,
				"day_one_completed_rooms": ["bathroom", "pool", "stuffie", "art"],
				"companion_id": "eagle"}
	return {}


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		scenario = args[0]
	DirAccess.make_dir_recursive_absolute(OUT + "/regions")
	DirAccess.make_dir_recursive_absolute(OUT + "/shots")
	var path := ProjectSettings.globalize_path("user://transparency_audit_%s.json" % scenario)
	_save_doc(path, _scenario_doc())
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, path)
	get_root().add_child(main)
	for _i in range(20):
		await process_frame
	main._start_menu_ref()._dismiss_menu()
	var day_one: bool = scenario != "free"
	main._launch_from_start_menu(day_one)
	await create_timer(2.0).timeout
	if scenario == "boss":
		main._enter_castle_interior_now()
		await create_timer(2.0).timeout
		main._day_one_trigger_boss()
		await create_timer(9.0).timeout
		await _scene("boss_arena")
	elif scenario == "free":
		main._enter_castle_interior_now()
		await create_timer(2.0).timeout
		for room: String in FREE_ROOMS:
			main._castle_rooms_ref().show_room(room, false)
			await create_timer(2.6).timeout
			await _scene("free_" + room)
	else:
		main._enter_castle_interior_now()
		await create_timer(2.0).timeout
		var room: String = main.day_one_castle_room_for_current()
		main._castle_rooms_ref().show_room(room, false)
		await create_timer(4.0).timeout
		await _scene(scenario + "_" + room)
	var f := FileAccess.open(OUT + "/inventory_%s.json" % scenario, FileAccess.WRITE)
	f.store_string(JSON.stringify({"scenario": scenario, "records": records}, "\t"))
	f.close()
	for s in ["", ".bak", ".tmp", ".old"]:
		if FileAccess.file_exists(path + s):
			DirAccess.remove_absolute(path + s)
	print("INVENTORY_DONE ", scenario, " records=", records.size(), " regions=", regions.size())
	quit(0)


func _scene(name: String) -> void:
	await RenderingServer.frame_post_draw
	var shot := get_root().get_texture().get_image()
	shot.save_png(OUT + "/shots/%s.png" % name)
	var to_window: Transform2D = get_root().get_final_transform()
	var count_before := records.size()
	_walk(main, name, to_window)
	print("SCENE ", name, " room=", main.castle_room_id, " items=", records.size() - count_before, " shot=", shot.get_size())


func _walk(node: Node, scene_name: String, to_window: Transform2D) -> void:
	for child in node.get_children():
		if child is CanvasLayer and not (child as CanvasLayer).visible:
			continue
		if child is CanvasItem:
			var ci := child as CanvasItem
			if not ci.is_visible_in_tree():
				continue
			_record(ci, scene_name, to_window)
		_walk(child, scene_name, to_window)


func _record(ci: CanvasItem, scene_name: String, to_window: Transform2D) -> void:
	var tex: Texture2D = null
	var local_rect := Rect2()
	var extra := {}
	if ci is Sprite2D:
		var s := ci as Sprite2D
		tex = s.texture
		if tex == null:
			return
		local_rect = s.get_rect()
		extra = {"region_enabled": s.region_enabled, "region_rect": _r(s.region_rect),
			"hframes": s.hframes, "vframes": s.vframes, "frame": s.frame,
			"flip_h": s.flip_h, "flip_v": s.flip_v}
	elif ci is AnimatedSprite2D:
		var a := ci as AnimatedSprite2D
		if a.sprite_frames == null:
			return
		tex = a.sprite_frames.get_frame_texture(a.animation, a.frame)
		if tex == null:
			return
		var size := tex.get_size()
		var offset := a.offset - (size * 0.5 if a.centered else Vector2.ZERO)
		local_rect = Rect2(offset, size)
		extra = {"animation": String(a.animation), "anim_frame": a.frame, "flip_h": a.flip_h}
	elif ci is TextureRect:
		var t := ci as TextureRect
		tex = t.texture
		if tex == null:
			return
		local_rect = Rect2(Vector2.ZERO, t.size)
		extra = {"stretch_mode": t.stretch_mode, "expand_mode": t.expand_mode}
	elif ci is TextureButton:
		var b := ci as TextureButton
		tex = b.texture_normal
		if tex == null:
			return
		local_rect = Rect2(Vector2.ZERO, b.size)
		extra = {"stretch_mode": b.stretch_mode, "ignore_texture_size": b.ignore_texture_size,
			"flip_h": b.flip_h}
	elif ci is NinePatchRect:
		var np := ci as NinePatchRect
		tex = np.texture
		if tex == null:
			return
		local_rect = Rect2(Vector2.ZERO, np.size)
		extra = {"nine_patch": true}
	else:
		return
	var sample := _sample_rect(ci, tex)
	var atlas_path: String = sample["path"]
	var key := "%s|%s" % [atlas_path, str(sample["rect"])]
	if not regions.has(key):
		regions[key] = _save_region(tex, sample, key)
	var xf: Transform2D = to_window * ci.get_global_transform_with_canvas()
	var win_rect := _bounds(xf, local_rect)
	var mat_path := ""
	if ci.material is ShaderMaterial and (ci.material as ShaderMaterial).shader != null:
		mat_path = (ci.material as ShaderMaterial).shader.resource_path
	records.append({
		"scene": scene_name,
		"node": String(ci.get_path()),
		"class": ci.get_class(),
		"texture": atlas_path,
		"sample_rect": sample["rect"],
		"region_file": regions[key],
		"window_rect": _r(win_rect),
		"z": ci.z_index,
		"modulate_a": ci.modulate.a * ci.self_modulate.a,
		"material": mat_path,
		"meta_role": String(ci.get_meta("source_asset_role", "")),
		"extra": extra,
	})


func _sample_rect(ci: CanvasItem, tex: Texture2D) -> Dictionary:
	# Resolve AtlasTexture wrappers and Sprite2D region/frames to one rect in
	# the underlying image.
	var base_tex: Texture2D = tex
	var rect := Rect2(Vector2.ZERO, tex.get_size())
	if tex is AtlasTexture:
		var at := tex as AtlasTexture
		base_tex = at.atlas
		rect = at.region
	if ci is Sprite2D:
		var s := ci as Sprite2D
		if s.region_enabled:
			rect = Rect2(rect.position + s.region_rect.position, s.region_rect.size)
		if s.hframes > 1 or s.vframes > 1:
			var cell := rect.size / Vector2(s.hframes, s.vframes)
			var coords := Vector2(s.frame % s.hframes, s.frame / s.hframes)
			rect = Rect2(rect.position + coords * cell, cell)
	var path := base_tex.resource_path if base_tex != null else ""
	if path == "":
		path = "generated:%s#%d" % [base_tex.get_class() if base_tex != null else "null", base_tex.get_instance_id() if base_tex != null else 0]
	return {"path": path, "rect": _r(rect), "tex": base_tex}


func _save_region(tex: Texture2D, sample: Dictionary, key: String) -> String:
	var base_tex: Texture2D = sample["tex"]
	if base_tex == null:
		return ""
	var img: Image = base_tex.get_image()
	if img == null:
		return ""
	if img.is_compressed():
		img.decompress()
	img.convert(Image.FORMAT_RGBA8)
	var r: Array = sample["rect"]
	var rect := Rect2i(int(round(r[0])), int(round(r[1])), int(round(r[2])), int(round(r[3])))
	rect = rect.intersection(Rect2i(Vector2i.ZERO, img.get_size()))
	if rect.size.x <= 0 or rect.size.y <= 0:
		return ""
	var sub := img.get_region(rect)
	var file_name := key.md5_text() + ".png"
	sub.save_png(OUT + "/regions/" + file_name)
	return file_name


func _bounds(xf: Transform2D, r: Rect2) -> Rect2:
	var pts := [xf * r.position, xf * Vector2(r.end.x, r.position.y),
		xf * r.end, xf * Vector2(r.position.x, r.end.y)]
	var mn: Vector2 = pts[0]
	var mx: Vector2 = pts[0]
	for p: Vector2 in pts:
		mn = mn.min(p)
		mx = mx.max(p)
	return Rect2(mn, mx - mn)


func _r(r: Rect2) -> Array:
	return [snappedf(r.position.x, 0.01), snappedf(r.position.y, 0.01),
		snappedf(r.size.x, 0.01), snappedf(r.size.y, 0.01)]
